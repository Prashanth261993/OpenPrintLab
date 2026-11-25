import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from tools.assembly_checks import check_assembly


@unittest.skipUnless(importlib.util.find_spec("cadquery"), "Optional CAD environment required")
class AssemblyTests(unittest.TestCase):
    def test_overlap_clearance_and_contact_are_kernel_measurements(self):
        import cadquery as cq
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cube = cq.Workplane("XY").box(2, 2, 2).val()
            cq.exporters.export(cube, str(root / "cube.step"))
            digest = hashlib.sha256((root / "cube.step").read_bytes()).hexdigest()
            manifest = {"units": "mm", "clearance_mm": 0.5, "contacts": [],
                        "parts": [{"id": "a", "step": "cube.step", "sha256": digest, "translation_mm": [0, 0, 0]},
                                  {"id": "b", "step": "cube.step", "sha256": digest, "translation_mm": [3, 0, 0]}]}
            path = root / "assembly.json"
            def run():
                path.write_text(json.dumps(manifest))
                return check_assembly(path)
            result = run()
            self.assertFalse(result["has_errors"])
            self.assertAlmostEqual(result["pairs"][0]["distance_mm"], 1)
            manifest["parts"][1]["translation_mm"] = [1, 0, 0]
            result = run()
            self.assertTrue(result["has_errors"])
            self.assertAlmostEqual(result["pairs"][0]["intersection_volume_mm3"], 4)
            manifest["parts"][1]["translation_mm"] = [2, 0, 0]
            self.assertTrue(run()["has_errors"])
            manifest["contacts"] = [["a", "b"]]
            self.assertFalse(run()["has_errors"])
            manifest["parts"][1]["sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "hash"):
                run()

    def test_hollow_space_has_clearance_despite_overlapping_bounds(self):
        import cadquery as cq
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ring = cq.Workplane("XY").rect(10, 10).rect(6, 6).extrude(2).val()
            middle = cq.Workplane("XY").box(2, 2, 2, centered=(True, True, False)).val()
            parts = []
            for name, shape in (("ring", ring), ("middle", middle)):
                cq.exporters.export(shape, str(root / f"{name}.step"))
                parts.append({"id": name, "step": f"{name}.step",
                              "sha256": hashlib.sha256((root / f"{name}.step").read_bytes()).hexdigest(),
                              "translation_mm": [0, 0, 0]})
            manifest = root / "assembly.json"
            manifest.write_text(json.dumps({"units": "mm", "clearance_mm": 1,
                                            "contacts": [], "parts": parts}))
            result = check_assembly(manifest)
            self.assertFalse(result["has_errors"])
            self.assertAlmostEqual(result["pairs"][0]["distance_mm"], 2)
            self.assertAlmostEqual(result["pairs"][0]["intersection_volume_mm3"], 0)


class ManifestTests(unittest.TestCase):
    def test_invalid_manifest_fails_before_loading_cad(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assembly.json"
            for manifest in ({}, {"units": "inch", "parts": []},
                             {"units": "mm", "parts": [], "clearance_mm": float("nan"), "contacts": []}):
                path.write_text(json.dumps(manifest))
                with self.assertRaises(ValueError):
                    check_assembly(path)
