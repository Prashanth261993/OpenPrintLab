"""Shared catalog, parameter validation and build entry points. MIT license."""

import hashlib
import json
from pathlib import Path
import re
import zipfile

from models.recipes import PARAMETERS, boxes, validate_parameters
from tools.geometry import decode_stl, encode_stl, mesh_union, validate_mesh

ROOT = Path(__file__).resolve().parents[1]


def load_catalog():
    catalog = json.loads((ROOT / "models" / "catalog.json").read_text(encoding="utf-8"))
    if catalog["schema_version"] != 1 or catalog["units"] != "mm":
        raise ValueError("Unsupported catalog schema or units")
    ids = set()
    for model in catalog["models"]:
        identifier = model["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier) or identifier in ids:
            raise ValueError("Invalid or duplicate model ID")
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
    report = {
        "model": identifier, "units": "mm", "parameters": parameters,
        "sha256": hashlib.sha256(data).hexdigest(),
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
