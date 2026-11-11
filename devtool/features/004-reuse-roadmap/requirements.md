---
artifact: requirements
feature: 004-reuse-roadmap
status: draft
updated: 2026-11-11
requirements: [R-01, R-02, R-03, R-04, R-05, R-06, R-07, R-08]
---

# Tracked next capabilities and evaluation

## Problem

Useful next capabilities and upstream reuse ideas must remain discoverable in
the repository, not depend on a chat session. The user approved **tracking**:
"everything should be in repo and not within session". The requirements below
are proposed feature/evidence contracts, not authorization to implement them.
Subsequent selective implementation is tracked in
[006](../006-reuse-slices/plan.md): curated pattern records and bounded geometry
screening are implemented subsets of R-05/R-07, not completion of these broader
contracts. The remaining feature contracts below are not shipped.
The [clarified storage scope](../../DECISIONS.md#d-04---retain-product-plans-remove-one-off-test-records-from-the-current-tree)
covers reusable product planning, not automatic publication of one-off test data.

## Goals

Preserve completed milestones; prioritize controlled new designs, P2S project
export/slicer evidence, and installable cross-assistant packages plus reusable
patterns. Track relevant upstream ideas with provenance and explicit evidence
gates. Keep reusable evaluation tooling distinct from one-off test data.

## Non-goals

This roadmap authorizes no generator, adapter, project writer, evaluation runner,
installation or test run. It copies no upstream implementation. Generic
evaluation support is a future capability, not consent to publish individual
test data or change product capability to favor a comparison.

## Requirements

### R-01 - Repository-owned history and current backlog

**Priority:** must. **Status:** active for tracking.

- **AC-01.1:** When the roadmap is updated, the README and existing plans shall
  link to one current backlog without rewriting completed milestone evidence.
- **AC-01.2:** When work is proposed, its requirement, scope, dependency,
  priority, source, status and acceptance gate shall be recorded in the repo.
- **AC-01.3:** Before implementation, a separate explicit authorization and
  bounded execution plan shall be recorded. Tracking approval alone is insufficient.

### R-02 - Controlled new designs beyond templates

**Priority:** must if commissioned. **Status:** proposed; implementation not approved.

- **AC-02.1:** When a request is outside an existing template, the workflow shall
  clarify units, dimensional meaning, intended use and constraints, then either
  author editable source in an approved isolated work surface or honestly decline
  unsupported geometry/use. It shall not pretend a template can express anything.
- **AC-02.2:** Before exporting, authored source changes and execution permissions
  shall be explicit; existing designs shall remain unchanged. Arbitrary submitted
  code execution is not implicitly authorized by this workflow.
- **AC-02.3:** Each accepted design shall retain the brief, editable source,
  dimensions/constraints, source/backend/output identities, actual preview,
  validation results and unsupported/unverified limits.

### R-03 - Bambu P2S project-3MF and real slicer evidence

**Priority:** must if commissioned. **Status:** proposed; implementation not approved.

- **AC-03.1:** When exporting a Bambu project, the result shall distinguish a
  geometry-only 3MF from a Bambu Studio project-3MF containing the actual selected
  P2S/nozzle/plate/filament/process settings, provenance and explicit overrides.
- **AC-03.2:** Before calling the project usable, archive/schema checks and an
  actual Bambu Studio open/round-trip/slice review shall confirm dimensions,
  placement, selected presets, layer continuity and warnings. A ZIP that opens
  in a generic 3MF library alone shall not satisfy this gate.
- **AC-03.3:** Slicer evidence shall identify Studio version, project/STL hashes,
  actual settings and screenshots/observations. Missing presets or unresolved
  warnings shall block promotion. No machine-ready G-code or printer control
  shall be added by this tracking approval.

### R-04 - Installable cross-assistant distribution

**Priority:** must if commissioned. **Status:** proposed; implementation not approved.

- **AC-04.1:** When packaging for multiple assistants, adapters and plugin/skill
  ZIPs shall be generated from shared instructions/contracts rather than forked
  geometry or validation logic.
- **AC-04.2:** Each release shall include versions, checksums, license notices,
  explicit permissions, isolated Windows setup and clean install/uninstall tests.
  CAD remains optional; no mandatory hosted AI or paid provider is introduced.
- **AC-04.3:** Compatibility claims shall distinguish protocol conformance from
  named clients and versions actually exercised. A generic model/chat page
  without local tools shall not be presented as a working integration.

### R-05 - Reusable, evidence-backed design patterns

**Priority:** must if commissioned. **Status:** partial in 006; curated source-scoped records, no local physical promotion.

- **AC-05.1:** When storing a fastener, support, material or tolerance pattern,
  record source/license, intended use, hardware/material/orientation, dimensions,
  applicable limits and exact supporting or contradicting artifacts.
- **AC-05.2:** Pattern records shall distinguish proven in a recorded configuration,
  failed and unprinted, while retaining separate geometry/slicer/physical evidence.
  Upstream load, material or clearance claims shall not become universal facts.
- **AC-05.3:** Promotion shall require evidence appropriate to the claim:
  physical fit/load/material claims need relevant physical evidence, not renders
  or a watertight mesh. Modified configurations shall not inherit proof.

### R-06 - Broader OpenSCAD authoring and multi-part assembly

**Priority:** should if commissioned. **Status:** proposed; implementation not approved.

- **AC-06.1:** When source-based OpenSCAD creation/editing is added, preserve
  editable parameters and original source, bound execution, expose unsupported
  operations and record actual export diagnostics.
- **AC-06.2:** Multi-part output shall include part IDs, transforms, assembly
  relationships, orientation, bill of materials, build instructions and per-part
  artifacts/passports. An assembly preview shall not imply assembleability.
- **AC-06.3:** Release of an assembly shall depend on the applicable checks in
  R-07 and, when project-3MF is claimed, R-03.

### R-07 - Assembly and print-orientation analysis

**Priority:** should if commissioned. **Status:** partial in 006; read-only screening, not exact collisions or first-layer analysis.

- **AC-07.1:** Checks shall cover part collisions/interferences, intended versus
  unintended contacts, Z=0/bed contact, overhangs and first-layer islands.
- **AC-07.2:** Known passing and deliberately failing fixtures shall prove the
  checks detect the targeted condition. The report shall state units,
  thresholds, assumptions, unsupported geometries and false-positive limits.
- **AC-07.3:** Geometric heuristics shall remain distinct from actual slicer
  support/layer evidence and physical assembly/strength evidence.

### R-08 - Reusable neutral A/B evaluation capability

**Priority:** should if commissioned. **Status:** proposed generic capability; not implemented.

- **AC-08.1:** Before either arm starts, freeze one common brief, rubric, tool
  allowlists, product/no-product conditions, versions, budgets and stopping rules
  in an explicitly approved storage location. Use fresh independent design
  contexts; a product-planning preference does not authorize publishing the data.
- **AC-08.2:** The no-product baseline shall not receive OpenPrintLab product
  instructions/artifacts indirectly. Shared ordinary tools, model/version and
  budgets should match where feasible; unavoidable differences are confounders.
- **AC-08.3:** Record objective requirements/geometry checks, identical fixed-camera
  render settings and a predeclared human aesthetic review. Preserve failures and
  retries. No product changes may be made mid-comparison to help one arm.
- **AC-08.4:** Reusable evaluation tooling and approved synthetic fixtures may
  live in the product repo. One-off briefs, prompts, candidate identifiers,
  outputs and run bookkeeping stay in their designated session/test storage
  unless the user separately approves publication. Cost, tokens and elapsed
  time shall be actual available measurements or explicitly unavailable; no
  invented estimates or physical-print claims.
- **AC-08.5:** When the user changes a shared requirement mid-run, append the
  amendment with provenance, reported equal delivery and the effective input
  version. Preserve original prompts/hashes, record receipt/redesign when
  collected, and do not silently change other scoring criteria.

The evaluation capability requires a separate implementation approval. These
criteria do not represent an active run or authorize result ingestion.

## Assumptions

- **A-1:** Sources U-01 through U-07 in the plan are reuse candidates, not an
  endorsement or proof of their claims on our hardware.
- **A-2:** Actual slicing can be evaluated offline. Physical verification remains
  unavailable until a real print/test is performed.
- **A-3:** No paid services, new runtime dependencies or client installations
  follow automatically from a backlog item.

## Open questions

Which reusable capability should be implemented next remains an explicit user
decision. Any future evaluation needs an approved protocol, storage boundary
and tested-client/tool matrix. This product roadmap contains no one-off design
brief, candidate identity, prompt archive or active-run bookkeeping.
