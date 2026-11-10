# T-05 CadQuery evaluation - choose for an opt-in follow-up, not a migration

## Decision status

**Recommendation: choose CadQuery as the candidate for a separately reviewed,
opt-in precise-CAD adapter. Decline a default catalog/core migration now.**
The bounded experiment meets G-2 on Windows and Linux and demonstrates useful
rounded geometry plus STEP interchange without extending our own mesh engine.
The approximately 1.21 GB environment, native/bundled licensing obligations and
platform-dependent tessellation are material costs. Keep V1 dependency-free.

This is the experiment's choose/decline recommendation, **not adoption approval**.
The user authorized T-05 only. No provider, slicer or printer operation occurred.

## Trial contract and evidence

CadQuery 2.8.0, cadquery-ocp 7.9.3.1.1 and Python 3.12 in a separate environment.
`requirements.txt` and `constraints.txt` preserve the tested dependency selection.
`artifacts/windows/environment-and-results.json` and its `linux` counterpart
record actual package versions, license declarations, license-file hashes,
baseline hashes and geometry results. Both runs contain 45 installed
distributions including pip, with matching recorded version strings.
Python was 3.12.10 on Windows and 3.12.16 on Linux.

| Case | Dimensions (mm) | Outer radius | Walls / base | Windows / Linux |
|---|---|---|---|---|
| reference-sharp | 96 x 64 x 16 | 0 mm | 2.4 / 2 mm | passed / passed |
| rounded-96 | 96 x 64 x 16 | 6 mm | 2.4 / 2 mm | passed / passed |
| rounded-120 | 120 x 80 x 18 | 6 mm | 2.4 / 2 mm | passed / passed |

Each case has original editable source, STEP, STL, SVG geometry preview and
reported hashes. Four focused tests check parameter refusal/boundaries,
kernel/analytic/mesh geometry, STEP round-trip and repeated same-process STL
reproducibility. They passed on Windows and in the
[isolated Ubuntu 24.04 run](https://github.com/Prashanth261993/OpenPrintLab/actions/runs/42910032523).
A fifth test verifies stored cross-platform evidence and rejects modified
downloads. The separate [baseline CI/Pages run](https://github.com/Prashanth261993/OpenPrintLab/actions/runs/42910032719)
also passed.

Both platforms: largest dimension-bound deviation 0.003615 mm (limit
0.05 mm); kernel/analytic volume error below 0.000000001% (limit 0.1%);
mesh/kernel error at most 0.002212% (limit 0.5%). Each exported/reimported STEP
is a valid single solid with volume drift below 0.000000001%.
The rounded STL meshes each contain 1,052 triangles. No repair calls were used.

## G-2 decision table

| Gate | Actual evidence | Result |
|---|---|---|
| Explicit approval and isolation | User selected T-05; separate `.venv`; no core dependency or catalog changes | pass |
| Dependencies and licenses recorded | Pinned requirements/constraints; per-platform installed inventory and license-file hashes; license caveats below | pass as inventory, not legal clearance |
| Windows/Linux verification | Local Windows tests and isolated Ubuntu workflow linked above | pass |
| Nominal dimensions within 0.05 mm | Maximum reported bounding deviation 0.003614376 mm | pass |
| Unrounded volume within 0.1% analytic | 22,717.44 mm3 kernel volume; error approximately 1.6e-14% | pass |
| Mesh volume within 0.5% kernel | Worst case 0.002211015% | pass |
| Valid single solid and STEP round-trip | All three cases, both platforms; maximum round-trip volume error below 1e-9% | pass |
| No silent repair | No repair calls; kernel validity and exported mesh checks pass as produced | pass |
| Baseline exports unchanged | Same hashes for all 16 baseline artifacts on both platforms; baseline CI passed | pass |
| Human slicer/physical evidence | Not performed; no printer used | pending, not part of software success |

### Rebuild differences are real

The sharp-reference STL is byte-identical across the two runs. Rounded STLs are
**not** byte-identical and their triangle connectivity differs. Each has 528 unique
vertex positions at 0.000001 mm precision; those sets match, and the reported
kernel and mesh volumes match. This does not claim byte-identical triangulation
or universal reproducibility. Same-process repeated STL export passed on each
platform.

STEP files differ, including their export timestamps. They preserve valid
geometry through reimport, not the Python parameter/feature history.
Use the exact per-platform artifact hash for feedback and evidence. Do not copy
a slice/print result between different hashes because the nominal dimensions match.

[`artifacts/comparison.json`](artifacts/comparison.json) preserves these
differences. `compare.py` rechecks raw file hashes and mesh evidence before
comparing reports; it never rewrites the trial meshes. `.step` files are marked
non-text in Git attributes so line-ending normalization cannot invalidate hashes.

## Cost and licensing observations

The Windows environment occupies **1,213,844,839 bytes** across 14,769 files at
the initial measurement, roughly 1.21 GB decimal. This includes the Python
environment and dependencies, not just model files; it is not an install-time
claim. This is substantial compared with the dependency-free baseline.

Package inventory is restricted to this environment's site-packages, not the
repository's editable package metadata. CadQuery and OCP Python wrappers declare
Apache licensing; their native dependency stack must not be assumed uniformly
permissive. The underlying [OCCT documentation](https://occt3d.com/open-cascade-technology/index.html)
states LGPL 2.1 with an additional exception.
[CasADi](https://github.com/casadi/casadi/blob/main/LICENSE.txt), present in the
dependency closure, is LGPL-3.0; its bundled components have additional notices.
CadQuery's [actual license](https://github.com/CadQuery/cadquery/blob/master/LICENSE)
states Apache 2.0 even though GitHub's automatic SPDX classifier returned
`NOASSERTION`. License metadata and hashes are
an inventory, **not** a redistribution/compliance audit.

Original `design.py` and generated models are CC BY 4.0; probe/tests are MIT.
No installed third-party libraries are committed or bundled for redistribution.

## Reproduce

See [README.md](README.md) for Windows setup/customization commands.
The [experiment-only workflow](../../.github/workflows/cadquery-experiment.yml)
runs the same tests and exports on Ubuntu without installing CadQuery in
the default Pages job.

```powershell
experiments\cadquery\.venv\Scripts\python.exe -m unittest discover -s experiments\cadquery -p test_probe.py -v
experiments\cadquery\.venv\Scripts\python.exe experiments\cadquery\probe.py
python -m tools.release --check
python experiments\cadquery\compare.py
```

## Remaining limits

All 16 baseline export files are unchanged. The existing localhost catalog
remains responsive. STEP is an editable geometric interchange file, not a
replacement for the Python parametric history.
No slicer review, measured fit or physical-print result exists. Real offline
slicing and later printing remain independent gates.

## What a separately approved follow-up would need

Before any adapter or migration: decide whether the install footprint is
acceptable; review native/bundled dependency notices for the chosen distribution
method; specify source/version/hash and tessellation settings in the passport;
keep CadQuery optional; and review a human slice of the exact selected artifact.
Do not treat this list as implementation authorization. T-06 and T-07 remain
outside this experiment.
