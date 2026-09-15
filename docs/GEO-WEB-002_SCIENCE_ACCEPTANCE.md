# GEO-WEB-002 / MER-102 — Terminal Science acceptance

**State:** `ACCEPTED / COMPLETE`  
**Date:** 2026-09-16  
**Owner domain:** Science & Geospatial  
**Consumer:** WEB-005 / MER-93  
**Authority baseline:** `8a4fe9ba5cb19d09390cb8816c2324e012331728`  
**Accepted implementation HEAD:** `ea693c29762279131fbed005e832c5ff2dca587b`  
**Accepted REVIEW_READY branch tip:** `adaee0c90413cd88dba89bb8c041090a19977a7e`  
**Canonical package:** `docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md`

## Terminal finding

GEO-WEB-002 passes terminal Science review. The published package is accepted for Product binding into WEB-005. No further Science revision is required.

The accepted result remains within the published task boundary:

- Act 2 uses a real, public-safe Kızıldere-area natural-colour Landsat 8 OLI context master (`LC08_L2SP_179034_20250505_02_T1`, acquired 2025-05-05) rendered at native 30 m into a 2400 × 1500 px EPSG:32635 frame, with exact source, processing, rights, dimensions and SHA-256 records.
- Terrain, THM-01, ALT-01, ALT-02 and priority presentation masters are derived only from the accepted GEO-039 Workbench exports of persisted `kizildere_mvp_v2`; master export identities and checksums are pinned, and website derivatives are crop/downscale/encode-only.
- The accepted scoring identity is unchanged: `mvp_remote_sensing_priority_v1` / `remote_sensing_equal_family_v1`, deterministic accepted run `8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c`, mandatory core THM-01 + ALT-01 + ALT-02.
- Terrain remains context/display only. Structure and Geology remain `optional support / DATA_GAP / score-invariant`. No structure/geology asset is fabricated.
- No MTA paid/closed/restricted data, raw-provider redistribution, new analytical provider, new scientific interpretation, validation claim, probability claim, reserve/resource claim, or drilling-success claim is introduced.
- Existing CRS/grid/units/NoData/mask/resampling/feature-eligibility/scoring semantics are unchanged.

## Resolution acceptance

The task's large-display targets were presentation preferences, not authority to invent resolution. The accepted Kızıldere grid contains 1200 × 1200 cells at 30 m and the accepted GEO-039 renderer produces a 1249 × 1249 px map panel. Therefore:

- Act-2 context target ≥2000 px: **PASS** at 2400 px.
- Evidence-card target ≥1200 px: **PASS** at 1249 px.
- Priority/result target ≥2000 px: **NOT ACHIEVABLE without enlargement under accepted science**, handled by the task-authorized fallback.

The published **1249 device-pixel maximum safe rendered width** for class-B cartographic assets is accepted. WEB-005 must use a deliberately contained priority/result composition rather than browser-upscaling the raster. On a 2× display this corresponds to approximately 624 CSS px if native device-pixel density is to be preserved.

This is not a waiver of scientific quality; it is the truthful presentation constraint required by the accepted source/render path.

## Visual and provenance findings carried forward

- ALT-01 is the preferred single alteration card for the compact homepage evidence trio under the published package. ALT-01/ALT-02's dark-field appearance is a consequence of the accepted governed style and must not be "fixed" by re-stretching, re-normalizing, recolouring or CSS colour/contrast transforms.
- NoData remains visible and must not be cosmetically filled.
- Necessary legends may use the published native legend crops inside their associated visual frame; detached decorative homepage scale bars/legends remain disallowed by Product authority.
- Mandatory warning semantics and public labels in the canonical package remain binding for WEB-005.

## Verification accepted

The REVIEW_READY evidence records:

- `python scripts/validate_site.py` — **PASS, 0 warnings**;
- `git diff --check` — **GREEN**;
- six validator negative tests — expected failures observed and repository restored cleanly;
- deliberately tampered cartographic master — rejected by the derivative builder;
- full derivative rebuild — all 19 generated files reproduced byte-for-byte;
- `geothermal-prospectivity` remained read-only at accepted release authority;
- no GitHub status/check context is configured on this branch, so no unreported remote CI result is being treated as evidence.

Terminal review also verified the branch is a linear continuation of the published MER-102 authority: no force-push, history rewrite or main-branch feature work. The final implementation safety revision `ea693c2` fails closed unless the source export manifest reports the accepted 1200 × 1200 grid before applying the recorded crop/resolution ceiling.

## Review hygiene

A non-semantic documentation inconsistency in `scripts/build_final_visual_masters.py` described 1200 px as the presentation ceiling even though the accepted renderer-native panel and package correctly use 1249 px. Terminal review corrected that wording only; derivative behavior, checksums and scientific semantics are unchanged.

Repository status text inherited stale WEB-004 `REVIEW_READY` wording even though MER-92 is already Product-accepted and canonical main contains the WEB-004 acceptance publication. Terminal publication reconciles repository/Drive/Linear status to the accepted state; this is governance hygiene only and does not reopen WEB-004.

## Product handoff

Science dependency GEO-WEB-002 / MER-102 is resolved. Product may bind `docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md` into the eventual `tasks/WEB-005_CINEMATIC_HERO.md` without a new Science decision, provided the package's exact labels, warnings, provenance and maximum-safe-render constraints are preserved.

GEO-WEB-002 acceptance does **not** start WEB-005. WEB-005 remains subject to its other canonical dependencies and deliberate CTO start approval.
