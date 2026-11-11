import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.diagnostics import inspect_stl, inspect_variant
from tools.geometry import encode_stl, mesh_union
from tools.variants import create_variant


def cube(x=0, y=0, z=0, size=2):
    return mesh_union([(x, y, z, x + size, y + size, z + size)])


def codes(report):
    return {f["code"] for f in report["findings"]}


class DiagnosticTests(unittest.TestCase):
    def test_cube_metrics_and_hash_without_modifying_input(self):
        data = encode_stl(cube())
        result = inspect_stl(data)
        self.assertEqual(result["stl_sha256"], hashlib.sha256(data).hexdigest())
        self.assertFalse(result["has_errors"])
        part = result["components"][0]
        self.assertAlmostEqual(part["volume_mm3"], 8)
        self.assertAlmostEqual(part["bed_contact_area_mm2"], 4)
        self.assertEqual(part["downward_area_above_threshold_mm2"], 0)
        self.assertEqual(part["bounds_mm"], [[0, 0, 0], [2, 2, 2]])

    def test_plate_checks_each_component_and_part_requires_single_body(self):
        data = encode_stl(cube() + cube(10, z=3))
        plate = inspect_stl(data, mode="plate")
        self.assertEqual(len(plate["components"]), 2)
        self.assertIn("off_bed", codes(plate))
        self.assertIn("multiple_components", codes(inspect_stl(data)))
        assembly = inspect_stl(data, mode="assembly")
        self.assertNotIn("off_bed", codes(assembly))
        self.assertFalse(assembly["has_errors"])

    def test_bridge_has_contact_and_downward_area_not_slicer_certification(self):
        bridge = mesh_union([(0, 0, 0, 2, 4, 4), (8, 0, 0, 10, 4, 4), (0, 0, 4, 10, 4, 6)])
        report = inspect_stl(encode_stl(bridge))
        component = report["components"][0]
        self.assertAlmostEqual(component["bed_contact_area_mm2"], 16)
        self.assertAlmostEqual(component["downward_area_above_threshold_mm2"], 24)
        self.assertIn("downward_faces", codes(report))

    def test_sloped_face_threshold_is_from_vertical(self):
        angle = math.radians(30)
        rotated = [
            tuple((x, y * math.cos(angle) - z * math.sin(angle),
                   y * math.sin(angle) + z * math.cos(angle) + 3) for x, y, z in face)
            for face in cube()
        ]
        data = encode_stl(rotated)
        below = inspect_stl(data, mode="assembly", overhang_degrees=59)
        above = inspect_stl(data, mode="assembly", overhang_degrees=61)
        self.assertAlmostEqual(below["components"][0]["downward_area_above_threshold_mm2"], 4, places=5)
        self.assertEqual(above["components"][0]["downward_area_above_threshold_mm2"], 0)

    def test_separation_bound_and_overlap_are_not_exact_collision_claims(self):
        report = inspect_stl(encode_stl(cube() + cube(4)), mode="plate", clearance_mm=1)
        pair = report["component_pairs"][0]
        self.assertEqual(pair["bbox_distance_lower_bound_mm"], 2)
        self.assertEqual(pair["status"], "separated_bounds")
        self.assertIn("possible_contact_or_clearance", codes(
            inspect_stl(encode_stl(cube() + cube(4)), mode="plate", clearance_mm=3)))
        ring = mesh_union([(0, 0, 0, 10, 2, 2), (0, 8, 0, 10, 10, 2),
                           (0, 2, 0, 2, 8, 2), (8, 2, 0, 10, 8, 2)])
        hollow = inspect_stl(encode_stl(ring + cube(4, 4)), mode="assembly")
        self.assertEqual(hollow["component_pairs"][0]["status"], "needs_exact_check")
        self.assertFalse(hollow["has_errors"])

    def test_geometry_errors_and_placement_modes(self):
        for triangles, error in ((cube()[:-1], "edge_topology"),
                                 ([tuple(reversed(t)) for t in cube()], "nonpositive_volume"),
                                 (cube() + [cube()[0]], "duplicate_faces")):
            with self.subTest(error=error):
                self.assertIn(error, codes(inspect_stl(encode_stl(triangles))))
        self.assertIn("plate_margin", codes(inspect_stl(encode_stl(cube()), margin_mm=1)))
        self.assertIn("outside_envelope", codes(inspect_stl(encode_stl(cube(255)))))
        self.assertNotIn("outside_envelope", codes(inspect_stl(encode_stl(cube(255)), mode="assembly")))
        touching = inspect_stl(encode_stl(cube() + cube(2, 2, 2)), mode="assembly")
        self.assertEqual(len(touching["components"]), 2)

    def test_invalid_inputs_are_explicit_errors(self):
        data = encode_stl(cube())
        for kwargs in ({"mode": "unknown"}, {"margin_mm": -1}, {"margin_mm": True},
                       {"overhang_degrees": float("nan")}, {"overhang_degrees": 90},
                       {"clearance_mm": -1}, {"margin_mm": 128}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                inspect_stl(data, **kwargs)
        for malformed in (b"", data[:-1], data + b"x"):
            with self.assertRaises(ValueError):
                inspect_stl(malformed)
        bad = bytearray(data)
        import struct
        struct.pack_into("<f", bad, 96, float("inf"))
        with self.assertRaisesRegex(ValueError, "finite"):
            inspect_stl(bytes(bad))

    def test_cli_reports_errors_and_preserves_input(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "raised.stl"
            original = encode_stl(cube(z=2))
            path.write_bytes(original)
            result = subprocess.run([sys.executable, "-m", "tools.cli", "inspect-stl", str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("off_bed", codes(json.loads(result.stdout)))
            self.assertEqual(path.read_bytes(), original)
            malformed = subprocess.run([sys.executable, "-m", "tools.cli", "inspect-stl", str(path),
                                        "--margin", "nan"], capture_output=True, text=True)
            self.assertEqual(malformed.returncode, 2)

    def test_variant_inspection_rejects_tampering_and_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            created = create_variant("pocket-tray", "trial", output=root)
            result = inspect_variant("trial", root=root)
            self.assertEqual(result["stl_sha256"], created["report"]["sha256"])
            with self.assertRaises(ValueError):
                inspect_variant("../trial", root=root)
            path = Path(created["stl"])
            path.write_bytes(encode_stl(cube()))
            with self.assertRaisesRegex(ValueError, "hash"):
                inspect_variant("trial", root=root)
