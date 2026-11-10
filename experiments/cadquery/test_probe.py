"""Focused acceptance tests for the isolated CadQuery experiment."""

import dataclasses
from pathlib import Path
import tempfile
import unittest

import probe


class TrayExperimentTests(unittest.TestCase):
    def test_reference_and_both_rounded_sizes_meet_g2_and_step_roundtrip(self):
        with tempfile.TemporaryDirectory() as temp:
            for name, parameters in probe.CASES.items():
                with self.subTest(case=name):
                    report = probe.export_case(name, parameters, Path(temp))
                    self.assertTrue(report["g2_geometry_passed"])
                    self.assertLessEqual(report["checks"]["max_dimension_error_mm"], 0.05)
                    self.assertLessEqual(report["checks"]["kernel_analytic_volume_error_percent"], 0.1)
                    self.assertLessEqual(report["checks"]["mesh_kernel_volume_error_percent"], 0.5)
                    self.assertTrue(report["checks"]["kernel_valid"])
                    self.assertEqual(report["checks"]["solid_count"], 1)
                    self.assertTrue(report["checks"]["step_roundtrip_valid"])
                    self.assertLessEqual(report["checks"]["step_roundtrip_volume_error_percent"], 0.001)
                    self.assertEqual(report["repair_operations"], [])
                    self.assertFalse(report["validation"]["slicer_checked"])
                    self.assertFalse(report["validation"]["physical_print_tested"])
                    for extension in ("stl", "step"):
                        self.assertGreater((Path(temp) / f"{name}.{extension}").stat().st_size, 100)

    def test_invalid_inputs_are_rejected_before_cad_operations(self):
        base = probe.TrayParameters()
        for overrides in (
            {"length": 0}, {"length": 161}, {"width": float("nan")},
            {"height": float("inf")}, {"radius": -1}, {"radius": 1},
            {"radius": 17}, {"wall": True}, {"base": 3.1}, {"height": "16"},
        ):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                probe.make_tray(dataclasses.replace(base, **overrides))

    def test_radius_changes_geometry_and_customization_is_reproducible(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            parameters = probe.TrayParameters(radius=6)
            first = probe.export_case("rounded", parameters, root)
            second = probe.export_case("rounded", parameters, root)
            self.assertEqual(first["artifacts"]["stl_sha256"], second["artifacts"]["stl_sha256"])
            sharp = probe.make_tray(dataclasses.replace(parameters, radius=0))
            rounded = probe.make_tray(parameters)
            self.assertLess(rounded.Volume(), sharp.Volume())
            self.assertTrue(rounded.isValid())
            self.assertGreater(probe.make_tray(dataclasses.replace(parameters, length=120)).Volume(), rounded.Volume())

    def test_radius_boundaries_are_valid(self):
        for radius in (2.9, 16):
            with self.subTest(radius=radius):
                shape = probe.make_tray(probe.TrayParameters(radius=radius))
                self.assertTrue(shape.isValid())
                self.assertEqual(len(shape.Solids()), 1)


if __name__ == "__main__":
    unittest.main()
