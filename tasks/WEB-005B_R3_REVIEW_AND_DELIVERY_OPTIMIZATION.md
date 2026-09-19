# WEB-005B R3 — Review Disposition and Bounded Delivery Optimization

**State:** PRODUCT_REVIEW_PENDING_VISUAL / BOUNDED_REVISION_AUTHORIZED  
**Implementation under review:** `feat/web-005b-homepage-visual-fidelity@b597bafc605bfed9466aea82e31d539cf6e5035a`  
**Parent authorities:** WEB-005B R1 / R2  
**Science authority consumed:** MER-108 website display derivative authority `11c32e8d2d072aa709262e513c8888e6a745bb76`

## 1. Technical disposition

The submitted WEB-005B package is technically REVIEW_READY and may proceed to the final Product human visual gate. The accepted WEB-005A hero baseline is preserved and no further hero work is authorized.

## 2. Delivery optimization decision

Before terminal Product acceptance, perform one bounded responsive-image delivery optimization for the Acts 3–4 analytical derivatives.

MER-108 §8 already permits visually-lossless lossy web encoding when it does not introduce visible false classes, ringing, or colour shifts that materially change interpretation.

Therefore:

- keep the governed scientific masters and the current lossless WEB-005B derivatives as upstream/reference assets and evidence;
- generate responsive delivery candidates using a modern browser-supported lossy web codec already compatible with the current site delivery stack;
- preserve the exact spatial footprint, normalization, palette topology, context/hillshade rule, analytical opacity, and NoData/mask semantics;
- mask/transparent support must remain exact; compression must not create visible colour contamination into NoData or outside governed support;
- the coupled legend remains lossless and canonical;
- select lossy delivery only where it produces a meaningful payload reduction while remaining visually indistinguishable at intended display size and without changing interpretation;
- if a layer cannot meet that bar, keep its lossless derivative;
- do not change source dimensions, scientific normalization, palette stops, hillshade parameters, or CSS visual hierarchy merely to improve compression.

Required evidence:
- before/after bytes for every candidate;
- decoded comparison against the lossless reference at the same dimensions;
- edge/NoData inspection;
- real-page screenshots at representative desktop/mobile DPRs;
- validator confirmation that scientific/provenance invariants remain intact.

This is implementation optimization, not a Science re-entry.

## 3. ALT-01 decision

Keep the current canonical ALT-01 rendering. Do not reopen Science or add a display-window exception merely to increase visual contrast on the homepage.

The dark-field appearance is accepted as a truthful consequence of the governed rendering for this surface. Visual hierarchy should be carried by layout/composition, not by changing ALT-01 semantics.

## 4. Footer attribution

Do not change the footer copy in WEB-005B. The attribution mismatch is a content-owner handoff because final website copy/content is outside Product/Software scope for this task.

Record the issue for the content-owning domain, but do not block visual implementation or rewrite the sentence here.

## 5. Final Product gate

After the bounded encoding pass, return the final homepage visual evidence for human Product/CTO review.

Do not merge, deploy, begin WEB-006, or redesign other routes before Product visual acceptance.

**Terminal implementation state remains:** `REVIEW_READY`.
