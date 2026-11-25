# Select OpenPrintLab Designer

[OpenPrintLab Designer](../.github/agents/openprintlab-designer.agent.md) is a
repository custom agent. **`AGENTS.md` is shared repository instructions, not
a selectable agent definition.** The profile delegates to the existing skill
and safety guides rather than maintaining a second set of rules.

## Discovery and invocation

Open a trusted, updated **full OpenPrintLab checkout**. The profile needs local
file read/search/edit and command execution; web research is useful for official
documentation. Tool permissions still belong to your client. No model is pinned:
the client/session's model selection is inherited.

| Client | Selection / scope |
|---|---|
| Copilot CLI | Start `copilot` from the checkout, then `/agent` and select **OpenPrintLab Designer**. The documented command-line alternative is `copilot --agent=openprintlab-designer`; the identifier is the filename stem. Review trust/tool prompts. |
| VS Code Copilot harness | Open the checkout; use Chat's Agent dropdown to select **OpenPrintLab Designer**. If missing, inspect **Chat: Open Customizations > Agents** and file errors; refresh/reload as appropriate for your version. |
| GitHub cloud agent | Select this repository/branch and the custom agent in GitHub's agent picker after the definition is on that branch. Python/CAD availability belongs to that execution environment; a local desktop preview URL is not remotely reachable. |
| Other desktop/client surfaces | Repository-agent loading and refresh rules vary. Do not assume this conversation hot-loads the file or that every client supports it. If no compatible picker exists, explicitly ask your tool-capable assistant to read the profile and canonical skill; that is instruction use, not native agent registration. |

Example after selecting the agent:

> Customize a dry desk organizer to 120 x 80 x 18 mm with three compartments.
> Preserve prior outputs and show the actual geometry and downloads.
> Ask for my actual printer, nozzle, plate and filament before print advice.

The baseline needs Python 3.11+. Rounded templates require the separately
installed optional CadQuery environment in the [template-lab walkthrough](template-lab.md).
Selecting an agent installs neither Python nor CAD, starts no viewer and gives
no automatic permission to execute source. The profile uses CLI tools and does
not silently configure MCP or other agents.

## Using it alongside another workspace

Prefer opening the OpenPrintLab checkout as its own workspace. In Copilot CLI
1.0.114, `--add-dir` documents loading a trusted directory's `.github/agents`
and `.github/skills`; add your approved checkout when starting from elsewhere,
then select the same agent. This grants additional file/configuration access:
review that trust boundary. The agent must run OpenPrintLab commands from that
checkout, and not overwrite unrelated work in the calling workspace.

For clients without additional-directory discovery, a user may manually copy the
profile into the destination repository's `.github/agents/` and give it the
approved full-checkout path. Do not copy only the skill and expect tools, sources
or safety references to travel with it. Check for an existing profile before
copying; maintain the copied profile when OpenPrintLab changes. No global
installation or user configuration change is performed by this project.

Offline Bambu Studio slicing is permitted without a physical printer. Local
toolpaths are disposable inspection artifacts, not downloads to publish or jobs
to send. Project-open/round-trip, actual toolpath review and physical evidence
are distinct; see the [offline slicing policy](offline-slicing.md).

## Evidence and references

Validated against GitHub's current profile schema on 2026-11-25: required string
description, optional name and tool aliases, Markdown body below 30,000 characters.
The local Copilot CLI **1.0.114** help was checked for `--agent` and `--add-dir`.
This is schema/help evidence, **not** a completed native picker or model-run
certification in CLI, VS Code, GitHub cloud or this desktop session. Existing
CLI/model workflows are independently software-tested; no physical print claim.

- [GitHub profile schema](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [GitHub creation and selection](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents)
- [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [Copilot CLI usage](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview)
