# WEB Heat Trace brand adoption — palette, marks and map rule

**Task:** brand adoption on the existing website (CTO decision of 2026-10-25, "bu son tasarım kararı uygula"); not a site replacement.
**Status:** **review, pending CTO acceptance.** Nothing here is published; it becomes binding only when the CTO accepts the reviewed branch and authorizes a publication.
**Baseline:** the light-theme branch (white header and footer, Pumice-style pages, plain-spoken copy), which itself sits on the Agate adoption (MER-279) and the Atlas integration (MER-274). This work changes colour and brand marks on top of it and nothing else.
**Governs, once accepted:** the UI palette, the colours of the grounds, the logo, the favicon family and the map rule. It **supersedes `docs/WEB_AGATE_BRAND_AUTHORITY.md`** (§1 palette, §3 interaction colours, §4 marks, §5 map rule, §8 checks) and the palette lines of `docs/WEB_LIGHT_THEME_AUTHORITY.md` and `docs/WEB_ATLAS_DESIGN_AUTHORITY.md`. It changes nothing in type, fonts, the structure of the shared components, the four-act homepage, the scientific, legal, claim and content rules, the page set, the navigation, the URLs or the light-theme page map (`docs/WEB_LIGHT_THEME_AUTHORITY.md` §1).
**Package:** `OrbGSS Logo Tasarım4.zip` (SHA-256 `cc5f769b…625635`), folder `Final_v3/`, "6a Heat Trace" palette. `Final_v2/` and the older Agate folder `final/` are superseded and not used.

## 0. Özet (CTO için)

* **Renk:** Agate (grafit, teal, altın) gitti. Yerine onayladığın "Heat Trace" geldi: Magma `#CD1B74` (tek etkileşim rengi: bağlantı, aktif menü, odak halkası), Amber `#FFA323` (ölçülü vurgu: ince çizgi, "yok" etiketi; düğme dolgusu ya da yazı değil), Plum `#371641` (yalnız logonun yazısı) ve Glow `#FEF1A1` (yalnız logonun küresi). Koyu zeminde okunsun diye açık eşleri: Magma `#F94997`, Amber `#FFAA2E`, yazı Mist `#F5EFF7`, zemin Night `#160A19`. Açık sayfalarda yazı Ink `#2D1B30` (Plum'un yazılık tonu), sayfa zemini Pumice `#F7F5F8`.
* **Logo ve ikonlar:** Başlık ve altlıkta yeni yatay logo (Plum yazı, Magma ve Amber yörüngeler). Favicon, dokunma ikonu, 192 / 512 ikonlar paketten birebir, Night zeminli. Başlıkta logo 138 × 32 px (telefonda 120 × 28), marka asgarisi 120 px.
* **Harita:** Kızıldere konum haritası markanın harita kuralıyla yeniden üretildi: Night tonlarında zemin, ilgi alanı kesikli Magma çerçeve ve koyu hale. Haritada Amber ve Glow yok. Ana sayfadaki Act 4 hedef çerçevesi de aynı kuralla Magma oldu (önceden altındı).
* **Kontrast:** Okunur yazı her zeminde en az 7:1; Magma bağlantılar açık zeminde 4.84–5.24:1, koyu zeminde 5.89:1; odak halkası 4.84:1 ve üstü. Tarayıcıda 13 sayfa × iki ekran genişliğinde 1.354 yazı ölçüldü, eşiğin altında çıkan olmadı (§3).
* **Değişmeyenler:** Dört perdeli ana sayfa, gerçek uydu görüntüleri, bilimsel rasterlar (hiçbirine dokunulmadı), hero videosu, metinler, menü, adresler, yazı tipleri.
* **Hero dikişi:** Üst çubuk beyaz olduğu için hero ile başlık arasında zaten net bir sınır var; hero'nun sol gölgesi artık Night'tan türetiliyor, ölçülen sol kenar `(26,14,28)`, Night'a (`22,10,25`) çok yakın. Videonun kendi lacivert-siyah uzayı yalnız sağdaki fotoğraflı bölgede ve sahne içinde kalıyor; sol gölge onu örtüyor.
* **Senin kararın gereken:** §9.

## 1. Palette — the only UI colours

Defined once in `:root` of `styles.css`; `scripts/validate_site.py` pins every value (`BRAND_TOKENS`) and recomputes every contrast pair below.

| Token | Value | Role | Contrast (computed) |
| --- | --- | --- | --- |
| `--ink` | `#2D1B30` | text on light grounds and the dark caption tone (the brand's Pumice theme text colour; Plum itself is the wordmark's colour) | on Pumice 14.78:1, white 16.02:1, Mist 14.17:1 |
| `--muted` | `#756D76` | secondary text and lines on light grounds | on Pumice 4.61:1, white 4.99:1 |
| `--magma` | `#CD1B74` | Magma on light grounds: links, active state, focus ring | on Pumice 4.84:1, white 5.24:1 |
| `--amber` | `#FFA323` | Amber on light grounds: rules and marks, **never text** (2.00:1 on white) | |
| `--mist` | `#F5EFF7` | the brand's dark-ground wordmark colour: primary text on dark, the light caption tone | on Night 17.01:1, Night lift 14.43:1 |
| `--mist-soft` | `#C3BAC5` | secondary text and captions on dark | on Night 10.21:1, Night lift 8.66:1 |
| `--magma-light` | `#F94997` | Magma on dark (the Obsidian accent): links, active nav, focus ring, the Act 4 target frame | on Night 5.89:1, Night lift 4.99:1 |
| `--amber-light` | `#FFAA2E` | Amber on dark: limits, data gaps | on Night 10.12:1, Night lift 8.58:1 |
| `--night` | `#160A19` | the dark ground (the brand's Night) | |
| `--night-lift` | `#241E25` | the dark step: the Act 4 stage, the Mining / Marine bands (the Obsidian raised surface) | |
| `--pumice` | `#F7F5F8` | the light ground (the brand's Pumice) | |
| `--white` | `#FFFFFF` | the header, the footer and the light cards | Ink 16.02:1, Ink soft 7.40:1, Muted 4.99:1, Magma 5.24:1, Amber ink 5.18:1 |
| `--ink-soft` | `#5D525F` | secondary text on light grounds | on Pumice 6.83:1, white 7.40:1 |
| `--amber-ink` | `#A15C13` | Amber as text on light grounds (the data-gap label; the brand's "amber text in Pumice") | on Pumice 4.78:1, white 5.18:1 |
| `--rule`, `--rule-soft` | `rgba(195,186,197,.22)` / `.11` | lines on dark (Mist soft) | |
| `--rule-paper`, `--rule-paper-soft` | `rgba(117,109,118,.30)` / `.15` | lines on light grounds (Muted) | |

The first eight rows are the brand's own values (Plum is represented by Ink as UI text; Glow and Violet live in the logo files only). `--night-lift`, `--ink-soft`, `--amber-ink` and the two rule families are derived or taken from the brand token file (`Final_v3/tokens/orbgss-tokens.css`); they are neutral steps and one darker amber for text, not new brand colours.

**Rules.**

1. **Nothing else is a UI colour.** The stylesheet, `<style>` blocks and inline styles may use the tokens' hexes, `rgba()` of a palette triple at any alpha, `transparent` and `currentColor`. Every other hex, `rgb()` of anything else, `hsl()`, `color-mix()` and every CSS named colour fails the validator. Images are exempt: rasters, the hero video and the SVG files are checked on their own terms (§4, §6).
2. **Magma is the interactive accent, and only that.** Links, the active navigation item, the focus ring (2 px), tab and control states, and the area-of-interest mark (the locator-map callout and the Act 4 target frame). It is never a data colour.
3. **Amber is a restrained highlight, never a fill and never body text on a light ground.** A line, a label, a mark: the data-gap label, rules. The validator fails any rule that fills a background with an amber value (`--amber`, `--amber-light`, `--amber-ink` or their hexes) or with `--limit`. On light grounds amber text is `--amber-ink`; `--amber` is only a line there. Magma sits near danger red and Amber near warning orange, so a state always carries a word and a shape, and Magma is never used for destructive actions (brand trade-off).
4. **Glow and Violet are logo-only.** Glow is the logo's orb on dark grounds and appears in the favicon tile; no UI colour is Glow or Violet.
5. **No cyan, no teal, no copper, no navy surface, no gradient accent.** The Agate tokens (`--graphite`, `--graphite-soft`, `--mineral`, `--mineral-light`, `--teal`, `--teal-light`, `--gold`, `--gold-light`, `--gold-ink`, `--ground`, `--ground-lift`, `--limestone`), the Atlas tokens and every earlier retired token fail the validator if they return. `--muted` was once retired (a MER-255 grey) and is a Heat Trace token again; the validator's list was changed accordingly.
6. **Scientific colour maps are not part of this system.** No UI colour goes inside a figure frame, and no CSS filter, transform or upscale goes on a governed raster. No analytical raster, hero frame or photograph was re-coloured by this work; the palette applies to the page, never to the evidence.
7. **Ground-aware roles are unchanged.** Components take `--fg`, `--fg-2`, `--link`, `--limit`, `--limit-line`, `--hair`, `--hair-soft`, `--surface`, `--matte`, `--wash` from the ground, so one component reads correctly on dark and on light.
8. **Caption tone.** The per-panel `data-label-tone` stays: the light tone is Mist with a Night halo, the dark tone is Ink. `script.js` flips between them at the luminance where Mist and Ink contrast equally against the backdrop (`CAPTION_TONE_CROSSOVER`, 0.1967: √((L_Mist + 0.05)(L_Ink + 0.05)) − 0.05; it was 0.1885 for the Agate pair). The validator now **derives** this number from the two caption tokens and fails when `script.js` disagrees by more than 0.0005, so a palette change cannot leave a stale crossover behind.

## 2. Grounds

The structural class names are unchanged (a comment in `scripts/validate_site.py` says so): `ground-orbit` is the dark ground (Night), `ground-lift` the lifted step (Night lift), `ground-paper` the light ground (Pumice). The page map (which sections are light and which dark) is `docs/WEB_LIGHT_THEME_AUTHORITY.md` §1 and does not change. The header and footer are white and carry the light-ground logo.

## 3. Interaction states and measured contrast

Measured in the browser (headless Chromium) on all 13 routes, English and Turkish, at 1440 and 390 px: every text node on a solid ground (text over photographs is judged by the caption-tone rule) at or above its WCAG floor, 4.5:1, or 3:1 for large text. Result: 0 failures in 1,354 text checks (`evidence/heat_trace/measure_contrast.py`, output in `evidence/heat_trace/measurements/contrast_audit.json`); the focus-ring and hover measurements are in `states.json` (`measure_states.py`).

* **Rest:** primary text Ink on light and Mist on dark; secondary text Ink soft / Mist soft; links and kickers Magma / Magma light; limits Amber ink / Amber light.
* **Hover:** a navigation link rises from Ink soft to Ink; a body link takes the accent; the ghost button fills with Mist and sets its label in Ink (14.17:1; never amber, never magma).
* **Focus:** `:focus-visible` draws a 2 px outline: Magma on light grounds (5.24:1 on white, 4.84:1 on Pumice), Magma light on dark grounds (5.89:1 on Night). Every keyboard stop on the homepage shows it. The skip link shows its own Pumice chip with the Magma ring.
* **Reduced motion:** unchanged. The hero video is never attached, no animation runs, and the transitions that remain are colour changes only.
* **Mobile navigation (≤ 980 px):** unchanged behaviour (opens, closes with the button and Escape, `aria-expanded` truthful, rows at least 44 px high); the header logo is 138 × 32 px above 560 px and 120 × 28 px at 560 px and below.

## 4. Brand marks

Built by `scripts/build_brand_assets.py` from the package; recorded in `assets/brand/brand.json`; recomputed by the validator on every run.

| Role | Shipped file | Used for |
| --- | --- | --- |
| `logo-light` | `assets/brand/orbgss-logo-light.27e93f98.svg` (viewBox 619.41 × 144; markup `width="619" height="144"`) | header and footer, every page, white ground |
| `favicon` | `assets/brand/orbgss-favicon.73a16b96.svg` | `<link rel="icon" type="image/svg+xml">`: Night tile, dark-ground symbol |
| `favicon-ico` | `/favicon.ico` (16, 32, 48 px, byte for byte) | `<link rel="icon" href="/favicon.ico" sizes="32x32">` and the root path browsers ask for |
| `apple-touch-icon` | `assets/brand/orbgss-apple-touch-icon.a33306fa.png` (180) | `<link rel="apple-touch-icon">` |
| `icon-192`, `icon-512` | `assets/brand/orbgss-icon-192.c09d98af.png`, `orbgss-icon-512.7879a110.png` | `site.webmanifest` |

* **Hash names.** `/assets/` is served `immutable` for a year, so a changed logo must be a new file name: `<stem>.<first 8 of SHA-256>.<ext>`. The validator checks the name against the content; the old Agate files are deleted.
* **One change to the supplied SVGs.** Each carries an embedded C2PA `<metadata>` provenance manifest that no browser reads and that no longer verifies once a file is touched; it and its `xmlns:c2pa` declaration are removed. The drawing is not touched. The validator proves that every paint in a shipped SVG is a brand colour for its ground (the light-ground logo: Plum, Magma, Amber, and the black and white a mask needs; the favicon: Night, Mist, Magma, Amber, Glow) and that no script, text, embedded image or link is present. PNGs and the `.ico` are copied byte for byte. The originals stay in the package.
* **Markup.** Header: `<a class="brand" …><img class="brand-logo" src="/assets/brand/orbgss-logo-light.27e93f98.svg" alt="" width="619" height="144" /></a>` (the link's own `aria-label` is the accessible name, so the image is decorative); footer: the same file with `alt="OrbGSS"`. `.brand-logo` is 32 px high (28 px at ≤ 560 px), which is 138 px and 120 px wide: at or above the brand's 120 px minimum for the horizontal logo. The validator recomputes the width from the CSS height and fails below 120. The footer logo is 172 px wide (150 px at ≤ 560 px).
* **Theme colour.** `<meta name="theme-color" content="#FFFFFF">` on every page, and `#FFFFFF` as the manifest's `theme_color` and `background_color` (the header is white).
* **Not used:** `Final_v3/assets/illustrative-map.jpg` (a generated illustration; the validator fails if it is placed on a page or shipped), the application templates (cards, slides, banners), the stacked logos and the Tauri icon set. The brand's rule "not on maps or busy imagery" holds: the logo is not placed on a photograph.

## 5. The map rule

From the brand package: on the map, the selected area of interest is dashed Magma `#E43386` with a Night halo; Amber and Glow are never drawn on the canvas. `scripts/build_locator_map.py` applies it to the Kızıldere locator map: a Night-family sea (`#110C12`) and neighbouring land (`#1C161D`), Türkiye one step lighter (`#241E25`) with a neutral outline (`#69646A`), the 36 km area as a dashed Magma callout (`#E43386`, a 14 % fill, a 2 px line, dash 6 3) inside a 5 px Night halo (`#160A19` at 60 %). Same Natural Earth source and projection as before; the file is `assets/maps/kizildere-locator-006fcf1f.svg` (the old file is removed; the name carries the checksum because `/assets/` is immutable) and its record in `assets/imagery/sources.json` (`web_m6.locator_map`) carries the new bytes and SHA-256. The validator checks the SVG for the six map colours, exactly one Magma callout that is dashed, and fails Amber or Glow.

## 6. What the hero does and does not do

The hero video (class C, a rendered orbital sequence) is **render content**, not UI: its space background is a navy-black baked in at render time. It is not recoloured (no filter, no blend hack, no re-encode), which would also violate the rule that governed pixels are not altered after the fact. The page chrome around it is white above and Night beside it. The overlay shade that blends the hero text zone is re-derived on Night (`rgba(22,10,25,…)`), so the left of the hero reads as the brand's Night: measured at the left edge `(26,14,28)`, `(25,13,27)`, `(23,11,25)` against Night `(22,10,25)`.

## 7. Residuals the CTO should know

* **Hero video space.** The video's own space is still navy-black where the render shows it uncovered. The left shade covers it on the homepage; a complete match means re-rendering the hero on a Night space background (`hero/config/scene.json`, local Blender production), a separate decision and a separate task that needs new accepted master frames, the two-tier encode and the shot audit again. With a white header the visible seam is small; the CTO can leave it.
* **Fonts.** The brand token file names Mona Sans (text) and Martian Mono (data); the site keeps its self-hosted OrbGSS Sans / Mono (renamed IBM Plex subsets), because changing type is outside a colour and mark adoption and needs its own licence entry, subsets and a layout re-measure. This is an open decision (§9).
* **Social image.** `og:image` is still the hero poster (`assets/hero/hero-poster-1600.webp`), which has no logo in it. A Night OG card with the logo is an option, not part of this task.
* **Decorative language separator.** The `|` between EN and TR is `aria-hidden` and at the line colour; decoration, not information, unchanged in kind.
* **Icon files are the supplied ones.** The manifest declares `purpose: any` only; no maskable variant was supplied. The small Amber orbit and orb are weak on white at small sizes (the brand's own note); the header logo is at least 120 px wide and the favicon uses the Night tile.
* **GitHub is public.** Working notes in the repository stay readable there (unchanged from the light-theme review); this work adds none to a deployed page.

## 8. What the validator enforces

`scripts/validate_site.py` (the brand checks are `brand_checks`, the palette checks the Atlas foundation's, on `BRAND_TOKENS`):

1. every palette token, defined once in `:root`, exactly; the validator recomputes the 19 text/ground contrast pairs against their floors (7:1 for the main roles, 4.5:1 for the accent and the secondary tones);
2. no other colour literal in `styles.css`, any `<style>` block or any inline style; no retired token (Agate, Atlas and older names); no amber fill;
3. `assets/brand/brand.json` records the Heat Trace identity, the approved palette and exactly the seven roles, with source and shipped SHA-256, size and name-by-hash for each; no unrecorded file in `assets/brand/`;
4. each SVG paints only brand colours for its ground (the light-ground logo must carry Plum, Magma and Amber) and holds no metadata, script, text, image or link; the logo's viewBox is `0 0 619.41 144`; each PNG is a plain PNG of the right size; `favicon.ico` holds 16, 32 and 48 px;
5. every page's head carries the favicon links, the touch icon and the white `theme-color`; no page still names the old logo files or the text wordmark; the header and footer brand markup is exactly as in §4; `.brand-logo` never goes under 120 px wide;
6. `site.webmanifest` icons and colours; `favicon.ico` is in `.vercelignore`; the illustrative map is not placed or shipped;
7. the locator map follows the map rule (§5);
8. `CAPTION_TONE_CROSSOVER` in `script.js` equals the value derived from the Mist and Ink tokens (§1 rule 8);
9. the Act 4 target frame is Magma light.

`scripts/negative_tests_brand.py` (43 cases; it replaces the Agate suite) breaks each of those in memory, and the suites of earlier tasks were moved to the new tokens, files and messages; run them one at a time in a detached worktree (`tasks/HEAT_TRACE_EVIDENCE.md`).

## 9. Handed over, and for the CTO

* **Fonts (open):** keep OrbGSS Sans / Mono (Plex), or move to the brand's Mona Sans / Martian Mono. Recommendation: keep Plex for now and decide with the product design; a type change is its own task (licence, subsets, layout measurement).
* **Hero (open):** re-render the hero on a Night space background, or leave it (§7). Recommendation: leave it unless the seam bothers you on a real screen.
* **Social card (open):** whether to add a Night OG card with the logo (§7).
* **Acceptance:** of the Heat Trace colours and the new locator map as the published look, then the separate authorization to publish.
* **No change to the Atlas open items.** A1 (MER-151 derivatives full-size on the Geothermal page), the CTO's reading of the new Turkish copy, the font and colour-map licence links and the empty MER-242 slots stay exactly as `docs/WEB_ATLAS_DESIGN_AUTHORITY.md` §8 left them.
* **Nothing here is merged, deployed or on the public domain.**
