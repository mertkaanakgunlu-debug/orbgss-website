# OrbGSS public homepage visual narrative authority

**State:** `CANONICAL PRODUCT DECISION / PLANNING LOCK`  
**Owner:** Product & Software  
**Applies to:** future `WEB-005` final homepage/public-release integration  
**Does not start implementation:** yes  
**Current implementation baseline:** WEB-004 accepted; existing six-route site remains valid until WEB-005 replaces the homepage composition  
**Primary blocker before WEB-005 start:** accepted `WEB-HERO-001D` handoff + deliberate CTO start approval

## 1. Why this authority exists

WEB-001..WEB-004 established the correct product semantics, real Kızıldere proof assets, public routes, provenance discipline, accessibility and performance baseline. The accepted homepage is therefore a technically valid intermediate state, but it is not the intended final public composition.

Product review of the accepted WEB-004 homepage identified four presentation problems that WEB-005 must resolve without reopening scientific method:

1. the repeated `dark beam -> full-width raster` rhythm makes the page feel like a technical gallery rather than a premium product story;
2. several proof derivatives are visually soft when stretched full-width, so correct scientific imagery reads as low-quality texture rather than intentional cartography;
3. detached explanations, warnings and scale bars make ownership between copy and the associated visual ambiguous;
4. the homepage gives too many scientific states equal visual weight instead of building toward one clear analytical result.

The final public homepage must therefore preserve truth/provenance while becoming materially simpler, more legible and more cinematic.

## 2. Locked public-homepage story

The primary visual story has **four major visual acts**. Supporting product/company/contact sections may follow, but they must not create additional equal-weight gallery scenes.

### Act 1 — Cinematic acquisition hero

Accepted `WEB-HERO-001D` supplies the pre-data scene base. WEB-005 owns final real-data/media integration.

Required presentation:
- Earth/satellite/AOI acquisition motion as the background/visual field;
- HTML headline/copy remains separate from the render;
- primary copy sits in a stable motion-safe region, normally left-aligned on desktop;
- a restrained dark gradient/shade may protect text contrast without hiding the scene;
- the hero communicates observation/acquisition, not fabricated sensor physics;
- mobile/reduced-data/reduced-motion receive an intentional static/poster experience.

Binding media envelope inherited from WEB-004:
- WebM <= 3.0 MiB;
- MP4 <= 4.5 MiB;
- poster <= 180 KiB;
- mobile/reduced-data must not download both video encodes.

### Act 2 — Real AOI / Earth-observation context

Immediately after the hero, show **one high-quality real image of the selected Kızıldere AOI** so the viewer understands that the subsequent analysis belongs to a real place.

Presentation intent:
- one strong image, not another sequence of technical map panels;
- modest copy integrated with the visual through overlay or a tightly coupled split layout;
- avoid aggressive zoom/crop that turns terrain into an indistinct texture;
- do not upscale a low-resolution proof derivative to fill a large desktop viewport.

This act requires a public-safe, provenance-traceable EO/natural-colour or equivalent approved AOI master. The existing WEB-002 `observe` DEM/AOI proof is not automatically sufficient for this role and no ungoverned basemap/raw provider raster may be substituted.

### Act 3 — Compact evidence section

Replace the current separate full-width Observe/Terrain/Evidence/Structure scenes with **one compact evidence composition**.

Default three evidence cards:
1. **Terrain / Topography** — NASADEM context;
2. **Thermal** — THM-01 evidence;
3. **Alteration** — accepted Sentinel-2 alteration evidence, choosing the clearest truthful public presentation of ALT-01/ALT-02 without implying mineral identification.

Rules:
- cards are a deliberate exception to the general anti-card-wall rule: exactly one compact three-evidence composition, not a generic SaaS card grid;
- the three cards must visibly belong to the same AOI and same story stage;
- Structure/Geology is **not a mandatory third card**. Under current authority it remains `optional support / DATA_GAP / score-invariant` and must not consume a large empty homepage scene;
- if public-safe structure/geology becomes available later, Product may decide whether it replaces or supplements a card, but WEB-005 must not invent it;
- scientific warnings remain truthful and visible, but should be subordinate supporting copy rather than dominating the page hierarchy. Deep technical explanation remains available on `/pilot/` and `/platform/`.

### Act 4 — Priority/result climax

The analytical climax is **one large, high-quality priority/result map** using the accepted `mvp_remote_sensing_priority_v1` semantics.

Public label remains:

**Remote-Sensing Relative Priority — Experimental Baseline**

Do not relabel it as probability, Full Prospectivity, reserve/resource, discovery likelihood or drilling-success likelihood.

Presentation intent:
- this is the strongest analytical visual after the hero;
- it may be full-width only when the delivered pixel density supports that presentation without visible softness;
- otherwise use a deliberately contained/max-width composition rather than stretching a smaller raster;
- the result should visually answer the hero promise: **where to look next**.

## 3. Beam, copy and hierarchy decision

The WEB-001/002 dark-beam grammar remains part of the OrbGSS identity, but **the repeated tall detached beam between every scientific image is superseded for the final homepage**.

WEB-005 should:
- retain dark technical surfaces, thin separators, small monospace chapter metadata and restrained cyan accents;
- reduce large beam blocks to occasional section transitions or tightly coupled copy regions;
- visually attach each heading/explanation to the visual it describes;
- use overlay copy on protected image regions or intentional split layouts where appropriate;
- vary composition across the four acts so the page does not repeat one template mechanically;
- keep deep technical detail on the dedicated Platform/Pilot pages rather than reproducing report-like density on the homepage.

## 4. Legend / colour-bar policy

Detached scientific colour bars or scale strips must **not** sit in a separate homepage beam as decorative technical chrome.

Homepage rule:
- evidence cards normally show no detached legend;
- if a legend is necessary to understand a map, integrate a compact truthful legend **inside the map/visual frame**;
- the priority map may carry a small embedded 0–100 legend when useful, but it must not become an independent layout element;
- detailed legends, methodology and interpretation belong on `/pilot/` or `/platform/`.

This changes presentation only. It does not authorize recolouring or reinterpretation of scientific values outside accepted Science/public-visual authority.

## 5. Image-quality / derivative policy

WEB-005 must treat visual quality as an acceptance criterion, not merely file validity.

Rules:
- do not stretch a scientific derivative materially beyond its useful native pixel density merely to fill the viewport;
- prefer a higher-resolution web derivative from an accepted/public-safe master when available;
- if a higher-resolution master cannot be produced without changing Science/data authority, use a contained composition instead of upscaling;
- preserve scientific rendering semantics, NoData/mask behavior and provenance;
- crop only for presentation and only when the crop does not create misleading spatial interpretation;
- same-AOI visuals should keep coherent geographic framing/orientation unless a deliberate close-up is clearly signalled;
- responsive `srcset`/`sizes` and checksums/provenance remain mandatory.

For full-width desktop visual roles, Product expects a master/derivative large enough to remain visually crisp at the rendered size. `1400px square stretched across a ~1600px+ viewport` is not an acceptable default presentation pattern.

## 6. Supporting homepage sections after the four acts

After the four visual acts, the homepage may contain compact supporting sections:
- Geothermal = active first application / Kızıldere pilot;
- Mineral Exploration and Environmental & Land Intelligence = expansion directions;
- company/trust principles;
- restrained contact/partnership CTA.

These sections must remain visually subordinate to the four-act story and should not restart the full-width technical gallery rhythm.

The accepted deep routes `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/` remain valid and should carry the denser technical/product context removed from the homepage.

## 7. WEB-HERO-001 join rule

This authority does **not** change active WEB-HERO-001C/D implementation.

The hero lane remains pre-data and isolated. Its responsibility is to deliver:
- a premium continuous global-to-regional scene;
- headline-safe opening composition;
- stable regional AOI hold;
- clean real-data injection/handoff points.

WEB-005 consumes the accepted WEB-HERO-001D result and performs:
- approved real-data/layer integration;
- final media encoding/fallbacks;
- the four-act homepage recomposition in this authority;
- responsive/accessibility/performance regression testing;
- release-candidate evidence.

No separate homepage-redesign implementation starts before that gate unless Product publishes a new task.

## 8. Additional WEB-005 acceptance requirements

The eventual exact `tasks/WEB-005_CINEMATIC_HERO.md` must include, in addition to existing hero/media requirements:

1. Homepage primary visual hierarchy is exactly four major acts: Hero -> real AOI context -> compact evidence trio -> priority/result climax.
2. No repeated six-scene Observe/Terrain/Evidence/Structure/Priority/Geothermal full-width gallery remains on the final homepage.
3. Structure/Geology is not fabricated and does not occupy a large standalone homepage gap scene under current authority.
4. Copy/visual ownership is immediately clear without relying on scroll position to infer which text belongs to which image.
5. No detached homepage scale bars/legends; any necessary legend is integrated inside its associated visual.
6. Homepage scientific imagery is visually crisp at desktop/tablet/mobile presentation sizes; no obvious browser upscaling of undersized proof rasters.
7. Scientific warnings/labels remain truthful and accessible, with deep technical detail delegated to the accepted deep routes where appropriate.
8. Existing EN/TR, keyboard, provenance/checksum, responsive, metadata and claim-discipline checks remain green.
9. WEB-004 performance floors remain the regression baseline; hero media stays inside the accepted envelope unless Product explicitly revises it.
10. Review evidence includes desktop/tablet/mobile screenshots of all four acts, plus a visual-quality inventory showing source/master dimensions, rendered dimensions and derivative selection for each major homepage visual.

## 9. WEB-006 launch-gate additions

WEB-006 remains a deployment/DNS task, not a redesign task. Before DNS cutover it must verify that the accepted WEB-005 release candidate, not an older WEB-004/static or legacy build, is the deployed source.

Launch visual smoke must include:
- hero poster/playback/fallback state;
- real AOI visual;
- three-card evidence section;
- priority/result climax;
- EN/TR on representative routes;
- mobile layout;
- no broken/degraded major imagery;
- production asset caching/content-type behavior for WebM/MP4/WebP/poster assets.

Any visual regression found during WEB-006 returns to a bounded code branch/review; WEB-006 itself does not redesign the site.

## 10. Outstanding domain input before WEB-005

A future public-safe visual package is required for the final composition:

- one high-quality real Kızıldere EO/natural-colour context master suitable for Act 2;
- sufficiently high-resolution, presentation-safe masters/derivatives for the evidence cards and large priority result so WEB-005 does not rely on browser upscaling;
- exact provenance/rights/checksum/public labels and the same no-new-science boundaries as WEB-002.

This is a Science & Geospatial publication/export dependency, not authority for Product to invent new imagery or scientific semantics.

## 11. Precedence

This document supersedes earlier homepage-layout concepts where they conflict, including the repeated full-width proof-scene rhythm and the R7 assumption that faults/structural evidence must occupy one of the three evidence cards.

It does **not** supersede:
- accepted Science semantics;
- WEB-002 provenance/public-safe constraints;
- WEB-004 performance/accessibility decisions;
- WEB-HERO-001 geometry/cinematography invariants;
- the accepted public route/navigation architecture.
