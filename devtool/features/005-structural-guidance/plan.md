---
artifact: plan
feature: 005-structural-guidance
status: verified
updated: 2026-11-11
tasks: [T-01, T-02, T-03]
---

# 005 - Structural-prototype guidance

## Scope and approval

The user authorized a careful reusable guidance revision. This permits bounded
decorative engineering exploration, not deployment assurance or implementation
of a structural template. No individual design or comparison is part of this work.
See [requirements](requirements.md) and [decision D-05](../../DECISIONS.md#d-05---allow-bounded-structural-prototype-guidance).

Keep the existing runnable CLI/template workflow and its evidence. Add a
canonical policy and concise entry-point links, not a second geometry pipeline.
Primary manufacturer references are recorded with their limits in the guide.

## Tasks

| ID | Task | Req | Depends on | Files owned | Parallel group | State | Verification |
|----|------|-----|-----------|-------------|----------------|-------|--------------|
| T-01 | Ground and write canonical prototype policy, screening and evidence gates | R-01, R-02, R-03, R-04 | - | `docs/structural-design.md`, this milestone, `devtool/DECISIONS.md` | - | done | Inspect primary sources; manually trace every requirement to the guide and verify allowed, uncertain and excluded case dispositions without designing them |
| T-02 | Align assistant and public entry points without expanding templates | R-04, R-05 | T-01 | `AGENTS.md`, `.github/skills/create-printable-model/SKILL.md`, `README.md`, `docs/template-lab.md`, `docs/create.html`, `docs/beginner.html`, `docs/decisions.md`, `tools/site.py`, `devtool/features/004-reuse-roadmap/plan.md` | - | done | Review current `guidance` contract and source utilities; scan current entry points for contradictory blanket exclusions |
| T-03 | Verify unchanged baseline, links and publication candidate | R-06 | T-01, T-02 | Verification/evidence section here; no new test infrastructure | - | done | `python -m unittest tests.test_site tests.test_models tests.test_variants -v`; `python -m tools.release --check`; internal Markdown links; exact diff/artifact review |

No parallel workers or new environments are needed. Uncertainty is in applying
general engineering principles to future designs, not in claiming a validated
structure here. Source retrieval/limits and the actual utility contracts must
be resolved before describing support.

## Evidence

Local verification on 2026-11-11:

- 14 existing site/model/variant tests passed, including generated-site links,
  source-archive rebuild, unchanged setup rejection and non-overwrite behavior.
- `python -m tools.release --check` verified all 16 original model artifacts.
- 71 internal Markdown links resolved, including new guide/decision anchors.
- The task table covers R-01 through R-06. Geometry sources, exported examples,
  historical experiment artifacts, CLI/MCP, setup allowlists and dependencies
  are unchanged. The only Python edit is user-facing site guidance text.
- Primary source sections were read; no upstream skill, solver or new package
  was installed. Source review is not physical validation.

Manual policy walkthroughs (not generated designs or physical tests):

| Situation | Required disposition checked against the guide |
|---|---|
| Decorative modular object, no printer evidence or known wall yet | Eligible bounded CAD/coupon handoff; unresolved installation inputs and unvalidated state, not blanket refusal |
| Heavy breakable glazing above occupied space | Escalate qualified review; no unsupported installation approval; only contained non-deployable exploration if hazards can be bounded |
| Human-support or other life-safety part | Exclude DIY functional design; a prototype label cannot bypass scope |
| Mesh passes and a coupon fits | Geometry/fit evidence only; no automatic hanging or long-term suitability |
| Purchased hardware has a rating | Verify its exact conditions; printed attachments and the whole load path require independent evidence |
| New design/material is rejected by setup guidance | Preserve rejection/no invented profile; distinguish API limits from custom-modeling eligibility |
| User has only basic hand tools | Check sourcing and service path; do not assume unavailable fabrication equipment |

Publication uses a normal fast-forward update after remote-ancestry review.
Remote content and live Pages pointers must be verified before reporting them
published; GitHub commit/check/deployment history is the publication record.
No design comparison or physical validation is launched by this milestone.
