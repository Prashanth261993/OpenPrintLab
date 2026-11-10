import copy
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from models.recipes import PARAMETERS, boxes, validate_parameters
from tools.catalog import ROOT, build_model, load_catalog, source_archive
from tools.geometry import decode_stl, encode_stl, mesh_union, validate_mesh
from tools.release import release


class ModelTests(unittest.TestCase):
    def test_defaults_match_analytical_solid_volumes(self):
        for model in load_catalog()["models"]:
            with self.subTest(model=model["id"]):
                data, report = build_model(model["id"])
                p = model["parameters"]
                length, width, height = (p[k] for k in ("length", "width", "height"))
                if model["recipe"] == "tray":
                    cavity = (length - (p["dividers"] + 2) * p["wall"]) * (width - 2 * p["wall"]) * (height - p["base"])
                    expected = length * width * height - cavity
                elif model["recipe"] == "rest":
                    expected = length * width * p["base"] + length * (p["channels"] + 1) * p["wall"] * (height - p["base"])
                else:
                    expected = length * width * height * (p["steps"] + 1) / (2 * p["steps"])
                self.assertAlmostEqual(report["checks"]["volume_mm3"], expected, delta=0.02)
                self.assertEqual(report["checks"]["dimensions_mm"], [length, width, height])
                self.assertEqual(report["sha256"], hashlib.sha256(data).hexdigest())
                self.assertEqual(report["validation"], {
                    "generated": True, "software_checked": True,
                    "slicer_checked": False, "physical_print_tested": False,
                })
                self.assertEqual(data, build_model(model["id"])[0])

    def test_custom_dimensions_and_relations(self):
        _, report = build_model("pocket-tray", {"length": 120, "width": 80, "height": 18})
        self.assertEqual(report["checks"]["dimensions_mm"], [120, 80, 18])
        for parameters in (
            {"length": 500}, {"length": float("nan")}, {"width": float("inf")},
            {"length": True}, {"wall": "2"}, {"typo": 20}, {"wall": 0.1},
            {"dividers": 1.2}, {"length": 30, "wall": 5, "dividers": 4},
            {"base": 5, "height": 6},
        ):
            with self.subTest(parameters=parameters), self.assertRaises(ValueError):
                build_model("pocket-tray", parameters)
        with self.assertRaises(ValueError):
            build_model("step-study", {"length": 16, "steps": 8})
        with self.assertRaises(ValueError):
            build_model("pen-rest", {"width": 20, "channels": 5})
        with self.assertRaises(ValueError):
            build_model("../escape")

    def test_supported_parameter_samples_are_closed(self):
        rng = random.Random(261993)
        successful = 0
        for model in load_catalog()["models"]:
            for _ in range(25):
                parameters = {
                    name: rng.randint(low, high) if name in ("channels", "steps", "dividers")
                    else round(rng.uniform(low, high), 3)
                    for name, (low, high) in PARAMETERS[model["recipe"]].items()
                }
                try:
                    validate_parameters(model["recipe"], parameters)
                except ValueError:
                    continue
                _, report = build_model(model["id"], parameters)
                self.assertTrue(report["checks"]["closed_edges"])
                successful += 1
        self.assertGreater(successful, 60)

    def test_defective_meshes_are_rejected(self):
        triangles = mesh_union([(0, 0, 0, 10, 10, 10)])
        self.assertAlmostEqual(validate_mesh(triangles)["volume_mm3"], 1000)
        invalid = [
            [], triangles[:-1], triangles + [triangles[0]],
            [tuple(reversed(t)) for t in triangles],
            [(triangles[0][0],) * 3] + triangles[1:],
            mesh_union([(0, 0, 0, 10, 10, 10), (20, 20, 0, 30, 30, 10)]),
            mesh_union([(0, 0, 1, 10, 10, 10)]),
            mesh_union([(0, 0, 0, 257, 10, 10)]),
        ]
        for mesh in invalid:
            with self.subTest(triangles=len(mesh)), self.assertRaises(ValueError):
                validate_mesh(mesh)
        data = encode_stl(triangles)
        for broken in (b"", data[:-1], data + b"x"):
            with self.assertRaises(ValueError):
                decode_stl(broken)

    def test_catalog_duplicates_and_bad_metadata_fail(self):
        catalog = load_catalog()
        for changed in (
            {**catalog, "units": "inches"},
            {**catalog, "models": catalog["models"] + [catalog["models"][0]]},
        ):
            with patch.object(Path, "read_text", return_value=json.dumps(changed)):
                with self.assertRaises(ValueError):
                    load_catalog()
        changed = copy.deepcopy(catalog)
        changed["models"][0]["color"] = '"><script>'
        with patch.object(Path, "read_text", return_value=json.dumps(changed)):
            with self.assertRaises(ValueError):
                load_catalog()

    def test_release_detects_stale_missing_and_extra_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            release(destination=directory)
            release(check=True, destination=directory)
            path = directory / "pocket-tray.stl"
            original = path.read_bytes()
            path.write_bytes(original + b"bad")
            with self.assertRaisesRegex(ValueError, "Stale"):
                release(check=True, destination=directory)
            path.write_bytes(original)
            extra = directory / "unexpected.txt"
            extra.write_text("not a model")
            with self.assertRaisesRegex(ValueError, "unexpected"):
                release(check=True, destination=directory)
            extra.unlink()
            path.unlink()
            with self.assertRaisesRegex(ValueError, "Missing"):
                release(check=True, destination=directory)

    def test_source_archive_can_rebuild_without_installation(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "source.zip"
            source_archive("pocket-tray", archive)
            first = archive.read_bytes()
            source_archive("pocket-tray", archive)
            self.assertEqual(first, archive.read_bytes())
            source = Path(temp) / "source"
            with zipfile.ZipFile(archive) as bundle:
                self.assertIn("LICENSE-CONTENT.md", bundle.namelist())
                bundle.extractall(source)
            result = subprocess.run(
                [sys.executable, "-m", "tools.cli", "build", "pocket-tray"],
                cwd=source, capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((source / "build" / "pocket-tray.stl").read_bytes(), build_model("pocket-tray")[0])

    def test_cli_invalid_input_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "invalid"
            result = subprocess.run(
                [sys.executable, "-m", "tools.cli", "build", "pocket-tray", "--set", "length=nan", "--output", str(output)],
                cwd=ROOT, capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("length must be", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
