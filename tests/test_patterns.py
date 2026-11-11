import json
from pathlib import Path
import subprocess
import sys
import unittest

from tools.patterns import describe_pattern


class PatternTests(unittest.TestCase):
    def test_unknown_pattern_is_not_replaced_with_generic_advice(self):
        with self.assertRaisesRegex(ValueError, "Unknown pattern"):
            describe_pattern("../../anything")
        result = subprocess.run(
            [sys.executable, "-m", "tools.cli", "pattern", "missing"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_cli_returns_selected_pattern_with_unpromoted_source_evidence(self):
        result = subprocess.run(
            [sys.executable, "-m", "tools.cli", "pattern", "fastener-selection"],
            capture_output=True, text=True, check=True,
        )
        record = json.loads(result.stdout)
        library = json.loads(Path("patterns/review.json").read_text())
        self.assertEqual(record, library["patterns"][0] |
                         {"license": library["license"], "attribution": library["attribution"]})
        self.assertEqual({e["source_status"] for e in record["upstream_observations"]},
                         {"failed", "proven", "designed_not_printed"})
        self.assertTrue(all(not e["independently_verified"] for e in record["upstream_observations"]))
        self.assertEqual(record["local_evidence"]["physical"], "not_performed")
