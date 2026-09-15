# WEB-003 — Public-Site Depth, Credibility, Conversion & Bilingual Content

**Linear:** MER-91  
**Authority:** CURRENT — OrbGSS Website vNext Product & Execution Authority v1.7 + this exact task.  
**Canonical repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Reference/upstream only:** `baran-orbgss/website`  
**Accepted baseline:** `main@79484bb7d11c3b26373649c802fb4db7d2bd445f` (WEB-002 accepted/published; accepted implementation head `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`).  
**Branch:** `feat/web-003-public-site-depth`  
**Product state:** `READY_FOR_CTO_APPROVAL — NOT STARTED`

## Outcome

Turn the accepted WEB-002 homepage into a credible small public product site, without diluting the cinematic gallery identity or overstating product maturity.

A prospective customer, technical reviewer, partner, or investor should be able to move from the homepage into meaningful Platform, Solutions, Pilot, Company, and Contact destinations and understand:

- what OrbGSS does;
- how the accepted evidence-to-priority workflow is framed;
- what is active today versus an expansion direction;
- what the Kızıldere first application proves and does not prove;
- how provenance/data gaps/scientific boundaries are handled;
- what the next legitimate contact action is.

The site remains a restrained public product/company experience, not a signup SaaS application and not a technical manual.

## Public information architecture

The canonical public route model for WEB-003 is:

- `/` — homepage / accepted evidence-to-intelligence gallery;
- `/platform/` — platform workflow, provenance and decision-support framing;
- `/solutions/` — application portfolio and maturity, with Geothermal active first and Mineral + Environmental/Land as expansion directions;
- `/pilot/` — Kızıldere first-application proof, evidence families, output meaning, data gaps and scientific/public-claim boundaries;
- `/company/` — OrbGSS identity, VirgaSoft parent attribution, operating principles and credibility context;
- `/contact/` — restrained contact/partnership path using the accepted public contact target, with no backend or personal-data capture.

Use the existing static HTML/CSS/vanilla-JS architecture. The exact static-directory/template/refactor strategy is implementer-owned, but these public URLs and semantics are Product behavior.

The homepage navigation must route to these destinations. The Solutions disclosure may link to relevant sections within `/solutions/` for Geothermal, Mineral and Environmental & Land Intelligence.

## Product/content invariants

Preserve the accepted WEB-001/WEB-002 design and content authority:

- **OrbGSS** is the primary public brand; **VirgaSoft** is secondary parent attribution (`Built by VirgaSoft`).
- Geothermal Exploration = **active first application / pilot**.
- Mineral Exploration = **expansion direction**.
- Environmental & Land Intelligence = **expansion direction**.
- Do not imply expansion directions are production-ready.
- OrbGSS is decision support and field-investigation prioritization; it does not replace field work.
- The accepted score remains **Remote-Sensing Relative Priority — Experimental Baseline** under `mvp_remote_sensing_priority_v1`.
- Do not call the score probability, Full Prospectivity, reserve/resource estimation, discovery likelihood, drilling-success likelihood, or a cross-AOI calibrated metric.
- THM-01 and ALT-01/ALT-02 retain their accepted warning semantics.
- Structure/Geology remain explicit optional-support/data-gap states for the current public Kızıldere proof unless separately authorized.
- No paid/closed/restricted MTA material.
- No unsupported customer, partner, traction, revenue, ROI, accuracy, AI-performance, deployment, discovery, reserve or drilling-success claims.

The scientific visuals and provenance accepted in WEB-002 may be reused, but their meaning, rendering, warnings, checksums and rights boundary must not be altered.

## Visual/UX direction

WEB-003 adds depth without replacing the accepted presentation grammar.

Preserve:

- near-black / deep-navy base;
- soft-white type and restrained cyan accent;
- wide editorial/geospatial composition;
- large approved imagery where it advances understanding;
- dark technical beams / restrained monospace metadata;
- sparse, confident copy;
- existing navigation interaction language;
- EN/TR language switching and keyboard/focus behavior.

Do not introduce:

- generic SaaS card walls;
- icon-heavy feature grids;
- fake GIS controls or dashboard screenshots that imply non-existent behavior;
- HUD/neon overload;
- stock imagery;
- decorative motion that competes with the later WEB-005 hero;
- long methodology dumps on public pages.

Deeper pages may use editorial text/image layouts rather than repeating the homepage beam pattern mechanically. They must still feel like the same OrbGSS system.

## Route content requirements

### `/platform/`

Explain the accepted product workflow at a public-product level:

`AOI → source/context → evidence → explicit data gaps → integrated spatial priority → investigation decision support`

Required concepts:

- source/provenance traceability;
- evidence families and explicit missing-data handling;
- within-AOI priority meaning;
- field investigation remains necessary;
- no implication that every optional evidence family is always available.

Do not reproduce internal implementation or Control Plane details.

### `/solutions/`

Present the application portfolio with visually explicit maturity:

1. Geothermal Exploration — active first application;
2. Mineral Exploration — expansion direction;
3. Environmental & Land Intelligence — expansion direction.

The page may explain how the same evidence-to-priority operating pattern can extend across domains, but must not claim completed scientific methods, validated products or production readiness for the expansion directions.

### `/pilot/`

Use Kızıldere as the concrete first-application proof. Reuse accepted WEB-002 imagery/provenance where useful.

The page must make these distinctions understandable without a technical paper:

- AOI/project context;
- NASADEM terrain as context/display only;
- THM-01 + ALT-01/ALT-02 as the accepted remote-sensing evidence core;
- Structure/Geology public data gap / optional support;
- `mvp_remote_sensing_priority_v1` as AOI-relative experimental screening;
- first-application proof is not field validation/discovery/reserve/drilling-success proof.

Do not introduce new scientific interpretation.

### `/company/`

Provide an actual company/about destination rather than treating the footer as the entire company presence.

Required framing:

- OrbGSS — Orbital Geo-Spatial Solutions;
- built by VirgaSoft;
- geospatial-intelligence / GIS product direction;
- operating principles: traceable provenance, explicit data gaps, evidence-backed outputs, decision support;
- restrained statement of expansion potential without unsupported commercial claims.

Do not publish personal biographies, team member names, investment terms, financials or unapproved partner/customer claims under this task.

### `/contact/`

Provide a credible, minimal public contact/partnership destination.

- Use the accepted public contact target already present in the site (`contact@orbgss.com`) unless canonical Product authority changes it.
- Primary actions may cover pilot, partnership and technical conversations.
- No form backend, CRM, analytics, lead scoring, authentication or user account system.
- Do not collect/store PII inside this task.
- Mailto-based contact is acceptable.

Mailbox ownership/release verification remains a later launch gate; WEB-003 must not perform external account/admin actions.

## Bilingual content

EN remains default; TR is the second language.

All public routes must provide complete EN/TR visible-copy parity, including:

- page titles and descriptions;
- headings/body copy;
- navigation/footer labels;
- CTA labels;
- alt text;
- aria labels where text differs by language;
- metadata descriptions where the architecture supports localization.

Language choice should persist coherently when navigating between public routes using the existing lightweight client-side approach. Turkish must be natural professional Turkish, not literal translation.

## Discoverability / metadata

For each public route, provide truthful and route-specific:

- `<title>`;
- meta description;
- canonical URL;
- Open Graph title/description/url;
- appropriate social preview metadata using only approved/self-hosted assets;
- semantic heading hierarchy and landmarks.

Update `sitemap.xml` and `robots.txt` only as needed for the new public route inventory.

Do not add analytics/tracking scripts.

Structured data may be added only if it truthfully represents current public identity and does not invent organization/product facts. If it creates ambiguity, omit it rather than guess.

## Architecture / implementation scope

Allowed implementation surfaces include:

- new static route directories/pages;
- shared `styles.css` / `script.js` or a bounded maintainability refactor of static assets;
- route-specific approved imagery reuse;
- `sitemap.xml`, `robots.txt`, metadata/social-preview assets;
- validator/test updates;
- `STATUS.md`, `CLAUDE.md`, `CHANGELOG.md` and relevant public-content/provenance documentation.

Do not introduce React, Next.js, Tailwind, a package-manager dependency tree, CMS, backend or routing framework merely to implement these pages.

A dependency/framework/architecture change requires Product re-entry.

## Security / data permissions

- Public website assets/content only.
- No credentials, secrets, private APIs or admin sessions in repository content.
- No form submissions or PII storage.
- No analytics/tracking/privacy-sensitive integration.
- No paid/closed/restricted datasets.
- No deployment, Vercel project write, DNS or Squarespace changes.
- Do not alter Google Workspace or mail configuration.

## Acceptance

WEB-003 is complete only if:

1. `/`, `/platform/`, `/solutions/`, `/pilot/`, `/company/` and `/contact/` resolve as coherent public destinations under the static architecture.
2. Homepage navigation and all deeper-page navigation/footer links are coherent; no placeholder or broken route remains.
3. The accepted homepage WEB-002 proof narrative remains intact and scientifically truthful.
4. Geothermal is visibly the active first application; Mineral and Environmental/Land remain visibly subordinate expansion directions.
5. Kızıldere pilot copy preserves accepted score/evidence/data-gap semantics and mandatory warning boundaries.
6. Company identity remains OrbGSS primary / VirgaSoft secondary and contains no unsupported commercial/team claims.
7. Contact provides a clear public next action without backend, auth, CRM, analytics or PII collection.
8. EN/TR parity is complete across every new route, including visible copy and accessibility text.
9. Language selection persists coherently across route navigation.
10. Route-specific title/description/canonical/Open Graph metadata is truthful and complete; sitemap reflects the new public routes.
11. Semantic headings, landmarks, keyboard/focus navigation and mobile usability remain sound.
12. No scientific/product-proof asset is recolored/reinterpreted and provenance remains valid.
13. No unsupported accuracy/ROI/customer/partner/AI/discovery/reserve/drilling claim appears.
14. Repository validation passes with zero unexplained warnings.
15. WEB-004 hosted-preview work, WEB-005 cinematic hero integration and WEB-006 DNS/cutover remain untouched.

## Verification / evidence

Provide at minimum:

- exact branch and final implementation HEAD;
- changed-path inventory;
- route inventory with canonical public URLs;
- `py -3.14 scripts/validate_site.py` result;
- EN/TR coverage/parity result across all routes;
- internal-link/route validation;
- metadata/SEO validation for each route;
- representative desktop/tablet/mobile evidence for homepage plus all five deeper destinations;
- keyboard/focus/navigation and language-persistence QA;
- confirmation that WEB-002 proof/provenance checks still pass;
- confirmation that no deploy/DNS/hero/backend/analytics work was introduced.

## STOP / route conditions

Stop and return to Product only if implementation would require:

- a framework/dependency/route architecture change outside the accepted static-site model;
- new product behavior or information architecture beyond the canonical routes above;
- new scientific interpretation, score semantics, validation claims or rights decisions;
- public named customer/partner claims or other new commercial assertions;
- analytics/tracking/privacy policy;
- a contact form/backend, authentication, database, CRM or security architecture;
- a social/visual asset whose public rights are unclear;
- credentials/admin access, paid service, Vercel write, DNS or another external irreversible/high-risk action.

Routine HTML/CSS/JS defects, static-route plumbing, copy fitting, responsive/accessibility issues, metadata fixes, validator updates and small conformant refactors are Claude Code Desktop implementer-owned.

## Branch / publication policy

- No feature work on `main`.
- Implement only on `feat/web-003-public-site-depth` from accepted `main@79484bb7d11c3b26373649c802fb4db7d2bd445f`.
- This task publication is authority only and does not start implementation.
- Normal bounded implementation commits are allowed; no artificial micro-step commit budget.
- Do not begin WEB-004, WEB-005 or WEB-006.
- Do not deploy or change DNS.
- Do not merge to `main`; Product performs terminal acceptance/publication after `REVIEW_READY`.
- Terminal implementation state: `REVIEW_READY`.
