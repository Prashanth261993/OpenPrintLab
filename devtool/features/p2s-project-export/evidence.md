# P2S native round-trip and local slice evidence

Status: **experimental; exact-fixture native open/save/reopen and local slicing
passed, complete visual layer/warning review remains blocked**.

The user granted an uninterrupted Bambu Studio verification window after the
initial attempt. The follow-up below supersedes the initial UI interruption
blocker; it does not promote every exported variant to slicer-checked.

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

## Native open/save/reopen: passed for this fixture

The generated project opened as a project, not just a mesh. Prepare and the
reopened project exposed P2S, 0.4 mm, Standard flow, Textured PEI Plate,
PLA Basic and the modified `0.20mm Standard @BBL P2S` process. Actual settings
showed 0.2 mm layers, three walls and 20% grid infill.

Save As produced a **different** unsliced file; original overwrite prompts caused
by a file-dialog value update not reaching its internal state were declined.
The original's SHA-256 remained unchanged. The saved file was reopened in Studio.
`compare_saved_project` passed against the actual saved file: all 72 oriented
triangles and their placement, hence 48 x 24 x 16 mm dimensions, and **all
explicitly exported settings** were retained. Studio removed the custom
`Metadata/openprintlab/` entries. Retain the original export/passport, not only
the app-saved copy.

The saved settings also record PLA Basic / 1.75 mm filament, 0.98 flow ratio,
220 C nozzle and 55 C textured-plate temperatures. These are observed profile
values, **not generic print recommendations**.

| Artifact | SHA-256 |
|---|---|
| Original unsliced candidate | `911d2cac1b5883a4595c48578a1817fa83a464209cb7a7b539f062da6b4c8901` |
| Actual Studio-saved unsliced copy | `e2d6a84e3397957167252d43fa72a6522b4f6710251736385483a9b501cd8be9` |
| Local-only sliced archive; not published | `b8d952a0be33f003156bbbb879f9f23db6f7ee9f386f0c357cab7a4d60cec3de` |
| Local-only toolpath member; not published | `d6914580689c8fa8509a2e88b29f9645f09cdbc1e047b0128ac37dfbe5fa7e71` |

![Actual Studio-saved model thumbnail](studio-saved-thumbnail.png)

This is Studio's saved geometry thumbnail, **not a UI screenshot, physical photo
or toolpath-review image**. The native screenshots were observed through
Computer Use in the session; they are not standalone committed screenshots.

## Local slice: generated; visual review incomplete

Actual Bambu Studio slicing completed. Its native **Export plate sliced file**
operation produced a separate local-only `.gcode.3mf` in ignored storage.
There was no printer connection, device inspection, synchronization, send or
print action. Ordinary Save Project produced an unsliced project even after
slicing, so the distinct sliced-file export was necessary for durable local
slice evidence. No sliced archive or G-code is included in this commit.

Observed output facts:

- 80 layers, with emitted Z heights exactly 0.2, 0.4, ... 16.0 mm.
- Slice metadata: `outside=false`, `support_used=false`, zero pauses.
- Slicer estimates: **17m 04s total** (10m 02s model printing), **6.73 g** and
  approximately **2.22 m** filament; these are not actual print measurements.
- Read-only toolpath metadata inspection found outer-wall feature blocks on
  all 80 layers, bottom surface at layer 1, and top surfaces at 20/40/60/80.
- Bridge feature blocks occur at **16/36/56/76**. "Floating vertical shell"
  feature blocks occur at **15/21/22/35/41/42/55/61/62/75**. These are slicer
  feature classifications, not automatic errors or evidence of safe bridging.

The actual Preview and a slider-adjusted view displayed the stepped toolpaths
and grid infill. However, Computer Use rendered the ImGui legend, layer values
and warning areas as unreadable black blocks, without accessible text nodes.
Exact visual layer numbers, full shell continuity, islands/bridges and complete
warning disposition therefore **could not be verified**. The file-derived
metadata above is complementary evidence, not a replacement for that review.
Do not mark the complete slicer-review acceptance gate passed.

On initial open, an informational "Parameter recommendation" suggested enabling
clumping detection by probing. It was recorded and closed without changing
settings or disabling protection. It does not establish a no-warnings result;
the unreadable Preview warning area remains unresolved.

The next reviewer should inspect layer 1, all step transitions, and especially
the bridge/floating-shell layers listed above in a correctly rendered native
Preview. No physical adhesion, fit, quality, strength or creep evidence exists.

## Initial interruption and application environment

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

That initial attempt had no successful project open or slice. After the user
explicitly granted the uninterrupted window, native work resumed using fresh
observations and the normal engine permission rules; the outcomes above were
then obtained. No new user-interruption gate was bypassed.

The initial policy restriction on local slicing was superseded by the user's
explicit approval and policy commit
`509677fcfb149928533941c901b7ee49d989095e`, whose offline guide and updated skill
were read. Policy is no longer the blocker; incomplete native Preview perception
is the remaining review limitation.

## Automated checks

Focused tests cover exact float32 triangle/winding preservation, originals and
passport retention, deterministic output, non-overwrite, preset parents/includes
and hash drift, unsupported/missing/ambiguous/conditional profiles, malformed
meshes/passports, finite/count/range overrides, placements, package relationships,
content types, UUIDs, member hashes, extruder assignment and CLI errors.
Synthetic saved-copy tests exercise reordered faces/recentered coordinates and
setting/placement failures. A separate actual Studio-saved fragment fixture now
exercises the native layout and explicit settings, without redistributing full
profiles/G-code. See `tests/fixtures/bambu_project/README.md`.

The bounded source comparator checks installed resource identity only. Studio
can bind different cached/active profiles, so source hashes do not replace the
native selections/round-trip gate.

Recorded initial local results on 2026-11-25:

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

The follow-up has **13 focused tests**, including actual saved fragments.
Its full suite ran 44 tests: 42 passed, with the same two optional-CAD skips;
all 16 default model artifacts remained unchanged and the actual saved-project
comparison passed again.
[Sanitized native evidence](native-evidence.json) records the full dependency
hashes, exact archive comparisons, selected material values and slice facts.
The small saved XML/settings fixture and geometry thumbnail are deliberately
reusable evidence. No full production profiles, personal paths/accounts, sliced
archives or G-code are committed. Original input bytes and every source/member
hash remain in the preserved local candidate.

## Required continuation

Complete the native layer/warning review in `docs/bambu-project.md` without
claiming the observations transfer to other variants or profile revisions.
The original passport and fresh-export validation flags remain unchanged;
this exact-fixture evidence is attached separately. Retain the experimental
label until the remaining review gate is satisfied.
