---
artifact: plan
feature: 004-reuse-roadmap
status: planning
updated: 2026-11-11
tasks: [T-01, T-02, T-03, T-04, T-05, T-06, T-07, T-08]
---

# 004 - Durable roadmap and reuse backlog

## Objective

Track the next product capabilities and useful upstream ideas in one repository
spine. **Approval to track is not approval to implement.** This documentation-only
assignment does not build features, design the frame or launch comparison agents.

## Current state

The working product is [milestone 003](../003-template-lab/plan.md): original
dependency-free models, optional CadQuery templates, non-destructive variants,
real previews, CLI/MCP and honest evidence. The
[002 plan](../../../plan.md) and [T-05 experiment](../../../experiments/cadquery/report.md)
retain their history. The current frame A/B effort is
[frozen actual launch inputs, two arms launched](../../../evals/frame-shadowbox-24x36/README.md).

Tracking is approved by the user's 2026-11-11 request that plans and useful reuse
ideas live in the repo rather than only the session. Product items remain
blocked on separate implementation authorization. The coordinator subsequently
supplied the frozen comparison inputs and exact prompts for two sessions it has
now launched. T-08 is in progress under that coordinator, not permission for this
administrative session to design, launch or inspect either running candidate.

## Phases

- [x] Record user priorities, source provenance and history.
- [x] Persist proposed requirements, backlog and evaluation hold.
- [ ] Approve a bounded implementation plan for any selected item.
- [ ] Implement and verify that approved item.
- [x] Persist the coordinator-supplied frozen benchmark inputs.
- [x] Record coordinator-reported launches and exact actual prompts.
- [ ] Coordinator collects completed outputs and evaluates; no candidate work is inspected here.
- Red-team - not commissioned; future source-execution/install boundaries need review.

## Priorities, sources and dependencies

Priorities are recommended sequencing, not launch instructions. Dependencies
reflect actual prerequisites, not the order of this table.

| Item | Priority | Scope / source | Prerequisite and release gate | Status |
|---|---|---|---|---|
| T-02: controlled new design | 1 - suggested next | Beyond fixed templates, editable source, explicit unsupported cases; user direction, U-01 | Existing 003 pipeline; R-02 brief/source/permissions/geometry gates | tracked; not authorized |
| T-03: P2S project-3MF + slicing | 2 - suggested next | Actual printer/process/filament preset project, not just mesh-in-ZIP; user direction, U-02 | Can start with an existing variant, not dependent on T-02; R-03 actual Studio review | tracked; not authorized |
| T-04: cross-assistant packages | 3 | Generated adapters and plugin/skill ZIPs from one source; user direction, U-06/U-07 | Existing CLI/MCP contract; R-04 clean-install/permission/client evidence | tracked; not authorized |
| T-05: reusable design patterns | 3 | Mechanical fasteners, supports, material/tolerance patterns with failed/unprinted evidence; user direction, U-01/U-04 | Existing passport schema; R-05 scoped claims and evidence. No universal upstream load ratings | tracked; not authorized |
| T-06: OpenSCAD + assembly | later extension | Broader source authoring/editing, multi-part BOM/assembly flow; U-01 | T-02 control boundary and T-07 assembly checks; add T-03 if a Bambu project is claimed | tracked; not authorized |
| T-07: assembly/orientation checks | enabling research | Collisions, Z=0, overhangs, first-layer islands; U-03 | Existing geometry pipeline and synthetic fixtures; does not need T-06 implemented first | tracked; not authorized |
| T-08: controlled A/B benchmark | separate research track | No-product baseline, objective checks, fixed-camera renders and available cost/time metrics; user challenge, U-05 | Common text frozen in launch messages; exact prompts/IDs archived after launch. Does **not** depend on T-02 through T-07 | two fresh arms launched; outputs not collected |

## Tasks

The required verification commands for future tasks are **proposed interfaces,
not tools that exist today**. Human slicer/evidence gates cannot be replaced by
an invented green command. Ownership paths are proposed and must be confirmed
in the selected item's implementation plan.

| ID | Task | Req | Depends on | Files owned | Parallel group | State | Verification |
|----|------|-----|-----------|-------------|----------------|-------|--------------|
| T-01 | Retain the completed runnable walking skeleton and its evidence | R-01 | - | Existing `README.md`, `tools/lab.py`, milestone 003 evidence; no code changes assigned here | - | done | Existing: `python -m tools.lab --port 8766`; `python -m tools.release --check`; [implementation CI](https://github.com/Prashanth261993/OpenPrintLab/actions/runs/42926464493) |
| T-02 | Plan and build a bounded new-design authoring workflow after approval | R-02 | T-01 | Proposed `tools/new_design.py`, `tests/test_new_design.py`, `docs/new-design.md`, reviewed per-design source directories | - | blocked | Planned: `python -m unittest tests.test_new_design -v`; representative accepted/unsupported briefs, source/permission review and exact artifacts |
| T-03 | Plan and build Bambu project export with real P2S slicer evidence | R-03 | T-01 | Proposed `tools/bambu_project.py`, `tests/test_bambu_project.py`, `docs/bambu-project.md`, sanitized `evidence/slicer/` | - | blocked | Planned: `python -m unittest tests.test_bambu_project -v`; actual Studio open/round-trip/slice review and recorded project/preset hashes |
| T-04 | Generate installable adapters and skill/plugin archives | R-04 | T-01 | Proposed `scripts/build_adapters.py`, `scripts/build_skill_zip.py`, `adapters/`, `tests/test_distribution.py` | - | blocked | Planned: `python -m unittest tests.test_distribution -v`; clean Windows install/uninstall and per-client smoke matrix |
| T-05 | Establish scoped reusable pattern records and promotion rules | R-05 | T-01 | Proposed `patterns/`, `tests/test_patterns.py`, `docs/pattern-evidence.md` | - | blocked | Planned: `python -m unittest tests.test_patterns -v`; audit each claimed state against exact source, setup and success/failure evidence |
| T-06 | Extend controlled OpenSCAD source and multi-part assembly flow | R-06 | T-02, T-07 | Proposed `tools/openscad_backend.py`, `tools/assembly.py`, `tests/test_openscad_workflow.py`, `docs/assemblies.md` | - | blocked | Planned: `python -m unittest tests.test_openscad_workflow -v`; reviewed assembly/BOM and part checks; actual slicer gate where applicable |
| T-07 | Add bounded assembly and print-orientation diagnostics | R-07 | T-01 | Proposed `tools/assembly_checks.py`, `tests/test_assembly_checks.py`, `tests/fixtures/assemblies/` | - | blocked | Planned: `python -m unittest tests.test_assembly_checks -v`; known collision/contact, elevated-base, overhang and island fixtures with limits |
| T-08 | Run and evaluate exactly two fresh design arms from the frozen inputs | R-08 | T-01 | `evals/frame-shadowbox-24x36/` inputs/actual prompts are present; `results/` outputs/evaluation and future `evals/verify_run.py` are reserved | - | in progress | Future: `python evals/verify_run.py evals/frame-shadowbox-24x36/results/RUN_ID`; exact prompt hashes, equivalent checks, fixed views and human rubric; no runner implemented now |

No parallel execution is scheduled or authorized. Before scheduling, narrow
shared paths and prove disjoint ownership. T-01 is inherited evidence of the
already-working system, not a claim that new roadmap features were implemented
or re-tested during this documentation assignment.

## Evidence gates and uncertainty

| Item | Uncertainty | Required acceptance evidence / stop condition |
|---|---|---|
| T-02 | risky | Demonstrable brief -> editable new source -> real checked outputs, preserved originals, honest unsupported case; stop if the only implementation is arbitrary unreviewed code execution |
| T-03 | risky | Actual P2S/nozzle/plate/filament/process preset selections with origin/version/hash and overrides; stop on missing presets, changed defaults or unresolved Studio warnings. No printer connection is necessary for offline slicing |
| T-04 | unclear | One canonical instruction/tool contract, deterministic archive manifest/checksums, preserved notices and explicit permission model; do not claim clients tested solely because JSON was generated |
| T-05 | risky | Proven/failed/unprinted states plus separate geometry/slicer/physical evidence, scoped to version/settings. Material/strength/fit claims without relevant evidence stay unprinted/unverified |
| T-06 | risky | Reproducible part sources, transforms, BOM, assembly steps and export diagnostics; do not infer joint fit or safe assembly from a screenshot |
| T-07 | unclear | Positive/negative fixtures with specified geometric thresholds; collision contacts and mesh overhang heuristics are not universal physical/slicer truth |
| T-08 | risky | Common frozen inputs, equal opportunity/declared confounders, no product changes to favor an arm, complete artifacts and transparent missing metrics; no run while dimensional semantics or rubric remain unfrozen |

## Upstream reuse ledger

Source repository: [wilsonwaters/3d-printing](https://github.com/wilsonwaters/3d-printing).
The coordinator inspected the listed documents/scripts. For this tracking
update, their paths and the repository MIT license were verified at commit
`f5e18a16031f5a11b20f7753574ff48494891587` on 2026-11-11.
**No upstream tools were executed or installed, and no implementation was copied.**

| Source | Pinned reference | Candidate idea; qualification |
|---|---|---|
| U-01 | [designer skill](https://github.com/wilsonwaters/3d-printing/blob/f5e18a16031f5a11b20f7753574ff48494891587/.claude/skills/3d-print-designer/SKILL.md) | Broader OpenSCAD authoring/editing and multi-part assembly flow; not a claim that arbitrary designs are supported or printable |
| U-02 | [Bambu 3MF export](https://github.com/wilsonwaters/3d-printing/blob/f5e18a16031f5a11b20f7753574ff48494891587/.claude/skills/3d-print-designer/bambu-3mf-export.md) | Writer preserving actual project/printer/process settings; validate against our exact Studio/P2S setup, not merely archive structure |
| U-03 | [verification guide](https://github.com/wilsonwaters/3d-printing/blob/f5e18a16031f5a11b20f7753574ff48494891587/.claude/skills/3d-print-designer/verification.md) | Assembly collision, Z=0, overhang and first-layer-island checks; retain heuristics and unsupported-case limits |
| U-04 | [fastener patterns](https://github.com/wilsonwaters/3d-printing/blob/f5e18a16031f5a11b20f7753574ff48494891587/.claude/skills/3d-print-designer/pattern-fasteners.md) | Reusable mechanical/material/support/tolerance reasoning and evidence labels; upstream dimensions/load claims need local validation |
| U-05 | [evaluation approach](https://github.com/wilsonwaters/3d-printing/blob/f5e18a16031f5a11b20f7753574ff48494891587/evals/README.md) | Controlled agent A/B with a no-product baseline, objective checks, fixed views and available time/cost metrics; not inherited benchmark results |
| U-06 | [adapter builder](https://github.com/wilsonwaters/3d-printing/blob/f5e18a16031f5a11b20f7753574ff48494891587/scripts/build-adapters.py) | Generated client adapters rather than hand-maintained instruction forks; evaluate installation/permissions and tested-client claims |
| U-07 | [skill ZIP builder](https://github.com/wilsonwaters/3d-printing/blob/f5e18a16031f5a11b20f7753574ff48494891587/scripts/build-skill-zip.py) | Reproducible distributable skill/plugin archives with manifests and notices; no packages built or installed here |

[Pinned MIT license](https://github.com/wilsonwaters/3d-printing/blob/f5e18a16031f5a11b20f7753574ff48494891587/LICENSE).
Before any code reuse: inspect the selected files/dependency versions, retain
copyright/license notices, record modifications and provenance, and test the
behavior independently. The repository license is not blanket clearance for
every third-party model, font, image or material claim. Do not copy wholesale
or relicense upstream code as original CC BY content.

## Benchmark boundary

The frame comparison is an independent research track, not an implementation
test to tune product capability against. The coordinator supplied confirmed
dimensions and a frozen brief/rubric/protocol for persistence. This assignment
records those [common inputs and actual launch prompts](../../../evals/frame-shadowbox-24x36/README.md);
it does not choose a design, start an arm or inspect candidate work. The
coordinator has launched both sessions with inherited model settings and no
overrides or time/token/spending ceilings. The repository archive followed launch;
do not claim a pre-launch Git freeze. Product code is pinned separately
to `8d78523aa68fc1973b61c16fa435d1550833ecd4`; the later administrative commit
must not be mistaken for a capability change.

The final brief, rubric, protocol, source, outputs, fixed-camera renders,
available measured cost/time, failures and evaluation must be inspectable from
the repository without the originating session. Large artifacts need an approved
repository storage approach (for example Git LFS), not silent replacement with
session-only paths or expiring download links.

## Retained deferrals

Existing-template customization is shipped, not a reason to mark controlled
new-design authoring complete. Arbitrary external STL/STEP/3MF import/editing,
font/nameplate generation, browser-live CAD editing and paid decorative providers
remain separately deferred under [003 requirements](../003-template-lab/requirements.md)
and the [002 reuse plan](../../../plan.md). This backlog does not silently
activate those paths or replace the no-key local baseline.

## Open questions

| # | Question | Blocking? | Raised | Answer |
|---|----------|-----------|--------|--------|
| Q-1 | Which tracked product item should receive a bounded implementation authorization? | Implementation only | 2026-11-11 | Priorities recorded; no build authorization in this assignment |
| Q-2 | What are the frame units, measured dimensions, depth meaning and aesthetic requirements? | Resolved in common input | 2026-11-11 | See the frozen brief; no frame design is chosen here |
| Q-3 | Which common inputs and product revision govern the two arms? | Actual launch record archived | 2026-11-11 | Exact prompts and hash manifest; code pin 8d78523; two fresh sessions launched by the coordinator |

## Links

- [Proposed requirements and acceptance criteria](requirements.md)
- [Frozen frame benchmark and repository record layout](../../../evals/frame-shadowbox-24x36/README.md)
- [Completed template lab](../003-template-lab/plan.md)
- [Historical reuse spine](../../../plan.md)
