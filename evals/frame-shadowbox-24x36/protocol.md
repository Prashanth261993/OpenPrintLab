# Frozen two-arm experiment protocol

Freeze ID: `frame-shadowbox-24x36-v1`.
Status: **both fresh design sessions launched**, as reported by the coordinator
on 2026-11-11. No candidate outputs have been inspected by this administrative task.

## Actual launch record and authority

The exact coordinator-owned launch-prompt artifact is copied byte-for-byte into
[`actual-prompts.md`](actual-prompts.md). Its common preamble, common design prompt,
common scoring and the corresponding arm-specific condition/handoff concatenate
into each actual kickoff prompt. It takes precedence over wording differences in
the earlier administrative brief or protocol. Original user quotes and confirmed
clarifications remain in `brief.md`.

| Condition | Actual session ID | State |
|---|---|---|
| With toolkit | `2d9929e5-abdd-4dcd-a460-dc99f0472f94` | launched; outputs not collected |
| Independent no-product baseline | `0a781a5e-151a-4763-bca7-a60ac9e00b3b` | launched; outputs not collected |

Both creations inherited the parent model configuration without overrides.
No elapsed-time, token or spending ceilings were requested or set. Resolved
model versions and actual metrics remain to be reported, not guessed.

**Chronology:** the coordinator froze common text in the actual launch messages
and created both sessions before this repository archival commit. The repo-first
pre-launch archival gate was therefore not met for this initial run. Preserve
that procedural difference rather than claiming a Git freeze existed earlier.
No product changes or candidate collaboration are authorized.

## Common inputs and starting revisions

Both arms receive the same frozen `brief.md` and `rubric.md`, with the same
inherited model settings. Record resolved agent/model versions and any differences
that are actually observable; do not invent missing metadata.

The starting **product code revision** is:

```text
8d78523aa68fc1973b61c16fa435d1550833ecd4
```

This was verified as repository HEAD before this documentation-only assignment.
No runtime product code has changed in the administrative update. Freeze this code
revision separately from the later **administrative documentation commit** that
contains this brief, rubric, protocol and `freeze.json`. The coordinator records
the actual starting checkout revision and later administrative archive revision
in the run manifest; do not claim that later archive revision was supplied before
launch or confuse it with a new product capability.

The brief/rubric/protocol hashes in `freeze.json` refer to committed UTF-8/LF
Git-blob bytes. `actual-prompts.md` additionally preserves the exact source bytes
through a path-specific `-text` Git attribute, and its hash matches the
coordinator-owned artifact. If a common input changes, create a
new freeze/run version and disclose it; do not silently amend an active comparison.

## Exactly two fresh sessions

The coordinator launched exactly **two new, fresh design sessions**, not reused
sessions with prior design context:

- **Product arm:** current shipped OpenPrintLab code/skills/tools at the frozen
  product revision, in its own worktree.
- **No-product baseline:** a fresh non-project workspace, with **no OpenPrintLab
  source/skills or previous conversation**.

Both may use standard CAD libraries and publicly available non-product
documentation, including the same public references in the common brief.
Prepare independent optional environments and record differences.
Neither arm uses the `wilsonwaters/3d-printing` toolkit. The baseline also does
not use another prepackaged domain-specific agent skill, as stated in the actual
baseline prompt.

No arm sees the other's outputs. There are no shared refinements. Record which
neutral A/B label maps to which condition in the run manifest; the parent knows
the mapping and the evaluation is not claimed to be parent-blinded.

The product arm uses the product **as shipped**. It may author task-specific
source if necessary, but must report where supported product workflow ends and
custom engineering begins. **Do not change core product code to pass the test.**
Preserve a diff/check proving that boundary.

## Permissions and execution boundary

No printer connection, automatic printing, purchases, paid generation API or
external service upload. Only generated frame designs and brief/evaluation
artifacts are in scope for repository ingestion, not automatic publication of
the user's art itself. Respect source and asset licenses.

There are no hidden time/token caps. Record observable elapsed time and usage,
and any actual platform limitation encountered, without inventing costs.
Keep failures and attempts visible rather than reporting only the successful
last attempt. Do not fabricate unavailable usage or cost measurements.

## Neutral evaluation and presentation

The parent independently performs equivalent requirement/geometry checks on
both outputs, then applies the frozen rubric to manufacturability, appearance
and instructions. This does not substitute for physical validation.

Before evaluating outputs, record the common camera, projection, framing/scale,
lighting, background, resolution and renderer/version used for the fixed-camera
views. Apply the same settings to both, label assembly versus printable-part
views, and do not adjust one arm's presentation to conceal defects.

The parent knows arm identity; user-facing presentation uses A/B labels. Critical
failures are reported separately from the 100-point score. This is one case study,
not a universal superiority claim.

## Repository-owned record

Ingest final prompts, source, versions, output artifacts, redacted logs/check
evidence, available metrics and parent evaluation under this benchmark folder.
Exclude secrets, user art outside the agreed scope, virtual environments and
cache files. Preserve licenses/notices and provenance for each reused artifact.

Proposed record layout (future run files are not present or fabricated now):

```text
results/<run-id>/
  manifest.json
  prompts/
  arm-a/
    source/
    outputs/
    renders/
    evidence/
    trace.redacted.md
    metrics.json
  arm-b/
    source/
    outputs/
    renders/
    evidence/
    trace.redacted.md
    metrics.json
  evaluation.md
```

The actual product-arm handoff path is
`evals/frame-shadowbox-24x36/arms/with-toolkit/` in its own worktree. The baseline
works in its independent session-owned deliverables directory. The coordinator
will archive those exact baseline deliverables into this benchmark **after
completion**; temporary execution outside the repo is not their final storage.
Use the results manifest to link the final ingested arm paths without duplicating
or silently rewriting originals. Do not fetch running candidate outputs or feed
designs between arms.

The manifest binds frozen input hashes, starting/archive revisions, arm mapping,
resolved versions/conditions and output hashes. Large artifacts require an
approved repository-owned storage approach rather than session-only copies or
expiring links.

## Administrative step only

This commit persists common inputs, exact actual prompts, launch metadata and
roadmap. This administrative session creates no frame design, starts no arm,
installs no tool and adds no evaluation runner. Launches were performed separately
by the coordinator; no candidate outputs were fetched for this update.
