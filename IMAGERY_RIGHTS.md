# OrbGSS imagery rights and provenance — v0.12 (2026-10-25, MER-279)

## Three asset classes

OrbGSS serves only self-hosted imagery, and the site now publishes **three distinct classes** with
different sources, different rights bases and different handling rules. Do not describe one with
the other's wording.

| | **A — Landsat gallery imagery** | **B — WEB-002 product-proof exports** |
| --- | --- | --- |
| What it is | Natural-colour photographic composites of a landscape | Cartographic renderings of scientific analysis output |
| Source | USGS Landsat Collection 2 Level-2 surface reflectance (public domain) | OrbGSS cartographic exports of the accepted `kizildere_mvp_v2` project |
| Produced by | `scripts/build_imagery.py` (crop / stretch / encode) | The accepted GEO-039 Workbench cartographic export path; the homepage derivatives by `scripts/build_web005b_presentation.py` under MER-151 |
| Recorded in | `sources.json` → `scenes`, → `geo_web_002.context_scenes`, and → `web_005b.context` | `sources.json` → `web_002.proof_assets`, → `geo_web_002.assets`, and → `web_005b.analytical` |
| Where used | Act 2 of the homepage and the inspection-aid base (the WEB-005B natural-colour Kızıldere master), and the three illustrative domain photographs (the homepage Solutions cards and, at full size, the `/solutions/` hub bands since MER-240); Crater Lake is retired. Since MER-240 class A also holds one cartographic illustration, the Kızıldere locator map (see below) | Acts 3 and 4 and the inspection aid on the homepage (`web_005b.analytical`). The `web_002.proof_assets` were shown on `/pilot/` until MER-240 retired that route; like the `geo_web_002.assets` they are deployed but placed on no page |
| Permitted edits | Crop, contrast stretch, gamma, saturation, encoding | Crop and resize for presentation **only** — never re-colour, re-project, re-classify or change values, and no CSS colour/contrast/opacity transform on the served raster. The one exception: the homepage surfaces may carry MER-151's bounded display window and one fixed monotonic gamma per layer, and priority is never windowed. |
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

### Crater Lake — former hero (retired; placed on no page)
- Location: Crater Lake, Oregon, USA
- Coordinates displayed: 42.9443° N, 122.1353° W
- Acquisition: 18 March 2023
- Sensor: Landsat 8 OLI
- Production source product: `LC08_L2SP_045030_20230318_02_T1` (WRS-2 path 045 row 030, Tier 1)
- Reference page: https://science.nasa.gov/earth/earth-observatory/a-clear-view-of-crater-lake-151161/

### Yellowstone — geothermal (illustrative domain photograph: homepage card, `/solutions/` hub band)
- Location: Yellowstone National Park, USA
- Coordinates displayed: 44.4604° N, 110.8282° W
- Acquisition: 9 June 2013
- Sensor: Landsat 8 OLI
- Production source product: `LC08_L2SP_038029_20130609_02_T1` (path 038 row 029, Tier 1)
- Reference page: https://science.nasa.gov/earth/earth-observatory/yellowstone-national-park-87881/
- Note: the NASA reference rendering also used ASTER GDEM terrain. The production composite is a plain orthographic Landsat view with no ASTER data.

### Chuquicamata — mining (illustrative domain photograph: homepage card, `/solutions/` hub band)
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
- Published for WEB-005 under `docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md`. Superseded on the homepage by the WEB-005B natural-colour master below, it stays recorded and deployed but is placed on no page.

### Kızıldere natural-colour context — WEB-005B Act 2 (placed)
- Same product and place as above: `LC08_L2SP_179034_20250505_02_T1`, Landsat 8 OLI, 5 May 2025, displayed at 37.9794° N, 28.7907° E.
- Re-cropped wider at the native 30 m to 3200 × 1800 px and tone-rendered on one common reflectance scale. Master `assets/imagery/kizildere-aoi-context-2025-natural.jpg` (JPEG q90, 4:4:4), with WebP derivatives at 3200 / 2400 / 1600 / 1200 / 800.
- Recorded in `sources.json` → `web_005b.context` (production, frame, checksums, rights basis).
- Used for homepage Act 2 and as the base of the inspection aid. Public-domain USGS pixels: only the crop, tone rendering and encoding are OrbGSS work, and the USGS acknowledgement stays in the footer.

### Kızıldere interior-page crops — MER-255 (class A, four crops of the Act 2 master)
- What they are: four crops of the WEB-005B Act 2 master above (`kizildere-aoi-context-2025-natural.jpg`, 3200 × 1800 px, native 30 m, USGS Landsat 8 OLI, `LC08_L2SP_179034_20250505_02_T1`), made by `scripts/build_interior_crops.py` for the redesigned interior pages. Public-domain USGS pixels: only the crop and the WebP encode (quality 82) are OrbGSS work. No tone, colour, sharpening, upscaling or generative step; a derivative narrower than its crop is a Lanczos downscale and none is wider than its crop.
- `kizildere-stage` — the wide strip behind the Geothermal page headline (crop 3200 × 1100, derivatives 3200 / 2400 / 1600). Shown on `/solutions/geothermal/` only.
- `kizildere-aoi` — the 36 × 36 km analysis grid in natural colour (crop 1200 × 1200, derivatives 1200 / 800), with the same crop as the base frame of the layer diagram. Shown on `/solutions/geothermal/` only. It is a photograph of the area, not analysis.
- `kizildere-terrain` — eroded ground north-east of the pilot area, beyond the east edge of the analysis grid (crop 1459 × 897, derivatives 1459 / 1000). Shown on `/about/` only.
- `kizildere-valley` — the cultivated graben floor in the south-west of the context frame (crop 1000 × 1000, derivatives 1000 / 700). Its eastern third overlaps the western edge of the analysis grid, so its alt text places it "in the south-west of the Kızıldere context view" and the record states the overlap. Shown on `/partner/` only.
- Captions: the standard bottom-right caption (place, coordinates, "Natural-color composite"). The coordinates are the crop's `label_point` in `sources.json`: the declared pilot centre (37.9794° N, 28.7907° E) for `kizildere-stage` and `kizildere-aoi`, which contain it; the crop's own centre for `kizildere-terrain` (38.0936° N, 29.2483° E, "East of the Kızıldere pilot area") and `kizildere-valley` (37.8744° N, 28.5695° E, "South-west of the Kızıldere pilot area"), which do not. The pilot centre is never printed on a crop that does not show it. `scripts/geo_frame.py` (UTM 35N, 30 m master grid) projects each printed pair onto the master, and `scripts/validate_site.py` fails when it falls outside the crop box.
- Recorded in `sources.json` → `web_m6.interior_crops` (parent checksum, crop box, size, per-file SHA-256 and bytes, content-hash file names, rights basis, overlap with the analysis grid, caption keys, `rendered`). `rendered` is measured in a real browser by `scripts/measure_interior_renders.py` (19 viewport widths from 360 to 3840 CSS px at device pixel ratios 1 and 2; the drawn width, including `object-fit: cover`, against the candidate the browser selected). No crop is drawn above its own pixels (worst ratio 1.00); the validator also holds the CSS width caps to the same bound without a browser.
- Rule R2 (`docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md`) applies to each crop: one full-size appearance; the Sources page lists images only as thumbnails of at most 160 CSS px, each a recorded image.

### Ili River Delta / Lake Balkhash — marine (illustrative domain photograph: homepage card, `/solutions/` hub band; MER-238 D5 may replace it with a coastal scene)
- Location: Ili River Delta & Lake Balkhash, Kazakhstan
- Coordinates displayed: 45.0600° N, 74.5200° E
- Acquisition: 7 March 2020
- Sensor: Landsat 8 OLI
- Production source products: `LC08_L2SP_152029_20200307_02_T1` and `LC08_L2SP_152028_20200307_02_T1` (path 152 rows 029 + 028, same overpass, mosaicked)
- Reference page: https://earthobservatory.nasa.gov/images/146552/a-delta-oasis-in-southeastern-kazakhstan

**Hub bands (MER-240).** The `/solutions/` hub shows the three photographs at full size, in bands capped at 1440 CSS px, so a 2× display is served the 2880 px master width and nothing is upscaled. Chuquicamata and the Ili Delta gained 2400 and 2880 px WebP derivatives for this, built by `scripts/build_domain_derivatives.py` with the same resize-and-encode operation as their existing ones (no crop, colour, tone or gamma change); the existing derivatives were kept byte for byte. Each scene records the placement in `sources.json` → `web_m6_placement`, and the page footnote frames the photographs as other places, not OrbGSS results.

### Kızıldere locator map — Natural Earth (class A cartographic illustration, MER-240)
- What it is: an outline map of Türkiye and its neighbours with the 36 km pilot area of interest drawn as a square at its declared centre (37.9794° N, 28.7907° E). A locator, not Earth-observation imagery and not product proof. It shows no analysis and carries no text; the page caption says `Locator map — Natural Earth`.
- Source: Natural Earth 1:50m Cultural Vectors, Admin 0 – Countries, v5.1.2 (`ne_50m_admin_0_countries.geojson` from the `nvkelso/natural-earth-vector` v5.1.2 release, SHA-256 `3e458fc0…`). Downloaded on 2026-10-16 with CTO approval; the download is not committed, only the generated SVG is.
- Rights: Natural Earth data are in the public domain (https://www.naturalearthdata.com/about/terms-of-use/). No permission or attribution is required; the Sources page (`/sources/`) credits it as "Made with Natural Earth".
- Produced by: `scripts/build_locator_map.py` (Python standard library only): equirectangular projection true at 39° N, clipped outside the frame, lightly simplified. Türkiye is filled and outlined; neighbouring countries are filled in one colour with no borders between them, so the map draws no third-country boundary. Since the Heat Trace adoption (2026-10-25) the colours follow the brand's map rule (Night-family neutrals, no Amber or Glow, the 36 km area as a dashed Magma callout inside a Night halo); the geometry, source and projection are unchanged, and the file is the new, checksum-named `assets/maps/kizildere-locator-006fcf1f.svg` (the previous files, Agate `…226827d0` and the one before it, are removed).
- Recorded in: `sources.json` → `web_m6.locator_map` (source URL and checksum, licence, generator, output checksum). The file name carries its own checksum, because `/assets/` is served immutable.
- Used on: the Geothermal page, as the lead of "Where the pilot is" (`/solutions/geothermal/`), only; the Sources page lists it as a 160 px thumbnail.

## Class B — WEB-002 product-proof visuals (2026-09-15)

Story panels 01–06 no longer carry Landsat gallery material. (Since WEB-005 these WEB-002 exports were shown on `/pilot/`, not on the homepage; since MER-240 retired `/pilot/` they are deployed but placed on no page.) They carry OrbGSS **cartographic
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
homepage needs, for WEB-005 to bind after Science acceptance. WEB-005B later took over its homepage role: Act 2
uses the natural-colour master above, and Acts 3–4 use the MER-151 derivatives below. The package stays recorded
and deployed (`assets/proof/final/`, `assets/imagery/kizildere-aoi-context-2025*`) but is placed on no page.
MER-238 D1 / MER-242 decide whether its ALT-02 and priority-over-relief roles return, as MER-151-family
derivatives. It adds one class-A asset and five class-B assets; the rights bases above are unchanged.

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

## Class B — WEB-005B homepage presentation derivatives under MER-151 (2026-09-20)

Homepage Acts 3–4 and the inspection aid bind `sources.json` → `web_005b.analytical`: presentation
derivatives of the governed rasters of the accepted `kizildere_mvp_v2` export `20260917T161155Z-5e7a0e53`
(scientific master 1200 × 1200 at 30 m, EPSG:32635, unchanged and authoritative). They are built by
`scripts/build_web005b_presentation.py` under MER-151 / GEO-WEB-004
(`geothermal-prospectivity@e8aa5d65:tasks/MER-151_GEO-WEB-004_HOMEPAGE_EVIDENCE_PRESENTATION_PARITY_AUTHORITY.md`).

* **Transforms:** canonical normalization, then a bounded display window and one fixed monotonic gamma per layer:
  * Terrain and priority: transfer disabled; priority is never windowed.
  * THM-01: `q_abs 0.998` window with gamma 0.85.
  * ALT-01: `q_low 0.02 / q_high 0.98` window.
* **Rendering:** the frozen hero palette stops; NoData transparent over a neutral hillshade; lossless WebP.
* **Files:** `assets/proof/web005b/` → `terrain-{600,900,1200}-d.webp`, `thm01-*`, `alt01-*`, `priority-*` and `priority-legend-ramp.png`.
* **Records:** each layer records its governed source SHA-256, its window and gamma decision, and a SHA-256 per derivative. `scripts/validate_site.py` recomputes the checksums and the palette LUT and re-checks every MER-151 bound.
* **Rights:** the same basis as every class-B export. The output is OrbGSS's own analytical rendering: no raw provider raster is redistributed, and no paid, closed or restricted data is used. The underlying providers (NASADEM, Landsat thermal, Sentinel-2) are credited on `/sources/` (since MER-255; before it, in a long footer sentence), and the footer keeps the two credits the providers ask for there: the Landsat acknowledgement and "Contains modified Copernicus Sentinel data (2025)".
* **Warnings:** each surface carries its mandatory scientific warning as visible EN/TR copy.
* **Ceiling:** the native 1200 px grid, designed against 600 CSS px. MER-151 permits a 4K presentation derivative, but none is published.

## WEB-001 placement (2026-09-15, superseded by WEB-002, then by WEB-005)

WEB-001 reused the four Landsat scenes as temporary gallery material across the story panels.
WEB-002 replaced every story slot with product proof, leaving only Crater Lake placed as the hero
poster. **WEB-005 retires that too:** the homepage hero is now the rendered cinematic acquisition
sequence, and Act 2 uses the accepted Kızıldere context master instead. All four original scenes
are now `retired-from-homepage`. They keep their files, full provenance and reuse rights in
`assets/imagery/sources.json`. WEB-005B R11 then placed resize-and-encode derivatives of Yellowstone,
Chuquicamata and the Ili Delta as the illustrative Solutions-card photographs. The scene masters are
unchanged, and the cards' footnote says they show other places, not OrbGSS results. Crater Lake is placed on
no page. The USGS acknowledgement stays in the footer, because Act 2 and the cards are Landsat-derived.

## Class C — WEB-005 rendered hero media (2026-09-16)

A third class joined the site with WEB-005, and it must not be described as either of the others.

| | **C — rendered cinematic hero** |
| --- | --- |
| What it is | A 3D render of Earth from orbit with an acquisition frame over the pilot region. **Not sensor imagery.** |
| Files | Since MER-216, a two-tier ladder of the same 276 master frames, hash-named because `/assets/` is immutable-cached: `assets/hero/orbgss-hero-1280-21da1079.webm`, `orbgss-hero-1280-164c957f.mp4`, `orbgss-hero-1920-ca741624.webm`, `orbgss-hero-1920-c8db4a5a.mp4`. Stills: `hero-opening-1600.webp` (startup poster), `hero-poster-1600.webp` and `hero-poster-900.webp` (held frame). Lossless drape states `assets/hero/drape/hero-drape-{terrain,thm01,alt01,priority}-1920.png` and relief-rise frames `hero-rise-f278…f290-1920.webp` (WebP lossless), composited by the page over the held frame. The earlier single `orbgss-hero.webm` / `.mp4` pair is deleted. |
| Produced by | The accepted WEB-HERO-001 Blender production lane (`hero/`), scene `hero_production_kizildere`, carried forward from `feat/web-hero-001-predata-scene@e95fdcac7cac82e597d40dab4cdc96ce1a6b319e`; visual treatment revised under WEB-005A / MER-107 (`tasks/WEB-005A_HERO_VISUAL_FIDELITY.md`) |
| Recorded in | `sources.json` → `web_005.hero_media`, `web_005.hero_drape_states` and `web_005.hero_relief_rise`. Render and encode evidence: `hero/evidence/production_media.json` and `hero/evidence/responsive_media.json` (MER-216). |
| Underlying texture rights | NASA Earth Observatory imagery, public domain, recorded with checksums in `hero/assets/manifest.json`: since WEB-005A R2 the Blue Marble Next Generation July 2004 global composite with topography and bathymetry (21600 × 10800), a lossless OrbGSS crop of its 500 m C1 tile (8160 × 5520, lon 12–46 E / lat 27–50 N) as the regional detail window, the Blue Marble 8192 cloud composite, and the Earth-at-Night 2012 composite. Rights basis: NASA media usage guidelines (`https://www.nasa.gov/nasa-brand-center/images-and-media/`); no NASA insignia is used and no endorsement is implied. Since WEB-005A R3 the regional hold additionally multiplies the Blue Marble albedo by a greyscale **detail ratio derived from Copernicus Sentinel-2 L2A** (tiles T35SPC/T35SPB, 2025-09-25; `hero/assets/source/s2_kizildere_detail_30m.png`, record `hero/evidence/earth_detail_sharpen.json`): 30 m broadband reflectance divided by its own 510 m blur, so only ground structure is carried and no colour, season or value. Copernicus Sentinel data are free, full and open (Legal Notice on the use of Copernicus Sentinel Data and Service Information); the required attribution *Contains modified Copernicus Sentinel data (2025)* is carried by the site footer. The source tiles are not copied into this repository. The ratio texture has no units and no palette, is not a measured layer and is never delivered to the page. The satellite is a procedural OrbGSS original and introduces no external asset. |
| Permitted edits | Re-render or re-encode from the accepted scene definition. The scene is configuration, so a change is a config change with a diff, not a retouch. |
| Extra duties | The caption must say it is a render. `scene.hero.kind` carries "Rendered orbital sequence — not sensor imagery" in EN and TR, and that wording is not optional. |

The honesty rule for class C is the mirror of the one for class B. Class B must never be made to
look prettier than the science; class C must never be allowed to look like measurement. It shows
where OrbGSS is pointed, not what any instrument recorded.

**No scientific raster is baked into class C.** The hero's real-data result handoff is a page
element carrying the accepted class-B derivative as its own checksummed file. The drape and rise states
carry the MER-108 hero display textures only as lossless stills, never inside the video. A governed raster
inside a lossy video encode would have its colours and values changed by chroma subsampling and
quantisation, which the accepted package forbids — so the encoder never sees one.

## Brand assets — OrbGSS identity files (MER-279; replaced by the Heat Trace package, 2026-10-25)

First-party artwork supplied by the CTO as the final identity, "Heat Trace" (`OrbGSS Logo Tasarım4.zip`, SHA-256 `cc5f769be1007a4929618237203218b94319454325188b8ea409fd53ee625635`, folder `Final_v3/`; `Final_v2/` and the earlier Agate package are superseded and not used). Not Earth-observation imagery and not a data product: no source-data rights apply, and none are claimed beyond OrbGSS's own authorship.

- **Shipped:** the horizontal logo for light grounds (header and footer are white), the favicon tile (SVG), `favicon.ico` (16, 32, 48 px), the 180 px touch icon and the 192 / 512 px manifest icons, under `assets/brand/` (and `favicon.ico` at the site root). `assets/brand/brand.json` records, for each file, the package source path and SHA-256, the shipped path, SHA-256 and size, and the one transform applied.
- **Transform:** the embedded C2PA `<metadata>` element of each SVG (an 8 KB provenance manifest that no browser reads and that cannot verify once a file changes) and its `xmlns:c2pa` declaration are removed; PNG and ICO files are byte for byte. The drawing is untouched, and `scripts/build_brand_assets.py --check` proves the shipped files equal a fresh build from the package.
- **Not used:** `Final_v3/assets/illustrative-map.jpg` is a generated illustration, and so are the package's application templates (cards, slides, banners). It is not placed on any page and not shipped; the validator fails if it is. Generated imagery stays out of the production site (see the policy at the top of this file).
- **Colour:** the logo carries only Plum, Magma and Amber (plus the black and white a mask needs) and the favicon tile only Night, Mist, Magma, Amber and Glow; the validator checks every paint in each SVG. No class A or class B asset was recoloured by the rebrand.
- **Retired:** `assets/logo.svg` and `assets/mark.svg` (the previous logo and mark) are deleted.

## Resolution note

The composites are native 30 m Landsat surface reflectance. 15 m pan-sharpened Level-1 products for these acquisitions are only obtainable through USGS EarthExplorer / Machine-to-Machine access, which requires an account that was not authorized for this work. If sharper hero imagery is wanted later, that is the path; the provenance model above stays the same.

Class B has its own, harder ceiling: the accepted `kizildere_mvp_v2` grid is 1200 × 1200 cells at 30 m, and
the accepted GEO-039 renderer draws that panel at 1249 px. 1249 device pixels is therefore the maximum
honest rendered width for any cartographic asset, and no derivative in this repository exceeds it. Widening
one would invent resolution, so a larger presentation must be answered with a contained composition instead.
Each GEO-WEB-002 asset records its own `max_safe_rendered_px`.

## Deployment gate

`orbgss.com` has been public since WEB-006, and these checks held at publication. Since MER-237, only the
public site is deployed (`.vercelignore`), and the gate stays in force for every new asset:

1. Every file listed in `assets/imagery/sources.json` under `local_file` exists and passes `python scripts/validate_site.py` (done in v0.5).
2. Each image has been visually checked against its scene metadata (done in v0.5).
3. No NASA logo/identifier is embedded in any image (none: assets are generated from raw Landsat bands).
4. Keep the USGS acknowledgement in the footer. Since MER-255 the footer attribution ends in a link to `/sources/` ("Data sources and attributions"), the one page that carries every source, credit line, image credit, reference and licence notice (the MIT text of the Scientific colour maps, kept in English in both languages). Keep it complete when a source changes.
5. If a non-USGS source is introduced later, record its exact license and attribution requirement here before it enters production.
