# Experimental P2S project export

**Native open/save/reopen and local slicing passed for the recorded staircase
in Bambu Studio 02.09.02.62. Complete per-layer/warning review remains pending.**
This module writes an unsliced Bambu project candidate with mesh, model settings,
named system-preset bindings, explicit process values/overrides and provenance.
It is more than a geometry-only ZIP, but package tests are **not** application
compatibility evidence. Do not label arbitrary exports ready to print or
slicer-checked.

After an initially interrupted session, the user granted an uninterrupted window.
The project opened and round-tripped with all 72 placed triangles and explicit
settings retained; local slicing produced 80 layers. Studio discarded the custom
provenance members, as anticipated. The native Preview's ImGui labels/legend and
warning areas rendered as unreadable black blocks to Computer Use, so exact
per-layer visual coverage and complete warning review cannot be claimed.
See the [bounded slice evidence](../devtool/features/p2s-project-export/evidence.md).

**Unresolved review items:** bridge feature blocks at layers 16/36/56/76 and
floating-vertical-shell blocks at 15/21/22/35/41/42/55/61/62/75. Do not dismiss
these as benign or infer support-free suitability from `support_used=false`.
Review their support below, continuity, span/anchoring and the actual warning
area in a correctly rendered Preview before completing the slice-review gate.

Read-only source research provides context, not a pass: at BambuStudio source
revision `23a33758933e712c6041e1f8f135f7d6b50004aa`,
[`ExtrusionEntity.cpp`](https://github.com/bambulab/BambuStudio/blob/23a33758933e712c6041e1f8f135f7d6b50004aa/src/libslic3r/ExtrusionEntity.cpp#L615-L628)
maps both strings to extrusion roles.
[`ExtrusionEntity.hpp`](https://github.com/bambulab/BambuStudio/blob/23a33758933e712c6041e1f8f135f7d6b50004aa/src/libslic3r/ExtrusionEntity.hpp#L99-L128)
includes floating vertical shell among solid-infill roles, and
[`Fill.cpp`](https://github.com/bambulab/BambuStudio/blob/23a33758933e712c6041e1f8f135f7d6b50004aa/src/libslic3r/Fill/Fill.cpp#L354-L364)
can assign it a bridge-speed setting. Thus the label is not by itself a verdict
that the exported mesh is disconnected, nor evidence it will print successfully.
The inspected source revision was not established as the exact installed
binary's source; no source-level inference substitutes for reviewing these
specific toolpaths. No settings were changed based on this research.

## Deliberately narrow contract

| Choice | Accepted value |
|---|---|
| Application file version | `02.09.02.62` |
| Printer / nozzle | `Bambu Lab P2S 0.4 nozzle` / `0.4` mm |
| Extruder | `Direct Drive Standard` (Standard nozzle flow) |
| Process | `0.20mm Standard @BBL P2S` |
| Filament | `Bambu PLA Basic @BBL P2S` |
| Plate | `Textured PEI Plate` |
| Geometry | One connected, already oriented binary STL with an exact OpenPrintLab v1 passport, mm, Z=0 |
| Placement | Explicit XY translation, unchanged scale/rotation/Z, 8 mm XY bed-edge clearance |

These are **declared offline test choices**, not a claim about the user's actual
plate/filament/hotend or ownership of AMS. No other version/material/nozzle/process,
multi-material, assembly, arbitrary 3MF import, profile editing or mesh repair is
supported. New custom-engineering authoring reports without a v1 model passport
are also rejected; never fabricate a template passport to bypass this boundary.
Exact names are required; missing or ambiguous presets fail instead
of substituting P1S or another material.

`--profiles-dir` points to the installed official `resources\profiles\BBL`
directory. It is read-only. Parents and `include` dependencies are resolved;
arrays replace whole arrays, and explicit child values take precedence. Every
read file and resolved profile gets a SHA-256 identity. No official profile
content or machine/filament G-code is redistributed.

**This is named-preset binding, not a portable full-profile bundle.** The opening
Studio must have matching system presets. A user's cached/updated/modified
presets can differ from installation resources. `check-profiles` detects changed
resource bytes, not active in-memory settings. Inspect native selections and
compare the app-saved copy; changed profiles require a fresh export/review.
The version argument is a caller assertion, not automatic executable detection.

## Commands

Run from the repository root with Python 3.11+; no additional dependency is needed.
Use a new output name on every revision. Existing files, including symlinks,
are never overwritten.

```powershell
python -m tools.bambu_project supported
python -m tools.bambu_project export --stl models\exports\step-study.stl --report models\exports\step-study.report.json --output build\p2s-projects\step-study.3mf --profiles-dir "C:\Program Files\Bambu Studio\resources\profiles\BBL" --studio-version 02.09.02.62 --printer "Bambu Lab P2S 0.4 nozzle" --process "0.20mm Standard @BBL P2S" --filament "Bambu PLA Basic @BBL P2S" --plate "Textured PEI Plate" --nozzle-mm 0.4 --extruder-variant "Direct Drive Standard" --translate 104 116 --set wall_loops=3 --set sparse_infill_density=20% --set brim_type=no_brim
python -m tools.bambu_project inspect build\p2s-projects\step-study.3mf
python -m tools.bambu_project check-profiles build\p2s-projects\step-study.3mf --profiles-dir "C:\Program Files\Bambu Studio\resources\profiles\BBL"
```

The shipped staircase is 48 x 24 x 16 mm. Translation `(104, 116, 0)` centers its
original `(0, 0, 0)`-based mesh on a 256 mm square bed; it does not resize it.
Substitute the actual STL and report paths for a named variant. A passport hash
mismatch is an error, not permission to attach another model's identity.

Process-only overrides:

| Key | Allowed values |
|---|---|
| `layer_height` | 0.08-0.28 mm |
| `wall_loops` | Integer 1-8 |
| `top_shell_layers`, `bottom_shell_layers` | Integer 1-12 |
| `sparse_infill_density` | 0-50, optionally suffixed `%` |
| `sparse_infill_pattern` | `grid`, `gyroid`, `rectilinear` |
| `enable_support` | `0` only |
| `brim_type` | `no_brim` only |

These are validation bounds, not recommendations for every geometry. Temperatures,
speeds, machine settings, arbitrary keys and G-code overrides are rejected.
If the installed profile omits one of these process values (for example
`brim_type` in the inspected resources), supply it explicitly with `--set`;
the exporter will not guess the application's implicit default.

## Python integration

```python
from tools.bambu_project import (
    export_project, inspect_project, supported_setup,
    verify_profile_sources, compare_saved_project,
)

receipt = export_project(
    stl_path, report_path, new_project_path,
    profiles_dir=official_bbl_resources, studio_version="02.09.02.62",
    printer="Bambu Lab P2S 0.4 nozzle", process="0.20mm Standard @BBL P2S",
    filament="Bambu PLA Basic @BBL P2S", plate="Textured PEI Plate",
    nozzle_mm=0.4, extruder_variant="Direct Drive Standard",
    translation_xy=(104, 116),
    overrides={"wall_loops": 3, "sparse_infill_density": "20%", "brim_type": "no_brim"},
)
```

`receipt` contains the absolute output `path`, project `sha256`, and embedded
`manifest`. No shared CLI/MCP/site integration is included in this slice.
Input/output I/O and validation failures are explicit exceptions; the standalone
CLI prints the error to stderr and exits 2. Inputs and expanded archives are
bounded to 64 MiB. The writer does not launch Studio, slice, connect to a printer,
send a job or print.

## Provenance and fidelity

Inside the ZIP, `Metadata/openprintlab/` contains the **original byte-for-byte**
`source.stl`, `source.report.json`, and `manifest.json`. Original passport version,
variant ID, editable-source identities and historical evidence are preserved.
The project manifest separately starts with `app_open_verified`, `slicer_checked`
and `physical_print_tested` all false. It records source/member hashes, exact
profile dependency hashes, explicit placement and process overrides.

No rounded/merged-nearby vertices or dropped faces: binary float32 coordinates
are serialized exactly as Python round-trippable decimal values; vertex sharing
only combines exactly equal triples. Triangle order and winding are retained.
Software checks remain the existing shared mesh checks, not self-intersection,
support, adhesion, fit, strength or printability certification.

The observed Studio save discarded unknown provenance members. Preserve the original
export and its passport; never replace it with the app-saved copy. The comparison
reports whether Studio retained the original passport, without treating loss as
new provenance or silently reconstructing it.

## Repeating and completing native acceptance

With an uninterrupted, approved native UI session:

1. Recheck the installed executable version and `check-profiles`; open the
   generated `.3mf` **as a project**, not as geometry only. Inspect printer,
   nozzle flow/type, nozzle diameter, process, filament, plate and overrides.
   Verify 48 x 24 x 16 mm size, placement/orientation, one object and warnings.
2. Save a **different unsliced** project path, reopen that saved copy, and run:
   `python -m tools.bambu_project compare ORIGINAL.3mf SAVED.3mf`.
   This compares every explicitly exported setting plus placed oriented triangles
   at 0.00001 mm precision, allowing face reordering and object-local recentering.
   It is a bounded file comparison, not a claim that the native UI was inspected.
   Other layouts and any changed geometry/settings fail explicitly.
3. Slice locally under the separately approved offline-slicing policy. Keep
   toolpaths/sliced output in separate ignored local storage. Inspect first
   layers, step transitions, shells/infill, support/bridge/island behavior and
   warnings in the actual Preview. Record precise layer ranges reviewed and any
   unreviewed gaps; merely clicking Slice does not complete this gate.
4. Attach separate exact-artifact evidence: hashes, application/resource version,
   actual selections/overrides, sanitized screenshots/observations, warning
   disposition and comparison result. Slicer time/material are estimates, not
   observations of a physical print. Do not alter old immutable passports.

Never connect/control a printer, send jobs, print automatically, or publish
machine-ready G-code (including sliced `.3mf` files). A local slice does not need
a physical printer and does not establish adhesion, dimensional fit, physical
quality, strength or creep. A native warning or interruption is a blocker, not a
reason to approve/disable a protection or bypass the automation permission gate.

## Reuse and licensing

Project layout and preset-difference slots are selectively adapted from
[Wilson Waters' pinned MIT writer](https://github.com/wilsonwaters/3d-printing/blob/f5e18a16031f5a11b20f7753574ff48494891587/.claude/skills/3d-print-designer/make-bambu-3mf.py).
See [notice and retained license](../third_party/bambu_project/NOTICE.md).
No fallback preset table, random placement, loose STL parsing, degenerate removal,
installer or printer-send logic is reused.
[text-to-cad's pinned print3d guide](https://github.com/earthtojake/text-to-cad/blob/a35df3f4ab8abe86d370fbffb631277a4e170e7b/skills/print3d/SKILL.md)
was research only for inherited-profile and project-handoff pitfalls.
Tooling/tests are MIT; this guide and original model content remain CC BY 4.0.
