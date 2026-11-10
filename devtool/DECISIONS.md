---
artifact: decisions
updated: 2026-11-10
decisions: [D-01]
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
