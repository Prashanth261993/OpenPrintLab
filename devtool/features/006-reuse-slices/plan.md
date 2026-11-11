---
artifact: plan
feature: 006-reuse-slices
status: verified
updated: 2026-11-11
tasks: [T-01, T-02, T-03]
---

# 006 - Verified reuse slices

User approval: "lets also add any good skills, features present in github repo
I shared earlier. Make sure those are called out inout readme, github page.
Ofc post verification". This implements selected portions of 004, not all of it.
Stack remains the active [constitution](../../constitution.md).

## Source review and selection

Upstream revision: `f5e18a16031f5a11b20f7753574ff48494891587` in
[wilsonwaters/3d-printing](https://github.com/wilsonwaters/3d-printing/tree/f5e18a16031f5a11b20f7753574ff48494891587).
The root MIT license is copyright 2026 Wilson Waters. Read the actual Python
implementations below, not only marketing descriptions; none were executed.

| Candidate | Decision and reason | Release gate / remaining risk |
|---|---|---|
| `pattern-fasteners.md`, `material-petg.md`, `design-review.md` | Adapt scoped reference patterns now; retain reported evidence but omit universal dimensions, strengths, heat settings and food-contact advice | Canonical structural policy takes precedence; no local physical evidence |
| `verify-model.py`, `verification.md` | Adapt component/placement and face-normal reasoning into binary-STL diagnostics using existing geometry helpers | Do not import source execution, name-based gate bypass, silent normalization, island heuristics or collision certification |
| `make-bambu-3mf.py` | Defer project writer: upstream binds named installed profiles with overrides, has built-in fallback identities and mesh parsing/degenerate-removal behaviors that do not meet our no-silent-fallback contract | Bambu Studio was found in the standard Windows installation (file version 02.09.01.70); not an unavailable-app claim. Need strict mesh/profile inheritance/identity handling and actual P2S project round-trip plus slicer review before shipping |
| `build-adapters.py`, `build-skill-zip.py` | Defer packaging: upstream first-level Markdown inlining and recursive ZIP inclusion do not preserve our nested canonical policy/licensing/tool availability contract without an explicit allowlist and installation design | Deterministic manifest, transitive references, clean install/uninstall and named-client evidence; do not install global instructions |
| Broader OpenSCAD authoring | Retain 005's explicit custom-engineering path, not import upstream agent instructions | Controlled source permissions, assembly/source identities and reproducible export first |
| `evals/README.md` | Retain neutral methodology; defer runner integration | Its paid/client-specific runner/judge is not authorized to execute; requires neutral synthetic calibration and storage/privacy contract, never resurrect one-off records |

The 3MF writer's opening profile/mesh-resolution implementation was reviewed;
the remaining writer is not claimed audited or tested. No source-specific rating
is transferred to P2S prints. Notices record exact adaptation scope.

## Tasks

| ID | Task | Req | Depends on | Files owned | Parallel group | State | Verification |
|----|------|-----|-----------|-------------|----------------|-------|--------------|
| T-01 | Deliver runnable curated review patterns with shared CLI/MCP | R-01, R-04 | - | `patterns/`, `tools/patterns.py`, CLI/MCP, pattern tests, notices | - | done | `python -m tools.cli pattern fastener-selection` returned scoped JSON; `python -m unittest tests.test_patterns -v`: 2 passed; actual MCP smoke in T-03 |
| T-02 | Add read-only mesh and variant diagnostics | R-02, R-03 | T-01 | `tools/diagnostics.py`, CLI/MCP, diagnostic tests | - | done | `python -m unittest tests.test_diagnostics tests.test_patterns -v`: 10 passed; analytic fixtures and non-destructive CLI cases |
| T-03 | Verify walkthrough/site integration and prepare publication | R-03, R-04 | T-01, T-02 | README, docs/skill, site generator/home, MCP smoke, roadmap/decisions | - | done | Full unittest; `python -m tests.mcp_smoke`; release check; site/browser checks; results below |

T-02 follows T-01 because CLI/MCP files overlap. Risk: diagnostic warnings may be
mistaken for exact collision, slicing or safety evidence; explicit scope and
conservative results are acceptance criteria, not footnotes. No new dependency.

## Evidence

Verified locally on 2026-11-11:

- Tests were written and failed before the new pattern/diagnostic modules existed.
- `python -m unittest discover -s tests -q`: 31 tests, 29 passed and the two
  optional-CAD geometry cases explicitly skipped in the no-CAD interpreter.
- `.\.venv-cadquery\Scripts\python.exe -m unittest tests.test_cadquery_templates tests.test_diagnostics tests.test_variants -v`:
  all 16 passed, including actual CAD exports and the sloped-face threshold case.
- `python -m tests.mcp_smoke` in both existing SDK environments passed actual
  stdio discovery, pattern lookup, known-variant inspection, hash identity,
  unsafe-name/invalid-argument rejection, generation and optional CAD inspection.
- `python -m tools.release --check`: 16 original artifacts unchanged.
- `.\.venv\Scripts\python.exe -m tests.browser_smoke`: new page and navigation,
  desktop/mobile, enlarged text, downloads and no-JavaScript fallback passed.
  An enlarged-text callout overflow was found and fixed using existing typography.
  Actual desktop/mobile guide screenshots were inspected.
- 82 internal Markdown links resolved. Catalog geometry, published model examples,
  historical experiment artifacts and dependency manifests are unchanged.

Publishing uses normal non-force main updates after ancestry checks. Verify
GitHub CI and live Pages before reporting release availability; GitHub's
commit/check/deployment history is the publication record. No physical tests,
printer operations, individual designs, comparison runs or new installations.
