# WEB-005C R3 — Product Acceptance / Exact-Head Publication Gate

**Linear:** MER-149  
**State:** PRODUCT_ACCEPTED / WAITING_EXACT_HEAD_PUBLICATION  
**Implementation under review:** local `feat/web-005c-public-domain-taxonomy-parity@79cc2cb82a4542461cbbfc1d0c349cf02b861084`  
**Parent authority:** WEB-005C R2

## Decision

The bounded R2 revision is accepted.

Accepted behavior:
- homepage Geothermal / Mining / Marine cards are native full-card navigation surfaces;
- destinations are `/solutions/#geothermal`, `/solutions/#mining`, `/solutions/#marine`;
- navigation works without JavaScript;
- keyboard tab/Enter behavior is valid;
- visible focus uses the existing accent system;
- EN/TR labels remain aligned;
- legacy `#mineral` and `#environment` aliases still resolve to the canonical Mining/Marine rows;
- the superseded public taxonomy invariant in `CLAUDE.md` is corrected;
- no unrelated homepage geometry/copy change is accepted or required.

## Gradient rasterization observation

The reported <=7/255 single-channel dither shift over the card shade is accepted as non-blocking.

Reason:
- deterministic DOM geometry/computed-style evidence shows no layout/style drift;
- the shift is below the defined visible-regression threshold and isolated to browser gradient rasterization caused by the positioned full-card link overlay;
- removing the overlay would weaken the accepted Product behavior by making only the copy region navigate.

Product prefers semantically complete full-card navigation over literal pixel identity for this case.

Do not revise the overlay solely to eliminate this rasterization noise.

## Non-blocking content observations

Do not expand WEB-005C to reconcile:
- homepage “In development” vs Solutions “Expansion direction”;
- lowercase capability/activity wording such as “mineral exploration”.

Those remain content/messaging follow-ups.

## Publication gate

Before MER-149 can close:
1. push `feat/web-005c-public-domain-taxonomy-parity` normally, non-force;
2. publish the exact reviewed HEAD `79cc2cb82a4542461cbbfc1d0c349cf02b861084`;
3. verify remote HEAD equals that exact SHA;
4. make no amend/squash/new implementation commit during publication;
5. leave unrelated untracked user files untouched.

No merge, deployment, Vercel mutation or DNS change is authorized.

After exact-head publication is verified, MER-149 may close and WEB-006 release/cutover planning may bind this HEAD as the accepted website release candidate.

**Current state:** WAITING_EXACT_HEAD_PUBLICATION.
