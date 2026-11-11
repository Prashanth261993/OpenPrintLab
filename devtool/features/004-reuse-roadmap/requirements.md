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

## Goals

Preserve completed milestones; prioritize controlled new designs, P2S project
export/slicer evidence, and installable cross-assistant packages plus reusable
patterns. Track relevant upstream ideas with provenance and explicit evidence
gates. Keep the two-arm frame benchmark separate from product development.

## Non-goals

This update implements no generators, adapters, project writer, evaluation
runner or frame design; installs nothing; launches no design agents; copies no
upstream implementation. No capability may be changed to favor the benchmark.

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

**Priority:** must if commissioned. **Status:** proposed; implementation not approved.

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

**Priority:** should if commissioned. **Status:** proposed; implementation not approved.

- **AC-07.1:** Checks shall cover part collisions/interferences, intended versus
  unintended contacts, Z=0/bed contact, overhangs and first-layer islands.
- **AC-07.2:** Known passing and deliberately failing fixtures shall prove the
  checks detect the targeted condition. The report shall state units,
  thresholds, assumptions, unsupported geometries and false-positive limits.
- **AC-07.3:** Geometric heuristics shall remain distinct from actual slicer
  support/layer evidence and physical assembly/strength evidence.

### R-08 - Fair, repository-owned A/B evaluation

**Priority:** must before an authorized comparison. **Status:** common launch text frozen; arms launched; repository archive follows launch.

- **AC-08.1:** Before either arm starts, freeze one common brief, rubric, tool
  allowlists, product/no-product conditions, versions, budgets and stopping rules
  in the repo. Use exactly two fresh design agents only after that gate.
- **AC-08.2:** The no-product baseline shall not receive OpenPrintLab product
  instructions/artifacts indirectly. Shared ordinary tools, model/version and
  budgets should match where feasible; unavoidable differences are confounders.
- **AC-08.3:** Record objective requirements/geometry checks, identical fixed-camera
  render settings and a predeclared human aesthetic review. Preserve failures and
  retries. No product changes may be made mid-comparison to help one arm.
- **AC-08.4:** Final brief, rubric, redacted run records, editable sources,
  outputs, renders, evidence and evaluation shall be repository-owned. Cost,
  tokens and elapsed time shall be actual available measurements, or explicitly
  unavailable; no invented estimates or physical-print claims.

## Assumptions

- **A-1:** Sources U-01 through U-07 in the plan are reuse candidates, not an
  endorsement or proof of their claims on our hardware.
- **A-2:** Actual slicing can be evaluated offline. Physical verification remains
  unavailable until a real print/test is performed.
- **A-3:** No paid services, new runtime dependencies or client installations
  follow automatically from a backlog item.

## Open questions

The coordinator supplied the frozen common inputs and then the exact actual
prompts/IDs for two launched sessions. They are persisted at
`evals/frame-shadowbox-24x36/`. Common text was frozen in launch messages, but the
repository archive followed launch; the repo-first portion of AC-08.1 is recorded
as unmet for this initial run, not retroactively claimed. No running candidate
outputs are inspected here. Product implementation authorization remains separate.
