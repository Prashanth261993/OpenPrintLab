# Decorative structural prototypes: guidance and evidence boundary

This is OpenPrintLab's **canonical structural-design guidance** for assistants
and contributors. It permits useful engineering exploration; it is not a
structural design standard, load rating or installation approval. Starter models
remain restricted to their catalog uses. A new decorative design with joints or
loads is not automatically prohibited, and is not automatically safe.

## Classify before designing

Record four separate judgments; do not collapse them into one "printable" flag.

| Judgment | Required distinction |
|---|---|
| Hazard | Intended use, foreseeable misuse, who/what could be struck, cut, trapped or otherwise harmed if any component fails; installation height and surroundings matter. "Decorative" is not a safety classification. |
| Uncertainty | Unknown material/process properties, mass, geometry, environment, connections and support conditions. Missing evidence is uncertainty, not proof of impossibility or safety. |
| Prototype eligibility | Can the proposed modeling and contained floor-level investigation avoid exposing people/property to the failure hazard? State the bounded scope and any prerequisite risk reduction. |
| Suitability | Evidence and competent review for the exact assembled configuration, environment, duty and installation. Never inferred from eligibility, a render, a mesh report or a single successful print. |

**Permitted:** task-specific editable CAD, transparent plausibility screening,
printable fit/joint coupons and a validation plan for non-safety-critical
decorative objects, including modular displays or frames. Delivery may stop at a
useful unvalidated prototype. Unknown wall construction or final mass prevents
installation approval, not all modeling: record conditional interfaces and
unresolved inputs rather than guessing anchors or refusing all geometry.

**Escalate:** heavy or brittle glazing, overhead mounting, locations above people,
beds/seating or routes of travel, public/child-accessible installations, unknown
support integrity, and other credible serious-injury consequences. Do not supply
an unsupported hang/install go-ahead. Obtain an appropriately qualified engineer,
glazing specialist or installer for the relevant hazard; reduce scope to
contained, non-deployable concepts/coupons if that can be done without exposure.
Competence must cover the failure mechanism: anchor installation advice alone
does not validate a printed joint, and an assistant's self-review is not
independent mechanical evidence.
If consequences cannot be bounded, stop the hazardous part of the task and
explain the missing review or safer alternative. There is no universal safe
mass/height threshold.

**Hard exclusions:** DIY safety-critical parts or instructions whose failure
could compromise human support, lifting/fall protection, vehicle or building
structure, pressure containment, medical function, electrical/fire/heat
protection, or other life-safety systems. Weapons, food-contact designs,
energized electrical enclosures and high-temperature functional applications
also remain outside this project's supported design scope. A "prototype" label
must not be used to bypass these exclusions. Offer nonfunctional visualization
or qualified professional/commercial alternatives instead.

## Capture the design basis

Before detail design, record intended use, units, dimensional meaning, permitted
materials/purchased components, actual tools and assembly skills, intended life,
temperature/humidity/sunlight exposure and service/handling loads. Identify
constraints that must be clarified versus provisional assumptions that allow
modeling. Do not assume machining, glass cutting, drilling, heat-set insertion,
adhesives or tools the user does not have. Vendor-sized parts and reversible
hand-tool assembly may be more appropriate; respect the user's construction
allowance instead of silently substituting a stronger hybrid structure.

Maintain a risk register with: failure mode and consequence, affected interface,
assumption/evidence, mitigation, remaining uncertainty, required observation/test,
stop criterion and responsible reviewer. Address loss of a retainer or fastener,
accidental bump/handling, incorrect assembly and service disassembly as well as
steady self-weight. Do not treat unknown risk as a low score.

### Mass and transparent screening

List dimensions, quantity and estimated/measured mass of **every** component:
glazing, art/mat, printed members, spacers, backing, fasteners and hanging hardware.
Include adhesives/finish where relevant. Identify the center of mass and offsets
from supports; distinguish estimated mass, measured finished mass and force.

- Use `m = rho * V` with consistent units and a source for the **specific material
  and grade**. For a solid rectangular panel, `V = width * height * thickness`;
  use the actual cut size, not the visible opening. Record source/version,
  nominal thickness and tolerance, density conditions and uncertainty.
- For example, the ACRYLITE sheet/rod/tube SDS [S-4] reports approximately
  `1.20 g/cm^3` at `20 C` (`1200 kg/m^3`). This is an indicative bulk acrylic
  value, not a filament density, strength allowable or universal glazing spec.
  Confirm the actual supplier/grade and replace estimates with measured mass.
- Printed solid CAD volume times bulk polymer density is not actual print mass.
  Label a solid-material estimate separately; walls, infill, process and material
  affect mass. Do not multiply total CAD volume by infill percentage: shells
  remain. Use an actual slice estimate when available (identify the file/profile),
  then weigh the finished assembly. Unsliced usage remains unknown.
- Convert mass to force explicitly (`W = m * g`, approximately `g = 9.81 m/s^2`).
  Free-body reasoning may estimate reactions and eccentric moments (`M = W * e`).
  Check equilibrium and show the assumed contact/support model. Never assume
  equal sharing just because two hangers or several fasteners are present.
- Report a range/sensitivity to panel thickness, dimensions, density, load offset
  and unequal support sharing. If screening stress/deflection, name the equation,
  section/contact model and its limitations. Isotropic beam formulae or bulk
  tensile data do not establish capacity of a layered, jointed printed assembly.

Calculations screen plausibility and expose missing inputs; they do not prove
retention, fatigue, creep or safe installation. No universal PLA/PETG strength,
allowable load, fastener torque, safety-factor multiplier or DIY proof-load recipe
is supplied. Do not invent FEA or a solver result. A future analysis would need
actual inputs, boundary conditions, material/process evidence and independent
review, not just a colored stress image.

## Trace the whole load path

Provide a labeled load-path diagram tied to actual part and interface IDs, not
only an attractive assembly view. For example, the *categories* might be:

```text
supported contents / glazing
  -> bearing seats and retainers
  -> printed members and modular joints
  -> attachment contact areas and fasteners
  -> purchased hanging hardware
  -> substrate-specific anchors or studs
  -> verified supporting structure
```

This is a checklist, not a prescribed design. Show separate paths for art/backing,
glazing, self-weight, out-of-plane restraint and handling. Any missing arrow is
an unresolved interface. Neither paper mat nor a thin dust cover is automatically
a structural diaphragm.

| Interface or effect | Required reasoning and evidence |
|---|---|
| Modular joints | Distinguish alignment from retention; dimension engagement, edge distances, bearing surfaces and assembly order. Show resistance to separation, twist and in-plane racking. Examine accumulated joint clearances, shrinkage, finish thickness, squareness/diagonal mismatch and tolerance stack-up, not only a nominal CAD fit. |
| Fasteners and attachments | Account for bearing/crushing, pull-through, thread/insert pull-out, edge breakout, net-section loss, layer separation and prying. Distribute contact and load where justified; washers or additional screws do not establish capacity by themselves. Check access, seating, engagement, loosening and clamping relaxation. Do not assume friction-only or adhesive-only retention of suspended contents. |
| Printed material | Map load direction to layer and extrusion direction, local shell continuity, seams, holes and notches. Explain print orientation/support tradeoffs rather than a blanket "strongest" orientation. Capture actual filament grade/condition, printer, temperatures, walls, infill and conditioning in physical evidence. Bulk or another printer's data is not a printed allowable [S-1, S-2]. |
| Time and environment | Address sustained-load deformation, clamp relaxation, repeated handling and temperature/humidity cycles. Sun-warmed surfaces and storage can differ from room temperature. Neither PETG selection, more infill nor a short room-temperature test eliminates creep [S-1, S-3]. |
| Glazing | Prefer lightweight shatter-resistant glazing where suitable, but assess bow, scratches, chemical compatibility, expansion, edge support and retention. Shatter-resistant is not unbreakable. Heavy/breakable glass changes consequences and needs specialist review, not a generic substitution. No universal panel thickness or clearance [S-4, S-5]. |
| Service access | Dimension the insertion/removal path, retaining overlap, stack-up and tolerances. Provide non-destructive access to art, glazing and hardware, with the assembly fully supported during service. Explain how retention is re-established and checked; do not unintentionally trap contents or require dangerous manipulation. |
| Wall/support connection | Cite the exact hardware product, rating type, load direction, substrate, installation requirements and applicable manufacturer document. Confirm substrate/condition, fastener compatibility, embedment, spacing/edge distances and installer capability as applicable. A hardware rating does not transfer to a printed mount or the assembled system [S-6]. |

SPIROL [S-3] illustrates plastic creep and local bearing/clamp-load problems in
engineered bolted joints. Its compression limiters, dimensions, torque tables
and molded-plastic assumptions are **not** automatically applicable to FDM.
Any proposed insert/limiter must fit the permitted bill of materials, be sourced
and evaluated in the actual printed joint; this guide prescribes none.

## Real tool boundary: custom engineering, not template support

Frames and general structural assemblies are **not named templates**. Start with
`python -m tools.cli templates` / `template ID` to identify what exists. Do not
call an unknown shape a supported generator, disguise it as a tray variant or
weaken template constraints/allowed uses to obtain a successful report.

For an eligible request, a tool-capable assistant may author reviewed,
task-specific editable CAD with a suitable standard library/tool in the user's
authorized workspace. CadQuery is opt-in; OpenSCAD or another tool requires its
own availability/setup check. This is **custom engineering by the assistant**,
not shipped general-design automation. Record where shared tooling ends and
custom modeling, assembly analysis or checking begins.

Keep each revision in a new user-approved directory such as
`build/custom/NAME-v1`, preserving source, parameters, export commands, library
versions, source licenses and output hashes. Never overwrite prior variants,
change catalog defaults or publish private designs automatically. Give actual
geometry-derived previews and file paths; include STEP only if actually exported.

Shared Python utilities have narrow contracts:

- `tools.geometry.decode_stl` reads **binary STL**, not every mesh format.
  `validate_mesh` checks finite/nondegenerate faces, duplicate faces, edge
  closure/winding, connectivity, positive volume and origin/envelope conditions.
  It expects **one connected printable mesh**, nonnegative coordinates, Z=0 and
  coordinates within the P2S 256 mm envelope. It is not a general solid,
  self-intersection, collision, overhang, island or strength verifier.
- Use those checks per compatible printable part, in its recorded print
  orientation. Keep assembly transforms separately. Include joints/tabs and
  practical brim/placement margins; the check's theoretical envelope does not
  reserve margins. An oversized/multipart assembly is a **non-printable assembly
  view**, not a failed part to shrink silently. Do not bypass a check or falsely
  report it passed; disclose incompatibility and use separately identified
  appropriate checks when necessary.
- `tools.mesh_preview.render_svg` renders supplied triangles; it does not
  validate them, compute clearances or prove assembleability. Custom section
  views, fit checks and assemblies need explicit task-specific work and actual
  geometry. A load-path diagram is separate from a geometry-derived render.
- CLI/MCP check/export/customize commands accept **known models/templates**, not
  arbitrary source or STL paths. The `guidance` / `variant_guidance` API gives
  model-specific setup suggestions only. `unsupported_setup` for a new use or
  material is not a general prohibition on custom modeling and must not be
  converted to a tested preset. There is no custom-source MCP execution endpoint,
  general assembly checker, FEA solver or automated structural-suitability API.

Never attach a known template's passport to different custom geometry. A custom
manifest/report must bind its own source, parameters, per-part STL/STEP identities,
versions and actual checks, and explicitly mark missing slicer/physical evidence.
Changing geometry, material, orientation, settings or installation requires
reassessment; evidence is not silently inherited.

## Required prototype handoff

Deliver the following, or identify each missing item and its consequence:

1. Intended-use/hazard classification, assumptions, risk register, unresolved
   user inputs and the explicit state **"Prototype - not validated for hanging/load use."**
2. Dimensioned editable source, reproducible export instructions, quantities and
   orientations per unique printable part; separately labeled non-printable
   assembly plus actual geometry-derived assembly/section/joint views.
3. Source/output hashes, dependency versions, licenses/provenance, mass budget
   and sensitivity calculations, and the complete part-ID load-path diagram.
4. BOM/cut sizes, compatible tools, sequential assembly and reversible service
   instructions; sources and conditions for any hardware rating.
5. Printable mating/fit and representative joint/retainer coupons with matching
   orientation/material/process and measured features to inspect. Small coupons
   do not represent full-span bending, racking or long-term assembly behavior.
6. Exact checks actually run with commands/results and failure details; separate
   generated, geometry-checked, slicer-reviewed and physical evidence. Include
   remaining failure modes, a staged physical plan and the required review.

These are documentation obligations, **not new automatic passport states**.
No existing tool can mark a design mechanically suitable.

### Physical gates, not a universal proof-load test

Define design-specific observations, equipment, acceptance/stop criteria,
duration/environment and competent reviewer **before** testing. Where those
cannot be justified, mark the plan incomplete and do not authorize load use.

| Stage | Required gate and limitation |
|---|---|
| Offline review | Inspect the actual slice and process selections for each part; check shells, holes, contacts, first layers and support removal. Software geometry success alone is insufficient. |
| Coupons and dry fit | With parts supported at floor level, inspect print defects, dimensions, fit, hardware seating, retainer engagement and disassembly. Start with a harmless surrogate panel if appropriate; do not force brittle glazing into a tight fit. Record photos, measurements and failures. |
| Contained assembly inspection/testing | Use a floor-level supported/contained setup that prevents falling, tipping and released pieces from reaching people, pets or valuables. A competent person must specify any representative loading/handling and fixture. Do not hang an unvalidated assembly to test it, stand under it, improvise overload weights or test to destruction using this guide. |
| Sustained-service evidence | Separately address time-dependent deformation/relaxation and relevant environmental cycling for the intended duty. Record baseline and repeated observations. A short hold, coupon pass or absence of visible cracks cannot establish a service life; no universal duration or acceleration factor is provided. |
| Installation review | Measure finished mass; resolve actual substrate, hardware and installation inputs. Obtain competent review appropriate to the hazard of the entire load path and physical evidence. Only that scoped decision can support installation instructions; it is not automatic certification by OpenPrintLab. |
| In-service care | Establish inspection/replacement criteria and safe removal/service procedures with the reviewer. Movement, cracking, whitening, looseness, panel migration or increasing deformation are reasons to stop use and have the supported assembly assessed, not merely tighten it and continue. |

Keep the unvalidated state until appropriate evidence **and** competent review
exist. A documented physical print or one short test does not alone satisfy that
gate. Record any later suitability conclusion with its reviewer, exact artifact,
scope, conditions and remaining limitations; never a blanket "safe" badge.

## Primary sources and limits

Reviewed 2026-11-11. These inform the reasoning above, not a load rating or
endorsement of any OpenPrintLab design. Do not reuse upstream assets or reproduce
manufacturer tables wholesale; follow licenses when incorporating source.

- **S-1:** Stratasys, [Design Considerations: FDM Additive Manufacturing Tooling](https://www.stratasys.com/contentassets/1a0cc7a8e7d14f29ac972189bfeade4c/dg_fdm_designconsiderationsfdmtooling_0718a.pdf),
  sections 2.2.1, 2.2.3 and 2.3.1 (PDF pages 6-7): service environment, creep and
  anisotropy. Industrial tooling/material examples are not P2S PLA/PETG allowables.
- **S-2:** Prusa, [Modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135),
  tolerance, iteration and orientation sections. Use the principles, not its
  printer-specific accuracy, overhang angles, clearance numbers or seam claims.
- **S-3:** SPIROL, [Compression Limiter Design Guide](https://www.spirol.com/assets/files/cmpl-compression-limiter-design-guide-us.pdf),
  introduction and plastic-host/bolted-joint guidance (PDF pages 2, 8-10):
  bearing and clamp retention/creep. Not a printed-joint rating or generic torque recipe.
- **S-4:** ACRYLITE, [Sheet/Rod/Tube SDS, version 3.0, 2025-10-20](https://www.acrylite.co/files/content/acrylite.co/documents/safety-data-sheet/ACRYLITE-Acrylic-Sheet-Rod-and-Tube-US-v3.0-20251020.pdf),
  section 9 (PDF page 5): approximate bulk density at stated temperature, not a
  structural allowable. Verify the selected grade and actual panel dimensions.
- **S-5:** ACRYLITE, [Gallery framing grade FF3](https://www.acrylite.co/products/brands/acrylite-gallery/framing-grade)
  and [acrylic/glass properties](https://www.acrylite.co/resources/knowledge-base/article/properties):
  shatter resistance, stiffness, expansion and surface-care tradeoffs. These do
  not establish universal glazing thickness, retention or safety for a complete assembly.
- **S-6:** Hilti, [Anchor Design Center](https://www.hilti.com/content/hilti/W1/US/en/business/business/engineering/anchors.html)
  and [Product Technical Guides](https://www.hilti.com/content/hilti/W1/US/en/business/business/engineering/product-technical-guides.html):
  substrate-specific product data, approvals and installation resources.
  No anchor or numerical rating is selected here; consult the exact product
  instructions for the confirmed support, not a marketing maximum.
