# WEB light theme and plain-spoken pages — what the site shows and what it keeps back

**Task:** CTO request of 2026-10-25 ("the pages feel too dark", then "the homepage needs the same contrast", then "do not explain how the app works behind the scenes").
**Status:** **review, pending CTO acceptance.** Nothing here is published. It becomes binding only when the CTO accepts the reviewed branch and authorizes a publication.
**Baseline:** the Agate adoption (`claude/project-thread-wbral7`, MER-279, PR #1). This work changes the grounds of the pages, the logo role, and removes copy; it does not touch imagery, the scientific rasters, the hero video, type, fonts, the page set, the navigation, the URLs or the contact route.
**Recoloured 2026-10-25 (Heat Trace, `docs/WEB_HEAT_TRACE_BRAND_AUTHORITY.md`):** the grounds keep their roles and this document's page map, but the colours named below are now Night `#160A19` (was Ground `#171A1B`), Night lift `#241E25` (was Ground lift `#252A2B`) and Pumice `#F7F5F8` (was Limestone `#F6F5F2`); the logo file is `orbgss-logo-light.27e93f98.svg`. Read "Limestone", "Ground" and "granite" below as Pumice, Night and dark.
**Review (2026-10-25):** independent review PASS at the first head; its findings and the CTO's closing-band request are folded in (§0, §3, §4).
**Governs, once accepted:** the grounds of every page, the colour of the header and footer, the logo role, and the rule on what the public site explains. It wins over `docs/WEB_AGATE_BRAND_AUTHORITY.md` §2 (grounds), §4 (logo role, theme colour) and the "mandatory warning" lines of `CLAUDE.md`, `docs/WEB_ATLAS_DESIGN_AUTHORITY.md` and `docs/WEB_ATLAS_GEOTHERMAL_AUTHORITY.md`.

## 0. Özet (CTO için)

* **Açık tema.** Üst ve alt çubuk beyaz; onayladığın açık zemin logosu tasarlandığı gibi görünüyor. Sayfalar Limestone (sıcak açık gri) üzerinde, granit/antrasit zeminler yalnızca fotoğrafın veya renkli sonucun öne çıktığı yerlerde. Ana sayfada hero videosu ve Kızıldere bandı koyu kaldı, üç evre kanıtı, inceleme aracı ve Çözümler bölümü açık oldu; Evre 4 (sonuç) koyu kaldı. Böylece diğer sayfalardaki kontrast ana sayfada da var.
* **Sade içerik.** Sayfa içi gezinme çubukları (Jeotermal'de dört bölüm, Kaynaklar'da dört bölüm, Çözümler'de pilot çubuğu) kalktı. Katman atlasındaki her katmanın altındaki altın çizgili uyarılar, sonuçtaki uyarı ve "neyi ortaya koymaz" tablosu kalktı. Katmanların nasıl kullanıldığını, skorun nasıl hesaplandığını anlatan her metin (ana sayfa ve Jeotermal) çıkarıldı; site ne sunduğunu söylüyor, nasıl yaptığını değil. İlgilenen bizimle iletişime geçiyor.
* **İnceleme düzeltmeleri (aynı gün).** Bağımsız inceleme geçti; bulguları işledik: Jeotermal'deki "katmanlar tek skorda birleştirilir" cümlesi çıktı. Sayfa kaynağındaki tüm yorum satırları (ana sayfadaki ~15 KB'lık çalışma notları dahil) silindi, notlar `docs/`'ta duruyor. Görsellerin nasıl hazırlandığını ve karar notlarını taşıyan `assets/imagery/sources.json` depoda kalıyor ama artık siteden sunulmuyor. Mobil alt menü gölgesi ve atla bağlantısının odak halkası düzeltildi.
* **Kapanış "Partner with us" bandı kalktı** (senin isteğin): her sayfada zaten üstte, altta ve ana sayfada hero'da bağlantı var; sayfalar içeriğiyle ve alt çubukla bitiyor.
* **Senin kararın gereken:** §6.

## 1. Grounds

The names stay structural: `ground-orbit` and `ground-lift` are the dark grounds (Ground `#171A1B`, Ground lift `#252A2B`), `ground-paper` the light ground (Limestone `#F6F5F2`). The header and footer are white (`--white` `#FFFFFF`, the brand token `--ogs-bg-surface`), not Limestone, so the logo and the page edge read as two surfaces.

| Page | Light | Dark |
| --- | --- | --- |
| Home | Act 3 evidence trio, inspection aid, Solutions section | hero (video), Act 2 Kızıldere band, Act 4 priority result |
| Solutions | opening, Mining and Marine pair, footnote | the photographic Geothermal band and the two domain images |
| Geothermal | pilot record, layer atlas, "what is missing" | the photographic opening, the priority result and its relief slot |
| About | opening, statement, principles, data section | the problem statement |
| Partner | opening | the conversations |
| Sources | the four parts | the opening |

Components take their colours from role variables (`--fg`, `--fg-2`, `--link`, `--limit`, `--limit-line`, `--hair`, `--hair-soft`, and since this change `--surface`, `--matte`, `--wash`). The default roles and the dark scope (`.ground-orbit`, `.ground-lift`, `.domain-card`, `.domain-band`) are the dark ones; the light scope (`.ground-paper`, `.site-header`, `.site-footer`) redefines them, so a component nested in either reads correctly and a dark band on a light page needs no override. The validator checks both scopes.

Measured in the browser (`tasks/LIGHT_THEME_EVIDENCE.md`): every text node off a photograph is at least 4.5:1 against its rendered ground on every route in English and Turkish at 390 and 1440 px, and no route scrolls sideways at 320, 390, 768, 1024 or 1440 px. Text over a photograph keeps the per-panel caption tone and halo.

## 2. Logo, icons, theme colour

The horizontal logo for light grounds (`final/logo/orbgss-logo-light.svg` of the approved package) replaces the dark-ground one in the header and the footer on every page: `assets/brand/orbgss-logo-light.de682b8e.svg`, built by `scripts/build_brand_assets.py` (role `logo-light` in `assets/brand/brand.json`; the dark-ground logo is no longer shipped). The favicon family is unchanged. `theme-color` and the manifest's `theme_color` and `background_color` are `#FFFFFF`, the colour of the header. The hero seam recorded as a residual in the Agate document (§7) is gone: the header is white against a dark hero, so there is a boundary instead of a near-match.

## 3. What the public site does not explain

The site says what OrbGSS delivers, not how it gets there. Removed in English and Turkish, and refused by the validator if they return (`RETIRED_EXPLANATION_KEYS`):

* the in-page section bars: the Geothermal chapter bar, the Sources index, the Solutions pilot bar;
* the per-layer warnings under every plate of the layer atlas, the warning under the priority result and under the homepage Kızıldere band, the legacy `story.*.note` warnings, and the Geothermal ledger of what the result does and does not establish;
* every sentence on how a layer is used, what it is not, how the score is built and what it does not mean (homepage Act 3 bodies, the Act 4 definitions, the inspection note, the homepage structure-gap footnote, the Geothermal glance and gap copy);
* "limits" in titles, descriptions and the About position statement ("evidence layers and their gaps" now);
* the Geothermal result sentence that said the layers are combined into one score (it says "One experimental ranking, 0 to 100, orders ground inside this area only." now; `RETIRED_METHOD_PHRASES` refuses the old wording in both languages);
* the closing Partner band: the dark line with one Partner link that ended the homepage, Solutions, About and Geothermal ("Discuss a pilot"), its CSS and the key `geothermalPage.next` (CTO, 2026-10-25: the header and the footer already carry Partner with us, and the hero keeps its own link). `#contact` is gone with it; a `/#contact` link opens the homepage.

`assets/imagery/sources.json` records the decision (`public_warnings`: status `retired`, decided by the CTO on 2026-10-25). The seventeen `visible_warning` records stay as the wording of record, so a reinstatement would use the approved text; the validator now fails when one of their i18n keys is in the dictionary or rendered on any page, English or Turkish.

**The page source and the served files say nothing either (review, 2026-10-25).** Deployed pages carry no HTML comment: the homepage's working notes (display windows, how the figures are prepared, build scripts, internal task ids, about 15 KB), the Sources page's licence-year note and the "generated file" line of the Turkish pages were removed. The notes are kept, verbatim, in `docs/WEB_HOMEPAGE_SOURCE_NOTES.md`, which is not deployed. `assets/imagery/sources.json` holds each figure's display window, gamma, palette stops, source rasters and the CTO's decisions; it stays in the repository because the validator reads it, but `.vercelignore` ignores it after the allowlist (`/assets/imagery/sources.json`), so the site returns 404 for it. The repository itself is public on GitHub (`STATUS.md`, open decision 5), so this keeps the *site* quiet, not the repository; whether the repository should be private is the CTO's call.

**Unchanged:** the score's public label, *Remote-Sensing Relative Priority — Experimental Baseline*, and the claim discipline in copy (never probability, reserve, discovery, drilling-success likelihood, Full Prospectivity or a cross-AOI score; `PROHIBITED_SCORE_COPY`); the illustrative-imagery footnote on Solutions; the cinematic hero's "Rendered orbital sequence — not sensor imagery" line; the data-gap and "accepted, not shown yet" placeholders on the Geothermal page; every caption's place, coordinates and layer line; the attribution in the footer and the Sources page.

## 4. What the validator enforces

`scripts/validate_site.py`: `--white` and its five contrast pairs; header and footer on white; the light and dark scopes' role variables; the grounds per page (above); the `logo-light` role, its four light-ground brand colours and the white `theme-color` and manifest; no `.beam-note`, `.plate-note` or `.warning-label` in the stylesheet or on a page; no in-page bar class on any page; none of the retired keys in the dictionary; no retired warning key in the dictionary or on a page; `public_warnings` in the manifest.

Added after review: no HTML comment in any deployed page (`light theme: … carries an HTML comment`); `RETIRED_METHOD_PHRASES`; no `page-closing` or `sec-contact` class and no `#contact` on any page, and the footer must link to Partner with us (`/partner/`, `/tr/is-birligi/`); the Solutions footnote closes the page; the skip link's focus ring is Agate Teal and the mobile Solutions sublist resets the dropdown shadow. `scripts/validate_site.py` also models one new `.vercelignore` form, an exact-path line after the allowlist, requires `assets/imagery/sources.json` to be ignored by it, and fails if a page links the file.

`scripts/negative_tests_light_theme.py` (27 cases) and `scripts/negative_tests_mer237.py` (the ignore rules) break each in memory; the suites of earlier tasks were updated to the new grounds and strings (`atlas_geothermal`, `atlas_solutions_about`, `atlas_partner_sources`, `atlas_foundation`, `agate_brand`, MER-240, MER-241, MER-255, WEB-005B, WEB-005C). Run them one at a time in a detached worktree.

## 5. Not changed

Hero video and its masters; every governed raster and its derivatives, windows and checksums; the four-act homepage order; the Solutions cards' links; navigation, URLs, redirects, hreflang, sitemap; the contact route and its subjects; type and fonts; `.vercelignore`. The Turkish pages are regenerated from the English pages and the dictionary (`scripts/build_tr_pages.py`); the new and rewritten Turkish strings are marked for the CTO's language review, as before.

## 6. For the CTO

1. **One neutral line near the results?** The warnings are gone as asked. A single short, neutral site-level line near the priority result (for example "Illustrative pilot output; not a resource or drilling-success claim") is the one thing worth deciding on purpose. None is on any page.
2. **Pilot record details.** The Geothermal record still lists the 30 m grid, EPSG:32635 and the score's name and range. They are facts, not method, but you may prefer to keep the grid and projection for the conversation.
3. **Placeholders.** "What is missing" on the Geothermal page and the two pending plates say publicly what is not yet shown. Keep, or remove the section.
4. **About.** The principles still say how OrbGSS publishes (for example "one declared area, projection and grid before any interpretation") and the page closes with "No accuracy, performance, deployment, customer or scale figures are published for this baseline." Both can go.
5. **Turkish copy.** The rewritten Turkish strings need your reading.
6. **Publication** is a separate authorization. Nothing here is merged or deployed.
