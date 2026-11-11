---
artifact: requirements
feature: 006-reuse-slices
status: approved
updated: 2026-11-11
requirements: [R-01, R-02, R-03, R-04]
---

# Selective reuse, first release slices

The user authorized useful upstream integrations with verification before claims.
This first bounded release selects two independent-of-CAD capabilities, not the
entire backlog. No individual design/comparison or global installation is involved.

| Requirement | Acceptance |
|---|---|
| R-01: Curated review patterns | Runnable CLI/MCP access to fastener, material/service and design-review guidance with pinned upstream provenance. Preserve source-reported failures/proven/unprinted distinctions without importing ratings or promoting local evidence. Unknown IDs fail explicitly. |
| R-02: Read-only geometry diagnostics | Inspect binary STL and existing variants without changing bytes. Report edge-connected components, per-component placement/contact, oriented downward-face areas and conservative pair bounding-box separation. Explicit part/plate/assembly modes; never infer collision-free interiors from overlapping bounds. Reject malformed/nonfinite input. No silent transforms or repair. |
| R-03: Meaningful verification | Synthetic positive/negative fixtures with analytical sizes/areas/separation; floating component, reversed/open mesh, margin and overhang cases; CLI exit behavior and actual MCP parity/rejection. Preserve original artifacts and optional CAD workflow. |
| R-04: Honest distribution and claims | README and live Pages show runnable examples, provenance/license and limits only after verification. Retain upstream MIT notice and distinguish adapted content from original CC BY designs/guides. Record adopt/adapt/defer decisions for every reviewed candidate. |

No automatic strength, fit, first-layer-island, exact collision or minimum
surface-clearance claim. No new arbitrary-code MCP endpoint, solver, preset,
printer control or physical evidence. Project-3MF, client packaging and wider
authoring/evaluation remain separate slices with explicit gates in the plan.
