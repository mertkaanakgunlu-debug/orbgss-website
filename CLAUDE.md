# CLAUDE.md — OrbGSS website repository authority

This file is the first authority to read when continuing OrbGSS website work in Claude Code.

## Bootstrap order

Before changing code, read in this order:

1. `STATUS.md`
2. `docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md` (MER-255 interior redesign; on its review branch until the CTO accepts it. Where it disagrees with 3 about how the five interior routes are presented — tables, R2 thumbnails, R5/R6 budgets, the sources architecture — it wins; it changes no scientific, legal or claim rule)
3. `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` (Milestone 6, CTO-approved 2026-10-15; wins over 4–6 on pages, navigation, URLs and content rules)
4. `docs/WEB_VNEXT_AUTHORITY.md` (vNext authority; wins over 5–6 where they disagree)
5. `docs/DESIGN_AUTHORITY.md`
6. `docs/PRODUCT_AND_CONTENT_AUTHORITY.md`
7. `IMAGERY_RIGHTS.md`
8. `assets/imagery/sources.json`
9. the exact task file named by `STATUS.md`

Then inspect `index.html`, `styles.css`, `script.js`, and run the site validator before editing.

Hero production work also reads `hero/README.md` and `hero/config/lane.json`, and is validated by
`py -3.14 hero/scripts/validate_hero.py`. The hero validator needs the git-ignored local source textures under `hero/assets/source/`; in a fresh clone exactly 13 checks fail for that reason alone (the accepted result, 420/0, is from the hero workstation). Treat any other failure as real. The production satellite pass and the camera are both derived from intents in `hero/config/scene.json` (`orbit_intent` with its `rate_profile`, `shot_intent`); edit the intent and re-derive, never type keyframes. The page-layer handoff is registered to the audited corners of the 36 km analysis frame (`hero/evidence/shot_audit_production.json` → `handoff_anchor` → `data-hero-anchor`); re-run the shot audit and rebind the anchor whenever the camera changes. Blender 4.5 LTS is local production tooling, never a
site runtime dependency. The delivered hero video is a two-tier WebM + MP4 ladder (1280 and 1920) of the same master frames, built by `hero/scripts/encode_responsive_media.py` with FFmpeg as local tooling (MER-216): the encodes are hash-named because `/assets/` is immutable-cached, MP4s are faststart, the 1920 tier keeps the WebM <= 3.0 MiB / MP4 <= 4.5 MiB envelope, `data-hero-tiers` in the markup must equal the recorded tiers, and `script.js` picks one tier and codec before any video byte and never swaps a source mid-play (enforced by `scripts/validate_site.py` and `scripts/negative_tests_mer216.py`).

## Repository intent

This repository contains the public OrbGSS product landing page. It is intentionally a small static site: semantic HTML, CSS and minimal vanilla JavaScript. Do not introduce React, Next.js, Tailwind, a component framework, package manager dependencies, animation libraries or a CMS merely for convenience. A stack migration requires explicit approval.

## Design invariants

These are requirements, not suggestions:

- The page is image-led and extremely restrained.
- Full-width real Earth-observation imagery dominates the page.
- Hero text may overlay the first image; story panels after the hero are clean.
- The homepage has exactly **four major visual acts**, in this order: Act 1 cinematic acquisition hero → Act 2 real Kızıldere EO context → Act 3 compact three-card evidence trio → Act 4 priority/result climax (WEB-005, `docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md`). After the four acts come the inspection aid, the Solutions cards and one Partner line, all visually subordinate (since MER-240). Method and Company content lives on `/about/`. The WEB-001/002 six-scene `dark beam → full-width raster` gallery is superseded and must not return; `scripts/validate_site.py` fails if it does.
- Each act owns a different composition on purpose — full-bleed hero, full-bleed natural-colour band (Act 2, WEB-005B), one analytical stage of three aligned squares (Act 3), contained result figure on its own stage (Act 4). Do not collapse them back into one repeated template. Act 3 is the single permitted card-like composition on the whole site: exactly three panels, never a feature grid.
- The dark technical grammar survives on `/solutions/geothermal/` (since MER-240), not as a repeated homepage rhythm.
- Each image carries its location and coordinates directly on the image, bottom-right, as bare monospace text (no card, box, band or background container). The third line names what the layer is: the accepted public label on a product-proof panel, `Natural-color composite` on gallery imagery, and `Rendered orbital sequence — not sensor imagery` on the cinematic hero, which is a render and must always say so. Sensor and acquisition date stay in the manifest and are not shown on the homepage. There is no separate metadata strip below any image. Caption tone (`data-label-tone`) is chosen per panel from the measured luminance under the caption, because the cartographic exports are pale where the satellite photography was dark.
- Every scientific visual is product proof: a real OrbGSS cartographic export of the Kızıldere pilot AOI, materialized through the accepted GEO-039 Workbench export path and recorded in `assets/imagery/sources.json` — under `web_002.proof_assets` (WEB-002), `geo_web_002.assets` (the accepted final master package, deployed under `assets/proof/final/`) or `web_005b.analytical` (WEB-005B: presentation derivatives of the governed MER-113 rasters, which is what the homepage Acts 3 and 4 bind). Since R15 those are built by `scripts/build_web005b_presentation.py` under **MER-151 / GEO-WEB-004** (`geothermal-prospectivity@e8aa5d65:tasks/MER-151_GEO-WEB-004_HOMEPAGE_EVIDENCE_PRESENTATION_PARITY_AUTHORITY.md`), which supersedes the MER-108 website profile for these surfaces only: canonical normalization, a BOUNDED display window and one fixed monotonic gamma per layer, the frozen hero palette stops, NoData transparent over a neutral hillshade, lossless. A 4K/HiDPI presentation derivative is allowed (one final RGBA Lanczos3 resize, 0.50–4.00× per axis, 4800 px ceiling, premultiplied and mask-aware) but is currently not published — describe any such file as a "4K presentation derivative generated from the governed analytical raster", never as higher-resolution science: the scientific master stays 1200 × 1200 at 30 m, EPSG:32635. Priority may never be windowed and stays on the fixed 0–100 domain. Each layer carries export id / governed source SHA-256, its window and gamma decision, and per-derivative SHA-256. Never add a scientific visual without that record; the validator recomputes the checksums and the palette LUT and re-checks every MER-151 bound. Since MER-240 retired `/pilot/`, the `web_002.proof_assets` and the `geo_web_002.assets` stay deployed and checksum-checked but are placed on no page; removing them is a separate decision.
- No class-B scientific raster may be baked into the hero video, or into any other lossy encode. Lossy compression changes governed colours and values. Ship the accepted derivative as its own checksummed file and composite it in the page.
- Class-B assets have a hard honest-render ceiling on the long axis: **1249 device pixels** for the GEO-WEB-002 exports, and the **native 1200 px** grid for the WEB-005B homepage derivatives (design against 600 CSS px so a 2× display still fits; MER-151 would permit an enlarged presentation derivative, but none is published, so 600 CSS px remains the cap). Answer a bigger presentation with a contained composition, never a stretch — the homepage never upsamples a governed raster, even where MER-108 would permit it for the hero. Each asset records its own ceiling and its placement's measured `rendered` width, and the validator checks the layout against them.
- Structure/geology is a deliberate data gap. No public-safe fault or lithology master is authorized, and the gap is score-invariant. Since WEB-005 it is a short subordinate footnote under Act 3 rather than a full scene. Do not fill it, and do not promote it back into an act.
- The published score is `mvp_remote_sensing_priority_v1`, public label **Remote-Sensing Relative Priority — Experimental Baseline**: a deterministic 0–100 within-AOI screening surface. Never call it probability, Full Prospectivity, a reserve/resource estimate, discovery or drilling-success likelihood, or a cross-AOI calibrated score. Every proof panel carries its mandatory scientific warning as visible EN/TR copy.
- The public domain taxonomy is exactly **Geothermal / Mining / Marine** (WEB-005C / MER-149), on the homepage, in the navigation and on `/solutions/` alike. The superseded application-ledger labels (Mineral Exploration, Environmental & Land Intelligence) must not return to visible copy. `/solutions/#mineral` and `/solutions/#environment` survive only as compatibility aliases on the renamed rows, and must keep resolving.
- Desktop navigation is right-aligned; every item resolves to a real page or anchor; no flags in the language switch. Order (since MER-240): Home → Solutions (dropdown: Geothermal, Mining, Marine) → About → Partner with us → EN | TR. Geothermal links `/solutions/geothermal/`; Mining and Marine link `/solutions/#mining` and `/solutions/#marine`.
- The three homepage Solutions cards are native links (WEB-005C R2). They navigate without JavaScript and carry no CTA button, arrow or added copy — the card itself is the link. Targets (since MER-240): `/solutions/geothermal/`, `/solutions/#mining`, `/solutions/#marine`. A card shows the image, the domain name and its status label only.
- The site is bilingual (English default, Turkish). Live in production: the lightweight client-side dictionary in `script.js`. Implemented on the MER-241 branch and waiting for acceptance and publication: static Turkish pages under `/tr/` with Turkish slugs, generated from the same dictionary by `scripts/build_tr_pages.py`. Every new visible string needs both languages. **From MER-241 on, `/tr/*`, the Turkish `404.html` line and `sitemap.xml` are generated files: never hand-edit them.** After any change to an English page or to the `I18N` dictionary in `script.js`, run `python3 scripts/build_tr_pages.py` and commit the result; `scripts/validate_site.py` fails when the tree is not byte-identical to the generator's output. The language switch is a pair of real links (EN → the English page, TR → the Turkish one); the site neither redirects by browser language nor stores a language preference.
- No `How it works` section.
- No icon wall, feature-card grid, fake dashboard overlay, HUD chrome or decorative map pins.
- Keep generous horizontal/vertical scale on desktop. The user explicitly wants sections broader in both physical size and visual context.
- The logo orbital mark has no globe in the middle.
- Do not replace the current aesthetic with generic blue-gradient SaaS styling.

If a requested change conflicts with these rules, stop and ask for explicit design approval rather than silently drifting.

## Milestone 6 target (approved MER-238, 2026-10-15)

The CTO approved `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` (mockups `docs/mockups/m6/`). It is the authority for MER-240 (English pages) and MER-241 (static `/tr/`). Where a "live" invariant above and the target differ, the live one describes production until the task that implements the target is accepted and published. From then on, the target is the invariant.

MER-240 implemented the English target. It was independently accepted at `a2045344` and published on 2026-10-16, so the English pages, navigation, redirects and homepage trim below are now the live invariants (`tasks/MER-240_EVIDENCE.md`, §8 for the publication). `scripts/validate_site.py` enforces the page set, the navigation, the redirects, the homepage trim and rules R1–R5 and R8, and `scripts/negative_tests_mer240.py` proves each check fires. Three parts of the target wait: the Geothermal page's G3 / G4 figures and the layer-table thumbnails (MER-242; the MER-151 derivatives are authorized for the homepage only), the coastal Marine scene (D5), and `/tr/` (MER-241: implemented on `claude/mer-241-turkish-static-pages-sihwiy`, `REVIEW_READY`, not published; `tasks/MER-241_EVIDENCE.md`).

- **Pages:** `/` (the four acts and the inspection aid unchanged), `/solutions/` (a hub with a comparison table and a full-bleed band per domain; `#mining` and `#marine` keep the `#mineral` / `#environment` aliases), `/solutions/geothermal/` (the Kızıldere reference sheet that replaces `/pilot/`), `/about/` (principles and data sources; no team, address or legal-entity details), `/partner/` (Partner with us: conversation table plus email; no form, backend, CRM, analytics or cookies).
- **Redirects:** 301 `/platform/` → `/`, `/pilot/` → `/solutions/geothermal/`, `/company/` → `/about/`, `/contact/` → `/partner/`. The old `#pilot-*` anchors survive as aliases on the Geothermal page.
- **Turkish URLs:** `/tr/`, `/tr/cozumler/`, `/tr/cozumler/jeotermal/`, `/tr/hakkimizda/`, `/tr/is-birligi/`. Anchor ids are identical in both languages. Generated by `scripts/build_tr_pages.py` (MER-241); `/tr/` is in the `.vercelignore` allowlist; `scripts/negative_tests_mer241.py` proves the language checks in `scripts/validate_site.py` fire.
- **Homepage changes:** Method and Company leave the homepage for `/about/`; Contact becomes one "Partner with us →" line; the homepage carries no `mailto:` of its own; the Act 3 / Act 4 links into `/pilot/` point to the Geothermal page.
- **Content rules (apply to every page built or changed from MER-240 on):**
  - **R1** — every fact has exactly one home page; elsewhere it is only linked.
  - **R2** — a visual appears full-size on one page; elsewhere only as a thumbnail of at most 160 CSS px inside an index table or a linking card.
  - **R3** — no software or development content: no workflow steps, pipelines, tooling, file formats or export paths. Geospatial facts live once, in the Geothermal facts table.
  - **R4** — every content section opens with its lead visual (image, map, chart or table).
  - **R5** — budgets (EN; TR may run 15 % longer): headline 8 words, page intro 30, section body 40, table cell 12, at most 7 rows per table; at most 250 budgeted words per page (Geothermal 350).
  - **R6** — mandatory scientific warnings, the illustrative-imagery footnote, captions, status labels, the footer attribution are fixed texts, exempt from R1 and R5.
  - **R7** — claim discipline unchanged.
  - **R8** — Mining and Marine are labelled "Expansion direction" / "Genişleme yönü" everywhere.

  Tables are show-first elements, not cards; Act 3 and the Solutions cards remain the only card-like compositions.
- **Decisions:**
  - **Decided:**
    - D1: the Geothermal page's priority-over-relief and ALT-02 figures use only MER-151-family derivatives from Science (MER-242). Until then they are left out, and the layer table says "Accepted, not shown yet".
    - D2: Turkish slugs.
    - D4: `contact@orbgss.com` receives external mail (CTO test, 2026-10-16), which closed the MER-240 ship gate. The test mail landed in spam; a Gmail "never send to spam" filter is the CTO's action.
  - **Open:**
    - D3: privacy / KVKK page, a legal call.
    - D5: a coastal Marine scene to replace the inland Ili Delta.

## Interior redesign (MER-255, pending the CTO's acceptance)

`docs/WEB_INTERIOR_REDESIGN_AUTHORITY.md` rebuilds the five interior routes. Once the CTO accepts and publishes it, these are invariants; until then the Milestone 6 text above describes production.

- **One grammar, five openings.** The interior routes carry `<body class="interior">`; the homepage never does. Each page opens differently: Solutions a state ledger, Geothermal a wide Kızıldere strip, About the orbital motif, Partner a split with one photograph, Sources a register. Do not collapse them back into one template.
- **No tables on the interior routes.** Comparison and reference content is a ruled list, a numbered list or a record; the 12-word cell budget now holds every line of a `lead-set`. The validator fails on any `<table>` there.
- **Interior photographs are four recorded Class A crops** of the Act 2 master (`web_m6.interior_crops`, `scripts/build_interior_crops.py`), each shown full size on one page, none drawn above its own pixels (CSS caps plus the browser measurement of `scripts/measure_interior_renders.py`, bound 1.01).
- **Geothermal shows no governed derivative.** MER-151 / GEO-WEB-002 rasters stay homepage-only until MER-242; the layer diagram is a captioned schematic of empty frames and the 0–100 ruler is neutral. Do not fill a gap with a picture.
- **A caption names ground the image shows.** The coordinates printed on a crop are its `label_point` in `web_m6.interior_crops`: the declared pilot centre where the crop contains it (stage, aoi), otherwise the crop's own centre (terrain, valley, with their own place lines "East of / South-west of the Kızıldere pilot area"). `scripts/geo_frame.py` projects them onto the master's grid and the validator fails when a caption lies outside its crop. Never reuse the pilot's coordinates on a crop that does not show them.
- **Mining and Marine on `/solutions/` are captioned photographs, not cards** (authority §2, "CLAUDE.md card rule — Clarified, not loosened"). The "single permitted card-like composition" rule still stands: a card is a bordered or filled container, an equal-weight grid cell or a link target. The validator holds the expansion figures to no frame, no link and no grid.
- **Attribution has its own page.** `/sources/` (TR `/tr/kaynaklar/`) holds every source, credit line, image credit, reference DOI and licence (the Scientific colour maps MIT permission and warranty text, standard wording, English in both languages); the footer carries the Landsat and Copernicus credits and the link to it; About keeps a short trust note under `#sources`. Keep it complete when a source changes, and keep `IMAGERY_RIGHTS.md` current.
- **The Scientific colour maps copyright line carries no year** ("Copyright (c) Fabio Crameri") because no reachable source states the year of the v8.0 release file; `web_m6.licence_notices` records that, and the validator fails on a year without a recorded `year_verified_from`. Taking the exact notice from the release file is the CTO's call. Never invent a year or a holder line.
- Checks: `scripts/validate_site.py` and `scripts/negative_tests_mer255.py` (run the negative suites one at a time, never in parallel; they mutate the working tree).

## Content / claim discipline

- OrbGSS is a geospatial intelligence / GIS platform with geothermal as the first pilot vertical.
- Mining and marine may be presented as solution directions.
- Do not claim a capability, customer, pilot result, AI feature, benchmark, accuracy figure or production integration unless it is explicitly supported by current canonical material supplied by the user.
- Keep copy concise. The design is not intended to explain the entire platform on the landing page.
- **Brand (CTO decision, 2026-10-17):** the public site names only **OrbGSS** (expanded name "Orbital Geo-Spatial Solutions" stays in the logo tagline and the About title). It never names VirgaSoft, in any language, spelling or file, and it does not publish the planned legal name or any legal-entity text. `scripts/validate_site.py` scans every deployed file for the former parent brand and `scripts/negative_tests_mer241.py` proves it. Internal records, provenance files and Vercel / hosting identifiers (the `virga-soft` team in deployment hostnames) are not site content and stay as they are.
- Geothermal is the first active application; Mining and Marine are expansion directions and must be labelled as such.

## Imagery policy

- Production imagery must have documented provenance and reuse rights.
- Preferred source: USGS Landsat Collection 2 / OrbGSS-generated composites from public-domain Landsat source data.
- Every production scene must be recorded in `assets/imagery/sources.json`.
- Scientific/product-proof visuals are a separate class: they are OrbGSS cartographic exports produced only through the accepted GEO-039 Workbench export path from a persisted, accepted project. Never copy a raw provider raster into this repository, and never publish paid/closed/restricted data. Derivatives may be cropped and resized for presentation only — no re-colouring, re-projection, re-classification or value change.
- Keep `IMAGERY_RIGHTS.md` current when a source changes.
- Do not add stock-photo satellite imagery or AI-generated satellite imagery to the production site.
- Remote NASA Earth Observatory URLs are prototype fallbacks, not the desired final production dependency.

## Branching

No feature work on `main`. Every task lands on a bounded branch for its own Linear issue and is reviewed before anything is merged.

Current baseline (updated after the MER-240 publication, 2026-10-17; the day-to-day detail is in `STATUS.md`):

- **Git `main` = production:** the MER-240 English Milestone 6 pages, `a2045344f4cc70fe189160ffd7254fe61020cad9`, published 2026-10-16 by a CTO-authorized non-force fast-forward `464a7354` → `a2045344`, plus a docs-only records commit on top of it that changes no deployed file. Before that: the launched code (`79cc2cb`, WEB-005C) plus MER-216, MER-218, MER-237 and MER-239, published 2026-10-15 as `f4f1d4d6` → `2517369e` → `464a7354` (MER-219).
- **Production topology:** Vercel project `orbgss-website`, team `virga-soft`. The Git integration deploys `main` to production automatically (**COUPLED**), so a push to `main` *is* a production deployment. Every other pushed branch gets a protected Preview. The current production deployment, rollback target and smoke tooling are in `STATUS.md` and `tasks/MER-219_PREFLIGHT.md`.
- **Where new work branches from:** the exact baseline its Linear issue names, verified by fetch. Normally that is `main`.
- **Earlier accepted heads, for provenance only:** WEB-001 `677bfa7`; WEB-002 `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`; WEB-003 `3670d43`; WEB-004 `56cb53039b85a852110c737505bc2ae2282acb08`; GEO-WEB-002 `ea693c29762279131fbed005e832c5ff2dca587b`; WEB-HERO-001D `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e`; WEB-005 terminal acceptance `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`; WEB-005A `1135e7a7e0b0f6db6348dee139d505550d8ca8b9`; launched code baseline WEB-005C `feat/web-005c-public-domain-taxonomy-parity@79cc2cb82a4542461cbbfc1d0c349cf02b861084`; MER-213 `f4f1d4d6`; MER-216 `adf08186`; MER-218 `5ca7bdd4`; MER-237 `2517369e`; MER-239 `464a7354`; MER-240 `a2045344`.
- **Gates:** updating `main` (a production deployment, given the topology), any other production deployment, and DNS are separate CTO-authorized gates. An auto-created session branch (for example `claude/...`) is workspace plumbing, not canonical state.

## Task execution rule

`MER-###'e başla` means: execute that exact Linear issue, and only its scope.

1. Resolve the issue from Linear by ID; read its description, status, dependencies and project position. If Linear cannot be read, stop and report the environment blocker.
2. Fetch Git; verify the repository identity, `origin`, a clean working tree, `main`, and the exact baseline the issue names. If Linear, Git and this repository disagree, stop and report the conflict instead of guessing.
3. Create or use a bounded branch for the issue from that exact baseline.
4. Implement only the issue scope. Run the acceptance the issue and this repository require (see Change discipline), review the exact diff, then commit and push the branch.
5. Report the branch, HEAD SHA, baseline SHA, changed files, verification, remote/local HEAD match and remaining risks, and stop at `REVIEW_READY`.
6. Never merge or fast-forward `main`, deploy, change DNS, credentials or Vercel configuration, force-push or rewrite history, close the Linear issue, or grant the work its own acceptance. The CTO/Product review does that.

## Deployment safety

Target deployment:

- source: Git repository
- hosting: Vercel
- domain registrar/DNS: Squarespace
- public domain: `orbgss.com`

Publishing follows `tasks/MER-219_PREFLIGHT.md` §5: guard, non-force fast-forward, watch the production deployment, then run `evidence/mer219/smoke_production.py --expect-sha <sha>` and `evidence/mer219/browser_checks_production.py`. Rollback is Instant Rollback in the Vercel dashboard (§4). Task-execution rule 6 stands: an agent never fast-forwards `main` on its own. In MER-219, and again for MER-240 and its records commit, the CTO explicitly authorized the agent, in the conversation, to run one reviewed publication. Each authorization covers only that publication.

Only the public site is deployed (MER-237). `.vercelignore` is a root allowlist: `/*` first, then one `!<entry>` line per public root file or directory. A new public page or top-level file must be added there or it will not be deployed; `scripts/validate_site.py` fails when anything a public page, stylesheet, manifest, sitemap or robots.txt references falls outside the allowlist, when an internal path (`STATUS.md`, `CLAUDE.md`, `docs/`, `tasks/`, `evidence/`, `scripts/`, `hero/`, `references/` …) is let back in, when documentation or tooling sits inside a deployed directory, or when a route's `og:image` is not a deployed image some page shows.

When the custom domain is connected, only change DNS records needed for web hosting. Do not modify Google Workspace MX/SPF/DKIM/DMARC records.

Never create/delete external resources, connect DNS, publish the production domain, or modify the user's email setup unless the user explicitly authorizes that external write.

## Change discipline

For each bounded task:

1. state the task and files expected to change;
2. run `python scripts/validate_site.py` before changes;
3. make the smallest coherent change (after editing an English page or the `I18N` dictionary, regenerate `/tr/` with `python3 scripts/build_tr_pages.py`);
4. run the validator again (and `python3 scripts/negative_tests_mer241.py` when a language check is touched);
5. preview locally if visual behavior changed;
6. report changed paths, validation result, remaining blockers and the next safe action.

Do not opportunistically redesign unrelated sections.
