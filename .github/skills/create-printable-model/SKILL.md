---
name: create-printable-model
description: Create or customize OpenPrintLab parametric 3D models with validated dimensions, STL exports and honest print-readiness reports. Use for model authoring and dimension changes.
---

# Create a printable-model candidate

This skill produces a **candidate for slicing**, not a printability certification.

1. Read `AGENTS.md`, `docs/decisions.md`, and the target entry in
   `models/catalog.json`. Confirm the intended object, non-critical use,
   dimensions in mm, clearance and actual printer/nozzle/material when relevant.
   Never assume AMS. Refuse out-of-scope safety-critical applications.
2. Run `python -m tools.cli parameters MODEL`. Prefer changing supported
   parameters over inventing new mesh logic. If the requested shape cannot be
   expressed by a supported recipe, explain that boundary before implementing
   an original recipe and focused tests.
3. Use `python -m tools.cli check MODEL --set length=120` (replace with actual
   dimensions). Address invalid values; never weaken constraints just to pass.
4. Export with `python -m tools.cli build MODEL --set length=120 --output
   build/my-variant`. Run commands as single lines. Keep user variants separate
   from catalog defaults. Review report dimensions and the actual STL hash.
5. For catalog additions, add metadata, recipe tests and truthful print notes.
   Run `python -m unittest discover -s tests -v`, `python -m tools.release`,
   `python -m tools.release --check`, and `python -m tools.site`.
6. Hand back exact source/output paths, dimensions, parameter changes, checks
   performed, and any failures. Say "not slicer-checked or physically print-tested".
   Point to `docs/beginner.html` for a human Bambu Studio review and print.

Never generate machine-ready G-code or invoke printer controls. Never fabricate
print time, material usage, photos or successful prints. Suggested settings are
starting points, not certified profiles. Changing a model invalidates any
previous slicer or physical test evidence. Preserve CC BY 4.0 attribution for
design sources and models, distinct from MIT tooling.

If connected to the optional local MCP server, `describe_model`, `check_model`
and `export_model` expose the same pipeline. Export overwrites that model's
previous files under `build/mcp`; get user approval through the client's tool
approval mechanism. The CLI is the fallback when MCP is not installed.
