# WEB Public Presentation Fidelity Policy

**State:** ACCEPTED PRODUCT/SOFTWARE AUTHORITY  
**Scope:** OrbGSS public marketing website, homepage analytical storytelling, future public visual surfaces  
**Consumes Science authority:** MER-108 website/public-facing display derivative authority @ `geothermal-prospectivity@11c32e8d2d072aa709262e513c8888e6a745bb76`

## 1. Product intent

The OrbGSS public website is a marketing/product presentation surface, not a scientific technical report or customer analytical deliverable.

The website should therefore optimize for:
- visual clarity;
- high perceived quality;
- spatial legibility;
- coherent palette continuity;
- engaging product storytelling;

while remaining truthful about what the imagery is and preserving the scientific master upstream.

The website may use polished **display derivatives** of pilot/development outputs. Those derivatives are presentation assets only and are not scientific masters, report cartography, validation evidence or quantitative exports.

## 2. Terminology and truthfulness

Do not describe the analytical visuals as "field data" unless a separate authority confirms that exact claim.

Preferred product framing:
- derived from real Earth-observation / geoscience source inputs;
- produced from the Kızıldere pilot/development workflow;
- rendered as public web presentation derivatives;
- not a field-validated technical map;
- not probability, reserve/resource estimation or drilling-success prediction.

The word "representative" may be used only to mean **representative presentation of pilot-derived outputs**, not fabricated or synthetic evidence.

## 3. Two visual classes

### A. Cinematic / contextual presentation media

Includes:
- approved hero animation;
- rendered orbital sequence;
- natural-colour context imagery;
- non-analytical geographic presentation media.

These may receive normal presentation-oriented media treatment where provenance/rights are preserved:
- high-quality web encoding;
- responsive derivatives;
- display scaling;
- cinematic compositing;
- non-semantic interpolation/upscaling where appropriate;
- tasteful denoising/encoding optimization where it does not falsely imply analytical precision.

Rendered/cinematic material must remain clearly distinguished from sensor imagery when relevant.

### B. Analytical evidence / result media

Includes:
- Terrain display derivative;
- THM-01;
- ALT-01;
- Priority/result surface.

These remain governed by MER-108.

For public-web presentation, maximize quality within that authority:
- preserve accepted normalization;
- preserve accepted MER-108 palette topology/stops;
- preserve mask/NoData semantics;
- use the same display family across hero/evidence/result;
- use allowed mask-aware bilinear interpolation for display-only scalar upsampling/reprojection;
- use allowed area/box downsampling;
- use neutral hillshade/context blending where beneficial, with fixed parameters and permitted opacity;
- use visually-lossless delivery only when proven safe;
- otherwise keep lossless assets.

Do **not** use:
- AI/generative super-resolution on analytical content;
- Gaussian blur / denoising / sharpening / unsharp mask;
- bicubic/spline/Lanczos on scalar values;
- histogram equalization / CLAHE;
- gamma/contrast/saturation/hue changes to analytical colours;
- local tone mapping;
- hotspot enhancement;
- inpainting / hole filling / extrapolation;
- any manipulation that alters analytical interpretation.

Final RGBA Lanczos3 remains allowed only for downsampling as already authorized by Science.

## 4. Visual-quality strategy

The website should not force scientific rasters to look like raw report exports.

Public quality should instead come from:
- governed palette continuity;
- high-resolution presentation derivatives where source density permits;
- mask-aware bilinear display interpolation;
- neutral terrain/context compositing;
- premium framing;
- generous whitespace;
- careful scale;
- responsive delivery;
- exact legend treatment;
- strong hierarchy and interaction.

Do not manufacture apparent resolution that the scientific source does not contain.

For large/high-DPR screens, prefer generating a larger conformant display derivative from the governed scalar master using the allowed display pipeline rather than upscaling an already-rendered low-resolution PNG.

## 5. Pilot disclosure

Homepage Evidence / Result surfaces should carry one concise disclosure, visually subordinate to the imagery.

Product-approved structural meaning:
> Pilot presentation derivative. Derived from real Earth-observation/geoscience source inputs and resampled/composited for web presentation. Scientific masters remain unchanged; not a field-validated technical map.

Final wording is owned by the website content domain and may be shortened, but it must preserve:
- pilot/development status;
- source-derived nature;
- presentation-derivative status;
- unchanged scientific master;
- non-technical-report / non-field-validation boundary.

Do not claim "interpolated field data".

## 6. Palette continuity

The public analytical story should use the accepted MER-108 display family consistently across:
- hero analytical payoff;
- Act 03 evidence layers;
- Act 04 Priority result;
- any Context ↔ Priority compare module where the analytical side is shown.

The compare module must use the exact same governed Priority display derivative family as Act 04.

## 7. Acceptance principle

For public-web analytical media, visual appeal is an explicit Product objective, but it is achieved only inside the accepted Science display envelope.

The acceptance question is therefore not "does this look like raw report cartography?" but:
- does it look premium and legible;
- does it preserve governed analytical meaning;
- is the display transformation documented and reproducible;
- is the presentation boundary disclosed honestly?

No React/framework migration is required.

**Current decision:** maximize visual quality within MER-108; do not reopen Science unless a desired enhancement exceeds the accepted display-derivative envelope.
