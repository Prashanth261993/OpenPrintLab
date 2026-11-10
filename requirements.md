---
artifact: requirements
feature: 002-evidence-and-reuse
status: approved
updated: 2026-11-10
requirements: [R-01, R-02, R-03, R-04, R-05, R-06]
---

# Evidence-first foundation and technology reuse

## Problem

V1 is runnable and published, but a mesh hash alone does not explain the design
version, suggested printer recipe, or which real-world evidence applies to a
customized variant. We also need a deliberate way to reuse mature CAD and AI
tools without turning a no-key starter project into an uncontrolled integration.

## Goals

Preserve the working local skeleton, make print evidence attributable, collect
both successes and failures, and prepare a reviewable reuse plan.

## Non-goals

No paid provider calls, API-key collection, new provider installation, arbitrary
editor execution, broad CAD migration, printer control, automatic evidence
promotion, or claim that a model has been sliced or printed.

## Requirements

### R-01 - Local walking skeleton

**Priority:** must. **Status:** active.

- **AC-01.1:** When a user has Python 3.11+ and this checkout, the documented
  Windows commands shall build and serve the catalog without a key or dependency.
- **AC-01.2:** When the user follows the customization example, the CLI shall
  export a checked 120 x 80 x 18 mm tray and a report to the named local folder.
- **AC-01.3:** When local testing becomes possible, the user shall receive the
  working directory, responsive preview URL, commands and a human slicer checklist
  without waiting for any external integration.

### R-02 - Versioned model passport

**Priority:** must. **Status:** active.

- **AC-02.1:** When a model is exported, its report shall identify model ID,
  model version, effective dimensions/parameters, original editable source hashes,
  design license, suggested printer recipe and exact STL hash.
- **AC-02.2:** When geometry or parameters change, the export shall get a fresh
  variant identity and run geometry checks; slicer/physical evidence shall not
  be inherited from a different variant.
- **AC-02.3:** When no human slice or physical test exists, evidence shall state
  not performed with no invented actual settings or result. Future evidence must
  bind the exact version, variant, STL hash and actual setup.

### R-03 - First-successful-print path

**Priority:** must. **Status:** active.

- **AC-03.1:** When a beginner selects the Layer staircase, the guide shall cover
  single-color PLA, the actual P2S/nozzle/plate/material presets, base-down
  orientation, no-support starting intent, layer inspection and human-initiated print.
- **AC-03.2:** When starting settings are shown, they shall be labeled unverified
  suggestions rather than certified profiles; no AMS shall be assumed.

### R-04 - Print-result feedback

**Priority:** must. **Status:** active.

- **AC-04.1:** When a user reports a result, a GitHub issue form shall accept
  success, partial success, failure and stopped-before-print outcomes, and collect
  model ID/version/variant/hash, actual printer/material/settings and observations.
- **AC-04.2:** When submitting evidence, the form shall request relevant photos or
  slicer screenshots, permit an honest "not available", warn that submissions are
  public, and not automatically promote catalog verification status.

### R-05 - Distinct creation paths

**Priority:** must. **Status:** active.

- **AC-05.1:** When choosing a workflow, a creator shall see precise functional
  parametric CAD separated from decorative AI mesh generation. Only the limited
  orthogonal local CAD path shall be described as shipped in V1.
- **AC-05.2:** When a decorative provider is evaluated, dimensions, topology,
  thickness, rights, privacy and human slice checks shall remain explicit gates;
  "AI generated" or "repaired" shall never imply printable.

### R-06 - Reviewable reuse plan

**Priority:** must. **Status:** active for planning, not implementation approval.

- **AC-06.1:** When planning future work, `plan.md` shall map requirements to
  tasks, dependencies, owned files, uncertainty, commands and acceptance gates,
  starting with the existing V1 skeleton and its actual evidence.
- **AC-06.2:** Before any provider integration or CAD migration is implemented,
  the decomposition shall be presented for user review. The first proposed
  experiment shall be bounded and preserve the no-key baseline.
- **AC-06.3:** When assessing CadQuery, Meshy, FreeCAD MCP, Blender MCP, Zoo, Tripo,
  MakerWorld and Printables, the plan shall record source URLs, adopt/evaluate/defer
  rationale and explicit choose/decline criteria without copying third-party models.

## Assumptions

- **A-1:** The user approved small missing foundation pieces and reuse planning,
  not enabling all named technologies or spending provider credits.
- **A-2:** Public feedback may include voluntarily supplied photos; machine
  serials, network identifiers, credentials and private designs are not required.
- **A-3:** A model version describes its original design; effective parameter
  variants also need content-bound identities. Recipe changes require a version
  review even when the mesh happens to remain unchanged.

## Open questions

| ID | Question | Blocking? |
|---|---|---|
| Q-1 | Approve the isolated CadQuery tray experiment after reviewing `plan.md`? | Future T-05 only |
| Q-2 | If Meshy is later evaluated, which account, privacy terms and credit cap are approved? | Future T-06 only |
| Q-3 | Which actual P2S nozzle, plate and PLA will the human trial use? | Human slice/print only, not local preview |
