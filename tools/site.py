"""Build a static, subpath-safe website from the checked catalog."""

from html import escape
from pathlib import Path
import shutil

from tools.catalog import ROOT, build_model, load_catalog, parameter_schema, source_archive
from tools.release import release
from tools.lab import seed_examples


def page(title, body, prefix=""):
    template = (ROOT / "web" / "page.html").read_text(encoding="utf-8")
    return template.replace("%%TITLE%%", escape(title)).replace("%%ROOT%%", prefix).replace("%%BODY%%", body)


def dimensions(report):
    return " &times; ".join(f"{v:g}" for v in report["checks"]["dimensions_mm"]) + " mm"


def card(model, report, index):
    identifier = model["id"]
    name = escape(model["name"])
    search = escape(" ".join([model["name"], model["summary"], model["category"], *model["tags"]]).lower(), quote=True)
    return f"""<article class="model-card" data-search="{search}" data-category="{escape(model['category'])}">
      <a class="model-image" href="models/{identifier}.html" aria-label="View {name}">
      <span class="image-label">MODEL / 0{index}</span>
      <img src="downloads/{identifier}.svg" width="700" height="460" loading="lazy" alt="{name}: generated geometry, not a print photo"></a>
      <div class="model-body"><div class="model-heading"><h3><a href="models/{identifier}.html">{name}</a></h3><span class="category-tag">{escape(model['category'])}</span></div>
      <p>{escape(model['summary'])}</p><div class="model-meta"><span>{dimensions(report)}</span><span>PLA / 1 color</span></div>
      <span class="state yes">Software-checked</span><p class="small">Not slicer-checked or print-tested</p>
      <div class="model-actions"><a href="models/{identifier}.html">Details &amp; print guide <span aria-hidden="true">&nbsp;&#8594;</span></a>
      <a class="download" href="downloads/{identifier}.stl" download aria-label="Download {name} STL">STL <span aria-hidden="true">&#8595;</span></a></div></div></article>"""


def detail(model, report):
    identifier = model["id"]
    rows = "".join(
        f"<tr><td>{escape(name)}</td><td>{rule['default']:g} {rule['unit']}</td><td>{rule['minimum']:g} to {rule['maximum']:g}</td></tr>"
        for name, rule in parameter_schema(identifier).items()
    )
    return f"""<div class="wrap detail"><a class="breadcrumb" href="../index.html#catalog">&#8592; Back to the collection</a>
    <div class="detail-hero"><figure class="detail-image"><img src="../downloads/{identifier}.svg" width="700" height="460" alt="{escape(model['name'])} generated geometry">
    <figcaption>Generated from the exported STL. Not a physical-print photo.</figcaption></figure>
    <div><p class="eyebrow">{escape(model['category']).upper()} / ORIGINAL DESIGN</p><h1>{escape(model['name'])}</h1>
    <p class="lede">{escape(model['summary'])}</p><p><strong>{dimensions(report)}</strong><br>Version {escape(model['version'])} &middot; millimeters &middot; single-color PLA</p>
    <a class="button primary" href="../downloads/{identifier}.stl" download>Download STL <span aria-hidden="true">&#8595;</span></a>
    <div class="detail-links"><a href="../downloads/{identifier}.source.zip" download>Editable source ZIP</a><a href="../downloads/{identifier}.scad" download>OpenSCAD snapshot</a><a href="../downloads/{identifier}.report.json">Model passport &amp; report</a></div>
    <aside class="notice"><strong>Not slicer-checked or physically print-tested.</strong> Review the slice before printing. No fit, time, material-use or strength claims.</aside></div></div>
    <div class="detail-columns"><section><h2>Place it on the plate</h2><p>{escape(model['notes'])}</p>
    <h2>Suggested starting points</h2><p>For PLA and an actual 0.4 mm nozzle: a compatible 0.20 mm layer-height process, 3 wall loops, 4 top and 4 bottom shell layers, 15% infill. Start base-down with supports off and no brim, then inspect the slice. These are suggestions, <strong>not certified presets</strong>.</p>
    <p>Select the actual <strong>Bambu Lab P2S</strong>, installed nozzle, build plate and filament presets in Bambu Studio. Use their temperature and speed defaults. No AMS is required. Check dimensions, first-layer contact, shell closure, overhangs and all warnings before initiating a print yourself.</p>
    <a class="button secondary" href="../beginner.html">Full beginner printing guide &#8594;</a>
    <h2>Use it thoughtfully</h2><p>For light, non-critical organization or learning only. Not for food, heat, electrical, medical, structural, weapon or safety-critical use. Follow the printer manufacturer's safety and ventilation guidance.</p></section>
    <section><h2>Make it your own</h2><p>{escape(model['customize'])}</p>
    <table><thead><tr><th>Parameter</th><th>Default</th><th>Allowed range</th></tr></thead><tbody>{rows}</tbody></table>
    <p>Additional relationship checks apply. Model notes describe the default dimensions; re-check clearances for variants.</p>
    <pre><code>python -m tools.cli parameters {identifier}
python -m tools.cli build {identifier} --output build/my-variant</code></pre>
    <p><a href="../create.html">Learn the AI-assisted creation workflow &#8594;</a></p>
    <h2>What we checked</h2><ul class="checks-list"><li>Generated: yes</li><li>Software checks: passed on the exported STL</li><li>Slicer review: not performed</li><li>Physical print: not performed</li></ul>
    <p>{report['checks']['triangles']} triangles. Closed, consistently wound edges; finite, nondegenerate faces; connected mesh; positive volume; Z=0 placement within the P2S build envelope. These limited checks do not prove printability or detect every possible geometry defect.</p>
    <p class="small">STL SHA-256: <code>{report['sha256']}</code></p>
    <p class="small">Variant ID: <code>{report['passport']['variant_id']}</code><br>Suggested recipe: <code>{escape(report['passport']['suggested_print_recipe']['id'])}</code> (unverified). Exact design-source hashes and separate evidence scope are in the passport.</p>
    <p><a href="https://github.com/Prashanth261993/OpenPrintLab/issues/new?template=print-result.yml">Share a print result: successes and failures welcome &#8594;</a></p>
    <p class="small">Include model version, variant ID, STL hash and actual settings. Public reports are observations, not automatic certification.</p>
    <p class="small">Original design by OpenPrintLab contributors. <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>; keep attribution and indicate changes. Tooling code has a separate MIT license.</p></section></div></div>"""


def build_site(destination=None):
    release(check=True)
    directory = Path(destination) if destination else ROOT / "site"
    for subdir in ("assets", "downloads", "models"):
        (directory / subdir).mkdir(parents=True, exist_ok=True)
    for filename in ("style.css", "catalog.js", "favicon.svg"):
        shutil.copyfile(ROOT / "web" / filename, directory / "assets" / filename)
    cards = []
    for index, model in enumerate(load_catalog()["models"], 1):
        identifier = model["id"]
        _, report = build_model(identifier)
        for suffix in (".stl", ".svg", ".report.json", ".scad"):
            shutil.copyfile(ROOT / "models" / "exports" / f"{identifier}{suffix}", directory / "downloads" / f"{identifier}{suffix}")
        source_archive(identifier, directory / "downloads" / f"{identifier}.source.zip")
        (directory / "models" / f"{identifier}.html").write_text(page(model["name"], detail(model, report), "../"), encoding="utf-8")
        cards.append(card(model, report, index))
    home = (ROOT / "web" / "home.html").read_text(encoding="utf-8").replace("%%CARDS%%", "\n".join(cards))
    (directory / "index.html").write_text(page("Small ideas. Real objects.", home), encoding="utf-8")
    for name, title in (("beginner", "Your first print"), ("create", "Create with AI")):
        body = (ROOT / "docs" / f"{name}.html").read_text(encoding="utf-8")
        (directory / f"{name}.html").write_text(page(title, f'<article class="wrap article">{body}</article>'), encoding="utf-8")
    (directory / ".nojekyll").write_text("", encoding="utf-8")
    seed_examples(directory / "lab", refresh_curated=True)
    print(f"Built {len(cards)} model pages and guides in {directory}")


if __name__ == "__main__":
    build_site()
