"""Bounded, unsliced Bambu Studio project export. SPDX-License-Identifier: MIT.

Project layout/preset binding adapted from Wilson Waters' MIT writer; see
third_party/bambu_project/NOTICE.md. No slicer or printer is invoked.
"""

import argparse
from collections import Counter
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import re
import uuid
import xml.etree.ElementTree as ET
import zipfile

from tools.geometry import decode_stl, validate_mesh

PRINTER = "Bambu Lab P2S 0.4 nozzle"
PROCESS = "0.20mm Standard @BBL P2S"
FILAMENT = "Bambu PLA Basic @BBL P2S"
PLATE = "Textured PEI Plate"
EXTRUDER = "Direct Drive Standard"
STUDIO_VERSION = "02.09.02.62"
CORE = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
PRODUCTION = "http://schemas.microsoft.com/3dmanufacturing/production/2015/06"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
MODEL_REL = "http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"
TYPES = "http://schemas.openxmlformats.org/package/2006/content-types"
IDENTITY = "1 0 0 0 1 0 0 0 1 0 0 0"
MAX_BYTES = 64 * 1024 * 1024
OVERRIDES = {
    "layer_height": (0.08, 0.28, False),
    "wall_loops": (1, 8, True),
    "top_shell_layers": (1, 12, True),
    "bottom_shell_layers": (1, 12, True),
    "sparse_infill_density": (0, 50, False),
}
ENUM_OVERRIDES = {
    "sparse_infill_pattern": {"grid", "gyroid", "rectilinear"},
    "enable_support": {"0"},
    "brim_type": {"no_brim"},
}


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def _json(data):
    return (json.dumps(data, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def _load_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def bad_constant(value):
        raise ValueError(f"Non-finite JSON value: {value}")

    result = json.loads(data, object_pairs_hook=pairs, parse_constant=bad_constant)
    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object")
    return result


def _read(path):
    path = Path(path)
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Input exceeds the 64 MiB bound")
    return path.read_bytes()


def _profile_name(name):
    if (not isinstance(name, str) or not name or len(name) > 180
            or any(c in name for c in '/\\:*?"<>|\r\n') or name in {".", ".."}):
        raise ValueError("Expected an exact safe preset name, not a path or alias")
    return name


def resolve_profile(profiles_dir, kind, name):
    """Resolve a flat official BBL JSON chain and includes; retain byte hashes.

    Only the explicit type directory is searched. Duplicate names, missing
    parents/includes, cycles and path escapes are errors, never first-hit wins.
    This is not an evaluator for arbitrary third-party conditional presets.
    """
    if kind not in {"machine", "process", "filament"}:
        raise ValueError("Unsupported preset type")
    root = Path(profiles_dir).resolve(strict=True)
    directory = root / kind
    records = {}
    paths = {}
    for path in directory.rglob("*.json"):
        paths.setdefault(path.stem, []).append(path)

    def resolve(current, stack=()):
        _profile_name(current)
        if current in stack or len(stack) > 32:
            raise ValueError(f"Preset dependency cycle/depth: {current}")
        matches = paths.get(current, [])
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one {kind} preset: {current}; found {len(matches)}")
        path = matches[0]
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError("Preset path escapes the supplied root")
        raw = _read(path)
        data = _load_json(raw)
        if data.get("name") != current or data.get("type", kind) != kind:
            raise ValueError(f"Preset identity/type mismatch: {current}")
        if data.get("from", "system") != "system":
            raise ValueError("Only official system-preset inputs are supported")
        records[path.relative_to(root).as_posix()] = _hash(raw)
        chain = (*stack, current)
        parent = data.get("inherits")
        merged = resolve(parent, chain) if parent else {}
        includes = data.get("include", [])
        if (not isinstance(includes, list) or not all(isinstance(v, str) for v in includes)
                or len(includes) != len(set(includes))):
            raise ValueError("Invalid preset include list")
        for dependency in includes:
            merged.update(resolve(dependency, chain))
        merged.update(data)
        return merged

    effective = resolve(name)
    if effective.get("instantiation") != "true" or effective.get("from") != "system":
        raise ValueError("Selected preset is not an instantiable system preset")
    return effective, [
        {"path": path, "sha256": digest} for path, digest in sorted(records.items())
    ]


def _number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError(f"{label} must be a finite number")
    try:
        result = float(value)
    except (ValueError, OverflowError) as exc:
        raise ValueError(f"{label} must be a finite number") from exc
    if not math.isfinite(result):
        raise ValueError(f"{label} must be a finite number")
    return result


def _overrides(values, process):
    if not isinstance(values, dict):
        raise ValueError("Overrides must be a dictionary of explicitly chosen process settings")
    result = {}
    for key, value in values.items():
        if key in process and not isinstance(process[key], str):
            raise ValueError(f"Override has no supported scalar preset baseline: {key}")
        if key in OVERRIDES:
            is_percent = key == "sparse_infill_density"
            raw = value[:-1] if is_percent and isinstance(value, str) and value.endswith("%") else value
            number = _number(raw, key)
            low, high, integer = OVERRIDES[key]
            if not low <= number <= high or (integer and not number.is_integer()):
                raise ValueError(f"{key} must be {'an integer ' if integer else ''}between {low} and {high}")
            result[key] = format(number, ".15g") + ("%" if is_percent else "")
        elif key in ENUM_OVERRIDES and isinstance(value, str) and value in ENUM_OVERRIDES[key]:
            result[key] = value
        else:
            raise ValueError(f"Unsupported override: {key}")
    return result


def _settings(profiles_dir, studio_version, printer, process, filament, plate,
              nozzle_mm, extruder_variant, overrides):
    if (studio_version != STUDIO_VERSION or printer != PRINTER or process != PROCESS
            or filament != FILAMENT or plate != PLATE
            or _number(nozzle_mm, "nozzle") != 0.4 or extruder_variant != EXTRUDER):
        raise ValueError("Unsupported setup; see supported_setup() for the exact bounded combination")
    profiles, sources = {}, {}
    for kind, name in (("machine", printer), ("process", process), ("filament", filament)):
        profiles[kind], sources[kind] = resolve_profile(profiles_dir, kind, name)
    machine, proc, fil = (profiles[k] for k in ("machine", "process", "filament"))
    required = {
        "printer_model": "Bambu Lab P2S", "printer_variant": "0.4",
        "nozzle_diameter": ["0.4"], "printable_height": "256",
        "printable_area": ["0x0", "256x0", "256x256", "0x256"], "bed_exclude_area": [],
        "extruder_type": ["Direct Drive"], "default_nozzle_volume_type": ["Standard"],
    }
    if any(machine.get(key) != value for key, value in required.items()):
        raise ValueError("P2S machine geometry/nozzle differs from the supported contract")
    for profile in (proc, fil):
        if profile.get("compatible_printers") != [printer]:
            raise ValueError("Preset compatibility must explicitly name only the selected P2S")
        if profile.get("compatible_printers_condition") not in (None, ""):
            raise ValueError("Conditional compatibility is unsupported")
    if (fil.get("filament_type") != ["PLA"] or not fil.get("filament_id")
            or EXTRUDER not in proc.get("print_extruder_variant", [])
            or EXTRUDER not in fil.get("filament_extruder_variant", [])):
        raise ValueError("Material/extruder identity differs from the supported contract")
    for key in ("textured_plate_temp", "textured_plate_temp_initial_layer"):
        values = fil.get(key)
        if not isinstance(values, list) or not values or any(not 0 < _number(v, key) <= 100 for v in values):
            raise ValueError("Missing or invalid selected-plate filament temperatures")
    effective_overrides = _overrides(overrides, proc)
    process_values = {}
    for key in OVERRIDES.keys() | ENUM_OVERRIDES.keys():
        if key not in proc and key in effective_overrides:
            continue
        if not isinstance(proc.get(key), str):
            raise ValueError(f"Missing supported process setting: {key}")
        process_values[key] = proc[key]
    cfg = {
        "from": "project", "name": "project_settings", "version": studio_version,
        "printer_settings_id": printer, "print_settings_id": process,
        "filament_settings_id": [filament], "filament_ids": [fil["filament_id"]],
        "filament_type": ["PLA"], "curr_bed_type": plate,
        **required, "nozzle_volume_type": ["Standard"], **process_values, **effective_overrides,
        "different_settings_to_system": [
            ";".join(sorted(k for k, v in effective_overrides.items() if v != proc.get(k))), "", "",
        ],
    }
    # Bind trusted installed presets, not copied machine/filament G-code.
    provenance = {
        "files": sources, "resolved_sha256": {kind: _hash(_json(p)) for kind, p in profiles.items()},
        "overrides": effective_overrides, "extruder_variant": extruder_variant,
        "binding": "named installed system presets; not self-contained",
    }
    return cfg, provenance


def supported_setup():
    """Return an export contract, not a claim of slicing or physical validation."""
    return {
        "status": "experimental; recorded native round-trip/slice passed, complete layer review pending",
        "studio_version": STUDIO_VERSION, "printer": PRINTER, "process": PROCESS,
        "filament": FILAMENT, "plate": PLATE, "nozzle_mm": 0.4,
        "extruder_variant": EXTRUDER, "units": "mm", "objects": 1, "filaments": 1,
        "overrides": sorted(OVERRIDES.keys() | ENUM_OVERRIDES.keys()),
        "slicing": "not performed by this exporter; separate local application review required",
    }


def _passport(raw, stl):
    report = _load_json(raw)
    passport = report.get("passport", {})
    if not isinstance(passport, dict) or not isinstance(passport.get("editable_source", {}), dict):
        raise ValueError("Invalid passport/source object")
    digest = _hash(stl)
    if (report.get("units") != "mm" or report.get("sha256") != digest
            or passport.get("schema_version") != 1):
        raise ValueError("Expected a millimeter OpenPrintLab v1 passport bound to this STL")
    for value in (passport.get("variant_id"), passport.get("editable_source", {}).get("recipe_sha256")):
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError("Passport is missing a variant/source identity")
    if not re.fullmatch(r"\d+\.\d+\.\d+", passport.get("model_version", "")):
        raise ValueError("Passport model version is missing")
    if report.get("evidence", {}).get("scope") != {
        "model_version": passport["model_version"], "variant_id": passport["variant_id"], "stl_sha256": digest,
    }:
        raise ValueError("Passport evidence scope differs from the source identity")
    if report.get("validation", {}).get("software_checked") is not True:
        raise ValueError("Source passport has no passed software check")
    return report


def _xml(root):
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _model():
    return ET.Element("model", {
        "unit": "millimeter", "xml:lang": "en-US", "xmlns": CORE,
        "xmlns:p": PRODUCTION, "requiredextensions": "p",
        "xmlns:BambuStudio": "http://schemas.bambulab.com/package/2021",
    })


def _relationships(target):
    root = ET.Element("Relationships", xmlns=REL)
    ET.SubElement(root, "Relationship", Target=target, Id="rel-1", Type=MODEL_REL)
    return _xml(root)


def _parts(triangles, cfg, translation, name, identity):
    def uid(label):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, identity + ":" + label))

    root, mesh_model = _model(), _model()
    for model in (root, mesh_model):
        ET.SubElement(model, "metadata", name="BambuStudio:3mfVersion").text = "1"
    ET.SubElement(root, "metadata", name="Application").text = "BambuStudio-" + cfg["version"]
    ET.SubElement(root, "metadata", name="Description").text = "OpenPrintLab unsliced candidate; not print-tested"
    obj = ET.SubElement(ET.SubElement(mesh_model, "resources"), "object",
                        {"id": "1", "type": "model", "p:UUID": uid("mesh")})
    mesh = ET.SubElement(obj, "mesh")
    vertices, faces = ET.SubElement(mesh, "vertices"), ET.SubElement(mesh, "triangles")
    index = {}
    for triangle in triangles:
        ids = []
        for point in triangle:
            if point not in index:
                index[point] = len(index)
                ET.SubElement(vertices, "vertex", dict(zip(("x", "y", "z"), (repr(v) for v in point))))
            ids.append(index[point])
        ET.SubElement(faces, "triangle", {f"v{i + 1}": str(v) for i, v in enumerate(ids)})
    ET.SubElement(mesh_model, "build")
    container = ET.SubElement(ET.SubElement(root, "resources"), "object",
                              {"id": "2", "type": "model", "p:UUID": uid("object")})
    ET.SubElement(ET.SubElement(container, "components"), "component", {
        "p:path": "/3D/Objects/object_1.model", "objectid": "1",
        "p:UUID": uid("component"), "transform": IDENTITY,
    })
    build = ET.SubElement(root, "build", {"p:UUID": uid("build")})
    ET.SubElement(build, "item", {
        "objectid": "2", "p:UUID": uid("item"), "printable": "1",
        "transform": "1 0 0 0 1 0 0 0 1 " + " ".join(repr(v) for v in translation),
    })
    settings = ET.Element("config")
    obj = ET.SubElement(settings, "object", id="2")
    ET.SubElement(obj, "metadata", key="name", value=name)
    ET.SubElement(obj, "metadata", key="extruder", value="1")
    ET.SubElement(obj, "metadata", face_count=str(len(triangles)))
    part = ET.SubElement(obj, "part", id="1", subtype="normal_part")
    for key, value in {
        "name": name, "matrix": "1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1",
        "source_file": "source.stl", "source_object_id": "0", "source_volume_id": "0",
    }.items():
        ET.SubElement(part, "metadata", key=key, value=value)
    ET.SubElement(part, "mesh_stat", face_count=str(len(triangles)), edges_fixed="0",
                  degenerate_facets="0", facets_removed="0", facets_reversed="0", backwards_edges="0")
    plate = ET.SubElement(settings, "plate")
    for key, value in (("plater_id", "1"), ("plater_name", ""), ("locked", "false")):
        ET.SubElement(plate, "metadata", key=key, value=value)
    instance = ET.SubElement(plate, "model_instance")
    ET.SubElement(instance, "metadata", key="object_id", value="2")
    ET.SubElement(instance, "metadata", key="instance_id", value="0")
    types = ET.Element("Types", xmlns=TYPES)
    for extension, content in {
        "rels": "application/vnd.openxmlformats-package.relationships+xml",
        "model": "application/vnd.ms-package.3dmanufacturing-3dmodel+xml",
        "config": "application/octet-stream", "json": "application/json", "stl": "application/sla",
    }.items():
        ET.SubElement(types, "Default", Extension=extension, ContentType=content)
    return {
        "[Content_Types].xml": _xml(types), "_rels/.rels": _relationships("/3D/3dmodel.model"),
        "3D/_rels/3dmodel.model.rels": _relationships("/3D/Objects/object_1.model"),
        "3D/3dmodel.model": _xml(root), "3D/Objects/object_1.model": _xml(mesh_model),
        "Metadata/model_settings.config": _xml(settings),
        "Metadata/project_settings.config": _json(cfg),
    }


def export_project(stl_path, report_path, output_path, *, profiles_dir, studio_version,
                   printer, process, filament, plate, nozzle_mm, extruder_variant,
                   translation_xy, overrides=None):
    """Write one new unsliced project; originals and passports are never edited.

    translation_xy is an explicit XY translation in mm, NOT a scale, rotation
    or automatic recenter. The existing Z=0 orientation is preserved.
    """
    output = Path(output_path)
    if output.suffix.lower() != ".3mf" or output.name.lower().endswith(".gcode.3mf"):
        raise ValueError("Output must be an unsliced .3mf path, not .gcode.3mf")
    if output.exists() or output.is_symlink():
        raise FileExistsError("Project already exists; choose a new output name")
    stl, raw_report = _read(stl_path), _read(report_path)
    report = _passport(raw_report, stl)
    triangles = decode_stl(stl)
    checks = validate_mesh(triangles)
    if checks["dimensions_mm"] != report.get("checks", {}).get("dimensions_mm"):
        raise ValueError("Passport dimensions differ from the actual STL")
    cfg, profiles = _settings(profiles_dir, studio_version, printer, process, filament,
                             plate, nozzle_mm, extruder_variant, {} if overrides is None else overrides)
    if not isinstance(translation_xy, (tuple, list)) or len(translation_xy) != 2:
        raise ValueError("Explicit translation_xy must have two finite mm values")
    translation = [_number(v, "translation") for v in translation_xy] + [0.0]
    vertices = {p for t in triangles for p in t}
    for i in (0, 1):
        if min(p[i] for p in vertices) + translation[i] < 8 or max(p[i] for p in vertices) + translation[i] > 248:
            raise ValueError("Placement must retain 8 mm clearance inside the P2S bed; no automatic rescale")
    manifest = {
        "schema_version": 1, "exporter": "openprintlab.bambu_project.v1", "units": "mm",
        "source_stl_sha256": _hash(stl), "source_report_sha256": _hash(raw_report),
        "passport": report["passport"], "checks": checks, "translation_mm": translation,
        "profiles": profiles, "setup": supported_setup(), "settings": cfg,
        "validation": {"software_checked": True, "app_open_verified": False,
                       "slicer_checked": False, "physical_print_tested": False},
        "limitations": [
            "Named system presets must exist and match these hashes on the opening installation.",
            "This is not a self-contained profile bundle; a different installation can bind different defaults.",
            "No geometry repair, model scaling, slicing, printer connection or print operation was performed.",
            "Original passport evidence is historical source evidence, not validation of this project.",
        ],
    }
    parts = _parts(triangles, cfg, translation, "OpenPrintLab candidate", _hash(_json(manifest)))
    parts["Metadata/openprintlab/source.stl"] = stl
    parts["Metadata/openprintlab/source.report.json"] = raw_report
    manifest["members_sha256"] = {name: _hash(data) for name, data in parts.items()}
    parts["Metadata/openprintlab/manifest.json"] = _json(manifest)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(parts.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    payload = buffer.getvalue()
    inspect_project(io.BytesIO(payload))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as handle:
        try:
            handle.write(payload)
        except OSError:
            handle.close()
            output.unlink()
            raise
    return {"path": str(output.resolve()), "sha256": _hash(payload), "manifest": manifest}


def _archive(path):
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            names = [i.filename for i in infos]
            if len(names) != len(set(names)) or len(names) > 100:
                raise ValueError("Duplicate or excessive archive members")
            if sum(i.file_size for i in infos) > MAX_BYTES:
                raise ValueError("Project exceeds the 64 MiB expanded bound")
            for name in names:
                if (PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts
                        or "\\" in name or name.lower().endswith((".gcode", ".gcode.3mf"))):
                    raise ValueError("Unsafe path or sliced G-code member")
            return {name: archive.read(name) for name in names}
    except zipfile.BadZipFile as exc:
        raise ValueError("Invalid project ZIP") from exc


def _parse_xml(data):
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ValueError("XML declarations/entities are unsupported")
    return ET.fromstring(data)


def _mesh_and_transform(parts):
    """Read only the single-object/component layout this writer and Studio save."""
    root = _parse_xml(parts["3D/3dmodel.model"])
    if root.get("unit") != "millimeter":
        raise ValueError("Project units must be millimeter")
    objects = root.findall(f"{{{CORE}}}resources/{{{CORE}}}object")
    items = root.findall(f"{{{CORE}}}build/{{{CORE}}}item")
    if (len(objects) != 1 or len(items) != 1 or items[0].get("objectid") != objects[0].get("id")
            or items[0].get("printable", "1") != "1"):
        raise ValueError("Expected exactly one built object")
    components = objects[0].findall(f"{{{CORE}}}components/{{{CORE}}}component")
    if len(components) != 1:
        raise ValueError("Expected one component")
    component = components[0]
    name = component.get(f"{{{PRODUCTION}}}path", "").lstrip("/")
    if name not in parts:
        raise ValueError("Missing component model")
    leaf = _parse_xml(parts[name])
    if leaf.get("unit") != "millimeter":
        raise ValueError("Component units must be millimeter")
    meshes = leaf.findall(f"{{{CORE}}}resources/{{{CORE}}}object")
    if len(meshes) != 1 or meshes[0].get("id") != component.get("objectid"):
        raise ValueError("Expected exactly one referenced mesh")
    vertices = [
        tuple(_number(v.get(k), "vertex") for k in ("x", "y", "z"))
        for v in meshes[0].findall(f"{{{CORE}}}mesh/{{{CORE}}}vertices/{{{CORE}}}vertex")
    ]
    triangles = []
    for face in meshes[0].findall(f"{{{CORE}}}mesh/{{{CORE}}}triangles/{{{CORE}}}triangle"):
        indices = [int(face.get(k)) for k in ("v1", "v2", "v3")]
        if min(indices) < 0 or max(indices) >= len(vertices):
            raise ValueError("Triangle index out of range")
        triangles.append(tuple(vertices[i] for i in indices))
    transforms = []
    for node in (component, items[0]):
        values = [_number(v, "transform") for v in node.get("transform", IDENTITY).split()]
        if len(values) != 12:
            raise ValueError("Invalid 3MF transform")
        transforms.append(values)
    return triangles, transforms


def _placed(triangles, transforms):
    for matrix in transforms:
        triangles = [
            tuple(tuple(sum(p[j] * matrix[j * 3 + i] for j in range(3)) + matrix[9 + i]
                        for i in range(3)) for p in t) for t in triangles
        ]
    return triangles


def inspect_project(path):
    """Check our export's package/fidelity; this does NOT open or slice in Studio."""
    parts = _archive(path)
    manifest = _load_json(parts["Metadata/openprintlab/manifest.json"])
    expected = manifest["members_sha256"]
    if set(parts) != set(expected) | {"Metadata/openprintlab/manifest.json"}:
        raise ValueError("Unexpected/missing project members")
    if any(_hash(parts[n]) != digest for n, digest in expected.items()):
        raise ValueError("Project member hash mismatch")
    for relfile, target in (
        ("_rels/.rels", "/3D/3dmodel.model"),
        ("3D/_rels/3dmodel.model.rels", "/3D/Objects/object_1.model"),
    ):
        rels = _parse_xml(parts[relfile]).findall(f"{{{REL}}}Relationship")
        if len(rels) != 1 or rels[0].get("Target") != target or rels[0].get("Type") != MODEL_REL:
            raise ValueError("Invalid model package relationship")
    types = _parse_xml(parts["[Content_Types].xml"])
    extensions = {e.get("Extension"): e.get("ContentType") for e in types.findall(f"{{{TYPES}}}Default")}
    if (extensions.get("model") != "application/vnd.ms-package.3dmanufacturing-3dmodel+xml"
            or extensions.get("rels") != "application/vnd.openxmlformats-package.relationships+xml"
            or not {"config", "json", "stl"} <= extensions.keys()):
        raise ValueError("Missing/invalid package content types")
    uuids = []
    for name in ("3D/3dmodel.model", "3D/Objects/object_1.model"):
        root = _parse_xml(parts[name])
        if root.find(f"{{{CORE}}}build") is None:
            raise ValueError("Missing 3MF build element")
        uuids.extend(node.get(f"{{{PRODUCTION}}}UUID") for node in root.iter()
                     if node.get(f"{{{PRODUCTION}}}UUID"))
    if len(uuids) != 5 or len(set(uuids)) != 5:
        raise ValueError("Expected five distinct production-extension UUIDs")
    for identifier in uuids:
        uuid.UUID(identifier)
    stl, report = parts["Metadata/openprintlab/source.stl"], parts["Metadata/openprintlab/source.report.json"]
    original = _passport(report, stl)
    if (manifest["source_stl_sha256"] != _hash(stl) or manifest["source_report_sha256"] != _hash(report)
            or manifest["passport"] != original["passport"]):
        raise ValueError("Source provenance mismatch")
    triangles, transforms = _mesh_and_transform(parts)
    if triangles != decode_stl(stl):
        raise ValueError("Export changed triangle coordinates, order or winding")
    validate_mesh(triangles)
    if transforms != [[float(v) for v in IDENTITY.split()], [1., 0., 0., 0., 1., 0., 0., 0., 1., *manifest["translation_mm"]]]:
        raise ValueError("Export changed the explicit placement")
    cfg = _load_json(parts["Metadata/project_settings.config"])
    if cfg != manifest["settings"] or len(cfg["different_settings_to_system"]) != 3:
        raise ValueError("Project settings/difference slots mismatch")
    allowed = {
        "from", "name", "version", "printer_settings_id", "print_settings_id",
        "filament_settings_id", "filament_ids", "filament_type", "curr_bed_type",
        "printer_model", "printer_variant", "nozzle_diameter", "printable_height",
        "printable_area", "bed_exclude_area", "extruder_type", "default_nozzle_volume_type",
        "nozzle_volume_type", "different_settings_to_system",
    } | OVERRIDES.keys() | ENUM_OVERRIDES.keys()
    if set(cfg) != allowed:
        raise ValueError("Unexpected/missing project settings; arbitrary config/G-code is unsupported")
    if (cfg.get("printer_settings_id") != PRINTER or cfg.get("print_settings_id") != PROCESS
            or cfg.get("filament_settings_id") != [FILAMENT] or cfg.get("curr_bed_type") != PLATE
            or cfg.get("nozzle_diameter") != ["0.4"] or cfg.get("printer_model") != "Bambu Lab P2S"
            or cfg.get("printer_variant") != "0.4" or cfg.get("filament_type") != ["PLA"]
            or cfg.get("nozzle_volume_type") != ["Standard"]
            or cfg.get("extruder_type") != ["Direct Drive"]):
        raise ValueError("Project setup is not the supported P2S combination")
    changed = cfg["different_settings_to_system"]
    if changed[1:] != ["", ""] or not set(filter(None, changed[0].split(";"))) <= set(manifest["profiles"]["overrides"]):
        raise ValueError("Invalid override category/difference slots")
    for key, value in manifest["profiles"]["overrides"].items():
        if cfg.get(key) != value or key not in OVERRIDES.keys() | ENUM_OVERRIDES.keys():
            raise ValueError("Unsupported or inconsistent process override")
    model_settings = _parse_xml(parts["Metadata/model_settings.config"])
    objects = model_settings.findall("object")
    if len(objects) != 1 or objects[0].get("id") != "2":
        raise ValueError("Model settings must reference the exported object")
    mesh_stats = objects[0].findall("part/mesh_stat")
    extruder = objects[0].find("metadata[@key='extruder']")
    if (len(mesh_stats) != 1 or mesh_stats[0].get("face_count") != str(len(triangles))
            or extruder is None or extruder.get("value") != "1"):
        raise ValueError("Model settings face count/extruder differs")
    return manifest


def verify_profile_sources(project_path, profiles_dir):
    """Fail if the supplied installed resource chains changed since export.

    This cannot inspect Studio's active in-memory/cached/user presets; the UI
    and saved-project review are still required even after this passes.
    """
    manifest = inspect_project(project_path)
    for kind, name in (("machine", PRINTER), ("process", PROCESS), ("filament", FILAMENT)):
        effective, records = resolve_profile(profiles_dir, kind, name)
        if (records != manifest["profiles"]["files"][kind]
                or _hash(_json(effective)) != manifest["profiles"]["resolved_sha256"][kind]):
            raise ValueError(f"Installed {kind} profile sources changed; export a new project and review again")
    return {"profile_source_hashes_match": True, "active_studio_presets_verified": False}


def compare_saved_project(original_path, saved_path):
    """Compare an app-saved copy without promoting evidence or importing models.

    Only our one-object layout is supported. Studio may reorder vertices/faces
    and recenter object-local coordinates. Compare oriented placed triangles at
    1e-5 mm precision and every explicitly exported setting, not just bounds.
    """
    manifest = inspect_project(original_path)
    original, saved = _archive(original_path), _archive(saved_path)
    before = _placed(*_mesh_and_transform(original))
    after = _placed(*_mesh_and_transform(saved))

    def faces(triangles):
        result = []
        for triangle in triangles:
            rounded = tuple(tuple(round(v, 5) for v in p) for p in triangle)
            result.append(min(rounded[i:] + rounded[:i] for i in range(3)))
        return Counter(result)

    if faces(before) != faces(after):
        raise ValueError("App-saved geometry/placement differs (1e-5 mm comparison)")
    cfg = _load_json(saved["Metadata/project_settings.config"])
    ignored = {"from", "name", "version", "different_settings_to_system"}
    differences = [key for key, value in manifest["settings"].items()
                   if key not in ignored and cfg.get(key) != value]
    if differences:
        raise ValueError("App-saved settings differ: " + ", ".join(sorted(differences)))
    return {
        "geometry_and_placement_retained": True, "explicit_settings_retained": True,
        "triangles": len(before), "coordinate_comparison_mm": 0.00001,
        "original_sha256": _hash(_read(original_path)), "saved_sha256": _hash(_read(saved_path)),
        "source_passport_retained_by_studio": saved.get("Metadata/openprintlab/source.report.json")
        == original["Metadata/openprintlab/source.report.json"],
        "slicer_checked": False, "physical_print_tested": False,
        "scope": "File comparison only; native UI observations must be recorded separately.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("supported")
    inspect = sub.add_parser("inspect")
    inspect.add_argument("project")
    compare = sub.add_parser("compare")
    compare.add_argument("original")
    compare.add_argument("saved")
    profiles = sub.add_parser("check-profiles")
    profiles.add_argument("project")
    profiles.add_argument("--profiles-dir", required=True)
    export = sub.add_parser("export")
    for flag in ("stl", "report", "output", "profiles-dir", "studio-version",
                 "printer", "process", "filament", "plate", "nozzle-mm", "extruder-variant"):
        export.add_argument("--" + flag, required=True)
    export.add_argument("--translate", nargs=2, type=float, required=True, metavar=("X", "Y"))
    export.add_argument("--set", action="append", default=[], metavar="KEY=VALUE")
    args = parser.parse_args(argv)
    try:
        if args.command == "supported":
            result = supported_setup()
        elif args.command == "inspect":
            result = inspect_project(args.project)
        elif args.command == "compare":
            result = compare_saved_project(args.original, args.saved)
        elif args.command == "check-profiles":
            result = verify_profile_sources(args.project, args.profiles_dir)
        else:
            overrides = {}
            for pair in args.set:
                key, separator, value = pair.partition("=")
                if not separator or key in overrides:
                    raise ValueError("Overrides must be unique KEY=VALUE entries")
                overrides[key] = value
            result = export_project(
                args.stl, args.report, args.output, profiles_dir=args.profiles_dir,
                studio_version=args.studio_version, printer=args.printer, process=args.process,
                filament=args.filament, plate=args.plate, nozzle_mm=args.nozzle_mm,
                extruder_variant=args.extruder_variant, translation_xy=args.translate, overrides=overrides,
            )
        print(_json(result).decode(), end="")
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        parser.exit(2, f"bambu-project: {exc}\n")


if __name__ == "__main__":
    main()
