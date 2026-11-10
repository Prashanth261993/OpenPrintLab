"""Verify stored trial evidence and compare platforms. SPDX-License-Identifier: MIT."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.geometry import decode_stl, validate_mesh


def geometry_signatures(data):
    def rounded(point):
        return tuple(round(value, 6) or 0.0 for value in point)
    faces = sorted(tuple(sorted(rounded(point) for point in face)) for face in decode_stl(data))
    vertices = sorted({point for face in faces for point in face})
    return {
        "triangles": hashlib.sha256(json.dumps(faces, separators=(",", ":")).encode()).hexdigest(),
        "vertices": hashlib.sha256(json.dumps(vertices, separators=(",", ":")).encode()).hexdigest(),
    }


def verify(directory):
    evidence = json.loads((directory / "environment-and-results.json").read_text(encoding="utf-8"))
    if not evidence["baseline_unchanged"] or not evidence["all_geometry_gates_passed"]:
        raise ValueError("Stored run did not pass baseline and geometry gates")
    if {case["case"] for case in evidence["cases"]} != {"reference-sharp", "rounded-96", "rounded-120"}:
        raise ValueError("Expected exactly the three bounded trial cases")
    cases = {}
    for report in evidence["cases"]:
        name = report["case"]
        standalone = json.loads((directory / f"{name}.report.json").read_text(encoding="utf-8"))
        if standalone != report:
            raise ValueError(f"{name}: standalone report differs from environment evidence")
        for extension in ("stl", "step"):
            digest = hashlib.sha256((directory / f"{name}.{extension}").read_bytes()).hexdigest()
            if digest != report["artifacts"][f"{extension}_sha256"]:
                raise ValueError(f"{name}: {extension} bytes do not match evidence")
        if validate_mesh(decode_stl((directory / f"{name}.stl").read_bytes())) != report["checks"]["mesh"]:
            raise ValueError(f"{name}: mesh checks differ from evidence")
        checks = report["checks"]
        if not (
            checks["kernel_valid"] and checks["solid_count"] == 1
            and checks["step_roundtrip_valid"]
            and checks["max_dimension_error_mm"] <= 0.05
            and checks["kernel_analytic_volume_error_percent"] <= 0.1
            and checks["mesh_kernel_volume_error_percent"] <= 0.5
            and checks["step_roundtrip_volume_error_percent"] <= 0.001
            and report["repair_operations"] == []
            and report["validation"]["slicer_checked"] is False
            and report["validation"]["physical_print_tested"] is False
        ):
            raise ValueError(f"{name}: evidence does not meet the stated gates")
        cases[name] = report
    return evidence, cases


def compare(windows, linux):
    win, win_cases = verify(windows)
    lin, lin_cases = verify(linux)
    if win["os"] != "Windows" or lin["os"] != "Linux":
        raise ValueError("Expected actual Windows and Linux run evidence")
    if win["baseline_hashes"] != lin["baseline_hashes"]:
        raise ValueError("Platforms did not verify the same baseline")
    results = []
    for name in sorted(win_cases):
        a, b = win_cases[name], lin_cases[name]
        if a["parameters"] != b["parameters"] or a["source_sha256"] != b["source_sha256"]:
            raise ValueError(f"{name}: different design source or parameters")
        win_geometry = geometry_signatures((windows / f"{name}.stl").read_bytes())
        lin_geometry = geometry_signatures((linux / f"{name}.stl").read_bytes())
        results.append({
            "case": name,
            "stl_bytes_identical": a["artifacts"]["stl_sha256"] == b["artifacts"]["stl_sha256"],
            "step_bytes_identical": a["artifacts"]["step_sha256"] == b["artifacts"]["step_sha256"],
            "triangle_geometry_equal_rounded_to_1e_6_mm": win_geometry["triangles"] == lin_geometry["triangles"],
            "vertex_positions_equal_rounded_to_1e_6_mm": win_geometry["vertices"] == lin_geometry["vertices"],
            "kernel_volume_difference_mm3": abs(a["checks"]["kernel_volume_mm3"] - b["checks"]["kernel_volume_mm3"]),
            "mesh_volume_difference_mm3": abs(a["checks"]["mesh"]["volume_mm3"] - b["checks"]["mesh"]["volume_mm3"]),
        })
    return {
        "baseline_hashes_identical": True,
        "both_platforms_pass_geometry_gates": True,
        "windows_python": win["python"], "linux_python": lin["python"],
        "cases": results,
        "note": "Hash differences are recorded, not silently normalized. Rounded geometry comparison is supplementary, not a byte-equivalence claim.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).parent / "artifacts"
    parser.add_argument("--windows", type=Path, default=root / "windows")
    parser.add_argument("--linux", type=Path, default=root / "linux")
    parser.add_argument("--output", type=Path, default=root / "comparison.json")
    args = parser.parse_args()
    result = compare(args.windows, args.linux)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
