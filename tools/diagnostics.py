"""Read-only mesh screening. MIT; see third_party/wilsonwaters/NOTICE.md."""

from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path

from tools.catalog import source_hash
from tools.geometry import cross, decode_stl, dot, subtract

MAX_BYTES = 84 + 50 * 200_000
TOLERANCE_MM = 0.0001


def _number(value, name, minimum, maximum):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")


def inspect_stl(data, mode="part", margin_mm=0, overhang_degrees=45, clearance_mm=0):
    """Screen already-oriented binary STL; never repair or transform input."""
    if mode not in ("part", "plate", "assembly"):
        raise ValueError("mode must be part, plate or assembly")
    _number(margin_mm, "margin_mm", 0, 127.999)
    _number(overhang_degrees, "overhang_degrees", 0, 89.999)
    _number(clearance_mm, "clearance_mm", 0, 256)
    if len(data) > MAX_BYTES:
        raise ValueError("Diagnostics supports at most 200000 triangles")
    triangles = decode_stl(data)
    parent = list(range(len(triangles)))
    owners = {}

    def root(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for index, face in enumerate(triangles):
        if not all(math.isfinite(v) for point in face for v in point):
            raise ValueError("Mesh coordinates must be finite")
        a, b, c = face
        n = cross(subtract(b, a), subtract(c, a))
        if dot(n, n) < 1e-12:
            raise ValueError("Degenerate triangle")
        for start, end in ((a, b), (b, c), (c, a)):
            edge = tuple(sorted((start, end)))
            if edge in owners:
                parent[root(index)] = root(owners[edge])
            else:
                owners[edge] = index
    groups = defaultdict(list)
    for index, face in enumerate(triangles):
        groups[root(index)].append(face)
    if len(groups) > 128:
        raise ValueError("Diagnostics supports at most 128 edge-connected components")
    findings, components = [], []

    def finding(code, severity, **scope):
        findings.append({"code": code, "severity": severity, **scope})

    if mode == "part" and len(groups) != 1:
        finding("multiple_components", "error")
    threshold = math.sin(math.radians(overhang_degrees))
    for index, faces in enumerate(groups.values()):
        points = [p for face in faces for p in face]
        low = [min(p[axis] for p in points) for axis in range(3)]
        high = [max(p[axis] for p in points) for axis in range(3)]
        edges = Counter((start, end) for a, b, c in faces
                        for start, end in ((a, b), (b, c), (c, a)))
        if any(count != 1 or edges[end, start] != 1 for (start, end), count in edges.items()):
            finding("edge_topology", "error", component=index)
        if len({tuple(sorted(face)) for face in faces}) != len(faces):
            finding("duplicate_faces", "error", component=index)
        volume, contact, downward = 0.0, 0.0, 0.0
        # A local reference improves volume precision without changing source coordinates.
        origin = faces[0][0]
        for a, b, c in faces:
            n = cross(subtract(b, a), subtract(c, a))
            norm = math.sqrt(dot(n, n))
            volume += dot(subtract(a, origin), cross(subtract(b, origin), subtract(c, origin))) / 6
            at_bed = all(abs(p[2]) <= TOLERANCE_MM for p in (a, b, c))
            if n[2] < 0 and at_bed:
                contact += norm / 2
            elif -n[2] / norm > threshold:
                downward += norm / 2
        if volume <= 0:
            finding("nonpositive_volume", "error", component=index)
        if mode != "assembly":
            if abs(low[2]) > TOLERANCE_MM:
                finding("off_bed", "error", component=index)
            if any(low[i] < -TOLERANCE_MM or high[i] > 256 + TOLERANCE_MM for i in range(3)):
                finding("outside_envelope", "error", component=index)
            if any(low[i] < margin_mm - TOLERANCE_MM or high[i] > 256 - margin_mm + TOLERANCE_MM
                   for i in (0, 1)):
                finding("plate_margin", "error", component=index)
            if contact <= 0:
                finding("no_planar_bed_contact", "warning", component=index)
            if downward > 0:
                finding("downward_faces", "warning", component=index)
        components.append({
            "id": index, "triangles": len(faces), "bounds_mm": [low, high],
            "volume_mm3": round(volume, 6), "bed_contact_area_mm2": round(contact, 6),
            "downward_area_above_threshold_mm2": round(downward, 6),
        })
    pairs = []
    for i, a in enumerate(components):
        for b in components[i + 1:]:
            alo, ahi = a["bounds_mm"]
            blo, bhi = b["bounds_mm"]
            gaps = [max(0, alo[k] - bhi[k], blo[k] - ahi[k]) for k in range(3)]
            distance = math.sqrt(sum(g * g for g in gaps))
            separated = distance > TOLERANCE_MM and distance >= clearance_mm + TOLERANCE_MM
            pairs.append({"components": [a["id"], b["id"]],
                          "bbox_distance_lower_bound_mm": distance,
                          "status": "separated_bounds" if separated else "needs_exact_check"})
            if not separated:
                finding("possible_contact_or_clearance", "warning", components=[a["id"], b["id"]])
    return {
        "schema_version": 1, "status": "diagnostics_only", "units": "mm",
        "stl_sha256": hashlib.sha256(data).hexdigest(),
        "checker_source_sha256": source_hash("tools/diagnostics.py"),
        "decoder_source_sha256": source_hash("tools/geometry.py"),
        "mode": mode, "settings": {"build_volume_mm": [256, 256, 256], "margin_mm": margin_mm,
                                   "overhang_degrees_from_vertical": overhang_degrees,
                                   "clearance_mm": clearance_mm, "tolerance_mm": TOLERANCE_MM},
        "components": components, "component_pairs": pairs, "findings": findings,
        "has_errors": any(f["severity"] == "error" for f in findings),
        "not_checked": ["self-intersections", "solid-shell nesting or enclosed cavities",
                        "exact inter-part intersections or surface clearance",
                        "first-layer islands", "support/bridge feasibility", "slicer behavior",
                        "mechanical suitability or physical printing"],
        "limitations": ["Components use exact shared edges; vertex-only contacts remain separate.",
                        "Bounds give conservative separation only; overlap is inconclusive.",
                        "Enclosed cavity shells may trigger component/volume findings; use native solid review, not automatic repair.",
                        "Areas/volumes assume oriented closed surfaces; interpret topology errors first.",
                        "Assembly mode does not assess print orientation or plate placement.",
                        "Angle and margin settings are review thresholds, not certified printer rules."],
    }


def inspect_file(path, **settings):
    with Path(path).open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    return inspect_stl(data, **settings)


def inspect_variant(name, root=None, **settings):
    from tools.variants import DEFAULT_OUTPUT, safe_name
    safe_name(name)
    root = Path(root) if root is not None else DEFAULT_OUTPUT
    directory = root / name
    paths = [root, directory, directory / "report.json", directory / f"{name}.stl"]
    if any(path.is_symlink() or path.resolve() != path.absolute() for path in paths):
        raise ValueError("Variant inspection paths must not use symlinks or traversal")
    report = json.loads(paths[2].read_text(encoding="utf-8"))
    result = inspect_file(paths[3], **settings)
    if not isinstance(report, dict) or report.get("sha256") != result["stl_sha256"]:
        raise ValueError("Variant STL hash does not match its report; rebuild a fresh variant")
    return result
