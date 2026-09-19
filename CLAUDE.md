# CLAUDE.md — OrbGSS website repository authority

This file is the first authority to read when continuing OrbGSS website work in Claude Code.

## Bootstrap order

Before changing code, read in this order:

1. `STATUS.md`
2. `docs/WEB_VNEXT_AUTHORITY.md` (vNext authority; wins over 3–4 where they disagree)
3. `docs/DESIGN_AUTHORITY.md`
4. `docs/PRODUCT_AND_CONTENT_AUTHORITY.md`
5. `IMAGERY_RIGHTS.md`
6. `assets/imagery/sources.json`
7. the exact task file named by `STATUS.md`

Then inspect `index.html`, `styles.css`, `script.js`, and run the site validator before editing.

Hero production work also reads `hero/README.md` and `hero/config/lane.json`, and is validated by
`py -3.14 hero/scripts/validate_hero.py`. The production satellite pass and the camera are both derived from intents in `hero/config/scene.json` (`orbit_intent` with its `rate_profile`, `shot_intent`); edit the intent and re-derive, never type keyframes. The page-layer handoff is registered to the audited corners of the 36 km analysis frame (`hero/evidence/shot_audit_production.json` → `handoff_anchor` → `data-hero-anchor`); re-run the shot audit and rebind the anchor whenever the camera changes. Blender 4.5 LTS is local production tooling, never a
site runtime dependency.

## Repository intent

This repository contains the public OrbGSS product landing page. It is intentionally a small static site: semantic HTML, CSS and minimal vanilla JavaScript. Do not introduce React, Next.js, Tailwind, a component framework, package manager dependencies, animation libraries or a CMS merely for convenience. A stack migration requires explicit approval.

## Design invariants

These are requirements, not suggestions:

- The page is image-led and extremely restrained.
- Full-width real Earth-observation imagery dominates the page.
- Hero text may overlay the first image; story panels after the hero are clean.
- The homepage has exactly **four major visual acts**, in this order: Act 1 cinematic acquisition hero → Act 2 real Kızıldere EO context → Act 3 compact three-card evidence trio → Act 4 priority/result climax (WEB-005, `docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md`). Supporting pilot-ledger, company/trust and contact sections follow and must stay visually subordinate. The WEB-001/002 six-scene `dark beam → full-width raster` gallery is superseded and must not return; `scripts/validate_site.py` fails if it does.
- Each act owns a different composition on purpose — full-bleed hero, full-bleed natural-colour band (Act 2, WEB-005B), one analytical stage of three aligned squares (Act 3), contained result figure on its own stage (Act 4). Do not collapse them back into one repeated template. Act 3 is the single permitted card-like composition on the whole site: exactly three panels, never a feature grid.
- The dark technical beam grammar survives on the deep routes (`/platform/`, `/pilot/`, …), not as a repeated homepage rhythm.
- Each image carries its location and coordinates directly on the image, bottom-right, as bare monospace text (no card, box, band or background container). The third line names what the layer is: the accepted public label on a product-proof panel, `Natural-color composite` on gallery imagery, and `Rendered orbital sequence — not sensor imagery` on the cinematic hero, which is a render and must always say so. Sensor and acquisition date stay in the manifest and are not shown on the homepage. There is no separate metadata strip below any image. Caption tone (`data-label-tone`) is chosen per panel from the measured luminance under the caption, because the cartographic exports are pale where the satellite photography was dark.
- Every scientific visual is product proof: a real OrbGSS cartographic export of the Kızıldere pilot AOI, materialized through the accepted GEO-039 Workbench export path and recorded in `assets/imagery/sources.json` — under `web_002.proof_assets` (WEB-002), `geo_web_002.assets` (the accepted final master package, still bound by `/pilot/`) or `web_005b.analytical` (WEB-005B: MER-108 website display derivatives of the governed MER-113 rasters, which is what the homepage Acts 3 and 4 now bind — canonical normalization, the frozen hero palette stops, NoData transparent over a neutral hillshade, lossless, never above the native grid, and none of the hero-only transforms). Each carries export id / governed source SHA-256 and per-derivative SHA-256. Never add a scientific visual without that record; the validator recomputes the checksums and the palette LUT.
- No class-B scientific raster may be baked into the hero video, or into any other lossy encode. Lossy compression changes governed colours and values. Ship the accepted derivative as its own checksummed file and composite it in the page.
- Class-B assets have a hard honest-render ceiling on the long axis: **1249 device pixels** for the GEO-WEB-002 exports, and the **native 1200 px** grid for the WEB-005B homepage derivatives (design against 600 CSS px so a 2× display still fits). Answer a bigger presentation with a contained composition, never a stretch — the homepage never upsamples a governed raster, even where MER-108 would permit it for the hero. Each asset records its own ceiling and its placement's measured `rendered` width, and the validator checks the layout against them.
- Structure/geology is a deliberate data gap. No public-safe fault or lithology master is authorized, and the gap is score-invariant. Since WEB-005 it is a short subordinate footnote under Act 3 rather than a full scene. Do not fill it, and do not promote it back into an act.
- The published score is `mvp_remote_sensing_priority_v1`, public label **Remote-Sensing Relative Priority — Experimental Baseline**: a deterministic 0–100 within-AOI screening surface. Never call it probability, Full Prospectivity, a reserve/resource estimate, discovery or drilling-success likelihood, or a cross-AOI calibrated score. Every proof panel carries its mandatory scientific warning as visible EN/TR copy.
- Desktop navigation is right-aligned in exactly this order: Platform → Solutions (dropdown: Geothermal Exploration, Mineral Exploration, Environmental & Land Intelligence) → Pilot → Company → Contact → EN | TR. Every item resolves to a real anchor; no flags in the language switch.
- The homepage is bilingual (English default, Turkish) via the lightweight client-side dictionary in `script.js`. Every new visible string needs both languages.
- No `How it works` section.
- No icon wall, feature-card grid, fake dashboard overlay, HUD chrome or decorative map pins.
- Keep generous horizontal/vertical scale on desktop. The user explicitly wants sections broader in both physical size and visual context.
- The logo orbital mark has no globe in the middle.
- Do not replace the current aesthetic with generic blue-gradient SaaS styling.

If a requested change conflicts with these rules, stop and ask for explicit design approval rather than silently drifting.

## Content / claim discipline

- OrbGSS is a geospatial intelligence / GIS platform with geothermal as the first pilot vertical.
- Mineral and environmental/land intelligence may be presented as solution directions.
- Do not claim a capability, customer, pilot result, AI feature, benchmark, accuracy figure or production integration unless it is explicitly supported by current canonical material supplied by the user.
- Keep copy concise. The design is not intended to explain the entire platform on the landing page.
- Geothermal Exploration is the first active application; Mineral Exploration and Environmental & Land Intelligence are expansion directions and must be labelled as such.

## Imagery policy

- Production imagery must have documented provenance and reuse rights.
- Preferred source: USGS Landsat Collection 2 / OrbGSS-generated composites from public-domain Landsat source data.
- Every production scene must be recorded in `assets/imagery/sources.json`.
- Scientific/product-proof visuals are a separate class: they are OrbGSS cartographic exports produced only through the accepted GEO-039 Workbench export path from a persisted, accepted project. Never copy a raw provider raster into this repository, and never publish paid/closed/restricted data. Derivatives may be cropped and resized for presentation only — no re-colouring, re-projection, re-classification or value change.
- Keep `IMAGERY_RIGHTS.md` current when a source changes.
- Do not add stock-photo satellite imagery or AI-generated satellite imagery to the production site.
- Remote NASA Earth Observatory URLs are prototype fallbacks, not the desired final production dependency.

## Branching

No feature work on `main`. vNext tasks (WEB-001 → WEB-006) land on feature branches and are reviewed before merge. WEB-001 is accepted at `677bfa7`; WEB-002 is accepted (implementation HEAD `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`, merged to `main`); WEB-003 and WEB-004 are accepted; GEO-WEB-002 is Science-accepted at `ea693c29762279131fbed005e832c5ff2dca587b`. WEB-HERO-001D is terminally accepted at evidence HEAD `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e`. WEB-005 / MER-93 (cinematic hero + four-act homepage release candidate) is terminally accepted at `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`. WEB-005A / MER-107 (hero visual fidelity, Product R2 visual lock) is on `feat/web-005a-hero-visual-fidelity` under `tasks/WEB-005A_HERO_VISUAL_FIDELITY.md` and `docs/WEB_005_POLISH_VISUAL_DIRECTION_AUTHORITY.md`; the `ffa2f29` checkpoint was rejected visually, the R2 package (`a689782`, implementation `b285c90`) did not pass the human visual gate, and both are retained as before-evidence; R3 (`37152222`) was reviewed `REVISION_REQUIRED`, went through three low-cost preview gates, and the accepted gate-3 direction is now delivered at final production quality and `REVIEW_READY` under `tasks/WEB-005A_FINAL_PRODUCTION_EVIDENCE.md` (motion video with no analytical pixel + four lossless page-composited drape states; no legend, card or label in the hero); Product accepted it in substance at `e7098de` and the bounded final polish (startup poster = opening frame with a separate held base; lossless relief-rise states between the held frame and Terrain) is `REVIEW_READY` under `tasks/WEB-005A_FINAL_RELIEF_RISE_POLISH_EVIDENCE.md`. WEB-005A is terminally accepted and published at `origin/feat/web-005a-hero-visual-fidelity@1135e7a7e0b0f6db6348dee139d505550d8ca8b9`, which is the baseline every later task branches from. WEB-005B / MER-109 (homepage visual fidelity, Acts 2-4) is on `feat/web-005b-homepage-visual-fidelity` under `tasks/WEB-005B_EVIDENCE.md` and the R1 boundary `docs/web-005-polish-authority@e47da637:tasks/WEB-005B_R1_HOMEPAGE_DESIGN_IMPLEMENTATION_BOUNDARY.md`; it is `REVIEW_READY` and the accepted hero is preserved byte- and pixel-identical. Production DNS cutover is WEB-006 / MER-95 and remains a separate human CTO gate.

## Deployment safety

Target deployment:

- source: Git repository
- hosting: Vercel
- domain registrar/DNS: Squarespace
- public domain: `orbgss.com`

When the custom domain is connected, only change DNS records needed for web hosting. Do not modify Google Workspace MX/SPF/DKIM/DMARC records.

Never create/delete external resources, connect DNS, publish the production domain, or modify the user's email setup unless the user explicitly authorizes that external write.

## Change discipline

For each bounded task:

1. state the task and files expected to change;
2. run `python scripts/validate_site.py` before changes;
3. make the smallest coherent change;
4. run the validator again;
5. preview locally if visual behavior changed;
6. report changed paths, validation result, remaining blockers and the next safe action.

Do not opportunistically redesign unrelated sections.
