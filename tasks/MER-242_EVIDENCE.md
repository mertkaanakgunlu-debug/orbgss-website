# MER-242 — Geothermal-page presentation derivatives (ALT-02, priority over relief)

**Status:** `REVIEW_READY` — files and records delivered; independent review and CTO acceptance pending. Not placed on any page, not published.
**Linear:** MER-242. **Owner:** Science (assigned by the CTO to the website workstream, 2026-10-25).
**Baseline:** `claude/project-thread-osxzu4@5c978427886d1b102c98a95b0c2d4a59e7d6d1e4`.
**Builder:** `scripts/build_mer242_presentation.py` (reuses the functions of `scripts/build_web005b_presentation.py`). **Record:** `assets/imagery/sources.json` → `mer_242`.

## 0. Özet (CTO için)

* **Ne teslim edildi:** Jeotermal sayfası için iki yeni bilimsel görsel ve Kaynaklar satırı için bir küçük resim. Pl. 06 demir alterasyonu (ALT-02) ve "rölyef üstünde öncelik". İkisi de anasayfadaki MER-151 görselleriyle aynı yönetilen export'tan (`20260917T161155Z-5e7a0e53`), aynı kodla, kayıpsız üretildi. Sayfaya henüz konmadı.
* **Bilimsel kararlar (senin kabulün gerekiyor):**
  1. ALT-02, ALT-01'in paletini kullanıyor; yazılımda ikisi zaten aynı stil (`alt_batlow_sequential`). Yeni palet seçilmedi.
  2. ALT-02'nin pencere kuralı ALT-01'in aynısı (%2–%98, gama yok).
  3. Rölyef üstü öncelik: öncelik renkleri değişmedi; MER-108'in izin verdiği en düşük opaklık (0.90) ve 3× abartılı nötr gölgeli rölyef. Rölyef en çok skorun boş olduğu dağlık alanlarda, geçerli hücrelerin altında ise hafif görünüyor. Daha güçlü bir rölyef için MER-108 kuralının (opaklık ≥ 0.90, karışım modu yok) gevşetilmesi gerekir; bunu önermiyorum.
* **Tam genişlik:** 1200 px'lik özgün ızgara 600 CSS px'e kadar 2× ekranda keskin. Daha geniş bir figür için MER-151'in büyütme yolu var ama ağır: 1800 px kayıpsız ≈ 5,9 MB, 2400 px ≈ 9,1 MB. Yayımlanmadı.

## 1. Source identity

| Surface | Governed raster (MER-113 export `20260917T161155Z-5e7a0e53`, `kizildere_mvp_v2`) | SHA-256 |
| --- | --- | --- |
| alt02 | `alt-alt02.tif` (`byte_copy_of_accepted_source`, style `alt_batlow_sequential` in `export_manifest.json`) | `7b3aa4a7c7586503df805021063d497cca7e28a31acf31222314a38d69e9bb0a` |
| relief | `score-mvp-remote-sensing-priority.tif` | `15065152f6f21eaf66236d51d6814acfb32326c5698bc2433dcb69653d8a9d1e` |
| context | `top-dem.tif` (hillshade only) | `590f74322c6ad942e0d36b79446934da7a0938c7d87c06ab8c9bd27da73fb694` |

ALT-02 is part of the same accepted export the homepage uses, so `BLOCKED_SOURCE_MASTERS` does not apply. Grid: EPSG:32635, 1200 × 1200, 30 m, origin (639270, 4223040); the builder refuses a raster whose CRS or transform differs from the DEM's. Nothing was regenerated from website PNG/WebP files.

## 2. Science decisions

| | Decision | Basis |
| --- | --- | --- |
| S1 | **ALT-02 palette** = `alt_violet_blue_cyan_green_yellow_v1` with the exact ALT-01 stops and LUT (`ed32cf67…`). | The accepted renderer gives ALT-01 and ALT-02 one style (`geothermal-prospectivity@215ef89d:src/geothermal/workbench/style_registry.py`, `LAYER_ID_ALT01` / `LAYER_ID_ALT02` → `alt_batlow_sequential`); MER-108's terminal amendment pinned the hero topology for that style. No new palette is selected, so MER-108 §12 is not reopened. |
| S2 | **ALT-02 transfer** = canonical `linear_min_max` (vmin −20.6428, vmax 303.0005), then the MER-151 §3 ALT-01 window with the ALT-01 values: `q_low 0.02`, `q_high 0.98` (span 0.96), resolved over all valid cells → [0.064266, 0.065965]; 4.0 % of valid cells clip. Gamma disabled. | 98 % of ALT-02's valid cells sit inside 0.17 % of the canonical range (outliers at both ends), so without a window the plate is one flat colour. Keeping ALT-01's exact rule keeps Pl. 05 and Pl. 06 comparable. A 0.01 / 0.99 window was tried and leaves the map flat violet; gamma 0.80 was tried and adds nothing ALT-01 does not have. |
| S3 | **ALT-02 context** = the homepage hillshade (z 1.0, az 315°, alt 45°, grey 0.07 + 0.32·hs) at analytical opacity 0.90. | Same family as Pl. 02, 04, 05. |
| S4 | **Priority over relief** = the priority LUT with no window and no gamma (priority may never be windowed), source-over at **0.90** onto a neutral hillshade of the governed DEM: z-factor **3.0**, az 315°, alt 45°, grey **0.05 + 0.55·hs**. | MER-108 `11c32e8d` §6: source-over only, priority opacity 0.90–1.00, hillshade from the governed DEM with fixed parameters. 0.90 is the most context the rule allows; 3.0 is the accepted WEB-005A hero relief exaggeration; the dark grey range keeps the context under the priority colours (a full 0–1 grey range was tried and turns the masked ridges into bright white speckle). Measured relief modulation under valid cells: 1.3–14.7 of 255 levels (p5–p95). |
| S5 | **Legends.** ALT-02 gets `alt02-legend-ed32cf67.png` (the unblended LUT; left = 2nd, right = 98th percentile of the governed cells; a dimensionless proxy, so words, not numbers). The relief figure reuses the homepage `priority-legend-ramp.png` (same LUT; position = score 0–100). | MER-108 §6: legends use unblended canonical colours. |
| S6 | **Surfaces.** MER-151's derivative family is extended to `/solutions/geothermal/` (Pl. 06 and `#relief`) and to thumbnails of at most 160 CSS px on `/sources/`, public website presentation only. | MER-242 request 3. The Pl. 02/04/05 homepage derivatives on the Geothermal page remain the separate A1 decision of `docs/WEB_ATLAS_GEOTHERMAL_AUTHORITY.md`. |
| S7 | **No enlargement published.** Ladder = native 1200 plus box downsamples. | MER-151 §2 would allow a Lanczos3 rung, measured for relief at 1800 px = 5,863,542 B and 2400 px = 9,123,660 B lossless; the homepage build declined the same rung for the same reason. |

Unchanged: every governed value, mask, NoData, CRS, grid, normalization, weight and score meaning. Not used: AI/super-resolution, scalar interpolation, smoothing, sharpening, local tone mapping, per-crop autoscaling, mask edits, blend modes, colourised or data-driven hillshade, data-dependent opacity, hotspot emphasis.

Public label and warning of record (not rendered while `public_warnings` is retired):

* ALT-02: "ALT-02 Alteration Proxy — ferric/iron" · "Broad Sentinel-2 spectral alteration proxy; not mineral identification and not proof of hydrothermal alteration."
* Relief: "Remote-Sensing Relative Priority — Experimental Baseline", over shaded NASADEM relief · "AOI-relative experimental screening only. Not probability, reserve/resource estimation, discovery likelihood, drilling-success likelihood, Full Prospectivity, or a calibrated cross-AOI score."

## 3. Outputs

`assets/proof/mer242/`, lossless WebP (`lossless=True quality=100 method=6 exact=True`), each read back and compared pixel for pixel. Names carry the first 8 hex of the SHA-256 of the native RGB pixels because `/assets/` is served immutable.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `alt02-9266ceca-600.webp` | 717,676 | `69d4217b21ef913e30ac19f66b6f9f4b5f2b791d2b6d14d6f029ea63bd1a72fd` |
| `alt02-9266ceca-900.webp` | 1,480,520 | `263ef15c6801ad06d3a3f16d74f5c3bb017b85e70abd98d4e51a386d232c098a` |
| `alt02-9266ceca-1200.webp` | 2,075,972 | `f5a12c9e7b7217fd123a5fe8603c5851496a9f94e3cee11ab104da45ddb37238` |
| `alt02-legend-ed32cf67.png` | 272 | `1010a6dd97711c218c0c688cd069239622b894f7a78faef752f48d90eee235fe` |
| `relief-55f5fc73-160.webp` (Sources thumbnail, 1×) | 57,708 | `288213960f383b3da0d1c4619059ffd12b25bf6e89d29ea1e075b6416301d559` |
| `relief-55f5fc73-320.webp` (Sources thumbnail, 2×) | 225,734 | `4723dd848ff32ce2c56b4539b1e09677dec49bb673d5bf8b7e2e9d958c868b8a` |
| `relief-55f5fc73-600.webp` | 785,302 | `11fccddf9382c4985612e76f1366efe8bee96aecf5afd7bc9e458b38f04cd439` |
| `relief-55f5fc73-900.webp` | 1,728,748 | `d1fe802d42bf83296bab093371d36bff176e4f27071c1fb7653c38fc467ec359` |
| `relief-55f5fc73-1200.webp` | 2,900,294 | `b2e17ec6321363999bc15909be98c4aa2cd6d3b59113b60b204adecfe4df5c60` |

LUT SHA-256: ALT-02 `ed32cf671a87…` (= ALT-01), relief `7babdc574d6d…` (= homepage priority; the builder stops if they drift). Valid fraction: ALT-02 0.836847, priority 0.833898. Review sheet (lossy, evidence only): `evidence/mer242/review_sheet.webp`.

## 4. Verification

| Check | Result |
| --- | --- |
| Governed source SHA-256 against the export manifest and the MER-108 pins | PASSED |
| Same environment rebuilds the four published homepage MER-151 derivatives byte for byte (LUT, 1200 and 600 of terrain, THM-01, ALT-01, priority) | PASSED (Python 3.12.13, numpy 2.5.1, rasterio 1.5.1, Pillow 12.3.0, libwebp 1.6.0) |
| Determinism: two full builds, identical SHA-256 for all 8 WebP files | PASSED |
| Lossless round trip of every WebP | PASSED |
| `python scripts/validate_site.py` with the files and the `mer_242` record | PASSED (Windows, LF checkout) |
| Placement on a page, browser render measurement, EN/TR | NOT RUN — not placed by this task |
| Independent review, CTO acceptance | NOT RUN — pending |

## 5. To place them (page work, not done here)

* Pl. 06 `#iron`: `alt02-9266ceca-{600,900,1200}.webp`, declared 1200 × 1200, the bottom-right caption and `data-label-tone` like Pl. 05, `data-visual-status="product-proof"`; the state line "Accepted, not shown yet" goes.
* `#relief`: `relief-55f5fc73-{600,900,1200}.webp` with the priority ramp; the 1200 px grid serves 600 CSS px at 2× (1200 CSS px at 1×).
* `/sources/` "Evidence and priority maps": `relief-55f5fc73-160.webp` / `-320.webp` as `.thumb`, 160 × 160.
* The `atlas:geothermal` validator region allows only `web_005b` derivatives on the page today; it has to accept `mer_242` paths (with the same checksum and bound checks) when the page binds them.

## 6. Notes

* MER-242's text asks for this record in `geothermal-prospectivity/tasks/`. It lives here, with the files, because Science now sits in the website workstream; it can be mirrored there once accepted.
* Re-running `--record` re-serializes `sources.json` and re-indents one hand-edited line of `web_m6.locator_map.colours`; the value does not change.
* On a Windows checkout with `core.autocrlf=true` the validator fails the two brand SVGs (end-of-line conversion; `.gitattributes` protects `assets/maps/*.svg` only). The blobs are correct; this run used an LF checkout.
