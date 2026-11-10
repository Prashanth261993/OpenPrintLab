import json
import unittest

from tools.catalog import ROOT


class FeedbackTests(unittest.TestCase):
    def test_issue_form_accepts_failures_and_captures_versioned_evidence(self):
        # JSON is a YAML subset, so the GitHub form is also dependency-free to validate.
        form = json.loads((ROOT / ".github" / "ISSUE_TEMPLATE" / "print-result.yml").read_text(encoding="utf-8"))
        fields = {field["id"]: field for field in form["body"] if "id" in field}
        self.assertEqual(len(fields), len([field for field in form["body"] if "id" in field]))
        for field in form["body"]:
            self.assertIn(field["type"], ("markdown", "input", "textarea", "dropdown", "checkboxes"))
            self.assertIn("attributes", field)
        for identifier in (
            "outcome", "model_id", "model_version", "variant_id", "stl_sha256",
            "parameters", "actual_settings", "test_date", "observations", "evidence",
        ):
            self.assertTrue(fields[identifier]["validations"]["required"])
        self.assertEqual(fields["outcome"]["attributes"]["options"], [
            "Success", "Partial success", "Failure", "Stopped before printing (slicer review only)",
        ])
        self.assertIn("unavailable", fields["evidence"]["attributes"]["description"])
        settings = fields["actual_settings"]["attributes"]["placeholder"].lower()
        for item in ("slicer", "printer", "nozzle", "plate", "filament", "layer", "infill", "orientation", "supports"):
            self.assertIn(item, settings)
        self.assertTrue(all(option["required"] for option in fields["acknowledgements"]["attributes"]["options"]))
        self.assertNotIn("labels", form)  # Do not rely on labels that may not exist.


if __name__ == "__main__":
    unittest.main()
