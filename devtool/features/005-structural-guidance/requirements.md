---
artifact: requirements
feature: 005-structural-guidance
status: approved
updated: 2026-11-11
requirements: [R-01, R-02, R-03, R-04, R-05, R-06]
---

# Bounded structural-prototype guidance

The user authorized reusable structural guidance, not a particular design,
structural generator, solver, safety certification or comparison run.

| Requirement | Acceptance gate |
|---|---|
| R-01: Distinguish hazard, uncertainty, prototype eligibility and suitability | One canonical guide permits contained exploration of non-safety-critical decorative objects, retains hard exclusions, and leaves unknown installation conditions unresolved without declaring all modeling impossible. No evidence-free safe-to-hang claim. |
| R-02: Require engineering reasoning and honest sources | Cover complete load paths, component dimensions/masses and sourced densities, joints/racking/tolerances, fastener bearing/pull-through, distributed attachment, orientation/anisotropy, creep/environment, glazing and service access. Calculations show units/assumptions/sensitivity; no universal strength or proof-load recipe. |
| R-03: Define a deliverable and physical-evidence gate | Require a risk register, identities, load-path diagram, actual checks, printable fit/joint coupons, unresolved modes and a staged floor-level inspection/test plan. Keep short tests separate from long-term evidence and competent review. |
| R-04: State the real product boundary | Custom source is assistant-authored engineering, not a named template or arbitrary-code MCP feature. Reuse geometry utilities only within their documented mesh/envelope limits; preserve originals, licenses and fresh evidence. |
| R-05: Align discovery and user-facing instructions | AGENTS, skill, README and directly related guides point to the canonical policy. Starter catalog uses and setup API allowlists do not expand. No new dependency, solver, provider, printer control or comparison artifact. |
| R-06: Verify and publish the bounded revision | Existing relevant site/model/guidance checks and internal links pass; original exports remain unchanged. Normal non-force publication, verified remote revision and live guide pointers. |

No print, slicer, mechanical or installation suitability evidence is produced by
this documentation milestone. Generic new-design automation remains separately
tracked in [004](../004-reuse-roadmap/plan.md). User-specific prompts, designs and
comparison records remain outside the product tree by default.
