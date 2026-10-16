# WEB M6 — Information architecture and page content authority

**Task:** MER-238 (Milestone 6 — Bilgi Mimarisi ve Gösterim Odaklı Sayfalar)
**Status:** approved by the CTO on 2026-10-15 (in the MER-238 session: "MER-238'i onaylıyorum; D1'de Science'tan MER-151 türevlerini isteyelim, D2 için Türkçe sözcükler olsun."). D1 and D2 are decided (§9); D3–D5 stay open. **Implementation:** MER-240 builds the English pages on its own branch (`REVIEW_READY` 2026-10-16, not published; `tasks/MER-240_EVIDENCE.md`); G3, G4 and the G2 thumbnails wait for MER-242, V4 waits for D5, and `/tr/` is MER-241. Until MER-240 is published, the live site is unchanged.
**Baseline:** `mertkaanakgunlu/mer-218-website-mer-216-canonical-publication-closure@5ca7bdd4` (MER-216 is not yet published and MER-237 is not yet accepted, so this is the baseline MER-238 names).
**Consumers once approved:** MER-239 (writes the approved rules into `CLAUDE.md` and the other authorities), MER-240 (builds the English pages), MER-241 (generates the static `/tr/` pages).
**Mockups:** `docs/mockups/m6/` (open locally); screenshots in `evidence/mer238/`.

## 0. Özet (CTO için)

* **Menü:** Home · Solutions ▾ (Geothermal, Mining, Marine) · About · Partner with us · EN | TR.
* **Sayfalar:** `/` (anasayfa, dört bölüm değişmez) · `/solutions/` (üç alanın karşılaştırması) · `/solutions/geothermal/` (Kızıldere pilotunun tamamı) · `/about/` (ilkeler ve veri kaynakları) · `/partner/` (görüşme türleri ve e-posta).
* **Kalkanlar:** `/platform/` (yazılım ayrıntısı) → `/`; `/pilot/` → `/solutions/geothermal/`; `/company/` → `/about/`; `/contact/` → `/partner/`. Hepsi 301 ile yönlendirilir, eski bağlantılar kırılmaz.
* **Anasayfa:** dört ana bölüm ve inceleme aracı aynen kalır. Method ve Company bölümleri kalkar, içerikleri About'a taşınır. Contact bölümü tek satırlık bir Partner bağlantısına iner. Solutions kartları yalnızca görsel, alan adı ve durum etiketi taşır.
* **Kurallar:** her bilgi tek bir sayfada; görsel tam boyutta tek yerde; her bölüm bir görsel, harita, grafik ya da tabloyla açılır; metin sınırlı (bölüm başına 40 kelime); yazılım ve geliştirme ayrıntısı yok.
* **Türkçe:** `/tr/`, `/tr/cozumler/`, `/tr/cozumler/jeotermal/`, `/tr/hakkimizda/`, `/tr/is-birligi/`.
* **Karar (2026-10-15):** belge ve maketler onaylandı. D1: kabartma üstü öncelik ve ALT-02 için Science'tan MER-151 türevleri istenir (MER-242); gelene kadar bu iki bölüm sayfada yer almaz. D2: Türkçe adreslerde Türkçe sözcükler.
* **Hâlâ açık:** D3 (KVKK/gizlilik, hukuki karar), D4 (`contact@orbgss.com` doğrulaması), D5 (Marine için kıyı sahnesi).

## 1. Binding decisions

From the CTO, 2026-10-15 (Milestone 6 and this task's decision round):

1. Navigation: Home / Solutions (Geothermal, Mining, Marine) / About / Partner with us / EN | TR.
2. No information is repeated across pages.
3. No detailed software or development content.
4. Content is shown first — images, maps, charts, tables — and text is short, clear and never drowns the page.
5. Every page except the homepage is reworked. The homepage's four acts do not change.
6. Turkish ships as static `/tr/` pages.
7. Solutions: one hub page plus a dedicated Geothermal page. Mining and Marine stay as hub sections until they have something to show.
8. Homepage: light trim. The four acts and the inspection aid stay; the Solutions cards stay as the entry to the domains; Method and Company leave the homepage for About; Contact becomes one Partner line.
9. About carries no team, address or legal-entity details: none exist in canonical material, and WEB-003 forbids personal biographies.
10. Partner with us is email only. No form, backend, CRM, analytics or cookies.

Everything else in `CLAUDE.md` that this document does not explicitly replace stays binding: the stack, the claim discipline, the score label and its warnings, the Geothermal / Mining / Marine taxonomy and its aliases, the class-B raster rules, the imagery rights policy and the caption rules.

## 2. Page set, URLs and navigation

| Page | EN URL | TR URL (MER-241) | Purpose |
| --- | --- | --- | --- |
| Home | `/` | `/tr/` | The story, shown: hero, the real place, three layers, the result. Unchanged acts. |
| Solutions | `/solutions/` | `/tr/cozumler/` | Where OrbGSS works today and where it is going, compared in one table. |
| Geothermal | `/solutions/geothermal/` | `/tr/cozumler/jeotermal/` | The reference sheet for the Kızıldere pilot: where it is, every layer and its limits, what is missing. |
| About | `/about/` | `/tr/hakkimizda/` | What OrbGSS is, the principles it publishes by, and every data source it uses. |
| Partner with us | `/partner/` | `/tr/is-birligi/` | Which conversation to start, and the address to start it at. |
| Not found | `404.html` | (bilingual, MER-241) | Way back into the site. |

Anchor ids stay the same in both languages (`#geothermal`, `#mining`, `#marine`, …), so the generator never has to translate an id and every alias keeps working under `/tr/`.

**Desktop navigation** (right-aligned, in this order; every item a real page or anchor):

| EN label | TR label | Target |
| --- | --- | --- |
| Home | Ana Sayfa | `/` |
| Solutions ▾ | Çözümler ▾ | menu trigger |
| — Geothermal | — Jeotermal | `/solutions/geothermal/` |
| — Mining | — Madencilik | `/solutions/#mining` |
| — Marine | — Denizel | `/solutions/#marine` |
| About | Hakkımızda | `/about/` |
| Partner with us | İş Birliği | `/partner/` — a normal text item; the only boxed call to action stays in the hero |
| EN \| TR | EN \| TR | language switch, no flags; after MER-241 a real link to the equivalent page |

The brand mark links home as today. The mobile menu lists the same items in the same order. The footer navigation lists the same five pages.

## 3. Content rules

These operationalise decisions 2–4. MER-240 enforces R1–R5 in `scripts/validate_site.py`.

* **R1 — one home per fact.** Every fact or claim in section 5 has exactly one page where it is stated. Elsewhere it may only be linked to.
* **R2 — one full-size appearance per visual.** A visual appears at full size on one page only. Elsewhere it may appear only as a thumbnail (at most 160 CSS px on its long side) inside an index table or a card that links to its home. Thumbnails are downscales of existing derivatives; nothing is ever upscaled.
* **R3 — no software or development content.** No workflow steps, pipelines, tooling, file formats, export paths, model or code names, or "how it's built" narration. The pilot's geospatial facts (area, grid, projection, sensors, dates) are not software detail; they live once, in the Geothermal facts table, plus the bottom-right captions.
* **R4 — show first.** Every content section opens with its lead visual: an image, map, chart or table. A page header (kicker, title, intro) is the only block that may be text alone.
* **R5 — text budgets (EN; TR may run up to 15 % longer):**
  * a headline is at most 8 words;
  * a page intro is at most 30 words;
  * a section body is at most 40 words;
  * a table cell is at most 12 words, and a table has at most 7 rows;
  * a page carries at most 250 budgeted words (Geothermal: 350).
* **R6 — fixed texts are exempt from R1 and R5,** because they must travel with what they qualify:
  * each visual's mandatory scientific warning, in its accepted wording;
  * the illustrative-imagery footnote wherever the domain photographs appear;
  * the bottom-right captions;
  * a domain's status label next to its name ("Active · First application" / "Expansion direction");
  * the footer's short attribution and copyright;
  * the "Built by VirgaSoft" mark.
* **R7 — claim discipline is unchanged.** No customer, partner, revenue, accuracy, AI, deployment, field-validation, discovery, reserve or drilling claims. The score is never a probability. Mining and Marine are always expansion directions.
* **R8 — one status vocabulary.** Mining and Marine are labelled "Expansion direction" / "Genişleme yönü" everywhere. The homepage's "In development" goes, which ends the divergence WEB-005C recorded as acceptable.

## 4. Page specifications

The copy below is proposed wording. Where a line says *existing*, the accepted text already in `script.js` is reused verbatim (trimmed only where a budget forces it, and then marked). New strings are given in EN with a TR draft; MER-240 owns the final TR proofread.

### 4.1 Home (`/`) — changes only

| Block | Change |
| --- | --- |
| Hero | Unchanged, except that the secondary call "Partner With Us →" points to `/partner/` instead of a `mailto:`. The same applies to the "Partner With Us →" beside the Act 4 result: the homepage carries no `mailto:` of its own. |
| Acts 2–4 and the inspection aid | Unchanged, apart from their two links into `/pilot/`. The structure/geology footnote under Act 3 stays (a `CLAUDE.md` invariant). |
| Act 3 deep link | "How the layers are built →" (`/pilot/`) describes a build process (R3). It becomes "See every layer →" / "Tüm katmanları görün →", linking `/solutions/geothermal/#layers`. |
| Act 4 deep link | "Read the pilot method →" (`/pilot/`) becomes "See the Kızıldere pilot →" / "Kızıldere pilotunu görün →", linking `/solutions/geothermal/`. |
| Solutions cards | Stay as the three native-link cards, with image, domain name and status label only; the description sentence moves to the hub. New targets: Geothermal → `/solutions/geothermal/`, Mining → `/solutions/#mining`, Marine → `/solutions/#marine`. Mining and Marine read "Expansion direction" (R8). The section title, statement and illustrative footnote are unchanged. |
| Method (`#proof`) | Removed. Its six commitments become the About principles table (4.4). |
| Company (`#company`) | Removed. Its copy becomes the About header (4.4). |
| Contact (`#contact`) | Reduced to one centred line keeping `id="contact"`: "Partner with us →" (existing `contact.cta`), linking `/partner/`. |
| Footer | New navigation. The last attribution sentence "Full provenance is documented in the production package." becomes "Every source is listed on the About page." / "Tüm kaynaklar Hakkımızda sayfasında listelenir." with a link to `/about/#sources`. |

### 4.2 Solutions (`/solutions/`)

| # | Section | Lead visual | Copy |
| --- | --- | --- | --- |
| S0 | Header | — | Kicker "Solutions". Title (new): "Where OrbGSS works today, and where next." / "OrbGSS bugün nerede çalışıyor, sırada ne var." Intro (new, 19 words): "Geothermal is active, with a published pilot. Mining and marine are expansion directions: nothing is published for them yet." / "Jeotermal aktif ve yayımlanmış bir pilotu var. Madencilik ve denizel genişleme yönleri: bunlar için henüz yayımlanmış bir şey yok." |
| S1 | At a glance | **Table** — Domain · Status · Ground it reads · Published today | Geothermal · Active · First application · Geothermal exploration ground · The Kızıldere pilot → `/solutions/geothermal/`. Mining · Expansion direction · Mineral exploration targets · Nothing yet. Marine · Expansion direction · Coastal and marine ground · Nothing yet. The "ground it reads" cells reuse the accepted `domain.*.copy` phrases, so no new capability is claimed. |
| S2 `#geothermal` | Geothermal band | **Full-bleed image** — Yellowstone 2013 (existing `yellowstone-2013-*`) | Name + status label; one link "See the Kızıldere pilot →" / "Kızıldere pilotunu görün →". No sentence: the description lives in S1. Caption bottom-right: place · coordinates · "Natural-color composite". |
| S3 `#mining` (alias `#mineral`) | Mining band | **Full-bleed image** — Chuquicamata 2024 (existing) | Name + status label. Caption as S2. |
| S4 `#marine` (alias `#environment`) | Marine band | **Full-bleed image** — a coastal scene (visual need V4; Ili Delta stays until V4 lands) | Name + status label. Caption as S2. |
| S5 | Footnote | — | The illustrative-imagery footnote (existing `domain` footnote wording, R6). |

The band images are the same scenes as the homepage cards. Under R2 the hub is their full-size home and the cards are links to it.

### 4.3 Geothermal (`/solutions/geothermal/`) — the Kızıldere reference sheet

It replaces `/pilot/` and does not retell the homepage story. The homepage shows the layers working; this page records what they are.

| # | Section | Lead visual | Copy |
| --- | --- | --- | --- |
| G0 | Header | **Locator map** — Türkiye outline with the 36 km area marked at Denizli (new, V1) | Kicker "Geothermal · Active · First application". Title (new): "Kızıldere: the first published pilot." / "Kızıldere: yayımlanan ilk pilot." Intro (new, 25 words): "Everything published for the pilot, in one place: where it is, which layers it holds, what each layer is not, and what is still missing." / "Pilot için yayımlanan her şey tek yerde: nerede olduğu, hangi katmanları içerdiği, her katmanın ne olmadığı ve neyin hâlâ eksik olduğu." |
| G1 `#glance` (aliases `#pilot-observe`) | The pilot at a glance | **Facts table** (key · value) | Area · 36 × 36 km. Place · Büyük Menderes graben, Denizli, Türkiye. Centre · 37.9794° N, 28.7907° E. Grid · 30 m, EPSG:32635, 1,200 × 1,200 cells. Layers · 2 context, 3 evidence, 1 priority surface. Score · Remote-Sensing Relative Priority — Experimental Baseline, 0–100 within the area. Not available · Structure and geology. |
| G2 `#layers` (aliases `#pilot-terrain`, `#pilot-evidence`) | Every layer, and what it is not | **Layer table with thumbnails** — Layer · From · Role · What it is not | Natural colour · Landsat 8 OLI, 2025-05-05 · Context. Elevation · NASADEM · Context. Thermal anomaly · Landsat thermal bands · Evidence. Alteration signal · Sentinel-2 · Evidence. Second alteration signal (iron) · Sentinel-2 · Evidence. Priority · the evidence layers · Score. "What it is not" carries each layer's mandatory warning verbatim (R6). Thumbnails: the homepage's MER-151 derivatives. The iron row shows no thumbnail and reads "Accepted, not shown yet" / "Kabul edildi, henüz gösterilmiyor" until MER-242 delivers its derivative (D1). Layer codes (THM-01, ALT-01, ALT-02) stay out of visible copy, as on the homepage since R14. |
| G3 `#relief` (aliases `#pilot-priority`, `#pilot-geothermal`) | Priority over relief | **Large figure** — the priority surface over shaded NASADEM relief (V2), 0–100 legend. **Shown only once MER-242 delivers its MER-151-family derivative (D1);** until then G3 is absent and its alias anchors sit on G2. | One line (existing `pilotPage.closing.copy`, trimmed): "The priority surface read over NASADEM relief, so ranked ground can be seen against the valleys and ridges it sits on." The priority warning (R6). |
| G4 `#iron` | The second alteration signal | **Large figure** — the iron alteration proxy (V3) with its legend | One line (new): "A second Sentinel-2 proxy, sensitive to iron-bearing surfaces, mapped on the same frame." / "Aynı çerçevede haritalanan, demir içeren yüzeylere duyarlı ikinci bir Sentinel-2 göstergesi." Its warning (R6). **Shown only once MER-242 delivers (D1);** until then G4 is absent and the G2 row reads "Accepted, not shown yet". |
| G5 `#outputs` | What the pilot produced | **Table** — Output · What it is | Area definition · One boundary, grid and projection for every layer. Context layers · Natural colour and elevation, for orientation only. Evidence layers · Mapped remote-sensing signals, each with its limits. Data-gap statement · What is missing, stated instead of filled. Priority surface · One within-area ranking, 0 to 100. Provenance record · The source and export behind every visual. |
| G6 `#gap` (alias `#pilot-structure`) | Not available: structure and geology | **Empty frame** — the panel outline at the same size as the figures, drawn empty with the label "No public-safe fault or lithology layer" | Existing `/pilot/` gap text trimmed to 40 words: "No public-safe fault or lithology layer is authorized for this pilot. The gap is shown, not filled, and it does not change the priority: structure and geology are optional support and score-invariant." |
| G7 | Next | — | One link: "Discuss a pilot →" / "Pilot görüşün →" to `/partner/`. |

Every figure on this page keeps the bottom-right caption: place, coordinates and the accepted public label.

### 4.4 About (`/about/`)

| # | Section | Lead visual | Copy |
| --- | --- | --- | --- |
| A0 | Header | — | Kicker "About". Title (existing `company.title`): "OrbGSS — Orbital Geo-Spatial Solutions". Intro (existing `company.copy`, 22 words). The existing "Built by VirgaSoft" mark. |
| A1 `#principles` | How OrbGSS publishes | **Principles table** — Principle · What it means · See it | The six existing `proof.*` commitments, one row each. Titles are kept; the meaning is trimmed to the 12-word cell budget. Each "See it" link points to where the site shows the principle. Evidence-backed screening · "Priorities come from mapped layers, not an unexplained model output." · `/#evidence`. Traceable provenance · "Every published visual maps back to a source and a recorded export." · `#sources`. Explicit data gaps · "A missing layer is published as missing, never invented." · `/solutions/geothermal/#gap`. AOI-first analysis · "One declared area, projection and grid before any interpretation." · `/solutions/geothermal/#glance`. Remote narrowing · "Large areas are ordered from orbit before field time is committed." · `/#priority`. Decision support · "Helps decide where to investigate; field investigation remains necessary." · no link. Below the table, existing `proof.foot`: "No accuracy, performance, deployment, customer or scale figures are published for this baseline." |
| A2 `#sources` | Data and imagery sources | **Sources table** — Source · Used for · Credit | Landsat 8 (USGS) · natural colour, thermal evidence, domain photographs · courtesy of the U.S. Geological Survey, public domain. NASADEM (NASA) · elevation and relief · NASA Earthdata. Copernicus Sentinel-2 · alteration evidence; hero ground detail · "Contains modified Copernicus Sentinel data (2025)". NASA Blue Marble · the rendered hero's Earth texture · NASA, public domain. Scientific colour maps v8.0 · map palettes · Fabio Crameri, MIT. Each row's wording follows `IMAGERY_RIGHTS.md` exactly; MER-240 copies it from there rather than from this table. |
| A3 | Next | — | "Partner with us →" to `/partner/`. |

Not on About: team names, biographies, address, legal entity, investors, timeline or traction (decision 9, R7). Domain status is not repeated here either: it lives on the hub (R1).

### 4.5 Partner with us (`/partner/`)

| # | Section | Lead visual | Copy |
| --- | --- | --- | --- |
| P0 | Header | — | Kicker "Partner with us" / "İş Birliği". Title (existing `contactPage.title`): "Let's talk about where to look next." Intro (existing `contactPage.intro`). |
| P1 | Which conversation | **Table** — Conversation · What it covers · Write | The existing `contactPage.*.copy`, trimmed to the 12-word cell budget. Pilot · "A geothermal pilot, or a first application in a new area." · "Write →" (`mailto:` with the existing pilot subject). Partnership · "A partnership or collaboration with OrbGSS." · "Write →" (partnership subject). Technical · "The evidence, its limits, or how a pilot would be scoped." · "Write →" (technical subject). The three links are rows of one table, not competing buttons. |
| P2 | Direct | **Address block** — `contact@orbgss.com` set large in the mono face | Label (existing `contactPage.direct.label`): "Direct". |

**Gate:** MER-240 does not ship until the CTO confirms `contact@orbgss.com` receives mail (`CONTACT_RELEASE_GATE`).

### 4.6 Not found (`404.html`)

New navigation; one line and a link home. Bilingual in MER-241.

## 5. No-repeat matrix

● is the fact's home. → is a link or thumbnail only. R6 marks a fixed text that travels with its visual.

| Fact or claim | Home | Solutions | Geothermal | About | Partner |
| --- | --- | --- | --- | --- | --- |
| Positioning line ("turns Earth observation … where to investigate next") | ● hero | | | | |
| Company sentence ("a geospatial-intelligence platform built by VirgaSoft …") | | | | ● | |
| Natural-colour view of Kızıldere | ● Act 2 | | → thumbnail | | |
| Terrain, thermal and alteration shown together | ● Act 3 | | → thumbnails | | |
| Priority result and its four-part definition | ● Act 4 | | → thumbnail; G3 is a different figure | | |
| Inspection wipe | ● | | | | |
| Pilot facts (area, grid, projection, sensors, dates) | captions (R6) | | ● G1/G2 | | |
| Second (iron) alteration signal | | | ● G4 | | |
| Priority over relief | | | ● G3 | | |
| Structure/geology gap | footnote → | | ● G6 | → (principles link) | |
| What the pilot produced | | | ● G5 | | |
| Domain status | labels (R6) | ● S1 | label (R6) | | |
| Domain one-line descriptions | | ● S1 | | | |
| Domain photographs | → cards | ● S2–S4 | | | |
| Illustrative-imagery footnote | R6 | R6 | | | |
| Six publishing principles + "no figures published" | | | | ● A1 | |
| Data and imagery sources | footer short form (R6) | | | ● A2 | |
| Conversation types and the address | → hero/closing line | | → G7 | → A3 | ● |
| Mandatory scientific warnings | R6 | | R6 | | |

## 6. Redirects and anchors

**301 redirects in `vercel.json` (MER-240):**

| From | To |
| --- | --- |
| `/platform/` | `/` |
| `/pilot/` | `/solutions/geothermal/` |
| `/company/` | `/about/` |
| `/contact/` | `/partner/` |

`trailingSlash: true` already normalises `/pilot` → `/pilot/` first. Fragments are never sent to the server, so the browser carries `#…` across a redirect unchanged. That is why the targets keep alias ids:

| Old link | Lands on |
| --- | --- |
| `/pilot/#pilot-observe` | `/solutions/geothermal/#pilot-observe` → G1 |
| `/pilot/#pilot-terrain`, `#pilot-evidence` | G2 |
| `/pilot/#pilot-priority`, `#pilot-geothermal` | G3 (on G2 until MER-242 delivers G3) |
| `/pilot/#pilot-structure` | G6 |
| `/solutions/#geothermal` | S2 (still on the hub) |
| `/solutions/#mineral`, `#environment` | S3, S4 (existing aliases, unchanged) |
| `/#company`, `/#proof` | Dropped: the homepage top. No known inbound use. |
| `/#contact` | The one-line Partner call |

The old routes had no `/tr/` versions, so no Turkish redirects are needed. Every new page goes into `.vercelignore` (MER-237's allowlist), or it will not deploy. The removed route directories leave the allowlist in the same change.

## 7. Visual needs

| Id | Visual | Source and rights | Owner | Blocks |
| --- | --- | --- | --- | --- |
| V1 | Locator map: Türkiye outline, Denizli, the 36 km AOI square | Natural Earth 1:10m Admin 0 (public domain), rendered to SVG by a local script; recorded in `sources.json` and `IMAGERY_RIGHTS.md` as class A, not product proof. Downloading the dataset needs CTO approval at the time. | MER-240 | G0 |
| V2 | Priority over shaded relief, in the MER-151 presentation family | Science: **MER-242** (D1, decided 2026-10-15). The WEB-002 `geothermal-*` composite is not used. | Science → MER-240 | G3 (absent until delivered) |
| V3 | Iron (ALT-02) alteration proxy, in the MER-151 presentation family | Science: **MER-242** (D1, decided 2026-10-15). The GEO-WEB-002 `alt02-*` export is not used. | Science → MER-240 | G4 (absent until delivered) |
| V4 | A coastal Marine context scene to replace the inland Ili Delta | USGS Landsat Collection 2, natural colour, public domain, through the existing imagery pipeline. Suggested: the Büyük Menderes delta and the Aegean coast near Söke, the same river that crosses the Kızıldere graben. Illustrative only, never a result. | MER-240 | S4 (Ili Delta is the fallback) |
| V5 | Layer-table thumbnails | Existing derivatives displayed at most 160 CSS px; no new files. | MER-240 | — |
| V6 | Per-page social previews | Existing placed images: the hero poster for Solutions, About and Partner; the Kızıldere priority for Geothermal (MER-237's rule requires a placed image). | MER-240 | — |

## 8. `CLAUDE.md` invariants that change (MER-239 applies them)

| Current text (abridged) | Proposed text |
| --- | --- |
| "Desktop navigation is right-aligned in exactly this order: Platform → Solutions (dropdown: Geothermal, Mining, Marine) → Pilot → Company → Contact → EN \| TR." | "Desktop navigation is right-aligned in exactly this order: Home → Solutions (dropdown: Geothermal, Mining, Marine) → About → Partner with us → EN \| TR. Geothermal links `/solutions/geothermal/`; Mining and Marine link `/solutions/#mining` and `/solutions/#marine`." |
| "The three homepage Solutions cards are native links to `/solutions/#geothermal`, `/solutions/#mining` and `/solutions/#marine` …" | "… native links to `/solutions/geothermal/`, `/solutions/#mining` and `/solutions/#marine`. A card shows the image, the domain name and its status label only." |
| "Supporting pilot-ledger, company/trust and contact sections follow and must stay visually subordinate." | "After the four acts come the inspection aid, the Solutions cards and one Partner line, all visually subordinate. Method and Company content lives on `/about/`." |
| "The dark technical beam grammar survives on the deep routes (`/platform/`, `/pilot/`, …)" | "The dark technical grammar survives on `/solutions/geothermal/`." |
| GEO-WEB-002 "(the accepted final master package, still bound by `/pilot/`)" | "… bound by `/solutions/geothermal/` where D1 uses it." |
| "The homepage is bilingual (English default, Turkish) via the lightweight client-side dictionary in `script.js`." | "The site is bilingual: English at `/`, Turkish as static pages under `/tr/`, generated from one dictionary by `scripts/build_tr_pages.py` (MER-241)." |
| (new) | A **Content rules** section stating R1–R8 of this document. |
| (unchanged, restated) | Taxonomy, aliases, the score label and warnings, the class-B ceilings, "no How it works", no icon wall or feature grid. Tables are show-first elements, not cards; Act 3 remains the single card-like composition besides the Solutions cards. |

The validator's `ROUTES` and `REQUIRED_FILES` follow the page set in section 2. MER-240 updates them together with the routes.

## 9. Decisions (D1–D2 decided, D3–D5 open)

| Id | Decision | Decided, or recommended | Alternative |
| --- | --- | --- | --- |
| D1 | The palette of G3 (priority over relief) and G4 (iron proxy) | **Decided 2026-10-15:** Science provides MER-151-family derivatives of both (**MER-242**). Until they exist, G3 and G4 are left out, and the G2 row says "Accepted, not shown yet". | (Not chosen: ship the WEB-002 / GEO-WEB-002 exports in the report palette, as the mockups show.) |
| D2 | Turkish URL slugs | **Decided 2026-10-15:** Turkish slugs, ASCII only — `/tr/`, `/tr/cozumler/`, `/tr/cozumler/jeotermal/`, `/tr/hakkimizda/`, `/tr/is-birligi/`. | (Not chosen: English slugs under `/tr/`.) |
| D3 | A privacy / KVKK notice page | A legal question for the company, not one this document can answer. Facts for that review: the site sets no cookies, has no forms, analytics or third-party scripts, and stores only the language choice in the visitor's own browser (`localStorage`). | — |
| D4 | `contact@orbgss.com` deliverability | The CTO confirms the mailbox receives external mail before MER-240 ships. | — |
| D5 | Marine imagery | Source a coastal scene (V4) during MER-240. | Keep the Ili Delta with its current illustrative footnote. |

## 10. Handoff

* **MER-239:** apply section 8 and rules R1–R8 to `CLAUDE.md` and the other authorities; record D1 and D2 as decided (2026-10-15) and D3–D5 as they are decided.
* **MER-240:**
  * build sections 2 and 4 in English;
  * add the section 6 redirects and alias ids;
  * source the section 7 visuals;
  * update `.vercelignore`, `ROUTES`, the sitemap and the per-route metadata;
  * enforce R1–R5 and R8 in the validator with a negative suite: word budgets, at most one full-size use per visual, a lead visual per section, no duplicate claim strings across routes, one status vocabulary.
* **MER-241:** generate `/tr/` from the same dictionary under the D2 scheme (Turkish slugs).
* **MER-242 (Science):** the G3 / G4 derivatives; MER-240 adds G3 and G4 when they are accepted.

## 11. Mockups

`docs/mockups/m6/` holds static mid-fidelity mockups built from the live `styles.css`, real assets and real copy. Each has a mockup banner, and the files exist for review only:

* `home.html` — the homepage with this document's changes applied;
* `solutions.html`, `geothermal.html`, `about.html`, `partner.html`;
* `mockup.css` — the few mockup-only rules (tables, locator placeholder, empty-gap frame) MER-240 will turn into real components.

To view them, serve the repository root (`py -3.14 -m http.server 8080`) and open `http://localhost:8080/docs/mockups/m6/solutions.html`. Desktop (1440 px) and mobile (390 px) screenshots of every mockup are in `evidence/mer238/`. The locator map (V1) is a labelled placeholder until MER-240 builds it from Natural Earth. G3 and G4 in the mockups show the interim report-palette exports, which D1 did not choose: the implementation leaves both out until MER-242 delivers.
