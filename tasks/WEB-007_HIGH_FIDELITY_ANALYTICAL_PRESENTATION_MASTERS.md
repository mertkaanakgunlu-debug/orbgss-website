# WEB-007 — High-Fidelity Analytical Presentation Masters

**Linear:** MER-143  
**State:** READY_FOR_CTO_APPROVAL — DO NOT START  
**Start dependency:** WEB-006 / MER-95 terminal public-launch acceptance  
**Science authority:** MER-108 website/public-facing display derivative authority  
**Architecture:** HTML/CSS/vanilla JS remains unchanged

## Outcome

Materialize a production-quality public-web visual master family for Terrain, THM-01, ALT-01 and Priority from governed Kızıldere scalar masters. These are website presentation derivatives, not scientific/report exports.

## Required behavior

### Terrain
- preserve governed Terrain scalar master, normalization and accepted MER-108 palette;
- render Terrain/Elevation over a **neutral grayscale hillshade derived from the same governed DEM**;
- hillshade parameters are fixed and recorded for the entire public asset family;
- use constant analytical opacity within MER-108 bounds;
- canonical legend remains unblended;
- do not add a slope overlay under this task.

### THM-01 / ALT-01 / Priority
- regenerate display assets from governed scalar masters at production delivery dimensions;
- preserve exact accepted normalization, palette topology/stops, footprint, mask and NoData semantics;
- use mask-aware bilinear interpolation only where display-only upsampling/reprojection is required;
- use area/box for downsampling where appropriate;
- create larger public derivatives from the scalar master rather than enlarging a previously rendered low-resolution PNG;
- keep lossless delivery where visually-lossless lossy candidates do not pass fidelity/mask gates.

### Context ↔ Priority compare pair
If the final accepted homepage design contains the compare module:
- produce exactly aligned Context and Priority presentation assets;
- same crop/footprint/aspect ratio;
- no browser-side reprojection;
- Priority side uses the same governed derivative family as Act 04.

## Hard boundaries

Do not:
- use AI/generative super-resolution;
- blur, denoise, sharpen or apply unsharp-mask;
- use bicubic/spline/Lanczos on scientific scalar values;
- fill holes, inpaint, extrapolate or alter valid-data topology;
- apply CLAHE, histogram equalization, gamma/contrast/saturation/hue changes to analytical colours;
- alter scoring/feature semantics;
- add slope as decorative texture without a separate accepted Science decision.

## Provenance

Every asset family records:
- scalar/master source pointer;
- governing Science commit;
- normalization reference;
- palette ID/version;
- output dimensions;
- scalar/final resampler;
- mask mode;
- hillshade source + fixed parameters;
- analytical opacity;
- codec/encoder settings;
- checksum.

## Acceptance

- desktop/high-DPR derivatives are visually crisp at their intended device-pixel size;
- no browser upscaling of undersized analytical derivatives in the accepted design;
- palette/legend/mask/NoData comparisons remain conformant;
- Terrain relief is materially more legible through neutral hillshade without semantic change;
- deterministic rebuild matches checksums;
- no website derivative is used as a scientific input/report map.

**Terminal:** REVIEW_READY.