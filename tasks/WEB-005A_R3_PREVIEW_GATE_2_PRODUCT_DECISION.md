# WEB-005A R3 Preview Gate 2 — Product Open-Point Decision

**State:** CONTINUATION_AUTHORIZED / AWAITING_PUBLISHED_PREVIEW_REVIEW  
**Parent:** WEB-005A / MER-107  
**Reported local preview checkpoint:** `feat/web-005a-hero-visual-fidelity@b6cd5fb8df017a9c2b8b847c14348633bdc933e8`  
**Reported evidence:** `tasks/WEB-005A_R3_PREVIEW_GATE_2.md`  
**Previous Product decision:** `c7c6cb10e305c9de63d805c414b332440fd87ddb:tasks/WEB-005A_R3_PREVIEW_GATE_PRODUCT_DECISION.md`

This decision resolves the Product questions raised by Preview Gate 2. It does not constitute exact-head acceptance because the reported feature commit has not yet been published to origin and the motion animatic has not yet been visually reviewed by Product/CTO.

## 1. Four-beam bundle at the true AOI is accepted in principle

The primary four beams must continue to terminate at the four true governed AOI corners.

At global-view scale the true 36 km footprint is only a few pixels wide, so the four lines will naturally read as a slender bundle near the ground. That is acceptable and is preferable to visually separating them by using false enlarged ground anchors.

Preserve:

- true governed corner endpoints;
- progressive satellite-to-ground draw-on;
- thin cyan cores;
- staggered draw timing;
- translucent scan fan / curtain as the element that gives acquisition breadth.

Do not artificially spread primary beam endpoints away from the true AOI solely for readability.

## 2. Satellite/caption collision is NOT accepted

The reported lower-right exit crossing the hero caption around frame 204 is a Product defect.

Required:

- preserve the <=22% no-fly-by envelope;
- preserve the acquisition position that clears the main copy;
- alter the post-scan orbital continuation, timing, camera easing, or bounded combination so the satellite and its motion-blur envelope remain clear of the bottom-right caption/readability zone;
- do not solve this by moving or weakening required caption copy.

The satellite may leave frame after acquisition, but it must retire visually without crossing text or becoming a distracting streak.

## 3. NoData / masked areas should reveal non-analytical Terrain/context below, not render as dark analytical patches

The dark areas reported on ALT-01 / Priority are caused by the feathered analytical alpha/mask. Do not fill, extrapolate, or invent analytical values.

For the website hero presentation:

- governed invalid / NoData support remains analytical alpha 0;
- show the already-authorized Terrain / neutral Earth-context surface beneath those transparent analytical areas;
- the underlay must remain clearly non-analytical context and must not be interpreted as valid Priority/ALT data;
- filtering must not expand the governed valid mask;
- no hole filling, inpainting, dilation, or invented support.

This is consistent with the terminal MER-108 hero display authority, which allows authorized context/hillshade beneath analytical NoData while preserving the mask.

The final visual should therefore read as thematic analysis draped over terrain, with terrain visible through invalid/masked support, rather than black/dark false data patches.

## 4. No hero colorbar, legend, info card, or layer label

The WEB-005A hero analytical reveal is intentionally visual-only.

Do not add:

- colorbars;
- legends;
- floating result cards;
- information cards;
- per-layer title/label overlays;
- a final Priority label inside the hero.

The lower homepage acts already explain the analytical layers and their semantics.

Retain only the existing generic hero/caption disclosures required by the wider website authority (for example rendered-sequence/source truthfulness), outside the cinematic analytical payoff. Do not introduce analytical UI chrome into the hero.

## 5. Timing

The reported Preview Gate 2 timing is inside the previously approved envelope:

- motion: 11.5 s;
- analytical reveal: 2.75 s;
- then stable Priority hold.

Do not lengthen it.

The scan sweep at 1.33 s is directionally acceptable and materially better than the first preview's 1.92 s. Final pacing remains subject to human motion review of the actual animatic. If it still feels slow, shorten dead time around settle/slew/lock rather than making the beam draw-on abrupt or turning the analytical reveal into a flash.

## 6. Colour / line language

The reported move from near-white to measured cyan and the thinner line/frame intent are accepted directionally.

Preserve:

- thin technical beam cores;
- thinner AOI/reticle language;
- restrained cyan/teal fan;
- no milky-white dominant scan volume.

Production colour acceptance will be judged from the published visual evidence, not numeric saturation alone.

## 7. Publication and review gate

Push the reported feature checkpoint to origin so Product can verify the exact commit and committed evidence.

The motion animatic itself may remain outside Git/site media, but it must be provided directly for Product/CTO review together with the five 1440x900 composites.

Do not start a long/full production render until:

1. the feature checkpoint is published and exact-head verified;
2. Product/CTO visually reviews the actual Preview Gate 2 motion animatic;
3. the satellite/caption collision is corrected;
4. the NoData/context behavior above is reflected in the final preview evidence.

**Continuation:** existing MER-107 execution authority remains active. No new CTO start is required.
