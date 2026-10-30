# WEB Violet brand adoption — palette, marks and map rule

**Task:** brand adoption on the existing website (CTO decision of 2026-10-25, "Violet vurgu"); not a site replacement.
**Status:** **superseded on 2026-10-30 by `docs/WEB_V6_BRAND_AUTHORITY.md`** (the team and the CTO chose package `Final_v6`, the Ocean accent on Navy, Maroon and Gold); kept as history. The Violet and Amber tokens, the logo and icon files, the locator map and the `brand_checks` pins it cites were replaced. It was: **review, pending CTO acceptance.** Nothing here was published.
**Baseline:** the Heat Trace branch (`claude/project-thread-r4bx3f` at `a213731`: white header and footer, Pumice-style pages, plain-spoken copy, Heat Trace palette), which sits on the light theme, the Agate adoption (MER-279) and the Atlas integration (MER-274). This work changes the interface accent, the logo and icon files and the map rule on top of it and nothing else.
**Governs, once accepted:** the UI palette, the logo, the favicon family and the map rule. It **supersedes `docs/WEB_HEAT_TRACE_BRAND_AUTHORITY.md`** (§1 palette, §4 marks, §5 map rule, §8 checks), which stays as history, and through it the palette lines of `docs/WEB_AGATE_BRAND_AUTHORITY.md`, `docs/WEB_LIGHT_THEME_AUTHORITY.md` and `docs/WEB_ATLAS_DESIGN_AUTHORITY.md`. It changes nothing in type, fonts, the structure of the shared components, the four-act homepage, the scientific, legal, claim and content rules, the page set, the navigation, the URLs, the grounds or the light-theme page map (`docs/WEB_LIGHT_THEME_AUTHORITY.md` §1).
**Package:** `OrbGSS_Brand_Tasarim_Final.zip` (SHA-256 `b8869634…c675`), folder `Final_v4/` ("5c symbol and wordmark with a Violet interface accent"). The zip also carries `Final_v2/`, `Final_v3/` and the older Agate `final/`; those are superseded and not used (the CTO named `Final_v4` the authority where folders conflict).

## 0. Özet (CTO için)

* **Renk:** Heat Trace'in pembe Magma vurgusu gitti. Tek etkileşim rengi artık Mor (Violet) `#854AA6`: bağlantı, aktif menü, odak halkası. Koyu zeminde okunsun diye açık eşi `#AB7CC7`. Amber `#FFA323` ölçülü vurgu olarak kaldı (çizgi ve etiket; dolgu ya da açık zeminde yazı değil), koyu zeminde de aynı değer (paket artık tek amber veriyor, eski `#FFAA2E` bitti). Magma `#E43386` ve Plum `#371641` yalnız logoda; arayüzde yok.
* **Logo ve ikonlar:** Başlık ve altlıkta yeni yatay logo (Plum yazı, Plum dış yörünge, Amber iç yörünge ve küre, Magma dikey yörünge). Favicon, dokunma ikonu, 192 / 512 ikonlar ve `favicon.ico` paketten birebir (yalnız gömülü C2PA künyesi atıldı), Night zeminli.
* **Harita:** Paketin harita kuralı: haritaya marka rengi çizilmez (bilimsel renk skalaları mordan sarıya gider; Mor ya da Amber haritada veri gibi okunur). İlgi alanı beyaz kesikli çizgi ve koyu hale oldu; Kızıldere konum haritası bu kuralla yeniden üretildi. Ana sayfada Act 4 hedef çerçevesi de aynı kuralla beyaz oldu (önceden Magma'ydı).
* **Kontrast:** Mor açık zeminde 5.49–5.95:1, koyu zeminde 5.00–5.90:1; odak halkası en az 5.49:1. Tarayıcıda 13 sayfa × iki ekran genişliğinde yazı kontrastı ölçüldü (§3); eşiğin altında çıkan olmadı.
* **Değişmeyenler:** Dört perdeli ana sayfa, gerçek uydu görüntüleri, bilimsel rasterlar (hiçbirine dokunulmadı), hero videosu, metinler, menü, adresler, **yazı tipleri**.
* **Yazı tipi uyarısı:** Paket Mona Sans ve Martian Mono adlarını veriyor ve `fonts/` altında dosyalarını getiriyor. Site kendi OrbGSS Sans / Mono'sunu (Plex alt kümeleri) koruyor. Yazı tipi değişikliği ayrı iş (lisans, alt küme, yerleşim ölçümü) ve senin kararın; §9.
* **Senin kararın gereken:** §9.

## 1. Palette — the only UI colours

Defined once in `:root` of `styles.css`; `scripts/validate_site.py` pins every value (`BRAND_TOKENS`) and recomputes every contrast pair below.

| Token | Value | Role | Contrast (computed) |
| --- | --- | --- | --- |
| `--ink` | `#2D1B30` | text on light grounds and the dark caption tone (the brand's Pumice theme text colour; Plum itself is the wordmark's colour) | on Pumice 14.78:1, white 16.02:1, Mist 14.17:1 |
| `--muted` | `#756D76` | secondary text and lines on light grounds | on Pumice 4.61:1, white 4.99:1 |
| `--violet` | `#854AA6` | Violet on light grounds: links, active state, focus ring (the brand's Pumice accent) | on Pumice 5.49:1, white 5.95:1, Mist 5.27:1 |
| `--amber` | `#FFA323` | Amber on light grounds: rules and marks, **never text** (2.00:1 on white) | |
| `--mist` | `#F5EFF7` | the brand's dark-ground wordmark colour: primary text on dark, the light caption tone | on Night 17.01:1, Night lift 14.43:1 |
| `--mist-soft` | `#C3BAC5` | secondary text and captions on dark | on Night 10.21:1, Night lift 8.66:1 |
| `--violet-light` | `#AB7CC7` | Violet on dark (the Obsidian accent, violet-300): links, active nav, focus ring | on Night 5.90:1, Night lift 5.00:1 |
| `--amber-light` | `#FFA323` | Amber on dark: limits, data gaps (the package gives one Amber for both grounds) | on Night 9.63:1, Night lift 8.17:1 |
| `--night` | `#160A19` | the dark ground (the brand's Night) | |
| `--night-lift` | `#241E25` | the dark step: the Act 4 stage, the Mining / Marine bands (the Obsidian raised surface) | |
| `--pumice` | `#F7F5F8` | the light ground (the brand's Pumice) | |
| `--white` | `#FFFFFF` | the header, the footer, the light cards and the map / figure area-of-interest line | Ink 16.02:1, Ink soft 7.40:1, Muted 4.99:1, Violet 5.95:1, Amber ink 5.18:1 |
| `--ink-soft` | `#5D525F` | secondary text on light grounds | on Pumice 6.83:1, white 7.40:1 |
| `--amber-ink` | `#A15C13` | Amber as text on light grounds (the data-gap label; the brand's "amber text in Pumice") | on Pumice 4.78:1, white 5.18:1 |
| `--rule`, `--rule-soft` | `rgba(195,186,197,.22)` / `.11` | lines on dark (Mist soft) | |
| `--rule-paper`, `--rule-paper-soft` | `rgba(117,109,118,.30)` / `.15` | lines on light grounds (Muted) | |

The values are the brand's own (`Final_v4/tokens/orbgss-tokens.css`); `--night-lift`, `--ink-soft`, `--amber-ink` and the two rule families are neutral steps from the same file. The package's hover and pressed tones (`#763B96`, `#662F84`, `#B88ED2`, `#9B6DB7`) and wash (`#F6ECFC`) are not tokens here: the site never had accent-coloured hover or pressed states (a link's hover sets `--fg`), and the hover wash is the accent at 7 % alpha (`--wash`).

**Rules.**

1. **Nothing else is a UI colour.** The stylesheet, `<style>` blocks and inline styles may use the tokens' hexes, `rgba()` of a palette triple at any alpha, `transparent` and `currentColor`. Every other hex, `rgb()` of anything else, `hsl()`, `color-mix()` and every CSS named colour fails the validator. Images are exempt: rasters, the hero video and the SVG files are checked on their own terms (§4, §6).
2. **Violet is the interactive accent, and only that.** Links, the active navigation item, the focus ring (2 px) and control states. It is never a data colour and never marks an area of interest.
3. **Amber is a restrained highlight, never a fill and never body text on a light ground.** A line, a label, a mark: the data-gap label, rules. The validator fails any rule that fills a background with an amber value or with `--limit`. On light grounds amber text is `--amber-ink`; `--amber` is only a line there.
4. **Plum and Magma are logo-only.** Plum is the wordmark and outer orbit on light grounds; Magma is the vertical orbit. No UI colour is Plum or Magma. The Heat Trace tokens `--magma` and `--magma-light` are retired and fail the validator if they return, together with the Agate, Atlas and earlier retired names.
5. **No cyan, no teal, no copper, no navy surface, no gradient accent.**
6. **Scientific colour maps are not part of this system.** No UI colour goes inside a figure frame, and no CSS filter, transform or upscale goes on a governed raster. No analytical raster, hero frame or photograph was re-coloured by this work. The brand notes that viridis-style ramps start in violet, so a violet UI mark beside a figure could read as data; the accent stays outside frames, and the area-of-interest line is white (§5).
7. **Ground-aware roles are unchanged.** Components take `--fg`, `--fg-2`, `--link`, `--limit`, `--limit-line`, `--hair`, `--hair-soft`, `--surface`, `--matte`, `--wash` from the ground, so one component reads correctly on dark and on light. `--wash` is the accent at 7 % alpha (`rgba(171,124,199,.07)` on dark, `rgba(133,74,166,.07)` on light).
8. **Caption tone.** The per-panel `data-label-tone` stays: the light tone is Mist with a Night halo, the dark tone is Ink. Mist and Ink did not change, so `CAPTION_TONE_CROSSOVER` in `script.js` stays 0.1967; the validator derives it from the two caption tokens and fails a stale value.

## 2. Grounds

Unchanged (`docs/WEB_HEAT_TRACE_BRAND_AUTHORITY.md` §2): `ground-orbit` is the dark ground (Night), `ground-lift` the lifted step (Night lift), `ground-paper` the light ground (Pumice); the header and footer are white and carry the light-ground logo.

## 3. Interaction states and measured contrast

Measured in the browser (headless Chromium) on all 13 routes, English and Turkish, at 1440 and 390 px (`evidence/heat_trace/measure_contrast.py`, run with `--out evidence/violet/measurements/contrast_audit.json`; focus and hover in `states.json`, overflow and console in `overflow.json`); the figures are in `tasks/VIOLET_EVIDENCE.md`.

* **Rest:** primary text Ink on light and Mist on dark; secondary text Ink soft / Mist soft; links and kickers Violet / Violet light; limits Amber ink / Amber light.
* **Hover:** a navigation link rises from Ink soft to Ink; a body link takes the foreground; the ghost button fills with Mist and sets its label in Ink (14.17:1; never amber, never violet).
* **Focus:** `:focus-visible` draws a 2 px outline: Violet on light grounds (5.95:1 on white, 5.49:1 on Pumice), Violet light on dark grounds (5.90:1 on Night, 5.00:1 on Night lift). The skip link shows its own Pumice chip with the Violet ring.
* **Reduced motion and the mobile navigation:** unchanged.

## 4. Brand marks

Built by `scripts/build_brand_assets.py --source <Final_v4/>` from the package; recorded in `assets/brand/brand.json`; recomputed by the validator on every run.

| Role | Shipped file | Used for |
| --- | --- | --- |
| `logo-light` | `assets/brand/orbgss-logo-light.f613dc85.svg` (viewBox 619.41 × 144; markup `width="619" height="144"`) | header and footer, every page, white ground |
| `favicon` | `assets/brand/orbgss-favicon.03c5e667.svg` | `<link rel="icon" type="image/svg+xml">`: Night tile, dark-ground symbol (outer orbit Mist at 32 px) |
| `favicon-ico` | `/favicon.ico` (16, 32, 48 px, byte for byte) | `<link rel="icon" href="/favicon.ico" sizes="32x32">` and the root path browsers ask for |
| `apple-touch-icon` | `assets/brand/orbgss-apple-touch-icon.57501a4a.png` (180) | `<link rel="apple-touch-icon">` |
| `icon-192`, `icon-512` | `assets/brand/orbgss-icon-192.59e724fd.png`, `orbgss-icon-512.e0404e64.png` | `site.webmanifest` |

* **What changed from Heat Trace.** The light-ground logo's vertical orbit is Magma `#E43386` (it was `#CD1B74`), the orb is Amber (the Glow orb is gone), and the dark-ground favicon carries Mist, Amber and Magma only. Marks are otherwise the same lock-up, same viewBox, same sizes.
* **Hash names.** `/assets/` is served `immutable` for a year, so a changed logo must be a new file name: `<stem>.<first 8 of SHA-256>.<ext>`. The validator checks the name against the content; the Heat Trace files are deleted.
* **One change to the supplied SVGs.** Each carries an embedded C2PA `<metadata>` provenance manifest that no browser reads and that no longer verifies once a file is touched; it and its `xmlns:c2pa` declaration are removed. The drawing is not touched. The validator proves that every paint in a shipped SVG is a brand colour for its ground (the light-ground logo: Plum, Amber, Magma, and the black and white a mask needs; the favicon: Night, Mist, Violet, Magma, Amber) and that no script, text, embedded image or link is present. PNGs and the `.ico` are copied byte for byte.
* **Markup, theme colour, minimum width:** unchanged from Heat Trace §4 (header logo 138 × 32 px, 120 × 28 px at ≤ 560 px; `theme-color` and manifest colours white `#FFFFFF`; the validator fails under 120 px).
* **Not used:** `Final_v4/assets/illustrative-map.jpg` (a generated illustration), the application templates, the stacked logos, the Tauri set and the font files. The brand's rule "not on maps or busy imagery" holds: the logo is not placed on a photograph.

## 5. The map rule

From the brand package: no brand colour is drawn on the map, because viridis starts in violet and ends in yellow and a Violet or Amber mark would read as data; the selected area of interest is a white dashed line with a dark halo (`--ogs-map-callout: #FFFFFF`, `--ogs-map-callout-halo: rgba(22,10,25,.7)`). `scripts/build_locator_map.py` applies it to the Kızıldere locator map: the same Night-family neutrals as before (sea `#110C12`, neighbouring land `#1C161D`, Türkiye `#241E25` with a `#69646A` outline), the 36 km area as a dashed white callout (`#FFFFFF`, a 14 % fill, a 2 px line, dash 6 3) inside a 5 px Night halo (`#160A19` at 70 %). Same Natural Earth source (v5.1.2, SHA-256 `3e458fc0…`) and projection, byte-identical geometry; the file is `assets/maps/kizildere-locator-19b40fa0.svg` (the old file is removed) and its record in `assets/imagery/sources.json` (`web_m6.locator_map`) carries the new bytes and SHA-256. The validator checks the SVG for the six map colours, exactly one white callout that is dashed with the 70 % Night halo, and fails any brand colour. The homepage Act 4 target frame follows the same rule: white corners.

## 6. What the hero does and does not do

Unchanged from Heat Trace §6: the hero video (class C, a rendered orbital sequence) is render content, not UI, and is not recoloured; the overlay shade is derived on Night. Its baked pale-cyan reticle and orbit trail remain (§7).

## 7. Residuals the CTO should know

* **Hero video.** The video's own space is still navy-black and its area-of-interest reticle and orbit trail are baked pale cyan, which matches neither Night nor the brand's white AOI line. The left shade covers the space on the homepage; a complete match means re-rendering the hero (`hero/config/scene.json`, local Blender production), a separate decision and task.
* **Fonts.** The package names Mona Sans (text) and Martian Mono (data), ships their variable TTFs and a `fonts.css`, and draws the wordmark from Mona Sans Display Expanded Medium (outlined, so the logo needs no font). The site keeps its self-hosted OrbGSS Sans / Mono (renamed IBM Plex subsets). A type change needs its own licence entry, WOFF2 subsets and a layout re-measure (§9).
* **Violet beside figures.** The Act 3 and Act 4 ramps start in violet/purple. Violet UI text appears only outside figure frames (links, the Act 4 definition labels under the map), never inside one.
* **Social image.** `og:image` is still the hero poster; a branded card is optional.
* **Icon files are the supplied ones.** The manifest declares `purpose: any` only; no maskable variant was supplied. The small Amber orbit and orb are weak on white at small sizes (the brand's own note); the header logo is at least 120 px wide and the favicon uses the Night tile.
* **Supplied SVG metadata.** The stripped C2PA block is a "provided by Claude" content credential on the supplied files; the CEO/COO own any trademark question.
* **GitHub is public.** Working notes in the repository stay readable there (unchanged); this work adds none to a deployed page.

## 8. What the validator enforces

`scripts/validate_site.py` (the brand checks are `brand_checks`, the palette checks the Atlas foundation's, on `BRAND_TOKENS`):

1. every palette token, defined once in `:root`, exactly; the 19 text/ground contrast pairs against their floors (7:1 for the main roles, 4.5:1 for the accent and the secondary tones);
2. no other colour literal in `styles.css`, any `<style>` block or any inline style; no retired token (Heat Trace `--magma` / `--magma-light`, Agate, Atlas and older names); no amber fill;
3. `assets/brand/brand.json` records the Violet identity, the approved palette (the six brand colours and the two UI forms of Violet) and exactly the seven roles, with source and shipped SHA-256, size and name-by-hash for each; no unrecorded file in `assets/brand/`;
4. each SVG paints only brand colours for its ground (the light-ground logo must carry Plum, Amber and Magma) and holds no metadata, script, text, image or link; the logo's viewBox is `0 0 619.41 144`; each PNG is a plain PNG of the right size; `favicon.ico` holds 16, 32 and 48 px;
5. every page's head carries the favicon links, the touch icon and the white `theme-color`; the header and footer brand markup is exactly as in §4; `.brand-logo` never goes under 120 px wide;
6. `site.webmanifest` icons and colours; `favicon.ico` is in `.vercelignore`; the illustrative map is not placed or shipped;
7. the locator map follows the map rule (§5);
8. `CAPTION_TONE_CROSSOVER` in `script.js` equals the value derived from the Mist and Ink tokens;
9. the Act 4 target frame is white; the skip link's focus ring and the paper ground's link colour are Violet.

`scripts/negative_tests_brand.py` breaks each of those in memory, and the suites of earlier tasks were moved to the new tokens, files and messages; run them one at a time in a detached worktree (`tasks/VIOLET_EVIDENCE.md`).

## 9. Handed over, and for the CTO

* **Fonts (open):** keep OrbGSS Sans / Mono (Plex), or move to the brand's Mona Sans / Martian Mono. Recommendation: keep Plex for now and decide with the product design; the type change is its own task.
* **Hero (open):** re-render the hero on a Night space with a white or no reticle, or leave it (§7). Recommendation: leave it unless the seam or the cyan reticle bothers you on a real screen.
* **Social card (open):** whether to add a Night OG card with the logo.
* **Acceptance:** of the Violet colours, the logo and icons, and the new locator map as the published look, then the separate authorization to publish.
* **No change to the Atlas open items.** A1 (MER-151 derivatives full-size on the Geothermal page), the CTO's reading of the new Turkish copy, the font and colour-map licence links and the empty MER-242 slots stay exactly as `docs/WEB_ATLAS_DESIGN_AUTHORITY.md` §8 left them.
* **Nothing here is merged, deployed or on the public domain.**
