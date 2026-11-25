# Offline slicing without a physical printer

Bambu Studio can generate and review toolpaths using selected profiles without
a connected printer. A physical P2S is **not** a prerequisite for this software
validation. The user approved this workflow on 2026-11-25.

Local toolpath/G-code generation is allowed **only for offline inspection**.
Never connect to/control a printer, send a job or automatically print. Do not
publish or distribute machine-ready G-code, including a sliced 3MF containing
it. Preserve the original unsliced project, STL/STEP/source and identity report.
Write disposable slice outputs separately under ignored `build/` storage, not
over the originals. Review archive contents before sharing any 3MF.

| Evidence | What it establishes | Required record |
|---|---|---|
| Project opened / round-tripped | Application accepted and restored the project | Studio version; input/output hashes; actual printer/nozzle/plate/filament/process identities and overrides; restored dimensions/settings; warnings |
| Sliced and toolpath-reviewed | Actual toolpaths inspected in that application/configuration | All above plus slice result, per-layer review, supports/bridges/islands, shell continuity, warnings and screenshots/observations; estimates explicitly labeled as slicer's estimates |
| Physically printed / tested | Only the observations actually made on that configuration | Actual hardware/settings, exact artifact identities, photos/measurements, failures and scope; no inheritance across revisions |

A ZIP/schema check or successful project open is not a toolpath review.
Toolpath generation alone is not evidence every relevant layer was inspected.
Do not silently promote `slicer_checked` in old immutable reports; attach a
separate exact-artifact evidence record identifying what was reviewed.

Profiles selected for an offline hypothetical setup are **declared test
assumptions**, not claims about hardware the user owns. Missing profiles,
unresolved warnings, application incompatibility or unavailable slicing
capabilities are explicit blockers, never substituted presets.

Slicing cannot establish bed adhesion, physical dimensions/fit, material quality,
glazing retention, joint strength or long-term creep. Those remain governed by
the [structural-prototype policy](structural-design.md) and real physical evidence.
Manual printing, if the user later chooses it, is outside this agent's control.
