# Changelog

## WEB-005B homepage visual fidelity — 2026-09-20 (MER-109, branch `feat/web-005b-homepage-visual-fidelity`; `REVIEW_READY`, nothing deployed)

Acts 2-4 rebuilt as one continuous story after the terminally accepted WEB-005A hero, which is
preserved byte- and pixel-identical. Full evidence in `tasks/WEB-005B_EVIDENCE.md` and
`evidence/web005b/`.

- **Act 2 — the real place.** Full-bleed natural-colour Landsat band. Same USGS product as the
  GEO-WEB-002 master, re-cropped wider at native 30 m (3200 x 1800 px, 96 x 54 km, 100 % valid) and
  re-rendered on ONE common reflectance scale — the old per-band 1-99 percentile stretch is what made
  the photograph read as a processed raster. Four corner marks draw the true 36 km analysis square
  from the recorded frame geometry, which the validator checks against the CSS.
- **Act 3 — one evidence stage.** Terrain, THM-01 and ALT-01 as three identical squares of the same
  ground on one plate with hairline gutters and a shared caption rail; a tablet row layout between 561
  and 900 px keeps the stack compact. Still exactly three; Structure/geology stays a footnote.
- **Act 4 — the result.** The priority surface alone on its own stage at 600 CSS px, 2.2x the area of
  any evidence panel, with the hero's cyan target corners and the map's own unblended LUT as a legend
  coupled beneath it. No detached colour strip.
- **Acts 3 and 4 now ship MER-108 website display derivatives** of the governed MER-113 rasters
  (`scripts/build_web005b_derivatives.py`), so the page reads as one palette system from the hero
  payoff to the result. Canonical normalization, frozen hero palette stops, NoData transparent over a
  neutral DEM hillshade at fixed analytical opacity, at most one area downsample, lossless WebP, never
  above the native 1200 px grid. None of the hero-only transforms (display window, gamma, Gaussian,
  unsharp, upsampling) is used. Recomputing the priority layer reproduces the CTO-approved
  `priority_webhero_v1` raster exactly. The GEO-WEB-002 exports stay published for `/pilot/`.
- **Product palette tokens** defined once in `:root` and pinned by the validator.
- **New gates.** `scripts/negative_tests_web005b.py` (24/24 caught) and
  `scripts/check_copy_preservation.py`. The site validator gained the whole WEB-005B contract,
  including recomputing each palette LUT from its recorded stops.
- **Copy unchanged.** Only `alt.terrain.home` (EN/TR, because the old alt text described the previous
  palette) and the legend's `0` / `100` ticks were added.

## WEB-005A R3 preview gate — 2026-09-18 (MER-107, branch `feat/web-005a-hero-visual-fidelity`; no version bump, nothing shipped)

Product reviewed `37152222` and returned it `REVISION_REQUIRED`
(`docs/web-005-polish-authority@473b48a`): the camera moved before the scan, the platform sat under the
hero copy on the real page, and the analytical reveal was a planar page overlay rather than DEM relief.
The review requires a low-cost preview gate before any further long render. This is that gate; full
evidence in `tasks/WEB-005A_R3_PREVIEW_GATE.md`. **No site file, shipped media or production scene
changed.**

- **New scene `hero_r3_preview_gate`** (role `hero_preview_gate`, extends the production scene) and
  render profiles `preview_gate` / `preview_gate_animatic` (Cycles 1280 x 720 at 48 samples; about a
  twentieth of a production frame).
- **Fixed observer.** Shot-intent mode `hold_of` and `camera.fixed_through_frame`: the opening camera
  state is the acquisition state, the builder refuses any channel that changes before frame 208 and
  holds the rest CONSTANT. Measured 0.0 m / 0.0 deg / 0.0 mm over 208 frames.
- **Pass re-solved for the real page.** The platform comes round the left limb and settles at
  x = 0.555; its silhouette never comes left of 0.490 while acquiring (copy column ends at 0.473 at
  1440 x 900). No CSS or copy change.
- **Scan fan.** Four lines plus a veil on the faces they span and a light curtain of translucent slices,
  swept west to east in step with the ground band (one keyed value). Fan, wash and lines retire by 208;
  the camera first moves at 209.
- **One persistent lock frame.** Drawn on the accepted 36 km fixture with `presented` / `sag_comp` /
  `weight` / `drape` shape keys derived from the evaluated camera (`derive_presentation.py`): 7 % to
  24 % of the frame with no swap, line weight 1.5-2.2 px throughout, 0.31 m from the true corners when
  settled.
- **DEM relief.** `aoi_relief` displaces a 600 x 600 grid from the governed `top-dem.tif` only (3x), and
  the prepared Terrain / THM-01 / ALT-01 / priority display textures cross-fade on that one UV, ending
  on priority alone. `materialize_analytical_assets.py` ingests the pinned handoff by copy and SHA-256.
- **Gates.** `audit_preview_gate.py` 36/36 over 420 evaluated frames; hero validator 343 checks
  (34 new), and it fails if the production scene picks up the relief while this gate is open; site
  validator PASS, 0 warnings.
- **Inheritance.** Scene objects may now declare `replace` (re-author wholesale, position kept) and
  `omit`. `render_animatic.py` plays a stepped animatic in real time.

## v1.0.0-rc3-web-005a-hero-visual-revision — 2026-09-18 (WEB-005A R3, MER-107, branch `feat/web-005a-hero-visual-fidelity`)

The R2 package was technically green and did not pass the human visual gate. R3 keeps its satellite
model, sensing-line envelope and Earth stack and re-choreographs the shot. Full evidence in
`tasks/WEB-005A_HERO_FIDELITY_EVIDENCE.md` (Part A).

- **The satellite settles.** `orbit_intent.rate_profile` time-remaps one circular 900 km orbit: fast
  round the limb, 0.03 °/frame from frame 110. Per-frame measurement showed the remaining drift was
  parallax from the camera's dolly, so the camera is locked off from the handover to the release and
  the platform holds within 0.01 of (0.25, 0.40) for 56 frames.
- **The lines release while the platform is still in frame**, with an acquisition-complete pulse;
  R2 drew them from off-screen for two seconds.
- **One dive, a frame that can vanish, and the analysis frame.** The regional frame's materials gain
  a transparent presence gate and a `vanish` range; the accepted 36 km analysis AOI is a second
  fixture (`production_analysis_aoi`) drawn as its own frame with a lock event; the hold is keyed
  twice so it is still. Motion blur (shutter 0.5) on the production profile.
- **30 m ground structure under the hold** from a Sentinel-2-derived detail ratio that multiplies
  the Blue Marble albedo — no colour, no season, no seam — with the Copernicus attribution in the
  footer.
- **The handoff is inside the target.** The four accepted derivatives are registered onto the
  audited corners of the analysis frame by a CSS homography and revealed in evidence order, ending
  on the priority result; the stack is clamped under 1249 device pixels. No faults layer: the
  structure/geology data gap is not filled.
- Validators: hero 292 checks, site PASS 0 warnings, negative tests 27/27, shot audit 18/18.

## v1.0.0-rc1-web-005-cinematic-hero — 2026-09-16 (WEB-005, MER-93, branch `feat/web-005-cinematic-hero`)

The pre-launch homepage release candidate. Consumes the accepted WEB-HERO-001D cinematic system
(`e95fdcac7cac82e597d40dab4cdc96ce1a6b319e`) and the accepted GEO-WEB-002 visual master package, and
replaces the intermediate six-scene homepage with the locked four-act narrative. No new science, no
new routes, no deployment. Full measurements in `tasks/WEB-005_REVIEW_EVIDENCE.md`.

- **The homepage is now four acts:** cinematic acquisition hero → real Kızıldere EO context → a
  compact three-card evidence trio → the priority/result climax. The WEB-001/002
  `dark beam → full-width raster` rhythm is gone. It gave every scientific state equal weight and
  stretched correct cartography until it read as texture; each act now owns a different composition,
  and every explanation sits against the visual it describes instead of being inferred from scroll
  position. `scripts/validate_site.py` fails the build if the old components, act count or act order
  come back, or if the evidence act ever holds anything but three cards.
- **The hero is the accepted WEB-HERO-001D sequence, re-rendered against the real pilot region.** The
  design fixture that "names no site" is replaced by the real accepted Kızıldere centre
  (37.9794 N, 28.7907 E) through the `aoi_injection_interface` that was built for exactly this, as a
  configuration change. The camera was re-derived rather than retyped — an 8 km centre shift moves a
  camera 1179 km up by about 25 m — and frames 241–276 add no new motion, only the accepted final
  easing continued to a standstill so the shot ends on the frame that becomes the poster.
- **The hero's 420 km footprint is a regional acquisition frame, not the analysis AOI.** The accepted
  analysis AOI is 36 × 36 km. The fixture declares `is_analysis_aoi: false`, the hero validator fails
  without that disclaimer, and public copy states the 36 km extent separately.
- **No scientific raster is baked into the video, deliberately.** VP9 and H.264 ship 4:2:0 chroma at
  a lossy bitrate, and the priority surface is read *by colour* against a governed `batlow` ramp — so
  encoding it would quantise and subsample precisely the channel its meaning lives in. The video
  carries the acquisition only; the result handoff is a page element shipping the exact checksummed
  accepted derivative. The hero scene records this as `render_surface: "html_overlay"` with its
  reason, and `validate_hero.py` enforces it. It also gives the viewer what the task asks for —
  acquisition imagery and analytical result are visibly different kinds of thing.
- **The hero says it is a render.** `Rendered orbital sequence — not sensor imagery`, in EN and TR, in
  the caption, non-optional. `IMAGERY_RIGHTS.md` gains a third asset class for it: class B must never
  be made prettier than the science, and class C must never be allowed to look like measurement.
- **Safe display density is measured, not asserted — and the measurement caught a real violation.**
  Across a 360 → 3840 CSS px sweep of the built page, an uncapped evidence card reached **767 CSS px
  on a 2560 px display, 1534 device pixels** against a raster whose honest ceiling is 1249 — browser
  upscaling of scientific content that the `sizes` attribute alone would never have revealed. Cards
  are now capped at 624 px. Final worst cases: Act-2 context 1199 CSS px (2398 device px at 2×,
  ceiling 2400), each evidence card 624 (1248, ceiling 1249), the priority map 623 (1246, ceiling
  1249), the in-frame legend 248 against a 732 px native crop. Every figure is recorded in
  `geo_web_002.assets[].web_005_placement.rendered`, and the validator now recomputes
  `max_css_width × dpr ≤ device_px` so a later layout change cannot quietly widen a scientific visual.
- **Act 4 is contained because it must be.** The accepted score raster is 1200 × 1200 cells at 30 m
  drawn at 1249 px and cannot reach the ≥ 2000 px Act-4 target from accepted science. The composition
  carries the weight instead of the raster being stretched, and the export's own governed legend sits
  *inside* the map frame — no detached homepage colour bar, and the validator checks for one.
- **One encode per visitor, and often none.** The hero ships a poster `<img>` and an empty `<video>`
  whose candidates live in `data-` attributes: a `<source>` child starts fetching during parse, and
  with two declared a browser can fetch both. `script.js` decides instead. Verified end-to-end with
  stubbed conditions: `prefers-reduced-motion`, `saveData`, `effectiveType` ∈ {slow-2g, 2g, 3g} and
  viewports ≤ 780 px each produce an intentional still hero with **zero video bytes**, and a refused
  autoplay settles to the poster rather than leaving a blank frame. Reduced motion is honoured
  mid-visit, and a 15 s timer guarantees the analytical result is never hidden behind a video that
  failed.
- **Structure/geology remains an explicit, subordinate data gap** — a short footnote under Act 3,
  stated as score-invariant, not fabricated and not promoted into an act.
- **Mandatory warnings are now checked per route that shows the asset**, in both languages and in
  static HTML, rather than on the homepage only — which matters now that the WEB-002 proof assets
  live on `/pilot/` and no longer on the homepage.
- **Dead code removed:** the evidence layer switch (markup, ~90 lines of JS, CSS) is gone from every
  page along with the detached score scale strip.
- **Validators extended:** hero workspace 151 → 184 checks; the site validator gains the four-act
  contract, the package-placement and safe-density checks, the hero media contract and the
  per-route warning rule. The hero lane's isolation rule became a lane *boundary* — WEB-005 was
  always named as its one authorized integration gate, so the pin moves to the WEB-005 baseline and
  the rule becomes "public-site changes stay inside the declared integration write surface".
- **EN/TR parity complete**, including accessible names, `alt` text and `<html lang>`; 23 focusables
  in DOM order with no missing focus ring; landmarks and heading order clean; all six canonical
  routes plus `/404.html` return 200 with no broken imagery; no horizontal overflow at any width.
- No merge to `main`, no deployment, no Vercel or domain change, no DNS/MX/SPF/DKIM/DMARC change, no
  analytics or backend, no framework or dependency, no new route, no new public claim, and no
  WEB-006 work.

## v0.9.0-web-004-preview-hardening — 2026-09-16 (WEB-004, MER-92, branch `feat/web-004-preview-hardening`)

Hardening and acceptance of the accepted six-route site. No redesign, no new routes, no change to
product, science or claim semantics. Full measurements in `docs/WEB-004_HARDENING_EVIDENCE.md`.

- **Homepage performance 77 → 94** (Lighthouse 13.4.1, mobile profile, simulated Slow-4G), LCP 6.5 s → 3.2 s, CLS 0, TBT 0 ms. Total page transfer fell **1369.6 KiB → 645.1 KiB (−53%)**. Every route now clears the task's Accessibility / Best Practices / SEO ≥ 95 and Performance ≥ 90 floors.
- **Hero delivery.** The 553 KiB JPEG that served every viewport now has three recorded WebP derivatives (900 / 1400 / 1800), wired with `srcset`/`sizes` and a matching `<link rel="preload" imagesrcset>` so the poster is discovered during the initial HTML scan rather than after the stylesheet. A 375 px phone fetches ~148 KiB instead of 553 KiB. Resize-and-encode only — no crop, colour, tone or gamma change — and each derivative is recorded in `assets/imagery/sources.json` with its operation, byte size and SHA-256.
- **Inactive evidence layers are deferred.** All three evidence rasters used to load during the initial page load; the two nobody was looking at cost 340 KiB and six performance points. They now carry `data-src`/`data-srcset` and are promoted as the evidence section approaches the viewport, so switching stays instant. Without JavaScript the inactive panes are permanently hidden, so not fetching them is the truthful behaviour.
- **Caption contrast is now measured, not assumed.** `object-fit: cover` re-crops each proof raster as the viewport changes shape, so the pixels under the bottom-right caption move — and the WEB-002 hand-chosen tones measured **2.84:1, 3.53:1 and 4.21:1** at some widths, below WCAG 1.4.3. `script.js` now applies WEB-002's own rule continuously: sample the rendered region, keep whichever of the two already-accepted tones contrasts better. Every caption now clears 4.5:1 at 375 / 768 / 1024 / 1440 (worst case 4.58:1). The raster is never touched and the caption is still bare monospace text with no card, box or band; without JavaScript the authored tone stands.
- **Viewport-change state reset.** Crossing the 980 px breakpoint with the mobile menu open left the hidden menu button reporting `aria-expanded="true"` and left the Solutions submenu visibly open on the desktop bar. Both disclosures now reset on the breakpoint crossing.
- **Touch targets meet WCAG 2.5.8.** Footer nav links (11 px tall), the direct email link (18 px), the brand wordmark (21 px) and the desktop EN/TR buttons (21–22 px wide) are now ≥ 24 px, via padding and `min-width` only — no type-size or density change. Zero undersized targets across all six routes at all four widths.
- **`/contact/` heading order fixed** — three `<h3>` directly under the page `<h1>` are now `<h2>`; route Accessibility 98 → 100.
- **`site.webmanifest`** declares a real icon instead of an empty `icons: []`.
- **Validator extended and negative-tested.** `srcset`, `imagesrcset` and `data-src`/`data-srcset` candidates are now collected, so responsive or deferred imagery cannot enter a page without provenance; scene derivatives are checked like proof derivatives (fields, existence, byte size, recomputed SHA-256). Both new checks were confirmed to fail the build when deliberately broken. PASS with 0 warnings.
- **WEB-005 hero media budget accepted (MER-92)** and published in `STATUS.md` and the evidence document: WebM ≤ 3.0 MiB, MP4 ≤ 4.5 MiB, poster ≤ 180 KiB, mobile/reduced-data an intentional static/poster fallback with no dual-video download. WEB-005 may tighten these; it may not loosen them without Product re-entry.
- **Two bounded deviations, accepted by Product on MER-92:** homepage LCP remains 3.2 s against the 2.5 s target under the local synthetic profile, the residual being an accepted checksummed proof derivative (`priority-800.webp`, 249.7 KiB) — accepted scientific proof derivatives must not be re-encoded solely to chase 2.5 s; and `image-aspect-ratio` still flags the deliberately squashed score legend (Best Practices 96, above its ≥ 95 floor) — the scientific legend must not be re-proportioned.
- **`HOSTED_PREVIEW_NOT_RUN — permission unavailable`** (no Vercel CLI, link or token on this machine; no credentials requested, no account state touched) with a reproducible local preview command — accepted under the task on MER-92. **`CONTACT_RELEASE_GATE`** remains open for pre-WEB-006 launch verification: every mailto across both languages correctly targets `contact@orbgss.com`, but mailbox ownership cannot be proven without Workspace access.
- No WEB-005 integration, no deployment, no domain or DNS change, no analytics/backend, no framework or dependency added.

## v0.8.1-web-003-review-revision — 2026-09-15 (WEB-003 Product review revision, MER-91, branch `feat/web-003-public-site-depth`)

Bounded conformant fixes from Product review. No redesign, no scope or semantics change.

- **EN/TR accessibility-text parity closed.** `/contact/`'s `aria-label="Contact options"` and `/pilot/`'s `aria-label="Next steps"` were the only two `aria-label` values on any canonical public route not bound to `data-i18n-aria-label` — both now carry it (`contactPage.optionsLabel`, `pilotPage.nextStepsLabel`), so they switch with the page like every other accessible name. `scripts/validate_site.py` now fails the build if any canonical route ever reintroduces an aria-label with no `data-i18n-aria-label` on the same element; verified the check has teeth by reverting each fix locally, confirming the new error, then restoring it.
- **`/pilot/` social preview is now truthful.** Its Open Graph image no longer borrows the homepage's Crater Lake hero photo; it now points at the already-approved, already-checksummed Kızıldere `assets/proof/geothermal-1400.webp` derivative (unmodified — no re-colour, re-crop or re-encode), with `og:image:type` / `:width` / `:height` added for correctness. The validator now rejects the Crater Lake image specifically on `/pilot/` and requires its `og:image` to be a self-hosted `assets/proof/` or `assets/imagery/` asset.
- **Authority/status pointers reconciled.** `docs/WEB_VNEXT_AUTHORITY.md` and `STATUS.md` now read Product & Execution Authority v1.7 and record WEB-003's actual state (implemented, `REVIEW_READY`, MER-91 bounded review revision) instead of the stale "not started" language left over from before CTO approval. No Product/Science semantics changed anywhere in this revision.

## v0.8.0-web-003-public-site-depth — 2026-09-15 (WEB-003, branch `feat/web-003-public-site-depth`)

- published five new public routes as real static directories — `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/` (each `<route>/index.html`, root-relative assets) — completing the public information architecture beyond the homepage;
- `vercel.json` now serves trailing-slash canonical URLs (`trailingSlash: true`) to match the published route model; `sitemap.xml` lists all six canonical routes;
- the homepage and every new route share one persistent header/footer navigation that now routes to these five destinations instead of same-page anchors; the homepage's own WEB-002 section ids, content and hero CTA are untouched, so the accepted evidence-to-intelligence narrative and its provenance/checksums are unchanged;
- `/platform/` explains the accepted workflow (AOI → source/context → evidence → explicit data gaps → integrated priority → investigation decision support) as an editorial numbered list, not a feature grid;
- `/solutions/` presents the three-application portfolio (Geothermal active first application; Mineral and Environmental & Land Intelligence as expansion directions) as an extended ledger, reusing the homepage's own application copy and status labels;
- `/pilot/` reuses the accepted WEB-002 proof imagery and the structure/geology data-gap panel verbatim for Kızıldere — same assets, same checksums, same "no CSS transform on scientific rasters" guard, same mandatory EN/TR warnings — around new explanatory prose, so the first-application story can be read in depth without restating or drifting from the accepted semantics;
- `/company/` and `/contact/` give OrbGSS an actual about/contact destination (operating principles, restrained expansion framing, three mailto conversation starters); no form, backend, analytics or PII capture;
- every route carries truthful route-specific `<title>`, meta description, canonical URL and Open Graph metadata; `aria-current="page"` marks the active nav item; language selection persists coherently across routes via the existing shared `localStorage` key;
- `script.js` gained new EN/TR key pairs for the five routes (plus `mail.pilot` / `mail.technical`), reusing existing homepage keys everywhere the meaning is identical (nav labels, trust list, company copy, mandatory warnings, image captions, coordinates) rather than forking duplicate strings;
- `styles.css` gained a small set of new page-level components (`.page-hero`, `.workflow-list`, `.contact-options`, `.editorial-note`, `.ledger-copy-group`) built from the existing palette and type scale; no new visual system, no card grid;
- validator extended site-wide: every route now gets metadata checks, internal-link and cross-page fragment resolution, sitemap coverage, and an EN/TR parity check across every `data-i18n*` key referenced anywhere on the site; the WEB-002 provenance/checksum/warning checks above it are untouched and stay scoped to `index.html`; PASS with 0 warnings;
- no deploy, DNS, analytics, form backend, or WEB-004/WEB-005/WEB-006 work introduced.

## v0.7.1-web-002-review-revision — 2026-09-15 (WEB-002 Product review revision, branch `feat/web-002-product-proof`)

Bounded conformant fixes from Product review at `854c37f`. No redesign, no scope or semantics change.

- **Scientific rasters are no longer visually transformed.** Removed `saturate(.9) contrast(1.03)` from the story panels and evidence panes and the `opacity:.92` from the score colour ramp, and added an explicit `[data-visual-status="product-proof"] img, .scale-strip>img{filter:none;opacity:1}` guard so a future gallery-grade edit cannot reach proof imagery. The hero keeps its gallery grade.
- **One frame for one ground.** Deleted the six per-slot `object-position` crops left over from WEB-001, when each slot held a different Landsat scene. Every story panel renders the same Kızıldere AOI, so all now use the default centred framing.
- **THM-01 warning semantics restored** in EN, TR and the static HTML: THM-01 is thermal evidence, not geothermal probability, reserve or resource, discovery or drilling-success evidence.
- **Warning coverage is now enforced.** Each proof asset carries a `visible_warning` record naming the i18n key and the exact wording required in each language; the validator checks the term appears in the EN dictionary, the TR dictionary and the static HTML, so a warning cannot silently disappear — including for readers with JavaScript disabled.
- **Caption contrast re-checked** against the new framing; `priority` moved to the dark tone (5.1:1 desktop / 6.4:1 mobile, against 3.7 / 2.9 for white) and the dark halo was tightened so it no longer blooms over mid-tone ground.
- **Stale copy reconciled:** the no-JS footer attribution in `index.html` now matches the dictionary (Landsat hero + WEB-002 cartographic exports); `STATUS.md` moves to Product authority v1.5 and drops the obsolete temporary-gallery / `Natural-color composite` story-panel rules; `IMAGERY_RIGHTS.md` and the `sources.json` policy now state the two asset classes and their different handling rules explicitly.

## v0.7.0-web-002-product-proof — 2026-09-15 (WEB-002, branch `feat/web-002-product-proof`)

- replaced the temporary gallery story panels with real OrbGSS product proof: every panel 01–06 now shows the same Kızıldere pilot AOI (36 × 36 km, EPSG:32635, 30 m) so the reader watches one place gain evidence rather than six unrelated places;
- materialized seven website masters through the accepted GEO-039 Workbench cartographic export path from the persisted `kizildere_mvp_v2` project — `observe`, `terrain`, THM-01, ALT-01, ALT-02, `priority` and the Kızıldere first-application composite — using only the layer selections authorized by `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`;
- `05 Priority` and `06 Geothermal` carry the accepted `mvp_remote_sensing_priority_v1` output from run `8716e893…`, published as **Remote-Sensing Relative Priority — Experimental Baseline** with its 0–100 legend cropped from the same export;
- `03 Evidence` gained a restrained, keyboard-accessible layer switch (THM-01 / ALT-01 / ALT-02) — the page's single interactive moment; each layer's caption travels with its pane so the label can never drift from the raster;
- `04 Structure` is a deliberate data-gap state with no image: no public-safe fault or lithology master is authorized, and the copy says so and records that the gap is score-invariant;
- every proof panel carries its mandatory scientific warning as visible copy in EN and TR;
- `assets/imagery/sources.json` gained `web_002` with, per asset, the export id, `export_manifest.json` pointer, master SHA-256 from that manifest, crop box and a SHA-256 for each shipped derivative; the three Landsat scenes no longer placed on the homepage are marked `retired-from-homepage` with rights intact;
- validator now verifies proof-asset provenance by recomputing every derivative checksum, requires a `data_gaps` record behind any data-gap slot, and rejects overstated score wording outside a mandatory warning; PASS with 0 warnings;
- no raw provider raster, no MTA data, no change to CRS/grid/units/NoData/scoring semantics; WEB-005 hero, WEB-003, deployment and DNS untouched.

## v0.6.0-web-001-vnext-foundation — 2026-09-15 (WEB-001, branch `feat/web-001-vnext-foundation`)

- published the repository-local vNext authority (`docs/WEB_VNEXT_AUTHORITY.md`) and the WEB-001 contract (`tasks/WEB-001_VNEXT_FOUNDATION.md`) before feature code;
- rebuilt the homepage as an evidence-to-intelligence story while keeping the beam → full-width panel gallery rhythm: Hero → 01 Observe → 02 Terrain → 03 Evidence → 04 Structure → 05 Priority → 06 Geothermal → Pilot ledger → Company/Trust → Contact → Footer;
- static poster hero (`Earth data. Evidence. Priority.` / `Know where to look next.` / `Explore the Platform`), built so WEB-005 replaces only the visual layer;
- navigation: Platform / Solutions (Geothermal Exploration, Mineral Exploration, Environmental & Land Intelligence) / Pilot / Company / Contact / EN | TR; all anchors real; disclosure and mobile behaviour unchanged;
- technical beams now carry index, title, statement and a monospace descriptor; scene labels moved to the monospace treatment; story panels add a `Natural-color composite` line;
- pilot ledger marks Geothermal `Active · First application`, Mineral and Environmental & Land `Expansion direction`; company block with restrained trust list; contact beam;
- temporary story visuals reuse the four provenance-safe Landsat composites (marked `data-visual-slot` / `temporary-gallery`; placement recorded in `sources.json`); no scientific outputs fabricated; WEB-002 owns replacements;
- full EN/TR parity for every new string;
- validator extended to the vNext anchors and visual-slot discipline; PASS with 0 warnings.

## v0.5.1-nav-labels-bilingual — 2026-09-09 (ORBWEB-001.1)

- replaced the metadata strips under every satellite image with a bottom-right on-image location + coordinates label (no background container, subtle text-shadow only); sensor/date remain in the manifest and rights documentation;
- rebuilt desktop navigation: right-aligned Home → Solutions (dropdown: Geothermal, Mining, Marine) → About → Partner With Us → EN | TR; Home cyan underline; Partner With Us as a plain item;
- Solutions dropdown as an accessible disclosure: hover, focus and click open; Escape, click-outside and focus-out close; ArrowUp/Down/Home/End move through items; tap-to-expand on mobile;
- added client-side EN/TR bilingual support (`I18N` dictionary in `script.js`): instant switch, scroll preserved, `<html lang>`, title, meta/og descriptions, alt texts and mail subjects update, choice persisted in `localStorage`, English default;
- footer navigation now Home / Solutions / About / Contact; footer is the `#about` anchor;
- design and product authority docs updated so the new decisions are canonical;
- imagery, provenance, pipeline and product claims unchanged; validator PASS with 0 warnings.

## v0.5-production-imagery — 2026-09-09

- populated all four production scenes as self-hosted OrbGSS natural-color composites built from USGS Landsat Collection 2 Level-2 surface reflectance (public domain);
- added `scripts/build_imagery.py` (reproducible crop/stretch/encode pipeline; `--record` writes render provenance into the manifest);
- pinned Landsat product identifiers, crop geometry, stretch parameters and rendered bounds per scene in `assets/imagery/sources.json`;
- removed the remote NASA Earth Observatory fallback dependency (`data-fallback`, preconnect) while keeping graceful image-failure behavior;
- updated footer attribution and `IMAGERY_RIGHTS.md` for the live asset provenance;
- removed `scripts/fetch-imagery.py` (superseded by the build pipeline);
- validator passes with zero warnings.

## v0.4-claude-handoff — 2026-09-09

- added canonical Claude Code bootstrap authority (`CLAUDE.md`);
- added current state pointer (`STATUS.md`);
- documented locked visual direction and product/content boundaries;
- documented Squarespace → Vercel deployment guardrails;
- added bounded continuation tasks;
- added site validator and handoff prompt;
- included visual-direction reference image;
- retained v0.3 page implementation and imagery provenance files.

## v0.3

- locked four visual scene roles and provenance manifest;
- local-first imagery paths with verified prototype fallback URLs;
- imagery rights/provenance documentation.
