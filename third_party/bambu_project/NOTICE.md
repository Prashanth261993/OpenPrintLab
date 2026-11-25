# Selective Bambu project-format adaptation

Source: Wilson Waters, `wilsonwaters/3d-printing`, revision
`f5e18a16031f5a11b20f7753574ff48494891587`, reviewed 2026-11-25.

- `.claude/skills/3d-print-designer/make-bambu-3mf.py`
- `.claude/skills/3d-print-designer/bambu-3mf-export.md`

`tools/bambu_project.py` selectively adapts the project ZIP/production-extension
layout, model settings and named-system-preset/difference-slot strategy.
Copyright (c) 2026 Wilson Waters; MIT license reproduced in LICENSE.
OpenPrintLab modifications: strict binary STL/passport validation, unrounded
coordinates, explicit bounded placement/setup, dependency provenance, limited
overrides, non-overwriting deterministic exports and save-copy fidelity checks.
No upstream installer, CAD execution, mesh repair, profile fallback, randomized
placement or printer operation is incorporated.

Installed Bambu profiles are read at the caller's explicit path and hashed, not
redistributed. Upstream MIT does not license Bambu's profiles. Test profiles are
synthetic minimal contracts, not usable printer presets.
