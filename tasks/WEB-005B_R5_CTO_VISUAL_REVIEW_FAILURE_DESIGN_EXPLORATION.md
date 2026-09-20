# WEB-005B R5 — CTO Visual Review Failure / Design Exploration Authority

**State:** DESIGN_REVISION_REQUIRED / DESIGN_EXPLORATION_ACTIVE  
**Implementation reviewed:** `feat/web-005b-homepage-visual-fidelity@176e345166bcc084219aa5972c3209c872889626`  
**Parent:** MER-109 / WEB-005B  
**Accepted upstream hero:** WEB-005A `1135e7a7e0b0f6db6348dee139d505550d8ca8b9`

## 1. CTO visual disposition

The technical package remains accepted, but the CTO did **not** accept the post-hero homepage design.

The accepted hero remains approved and immutable.

The rejected design scope is the post-hero homepage presentation, especially Acts 02, 03 and 04:

- Act 02: current separated text-panel + image-panel composition is rejected.
- Act 03: current three-equal-gallery-card presentation is rejected.
- Act 04: current contained result-card/payoff composition is rejected.
- More generally, the current post-hero "gallery/report blocks" visual language is not launch quality and must not be treated as Product design authority.

The exact implementation head `176e3451...` remains useful as technical/reference baseline only.

## 2. Design-system interpretation rules

The generated OrbGSS design system may learn stable brand tokens from the repository, but it MUST NOT freeze rejected layout choices into brand rules.

Keep as brand/system authority:

- dark deep-navy surfaces;
- restrained cyan accent;
- premium editorial composition;
- generous negative space;
- Inter/light-weight primary typography;
- restrained technical monospace metadata;
- thin low-contrast dividers and framing;
- Earth-observation/geoscience imagery as primary visual material;
- subtle, functional motion;
- scientific/provenance guards and MER-108 governed analytical rendering.

Treat as provisional / not authoritative:

- current Acts 02–04 section layouts;
- "three equal evidence cards";
- "only hero may carry substantial overlay copy";
- "cards are essentially forbidden";
- any rule derived only from the rejected post-hero composition;
- the current repository logo/mark as final brand identity. The logo/mark is temporary and must not constrain future brand design.

The design system must explicitly allow new marketing-site components such as:
- image-led domain cards;
- compact differentiator/proof modules;
- overlay copy on non-scientific context imagery where readability is protected;
- a single-stage analytical comparison/reveal composition;
- a stronger result/payoff stage.

## 3. Exploration scope

Design exploration is homepage-only. Do not redesign other routes yet.

The design tool may explore multiple concepts before implementation.

Required story:
`approved hero → place/context → evidence → result → domains/proof → company/contact`

### Act 02 — Place
Prefer an immersive, image-led composition. Text may be integrated over the natural-colour EO image using safe contrast treatment. Avoid a detached text panel followed by a separate image panel.

### Act 03 — Evidence
Do not use three equal disconnected cards. Explore a single dominant analytical stage that communicates "the same ground through multiple evidence layers", e.g. tabs, progressive reveal, controlled layer switching, or another coherent comparison system.

### Act 04 — Result
Make the Priority result a clear payoff and dominant analytical moment. The result should feel valuable and legible, not like another report card.

### Later homepage modules
Exploration may include:
- domain cards: Geothermal active; Mining and Marine as coming soon / in development;
- differentiator/proof modules inspired structurally by strong geospatial/enterprise sites;
- subtle ambient motion/particle texture in trust/reference areas;
- scale/proof storytelling only when metrics are real and verifiable.

Final copy/content is owned by another domain. Do not invent unsupported claims, accuracy percentages, customers, revenue, deployment counts or scale metrics.

## 4. External inspiration boundary

External references are inspiration, not copy targets.

Useful patterns:
- UP42: image-led category/domain cards and clean geospatial enterprise grouping;
- Kayrros: compact differentiators and proof-oriented content structure;
- EarthDaily: optional spatial/orbital interaction inspiration, only if it materially improves the page without duplicating the hero;
- Seequent: subtle low-noise ambient motion;
- Planet: communicating scale/importance through strong proof blocks.

Do not imitate any brand literally.

## 5. Design-first workflow

Do not send this revision directly to implementation.

First:
1. refine the generated OrbGSS design system under the interpretation rules above;
2. create multiple homepage redesign directions in Claude Design;
3. inspect interactive prototypes/screens;
4. obtain CTO selection/visual acceptance of one direction;
5. only then publish the implementation contract and hand off to Cloud Code.

No merge, deploy, DNS, WEB-006, or other-route redesign is authorized.

**Current Product state:** `DESIGN_REVISION_REQUIRED / WAITING_DESIGN_DIRECTION`.
