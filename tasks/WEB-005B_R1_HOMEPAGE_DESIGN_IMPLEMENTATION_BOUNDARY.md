# WEB-005B R1 — Homepage Design & Implementation Boundary

**State:** CTO_START_GRANTED / BLOCKED_ONLY_BY_WEB-005A_PUBLICATION  
**Parent:** WEB-005 / MER-93  
**Consumes:** WEB-005A / MER-107 terminal accepted hero once exact remote HEAD is published  
**Implementation branch:** `feat/web-005b-homepage-visual-fidelity`  
**Supersedes only where conflicting:** `tasks/WEB-005B_HOMEPAGE_VISUAL_FIDELITY_PALETTE.md`

## 1. CTO decision

The WEB-005A hero visual is CTO-approved. No further hero visual redesign is requested.

WEB-005B now owns the remaining **homepage visual design and frontend implementation** needed to bring Acts 2–4 to launch quality. This task does not own marketing copy, product messaging, claims, narrative wording, or final page content. Those decisions will be supplied by a separate content-owning domain later.

Other website routes/pages are deliberately deferred until the homepage reaches Product visual acceptance.

## 2. Start dependency and baseline

Before WEB-005B implementation begins, finish the publication-only closeout of WEB-005A:

1. publish local accepted checkpoint `1135e7a7e0b0f6db6348dee139d505550d8ca8b9` to `origin/feat/web-005a-hero-visual-fidelity` by non-force fast-forward;
2. verify exact remote HEAD equals that SHA;
3. rerun only the bounded existing validators needed to prove published bytes remain GREEN;
4. do not rerender the 276-frame hero;
5. do not revise the accepted hero visuals.

If and only if those checks pass, treat `1135e7a7e0b0f6db6348dee139d505550d8ca8b9` as the WEB-005A terminal implementation baseline for WEB-005B and branch `feat/web-005b-homepage-visual-fidelity` from that exact commit unless an already-published canonical integration commit contains byte-identical accepted hero output.

Do not merge to `main`, deploy, or change DNS in this task.

## 3. Scope — homepage only

WEB-005B owns the visual system and implementation for the homepage after the accepted hero:

- Act 2 — Kızıldere real EO context;
- Act 3 — Terrain / THM-01 / ALT-01 evidence composition;
- Act 4 — Priority/result climax;
- section spacing, visual rhythm, responsive composition, framing, typography treatment, image sizing/cropping, motion that is lightweight and frontend-native, and shared visual tokens;
- responsive/accessibility implementation for the homepage;
- integration continuity with the accepted hero.

Do not redesign or implement the other public routes/pages in this task.

## 4. Content ownership boundary

Existing homepage copy is **content placeholder/frozen input**, not Product authority for final wording.

Implementation must:

- preserve existing visible copy unless a change is mechanically required for layout, localization integrity, accessibility, or a clearly broken UI string;
- not invent new marketing claims, technical claims, headings, slogans, customer promises, statistics, scientific interpretation, or CTA language;
- not spend implementation time rewriting EN/TR copy;
- use layout structures that can tolerate later content replacement without redesign;
- flag any copy-length/layout collision as a content-handoff note rather than solving it by rewriting meaning.

Placeholder shortening for purely visual prototyping is allowed only in non-shipping scratch evidence and must not replace repository copy.

## 5. Hero preservation boundary

WEB-005A is visually accepted and becomes an immutable upstream component for this task.

Allowed:

- bounded DOM/CSS integration needed to make the transition from hero to Act 2 coherent;
- performance/loading wiring that does not change accepted hero appearance or choreography;
- responsive shell fixes outside the accepted visual sequence where necessary.

Not allowed:

- Blender work;
- rerendering the accepted production hero;
- changing choreography, camera, satellite, beam/scan behavior, AOI lock, DEM rise, Terrain→THM→ALT→Priority sequence, timing, or final hold;
- palette or asset substitutions inside the accepted hero without a new Product decision.

## 6. Visual direction

### Act 2 — real place before analysis

The section must read immediately as **natural Earth-observation context**, not as an analytical raster or report export.

Priorities:

- large, image-led composition;
- natural-colour EO appearance;
- strong geographic legibility;
- restrained framing;
- continuity from the cinematic hero into the real Kızıldere ground context;
- provenance-safe source/derivative only.

### Act 3 — evidence system

Terrain, THM-01 and ALT-01 remain exactly the three major evidence families shown.

The three must read as a **single analytical composition**, not three independent report cards.

Priorities:

- stronger image area;
- common geometry/alignment language;
- clear but restrained metadata;
- consistent framing and responsive behavior;
- visual depth through layout, contrast, cropping and surrounding UI rather than semantic transformation;
- no Structure/Geology promotion into a fourth major homepage evidence act.

### Act 4 — analytical climax

The Priority result must be the dominant post-hero visual on the homepage.

Priorities:

- materially larger than an individual evidence visual;
- minimal surrounding clutter;
- strong negative space;
- direct visual continuity from evidence to result;
- governed palette from accepted MER-108 authority;
- no decorative detached scientific colour strip;
- preserve exact scientific meaning and warnings already governed elsewhere.

## 7. Palette authority

Consume accepted Science authority from MER-108:

- terminal hero/display authority at `geothermal-prospectivity@30779547ced0cbf047cb51fb6c2c6ed178547d56`;
- do not invent alternative value-to-colour mappings;
- keep NoData/masked support transparent as governed;
- UI/brand cyan and framing FX remain Product-owned and non-scientific.

The existing Product UI tokens from the parent WEB-005B task remain valid unless a purely presentational token refinement is needed. Any governed analytical mapping change is out of scope.

## 8. Implementation envelope

This is now ordinary frontend/product visual implementation. Heavy Blender/render work is not expected.

The implementer may independently resolve routine:

- CSS/layout/component structure;
- image derivatives and responsive delivery;
- lightweight motion/transitions;
- accessibility;
- localization-safe layout;
- test/validator updates;
- asset loading/performance;
- bounded refactors needed for maintainability.

Do not return to Product for routine implementation details. Return only for a genuine change to public behavior, material architecture, governed scientific semantics, security/data policy, or this scope boundary.

## 9. Acceptance

All parent WEB-005B gates B-VIS-01..B-VIS-12 remain applicable, with these additions:

### B-VIS-13 — copy-preservation boundary
Repository-visible marketing/product/scientific copy is not materially rewritten by WEB-005B. Any mechanical text change is enumerated and justified.

### B-VIS-14 — homepage-only scope
Changed-path and screenshot evidence shows no intentional visual redesign of non-homepage routes.

### B-VIS-15 — accepted-hero preservation
Visual regression evidence shows the WEB-005A accepted hero remains materially unchanged while the hero→Act 2 transition remains coherent.

At REVIEW_READY provide:

- exact final HEAD and changed-path inventory;
- 1440, 1024, 768 and 375 px homepage screenshots;
- before/after evidence for Acts 2–4;
- B-VIS-01..B-VIS-15 matrix;
- provenance/checksum evidence for analytical/context assets;
- responsive/accessibility/localization validator results;
- explicit list of any visible-copy changes, expected to be empty or mechanical only;
- explicit statement that no Blender/full hero rerender was performed;
- explicit `NOT RUN` for any unavailable check.

## 10. Out of scope

- non-homepage page redesign;
- final website copy/content decisions;
- new marketing/scientific claims;
- hero visual redesign or heavy render work;
- new scientific method/threshold/score semantics;
- production deployment, DNS, domain cutover;
- CMS/framework migration.

**Terminal implementation state:** `REVIEW_READY`.
