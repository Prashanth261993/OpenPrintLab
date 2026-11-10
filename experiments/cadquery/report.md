# T-05 CadQuery evaluation - Windows passed, Linux verification pending

## Decision status

**No adoption decision yet.** The user approved this bounded experiment only.
Windows geometry and round-trip tests pass; Linux proof is the remaining G-2
gate. No catalog migration, external provider, slicer invocation or physical
print is part of this experiment.

## Trial contract and evidence

CadQuery 2.8.0, cadquery-ocp 7.9.3.1.1 and Python 3.12 in a separate environment.
`requirements.txt` and `constraints.txt` preserve the tested dependency selection.
`artifacts/windows/environment-and-results.json` records actual package versions,
license declarations, license-file hashes, baseline hashes and geometry results.

| Case | Dimensions (mm) | Outer radius | Walls / base | Windows |
|---|---|---|---|---|
| reference-sharp | 96 x 64 x 16 | 0 mm | 2.4 / 2 mm | passed |
| rounded-96 | 96 x 64 x 16 | 6 mm | 2.4 / 2 mm | passed |
| rounded-120 | 120 x 80 x 18 | 6 mm | 2.4 / 2 mm | passed |

Each case has original editable source, STEP, STL, SVG geometry preview and
reported hashes. Four focused tests check parameter refusal/boundaries,
kernel/analytic/mesh geometry, STEP round-trip and repeated same-process STL
reproducibility. They passed on Windows before publication.

Windows observations: largest dimension-bound deviation 0.003615 mm (limit
0.05 mm); kernel/analytic volume error below 0.000000001% (limit 0.1%);
mesh/kernel error at most 0.002212% (limit 0.5%). Each exported/reimported STEP
is a valid single solid with volume drift below 0.000000001%.
The rounded STL meshes each contain 1,052 triangles. No repair calls were used.

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
will run the same tests and exports on Ubuntu without installing CadQuery in
the default Pages job.

```powershell
experiments\cadquery\.venv\Scripts\python.exe -m unittest discover -s experiments\cadquery -p test_probe.py -v
experiments\cadquery\.venv\Scripts\python.exe experiments\cadquery\probe.py
python -m tools.release --check
```

## Remaining limits

All 16 baseline export files are unchanged. The existing localhost catalog
remains responsive. STEP is an editable geometric interchange file, not a
replacement for the Python parametric history.
No slicer review, measured fit or physical-print result exists. The user's printer
is not available yet. Real slicing and later printing remain independent gates.
