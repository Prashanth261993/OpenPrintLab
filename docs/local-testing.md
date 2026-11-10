# Local testing on Windows

The dependency-free V1 catalog and model tools are ready for a local trial.
No paid provider, API key, AMS or printer connection is needed.
**No model has yet been sliced or physically printed by this project.**

## Choose your checkout directory

```powershell
Set-Location 'C:\src\OpenPrintLab'
```

Replace this example with your clone's absolute directory. In a managed worktree
session, use the session's working directory, not the separate primary checkout;
renaming a branch does not rename its directory. The exact active workspace path
is provided in the local-ready handoff, rather than published in this guide.
Python 3.11+ must be on PATH.

## Build, customize and validate

Run these commands from that directory:

```powershell
python -m unittest discover -s tests -v
python -m tools.release --check
python -m tools.site
python -m tools.cli parameters pocket-tray
python -m tools.cli check pocket-tray --set length=120 --set width=80 --set height=18
python -m tools.cli build pocket-tray --set length=120 --set width=80 --set height=18 --output build\local-trial
```

Expected: tests pass, committed artifacts are consistent, and a 120 x 80 x 18 mm
tray is exported to `build\local-trial\pocket-tray.stl` with an accompanying
`pocket-tray.report.json`. The report must say geometry passed and
slicer/physical evidence not performed. Repeating the export replaces those files.
Do not run `release` without `--check` just to hide a stale-artifact failure;
inspect the source/default changes first.

## Preview the catalog

A detached preview for this session was started and checked at
**http://127.0.0.1:8765/** on November 10, 2026. If it is still running, open that
address without starting a second server. To start a fresh preview:

```powershell
python -m tools.site
python -m http.server 8765 --directory site --bind 127.0.0.1
```

Keep that terminal open. In a second terminal:

```powershell
(Invoke-WebRequest http://127.0.0.1:8765/ -UseBasicParsing).StatusCode
```

Expected: `200`, four catalog cards, working search/category filters and model
downloads. Stop a foreground server with Ctrl+C. If port 8765 is already in use,
use that known preview or choose another port; do not kill an unrelated process.
Only localhost is bound. Regenerate with `python -m tools.site` after site/content
changes, then reload the browser.

## First human Bambu Studio smoke test

Use the **default Layer staircase**, not a customized part for the first trial:
`models\exports\step-study.stl`, nominal **48 x 24 x 16 mm**.

1. Download/open the STL and keep its accompanying report/passport.
2. Select the actual **P2S**, installed nozzle, plate and PLA preset in Bambu
   Studio. No P1S substitution; no assumption of AMS. Record Studio version.
3. Confirm millimeter dimensions and place the full rectangular base down at Z=0.
4. With an actual 0.4 mm nozzle, consider 0.20 mm layers, 3 walls, 4 top/bottom
   layers and 15% infill as starting suggestions. Keep actual preset
   temperatures/speeds. Start supports off; inspect rather than trust the suggestion.
5. Slice and move the layer slider from base to top. Expected candidate behavior:
   one connected footprint, closed bases and step tops, no floating starts,
   no required support structures in this orientation, no unresolved warnings.
   Each tread is 12 mm long and each rise is 4 mm. If the preview differs, stop
   and report it; do not mark the test successful.
6. This is a **slicer** smoke test until you deliberately start and complete a real
   print. If you choose to print, follow the full beginner safety guide, watch the
   first layer safely, and record success, partial success, failure or a stopped trial.

File a [print-result report](https://github.com/Prashanth261993/OpenPrintLab/issues/new?template=print-result.yml)
with exact model version, variant ID, STL SHA-256 and actual settings, plus
screenshots/photos when available. It is a public issue; remove personal details,
serials and credentials. A report does not automatically certify the model.

## Integration boundary

See [../plan.md](../plan.md) for staged reuse of CadQuery and optional AI providers.
The first proposed CadQuery experiment and any Meshy trial await user review.
They are not prerequisites for this local test and are not installed.
