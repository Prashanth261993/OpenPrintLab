# P2S project export - bounded slice

Scope: `tools/bambu_project.py`, its focused tests/fixtures, this feature directory,
`docs/bambu-project.md`, and adaptation notices only. Shared CLI/MCP/site wiring
belongs to the integrating worker. No dependency, catalog or default-export edits.

1. Read the shared mesh/passport contracts and pinned upstream writer; resolve
   actual installed P2S presets and fail closed on unsupported choices.
2. Implement a dependency-free, non-overwriting unsliced project writer with
   exact mesh coordinates, explicit placement, preset chain hashes and original
   passport bytes. Limit supported profiles and overrides rather than guessing.
3. Exercise positive/negative package and fidelity tests. Open in the actual
   Bambu Studio, inspect selections/warnings, save a separate copy and reopen.
4. Record sanitized version-specific evidence, limitations and exact interfaces;
   commit owned files locally for coordinator integration.

Evidence gates are separate: package tests do not imply native-app compatibility,
slicer review or physical testing. The user subsequently explicitly approved
offline slicing; canonical policy revision
`509677fcfb149928533941c901b7ee49d989095e` was read from git (including
`docs/offline-slicing.md` and the updated skill). It permits disposable local
toolpaths, not printer connection/control, sending jobs, automatic printing or
G-code distribution. Shared policy files remain owned by the integrating worker.

Research pinned on 2026-11-25:

- `wilsonwaters/3d-printing` at
  `f5e18a16031f5a11b20f7753574ff48494891587`: reviewed the MIT writer and guide;
  reuse project relationships and named-preset/difference-list layout, not loose
  STL parsing, vertex rounding/face deletion, fallback identities, random
  placement, raw configuration injection or installation instructions.
- `earthtojake/text-to-cad` at
  `a35df3f4ab8abe86d370fbffb631277a4e170e7b`: research only; inherited profiles
  and project-based handoff caveats. No installer, engine or printer-send code.

Current application executable file version: `02.09.02.62`. Installed profile
inspection, exporter, focused tests and baseline compatibility checks are done.
The user subsequently granted an uninterrupted native window: actual project
open/save/reopen and local slicing passed for the staircase. Full visual
layer/warning review remains incomplete because the automation capture renders
the native Preview labels/legend/warning areas as unreadable black blocks.
See [evidence](evidence.md) and [integration interface](../../../docs/bambu-project.md).
Only the recorded exact-fixture native observations are claimed, not complete
slicer review or physical validation.

For the integrating worker: shared CLI/MCP/site wiring is intentionally absent.
Do not remove the experimental label or mark roadmap 004 R-03 fully accepted
until the actual application gates pass. The module is independently runnable
with `python -m tools.bambu_project`; the guide lists callable APIs.
