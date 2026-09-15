# WEB-004 — Terminal Product Acceptance

**Date:** 2026-09-16  
**Linear:** MER-92  
**Task:** `tasks/WEB-004_PREVIEW_HARDENING.md`  
**Accepted branch:** `feat/web-004-preview-hardening`  
**Accepted implementation commit:** `56cb53039b85a852110c737505bc2ae2282acb08`  
**Accepted REVIEW_READY branch head:** `fc5d2e2eb595944d194603e15f894ea9fb643593`  
**Accepted baseline:** `main@f4d77b4144ddff70c309986e6a45b163f62cdcd4`

## Decision

`WEB-004` is **PRODUCT_ACCEPTED / COMPLETE**.

Product terminal review verified the remote branch topology and the bounded implementation/evidence publication. Canonical `main` was advanced non-destructively by fast-forward to the accepted REVIEW_READY branch head before this acceptance publication.

The accepted result preserves the WEB-001..WEB-003 product/science contract while hardening the six-route public site for responsive behavior, accessibility and loading/performance.

## Accepted evidence

- repository validator: PASS / 0 warnings;
- homepage Lighthouse mobile-profile performance: 77 → 94;
- homepage LCP: 6.5 s → 3.2 s under the recorded local synthetic profile;
- CLS 0; TBT 0 ms;
- homepage transfer: 1369.6 KiB → 645.1 KiB;
- all six routes meet the recorded Accessibility / Best Practices / SEO floors; homepage and deep-route Performance floors pass;
- responsive measurement matrix covers 375 / 768 / 1024 / 1440 CSS px;
- caption contrast defects, stale disclosure state, WCAG 2.5.8 touch-target defects and `/contact/` heading-order defect are closed;
- hero poster derivatives and deferred evidence loading remain provenance/checksum guarded;
- no framework/backend/analytics, WEB-005 integration, production deployment, domain or DNS work was introduced.

Full evidence: `docs/WEB-004_HARDENING_EVIDENCE.md`.

## Accepted Product decisions

The following MER-92 decisions are terminally accepted and remain binding downstream:

1. Homepage LCP `3.2 s` under the recorded local synthetic profile is an accepted bounded WEB-004 deviation. Accepted scientific proof derivatives must not be re-encoded solely to chase the `2.5 s` target.
2. The score-legend `image-aspect-ratio` audit finding is an accepted intentional deviation. The accepted scientific legend must not be re-proportioned solely to clear that heuristic.
3. WEB-005 media envelope:
   - desktop autoplay WebM ≤ `3.0 MiB`;
   - MP4 fallback ≤ `4.5 MiB`;
   - poster ≤ `180 KiB`;
   - mobile/reduced-data uses an intentional static/poster fallback and must not require downloading both video encodes.
4. `HOSTED_PREVIEW_NOT_RUN — permission unavailable` is accepted under WEB-004 and does not block technical acceptance.
5. `CONTACT_RELEASE_GATE` remains open and mandatory before WEB-006/public launch.

## Downstream state

WEB-005 is no longer blocked by WEB-004. It remains blocked by the dedicated pre-data hero lane until an accepted `WEB-HERO-001D / MER-101` handoff exists, and it still requires deliberate CTO start approval.

No production DNS/cutover action is authorized by this acceptance.
