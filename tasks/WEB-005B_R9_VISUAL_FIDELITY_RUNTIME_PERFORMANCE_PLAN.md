# WEB-005B R9 — Visual Fidelity and Runtime Performance Plan

**State:** ACCEPTED PRODUCT/SOFTWARE AUTHORITY  
**Parent:** MER-109 / WEB-005B  
**Consumes Science authority:** MER-108 website/public-facing display derivative authority @ `geothermal-prospectivity@11c32e8d2d072aa709262e513c8888e6a745bb76`

## 1. Architecture remains unchanged

The public website remains semantic HTML + CSS + progressive-enhancement vanilla JavaScript.

No React/framework migration is authorized or required for visual fidelity, media quality, page transitions, layer switching or compare interactions.

## 2. Terrain presentation

For the public website, Terrain/Elevation should not be shown as a visually weak raw elevation export when a conformant display derivative can communicate topography more clearly.

Within current MER-108 authority:

- keep the governed Terrain/elevation scalar master and accepted normalization/palette unchanged;
- permit mask-aware bilinear display interpolation where enlargement/reprojection is needed;
- permit a neutral grayscale hillshade derived from the governed Terrain/elevation master underneath the analytical colour layer;
- use fixed hillshade parameters for the asset family and record them in provenance;
- use constant analytical opacity within the MER-108 range;
- keep the legend swatches canonical/unblended.

A separate semi-transparent **slope** overlay is NOT currently assumed equivalent to hillshade and is not authorized by Product as a presentation context layer under MER-108. Slope is a derived geoscience layer with its own spatial meaning. Do not add it merely as visual texture without an explicit Science decision.

Product preference for WEB-005B is therefore:
**Elevation/Terrain palette + neutral hillshade**, not Elevation + slope + hillshade.

This achieves stronger relief perception without introducing another analytical layer into the visual.

## 3. Analytical interpolation boundary

For Terrain, THM-01, ALT-01 and Priority:

Allowed:
- mask-aware bilinear interpolation for display-only scalar upsampling/reprojection;
- area/box downsampling;
- approved neutral hillshade/context compositing;
- final RGBA downsampling under MER-108 rules;
- larger presentation derivatives regenerated from governed scalar masters.

Not allowed:
- AI/generative super-resolution;
- blur/denoise/sharpen/unsharp mask;
- bicubic/spline/Lanczos on scalar values;
- hole filling/inpainting/extrapolation;
- contrast/gamma/saturation/hue manipulation of analytical colours;
- any step that invents or strengthens analytical structure.

Public-web quality comes from a better display derivative, not fabricated spatial detail.

## 4. Cinematic hero quality

The cinematic hero is a separate presentation-media class.

Product objective:
**use the highest perceptual quality that remains smooth on the target device/network.**

Maintain:
- approved visual master separately from delivery encodes;
- high-quality poster frame;
- WebM and MP4 fallback paths;
- no hero rerender or choreography change under WEB-005B.

Before public launch, produce/select delivery variants based on the actual accepted master:
- baseline desktop encode;
- higher-resolution/high-bitrate desktop encode for large/high-DPR displays if source quality warrants it;
- lighter mobile/low-bandwidth encode where needed.

Do not force every client to download the largest encode.

Selection should happen before playback using viewport/DPR and, where safely available, reduced-data/network hints. Once playback starts, do not swap sources merely because the viewport changes.

## 5. Hero loading behavior

Required behavior:
- render a high-quality poster immediately;
- do not block first contentful paint on the full video;
- load/decode the chosen hero video without stalling initial page rendering;
- use muted, playsinline playback;
- preserve the accepted reduced-motion path;
- when video cannot start promptly, keep the poster visually complete rather than showing a blank/black state.

Avoid eager loading of post-hero analytical media that is below the fold.

## 6. Image/media delivery

### Context / photographic imagery
- maintain high-resolution masters;
- generate responsive width/DPR derivatives;
- use `srcset` / `sizes`;
- prefer modern visually-lossless web encodes;
- lazy-load below-the-fold media;
- never upscale a low-resolution derivative to fill a large desktop surface.

### Analytical imagery
- regenerate larger conformant web derivatives from governed scalar masters when more display pixels are needed;
- do not enlarge an already-rendered small PNG and call it higher resolution;
- keep THM/ALT/Priority lossless where visually-lossless lossy encoding fails fidelity/mask checks;
- preserve palette/legend/mask semantics.

## 7. Interaction and animation performance

Act 03 layer switching:
- prefetch/decode only the small set of next-likely analytical states;
- crossfade opacity/transform only;
- avoid layout-triggering animation;
- no canvas/WebGL requirement.

Context ↔ Priority compare:
- use two already-decoded aligned images;
- move only the clipping boundary/handle;
- do not continuously recompute/reproject raster data in the browser.

Page motion:
- prefer compositor-friendly opacity/transform transitions;
- avoid scroll handlers that perform per-frame layout reads/writes;
- respect `prefers-reduced-motion`.

## 8. Page/navigation smoothness

Because the public site is static/multi-page, page navigation quality should come from low page weight, cached shared assets and restrained transitions rather than framework client-side routing.

Allowed enhancements:
- prefetch likely internal navigation targets when idle/appropriate;
- long-cache immutable hashed media/assets;
- keep shared CSS/JS small and cacheable;
- use browser-native view transitions only as progressive enhancement if supported and if they do not delay navigation.

Navigation must remain correct with JavaScript disabled.

## 9. Performance acceptance gates

Before public launch, validate on representative real devices/browsers, not only screenshots.

Required viewport classes:
- 375 mobile;
- 768 tablet;
- 1024;
- 1440 desktop;
- 1920-class desktop;
- 4K/high-DPR desktop where available.

Required checks:
- no visible hero playback stutter after steady-state playback begins;
- no blank hero while media initializes;
- no accidental analytical upscaling beyond the accepted density envelope;
- no layer-switch jank;
- no compare-slider jank;
- no layout shift caused by late image dimensions;
- no scientific palette/mask drift;
- no unnecessary eager loading of below-fold high-resolution imagery.

Use measured browser evidence (selected source, decoded dimensions, rendered device-pixel dimensions, transfer bytes, playback/drop-frame evidence where available) rather than assuming quality from file size alone.

## 10. Product priority order

When quality and performance conflict, optimize in this order:

1. preserve truthful analytical meaning;
2. preserve perceptual visual quality of the focal media;
3. preserve smooth interaction/playback;
4. reduce transfer/decode cost through responsive delivery;
5. only then reduce asset fidelity.

Do not solve performance problems by visibly degrading the focal scientific maps or accepted hero when a better responsive-delivery strategy exists.

**Current state:** ready to be consumed by the final WEB-005B design/implementation contract.
