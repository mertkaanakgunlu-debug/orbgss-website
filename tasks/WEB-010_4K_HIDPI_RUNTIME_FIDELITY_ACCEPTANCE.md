# WEB-010 — 4K/HiDPI Runtime Fidelity & Smoothness Acceptance

**Linear:** MER-146  
**State:** READY_FOR_CTO_APPROVAL — DO NOT START  
**Blocked by:** WEB-009 / MER-145

## Outcome

Terminally verify that the media-hardened public site remains visually premium, scientifically truthful and smooth on representative real browsers/devices, including large/high-DPR displays.

## Required matrix

At minimum:
- 375 mobile;
- 768 tablet;
- 1024;
- 1440 desktop;
- 1920-class desktop;
- 4K/high-DPR desktop where available.

Test representative supported browsers rather than relying on screenshots alone.

## Evidence

For focal image/video surfaces record:
- selected asset/encode;
- transfer bytes;
- decoded pixel dimensions;
- CSS rendered dimensions;
- device-pixel dimensions / DPR;
- cache/content-type behavior;
- whether any upscaling occurs.

For hero:
- poster continuity;
- time-to-play where measurable;
- steady-state dropped-frame/playback evidence where available;
- no black/blank transition;
- fallback and reduced-motion path.

For Act 03:
- selected-state responsiveness;
- no input lag/jank;
- no layout shift;
- predecode/prefetch remains bounded.

For compare module, if present:
- pointer/touch/keyboard behavior;
- smooth clip-boundary movement;
- no browser-side raster recomputation;
- mobile fallback quality.

Scientific checks:
- no palette drift;
- no NoData/mask bleed;
- legends/caveats remain correct;
- no unintended browser filters.

## Allowed bounded fixes

May tune:
- responsive breakpoints/source thresholds;
- preload/prefetch/lazy-load policy;
- accepted codec/bitrate variant choice;
- caching/content headers and immutable asset naming;
- compositor-friendly transition duration;
- native View Transitions as progressive enhancement only when measured beneficial.

Do not:
- redesign;
- migrate frameworks;
- change scientific semantics;
- revise hero choreography/render content.

## Terminal criteria

All critical fidelity/runtime gates GREEN and any unavailable check explicitly NOT RUN with reason.

**Terminal:** MEDIA_FIDELITY_ACCEPTED.