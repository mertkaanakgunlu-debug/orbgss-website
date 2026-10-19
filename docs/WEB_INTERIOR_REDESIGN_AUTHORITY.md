# WEB interior redesign — presentation authority

**Task:** MER-255 (premium multi-page visual redesign of the non-home pages)
**Status:** decided by the implementation task under the design authority the CTO delegated for it (task brief, 2026-10-19). It becomes binding on the CTO's acceptance of the MER-255 review; until then the published site (`main`) is unchanged.
**Baseline:** `main@81d1f911` plus the unpublished MER-241 branch (`claude/mer-241-turkish-static-pages-sihwiy@f071751b`), because the Turkish generator and the VirgaSoft removal are part of what the redesign builds on.
**Wins over `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` where they disagree about how the five interior routes are presented** (§2 below). It changes nothing in the scientific, legal and claim rules: those stay as `CLAUDE.md` and the M6 document state them.
**Evidence:** `tasks/MER-255_EVIDENCE.md`.

## 0. Özet (CTO için)

* **Ne değişti:** Solutions, Geothermal, About ve Partner artık birbirine benzeyen tablo şablonları değil; her birinin kendi açılışı var (Solutions: durum defteri; Geothermal: Kızıldere şeridi; About: yörünge motifi; Partner: tek görsel + e-posta; Sources: kayıt defteri). Anasayfanın dört bölümü aynen duruyor.
* **Tablolar kalktı.** Karşılaştırma ve referans içeriği çizgili listelere, numaralı katman listesine ve kayıt kartlarına taşındı. Bilgi kaybı yok: durum etiketleri, uyarılar, kaynaklar ve lisanslar yerinde.
* **Kaynaklar ve atıflar** `/about/#sources` tablosundan çıkıp kendi sayfasına taşındı: `/sources/` (TR: `/tr/kaynaklar/`). Altbilgideki sade bir bağlantıyla ulaşılıyor, her görselin altında yerel alt yazısı var, About'ta kısa bir güven notu kaldı.
* **Geothermal'da yeni bilimsel görsel yok.** MER-242 (Science türevleri) gelmediği için öncelik haritası ve ikinci alterasyon göstergesi yine sayfada değil; katman hikâyesi doğal renkli Landsat kırpımları, "şema" olarak etiketli boş çerçeveli bir katman diyagramı ve renksiz 0–100 cetveliyle anlatılıyor.
* **Senin kararın gereken:** §8.

## 1. What the redesign answers

The CTO's review found the interior pages to be text-and-table templates: weak hierarchy, large empty areas, little imagery, and the same rhythm on every page. The `/about/#sources` table was the most criticised block. The target is a premium, scientific, dark-navy look with controlled cyan; large meaningful Earth-observation imagery; editorial composition; subtle motion only; consistent but not uniform pages. The homepage's four acts, its hero and its inspection aid are not touched.

**Research basis, stated honestly.** The reference sites (seequent.com, planet.com, mapbox.com, esri.com, carto.com) could not be fetched: the build container's network allowlist refuses them (`getaddrinfo ENOTFOUND`). Web search returned link lists, not page content. The principles below are therefore general practice for premium B2B geospatial sites, written down as principles and checked against nothing those sites currently show. Nothing is copied from any of them.

Principles applied:

1. **One dominant image per page, chosen for what it says.** The page's job is carried by a photograph of the ground it is about, not by decoration.
2. **A different opening for each page.** Consistency comes from the shared grammar (ground, type, numerals, rules, captions); the composition of each page's first screen is its own.
3. **Records instead of grids.** Status, sources and layers are ruled lists with a numeral and one line each. Comparison is read down a list, not across a table.
4. **Attribution is information architecture, not a footnote.** Credit on the image, a trust note where a reader doubts, one organised page for everything else, one sober footer link.
5. **No chrome that looks like data.** No dashboard, HUD, pins, glass or gradient washes; a diagram that is not data says so in its caption.

## 2. Accepted decisions this document revises

| M6 / earlier decision | Where | What changes | Why |
| --- | --- | --- | --- |
| Tables as lead elements and as the comparison form | M6 R4, §4.2 S1, §4.3 G1/G2/G5, §4.4 A1/A2, §4.5 P1 | **D2.** Tables are retired on the interior routes. Leads may also be a statement or a marked set of records (`lead-set`, `lead-statement`). `scripts/validate_site.py` fails on any `<table>` on those routes. | CTO feedback; a table of three rows or a 6-row sources register reads as a spreadsheet. The same facts survive as a state ledger, a fact list, a numbered layer list, a principle list, a route list and source records. |
| R2: a thumbnail sits "inside an index table or a card that links to its home" | M6 R2 | The credit register on `/sources/` is an index; its thumbnails (at most 160 CSS px, lazy, recorded, with alt text in both languages) need not link to the visual's home. | The register's job is to say which source an image comes from; a link per thumbnail would add nothing. |
| R5 table-cell budget | M6 R5 | The 12-word cell budget now governs the one-line mono labels that replaced cells (`layer-meta`, `layer-pending`). The Sources page budget is 450 words (Geothermal stays 350). | Tables are gone; the sources register is names, uses and one-line labels. |
| R6 fixed texts | M6 R6 | Credit lines, citations, DOIs, image-credit lines and licence text on `/sources/` are fixed texts (class `source-fixed`): exempt from R1 and R5. | They are attribution and licence notices fixed by their sources, like the footer attribution. |
| One home page per fact (R1) for sources | M6 §4.4 A2, §4.1 footer | **D3.** Source credits move from `/about/#sources` to the new `/sources/`. About keeps a short trust note under the same anchor `#sources` (so old links still land on it) with the six source names and a link. The footer attribution sentence ends in the link "Data sources and attributions" → `/sources/` on every page. | Source data, image credit, academic references and software licences are different kinds of information; one table mixed them. |
| Page set of five | M6 §2 | Six routes: `/sources/` (EN) and `/tr/kaynaklar/` (TR slug, same rule as D2). It is in the footer and in the sitemap, not in the primary navigation. | A reference page should be findable and sober, not promoted. |
| Mining and Marine as full-bleed bands | M6 §4.2 S3/S4 | The two expansion directions are two image-led ruled panels under one heading "Expansion directions", after the Geothermal full-bleed band. Same photographs, same captions, same status label, same footnote. | Geothermal is the one active, published application and must be the page's dominant visual; two more full-bleed bands gave the unpublished directions the same weight. See §8 (decision 2). |
| Geothermal G1/G2/G5 as tables | M6 §4.3 | G1 → "One area, one grid" (figure + fact list). G2 → "Every layer, and what it is not" (layer diagram + numbered list, each layer with its mandatory warning). G5 "What the pilot produced" is dropped as a section: its rows restated the layers and the priority (R1). | R1 and the CTO's "less text, fewer tables" |

**Not revised** (still binding exactly as `CLAUDE.md` states): the four homepage acts; the score name and its AOI-relative definition; every mandatory scientific warning and the data-gap statement; the sensor-imagery / render distinction and the bottom-right caption rule; Class B raster rules (MER-151 derivatives are homepage-only); the taxonomy and "Expansion direction" label (R8); claim discipline (R7); no form, backend, CRM, analytics or cookies; static HTML, CSS and vanilla JavaScript; the MER-241 generation mechanism for `/tr/`; the VirgaSoft ban; `IMAGERY_RIGHTS.md` and `assets/imagery/sources.json` as the imagery authorities.

## 3. Page compositions

Each page has a different first screen. Below the first screen they share one grammar: numbered chapter heads (`01`, `02`…) beside their lead visual, ruled lists, mono captions, cyan used sparingly (numerals, kickers, the active state).

| Page | Opening | Lead visual of each chapter | Notes |
| --- | --- | --- | --- |
| `/solutions/` | **State ledger:** three ruled rows (Geothermal leading, with the cyan top rule; Mining; Marine), each a link to its section: name, status label, what is published. | Geothermal full-bleed band (Yellowstone, existing derivative); two expansion panels (Chuquicamata, Ili Delta; existing derivatives). | The comparison table is replaced by the ledger: purpose is in the panel line ("Mineral exploration targets", "Coastal and marine ground"), status in the label, the path in the link. Mining and Marine carry no capability, evidence or maturity claim: "Nothing published yet". |
| `/solutions/geothermal/` | **Stage:** a 1600 px strip of the Büyük Menderes graben (class A crop `kizildere-stage`) behind the headline; two-row composition on phones. | Locator map; the analysis area crop with a fact list; a layer diagram with the numbered layer list; the 0–100 ruler; the empty structure/geology frame. | Follows the brief's axis: where the pilot is → area and grid → layers → what each layer is not → the AOI-relative priority and its limits → the structure/geology gap. |
| `/about/` | **Statement:** the brand's thin orbital motif behind the headline (no globe in the mark). | A Kızıldere crop (`kizildere-terrain`); a statement; a six-principle numbered list; the source-names trust note. | Company character only. No team history, founding date, headcount, certificates, investment, partnerships or references; no VirgaSoft; no unannounced legal name. |
| `/partner/` | **Split:** headline and one photograph (`kizildere-valley`). | Route list (pilot, partnership, technical: three `mailto:` links with their own subjects); the address set large. | An invitation, not a contact table. No form. |
| `/sources/` | **Register:** a section index (data, images, references, licences). | Source records; image credits with thumbnails; references with DOIs; terms per source and the MIT text. | Every source, credit line, reference and licence of the old About table is kept (§5). |

Layer diagram rule: the Geothermal layer diagram is a **schematic**. Its frames are empty except the natural-colour base frame, which is a Class A crop; its caption begins "Schematic" and says the frames are empty. No frame paints data. The 0–100 ruler is hairlines in neutral tokens and the two numbers 0 and 100; it carries the public label of the score and no colour ramp.

## 4. Imagery

* **New assets are four Class A crops** of the accepted WEB-005B Act 2 master (`assets/imagery/kizildere-aoi-context-2025-natural.jpg`, USGS Landsat 8 OLI, public domain), built by `scripts/build_interior_crops.py` and recorded in `assets/imagery/sources.json` → `web_m6.interior_crops` with parent checksum, crop box, per-file SHA-256, content-hash file names, the rights basis and the overlap with the analysis grid. A crop is a crop and an encode: no tone, colour, sharpening, upscaling or generative step. Names: `kizildere-stage` (Geothermal), `kizildere-aoi` (Geothermal), `kizildere-terrain` (About), `kizildere-valley` (Partner).
* Each crop is a distinct recorded visual shown full size on one page (R2). The Act 2 frame stays the homepage's.
* The valley crop includes the western part of the analysis grid; its alt text therefore says "in the south-west of the Kızıldere context view", not "west of the analysis area". The record carries the overlap so the claim stays checkable.
* **Nothing is drawn above its own pixels.** A figure's CSS width cap at 2× never exceeds the crop's widest derivative (checked statically by the validator) and a real-browser run (`scripts/measure_interior_renders.py`) measures every interior photograph at 19 viewport widths (360–3840) at DPR 1 and 2 and records the worst drawn-to-candidate ratio next to each asset (current worst 1.00; the bound is 1.01 for rounding). `sizes` attributes follow the cover-cropped drawn width, not the viewport.
* Existing derivatives (Yellowstone, Chuquicamata, Ili Delta, the locator map, the hero poster, the Act 2 derivatives) are reused unchanged; the Sources page shows them as thumbnails of at most 160 CSS px.
* **MER-242 stance (D1 unchanged).** No MER-151 or GEO-WEB-002 derivative appears on the Geothermal page (validator-enforced). The priority-over-relief figure and the iron proxy stay absent; the iron layer reads "Accepted, not shown yet". When Science delivers accepted derivatives, they come in as new records under their own task.

## 5. Sources and attributions

The old About table is split by kind of information; nothing was dropped.

| Kind | Where | What it holds |
| --- | --- | --- |
| Trust | `/about/#sources` | One sentence and the six source names, linking to `/sources/`. |
| Local credit | each image; every page footer | The bottom-right caption (place, coordinates, kind), unchanged. The footer attribution is now two sentences, "Landsat data courtesy of the U.S. Geological Survey. Contains modified Copernicus Sentinel data (2025).", followed by the link "Data sources and attributions". It used to be one long sentence that also named NASA Blue Marble, NASADEM and the Scientific colour maps; those credits are now on `/sources/` (§8, decision 3). |
| Source data | `/sources/#data` | Landsat 8/9 (USGS), NASADEM (NASA JPL / Land Processes DAAC), Copernicus Sentinel-2, NASA Earth Observatory imagery, Natural Earth, Scientific colour maps (Crameri). Each: what it is used for, the credit line, the official page. |
| Image credits | `/sources/#images` | Hero, Kızıldere, Yellowstone, Chuquicamata, Ili Delta, locator map, evidence and priority maps: thumbnail, what it shows, scene and acquisition, source. |
| References | `/sources/#references` | Crameri et al. 2020 (doi:10.1038/s41467-020-19160-7), Crameri 2023 v8.0 (doi:10.5281/zenodo.8035877), NASADEM (doi:10.5067/MEaSUREs/NASADEM/NASADEM_HGT.001). |
| Licences and notices | `/sources/#licences` | Terms per source with the official policy link; the MIT licence text of the Scientific colour maps, in English in both languages (the binding text) with its copyright line. |

The validator checks: the six source records and their official links; the credit-line wording; the three reference DOIs; every external link is `https` with `target="_blank" rel="noopener"`; the MIT text equals the standard text in both languages; the footer link exists on every page; `IMAGERY_RIGHTS.md` mentions every crop.

**Not verified from the build environment:** the container cannot reach zenodo.org, github.com or any reference site, so the exact copyright line of the Scientific colour maps licence file ("Copyright (c) 2023, Fabio Crameri") and the live state of the external links were not checked. The page carries a source comment marking it; this is listed in §8.

## 6. Turkish

The Turkish pages are generated, not edited: `scripts/build_tr_pages.py` renders `/tr/cozumler/`, `/tr/cozumler/jeotermal/`, `/tr/hakkimizda/`, `/tr/is-birligi/` and the new `/tr/kaynaklar/` from the English pages and the `script.js` dictionary (MER-241 mechanism, unchanged). New strings were added in both languages together. The MIT text is English in both, with a note saying so. The sitemap carries `/sources/` and `/tr/kaynaklar/` with `hreflang` alternates.

## 7. Content budgets under this document

Headline 8 words, page intro 30, section body 40, label line 12, at most 250 budgeted words per page (Geothermal 350, Sources 450); Turkish may run 15 % longer. All of these are still enforced by `scripts/validate_site.py`.

## 8. Decisions for the CTO

1. **Geothermal layer imagery (D1).** The page tells the layer story without a governed derivative. If you want the priority surface or the iron proxy on this page, Science must deliver MER-151-family derivatives (MER-242); no agent should publish the homepage derivatives here.
2. **Mining and Marine as panels, not bands.** If you prefer two more full-bleed bands, the previous composition is one CSS and markup change; the content rules do not forbid either.
3. **Footer attribution shortened (all pages, including the homepage footer).** The long footer sentence is replaced by the two credits Landsat and Copernicus ask for in that place plus the `/sources/` link; the NASA Blue Marble, NASADEM and Scientific colour maps credits live on `/sources/` (the MIT licence text in full, which the footer sentence never carried). This follows the brief's "sober footer link" but touches the homepage footer and the way credits are placed, so it needs your yes. Reverting is a dictionary change (`footer.attribution`, EN and TR) and two lines of markup per page.
4. **Scientific colour maps licence line.** Confirm the copyright line against the licence file of the Zenodo v8.0 release before publication (not reachable from the build container).
5. **D3 (privacy / KVKK) and D5 (coastal Marine scene)** remain open and unchanged.
6. **MER-241 is not published.** This branch contains it. Publication of either needs the CTO's explicit "main'e push et".
