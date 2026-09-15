# WEB-002 — Evidence-to-Intelligence Product Proof & Geothermal Pilot Experience

**Linear:** MER-90  
**Authority:** CURRENT — OrbGSS Website vNext Product & Execution Authority v1.3.  
**Canonical repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Reference/upstream only:** `baran-orbgss/website`  
**Accepted baseline:** `main` at `677bfa7672ac18c2c808ddaaf235ff12863de443` (accepted WEB-001).  
**Branch:** `feat/web-002-product-proof`.  
**Product state:** READY_FOR_CTO_APPROVAL. Publication of this file does **not** start implementation.

## Outcome

Turn the accepted WEB-001 gallery shell into a credible OrbGSS product demonstration. A first-time visitor should be able to understand, through the existing cinematic gallery rhythm, how OrbGSS moves from an area of interest and source data to interpretable evidence and finally to an integrated spatial-priority output, with geothermal presented as the active first application.

The presentation grammar remains:

> **Gallery is the presentation grammar. Evidence-to-intelligence is the story.**

WEB-002 replaces temporary atmospheric gallery panels with truthful product-proof visuals where public-safe canonical outputs exist. It does not redesign the information architecture and does not create the cinematic Earth/satellite hero.

## Required homepage proof sequence

Preserve the accepted WEB-001 structure and progressively replace the existing `data-visual-status="temporary-gallery"` slots:

1. `observe` — AOI / source-observation context that truthfully establishes where analysis begins.
2. `terrain` — approved terrain / DEM-derived visual context.
3. `evidence` — approved domain-relevant EO evidence visual, such as thermal or alteration evidence, only when canonical/public-safe semantics are available.
4. `structure` — approved geological / structural context, such as faults or lithology, only when canonical/public-safe semantics are available.
5. `priority` — approved integrated spatial-priority / prospectivity output.
6. `geothermal` — geothermal first-application proof tying the preceding evidence sequence to the pilot/product context.

The exact scientific layer names shown publicly must match canonical Science/Product authority and the actual assets used. Do not force a layer into the page merely to satisfy the above examples if its public-safe canonical output is not available.

## Scientific boundary

Product/website work may present accepted scientific outputs but may not redefine them.

Do **not** change or invent:
- CRS, grid, units, NoData/mask behavior;
- resampling or categorical/QA semantics;
- constants or feature eligibility;
- validation meaning;
- uncertainty semantics;
- score interpretation;
- geothermal methodology;
- layer weights or thresholds.

If the implementation requires a scientific decision that is not already present in canonical Science authority, stop and route an exact decision request to **Science & Geospatial**.

## Public-safe asset rule

Every product-proof visual must satisfy one of these conditions:

1. it is an accepted public-safe OrbGSS output with a traceable canonical source pointer; or
2. it is an explicitly labelled design mockup that cannot reasonably be interpreted as measured/validated evidence.

For the core `terrain`, `evidence`, `structure`, `priority`, and geothermal proof states, prefer real accepted outputs. A mockup must never silently stand in for a real result.

If required proof assets are absent at implementation start and cannot be resolved from accepted canonical sources without inventing science, stop with:

`WAITING_DOMAIN_DECISION — Science & Geospatial public-safe asset/pointer required`

and report the exact missing slot(s) and canonical pointer needed.

## Scope

- Replace the temporary gallery story panels with product-proof visuals as canonical/public-safe assets become available.
- Preserve the dark technical beam → full-width visual rhythm.
- Keep the existing section order and navigation accepted in WEB-001.
- Add concise technical metadata/captions that explain what each proof visual represents without turning the page into a dashboard.
- Make the AOI → inputs → evidence → structure → priority relationship understandable without a long technical document.
- Present geothermal as the first active application and make its maturity truthful.
- Keep Mineral Exploration and Environmental & Land Intelligence visually/verbally subordinate as expansion directions.
- Update `assets/imagery/sources.json` or the accepted asset/provenance manifest for every new public visual.
- Preserve EN/TR parity for all new visible copy and alt text.
- Optimize new raster/image derivatives for web delivery while preserving truthful interpretation.
- Update the repository validator only where needed to enforce the accepted product-proof contract.

## Product-proof visual behavior

The site may use restrained interactions when they improve comprehension, for example:
- a before/after reveal between source context and processed output;
- a controlled layer-state switch;
- subtle fade/opacity transitions as proof states enter the viewport.

These interactions must remain optional, accessible, mobile-safe and non-essential to understanding. No scroll-jacking, fake GIS controls, decorative HUD chrome, or dense dashboard UI.

## Copy and claim rules

Allowed direction:
- traceable provenance;
- evidence-backed spatial prioritization;
- explicit data gaps;
- decision support;
- field investigation remains necessary;
- geothermal is the active first application.

Not allowed without separate accepted authority:
- accuracy percentages;
- ROI claims;
- customer/partner logos or named enterprise endorsements;
- production-readiness claims for expansion verticals;
- AI/model-performance claims;
- claims that OrbGSS replaces field exploration;
- validation claims inferred from visual appearance alone.

## Out of scope

- Any new scientific method or analysis pipeline.
- Recomputing or changing canonical score semantics.
- Cinematic Earth/satellite hero production or WebM/MP4 hero integration (WEB-005).
- Site-depth / multi-page expansion beyond bounded proof-content needs (WEB-003).
- Vercel production cutover or Squarespace DNS changes (WEB-006).
- New frontend framework or backend.
- Analytics/tracking, auth, billing, CRM.

## Acceptance

WEB-002 is complete only if:

1. The WEB-001 gallery identity remains intact.
2. The homepage now communicates a coherent evidence-to-priority workflow using real public-safe proof visuals wherever required canonical outputs exist.
3. No temporary atmospheric image is labelled or visually presented as a DEM, alteration/thermal result, fault/geology layer, or score output when it is not one.
4. Every new scientific/product visual has explicit provenance or explicit mockup status.
5. The priority/prospectivity state is clearly presented as an integrated spatial-priority output, with wording consistent with canonical Science/Product semantics.
6. Geothermal is clearly the active first application; expansion directions remain subordinate.
7. No unsupported accuracy, ROI, customer, partner, validation, or AI-performance claim appears.
8. New visible copy and alt text have EN/TR parity.
9. New imagery is responsive and optimized for representative mobile/tablet/desktop widths.
10. Keyboard/focus/accessibility behavior from WEB-001 remains intact.
11. Existing provenance records remain valid and new asset records are added.
12. Repository validation passes with zero unexplained warnings.
13. No cinematic hero work has begun.

## Verification / evidence

At minimum provide:
- exact branch and final implementation HEAD;
- changed-path list;
- validator output (`py -3.14 scripts/validate_site.py` on the current workstation when applicable);
- provenance/source pointer for every new public product visual;
- screenshots or preview evidence for desktop, tablet and narrow mobile;
- explicit mapping of `observe`, `terrain`, `evidence`, `structure`, `priority`, `geothermal` to their final asset and public label;
- list of any slot intentionally left non-proof/temporary and the exact reason;
- confirmation that WEB-005 hero media was not started.

## STOP / route conditions

Stop and report rather than inventing a solution if:

- a required product-proof asset lacks an accepted public-safe source/provenance pointer;
- scientific meaning is ambiguous or conflicts with canonical Science authority;
- completing the page would require inventing validation semantics, score interpretation, uncertainty, or product maturity;
- a new dependency/framework is genuinely required;
- a desired interaction changes accepted information architecture or UX policy;
- rights/licensing for a required asset are unclear;
- implementation would require publishing paid/closed/restricted data;
- destructive Git history changes would be required.

Routine HTML/CSS/JS bugs, image optimization, responsive fixes, accessibility defects, bounded validator changes and conformant visual polish are implementation-owned and must not trigger Product re-entry.

## Branch and publication policy

- No feature work on `main`.
- Continue implementation on `feat/web-002-product-proof` only after explicit CTO start approval.
- The task publication commit is authority-only; publication itself does not start implementation.
- Normal bounded implementation commits are allowed; do not impose artificial micro-step commit budgets.
- Do not begin WEB-003.
- Terminal implementation state: `REVIEW_READY`.