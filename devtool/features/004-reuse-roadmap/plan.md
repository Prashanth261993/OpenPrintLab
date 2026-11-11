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
roadmap does not implement features, launch comparisons or authorize publishing
one-off test data.

## Current state

The working product is [milestone 003](../003-template-lab/plan.md): original
dependency-free models, optional CadQuery templates, non-destructive variants,
real previews, CLI/MCP and honest evidence. The
[002 plan](../../../plan.md) and [T-05 experiment](../../../experiments/cadquery/report.md)
retain their history. Generic A/B evaluation remains an unimplemented product
backlog item, separate from individual experiments.

[Milestone 005](../005-structural-guidance/plan.md) separately implements bounded
structural-prototype guidance. It does not complete the controlled-new-design
automation, assembly diagnostics or evaluation-harness items below.

The user subsequently authorized selective implementation. [Milestone 006](../006-reuse-slices/plan.md)
implements curated patterns and bounded read-only diagnostics. Remaining items
are deferred by explicit integration/evidence gates, not silently marked shipped.

Tracking is approved by the user's 2026-11-11 request that plans and useful reuse
ideas live in the repo rather than only the session. The user clarified that
one-off tests should not be stored in the product tree by default. Keep reusable
plans/research here; separate approval is needed for implementation and for any
publication of case-specific test data.

## Phases

- [x] Record user priorities, source provenance and history.
- [x] Persist proposed requirements, backlog and reusable evaluation ideas.
- [ ] Approve a bounded implementation plan for any selected item.
- [ ] Implement and verify that approved item.
- [ ] Approve and implement generic evaluation support if selected.
- Red-team - not commissioned; future source-execution/install boundaries need review.

## Priorities, sources and dependencies

Priorities are recommended sequencing, not launch instructions. Dependencies
reflect actual prerequisites, not the order of this table.

| Item | Priority | Scope / source | Prerequisite and release gate | Status |
|---|---|---|---|---|
| T-02: controlled new design | 1 - suggested next | Beyond fixed templates, editable source, explicit unsupported cases; user direction, U-01 | Existing 003 pipeline; R-02 brief/source/permissions/geometry gates | deferred; 005 documents custom engineering, not automation |
| T-03: P2S project-3MF + slicing | 2 - suggested next | Actual printer/process/filament preset project, not just mesh-in-ZIP; user direction, U-02 | Can start with an existing variant, not dependent on T-02; R-03 actual Studio review | deferred; profile/round-trip/slice gates pending |
| T-04: cross-assistant packages | 3 | Generated adapters and plugin/skill ZIPs from one source; user direction, U-06/U-07 | Existing CLI/MCP contract; R-04 clean-install/permission/client evidence | deferred; packaging/client gates pending |
| T-05: reusable design patterns | 3 | Mechanical fasteners, supports, material/tolerance patterns with failed/unprinted evidence; user direction, U-01/U-04 | Existing passport schema; R-05 scoped claims and evidence. No universal upstream load ratings | partial: curated source-scoped records in 006; promotion not implemented |
| T-06: OpenSCAD + assembly | later extension | Broader source authoring/editing, multi-part BOM/assembly flow; U-01 | T-02 control boundary and T-07 assembly checks; add T-03 if a Bambu project is claimed | deferred; authoring boundary pending |
| T-07: assembly/orientation checks | enabling research | Collisions, Z=0, overhangs, first-layer islands; U-03 | Existing geometry pipeline and synthetic fixtures; does not need T-06 implemented first | partial: 006 geometry screening; exact collisions/islands deferred |
| T-08: reusable A/B evaluation | later product capability | No-product baseline, objective checks, fixed-camera renders and available cost/time metrics; user-approved reuse idea, U-05 | Approved harness scope and data-storage boundary; does not depend on building T-02 through T-07 | deferred; no runner implemented |

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
| T-08 | Build reusable neutral evaluation support after approval | R-08 | T-01 | Proposed `tools/evaluation.py`, `tests/test_evaluation.py`, `tests/fixtures/evaluation/`, `docs/evaluation.md`; no one-off run records | - | blocked | Planned: `python -m unittest tests.test_evaluation -v`; synthetic pass/fail fixtures, equivalent measurement and rendering, missing-metric handling and explicit storage boundary |

No parallel execution is scheduled or authorized. Before scheduling, narrow
shared paths and prove disjoint ownership. T-01 is inherited evidence of the
already-working system, not a claim that new roadmap features were implemented
or re-tested during this documentation assignment.

T-08 describes a future reusable capability, not an active comparison. No
candidate-specific records or results are tracked by this product backlog.

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

## Evaluation and storage boundary

Retain the reusable methodology: a no-product baseline, objective geometry and
requirements checks, fixed-camera presentation, declared confounders and actual
available effort/cost measurements. Freeze each authorized comparison's inputs
before execution, and do not tune the product mid-run to favor an arm.

Implementation approval for that methodology does not authorize publishing test
data. Product code, reusable plans and approved synthetic fixtures belong in the
repo. One-off briefs, prompts, candidate identifiers, outputs and run bookkeeping
remain in designated session/test storage unless separately approved for
publication. Preserve provenance and honest missing-evidence labels there.

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
| Q-2 | What reusable evaluation scope and synthetic fixtures would justify a harness? | T-08 implementation | 2026-11-11 | Not yet commissioned |
| Q-3 | Where may a future comparison's case-specific data be stored or published? | That comparison only | 2026-11-11 | Require explicit approval; no default product-repo ingestion |

## Links

- [Proposed requirements and acceptance criteria](requirements.md)
- [Completed template lab](../003-template-lab/plan.md)
- [Historical reuse spine](../../../plan.md)
