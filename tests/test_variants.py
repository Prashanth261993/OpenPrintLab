import json
from pathlib import Path
import tempfile
import unittest

from tools.variants import create_variant, guidance


class VariantTests(unittest.TestCase):
    def test_builtin_variant_is_previewable_and_cannot_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = create_variant("pocket-tray", "my-tray", {"length": 120}, root)
            directory = root / "my-tray"
            report = json.loads((directory / "report.json").read_text())
            self.assertEqual(report["checks"]["dimensions_mm"], [120, 64, 16])
            self.assertEqual(report["backend"]["name"], "builtin")
            self.assertTrue((directory / "index.html").is_file())
            self.assertTrue((directory / "preview.svg").is_file())
            self.assertTrue((directory / "source.zip").is_file())
            self.assertTrue(Path(result["stl"]).is_file())
            before = (directory / "report.json").read_bytes()
            with self.assertRaises(FileExistsError):
                create_variant("pocket-tray", "my-tray", {"length": 130}, root)
            self.assertEqual(before, (directory / "report.json").read_bytes())

    def test_paths_and_invalid_parameters_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            for name in ("../escape", "/absolute", "a\\b", ".", ""):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    create_variant("pocket-tray", name, {}, Path(temp))
            with self.assertRaises(ValueError):
                create_variant("pocket-tray", "bad", {"length": float("nan")}, Path(temp))
            self.assertFalse((Path(temp) / "bad").exists())

    def test_guidance_requests_real_setup_and_does_not_invent_profiles(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            create_variant("pocket-tray", "my-tray", {}, root)
            missing = guidance("my-tray", {}, root)
            self.assertEqual(missing["status"], "needs_input")
            self.assertIn("nozzle_mm", missing["missing"])
            setup = {"printer": "Bambu Lab P2S", "nozzle_mm": 0.4, "plate": "Textured PEI", "material": "PLA", "use": "desk-organization"}
            supported = guidance("my-tray", setup, root)
            self.assertEqual(supported["status"], "suggested_starting_points")
            self.assertTrue(supported["sources"])
            rejected = guidance("my-tray", setup | {"material": "ABS"}, root)
            self.assertEqual(rejected["status"], "unsupported_setup")


if __name__ == "__main__":
    unittest.main()
