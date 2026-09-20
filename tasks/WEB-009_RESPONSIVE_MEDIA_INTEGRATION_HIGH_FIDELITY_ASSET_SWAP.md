# WEB-009 — Responsive Media Integration & High-Fidelity Asset Swap

**Linear:** MER-145  
**State:** READY_FOR_CTO_APPROVAL — DO NOT START  
**Blocked by:** WEB-007 / MER-143 and WEB-008 / MER-144  
**Design authority:** the final CTO-accepted homepage design at execution time

## Outcome

Swap the accepted high-fidelity media families into the accepted public design and wire responsive/runtime behavior without redesigning the page.

## Scope

- replace provisional/low-quality context, Terrain, THM-01, ALT-01 and Priority visuals with accepted WEB-007 assets;
- integrate WEB-008 hero delivery variants without changing hero composition;
- configure photographic/context `srcset` / `sizes` and high-DPR selection;
- keep below-fold heavy media lazy;
- preserve explicit intrinsic dimensions/aspect ratios to prevent layout shift;
- Act 03: selected layer uses one shared frame; preload/decode only the bounded next-likely states; transitions use opacity/compositor-safe behavior;
- Context ↔ Priority compare module, if present in final design, consumes the aligned WEB-007 pair and changes only clip boundary/handle in-browser;
- preserve no-JS and reduced-motion fallbacks;
- preserve EN/TR and accessibility behavior;
- keep content blocks modular so later copy and a future verified metric can be inserted without redesign.

## Hard boundaries

No:
- new framework;
- homepage redesign;
- scientific recolouring/semantic change;
- browser-side raster reprojection or continuous analytical computation;
- fabricated quantitative proof;
- unrelated-route redesign.

## Acceptance

- exact accepted design remains visually intact except for intended quality improvement;
- focal media is sharper at intended screens without false detail;
- correct responsive candidate is selected on representative DPRs;
- no accidental eager loading of all analytical states;
- layer switch and compare interaction are smooth;
- no new CLS/accessibility/localization regression;
- media provenance/checksum pointers remain traceable.

**Terminal:** REVIEW_READY.