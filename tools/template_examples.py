"""Regenerate curated public examples only; never touches private user variants."""

from pathlib import Path
import shutil
import tempfile

from tools.catalog import ROOT
from tools.variants import create_variant, render_index

EXAMPLES = {
    "rounded-organizer": "example-organizer",
    "rounded-pen-rest": "example-pen-rest",
    "paper-card-stand": "example-card-stand",
}


def main():
    destination = ROOT / "examples" / "template-lab"
    if destination.resolve() != ROOT.resolve() / "examples" / "template-lab":
        raise ValueError("Curated example directory must not use symlinks")
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        for template, name in EXAMPLES.items():
            create_variant(template, name, {}, Path(temp))
        for name in EXAMPLES.values():
            if (destination / name).is_symlink():
                raise ValueError("Curated example directories must not use symlinks")
            shutil.copytree(Path(temp) / name, destination / name, dirs_exist_ok=True)
    render_index(destination)
    print("Regenerated three curated public examples. Private build/variants outputs were not changed.")


if __name__ == "__main__":
    main()
