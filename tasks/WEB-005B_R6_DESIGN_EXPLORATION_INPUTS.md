# WEB-005B R6 — Design Exploration Inputs and Interaction Boundary

**State:** DESIGN_EXPLORATION_READY  
**Parent:** MER-109 / WEB-005B  
**Consumes:** WEB-005B R5 CTO visual-review failure / design-exploration authority  
**Accepted hero:** WEB-005A @ `1135e7a7e0b0f6db6348dee139d505550d8ca8b9`

## 1. Identity during concept exploration

No final OrbGSS logo/mark is approved.

For all homepage concepts:
- use a neutral text wordmark `OrbGSS` only where a brand label is required;
- do not use repository `logo.svg` / `mark.svg` as final identity;
- do not spend this task on logo design;
- identity work may happen separately later without blocking homepage composition.

## 2. Domain-card taxonomy for design exploration

Use the following structural prototype taxonomy:

- **Geothermal** — active / first application
- **Mining** — coming soon / in development
- **Marine** — coming soon / in development

These are Product-approved prototype labels for design exploration, not final marketing copy.

Do not substitute Environmental & Land Intelligence as the third domain in this exploration.

## 3. Evidence interaction decision

The preferred production interaction for Act 03 is a **single dominant evidence stage with accessible tabs / segmented layer selector** controlling the same geographic frame:

- Terrain / Elevation
- THM-01 / Thermal
- ALT-01 / Alteration

Desktop may add subtle crossfade / spatial continuity motion between states.
Mobile must remain direct and touch-friendly.

A scroll-driven progression may be explored only as an enhancement around the tabbed state model, not as the sole control. Avoid comparison sliders as the default because these are three discrete governed layers, not a two-image before/after problem.

The selected design must have a usable no-JS fallback:
- all evidence remains reachable/understandable;
- scientific imagery/caveats are not hidden behind JS-only behavior.

This preserves accessibility, resilience and the current static-site architecture.

## 4. Proof / differentiator content

No quantitative OrbGSS accuracy, success-rate, ROI, customer, revenue, deployment-count or scale metric is currently Product-authorized for homepage publication.

Therefore concept exploration must use **qualitative proof/differentiator modules only**.

Safe structural themes include:
- evidence-backed screening;
- traceable provenance;
- explicit data gaps;
- AOI-first analysis;
- remote narrowing before field investigation;
- decision support, not fieldwork replacement.

Design may reserve a future metric/proof slot, but it must be visibly placeholder-only in design artifacts and must not ship until an owning domain publishes a verifiable metric.

## 5. Production-stack boundary

The production website remains static HTML + CSS + vanilla JavaScript under current repository authority.

Design concepts must therefore be implementable without introducing React, Vue, WebGL frameworks or another application framework.

Claude Design may use its own prototyping machinery internally, but the selected concept must map cleanly to:
- semantic HTML;
- responsive CSS;
- progressive-enhancement vanilla JS;
- reduced-motion behavior;
- existing asset/provenance constraints.

A lightweight canvas/WebGL effect is not authorized by default. If a concept materially depends on one, flag it explicitly as a Product architecture decision rather than assuming it.

## 6. Design skills / spatial boundary

For Claude Design exploration, use:

- **Front-end Design** — primary skill.
- **Maps & Geography** — allowed as a supporting skill.

Maps & Geography is authorized only for:
- geographic framing;
- AOI/spatial hierarchy;
- same-ground layer comparison;
- coordinate/scale/legend literacy;
- spatial storytelling and map-aware responsive composition.

It must NOT turn the marketing homepage into:
- a GIS dashboard;
- a slippy-map application;
- a control-heavy map UI;
- a field of pins/markers;
- a generic cartographic interface.

The homepage remains an editorial product story.

## 7. Concept exploration requirement

Create three genuinely different homepage concepts after the immutable hero:

### Direction A — Cinematic spatial narrative
Immersive image-led continuation; Act 02 overlay composition; Act 03 one-stage layer switching; Act 04 strong visual payoff.

### Direction B — Premium geospatial platform
Clearer product structure; image-led domain cards; compact differentiators/proof modules; evidence stage remains central.

### Direction C — Editorial science-led
Restrained, publication-like composition; strongest typography/negative-space discipline; analytical imagery treated as premium editorial material.

All directions must include:
- approved hero unchanged;
- redesigned Acts 02–04;
- domain cards using Geothermal / Mining / Marine prototype taxonomy;
- qualitative differentiator/proof treatment;
- responsive desktop/tablet/mobile logic;
- restrained motion;
- no unsupported copy/metrics.

## 8. Review output

Before implementation, surface:
- interactive or page-scrollable concept for each direction;
- desktop and mobile views;
- section-by-section rationale;
- interaction behavior;
- implementation complexity;
- accessibility/reduced-motion implications;
- explicit list of any concept feature that would exceed current vanilla-stack authority.

No Cloud Code implementation begins until CTO selects a direction.

**Current state:** `DESIGN_EXPLORATION_READY / WAITING_CONCEPTS`.
