"""Read-only curated patterns. MIT; adaptation provenance accompanies the data."""

import json

from tools.catalog import ROOT


def list_patterns():
    return json.loads((ROOT / "patterns" / "review.json").read_text(encoding="utf-8"))


def describe_pattern(identifier):
    library = list_patterns()
    for pattern in library["patterns"]:
        if pattern["id"] == identifier:
            return pattern | {"license": library["license"], "attribution": library["attribution"]}
    raise ValueError(f"Unknown pattern: {identifier}")
