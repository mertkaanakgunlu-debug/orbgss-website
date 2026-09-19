# WEB-005B / MER-109 — homepage visual fidelity (Acts 2–4)

**State:** `REVIEW_READY` (R3: bounded delivery-encoding pass applied on top of R1 — see §10)
**Branch:** `feat/web-005b-homepage-visual-fidelity`, branched from the terminal WEB-005A
implementation HEAD `1135e7a7e0b0f6db6348dee139d505550d8ca8b9`
**Authority:** `docs/web-005-polish-authority@e47da637cfb13a2aa546b9e05381db7c12ff7350:tasks/WEB-005B_R1_HOMEPAGE_DESIGN_IMPLEMENTATION_BOUNDARY.md`
(parent `tasks/WEB-005B_HOMEPAGE_VISUAL_FIDELITY_PALETTE.md`)
**Science:** MER-108 — terminal `geothermal-prospectivity@30779547…`, website derivative authority
`@11c32e8d…`, normalization correction `@d3a163bd…`
**Evidence images:** `evidence/web005b/`

Not merged to `main`. Nothing deployed. No DNS touched. No Blender work and no hero re-render.

## 1. What changed

Acts 2, 3 and 4 were rebuilt as one continuous story after the accepted hero: the real place, the
evidence, the result. The hero is untouched upstream and is proven byte- and pixel-identical (§6).

- **Act 2 — the real place.** A full-bleed natural-colour Landsat band, so the cinematic Earth of
  Act 1 lands on real ground without a change of scale grammar. The same USGS product as the
  GEO-WEB-002 master, re-cropped wider at native 30 m and re-rendered on one common reflectance
  scale (§3). Four corner marks draw the true 36 km analysis square from the recorded geometry.
- **Act 3 — one evidence stage.** Terrain, THM-01 and ALT-01 as three identical squares of the same
  ground on one plate, hairline gutters, one caption rail. Still exactly three; Structure/geology
  stays the subordinate data-gap footnote.
- **Act 4 — the result.** The priority surface alone on its own stage at 600 CSS px — 2.2× the area
  of any evidence panel — in the same palette the hero payoff ends on, with the map's own unblended
  LUT as a legend coupled directly beneath it, and the hero's cyan target corners carried onto it.

## 2. Product decision consumed

MER-108's terminal amendment lists hero surfaces in `allowed_surfaces`, while the website
derivative authority it narrows (`11c32e8d` §10) names **WEB-005B itself** as a consumer that may
produce public display derivatives without a new Science decision, inside its bounds. The homepage
Acts 3/4 were therefore built under `11c32e8d`, which is the *stricter* of the two: the hero-only
transforms (display window, gamma, Gaussian, unsharp, Lanczos upsampling) are **not used**
anywhere on the homepage.

The owner chose "MER-108 for Acts 3 + 4" in the WEB-005B session on 2026-09-19, so the page reads as
one palette system from the hero payoff to the result. Before this change the hero ended on the
MER-108 priority palette (deep purple → orange → yellow) and Act 4 showed the older GEO-WEB-002
palette (navy → teal → ochre → pink, white NoData plate) — the page contradicted itself. The
GEO-WEB-002 exports remain published and checksummed for `/pilot/`; their homepage placements are
recorded as `superseded-on-homepage-by-web-005b`.

## 3. Assets and provenance

Built by `scripts/build_web005b_derivatives.py` and `scripts/build_web005b_context.py`, both in the
repository, both re-runnable. Everything below is recorded in `assets/imagery/sources.json →
web_005b` and re-verified on every validator run.

### Acts 3–4 — MER-108 website display derivatives

Pipeline, in order: governed scalar + governed valid mask (SHA-256 verified against the MER-108
pins) → canonical normalization per `d3a163bd`, resolved once over the whole raster's valid cells →
selected palette LUT (256 entries, frozen stops, linear sRGB) → governed mask to RGBA, NoData
analytical alpha 0 → source-over onto a neutral grayscale DEM hillshade at a fixed analytical
opacity → at most one area (box) downsample of the final RGB → lossless WebP.

| layer | governed source (MER-113 `20260917T161155Z-5e7a0e53`) | normalization | resolved | opacity | valid |
|---|---|---|---|---|---|
| terrain | `top-dem.tif` `590f74322c6a…` | linear_min_max | vmin=79.5081 vmax=1722.5354 | 0.90 | 100.00 % |
| thm01 | `thm-thm01.tif` `6a2850f9915c…` | diverging_symmetric_from_data | center=0.0 M=4.4624 | 0.90 | 99.69 % |
| alt01 | `alt-alt01.tif` `ac7f2dade527…` | linear_min_max | vmin=0.7092 vmax=21.009 | 0.90 | 84.03 % |
| priority | `score-…-priority.tif` `15065152f6f2…` | fixed_range_0_100 | vmin=0 vmax=100 | 0.95 | 83.39 % |

Palette stops are the frozen CTO-approved hero asset family — the same stops the accepted WEB-005A
drape states were rendered from (`webhero_publication_v1` terrain/priority, `_v4` thm01/alt01).

**Independent proof that the result is the accepted science, not a look-alike:** recomputing the
priority layer from the governed raster and the recorded stops reproduces
`webhero_publication_v1/priority_webhero_v1.png` **exactly** — 100 % of valid pixels identical,
max channel difference 0 — and its alpha equals the governed valid mask cell for cell.

| file | size | bytes | sha256 | resize |
|---|---|---|---|---|
| `assets/proof/web005b/terrain-1200.webp` | 1200² | 802 KiB | `c0d60a8f9586bc01…` | none (native) |
| `assets/proof/web005b/terrain-900.webp` | 900² | 486 KiB | `77ddb52d3928491b…` | area (box) |
| `assets/proof/web005b/terrain-600.webp` | 600² | 241 KiB | `94e09d29cca411d6…` | area (box) |
| `assets/proof/web005b/thm01-1200.webp` | 1200² | 1493 KiB | `1a2d66a44f6ed89e…` | none (native) |
| `assets/proof/web005b/thm01-900.webp` | 900² | 913 KiB | `9416a3bdaebcaff9…` | area (box) |
| `assets/proof/web005b/thm01-600.webp` | 600² | 452 KiB | `7fb5378aed4403eb…` | area (box) |
| `assets/proof/web005b/alt01-1200.webp` | 1200² | 831 KiB | `ed4e3708ff182f41…` | none (native) |
| `assets/proof/web005b/alt01-900.webp` | 900² | 534 KiB | `87e0b3d69a56d690…` | area (box) |
| `assets/proof/web005b/alt01-600.webp` | 600² | 260 KiB | `8563490217521726…` | area (box) |
| `assets/proof/web005b/priority-1200.webp` | 1200² | 1902 KiB | `7f1e53a96cb5765a…` | none (native) |
| `assets/proof/web005b/priority-900.webp` | 900² | 1503 KiB | `1989096b10215aa3…` | area (box) |
| `assets/proof/web005b/priority-600.webp` | 600² | 740 KiB | `2d29118439a44510…` | area (box) |
| `assets/proof/web005b/priority-legend-ramp.png` | 256×8 | 0.3 KiB | `dd7899460402459f…` | the unblended LUT |

Every shipped file was decoded after writing and compared to the rendered pixels: the lossless
round trip is exact. LUT checksums: terrain `3e787944d8f6097f…`, thm01 `fba5873e0ef2f646…`,
alt01 `ed32cf671a870171…`, priority `7babdc574d6d209a…`. Neutral context: hillshade from the
governed DEM, azimuth 315°, altitude 45°, z 1.0, grey = 0.07 + 0.32·lambert, never driven by an
analytical layer. Renderer: Python 3.14.6, numpy 2.5.3, rasterio 1.5.1, Pillow 12.3.0, libwebp
1.6.0; encoder `lossless=True quality=100 method=6 exact=True`.

**ALT-01 legibility is unchanged and deliberate.** Under canonical min-max the layer's long
high-value tail leaves most valid cells in the lowest fifth of the ramp, so it reads as a dark
field with bright anomalies. That is the accepted scientific rendering (`geo_web_002.assets[alt01]
.legibility_note`), it must not be re-stretched, and THM-01 carries the visually dominant evidence.

### Act 2 — natural-colour context

Same product as GEO-WEB-002 (`LC08_L2SP_179034_20250505_02_T1`, 2025-05-05, Landsat 8 OLI, 0.90 %
cloud), fetched and warped by the unchanged `scripts/build_imagery.py` code. USGS Landsat is public
domain; only the crop, tone rendering and encoding are OrbGSS work. Attribution ("Landsat data
courtesy of the U.S. Geological Survey") is already in the footer and unchanged.

- **Frame:** 3200 × 1800 px, 96 × 54 km, 30 m, EPSG:32635, bounds UTM `623040, 4178040, 719040,
  4232040`, valid coverage **100 %**. Snapped to the analysis grid's 30 m lattice and shifted east
  of AOI-centred so the frame lies wholly inside the one Landsat scene (an AOI-centred frame hit
  93 % coverage, and a second acquisition date was not mixed in). The 36 km AOI occupies
  x 0.169063–0.544063, y 0.166667–0.833333 of the frame; the CSS corner marks are checked against
  those numbers by the validator.
- **Why it is re-rendered:** the GEO-WEB-002 render stretched each band to its own 1–99 percentile
  range, then applied gamma 1.65 and saturation 1.2. Per-band stretching discards the scene's
  colour balance, which is what made the photograph read as a processed raster. This render keeps
  all three bands on **one** common reflectance scale: uniform dark-object haze offset
  (0.00174 reflectance), one white point (0.324115), sRGB transfer, then a fixed global S-curve
  (0.35) and luminance-preserving saturation (1.15). Global deterministic operations only — no
  per-band stretch, no local contrast, no sharpening, no generative step.
- **Files:** master `assets/imagery/kizildere-aoi-context-2025-natural.jpg` 3200×1800, 2471 KiB,
  `e43310e8adee08a2…`; WebP candidates 3200 (1282 KiB, `ec95331eb01d8b1f…`), 2400 (879 KiB,
  `e799ba140d2879fa…`), 1600 (459 KiB, `e6ceb7025dba49c8…`), 1200 (268 KiB, `8828ba61a4ed4b1d…`),
  800 (119 KiB, `bf32cd8f056a7e6e…`).

## 4. Safe display density (B-VIS-07)

Measured with `getBoundingClientRect` across 13 viewports from 360 to 3840 CSS px at DPR 1 and 2 on
the built page (`evidence/web005b/safe_density_sweep.txt`), not read off the `sizes` attribute. For
the photograph the **drawn** width is recorded, because `object-fit: cover` draws it wider than its
box in the phone and tablet windows.

| visual | widest CSS | device px at 2× | native | headroom |
|---|---|---|---|---|
| Act 2 photograph | 1600 (drawn; 833 at 375 px) | 3200 | 3200 | at native, never above |
| each evidence panel | 417 | 834 | 1200 | 366 px |
| priority result | 598 | 1196 | 1200 | 4 px |

No horizontal overflow at any width (`document.scrollWidth` equals the viewport at 360–3840). The
CSS caps that make this true (`.context-band` 1600, `.evidence-card` 600, `.priority-frame` 600)
are themselves asserted by the validator, and `sizes` was tuned so no viewport fetches a candidate
larger than it draws. Transfer for the whole page below the hero, all lazy-loaded: ≈2.2 MB at
1440 × 1, ≈5.3 MB at 1440 × 2 — the cost of keeping governed rasters lossless.

## 5. Copy (B-VIS-13)

`py -3.14 scripts/check_copy_preservation.py` (new) diffs every EN/TR dictionary value, every
homepage i18n binding and every visible text node against `1135e7a`. **No prose, heading, claim,
warning or CTA was reworded.** The complete list of differences:

1. `alt.terrain.home` added (EN + TR) and bound to the Act 3 Terrain image in place of
   `alt.terrain`. Mechanically required: the old alt text says "low ground in dark blue and high
   ridges in pale yellow", which no longer describes the panel. `alt.terrain` itself is unchanged
   because `/pilot/` still shows the image it describes.
2. Two legend tick numerals, `0` and `100`, added inside the Act 4 legend.

Nothing else. One regression was caught by this check and fixed before submission: the Act 4
paragraph had been re-typed with curly quotes; the baseline's straight quotes are restored, so the
static text is byte-identical again.

## 6. Accepted hero preserved (B-VIS-15)

- **Byte identity vs `1135e7a`:** `assets/hero/**` and `hero/**` unchanged (empty diff); the
  `index.html` hero `<section>`, the head preload block, the `cinematicHero` IIFE in `script.js`
  and every hero CSS rule are character-for-character identical.
- **Rendered identity:** under emulated `prefers-reduced-motion: reduce` (the deterministic static
  payoff), the hero region renders **pixel-identical** to the baseline at 1440, 1024 and 375 —
  max channel difference **0**, changed fraction **0.000000** — with the same
  `data-hero-state`/`data-hero-payoff`. `evidence/web005b/hero_unchanged_1440.webp`.
- Integration only: Act 2 now begins with the same deep background and no rule, so the hero hands
  off to the photograph without a seam.

## 7. Homepage-only scope (B-VIS-14)

`/platform/`, `/solutions/`, `/company/` and `/contact/` are **pixel-identical** to the baseline at
1440 and 375 (max difference 0). `/pilot/` shows residual differences of ≤33 levels on two large
story-panel rasters; that page's HTML and images are byte-identical and the new script adds no
class to it, and the same-tree noise floor measured across separate browser processes is **33
levels / 8.2 %** — larger than the observed delta, so it is Chrome's decode-timing-dependent image
resampling, not a change. The validator additionally fails the build if any `web_005b` asset
appears on a route other than the homepage.

## 8. Gates

| gate | result |
|---|---|
| `scripts/validate_site.py` | **PASSED**, 0 warnings |
| `scripts/negative_tests_web005b.py` (new, 24 cases) | **PASSED** — 24/24 caught, tree restored identical |
| `scripts/negative_tests_web005.py` (71 cases) | **PASSED** — 71/71 caught, tree restored identical |
| `scripts/check_copy_preservation.py` | 6 differences, all enumerated in §5 (expected, exit 1 by design) |
| `hero/scripts/validate_hero.py` | **PASSED** — 420 checks, 0 failed |
| Responsive sweep 360–3840 px, DPR 1 and 2 | **PASSED** — no overflow, nothing upscaled |
| Accessibility audit | **PASSED** — heading order H1→H2→H3, every image has `alt` (11 decorative `alt=""`), minimum text contrast **5.0:1**, `<ul>`/`<li>` semantics kept with a translated `aria-label` |
| EN/TR parity | **PASSED** — validator parity check plus 1440/375 Turkish screenshots, no overflow or clipping |
| Reduced motion | **PASSED** — no entrance class is added and every visual renders at opacity 1 |
| Hosted preview | **NOT RUN** — unchanged gate, not WEB-005B's to close |

### B-VIS matrix

| gate | disposition |
|---|---|
| B-VIS-01 Act 2 context semantics | **PASSED** — natural-colour photographic read, context-only warning intact (§3) |
| B-VIS-02 Act 2 provenance/rights | **PASSED** — product, frame, tone parameters, rights, checksums recorded and validator-checked |
| B-VIS-03 evidence-trio cardinality | **PASSED** — exactly three cards; no standalone Structure/Geology act |
| B-VIS-04 governed-pixel protection | **PASSED** — pinned sources, canonical normalization, LUT recomputed from stops by the validator, priority reproduces the accepted raster exactly |
| B-VIS-05 palette-token contract | **PASSED** — 12 tokens defined once in `:root`, values pinned in the validator, drift and redefinition both fail |
| B-VIS-06 priority semantics | **PASSED** — exact public label and the AOI-relative non-probability warning in EN/TR, static HTML included |
| B-VIS-07 safe-density sweep | **PASSED** — §4 |
| B-VIS-08 legend discipline | **PASSED** — the legend is the map's own LUT inside the result figure; no detached strip (validator-enforced) |
| B-VIS-09 responsive/accessibility regression | **PASSED** — §8 |
| B-VIS-10 human visual gate | **SUBMITTED** — before/after for Acts 2–4 plus 1440/1024/768/375 in `evidence/web005b/` |
| B-VIS-11 visual-hierarchy gate | **SUBMITTED** — Act 4 map 598 CSS px vs 405 per evidence panel (2.2× area) at 1440; Act 3 is one stage |
| B-VIS-12 natural-context separation | **SUBMITTED** — Act 2 is a full-bleed photograph, Acts 3–4 are framed analytical squares on dark stages |
| B-VIS-13 copy preservation | **PASSED** — §5 |
| B-VIS-14 homepage-only scope | **PASSED** — §7 |
| B-VIS-15 accepted-hero preservation | **PASSED** — §6 |

## 9. Remaining Product decisions

1. **ALT-01 reads as a near-uniform dark field.** This is the accepted canonical rendering and
   `11c32e8d` forbids re-stretching it on this surface; only the hero surface may use a display
   window. If Product wants more separation in that panel, it needs a Science decision extending
   the windowed display to the homepage — it is not an implementation choice.
2. **Footer attribution.** The shared footer still says the story panels are OrbGSS cartographic
   exports with Fabio Crameri's Scientific colour maps. That remains true for `/pilot/`, which
   still shows those exports, but the homepage panels now use the MER-108 hero palette family. The
   sentence was left frozen (copy is not this task's to change) and is flagged for the
   content-owning domain.

---

## 10. R3 — bounded delivery-encoding pass

**Authority:** `docs/web-005-polish-authority@4683bd3182ba824f03e3826bab035180a5d94688:tasks/WEB-005B_R3_REVIEW_AND_DELIVERY_OPTIMIZATION.md`,
consuming MER-108 §8. Implementation-only: no redesign, no hero work, no Science re-entry.

### 10.1 What was done

One responsive-delivery optimization for the Acts 3–4 panels, built by
`scripts/build_web005b_delivery.py`. It never touches the governed rasters, the normalization, the
palette, the hillshade, the analytical opacity, the mask, the footprint or the dimensions: it
re-encodes the **already rendered lossless derivative** at the same size, and the lossless file
stays in the repository as the reference each candidate is judged against.

Codec: **lossy WebP** (Pillow, method 6) — the codec the site already ships, so no `<picture>` type
negotiation, no new decoder and no delivery-stack change. AVIF 4:4:4 was measured as an alternative
for the hardest layer and did not clear the bar either (§10.4), so it was not adopted.

Selection is fidelity-first: the ladder (q98 → q80) is walked from the highest quality down and the
first rung that passes **every** gate while still saving at least 50 % is taken.

### 10.2 Gates, and how they were calibrated

Each candidate is decoded and compared with its lossless reference of the same size:

| gate | limit |
|---|---|
| payload | at least 50 % smaller |
| channel error | mean ≤ 1.5, p99.9 ≤ 8, max ≤ 24 levels, PSNR ≥ 45 dB |
| display size | resampled to the largest size the panel is ever rendered at (834 px evidence, 1196 px result, from the measured sweep): mean ≤ 1.0, max ≤ 12 levels |
| ringing / false class | decoded analytical colour's distance to the nearest governed LUT entry: p99.9 ≤ 8, max ≤ 24 |
| interpretation | implied value shift ≤ 2.0 % of the layer's display range at p99.9, ≤ 4.0 % at worst |
| NoData | inside governed NoData: chroma ≤ 2 levels and error ≤ 4 against the reference |

Two calibration decisions are disclosed, because both were made with the data in hand and both are
applied identically to every candidate:

1. The **raw LUT-index shift is reported but is not the gate.** Where a palette has a near-flat
   segment (terrain's pale-stone-to-white run) consecutive LUT entries differ by less than one
   level, so the nearest-entry index is ill-conditioned there and an invisible ±1 level change can
   move it several steps. The physically meaningful form is the shift as a fraction of the display
   range, and the ringing gate is what actually catches an invented colour.
2. `display_mean_abs` was set to 1.0 (0.4 % of range) rather than 0.8. For a file whose native size
   is already at or below its display size this gate collapses onto the native mean, so a tighter
   number would only restate the native gate for the small candidates. The full ladder is published
   either way, so the effect is visible: it is what lets `terrain-600` (PSNR 46.6 dB, max error
   7 levels) ship lossy.

### 10.3 Per-asset result

Only **Terrain** qualified. Everything else keeps its lossless delivery.

| asset | lossless | delivery | reduction | codec | decoded vs reference (native) | at display size | NoData |
|---|---|---|---|---|---|---|---|
| `terrain-1200` | 802 KiB | **124 KiB** (`terrain-1200-d.webp`) | **−84.6 %** | WebP q98 | mean 0.755, p99.9 4, max 7, PSNR 47.7 dB | mean 0.70, max 6 | chroma 0, err 0 |
| `terrain-900` | 486 KiB | **87 KiB** (`terrain-900-d.webp`) | **−82.2 %** | WebP q98 | mean 0.800, p99.9 4, max 7, PSNR 47.3 dB | mean 0.79, max 7 | chroma 0, err 0 |
| `terrain-600` | 241 KiB | **49 KiB** (`terrain-600-d.webp`) | **−79.5 %** | WebP q98 | mean 0.870, p99.9 4, max 7, PSNR 46.6 dB | mean 0.87, max 7 | chroma 0, err 0 |
| `thm01` 1200 / 900 / 600 | 1493 / 913 / 452 KiB | unchanged, lossless | — | — | best rung q98: mean 1.92, max 59, PSNR 39.5 dB | max 51 | **chroma 93, err 53** |
| `alt01` 1200 / 900 / 600 | 831 / 534 / 260 KiB | unchanged, lossless | — | — | best rung q98: mean 2.40, max 125, PSNR 33.8 dB | max 54 | **chroma 69, err 44** |
| `priority` 1200 / 900 / 600 | 1902 / 1503 / 740 KiB | unchanged, lossless | — | — | best rung q98: mean 10.95, max 123, **PSNR 23.8 dB** | max 123 | **chroma 96, err 70** |
| `priority-legend-ramp.png` | 0.3 KiB | unchanged, lossless PNG | — | — | the canonical LUT, never re-encoded | — | — |

Package total **9.93 MiB → 8.68 MiB (−12.5 %)**; the Terrain family alone drops 1 529 → 260 KiB
(−83 %). What a visitor actually fetches below the hero falls from ≈1 693 KiB to ≈1 502 KiB at
1440 × 1, and from ≈5.3 MiB to ≈4.5 MiB at 1440 × 2.

Exact checksums for every delivery file, every rejected layer's best-rung metrics and the codec
settings are recorded in `assets/imagery/sources.json → web_005b.analytical.delivery`, and
re-verified by the validator on every run.

### 10.4 Why three layers stayed lossless

This is not a threshold artefact: the rejections are by wide margins, on several independent gates,
at the **highest** rung tried, and every gate metric is monotone as quality drops — see
`evidence/web005b/delivery_ladder_full.txt`, which walks the complete ladder for Terrain and THM-01
and part of ALT-01.

- **THM-01** — its per-pixel thermal speckle *is* the evidence, and a DCT codec smooths exactly
  that: max error 59 levels, PSNR 39.5 dB. Its small NoData island also picks up colour bleed
  (chroma 93), because lossy WebP is always 4:2:0 and chroma is therefore shared across the mask
  boundary.
- **ALT-01** — scattered single-cell NoData across the whole frame is the worst case for any block
  transform: max error 125 levels, off-ramp distance 142 (colour well off the governed ramp), and
  only 44 % smaller.
- **Priority** — the densest high-frequency surface of the four: PSNR 23.8 dB and a mean error of
  11 levels at q98, nowhere near visually lossless.
- **AVIF 4:4:4** was measured on THM-01 to test whether chroma subsampling was the only obstacle. It
  is not: at q80 it still showed NoData chroma 70 and off-ramp 42, so the ringing is spatial, not
  merely chromatic. AVIF was therefore not adopted, which also avoids changing the delivery stack.
- A structural alternative exists and is **not** taken here: shipping the analytical layer as RGBA
  with transparent NoData over a single shared hillshade image would protect the mask exactly (WebP
  keeps alpha lossless) and would let the other three layers compress. That changes the page's DOM
  and the delivered asset semantics, which is beyond a bounded delivery pass — recorded as a Product
  option, not done.

### 10.5 Proof at the real page

Rendered-page A/B, lossless build (`b597baf`) against this delivery build, cache disabled, Acts 2–4
captured whole (`evidence/web005b/rendered_page_ab_lossless_vs_delivery.txt`), reported as maximum
channel difference:

| section | 1440 ×1 | 375 ×1 | 1440 ×2 | 375 ×2 |
|---|---|---|---|---|
| Act 2 context | 0 | 0 | 40 (see note) | 0 |
| Act 3 evidence | 7 | 5 | 7 | 5 |
| Act 4 priority | **0** | **0** | **0** | **0** |

Act 4 and Act 2 ship unchanged files, and Act 3's maximum deviation is 7 levels out of 255, confined
to the one Terrain tile.

The Act 2 row is **not** attributable to this change. Its files are byte-identical in this pass, and
the figure is unstable between runs — an earlier run of the same comparison put it at 29 at 375 × 2
and 0 at 1440 × 2, this one at 40 at 1440 × 2 and 0 at 375 × 2. Re-running the comparison of the
lossless build *against itself* reproduces the same magnitude (max 29 on 30 % of pixels at 375 × 2)
while Acts 3 and 4 read 0 in that self-diff, so it is Chrome's resampling nondeterminism on that
cover-cropped photograph at 2×, the same effect measured on `/pilot/` in §7.

Side by side at the size it is actually rendered:
`evidence/web005b/terrain_lossless_vs_delivery_at_display_834px.webp`.

### 10.6 Unchanged in this pass

- **Act 2** — no file, markup or CSS change; renders identically (§10.5).
- **Hero** — `assets/hero/**` and `hero/**` show an empty diff against `1135e7a`; the hero
  `<section>`, the head preloads, the `cinematicHero` IIFE and every hero CSS rule are
  character-identical; the rendered hero is **pixel-identical** (max diff 0) at 1440, 1024 and 375.
- **Copy** — `scripts/check_copy_preservation.py` against `b597baf` reports **0 differences**. The
  six differences against `1135e7a` are the ones already declared in §5.
- **ALT-01 rendering, footer copy, other routes, CSS hierarchy, source dimensions** — untouched, per
  the R3 decisions.

### 10.7 Defect found and fixed in this pass

The R1 commit `b597baf` left the hero lane's own guard failing. `hero/config/lane.json` lists the
exact public-site paths the current integration task may write, protected `assets/imagery/` is one
of those paths, and R1 added six Act 2 context files there without extending that list. It passed
when I ran it before committing **only because those files were still untracked**, so the "hero
validator 420/0" reported for R1 was true of the tree I ran it on but not of the commit. R3 fixes it
properly: `lane.json` now names WEB-005B / MER-109 as the integration task with its authority,
records the consumed terminal WEB-005A head, and adds the six Act 2 files to the integration write
surface. The guard still holds everywhere else — hero paths remain byte-identical and every other
protected path is still refused. `py -3.14 hero/scripts/validate_hero.py` → **420 checks, 0 failed**.

### 10.8 R3 gates

| gate | result |
|---|---|
| `scripts/validate_site.py` (now also enforces the delivery contract) | **PASSED**, 0 warnings |
| `hero/scripts/validate_hero.py` | **PASSED** — 420 checks, 0 failed |
| `scripts/negative_tests_web005b.py` — 35 cases (24 + 11 new delivery cases) | **PASSED** — 35/35 caught, tree restored identical |
| `scripts/negative_tests_web005.py` — 71 cases | **PASSED** — 71/71 caught, tree restored identical |
| `scripts/check_copy_preservation.py` against `b597baf` | **PASSED** — 0 differences |
| Safe-density sweep 360–3840 px, DPR 1 and 2 | **PASSED** — delivery candidates selected, nothing upscaled, no overflow |
| Rendered-page A/B against the lossless build | **PASSED** — §10.5 |
| Hosted preview | **NOT RUN** — unchanged gate, not WEB-005B's to close |

New validator rules for the delivery contract: every delivery entry must name a lossless reference
of its own layer, exist with a matching checksum and byte count, stay at or below the native grid,
cover the same widths as the lossless set, be recorded as lossy only with a decoded comparison whose
every metric is inside the declared limits, and be smaller than the reference it replaces; the
coupled legend must remain a lossless PNG. All eleven rules are exercised by the negative suite.

### 10.9 Remaining Product decisions

Unchanged from §9, minus the ALT-01 item, which R3 closed: the ALT-01 canonical rendering stays and
its visual weight is carried by layout. The footer attribution remains a content-owner handoff and
was not touched. The RGBA-plus-shared-context delivery architecture in §10.4 is available if Product
later wants the other three layers to compress.
