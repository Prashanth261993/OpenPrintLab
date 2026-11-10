# Your instructions, your assistant, real geometry

The template lab is a **local viewer and deterministic tool workflow**, not a
website chatbot. Your own compatible assistant interprets your instructions,
clarifies missing constraints and calls the CLI or MCP tools. OpenPrintLab does
not require its own hosted model, API key or paid generation provider.

A generic chat website or model alone cannot run these tools. You need a coding
assistant/client with permitted local command execution or stdio MCP support.
Your assistant's subscription and data-handling terms are separate; local CAD
does not imply the assistant itself runs offline.

## What is supported

| Generator | Editable operations | Intended use |
|---|---|---|
| `rounded-organizer` | Length/width/height, wall/base, compartments, corner radius | Dry desk or craft organization |
| `rounded-pen-rest` | Length/width/height, wall/base, channels, corner radius | Shallow rest for measured pens |
| `paper-card-stand` | Length/width/height, base, slot width/end margin, corner radius | Lightweight paper/photo cards only |

The original four models also work with the non-destructive `customize` command,
using the builtin backend without CadQuery. They export STL, not STEP.
The three new CAD generators export both STL and STEP.

Supported aesthetics are defined operations: square/rounded corners and repeated
compartments or channels. This is not arbitrary sculpting. Text nameplates are
deferred until a specific font binary, redistribution terms and glyph geometry
are tested; arbitrary system fonts are not silently substituted. External
STL/STEP/3MF editing/import remains future work.

## Windows: browse without installing CAD

From your clone's root:

```powershell
python -m tools.lab --port 8766
```

Open **http://127.0.0.1:8766/**. This seeds the deliberately published examples
and serves only the variant directory on loopback. Keep the terminal open;
Ctrl+C stops it. If that port is in use, use the existing known lab or choose
another port; do not terminate unrelated processes.

The browser previews exact exported STL geometry. It has no upload box or AI
prompt field. Give new instructions in your assistant and refresh the lab after
the tool finishes. The original catalog can still run separately on port 8765.

## Windows: opt into generation

Python 3.12 is the tested CAD setup. Keep the dependency-free environment:

```powershell
python -m venv .venv-cadquery
.\.venv-cadquery\Scripts\python.exe -m pip install -e ".[cadquery,mcp,test]" -c experiments\cadquery\constraints.txt
.\.venv-cadquery\Scripts\python.exe -m tools.cli templates
.\.venv-cadquery\Scripts\python.exe -m tools.cli template rounded-organizer
```

CadQuery alone measured approximately 1.21 GB in T-05; MCP/browser test extras add
more. Installation is explicit, never automatic, and uses no provider API.
CadQuery/OCP package/native dependencies retain their own licenses (including
OCCT and CasADi obligations); see the
[experiment report](../experiments/cadquery/report.md). Original model sources
and outputs are CC BY 4.0; tooling is MIT.

## One complete custom result

Example instruction for your own assistant:

> Read AGENTS.md and use create-printable-model. Make a 120 x 80 x 18 mm
> rounded organizer for dry desk bits, three compartments, 8 mm corners,
> 2.4 mm walls and a 2 mm base. Preserve the original. Name it my-desk-organizer
> and show me the actual geometry preview, STL, STEP and passport.
> Ask for my actual hardware before recommending settings. Do not control a printer.

The assistant should discover the schema and then execute the equivalent of:

```powershell
.\.venv-cadquery\Scripts\python.exe -m tools.cli customize rounded-organizer --variant my-desk-organizer --set length=120 --set width=80 --set height=18 --set compartments=3 --set radius=8 --set wall=2.4 --set base=2
```

Open **http://127.0.0.1:8766/my-desk-organizer/** with the lab running, or open
the returned local HTML preview URI directly. The bundle under
`build\variants\my-desk-organizer` contains:

- Actual mesh-derived SVG and HTML viewer, never an illustrative AI image.
- STL, STEP for this backend, effective parameter JSON and editable source ZIP.
- Passport with template version, source/backend/export settings, exact file
  hashes, fresh geometry checks and explicit missing slicer/physical evidence.

This example prompt is mapped to tool parameters by the assistant, not a hidden
natural-language parser. Unknown dimensions, impossible features or ambiguous
style must be clarified, not guessed into a claim of success.

Repeating a name **fails without overwriting**. Ask for `my-desk-organizer-v2`
for a revision. To use the previous parameters as a starting point:

```powershell
.\.venv-cadquery\Scripts\python.exe -m tools.cli customize rounded-organizer --variant my-desk-organizer-v2 --params build\variants\my-desk-organizer\parameters.json --set length=140
```

The second variant preserves the first. Fresh geometry/source/backend identity
means no inherited slicing or print evidence. Cross-platform tessellation and
STEP timestamps can differ; feedback must name the exact artifact hash.

More prompts:

> Make a rest for three pens, 90 mm long and 54 mm wide, 8 mm tall with
> 6 mm corners. Show nominal channel width; do not promise friction fit.

> Make a stand for a lightweight paper card, 90 x 30 x 12 mm, 2 mm slot,
> 3 mm base and 4 mm corners. Show the real preview and download files.

## Setup/profile/material questions

```powershell
python -m tools.cli guidance my-desk-organizer
python -m tools.cli guidance my-desk-organizer --printer "Bambu Lab P2S" --nozzle 0.4 --plate "Textured PEI" --material PLA --use desk-organization
```

The first command returns `needs_input` and the missing actual setup. The second
returns **suggested starting points**, model-specific notes and official sources.
Other printers/nozzles/materials or unsupported uses return `unsupported_setup`,
not a fabricated preset. The agent can explain this boundary and consult official
documentation, but cannot label the result tested. Never supply serials,
credentials or network identifiers.

Choose your actual printer, nozzle, plate and filament preset in Bambu Studio.
For the example, expect a 120 x 80 x 18 mm base-down organizer with three open
compartments. Inspect the first layer, all shell closures and warnings. Supports
off is only a starting suggestion. A human offline slice is the next check;
physical verification remains pending.

## MCP and compatibility

Use the same server as V1, but point a CAD-capable client at the optional
environment. For clients using `mcpServers` (other clients use different wrappers):

```json
{
  "mcpServers": {
    "openprintlab": {
      "command": "C:\\src\\OpenPrintLab\\.venv-cadquery\\Scripts\\python.exe",
      "args": ["-m", "tools.mcp_server", "--cadquery"],
      "cwd": "C:\\src\\OpenPrintLab"
    }
  }
}
```

Replace paths with your clone. Keep the client's tool-write approval enabled.
`--cadquery` explicitly initializes the native CAD stack before the async server
starts. Without it, discovery and builtin tools work, but CAD export returns an
actionable enablement error. This avoids lazy native-import stalls observed on
Windows under an already-running MCP event loop.
New shared tools: `list_templates`, `describe_template`, `create_variant`,
`variant_guidance`. Original model tools remain available. Variant writes are
confined to `build/variants`; MCP never accepts an arbitrary output path.
No arbitrary source execution, provider calls or printer controls are exposed.

| Surface | Evidence boundary |
|---|---|
| CLI from this tool-capable coding-assistant session | Actual generation and local preview are exercised |
| Official Python MCP SDK over stdio | Protocol/tool integration tested; not a certification of every UI client |
| Generic MCP-capable clients | Compatible protocol expected; follow client-specific setup/approval docs |
| Standalone Copilot CLI, Claude Desktop, Cursor and other named client UIs | Not individually certified by these tests |
| Plain chat webpage/model without local tools | Cannot perform this workflow by itself |

## Verify

```powershell
python -m unittest discover -s tests -v
python -m tools.release --check
.\.venv-cadquery\Scripts\python.exe -m unittest tests.test_cadquery_templates tests.test_variants -v
.\.venv-cadquery\Scripts\python.exe -m tests.mcp_smoke
.\.venv-cadquery\Scripts\python.exe -m tests.lab_browser_smoke
```

Tests without CadQuery explicitly skip the optional geometry cases; the dedicated
optional-backend CI environment must run them. No test creates physical evidence.
