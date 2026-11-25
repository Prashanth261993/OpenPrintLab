"""Build the two reviewed public custom-palette revisions, never overwrite. MIT."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

from tools.catalog import ROOT
from tools.designs import create_design, revise_design, review_digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "designs")
    args = parser.parse_args()
    example = ROOT / "examples" / "custom-designs" / "round-palette"
    brief = json.loads((example / "brief.json").read_text(encoding="utf-8"))
    source = (example / "source.py").read_text(encoding="utf-8")
    draft = create_design("round-palette", brief, source, args.output)
    for i in (1, 2):
        if i == 2:
            draft = revise_design("round-palette", args.output)
            directory = Path(draft["directory"])
            brief["parameters"].update(diameter=80, wells=8)
            brief["expected_dimensions_mm"] = [80, 80, 8]
            brief["acceptance"] = ["Outside diameter 80 mm and height 8 mm",
                                   "Eight blind circular wells of diameter 14 mm",
                                   "Base 2 mm and at least 2 mm material between wells"]
            (directory / "brief.json").write_text(json.dumps(brief, indent=2) + "\n", encoding="utf-8")
        directory = Path(draft["directory"])
        result = subprocess.run([sys.executable, str(directory / "source.py"), "--reviewed-sha256",
                                 review_digest(directory)], cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
        report = json.loads(result.stdout)
        print(f"{report['design_id']}:{report['revision']} {report['checks']['dimensions_mm']} STL {report['sha256']}")
    print(f"Preview directory: {directory.parent}")


if __name__ == "__main__":
    main()
