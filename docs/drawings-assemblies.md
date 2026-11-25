# Geometry-derived overview drawings and assembly checks

These tools supplement, not replace, the [prototype guidance](structural-design.md).
They generate or measure real geometry; neither certifies physical fit or strength.

## Dimensioned orthographic overviews

```powershell
python -m tools.cli draw-stl models\exports\step-study.stl --output build\drawings\staircase-v1
```

The new directory contains top/front/right SVGs plus a hash-bound report.
[View the palette's actual top drawing](https://prashanth261993.github.io/OpenPrintLab/custom/round-palette/r0002/drawings/top.svg),
[front](https://prashanth261993.github.io/OpenPrintLab/custom/round-palette/r0002/drawings/front.svg),
and [right](https://prashanth261993.github.io/OpenPrintLab/custom/round-palette/r0002/drawings/right.svg).
Dimensions are **overall exported mesh extents** on labeled axes, in mm.
The projected depth-shaded geometry comes from the same triangles; it is not generated
illustrative art. No CadQuery dependency is needed. Existing directories are
refused and source STL is never changed.

These are not complete manufacturing drawings: no automatic feature dimensions,
GD&T, datum selection, physical tolerances, hidden-line guarantees or paper
scale. SVG dimensions reflect tessellation precision. Inspect the source
and measured requirements before fabrication.

## Optional-kernel static assembly checks

Use the existing optional CadQuery environment and an explicit JSON manifest:

```json
{
  "units": "mm",
  "clearance_mm": 0.5,
  "contacts": [],
  "parts": [
    {"id": "left", "step": "left.step", "sha256": "EXACT-FILE-SHA256", "translation_mm": [0, 0, 0]},
    {"id": "right", "step": "right.step", "sha256": "EXACT-FILE-SHA256", "translation_mm": [30, 0, 0]}
  ]
}
```

Replace the example values with your actual part identities and placements.
STEP files must be beneath the manifest directory; no traversal or symlinks.
Each file must be one valid positive-volume solid. Accepted manifests have
2-32 parts, an explicit clearance and translation-only placements.

```powershell
.\.venv-cadquery\Scripts\python.exe -m tools.cli check-assembly build\assembly\assembly.json
```

The report gives kernel minimum distance and intersection volume for each pair,
input hashes, backend versions and numerical tolerances. Unlike bounding-box
screening, a part in a clear hollow region can pass despite overlapping bounds.
Any positive-volume interference above `0.000001 mm3` fails. Distances use
`0.00001 mm` numerical tolerance; these are kernel-comparison thresholds, not
physical fit allowances.

For an intentional touching pair, list its two IDs in `contacts`.
Declared contacts must actually touch within the numerical tolerance and never
permit volumetric interference. Undeclared touching or insufficient clearance
fails. The CLI exits 1 for reported violations and 2 for invalid inputs or
unavailable dependencies. Read the complete report, not just process success.

This is **static B-rep analysis**, not an exact physical measurement, assembly
order check, motion sweep, fastener analysis, load/creep proof or slicer check.
Rotations and arbitrary imported-assembly editing are not supported: author the
required orientation in your source and export a new hash-bound part.

Verified synthetic cases include known gaps/intersection volumes, declared
contact, a clear part inside a hollow ring, wrong hashes and malformed
manifests. Real material tolerances and service behavior need separate evidence.
