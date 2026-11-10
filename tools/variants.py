"""Shared non-destructive variants and local preview surfaces. MIT license."""

from html import escape
import hashlib
import importlib
from importlib import metadata
import json
import math
from pathlib import Path
import re
import shutil
import tempfile
import zipfile

from tools.catalog import ROOT, build_model, canonical_hash, load_catalog, parameter_schema, source_archive, source_hash
from tools.geometry import decode_stl, validate_mesh
from tools.mesh_preview import render_svg

DEFAULT_OUTPUT = ROOT / "build" / "variants"
GUIDE = "https://prashanth261993.github.io/OpenPrintLab/beginner.html"


def safe_name(name):
    if not isinstance(name, str) or len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Variant name must be 1-64 lowercase letters/digits with single hyphens")
    if name in {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}:
        raise ValueError("Variant name is reserved by Windows; choose another name")
    return name


def list_templates():
    builtins = [
        dict(model, backend="builtin", parameter_schema=parameter_schema(model["id"]))
        for model in load_catalog()["models"]
    ]
    document = json.loads((ROOT / "models" / "templates.json").read_text(encoding="utf-8"))
    if document["schema_version"] != 1:
        raise ValueError("Unsupported template schema")
    templates = document["templates"]
    seen = {item["id"] for item in builtins}
    for template in templates:
        safe_name(template["id"])
        if template["id"] in seen or template["backend"] != "cadquery":
            raise ValueError("Duplicate template or unsupported backend")
        seen.add(template["id"])
        template["parameter_schema"] = {
            key: {"default": value, "minimum": template["limits"][key][0], "maximum": template["limits"][key][1],
                  "unit": "count" if key in template["counts"] else "mm"}
            for key, value in template["parameters"].items()
        }
    return builtins + templates


def describe_template(identifier):
    for template in list_templates():
        if template["id"] == identifier:
            return template
    raise ValueError(f"Unknown template: {identifier}")


def _generate(template, name, overrides, directory):
    if template["backend"] == "cadquery":
        return _generate_cadquery(template, name, overrides, directory)
    data, report = build_model(template["id"], overrides)
    filename = f"{name}.stl"
    (directory / filename).write_bytes(data)
    source_archive(template["id"], directory / "source.zip")
    report["backend"] = {"name": "builtin", "version": "1", "step_supported": False}
    report["artifacts"] = {"stl": filename, "stl_sha256": report["sha256"], "step": None}
    return data, report


def _cadquery():
    try:
        return importlib.import_module("cadquery")
    except ModuleNotFoundError as exc:
        message = (
            "Optional CadQuery backend is not installed or is incomplete. "
            'Create .venv-cadquery and run its Python with: -m pip install -e ".[cadquery]" '
            "-c experiments/cadquery/constraints.txt . Then run this command with that interpreter. "
            "The original builtin build command does not need CadQuery."
        )
        raise ValueError(message) from exc


def _generate_cadquery(template, name, overrides, directory):
    from models.cadquery_templates import make_shape, validate_relations
    parameters = template["parameters"] | overrides
    if set(parameters) != set(template["parameters"]):
        raise ValueError(f"Expected parameters: {', '.join(template['parameters'])}")
    for key, value in parameters.items():
        low, high = template["limits"][key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f"{key} must be a finite number between {low} and {high}")
        if key in template["counts"] and int(value) != value:
            raise ValueError(f"{key} must be a whole number")
    validate_relations(template["id"], parameters)
    cq = _cadquery()
    shape = make_shape(template["id"], parameters, cq)
    if not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 0:
        raise ValueError("CAD output must be one valid positive-volume solid")
    stl, step = directory / f"{name}.stl", directory / f"{name}.step"
    shape.exportStl(str(stl), tolerance=0.02, angularTolerance=0.1, ascii=False, relative=False, parallel=False)
    cq.exporters.export(shape, str(step))
    data = stl.read_bytes()
    checks = validate_mesh(decode_stl(data))
    if any(abs(actual - parameters[key]) > 0.05 for actual, key in zip(checks["dimensions_mm"], ("length", "width", "height"))):
        raise ValueError("Export dimensions differ from requested dimensions by more than 0.05 mm")
    volume_error = abs(checks["volume_mm3"] - shape.Volume()) / shape.Volume() * 100
    if volume_error > 0.5:
        raise ValueError("Export mesh volume differs from kernel volume by more than 0.5%")
    imported = cq.importers.importStep(str(step)).val()
    if not imported.isValid() or len(imported.Solids()) != 1 or abs(imported.Volume() - shape.Volume()) / shape.Volume() > 0.00001:
        raise ValueError("STEP round-trip validation failed")
    checks.update(kernel_valid=True, solid_count=1, kernel_volume_mm3=shape.Volume(),
                  mesh_kernel_volume_error_percent=volume_error, step_roundtrip_valid=True)
    stl_hash = hashlib.sha256(data).hexdigest()
    backend = {
        "name": "cadquery", "version": metadata.version("cadquery"),
        "ocp_version": metadata.version("cadquery-ocp"),
        "linear_tolerance_mm": 0.02, "angular_tolerance_radians": 0.1,
        "relative": False, "parallel": False, "step_supported": True,
    }
    source = {"recipe_path": "models/cadquery_templates.py", "recipe_sha256": source_hash("models/cadquery_templates.py"),
              "catalog_path": "models/templates.json", "catalog_entry_sha256": canonical_hash(template)}
    variant_id = canonical_hash({"template": template["id"], "version": template["version"], "source": source,
                                 "parameters": {k: float(v) for k, v in parameters.items()}, "backend": backend, "stl_sha256": stl_hash})
    report = {
        "model": template["id"], "units": "mm", "parameters": parameters, "sha256": stl_hash, "backend": backend,
        "passport": {"schema_version": 1, "model_version": template["version"], "variant_id": variant_id,
                     "design_license": "CC-BY-4.0", "attribution": "OpenPrintLab contributors",
                     "editable_source": source, "suggested_print_recipe": load_catalog()["suggested_print_recipe"]},
        "evidence": {
            "scope": {"model_version": template["version"], "variant_id": variant_id, "stl_sha256": stl_hash},
            "geometry": {"status": "passed", "checker": "cadquery-brep-and-openprintlab-mesh", "checker_source_sha256": source_hash("tools/variants.py")},
            "slicer": {"status": "not_performed", "actual_settings": None, "record_url": None},
            "physical": {"status": "not_performed", "actual_settings": None, "record_url": None},
        },
        "validation": {"generated": True, "software_checked": True, "slicer_checked": False, "physical_print_tested": False},
        "checks": checks, "repair_operations": [],
        "artifacts": {"stl": stl.name, "stl_sha256": stl_hash, "step": step.name, "step_sha256": hashlib.sha256(step.read_bytes()).hexdigest()},
        "limitations": ["Geometry checks do not certify printability, fit or safety.", "STEP carries geometry, not Python parameter history.",
                        "Tessellation can vary by platform; keep the exact file hash.", "No slicer or physical test has been performed."],
    }
    with zipfile.ZipFile(directory / "source.zip", "w", zipfile.ZIP_DEFLATED) as bundle:
        for relative in ("models/cadquery_templates.py", "models/templates.json", "LICENSE", "LICENSE-CONTENT.md"):
            bundle.write(ROOT / relative, relative)
    return data, report


def _page(title, body):
    style = (ROOT / "web" / "style.css").read_text(encoding="utf-8")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)} | OpenPrintLab local lab</title><style>{style}
    .lab-header{{padding-block:24px;border-bottom:1px solid var(--line)}}
    .lab-body{{padding-block:40px}} .lab-card img{{width:100%;height:auto}}
    .lab-card{{padding:24px;background:var(--surface);border:1px solid var(--line);border-radius:12px}}
    .lab-body h1,.lab-card h2{{overflow-wrap:anywhere}}
    </style></head><body><a class="skip" href="#main">Skip to content</a>
    <header class="wrap lab-header"><a class="brand" href="../">OpenPrintLab / Template lab</a></header>
    <main class="wrap lab-body" id="main">{body}</main></body></html>"""


def render_variant(template, report):
    name = report["variant_name"]
    dimensions = " &times; ".join(f"{n:g}" for n in report["checks"]["dimensions_mm"])
    step = report["artifacts"].get("step")
    step_link = f'<a class="button secondary" href="{escape(step)}" download>Download STEP</a>' if step else ""
    rows = "".join(f"<tr><td>{escape(k)}</td><td>{escape(str(v))}</td></tr>" for k, v in report["parameters"].items())
    return _page(name, f"""
    <a class="breadcrumb" href="../">&#8592; All templates and variants</a>
    <p class="eyebrow">YOUR ASSISTANT INTERPRETS. LOCAL TOOLS BUILD.</p><h1>{escape(name)}</h1>
    <p class="lede">{escape(template['name'])} &middot; {dimensions} mm &middot; {escape(report['backend']['name'])}</p>
    <div class="detail-hero"><figure class="detail-image"><img src="preview.svg" width="700" height="460"
    alt="Actual exported geometry for {escape(name)}"><figcaption>Preview derived from this STL. Not a physical-print photo.</figcaption></figure>
    <section><h2>Inspect your result</h2><p>{escape(template['notes'])}</p>
    <div class="actions"><a class="button primary" href="{escape(report['artifacts']['stl'])}" download>Download STL</a>{step_link}</div>
    <div class="detail-links"><a href="source.zip" download>Editable source ZIP</a><a href="report.json">Variant passport</a><a href="parameters.json">Effective parameters</a></div>
    <aside class="notice"><strong>Geometry checked only.</strong> Not slicer-checked or physically print-tested.
    No time, fit, strength or material-use guarantees. Inspect the exact downloaded file in Bambu Studio.</aside>
    <p><a href="{GUIDE}">Manual slicer review and safety guide</a></p></section></div>
    <div class="detail-columns"><section><h2>Change it with your own assistant</h2>
    <p>This browser is a viewer, not a chatbot or CAD editor. Ask a tool-capable assistant to read the repository skill,
    describe this template, clarify your dimensions/use, and create a <strong>new</strong> named variant.</p>
    <pre><code>python -m tools.cli customize {escape(template['id'])} --variant another-name --set length=120</code></pre>
    <p>Supported aesthetics are defined operations such as rounding and compartment/channel counts.
    No arbitrary sculpting or external-file import. Originals and prior variants are preserved.</p>
    <h2>Setup questions come first</h2><p>Tell your assistant your actual printer, installed nozzle, plate,
    filament and intended use. The guidance tool asks for missing facts; it does not invent a tested profile.
    Suggested P2S/0.4 mm/PLA starting points remain unverified.</p></section>
    <section><h2>Parameters and identity</h2><table><thead><tr><th>Parameter</th><th>Value (mm, except counts)</th></tr></thead><tbody>{rows}</tbody></table>
    <p>Original: {escape(template['id'])}, version {escape(report['passport']['model_version'])}.
    Design: CC BY 4.0, OpenPrintLab contributors. Tooling: MIT.</p>
    <p class="small">Variant ID: <code>{report['passport']['variant_id']}</code></p>
    <p class="small">STL SHA-256: <code>{report['sha256']}</code></p>
    <p>Keep this passport with the exact export. Changed dimensions, source or backend get fresh checks,
    never inherited slice/physical evidence.</p></section></div>""")


def render_index(directory):
    directory = Path(directory)
    cards = []
    for path in sorted(directory.glob("*/report.json")):
        if path.parent.name.startswith(".variant-"):
            continue
        if path.parent.is_symlink():
            raise ValueError("Symlink variant directories are not supported")
        report = json.loads(path.read_text(encoding="utf-8"))
        name = safe_name(path.parent.name)
        if report["variant_name"] != name:
            raise ValueError(f"Variant directory/report mismatch: {name}")
        dims = " x ".join(f"{n:g}" for n in report["checks"]["dimensions_mm"])
        cards.append(f"""<article class="lab-card"><a href="{name}/"><img src="{name}/preview.svg" width="700" height="460"
        alt="Generated geometry: {name}"><h2>{escape(name)}</h2></a><p>{dims} mm &middot; {escape(report['backend']['name'])}</p>
        <p>Software-checked. Not slicer- or print-tested.</p><a class="button secondary" href="{name}/">Preview &amp; downloads &#8594;</a></article>""")
    body = f"""<p class="eyebrow">LOCAL, OPEN, BRING YOUR OWN ASSISTANT</p><h1>Your ideas. Your templates.</h1>
    <p class="lede">Choose an example, then tell your own tool-capable AI assistant what to change.
    It clarifies constraints and calls deterministic local tools. No hosted chatbot, API key or printer connection here.</p>
    <aside class="notice">This is a geometry viewer. New instructions belong in your assistant, not a nonexistent web prompt box.
    Ask it to use <code>create-printable-model</code> and return the new preview link. Refresh this page after generation.</aside>
    <div class="model-grid">{''.join(cards)}</div>
    <p><a href="{GUIDE}">Beginner printing guidance</a> &middot; Original designs: CC BY 4.0, OpenPrintLab contributors.</p>"""
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=directory, suffix=".tmp", delete=False) as handle:
        handle.write(_page("Template lab", body))
        temporary = Path(handle.name)
    temporary.replace(directory / "index.html")


def create_variant(identifier, name, overrides=None, output=None):
    safe_name(name)
    template = describe_template(identifier)
    directory = Path(output) if output is not None else DEFAULT_OUTPUT
    target = directory / name
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Variant '{name}' already exists; choose a new name. Nothing was overwritten.")
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".variant-", dir=directory) as temp:
        working = Path(temp)
        data, report = _generate(template, name, overrides or {}, working)
        report["variant_name"] = name
        report["parent_template"] = identifier
        report["original_parameters"] = template["parameters"]
        report["template_notes"] = template["notes"]
        report["allowed_uses"] = template.get("uses", ["desk-organization", "hobby-sorting", "learning"])
        if identifier == "rounded-pen-rest":
            p = report["parameters"]
            report["derived_dimensions"] = {"channel_width_mm": (p["width"] - (p["channels"] + 1) * p["wall"]) / p["channels"]}
        with zipfile.ZipFile(working / "source.zip", "a", zipfile.ZIP_DEFLATED) as bundle:
            bundle.writestr("parameters.json", json.dumps(report["parameters"], indent=2) + "\n")
            bundle.writestr("VARIANT.txt", f"Original template: {identifier}\nParameters: parameters.json\n"
                "For a validated rebuild, use the matching source in an OpenPrintLab clone:\n"
                f"python -m tools.cli customize {identifier} --variant new-name --params parameters.json\n"
                "Keep source/parameters together. Modified source needs fresh validation; do not inherit this export's evidence.\n")
        (working / "parameters.json").write_text(json.dumps(report["parameters"], indent=2) + "\n", encoding="utf-8")
        preview = render_svg(decode_stl(data), template["color"], name)
        (working / "preview.svg").write_bytes(preview.encode())
        report["preview"] = {"renderer": "orthographic-depth-buffer-v1",
                             "renderer_source_sha256": source_hash("tools/mesh_preview.py"),
                             "sha256": hashlib.sha256(preview.encode()).hexdigest()}
        (working / "index.html").write_text(render_variant(template, report), encoding="utf-8")
        (working / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        target.mkdir()  # Exclusive reservation: concurrent requests cannot overwrite.
        for path in sorted(working.iterdir(), key=lambda p: (p.name == "report.json", p.name)):
            shutil.copyfile(path, target / path.name)
    render_index(directory)
    return {
        "directory": str(target.resolve()), "preview": (target / "index.html").resolve().as_uri(),
        "relative_preview_url": f"/{name}/", "stl": str((target / report["artifacts"]["stl"]).resolve()),
        "step": str((target / report["artifacts"]["step"]).resolve()) if report["artifacts"].get("step") else None,
        "report": report,
    }


def guidance(name, setup, output=None):
    safe_name(name)
    root = Path(output) if output is not None else DEFAULT_OUTPUT
    if (root / name).is_symlink():
        raise ValueError("Symlink variant directories are not supported")
    report = json.loads((root / name / "report.json").read_text(encoding="utf-8"))
    required = ("printer", "nozzle_mm", "plate", "material", "use")
    missing = [key for key in required if key not in setup or setup[key] in ("", None)]
    base = {
        "variant_id": report["passport"]["variant_id"], "stl_sha256": report["sha256"],
        "model_notes": report["template_notes"],
        "sources": ["https://bambulab.com/en/p2s/specs", "https://wiki.bambulab.com/en/p2s"],
        "evidence": "Unverified starting suggestions only; not a slicer or physical test.",
    }
    if missing:
        return base | {"status": "needs_input", "missing": missing, "message": "Ask for the actual installed hardware, filament and intended use before choosing settings."}
    unsupported = []
    if setup["printer"] not in ("P2S", "Bambu Lab P2S"):
        unsupported.append("printer")
    if isinstance(setup["nozzle_mm"], bool) or setup["nozzle_mm"] != 0.4:
        unsupported.append("nozzle_mm")
    if setup["plate"] not in ("Textured PEI", "Smooth PEI", "Cool Plate SuperTack"):
        unsupported.append("plate")
    if setup["material"] != "PLA":
        unsupported.append("material")
    allowed_uses = report["allowed_uses"]
    if setup["use"] not in allowed_uses:
        unsupported.append("use")
    if unsupported:
        return base | {"status": "unsupported_setup", "unsupported": unsupported,
                       "message": "No model-specific preset is established for this setup/use. Consult manufacturer guidance; do not substitute defaults."}
    return base | {"status": "suggested_starting_points", "actual_setup_as_reported": setup,
                   "suggestions": report["passport"]["suggested_print_recipe"],
                   "next_step": "Select your actual presets, place the broad base down, inspect every layer and warning; only you initiate a print."}
