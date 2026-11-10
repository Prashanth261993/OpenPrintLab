import hashlib
import json
import unittest
import zipfile

from tools.catalog import ROOT, canonical_hash, source_hash
from tools.variants import describe_template


class TemplateExampleTests(unittest.TestCase):
    def test_published_examples_match_sources_and_download_hashes(self):
        root = ROOT / "examples" / "template-lab"
        reports = list(root.glob("*/report.json"))
        self.assertEqual(len(reports), 3)
        templates = set()
        for path in reports:
            report = json.loads(path.read_text(encoding="utf-8"))
            templates.add(report["parent_template"])
            source = report["passport"]["editable_source"]
            self.assertEqual(source["recipe_sha256"], source_hash("models/cadquery_templates.py"))
            self.assertEqual(source["catalog_entry_sha256"], canonical_hash(describe_template(report["parent_template"])))
            self.assertEqual(report["evidence"]["geometry"]["checker_source_sha256"], source_hash("tools/variants.py"))
            self.assertEqual(report["preview"]["renderer_source_sha256"], source_hash("tools/mesh_preview.py"))
            self.assertEqual(report["preview"]["sha256"], hashlib.sha256((path.parent / "preview.svg").read_bytes()).hexdigest())
            for kind in ("stl", "step"):
                artifact = path.parent / report["artifacts"][kind]
                self.assertEqual(hashlib.sha256(artifact.read_bytes()).hexdigest(), report["artifacts"][kind + "_sha256"])
            with zipfile.ZipFile(path.parent / "source.zip") as bundle:
                self.assertEqual(json.loads(bundle.read("parameters.json")), report["parameters"])
            self.assertFalse(report["validation"]["slicer_checked"])
            self.assertFalse(report["validation"]["physical_print_tested"])
        self.assertEqual(templates, {"rounded-organizer", "rounded-pen-rest", "paper-card-stand"})


if __name__ == "__main__":
    unittest.main()
