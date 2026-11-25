"""Reviewed single-file custom CAD publishing; no source-execution endpoint. MIT."""

import argparse
import hashlib
from html import escape
from importlib import metadata
import json
import math
from pathlib import Path
import re
import shutil
import tempfile

from tools.catalog import ROOT, canonical_hash, source_hash
from tools.geometry import decode_stl, validate_mesh
from tools.mesh_preview import render_svg
from tools.variants import _cadquery, safe_name

DEFAULT_DESIGNS = ROOT / "build" / "designs"
FIELDS = {"intended_use", "assumptions", "acceptance", "parameters",
          "expected_dimensions_mm", "license", "attribution"}


def _safe_path(path):
    path = Path(path).absolute()
    if path.resolve() != path or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("Design paths must not use symlinks or traversal")
    return path


def validate_brief(brief):
    if not isinstance(brief, dict) or set(brief) != FIELDS:
        raise ValueError(f"Brief requires exactly: {', '.join(sorted(FIELDS))}")
    for key in ("intended_use", "license", "attribution"):
        if not isinstance(brief[key], str) or not brief[key].strip():
            raise ValueError(f"{key} must be nonempty text")
    for key in ("assumptions", "acceptance"):
        if not isinstance(brief[key], list) or not brief[key] or not all(
                isinstance(v, str) and v.strip() for v in brief[key]):
            raise ValueError(f"{key} must be a nonempty list of text")
    params = brief["parameters"]
    if not isinstance(params, dict) or not params:
        raise ValueError("parameters must be a nonempty numeric object")
    for key, value in params.items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise ValueError("Parameter names must be lowercase identifiers")
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{key} must be finite and numeric")
    dims = brief["expected_dimensions_mm"]
    if not isinstance(dims, list) or len(dims) != 3 or not all(
            not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)
            and 0 < v <= 256 for v in dims):
        raise ValueError("expected_dimensions_mm requires three finite positive lengths up to 256 mm")


def review_digest(directory):
    directory = _safe_path(directory)
    inputs = {}
    for name in ("source.py", "brief.json"):
        data = _safe_path(directory / name).read_bytes()
        inputs[name] = hashlib.sha256(data).hexdigest()
    validate_brief(json.loads((directory / "brief.json").read_text(encoding="utf-8")))
    return canonical_hash(inputs)


def _draft_result(directory):
    return {"directory": str(directory), "source": str(directory / "source.py"),
            "review_sha256": review_digest(directory),
            "next_step": "Read source.py and brief.json, review all code and imports, then explicitly run source.py with --reviewed-sha256 DIGEST using the optional CAD interpreter. Hash acknowledgement is not a sandbox or safety review."}


def create_design(name, brief, source, root=None):
    safe_name(name)
    validate_brief(brief)
    if not isinstance(source, str):
        raise ValueError("source must be text")
    root = _safe_path(root if root is not None else DEFAULT_DESIGNS)
    target = _safe_path(root / name)
    root.mkdir(parents=True, exist_ok=True)
    target.mkdir()  # Exclusive; never replace another design.
    revision = target / "r0001"
    revision.mkdir()
    (revision / "brief.json").write_text(json.dumps(brief, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (revision / "source.py").write_text(source, encoding="utf-8")
    (target / "index.html").write_text(_viewer(name), encoding="utf-8")
    return _draft_result(revision)


def revise_design(name, root=None):
    safe_name(name)
    root = _safe_path(root if root is not None else DEFAULT_DESIGNS)
    target = _safe_path(root / name)
    current_path = _safe_path(target / "current.json")
    if not current_path.is_file():
        raise ValueError("A design must be published before creating a revision")
    current = json.loads(current_path.read_text(encoding="utf-8"))
    revision = current["revision"]
    if not re.fullmatch(r"r[0-9]{4}", revision):
        raise ValueError("Invalid published revision")
    number = int(revision[1:]) + 1
    if number > 9999:
        raise ValueError("Revision limit reached")
    previous = _safe_path(target / revision / "output")
    report = json.loads(_safe_path(previous / "report.json").read_text(encoding="utf-8"))
    for filename in ("source.py", "brief.json"):
        data = _safe_path(previous / filename).read_bytes()
        if hashlib.sha256(data).hexdigest() != report["inputs"][filename]:
            raise ValueError("Published source hash mismatch; do not revise altered history")
    next_dir = _safe_path(target / f"r{number:04d}")
    next_dir.mkdir()
    for filename in ("source.py", "brief.json"):
        shutil.copyfile(previous / filename, next_dir / filename)
    return _draft_result(next_dir)


def publish_design(source_file, make_shape, reviewed_sha256):
    source_file = _safe_path(source_file)
    lock = _safe_path(source_file.parent.parent / ".publish.lock")
    with lock.open("x", encoding="utf-8"):
        pass
    try:
        return _publish_design(source_file, make_shape, reviewed_sha256)
    finally:
        lock.unlink()


def _publish_design(source_file, make_shape, reviewed_sha256):
    """Called by already reviewed/executing local source, never via CLI/MCP dispatch."""
    source_file = _safe_path(source_file)
    directory = source_file.parent
    if source_file.name != "source.py" or not re.fullmatch(r"r[0-9]{4}", directory.name):
        raise ValueError("Execute a source.py in a generated rNNNN design revision")
    safe_name(directory.parent.name)
    if reviewed_sha256 != review_digest(directory):
        raise ValueError("Source/brief review hash missing or stale; review both before execution")
    output = _safe_path(directory / "output")
    if output.exists():
        raise FileExistsError("Published revision already exists; create a new revision")
    current_path = _safe_path(directory.parent / "current.json")
    expected = 1
    if current_path.is_file():
        previous = json.loads(current_path.read_text(encoding="utf-8"))
        if not re.fullmatch(r"r[0-9]{4}", previous.get("revision", "")):
            raise ValueError("Invalid current revision")
        expected = int(previous["revision"][1:]) + 1
    if directory.name != f"r{expected:04d}":
        raise ValueError("Publish revisions in sequence; do not replace current with older work")
    inputs = {name: _safe_path(directory / name).read_bytes() for name in ("source.py", "brief.json")}
    brief = json.loads(inputs["brief.json"])
    cq = _cadquery()
    shape = make_shape(dict(brief["parameters"]))
    if not isinstance(shape, cq.Shape) or not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 0:
        raise ValueError("Custom output must be one valid positive-volume CadQuery Shape")
    with tempfile.TemporaryDirectory(prefix=".export-", dir=directory) as temp:
        work = Path(temp)
        shape.exportStl(str(work / "model.stl"), tolerance=0.02, angularTolerance=0.1,
                        ascii=False, relative=False, parallel=False)
        cq.exporters.export(shape, str(work / "model.step"))
        data = (work / "model.stl").read_bytes()
        triangles = decode_stl(data)
        checks = validate_mesh(triangles)
        if any(abs(a - b) > 0.05 for a, b in zip(checks["dimensions_mm"], brief["expected_dimensions_mm"])):
            raise ValueError("Export dimensions differ from the brief by more than 0.05 mm")
        if abs(checks["volume_mm3"] - shape.Volume()) / shape.Volume() > 0.005:
            raise ValueError("Mesh/kernel volume mismatch exceeds 0.5%")
        back = cq.importers.importStep(str(work / "model.step")).val()
        if not back.isValid() or len(back.Solids()) != 1 or abs(back.Volume() - shape.Volume()) / shape.Volume() > 0.00001:
            raise ValueError("STEP round-trip validation failed")
        if review_digest(directory) != reviewed_sha256:
            raise ValueError("Source/brief changed during export; review again")
        for filename, payload in inputs.items():
            (work / filename).write_bytes(payload)
        checks.update(kernel_valid=True, step_roundtrip_valid=True, kernel_volume_mm3=shape.Volume())
        svg = render_svg(triangles, "#497f70", f"{directory.parent.name}:{directory.name}")
        (work / "preview.svg").write_text(svg, encoding="utf-8")
        artifacts = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in work.iterdir()}
        report = {
            "schema_version": 1, "kind": "custom_engineering", "design_id": directory.parent.name,
            "revision": directory.name, "units": "mm", "brief": brief,
            "inputs": {name: hashlib.sha256(payload).hexdigest() for name, payload in inputs.items()},
            "review_sha256": reviewed_sha256, "artifacts": artifacts, "sha256": artifacts["model.stl"],
            "backend": {"name": "cadquery", "version": metadata.version("cadquery"),
                        "ocp_version": metadata.version("cadquery-ocp"),
                        "linear_tolerance_mm": 0.02, "angular_tolerance_radians": 0.1},
            "checks": checks, "acceptance_scope": "Dimensions/kernel/mesh/STEP checked. Other textual acceptance requires separate review; source checks run only if authored.",
            "validation": {"generated": True, "software_checked": True,
                           "slicer_checked": False, "physical_print_tested": False},
            "checker_sources": {name: source_hash(name) for name in
                                ("tools/designs.py", "tools/geometry.py", "tools/mesh_preview.py")},
            "state": "Prototype - not validated for hanging/load use",
            "limitations": ["Single-file trusted source only; external custom helpers/data are not captured.",
                            "Explicit source execution is not sandboxed; hash matching is not a security review.",
                            "One printable connected solid only; no assembly/import/edit/FEA capability implied.",
                            "Geometry checks do not certify printability, fit, material use or mechanical safety.",
                            "No actual printer/material profile is selected; slice/physical evidence is absent."],
        }
        (work / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        # Reserve the name before moving artifacts; never overwrite a published revision.
        output.mkdir()
        for path in work.iterdir():
            shutil.move(str(path), output / path.name)
    current = {"design_id": report["design_id"], "revision": report["revision"],
               "report_sha256": hashlib.sha256((output / "report.json").read_bytes()).hexdigest()}
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=directory.parent,
                                     prefix=".current-", delete=False) as handle:
        json.dump(current, handle)
        temporary = Path(handle.name)
    temporary.replace(_safe_path(directory.parent / "current.json"))
    return report


def run_design(source_file, make_shape):
    parser = argparse.ArgumentParser(description="Execute reviewed local CAD; this is not sandboxed.")
    parser.add_argument("--reviewed-sha256", required=True)
    args = parser.parse_args()
    print(json.dumps(publish_design(source_file, make_shape, args.reviewed_sha256), indent=2))


def _viewer(name):
    return f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(name)} | OpenPrintLab custom design</title>
<style>body{{font:16px system-ui;max-width:960px;margin:32px auto;padding:0 20px;background:#f7f6f2;color:#192b25}}
img{{width:100%;max-width:700px}} a{{display:inline-block;color:#215b47;margin-right:16px}} pre{{white-space:pre-wrap;overflow-wrap:anywhere}}
.notice{{padding:16px;background:#faefd9}} select{{font:inherit;padding:6px}}</style>
<h1>{escape(name)}</h1><p class="notice">Custom engineering. Not slicer-checked or physically print-tested.
Not validated for hanging/load use. The viewer cannot execute or edit source.</p>
<p id="status" role="status">Waiting for a published revision. Requires the local HTTP viewer for live updates.</p>
<p>Selection reference for your assistant: <strong id="reference">none</strong></p>
<p id="links"></p><img id="preview" alt="Actual exported geometry preview" hidden>
<pre id="details"></pre><noscript>JavaScript is needed to follow current.json; inspect the exported revision files directly.</noscript>
<script>
let version = "";
async function refresh() {{
 try {{
  const response = await fetch("current.json", {{cache:"no-store"}});
  if (!response.ok) throw Error(response.status === 404 ? "No published revision yet." : "Cannot read current revision.");
  const current = await response.json();
  if (!/^r[0-9]{{4}}$/.test(current.revision)) throw Error("Invalid revision record.");
  const key = current.revision + current.report_sha256;
  if (key !== version) {{
   const prefix = current.revision + "/output/";
   const r = await fetch(prefix + "report.json", {{cache:"no-store"}});
   if (!r.ok) throw Error("Revision report unavailable.");
   const text = await r.text();
   const hash = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(text)))).map(b=>b.toString(16).padStart(2,"0")).join("");
   if (hash !== current.report_sha256) throw Error("Report hash mismatch; not showing new revision.");
   const report = JSON.parse(text);
   document.getElementById("details").textContent = JSON.stringify({{dimensions_mm:report.checks.dimensions_mm, parameters:report.brief.parameters, checks:report.checks, limitations:report.limitations}},null,2);
   document.getElementById("reference").textContent = current.design_id + ":" + current.revision;
   const links = document.getElementById("links"); links.replaceChildren();
   for (const file of ["model.stl","model.step","source.py","brief.json","report.json"]) {{
    const a=document.createElement("a");a.href=prefix+file;a.textContent=file;a.setAttribute("download","");links.append(a);
   }}
   const img=document.getElementById("preview");img.src=prefix+"preview.svg";img.hidden=false;version=key;
  }}
  document.getElementById("status").textContent = "Showing " + current.revision + ". Watching for a newly published revision; your assistant performs edits.";
 }} catch (error) {{ document.getElementById("status").textContent = "Preview not current: " + error.message; }}
}}
refresh(); setInterval(refresh,2000);
</script></html>"""
