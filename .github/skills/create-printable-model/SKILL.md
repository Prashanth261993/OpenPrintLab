---
name: create-printable-model
description: Create or customize OpenPrintLab parametric 3D models with validated dimensions, STL exports and honest print-readiness reports. Use for model authoring and dimension changes.
---

# Create a printable-model candidate

This skill produces a **candidate for slicing**, not a printability certification.

For loads, joints, glazing or mounting, first read
[the canonical structural-prototype guide](../../../docs/structural-design.md).
Classify hazard, uncertainty, prototype eligibility and suitability separately.
Follow its exclusions and escalation; missing physical evidence is not by itself
a reason to refuse all modeling or a reason to promise safe use.

Use `python -m tools.cli patterns`, then `pattern ID` for the relevant
`fastener-selection`, `material-service-envelope` or `geometry-design-review`
checklist (MCP: `design_patterns`). Source-reported proven/failed/unprinted
observations are not local evidence or universal values.

For the optional template lab, also read `docs/template-lab.md`. You (the user's
tool-capable assistant) interpret their instructions. The CLI/MCP is a
deterministic geometry tool, not a natural-language model.

1. Discover with `python -m tools.cli templates`, then `template ID` (or MCP
   `list_templates` / `describe_template`). Clarify missing dimensions, intended
   use, fit/clearance and unsupported style requests. Supported CAD aesthetics
   are rounded corners and compartment/channel counts; text/sculpting/import
   are not shipped. For shapes outside these operations, use the custom
   engineering boundary below rather than pretending a template supports them.
2. With the optional interpreter, use `python -m tools.cli customize ID --variant
   NEW-NAME --set key=value`. For revisions, read the prior `parameters.json`,
   create a different name and use `--params FILE` plus explicit overrides.
   Never overwrite originals or prior variants. Missing CadQuery requires the
   user's approved isolated install, not silent fallback.
3. Inspect the actual report and SVG derived from the exported STL. Return the
   preview URI and, if the lab server is verified running, its exact local URL.
   Include STL, STEP when supported, source and passport. Do not substitute
   illustrative generated art for the model preview.
4. Ask for actual printer/nozzle/plate/filament/use or call `guidance NAME` /
   `variant_guidance`. Follow `needs_input` and `unsupported_setup` honestly.
   The supported P2S/0.4 mm/PLA suggestions are not certified profiles.
5. Hand off to human offline slicing. No printer operation or physical-test claim.

Original simple-model workflow (still dependency-free):

1. Read `AGENTS.md`, `docs/decisions.md`, and the target entry in
   `models/catalog.json`. Confirm the intended object, non-critical use,
   dimensions in mm, clearance and actual printer/nozzle/material when relevant.
   Never assume AMS. Refuse out-of-scope safety-critical applications.
2. Run `python -m tools.cli parameters MODEL`. Prefer changing supported
   parameters over inventing new mesh logic. If the requested shape cannot be
   expressed by a supported recipe, explain that boundary and follow the custom
   engineering path below. Do not silently add or alter catalog defaults.
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

## Eligible custom engineering beyond templates

Frames and general assemblies have no shipped generator. For a permitted
prototype, author task-specific editable CAD only with the user's authorized
tools/workspace. Preserve each revision and its source/license/output identities.
Follow the canonical guide's utility contracts: binary STL, one connected
printable part per mesh check, recorded print orientation and separate assembly
transforms. Unsupported checks must be reported, not bypassed.

Use `inspect-stl FILE` (CLI) or `inspect-variant NAME` (CLI/MCP) for read-only
component, placement, contact and downward-face screening. Select the appropriate
mode and thresholds and inspect every finding plus `has_errors`. Overlapping
bounds require an exact CAD check; no first-layer-island, exact collision,
mechanical or slicer result is implied. See `docs/reuse.html`.

Return the guide's complete prototype handoff: risk/assumptions, component mass
budget and load path, actual geometry views/checks, fit/joint coupons, assembly
and reversible service instructions, remaining modes and staged physical gates.
Keep **"Prototype - not validated for hanging/load use."** No ready-to-hang claim
comes from a mesh check, calculation, printed coupon or short test.

The setup-guidance API remains limited to known variants/uses. Its rejection of
a custom use is not a general modeling ban, nor permission to invent a tested
profile. There is no arbitrary-source MCP endpoint or automatic suitability check.

Never generate machine-ready G-code or invoke printer controls. Never fabricate
print time, material usage, photos or successful prints. Suggested settings are
starting points, not certified profiles. Changing a model invalidates any
previous slicer or physical test evidence. Preserve CC BY 4.0 attribution for
design sources and models, distinct from MIT tooling.

If connected to the optional local MCP server, `describe_model`, `check_model`
and `export_model` expose the same pipeline. Export overwrites that model's
previous files under `build/mcp`; get user approval through the client's tool
approval mechanism. The CLI is the fallback when MCP is not installed.
