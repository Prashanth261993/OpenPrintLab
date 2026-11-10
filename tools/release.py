"""Generate or check reproducible catalog artifacts."""

import argparse
import json

from models.recipes import boxes
from tools.catalog import ROOT, build_model, load_catalog
from tools.geometry import decode_stl
from tools.preview import render_svg


def artifacts(model):
    identifier = model["id"]
    stl, report = build_model(identifier)
    scad = [
        "// SPDX-License-Identifier: CC-BY-4.0",
        "// Original design: OpenPrintLab contributors. Units: mm.",
        "// Generated inspection snapshot; edit models/recipes.py and catalog.json to customize.",
        "// https://github.com/Prashanth261993/OpenPrintLab",
        "union() {",
    ]
    for box in boxes(model["recipe"], model["parameters"]):
        start = ", ".join(f"{v:.6f}" for v in box[:3])
        size = ", ".join(f"{box[i + 3] - box[i]:.6f}" for i in range(3))
        scad.append(f"  translate([{start}]) cube([{size}]);")
    scad.append("}")
    return {
        f"{identifier}.stl": stl,
        f"{identifier}.report.json": (json.dumps(report, indent=2) + "\n").encode(),
        f"{identifier}.svg": render_svg(decode_stl(stl), model["color"], model["name"]).encode(),
        f"{identifier}.scad": ("\n".join(scad) + "\n").encode(),
    }


def release(check=False, destination=None):
    directory = destination or ROOT / "models" / "exports"
    expected = {}
    for model in load_catalog()["models"]:
        expected.update(artifacts(model))
    if check:
        if not directory.is_dir():
            raise ValueError("Missing exports; run python -m tools.release")
        if {path.name for path in directory.iterdir()} != set(expected):
            raise ValueError("Missing or unexpected export files; regenerate and review exports")
        for name, data in expected.items():
            if (directory / name).read_bytes() != data:
                raise ValueError(f"Stale export: {name}; run python -m tools.release")
    else:
        directory.mkdir(parents=True, exist_ok=True)
        for name, data in expected.items():
            (directory / name).write_bytes(data)
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        count = release(check=args.check)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"{'Verified' if args.check else 'Generated'} {count} model artifacts.")


if __name__ == "__main__":
    main()
