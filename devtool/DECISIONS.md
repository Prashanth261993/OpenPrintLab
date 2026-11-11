---
artifact: decisions
updated: 2026-11-11
decisions: [D-01, D-02, D-03, D-04, D-05]
---

# Decisions

## D-01 - Execute the bounded CadQuery experiment, not a migration

- **When:** 2026-11-10.
- **Phase:** T-05 build, before experimental code.
- **Decided by:** human-confirmed.
- **Options:** keep the existing baseline only; run the isolated CadQuery trial;
  enable broader/provider integrations.
- **Chosen:** User selected "Start the isolated CadQuery experiment (Recommended)"
  after a description of isolated installation, editable rounded tray, STEP/STL,
  Windows/Linux geometry verification and no paid APIs.
- **Rejected because:** broad migration and paid providers were not approved.
- **Reversible:** yes; remove/ignore the isolated experiment without altering the
  core catalog, dependencies, original artifacts or local preview.

## D-02 - Implement bounded optional CAD/template lab

- **When:** 2026-11-10, before milestone 003 implementation.
- **Phase:** 003 planning/build.
- **Decided by:** human-confirmed.
- **Options:** retain the plan-only hold; implement a bounded optional backend and
  generators; migrate the core or add external/paid generation.
- **Chosen:** "integrate CadQuery as an optional backend, add a few useful
  generator. I want to be able to give my own instructions and see the output".
  Own tool-capable assistant interprets instructions; local tools create the
  non-destructive variant and real preview.
- **Rejected because:** migration, external-file import, hosted chatbot and paid
  providers were not requested or authorized.
- **Reversible:** yes; original no-CAD path and artifacts remain intact.

## D-03 - Track reusable roadmap in the repository (scope clarified by D-04)

- **When:** 2026-11-11.
- **Phase:** 004 administrative tracking, not feature implementation.
- **Decided by:** human-confirmed.
- **Options:** leave product ideas in chat; maintain a repository-owned backlog;
  immediately implement roadmap items.
- **Chosen:** "everything should be in repo and not within session". Record the
  requested next capabilities and useful upstream ideas with requirements,
  priorities, sources and evidence gates in
  [004 Roadmap](features/004-reuse-roadmap/plan.md).
- **Rejected because:** tracking approval is not implementation authorization.
  The original storage interpretation also included one-off test records; that
  scope is narrowed by D-04 rather than treated as the default product policy.
- **Reversible:** roadmap tracking can be amended with Git history retained.

## D-04 - Retain product plans, remove one-off test records from the current tree

- **When:** 2026-11-11.
- **Phase:** focused documentation cleanup.
- **Decided by:** human-confirmed.
- **Options:** retain all test records in the product repo; remove only one-off
  artifacts while retaining reusable plans; rewrite public history.
- **Chosen:** "ok clean them up please. Only relevant ones. Unless you see value
  for them to be in repo". Keep product roadmap/reuse research and generic
  evaluation capability tracking; remove one-off test records and their links
  from the current product tree. Do not retain case-specific prompts, identifiers,
  hashes or run bookkeeping in product docs.
- **Rejected because:** a product-planning preference is not blanket permission
  to publish one-off test data. History rewriting and changes to independent
  design workspaces are outside the authorized cleanup.
- **Reversible:** a normal deletion commit preserves Git history. Private archival
  copies may support the ongoing local comparison without re-adding them to the repo.

## D-05 - Allow bounded structural-prototype guidance

- **When:** 2026-11-11.
- **Phase:** 005 guidance revision, not a structural generator or individual design.
- **Decided by:** human-confirmed.
- **Options:** blanket rejection of loads; unrestricted structural authoring;
  bounded decorative prototype exploration with evidence and escalation.
- **Chosen:** "we need to consider how to solve structural gudiance within
  OpenPrintLab's guidance and then test this out". Implement the bounded guidance
  described in [005 requirements](features/005-structural-guidance/requirements.md)
  and [the canonical policy](../docs/structural-design.md). Distinguish hazard,
  uncertainty, prototype eligibility and verified suitability. Preserve hard
  exclusions, actual tool limits and physical/competent-review gates.
- **Rejected because:** lack of physical evidence alone does not establish
  impossibility, but useful prototype geometry does not establish safe use.
  Neither unrestricted load claims nor extending templates to hide unsupported
  operations is justified.
- **Reversible:** revise guidance with review; no catalog geometry, supported-use
  allowlist, solver, dependency or automatic safety status is changed.
