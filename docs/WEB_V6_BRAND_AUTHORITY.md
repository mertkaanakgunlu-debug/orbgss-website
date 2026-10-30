# WEB v6 brand adoption — palette, marks and map rule

**Task:** brand adoption on the existing website (decision of 2026-10-30: the team reviewed the candidate identities and the CTO chose package folder `Final_v6`); not a site replacement.
**Status:** **review, then publication.** The CTO's message of 2026-10-30 ("uygulayalım ve web sitesini yayınlayalım") is the authorization for one publication of this reviewed head; polish after the publication is a separate round of team review.
**Baseline:** the missing-visuals branch (`claude/project-thread-sqytba` at `4223f58`: Violet palette, white header and footer, Pumice pages, plain-spoken copy, the Landsat context scenes and the placed MER-242 figures), which sits on the Violet, Heat Trace, light-theme, Agate and Atlas work. This work changes the interface colours, the logo and icon files and the map neutrals on top of it, and nothing else.
**Governs:** the UI palette, the logo, the favicon family and the map rule. It **supersedes `docs/WEB_VIOLET_BRAND_AUTHORITY.md`** (§1 palette, §4 marks, §5 map rule, §8 checks), which stays as history, and through it the palette lines of `docs/WEB_HEAT_TRACE_BRAND_AUTHORITY.md`, `docs/WEB_AGATE_BRAND_AUTHORITY.md`, `docs/WEB_LIGHT_THEME_AUTHORITY.md` and `docs/WEB_ATLAS_DESIGN_AUTHORITY.md`. It changes nothing in type, fonts, the structure of the shared components, the four-act homepage, the scientific, legal, claim and content rules, the page set, the navigation, the URLs, the grounds or the light-theme page map (`docs/WEB_LIGHT_THEME_AUTHORITY.md` §1).
**Package:** `OrbGSS_Logo_Tasarim_Last.zip` (SHA-256 `9f1d0383…81b5`), folder `Final_v6/` ("Final_v5 with the team feedback applied: lighter, more saturated colours; lifted dark grounds; a Deep Gold inner orbit on white so the ring no longer fades"). The zip also carries `Final_v2/` to `Final_v5/` and the older Agate `final/`; those are superseded and not used.

## 0. Özet (CTO için)

* **Renk:** Mor (Violet) gitti; tek etkileşim rengi artık Okyanus (Ocean) `#006CCA` (açık zeminde bağlantı, aktif menü, odak halkası), koyu zeminde okunsun diye açık eşi `#54A4FB`. Altın (Gold) `#F8AD24` ölçülü vurgu olarak kaldı (çizgi ve etiket; dolgu ya da açık zeminde yazı değil); açık zeminde yazı gerektiğinde altın mürekkep `#9C5F00`. Lacivert (Navy), Bordo (Maroon) ve Koyu Altın (Deep Gold) yalnız logoda; arayüzde yok.
* **Koyu zemin:** Gece (Night) artık `#0D1626`, yani paketin parlatılmış lacivert-siyahı; yükseltilmiş koyu yüzey `#222934`. Hero videosunun kendi uzayı zaten lacivert-siyah olduğu için artık zeminle aynı aileden; önceki sürümdeki mor-siyah ile uzay arasındaki renk farkı kapandı.
* **Logo ve ikonlar:** Başlık ve altlıkta yeni yatay logo (Lacivert yazı ve dış yörünge, Koyu Altın iç yörünge, Bordo dikey yörünge, Altın küre). Favicon, dokunma ikonu, 192 / 512 ikonlar ve `favicon.ico` paketten birebir (yalnız gömülü C2PA künyesi atıldı), Gece zeminli.
* **Harita:** Paketin harita kuralı aynen duruyor: haritaya marka rengi çizilmez; ilgi alanı beyaz kesikli çizgi ve koyu hale. Kızıldere konum haritası yeni Gece ve Obsidyen tonlarıyla yeniden üretildi (coğrafya birebir aynı), Act 4 hedef çerçevesi beyaz kaldı.
* **Kontrast:** Okyanus açık zeminde 4.85–5.25:1, koyu zeminde 5.63–6.97:1; odak halkası en az 5.25:1. Tarayıcıda 13 sayfa × iki ekran genişliğinde yazı kontrastı ölçüldü (§3); eşiğin altında çıkan olmadı.
* **Değişmeyenler:** Dört perdeli ana sayfa, gerçek uydu görüntüleri, bilimsel rasterlar (hiçbirine dokunulmadı), hero videosu, metinler, menü, adresler, **yazı tipleri**.
* **Yazı tipi:** Paket yine Mona Sans ve Martian Mono veriyor; site kendi OrbGSS Sans / Mono'sunu (Plex alt kümeleri) koruyor. Değiştirmek ayrı iş (lisans, alt küme, yerleşim ölçümü) ve yayın sonrası cila turunun konusu; §9.

## 1. Palette — the only UI colours

Defined once in `:root` of `styles.css`; `scripts/validate_site.py` pins every value (`BRAND_TOKENS`) and recomputes every contrast pair below.

| Token | Value | Role | Contrast (computed) |
| --- | --- | --- | --- |
| `--ink` | `#142435` | text on light grounds and the dark caption tone (the brand's Pumice theme text colour) | on Pumice 14.54:1, white 15.75:1, Mist 14.00:1 |
| `--muted` | `#6A7178` | secondary text and lines on light grounds | on Pumice 4.57:1, white 4.95:1 |
| `--ocean` | `#006CCA` | Ocean on light grounds: links, active state, focus ring (the brand's Pumice accent) | on Pumice 4.85:1, white 5.25:1, Mist 4.67:1 |
| `--gold` | `#F8AD24` | Gold on light grounds: rules and marks, **never text** (1.91:1 on white) | |
| `--mist` | `#EDF2F9` | the brand's dark-ground wordmark colour: primary text on dark, the light caption tone | on Night 16.10:1, Night lift 13.01:1 |
| `--mist-soft` | `#B7BEC8` | secondary text and captions on dark | on Night 9.67:1, Night lift 7.82:1 |
| `--ocean-light` | `#54A4FB` | Ocean on dark (the Obsidian accent): links, active nav, focus ring | on Night 6.97:1, Night lift 5.63:1 |
| `--gold-light` | `#F8AD24` | Gold on dark: limits, data gaps (the package gives one Gold for both grounds) | on Night 9.48:1, Night lift 7.66:1 |
| `--night` | `#0D1626` | the dark ground (the brand's Night) | |
| `--night-lift` | `#222934` | the dark step: the Act 4 stage, the Mining / Marine bands (the Obsidian raised surface) | |
| `--pumice` | `#F4F6F8` | the light ground (the brand's Pumice) | |
| `--white` | `#FFFFFF` | the header, the footer, the light cards and the map / figure area-of-interest line | Ink 15.75:1, Ink soft 7.33:1, Muted 4.95:1, Ocean 5.25:1, Gold ink 5.18:1 |
| `--ink-soft` | `#4E5762` | secondary text on light grounds | on Pumice 6.77:1, white 7.33:1 |
| `--gold-ink` | `#9C5F00` | Gold as text on light grounds (the data-gap label; the brand's "gold text") | on Pumice 4.79:1, white 5.18:1 |
| `--rule`, `--rule-soft` | `rgba(183,190,200,.22)` / `.11` | lines on dark (Mist soft) | |
| `--rule-paper`, `--rule-paper-soft` | `rgba(106,113,120,.30)` / `.15` | lines on light grounds (Muted) | |

The values are the brand's own (`Final_v6/tokens/orbgss-tokens.css`); `--night-lift`, `--ink-soft`, `--gold-ink` and the two rule families are neutral steps from the same file. The package's hover and pressed tones (`#005DB9`, `#004EA4`, `#6CB4FF`, `#4494EA`) and wash (`#E3F2FF`) are not tokens here: the site never had accent-coloured hover or pressed states (a link's hover sets `--fg`), and the hover wash is the accent at 7 % alpha (`--wash`).

**Token names changed with the identity** (as they did at Heat Trace and Violet): `--violet` → `--ocean`, `--violet-light` → `--ocean-light`, `--amber` → `--gold`, `--amber-light` → `--gold-light`, `--amber-ink` → `--gold-ink`. The Violet and Amber names are retired and fail the validator if they return, together with `--plum`, `--navy`, `--maroon` and `--deep-gold` (logo-only colours) and every earlier retired name. `--gold`, `--gold-light` and `--gold-ink` were Agate names that the validator used to refuse; they are the v6 names now.

**Rules.**

1. **Nothing else is a UI colour.** The stylesheet, `<style>` blocks and inline styles may use the tokens' hexes, `rgba()` of a palette triple at any alpha, `transparent` and `currentColor`. Every other hex, `rgb()` of anything else, `hsl()`, `color-mix()` and every CSS named colour fails the validator. Images are exempt: rasters, the hero video and the SVG files are checked on their own terms (§4, §6).
2. **Ocean is the interactive accent, and only that.** Links, the active navigation item, the focus ring (2 px) and control states. It is never a data colour and never marks an area of interest.
3. **Gold is a restrained highlight, never a fill and never body text on a light ground.** A line, a label, a mark: the data-gap label, rules. The validator fails any rule that fills a background with a gold value or with `--limit`. On light grounds gold text is `--gold-ink`; `--gold` is only a line there.
4. **Navy, Maroon and Deep Gold are logo-only.** Navy is the wordmark and outer orbit on light grounds, Maroon the vertical orbit on every ground, Deep Gold the inner orbit on light grounds. No UI colour is any of them.
5. **No cyan, no teal, no copper, no gradient accent.** Night `#0D1626` is the brand's own dark ground (a navy-black); there is no other navy surface.
6. **Scientific colour maps are not part of this system.** No UI colour goes inside a figure frame, and no CSS filter, transform or upscale goes on a governed raster. No analytical raster, hero frame or photograph was re-coloured by this work. The area-of-interest line stays white (§5).
7. **Ground-aware roles are unchanged.** Components take `--fg`, `--fg-2`, `--link`, `--limit`, `--limit-line`, `--hair`, `--hair-soft`, `--surface`, `--matte`, `--wash` from the ground, so one component reads correctly on dark and on light. `--wash` is the accent at 7 % alpha (`rgba(84,164,251,.07)` on dark, `rgba(0,108,202,.07)` on light).
8. **Caption tone.** The per-panel `data-label-tone` stays: the light tone is Mist with a Night halo, the dark tone is Ink. Mist and Ink changed, so `CAPTION_TONE_CROSSOVER` in `script.js` moved from 0.1967 to **0.1995**; the validator derives it from the two caption tokens and fails a stale value.

## 2. Grounds

Unchanged (`docs/WEB_HEAT_TRACE_BRAND_AUTHORITY.md` §2): `ground-orbit` is the dark ground (Night), `ground-lift` the lifted step (Night lift), `ground-paper` the light ground (Pumice); the header and footer are white and carry the light-ground logo.

## 3. Interaction states and measured contrast

Measured in the browser (headless Chromium) on all 13 routes, English and Turkish, at 1440 and 390 px (`evidence/heat_trace/measure_contrast.py`, run with `--out evidence/v6/measurements/contrast_audit.json`; focus and hover in `states.json`, overflow and console in `overflow.json`, which accents are in use in `accent_colours.json`); the figures are in `tasks/V6_EVIDENCE.md`.

* **Rest:** primary text Ink on light and Mist on dark; secondary text Ink soft / Mist soft; links and kickers Ocean / Ocean light; limits Gold ink / Gold light.
* **Hover:** a navigation link rises from Ink soft to Ink; a body link takes the foreground; the ghost button fills with Mist and sets its label in Ink (14.00:1; never gold, never Ocean).
* **Focus:** `:focus-visible` draws a 2 px outline: Ocean on light grounds (5.25:1 on white, 4.85:1 on Pumice), Ocean light on dark grounds (6.97:1 on Night, 5.63:1 on Night lift). The skip link shows its own Pumice chip with the Ocean ring.
* **Reduced motion and the mobile navigation:** unchanged.

## 4. Brand marks

Built by `scripts/build_brand_assets.py --source <Final_v6/>` from the package; recorded in `assets/brand/brand.json`; recomputed by the validator on every run.

| Role | Shipped file | Used for |
| --- | --- | --- |
| `logo-light` | `assets/brand/orbgss-logo-light.00811851.svg` (viewBox 619.41 × 144; markup `width="619" height="144"`) | header and footer, every page, white ground |
| `favicon` | `assets/brand/orbgss-favicon.84b79d56.svg` | `<link rel="icon" type="image/svg+xml">`: Night tile, dark-ground symbol |
| `favicon-ico` | `/favicon.ico` (16, 32, 48 px, byte for byte) | `<link rel="icon" href="/favicon.ico" sizes="32x32">` and the root path browsers ask for |
| `apple-touch-icon` | `assets/brand/orbgss-apple-touch-icon.d9438a09.png` (180) | `<link rel="apple-touch-icon">` |
| `icon-192`, `icon-512` | `assets/brand/orbgss-icon-192.3e9a3871.png`, `orbgss-icon-512.219a6ca6.png` | `site.webmanifest` |

* **What changed from Violet.** The light-ground logo is Navy `#08336C` (wordmark and outer orbit), Deep Gold `#D48200` (inner orbit), Maroon `#C0303B` (vertical orbit) and Gold `#F8AD24` (the orb); the Plum, Amber and Magma of the Violet logo are gone. The favicon tile is Night `#0D1626` with Mist, Maroon and Gold. Marks are otherwise the same lock-up, same viewBox, same sizes.
* **Hash names.** `/assets/` is served `immutable` for a year, so a changed logo must be a new file name: `<stem>.<first 8 of SHA-256>.<ext>`. The validator checks the name against the content; the Violet files are deleted.
* **One change to the supplied SVGs.** Each carries an embedded C2PA `<metadata>` provenance manifest that no browser reads and that no longer verifies once a file is touched; it and its `xmlns:c2pa` declaration are removed. The drawing is not touched. The validator proves that every paint in a shipped SVG is a brand colour for its ground (the light-ground logo: Navy, Deep Gold, Maroon, Gold, and the black and white a mask needs; the favicon: Night, Mist, Maroon, Gold) and that no script, text, embedded image or link is present. PNGs and the `.ico` are copied byte for byte.
* **Markup, theme colour, minimum width:** unchanged from Heat Trace §4 (header logo 138 × 32 px, 120 × 28 px at ≤ 560 px; `theme-color` and manifest colours white `#FFFFFF`; the validator fails under 120 px).
* **Not used:** `Final_v6/assets/illustrative-map.jpg` (a generated illustration), the application templates, the stacked logos, the Tauri set and the font files. The brand's rule "not on maps or busy imagery" holds: the logo is not placed on a photograph.

## 5. The map rule

Unchanged from the package: no brand colour is drawn on the map, because viridis starts in violet and ends in yellow and an Ocean or Gold mark would read as data; the selected area of interest is a white dashed line with a dark halo (`--ogs-map-callout: #FFFFFF`, a 5 px Night halo at 70 %). `scripts/build_locator_map.py` applies it to the Kızıldere locator map with the neutrals of the brand's dark theme (Obsidian: sea `#0A0F17`, neighbouring land `#10161F`, Türkiye `#222934` with a `#6A707A` outline) and the Night halo `#0D1626`. Same Natural Earth source (v5.1.2, SHA-256 `3e458fc0…`, re-downloaded and verified against the recorded hash) and projection, byte-identical geometry; the file is `assets/maps/kizildere-locator-3c3c49fd.svg` (the Violet file is removed) and its record in `assets/imagery/sources.json` (`web_m6.locator_map`) carries the new bytes and SHA-256. The validator checks the SVG for the six map colours, exactly one white callout that is dashed with the 70 % Night halo, and fails any brand colour. The homepage Act 4 target frame follows the same rule: white corners.

## 6. What the hero does and does not do

Unchanged: the hero video (class C, a rendered orbital sequence) is render content, not UI, and is not recoloured; the overlay shade is derived on Night, and Night is now `#0D1626`, which sits next to the video's own navy-black space. Its baked pale-cyan reticle and orbit trail remain (§7).

## 7. Residuals

* **Hero video.** The area-of-interest reticle and orbit trail are baked pale cyan, which is neither the brand's white AOI line nor Ocean light. The seam between the video's space and Night is now small (the same colour family); a complete match means re-rendering the hero (`hero/config/scene.json`, local Blender production), a separate task.
* **Fonts.** The package names Mona Sans (text) and Martian Mono (data), ships their variable TTFs and a `fonts.css`, and draws the wordmark from Mona Sans Display Expanded Medium (outlined, so the logo needs no font). The site keeps its self-hosted OrbGSS Sans / Mono (renamed IBM Plex subsets). A type change needs its own licence entry, WOFF2 subsets and a layout re-measure (§9).
* **Social image.** `og:image` is still the hero poster; a branded card is optional.
* **Icon files are the supplied ones.** The manifest declares `purpose: any` only; no maskable variant was supplied. The Gold orbit and orb are the brand's own at small sizes; the header logo is at least 120 px wide and the favicon uses the Night tile.
* **Supplied SVG metadata.** The stripped C2PA block is a "provided by Claude" content credential on the supplied files; the CEO/COO own any trademark question.
* **GitHub is public.** Working notes in the repository stay readable there (unchanged); this work adds none to a deployed page.
* **Package documents not read in full.** The package's review and application pages (`Final_v6 Review.dc.html`, `Final_v6 - Website.dc.html`, …) are design-tool files; the token file, the README, the SVG and PNG marks were the sources used.

## 8. What the validator enforces

`scripts/validate_site.py` (the brand checks are `brand_checks`, the palette checks the Atlas foundation's, on `BRAND_TOKENS`):

1. every palette token, defined once in `:root`, exactly; the 19 text/ground contrast pairs against their floors (7:1 for the main roles, 4.5:1 for the accent and the secondary tones);
2. no other colour literal in `styles.css`, any `<style>` block or any inline style; no retired token (Violet and Amber names, Heat Trace `--magma` / `--magma-light`, Agate, Atlas and older names, and the logo-only `--navy`, `--maroon`, `--plum`, `--deep-gold`); no gold fill;
3. `assets/brand/brand.json` records the v6 identity, the approved palette (the seven brand colours and the two UI forms of Ocean) and exactly the seven roles, with source and shipped SHA-256, size and name-by-hash for each; no unrecorded file in `assets/brand/`;
4. each SVG paints only brand colours for its ground (the light-ground logo must carry Navy, Deep Gold, Maroon and Gold) and holds no metadata, script, text, image or link; the logo's viewBox is `0 0 619.41 144`; each PNG is a plain PNG of the right size; `favicon.ico` holds 16, 32 and 48 px;
5. every page's head carries the favicon links, the touch icon and the white `theme-color`; the header and footer brand markup is exactly as in §4; `.brand-logo` never goes under 120 px wide;
6. `site.webmanifest` icons and colours; `favicon.ico` is in `.vercelignore`; the illustrative map is not placed or shipped;
7. the locator map follows the map rule (§5);
8. `CAPTION_TONE_CROSSOVER` in `script.js` equals the value derived from the Mist and Ink tokens;
9. the Act 4 target frame is white; the skip link's focus ring and the paper ground's link colour are Ocean; the "Active" label's scrim keeps 4.5:1 for Ocean light over a white photograph pixel (it gives 6.1:1).

`scripts/negative_tests_brand.py` breaks each of those in memory (60 cases), and the suites of earlier tasks were moved to the new tokens, files and messages; run them one at a time in a detached worktree (`tasks/V6_EVIDENCE.md`).

## 9. Handed over

* **Fonts (open, for the polish round):** keep OrbGSS Sans / Mono (Plex), or move to the brand's Mona Sans / Martian Mono. Recommendation: keep Plex until the product design decides; the type change is its own task.
* **Hero (open):** re-render the hero on Night with a white or no reticle, or leave it (§7).
* **Social card (open):** whether to add a Night OG card with the logo.
* **The unchanged open items** of the Atlas, light-theme and missing-visuals work (the CTO's reading of the Turkish copy, the font and colour-map licence links, the Violet-era notes) stay as their documents left them.
