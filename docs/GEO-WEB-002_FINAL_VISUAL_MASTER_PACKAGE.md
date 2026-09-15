# GEO-WEB-002 — Final homepage public-safe visual master package

**Domain response:** GEO-WEB-002 / Linear MER-102
**Consumer:** `tasks/WEB-005_CINEMATIC_HERO.md` (not yet published) / Linear MER-93
**Authority branch:** `feat/geo-web-002-final-visual-masters`
**Authority baseline:** `8a4fe9ba5cb19d09390cb8816c2324e012331728`
**State:** `READY_FOR_PRODUCT_BINDING`
**Publication scope:** website visual masters only. No scientific method, scoring, weighting, threshold,
feature-eligibility, CRS/grid/unit/NoData/mask/resampling, validation or product-behaviour change.

This document is the canonical package pointer for the locked four-act final homepage. The machine-readable
record of the same package is `assets/imagery/sources.json` → `geo_web_002`, and
`scripts/validate_site.py` recomputes every shipped checksum on each run.

## 1. Governing accepted authority

Product presentation authority:

- `docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md` (locked four-act homepage story)
- `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md` (public-safe boundary and approved export recipes)
- `IMAGERY_RIGHTS.md`, `assets/imagery/sources.json`

Accepted Science / export authority, unchanged by this task:

- `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8` (tag `v1.0.0`)
  - `docs/decisions/ADR-0033-remote-sensing-first-mvp-scoring-boundary.md`
  - `tasks/GEO-037-mvp-relative-priority-scoring.md`
  - `tasks/GEO-039-cartographic-export-final-mvp-acceptance.md`

Accepted scoring identity, unchanged:

| | |
| --- | --- |
| project | `kizildere_mvp_v2` |
| profile | `mvp_remote_sensing_priority_v1` |
| weighting identity | `remote_sensing_equal_family_v1` |
| accepted run identity | `8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c` |
| mandatory score inputs | `thm-thm01`, `alt-alt01`, `alt-alt02` |
| public score label | **Remote-Sensing Relative Priority — Experimental Baseline** |

## 2. Two asset classes, two rule sets

| | **Class A — Act-2 Earth-observation context** | **Class B — Acts 3 and 4 cartographic masters** |
| --- | --- | --- |
| What it is | A natural-colour photographic composite of the area | A cartographic rendering of scientific analysis output |
| Source | USGS Landsat Collection 2 Level-2 surface reflectance (public domain) | Accepted GEO-039 Workbench exports of the persisted `kizildere_mvp_v2` project |
| Produced by | `scripts/build_imagery.py` | The accepted GEO-039 export path; derivatives by `scripts/build_final_visual_masters.py` |
| Master lives | In this repository (`assets/imagery/`) | In the Science repository, pinned here by export id + `export_manifest.json` + SHA-256 |
| Permitted edits | Crop, contrast stretch, gamma, saturation, encoding | Crop and downscale for presentation **only** |
| Extra duties | USGS acknowledgement | Mandatory scientific warnings in visible page copy; attribution carried from the export |

Class B is scientific output, not photography. The gallery grade class A may carry is exactly what must
never touch class B — no re-colouring, re-projection, re-classification, value change, or CSS
colour/contrast/opacity transform on the served raster.

No raw provider raster is committed to this repository as a product-proof asset, no third-party licence is
restated or widened, and no paid, closed or restricted MTA data is included or authorized.

## 3. The resolution ceiling — read this before composing Act 4

The accepted `kizildere_mvp_v2` grid is **1200 × 1200 cells at 30 m (36 × 36 km, EPSG:32635)**. The accepted
GEO-039 renderer draws that grid onto an A4-landscape page at 200 dpi, where the map panel occupies
**1249 × 1249 px**. Those two numbers bound every class-B asset in this package:

- 1200 cells is the real information content. Nothing in the accepted export path holds more.
- 1249 px is the master's own rendering of those cells, and therefore the largest honest derivative.
- The renderer composites rasters with nearest-neighbour interpolation, so the panel crop carries exact
  governed cell colours; it is not a resampled image.

Raising the renderer's DPI would produce a bigger file with no more information, and would change the
byte-for-byte determinism the accepted GEO-039 export contract depends on. It was not done. The
alternative the task allows — publish the exact maximum safe rendered size — is what this package does.

Against the task's presentation targets:

| Target | Delivered | Verdict |
| --- | --- | --- |
| Act-2 EO context ≥ 2000 px wide master | 2400 × 1500 px, native 30 m | **met** |
| Evidence-card masters ≥ 1200 px on the long axis | 1249 px | **met** |
| Priority/result master ≥ 2000 px on the large-display axis | 1249 px | **not met, and not honestly achievable** |

**Act 4 consequence.** WEB-005 must give the priority map a deliberately contained composition of at most
**1249 device pixels** on its long axis — 1249 CSS px on a 1× display, 624 CSS px on a 2× display. A
full-bleed priority raster across a 1600 px+ desktop viewport is not available from accepted science and
must not be faked by stretching. This is the case the visual-narrative authority §2 Act 4 already
anticipated ("otherwise use a deliberately contained/max-width composition rather than stretching a
smaller raster").

## 4. Asset inventory

Master and derivative SHA-256 values below are the authoritative record. Class-B master checksums are copied
from each export's own `export_manifest.json` and re-verified by `scripts/build_final_visual_masters.py`
before any derivative is written; derivative checksums are of the files in this repository and are
recomputed by `scripts/validate_site.py`.

### 4.1 Act 2 — `act2-context` (class A, **context**)

- **Public label:** Kızıldere — Büyük Menderes graben, Denizli, Türkiye
- **Source product:** `LC08_L2SP_179034_20250505_02_T1` — Landsat 8 OLI, acquired **2025-05-05**,
  WRS-2 path 179 / row 034, Tier 1, scene cloud cover 0.90 %
- **Access:** Microsoft Planetary Computer STAC (`landsat-c2-l2`), anonymous read of the USGS archive
- **Rendered frame:** EPSG:32635, 30 m, 2400 × 1500 px = **72 × 45 km**, bounds UTM
  `621268.9, 4182542.0, 693268.9, 4227542.0`, bounds WGS84 `28.3771, 37.7822, 29.2064, 38.1751`,
  valid coverage 100 %
- **AOI relationship:** centred on the accepted AOI centre 37.9794° N, 28.7907° E; the 36 × 36 km AOI
  occupies the middle half of the frame horizontally and all but 4.5 km of it vertically
- **Processing:** OLI bands 4/3/2, USGS surface-reflectance scaling, percentile stretch `[1.0, 99.0]`,
  gamma 1.65, luminance-preserving saturation 1.20, progressive JPEG quality 82; WebP candidates are
  Lanczos downscale + re-encode at quality 76 only
- **Rights:** USGS Landsat data are public domain; no permission required, no use or redistribution
  restriction. Only crop, stretch and encoding are OrbGSS work.
- **Attribution requirement:** *Landsat data courtesy of the U.S. Geological Survey.*
- **Mandatory warning:** Earth-observation context only. A natural-colour photographic composite of the
  area — not analytical evidence, not a scored input, and **not** the acquisition date of any THM or ALT
  evidence layer.
- **Max safe rendered size:** 2400 device px (2400 CSS px at 1×, 1200 CSS px at 2×)

| File | Size | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `assets/imagery/kizildere-aoi-context-2025.jpg` (master) | 2400 × 1500 | 1 183 575 | `9d4f93298d11b31ec7317e72bfd0485fe7bf8a724188108abdc48c8a630197a4` |
| `assets/imagery/kizildere-aoi-context-2025-2400.webp` | 2400 × 1500 | 867 942 | `77cac4d8f8d5a1a1a3d1db62b052b73817888aa3e2dac695336f0ebee22bc8b0` |
| `assets/imagery/kizildere-aoi-context-2025-1800.webp` | 1800 × 1125 | 587 504 | `9ce7b96ade034f83c2e7ae2a48fa82babd1f2575334bd3fe63c9d258bc43589f` |
| `assets/imagery/kizildere-aoi-context-2025-1200.webp` | 1200 × 750 | 300 384 | `6d687a756409340c41cf438382bc16d7b11dfbe9ef0c02e24ce68e190ee56fd1` |
| `assets/imagery/kizildere-aoi-context-2025-900.webp` | 900 × 562 | 176 920 | `0efb480c74864b571a9e300b66fbbd1be290d70bfbca0c3173399dc63167579a` |

### 4.2 Acts 3 and 4 — class-B cartographic masters

Every export below is the accepted GEO-039 Workbench cartographic export of `kizildere_mvp_v2`,
renderer revision `geo039-cartographic-renderer-v1`, project config hash
`c6eac56027d3118280d2a454bdcacf5b01ddb0d733ab23dacbf348b6a50b777c`, PNG master 2338 × 1654,
map panel 1249 × 1249. Manifest pointer:
`geothermal-prospectivity/outputs/kizildere_mvp_v2/exports/<export id>/export_manifest.json`;
master file `.../map.png`.

Derivation for all five: presentation crop `[179, 186, 1428, 1435]` of the rendered map panel — identical to
the accepted WEB-002 crop, so both generations frame the same ground. The `-1249` derivative is that crop
with **no resampling at all**; the `-800` derivative is a Lanczos downscale of the same crop; both are WebP
quality 82. The `-legend` file is a lossless PNG crop `[1552, 170, 2284, 292]` of the master's own governed
legend block (layer title with units, colour ramp, ticks) at native resolution, so WEB-005 can place a
truthful legend **inside** the map frame instead of a detached homepage colour bar
(visual-narrative authority §4).

**Attribution carried by every class-B asset** (rendered inside the master's own sources line and required
in public use): NASADEM elevation via `nasa_earthdata`; Landsat thermal via `usgs_m2m`; Sentinel-2
alteration proxies via `cdse_stac`; palettes are Fabio Crameri's Scientific colour maps v8.0
(MIT, doi:10.5281/zenodo.8035877).

**Rights basis for every class-B asset:** derived OrbGSS cartographic export only; no raw provider raster is
redistributed and no third-party licence is restated or widened. No MTA paid, closed or restricted data.

**Max safe rendered size for every class-B asset:** 1249 device px — 1249 CSS px at 1×, 624 CSS px at 2×.

#### `terrain` — **context**

- Public label: **Elevation — NASADEM context** · layer `top-dem` · style `dem_batlow_terrain` · units m
- Export `20260915T104731Z-00fae5eb`, rendered title *Elevation - NASADEM context*, plan
  `00fae5eb6962af61a14000688e3c8a9945a0bcd50760ff426248dda970d61152`
- Master SHA-256 `8fc9403a022f28a6e5d56443ad16e5b2390a676fd2cd9cf2e50285eae2be6ca1`, 1 018 062 bytes
- Mandatory warning: **Context/display only. Terrain is not a scored predictor and carries no universal
  geothermal-favourability direction.**

| File | Size | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `assets/proof/final/terrain-1249.webp` | 1249 × 1249 | 41 698 | `7d9c6cc14c4fcb97ab7ecd7a6be5e083bbf1cf4b63b341eae530ead7a645dc59` |
| `assets/proof/final/terrain-800.webp` | 800 × 800 | 23 674 | `c608219ec0248647e5d5bf9ad96fa4d4f2342dae91dde8871db7bffc935bbdeb` |
| `assets/proof/final/terrain-legend.png` | 732 × 122 | 9 189 | `ca56f442159057b87ff9985ad6c1ec640d79b330fcb6dc7f7632203179b5d268` |

#### `thm01` — **evidence** (mandatory score input)

- Public label: **THM-01 Thermal Anomaly** · layer `thm-thm01` · style `thm01_vik_diverging`
- Export `20260915T104733Z-cfba9119`, rendered title *THM-01 Thermal Anomaly*, plan
  `cfba9119b126568215b95dd010bbd11698cd24cb5da72743f6e0d6584dd90322`
- Master SHA-256 `fe789994c29a9a87a3e08a29af5663e7c922f07c6e3016027fb1f5d2ef505dac`, 2 251 165 bytes
- Temporal semantics: accepted Landsat-derived thermal evidence family, used exactly as persisted. The
  governing GEO-037/GEO-039 closeouts do not duplicate individual acquisition dates; **public copy must not
  invent one.**
- Mandatory warning: **Evidence layer only. Do not describe it as geothermal probability, reserve,
  discovery, or drilling-success evidence.**

| File | Size | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `assets/proof/final/thm01-1249.webp` | 1249 × 1249 | 251 574 | `0f1176c9ba6b5e8da6b2c0439f2444be335107f0abdc31cfc4c3c515f75587e6` |
| `assets/proof/final/thm01-800.webp` | 800 × 800 | 132 468 | `27d986785889dd900ed1a97eb438f773df28c3f97c89b6929011936cf141a870` |
| `assets/proof/final/thm01-legend.png` | 732 × 122 | 8 062 | `fe53c651d6e94d1075f8eceb8079d3a26c7320f24d6244b5b9d79267e25005b3` |

#### `alt01` — **evidence** (mandatory score input) · recommended alteration card

- Public label: **ALT-01 Alteration Proxy — clay/hydroxyl** · layer `alt-alt01` · style `alt_batlow_sequential`
- Export `20260915T104801Z-eb1bc414`, rendered title *ALT-01 Alteration Proxy (clay, hydroxyl)*, plan
  `eb1bc414e55ad30e4eefddf60857ecb2186b87166b98b516855baed0fdaa1c67`
- Master SHA-256 `80fd75303100728ca6fd935b56167f17f0fd68b0b719b9306e1fac9ed5b5adf8`, 1 158 724 bytes
- Mandatory warning: **Broad Sentinel-2 spectral alteration proxy; not mineral/kaolinite identification and
  not proof of hydrothermal alteration.**

| File | Size | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `assets/proof/final/alt01-1249.webp` | 1249 × 1249 | 393 032 | `d8e9b9d7ba1bb3d96eb059682cffe8a6aa9349e1d99bdf67b63ad1298a079f1b` |
| `assets/proof/final/alt01-800.webp` | 800 × 800 | 202 354 | `6e0be10cd8137f33b96bbc7e8ba2f2789199a3e744b739e463a06acab2a2131e` |
| `assets/proof/final/alt01-legend.png` | 732 × 122 | 13 248 | `776f90d4a62cc864281fedcd71802ba35e896a4c283d2f5e6a27315d8260fe69` |

#### `alt02` — **evidence** (mandatory score input) · alternate alteration card

- Public label: **ALT-02 Alteration Proxy — ferric/iron** · layer `alt-alt02` · style `alt_batlow_sequential`
- Export `20260915T104804Z-1f837163`, rendered title *ALT-02 Alteration Proxy (ferric, iron)*, plan
  `1f837163ca6f834142b0f0865cfa3e45fe9254827af726345dbfa3398a774595`
- Master SHA-256 `b3d1824de39293af4b10a56beb04f4e7bb28988cf86cafb30024da66b528f950`, 617 803 bytes
- Mandatory warning: **Broad Sentinel-2 spectral alteration proxy; not mineral identification and not proof
  of hydrothermal alteration.**

| File | Size | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `assets/proof/final/alt02-1249.webp` | 1249 × 1249 | 381 046 | `5fc048e589d5b5361c257cb9883cccadc15aafc3cf8c0a5a2bf8be9734556981` |
| `assets/proof/final/alt02-800.webp` | 800 × 800 | 194 992 | `855c0976a32881e4425f1f9bc1e513c14ce651e1d0b11abd91f210c0f11a650c` |
| `assets/proof/final/alt02-legend.png` | 732 × 122 | 12 594 | `bc6cb0d2a5a36c48c982a67e7ab3c39c682497e2ad2a0cb452c9487f60311f61` |

#### `priority` — **derived score**

- Public label: **Remote-Sensing Relative Priority — Experimental Baseline** ·
  layer `score-mvp-remote-sensing-priority` · style `score_priority_batlow_0_100`
- Export `20260915T104736Z-55609249`, rendered title
  *Remote-Sensing Relative Priority - Experimental Baseline*, plan
  `55609249d111db29817f71283b2f608559c87b611cf704800906790afa3fb581`
- Master SHA-256 `4791435a1b1c1d19a18337997eaf51dfb468ed022349771e1007c6da026aa2ad`, 3 634 791 bytes
- Scoring identity: profile `mvp_remote_sensing_priority_v1`, weighting `remote_sensing_equal_family_v1`,
  run `8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c`, mandatory inputs
  `thm-thm01` + `alt-alt01` + `alt-alt02`, value range 0–100, dimensionless AOI-relative priority,
  **not** a probability and **not** Full Prospectivity
- Mandatory warning: **AOI-relative experimental screening only. Not probability, reserve/resource
  estimation, discovery likelihood, drilling-success likelihood, Full Prospectivity, or a calibrated
  cross-AOI score.**

| File | Size | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `assets/proof/final/priority-1249.webp` | 1249 × 1249 | 702 856 | `137e1150dedcc873ad7f2a56b3bbe06659ee905230c56bcbfffa40be78a011a1` |
| `assets/proof/final/priority-800.webp` | 800 × 800 | 300 646 | `444356f044c1ffc0276345d05d4d738f09cc233f48399fd3f41473295696a2d4` |
| `assets/proof/final/priority-legend.png` | 732 × 122 | 12 887 | `aaf3c8cb1cb69be1178b1277d7166dd189650eb3463aa6d6e83e33e039ce51d4` |

## 5. Presentation findings WEB-005 must not "fix"

1. **ALT-01 and ALT-02 read as dark fields with bright anomalies.** The only registry-approved style for
   both layers normalizes linearly over the layer's full value range, and the data carry a long high-value
   tail, so roughly 87 % (ALT-01) and 88 % (ALT-02) of valid cells render in the lowest fifth of the batlow
   ramp. That is the accepted scientific rendering, and no alternative approved style exists for these
   layers. **Do not re-stretch, re-normalize or CSS-adjust them.** Present the alteration card at card
   scale with its legend and let THM-01 carry the visually dominant evidence card. ALT-01 is the
   recommended single alteration card; ALT-02 is published so Product has both accepted proxies.
2. **NoData is real and visible.** Measured on the shipped 1249 px panels, the neutral `#f3f2ee`
   NoData / outside-AOI ground covers 0.0 % of `terrain`, 0.2 % of `thm01`, 4.0 % of `alt01`, 4.6 % of
   `alt02` and 5.5 % of `priority`. It must not be masked, filled, selectively cropped away or recoloured.
3. **The panels carry their own north arrow, scale bar and AOI outline** inside the map frame. That is the
   in-frame orientation the visual-narrative authority asks for; no separate homepage scale strip is needed
   or permitted.
4. **The Act-2 context is photography, not evidence.** It carries no scientific warning obligation beyond
   its own — but copy next to it must not describe it as a measurement, a layer, or the acquisition of any
   THM/ALT evidence.
5. **Transfer budget.** The class-A 2400 px candidate (848 KiB) is the heaviest file in the package. WEB-005
   selects `srcset` candidates against the WEB-004 performance floors; this package publishes the ladder,
   not the delivery decision.

## 6. Scientific invariants — unchanged by this package

- Mandatory numeric core remains THM-01 + ALT-01 + ALT-02 only.
- Missing mandatory evidence remains fail-closed; no weight renormalization.
- Terrain remains context/display only and is not a scored predictor.
- Structure and Geology remain `optional support / DATA_GAP / score-invariant` under ADR-0033 / GEO-037.
  This package publishes no structure or geology asset and nothing is fabricated to fill that gap.
- Known fields, wells and manifestations remain reference/context only, never predictors.
- No MTA paid, closed or restricted data.
- No CRS, grid, unit, NoData, mask, resampling, QA, feature-eligibility or scoring change.
- No new validation, uncertainty, probability, reserve/resource, discovery or drilling-success claim.
- No raw provider raster is committed to this repository as a product-proof asset.

## 7. Reproduction

```
python scripts/build_imagery.py kizildere-aoi-context-2025 --record   # class A master (network)
python scripts/build_final_visual_masters.py --record                 # all derivatives (local)
python scripts/validate_site.py                                       # recompute every checksum
```

`scripts/build_final_visual_masters.py` refuses to derive from a class-B master whose bytes do not match the
SHA-256 in its own `export_manifest.json`, refuses an export that renders layers other than the ones the
asset declares, and refuses any derivative wider than the master's own map panel.

## 8. Terminal domain state

`READY_FOR_PRODUCT_BINDING`. Product may bind this package into WEB-005 after terminal Science acceptance of
MER-102. Binding it does not license any change to the labels, warnings, styles, crops or maximum safe
rendered sizes recorded here.
