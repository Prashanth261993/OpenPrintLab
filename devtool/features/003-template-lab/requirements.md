---
artifact: requirements
feature: 003-template-lab
status: approved
updated: 2026-11-10
requirements: [R-01, R-02, R-03, R-04, R-05, R-06]
---

# Editable template lab

## Problem and approval

The user prioritized "Our editable template sources: richer customization before
importing external models", then explicitly requested:
"integrate CadQuery as an optional backend, add a few useful generator. I want
to be able to give my own instructions and see the output".

The assistant interprets natural language; deterministic local tools generate
geometry. A model or generic chat website without tool/CLI/MCP execution is not
sufficient. No OpenPrintLab hosted model, mandatory API key or paid provider.

## Goals and non-goals

Deliver a complete journey: browse templates, give one's own compatible assistant
dimensions/style/use, clarify missing constraints, derive a new variant, inspect
an actual geometry preview, download exports, get grounded guidance, and manually
review the slice. No arbitrary STL/STEP/3MF import, browser CAD editor, web chatbot,
automatic printer control, arbitrary sculpting or physical-print claim.

### R-01 - Optional backend and bounded generators

**Priority:** must. **Status:** active.

- **AC-01.1:** When CadQuery is absent, existing models, CLI and catalog shall
  still work; a CAD-template request shall fail with actionable isolated setup
  instructions, never silently change engines.
- **AC-01.2:** When selecting a supported generator, numeric dimensions, counts
  and relationships shall be validated before CAD operations.
- **AC-01.3:** The first set shall contain a rounded compartment organizer,
  rounded multi-pen rest and lightweight paper-card slot stand. Reuse T-05
  geometry operations and existing low-risk concepts, not a new geometry kernel.

### R-02 - Non-destructive modification

**Priority:** must. **Status:** active.

- **AC-02.1:** When customizing an original, tools shall create a named variant
  without modifying original sources, examples or previous outputs; collisions
  shall fail rather than overwrite.
- **AC-02.2:** Each result shall retain effective parameters, original template
  version/source hashes, backend versions/settings, exact STL/STEP hashes,
  design license and a content-bound variant identity.
- **AC-02.3:** Each export shall run fresh checks and leave slicer/physical
  evidence not performed. Different geometry never inherits prior evidence.

### R-03 - See and download the result

**Priority:** must. **Status:** active.

- **AC-03.1:** The local lab shall show useful seeded templates and a real custom
  sample, with previews derived from the exact exported STL, never illustrative AI art.
- **AC-03.2:** Each preview page shall expose dimensions, parameters, backend,
  evidence limits, downloadable STL, STEP when supported, report and editable source.
- **AC-03.3:** One documented command shall serve the local lab on loopback.
  Customization is assistant/tool-driven; the browser is a viewer, not a live editor.

### R-04 - Bring-your-own assistant and shared tools

**Priority:** must. **Status:** active.

- **AC-04.1:** Existing skill/CLI/MCP shall expose template discovery, description,
  variant generation and guidance through shared implementations.
- **AC-04.2:** Instructions shall distinguish protocol/tool compatibility from
  clients actually tested and explicitly deny a built-in natural-language parser.
- **AC-04.3:** Sample prompts shall clarify missing dimensions, supported style
  operations and intended use before generation, and return actual preview/output links.

### R-05 - Grounded model-aware setup guidance

**Priority:** must. **Status:** active.

- **AC-05.1:** Guidance shall request actual printer, nozzle, plate, filament and
  intended use when absent, rather than invent a tested profile.
- **AC-05.2:** Only the bounded P2S/0.4 mm/PLA starting suggestions shall be offered
  as such, with official sources and model orientation/use limits. Other setups
  shall be explicitly unsupported, not silently mapped to P2S defaults.
- **AC-05.3:** Guidance shall never change evidence status or initiate a print.

### R-06 - Local proof and retained baseline

**Priority:** must. **Status:** active.

- **AC-06.1:** Windows local and Linux CI shall verify geometry, non-overwrite,
  optional-dependency failure, exports, passports, preview links and MCP calls.
- **AC-06.2:** All 16 original export files shall remain byte-identical.
- **AC-06.3:** A real custom organizer demo shall be visible through a verified
  local URL and downloadable without any provider key. Human offline slicing
  remains pending until actually performed; no physical evidence is required.

## Assumptions and deferred questions

- **A-1:** Defined aesthetic operations are corner rounding and repeated
  compartments/channels, not unconstrained mesh sculpting.
- **A-2:** Font-free templates are the first reliable set. A nameplate is deferred:
  CadQuery's text API and Noto Sans OFL declaration were inspected, but no pinned
  font binary, cross-platform text geometry or minimum glyph features were tested.
  Never depend on an arbitrary installed Arial font or silently substitute glyphs.
- **A-3:** Optional CadQuery retains its measured ~1.21 GB cost and native-license
  review caveats. Use a separate environment, no global installation.
- **Q-1:** External model import remains future work: source provenance, units,
  topology, editability and rights must be addressed before arbitrary file editing.
- **Q-2:** No real named-client certification or physical-print claim is implied
  by an SDK protocol test. Record exactly what was exercised.
