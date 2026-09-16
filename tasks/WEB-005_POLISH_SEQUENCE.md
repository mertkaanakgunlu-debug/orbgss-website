# WEB-005 Polish Sequence — pre-WEB-006 execution order

**State:** ACTIVE PRODUCT PLAN  
**Baseline:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`

## Canonical sequence

1. **WEB-005A / MER-107 — Hero visual fidelity, orbital choreography & launch-quality motion**  
   State: `IN_PROGRESS`. Existing local `feat/web-005a-hero-visual-fidelity` work is adopted; do not restart conformant work.

2. **GEO-WEB-003 / MER-108 — Public analytical palette Science authority**  
   State: `WAITING_SCIENCE_DECISION`. May proceed in parallel with WEB-005A. It decides whether/how governed analytical rasters may receive new public/application colour mappings.

3. **WEB-005B / MER-109 — Homepage visual fidelity & public palette system**  
   State: `READY / BLOCKED_BY_WEB-005A` for final integration. Product-owned shell/layout/token work may begin once WEB-005A contracts are stable. Any scientific raster recolouring remains gated by MER-108.

4. **Combined Product visual review**  
   Evidence: screenshots + short hero video are sufficient; a public preview URL is optional. Product terminally accepts exact heads only after visual and machine-verifiable gates are green.

5. **WEB-006 / MER-95 — production domain cutover & public launch**  
   Remains blocked by MER-107 and MER-109 plus the separate CTO DNS human gate. No launch work starts automatically.

## Parallelism

- MER-107 and MER-108 may run in parallel.
- MER-109 should not integrate against a moving hero contract; start its non-hero work only when MER-107 is stable enough to avoid churn.
- MER-109 does not need to wait for MER-108 to improve Act 2 or presentation shells, but cannot ship a new governed value-to-colour mapping without MER-108 acceptance.

## Review inputs

For Product visual review, provide:

- hero before/after stills at entrance, acquisition, regional hold and final handoff;
- full hero screen/video capture;
- Act 2/3/4 before/after screenshots at 1440 desktop and representative responsive widths;
- exact validator/media/provenance evidence required by each task.

## No auto-start

Publishing this plan does not authorize WEB-005B or WEB-006 beyond their issue states. CTO deliberate start remains required for a new task plan. WEB-005A is already in progress under MER-107.
