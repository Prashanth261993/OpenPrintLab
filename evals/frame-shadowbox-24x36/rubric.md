# Frozen neutral evaluation rubric

Freeze ID: `frame-shadowbox-24x36-v1`.
The common scoring was identical in both launch messages and frozen there before
their work. [`actual-prompts.md`](actual-prompts.md) is authoritative for the
verbatim common scoring. This formatted repository record was archived after launch.

## Weighted score: 100 points

| Category | Points | Evidence to examine |
|---|---:|---|
| Requirement compliance, dimensional stack-up and printer-fit outputs | 25 | Display/seat/outer/cut dimensions, usable depth and clearance, oriented printable exports and practical bed margin |
| Modularity, joint alignment/retention, seam strategy and tolerances | 20 | Actual segmented geometry, dimensioned joint detail/coupon, alignment and concealed retention, racking/tolerance reasoning and realistic finishing |
| Glazing insertion/removal, support and clearance | 15 | Workable serviceable access, cut sizes/thickness rationale, retaining/support stack, expansion/tolerance allowance and material tradeoffs |
| Credible hanging load path and bounded safety assumptions | 15 | Explicit structural-to-rated-hardware-to-wall path, measured versus estimated mass, unknown wall assumptions and conservative checks without invented proof |
| Aesthetics, actual geometry-derived presentation and source references | 10 | Three required aesthetic concepts, recommended solution presentation, honest seam/finish discussion and cited real references |
| Usable BOM, cut list and fabrication/build/finishing instructions | 10 | Quantities, purchased components, labeled estimates and sequential instructions covering fabrication through hanging |
| Editable/reproducible outputs and honest evidence | 5 | Rebuildable source, exports, versions/hashes where possible, candid failures and print-only residuals |
| **Total** | **100** | |

## Critical failures: report separately from the weighted score

- No printable exports.
- Assembled size or usable depth fails the common brief.
- Required print parts exceed the printer in their specified orientation.
- Missing workable glazing access.
- Unaddressed hanging or retention load path.
- Fabricated test claims.

Do not hide a critical failure inside an otherwise attractive weighted total.
Report the observed failure, artifact and requirement involved. Do not invent
automatic disqualification rules or scoring bonuses beyond this frozen rubric.

## Neutrality and evidence rules

Do **not** score tool invocation, OpenPrintLab-branded passports, exact programming
language or report formatting as design quality. An appropriate editable
OpenSCAD source is not penalized merely for lacking STEP.

The parent independently measures both outputs using equivalent neutral checks,
then reviews manufacturability/appearance. Identify which results were measured,
inferred, estimated, not checked or blocked. Software checking is not physical
validation.

Use the protocol's fixed-camera conditions for comparable presentation. Preserve
raw outputs and failures; presentation normalization must not secretly repair or
redesign one arm.

The user sees **A/B** output labels. The parent knows arm identity, so do **not**
claim a blinded parent judgment. A single two-arm trial is a case study, not proof
of broad superiority.
