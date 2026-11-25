# Repository-scoped OpenPrintLab Designer package

[Download the verified source package](https://prashanth261993.github.io/OpenPrintLab/downloads/openprintlab-designer.zip).
This is a **complete committed source snapshot**, not a global plugin installer
or a claim that every assistant accepts the same agent format.

It includes the named profile, canonical skill/guides, sources, examples, tests
and licenses so references do not silently disappear in another workspace.
`PACKAGE.json` lists the Git commit and SHA-256 of every member. No `.git`
history, ignored `build/` models, credentials, environments, telemetry,
auto-updates, client configuration or third-party runtime is installed.

## Inspect and install

From an existing trusted full checkout with Python 3.11+:

```powershell
python -m tools.distribution inspect path\to\openprintlab-designer.zip
python -m tools.distribution install path\to\openprintlab-designer.zip --destination C:\work\OpenPrintLabDesigner
```

Choose a **new** destination with an existing parent. The installer refuses
existing directories; it never merges into your other repository or replaces
agents there. Hashes, paths, symlinks, duplicate names and archive limits are
checked before files are written. Hashes detect changes/corruption, not a trusted
publisher's signature: obtain the archive from the official project and review it.

Open that directory as a workspace and select **OpenPrintLab Designer**.
Alternatively, a compatible Copilot CLI can explicitly trust/add that directory
using `--add-dir` from another workspace; see the
[client-specific discovery guide](designer-agent.md). The toolkit's commands
still run in the installed directory. No automated global registration occurs.

The original model CLI works with Python alone. Optional CadQuery/MCP/browser
dependencies need their own isolated installation under the
[template-lab instructions](template-lab.md). No environment is bundled.
This package is not a Git checkout; repackaging and building the website's
committed-source download require the original Git repo. Runtime model CLI and
local viewers do not require Git history.

## Reproduce or remove

```powershell
python -m tools.distribution build build\packages\designer-snapshot.zip
python -m tools.distribution uninstall C:\work\OpenPrintLabDesigner
```

Build packages **committed HEAD** with deterministic member ordering/timestamps,
not dirty changes. Existing output archives are refused. The website generates
its package from the verified deployment commit.

Uninstall runs from the original toolkit checkout, not inside the directory
being removed. It removes only an intact marked installation and refuses any
changed/missing/extra file or directory. User models, virtual environments and
Python caches count as extras: preserve or remove them deliberately first,
or manage the installation manually. It never edits your client settings;
remove an explicit `--add-dir` selection from your own invocation if needed.

Tests exercised deterministic bytes, actual extracted CLI execution, refusal
to overwrite, changed/extra-file preservation and clean removal. Native
Copilot/VS Code picker integration is documented, not certified by these file
tests. Cross-assistant global installers remain out of scope.
