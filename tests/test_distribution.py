import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from tools.distribution import build_package, inspect_package, install_package, uninstall_package


class DistributionTests(unittest.TestCase):
    def test_deterministic_snapshot_install_run_and_guarded_uninstall(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            a, b = root / "a.zip", root / "b.zip"
            build_package(a)
            build_package(b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            manifest = inspect_package(a)
            self.assertIn(".github/agents/openprintlab-designer.agent.md", manifest["files"])
            self.assertIn("docs/structural-design.md", manifest["files"])
            self.assertTrue(all(not p.startswith(("build/", ".git/")) for p in manifest["files"]))
            destination = root / "installed"
            install_package(a, destination)
            result = subprocess.run([sys.executable, "-B", "-m", "tools.cli", "list"], cwd=destination,
                                    capture_output=True, text=True, check=True)
            self.assertEqual(len(json.loads(result.stdout)["models"]), 4)
            with self.assertRaises(FileExistsError):
                install_package(a, destination)
            changed = destination / "README.md"
            original = changed.read_bytes()
            changed.write_text("user edit")
            with self.assertRaisesRegex(ValueError, "changed"):
                uninstall_package(destination)
            self.assertTrue(changed.is_file())
            changed.write_bytes(original)
            extra = destination / "my-work.txt"
            extra.write_text("preserve me")
            with self.assertRaisesRegex(ValueError, "extra"):
                uninstall_package(destination)
            extra.unlink()
            # Running Python may create caches; these are deliberately user-owned
            # extras, not something the uninstaller can silently delete.
            for path in destination.rglob("*.pyc"):
                path.unlink()
            for path in sorted(destination.rglob("__pycache__"), reverse=True):
                path.rmdir()
            uninstall_package(destination)
            self.assertFalse(destination.exists())

    def test_tampered_or_traversing_package_is_refused_before_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            package = root / "package.zip"
            build_package(package)
            with zipfile.ZipFile(package) as source:
                records = {i.filename: source.read(i.filename) for i in source.infolist()}
            records["README.md"] = b"tampered"
            bad = root / "bad.zip"
            with zipfile.ZipFile(bad, "w") as z:
                for name, data in records.items():
                    z.writestr(name, data)
            with self.assertRaisesRegex(ValueError, "hash"):
                install_package(bad, root / "no-write")
            self.assertFalse((root / "no-write").exists())
            with zipfile.ZipFile(bad, "w") as z:
                z.writestr("../escape", "bad")
                z.writestr("PACKAGE.json", "{}")
            with self.assertRaises(ValueError):
                inspect_package(bad)
