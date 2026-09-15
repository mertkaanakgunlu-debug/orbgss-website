# WEB-004 — Responsive, Accessibility, Performance & Hosted Preview Acceptance

**Linear:** MER-92  
**Authority:** CURRENT — OrbGSS Website vNext Product & Execution Authority v1.8 + this exact task.  
**Canonical repository:** `mertkaanakgunlu-debug/orbgss-website`  
**Reference/upstream only:** `baran-orbgss/website`  
**Accepted baseline:** `main@f4d77b4144ddff70c309986e6a45b163f62cdcd4` (WEB-003 accepted/published; accepted WEB-003 implementation head `3670d43bece4ffba657a3d9645cbea20c7e698bf`).  
**Branch:** `feat/web-004-preview-hardening`  
**Product state:** `IMPLEMENTED — REVIEW_READY` (CTO start approval given; implemented on `feat/web-004-preview-hardening`. Evidence: `docs/WEB-004_HARDENING_EVIDENCE.md`. Two items routed to Product with the review: homepage LCP 3.2 s against the 2.5 s target, and the score-legend `image-aspect-ratio` deviation.)

## Outcome

Harden the accepted six-route OrbGSS public site into a release-candidate-quality static preview before final hero integration.

WEB-004 must prove that the existing public site is responsive, accessible, performant, stable and deployable on representative mobile/tablet/desktop conditions without depending on the future cinematic hero. It is a hardening/acceptance task, not a redesign task.

The result must leave WEB-005 with an explicit, evidence-backed media budget for the final hero and must leave production DNS untouched.

## Governing invariants

Preserve all accepted WEB-001..WEB-003 product/science behavior:

- canonical public routes remain `/`, `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/`;
- OrbGSS primary / VirgaSoft secondary brand hierarchy;
- Geothermal = active first application/pilot; Mineral + Environmental/Land = expansion directions;
- accepted Kızıldere proof imagery, warnings, checksums, provenance and score semantics remain unchanged;
- no scientific raster recoloring/reinterpretation;
- Structure/Geology remains an explicit public data gap unless separately authorized;
- EN default / TR parity and language persistence remain mandatory;
- static HTML/CSS/vanilla-JS architecture remains accepted;
- no framework/package-manager/CMS/backend introduction without Product re-entry;
- no analytics/tracking, auth, CRM, billing or PII collection;
- no production DNS or Squarespace changes;
- later R7 public visual/palette authority is downstream presentation guidance and does not authorize WEB-004 to redesign the accepted site.

## Scope

WEB-004 owns hardening and acceptance across the accepted site:

### Responsive behavior

- verify and fix layout across representative narrow mobile, large mobile/small tablet, tablet/laptop and wide desktop widths;
- remove horizontal overflow, clipped controls, unstable line wrapping, unreadable captions, unusable touch targets and accidental content overlap;
- preserve intentional full-width/cinematic composition without forcing desktop layouts onto mobile;
- verify orientation/viewport changes do not leave stale menu/disclosure state.

Representative widths must include at least `375`, `768`, `1024` and `1440` CSS px. Add another breakpoint only if a real defect requires it.

### Accessibility

Validate and fix, as applicable:

- skip-link and landmark structure;
- heading hierarchy;
- keyboard-only navigation through header, Solutions disclosure, language controls, evidence tabs and all primary CTAs;
- visible focus treatment;
- disclosure/tabs `aria-*` state synchronization;
- localized accessible names in EN/TR;
- alt text and decorative-image semantics;
- touch target usability;
- contrast for text, controls and on-image labels;
- reduced-motion behavior for current transitions/interactions;
- no focus loss/trap during mobile menu/disclosure use.

Do not weaken scientific warning visibility or hide evidence/data-gap semantics to satisfy layout.

### Performance and loading

Measure the accepted baseline before optimization and improve only with semantics-preserving changes.

Allowed examples include:

- image dimension/srcset/sizes/loading/decoding corrections;
- removing redundant bytes or duplicate fetches;
- bounded CSS/JS cleanup;
- cache/header/static-routing corrections;
- avoiding unnecessary eager media;
- eliminating major layout shift caused by known asset dimensions or late UI state.

Do not re-encode or visually alter accepted scientific proof derivatives unless the existing public-safe provenance authority explicitly permits the exact derivative operation and the resulting derivative is recorded/checksummed. Prefer loading-policy/CSS/layout fixes over changing proof pixels.

### Performance acceptance budgets

Use repeatable browser tooling and record tool/version/context. The accepted static site before WEB-005 must satisfy all of the following on the tested preview/local server:

1. **No critical route regression:** no canonical route may introduce a new render-blocking or duplicate-request defect versus the accepted WEB-003 baseline.
2. **Core Web Vitals target under controlled test:** representative mobile test should target LCP ≤ 2.5 s, CLS ≤ 0.10 and INP-equivalent interaction latency ≤ 200 ms where the chosen tooling can measure them reliably. If local synthetic tooling cannot produce a valid INP, record the nearest interaction metric and manual evidence rather than inventing a value.
3. **Lighthouse-style quality floor:** Accessibility ≥ 95; Best Practices ≥ 95; SEO ≥ 95 on representative public routes. Performance target ≥ 90 on the homepage and ≥ 90 on at least one deep content route under the recorded mobile profile. A deterministic functional/performance report may substitute for Lighthouse only if the environment cannot run it and the substitution is documented.
4. **Static code budget:** no new framework/dependency tree; combined first-party CSS + JS transfer must remain small enough that WEB-004 does not become the dominant page payload. Any >15% increase from accepted WEB-003 baseline requires a concrete justification in evidence.
5. **Future WEB-005 hero reserve:** publish an explicit final-media envelope based on measured remaining budget. Default Product ceiling unless measured evidence justifies a tighter value: desktop autoplay hero WebM ≤ 4 MiB, MP4 fallback ≤ 6 MiB, poster ≤ 500 KiB; mobile/reduced-data delivery must not require downloading both video encodes and must have an intentional static/reduced-motion fallback. WEB-004 may tighten these ceilings; it must not loosen them without Product re-entry.

Scores are evidence, not product claims; do not expose performance-test numbers as marketing copy.

### Hosted/reproducible preview

- If the existing Vercel project/team identity and authenticated write permission are already available without credentials/admin/payment changes, create or update a **preview deployment only** from the WEB-004 branch and record the exact URL/deployment identity.
- Do not attach or change production domains in WEB-004.
- Do not modify Squarespace DNS.
- If Vercel preview write permission is unavailable, do **not** ask for credentials or change account/admin state. Record `HOSTED_PREVIEW_NOT_RUN — permission unavailable` and provide an equivalent reproducible local preview command/evidence. This does not block WEB-004 code acceptance; production launch remains gated later.
- Any request for paid hosting, ownership transfer, credentials, admin changes or production-domain writes is a HUMAN_GATE.

### Contact release gate

The site may continue to use `contact@orbgss.com`. Verify route/mailto correctness and record one of:

- `CONTACT_TARGET_CONFIRMED` with the exact non-secret evidence available to the implementer; or
- `CONTACT_RELEASE_GATE` if mailbox ownership/delivery cannot be proven without Workspace/admin access.

`CONTACT_RELEASE_GATE` does not block WEB-004 technical acceptance, but it remains a mandatory pre-WEB-006/public-launch gate. Do not enter credentials or alter Google Workspace.

## Out of scope

- redesigning the accepted public information architecture or homepage narrative;
- implementing the later R7 final public-layout/palette recomposition;
- producing/integrating the final cinematic hero;
- changing scientific methodology, score semantics or proof assets beyond permitted loading/derivative handling;
- analytics/tracking/privacy integrations;
- contact form/backend/CRM/auth/database;
- production Vercel domain changes;
- Squarespace DNS changes;
- MX/SPF/DKIM/DMARC/Google Workspace administration;
- purchases, billing upgrades, credential entry, ownership transfer or irreversible hosting operations.

## Acceptance

WEB-004 is complete only if:

1. all six canonical routes render coherently at the representative width matrix with no horizontal overflow or critical responsive defect;
2. primary navigation, mobile menu, Solutions disclosure, language switching and evidence tabs are keyboard/touch usable and state-correct;
3. EN/TR visible and accessibility-text parity remains complete;
4. heading/landmark/focus/alt/contrast/reduced-motion checks have no unresolved critical issue;
5. accepted WEB-002/WEB-003 scientific/public-claim invariants still pass unchanged;
6. no broken internal route, fragment or asset remains;
7. repository validator passes with zero unexplained warnings;
8. performance evidence is repeatable and meets the budgets above, or a genuine Product trade-off is routed instead of silently relaxing them;
9. WEB-005 receives an explicit hero media budget in repository status/evidence;
10. a hosted Vercel preview is recorded when already-authorized permission exists, otherwise a reproducible local preview plus `HOSTED_PREVIEW_NOT_RUN` is recorded truthfully;
11. contact target is either confirmed or explicitly retained as `CONTACT_RELEASE_GATE`;
12. no WEB-005 hero integration, WEB-006 DNS/cutover, analytics/backend or unrelated redesign work is introduced.

## Verification / evidence

Provide at minimum:

- exact branch and final implementation HEAD;
- changed-path inventory;
- `py -3.14 scripts/validate_site.py` result;
- responsive screenshot/measurement matrix at 375 / 768 / 1024 / 1440 px for homepage plus representative deep routes, with all six routes at least spot-checked;
- keyboard/focus/mobile-menu/Solutions-disclosure/evidence-tabs/language-persistence QA;
- EN/TR and accessible-name parity result;
- contrast/reduced-motion/semantic-structure findings;
- broken-link/asset result;
- performance report with tool/version/profile and before/after comparison where changes were made;
- measured CSS/JS/static-media payload summary;
- exact WEB-005 hero media budget adopted from the evidence;
- Vercel preview URL/deployment identity if created, otherwise exact reproducible local preview command and `HOSTED_PREVIEW_NOT_RUN` reason;
- `CONTACT_TARGET_CONFIRMED` or `CONTACT_RELEASE_GATE` with non-secret rationale;
- confirmation that accepted scientific proof checksums/provenance/warnings still pass;
- explicit confirmation: no WEB-005 integration, no production deployment/domain change, no DNS, no analytics/backend.

## STOP / route conditions

Return to Product only for a genuine semantic/high-risk decision, including:

- framework/dependency/architecture change appears necessary;
- accepted route/product behavior or UX policy must change to satisfy hardening;
- performance budget cannot be met without degrading accepted product/science meaning or requiring a Product trade-off;
- accepted scientific asset would need visual reinterpretation or unapproved derivative semantics;
- new privacy/analytics/security policy is required;
- paid hosting/CDN/asset purchase is required;
- production-domain/DNS change is required;
- credentials/admin/ownership transfer is required;
- destructive/irreversible action is required.

Routine responsive bugs, CSS/JS defects, accessibility fixes, loading-policy changes, validator updates, local preview setup, preview-deployment mechanics under already-authorized credentials, CI/tooling friction and small conformant refactors are implementer-owned.

## Branch / publication policy

- No feature work on `main`.
- Implement only on `feat/web-004-preview-hardening` from accepted `main@f4d77b4144ddff70c309986e6a45b163f62cdcd4`.
- This task publication is authority only and does not start implementation.
- Normal bounded implementation commits are allowed; no artificial micro-step commit budget.
- Do not begin WEB-005 or WEB-006.
- Do not merge to `main`; Product performs terminal acceptance/publication after `REVIEW_READY`.
- Terminal implementation state: `REVIEW_READY`.
