# A new design, not another named template

OpenPrintLab Designer can now use a **single-file custom CAD workflow**:
measurable brief -> reviewed editable source -> checked STL/STEP -> live
geometry preview -> preserved revision. Your assistant does the design and
interprets natural language. There is no built-in prompt parser or hosted AI.

This first slice supports **one connected printable CadQuery solid** per design.
It does not import arbitrary STL/STEP, edit selected faces, model assemblies,
produce FEA or certify physical use. Those are not implied by "new design".
Follow the [structural policy](structural-design.md) before designing joints,
glazing, loads or mounting. Unknown installation conditions remain unresolved.

## Start with an actual new part

Use the optional CAD interpreter installed from the full checkout as described
in [template setup](template-lab.md). Python source execution needs the client's
explicit permission; a virtual environment is **not a security sandbox**.

The reviewed public example is a circular bead palette with six round blind
wells, not expressible by any named template. Its second revision is larger
and has eight wells. It is for dry craft sorting, not food contact.
[View the actual published geometry](https://prashanth261993.github.io/OpenPrintLab/custom/round-palette/);
both revision outputs are preserved there. The public page is a static copy, not
a remotely editable instance.
The initial six-well [STL](https://prashanth261993.github.io/OpenPrintLab/custom/round-palette/r0001/output/model.stl),
[preview](https://prashanth261993.github.io/OpenPrintLab/custom/round-palette/r0001/output/preview.svg)
and [report](https://prashanth261993.github.io/OpenPrintLab/custom/round-palette/r0001/output/report.json)
remain available alongside the latest eight-well revision.

Read `examples/custom-designs/round-palette/source.py` and `brief.json`, then:

```powershell
.\.venv-cadquery\Scripts\python.exe -m tools.design_examples
python -m tools.design_viewer --port 8767
```

Open **http://127.0.0.1:8767/round-palette/**. Generation refuses an existing
design; do not delete prior work to repeat the command. Instead use a new name
with `design-new`, or create a revision as below. The viewer serves only the
chosen design directory on loopback and has no upload, execution or editing API.
Leave it running for subsequent revisions; Ctrl+C stops it.

The page shows the actual mesh-derived preview, dimensions/checks and downloadable
STL, STEP, source, brief and report. The stable reference `round-palette:r0002`
can be quoted to your assistant; it identifies a whole design revision, **not
a selected geometric face**. It watches the current published revision, not
unreviewed source edits. File URLs do not support live polling; use HTTP.

## Your own brief and source

Use `design-new` with an unused lowercase name:

```powershell
python -m tools.cli design-new my-palette --brief examples\custom-designs\round-palette\brief.json --source examples\custom-designs\round-palette\source.py
```

For a different object, your assistant writes a self-contained source file and
brief first, using the example's contract rather than its geometry. The source
exports `make_shape(parameters)` returning a CadQuery `Shape` and calls
`tools.designs.run_design(__file__, make_shape)` under `if __name__ == "__main__"`.
Use real numeric bounds and relationship checks for the requested geometry.

The brief contains exactly `intended_use`, `assumptions`, `acceptance`,
`parameters`, `expected_dimensions_mm`, `license`, and `attribution`. Dimensions
are three positive millimeter extents within 256 mm. Counts and geometry-specific
relationships need source checks. Textual acceptance criteria are **not
automatically proven** by recording them.

The command copies files into `build/designs/my-palette/r0001/`; it never runs
submitted source. Read the entire source, imports and brief in that directory.
Keep it single-file: external custom helpers or data are not automatically
captured, and dependencies must be explicitly available and reviewed.

```powershell
python -m tools.cli design-review my-palette --revision r0001
.\.venv-cadquery\Scripts\python.exe build\designs\my-palette\r0001\source.py --reviewed-sha256 DIGEST-FROM-REVIEW
```

Replace the digest with the exact reported value **after review**. It binds the
source and brief and rejects stale input. It is an acknowledgement gate, **not
proof of safe code**: Python imports/top-level code execute before the library
gate. Never run untrusted code because a hash matched. There is intentionally no
generic source-running CLI, MCP or web endpoint.

The shared publisher accepts an already constructed shape. It uses existing mesh
validation and preview utilities, checks kernel validity/one solid, compares
the exported bounding dimensions (0.05 mm) and mesh/kernel volume (0.5%), and
round-trips STEP. Failed checks do not advance the live revision. Every successful
output snapshots source/brief, their exact byte hashes, export hashes, relevant
tool hashes and backend versions. No repair/scale/placement fallback is applied.

## Ask for an edit without losing the original

> OpenPrintLab Designer: revise my-palette:r0001 to 80 mm diameter and eight
> wells. Keep the 8 mm height and 2 mm base, check spacing and preserve the
> original. Show the actual new geometry and explain remaining evidence gaps.

```powershell
python -m tools.cli design-revise my-palette
```

This copies the latest published source/brief into the next draft, not over
the old output. Edit `r0002/source.py` and/or `r0002/brief.json`, update the
acceptance/dimension contract, review again and run that source with its new
digest. The same viewer URL updates to the newly published revision. Old
`r0001/output/` remains addressable and downloadable.

Only one publisher can run per design; overlapping writes fail. A stale lock
after a terminated process is an explicit blocker: establish that no publisher
is active before removing that design's `.publish.lock`. Published outputs are
never overwritten by the tools, but are ordinary local files; do not edit them.
Revision hashes detect altered published source when copying forward.

## Evidence and boundaries

The CAD model and geometry-derived preview are generated; the documented checks
are software evidence. Actual hardware/profile selection remains separate.
[Offline slicing](offline-slicing.md) may be performed without a printer, but
this workflow does not slice automatically or inherit slicer/physical evidence.
All initial reports state **not validated for hanging/load use**.

Custom artifacts stay under ignored `build/` by default. Only the deliberately
published palette examples are product content. Source licenses and attribution
are preserved as declared; do not import assets without permission.

The [007 ledger](../devtool/features/007-authoring-roadmap/plan.md) records the
inspected text-to-cad implementation. We adopted its useful separation of stable
identity and read-only preview as a design idea, not its code, installer, telemetry,
second CAD backend or complete document engine.
