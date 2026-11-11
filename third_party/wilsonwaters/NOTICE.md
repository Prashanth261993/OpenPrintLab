# Selected adaptations from wilsonwaters/3d-printing

Upstream: https://github.com/wilsonwaters/3d-printing

Revision: `f5e18a16031f5a11b20f7753574ff48494891587`, inspected 2026-11-11.
Copyright (c) 2026 Wilson Waters. [MIT license](LICENSE) retained.

`patterns/review.json` adapts reference/checklist concepts and explicitly scoped
source observations from `.claude/skills/3d-print-designer/pattern-fasteners.md`,
`material-petg.md` and `design-review.md`. It omits generic strength, tolerance,
temperature and food-contact recipes. Upstream claims are not independently
verified and are not OpenPrintLab evidence.

`tools/diagnostics.py` adapts the component, placement and downward-face area
reasoning in `.claude/skills/3d-print-designer/verify-model.py`. Changes include
explicit modes instead of name-derived permissions, strict existing binary STL
decoding, directed-edge checks, per-component plate checks, input hashes and
conservative bounding-box separation rather than source execution or claimed
exact collision tests. No OpenSCAD runner, first-layer algorithm, heuristic
strength/material numbers or implicit repair is imported.

These adaptations remain MIT, including the pattern content. Original model
designs and original guides retain their separately documented CC BY 4.0 scope.
Other upstream files are reviewed candidates, not installed integrations.
