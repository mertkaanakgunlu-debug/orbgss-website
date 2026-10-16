# OrbGSS Website — CURRENT

**Published:** `main@464a73543a440f7d51a1600599998e97b53e982f`, live on orbgss.com since 2026-10-15 22:24 UTC. It is the launched WEB-005C baseline (`v1.0.0-rc10-web-005c`, code `79cc2cb`) plus MER-216 (media fidelity and runtime hardening), MER-237 (only the public site is deployed) and the MER-239 documentation reconciliation.
**Date:** 2026-10-16 (MER-240)
**Stage:** Milestone 6 — information architecture and show-first pages. The English pages (MER-240) are `REVIEW_READY` on their branch and not published. Milestone 5 (post-launch audit, media fidelity and runtime hardening) is complete and published.

## Current state (2026-10-16, MER-240)

| Item | Value |
| --- | --- |
| Repository | `mertkaanakgunlu-debug/orbgss-website`. **Public on GitHub**, so everything committed here, `docs/`, `tasks/` and `evidence/` included, is world-readable there even though orbgss.com does not serve it (open decision 5). The legacy `baran-orbgss/website` is reference / upstream only. |
| GitHub `main` | `464a73543a440f7d51a1600599998e97b53e982f`. History: `f4f1d4d6` (MER-213 docs over the launched code `79cc2cb`) → `adf08186` (MER-216) → `5ca7bdd4` (MER-218 closure) → `2517369e` (MER-237; published 2026-10-15T13:45:21Z, MER-219 §9) → `464a7354` (MER-219 records, the MER-238 merge and MER-239; published 2026-10-15T22:24:13Z). Both publications were CTO-authorized non-force fast-forwards. |
| Production | Vercel project `orbgss-website`, team `virga-soft`. The Git integration deploys `main` to production automatically (**COUPLED**: a push to `main` *is* a production deploy) and builds a protected Preview for every other branch. Current production: GitHub deployment `7105858029` → `orbgss-website-29bzudvea-virga-soft.vercel.app`, serving `464a7354` (smoke 46/46). Domains: `orbgss.com` (canonical apex, HSTS), `www` → apex 308, `orbgss-website.vercel.app`. |
| Rollback target | The previous production deployment `orbgss-website-l0hjfxcdh-virga-soft.vercel.app` (`2517369e`; site files identical apart from the `sources.json` metadata), by Instant Rollback in the Vercel dashboard. A rollback switches off automatic domain assignment until "Undo Rollback" (`tasks/MER-219_PREFLIGHT.md` §4). |
| Deploy set | `.vercelignore` root allowlist (MER-237): only the public site is uploaded and served. Internal paths return 404 in production (verified). |
| Agent access to Vercel | The Vercel connector in Claude is signed in as the CTO's account, but its OAuth grant covers 0 teams, so agents cannot read `virga-soft`. Production state is read through GitHub deployment records, public HTTP, and dashboard reads the CTO provides. |
| Task branches | MER-240 `mertkaanakgunlu/mer-240-web-sitesi-yeni-sayfalarin-uygulanmasi-en`, from `main@464a7354`: the English Milestone 6 pages, `REVIEW_READY` (head SHA in the Linear issue and `tasks/MER-240_EVIDENCE.md`). Published task branches are history. New work branches from the exact baseline its Linear issue names, verified by fetch. |

**Live product (production, `main@464a7354`; MER-240 changes it only when published):**

* **Page flow:** hero (rendered orbital sequence, a two-tier WebM/MP4 ladder chosen once before any video byte, held frame and page-composited drape states; caption `Rendered orbital sequence — not sensor imagery`) → Act 02 real Kızıldere Landsat context → Act 03 three evidence layers over one frame → Act 04 priority result → co-registered inspection aid → Solutions cards → Method → Company → Contact.
* **Routes:** `/`, `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/` (+ `404.html`).
* **Navigation:** Platform → Solutions (Geothermal, Mining, Marine) → Pilot → Company → Contact → EN | TR.
* **Stack:** static HTML, CSS and vanilla JS; no package manager.

**On the MER-240 branch (the approved MER-238 target, English):**

* **Routes:** `/`, `/solutions/`, `/solutions/geothermal/`, `/about/`, `/partner/` (+ `404.html` with the new navigation). `/platform/`, `/pilot/`, `/company/` and `/contact/` answer with a 301 (`vercel.json`) to `/`, `/solutions/geothermal/`, `/about/` and `/partner/`; the old `#pilot-*` fragments land on the Geothermal page.
* **Navigation:** Home → Solutions (Geothermal, Mining, Marine) → About → Partner with us → EN | TR, on every page and in the footer.
* **Homepage:** the four acts and the inspection aid unchanged. Method and Company moved to `/about/`, Contact is one Partner line, the cards show image, name and status only ("Expansion direction" for Mining and Marine), and the homepage carries no `mailto:`.
* **Not in this change:** the Geothermal page's G3 (priority over relief) and G4 (iron proxy) and the layer-table thumbnails wait for MER-242 (MER-151 derivatives are authorized for the homepage only). Marine keeps the Ili Delta (D5 deferred). Static `/tr/` is MER-241.

The authority is `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md`. `CLAUDE.md` § "Milestone 6 target" states how the live invariants hand over to it once MER-240 is accepted and published.

## Milestone 6 — Bilgi Mimarisi ve Gösterim Odaklı Sayfalar (Linear)

| Issue | State on 2026-10-16 |
| --- | --- |
| MER-237 — internal files off the live site; route-wide og images | Accepted by the CTO; published in `2517369e`. Evidence `tasks/MER-237_EVIDENCE.md`. |
| MER-219 — publication and production preflight | Publications of `2517369e` and `464a7354` executed with CTO authorization. Record in `tasks/MER-219_PREFLIGHT.md` §9 and `evidence/mer219/`. |
| MER-238 — IA and page-content authority | Approved by the CTO, with D1 (Science derivatives, MER-242) and D2 (Turkish slugs) decided; D3 (privacy / KVKK, legal), D4 (`contact@orbgss.com` deliverability) and D5 (coastal Marine scene) open. Evidence `tasks/MER-238_EVIDENCE.md`. |
| MER-239 — documentation and authority reconciliation | Accepted by the CTO; published in `464a7354`. Evidence `tasks/MER-239_EVIDENCE.md`. |
| MER-240 — new pages (EN) | `REVIEW_READY` on its branch, not published. D4 is a ship gate. Evidence `tasks/MER-240_EVIDENCE.md`. |
| MER-241 — static `/tr/` pages | After MER-240. |
| MER-242 — Science: MER-151-family derivatives for priority over relief, ALT-02 and the layer-table thumbnails | Geothermal Domain project; the Geothermal page leaves those figures and thumbnails out until it is accepted. |

Linear closure is the CTO's action. Agents record acceptance comments and never close issues.

## MER-216 — media fidelity and runtime hardening (Done — accepted 2026-10-03; published 2026-10-15)

Independently accepted on Linear on 2026-10-03 at `claude/mer-216-s1r628@adf08186d3ee4a438bda73886272d05c970e670a`; published in `main@2517369e` on 2026-10-15 (MER-219). Residual, non-blocking items recorded by the reviewer: no physical Safari / Firefox / phone / 4K-panel acceptance, and production Vercel behaviour was not exercised (it was on 2026-10-15: MER-219 §9). The section below is the state at its handoff.

One bounded branch, `claude/mer-216-s1r628`, created from the verified `origin/main@f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85` and executed on the CTO workstation (the governed Kızıldere export `20260917T161155Z-5e7a0e53` and the 276-frame hero master live there). Nothing was merged to `main`, deployed, or changed in DNS / Vercel / credentials. Full evidence and the reviewer's decision list: `tasks/MER-216_EVIDENCE.md`, `evidence/mer216/`, `hero/evidence/responsive_media.json`.

| Phase | Outcome |
| --- | --- |
| 1 analytical fidelity | `PASS`. The published Act 3 / 4 / inspection derivatives rebuild byte for byte from the governed rasters (4 / 4 SHA-256 match), an independent re-derivation matches every pixel, NoData is pure neutral hillshade, and measured device-pixel demand (max 1196 px) is served by the native 1200 px grid. No new derivative family and no 4K enlargement was warranted; nothing analytical changed |
| 2 hero media | `PASS`. The single 1920 WebM / MP4 pair is replaced by a two-tier ladder (1280 and 1920, WebM + MP4) of the same 276 master frames: 1920 WebM 2.79 MiB VMAF 95.6 (was 2.83 MiB / 89.5), 1920 MP4 3.42 MiB / 95.2 (was 4.05 MiB / 90.3) with `moov` first (1 request, was 3); 1280 tier 1.57 / 1.97 MiB. WEB-004 / WEB-005 envelope kept. A 2304 tier was built, measured (+1 VMAF) and not published |
| 3 integration | `PASS`. `script.js` chooses one tier and codec before any video byte (frame demand x DPR, `downlink`, `mediaCapabilities`), shows the video only after a presented frame, and ends in the held still on stalls, dropped frames, a decoder that paints nothing, errors or refused autoplay. Analytical `sizes` re-fit and Act 03 predecode were measured and **not** shipped (no gain) |
| 4 browser acceptance | `PASS`. 10 viewport / DPR classes (375 @3x to 3840 @1x, three 4K scaling modes) x 7 routes: 0 overflow, 0 broken images, 0 console errors, homepage CLS 0, image bytes unchanged, hero bytes -44 % on 1280-class screens; EN / TR, reduced motion, no-JS, nav, evidence radios and the wipe verified. Emulated devices only (no physical phone or 4K panel) |

Validators on this branch: `validate_site.py` PASS (0 warnings); `validate_hero.py` 420 / 0 (hero workstation); negatives 72 / 72, 55 / 55, 18 / 18 and the new `negative_tests_mer216.py` 16 / 16 at the first reviewed head, 19 / 19 after the review revision (`tasks/MER-216_EVIDENCE.md` §5a). `hero/config/lane.json` names MER-216 as the integration gate for the hero ladder.

## Task execution contract (`MER-###'e başla`)

The short command `MER-###'e başla` authorizes exactly that Linear issue, in this order: resolve the issue from Linear → read its status, dependencies and project position → fetch Git and verify a clean tree, `origin`, `main` and the baseline the issue names → stop and report if Linear, Git and this repository disagree → create or use a bounded branch for the issue from the exact baseline → implement only the issue scope → run the acceptance the issue and this repository require → review the diff → commit and push the branch → report branch, HEAD, baseline, changed files, verification and remote/local HEAD match → stop at `REVIEW_READY`. The agent never merges or fast-forwards `main`, deploys, changes DNS, credentials or Vercel configuration, force-pushes, or closes its own issue; those are separate CTO-authorized gates. The auto-created session branch is plumbing, not canonical state.

## Validators (MER-240 branch, run 2026-10-16)

| Command | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | PASS, 0 warnings (4 scenes, 5 routes + `404.html`, 277 i18n keys, 6 geo-web-002 assets / 19 files, deploy set 12 root entries). Since MER-240 it also enforces the Milestone 6 navigation, redirects, homepage trim, the locator-map record and content rules R1–R5 and R8. |
| `negative_tests_web005.py` / `_web005b.py` / `_web005c.py` / `_mer216.py` / `_mer237.py` / `_mer240.py` | 72/72, 55/55, 18/18, 19/19, 29/29, 45/45 caught; restored trees identical. The web005b, web005c and mer237 cases that mutated the retired routes now mutate their successors (`tasks/MER-240_EVIDENCE.md` §5). |
| `py -3.14 hero/scripts/validate_hero.py` | 420 / 0 on the hero workstation; in a fresh clone exactly the 13 git-ignored source-texture checks fail and nothing else |
| `evidence/mer219/smoke_production.py --expect-sha 464a7354…` | 46/46 against production (2026-10-15). Since MER-240 the script expects the new routes and the four redirects, so it is for use after MER-240 is published. |

## Open gates and decisions

1. **MER-240 publication:** a CTO-authorized fast-forward of `main` to the reviewed MER-240 head (a production deployment, given the topology). Not done.
2. **`CONTACT_RELEASE_GATE` (MER-238 D4):** mailbox ownership and deliverability of `contact@orbgss.com` are not evidenced in this repository. A ship gate for MER-240: the CTO confirms the mailbox receives external mail.
3. **Redirect behaviour on Vercel:** the four 301s are configured in `vercel.json` and validated statically. Their live behaviour (including the `trailingSlash` hop for the slash-less forms) is first observable on the branch Preview (protected) or after publication, where `evidence/mer219/smoke_production.py` checks it.
4. **Production record:** recorded (MER-219: project, team, topology, deployments, rollback target). The WEB-006 DNS execution itself is still not recorded here; its observable result is (apex served by Vercel, `www` → apex 308, HSTS).
5. **Public repository:** whether `orbgss-website` should be private is a CTO decision. Vercel can deploy a private repository; the plan and permissions question is open.
6. **Agent access to Vercel:** the connector's OAuth grant has no team access. Until the CTO grants `virga-soft`, Vercel state comes from GitHub, HTTP and the CTO.
7. **Open MER-238 decisions:** D3 privacy / KVKK (legal), D5 coastal Marine scene.

## Superseded pre-launch status (kept as history)

The text below was the status before the launch and before MER-213. The WEB-005B/005C revision notes marked `(history)` and every later section describe earlier states; where they disagree with the sections above, the sections above win.

**Previous stage text (WEB-005B R3, superseded):**

WEB-005B / MER-109 is `REVIEW_READY` at **R14** (see the R11 block below; the R3 text that follows is the superseded previous state). WEB-005A / MER-107 is **terminally accepted and published**: the visually approved checkpoint `1135e7a7e0b0f6db6348dee139d505550d8ca8b9` was fast-forwarded to `origin/feat/web-005a-hero-visual-fidelity` (remote HEAD verified) with site PASS and hero 420/0 on the accepted bytes. **WEB-005B / MER-109 (homepage visual fidelity, Acts 2-4) is `REVIEW_READY` after the R3 delivery pass** (`docs/web-005-polish-authority@4683bd3:tasks/WEB-005B_R3_REVIEW_AND_DELIVERY_OPTIMIZATION.md`): the Acts 3-4 panels gained visually-lossless lossy WebP delivery candidates where they earn it and keep their lossless derivative as the reference. Only Terrain qualified (q98, -84.6 / -82.2 / -79.5 %, PSNR 46.6-47.7 dB, NoData untouched); THM-01, ALT-01 and priority stay lossless because their per-pixel structure and mask boundaries cannot survive a block transform (priority at the best rung is PSNR 23.8 dB). Package 9.93 -> 8.68 MiB. Act 2, the hero and all copy are unchanged in that pass, and it also fixed a latent hero-lane write-surface failure left by the R1 commit. It was on `feat/web-005b-homepage-visual-fidelity`, branched from that exact commit, under `docs/web-005-polish-authority@e47da637:tasks/WEB-005B_R1_HOMEPAGE_DESIGN_IMPLEMENTATION_BOUNDARY.md`; evidence is `tasks/WEB-005B_EVIDENCE.md` and `evidence/web005b/`. Act 2 is a full-bleed natural-colour Landsat band (same USGS product, re-cropped wider at native 30 m to 3200 x 1800 px and tone-rendered on one common reflectance scale, with the true 36 km AOI marked); Act 3 is one analytical stage of three aligned squares; Act 4 is the priority result alone on its own stage at 600 CSS px, 2.2x the area of any evidence panel, with its own LUT as a coupled legend. Acts 3 and 4 now ship **MER-108 website display derivatives** of the governed MER-113 rasters (`11c32e8d` section 10 names WEB-005B as a consumer), so the page reads as one palette system from the hero payoff to the result; recomputing the priority layer reproduces the CTO-approved `priority_webhero_v1` raster exactly. The GEO-WEB-002 exports stay published for `/pilot/`. Gates: site PASS, hero 420/0, WEB-005 negatives 71/71, new WEB-005B negatives 24/24, copy preservation clean apart from two declared accessibility/legend additions, accepted hero byte- and pixel-identical, other routes unchanged. Not merged, nothing deployed, no DNS touched. *History of the hero revision follows.*
**R11 (history):** the CTO-accepted final Claude Design homepage is implemented on
`feat/web-005b-homepage-visual-fidelity`, branched from the verified remote head `176e345`, under
`docs/web-005-polish-authority@1334e757:tasks/WEB-005B_R11_CLAUDE_DESKTOP_IMPLEMENTATION_HANDOFF.md`
and the R10 continuity contract `@4051c28f`. Evidence: `tasks/WEB-005B_R11_IMPLEMENTATION_EVIDENCE.md`
and `evidence/web005b_r11/`. The post-hero page is rebuilt to the accepted composition — Act 02 as one
contained photograph with integrated copy, Act 03 as ONE shared geographic frame read through three
cross-faded layers (the three-equal-card gallery is gone), Act 04 centred with a four-part definition
structure, the accepted inspection aid in its own section between the result and the domains, image-led
domains with Geothermal leading, a six-cell method grid, and a quiet centred contact ending. The three
continuity defects R10 named are fixed: the header plus hero own the first viewport exactly
(`calc(100svh - var(--header-h))`, measured leak-free at 19 widths x DPR 1 and 2), the whole post-hero
story including the footer sits on one governing background token, and the act handoffs are spacing,
hairlines and gradients rather than full-width colour changes. The hero markup is byte-identical; only
the box it is drawn in changed. Copy: 62 new EN/TR keys, no canonical visible copy removed, no metric,
accuracy, customer or ROI claim introduced. Science: no WEB-007..010 work, no reprocessing, every
Act 3/4 pixel is the same recorded MER-108 derivative; the only new assets are responsive WebP
derivatives of the three illustrative class-A domain photographs. Deviations from the prototype are
listed in section 3 of the evidence document — the domain names stay canonical
(Mineral Exploration / Environmental & Land Intelligence, not "Mining"/"Marine"), mobile Act 02 puts
its copy below the photograph, and the inspection aid is genuinely co-registered against the recorded
analysis grid rather than "approximate common framing".

**R13 (history):** Product reviewed the R11 implementation, accepted it for final visual review and
issued one mandatory correction, now implemented
(`docs/web-005-polish-authority@ba8d99b8:tasks/WEB-005B_R13_IMPLEMENTATION_REVIEW_DOMAIN_REVISION.md`).
The homepage domain taxonomy is **Geothermal / Mining / Marine** — R11's substitution of Mineral
Exploration and Environmental & Land Intelligence is not accepted, and an existing route anchor is not
authority to rename a published domain. Homepage anchors are now `#geothermal` / `#mining` / `#marine`;
Mining and Marine are labelled `In development` and no card navigates, because neither has a
production-ready destination route and the accepted design gives the cards no link. The module carries
its own `domain.*` strings: the `app.*` keys are published by `/solutions/` too, and this revision is
homepage-only, so `/solutions/` is untouched and still publishes the application-ledger vocabulary under
`#geothermal` / `#mineral` / `#environment`, which every nav link still resolves to. **That divergence
between the homepage and `/solutions/` taxonomies is now visitor-visible and wants a follow-up task.**
Two coupled defects were also fixed: the eleven R11 domain derivatives are now declared on
`hero/config/lane.json`'s integration write surface (the lane check only sees a path once it is tracked,
so the R11 gate passed while they were untracked and `validate_hero.py` started failing straight after
the commit), and the half-width domain cards now clear their own caption vertically instead of running
77-144 px into it. Evidence refreshed in place: `tasks/WEB-005B_R11_IMPLEMENTATION_EVIDENCE.md` section 0
and `evidence/web005b_r11/`. Nothing else changed — hero, Acts 02/03/04, the inspection aid, Company and
Contact are all as accepted at R11.

**R14 (history):** bounded polish pass on the accepted direction - no redesign, structure and
section order unchanged. (A) The domains section is now **Solutions** (`#solutions`), the "Geothermal
first" pilot framing is gone, and all three cards share one composition; their per-card
location/coordinate captions were removed at Product instruction, which makes the section footnote the
sole carrier of "these are other places, not OrbGSS results" - so the validator now enforces that
footnote's wording in both languages. (B) The evidence UI is de-technicalized: `THM-01`, `ALT-01` and
`clay/hydroxyl` appear nowhere in visible copy, tabs read Terrain / Thermal / Alteration, and the
duplicated extent/grid/projection strip is down to one line. The mandatory scientific warnings were NOT
shortened; two clauses were broadened so they stop carrying layer codes. (D) The Act 02 AOI marker is
removed - measured 72-100% hidden behind the copy column at every desktop width, and no crop can
separate them, so the authorized fallback applied; the geometry stays recorded and is still drawn by
the inspection aid. (E) Act 04 is sized against the viewport, so the headline and the whole map fit in
one view at 768/800/860/950 px heights (was 73-76%) while a tall desktop keeps the full 600 px map.
**(C) Evidence imagery polish is NOT delivered and needs Science authority:** the rasters are already
lossless at native density, and the dark Alteration rendering is pinned by
`geo_web_002.assets[alt01].legibility_note` ("no alternative approved style... must not re-stretch,
re-normalize or CSS-adjust it") with every tuning lever listed in `web_005b.analytical.not_used` as
hero-only. That is the post-WEB-006 WEB-007 programme. The two other asset packages in the repository
are report figures with a north arrow and scale bar burned in, so they are not the answer either -
see `evidence/web005b_r11/proof_sets_compare.webp`. Evidence refreshed in place.

**R15 (history):** the bounded final-polish pass, on the accepted direction - concept, hero,
section order and visual language are not reopened, and the hero markup is byte-identical. Evidence:
`tasks/WEB-005B_R15_FINAL_POLISH_EVIDENCE.md` and `evidence/web005b_r15/`.
**(A) The R14 evidence-imagery blocker is resolved.** Science issued
`geothermal-prospectivity@e8aa5d65:tasks/MER-151_GEO-WEB-004_HOMEPAGE_EVIDENCE_PRESENTATION_PARITY_AUTHORITY.md`
(`TERMINAL_ACCEPTED`, consumer WEB-005B / MER-109), which authorizes a bounded display window and one
fixed monotonic gamma per layer on the homepage Evidence / Result / inspection surfaces. Acts 3-4 are
rebuilt through it by the new `scripts/build_web005b_presentation.py`. ALT-01 gets `q_low 0.02 /
q_high 0.98` (span 0.96) - 99.9% of its governed valid cells sat in the bottom 8.3% of the canonical
range, so the unwindowed render spent the whole palette on outliers and published as a flat violet
field. THM-01 gets `q_abs 0.998` (resolved M 0.7036, the smallest clean quantile clearing the
mandatory 0.70 floor) plus gamma 0.85 with the centre fixed at 0. Terrain and priority keep their
transfer DISABLED and are byte-identical to R14 - terrain because its rendering is also the accepted
hero Terrain drape texture, priority because windowing it is prohibited and it must keep the colours
the hero payoff ends on. The authority's 4K/HiDPI enlargement is implemented, bounded and validated
but deliberately NOT published: every homepage analytical surface caps at 600 CSS px, which the native
1200 px grid already serves at a true 2x DPR, and three of four layers cannot be re-encoded down from
a 1800 px rung, so publishing one would ship 3-6 MB per panel for no density gain. That is a delivery
decision; MER-151 section 7 lets Product swap conformant derivatives in without Science re-entry.
**(B)** The numbered prep labels `02 The place` / `03 The evidence` / `04 The result` and the weak
`Solutions` kicker are gone from the UI and from both dictionaries; each section leads on its
headline. The one remaining piece of specialist vocabulary in visible copy (`clay and hydroxyl` in the
ALT-01 alt text) is replaced with a plain description. The mandatory scientific warnings are
untouched. **(C)** Act 03 is re-measured: the stage is sized to its content (1040 px: a 600 px map and
a 394 px column) instead of running the full 1280 shell, and the subordinate data-gap footnote moved
to the foot of the reading column, so the section no longer has empty ground on the right and under
the column. **(D)** Act 04: the headline's 13ch cap is gone (it broke "Where to look first." after
"look"), the definition strip's rules moved into real gutters inset from the type, and the section
gives up height - headline to legend now fits one viewport at 1280x720 through 1920x1080 (was 73-76%
of the section at R14). **(E)** Solutions drops the pilot framing from the card copy and all three
cards share one copy-block height. **(F)** A tonal hierarchy replaces the flat post-hero ground:
`--orb-lift` for reading sections, `--orb-deep` for the closing ones, one atmospheric tint behind the
result, every section still starting and ending on `--orb-bg` so no boundary is a colour step, and
boundary hairlines that fade out before the page gutter. Gates: site PASS, hero 420/0, WEB-005
negatives 72/72, WEB-005B negatives 55/55 (12 new MER-151 bounds), copy preservation 28 declared
differences and nothing else, no horizontal overflow at 13 widths x DPR 1/2/3, zero first-viewport
leak. Not merged, nothing deployed, no DNS touched.

**Site architecture:** static HTML + CSS + vanilla JavaScript
**Public domain target:** `https://orbgss.com`
**Canonical repository:** https://github.com/mertkaanakgunlu-debug/orbgss-website
**Accepted WEB-002 implementation HEAD:** `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`
**Accepted WEB-003 implementation HEAD:** `3670d43bece4ffba657a3d9645cbea20c7e698bf`
**Accepted WEB-004 implementation HEAD:** `56cb53039b85a852110c737505bc2ae2282acb08`
**Accepted GEO-WEB-002 implementation HEAD:** `ea693c29762279131fbed005e832c5ff2dca587b`
**Accepted WEB-005A terminal implementation HEAD (published):** `1135e7a7e0b0f6db6348dee139d505550d8ca8b9` on `origin/feat/web-005a-hero-visual-fidelity`
**Accepted WEB-005 terminal acceptance:** `main@00af0f232a8d7d77f5ca61d758461ff7316ba151` (`tasks/WEB-005_TERMINAL_PRODUCT_ACCEPTANCE.md`)
**WEB-005A rejected checkpoint (before-evidence):** `ffa2f2944ca5992afb9e9891b42745a9bd1105ad`
**WEB-005A R2 package (superseded, did not pass the human visual gate):** `a6897828d6e35595ea5a9a39a1e812b0fcbbfb35` (implementation `b285c90cf685f6ca9da61c41302ae496d7e8169b`)
**WEB-005A R3 implementation HEAD (reviewed, `REVISION_REQUIRED`):** `37152222c33fdc09265ba022ce45828c8d002723`
**WEB-005A R3 preview gate 1:** `tasks/WEB-005A_R3_PREVIEW_GATE.md` at `cd2018e` — reviewed, `PREVIEW_GATE_REVISION_REQUIRED` (before-evidence)
**WEB-005A R3 preview gate 2:** `tasks/WEB-005A_R3_PREVIEW_GATE_2.md` at `b6cd5fb` — reviewed as motion, `REVISION_REQUIRED` (before-evidence)
**WEB-005A R3 preview gate 3:** `tasks/WEB-005A_R3_PREVIEW_GATE_3.md` at `6e3d2f8` — direction accepted by Product in chat; moved to final production
**WEB-005A final production implementation HEAD:** `aed0597f961793f7a00d766673e7b9bc358df91a` (first render `92745527cf23c0be82573c37c60a62e5e3afb4c1` is defective before-evidence)
**WEB-005A final polish (relief rise + startup poster):** `tasks/WEB-005A_FINAL_RELIEF_RISE_POLISH_EVIDENCE.md` — `REVIEW_READY`, awaiting Product review. Product accepted the final production in substance at `e7098de` (`docs/web-005-polish-authority@1437fbb`) and authorized two bounded polishes: the startup poster is now the opening frame with the held frame kept as a separate held base for every static state, and the DEM relief now rises between the held frame and the Terrain state (`0e87675`: seven lossless states from the scene's own rise interval, 0.667 s, outline and shadow rising with it, motion path only, +1.51 MiB). No motion frame, encode, drape state, camera or asset changed. Site PASS, hero 420 / 0, negative tests 71 / 71. Not pushed
**WEB-005A final production:** `tasks/WEB-005A_FINAL_PRODUCTION_EVIDENCE.md` — accepted in substance by Product at `e7098de` (re-submitted 2026-09-19 after a motion re-render). The first render (`92745527`) was withdrawn at `99b7e25`: the owner saw a line leave the platform before it settled and a band sweep during its exit — a BLACK line platform → reticle corner (f72, f100–112, f180) and a dark band (f208–219), printed by invisible scan-fan geometry because slices went 64 → 96 under an unchanged `transparent_max_bounces` of 96. Budget now 512 with a validator rule and a negative test; frames 24–224 and 238–243 re-rendered, the rest proved untouched by A/B; the whole sequence was checked every 4th frame before encoding (evidence doc §2.1). Not pushed, not merged, not deployed
**Reference/upstream only:** https://github.com/baran-orbgss/website
**Science authority:** `mertkaanakgunlu-debug/geothermal-prospectivity@215ef89d794cf6cbf98e94f8fc17184c859ebcd8` (tag `v1.0.0`)
**Registrar / DNS:** Squarespace
**Hosting target:** Vercel
**Company:** VirgaSoft
**Product:** OrbGSS — Orbital Geo-Spatial Solutions
**Product authority:** OrbGSS Website vNext Product & Execution Authority v1.8 (`docs/WEB_VNEXT_AUTHORITY.md`); `docs/WEB_005_POLISH_VISUAL_DIRECTION_AUTHORITY.md` (R2 visual lock) where newer.
**Accepted WEB-HERO-001D evidence HEAD:** `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e` (terminal Product acceptance published at `573f4f1`)
**WEB-005 execution baseline:** `main@d2421a772f2e4cfa38c85dd5ee71a419c5160838`
**Tracking:** MER-90 (WEB-002 accepted); MER-91 (WEB-003 accepted); MER-92 (WEB-004 accepted); MER-102 / GEO-WEB-002 (Science-accepted); MER-101 / WEB-HERO-001D (terminally accepted); MER-93 / WEB-005 (terminally accepted); **MER-107 / WEB-005A (terminally accepted, published at `1135e7a`)**; **MER-109 / WEB-005B (R15 is part of the accepted baseline)**; **MER-149 / WEB-005C (accepted at `79cc2cb`)**; MER-151 / GEO-WEB-004 (Science authority for the Acts 3-4 presentation); MER-108 / GEO-WEB-003 (Science terminal, consumed); MER-96 / GEO-WEB-001 resolved; MER-95 / WEB-006 (cutover; see above); **MER-213 (post-launch audit, Done; its documentation head is `main@f4f1d4d6`)**; **MER-216 (media fidelity and runtime hardening, `REVIEW_READY`; supersedes MER-143 / WEB-007, MER-144 / WEB-008, MER-145 and MER-146, which are canceled)**

## Authority

`docs/WEB_VNEXT_AUTHORITY.md` is the repository-local summary of the product-owned *OrbGSS Website vNext Product & Execution Authority*. Where it disagrees with newer canonical Drive Product authority, the current Drive authority wins. WEB-002 is terminally accepted under `tasks/WEB-002_PRODUCT_PROOF.md`. WEB-003 is terminally accepted under `tasks/WEB-003_PUBLIC_SITE_DEPTH.md` at implementation HEAD `3670d43bece4ffba657a3d9645cbea20c7e698bf` after one bounded Product review revision. WEB-004 is terminally Product-accepted under MER-92 at implementation HEAD `56cb53039b85a852110c737505bc2ae2282acb08`; canonical acceptance publication is `716104d677fea5021787b581470a436ed708f3a3` and acceptance record is `docs/WEB-004_PRODUCT_ACCEPTANCE.md`.

`docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md` locks the final four-act homepage story for WEB-005 and supersedes the repeated full-width proof-scene rhythm where they conflict; it does not supersede accepted Science semantics, WEB-002 provenance constraints, WEB-004 performance/accessibility decisions or the accepted route architecture. GEO-WEB-002 / MER-102 is the Science & Geospatial publication dependency it named. It is terminally accepted under `docs/GEO-WEB-002_SCIENCE_ACCEPTANCE.md` at implementation HEAD `ea693c29762279131fbed005e832c5ff2dca587b`. Product may bind the package into WEB-005 while preserving its exact labels, warnings, provenance and maximum-safe-render constraints.

## State at WEB-005A final production (history; since terminally accepted)

What the branch ships now is described in `tasks/WEB-005A_FINAL_PRODUCTION_EVIDENCE.md`: motion video ending on
the held frame, four lossless drape states composited by the page, no legend / card / label in the hero. The
section below describes the reviewed R3 checkpoint (`37152222`) and is kept as history; its page-layer
homography stage, legend and handoff card are **removed**.

## Previous state (WEB-005A R3 as reviewed — `REVISION_REQUIRED`; superseded)

WEB-005A revises only the hero's rendered media, the hero production configuration that generates it,
the page-layer handoff, and one footer attribution sentence. The four-act homepage and every accepted
scientific asset, label and warning are unchanged and re-verified.

- **Satellite.** The R2 procedural generic EO platform, on a **time-remapped derived orbit**
  (`orbit_intent.rate_profile`): hidden for the first two seconds, round the lower-left limb near
  frame 55, then held at (0.25, 0.40) of the frame — lower-left of the target, 13 % of the frame
  width — from frame 136 to 192, because the camera is locked off for the same frames. It is left
  behind by the dive and never becomes a foreground fly-by.
- **Acquisition.** Four thin cyan lines connect (110–124), the 420 km frame locks with a 2.6× pulse
  while its corner locks draw in (128–144), a sweep band crosses it (144–178), and the lines release
  with an acquisition-complete pulse at 178–192 **while the satellite is still in frame**.
- **Dive and hold.** One eased, motion-blurred dive (192–262) on the same registered target. The
  regional frame vanishes as its edges leave; the **accepted 36 × 36 km analysis AOI** draws in as
  its own frame with a lock pulse and settles. The hold (262–276) is genuinely still: 166 km across
  the frame, the AOI 23 % of the frame width.
- **Earth.** Same model, lighting and atmosphere; Blue Marble colour everywhere, multiplied under the
  hold by a 30 m **Sentinel-2-derived detail ratio** (structure only) with the cloud veil cleared over
  that window. Structure is sampled at 0.35× at the hold (`hero/evidence/texel_coverage.json`);
  attribution *Contains modified Copernicus Sentinel data (2025)* is in the footer.
- **Handoff.** The page maps the accepted derivatives **inside the analysis frame** with a CSS
  homography on the audited corners and reveals Elevation → THM-01 → ALT-01 → priority, each
  byte-exact under its exact label and accepted warning, ending on the priority result with its own
  legend. The stack never exceeds 1249 device pixels. No faults layer is shown: structure/geology
  remains the stated data gap and nothing is fabricated for it.
- **Gates.** Site validator PASS 0 warnings; hero validator 292/292; negative tests 27/27; shot audit 18/18.

## State at WEB-005 (accepted; the four-act structure is still current)

The homepage is now the locked four-act story from `docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md`:
**Act 1 cinematic acquisition hero → Act 2 real Kızıldere EO context → Act 3 compact evidence trio →
Act 4 priority/result climax**, followed by the subordinate pilot ledger, company/trust and contact
sections. The WEB-001/002 six-scene `beam → full-width raster` gallery is gone, and
`scripts/validate_site.py` now fails the build if it returns.

- **Act 1** is the accepted WEB-HERO-001D sequence, re-rendered against the real accepted Kızıldere
  pilot centre and packaged as production WebM / MP4 / poster. It is a **render**, and its caption
  says so in both languages: `Rendered orbital sequence — not sensor imagery`.
- **The real-data/result handoff is a page element, not a video frame.** A governed class-B raster
  inside a lossy encode would have its colours and values changed by chroma subsampling and
  quantisation, which the accepted package forbids — so the accepted priority derivative is shipped
  as its own checksummed file and composited over the hero instead. The hero scene's
  `aoi_injection_interface.layer_slots` records that decision as `render_surface: html_overlay`, and
  `hero/scripts/validate_hero.py` enforces it.
- **Safe display density is measured, not asserted.** Across a 360–3840 CSS px viewport sweep of the
  built page, the widest render of each scientific visual is: Act-2 context 1199 CSS px (2398 device
  px at 2×, ceiling 2400), each evidence card 624 (1248, ceiling 1249), the Act-4 priority map 623
  (1246, ceiling 1249), the in-frame legend 248 against a 732 px native crop. Nothing is upscaled at
  any width or density. Each figure is recorded in `geo_web_002.assets[].web_005_placement.rendered`
  and re-checked by the validator.
- **Act 4 is deliberately contained.** The accepted score raster is 1200 × 1200 cells at 30 m drawn
  at 1249 px and *cannot* reach the ≥ 2000 px Act-4 presentation target from accepted science. The
  composition carries the weight instead of the raster being stretched, and the export's own legend
  sits inside the map frame — there is no detached homepage colour bar.
- **Structure/geology stays an explicit, subordinate data gap.** Not fabricated, not promoted to an
  act, and stated as score-invariant.

Remaining gates are unchanged and are **not** WEB-005's to close: `CONTACT_RELEASE_GATE`,
`HOSTED_PREVIEW_NOT_RUN`, and the WEB-006 production DNS cutover human gate.

## State at GEO-WEB-002 (accepted / complete)

`tasks/GEO-WEB-002_FINAL_HOMEPAGE_VISUAL_MASTERS.md` is implemented and terminally accepted. The canonical package is
`docs/GEO-WEB-002_FINAL_VISUAL_MASTER_PACKAGE.md` (`READY_FOR_PRODUCT_BINDING`), mirrored
machine-readably in `assets/imagery/sources.json` → `geo_web_002`. Nothing is placed on a public route:
this publishes the visual masters the locked four-act homepage in
`docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md` needs, for WEB-005 to bind under its own authority.

- **Act 2 — real AOI context.** One natural-colour Landsat 8 OLI composite of the Kızıldere AOI in its
  regional setting: `LC08_L2SP_179034_20250505_02_T1`, acquired 2025-05-05, 0.90 % cloud, rendered by the
  existing `scripts/build_imagery.py` grammar at native 30 m into a 2400 × 1500 px (72 × 45 km) EPSG:32635
  frame with 100 % valid coverage, plus 2400 / 1800 / 1200 / 900 WebP candidates.
- **Acts 3 and 4 — cartographic masters.** `terrain`, `thm01`, `alt01`, `alt02` and `priority` resolve to
  their accepted GEO-039 exports of persisted `kizildere_mvp_v2`. Each ships the rendered map panel as a
  crop with **no resampling at all** (1249 px), an 800 px card derivative, and a native-resolution lossless
  crop of the master's own governed legend — so a necessary legend can sit inside the map frame instead of becoming a
  detached homepage colour bar.
- **Resolution ceiling.** The accepted grid is 1200 × 1200 cells at 30 m and the accepted renderer draws it
  at 1249 px, so **1249 device pixels** is the maximum honest rendered width for any cartographic asset.
  Act 2 meets its ≥ 2000 px target natively and the evidence cards meet ≥ 1200 px. The Act-4 priority master
  **cannot** reach ≥ 2000 px from accepted science: the package publishes the exact ceiling instead of
  upscaling, and WEB-005 must give Act 4 a contained composition (1249 CSS px at 1×, approximately 624 CSS px at 2×).
- **Findings WEB-005 must not "fix".** ALT-01/ALT-02 render as dark fields with bright anomalies — their
  registry-approved style normalizes linearly over the full value range, so ~87 % of valid cells sit in
  the lowest fifth of the ramp. No re-stretch, re-normalize or CSS colour/contrast adjustment. NoData (0.0–5.5 % per panel)
  stays visible. ALT-01 is the preferred single alteration card under the accepted package.
- **Enforcement.** `scripts/build_final_visual_masters.py` rebuilds every derivative deterministically and
  refuses an altered master, a wrong-layer export, a wrong 1200 × 1200 source grid or any presentation upscale beyond the accepted renderer-native panel. `scripts/validate_site.py` recomputes all
  19 derivative checksums plus the class-A master and enforces the publication record,
  including each asset's declared no-upscale ceiling. REVIEW_READY evidence records validator PASS, 0 warnings; `git diff --check` green; negative tests and byte-for-byte rebuild PASS.
- **No semantic change.** Mandatory core remains THM-01 + ALT-01 + ALT-02; fail-closed behaviour,
  terrain-as-context, the structure/geology `DATA_GAP`, CRS/grid/unit/NoData/mask/resampling semantics and
  every public label and mandatory warning are carried from `docs/WEB-002_SCIENCE_ASSET_PACKAGE.md`.
  No structure or geology asset is published; nothing is fabricated to fill that gap.

## State at WEB-004 (accepted / complete)

WEB-004 hardened the accepted six-route site without redesigning it. Full measurements, tooling
versions and negative tests are in `docs/WEB-004_HARDENING_EVIDENCE.md`; terminal Product acceptance is in `docs/WEB-004_PRODUCT_ACCEPTANCE.md`.

- **Performance.** Homepage Lighthouse Performance 77 → **94**; LCP 6.5 s → 3.2 s; CLS 0; TBT 0 ms. Total page transfer **1369.6 KiB → 645.1 KiB (−53%)**. All six routes clear Accessibility / Best Practices / SEO ≥ 95, and Performance ≥ 90 on the homepage and every deep route.
- **Hero delivery.** Three recorded WebP derivatives (900 / 1400 / 1800) plus `srcset`/`sizes` and a matching preload; a 375 px phone fetches ~148 KiB instead of 553 KiB. Resize-and-encode only, checksummed in `assets/imagery/sources.json`, validator-enforced. The hero visual itself is untouched and still belongs to WEB-005.
- **Inactive evidence layers deferred** behind `data-src`/`data-srcset` and promoted as the section approaches the viewport — 340 KiB off the initial load, switching still instant, provenance still enforced.
- **Caption contrast is measured per viewport.** `object-fit: cover` re-crops each proof raster as the viewport changes shape, so the WEB-002 hand-chosen tones fell to 2.84 / 3.53 / 4.21:1 at some widths. The accepted rule is applied continuously between the same two accepted tones; every caption clears 4.5:1 at 375 / 768 / 1024 / 1440 (worst case 4.58:1). No raster is modified, and the caption remains bare monospace text with no card, box or band.
- **Accessibility.** Viewport-change reset for the mobile menu and Solutions disclosure; WCAG 2.5.8 touch targets (footer nav, direct email, brand, desktop EN/TR); `/contact/` heading order corrected (route Accessibility 98 → 100); real web-manifest icon. Zero horizontal overflow and zero undersized targets across all six routes at all four widths.
- **Gates.** `HOSTED_PREVIEW_NOT_RUN — permission unavailable` was accepted under WEB-004 on MER-92. `CONTACT_RELEASE_GATE` **remains open** for pre-WEB-006 launch verification: every mailto correctly targets `contact@orbgss.com` in both languages, but mailbox ownership still requires Workspace/account evidence.
- **Product decisions accepted (MER-92).** Homepage LCP 3.2 s under the recorded local synthetic mobile profile is an accepted bounded WEB-004 deviation; accepted scientific proof derivatives must not be re-encoded solely to chase 2.5 s. The score-legend `image-aspect-ratio` finding is an accepted intentional deviation; the scientific legend must not be re-proportioned solely to clear the heuristic. No Product/Science semantics changed.

### WEB-005 hero media budget (ACCEPTED, MER-92)

The binding WEB-005 media envelope accepted by Product is:

| Asset | Ceiling |
| --- | --- |
| Desktop autoplay WebM | ≤ 3.0 MiB |
| MP4 fallback | ≤ 4.5 MiB |
| Poster still | ≤ 180 KiB |
| Mobile / reduced-data | intentional static/poster fallback, no dual-video download |

The engineering conditions WEB-004 measured under remain: one encode per client; the poster stays the preloaded LCP element with
`imagesrcset`/`imagesizes` matching the `<img>`; `prefers-reduced-motion: reduce` gets the static
poster; the bottom-right caption region must keep ≥ 4.5:1; and hero media must be recorded and checksummed like the accepted derivatives.

## State at WEB-003 (accepted)

Five public routes extend the homepage into a complete small public site, each as a real static directory (`<route>/index.html`, canonical trailing-slash URL):

- `/platform/` — the accepted workflow (AOI → source/context → evidence → explicit data gaps → integrated priority → investigation decision support) as an editorial numbered list.
- `/solutions/` — the application portfolio (Geothermal active first application; Mineral and Environmental & Land Intelligence as expansion directions), reusing the homepage's own copy and status labels.
- `/pilot/` — the Kızıldere first-application proof in depth, reusing the accepted WEB-002 proof imagery and the structure/geology data-gap panel with the same checksums and mandatory EN/TR warnings.
- `/company/` — company/about destination: OrbGSS identity, VirgaSoft parent attribution, operating principles and restrained expansion framing.
- `/contact/` — three mailto conversation starters (pilot, partnership, technical) plus the direct address; no form, backend, analytics or PII capture.

The homepage and every deeper route share one persistent header/footer navigation. `vercel.json` serves trailing-slash canonical URLs; `sitemap.xml` lists all six canonical routes. Language choice persists across routes through the shared `localStorage` key. The validator checks route metadata, internal/cross-page links, sitemap coverage, EN/TR parity, accessibility-label localization, pilot social-preview truthfulness and the unchanged WEB-002 scientific provenance/checksum/warning invariants.

The MER-91 bounded Product review revision closed three findings before acceptance: every human-readable `aria-label` on canonical routes is bound to `data-i18n-aria-label`; `/pilot/` uses the accepted Kızıldere `assets/proof/geothermal-1400.webp` derivative for Open Graph instead of the unrelated Crater Lake hero; repository authority/status pointers were reconciled. Validator result remained PASS with 0 warnings and the implementation reported 185 site-wide i18n keys.

## State at WEB-002 (accepted; superseded by WEB-005 for the homepage)

The homepage tells the evidence-to-intelligence story on one real area of interest. The rhythm is unchanged — dark technical beam → large full-width visual panel — and every scientific story panel shows the same Kızıldere pilot AOI (36 × 36 km, EPSG:32635, 30 m grid).

1. navigation: Platform → Solutions⌄ → Pilot → Company → Contact → EN | TR
2. hero: static Crater Lake poster (`data-hero-slot="static-poster"`; final integration remains downstream)
3. `01 Observe` → Kızıldere AOI — accepted MVP project context
4. `02 Terrain` → Elevation — NASADEM context
5. `03 Evidence` → keyboard-accessible THM-01 / ALT-01 / ALT-02 switch
6. `04 Structure` → explicit public data gap
7. `05 Priority` → Remote-Sensing Relative Priority — Experimental Baseline, 0–100 within-AOI ranking
8. `06 Geothermal` → Kızıldere first-application composite
9. Pilot ledger, Company/Trust, Contact, footer

## Product-proof provenance

Every scientific visual is an OrbGSS cartographic export materialized through the accepted GEO-039 Workbench export path from persisted `kizildere_mvp_v2`, then cropped/resized for the web. `assets/imagery/sources.json` (`web_002.proof_assets`) records export identity, export manifest pointer, master SHA-256, derivative crop/size and derivative SHA-256. `scripts/validate_site.py` recomputes shipped derivative checksums.

`05 Priority` and `06 Geothermal` use accepted `mvp_remote_sensing_priority_v1` output from run `8716e89324ff5566859f470f207d5a1f0ab651c19d9c7e9dba3087960a63cf3c` under `remote_sensing_equal_family_v1`: deterministic 0–100 within-AOI screening/ranking, never probability, Full Prospectivity, reserve, discovery or drilling-success. Mandatory warning semantics remain visible in EN/TR.

`04 Structure` / geology remain `DATA_GAP / optional support / score-invariant`: no public-safe fault or lithology master is authorized and nothing is fabricated to fill the gap.

## Locked design decisions

- Full-width high-resolution EO/product imagery remains the core visual system.
- Scientific proof imagery stays clean; no fake GIS controls, HUD chrome or decorative overlays that imply functionality.
- Product-proof rasters and score ramp must preserve accepted scientific rendering; no color/contrast/opacity reinterpretation.
- Same-AOI proof panels maintain one-ground framing.
- Mandatory scientific warnings remain visible and validator-enforced.
- Secondary monospace is reserved for coordinates, evidence labels, metadata/status and technical descriptors.
- Navigation order remains Platform → Solutions → Pilot → Company → Contact → EN | TR.
- EN default / TR second language; no flags/framework.
- No unsupported customer, partner, revenue, ROI, accuracy, AI-performance or production-deployment claims.
- The locked four-act authority in `docs/WEB_PUBLIC_VISUAL_NARRATIVE_AUTHORITY.md` supersedes earlier homepage-layout assumptions where they conflict; WEB-005 owns that integration.

## Product positioning

OrbGSS is a geospatial-intelligence platform. Geothermal is the active first application (the Kızıldere pilot). Mining and Marine are expansion directions and remain labelled as such (taxonomy Geothermal / Mining / Marine since WEB-005C; the superseded application-ledger labels must not return).

## Production blockers

None. See "Open gates and decisions" at the top of this file. `main@2517369e` is published and verified in production (MER-219). `CONTACT_RELEASE_GATE` is carried as MER-238 D4, a ship gate for MER-240. DNS stays outside every website task except a CTO-authorized one, and Google Workspace MX / SPF / DKIM / DMARC must never be touched.

## Next canonical task

1. **MER-239** (this reconciliation, docs only) — `REVIEW_READY` on `mertkaanakgunlu/mer-239-web-sitesi-belge-ve-otorite-uzlastirmasi`, awaiting CTO review. Publishing it is a fast-forward of `main`. Because production is COUPLED, that push redeploys production. The only deployed file that changes is `assets/imagery/sources.json`, and only in its metadata (no page, asset, path or checksum). Every other changed path sits outside the deploy set (`.vercelignore`).
2. **MER-240** — the new English pages from `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md`, after MER-239 is accepted and published; D4 (mailbox) is its ship gate.
3. **MER-241** — static `/tr/` pages, after MER-240.
4. **MER-242** (Science, parallel) — MER-151-family derivatives for the Geothermal page's priority-over-relief and ALT-02 figures.

Updating `main`, any production deployment and any DNS change stay separate CTO-authorized gates.

## History

- ORBWEB-001 (2026-09-09): production imagery from USGS Landsat Collection 2 Level-2, provenance pinned.
- ORBWEB-001.1 (2026-09-09): on-image labels, right-aligned navigation with Solutions dropdown, EN/TR.
- ORBWEB-002A (2026-09-10): GitHub publication to `baran-orbgss/website`.
- WEB-001 (2026-09-15): vNext foundation accepted at `677bfa7672ac18c2c808ddaaf235ff12863de443`.
- WEB-002 (2026-09-15): public-safe GEO-039 proof exports, Kızıldere evidence/prospectivity presentation and provenance/checksum enforcement accepted after one bounded Product review revision; implementation HEAD `a10cc141e3a7830c5e3c67a22e950ab16c0fe92b`.
- WEB-003 (2026-09-15): `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/`; cross-route EN/TR, metadata, sitemap/link validation and reuse of accepted Kızıldere proof. Initial implementation `5d99eb811dfbb3396ebade17ff6ab863b5463a35`.
- WEB-003 bounded Product review revision (2026-09-15): accessibility-label localization guard, truthful Kızıldere pilot social preview and authority/status reconciliation; final implementation HEAD `3670d43bece4ffba657a3d9645cbea20c7e698bf`; Product accepted and fast-forwarded canonical main non-destructively.
- WEB-004 (2026-09-16): responsive/accessibility/performance hardening accepted under MER-92; implementation HEAD `56cb53039b85a852110c737505bc2ae2282acb08`; acceptance publication `716104d677fea5021787b581470a436ed708f3a3`. `HOSTED_PREVIEW_NOT_RUN` accepted; `CONTACT_RELEASE_GATE` remains open for launch verification.
- WEB-005 (2026-09-16): four-act homepage, production cinematic hero and truthful fallbacks; terminally accepted at `main@00af0f232a8d7d77f5ca61d758461ff7316ba151`.
- WEB-005A (2026-09-16): hero visual fidelity. Checkpoint `ffa2f2944ca5992afb9e9891b42745a9bd1105ad` (circular orbit, thinned frame, single boresight, resolved tail, bitrate investigation) was technically green but visually rejected; R2 delivered the Product visual lock — derived orbital pass, volumetric generic EO satellite, readable sensing lines, lock event, recomposed approach, NASA BMNG 500 m regional albedo, coupled page-layer analytical handoff — `REVIEW_READY`.
- GEO-WEB-002 (2026-09-16): final homepage visual master package for the locked four-act composition — Kızıldere Act-2 natural-colour Landsat context master at native 30 m (2400 × 1500 px), and renderer-native `terrain` / `thm01` / `alt01` / `alt02` / `priority` cartographic panels, card derivatives and in-frame legend crops from the accepted GEO-039 exports; per-asset provenance, checksums, rights, warnings and maximum safe rendered size published. Act-4 ≥2000 px target is not honestly achievable under accepted science and the task-authorized 1249-device-pixel contained-composition fallback is accepted. Implementation HEAD `ea693c29762279131fbed005e832c5ff2dca587b`; terminal Science acceptance `docs/GEO-WEB-002_SCIENCE_ACCEPTANCE.md`.
- WEB-005A → WEB-005C (2026-09-16 → 2026-09-21): hero visual fidelity (terminal head `1135e7a`), homepage after the hero rebuilt to the accepted design (WEB-005B R15), public taxonomy converged on Geothermal / Mining / Marine (WEB-005C R2). Accepted release candidate `79cc2cb82a4542461cbbfc1d0c349cf02b861084`; never merged to `main`, and per MER-213 it is what production serves.
- MER-213 (2026-09-29): post-launch reconciliation — baseline `79cc2cb` verified against `main`, repository docs reconciled, validators and a real-browser regression audit recorded in `tasks/MER-213_POST_LAUNCH_AUDIT_EVIDENCE.md`.
- MER-213 (2026-10-02): reviewed and Done; its documentation commit `f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85` was `main` until 2026-10-15.
- MER-216 (2026-10-02 / 2026-10-03): media fidelity and runtime hardening, Phases 1-4, `REVIEW_READY` on `claude/mer-216-s1r628`; supersedes MER-143..146. See `tasks/MER-216_EVIDENCE.md`.
- MER-216 (2026-10-03): independently accepted and Done at `adf08186d3ee4a438bda73886272d05c970e670a`; published 2026-10-15 in `main@2517369e` (MER-219).
- MER-218 (2026-10-03): docs-only canonical publication closure of MER-216 from exactly `adf08186`; accepted (Done) 2026-10-03, published 2026-10-15. See `tasks/MER-218_EVIDENCE.md`.
- MER-237 (2026-10-15): orbgss.com served the whole repository; a root `.vercelignore` allowlist, validator rules and `negative_tests_mer237.py` (29/29) limit the deploy to the public site, and four routes' Crater Lake `og:image` became the hero poster. Accepted by the CTO the same day at `2517369e`.
- MER-238 (2026-10-15): Milestone 6 information-architecture and page-content authority (`docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md`, mockups `docs/mockups/m6/`), approved by the CTO with D1 (Science derivatives, MER-242) and D2 (Turkish slugs) decided.
- MER-219 (2026-10-15): publication preflight; topology COUPLED; the CTO approved and authorized the agent to publish. `main` fast-forwarded `f4f1d4d6` → `2517369e` at 13:45:21Z; Vercel production deployment `7094313382` / `orbgss-website-l0hjfxcdh` 12 s later; production smoke 46/46, browser checks 21/21; no rollback.
- MER-239 (2026-10-15): post-publication documentation and authority reconciliation; MER-238 merged onto the published line; `AGENTS.md` replaced by a pointer to `CLAUDE.md` (CTO decision). See `tasks/MER-239_EVIDENCE.md`.
