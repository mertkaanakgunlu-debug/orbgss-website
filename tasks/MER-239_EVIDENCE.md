# MER-239 — documentation and authority reconciliation (evidence)

**Linear:** MER-239 "Web sitesi: belge ve otorite uzlaştırması" (Milestone 6).
**Branch:** `mertkaanakgunlu/mer-239-web-sitesi-belge-ve-otorite-uzlastirmasi`
**Baseline:** the published `main@2517369e0f0c4239d72603a3188227554053a6ea` (MER-216 + MER-218 + MER-237, published 2026-10-15 by MER-219), verified by a fresh fetch. The branch tracks no upstream, so a bare `git push` can never reach `main`.
**State at handoff:** `REVIEW_READY`. Documentation only, apart from metadata fields in `assets/imagery/sources.json`. No page, style, script, asset, route, Vercel setting or DNS record changed.

## 1. What the branch carries

| Commit | Content |
| --- | --- |
| `374b846` … `bd105ce` (fast-forward) | MER-219 preflight and publication record (`tasks/MER-219_PREFLIGHT.md`, `evidence/mer219/`), so the publication evidence reaches `main` with this task |
| `e8f54e8` (merge) | The CTO-approved MER-238 branch at `0041203` (content `663e6342`, decision `00412036`), merged so the approved commits stay reachable. One conflict: the status line both branches added to the top of `STATUS.md`; both were kept, then rewritten in the next commit |
| `e9e1f1b` | Current state reconciled in `STATUS.md`, `CLAUDE.md`, `README.md`, `docs/HANDOFF.md`; MER-238 codified in `CLAUDE.md`; `AGENTS.md` pointer |
| `a3e7aec` | vNext, design and product authorities |
| `1375bf0` | `IMAGERY_RIGHTS.md`, `sources.json` metadata, `hero/README.md`, `CHANGELOG.md` |
| this commit | `STATUS.md` deploy note correction and this record |

## 2. AGENTS.md (CTO decision, 2026-10-15)

The CTO chose "Kısa yönlendirme": the untracked WEB-001-era `AGENTS.md` (88 lines: six-scene homepage, old taxonomy, old branching) is replaced by a committed eight-line pointer. It says `CLAUDE.md` is the single authority for every coding agent and holds no rules of its own. `.vercelignore` already keeps `AGENTS.md` out of the deploy.

## 3. Stale statements fixed (file:line after this change)

| File:line | Was | Now |
| --- | --- | --- |
| `STATUS.md:3–5` | Canonical version rc10 "launched baseline"; date 2026-10-03; stage Milestone 5, MER-216 "not published" | Published `main@2517369e`, reconciled 2026-10-15, stage Milestone 6 |
| `STATUS.md:7–17` | Table: `main` = `f4f1d4d6`; "Accepted, unpublished artifact"; production `f4f1d4d6` (Linear-sourced); task branches before publication | Current-state table: public repository, `main` history, COUPLED production and deployment `7094313382`, rollback target, deploy set, agent Vercel access, branches |
| `STATUS.md:19–26` | Product state and navigation as the only truth | Live product plus the approved MER-238 target |
| `STATUS.md:28–40` | (none) | Milestone 6 issue table |
| `STATUS.md:42–44` | "MER-216 … not yet published"; "`main` remains `f4f1d4d6`" | Published 2026-10-15 |
| `STATUS.md:61–67` | Validators at `79cc2cb` (2026-09-29) | Validators on this branch (§4) and production smoke |
| `STATUS.md:70–77` | Open gates: publication pending; IA conflict unresolved; production record missing | Publication closed; IA resolved; production recorded; plus the public-repository decision, agent Vercel access and MER-238 D3 / D5 |
| `STATUS.md:404` | Positioning with Mineral Exploration / Environmental & Land Intelligence | Geothermal / Mining / Marine |
| `STATUS.md:408–410` | Production blockers referring to the pre-publication state | None; `CONTACT_RELEASE_GATE` as MER-238 D4 |
| `STATUS.md:412–419` | Next task: MER-218 `REVIEW_READY`; publication pending | MER-239 → MER-240 → MER-241; MER-242 in parallel |
| `STATUS.md:436–443` | History: MER-213 "is `main`"; MER-216 "not published"; MER-218 `REVIEW_READY` | Corrected; MER-237, MER-238, MER-219 and MER-239 added |
| `CLAUDE.md:9–16` | Bootstrap order without the Milestone 6 authority | `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` second; it wins on pages, navigation, URLs and content rules |
| `CLAUDE.md:35, 37` | Supporting sections and the deep-route beam grammar as fixed | Live versus Milestone 6 target |
| `CLAUDE.md:39` | GEO-WEB-002 package "still bound by `/pilot/`" (no `/pilot/` file uses it) | Deployed under `assets/proof/final/`, placed on no page; `/pilot/` shows `web_002.proof_assets` |
| `CLAUDE.md:45–47` | Navigation, Solutions-card targets and client-side-only TR as the sole rules | Live rule plus approved target for each |
| `CLAUDE.md:56–83` | (none) | "Milestone 6 target" section: pages, redirects, Turkish slugs, homepage changes, R1–R8, D1–D5 |
| `CLAUDE.md:106–112` | Branching: `main` = `f4f1d4d6`, "Accepted, unpublished artifact", production does not serve MER-216 | `main` = production = `2517369e`, COUPLED topology, provenance heads up to MER-237 |
| `CLAUDE.md:134–135` | Deployment safety without a publication procedure | Publication per MER-219 §5, rollback per §4. Rule 6 stands; the one CTO authorization on record is scoped to MER-219 |
| `README.md:13–19` | Bootstrap list without the Milestone 6 authority | Added |
| `README.md:59` | `main` = `f4f1d4d6`, MER-216 unpublished, MER-218 `REVIEW_READY` | Published state, COUPLED, next task MER-240 |
| `docs/HANDOFF.md:3–19` | MER-218-era state, unresolved IA, unpublished MER-216 | Published state, Milestone 6, open items |
| `docs/WEB_VNEXT_AUTHORITY.md:9` | WEB-004 `REVIEW_READY` | Accepted at `56cb530` |
| `docs/WEB_VNEXT_AUTHORITY.md:12–13` | (none) | Reconciliation note |
| `docs/WEB_VNEXT_AUTHORITY.md:27–31` | Mineral Exploration / Environmental & Land Intelligence | Geothermal / Mining / Marine, with the old labels marked superseded |
| `docs/WEB_VNEXT_AUTHORITY.md:45, 54, 58` | Routes, navigation and the Solutions disclosure as final | Live, with the approved target |
| `docs/WEB_VNEXT_AUTHORITY.md:125–128` | WEB-006 without execution; MER-213 `REVIEW_READY`; MER-143 / 144 blocked | WEB-006 executed; Milestones 5 and 6 recorded |
| `docs/DESIGN_AUTHORITY.md:5–6, 11` | WEB-001 structural rhythm as current | Marked superseded by WEB-005 (history) |
| `docs/DESIGN_AUTHORITY.md:85–92` | Navigation order fixed (WEB-001); anchors; old dropdown labels | Live and target order; real pages; Geothermal / Mining / Marine |
| `docs/PRODUCT_AND_CONTENT_AUTHORITY.md:5–6` | (none) | Reconciliation note |
| `docs/PRODUCT_AND_CONTENT_AUTHORITY.md:25–27` | Old taxonomy | Geothermal / Mining / Marine |
| `docs/PRODUCT_AND_CONTENT_AUTHORITY.md:31` | WEB-001 navigation table presented as current | Marked history |
| `docs/PRODUCT_AND_CONTENT_AUTHORITY.md:96` | Contact "must be confirmed before production launch" | `CONTACT_RELEASE_GATE` as MER-238 D4 |
| `IMAGERY_RIGHTS.md:1, 13–16` | Class table without WEB-005B / MER-151; "older gallery scenes are retired" | Records, uses and the MER-151 exception |
| `IMAGERY_RIGHTS.md:53, 61, 70, 95` | Scene headings "hero", "mineral", "environmental" | Former hero (retired); mining, marine and geothermal Solutions-card photographs |
| `IMAGERY_RIGHTS.md:87–95` | Kızıldere GEO-WEB-002 master "not yet placed on any route" | Superseded on the homepage, unplaced; new WEB-005B natural-colour master subsection |
| `IMAGERY_RIGHTS.md:105` | WEB-002 section silent on where its exports now appear | Shown on `/pilot/` since WEB-005 |
| `IMAGERY_RIGHTS.md:134–138` | GEO-WEB-002 "Nothing … is placed on a public route yet" | Role taken over by WEB-005B; deployed, unplaced; MER-242 |
| `IMAGERY_RIGHTS.md:159–177` | (none) | Class B section for the MER-151 homepage derivatives |
| `IMAGERY_RIGHTS.md:185–188` | "nothing on any route references them" | Three scenes placed as Solutions-card photographs; Crater Lake unplaced |
| `IMAGERY_RIGHTS.md:197–199` | Hero files `orbgss-hero.webm` / `.mp4` (deleted) | The MER-216 ladder, the stills, the drape and rise states; the records |
| `IMAGERY_RIGHTS.md:209, 226` | No drape note; deployment gate as pre-launch | Lossless drape note; gate in force since WEB-006 and MER-237 |
| `assets/imagery/sources.json:2–3` | `version` 0.8; policy "Only the hero is still placed", GEO-WEB-002 "not yet placed" | `0.9-mer-239-reconciled`; current placement, plus classes (4) hero and (5) MER-151 |
| `assets/imagery/sources.json:106` | Yellowstone `source_data` "… ASTER GDEM terrain rendering" (its production block uses Landsat only) | ASTER attributed to the NASA reference rendering only |
| `assets/imagery/sources.json:237, 353` | Scene roles `mineral`, `environment` | `mining`, `marine` (no code reads these values; the validator checks presence only) |
| `assets/imagery/sources.json:478` | `web_vnext.rule` "Story panels 01-06 … must be added to `web_002.proof_assets`" | WEB-002 panels on `/pilot/`; any of the three scientific records |
| `assets/imagery/sources.json:2139` | `web_005.state` `review_ready` | `accepted` |
| `hero/README.md:5` | Cites `docs/WEB_HERO_001_AUTHORITY.md`, absent from `main` | Points to `CLAUDE.md` and `lane.json`; records that the file lives on `feat/web-hero-001-predata-scene` |
| `hero/README.md:11–12` | Current state stops at WEB-005A R3 | WEB-005A terminal and MER-216 |
| `hero/README.md:30` | Isolation rule only | Integration mode since WEB-005 |
| `tasks/MER-237_EVIDENCE.md:6` | `REVIEW_READY` only | Accepted and published; section 8 item closed in production |
| `CHANGELOG.md:3–33` | Nothing after WEB-005B R15 | WEB-005C (rc10) through MER-239 |

**Left as is, on purpose:**

* `hero/config/lane.json` still lists `docs/WEB_HERO_001_AUTHORITY.md` under `write_surface.allowed_bounded_files`. That is a write permission for the hero lane, not a citation, and editing `lane.json` would move the hero validator's contract for no gain.
* Sections already labelled as history (`STATUS.md` "Superseded pre-launch status", the WEB-001 tables in the product authority, older changelog entries) keep their dated wording.

## 4. Verification (this branch, 2026-10-15)

| Command | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` | PASS, 0 warnings: 4 scenes, 6 routes, 268 i18n keys, 6 geo-web-002 assets / 19 files, deploy set 14 root entries / 110 files |
| `negative_tests_web005.py` / `_web005b.py` / `_web005c.py` / `_mer216.py` / `_mer237.py` | 72/72, 55/55, 18/18, 19/19, 29/29; restored trees identical (site and hero) |
| `py -3.14 hero/scripts/validate_hero.py` | 420 checks, 0 failed (hero workstation) |
| `py -3.14 scripts/check_copy_preservation.py 2517369e…` | 0 visible-copy differences |
| Site-file diff against `main` | None. Pages, `styles.css`, `script.js`, `vercel.json`, `.vercelignore`, `robots.txt`, `sitemap.xml` and `site.webmanifest` are all unchanged. |
| `sources.json` guard | A structural comparison excluding only the seven edited metadata fields proves every other value identical |

## 5. Publication note

Production is COUPLED, so publishing this branch (a fast-forward of `main`) redeploys production.

* **What changes on the live site:** only `assets/imagery/sources.json`, in its metadata. Every other changed path is outside the deploy set.
* **Caching:** `/assets/` is served with `Cache-Control: immutable` for a year, so a browser that already cached the old manifest keeps it until expiry. It is metadata only; no page reads it at runtime.
* **Process:** publishing stays a CTO gate and follows `tasks/MER-219_PREFLIGHT.md` §5.
