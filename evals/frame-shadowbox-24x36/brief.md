# Frozen common design brief: 24x36 shadow-box frame

Freeze ID: `frame-shadowbox-24x36-v1`.
This brief distinguishes the user's requirements from the agreed comparison scope
and retains the original user quotes. The verbatim blocks in
[`actual-prompts.md`](actual-prompts.md) are authoritative for what both candidates
actually received. This repository archive was completed after their launch;
it must not be represented as a pre-launch Git commit.

## Original user requirements

Original user request:

> For comparison. I would like to build a 24x36 frame with atleast 1 inch depth. It should be easily hangable in wall. Get inspiration of different designs available from web, and give me few options in terms of design aesthetic. Also need to find a way to insert glass (or any other transparent material) in the front. So that it looks like store bought frame. Think of how to achieve it and provide instructions on how I can build it

User addition:

> remember p2s will not be able to build it one piece. So we need to figure out modularity and how to seamlessy join them

## Confirmed clarifications

- **24x36 INCHES is the artwork/display size**, not the outside dimensions.
- **At least one inch is usable interior space behind the transparent front**,
  not overall frame thickness.
- Construction choice: **"Either—let both agents choose and justify the best
  approach"** between printed frame sections with hidden wood/aluminum
  reinforcement and a primarily printed structure with ordinary metal
  fasteners/hanging hardware.
- Contents: **"geometric art (using different paper colors and 3d shapes max
  0.75 inch protruding out) in a matte board"**.
- Printer: Bambu Lab P2S. It has not arrived, so no physical tests are possible.

## Agreed dimensional contract

Preserve an unobscured intended display rectangle of **609.6 x 914.4 mm** and
explicitly dimension the actual artwork/mat seat, any overlap margins, outer
dimensions, glazing and backing cut sizes. Do not silently reinterpret 24x36
as external dimensions.

Usable distance from the art/mat mounting surface to the inner glazing face must
be **at least 25.4 mm**. Artwork projection is **at most 19.05 mm**, leaving
**at least 6.35 mm nominal clearance before accounting for tolerances or panel
bow**. Account for the stack-up rather than using a 25.4-mm outer frame.

Portrait is a working assumption; explicitly state rotation/mounting
implications. Indoor residential display is an assumption. Wall construction
and actual completed mass are unknown and must be measured/confirmed before hanging.

## Printer and output contract

Use the P2S volume **256 x 256 x 256 mm** and a **0.4-mm nozzle** as the initial
design assumption. Every exported **printable** part must fit in its specified
print orientation, including joints/tabs. Allow practical brim/margin rather
than simply using the theoretical bed boundary.

Assembly files may exceed the printer but must be labeled **non-printable**.
Do not replace assembly output with a giant unprintable STL.

State PLA/PETG choice and rationale, suggested process/orientation/support, and
print-only residuals. Use purchased glazing/hardware/backing/reinforcement
where justified.

## Required design work

Research real web references and cite actual product/docs URLs. Present at least
three aesthetic options, including:

- Matte-black gallery.
- Warm wood-look.
- Stepped white.

Additional options are allowed, but do not spend effort making all of them fully
engineered. Fully model and document **one recommended solution**. Clearly label
alternative concept sketches versus generated CAD.

Explain segmented straight rails/corners, alignment, joinery, concealed
mechanical retention, assembly order, seam placement, accumulated tolerance/racking,
and the surface finishing necessary for store-bought appearance. Do not promise
invisible as-printed seams. Show and dimension the joint detail. Include a small
mating/joint test coupon where relevant.

## Glazing

Choose acrylic/glass/another suitable transparent material and justify weight,
breakage risk, clarity/scratch tradeoffs. Prefer a practical serviceable
rear-loading arrangement or otherwise fully explain the insertion/removal path.

Specify cut sizes, nominal thickness with sourcing rationale, retaining
lip/rabbet, tolerances/expansion clearance, spacer/backing/retainer stack and panel
support. Do not permanently trap the art unintentionally. Never imply that being
watertight/manifold proves safe glass retention or load strength.

## Hanging and bounded safety

Make the load path explicit from glazing/frame to structural reinforcement or
joints to rated purchased hardware to the wall. Consider ordinary metal
cleat/D-ring hardware as appropriate.

Do not hang a large heavy assembly from untested printed tabs, adhesive alone,
paper mat or thin nonstructural dust backing. Separate measured/estimated total
mass from manufacturer hardware ratings. Wall anchors depend on wall/studs and
cannot be universally specified.

Include dry assembly, floor-level coupon/joint/retention checks and conservative
pre-hanging checks. No invented load proof or actual print claims. If a credible
design cannot be completed, state blockers instead of certifying it.

## Required deliverables for both arms

- Editable CAD/source and reproducible export instructions.
- One STL per unique print part, with quantities and print orientation.
- Assembly and section/joint views derived from actual geometry.
- One complete recommended design, plus three aesthetic concepts and cited inspiration.
- Bill of materials with cut lists, purchased fasteners/glazing/backing/hardware,
  quantities and estimates clearly labeled.
- Sequential fabrication, finishing, glazing, assembly and hanging instructions.
- Objective geometry/dimension/fit checks and candid residuals.
- Source/output hashes and dependency versions where possible.

STEP exports are desirable if the backend supports them. Do not penalize an
appropriate editable OpenSCAD source simply for having no STEP.

No printer connection, auto-print, purchases, paid generation API or external
service upload. Do not copy copyrighted model assets or source beyond permitted
licenses.

## Shared primary references

These are already-fetched starting points, **not proof of our design**. Both arms
may research the same public sources and standard CAD documentation.

- https://frameusa.com/pages/24x36-shadow-box — shows Elite black/cherry/honey
  and Showcase black/honey/white profiles.
- https://www.custompictureframes.com/shadow-box-frames/sizes/24x36 — documents
  hardwood shadowbox, acrylic, backing and D-ring/French-cleat options.
- https://bambulab.com/en/p2s/specs — official P2S specifications.
- https://www.acrylite.co/products/brands/acrylite-gallery/framing-grade —
  acrylic manufacturer reference; verify before numeric reliance.
- https://www.acrylite.co/applications/framing-and-picture-glazing —
  acrylic manufacturer reference; verify before numeric reliance.

Search summaries previously returned unsupported universal thickness/clearance
statements. Those are **not accepted evidence**.
