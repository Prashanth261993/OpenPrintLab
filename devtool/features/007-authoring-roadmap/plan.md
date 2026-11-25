---
artifact: plan
feature: 007-authoring-roadmap
status: in_progress
updated: 2026-11-25
---

# Named designer and controlled authoring roadmap

User approved proceeding and requested a distinctive callable agent. Implement
sequential, verified releases; no comparison restart or private design ingestion.
Keep Python/CadQuery optional and the existing standard-library baseline.

| Phase | Scope / acceptance | State / dependencies |
|---|---|---|
| A: named designer | Real repository profile, canonical rule pointers, documented discovery/runtime/client limits; schema and links verified; README/Pages and canonical file published | Verified locally; publishing first slice |
| B: new-design/edit/live preview | Isolated editable design source, measurable brief, reviewed local execution, checked STL/STEP, immutable revision outputs, stable viewer and bounded edit example beyond named templates | Next, after A |
| C: P2S project-3MF | Strict actual profile identity, geometry + metadata, installed Studio round-trip and offline slice review; no printer control or machine-ready G-code distribution | Parallel isolated worker owns module/tests/app verification; shared integration follows B and reviewed handoff |
| D: assistant packaging | Generated repository-scoped package with full canonical references/notices, manifest, install/uninstall verification; no global config or telemetry | After C; client scope gate |
| E: drawings/assembly diagnostics | Actual geometry-derived dimensioned views and stronger bounded assembly checks with synthetic positive/negative cases | After D; precise contracts before claims |

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
revision `a35df3f4ab8abe86d370fbffb631277a4e170e7b`. Root license read:
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
