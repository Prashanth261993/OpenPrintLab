import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.variants import create_variant, describe_template, list_templates


class OptionalDependencyTests(unittest.TestCase):
    def test_missing_cad_is_actionable_without_breaking_builtin(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch("tools.variants.importlib.import_module", side_effect=ModuleNotFoundError("cadquery")):
                with self.assertRaisesRegex(ValueError, "Optional CadQuery backend"):
                    create_variant("rounded-organizer", "missing", {}, root)
                self.assertFalse((root / "missing").exists())
                result = create_variant("pocket-tray", "builtin-still-works", {}, root)
                self.assertTrue(Path(result["stl"]).is_file())


@unittest.skipUnless(importlib.util.find_spec("cadquery"), "Optional CAD environment required")
class CadQueryTemplateTests(unittest.TestCase):
    def test_all_generators_and_custom_result_have_real_checked_exports(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for template in list_templates():
                if template["backend"] != "cadquery":
                    continue
                result = create_variant(template["id"], template["id"], {}, root)
                report = result["report"]
                self.assertTrue(report["checks"]["kernel_valid"])
                self.assertTrue(report["checks"]["step_roundtrip_valid"])
                self.assertFalse(report["validation"]["physical_print_tested"])
                self.assertEqual(hashlib.sha256(Path(result["stl"]).read_bytes()).hexdigest(), report["sha256"])
                self.assertTrue(Path(result["step"]).is_file())
            result = create_variant("rounded-organizer", "my-desk-organizer", {"length": 120, "width": 80, "height": 18, "radius": 8, "compartments": 3}, root)
            self.assertEqual(result["report"]["checks"]["dimensions_mm"], [120, 80, 18])

    def test_variants_get_fresh_identity_and_reject_invalid_geometry(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            a = create_variant("rounded-organizer", "first", {}, root)["report"]
            b = create_variant("rounded-organizer", "second", {"length": 140}, root)["report"]
            self.assertNotEqual(a["passport"]["variant_id"], b["passport"]["variant_id"])
            self.assertEqual(b["evidence"]["slicer"]["status"], "not_performed")
            for parameters in ({"radius": 1}, {"compartments": 2.5}, {"length": True}, {"unknown": 1}, {"wall": float("inf")}, {"radius": 30, "width": 30}):
                with self.subTest(parameters=parameters), self.assertRaises(ValueError):
                    create_variant("rounded-organizer", "invalid", parameters, root)
            with self.assertRaises(ValueError):
                create_variant("rounded-pen-rest", "invalid-rest", {"width": 24, "channels": 5}, root)
            with self.assertRaises(ValueError):
                create_variant("paper-card-stand", "invalid-card", {"slot_width": 10}, root)


if __name__ == "__main__":
    unittest.main()
