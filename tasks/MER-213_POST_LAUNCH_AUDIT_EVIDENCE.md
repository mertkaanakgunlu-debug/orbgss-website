# MER-213 — Post-launch state and defect audit: evidence

**Linear:** MER-213 (project *OrbGSS — Website*, milestone 5 — Post-Launch Audit, Media Fidelity & Runtime Hardening)
**State:** `REVIEW_READY` — stopped for CTO/Product review. The implementation agent does not accept its own work.
**Date:** 2026-09-29
**Content baseline:** `feat/web-005c-public-domain-taxonomy-parity@79cc2cb82a4542461cbbfc1d0c349cf02b861084`
**Task branch:** `claude/mer-213-bp01w5`, created from exactly `79cc2cb`. This is the branch the workspace designated for the task; it previously pointed at stale `main` with no commits of its own, so it was reset to the baseline before any work. It is a bounded task branch, not canonical state. The commit SHA and the local/remote HEAD match are reported in the review hand-off, not here, because a document cannot name the commit that contains it.

## 1. Environment and task resolution

| Check | Result |
| --- | --- |
| Linear read from Claude Projects | **OK.** `MER-213` resolved by exact ID with `get_issue` (description, status Backlog at read time (no Linear write was made), relations `blocks MER-143, MER-144`, no comments). No `ENVIRONMENT_BLOCKED_LINEAR` |
| Repository identity | `origin` = `https://github.com/mertkaanakgunlu-debug/orbgss-website` (fetch and push) |
| Working tree before execution | Clean (`git status --short` empty on `claude/mer-213-bp01w5@00af0f2`) |
| `main` | `origin/main` = `00af0f232a8d7d77f5ca61d758461ff7316ba151` |
| Release candidate | `origin/feat/web-005c-public-domain-taxonomy-parity` = `79cc2cb82a4542461cbbfc1d0c349cf02b861084` |
| Ancestry | `git rev-list --left-right --count origin/main...origin/feat/web-005c-…` = `0 25`; `git merge-base --is-ancestor origin/main <baseline>` → true. Pure fast-forward possible |
| Linear vs Git vs repository | **No conflict on the baseline.** The issue names `79cc2cb` explicitly and Git agrees. One drift exists and is reported, not resolved (section 6): the Claude Project instructions' navigation differs from the repository's |
| Vercel | **Not re-verified.** Vercel reads from this environment returned 403 in the earlier read-only audit (`/mnt/project-files/audits/website-state-audit-2026-09-29.md`) and were not retried; the deployment identity in `STATUS.md` is copied from the MER-213 Linear record and labelled as such. Public `orbgss.com` is not reachable with `curl` through the environment proxy, so this audit ran against the exact baseline tree served locally, not against production |

## 2. Validators (baseline tree, before any change, and again after the documentation change)

| Command | Before | After |
| --- | --- | --- |
| `python3 -B scripts/validate_site.py` | PASS, 0 warnings — 4 scenes, 29 html images, 6 routes, 268 i18n keys, 6 geo-web-002 assets (19 files) | PASS, same counts |
| `python3 -B scripts/negative_tests_web005.py` | 72/72 caught; restored tree: site 0 PASS, hero 1 FAIL — identical to baseline | not re-run (no code or asset changed) |
| `python3 -B scripts/negative_tests_web005b.py` | 55/55 caught; restored tree identical | not re-run |
| `python3 -B scripts/negative_tests_web005c.py` | 18/18 caught; restored tree identical | not re-run |
| `python3 -B hero/scripts/validate_hero.py` | 412 checks, **13 failed** | 412 checks, the same 13 failed |

**The 13 hero failures are environmental, not defects.** They are exactly the checks that need the large Blender source textures (`hero/assets/source/*`: four Earth-texture SHA-256 comparisons, one detail-multiplier SHA-256 comparison, and the eight "materialized local path exists" checks for `land_ocean_ice_cloud_2048.jpg`, `land_ocean_ice_cloud_8192.tif`, `dnb_land_ocean_ice.2012.3600x1800.jpg`, `world.topo.bathy.200407.3x21600x10800.jpg`, `world.topo.bathy.200407.3x21600x21600.C1.jpg`, `world.topo.bathy.200407.C1.crop.png`, `cloud_combined_8192.tif`, `s2_kizildere_detail_30m.png`). That directory is deliberately untracked (`hero/assets/source/.gitignore`), so no clone can contain the files; the accepted 420/0 result comes from the hero workstation. The lane checks (baseline pinned, integration mode, and "public-site changes since the baseline stay inside the integration write surface") **pass**, including after this task's documentation edits. The authoritative hero result therefore cannot be produced in Claude Projects; that is a limitation of the lane, recorded here rather than papered over.

The site validator's provenance/checksum checks (`sources.json`, all derivative SHA-256, the MER-151 bounds, the palette LUT, the mandatory EN/TR scientific warnings, sitemap and route metadata) all pass, which covers the "scientific asset/provenance validation" item.

## 3. Real-browser regression audit

**Tooling:** Playwright 1.56.1 driving Chromium 141.0.7390.37 (headless), against `python3 -m http.server` on the baseline tree at `127.0.0.1:8099`. Scripts and raw output: `evidence/mer213/browser_audit.js`, `browser_audit.log`, `browser_audit_results.json`, `browser_interaction_checks.js`, `browser_interaction_checks.log`. Evidence tooling only; nothing is added to the site or its dependencies.

**Matrix:** 7 pages (`/`, `/platform/`, `/solutions/`, `/pilot/`, `/company/`, `/contact/`, `/404.html`) × 5 viewports (1440×900, 1024×768, 768×1024, 390×844, 360×740) × 2 languages (EN, TR) = **70 page loads**, each scrolled end to end so deferred images load.

| Check | Result |
| --- | --- |
| HTTP status of every load | all 200 |
| Console errors/warnings, page errors, failed or ≥400 requests | **none** in all 70 loads |
| Horizontal overflow (`scrollWidth − clientWidth`) | **0 px** in all 70 loads |
| Broken images / images without an `alt` attribute | none |
| Raw or empty i18n keys visible | none |
| `html[lang]` follows the language on every canonical route | correct in EN and TR |
| Links, EN desktop, all six routes | **69 unique links resolved, 69 OK**; 26 carry a `#anchor`, and every anchor id exists on its target page (including `/solutions/#geothermal|#mining|#marine`); every `mailto:` targets `contact@orbgss.com`; no external links |
| Navigation order and Solutions dropdown | EN: Platform → Solutions (Geothermal, Mining, Marine) → Pilot → Company → Contact; TR: Platform → Çözümler (Jeotermal, Madencilik, Denizel) → Pilot → Şirket → İletişim. Dropdown opens on click and closes on Escape |
| Language switch | TR button changes `<h1>` and `lang`, and TR persists to `/platform/` |
| Hero, desktop 1440, motion allowed | one `orbgss-hero.webm` request (200), state `playing` for the 11.5 s clip, then `held` with the payoff (drape) on; no console error. The MP4 fallback is not exercised by this Chromium build |
| Hero, `prefers-reduced-motion: reduce` | state `static`, video has no `src`, **no video request**, payoff on the held base |
| Hero, mobile 390 @2×, touch | state `static` (small-screen path), no video `src`, **no video request** |
| Hero, JavaScript disabled | poster image renders; `<h1>` present |
| Act 3 evidence radios (Terrain / Thermal / Alteration) and inspection aid (Thermal / Alteration / Priority), EN and TR | each selects, and every visible image is loaded; no console error |
| Mobile menu at 390 | opens and closes (`aria-expanded`), Solutions disclosure shows the three domain links with their `/solutions/#…` targets |

One audit-script correction is disclosed: the first run of the interaction script failed a `>= 5 visible links` threshold on the mobile menu because Solutions is a disclosure button and its links are hidden until it is opened; the threshold was mine, not a defect, and the script now opens the disclosure and asserts the three domain links. Both logs in `evidence/mer213/` are from the corrected script.

Observation, not a defect: at 768 px one below-the-fold `ili-delta-2020-900.webp` (the Solutions Marine photograph, `loading` deferred) was still in flight when the check sampled `img.complete`; it is not broken (0 broken images at every viewport) and loaded on the other viewports.

## 4. Defect inventory

**Confirmed defects: 0.** No code, copy, asset or manifest change was made or is proposed by this audit.

Not confirmed or out of scope, listed so nothing is silently dropped:

- Hero validator 13 failures — environmental (section 2).
- Navigation drift between the Claude Project instructions and the repository — a CTO decision, not a website defect (section 6).
- `404.html` is English-only and Turkish is client-rendered only (no per-language URLs, no `hreflang`) — known, accepted architecture; the earlier audit also noted no JSON-LD. Not touched.
- `CONTACT_RELEASE_GATE` — mailbox ownership cannot be evidenced from a static repository.

## 5. What this audit did not cover

- **Production itself:** not fetched (proxy blocks raw HTTP to the domain; Vercel returns 403). Production/baseline equality rests on the MER-213 Linear record. A CTO-side check of `dpl_FmP2d8LkVrst84SVzVnFEyuEDpLn` against `79cc2cb` remains the authoritative confirmation.
- Other browser engines (Firefox, WebKit), real devices, the H.264 MP4 fallback, Lighthouse/Core Web Vitals, and screen-reader passes. No performance number is claimed.
- Hover, keyboard-only traversal and the visual fidelity of the imagery beyond "loads, no overflow, no error"; hero and Act visuals are unchanged from the accepted baseline and were not redesigned or re-evaluated.

## 6. Documentation reconciliation (changed paths)

| Path | Change |
| --- | --- |
| `STATUS.md` | New current-state block at the top (launched baseline table, short-command contract, validator results, open gates and decisions); the pre-launch R3/R11–R15 notes are kept and marked as history; "Production blockers" and "Next canonical task" rewritten (they still said WEB-005A `REVISION_REQUIRED`, nothing deployed, WEB-006 not started); tracking and history lines updated |
| `CLAUDE.md` | "Branching" rewritten to the verified baseline and the stale-`main` warning; new **Task execution rule** for `MER-###'e başla`; a sentence recording the hero-validator limitation. **No design invariant, imagery, claim or deployment rule was touched** |
| `README.md` | Validation command list, current-state paragraph (it still named WEB-001 as the next task) |
| `docs/HANDOFF.md` | Rewritten to the current state (it described the ORBWEB-001 era and the `baran-orbgss/website` publication) |
| `docs/WEB_VNEXT_AUTHORITY.md` | Section 10 task-sequence status lines only (WEB-004 → WEB-006, plus the milestone-5 pointer) |
| `CLAUDE_SESSION_BOOTSTRAP.txt` | Replaced the pre-vNext bootstrap prompt (separator beams, metadata strips) with one that matches the invariants and the short-command rule |
| `tasks/MER-213_POST_LAUNCH_AUDIT_EVIDENCE.md`, `evidence/mer213/*` | This record and the audit tooling/logs |

Deliberately **not** changed: `index.html`, `styles.css`, `script.js`, `sitemap.xml`, `vercel.json`, every asset, `assets/imagery/sources.json`, `hero/`, `scripts/`, and all product semantics and copy.

**Unresolved drift, for the CTO:** the Claude Project instructions describe *Home / Solutions (Geothermal, Mining, Marine) / About / Partner with us*; the repository (`CLAUDE.md`) and the live site use *Platform / Solutions / Pilot / Company / Contact / EN | TR*. The Solutions taxonomy already agrees. `CLAUDE.md` remains authoritative for implementation until the CTO decides; nothing was changed to favour either.

## 7. Delivery path and `main` sync preparation

**Delivery path:** local edit, diff and commit on the bounded task branch, and a normal authenticated non-force push of `claude/mer-213-bp01w5` to `origin`, were exercised for this task (result and the local/remote HEAD match are in the hand-off). The branch is a plain fast-forward descendant of `79cc2cb`, so later MER issues can branch from `79cc2cb` (or from `main` after the sync) with no rebase or history rewrite. `main` was not touched. Nothing was deployed; Vercel, DNS and credentials were not accessed for writing.

**Main-sync preparation (not executed — needs CTO approval).** Immediately before hand-off the ancestry was re-confirmed against a fresh fetch: `origin/main` is still `00af0f232a8d7d77f5ca61d758461ff7316ba151`, still an ancestor of the baseline and of the task branch, with no divergence. Expected direction is a **non-force fast-forward**, with no merge commit, squash, rebase or history rewrite. Two options, recommended first:

1. Fast-forward `main` to the reviewed MER-213 head (baseline `79cc2cb` plus this documentation/evidence commit). The delta over the baseline is documentation and evidence only, so the served site content is identical to production:
   ```bash
   git fetch origin
   git merge-base --is-ancestor origin/main origin/claude/mer-213-bp01w5 && echo ANCESTOR_OK   # must print ANCESTOR_OK
   git push origin origin/claude/mer-213-bp01w5:refs/heads/main                                  # no --force
   ```
2. Fast-forward `main` to exactly the accepted release candidate first, then the documentation commit as a second fast-forward:
   ```bash
   git push origin 79cc2cb82a4542461cbbfc1d0c349cf02b861084:refs/heads/main                       # no --force
   ```
Either push is rejected by Git if `main` has moved, which is the intended safety property; if it is rejected, stop and re-audit rather than force. Note the hosting interaction: whether pushing to `main` triggers a Vercel Git deployment depends on the Vercel project's Git settings, which could not be read here (production is recorded as a `cli` deployment). The CTO should confirm that before the push, since a deployment is a separate gate.

**Result: `READY_FOR_MAIN_SYNC_REVIEW`** — with the two limitations above stated plainly: production equality is Linear-recorded rather than re-verified here, and the hero validator's authoritative run belongs on the hero workstation.
