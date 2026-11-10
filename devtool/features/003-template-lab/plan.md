---
artifact: plan
feature: 003-template-lab
status: complete
updated: 2026-11-10
tasks: [T-01, T-02, T-03, T-04, T-05]
---

# 003 - Own-assistant editable template lab

## Objective

Implement the user's newly approved bounded optional CadQuery/template milestone.
This supersedes the earlier plan-only hold for this milestone, not the refusal
to enable paid providers or migrate the original catalog. Historical 002/T-05
requirements, task states and evidence remain in the root documents.

## Current state

Existing walking skeleton: four no-dependency models, versioned passports,
local preview, real CLI/MCP and a successful isolated CadQuery trial on Windows
and Linux. The original 16 artifacts were rechecked at milestone start.
The three generators, non-destructive variants, CLI/MCP, grounded guidance and
local lab now pass local checks. A real custom organizer is visible at
`http://127.0.0.1:8766/my-desk-organizer-v2/`; the earlier variant was preserved.
The optional lab is published. Both Linux optional-backend and baseline/Pages
checks passed. Pages deployment is gated on both suites, while the baseline
suite deliberately runs without CadQuery. No physical or slicer test is claimed.

## Phases

- [x] Discover - `requirements.md`; approved priority and implementation update.
- [x] Design - bounded contract and tradeoffs below.
- [x] Plan - sequential task table.
- [x] Build.
- [x] Verify and publish.
- Red-team - not commissioned; ordinary focused checks still apply.

## Tasks

| ID | Task | Req | Depends on | Files owned | Parallel group | State | Verification |
|----|------|-----|-----------|-------------|----------------|-------|--------------|
| T-01 | Extend the existing walking skeleton with non-destructive variants and real previews | R-02, R-03 | - | `tools/variants.py`, `tools/lab.py`, `tests/test_variants.py` | - | done | `python -m unittest tests.test_variants -v` passed; `python -m tools.lab --port 8766` implemented |
| T-02 | Add the optional CAD backend and three bounded template families | R-01, R-02, R-06 | T-01 | `models/templates.json`, `models/cadquery_templates.py`, `tools/variants.py`, `tools/template_examples.py`, `pyproject.toml`, `.gitignore`, `tests/test_cadquery_templates.py`, `examples/template-lab/*` | - | done | `.venv-cadquery\Scripts\python.exe -m unittest tests.test_cadquery_templates -v`; curated exports generated and hash/source checked |
| T-03 | Wire shared CLI/MCP and model-aware setup guidance | R-04, R-05 | T-02 | `tools/cli.py`, `tools/mcp_server.py`, `tools/variants.py`, `tests/mcp_smoke.py`, `tests/test_variants.py`, `AGENTS.md`, `.github/skills/create-printable-model/SKILL.md` | - | done | `.venv-cadquery\Scripts\python.exe -m tests.mcp_smoke`; `python -m unittest tests.test_variants -v` passed |
| T-04 | Ship the local lab journey and exact prompt/run documentation | R-03, R-04, R-05 | T-03 | `README.md`, `docs/template-lab.md`, `docs/create.html`, `tools/lab.py`, `tools/mesh_preview.py`, `tests/test_mesh_preview.py`, `tests/lab_browser_smoke.py`, `LICENSE-CONTENT.md` | - | done | `.venv-cadquery\Scripts\python.exe -m tests.lab_browser_smoke` passed; real custom preview/downloads verified |
| T-05 | Verify on Windows/Linux, publish and report local readiness | R-01, R-02, R-03, R-04, R-05, R-06 | T-04 | `.github/workflows/template-lab.yml`, `.github/workflows/pages.yml`, `requirements.md`, `plan.md`, `devtool/features/003-template-lab/*` | - | done | `python -m unittest discover -s tests -v`; CAD suite; `python -m tools.release --check`; live local HTTP/hashes; [optional CI](https://github.com/Prashanth261993/OpenPrintLab/actions/runs/42925559346), [baseline/Pages](https://github.com/Prashanth261993/OpenPrintLab/actions/runs/42925559317) passed |

No parallel groups: shared pipeline/CLI files make these tasks sequential.
Commands marked planned are contracts, not claims that those modules exist yet.
The first task extends the runnable existing skeleton rather than starting with
an unrelated framework or database.

## Design and complete demonstrable journey

1. Browse three original templates in a local static lab. Read dimensions,
   allowed operations, previews and limits.
2. Tell a tool-capable assistant, for example: "Make a 120 x 80 x 18 mm organizer
   for dry desk bits, three compartments, 8 mm rounded corners, 2.4 mm walls and
   a 2 mm base. Preserve the original and show me the geometry and downloads."
3. The assistant reads the skill/schema, asks for missing constraints and chooses
   the supported generator. There is no fake natural-language parser.
4. Shared tools validate and create a fresh named directory, producing actual
   geometry, SVG preview, HTML viewer, STL, optional STEP, source ZIP and report.
5. The assistant opens/links the real preview, reports exact identity, and asks
   for actual setup before offering bounded, cited starting suggestions.
6. User opens the exact STL in Bambu Studio and manually reviews dimensions,
   orientation, layer continuity and warnings. Physical testing remains pending.

### Reuse and scope

- Keep all existing `build/check/list` behavior and original files intact.
- Reuse original tray/rest concepts, T-05 rounded-box/cavity operations, existing
  mesh validator and geometry-derived SVG renderer. Keep historical experiment
  evidence intact; it is not the production runtime's mutable state.
- One shared variant implementation serves CLI and MCP; no client-specific plugin
  matrix or duplicate geometry logic.
- Optional CadQuery is imported only for CAD templates. No silent fallback, repair,
  auto-install or global PATH change. Dedicated `.venv-cadquery` for local use.
- Browser scope is static template/result browsing. No hosted chatbot,
  browser CAD editing, external-file upload or automatic printing.
- Custom results stay under ignored `build/variants`; only deliberately generated
  public examples are committed. Path-safe variant names and exclusive creation
  protect originals; MCP uses the fixed output root, not arbitrary supplied paths.
- Parameter/source/backend/STL identity invalidates evidence after edits.
  STEP hashes are recorded separately because timestamps and tessellation can vary.

## Template feasibility and constraints

| Family | First bounded operations | Reuse / limits |
|---|---|---|
| Rounded organizer | Dimensions, wall/base, compartment count, corner radius | T-05 tray + existing divider idea; minimum compartment width and rounded-corner clearance must be checked |
| Rounded pen rest | Dimensions, wall/base, channel count, corner radius | Existing rest concept; channels remain open-ended, minimum width; no clip/friction-fit promise |
| Paper-card slot stand | Dimensions, slot width/base depth, corner radius | Simple subtractive slot in a rounded block; for lightweight paper only, not phones, structural loads or safety-critical use |
| Text nameplate | Deferred | Text API exists; a specific redistributable font binary, glyph bounds, embedding notices and Windows/Linux geometry still need validation |

Source reviewed: CadQuery 2.8.0 `Workplane.text` exposes explicit `fontPath`.
[Noto Sans OFL declaration](https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/OFL.txt)
was read on 2026-11-10. This is feasibility evidence, not permission to pretend
font packaging or text modeling is implemented.

## Risks, uncertainty and acceptance gates

| Task | Uncertainty | Gate |
|---|---|---|
| T-01 | known | Existing output collision must fail; no changed originals; preview must derive from exported mesh |
| T-02 | unclear | Windows/Linux valid single solids, positive volume, dimensions/envelope, closed oriented mesh; conditional missing dependency error; no default CAD imports |
| T-03 | unclear | Actual stdio calls and CLI exercise same functions; incomplete hardware yields clarification, unsupported setup no invented profile |
| T-04 | known | Real demo links download exact checked bytes; keyboard/mobile viewer usable; no client compatibility claims without recorded tests |
| T-05 | known | All 16 old artifacts unchanged, baseline suite passes without CAD, optional suite passes with CAD, local server responsive |

T-05 measured ~1.21 GB and 45 installed distributions. Package/native licenses
and cross-platform triangulation differences remain relevant; keep pins and
engine/export settings in reports. Optional installation needs user/client
permission. The user's assistant subscription and privacy terms are separate
from OpenPrintLab; geometry can run locally even when their assistant is hosted.

## Local-ready demo contract

From the clone root, after optional setup:

```powershell
python -m venv .venv-cadquery
.\.venv-cadquery\Scripts\python.exe -m pip install -e ".[cadquery,mcp,test]" -c experiments\cadquery\constraints.txt
.\.venv-cadquery\Scripts\python.exe -m tools.cli customize rounded-organizer --variant my-desk-organizer --set length=120 --set width=80 --set height=18 --set compartments=3 --set radius=8
python -m tools.lab --port 8766
```

These commands have now been implemented and exercised locally. Preview:
`http://127.0.0.1:8766/my-desk-organizer/`, with actual SVG, STL, STEP, source and
report. The lab can browse committed examples without CadQuery. The existing
catalog on port 8765 remains separate. Customization occurs through the assistant
and local tools, not by typing into a nonexistent website AI box.

## Open questions

No blocking decision remains after the explicit implementation approval.
Actual printer/nozzle/plate/material/use are requested when guidance is asked.
Nameplates, arbitrary import, paid providers, browser editing and physical testing
are deferred, not silently added to this milestone.

## Verification notes and resolved findings

- Baseline suite: 20 tests, with the two CAD-only cases explicitly skipped in the
  no-CAD interpreter; optional geometry tests passed in the CAD interpreter.
- Original 16 export files and original recipe/mesh/SVG code remain unchanged.
- Real MCP stdio CAD generation, overwrite refusal, strict numeric rejection and
  guidance calls passed. Client UIs are not individually certified.
- Windows native NumPy/VTK initialization stalled when first invoked inside the
  running MCP event loop. Explicit `--cadquery` startup pre-initializes the
  optional stack before serving; the default MCP server stays builtin-only.
- Centroid-sorted SVG faces could mis-occlude curved models. New variant previews
  use a dependency-free depth buffer with a draw-order/occlusion regression test.
  The original gallery renderer/artifacts were not altered.
- Browser checks cover the actual geometry image, STL/STEP byte hashes,
  passport links, three families, keyboard and 375px/landscape layouts.
- The optional Linux job runs the full unit suite with CAD, actual MCP CAD calls
  and the browser journey. The separate baseline run passes without installing CAD.
- Curated references are regenerated with `python -m tools.template_examples`
  in the optional environment. This intentionally refreshes only public examples;
  ordinary `customize` never overwrites private variants.
- A dedicated output-root guard also refuses an unrelated existing `index.html`;
  a variant export cannot overwrite another local site's landing page.

## Links

- [Requirements](requirements.md)
- [Historical 002 plan](../../../plan.md)
- [T-05 evidence](../../../experiments/cadquery/report.md)
