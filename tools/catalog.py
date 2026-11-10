"""Shared catalog, parameter validation and build entry points. MIT license."""

import hashlib
import json
from pathlib import Path
import re
import zipfile

from models.recipes import PARAMETERS, boxes, validate_parameters
from tools.geometry import decode_stl, encode_stl, mesh_union, validate_mesh

ROOT = Path(__file__).resolve().parents[1]


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def source_hash(relative_path):
    # Universal-newline reading keeps source identity stable across checkouts.
    return hashlib.sha256((ROOT / relative_path).read_text(encoding="utf-8").encode()).hexdigest()


def load_catalog():
    catalog = json.loads((ROOT / "models" / "catalog.json").read_text(encoding="utf-8"))
    if catalog["schema_version"] != 1 or catalog["units"] != "mm":
        raise ValueError("Unsupported catalog schema or units")
    ids = set()
    for model in catalog["models"]:
        identifier = model["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier) or identifier in ids:
            raise ValueError("Invalid or duplicate model ID")
        if not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", model.get("version", "")):
            raise ValueError("Model version must be a major.minor.patch version")
        ids.add(identifier)
        validate_parameters(model["recipe"], model["parameters"])
        for key in ("name", "summary", "category", "notes", "customize"):
            if not isinstance(model[key], str) or not model[key].strip():
                raise ValueError(f"Missing model {key}")
        if not re.fullmatch(r"#[a-fA-F0-9]{6}", model["color"]):
            raise ValueError("Invalid preview color")
    return catalog


def get_model(identifier):
    for model in load_catalog()["models"]:
        if model["id"] == identifier:
            return model
    raise ValueError(f"Unknown model: {identifier}")


def build_model(identifier, overrides=None):
    model = get_model(identifier)
    parameters = model["parameters"] | (overrides or {})
    shape = boxes(model["recipe"], parameters)
    data = encode_stl(mesh_union(shape))
    checks = validate_mesh(decode_stl(data))
    stl_hash = hashlib.sha256(data).hexdigest()
    recipe_hash = source_hash("models/recipes.py")
    variant_id = canonical_hash({
        "model": identifier, "model_version": model["version"],
        "parameters": {key: float(value) for key, value in parameters.items()},
        "recipe_sha256": recipe_hash, "stl_sha256": stl_hash,
    })
    report = {
        "model": identifier, "units": "mm", "parameters": parameters,
        "sha256": stl_hash,
        "passport": {
            "schema_version": 1,
            "model_version": model["version"],
            "variant_id": variant_id,
            "design_license": "CC-BY-4.0",
            "attribution": "OpenPrintLab contributors",
            "editable_source": {
                "recipe_path": "models/recipes.py", "recipe_sha256": recipe_hash,
                "catalog_path": "models/catalog.json", "catalog_entry_sha256": canonical_hash(model),
            },
            "suggested_print_recipe": load_catalog()["suggested_print_recipe"],
        },
        "evidence": {
            "scope": {"model_version": model["version"], "variant_id": variant_id, "stl_sha256": stl_hash},
            "geometry": {
                "status": "passed", "checker": "openprintlab.geometry.v1",
                "checker_source_sha256": source_hash("tools/geometry.py"),
            },
            "slicer": {"status": "not_performed", "actual_settings": None, "record_url": None},
            "physical": {"status": "not_performed", "actual_settings": None, "record_url": None},
        },
        "validation": {"generated": True, "software_checked": True, "slicer_checked": False, "physical_print_tested": False},
        "checks": checks,
        "limitations": [
            "No slicer review or physical print test has been performed.",
            "These checks do not certify printability, tolerances, strength or safety.",
            "Only axis-aligned box-union recipes are supported; not a general mesh repair tool.",
        ],
    }
    return data, report


def parameter_schema(identifier):
    model = get_model(identifier)
    return {
        name: {"minimum": limits[0], "maximum": limits[1], "default": model["parameters"][name],
               "unit": "count" if name in ("channels", "dividers", "steps") else "mm"}
        for name, limits in PARAMETERS[model["recipe"]].items()
    }


def write_build(identifier, output, overrides=None):
    data, report = build_model(identifier, overrides)
    directory = Path(output)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{identifier}.stl").write_bytes(data)
    (directory / f"{identifier}.report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def source_archive(identifier, destination):
    """Bundle runnable source, preserving its mixed-license boundaries."""
    model = get_model(identifier)
    paths = [
        "models/__init__.py", "models/recipes.py", "models/catalog.json",
        "tools/__init__.py", "tools/geometry.py", "tools/catalog.py", "tools/cli.py",
        "LICENSE", "LICENSE-CONTENT.md", "README.md",
    ]
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in paths:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (ROOT / name).read_bytes())
        info = zipfile.ZipInfo("SELECTED-MODEL.txt", date_time=(2026, 1, 1, 0, 0, 0))
        archive.writestr(info, (
            f"{model['name']}\nRun from the unzipped folder:\n"
            f"python -m tools.cli build {identifier}\n\n"
            "This archive includes the dependency-free CLI and original design source.\n"
            "For MCP, site generation, tests and the full documentation tree, clone:\n"
            "https://github.com/Prashanth261993/OpenPrintLab\n"
            "Design sources: CC BY 4.0. Tooling: MIT. See the included licenses.\n"
        ))
