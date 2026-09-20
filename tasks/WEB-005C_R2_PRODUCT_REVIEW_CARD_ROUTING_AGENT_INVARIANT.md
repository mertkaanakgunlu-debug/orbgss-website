# WEB-005C R2 — Product Review / Homepage Card Routing + Agent Invariant Correction

**Linear:** MER-149  
**State:** REVISION_REQUIRED / BOUNDED_PRODUCT_CORRECTION  
**Implementation under review:** local `feat/web-005c-public-domain-taxonomy-parity@289c8aef0c8237d1c4a123c1d2129c6142bd85ff`  
**Accepted baseline:** `feat/web-005b-homepage-visual-fidelity@0af5b1ad0a5645f8ff3f39f818625944a096635d`

## 1. Review disposition

The WEB-005C taxonomy implementation is technically acceptable and should not be reopened broadly.

Accepted:
- public taxonomy converged to Geothermal / Mining / Marine;
- EN/TR parity;
- legacy `#mineral` and `#environment` compatibility aliases;
- no-JS anchor behavior;
- validator coverage;
- no unrelated visual redesign;
- scientific warning copy preserved;
- lowercase “mineral exploration” may remain as an activity description rather than a top-level taxonomy label.

Two bounded Product corrections are required before terminal acceptance.

## 2. Mandatory correction A — homepage solution cards must navigate

The accepted homepage Product intent is that the three visible solution cards are navigation surfaces.

Now that stable public destinations exist, wire the homepage cards to:
- Geothermal → `/solutions/#geothermal`
- Mining → `/solutions/#mining`
- Marine → `/solutions/#marine`

Requirements:
- preserve the accepted visual design exactly;
- make the card interaction keyboard-accessible and semantically valid;
- preserve normal browser link behavior;
- do not require JavaScript for navigation;
- provide a visible focus state consistent with the existing design system;
- do not add CTA buttons, arrows, hover theatrics or new copy solely for this change;
- do not change the card imagery, hierarchy, spacing or status labels.

This is a Product behavior correction, not a redesign.

## 3. Mandatory correction B — update superseded agent/repository invariant

`CLAUDE.md` currently records a superseded public-navigation/domain invariant that conflicts with accepted Product authority.

Update only the affected invariant so future implementation sessions resolve the public taxonomy as:
- Geothermal
- Mining
- Marine

Do not rewrite unrelated agent instructions.

The durable Product authority remains the canonical task/ADR chain; `CLAUDE.md` must not contradict it.

## 4. Accepted non-blockers

### Status vocabulary

Homepage “In development” vs Solutions “Expansion direction” does not block WEB-005C.

This is content/messaging vocabulary and may be reconciled by the content owner later. Do not broaden this revision to rewrite maturity copy.

### Activity wording

Lowercase phrases such as “mineral exploration” may remain where they describe an activity/capability rather than the top-level public domain label.

### Existing route/anchor compatibility

Keep the legacy alias solution already implemented unless a focused regression test demonstrates a defect.

## 5. Revision envelope

Change only:
- homepage solution-card link semantics and directly coupled accessibility/CSS/test code;
- the exact superseded `CLAUDE.md` taxonomy invariant;
- evidence/status/validator material required to prove the correction.

Do not:
- redesign homepage or Solutions;
- change accepted copy beyond directly coupled accessibility text;
- change scientific semantics;
- alter hero/media;
- merge, deploy, touch Vercel or DNS;
- start WEB-006.

One bounded local revision commit is authorized.

## 6. Acceptance

Return:
`REVIEW_READY / WAITING_PRODUCT_REVIEW`

with:
- exact revised local HEAD;
- changed paths;
- proof all three homepage cards resolve to the correct canonical anchors with JS disabled;
- keyboard/focus proof;
- EN/TR proof;
- confirmation legacy `#mineral` / `#environment` aliases still land correctly;
- full relevant validators GREEN;
- confirmation no unrelated visible homepage delta occurred.

After Product accepts this revision and exact-head publication is complete, WEB-005C may close and WEB-006 preparation may begin.
