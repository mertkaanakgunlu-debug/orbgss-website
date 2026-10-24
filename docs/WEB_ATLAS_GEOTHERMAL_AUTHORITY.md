# WEB Atlas redesign — the Geothermal page

**Task:** MER-276 (parent MER-274). **Foundation:** MER-275, `docs/WEB_ATLAS_DESIGN_AUTHORITY.md`.
**Status:** **preview, pending CTO acceptance.** Nothing here is published. It becomes binding only when the CTO accepts the reviewed preview and authorizes a publication.
**Baseline:** `claude/project-thread-csvxkc@a477368` (MER-275 on top of MER-255, both unpublished).
**Governs, once accepted:** `/solutions/geothermal/` and `/tr/cozumler/jeotermal/`. It supersedes the MER-255 Geothermal section of `docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md` and the MER-255 "layer diagram, neutral ruler, no governed derivative" rules; every other rule stands.

## 0. Özet (CTO için)

* **Ne değişti:** Jeotermal sayfası artık "Atlas" tasarımında. Açılışta Landsat şeridi ve bir bölüm dizini; sonra açık zeminde pilot kaydı ve konum haritası; sonra koyu zeminde altı levhalık katman atlası; sonra öncelik haritası ve "ortaya koyar / koymaz" tablosu; en sonda eksik olanların listesi.
* **Senin kararın gereken (yayından önce):**
  1. **A1.** Dört MER-151 görseli (yükselti, termal, alterasyon, öncelik) ana sayfanın yanında bu sayfada da tam boy gösteriliyor. Bugün yalnızca ana sayfada duruyorlar. Önizleme için yapıldı; kabul etmezsen bu dört levha boş "henüz teslim edilmedi" çerçevesine döner.
  2. **Yeni Türkçe metin.** 38 yeni anahtar Türkçe'yi ben yazdım (liste §5). Dil kontrolünden geçmeden yayımlanmamalı.
  3. **Bilimsel iddia yok:** yeni skor, yeni sayı, yeni görsel eklenmedi. "Ortaya koymaz" listesi, öncelik uyarısının kendi kelimeleridir, yeni iddia değildir.
* **Eksik görseller:** demir oksit katmanı ve "rölyef üzerinde öncelik" Bilim'den (MER-242) gelmedi. İkisi için tam boy, kesikli çerçeveli yer tutucu duruyor. Yapı/jeoloji boşluğu yine bilinçli bir veri boşluğu.
* **Bilerek bırakılan:** eski sayfadaki `mvp_remote_sensing_priority_v1` satırı yazılım içeriği sayılır (R3), sayfada yok. Skorun kamuya açık adı yerinde.

## 1. Page sequence

| # | Section | Ground | Lead visual (R4) |
| --- | --- | --- | --- |
| 01 | Opening: stage crop, title, chapter index | Orbit, Lift for the index | the Landsat stage crop; the index list |
| 02 | `#glance` — the pilot record | Paper | the record list and the locator figure |
| 03 | `#layers` — the layer atlas | Orbit | one figure of six plates |
| 04 | `#result` — the priority plate and its legend | Orbit | the priority plate (600 CSS px max, with ramp and 10 km bar) |
| 04b | `#relief` — priority over relief | Orbit | a pending slot (A2) |
| — | the ledger: Establishes / Does not establish | Paper | the two-column set |
| 05 | `#missing` — what is missing | Lift | the index of three gaps |

The old `/pilot/` fragments (`#pilot-observe`, `#pilot-terrain`, `#pilot-evidence`, `#pilot-structure`, `#pilot-priority`, `#pilot-geothermal`) survive as `.anchor-alias` elements. `#outputs` is the result section's second id.

## 2. The atlas (A6)

One figure of small multiples, `figure.geo-atlas`, not a card grid. Six plates in a fixed order, in three states:

| Plate | State | Shows | Warning it carries (verbatim, visible) |
| --- | --- | --- | --- |
| 01 natural | evidence | the recorded natural-colour analysis-grid crop (Class A) | `act.context.note` |
| 02 elevation | evidence | MER-151 terrain derivative | `story.terrain.note` |
| 03 gap | data gap | dashed frame, no image: structure and geology | `geothermalPage.gap.copy` |
| 04 thermal | evidence | MER-151 THM-01 derivative | `act.evidence.thermal.note` |
| 05 alteration | evidence | MER-151 ALT-01 derivative | `act.evidence.alteration.note` |
| 06 iron | pending | pending frame, no image: accepted by Science, not delivered | `act.evidence.alteration.note` |

Every plate shows its number, name, role · source and its warning. Evidence plates carry the bottom-right caption (place, coordinates, layer name) and `data-label-tone`. A pending frame says "Accepted, not shown yet"; the priority-over-relief slot says "Figure to be supplied" and is styled apart from the data gap (A2, which keeps D1: nothing goes in until MER-242 delivers it).

## 3. Scientific discipline

* The four layers are the MER-151 presentation derivatives already governed in `sources.json` (`web_005b`). Nothing is re-coloured, re-classified, filtered, transformed or upscaled. Each is drawn at most 600 CSS px (native 1200 px at 2x). Measured in headless Chromium at 19 widths × DPR 1 and 2 (`scripts/measure_geothermal_renders.py`): terrain, THM-01 and ALT-01 reach 534 CSS px, priority 600 CSS px; the worst upscale is 1.000×, never above.
* The second home of each layer is recorded under `web_005b.placement[layer].geothermal_placement` with its status, acceptance ("pending"), route, plate and measured `rendered` block.
* Priority stays on the fixed 0–100 domain, shown with its legend ramp and a 10 km scale bar. The priority warning appears verbatim twice: in the result and under the relief slot.
* The ledger's "Does not establish" list is the priority warning's own seven terms, pinned in English (`not.*`). It is a warning, so it carries `beam-note`, the one place the claim words may appear.
* Structure and geology remain a deliberate data gap, score-invariant, not promoted back into an act.

## 4. What `scripts/validate_site.py` enforces (atlas:geothermal)

Only checks that exist in the region; each has a case in `scripts/negative_tests_atlas_geothermal.py`.

* Page frame: body class, every anchor id including the six aliases, the grounds of the chapters, the ledger as a paper band, the chapter-index and missing-index link targets, no "prototype" wording.
* Atlas: one figure, the six plates in order, each with number, name, role, visible warning (the key above); evidence plates have one described image, 1200 × 1200 declared, no inline style, the caption order, `data-label-tone`, `data-visual-status="product-proof"` on the four analytical plates, only the layer's own recorded derivatives, and the 600/900/1200 ladder; the gap and pending plates carry no image.
* Governed rasters: only the four MER-151 layers and the legend ramp appear on the page; no filter/transform/opacity/mix-blend/scale/zoom/clip/mask/backdrop in the region's CSS near a raster; `.plate` capped at 600 CSS px.
* Result: the priority plate, its candidate set, caption keys, legend ramp and scale bar; the verbatim priority warning in `#result` and `#relief`; the relief slot pending with no image.
* Ledger: one marked set, the two Establishes lines, the seven Does-not-establish terms in order and in English, `beam-note` on the list.
* Dictionary: every `geothermalPage.*` key used exists in both languages; none is unused; the Turkish block says its new strings await the CTO's language review.
* Placement records: each of the four layers has a `geothermal_placement` with status, an acceptance that says "pending", this route, a plate, a derivative that is the layer's own, 12 or more measured viewports, ≤ 600 CSS px, ≤ the native grid at 2x and no upscale.
* Generic checks adjusted for A1 only: a `web_005b` visual may sit on the Geothermal route besides the homepage (R2 and "homepage-only" skip exactly that route); the locator caption is found by class; the MER-255 "no governed derivative" block was removed.
* The shared foundation rules apply because the group is type-ready: no text under 10px, capitals only in label/caption size with the one tracking.

What is **not** enforced: the visual appearance of the plates, and whether the layers are scientifically "right"; Science's acceptance covers the last.

## 5. Copy

Changed or new strings sit under `geothermalPage.*` in both language blocks of `script.js`; the page and `/tr/…` are built from them (`scripts/build_tr_pages.py`). The Turkish for all 38 new keys is mine and **pending the CTO's language review**:

`title.lead`, `title.tail`, `index.aria`, `index.record`, `index.atlas`, `index.result`, `index.missing`, `fact.place`, `fact.placeValue`, `fact.score`, `fact.scoreValue`, `fact.gap`, `where.label`, `where.copy`, `plate.abbr`, `layer.structure`, `from.none`, `role.support`, `pending.asset`, `scale.bar`, `relief.kicker`, `relief.title`, `relief.copy`, `relief.state`, `relief.slot`, `ledger.title`, `ledger.establishes`, `ledger.not`, `ledger.is`, `ledger.for`, `not.probability`, `not.reserve`, `not.discovery`, `not.drilling`, `not.prospectivity`, `not.calibrated`, `not.validation`, `missing.title`.

The mandatory warnings (`act.priority.note`, `act.context.note`, `story.terrain.note`, `act.evidence.*.note`) and the scene captions are reused verbatim from the shared dictionary.

## 6. Authority changes carried by this page

| | Change | Where it lives | Status |
| --- | --- | --- | --- |
| A1 | MER-151 layers at full size on Geothermal | `geothermal_placement` records, validator hooks | preview, pending CTO acceptance |
| A2 | full-size pending slots (iron, priority over relief) | `.plate-pending`, `#iron`, `#relief` | preview, pending; nothing placed before MER-242 |
| A5 | "Does not establish" ledger | `.geo-ledger` | preview, pending |
| A6 | one atlas figure of small multiples, not a card grid | `.geo-atlas` | preview, pending |
| A7 | new and trimmed copy, EN and TR | §5 | preview, pending CTO language review |

**Deferred to the integration step** (kept out of the shared files so the sibling page threads stay conflict-free): the `CLAUDE.md` wording that moves "MER-151 derivatives: homepage only" to "homepage and Geothermal (A1)", and the matching line in `docs/WEB_ATLAS_DESIGN_AUTHORITY.md`. Until the CTO accepts A1 these two files keep describing production.

## 7. Open points

* A1 and the Turkish copy need the CTO before any publish. If A1 is declined, the four analytical plates revert to the pending frame; the validator's A1 hooks and records are then removed with them.
* MER-242 (iron layer, priority over relief) is a separate dependency; the two slots stay empty until Science's files are accepted.
* The `kizildere-stage` and `kizildere-aoi` crop records were not re-measured by this task; the measurement script of MER-255 owns them.
