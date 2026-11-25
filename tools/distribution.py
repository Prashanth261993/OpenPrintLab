"""Repository-scoped, verified source packages; never edit client/global config. MIT."""

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import zipfile

from tools.catalog import ROOT
from tools.designs import _safe_path

MANIFEST = "PACKAGE.json"
MARKER = ".openprintlab-install.json"
MAX_BYTES = 100 * 1024 * 1024


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def _name(name):
    p = PurePosixPath(name)
    devices = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
               *(f"LPT{i}" for i in range(1, 10))}
    if (not name or p.is_absolute() or "\\" in name or ":" in name or ".." in p.parts
            or str(p) != name or name.casefold() in (".git", MARKER)
            or name.casefold().startswith((".git/", "build/"))
            or any(part.endswith((".", " ")) or "\0" in part or part.split(".")[0].upper() in devices
                   for part in p.parts)):
        raise ValueError("Unsafe package member path")
    return name


def _records(archive):
    infos = archive.infolist()
    if len(infos) > 10000 or sum(i.file_size for i in infos) > MAX_BYTES:
        raise ValueError("Package exceeds size/member limits")
    result, names = {}, set()
    for info in infos:
        if info.is_dir():
            continue
        name = _name(info.filename)
        if name.casefold() in names or stat.S_ISLNK(info.external_attr >> 16):
            raise ValueError("Duplicate or symlink package member")
        names.add(name.casefold())
        result[name] = archive.read(info)
    return result


def build_package(output):
    """Package committed HEAD, not dirty/ignored source or user-private outputs."""
    output = _safe_path(output)
    if output.exists():
        raise FileExistsError("Package already exists; choose a new path")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    raw = subprocess.check_output(["git", "archive", "--format=zip", commit], cwd=ROOT)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        files = _records(z)
    if MANIFEST in files or MARKER in files:
        raise ValueError("Reserved package marker already exists in source")
    manifest = {"schema_version": 1, "commit": commit,
                "files": {name: _hash(data) for name, data in sorted(files.items())},
                "scope": "Full committed OpenPrintLab source snapshot; no environment, installation, global settings or private build outputs."}
    files[MANIFEST] = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        stream.write(buffer.getvalue())
    return {"path": str(output), "commit": commit, "sha256": _hash(buffer.getvalue())}


def _validated(package):
    with zipfile.ZipFile(package) as z:
        records = _records(z)
    if MANIFEST not in records:
        raise ValueError("Missing package manifest")
    manifest = json.loads(records.pop(MANIFEST))
    if (not isinstance(manifest, dict) or manifest.get("schema_version") != 1
            or not isinstance(manifest.get("commit"), str)
            or not re.fullmatch(r"[0-9a-f]{40}", manifest["commit"])
            or not isinstance(manifest.get("files"), dict) or set(manifest["files"]) != set(records)):
        raise ValueError("Invalid package manifest or member set")
    for name, data in records.items():
        if _hash(data) != manifest["files"][name]:
            raise ValueError(f"Package hash mismatch: {name}")
    return records, manifest


def inspect_package(package):
    return _validated(package)[1]


def install_package(package, destination):
    records, manifest = _validated(package)
    destination = _safe_path(destination)
    destination.mkdir()  # A separate empty directory, never merged into a user's repo.
    for name, data in records.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (destination / MARKER).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"directory": str(destination), "commit": manifest["commit"],
            "next_step": "Review and trust this separate checkout. Select OpenPrintLab Designer there, or explicitly add this directory in a supported client. No client/global configuration was changed."}


def uninstall_package(destination):
    destination = _safe_path(destination)
    marker = _safe_path(destination / MARKER)
    manifest = json.loads(marker.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1 or not isinstance(manifest.get("files"), dict):
        raise ValueError("Invalid installation marker")
    expected = {_name(name) for name in manifest["files"]}
    actual = {p.relative_to(destination).as_posix() for p in destination.rglob("*")
              if p.is_file() or p.is_symlink()}
    if actual != expected | {MARKER}:
        raise ValueError("Installation has extra/missing files; preserve your work and remove it manually")
    directories = set()
    for name in expected:
        path = _safe_path(destination / name)
        if _hash(path.read_bytes()) != manifest["files"][name]:
            raise ValueError(f"Installed file changed; preserving it: {name}")
        directories.update(p for p in path.parents if p != destination and p.is_relative_to(destination))
    present_dirs = {p for p in destination.rglob("*") if p.is_dir()}
    if present_dirs != directories:
        raise ValueError("Installation has extra directories; preserve them before removal")
    for name in sorted(expected):
        (destination / name).unlink()
    marker.unlink()
    for path in sorted(directories, key=lambda p: len(p.parts), reverse=True):
        path.rmdir()
    destination.rmdir()
    return {"removed": str(destination), "client_configuration_changed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for action in ("build", "inspect", "install"):
        p = sub.add_parser(action)
        p.add_argument("package")
        if action == "install":
            p.add_argument("--destination", required=True)
    p = sub.add_parser("uninstall")
    p.add_argument("destination")
    args = parser.parse_args()
    try:
        if args.command == "build":
            result = build_package(args.package)
        elif args.command == "inspect":
            result = inspect_package(args.package)
        elif args.command == "install":
            result = install_package(args.package, args.destination)
        else:
            result = uninstall_package(args.destination)
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"OpenPrintLab package: {exc}\n")


if __name__ == "__main__":
    main()
