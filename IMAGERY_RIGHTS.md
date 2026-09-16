# OrbGSS imagery rights and provenance — v0.9

## Three asset classes

OrbGSS serves only self-hosted imagery, and the site now publishes **three distinct classes** with
different sources, different rights bases and different handling rules. Do not describe one with
the other's wording.

| | **A — Landsat gallery imagery** | **B — WEB-002 product-proof exports** |
| --- | --- | --- |
| What it is | Natural-colour photographic composites of a landscape | Cartographic renderings of scientific analysis output |
| Source | USGS Landsat Collection 2 Level-2 surface reflectance (public domain) | OrbGSS cartographic exports of the accepted `kizildere_mvp_v2` project |
| Produced by | `scripts/build_imagery.py` (crop / stretch / encode) | The accepted GEO-039 Workbench cartographic export path |
| Recorded in | `sources.json` → `scenes`, and → `geo_web_002.context_scenes` | `sources.json` → `web_002.proof_assets`, and → `geo_web_002.assets` |
| Where used | Act 2 of the homepage (the Kızıldere context master); the older gallery scenes are retired | Acts 3 and 4 of the homepage, and the deeper `/pilot/` route |
| Permitted edits | Crop, contrast stretch, gamma, saturation, encoding | Crop and resize for presentation **only** — never re-colour, re-project, re-classify or change values, and no CSS colour/contrast/opacity transform on the served raster |
| Extra duties | USGS acknowledgement in the footer | Mandatory scientific warnings in visible EN/TR page copy; checksummed provenance |

Class B is a scientific output, not photography. The gallery grade that class A may carry is
exactly what must never touch class B.

## Class A — production rule

The production source is **USGS Landsat Collection 2 Level-2** surface reflectance.

USGS states that Landsat data are official USGS records in the public domain, permission is not required for use, and there are no restrictions on use or redistribution. USGS requests source acknowledgement.

Reference pages:

- https://www.usgs.gov/faqs/are-landsat-data-cloud-still-considered-be-within-public-domain
- https://www.usgs.gov/faqs/are-there-any-restrictions-use-or-redistribution-landsat-data
- https://www.usgs.gov/landsat-missions/landsat-collection-2-level-2-science-products

Acknowledgement carried in the site footer:

> Landsat data courtesy of the U.S. Geological Survey.

## How the live assets were produced

Every file under `assets/imagery/*.jpg` is an **OrbGSS-generated natural-color composite** (OLI bands 4, 3, 2) built by `scripts/build_imagery.py` from the Landsat Collection 2 Level-2 products listed below. The pipeline:

1. reads the surface-reflectance Cloud-Optimized GeoTIFFs for the pinned product identifiers through the Microsoft Planetary Computer STAC API (`landsat-c2-l2` collection, anonymous read-only mirror of the USGS archive);
2. crops a fixed frame in the scene's native UTM grid at 30 m, mosaicking consecutive rows of the same path/date where a frame crosses a scene boundary;
3. applies the USGS reflectance scaling, a documented per-scene contrast stretch and gamma, mild saturation;
4. encodes a progressive JPEG.

The pixels are USGS products; only the crop, stretch and encoding are OrbGSS work. All parameters and the rendered bounds are recorded in `assets/imagery/sources.json` under each scene's `production` block, so any asset can be regenerated bit-for-bit in intent.

No NASA-rendered pixels, NASA logos or identifiers are served. The NASA Earth Observatory pages listed below are kept only as the references that motivated each scene selection and as an independent confirmation of the acquisition metadata.

## Selected scenes

### Crater Lake — hero
- Location: Crater Lake, Oregon, USA
- Coordinates displayed: 42.9443° N, 122.1353° W
- Acquisition: 18 March 2023
- Sensor: Landsat 8 OLI
- Production source product: `LC08_L2SP_045030_20230318_02_T1` (WRS-2 path 045 row 030, Tier 1)
- Reference page: https://science.nasa.gov/earth/earth-observatory/a-clear-view-of-crater-lake-151161/

### Yellowstone — geothermal
- Location: Yellowstone National Park, USA
- Coordinates displayed: 44.4604° N, 110.8282° W
- Acquisition: 9 June 2013
- Sensor: Landsat 8 OLI
- Production source product: `LC08_L2SP_038029_20130609_02_T1` (path 038 row 029, Tier 1)
- Reference page: https://science.nasa.gov/earth/earth-observatory/yellowstone-national-park-87881/
- Note: the NASA reference rendering also used ASTER GDEM terrain. The production composite is a plain orthographic Landsat view with no ASTER data.

### Chuquicamata — mineral
- Location: Chuquicamata, Antofagasta, Chile
- Coordinates displayed: 22.3150° S, 68.9010° W
- Acquisition: 4 January 2024
- Sensor: Landsat 9 OLI-2
- Production source product: `LC09_L2SP_001075_20240104_02_T1` (path 001 row 075, Tier 1)
- Reference page: https://science.nasa.gov/earth/earth-observatory/copper-mining-at-chuquicamata-152368/

### Kızıldere AOI context — GEO-WEB-002 Act 2
- Location: Kızıldere — Büyük Menderes graben, Denizli, Türkiye
- Coordinates displayed: 37.9794° N, 28.7907° E (accepted `kizildere_mvp_v2` AOI centre)
- Acquisition: 5 May 2025
- Sensor: Landsat 8 OLI
- Production source product: `LC08_L2SP_179034_20250505_02_T1` (path 179 row 034, Tier 1, 0.90 % cloud)
- Rendered frame: EPSG:32635, 30 m, 2400 × 1500 px = 72 × 45 km, 100 % valid coverage
- No NASA Earth Observatory reference page: the scene was selected directly from the USGS Collection 2
  archive through the Planetary Computer STAC mirror on visual/contextual criteria only.
- Published for WEB-005 under `docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md`; not yet placed on any route.

### Ili River Delta / Lake Balkhash — environmental
- Location: Ili River Delta & Lake Balkhash, Kazakhstan
- Coordinates displayed: 45.0600° N, 74.5200° E
- Acquisition: 7 March 2020
- Sensor: Landsat 8 OLI
- Production source products: `LC08_L2SP_152029_20200307_02_T1` and `LC08_L2SP_152028_20200307_02_T1` (path 152 rows 029 + 028, same overpass, mosaicked)
- Reference page: https://earthobservatory.nasa.gov/images/146552/a-delta-oasis-in-southeastern-kazakhstan

## Class B — WEB-002 product-proof visuals (2026-09-15)

Story panels 01–06 no longer carry Landsat gallery material. They carry OrbGSS **cartographic
exports** of the Kızıldere MVP pilot AOI, produced through the accepted GEO-039 Workbench export
path from the persisted `kizildere_mvp_v2` project in
`mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8` (tag
`v1.0.0`). The authorizing publication boundary is `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`.

What is served: OrbGSS-rendered map imagery only. No raw provider raster is redistributed, no
third-party licence is restated or widened, and no paid, closed or restricted MTA data is
included. The underlying evidence families and their providers (NASADEM elevation via
`nasa_earthdata`; Landsat thermal via `usgs_m2m`; Sentinel-2 alteration proxies via `cdse_stac`)
remain credited inside each rendered export, whose attribution line the export itself carries.
The colour ramps are Fabio Crameri's Scientific colour maps v8.0 (MIT, doi:10.5281/zenodo.8035877),
credited in the same export.

Each website file under `assets/proof/` is a presentation derivative — a crop of the rendered map
panel, resized to 1400 px and 800 px and encoded as WebP. Cropping and resizing only; no
re-colouring, re-projection, re-classification or value change. For every asset,
`assets/imagery/sources.json` (`web_002.proof_assets`) records the export id, the
`export_manifest.json` pointer, the master PNG SHA-256 taken from that manifest, the crop box and
a SHA-256 for each derivative shipped here. `scripts/validate_site.py` recomputes those derivative
checksums on every run, so a changed file fails validation.

Mandatory scientific warnings from the package are carried on the page as visible EN/TR copy next
to each panel. `04 Structure` publishes no asset: no public-safe fault or lithology master is
authorized, and that gap is score-invariant under ADR-0033 / GEO-037.

## GEO-WEB-002 — final homepage visual master package (2026-09-16)

`docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md` publishes the visual masters the locked four-act final
homepage needs, for WEB-005 to bind after Science acceptance. Nothing in that package is placed on a public
route yet. It adds one class-A asset and five class-B assets; the rights bases above are unchanged.

**Class A — Act 2.** `assets/imagery/kizildere-aoi-context-2025.jpg` plus four responsive WebP candidates
(2400 / 1800 / 1200 / 900). Same rule as every other gallery scene: public-domain USGS Landsat pixels, with
only the crop, stretch and encoding as OrbGSS work, and the USGS acknowledgement carried in the footer.

**Class B — Acts 3 and 4.** `assets/proof/final/` carries `terrain`, `thm01`, `alt01`, `alt02` and
`priority`, each as a native-resolution map-panel crop (1249 px), an 800 px card derivative and a lossless
legend crop. Same rule as `assets/proof/`: derived OrbGSS cartographic exports only, no raw provider raster,
no restated or widened third-party licence, no MTA paid/closed/restricted data. The exports' own attribution
(NASADEM via `nasa_earthdata`, Landsat thermal via `usgs_m2m`, Sentinel-2 alteration via `cdse_stac`, Fabio
Crameri's Scientific colour maps v8.0, MIT) must be carried into public use, and each asset's mandatory
scientific warning must appear as visible EN/TR copy wherever the asset is shown.

The legend crops exist so a necessary legend can sit **inside** the map frame instead of becoming a detached
homepage colour bar. They are native-resolution crops of the master's own governed legend: no resize,
recolour or relabel.

Structure and geology are still absent from this package. No public-safe fault or lithology master is
authorized and the gap remains score-invariant.

## WEB-001 placement (2026-09-15, superseded by WEB-002, then by WEB-005)

WEB-001 reused the four Landsat scenes as temporary gallery material across the story panels.
WEB-002 replaced every story slot with product proof, leaving only Crater Lake placed as the hero
poster. **WEB-005 retires that too:** the homepage hero is now the rendered cinematic acquisition
sequence, and Act 2 uses the accepted Kızıldere context master instead. All four original scenes
are now `retired-from-homepage`. They keep their files, full provenance and reuse rights in
`assets/imagery/sources.json` and remain available for later use; nothing on any route references
them. The USGS acknowledgement stays in the footer, because Act 2 is Landsat-derived.

## Class C — WEB-005 rendered hero media (2026-09-16)

A third class joined the site with WEB-005, and it must not be described as either of the others.

| | **C — rendered cinematic hero** |
| --- | --- |
| What it is | A 3D render of Earth from orbit with an acquisition frame over the pilot region. **Not sensor imagery.** |
| Files | `assets/hero/orbgss-hero.webm`, `assets/hero/orbgss-hero.mp4`, `assets/hero/hero-poster-1600.webp`, `assets/hero/hero-poster-900.webp` |
| Produced by | The accepted WEB-HERO-001 Blender production lane (`hero/`), scene `hero_production_kizildere`, carried forward from `feat/web-hero-001-predata-scene@e95fdcac7cac82e597d40dab4cdc96ce1a6b319e` |
| Recorded in | `sources.json` → `web_005.hero_media`; render and encode evidence in `hero/evidence/production_media.json` |
| Underlying texture rights | NASA Earth Observatory Blue Marble albedo and night-lights composites, public domain, recorded with checksums in `hero/assets/manifest.json` |
| Permitted edits | Re-render or re-encode from the accepted scene definition. The scene is configuration, so a change is a config change with a diff, not a retouch. |
| Extra duties | The caption must say it is a render. `scene.hero.kind` carries "Rendered orbital sequence — not sensor imagery" in EN and TR, and that wording is not optional. |

The honesty rule for class C is the mirror of the one for class B. Class B must never be made to
look prettier than the science; class C must never be allowed to look like measurement. It shows
where OrbGSS is pointed, not what any instrument recorded.

**No scientific raster is baked into class C.** The hero's real-data result handoff is a page
element carrying the accepted class-B derivative as its own checksummed file. A governed raster
inside a lossy video encode would have its colours and values changed by chroma subsampling and
quantisation, which the accepted package forbids — so the encoder never sees one.

## Resolution note

The composites are native 30 m Landsat surface reflectance. 15 m pan-sharpened Level-1 products for these acquisitions are only obtainable through USGS EarthExplorer / Machine-to-Machine access, which requires an account that was not authorized for this work. If sharper hero imagery is wanted later, that is the path; the provenance model above stays the same.

Class B has its own, harder ceiling: the accepted `kizildere_mvp_v2` grid is 1200 × 1200 cells at 30 m, and
the accepted GEO-039 renderer draws that panel at 1249 px. 1249 device pixels is therefore the maximum
honest rendered width for any cartographic asset, and no derivative in this repository exceeds it. Widening
one would invent resolution, so a larger presentation must be answered with a contained composition instead.
Each GEO-WEB-002 asset records its own `max_safe_rendered_px`.

## Deployment gate

Before `orbgss.com` is made public:

1. Every file listed in `assets/imagery/sources.json` under `local_file` exists and passes `python scripts/validate_site.py` (done in v0.5).
2. Each image has been visually checked against its scene metadata (done in v0.5).
3. No NASA logo/identifier is embedded in any image (none: assets are generated from raw Landsat bands).
4. Keep the USGS acknowledgement in the footer.
5. If a non-USGS source is introduced later, record its exact license and attribution requirement here before it enters production.
