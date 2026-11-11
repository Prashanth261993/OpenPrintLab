# OpenPrintLab

**Small ideas. Real objects. Open tools.**

Download a simple model, learn to slice it, or use your AI coding assistant to
make it your own. Starting with **Bambu Lab P2S**, single-color PLA and no AMS
requirement. Independent community project, not affiliated with Bambu Lab.

**[Browse models & beginner guides](https://Prashanth261993.github.io/OpenPrintLab/)**

**New: [Template lab](https://prashanth261993.github.io/OpenPrintLab/lab/)** -
rounded organizers, multi-pen rests and lightweight paper-card stands.
Browse real geometry previews and examples, then use your own tool-capable
assistant to generate a new variant locally. No hosted AI or provider key.

> All four starter models are generated and software-checked. **None are
> slicer-checked or physically print-tested.** Review the slice yourself before
> printing. Suggested settings are starting points, not certified presets.

## Start with a download

| Model | Category | Size (mm) | Download |
|---|---|---|---|
| Pocket tray | Household | 96 x 64 x 16 | [STL](models/exports/pocket-tray.stl) |
| Two-pen rest | Desk | 70 x 38 x 8 | [STL](models/exports/pen-rest.stl) |
| Parts palette | Hobby | 108 x 60 x 14 | [STL](models/exports/parts-palette.stl) |
| Layer staircase | Learning | 48 x 24 x 16 | [STL](models/exports/step-study.stl) |

Use the **Download raw file** button when viewing an STL on GitHub, or use the
website's direct downloads. Each model page includes a geometry preview, source
ZIP, OpenSCAD snapshot, validation report and model-specific instructions.

1. Read the model's notes and download its STL.
2. Import in Bambu Studio. Select the actual **P2S**, installed nozzle, plate
   and PLA filament presets. Do not substitute P1S or assume AMS.
3. Place the broad base down, inspect dimensions, slice and inspect every layer.
4. Only then initiate the print yourself, following the manufacturer's guidance.

Read the [complete beginner guide](https://Prashanth261993.github.io/OpenPrintLab/beginner.html)
for suggested starting settings, first-layer checks, troubleshooting and safety.
No G-code is distributed and no tool controls a printer.

**Ready to test locally:** follow the [verified Windows walkthrough](docs/local-testing.md)
for the catalog preview, a 120 x 80 x 18 mm tray variant and a human Bambu Studio
smoke test. The local baseline needs no API key or provider installation.

## Create with an AI assistant

Clone this repository and open it in your coding assistant. Ask it to read
[`AGENTS.md`](AGENTS.md) and use the repository-local
[`create-printable-model` skill](.github/skills/create-printable-model/SKILL.md).
Supported clients discover `.github/skills`; otherwise explicitly tell your
assistant to read that file. No hosted AI service or repository API key is needed.
Your assistant's own subscription and policies still apply.

Example: "Customize pocket-tray to 120 x 80 x 18 mm for dry craft parts,
keeping 2.4 mm walls and a 2 mm base. Validate and export to build/my-tray.
Do not claim a print test or control my printer."

Python 3.11+ is sufficient for the core workflow, with **no dependencies**:

```shell
python -m tools.cli list
python -m tools.cli parameters pocket-tray
python -m tools.cli check pocket-tray --set length=120 --set width=80 --set height=18
python -m tools.cli build pocket-tray --set length=120 --set width=80 --set height=18 --output build/my-tray
```

Run from the repository root. Outputs include an STL and a JSON report. Repeated
exports to the same directory replace that model's files. Parameters are in mm,
except integer counts. Unknown, nonfinite, out-of-range and geometrically
inconsistent parameters are rejected. Default metadata notes describe default
sizes only; re-evaluate a variant.

The original designs use explicit box-union recipes in `models/recipes.py` and
parameters in `models/catalog.json`. This intentionally limited, open-source
parametric CAD approach keeps builds reproducible without a large CAD install.
It supports orthogonal solids, not curved or organic modeling. Exported `.scad`
snapshots can be inspected with OpenSCAD; editable Python recipes remain the
source of truth.

### Give your assistant instructions and see the result

The [template-lab walkthrough](docs/template-lab.md) covers the complete local
flow, supported edits, exact prompts, setup advice and client limitations.
Your assistant interprets the request; our shared CLI/MCP deterministically
validates and builds it. A generic model/chat page without tool access cannot
execute this workflow.

```powershell
python -m venv .venv-cadquery
.\.venv-cadquery\Scripts\python.exe -m pip install -e ".[cadquery,mcp,test]" -c experiments\cadquery\constraints.txt
.\.venv-cadquery\Scripts\python.exe -m tools.cli customize rounded-organizer --variant my-desk-organizer --set length=120 --set width=80 --set height=18 --set compartments=3 --set radius=8
python -m tools.lab --port 8766
```

Open `http://127.0.0.1:8766/my-desk-organizer/` for the actual STL-derived geometry,
STL/STEP downloads, editable source and variant passport. Existing variant names
are refused, never overwritten; request a new name for revisions. The viewer
also shows three public examples without requiring CadQuery to be installed.
CAD generation is opt-in and adds a substantial native dependency footprint;
the original four models remain dependency-free.

Example prompt: "Use create-printable-model to make a 120 x 80 x 18 mm organizer
for dry desk bits, three compartments, 8 mm corners, 2.4 mm walls and 2 mm base.
Preserve the original and show the preview and downloads. Ask for my actual
hardware before recommending settings."

Names/text, arbitrary sculpting and external STL/STEP/3MF editing are deferred.
No browser chatbot, paid generation or printer automation is implied.

### Optional MCP

Install in a virtual environment from this trusted clone:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[mcp]"
.\.venv\Scripts\python.exe -m tools.mcp_server
```

On macOS/Linux use `.venv/bin/python`. This starts a **stdio** server, not a web
service. Configure your MCP client to launch that Python command with
`["-m", "tools.mcp_server"]` and this clone as its working directory. Use an
absolute Python path. See the [creator guide](https://Prashanth261993.github.io/OpenPrintLab/create.html)
for a full JSON configuration example.

Original tools: `list_models`, `describe_model`, `check_model`, `export_model`.
Template tools: `list_templates`, `describe_template`, `create_variant`,
`variant_guidance`. For CAD generation, configure the same server with the
`.venv-cadquery` interpreter and add `--cadquery` to the server arguments; no
separate provider wrapper is needed. Native CAD initializes before the async
server starts; the default server stays builtin-only.
Exports are confined to `build/mcp`, overwriting the previous export for that
model. CLI and MCP share validation and generation logic. No arbitrary commands,
arbitrary output paths, network or printer controls are exposed. Enable tool
approval in your client and review exports before slicing.

## Build, check and contribute

```shell
python -m unittest discover -s tests -v
python -m tools.release
python -m tools.release --check
python -m tools.site
python -m http.server 8000 --directory site --bind 127.0.0.1
```

Open `http://127.0.0.1:8000`. `release` regenerates committed default STL, report,
SVG and OpenSCAD files; `--check` detects stale or extra outputs without writing.
`site` requires consistent exports and generates the deployable `site/` folder.

For browser and MCP integration checks, install optional dependencies:

```shell
python -m pip install -e ".[mcp,test]"
python -m playwright install chromium
python -m tests.mcp_smoke
python -m tests.browser_smoke
```

The browser check starts and stops its own local server. GitHub Actions runs
unit, integrity, browser and MCP checks before deploying main to GitHub Pages;
pull requests are checked without deployment. No third-party model files,
runtime CDNs, tracking, paid APIs or printer credentials are required.

See [scope and acceptance decisions](docs/decisions.md) and the
[creator guide source](docs/create.html). Contributions should include dimensions,
constraints, source, reproducible exports and evidence, not just screenshots.

### What a check actually means

- **Generated:** a real STL was exported from a known recipe.
- **Software-checked:** exported triangles passed the documented finite-coordinate,
  edge closure/winding, connectivity, nondegeneracy, positive-volume and envelope checks.
- **Slicer-checked:** requires a documented human slice review. **Not performed.**
- **Physical-print-tested:** requires an actual documented print. **Not performed.**

These are limited checks, not a general self-intersection/repair algorithm,
fit guarantee, strength rating or safety certification. Never use starter models
for food contact, electrical, medical, weapon, structural, hot or safety-critical
applications. All process suggestions must be reviewed against the actual setup.

### Model passports and real feedback

Each report includes model version, effective parameters/dimensions, a variant ID,
editable-source hashes, exact STL SHA-256, design license and a separately labeled
suggested printer recipe. Geometry evidence is generated afresh for every export.
Slicer and physical records remain `not_performed`, with null actual settings;
successful evidence from a different variant is never inherited.

Use the [print-result issue form](https://github.com/Prashanth261993/OpenPrintLab/issues/new?template=print-result.yml)
to share successes, partial successes, failures or a trial stopped before printing.
Include the passport IDs, actual setup and photos/screenshots when available.
Reports are public: remove private details and credentials. A user report is not
automatic certification or status promotion.

### Technology reuse plan

The current [repository roadmap and reuse backlog](devtool/features/004-reuse-roadmap/plan.md)
tracks controlled new-design authoring, P2S project-3MF plus real slicer review,
cross-assistant packages, reusable evidence-backed patterns, OpenSCAD/assembly
workflows and additional checks. **Tracked does not mean implemented or approved
to build.** Sources, priorities, dependencies and evidence gates are recorded.
The [frame A/B benchmark](evals/frame-shadowbox-24x36/README.md) now has a frozen
common brief, rubric, protocol and exact actual launch prompts. The coordinator
has launched the two fresh sessions; this administrative update creates no designs,
launches no agents and does not inspect running candidates.

[plan.md](plan.md) records requirements, owned files, dependencies, uncertainty,
verification commands and approval gates. It distinguishes **precise functional
CAD** (the shipped, limited local path) from **decorative AI meshes** (future opt-in).
The [isolated CadQuery tray experiment](experiments/cadquery/README.md) retains
its original Windows/Linux evidence. The user subsequently approved the bounded
optional backend and template lab, tracked separately in
[milestone 003](devtool/features/003-template-lab/plan.md). This is not a wholesale
catalog migration; the historical 002 plan and experiment report are preserved.

The plan evaluates reuse of Meshy's official MCP/skill, and defers community
FreeCAD/Blender bridges, Zoo/KCL and Tripo until justified. No provider keys,
installations or paid API calls are enabled by this plan. Only the explicitly
approved CAD environments are opt-in. The no-key V1 baseline stays working.
Real P2S test-print evidence, certified profiles, imported-model editing and
additional providers remain roadmap items, not shipped claims.

## Licenses

[MIT](LICENSE): build tooling, website code, tests, integrations and configuration.
[CC BY 4.0](LICENSE-CONTENT.md): original models, **editable design source
including `models/recipes.py`**, previews, catalog content, README and guides.
Keep attribution and indicate modifications. Third-party manufacturer pages and
trademarks are not relicensed.

Hardware facts are sourced from the [official P2S specifications](https://bambulab.com/en/p2s/specs),
checked November 10, 2026. Machine-specific help: [official P2S wiki](https://wiki.bambulab.com/en/p2s).
