# OrbGSS website vNext — repository-local authority

**Source of truth:** CURRENT — OrbGSS Website vNext Product & Execution Authority v1.4 (product-owned).  
**Canonical repository:** `mertkaanakgunlu-debug/orbgss-website`.  
**Reference/upstream only:** `baran-orbgss/website`.  
**Accepted WEB-001 head:** `677bfa7672ac18c2c808ddaaf235ff12863de443`.  
**Current tracking:** Linear MER-90 — WEB-002 — Evidence-to-Intelligence Product Proof & Geothermal Pilot Experience.  
**Status:** WEB-001 accepted; independent repository migration complete; WEB-002 was deliberately started, correctly stopped before feature code for the Science/public-safe asset dependency, and is now `IN_PROGRESS — EXECUTION_CONTINUATION_READY`. MER-96 / GEO-WEB-001 is resolved. Canonical package: `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`; exact resumed contract: `tasks/WEB-002_PRODUCT_PROOF.md`. Where this document and older `docs/DESIGN_AUTHORITY.md` / `docs/PRODUCT_AND_CONTENT_AUTHORITY.md` disagree, this document wins for vNext work; older documents remain valid for everything they cover that is not restated here (imagery rules, palette, on-image labels, logo, claim discipline).

## 1. Brand hierarchy

- **OrbGSS** (Orbital Geo-Spatial Solutions) is the primary public brand.
- **VirgaSoft** is the secondary parent attribution only ("Built by VirgaSoft"). It never leads.

## 2. Positioning

OrbGSS is a geospatial-intelligence platform. It turns Earth observation and geoscience data into evidence-backed spatial priorities that help teams decide where to investigate next.

Application maturity is explicit and must stay visible in copy:

| Application | Public status |
| --- | --- |
| Geothermal Exploration | active first application / pilot |
| Mineral Exploration | expansion direction |
| Environmental & Land Intelligence | expansion direction |

Never imply that expansion directions are production-ready. Never position OrbGSS as geothermal-only.

## 3. Presentation grammar: the gallery

The existing large-image gallery rhythm is a brand asset and survives vNext:

```text
HERO (image-led, overlay copy allowed)
DARK TECHNICAL BEAM → LARGE FULL-WIDTH VISUAL PANEL
DARK TECHNICAL BEAM → LARGE FULL-WIDTH VISUAL PANEL
…
TRUST / COMPANY / CONTACT
FOOTER
```

Canonical principle: **"Gallery is the presentation grammar. Evidence-to-intelligence is the story."**

Preserve: near-black / deep navy ground, soft-white type, restrained cyan accent, full-width cinematic imagery, dark separator beams, technical/editorial tone, coordinate/metadata language, wide desktop composition, restrained interaction. A secondary monospace treatment is allowed for coordinates, evidence labels, metadata and technical descriptors.

Prohibited: SaaS card grids, icon walls, dense feature tables, fake GIS dashboards, sci-fi HUD chrome, neon-heavy startup visuals, `How it works` sections, decorative pins/globes, scroll-jacking.

## 4. Narrative: evidence to intelligence

Homepage story order:

1. Hero
2. 01 — Platform / Observe
3. 02 — Terrain
4. 03 — Evidence
5. 04 — Structure
6. 05 — Priority
7. 06 — Geothermal (first active application)
8. Trust / Company / Contact
9. Footer

Each numbered story section keeps the beam → visual rhythm. The story is what the sequence communicates; the gallery is how it is shown.

## 5. WEB-002 Science alignment

Accepted Science authority already defines the active MVP score. Website work must present that authority, not reinvent it.

- Active profile: `mvp_remote_sensing_priority_v1`.
- Public meaning: **Remote-Sensing Relative Priority — Experimental Baseline**.
- It is a deterministic 0–100 within-AOI screening/ranking surface.
- It is **not** probability, Full Prospectivity, reserve estimate, discovery likelihood, drilling-success likelihood, or a calibrated cross-AOI score.
- Mandatory numeric evidence is the accepted remote-sensing core: THM-01 thermal plus ALT-01/ALT-02 broad spectral alteration proxies under ADR-0033.
- Sentinel alteration must never be described as mineral/kaolinite identification or proof of hydrothermal alteration.
- NASADEM elevation/slope/hillshade are context/display layers only; no universal geothermal-favourability direction is assigned.
- Structural/geological evidence is optional support and score-invariant. For WEB-002, the accepted public package returns Structure and Geology as explicit `DATA_GAP / optional support / score-invariant` states rather than authorizing public fault/lithology masters.

Canonical Science pointers are ADR-0033, GEO-037 / MER-32, GEO-039 / MER-40 and GEO-042 / MER-50. Exact WEB-002 presentation and asset requirements are governed by `tasks/WEB-002_PRODUCT_PROOF.md` and `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`.

The public-safe package authorizes derived website masters for Observe/AOI, NASADEM Terrain, THM-01, ALT-01, ALT-02, the accepted `mvp_remote_sensing_priority_v1` output, and Kızıldere first-application proof through the already-accepted GEO-039 Workbench PNG export path. Generated file SHA-256 values come from each materialized `export_manifest.json`; they must not be invented or copied from unrelated evidence.

## 6. Scientific and public-claim boundaries

- Do not fabricate DEM, thermal, alteration, geological, fault or score outputs. Temporary atmospheric imagery must never be labelled as one of those.
- Real evidence / product-proof visuals are owned by WEB-002 and require exact accepted/public-safe source pointers, provenance/rights and truthful labels.
- Scientific meaning remains owned by canonical Science authority. Product presentation must not redefine CRS/grid/units/NoData/mask, resampling, feature eligibility, validation semantics, uncertainty, score interpretation, weights or thresholds.
- Do not publish paid/closed/restricted MTA data without separate explicit authority.
- Never publish unsupported customer counts, enterprise partners, revenue, ROI, exploration accuracy, AI/model-performance claims, false production deployments, validation/discovery/reserve/drilling-success claims, or claims that OrbGSS replaces field investigation.
- Trust language is restrained and truthful: traceable provenance, explicit data gaps, evidence-based outputs, decision support, field investigation remains necessary.
- Imagery provenance rules in `IMAGERY_RIGHTS.md` and `assets/imagery/sources.json` remain mandatory.

## 7. Language

EN is the default, TR is the second language, both served from the `I18N` dictionary in `script.js`. A visible string is not done until both languages exist. Turkish is professional, natural Turkish, not literal translation.

## 8. Navigation (vNext)

Desktop, right-aligned, in this order:

`Platform` → `Solutions ⌄` → `Pilot` → `Company` → `Contact` → `|` → `EN | TR`

- Solutions is an accessible disclosure listing Geothermal Exploration, Mineral Exploration, Environmental & Land Intelligence.
- Every visible destination resolves to a real section anchor. No placeholder links to unrelated sections.
- Keyboard/disclosure behaviour (focus states, Escape, arrow keys, mobile tap expansion) is preserved.

This supersedes the `Home → Solutions → About → Partner With Us` order recorded in `docs/DESIGN_AUTHORITY.md` and `CLAUDE.md`.

## 9. Execution rules

- **No feature work on `main`.** All vNext work lands on feature branches and is reviewed before merge/acceptance.
- Static HTML + CSS + vanilla JavaScript remains the architecture. A framework or dependency change requires Product approval.
- No analytics, auth, CRM, backend, billing or production deployment inside website tasks unless a task says so.
- Each task publishes its contract under `tasks/` before implementation code is written.
- Publication alone never starts a new WEB task; each new task requires deliberate CTO start approval.
- WEB-002 already received start approval. The MER-96 Science dependency is resolved; implementation resumes on the same branch without a second CTO start gate.
- After this Product reconciliation, routine implementation, export materialization, provenance recording, visual polish, tests and bounded fixes remain E&D/implementer-owned until `REVIEW_READY`, unless a genuine new Product/Science/high-risk decision is required.

## 10. Task sequence

```text
WEB-001 → WEB-002 → WEB-003 → WEB-004 → WEB-005 → WEB-006
```

- **WEB-001** — information architecture, visual foundation, homepage shell — **ACCEPTED / COMPLETE** at `677bfa7672ac18c2c808ddaaf235ff12863de443`.
- **WEB-002** — real evidence / product-proof imagery and geothermal proof experience — exact contract: `tasks/WEB-002_PRODUCT_PROOF.md`; **IN_PROGRESS / EXECUTION_CONTINUATION_READY** after MER-96 resolution.
- **WEB-003, WEB-004** — blocked behind WEB-002 under the published dependency chain.
- **WEB-005** — cinematic Earth/satellite hero (motion, WebM/MP4). Deferred; the current hero remains a static poster designed to be replaced without changing surrounding architecture.
- **WEB-006** — production DNS cutover (`orbgss.com` via Squarespace → Vercel). Deferred; no DNS or production-domain change before then. Google Workspace MX/SPF/DKIM/DMARC are never touched by ordinary website work.