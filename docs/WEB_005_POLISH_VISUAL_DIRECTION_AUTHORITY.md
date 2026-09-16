# WEB-005 Polish Visual Direction Authority

**State:** ACCEPTED PRODUCT DIRECTION — R2 VISUAL LOCK  
**Repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Baseline:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`  
**Consumers:** WEB-005A, WEB-005B  
**Launch gate:** WEB-006 remains blocked until Product terminal review of these polish outcomes.

## 1. R2 disposition after current-site review

The current WEB-005A checkpoint at `ffa2f2944ca5992afb9e9891b42745a9bd1105ad` is technically coherent but **not visually accepted** for launch. Product review of the current complete-sequence recording found that the Earth treatment is strong, but the satellite/acquisition choreography and final analytical reveal remain materially below the accepted visual target.

This is not a new product concept. It is a bounded visual revision of the same WEB-005A outcome. Preserve all conformant geometry, fallback, scientific-boundary and media work that remains useful; do not restart from scratch merely to satisfy this revision.

The two execution-time reference images supplied by the CTO are accepted as **visual/composition references only**:

- **Reference A — orbital acquisition composition:** Earth dominant on the right, readable generic EO satellite in the lower-left/left-lower composition, visible orbital-arc feeling, multiple clean cyan acquisition lines, and a luminous rectangular target/footprint frame on Earth.
- **Reference B — analytical reveal composition:** camera nearer the target, target frame remains luminous, analytical surface inside the frame becomes vivid and visually dominant with relief/contour-like depth and high visual energy.

These references are not source assets, are not evidence, and must not be copied into production. They define composition, visual hierarchy, glow/energy level and reveal language only. All production assets must remain rights-safe and provenance-traceable.

## 2. Hero cinematography — hard visual direction

The hero must read as one premium orbital-acquisition story:

1. Earth establish with the strong accepted 3D Earth treatment;
2. a **readable** generic Earth-observation satellite emerges from behind/around the Earth limb on a visible orbital arc;
3. the satellite settles into an acquisition attitude in the lower-left / left-lower composition relative to Earth, without becoming oversized;
4. two or more clean cyan sensing lines, or an equally legible restrained multi-line/boresight treatment, visibly connect satellite and target region;
5. the target frame activates with a thin crisp cyan core plus controlled emissive halo/corner-lock response;
6. the camera continues toward the same registered target without a geometric jump;
7. the acquisition frame remains visually alive during the approach instead of fading into a nearly invisible outline;
8. the final handoff reveals governed analytical content **in or directly coupled to the target region**, creating a clear climax rather than a small detached result card or an accidental stalled hold.

The Earth remains the dominant visual object. The satellite must nevertheless be unmistakably readable during the acquisition beat: a viewer should recognize a 3D EO platform, solar panels and body silhouette without having to search for it.

### Satellite quality lock

Use a rights-safe generic EO 3D satellite, or an in-repository model with equivalent visual quality, with:

- volumetric body;
- solar panels with visible thickness / panel structure;
- material separation and physically coherent highlights;
- restrained antenna/sensor-housing detail;
- believable attitude relative to the target;
- no specific operational spacecraft/sensor identity claim.

A flat cutout, tiny unreadable silhouette, or generic bright speck is rejected.

### Orbital composition lock

The visible pass should approximate the accepted Reference-A reading:

- satellite enters from behind/around the Earth limb rather than appearing already parked near target;
- the orbital movement is legible in screen space;
- acquisition beat places the satellite toward the lower-left/left-lower part of the hero composition while Earth remains right-dominant;
- a subtle orbital trail may support the path but must remain secondary;
- the satellite must not clip the frame during the hero's intentional acquisition beat.

Numerical orbital solving remains implementation-owned. Physical plausibility does not override visual readability; both are required.

## 3. Acquisition FX — hard visual direction

The current nearly invisible cone treatment is **not** the target. The effect must be restrained but clearly readable at normal 1440-class desktop viewing.

Accepted direction:

- beam core: `#7FEFFF`;
- beam glow: `#3CCBFF`;
- target frame: `#98F5FF`;
- thin multi-line sensing / boresight geometry is preferred over one large translucent slab;
- lines may taper or soften toward the target but must stay visibly connected to satellite and footprint;
- optional local glow/pulse at acquisition is encouraged;
- target border must have a crisp core and controlled outer glow, not only a low-opacity grey/cyan line.

Rejected:

- fuzzy white slabs;
- opaque cones that obscure Earth;
- barely perceptible acquisition FX;
- noisy particles;
- game-like lasers;
- sensor-physics claims.

## 4. Target frame / final handoff lock

The target frame must have a visible activation event. A viewer should see the target become acquired/locked, not merely notice a rectangle later.

The final hero state must be a resolved visual handoff. Preferred behavior is:

- target frame/corner locks intensify briefly and settle;
- camera reaches the regional target;
- a governed page-layer analytical surface appears inside, clipped to, or immediately adjacent to the same target geometry;
- the analytical reveal is visually substantial enough to read as the product result, not a small floating UI card;
- HTML headline/CTA remains separate from rendered media;
- governed pixels are not baked into lossy video where colour semantics would be altered.

The analytical teaser may be the accepted priority output or another Science-authorized governed surface. It must retain exact public label/warning semantics where visible.

## 5. Earth/source-resolution lock

The current Earth model/lighting direction is accepted and should be preserved. The regional softness diagnosis is also accepted: the source texture is under-resolved at the regional hold.

WEB-005A is authorized to use a materially higher-resolution rights-safe Earth/albedo source after exact source, rights basis, dimensions and checksum are recorded. The regional hold must materially reduce source-texture upscaling compared with the rejected checkpoint. Media ceilings remain unchanged unless separately revised by Product.

## 6. Homepage public visual direction

The final homepage remains exactly four major visual acts:

1. cinematic acquisition hero;
2. real Kızıldere EO context;
3. compact Terrain + THM-01 + ALT-01 evidence trio;
4. large `mvp_remote_sensing_priority_v1` result climax.

### Act 2 — real place

The current Kızıldere context image remains provenance-valid but the reviewed implementation reads too much like a technical/processed raster. WEB-005B must replace or re-present it so it immediately reads as a real natural-colour Earth-observation view of the place before analysis.

Required qualities:

- natural-looking land/water/terrain relationships;
- photographic/geographic rather than thematic-raster appearance;
- restrained processing;
- enough local contrast to read terrain and settlement/agricultural structure;
- no synthetic-looking palette, fake basemap or ungoverned provider substitution;
- no aggressive browser upscaling.

### Act 3 — evidence trio

Terrain, THM-01 and ALT-01 remain exactly the evidence trio. The current cards are technically valid but visually too flat/report-like. The final presentation should feel like one coherent analytical stage:

- larger and more image-led cards;
- stronger framing and local contrast;
- consistent metadata/legend placement;
- vivid but truthful presentation;
- no detached technical chrome;
- no scientific recolouring unless Science authority permits it.

### Act 4 — analytical climax

The priority/result section must be the strongest non-hero visual on the page. The current small contained map presentation is not the desired final hierarchy.

The final result should be visually dominant through scale, framing, surrounding negative space, typography and an integrated legend. Once Science palette authority exists, the public analytical palette may become more vivid; until then governed pixels remain unchanged.

## 7. Product-owned palette lock

### Brand / UI

- Background: `#030B12`
- Surface: `#08131D`
- Panel: `#0D1B27`
- Fine lines/dividers: `#183245`
- Primary text: `#EAF2F8`
- Secondary text: `#9EB1C1`
- Muted metadata: `#6F8597`
- Accent cyan: `#73E7FF`
- Glow cyan: `#8AF1FF`

### Acquisition / hero FX

- Beam core: `#7FEFFF`
- Beam outer glow: `#3CCBFF`
- Target frame: `#98F5FF`
- Supporting glow/trail remains controlled but must be visible enough to communicate acquisition.

### Analytical palette direction — PRODUCT TARGET, SCIENCE-GATED

- Terrain/elevation: muted relief / earth-safe sequential treatment.
- Thermal anomaly: perceptually ordered dark-purple → magenta/red → warm-yellow progression.
- Alteration proxy: distinct teal → green → yellow progression.
- Priority/result: controlled ordered palette, high visual contrast without probability-like red/green good/bad semantics.

Exact value-to-colour mappings, class breaks and replacement of governed raster palettes require Science acceptance.

## 8. Human visual review evidence

A public preview URL is optional. Product visual review may be completed from:

- 1440 desktop screenshots;
- 768 tablet screenshots where layout changes materially;
- 375 mobile screenshots;
- short full-sequence hero capture;
- before/after hero stills at entrance, acquisition, regional hold and final handoff.

For WEB-005A R2, Product visual acceptance specifically compares the implementation against the two CTO-provided reference images for **composition and energy only**, while checking that production assets and scientific surfaces remain original/rights-safe/governed.

## 9. Invariants

- No production deploy, DNS/domain cutover or WEB-006 work under this authority.
- No new scientific method, score meaning, thresholds, eligibility, CRS/grid/unit/NoData/mask/resampling semantics.
- No specific-sensor identity or fabricated sensing-physics claim.
- Existing four-act architecture, EN/TR parity, accessibility and fallbacks remain binding.
- Routine render/encode iteration, CSS/layout fixes, test repair and evidence publication are implementation-owned.
