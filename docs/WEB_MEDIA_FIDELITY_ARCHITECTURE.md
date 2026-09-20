# WEB Media Fidelity Architecture

**State:** ACCEPTED PRODUCT/SOFTWARE ARCHITECTURE  
**Scope:** OrbGSS public marketing website and WEB-005B+ visual work  
**Production stack:** semantic HTML + CSS + vanilla JavaScript

## Decision

Visual fidelity is not coupled to a frontend framework. React, Vue or another application framework is not required to preserve image, map or video quality.

For the OrbGSS public marketing site, the accepted architecture remains semantic HTML + responsive CSS + progressive-enhancement vanilla JavaScript. This stack is sufficient for the current interaction envelope (hero playback, layer selector, compare slider, responsive image delivery and restrained motion) and minimizes runtime overhead.

Framework migration is not authorized solely for visual quality.

A future framework decision may be revisited only if product behavior materially expands into application-style state, authenticated workflows, client-side routing, complex shared interactive components or CMS/application requirements that justify it.

## Fidelity rules

### Scientific / analytical rasters
- Governed scientific masters remain immutable.
- Do not apply browser/CSS recolouring, contrast filters, blur, sharpening or semantic palette changes.
- Lossy delivery is permitted only where separately accepted and visually/semantically proven safe.
- Exact palette, mask/NoData and legend semantics must be preserved.
- Avoid browser upscaling beyond the accepted display density envelope.
- When a native analytical raster is 1200 px, target approximately 600 CSS px for 2x-density display unless a specifically validated larger derivative exists.
- Visual prominence should be achieved by layout, whitespace, framing and composition, not by arbitrary raster enlargement.

### Context / photographic imagery
- Keep a high-resolution master.
- Produce responsive 1x/2x delivery variants with `srcset`/`sizes`.
- Modern lossy codecs may be used when visually lossless at intended display size.
- Never force a low-resolution asset to fill a large desktop viewport.

### Hero video
- Maintain the approved visual master separately from web encodes.
- Web delivery should provide a modern WebM/AV1-or-VP9 path plus MP4/H.264 fallback where practical.
- Keep a high-quality poster and do not preload full video before first paint.
- Full-screen playback must not rely on a single low-resolution encode for all viewport/DPR combinations.
- If 4K/high-DPR desktop fidelity is a release requirement, provide a higher-resolution desktop encode (for example 2560-wide or 3840-wide, source permitting) and select variants based on viewport/DPR/data policy.
- Reduced-motion / reduced-data paths continue to use the poster or a lighter encode.

## Current WEB-005 observations

The current accepted site already uses several good fidelity controls:
- hero media has separate WebM and MP4 delivery;
- context imagery has responsive derivatives up to high-resolution desktop sizes;
- analytical output delivery is bounded by source/native dimensions rather than being treated as decorative texture;
- previous WEB-005B review already kept THM-01, ALT-01 and Priority lossless when lossy candidates failed fidelity/mask checks.

The main remaining risk is not the HTML/CSS/JS stack. It is accidental media upscaling or over-compression, especially for full-screen/high-DPR hero playback and large scientific figures.

## Quality gates

Before public launch, verify representative real-browser output at:
- desktop 1440 px DPR 1 and DPR 2;
- 1920-class desktop;
- at least one 4K/high-DPR desktop configuration;
- 1024, 768 and 375 mobile/tablet widths.

For each image/video surface inspect:
- selected source asset/encode;
- decoded dimensions versus rendered device-pixel dimensions;
- visible compression artefacts;
- colour/palette drift;
- NoData/mask edges;
- text/overlay readability;
- cropping and aspect ratio.

Scientific visuals fail the gate if interpretation can change due to delivery or rendering.

## Architecture boundary

Marketing-site visual fidelity and future analytical-application architecture are separate concerns.

Keep the public site lightweight and media-first. If OrbGSS later exposes a rich authenticated analytical application, choose its frontend framework based on application-state and product-engineering needs, not on image quality.
