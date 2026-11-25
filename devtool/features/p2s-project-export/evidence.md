# P2S export evidence and remaining native gate

Status: **experimental; application acceptance not established**.

## Environment and scope

On 2026-11-25, the installed Bambu Studio executable reported file version
`02.09.02.62`. The bundled BBL vendor manifest reported `02.09.00.89`.
The exact machine/process/filament chains were read from installed official
resources, including parent and `include` files. They are recorded by relative
path and byte hash in each generated project's manifest, not redistributed.
The test combination is P2S / 0.4 mm / Direct Drive Standard / 0.20mm Standard /
Bambu PLA Basic / Textured PEI Plate. These are offline test assumptions.

The known shipped `step-study` STL is 48 x 24 x 16 mm, source SHA-256:
`2c960fa1e38497cf5bb611c232b7b3119791727761780b0501ecd3e32a463ef9`.
Its original passport was not modified. Generated projects and receipts are
kept in ignored local storage, not default model exports.

## Native attempt and exact blocker

The already-installed application was launched through Computer Use. It
automatically displayed a network plug-in download/install-complete dialog.
No installer command, login, account/device selection or printer operation was
requested. The completion dialog was acknowledged before navigating to Open
Project. This observation means **network isolation is not established**;
"offline slicing" describes local computation/no printer job, not a no-network
claim about Studio.

Open Project reached the native file dialog. Attempts to enter the generated
path returned `user input was detected in Bambu Studio` interruptions, including
after fresh observations. Native actions were paused at the coordinating
session's direction. No shell launch/file-open workaround or alternate UI route
was used. No profile settings/preferences or live printer settings were edited.

Consequently, there is **no successful project open**, no verified selection or
native mesh-size observation, no save/reopen, no actual slice and no toolpath
review to report. Screenshots of a file dialog would not establish compatibility
and are not published as evidence. No machine G-code was generated/distributed
by this slice. Resume only after an explicitly uninterrupted verification window.

The initial policy restriction on local slicing was superseded by the user's
explicit approval and policy commit
`509677fcfb149928533941c901b7ee49d989095e`, whose offline guide and updated skill
were read. Policy is no longer the blocker; UI interruption is.

## Automated checks

Focused tests cover exact float32 triangle/winding preservation, originals and
passport retention, deterministic output, non-overwrite, preset parents/includes
and hash drift, unsupported/missing/ambiguous/conditional profiles, malformed
meshes/passports, finite/count/range overrides, placements, package relationships,
content types, UUIDs, member hashes, extruder assignment and CLI errors.
Synthetic saved-copy tests exercise reordered faces/recentered coordinates and
setting/placement failures. They are **not actual app-saved fixtures**.

The bounded source comparator checks installed resource identity only. Studio
can bind different cached/active profiles, so source hashes do not replace the
native selections/round-trip gate.

Recorded local results on 2026-11-25:

- `python -m unittest tests.test_bambu_project -v`: 12 focused cases pass.
- `python -m unittest discover -s tests -q`: 43 tests, 41 passed and two optional
  CadQuery geometry tests skipped in the no-CAD interpreter.
- `python -m tools.release --check`: all 16 original model artifacts unchanged.
- `python -m tools.site`: four model pages and guides built successfully.
- Export with real installed P2S resources and `check-profiles`: passed; nine
  machine, four process and five filament dependency files hashed.
- Current experimental unsliced staircase project SHA-256:
  `911d2cac1b5883a4595c48578a1817fa83a464209cb7a7b539f062da6b4c8901`.
  Original source-report bytes SHA-256:
  `1e493312fb1d67fd06c28300f6dcdb80f11ddc555d622f95dec510ef3f8e50a8`.
  Translation is `(104, 116, 0)` mm. Explicit overrides are three walls, 20%
  infill and no brim. The inherited recorded process values are 0.2 mm layers,
  grid infill, five top/three bottom layers and supports off.

The hash identifies a **software-checked candidate**, not an app-accepted model.
Original input bytes and every dependency/member hash remain inside its local
manifest. No production profiles, app-saved fixture, screenshot with personal
paths, account data, or G-code are committed.

## Required continuation

Follow `docs/bambu-project.md` native acceptance instructions. Test the **current**
exporter output, not an earlier development artifact. Keep separate original and
app-saved unsliced projects plus local-only sliced output. Verify actual nozzle
flow selection and all explicit process fields, inspect warnings, compare files,
then perform the permitted local slice/layer review. Until then, retain the
experimental label and false app/slicer/physical flags.
