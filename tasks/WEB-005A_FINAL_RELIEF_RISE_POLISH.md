# WEB-005A — Final relief-rise transition polish

**State:** CONTINUATION_AUTHORIZED / BOUNDED_POLISH  
**Parent:** WEB-005A / MER-107  
**Accepted final visual base:** `feat/web-005a-hero-visual-fidelity@e7098de8f05dfb3842620bbb578227d5c0bc2699`  
**Prior final visual review:** `1437fbb51263f4dfbdaadeb7d3f1d2820e50821e:tasks/WEB-005A_FINAL_PRODUCT_VISUAL_REVIEW_E7098DE.md`

## Decision

The final analytical handoff should preserve the earlier Preview Gate behavior in which DEM relief **rises into place progressively**. The current page handoff jumps from the held flat frame to a fully raised Terrain state, which makes the elevation model appear abruptly.

This is a bounded final-polish correction. It does **not** reopen the accepted 276-frame motion render or the Terrain -> THM-01 -> ALT-01 -> Priority semantics.

## Required behavior

After the motion video settles:

1. hold the accepted final camera/ground state;
2. animate the DEM relief from flat/near-flat to the accepted final 3x presentation relief over approximately **0.45–0.70 s** with eased interpolation;
3. the AOI frame/outline must rise with the same geometry so there is no detached-frame pop;
4. then continue the existing lossless Terrain -> THM-01 -> ALT-01 -> Priority reveal;
5. do not introduce a colorbar, legend, information card or layer label.

The relief-rise should feel like terrain physically resolving out of the Earth surface, not like a new rectangular panel appearing.

## Rendering boundary

A true 3D relief rise cannot be reconstructed faithfully from only the current flat held frame and the single fully raised Terrain PNG. CSS opacity/scale alone is not an acceptable substitute because it cannot interpolate the missing geometry.

However, **no full 276-frame production rerender is required**.

Implementation may render only the held-camera relief-rise interval from the already accepted deterministic production scene, using the existing DEM, camera, mapping and production-drape path. Preferred implementation is a short lossless transition sequence (for example 6–12 intermediate transparent/full-frame states) or an equivalent deterministic lossless micro-animation that preserves exact registration.

Do not change:
- motion choreography;
- camera/target geometry;
- 4K analytical source assets;
- DEM exaggeration target;
- layer palette/semantics;
- final Priority hold.

## Performance envelope

Keep the extra transition bounded:
- target duration: 0.45–0.70 s;
- avoid materially extending the overall hero;
- fetch transition assets only on the desktop motion/payoff path;
- reduced-motion/static paths may jump directly to the final raised Priority/static state.

## Evidence

Return:
- exact published HEAD;
- transition asset hashes and total incremental payload;
- one 1440x900 real-page playback proving: opening poster continuity, progressive relief rise, unchanged Terrain -> THM -> ALT -> Priority handoff;
- site/hero validator and negative-test results.

No merge, deploy or DNS action is authorized here.
