---
artifact: decisions
updated: 2026-11-10
decisions: [D-01, D-02]
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
