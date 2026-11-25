"""Optional-kernel checks of explicitly placed, hash-bound STEP solids. MIT."""

import hashlib
from importlib import metadata
import json
import math
from pathlib import Path

from tools.catalog import source_hash
from tools.designs import _safe_path
from tools.variants import _cadquery, safe_name


def check_assembly(manifest_path):
    manifest_path = _safe_path(manifest_path)
    raw = manifest_path.read_bytes()
    if len(raw) > 1024 * 1024:
        raise ValueError("Assembly manifest exceeds 1 MiB")
    manifest = json.loads(raw)
    if not isinstance(manifest, dict) or set(manifest) != {"units", "clearance_mm", "contacts", "parts"} or manifest["units"] != "mm":
        raise ValueError("Assembly requires units=mm, clearance_mm, contacts and parts")
    clearance = manifest["clearance_mm"]
    if isinstance(clearance, bool) or not isinstance(clearance, (int, float)) or not math.isfinite(clearance) or not 0 <= clearance <= 256:
        raise ValueError("clearance_mm must be finite between 0 and 256")
    parts = manifest["parts"]
    if not isinstance(parts, list) or not 2 <= len(parts) <= 32:
        raise ValueError("Expected 2 to 32 STEP parts")
    ids, files = set(), []
    for part in parts:
        if not isinstance(part, dict) or set(part) != {"id", "step", "sha256", "translation_mm"}:
            raise ValueError("Each part requires id, step, sha256 and translation_mm")
        safe_name(part["id"])
        if part["id"] in ids:
            raise ValueError("Duplicate part ID")
        ids.add(part["id"])
        step = part["step"]
        if not isinstance(step, str) or Path(step).is_absolute() or ".." in Path(step).parts:
            raise ValueError("STEP path must be within the manifest directory")
        path = _safe_path(manifest_path.parent / step)
        if not path.is_relative_to(manifest_path.parent) or path.suffix.lower() not in (".step", ".stp"):
            raise ValueError("Expected a local STEP file")
        if path.stat().st_size > 20 * 1024 * 1024:
            raise ValueError("STEP file exceeds 20 MiB")
        if hashlib.sha256(path.read_bytes()).hexdigest() != part["sha256"]:
            raise ValueError("STEP hash mismatch")
        offset = part["translation_mm"]
        if not isinstance(offset, list) or len(offset) != 3 or not all(
                not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)
                and abs(v) <= 10000 for v in offset):
            raise ValueError("translation_mm requires three finite coordinates within +/-10000 mm")
        files.append(path)
    contacts = manifest["contacts"]
    if not isinstance(contacts, list) or not all(
            isinstance(pair, list) and len(pair) == 2 and all(isinstance(x, str) and x in ids for x in pair)
            and pair[0] != pair[1] for pair in contacts):
        raise ValueError("contacts must list declared pairs of distinct existing IDs")
    declared = {frozenset(pair) for pair in contacts}
    cq = _cadquery()
    solids = []
    for part, path in zip(parts, files):
        shape = cq.importers.importStep(str(path)).val()
        if not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 0:
            raise ValueError("Each STEP input must contain one valid solid")
        if hashlib.sha256(path.read_bytes()).hexdigest() != part["sha256"]:
            raise ValueError("STEP changed while reading")
        solids.append(shape.translate(tuple(part["translation_mm"])))
    pairs = []
    for i, a in enumerate(solids):
        for j in range(i + 1, len(solids)):
            b = solids[j]
            distance, volume = a.distance(b), a.intersect(b).Volume()
            pair = [parts[i]["id"], parts[j]["id"]]
            expected_contact = frozenset(pair) in declared
            if not math.isfinite(distance) or not math.isfinite(volume):
                raise ValueError("Kernel returned non-finite measurement")
            if volume > 0.000001:
                status = "interference"
            elif expected_contact:
                status = "declared_contact" if distance <= 0.00001 else "missing_declared_contact"
            elif distance <= 0.00001 or distance + 0.00001 < clearance:
                status = "clearance_violation"
            else:
                status = "clear"
            pairs.append({"parts": pair, "distance_mm": distance, "intersection_volume_mm3": volume,
                          "status": status})
    return {"manifest_sha256": hashlib.sha256(raw).hexdigest(), "units": "mm",
            "inputs": manifest, "pairs": pairs,
            "backend": {"cadquery": metadata.version("cadquery"), "ocp": metadata.version("cadquery-ocp")},
            "checker_source_sha256": source_hash("tools/assembly_checks.py"),
            "tolerances": {"distance_mm": 0.00001, "intersection_volume_mm3": 0.000001},
            "has_errors": any(p["status"] not in ("clear", "declared_contact") for p in pairs),
            "limitations": ["Static translation-only poses, not motion or rotation validation.",
                            "Numerical B-rep intersections/distances, not exact physical measurements.",
                            "Declared contacts permit touching only, not positive-volume overlap.",
                            "No slicing, print fit, material, retention or structural evidence."],
            "slicer_checked": False, "physical_print_tested": False}
