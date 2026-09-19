# WEB-005A — Final Product Visual Review at e7098de

**State:** ONE_BOUNDED_POLISH_REQUIRED / CONTINUATION_AUTHORIZED  
**Parent:** WEB-005A / MER-107  
**Reviewed branch HEAD:** `feat/web-005a-hero-visual-fidelity@e7098de8f05dfb3842620bbb578227d5c0bc2699`  
**Implementation/media HEAD:** `aed0597f961793f7a00d766673e7b9bc358df91a`  
**Evidence:** `tasks/WEB-005A_FINAL_PRODUCTION_EVIDENCE.md` plus real 1440x900 homepage playback capture reviewed by Product/CTO.

## Accepted final visual behavior

The final production implementation is accepted in substance and should not be re-choreographed:

- Earth establish -> satellite entry/settle -> reticle -> four-corner draw-on -> cyan fan -> left-to-right sweep -> retire -> approach is visually coherent;
- no stray black line/dark band remains in the reviewed homepage playback;
- four-corner acquisition and scan now tell the intended story clearly;
- satellite exit is subordinate, caption-safe and within the accepted no-fly-by envelope;
- copy-safe left / analytical-payoff right composition works at 1440-class desktop;
- Terrain -> THM-01 -> ALT-01 -> Priority occurs in order using the prepared governed 4K display assets;
- no hero colorbar, legend, info card, result card or per-layer label is present;
- final Priority hold is visually substantial and remains clear of the copy shade;
- analytical NoData/masked support reads through to authorized Terrain/context rather than false dark analytical fill;
- motion and analytical reveal timing are acceptable;
- the reproducible production pipeline, validators, audits, hashes and deterministic asset handoff are accepted as the continuing polish foundation.

Do not reopen these accepted decisions without a concrete regression.

## One remaining visual defect — startup poster continuity

The real 1440x900 homepage playback exposes a brief startup discontinuity: for approximately the first 0.3 seconds the current poster/held regional frame is visible before the video establishes the global Earth view.

This creates a visible reverse-story flash:
held/regional target -> Earth establish -> acquisition.

It is not a render defect and does not require another long production render, but it is not launch-quality.

### Required correction

Separate the **startup poster** from the **held/static payoff base**.

Required behavior:

1. Autoplay/motion startup poster must visually match the first Earth-establish frame (or an equivalent opening-frame still) so poster -> video is perceptually continuous.
2. Preserve the current held regional frame as a separate held/static base asset if it is still needed for reduced-motion, Save-Data, no-autoplay, stalled/fallback, or lossless analytical-overlay registration.
3. Static/fallback analytical states must continue to register against the held geometry; do not overlay the Priority/other drape states on the opening Earth poster.
4. Do not rerender the 276-frame production sequence. Derive/repackage the required still assets from existing accepted render frames.
5. Update manifest/checksums, validator invariants and fallback tests so startup-poster continuity and held-base registration cannot regress.

## Final evidence required

After this bounded fix, return only:

- exact new remote HEAD;
- startup poster and any separate held-base asset hashes;
- site + hero validators and negative-test results;
- one short 1440x900 real-page playback capture proving the opening no longer flashes the held target before Earth establish and that the final Terrain -> THM -> ALT -> Priority handoff is unchanged.

No new full production render, re-choreography, deploy, merge or DNS action is authorized by this decision.

**Continuation:** MER-107 remains In Progress until this one bounded visual polish is verified. After that, WEB-005A is eligible for terminal Product acceptance.
