# OrbGSS website vNext — repository-local authority

**Source of truth:** CURRENT — OrbGSS Website vNext Product & Execution Authority v1.8 (product-owned).  
**Canonical repository:** `mertkaanakgunlu-debug/orbgss-website`.  
**Reference/upstream only:** `baran-orbgss/website`.  
**Accepted WEB-001 head:** `677bfa7672ac18c2c808ddaaf235ff12863de443`.  
**Accepted WEB-002 implementation head:** `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`.  
**Accepted WEB-003 implementation head:** `3670d43bece4ffba657a3d9645cbea20c7e698bf`.  
**Current tracking:** Linear MER-90 — WEB-002 accepted/complete; MER-91 — WEB-003 accepted/complete; MER-92 — WEB-004 next / not started.  
**Status:** WEB-001, WEB-002 and WEB-003 are accepted/complete. WEB-003 reached `REVIEW_READY`, completed one bounded conformant Product review revision, and was terminally accepted at `3670d43bece4ffba657a3d9645cbea20c7e698bf`; no Product/Science semantic change was required. Exact WEB-002 contract: `tasks/WEB-002_PRODUCT_PROOF.md`; exact WEB-003 contract: `tasks/WEB-003_PUBLIC_SITE_DEPTH.md`. Website implementation in this workstream proceeds directly through Claude Code Desktop under Product authority; E&D is reserved for the post-Control-Plane semi-automated/headless Claude execution flow. Where this document and older `docs/DESIGN_AUTHORITY.md` / `docs/PRODUCT_AND_CONTENT_AUTHORITY.md` disagree, this document wins for vNext work; older documents remain valid for non-superseded imagery, palette, on-image label, logo and claim-discipline rules.

## 1. Brand hierarchy

- **OrbGSS** (Orbital Geo-Spatial Solutions) is the primary public brand.
- **VirgaSoft** is secondary parent attribution only (`Built by VirgaSoft`). It never leads.

## 2. Positioning

OrbGSS is a geospatial-intelligence platform. It turns Earth observation and geoscience data into evidence-backed spatial priorities that help teams decide where to investigate next.

Application maturity is explicit:

| Application | Public status |
| --- | --- |
| Geothermal Exploration | active first application / pilot |
| Mineral Exploration | expansion direction |
| Environmental & Land Intelligence | expansion direction |

Never imply expansion directions are production-ready. Never position OrbGSS as geothermal-only.

## 3. Presentation grammar

Canonical principle: **“Gallery is the presentation grammar. Evidence-to-intelligence is the story.”**

Preserve the near-black/deep-navy ground, soft-white type, restrained cyan accent, large EO/product visuals, technical/editorial tone, coordinate/metadata language, wide desktop composition and restrained interaction.

Prohibited unless later explicitly superseded by Product authority: generic SaaS card walls, icon walls, fake GIS dashboards, sci-fi HUD chrome, neon overload, stock imagery, scroll-jacking and invented scientific outputs.

## 4. Accepted public site structure

Canonical public routes after WEB-003:

- `/` — accepted evidence-to-intelligence homepage;
- `/platform/` — public workflow and decision-support framing;
- `/solutions/` — application portfolio and maturity;
- `/pilot/` — Kızıldere first-application proof;
- `/company/` — OrbGSS/VirgaSoft company context;
- `/contact/` — restrained mailto-based contact/partnership path.

Navigation order remains:

`Platform` → `Solutions ⌄` → `Pilot` → `Company` → `Contact` → `EN | TR`

Solutions remains an accessible disclosure for Geothermal Exploration, Mineral Exploration and Environmental & Land Intelligence. All routes/links are real; no placeholder navigation.

## 5. Science alignment

Accepted Science authority defines the active MVP score; website work presents it and does not reinvent it.

- Active profile: `mvp_remote_sensing_priority_v1`.
- Public meaning: **Remote-Sensing Relative Priority — Experimental Baseline**.
- Deterministic 0–100 within-AOI screening/ranking surface.
- Not probability, Full Prospectivity, reserve/resource estimation, discovery likelihood, drilling-success likelihood or calibrated cross-AOI score.
- Numeric evidence core: THM-01 thermal + ALT-01/ALT-02 broad spectral alteration proxies under accepted Science authority.
- Sentinel alteration is never mineral/kaolinite identification or proof of hydrothermal alteration.
- NASADEM terrain is context/display, not a scored geothermal-favourability predictor.
- Structural/geological evidence is optional support and score-invariant; the current public Kızıldere proof exposes structure/geology as an explicit data gap.

Canonical Science pointers remain ADR-0033, GEO-037 / MER-32, GEO-039 / MER-40 and GEO-042 / MER-50. Public-safe WEB-002 asset authority remains `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`.

## 6. Scientific/public-claim boundaries

- Do not fabricate DEM, thermal, alteration, geology, fault or score outputs.
- Scientific visuals require accepted/public-safe source pointers, provenance/rights and truthful labels.
- Product presentation must not redefine CRS/grid/units/NoData/mask, resampling, feature eligibility, validation semantics, uncertainty, score interpretation, weights or thresholds.
- No paid/closed/restricted MTA data without separate explicit authority.
- No unsupported customer/partner counts, revenue, traction, ROI, accuracy, AI-performance, production deployment, field validation, discovery, reserve/resource or drilling-success claims.
- OrbGSS remains decision support; field investigation remains necessary.
- `IMAGERY_RIGHTS.md` and `assets/imagery/sources.json` provenance rules remain mandatory.

## 7. Language and accessibility

EN is default; TR is second language through the shared `I18N` dictionary in `script.js`. Visible copy and human-readable accessibility text are not complete until both languages exist. Language choice persists across canonical routes. Keyboard/focus behavior, disclosure semantics and mobile usability are mandatory.

The WEB-003 validator additionally enforces that human-readable `aria-label` values on canonical routes are bound to `data-i18n-aria-label` and that all referenced i18n keys resolve in both languages.

## 8. Accepted WEB-003 result

WEB-003 added real static destinations for Platform, Solutions, Pilot, Company and Contact; route-specific canonical/OG metadata; sitemap coverage; cross-route language persistence; site-wide internal-link/fragment validation; and reuse of accepted WEB-002 Kızıldere proof assets on `/pilot/`.

The Product review revision closed three bounded findings before acceptance:

1. localized the two accessibility labels that had escaped the i18n system and added validator enforcement;
2. replaced the location-mismatched Crater Lake `/pilot/` Open Graph preview with the accepted/self-hosted Kızıldere `assets/proof/geothermal-1400.webp` derivative;
3. reconciled repository authority/status pointers.

Accepted WEB-003 implementation HEAD: `3670d43bece4ffba657a3d9645cbea20c7e698bf`.

## 9. Execution rules

- **No feature work on `main`.** Product acceptance/publication updates may advance `main` non-destructively after terminal review.
- Static HTML + CSS + vanilla JavaScript remains the architecture. Framework/dependency changes require Product approval.
- No analytics, auth, CRM, backend, billing or production DNS inside ordinary website tasks unless the exact task says so.
- Each WEB task publishes its exact contract under `tasks/` before implementation.
- Publication alone never starts implementation; each new WEB task requires deliberate CTO start approval.
- The current website workstream executes directly through **Claude Code Desktop**. Product publishes authority; CTO dispatches the short task prompt; Claude Desktop owns routine implementation, tests, evidence and bounded conformant revision through `REVIEW_READY`.
- **Execution & Delivery is not the dispatch/revision bridge for this website workstream.** E&D remains reserved for post-Control-Plane semi-automated/headless Claude Code execution.
- Product re-enters only for genuine Product/Science/high-risk semantic decisions, scope/architecture/UX-policy/dependency/security changes or exact task STOP conditions.

## 10. Task sequence

```text
WEB-001 → WEB-002 → WEB-003 → WEB-004 → WEB-005 → WEB-006
```

- **WEB-001** — foundation/homepage shell — **ACCEPTED / COMPLETE** at `677bfa7672ac18c2c808ddaaf235ff12863de443`.
- **WEB-002** — product-proof/geothermal proof — **ACCEPTED / COMPLETE** at implementation HEAD `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`.
- **WEB-003** — public-site depth/credibility/conversion/bilingual content — **ACCEPTED / COMPLETE** at implementation HEAD `3670d43bece4ffba657a3d9645cbea20c7e698bf`.
- **WEB-004** — responsive, accessibility, performance and hosted preview acceptance — next; exact task publication may proceed under Product ownership, but implementation requires deliberate CTO approval.
- **WEB-005** — final cinematic hero integration/release candidate — deferred behind WEB-004 and deliberate CTO approval.
- **WEB-006** — production domain cutover (`orbgss.com` via Squarespace → Vercel) — deferred; explicit CTO human gate required for DNS writes.

## 11. Later public-visual authority

The later R7 public visual/palette decision remains valid: final public-facing outputs may be restyled/recomposed only when scientific meaning and Science invariants remain unchanged. Its intended downstream public narrative is cinematic hero → one high-quality real AOI/EO image → compact evidence presentation → large final priority/result map, with structural evidence shown only when genuinely public-safe. WEB-004 is a hardening/acceptance task and must not silently redesign the accepted WEB-003 site to implement that later narrative. Final hero/public-layout integration belongs downstream authority.
