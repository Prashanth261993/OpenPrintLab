import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from tools.designs import create_design, revise_design, review_digest, publish_design


BRIEF = {
    "intended_use": "Dry craft bead sorting on a desk; noncritical prototype",
    "assumptions": ["Indoor use", "No food contact"],
    "acceptance": ["Outside dimensions match the supplied contract"],
    "parameters": {"length": 20, "width": 15, "height": 4},
    "expected_dimensions_mm": [20, 15, 4],
    "license": "CC-BY-4.0", "attribution": "OpenPrintLab contributors",
}


class DesignDraftTests(unittest.TestCase):
    def test_published_example_identities_and_preserved_revisions(self):
        root = Path("examples/custom-designs/published/round-palette")
        reports = []
        for revision in ("r0001", "r0002"):
            output = root / revision / "output"
            report = json.loads((output / "report.json").read_text())
            for name, digest in report["artifacts"].items():
                self.assertEqual(hashlib.sha256((output / name).read_bytes()).hexdigest(), digest)
            reports.append(report)
        self.assertEqual([r["brief"]["parameters"]["wells"] for r in reports], [6, 8])
        self.assertNotEqual(reports[0]["sha256"], reports[1]["sha256"])
        self.assertEqual(json.loads((root / "current.json").read_text())["revision"], "r0002")
    def test_creation_revision_and_refusal_preserve_original(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            draft = create_design("test-part", BRIEF, "# reviewed source\n", root)
            directory = Path(draft["directory"])
            self.assertEqual(json.loads((directory / "brief.json").read_text()), BRIEF)
            self.assertEqual(draft["review_sha256"], review_digest(directory))
            with self.assertRaises(FileExistsError):
                create_design("test-part", BRIEF, "", root)
            with self.assertRaisesRegex(ValueError, "published"):
                revise_design("test-part", root)
            for bad in ("../outside", "with space", "UPPER"):
                with self.assertRaises(ValueError):
                    create_design(bad, BRIEF, "", root)

    def test_bad_contract_is_not_written(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for change in ({"parameters": {"x": float("nan")}},
                           {"parameters": {"x": True}}, {"expected_dimensions_mm": [0, 2, 3]},
                           {"expected_dimensions_mm": [257, 2, 3]}, {"acceptance": []},
                           {"intended_use": ""}, {"unexpected": "field"}):
                with self.subTest(change=change), self.assertRaises(ValueError):
                    create_design("bad", BRIEF | change, "", root)
            self.assertFalse((root / "bad").exists())

    def test_review_gate_precedes_shape_callback(self):
        with tempfile.TemporaryDirectory() as temp:
            draft = create_design("gate", BRIEF, "# source\n", Path(temp))
            directory = Path(draft["directory"])
            calls = []
            def shape(_):
                calls.append(True)
            with self.assertRaisesRegex(ValueError, "review"):
                publish_design(directory / "source.py", shape, "0" * 64)
            self.assertFalse(calls)
            (directory / "brief.json").write_text(json.dumps(BRIEF | {"parameters": {"height": 5}}))
            with self.assertRaisesRegex(ValueError, "review"):
                publish_design(directory / "source.py", shape, draft["review_sha256"])
            self.assertFalse(calls)


@unittest.skipUnless(importlib.util.find_spec("cadquery"), "Optional CAD environment required")
class DesignExportTests(unittest.TestCase):
    def test_example_wells_match_analytical_volume_and_spacing(self):
        import math
        import runpy
        module = runpy.run_path("examples/custom-designs/round-palette/source.py")
        make = module["make_shape"]
        for diameter, count in ((72, 6), (80, 8)):
            p = {"diameter": diameter, "height": 8, "base": 2, "well_diameter": 14, "wells": count}
            solid = make(p)
            expected = math.pi * ((diameter / 2) ** 2 * 8 - count * 7 ** 2 * 6)
            self.assertAlmostEqual(solid.Volume(), expected, places=5)
            self.assertEqual(len(solid.Solids()), 1)
        with self.assertRaisesRegex(ValueError, "between"):
            make({"diameter": 50, "height": 8, "base": 2, "well_diameter": 18, "wells": 8})

    def test_export_revision_hashes_and_refused_rebuild(self):
        import cadquery as cq
        def make(p):
            return cq.Workplane("XY").box(p["length"], p["width"], p["height"],
                                          centered=(False, False, False)).val()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            draft = create_design("sample", BRIEF, "# self-contained source\n", root)
            directory = Path(draft["directory"])
            result = publish_design(directory / "source.py", make, draft["review_sha256"])
            out = directory / "output"
            before = {p.name: p.read_bytes() for p in out.iterdir()}
            self.assertEqual(result["checks"]["dimensions_mm"], [20, 15, 4])
            self.assertEqual(result["sha256"], hashlib.sha256((out / "model.stl").read_bytes()).hexdigest())
            self.assertFalse(result["validation"]["slicer_checked"])
            with self.assertRaises(FileExistsError):
                publish_design(directory / "source.py", make, draft["review_sha256"])
            second = revise_design("sample", root)
            next_dir = Path(second["directory"])
            contract = json.loads((next_dir / "brief.json").read_text())
            contract["parameters"]["length"] = 25
            contract["expected_dimensions_mm"][0] = 25
            (next_dir / "brief.json").write_text(json.dumps(contract))
            revised = publish_design(next_dir / "source.py", make, review_digest(next_dir))
            self.assertNotEqual(result["sha256"], revised["sha256"])
            self.assertEqual(before, {p.name: p.read_bytes() for p in out.iterdir()})
            self.assertEqual(json.loads((root / "sample" / "current.json").read_text())["revision"], "r0002")
            self.assertEqual((out / "source.py").read_bytes(), (directory / "source.py").read_bytes())

    def test_geometry_failure_never_updates_current_or_leaves_output(self):
        import cadquery as cq
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            draft = create_design("bad-shape", BRIEF, "# source\n", root)
            d = Path(draft["directory"])
            with self.assertRaisesRegex(ValueError, "dimensions"):
                publish_design(d / "source.py", lambda _: cq.Workplane("XY").box(
                    21, 15, 4, centered=(False, False, False)).val(), draft["review_sha256"])
            self.assertFalse((d / "output").exists())
            self.assertFalse((root / "bad-shape" / "current.json").exists())
