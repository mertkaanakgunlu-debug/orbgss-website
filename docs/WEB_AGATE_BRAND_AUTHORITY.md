# WEB Agate brand adoption — palette, marks and map rule

**Task:** MER-279 (brand adoption on the existing website; not a site replacement).
**Status:** **review, pending CTO acceptance.** The CTO approved the Agate identity on 2026-10-25 and asked for it on the existing site. Nothing here is published; it becomes binding only when the CTO accepts the reviewed branch and authorizes a publication.
**Superseded 2026-10-25 by `docs/WEB_HEAT_TRACE_BRAND_AUTHORITY.md`, then by `docs/WEB_VIOLET_BRAND_AUTHORITY.md` and, on 2026-10-30, by `docs/WEB_V6_BRAND_AUTHORITY.md`** (CTO decisions on the final brand package, "Heat Trace", then "Violet"). The Agate palette (§1), interaction colours (§3), marks (§4), map rule (§5) and checks (§8) below are kept as the record of what MER-279 built; the tokens, files, hashes and the `agate_brand_checks` / `negative_tests_agate_brand.py` names they cite no longer exist (`brand_checks`, `negative_tests_brand.py`). The structure of this adoption (one palette defined once, role variables, hash-named brand files recorded in `brand.json`, no colour in a figure frame, the hero and the rasters never recoloured) carries over.
**Baseline:** `claude/project-thread-07ccos@4bbbe0ee` (the Atlas integration of MER-274: MER-275 foundation, MER-276 / 277 / 278 page groups). This work changes colour and brand marks on top of it and nothing else.
**Governs, once accepted:** the UI palette, the grounds' colours, the logo, the favicon family and the map rule. It wins over `docs/WEB_ATLAS_DESIGN_AUTHORITY.md` §0 (colour bullet), §1 and §2 (the palette and the colours of the grounds) and over the palette lines of the other design documents. It changes nothing in type, fonts, the shared components' structure, the four-act homepage, the scientific, legal, claim and content rules, the page set, the navigation or the URLs.
**Amended 2026-10-25 (`docs/WEB_LIGHT_THEME_AUTHORITY.md`, CTO request):** the header and footer are white and carry the light-ground logo, so §2 (grounds), §4 (logo role, markup, theme colour) and §7 (the hero seam) below read as amended here; the palette, the map rule, the interaction states and the hero rules stand. The mandatory warnings named in this document were retired the same day.
**Package:** `OrbGSS Logo Tasarim Final.zip`, folder `final/`; `final/variant-b/` and `final/assets/illustrative-map.jpg` are not used.

## 0. Özet (CTO için)

* **Renk:** Atlas'ın cyan + lacivert paleti gitti. Yerine onayladığın dört Agate rengi geldi: Graphite (koyu zemin ve açık zeminde yazı), Mineral Gray, Agate Teal ve Mineral Gold; koyu zeminde okunsun diye her birinin açık eşi (`#E3E5E4`, `#B7C0BD`, `#58AEB2`, `#D8B173`). Teal tek etkileşim rengi (bağlantı, aktif menü, odak halkası). Gold ölçülü bir vurgu: sınır, uyarı çizgisi, hedef çerçevesi, haritadaki ilgi alanı; hiçbir yerde dolgu rengi değil. Bakır yok, lacivert yüzey yok.
* **Logo ve ikonlar:** Başlıkta ve altlıkta yeni yatay logo (SVG, 141–225 px genişlikte, marka asgarisi 120 px). Favicon (SVG ve `.ico`), 180 px dokunma ikonu ve 192 / 512 px manifest ikonları paketten birebir. Her marka dosyası içerik özetiyle adlandırıldı (`/assets/` bir yıl önbellekte kalıyor) ve `assets/brand/brand.json` hepsinin kaynağını ve özetini kayıtlı tutuyor.
* **Harita:** Kızıldere konum haritası marka kuralıyla yeniden üretildi: Graphite nötrler, ilgi alanı altın bir çerçeve, haritada teal yok. Üretici betik aynı, yalnız renkler değişti.
* **Değişmeyenler:** Dört perdeli ana sayfa, gerçek uydu görüntüleri, bilimsel rasterlar (hiçbirine dokunulmadı), alt yazılar, menü, adresler, metinler, yazı tipleri.
* **Kalan iz:** Ana sayfadaki hero videosunun kendi uzay arka planı lacivert-siyah (render içeriği, arayüz rengi değil). Başlık ve sayfa zemini Graphite olduğu için hero'nun sol üstünde ince bir ton farkı görünüyor. CSS ile yumuşatıldı, video yeniden render edilmeden tam kapanmaz (§7).
* **Senin kararın gereken:** §9.

## 1. Palette — the only UI colours

Defined once in `:root` of `styles.css`; `scripts/validate_site.py` pins every value (`AGATE_TOKENS`) and recomputes every contrast pair below.

| Token | Value | Role | Contrast (computed) |
| --- | --- | --- | --- |
| `--graphite` | `#202629` | Agate Graphite: text on light grounds, the dark caption tone, the favicon tile | on Limestone 14.05:1, on Mist 12.11:1 |
| `--mineral` | `#69716F` | Mineral Gray: secondary text and lines on light grounds | on Limestone 4.59:1 |
| `--teal` | `#18777A` | Agate Teal on light grounds: links, active state | on Limestone 4.87:1 |
| `--gold` | `#C49A5A` | Mineral Gold on light grounds: rules, marks, never text | (2.37:1 on Limestone, so never text there) |
| `--mist` | `#E3E5E4` | the approved dark-ground "outer" colour: primary text on dark | on Ground 13.83:1, on Ground lift 11.49:1 |
| `--mineral-light` | `#B7C0BD` | Mineral Gray on dark: secondary text, captions | on Ground 9.41:1, on Ground lift 7.81:1 |
| `--teal-light` | `#58AEB2` | Agate Teal on dark: links, active nav, focus ring | on Ground 6.76:1, on Ground lift 5.62:1 |
| `--gold-light` | `#D8B173` | Mineral Gold on dark: limits, data gaps, the target frame | on Ground 8.71:1, on Ground lift 7.24:1 |
| `--ground` | `#171A1B` | the dark ground (Graphite, deepened one step so the page recedes behind the brand colour) | |
| `--ground-lift` | `#252A2B` | the derived dark step: indexes, the Mining/Marine pair, the Act 4 stage | |
| `--limestone` | `#F6F5F2` | the light ground (reading records only) | |
| `--graphite-soft` | `#565D5A` | secondary text on Limestone | 6.20:1 |
| `--gold-ink` | `#735525` | Mineral Gold as text on Limestone (the data-gap label on paper) | 6.30:1 |
| `--white` | `#FFFFFF` | the header, the footer and the light cards (the brand token `--ogs-bg-surface`) | Graphite 15.32:1, Graphite Soft 6.75:1, Mineral 5.01:1, Teal 5.30:1, Gold Ink 6.87:1 |
| `--rule`, `--rule-soft` | `rgba(183,192,189,.22)` / `.11` | lines on dark | |
| `--rule-paper`, `--rule-paper-soft` | `rgba(105,113,111,.30)` / `.15` | lines on Limestone | |

`--ground`, `--ground-lift`, `--limestone`, `--graphite-soft` and `--gold-ink` are derived: neutral steps and one darker gold tone for text on paper. They are not new brand colours and they are the only tones outside the approved eight.

**Rules.**

1. **Nothing else is a UI colour.** The stylesheet, `<style>` blocks and inline styles may use the tokens' hexes, `rgba()` of a palette triple at any alpha, `transparent` and `currentColor`. Every other hex, `rgb()` of anything else, `hsl()`, `color-mix()` and every CSS named colour fails the validator. Images are exempt: rasters, the hero video and SVG files are checked on their own terms (§4, §6).
2. **Teal is the interactive accent, and only that.** Links, the active navigation item, the focus ring (2 px, 6.76:1 on the ground), tab and control states. It is never a data colour and never appears on a map.
3. **Gold is a restrained highlight, never a fill.** A line, a label, a mark: the mandatory-warning rule, the data-gap label, the target frame on the Act 4 result, the area-of-interest callout on a map. The validator fails any rule that fills a background with a gold value. On Limestone, gold text is `--gold-ink`; `--gold` is only a line there.
4. **No copper, no navy surface, no gradient accent.** The retired Atlas tokens (`--orbit`, `--lift`, `--paper`, `--steel`, `--slate`, `--signal`, `--signal-deep`, `--caution`, `--caution-deep`) and every earlier retired token fail the validator if they return; so do the old cyan and navy hexes.
5. **Scientific colour maps are not part of this system.** No UI colour goes inside a figure frame, and no CSS filter, transform or upscale goes on a governed raster. No analytical raster, hero frame or photograph was re-coloured by this work; the Agate palette applies to the page, never to the evidence.
6. **Ground-aware roles are unchanged.** Components take `--fg`, `--fg-2`, `--link`, `--limit`, `--limit-line`, `--hair`, `--hair-soft` from the ground, so one component reads correctly on dark and on Limestone.
7. **Caption tone.** The per-panel `data-label-tone` stays: the light tone is Mist with a Ground halo, the dark tone is Graphite. `script.js` flips between them at the luminance where Mist and Graphite contrast equally against the backdrop (`CAPTION_TONE_CROSSOVER`, 0.1885, derived from the WCAG formula for those two colours; it was 0.185 for the Atlas pair).

## 2. Grounds

The three structural classes keep their names so that page markup, the three page-group regions and their suites are unchanged: `ground-orbit` is the dark ground (Ground), `ground-lift` the lifted step, `ground-paper` the light ground (Limestone). The names are structural, not colour names; a comment in `scripts/validate_site.py` says so.

* **Amended 2026-10-25:** the pages are a light theme. The header and footer are **white**; the pages sit on **Limestone**; **Ground** and **Ground lift** are for photographs, the priority result and the dark bands of each page. The per-page map is in `docs/WEB_LIGHT_THEME_AUTHORITY.md` §1. The three bullets that stood here (Ground for every opening, header and footer; Ground lift for index bars; Limestone for reading records only) are superseded.

## 3. Interaction states

Measured in the browser on every route (`tasks/MER-279_EVIDENCE.md`): text and UI at rest, on hover and on focus keep at least 4.5:1 for text and 3:1 for the focus ring.

* **Rest:** primary text Mist, secondary text Mineral Light, links and kickers Teal Light, limits Gold Light (Graphite, Graphite Soft, Teal and Gold Ink on Limestone).
* **Hover:** a navigation or footer link rises from Mineral Light to Mist; a body link goes to Teal Light; the ghost button fills with Mist and sets its label in Graphite (never gold, never teal).
* **Focus:** `:focus-visible` draws a 2 px Teal Light outline at 4 px offset (6.76:1 on the ground); card links draw it on their pseudo-element; the skip link shows its own Limestone chip with the same ring.
* **Reduced motion:** unchanged from Atlas. The hero video is never attached, no animation runs, and the transitions that remain are colour changes only. Measured identical to the Atlas build.
* **Mobile navigation (≤ 980 px):** the menu opens, closes with the button and with Escape, keeps `aria-expanded` truthful, and every row is at least 44 px high; the header logo is 141 × 24 px at 560 px and below, 176 × 30 px above.

## 4. Brand marks

Built by `scripts/build_brand_assets.py` from the package; recorded in `assets/brand/brand.json`; recomputed by the validator on every run.

| Role | Shipped file | Used for |
| --- | --- | --- |
| `logo-light` | `assets/brand/orbgss-logo-light.de682b8e.svg` (634 × 108) | header and footer, every page, white ground (amended 2026-10-25; the dark-ground logo is no longer shipped) |
| `favicon` | `assets/brand/orbgss-favicon.31dba293.svg` | `<link rel="icon" type="image/svg+xml">`: Graphite tile, dark-ground symbol |
| `favicon-ico` | `/favicon.ico` (16, 32, 48 px, byte for byte) | `<link rel="icon" href="/favicon.ico" sizes="32x32">` and the root path browsers ask for |
| `apple-touch-icon` | `assets/brand/orbgss-apple-touch-icon.ea0b5f7b.png` (180) | `<link rel="apple-touch-icon">` |
| `icon-192`, `icon-512` | `assets/brand/orbgss-icon-192.*.png`, `orbgss-icon-512.*.png` | `site.webmanifest` |

* **Hash names.** `/assets/` is served `immutable` for a year, so a changed logo must be a new file name: `<stem>.<first 8 of SHA-256>.<ext>`. The validator checks the name against the content.
* **One change to the supplied SVGs.** Each carries an 8 KB embedded C2PA `<metadata>` provenance manifest that no browser reads and that no longer verifies once a file is touched; it and its `xmlns:c2pa` declaration are removed. The drawing is not touched. The validator proves that every paint in a shipped SVG is one of the four dark-ground brand colours (the logo must carry all four) and that no script, text, embedded image or link is present. The originals stay in the package. PNGs and the `.ico` are copied byte for byte.
* **Markup.** Header: `<a class="brand" …><img class="brand-logo" src="/assets/brand/orbgss-logo-light.de682b8e.svg" alt="" width="634" height="108" /></a>` (the link's own `aria-label` is the accessible name, "OrbGSS home" / "OrbGSS ana sayfa", so the image is decorative); footer: the same file with `alt="OrbGSS"`. `.brand-logo` is 30 px high (24 px at ≤ 560 px), which is 176 px and 141 px wide: above the brand's 120 px minimum for the horizontal logo. The validator recomputes the width from the CSS height and fails below 120.
* **Theme colour.** `<meta name="theme-color" content="#FFFFFF">` on every page, and `#FFFFFF` as the manifest's `theme_color` and `background_color` (amended 2026-10-25: the header is white).
* **Not used:** `final/assets/illustrative-map.jpg` (a generated illustration; the validator fails if it is placed on a page or shipped) and `final/variant-b/`. The dark-ground logo is not shipped since 2026-10-25 because the header and footer are white.
* **Retired:** `assets/logo.svg` and `assets/mark.svg` (the old text-and-orbit logo and mark) are deleted; the validator fails any reference.

## 5. The map rule

From the brand package: no teal on a map; the area of interest is a gold callout with a dark halo; the base is Graphite neutrals. `scripts/build_locator_map.py` applies it to the Kızıldere locator map: a Graphite-neutral sea (`#121415`) and neighbouring land (`#252A2B`), Türkiye one step lighter (`#2C3233`) with a neutral outline (`#6C7472`), the 36 km area as a Gold Light callout (`#D8B173`, a 22 % fill and a 2 px line) inside a 5 px dark halo. Same Natural Earth source and projection as before; the file is `assets/maps/kizildere-locator-226827d0.svg` (the old file is removed; the name carries the checksum because `/assets/` is immutable). The validator checks the SVG for neutrals and exactly one gold callout, and fails teal.

## 6. What the hero does and does not do

The hero video (class C, a rendered orbital sequence) is **render content**, not UI: its space background is a navy-black baked in at render time. It is not recoloured (no filter, no blend hack, no re-encode), which would also violate the rule that governed pixels are not altered after the fact. The page chrome around it is Graphite.

## 7. Residuals the CTO should know

* **Hero seam (resolved 2026-10-25).** The header is white now, so the near-match described here is a clear boundary and the residual is closed. The original text: on the homepage the header and the page ground were Graphite `#171A1B`; the first frames of the hero video carry a navy-black `rgb(3,12,22)` at their upper left. Placed side by side the two read as one family but not as one colour, and the left of the hero looks slightly bluer than the header. The overlay shade that already blended the hero text zone was re-derived on Graphite so the join is as soft as CSS can make it. The complete fix is to re-render the hero with a Graphite space background (`hero/config/scene.json`, local Blender production), a separate decision and a separate task: it needs new accepted master frames, the two-tier encode and the shot audit again.
* **Social image.** `og:image` is still the hero poster (`assets/hero/hero-poster-1600.webp`), which has no logo in it. A Graphite OG card with the logo is an option, not part of this task.
* **Decorative language separator.** The `|` between EN and TR is `aria-hidden` and at the line colour (1.63:1). It is decoration, not information, and unchanged in kind from the Atlas build.
* **Icon files are the supplied ones.** The 192 and 512 px manifest icons have rounded, transparent corners as delivered; the 180 px touch icon is a full-bleed opaque square. No maskable variant was supplied, so the manifest declares `purpose: any` only (the two PNGs and the SVG favicon).

## 8. What the validator enforces

`scripts/validate_site.py` (the brand checks are `agate_brand_checks`, the palette checks the Atlas foundation's, now on `AGATE_TOKENS`):

1. every palette token, defined once in `:root`, exactly; the validator recomputes the 19 text/ground contrast pairs against their floors (7:1 for the main roles, 4.5:1 for teal and the paper tones);
2. no other colour literal in `styles.css`, any `<style>` block or any inline style; no retired token; no gold fill;
3. `assets/brand/brand.json` records the Agate identity, the approved palette and exactly the seven roles, with source and shipped SHA-256, size and name-by-hash for each; no unrecorded file in `assets/brand/`;
4. each SVG paints only brand colours for its ground (the light-ground logo all four light-background colours) and holds no metadata, script, text, image or link; each PNG is a plain PNG of the right size; `favicon.ico` holds 16, 32 and 48 px;
5. every page's head carries the favicon links, the touch icon and the white `theme-color`; no page still names the old logo files or the text wordmark; the header and footer brand markup is exactly as in §4; `.brand-logo` never goes under 120 px wide;
6. `site.webmanifest` icons and colours; `favicon.ico` is in `.vercelignore`; the illustrative map is not placed or shipped;
7. the locator map follows the map rule.

`scripts/negative_tests_agate_brand.py` breaks each of those in memory (38 cases) and the suites of earlier tasks were updated to the new tokens and files; run them one at a time in a detached worktree (`tasks/MER-279_EVIDENCE.md`).

## 9. Handed over, and for the CTO

* **No change to the Atlas open items.** A1 (MER-151 derivatives full-size on the Geothermal page), the CTO's reading of the new Turkish copy, the font and colour-map licence links and the empty MER-242 slots stay exactly as `docs/WEB_ATLAS_DESIGN_AUTHORITY.md` §8 left them. This task neither resolves nor worsens them.
* **Decisions only the CTO can take:** (1) whether to re-render the hero on a Graphite space background (§7); (2) whether to add a branded social card (§7); (3) acceptance of the Agate colours and the new locator map as the published look, then the separate authorization to publish.
* **Nothing here is merged, deployed or on the public domain.**
