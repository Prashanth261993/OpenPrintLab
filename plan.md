---
artifact: plan
feature: 002-evidence-and-reuse
status: planning
updated: 2026-11-10
tasks: [T-01, T-02, T-03, T-04, T-05, T-06, T-07]
---

# 002 - Evidence-first models and staged technology reuse

## Objective

Make the working OpenPrintLab starter trustworthy and easy to test locally,
then reuse mature CAD and AI capabilities only where they earn their complexity.
This plan does **not** authorize external installation, paid calls or a CAD migration.
Small passport/feedback additions are approved; future integrations require review.

## Current state

V1 is a published, dependency-free walking skeleton: four original models,
parametric customization, STL exports, reports, source downloads, beginner guides,
static catalog, optional local MCP and automated Pages deployment. Local preview
and a customized tray have been verified; the coordinator received the local-ready
handoff before this roadmap was completed. Versioned passports, a feedback form
and distinct creation-path guidance are implemented and locally verified.
Future integration tasks are blocked pending user review; the plan is not a
claim that those integrations have shipped. **No model has been sliced or
physically printed.**

## Phases

- [x] Discover - `requirements.md`; user-approved priorities, no reopened scope.
- [x] Design - existing `docs/decisions.md` plus the bounded contract below.
- [ ] Plan - this task table; future integration decomposition awaits user review.
- [x] Build - approved small foundation additions only.
- [x] Verify - approved foundation only; commands and evidence below.
- Red-team - not commissioned; no separate adversarial review claimed.

## Tasks

| ID | Task | Req | Depends on | Files owned | Parallel group | State | Verification |
|----|------|-----|-----------|-------------|----------------|-------|--------------|
| T-01 | Preserve and hand off the local walking skeleton | R-01, R-03 | - | `docs/local-testing.md`, `README.md` | - | done | `python -m tools.site`; `python -m tools.cli build pocket-tray --set length=120 --set width=80 --set height=18 --output build\local-trial`; `python -m http.server 8765 --directory site --bind 127.0.0.1`; in a second terminal: `(Invoke-WebRequest http://127.0.0.1:8765/).StatusCode` |
| T-02 | Bind passports and fresh evidence scope to model versions and variants | R-02 | T-01 | `models/catalog.json`, `models/exports/*`, `tools/catalog.py`, `tools/site.py`, `tests/test_models.py`, `docs/create.html`, `AGENTS.md` | - | done | `python -m unittest tests.test_models -v`; `python -m tools.release`; `python -m tools.release --check` |
| T-03 | Add public success/failure feedback form and privacy/evidence instructions | R-04 | T-02 | `.github/ISSUE_TEMPLATE/print-result.yml`, `tests/test_feedback.py` | - | done | `python -m unittest tests.test_feedback -v`; authenticated users can inspect the published GitHub issue-form preview without submitting an issue |
| T-04 | Document separate creation paths and verify the foundation for publication | R-01, R-03, R-05, R-06 | T-02, T-03 | `README.md`, `docs/create.html`, `docs/decisions.md`, `requirements.md`, `plan.md` | - | done | `python -m unittest discover -s tests -v`; `python -m tools.release --check`; `.\.venv\Scripts\python.exe -m tests.mcp_smoke`; `.\.venv\Scripts\python.exe -m tests.browser_smoke` |
| T-05 | Proposed first experiment: isolated CadQuery tray with editable parameters and STEP/STL | R-02, R-05, R-06 | T-04, Q-1 approval | `experiments/cadquery/requirements.txt`, `experiments/cadquery/probe.py`, `experiments/cadquery/test_probe.py`, `experiments/cadquery/report.md` | - | blocked | Planned after approval: `experiments\cadquery\.venv\Scripts\python.exe -m unittest discover -s experiments\cadquery -p test_probe.py -v`; baseline: `python -m tools.release --check` |
| T-06 | Optional decorative-path trial reusing official Meshy tools, not a new wrapper | R-02, R-04, R-05, R-06 | T-04, Q-2 approval | `experiments/meshy/check_evidence.py`, `experiments/meshy/consent.json`, `experiments/meshy/evidence.json`, `experiments/meshy/report.md` | - | blocked | Planned after approval: `python experiments\meshy\check_evidence.py --consent experiments\meshy\consent.json --evidence experiments\meshy\evidence.json`; baseline: `python -m tools.release --check` |
| T-07 | Choose a next integration from evidence, or explicitly decline it | R-05, R-06 | T-05; T-06 only if commissioned | `docs/integration-decision.md`, `plan.md` | - | blocked | Planned after experiments: `git diff --check`; `python -m unittest discover -s tests -v`; user review of measured results against G-2/G-3 |

No parallel groups are scheduled. T-02 and T-04 share documentation, so execute
them sequentially. Future experiment directories are disjoint, but do not launch
parallel installations or paid trials merely because that is possible. Future
verification scripts above are **planned files, not existing capabilities**.

### Uncertainty and stop conditions

| Task | Uncertainty | Main risk / stop |
|---|---|---|
| T-01 | known | Stop if the documented no-dependency command fails or localhost is not responsive. |
| T-02 | known | Version-only labels can misattribute evidence; compare canonical parameter/source identity and exact STL hash. |
| T-03 | known | User reports are untrusted observations, not automatic certification; no required sensitive identifiers. |
| T-04 | known | Keep the distinction between shipped capabilities and proposed integrations unmistakable. |
| T-05 | risky | Windows/kernel packaging, determinism and topology may outweigh benefits; reject rather than migrate by default. |
| T-06 | risky | API cost, input privacy, output rights and repair losses may make the trial unacceptable. No consent means no calls. |
| T-07 | unclear | The best result may be to retain V1 and defer all new dependencies. |

## Walking-skeleton evidence

Baseline commits: `b6a387b54e86ec89459b633da847cf80e1a536b9` (V1),
`dfd0f4b00f2814c6d8a93566380be03c6a43a5f3` (mixed-license metadata).
[Baseline CI and Pages deployment](https://github.com/Prashanth261993/OpenPrintLab/actions/runs/42905502286)
passed on Linux; the same tests passed on Windows.

- Nine unit/integrity tests: analytical model volumes, parameter rejection,
  sampled variants, malformed meshes, export consistency and source-ZIP rebuild.
- Real MCP stdio discovery, metadata, checked customization, export and rejection.
- Browser search/category/empty/reset/URL/keyboard/download/no-JS checks,
  375/768/1440 widths and landscape layouts.
- Seven live pages and 30 linked resources returned HTTP 200; all four published
  STL files matched locally rebuilt bytes and report hashes.
- Local preview at `http://127.0.0.1:8765/` returned HTTP 200 on 2026-11-10.
  This is a readiness observation, not a guarantee the process runs forever.
- Custom tray: 120 x 80 x 18 mm, STL SHA-256
  `ae02cf730822a379f97760426f04d05baa102e53ca0922b1b8338aa6e4215cef`.

Follow-up verification on 2026-11-10: **11 unit/integrity tests passed**,
including passport identity/evidence separation and public feedback-form
requirements; deterministic export checks, real MCP stdio tests and browser
checks passed again. The original four STL files are unchanged; passports add
version/source/variant scope without pretending a new physical test occurred.

The local skeleton has no backing service or database to provision. Once built,
one `python -m http.server ...` command serves a visible, seeded catalog.
See [local testing](docs/local-testing.md). Do not hold this handoff for T-05/T-06.

## Foundation contract

Model versions start at `1.0.0`; version changes are maintainer-reviewed design
decisions, not inferred dates. A passport includes the model version, canonical
effective parameters, source hashes, design license, suggested recipe and STL
hash. Variant identity includes the original recipe hash and parameters, so
changing a dimension forces a distinct evidence scope even before a new catalog
version. Source hashing normalizes line endings to avoid Windows/Linux drift.

Geometry evidence is produced on each export. Slicer and physical evidence remain
`not_performed`, with null actual settings and records. Reports request exact
actual settings via GitHub forms, including slicer version, nozzle, plate,
filament, process, orientation, support/brim and any repair or scaling.
An issue is not automatically trusted, merged into a passport, or promoted to
print-tested. One test never covers all variants.

## Two creation paths

**Precise functional CAD:** dimensions, relationships, intended use and editable
source are authoritative. V1 supports simple orthogonal solids. Evaluate CadQuery
for curves/fillets/STEP before adding those features to our own mesh code.
Future tolerances require measured physical evidence, not just exact CAD numbers.

**Decorative AI meshes:** visual shape is the starting point, not dimensional
intent. Optional provider output must pass rights/privacy review, scale and
topology/thickness checks, conservative repair review and a human slicer review.
Do not silently treat an AI mesh as parametric CAD or promise universal
printability. This path is planned, not installed or live.

## Reuse decisions and sources

Sources checked or supplied by the coordinating research on 2026-11-10; recheck
versions, licenses, pricing and tool permissions before installation.

| Technology | Decision now | Choose if / decline if | Source |
|---|---|---|---|
| Existing V1 CLI, catalog, skill and local MCP | Adopt and retain as the no-key baseline | Every experiment must leave its tests, exports and downloads working. Decline any integration that forces provider credentials for basic use. | [Repository](https://github.com/Prashanth261993/OpenPrintLab), `docs/decisions.md` |
| CadQuery / OpenCascade | Evaluate first; reuse a mature kernel rather than extend custom meshing to curves | Choose if isolated Windows/Linux builds preserve parameters, valid solids and STEP/STL export with reviewed dependency licenses. Decline if installation cannot be reproduced, geometry fails G-2, or a broad migration is needed before value is demonstrated. | [CadQuery introduction](https://cadquery.readthedocs.io/en/latest/intro.html) |
| Meshy official MCP and skill | Evaluate later, opt-in; do not write a duplicate provider wrapper | Choose only with explicit account/privacy/output-license review and a credit cap. Decline if outputs cannot be shared under acceptable terms, data is sensitive, costs cannot be bounded, or repair destroys intended shape. Provider claims are not local evidence. | [Official AI integration docs](https://docs.meshy.ai/en/api/ai), [official MCP](https://github.com/meshy-dev/meshy-mcp-server), [official skill](https://github.com/meshy-dev/meshy-3d-agent) |
| FreeCAD MCP | Defer; community candidate for advanced CAD editing | Evaluate only when GUI editing provides concrete value beyond CadQuery. Decline unattended use without isolation and explicit approval of Python execution. Review addon/bridge permissions and licenses first. | [Community repository](https://github.com/neka-nat/freecad-mcp) |
| MCP for Blender | Defer; community candidate for decorative mesh inspection/repair | Evaluate only when a controlled editor workflow is needed. It exposes arbitrary Python execution; do not give it unattended access to private files or credentials. Decline if the execution surface cannot be isolated. Not an official Blender Foundation plugin. | [Canonical community repository](https://github.com/ahujasid/mcp-for-blender) |
| Zoo Design Studio / KCL | Defer, optional editable conversational-CAD evaluation | Choose if editable/versioned output can be exported and independently rebuilt with acceptable terms and costs. Decline if essential design history or portability is unavailable. Not a necessary dependency. | [Design Studio](https://zoo.dev/design-studio), [data management](https://zoo.dev/docs/zoo-design-studio/features/data-management) |
| Tripo | Defer; alternative decorative workflow, not a second initial provider | Reconsider only if Meshy trial evidence exposes a need and Tripo meets the same rights/privacy/cost/geometry gates. Decline duplicate integration without a measured benefit. | [Tripo FDM guide](https://www.tripo3d.ai/blog/tripo-fdm-3d-printing-guide) |
| MakerWorld profiles / Printables Makes | Adopt the evidence/feedback idea only | Record exact setup and both successes and failures. Do not copy their code, models, photos or profiles without permission and license review. | [MakerWorld](https://makerworld.com/), [Printables](https://www.printables.com/) |

Meshy's official documentation describes generation, task status/download,
real-world resizing, printability analysis/repair, splitting and slicer handoff.
These are **upstream capabilities**, not OpenPrintLab features. The official MCP
uses an API key and API credit operations. Its analysis tool is described as free,
but that does not authorize an account connection or imply every operation is free.
The official skill can use the API directly; choose one integration route, not both
by default. A slicer handoff is not permission to print.

## First bounded integration experiment: T-05

Only after Q-1 approval, create an isolated CadQuery environment under its
experiment directory. Do not change the default catalog, core dependencies or
local MCP tools.

1. Reproduce the existing unrounded pocket tray with the same dimensions,
   2.4 mm walls and 2 mm base. Preserve an editable Python source and parameters.
2. Add one rounded-corner variant, with an explicit bounded radius parameter,
   at 96 x 64 x 16 and 120 x 80 x 18 mm. Do not generalize to arbitrary objects.
3. Export STEP and STL. Record kernel/package versions and source/output hashes.
   Record exact geometry checks and failures, not just screenshots.
4. Compare nominal dimensions, analytic unrounded volume, BRep validity,
   connected solids and mesh characteristics. Preserve the baseline command.
5. Produce a choose/decline report. Do not migrate V1 even if the spike succeeds;
   first review a separate adapter/migration proposal.

## Acceptance gates

- **G-0, local readiness:** no-key commands succeed; preview returns 200;
  beginner can download and find the exact expected dimensions. Human slices and
  prints remain pending until real evidence exists.
- **G-1, foundation:** passport tests prove same inputs stable, changed dimension
  or recipe identity different, and no inherited slicer/physical state. Feedback
  form captures failures and full actual setup. All V1 checks and Pages pass.
- **G-2, CadQuery choose/decline:** user approves installation; dependencies and
  licenses are recorded; isolated Windows and Linux test runs pass; dimensions
  within 0.05 mm of nominal; unrounded volume within 0.1% of the analytic value;
  tessellated volume within 0.5% of the kernel solid; valid single solid and
  printable-orientation candidate with no silent repairs. Rebuild differences are
  documented (kernel tessellation need not be byte-identical across platforms).
  V1 exports stay byte-identical. Human slicing is a separate required gate before
  any new model is labeled slicer-checked.
- **G-3, optional Meshy trial:** user approves precise non-sensitive input, provider,
  terms and a numeric total credit cap; no keys in files/logs/commits; one original
  decorative object, no paid automatic retries or regeneration. Record provider
  task ID, consent, model version, prompt provenance, source/output hashes,
  actual credits and rights. Failures are retained and labeled. Human reviews
  scale, thin features and repair changes. Existing limited box-mesh checks alone
  are not accepted as complete validation of arbitrary AI geometry.
- **G-4, promotion:** public feedback includes exact passport scope, actual
  settings, screenshots/photos and observations. A maintainer reviews evidence;
  separate slicer and physical statuses are never inferred from provider success.

## Open questions

| # | Question | Blocking? | Raised | Answer |
|---|----------|-----------|--------|--------|
| Q-1 | Approve T-05 as the first isolated CadQuery experiment? | T-05 only | 2026-11-10 | Awaiting review; no installation yet |
| Q-2 | Is a Meshy trial desired, and with what privacy/rights approval and credit cap? | T-06 only | 2026-11-10 | Deferred; no API calls |
| Q-3 | Which actual printer/nozzle/plate/PLA will be used for the first human trial? | Slicing/printing only | 2026-11-10 | User selects actual setup in Bambu Studio |

## Notes

The approved foundation work does not wait on these future decisions.
No FreeCAD, Blender, Zoo, CadQuery or cloud provider integration was installed by
this planning task. No public print report or fake test result is filed by the
agent. The issue form is an invitation for real observations.

## Links

- Requirements: [requirements.md](requirements.md)
- Existing decisions: [docs/decisions.md](docs/decisions.md)
- Local test handoff: [docs/local-testing.md](docs/local-testing.md)
- Site: https://prashanth261993.github.io/OpenPrintLab/
