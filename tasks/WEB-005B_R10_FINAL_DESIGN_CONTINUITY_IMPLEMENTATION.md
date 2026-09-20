# WEB-005B R10 — Final Design Acceptance & Continuity Implementation Contract

**Linear:** MER-109  
**State:** CTO_START_GRANTED / READY_FOR_E&D_DISPATCH  
**Design state:** ACCEPTED FOR IMPLEMENTATION  
**Scope:** homepage only  
**Architecture:** semantic HTML + CSS + progressive-enhancement vanilla JavaScript  
**Accepted hero:** WEB-005A @ `1135e7a7e0b0f6db6348dee139d505550d8ca8b9`  
**Technical/reference baseline:** `feat/web-005b-homepage-visual-fidelity@176e345166bcc084219aa5972c3209c872889626`

## 1. Decision

The final Claude Design homepage direction reviewed by the CTO on 2026-09-20 is accepted for implementation.

Do not reopen A/B/C concept exploration.

The remaining concerns are implementation-level continuity defects, not a new visual-design problem:
- Act 02 must not visibly leak into the initial hero viewport;
- transitions between major homepage acts must not read as abrupt background-colour cuts;
- the page must feel like one continuous spatial/product story rather than stacked gallery pages.

The accepted section composition, hierarchy, typography, card hierarchy, result layout, domain hierarchy, company/contact treatment and current interaction model are otherwise the implementation target.

## 2. Hero / first viewport invariant

At initial page load / scroll position 0:

- the header plus approved hero are the only intended visible homepage content;
- Act 02 must not peek up from below the hero;
- no old `hero-handoff` result card may reappear;
- hero choreography/media remain immutable.

Implementation may choose the most robust CSS approach for the current header model, but the visual invariant is that the hero owns the first viewport.

Prefer modern viewport units (`svh` / `dvh`) over brittle mobile `100vh` behavior.

Do not introduce scroll-jacking or mandatory scroll snapping.

## 3. Continuous page background

Acts 02, 03, 04 and the downstream homepage story should share one governing page-background token.

Do not alternate full-width section wrappers between visibly different near-black/navy colours merely to separate acts.

Section distinction should come from:
- spacing;
- typography;
- imagery;
- hairlines;
- inner-stage surfaces;
- restrained local tint where already part of the accepted design.

The viewport background itself should remain visually continuous through the main story.

## 4. Hero → Act 02 transition

The transition from the hero into The Place must feel intentional rather than exposing the next panel at rest.

Requirements:
- Act 02 begins below the hero fold;
- scrolling reveals it naturally;
- no hard colour seam between the hero bottom and Act 02 page background;
- a restrained gradient/fade bridge or equivalent compositional treatment is allowed if needed;
- do not add a large decorative animation.

A small progressive-enhancement reveal may be used:
- IntersectionObserver or equivalent;
- opacity plus a very small translate only;
- short duration;
- no per-frame layout work;
- disabled under `prefers-reduced-motion`.

## 5. Act 02 → Act 03 continuity

The Place currently ends with strong imagery while Evidence begins on a flat dark field. The implementation must soften this handoff.

Acceptable methods:
- shared background token plus sufficient vertical breathing room;
- a subtle lower-edge fade of the Act 02 visual into the page ground;
- a short transition band derived from the same page background;
- restrained hairline/metadata continuity.

Do not:
- extend the image as decorative fake content;
- create a full-screen animated transition;
- introduce a new visual concept.

## 6. Act 03 → Act 04 continuity

Evidence and Result must not appear to be separate pages because their section backgrounds differ.

Requirements:
- same governing page ground;
- retain accepted Evidence interaction and accepted Result composition;
- use spacing / heading scale / inner frames to establish hierarchy;
- no visible full-width background jump at the boundary.

The Result remains a strong payoff, but its dominance should come from the centered headline, map scale and supporting definition structure, not from a different page background.

## 7. Section heights and rhythm

Major sections do **not** need identical fixed heights.

Use content-driven heights with a consistent vertical rhythm.

Only the hero has the strict first-viewport ownership invariant.

For later acts:
- maintain generous top/bottom section spacing;
- keep the accepted centered max-width/gutter behavior for large monitors;
- avoid unnecessary full-screen sections;
- avoid content sitting against viewport edges.

## 8. Accepted composition to preserve

### Act 02 — The Place
Preserve the accepted large Landsat context composition with integrated text/protected readable zone and supporting metadata.

### Act 03 — The Evidence
Preserve the accepted same-ground layer selector and shared frame behavior.

Do not reintroduce the rejected three-equal-card gallery.

Do not add extra controls beyond the accepted final design.

Any previously explored compare-slider concept is optional/deferred unless it is explicitly present in the final accepted design; implementation must not invent one.

### Act 04 — The Result
Preserve the accepted centered result composition:
- large headline;
- dominant central Priority visual;
- concise supporting explanation;
- four-part definition/caveat structure beneath.

### Domains
Preserve the accepted current hierarchy:
- Geothermal visually primary;
- Mining + Marine secondary;
- status labels truthful.

### Proof / Company / Contact
Preserve the accepted calm low-density treatment.

No invented quantitative metric.

## 9. Motion policy

Motion is used only to improve continuity.

Allowed:
- restrained opacity/translate reveal;
- accepted layer crossfade;
- subtle hover/selection transitions;
- progressive-enhancement page transition if independently useful and no-delay.

Forbidden:
- scroll-jacking;
- mandatory scroll snap;
- parallax that competes with the hero;
- large section entrance choreography;
- motion that delays navigation;
- animation that changes scientific imagery.

All nonessential motion respects `prefers-reduced-motion`.

## 10. Media / Science boundaries

Consume the existing Product/Science authorities:
- MER-108 website display derivative authority;
- WEB Public Presentation Fidelity Policy;
- WEB-005B R9 Visual Fidelity & Runtime Performance Plan.

This implementation revision does not itself reopen or perform the post-WEB-006 WEB-007..010 media-hardening program.

Use the best currently accepted assets available to WEB-005B. The later media program may replace them without redesign.

## 11. Responsive behavior

Desktop, tablet and mobile must preserve the same narrative order.

Specific continuity gates:
- no Act 02 bleed into the first viewport on representative desktop and mobile;
- no full-width background-colour discontinuity between Acts 02/03/04;
- mobile viewport-unit behavior does not expose unintended next-section content;
- content remains centered and comfortably inset on wide monitors;
- accepted mobile stacking remains readable without horizontal overflow.

## 12. Implementation envelope

Claude may independently solve routine CSS/JS details inside these invariants:
- container sizing;
- exact spacing scale;
- gradient implementation;
- IntersectionObserver details;
- selector/crossfade mechanics;
- responsive breakpoints;
- semantic markup refinements;
- accessibility fixes;
- test updates;
- bounded cleanup/refactor required by the final layout.

Return to Product only if implementation would require:
- changing the accepted section hierarchy;
- changing public scientific meaning;
- changing the hero;
- adding a new major interaction/concept;
- changing framework/architecture;
- expanding to non-homepage routes.

## 13. Acceptance evidence

Required before Product visual review:

1. desktop full-page capture;
2. mobile full-page capture;
3. top-of-page desktop and mobile captures proving no Act 02 leakage;
4. short real-browser scroll recording showing:
   - Hero → Place;
   - Place → Evidence;
   - Evidence → Result;
   - Result → Domains;
5. reduced-motion check;
6. responsive test results;
7. existing WEB-005/WEB-005B test suite and `git diff --check`.

The scroll recording is specifically an acceptance artifact for continuity; screenshots alone are insufficient.

## 14. Terminal state

Implementation returns **REVIEW_READY / WAITING_CTO_VISUAL_REVIEW**.

No merge, deployment, DNS cutover or WEB-006 execution is authorized merely by implementation completion.
