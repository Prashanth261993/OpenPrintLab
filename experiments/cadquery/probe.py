"""Isolated experiment runner and evidence generation. SPDX-License-Identifier: MIT."""

import argparse
from dataclasses import asdict
import hashlib
from importlib import metadata
import json
from pathlib import Path
import platform
import sys
import sysconfig

import cadquery as cq

from design import TrayParameters, analytic_volume, make_tray

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.geometry import decode_stl, validate_mesh
from tools.preview import render_svg
from tools.release import release

CASES = {
    "reference-sharp": TrayParameters(radius=0),
    "rounded-96": TrayParameters(),
    "rounded-120": TrayParameters(length=120, width=80, height=18),
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def percent_error(value, expected):
    return abs(value - expected) / expected * 100


def dimensions(shape):
    box = shape.BoundingBox()
    return [box.xlen, box.ylen, box.zlen]


def export_case(name, parameters, output):
    if not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name):
        raise ValueError("Case name must be a lowercase filename-safe identifier")
    shape = make_tray(parameters)
    if not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 0:
        raise ValueError("Kernel result must be one valid positive-volume solid")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    stl, step = output / f"{name}.stl", output / f"{name}.step"
    shape.exportStl(str(stl), tolerance=0.02, angularTolerance=0.1, ascii=False, relative=False, parallel=False)
    cq.exporters.export(shape, str(step))
    triangles = decode_stl(stl.read_bytes())
    mesh = validate_mesh(triangles)
    imported = cq.importers.importStep(str(step)).val()
    expected_dimensions = [parameters.length, parameters.width, parameters.height]
    kernel_dimensions = dimensions(shape)
    step_dimensions = dimensions(imported)
    dimension_error = max(
        abs(actual - expected)
        for measured in (kernel_dimensions, mesh["dimensions_mm"], step_dimensions)
        for actual, expected in zip(measured, expected_dimensions)
    )
    kernel_volume = shape.Volume()
    analytic_error = percent_error(kernel_volume, analytic_volume(parameters))
    mesh_error = percent_error(mesh["volume_mm3"], kernel_volume)
    roundtrip_error = percent_error(imported.Volume(), kernel_volume)
    roundtrip_valid = imported.isValid() and len(imported.Solids()) == 1
    passed = dimension_error <= 0.05 and analytic_error <= 0.1 and mesh_error <= 0.5 and roundtrip_error <= 0.001 and roundtrip_valid
    report = {
        "experiment": "T-05-cadquery", "case": name, "model_version": "0.1.0-experiment",
        "design_license": "CC-BY-4.0", "attribution": "OpenPrintLab contributors",
        "units": "mm", "parameters": asdict(parameters),
        "source_sha256": hashlib.sha256(Path(__file__).with_name("design.py").read_text(encoding="utf-8").encode()).hexdigest(),
        "environment": {"os": platform.system(), "python": platform.python_version(), "cadquery": metadata.version("cadquery")},
        "export": {"linear_tolerance_mm": 0.02, "angular_tolerance_radians": 0.1, "relative": False, "parallel": False},
        "artifacts": {"stl_sha256": sha(stl), "step_sha256": sha(step)},
        "checks": {
            "kernel_valid": shape.isValid(), "solid_count": len(shape.Solids()),
            "kernel_dimensions_mm": kernel_dimensions,
            "kernel_volume_mm3": kernel_volume,
            "analytic_volume_mm3": analytic_volume(parameters),
            "mesh": mesh,
            "max_dimension_error_mm": dimension_error,
            "kernel_analytic_volume_error_percent": analytic_error,
            "mesh_kernel_volume_error_percent": mesh_error,
            "step_roundtrip_valid": roundtrip_valid,
            "step_roundtrip_volume_error_percent": roundtrip_error,
        },
        "g2_geometry_passed": bool(passed),
        "repair_operations": [],
        "validation": {"geometry_checked": bool(passed), "slicer_checked": False, "physical_print_tested": False},
        "limitations": [
            "Experimental original model, not part of the starter catalog.",
            "Kernel and mesh checks do not certify printability, fit or strength.",
            "No slicer review or physical print has been performed.",
            "STEP carries geometry, not the editable Python parameter history.",
        ],
    }
    (output / f"{name}.report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / f"{name}.svg").write_text(render_svg(triangles, "#88a79b", f"Experimental {name}"), encoding="utf-8")
    if not passed:
        raise ValueError(f"{name} failed G-2 geometry thresholds; inspect {name}.report.json")
    return report


def package_inventory():
    packages = []
    paths = sorted({sysconfig.get_path("purelib"), sysconfig.get_path("platlib")})
    for distribution in sorted(metadata.distributions(path=paths), key=lambda d: d.metadata["Name"].lower()):
        info = distribution.metadata
        license_files = []
        for file in distribution.files or []:
            if Path(str(file)).name.lower().startswith(("license", "copying", "copyright")):
                path = distribution.locate_file(file)
                if path.is_file():
                    license_files.append({"path": str(file).replace("\\", "/"), "sha256": sha(path)})
        packages.append({
            "name": info["Name"], "version": distribution.version,
            "license_expression": info.get("License-Expression"),
            "license_declaration_excerpt": (info.get("License") or "")[:300],
            "license_classifiers": [c for c in info.get_all("Classifier", []) if c.startswith("License ::")],
            "license_files": license_files,
        })
    return packages


def run(output, custom=None):
    release(check=True)
    baseline = {path.name: sha(path) for path in (ROOT / "models" / "exports").iterdir()}
    reports = [export_case(name, p, output) for name, p in ({"custom": custom} if custom else CASES).items()]
    after = {path.name: sha(path) for path in (ROOT / "models" / "exports").iterdir()}
    if baseline != after:
        raise ValueError("Baseline artifacts changed during the experiment")
    result = {
        "experiment": "T-05-cadquery", "os": platform.system(), "python": platform.python_version(),
        "baseline_unchanged": True, "baseline_hashes": baseline,
        "all_geometry_gates_passed": all(report["g2_geometry_passed"] for report in reports),
        "cases": reports, "installed_packages": package_inventory(),
        "slicer_checked": False, "physical_print_tested": False,
    }
    Path(output, "environment-and-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output), "cases": [r["case"] for r in reports],
        "all_geometry_gates_passed": result["all_geometry_gates_passed"], "baseline_unchanged": True,
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "artifacts" / platform.system().lower())
    parser.add_argument("--custom", action="store_true", help="Export one bounded customized experimental tray")
    for name, default in asdict(TrayParameters()).items():
        parser.add_argument(f"--{name}", type=float, default=default)
    args = parser.parse_args()
    if not args.custom and any(getattr(args, name) != default for name, default in asdict(TrayParameters()).items()):
        parser.error("Use --custom when overriding dimensions")
    try:
        custom = TrayParameters(**{name: getattr(args, name) for name in asdict(TrayParameters())}) if args.custom else None
        run(args.output, custom)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"CadQuery experiment: {exc}\n")


if __name__ == "__main__":
    main()
