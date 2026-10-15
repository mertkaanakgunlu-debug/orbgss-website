# OrbGSS website — product and content authority

> **WEB-001 (2026-09-15):** `docs/WEB_VNEXT_AUTHORITY.md` is the vNext authority and wins where the two disagree. Sections below marked *(WEB-001)* reflect the current homepage.

> **MER-239 (2026-10-15):** the public taxonomy is Geothermal / Mining / Marine (WEB-005C). The *(WEB-001)* navigation and copy sections below are history: current copy is canonical in `script.js`, and the Milestone 6 pages, navigation and content rules are in `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md`. Brand hierarchy, website job, positioning and the claims to avoid remain in force.

## Brand hierarchy

**OrbGSS** is the product/brand presented to website visitors.  
Expanded name: **Orbital Geo-Spatial Solutions**.  
**VirgaSoft** is the parent/company identity and should remain secondary (`Built by VirgaSoft` is appropriate).

## Website job

The landing page should allow an investor, technical partner or potential customer to understand within roughly a minute that OrbGSS converts Earth-observation and geoscience inputs into decision-oriented geospatial intelligence.

It is not currently intended to be a signup-heavy SaaS marketing site.

## Positioning

Do not position OrbGSS as a geothermal-only company. The first pilot is geothermal, while the platform direction is broader GIS/geospatial intelligence.

Current public-facing solution taxonomy:

1. **Geothermal** — first active application (the Kızıldere pilot)
2. **Mining** — expansion direction
3. **Marine** — expansion direction

The site should make the platform feel extensible without implying that every future vertical is already production-ready.

### Navigation labels *(WEB-001 — history; superseded by WEB-005C and Milestone 6)*

| Nav label (EN / TR) | Destination |
| --- | --- |
| Platform / Platform | `#platform` (01 Observe, start of the story) |
| Solutions / Çözümler → Geothermal Exploration / Jeotermal Arama | `#geothermal` (06, first active application) |
| Solutions → Mineral Exploration / Maden Arama | `#mineral` (pilot ledger row, expansion direction) |
| Solutions → Environmental & Land Intelligence / Çevre ve Arazi Zekâsı | `#environment` (pilot ledger row, expansion direction) |
| Pilot / Pilot | `#pilot` (application maturity ledger) |
| Company / Şirket | `#company` (company + how we work) |
| Contact / İletişim | `#contact` (contact beam) |

The former Marine placeholder and the footer `#about` anchor were removed; no navigation item points to a placeholder.

### Turkish copy

Turkish translations of the hero, beams, labels and footer are canonical in `script.js` (`I18N.tr`). Treat changes to them as content decisions, like the English copy.

## Current hero copy *(WEB-001)*

Eyebrow:

> Earth data. Evidence. Priority.

Headline:

> Know where to look next.

Supporting copy:

> OrbGSS turns Earth observation and geoscience data into evidence-backed spatial priorities that help teams decide where to investigate next.

Primary CTA: `Explore the Platform` (→ `#platform`). Secondary: `Partner With Us` (mailto).

This copy may be refined later, but substantial messaging changes should be treated as content decisions rather than incidental code cleanup.

## Current beam copy *(WEB-001)*

Each story beam: index, title, statement, monospace descriptor. Canonical EN/TR text is in `script.js` (`story.*`, `pilot.*`, `app.*`, `company.*`, `trust.*`, `contact.*`).

- `01 Observe` — the platform starts from an area of interest; inputs are brought into one spatial frame
- `02 Terrain` — terrain is physical context
- `03 Evidence` — domain-relevant signals are mapped as spatial evidence
- `04 Structure` — geological/structural context frames interpretation
- `05 Priority` — evidence is integrated into a spatial priority view
- `06 Geothermal` — first active application, applied in a pilot setting

Pilot ledger statuses: Geothermal `Active · First application`; Mineral and Environmental & Land `Expansion direction`. Trust list: traceable provenance, explicit data gaps, evidence-based outputs, decision support (field investigation remains necessary).

## Claims to avoid unless later substantiated

Do not invent or publish:

- customer counts
- revenue or traction figures
- false alpha/beta claims
- false production deployments
- exploration accuracy percentages
- ROI claims
- named enterprise partners without permission
- AI model performance claims
- unsupported statements that OrbGSS replaces field exploration

## Contact

`contact@orbgss.com` is the only public contact address. Its ownership and deliverability are not evidenced in this repository (`CONTACT_RELEASE_GATE`, now MER-238 D4, a ship gate for MER-240).
