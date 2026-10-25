# WEB Atlas redesign — colour, type and shared components

**Task:** MER-275 (foundation of the full-site redesign; parent MER-274). Page groups: MER-276 Geothermal, MER-277 Solutions and About, MER-278 Partner and Sources.
**Status:** **preview, pending CTO acceptance.** The CTO approved the palette and type page on 2026-10-24 and asked for the whole site in the new design as a finished preview. Nothing here is published; it becomes binding only when the CTO accepts the reviewed preview and authorizes a publication.
**Baseline:** `claude/premium-interior-redesign-65zdlt@fe8cc470` (MER-255 on top of MER-241, both unpublished).
**Governs, once accepted:** colour, type, fonts, grounds and the shared components of every page. It wins over `docs/DESIGN_AUTHORITY.md`, `docs/WEB_VNEXT_AUTHORITY.md` and `docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md` on those points only. It changes nothing in the scientific, legal, claim and content rules, and nothing in the homepage's four acts.
**Superseded in part (MER-279, 2026-10-25):** the CTO approved the Agate brand identity. Its palette, grounds' colours, logo and favicon family replace §0 (colour bullet), §1 and §2 (colours) below; read `docs/WEB_AGATE_BRAND_AUTHORITY.md` for them. Type (§3), fonts (§4), the homepage (§5), regions (§6), the validator contract's structure (§7) and the structural rules of §1 (one colour system, ground-aware roles, no colour in a figure frame) stand. The Atlas colour names and values below are kept as the record of what MER-275 built.
**Brief:** `/mnt/project-files/site-redesign/SPEC.md`. **Approved page:** https://claude.ai/artifact/TowszhEqnCko89rsQsP9d9.

## 0. Özet (CTO için)

* **Renk (MER-279 ile Agate paletine geçti, bkz. `docs/WEB_AGATE_BRAND_AUTHORITY.md`; aşağıdaki Atlas renkleri kayıt için duruyor):** Sitede artık yalnızca beş renk rolü var: Orbit (koyu zemin), Paper (açık zemin), Steel (ikincil yazı), Signal (tek vurgu, cyan) ve Caution (sınır ve uyarı). Açık zeminde okunabilsinler diye Signal ve Caution'ın birer koyu tonu var. Çizgiler Steel'in saydam hâli. Eski cyan, bronz ve onlarca gri kalktı. Doğrulayıcı bu listenin dışında renk kullanılırsa derlemeyi durduruyor.
* **Yazı tipi:** IBM Plex Sans (başlıklar 300, metin 400) ve IBM Plex Mono (veri, etiket, alt yazı). Space Grotesk yok, kalın (500/700) yok; vurgu renk tonuyla. Dosyalar kendi sunucumuzdan geliyor (üç dosya, toplam 59 KB), Google'a istek gitmiyor. IBM "Plex" adını ayırdığı için alt kümeler "OrbGSS Sans" ve "OrbGSS Mono" adıyla yeniden adlandırıldı; lisans metni ve IBM'in telif satırları yanında duruyor.
* **Ana sayfa:** Dört perde, görseller, metin, hareket aynen duruyor. Yalnızca yazı tipi ve renk eşlemesi değişti; "Know where / to look next." iki satırda kalıyor.
* **Henüz yapılmadı:** Geothermal, Solutions, About, Partner ve Sources sayfalarının yeni içeriği ve yerleşimi (üç ayrı iş). Bu sayfalar şimdilik MER-255'in düzeniyle, yeni renk ve yazı tipiyle görünüyor.
* **Senin kararın gereken:** §8.

## 1. Palette — the only UI colours (Atlas values; superseded by Agate, MER-279)

> **Superseded.** Since MER-279 the only valid palette is the Agate one in `docs/WEB_AGATE_BRAND_AUTHORITY.md` §1. The structure of this section survives (one palette defined once in `:root`, ground-aware roles, no colour in a figure frame, retired tokens may not return); the names and values below do not. Mapping, for anyone reading older evidence: `--orbit` → `--ground` `#171A1B`; `--lift` → `--ground-lift` `#252A2B`; `--paper` → `--mist` `#E3E5E4` as text on dark and `--limestone` `#F6F5F2` as the light ground; `--steel` → `--mineral-light` `#B7C0BD`; `--slate` → `--graphite-soft` `#565D5A`; `--signal` → `--teal-light` `#58AEB2`; `--signal-deep` → `--teal` `#18777A`; `--caution` → `--gold-light` `#D8B173`; `--caution-deep` → `--gold-ink` `#735525`; text on paper is `--graphite` `#202629`. The validator fails every Atlas token name.

Defined once in `:root` of `styles.css`; `scripts/validate_site.py` pins every value.

| Token | Value | Role | Contrast (measured) |
| --- | --- | --- | --- |
| `--orbit` | `#030B12` | dark ground; text on paper | Paper on Orbit 17.95:1 |
| `--lift` | `#061420` | derived dark step: indexes, the Mining/Marine pair, the Act 4 stage | Paper on Lift 16.86:1, Steel on Lift 8.43:1 |
| `--paper` | `#F2F4F5` | light ground; primary text on dark | Orbit on Paper 17.95:1 |
| `--steel` | `#9EB1C1` | secondary text, captions, emphasis tone | Steel on Orbit 8.97:1 |
| `--slate` | `#5B6B76` | Steel on paper | Slate on Paper 5.00:1 |
| `--signal` | `#73E7FF` | the only accent: links, active nav, kickers, focus ring, the homepage target frame | Signal on Orbit 13.77:1 |
| `--signal-deep` | `#0E6D81` | Signal on paper | 5.40:1 |
| `--caution` | `#C8A97A` | limits, data gaps, mandatory warnings | Caution on Orbit 8.88:1 |
| `--caution-deep` | `#7F602F` | Caution on paper | 5.26:1 |
| `--rule`, `--rule-soft` | `rgba(158,177,193,.22)` / `.11` | rules on dark | |
| `--rule-paper`, `--rule-paper-soft` | `rgba(3,11,18,.14)` / `.08` | rules on paper | |

**Rules.**

1. **Nothing else is a UI colour.** The stylesheet, `<style>` blocks and inline styles may use the nine hexes, `rgba()` of a palette triple at any alpha, `transparent` and `currentColor`. Every other hex, `rgb()` of anything else, `hsl()`, `color-mix()` and every CSS named colour fails the validator. Images are exempt: rasters, the legend ramp, the hero video and poster, and the logo SVG.
2. **Caution is a line and a label, never a fill.** The validator fails a rule that fills a background with a caution value.
3. **Scientific colour maps are not part of this system.** No UI colour goes inside a figure frame, and no CSS filter, transform or upscale goes on a governed raster.
4. **Ground-aware roles.** Components never name a ground colour for their text; they use `--fg`, `--fg-2`, `--link`, `--limit`, `--hair` and `--hair-soft`, which `.ground-orbit`, `.ground-lift` and `.ground-paper` set. The same component therefore reads correctly on dark and on paper.
5. **Retired:** every `--orb-*` token and the MER-255 grey tokens (`--accent`, `--line`, `--bg`, `--beam`, `--text`, `--muted`, `--dim`, and their variants). The validator fails any use. Retired values include `#43BFF0`, `#82D3F3`, `#98F5FF`, `#8AF1FF`, `#7FEFFF`, `#3CCBFF`, `#14698F`, the bronzes and the extra lights and greys.
6. **Caption tone.** The per-panel `data-label-tone` stays; light tone maps to Paper with an Orbit halo, dark tone to Orbit.

## 2. Grounds (colours superseded by Agate, MER-279)

> The three grounds keep their structural class names `ground-orbit`, `ground-lift` and `ground-paper`; their colours are now Ground `#171A1B`, Ground lift `#252A2B` and Limestone `#F6F5F2`.

* **Orbit:** every page opening (the header merges into it), every photograph, every analytical plate, the priority score, the header and the footer on every page.
* **Lift:** index bars, the Mining and Marine pair, the homepage Act 4 stage.
* **Paper:** reading records only: the Geothermal pilot record and its locator map, the "Establishes / Does not establish" ledger, the About statement and principles, the Sources body.

The five deliberate changes from the design package (About, Partner and Sources open on Orbit; Mining and Marine on Lift; the Geothermal result on Orbit) are carried out by the page threads. This foundation supplies the three ground wrappers and nothing page-specific.

## 3. Type

Two families, two weights. **OrbGSS Sans** 300 (display) and 400 (text and UI); **OrbGSS Mono** 400 (data, kickers, captions). There is no 500 and no bold; `body` sets `font-synthesis-weight:none`, and emphasis is tone (Steel, or Slate on paper).

| Token | 1440 → 390 px | Face | Use |
| --- | --- | --- | --- |
| `--t-page` | 92 → 44 | Sans 300, −0.03em | page title (the homepage h1) |
| `--t-section` | 54 → 34 | Sans 300, −0.025em | section title |
| `--t-statement` | 44 → 28 | Sans 300, −0.025em | statement |
| `--t-figure` | 21 → 19 | Sans 400, −0.01em | figure heading |
| `--t-lede` | 19 → 17 | Sans 400 | lede |
| `--t-body` | 17 → 16 | Sans 400 | body |
| `--t-warning` | 14 | Sans 400 | mandatory warning |
| `--t-label` | 11 | Mono 400 caps, `--track` .14em | kicker, data label, nav, links, buttons |
| `--t-caption` | 10.5 → 10 | Mono 400 caps, `--track` | image caption, never below 10 px |

Mono capitals come in exactly the two sizes `--t-label` and `--t-caption` and one tracking, `--track`. Turkish pages carry `lang="tr"`, so capitals render İ, Ş and Ğ.

## 4. Fonts

* **Files:** `assets/fonts/orbgss-sans-300.d8ab34ee.woff2` (22,136 B), `orbgss-sans-400.39dbd03f.woff2` (20,972 B), `orbgss-mono-400.62ab771d.woff2` (17,048 B): 60,156 B per page, under the 64 KiB budget. They are hash-named because `/assets/` is served immutable. `assets/fonts/fonts.json` records, per face, the upstream npm file and its SHA-256, the shipped SHA-256 and size, the family and the unicode range.
* **Source:** IBM Plex Sans Light, Plex Sans Regular and Plex Mono Regular from `@ibm/plex-sans@1.1.0` and `@ibm/plex-mono@1.1.0` (SIL Open Font License 1.1), fetched through `cdn.jsdelivr.net` with the upstream SHA-256 pinned. `scripts/build_fonts.py` rebuilds them (`--check` compares a fresh build with the record). It is local tooling (fontTools and brotli); nothing about it runs on the site and no package manager enters the repository.
* **Subset:** Latin, Latin-1 and Turkish plus the four diagonal arrows the Sources page draws; layout features kept (kerning, ligatures, Turkish `locl`); hinting kept. One file per face serves English and Turkish.
* **Name:** IBM reserves "Plex". The name table of each subset is renamed to "OrbGSS Sans" and "OrbGSS Mono"; the copyright, trademark and licence strings stay. `assets/fonts/OFL.txt` carries the full licence, IBM's notices (2018, 2017) and a header explaining the renaming. The validator fails a family name that contains "Plex" and a licence file that loses IBM's notices.
* **Loading:** `font-display:swap`, a `unicode-range` on each face, and a preload of Sans 300 and Sans 400 before the stylesheet on every page. Metric-matched fallback faces (`size-adjust`, ascent and descent overrides over Arial and Courier New) keep line breaks where they are until the webfont arrives; the Sans 300 values are measured here.
* **No third-party request.** No Google Fonts, no CDN at run time.

## 5. The homepage

Composition, imagery, copy, motion and the four acts are exactly as accepted (`docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md`). Only the fonts and the colour mapping change.

* The hero h1 uses `--t-page` with `text-wrap:balance`; "Know where / to look next." stays on two lines at every width measured (360 to 1920 px). In Turkish it takes three lines above 1000 px and at 360 px, and two between 390 and 820 px. The hero lede uses `text-wrap:pretty` to avoid a one-word last line.
* The handoff target frame is Signal. The rendered hero video does not clash with it (viewed at 1440); no re-render was needed and none was done.
* Act 3's three evidence panels, Act 4's result and the inspection aid keep their governed rasters untouched (no filter, no transform, no upscale); only the stage and the text around them use tokens. The Act 4 stage is Lift with a Steel hairline.
* The `.button` shape (11 px radius) and the Solutions cards are unchanged apart from tokens and type.

## 6. Regions and ownership

The three page threads work in parallel; the foundation cut every shared file into marked regions so they do not collide.

| Region | `styles.css` | `script.js` dictionary (EN and TR) | `validate_site.py` | Negative test |
| --- | --- | --- | --- | --- |
| foundation | `atlas:foundation` (shared components, header, footer, responsive) | all keys outside the three regions below | `atlas:foundation` | `negative_tests_atlas_foundation.py` |
| homepage | `atlas:home` | (shared keys) | (foundation) | (foundation) |
| interior shell | `atlas:shell` (interior page shell, 404, chapters) | (shared keys) | (foundation) | (foundation) |
| MER-276 Geothermal | `atlas:geothermal` | `atlas:geothermal`, prefix `geothermalPage.` | `atlas:geothermal` | `negative_tests_atlas_geothermal.py` |
| MER-277 Solutions + About | `atlas:solutions-about` | `atlas:solutions-about`, prefixes `solutionsPage.`, `aboutPage.` | `atlas:solutions-about` | `negative_tests_atlas_solutions_about.py` |
| MER-278 Partner + Sources | `atlas:partner-sources` | `atlas:partner-sources`, prefixes `partnerPage.`, `sourcesPage.` | `atlas:partner-sources` | `negative_tests_atlas_partner_sources.py` |

A page thread edits its own region only. A change to a shared component (anything in `atlas:foundation`, the tokens, the fonts, the header or footer) goes back to the foundation, not into a page region. Each page region, when its thread lands, registers itself in `ATLAS_GROUPS` (dictionary prefixes) and sets `type_ready` to true once its CSS holds to the type rules in §7; until then the legacy MER-255 rules in that region keep their old sizes.

## 7. What the validator enforces

`scripts/validate_site.py` (`atlas_foundation_checks`) fails the build when:

(Since MER-279 the colour items below read in Agate terms — the `AGATE_TOKENS`, a gold fill instead of a caution fill, the Ground instead of Orbit — and `docs/WEB_AGATE_BRAND_AUTHORITY.md` §8 adds the brand-mark checks.)

* a palette token is missing, defined twice or off its pinned value; a retired token is used; a promised text and ground pair falls below its contrast floor (7:1 on dark, 4.5:1 on paper);
* styles.css, a `<style>` block or an inline style carries a colour that is not in the palette; a rule fills a background with a caution value;
* a font family other than `var(--sans)`, `var(--mono)` or `inherit` is named, a `font` shorthand is used, a weight other than 300 or 400 is set, `font-synthesis-weight:none` is missing, or a retired family is named;
* `fonts.json` is missing or its hashes, sizes, names, upstream pins, per-page budget, `@font-face` list, `font-display`, `unicode-range`, fallback `size-adjust`, licence notices or preloads do not hold;
* the CSS, dictionary or validator regions are not exactly those in §6, one is missing its negative-test file, or a dictionary key sits in the wrong region;
* in a region marked type-ready (foundation, home, shell, and each page group once it opts in) text is set under 10 px, capitals use another tracking, or capitals use a size other than `--t-label` or `--t-caption`;
* a shared component (kicker, text link, caption, warning, record list, plate and the grounds) is missing, the warning loses its 2 px Caution rule, a plate gains border, radius, shadow, outline or hover, the header or footer is not on Orbit, the paper ground loses a role, or the homepage target frame is not Signal.

`negative_tests_atlas_foundation.py` proves each of these fires (39 cases). The three page-group negative-test files are empty until their threads fill them.

**Not enforced by the validator:** where a page uses a ground (the §2 assignments), the heading scale on interior pages, the look of any page region that is not type-ready, and line breaks of any headline other than the homepage hero. Those are checked by measurement in the page threads and the review, not by a script.

## 8. Handed over, and for the CTO

* **A1–A9 of `CTO Design Review.dc.html`** are implemented in the page threads, not here, and each needs the CTO's explicit acceptance before any publication. A1 (MER-151 derivatives shown full-size on the Geothermal page) also widens the MER-151 homepage-only scope, which is a scientific-asset decision.
* **Sources font licence (A8):** the font licence and IBM's copyright notices must appear on `/sources/`. The files are in `assets/fonts/OFL.txt`; the page entry belongs to MER-278.
* **Legacy text under 10 px** remains in two page regions until their threads restyle them: the Geothermal stack labels (8 px) and the Sources `dt.mono` (9.5 px). The validator will fail them when each region opts into `type_ready`.
* **Interior page titles** still use the MER-255 sizes; the page threads move them onto `--t-page` and `--t-section`.
* **Turkish copy** for new strings is marked pending the CTO's language review; the foundation adds no visible string.
* **Logo:** untouched. It still uses a five-blue gradient; making it single-colour is a separate later step.
* **Turkish hero headline** takes three lines on desktop ("Sırada nereye / bakacağınızı / bilin."); the homepage keeps its accepted composition, so this is left as measured.
