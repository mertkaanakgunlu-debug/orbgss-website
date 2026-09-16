# WEB-005 — Terminal Product Acceptance

**Linear:** `MER-93`  
**Task:** `WEB-005 — Cinematic Hero Production, Homepage Integration & Release-Candidate Gate`  
**State:** `TERMINAL_PRODUCT_ACCEPTANCE — ACCEPTED / COMPLETE`  
**Accepted implementation branch:** `feat/web-005-cinematic-hero`  
**Execution baseline:** `main@d2421a772f2e4cfa38c85dd5ee71a419c5160838`  
**Accepted implementation HEAD:** `0e3b878280a5c4b4198c223153178f89137bd01c`  
**Accepted REVIEW_READY / evidence HEAD:** `28785747e21a1b25483e739655fe4a8775f94785`  
**Review evidence:** `28785747e21a1b25483e739655fe4a8775f94785:tasks/WEB-005_REVIEW_EVIDENCE.md`

## Product decision

WEB-005 is terminally accepted. The implementation satisfies the published Product execution contract at:

`c62e26304efaac40aaf0cc4975efae976381d7be:tasks/WEB-005_CINEMATIC_HERO.md`.

The accepted release candidate preserves the required four-act public homepage narrative:

1. cinematic acquisition hero;
2. real Kızıldere Earth-observation context;
3. compact Terrain / THM-01 / ALT-01 evidence trio; and
4. the accepted **Remote-Sensing Relative Priority — Experimental Baseline** result climax.

The superseded six-scene homepage gallery is removed. Structure/Geology remains optional support / DATA_GAP / score-invariant and is not fabricated as a homepage evidence scene.

## Acceptance basis

Product reviewed the canonical remote REVIEW_READY state and accepts the recorded evidence, including:

- repository site validation: PASS, 0 warnings;
- hero validation: 184 checks, 0 failed;
- 12/12 deliberate negative regressions caught with the tree restored byte-identically;
- exact production media inventory and checksums;
- WebM, MP4 and poster assets inside the WEB-004 media ceilings;
- intentional mobile, reduced-motion, Save-Data and slow-network static fallbacks with zero video transfer in those states;
- exactly one desktop video encode fetched and no eager `<source>` children;
- responsive evidence at 375 / 768 / 1024 / 1440 CSS px;
- scientific-image safe-density enforcement, including the implementation-time violation that was found and corrected;
- caption contrast correction, with the measured worst case improved to 7.49:1;
- EN/TR visible-copy and accessible-name parity;
- keyboard, focus, landmark, route and image regressions green;
- mobile transfer effectively unchanged from the WEB-004 accepted baseline;
- no new scientific interpretation, scoring method, public probability claim, paid/restricted data, framework migration, backend, analytics, deployment, DNS/domain change or WEB-006 work.

## Hero result-handoff decision

Product explicitly accepts the implementation choice to keep governed scientific/result rasters out of the lossy cinematic video and present the accepted checksummed result through the page-layer handoff (`render_surface: html_overlay`).

This is conformant with WEB-005 because it preserves accepted scientific colours/pixels and avoids creating a video-only reinterpretation of the priority surface while retaining the accepted cinematic acquisition sequence and real-data/result handoff.

The regional 420 km acquisition footprint remains explicitly classified as a production/acquisition frame and **not** the 36 × 36 km analysis AOI. No public copy may reinterpret it as the analysis AOI.

## Honest NOT RUN disposition

The following do not block Product acceptance:

- `HOSTED_PREVIEW_NOT_RUN` — the WEB-005 contract explicitly allows a reproducible local preview when already-authorized hosted-preview credentials/context are unavailable;
- `LIGHTHOUSE_NOT_RUN` — the pinned WEB-004 Lighthouse tooling was unavailable and no new dependency was authorized; the changed transfer/layout/accessibility surfaces were measured directly instead;
- `CONTACT_RELEASE_GATE` remains open and is owned by WEB-006 / launch readiness, not WEB-005.

No PASS is inferred for these checks.

## Provenance correction

The WEB-HERO-001D implementation/evidence HEAD remains `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e`. Its terminal Product acceptance record was published one documentation-only commit later at `573f4f10cbe397e8f3bdf6611deea5cd2660dcae:tasks/WEB-HERO-001D_TERMINAL_PRODUCT_ACCEPTANCE.md`.

This acceptance record is the Product-authoritative correction for that citation defect. It changes no WEB-HERO-001D implementation or semantics and supersedes the incorrect task-file citation for downstream provenance purposes.

## Remaining launch boundary

WEB-005 acceptance authorizes publication of this accepted repository state to `main` by non-force fast-forward. It does **not** authorize production deployment, production-domain attachment/cutover, DNS mutation, mailbox administration or other WEB-006 human-gated launch actions.

After main publication, WEB-005 / MER-93 is complete and WEB-006 / MER-95 becomes the remaining production launch gate.