# V1 scope and acceptance criteria

## Confirmed product decisions

- Public project: OpenPrintLab, owned by Prashanth261993.
- Beginner path: download a model from a static website, then slice and print.
- Creator path: use an AI coding assistant with repository instructions and skills.
- Initial printer: **Bambu Lab P2S**, not P1S. No AMS required or assumed.
- MIT tooling; CC BY 4.0 original models, editable design source, and guides.
- No hosted AI backend, printer automation, or pre-generated machine G-code.

## Engineering decisions

Python 3.11+ standard-library tooling builds a deliberately small family of
orthogonal, parametric solids. A union of axis-aligned boxes is meshed on a shared
coordinate grid, exposing only exterior faces. This keeps installation simple,
outputs deterministic, and the original source understandable to coding assistants.
It is **not** a substitute for a general CAD kernel: no curves, fillets, organic
models, arbitrary mesh repair, or general CSG subtraction are promised.
OpenSCAD snapshots are exported for visual inspection; Python recipes and catalog
parameters remain the editable source of truth. No OpenSCAD installation is
needed for the build.

The static site uses generated HTML, CSS, and a small progressive-enhancement
search script. Downloads and guidance still work without JavaScript. Isometric
SVG previews come directly from exported STL triangles and are labeled as
generated geometry, never photographs. No external fonts, trackers or runtime
CDNs are needed. The design uses warm neutral surfaces, dark green actions,
large system typography, roomy cards and visible keyboard focus rather than
expensive interactive 3D rendering.

The optional stdio MCP adapter uses the official Python SDK and shares the CLI
catalog/build functions. It can describe, check and export known recipes locally;
it cannot execute arbitrary code, accept arbitrary output paths, or control a printer.
Use an editable installation from a trusted checkout.

## Release acceptance

- Four original low-risk PLA designs in four categories have editable dimensions,
  actual STL downloads, source ZIPs, OpenSCAD snapshots, previews and instructions.
- All dimensions are mm; limits and geometric relationships reject invalid inputs.
- Exported STL bytes are checked for finite coordinates, nondegenerate faces,
  duplicate faces, closed consistently wound edges, connectedness, positive
  volume, Z=0 placement and the P2S 256 mm build envelope.
- Every report differentiates generated, software-checked, slicer-checked and
  physically print-tested. The last two remain false in V1.
- Automated tests check analytical volumes, rejection cases, rebuild consistency,
  links, search, responsive layout and an actual MCP stdio exchange.
- Beginner guidance covers download, correct presets, orientation, slicing,
  layer preview, human-initiated printing, troubleshooting and safety.
- GitHub Actions checks every PR; only verified main builds deploy Pages.
- Public repository contents and live site downloads are verified after publishing.

## Explicit limitations and next evidence

There are no physical test prints or slicer-reviewed profiles in this release.
No actual time, filament usage, fit or strength results are claimed.
Suggested process settings are starting points, not certified presets.
Future work: document real P2S test prints and slicer reviews with exact file
hashes, settings and observations; add rounded CAD designs using a mature kernel;
expand accessible previews and community submissions. Those are roadmap items,
not shipped capabilities. A test of one parameter set does not validate its variants.
