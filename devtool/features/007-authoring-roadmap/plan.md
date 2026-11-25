---
artifact: plan
feature: 007-authoring-roadmap
status: blocked
updated: 2026-11-25
---

# Named designer and controlled authoring roadmap

User approved proceeding and requested a distinctive callable agent. Implement
sequential, verified releases; no comparison restart or private design ingestion.
Keep Python/CadQuery optional and the existing standard-library baseline.

| Phase | Scope / acceptance | State / dependencies |
|---|---|---|
| A: named designer | Real repository profile, canonical rule pointers, documented discovery/runtime/client limits; schema and links verified; README/Pages and canonical file published | Published c2221d9; CI succeeded |
| B: new-design/edit/live preview | Isolated editable design source, measurable brief, reviewed local execution, checked STL/STEP, immutable revision outputs, stable viewer and bounded edit example beyond named templates | Published 92dbd3d + exact-byte preservation dd22c8e; CI passed |
| C: P2S project-3MF | Strict actual profile identity, geometry + metadata, installed Studio round-trip and offline slice review; no printer control or machine-ready G-code distribution | Experimental: native open/save/reopen and slice generation verified for the exact fixture; full layer/warning review BLOCKED by unreadable Preview labels. Custom-report integration not implemented |
| D: assistant packaging | Generated repository-scoped package with full canonical references/notices, manifest, install/uninstall verification; no global config or telemetry | Published 3cb732b, CI passed; native client picker certification not claimed |
| E: drawings/assembly diagnostics | Actual geometry-derived dimensioned views and stronger bounded assembly checks with synthetic positive/negative cases | Published 3cb732b, CI passed; overview/static pair checks only, not complete engineering drawings or motion analysis |

## Phase B requirements and boundary

The assistant interprets a brief, records units/dimensions/intended use and writes
reviewed editable source in an isolated per-design area. Python source is code,
not a sandbox: execution uses the user's explicit local command permission.
Do not add a generic source-executing MCP or web endpoint. Shared export accepts
an already constructed CAD shape and binds source/output identity. Missing CAD,
invalid dimensions, stale reviewed source or an existing revision must fail.
Preserve the previous source and outputs while creating a new revision.

A loopback read-only viewer must show actual exported geometry and detect a new
published revision. It must not run Python or accept uploads/edits. Demonstrate
with a small safe object unavailable from named templates; preserve both example
revisions and verify actual source/export/preview/revision behavior. Physical and
slicer evidence stays not performed.

## Upstream assessment

Candidate: [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad/tree/a35df3f4ab8abe86d370fbffb631277a4e170e7b),
revision `a35df3f4ab8abe86d370fbffb631277a4e170e7b`. root license read:
MIT, copyright 2026 Thompson Labs LLC. `viewerAutoReload.js` implementation
reviewed: separates identity changes from transient errors, polls a read-only
server identity, does not execute source in the page. Adopt the separation of
document identity and read-only preview; do not import its installer, telemetry,
auto-update or second build123d stack. Additional engine/export implementation
review and adopt/adapt/defer findings will accompany phase B.

No upstream scripts run, dependencies installed or code copied in phase A.
006's patterns/diagnostics are retained, not duplicated. FEA, machining, PCB,
robotics, ordering, cloud generation and photoreal rendering remain out of scope.

Phase A evidence (2026-11-25): parsed YAML against the documented GitHub
name/description/tools schema; checked tool aliases, prompt length and referenced
local files. Local CLI 1.0.114 `--help` confirms `--agent` and `--add-dir`.
Existing generated-site link test and complete responsive/no-JS browser smoke
passed. Native agent-picker/model-run evidence is not claimed.

Phase B implementation/source review:

- `engine/document.py` documentation and identity structures and the complete
  `engine/export/stl.py` were inspected at the pinned upstream revision. Its
  XCAF prototype/instance/placement architecture is much broader than this slice.
  Defer importing that engine, persistent face selection and mesh placement
  export; retain our tested CadQuery/STL/checker utilities. No upstream code was
  copied, so no new adaptation license is claimed. Cite the upstream repository
  as design research, not installed functionality.
- Single-file drafts and explicit local script execution with reviewed source/
  brief hashes; no CLI/MCP/web source-execution endpoint. The publisher accepts
  an in-memory shape. Shared mesh and preview code is reused without modifying
  historical template sources or artifacts.
- Circular palette example: r0001 nominal 72 mm / six wells, r0002 nominal
  80 mm / eight wells. Source bounds, spacing and analytical solid-volume checks
  complement exported dimension/mesh/STEP checks. Both sources/briefs, exact
  artifacts and reports are deliberately published, not private user data.
- `python -m unittest discover -s tests -q`: 38 tests, 33 passed, 5 optional-CAD
  cases skipped in the no-CAD interpreter. All 7 `tests.test_designs` tests
  passed with CAD. All 16 original artifacts unchanged.
- `tests.design_browser_smoke` executed actual reviewed source, rejected stale
  review, published a dimension/count edit, detected it on the same page,
  preserved originals, verified download bytes and visibly rejected a corrupt
  report hash. The existing responsive/no-JS site smoke also passed.
- 98 internal Markdown links verified. Detached loopback viewer at port 8767
  responded with the actual r0002 palette; geometry screenshot inspected.
  Native client hot-load, physical printing and slicing of this palette are
  not claimed. Public CI/deployment is a subsequent release gate.

Phase C's native verification can run independently of D/E. It was paused on UI
interruptions and resumed by the user in an approved uninterrupted window; this
session does not operate Studio concurrently or mark the native gate passed.
Only reviewed worker evidence may promote that status.

Phase D packages committed Git HEAD, not dirty/ignored user work, as a complete
source snapshot retaining canonical instructions, tools and notices. Installation
is into a new separate directory; no client configuration edits. Uninstall
refuses modified or extra files/directories, including caches and user models.
Native client picker support is still documented evidence, not a claimed test.

Phase E scope: three geometry-derived projected SVG views with **overall bounds
only**, not GD&T, feature dimensions or toleranced fabrication drawings. Optional
CadQuery STEP-pair intersection volume and minimum distance use explicit
translations, hashes, expected contact pairs and a declared clearance. Reject
unsupported manifests, not silently drop parts. Numerical kernel results are
not physical fit, motion, strength or slicing evidence.

Combined local evidence: 57 baseline tests, 50 passed with 7 optional-CAD cases
skipped; 12 selected custom-CAD/drawing/assembly tests passed with CAD. Packaging
tests pass deterministic bytes, extracted CLI execution, changed/extra-file
preservation, malformed/tampered package rejection and clean removal. Original
16 model artifacts unchanged. Browser checks pass including custom preview and
package link; actual depth-shaded palette drawing was inspected and its extents
match the exported mesh. No upstream code was copied for D/E: existing standard
library, renderer and installed CadQuery kernel APIs are reused.

The P2S worker's follow-up a9420ce was integrated as daa77eb. See its
[native evidence](../p2s-project-export/evidence.md) and
[unresolved layer-role review](../../../docs/bambu-project.md). This does not
complete the full reviewed-slice requirement or authorize a physical print.
New custom-engineering reports are intentionally rejected by the v1-passport
project writer, not converted to fabricated template identities.

All 57 combined tests also passed in the optional-CAD environment; real MCP
smoke passed. The 3cb732b package contains all implemented modules, profile,
canonical references and notices (194 tracked files at that revision). Post-commit
package contents were inspected. Subsequent native evidence adds one focused
regression case and preserves the unreviewed/physical flags.

Final combined verification after native follow-up: 58 baseline tests (51 passed,
7 optional-CAD skips); all 58 passed with CadQuery installed. Release check still
verifies the original 16 artifacts. Browser/package-download checks passed and
115 internal Markdown links resolved. No G-code or sliced archives are tracked.
The full native layer/warning review remains incomplete within the bounded P2S
slice. Custom-report project integration is also not implemented; manual STL
handoff is documented instead. Broader capabilities explicitly listed as
unsupported are not silently claimed complete.
