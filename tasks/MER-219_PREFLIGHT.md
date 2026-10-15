# MER-219 — publication and production preflight gate

**Linear:** MER-219 (revised 2026-10-15: the publication head is the accepted MER-237 head).
**Branch:** `mertkaanakgunlu/mer-219-website-mer-218-publication-production-preflight-gate`, created from the publication target `2517369e` so this record sits on the same chain.
**Publication target:** `mertkaanakgunlu/mer-237-web-sitesi-ic-dosyalari-canli-yayindan-kaldir@2517369e0f0c4239d72603a3188227554053a6ea` (MER-237, accepted by the CTO 2026-10-15).
**Date:** 2026-10-15.

## 0. Gate status

**`READY_FOR_CTO_APPROVAL`** (revised 2026-10-15). The first pass stopped at `BLOCKED_LIVE_VERCEL_STATE`, because the agent's environment cannot read the Vercel project:

* the Vercel connector is authorized for 0 teams, and reconnecting did not change that in this session;
* the built-in browser has no Vercel session, and signing in is not an agent action;
* no Vercel CLI is installed.

The CTO then read the production overview in the Vercel dashboard (§2.1b), which supplies what the block was about: the current production deployment, its source branch and commit, its domains and its health. The settings still unread (§2.2) are recorded with the reason each one does not block.

* **Done:** the Git preflight (clean); the topology, **`COUPLED`**, confirmed from both GitHub and the dashboard; production identity; the rollback contract; the publication sequence; an executable smoke check with its pre-publication baseline; the reconciliation plan.
* **Changed by this preflight:** nothing in Git, Vercel, DNS, domains, credentials or production.

## 1. Git publication preflight (fresh fetch, 2026-10-15)

| Fact | Value |
| --- | --- |
| Repository | `mertkaanakgunlu-debug/orbgss-website`; default branch `main`; **public**; `main` has no branch protection |
| `origin/main` | `f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85` |
| MER-216 head | `adf08186d3ee4a438bda73886272d05c970e670a` |
| MER-218 head | `5ca7bdd4167020fc0f7dd5a58b017495de9002fe` |
| MER-237 head (target) | `2517369e0f0c4239d72603a3188227554053a6ea` |
| Ancestry | `f4f1d4d6` → `1e58031c` → `ef51cdb` → `adf08186` → `5ca7bdd4` → `58cbb7b8` → `2517369e`; every link verified with `git merge-base --is-ancestor` |
| `main...2517369e` | 0 behind / 6 ahead: a pure fast-forward; no merge, rebase or squash needed |
| Not included | MER-238 (`0041203…`) is a sibling branch from `5ca7bdd4` and is not part of this publication |

**Publication command (non-force; Git rejects it if it is not a fast-forward):**

```bash
git fetch origin
test "$(git rev-parse origin/main)" = f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85
git merge-base --is-ancestor origin/main 2517369e0f0c4239d72603a3188227554053a6ea
git push origin 2517369e0f0c4239d72603a3188227554053a6ea:refs/heads/main
```

**Git rollback pointer:** `f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85`. History is never rewritten; see §4.

## 2. Vercel state

### 2.1 Observed (live, 2026-10-15, through GitHub and public HTTP)

| Item | Evidence | Finding |
| --- | --- | --- |
| Project and scope | Vercel commit statuses point to `vercel.com/virga-soft/orbgss-website/…`; deployment hosts are `orbgss-website-*-virga-soft.vercel.app` | Project `orbgss-website`, team `virga-soft` |
| Git integration | `vercel[bot]` creates a GitHub deployment and a `Vercel` commit status for every pushed head | Enabled |
| Branch pushes | Preview records for every task-branch head, from `f4f1d4d6` (2026-09-29) to `00412036` (2026-10-15 11:25:42Z) | Every branch push builds a Preview |
| `main` pushes | GitHub activity: `main` pushed `00af0f23` → `f4f1d4d6` at **2026-10-02T07:42:45Z**. GitHub deployment `6803748076`, environment **Production**, `f4f1d4d6`, created **07:43:02Z** (+17 s), status success, `https://orbgss-website-p0heuwii3-virga-soft.vercel.app` | A push to `main` produced a production deployment by itself |
| Production identity now | `index.html`, `script.js`, `styles.css`, and the exposed `STATUS.md` and `CLAUDE.md`, are byte-identical to `f4f1d4d6`. `STATUS.md` and `CLAUDE.md` match no other commit. | orbgss.com serves `f4f1d4d6` |
| Linear record | MER-216 review (2026-10-03): `dpl_3NNNhqPozget7tpP1XfqCvMqWbJG`, READY, production, source git, `main`, `f4f1d4d6` | Consistent with the above |
| Earlier production deployments | `00af0f23` at 2026-09-20 22:15 (`main` had held it since 09-16, so this was not push-triggered). `79cc2cb8` at 2026-09-20 23:12, a commit that was never on `main`; `STATUS.md` records it as source `cli`. | Production has also been set outside `main` (CLI / promote) |
| Domains and HTTP | `https://orbgss.com/` 200, `Server: Vercel`, `X-Vercel-Cache: HIT`; `www` → apex 308; `http` → `https` 308; `Strict-Transport-Security: max-age=63072000` | Apex canonical, redirects in place |
| `vercel.json` effect | The live headers (`nosniff`, `Referrer-Policy`, `Permissions-Policy`, `X-Frame-Options`) match `vercel.json`; `/vercel.json` itself returns 404 | Repository config is applied |
| `.vercelignore` build | Preview builds of `58cbb7b8` and `2517369e` (allowlist present) report success | The allowlist does not break the build |
| Environment differences | The site is static; `script.js` and the pages read no environment variables | None the site depends on |

### 2.1b Read by the CTO in the Vercel dashboard (2026-10-15)

The CTO shared a screenshot of `vercel.com/virga-soft/orbgss-website` (Overview). The screenshot is not committed: the repository is public, and it shows the CTO's browser. Its content:

| Field | Value |
| --- | --- |
| Production deployment | `orbgss-website-p0heuwii3-virga-soft.vercel.app`, the same deployment as GitHub deployment `6803748076` |
| Domains | `orbgss.com`, `orbgss-website.vercel.app` (`www` answers with a 308 to the apex, §2.1) |
| Status | **Ready** |
| Created | Oct 2, "by claude". This is the Git commit author of `f4f1d4d6` (`Claude <noreply@anthropic.com>`), not a Vercel account or a CLI deploy |
| Source | branch **`main`**, commit **`f4f1d4d6`** "docs(mer-213): reconcile repository docs with the launched baseline an…" |
| Build settings | On-Demand Concurrent Builds disabled; Build Machine Basic (2 vCPU / 8 GB); Prioritize Production Builds enabled |
| Runtime settings | Fluid Compute enabled; Function CPU Standard. Not relevant to a static site with no functions |
| Rollback state | No rolled-back state is visible on the production tile. The production deployment is also the newest production record (§2.1); a rollback since Oct 2 would point at an older one |

### 2.2 Still not read, and why none of it blocks


| Item | Why it does not block |
| --- | --- |
| Settings → Git → Production Branch (literal value) | The production deployment's source is `main` (dashboard), and the last `main` push created it within 17 s (GitHub). Both say the production branch is `main`. |
| Settings → Environments → auto-assignment of custom production domains | The production deployment carries `orbgss.com` and was assigned when the push created it. No rollback is in effect (§2.1b), and that is the only automatic way the setting turns off. If it had been switched off by hand, the push would build without going live: §5 step 3 shows it within a minute, and §5 step 4 fails the identity check. |
| Framework preset, build and output settings | Production serves the repository root as a static site today, byte-identical to `f4f1d4d6`, and the `2517369e` preview built successfully, so the same settings serve this release. |
| Plan tier | Rollback to the immediately previous production deployment works on every plan. After publication that deployment is `p0heuwii3` (§4). |
| Deployment file tree (`.vercelignore` applied) | The §5 smoke proves it on production; §4 restores the previous state if it fails. |
| Deployment Protection (cut off in the screenshot) | Previews answer 302 to Vercel Authentication (observed), and production on `orbgss.com` is public (observed). |

Attempts made: Vercel MCP `list_teams` → 0 teams, and `list_deployments` (scope `virga-soft`) → 403; protection-bypass fetch of the preview → 403; the built-in browser at `vercel.com/virga-soft/orbgss-website/settings/git` → login page (not signed in; signing in is not an agent action); no Vercel CLI.

## 3. Release topology

**`COUPLED`.** Fast-forwarding `main` deploys production by itself. The most recent `main` push produced a production deployment 17 seconds later, and that deployment is what orbgss.com serves today.

Confirmed by the dashboard (§2.1b): the deployment serving `orbgss.com` has source `main` / `f4f1d4d6` and no rolled-back state. The settings left unread are covered in §2.2.

**Consequence:** the `git push` in §1 *is* the production deployment. No separate deploy step exists, and none may be added by an agent.

## 4. Rollback contract (prepared, not executed)

| Layer | Pre-publication state | Rollback |
| --- | --- | --- |
| Production | `orbgss-website-p0heuwii3-virga-soft.vercel.app`: dashboard Ready, source `main` / `f4f1d4d6`, domains `orbgss.com` and `orbgss-website.vercel.app`; GitHub deployment `6803748076`; Linear `dpl_3NNNhqPozget7tpP1XfqCvMqWbJG` | **Instant Rollback** to that deployment: Vercel dashboard → project → Production Deployment tile → Instant Rollback, or `vercel rollback <url>`. No rebuild, routing-level, seconds. It is eligible because it was aliased to production. On Hobby it qualifies only while it is the immediately previous production deployment, so roll back before anything else deploys to production. |
| After a rollback | — | Vercel switches off auto-assignment of production domains, so later `main` pushes do not go live until **Undo Rollback** (dashboard) or `vercel promote <deployment>` is used. Record which was used. |
| Git | `main@f4f1d4d6` | Never force-push or reset `main`. If `main` must carry the rollback: `git revert --no-edit f4f1d4d6..2517369e` on a branch, reviewed, then a normal fast-forward push. Because the topology is COUPLED, that push deploys the reverted content. Normally: Instant Rollback first, then fix forward. |
| DNS and mail | Squarespace DNS; Google Workspace MX / SPF / DKIM / DMARC | No rollback path touches DNS, domains or mail records |

Who: the CTO, as a member of `virga-soft` with production rights. No agent executes a rollback.

## 5. Publication sequence and acceptance checklist (COUPLED)

1. **Approve.** The CTO gives explicit approval in the conversation, after this preflight is reviewed and §8 is resolved.
2. **Guard, then push.** Run the §1 commands. If the guard fails, `main` moved: stop and re-run this preflight.
3. **Watch.** Run `gh api "repos/mertkaanakgunlu-debug/orbgss-website/deployments?sha=2517369e0f0c4239d72603a3188227554053a6ea&environment=Production"` until a Production record exists and its latest status is `success`. On 2026-10-02 this took 17 s.
4. **HTTP smoke.** Run `py -3.14 evidence/mer219/smoke_production.py --expect-sha 2517369e0f0c4239d72603a3188227554053a6ea`. Every check must pass: 46 once the hero ladder is present (38 today, because the 8 per-tier checks only run when the ladder exists):
   * HTTPS, the `www` and `http` redirects, HSTS;
   * the six routes and a real 404;
   * 15 internal paths not served;
   * every route's `og:image` self-hosted, loading, and not Crater Lake;
   * the MER-216 hero ladder in the markup, with every tier returning the right type, `immutable` caching and a 206 range response;
   * all homepage assets;
   * sitemap and robots;
   * `index.html`, `script.js` and `styles.css` byte-identical to `2517369e`.

   The pre-publication baseline is `evidence/mer219/baseline_smoke_2026-10-15.txt`: 23 / 38 pass. The 15 failures are exactly what this publication changes: internal files served, Crater Lake on four routes, no hero ladder, identity at `f4f1d4d6`.
5. **Browser checks** on production, in a real or headless browser:
   * hero: normal playback with one tier and codec chosen before any video byte; poster and held frame; reduced motion; no-JS; failure fallback (block the video URL);
   * Act 03 layer switching; the inspection wipe; navigation; EN / TR;
   * 1440 × 900 and 390 × 844;
   * zero console errors and no broken images;
   * palettes and NoData visually unchanged against the accepted MER-216 evidence.

   No physical Safari, Firefox, phone or 4K panel is available to the agent. Record that as a limitation; do not simulate it.
6. **If anything fails,** use the Instant Rollback in §4. Then re-run the smoke against `f4f1d4d6` to confirm the restore, and report.
7. **Then reconcile.** MER-239 applies §6.

## 6. Post-publication reconciliation plan (for MER-239; not executed here)

These lines go stale once `main` = `2517369e` and production serves it (line numbers at `2517369e`):

| File:lines | Today | After publication |
| --- | --- | --- |
| `STATUS.md:4–7` | Date, MER-237 `REVIEW_READY`, stage text "MER-216 … not published" | Published; production serves `2517369e` |
| `STATUS.md:15–19` | Launched-baseline table: `main` = `f4f1d4d6`; "Accepted, unpublished artifact"; production `f4f1d4d6`; task branches | `main` = `2517369e`; the new production deployment id from §5 step 3; "unpublished" row removed |
| `STATUS.md:23, 25` | "MER-216 … not yet published"; "`main` remains `f4f1d4d6`" | Published |
| `STATUS.md:52` | Open gate 1 (publication) | Closed, with the deployment record |
| `STATUS.md:396–397, 414–417` | Next-task list and history: MER-218 `REVIEW_READY`, publication pending | MER-218 / MER-237 / MER-219 outcomes |
| `CLAUDE.md:79–82` | Git `main`, "Accepted, unpublished artifact", "Production … does **not** serve MER-216", branching rule "until `main` is fast-forwarded" | `main` = `2517369e`; production serves it; new work branches from `main` |
| `README.md:58` | `main` = `f4f1d4d6`, MER-216 unpublished | Current |
| `docs/HANDOFF.md:7–8` | Launched baseline `79cc2cb`; MER-216 "3 ahead / 0 behind" | Current |
| `tasks/MER-237_EVIDENCE.md` header | `REVIEW_READY` | Accepted 2026-10-15; published at the recorded deployment |

## 7. Residual limitations and findings

* **§2.2** settings are not read literally; each is covered as stated there.
* **`.vercelignore` on Git deployments** has not been observed directly. The previews are protected and the dashboard is unreadable. The §5 smoke proves it on production within a minute of publication, and §4 restores the previous state if it fails.
* **The GitHub repository is public.** Removing the internal files from orbgss.com (MER-237) does not make them private: `STATUS.md`, `tasks/`, `evidence/` and the rest stay readable on GitHub. Whether the repository should be private is a CTO decision. Vercel can deploy from a private repository, but it is a settings and plan question this preflight does not answer.
* **No physical-device acceptance** (carried from MER-216).
* **Production has been set outside `main` before** (the `79cc2cb` CLI deployment). Any future CLI or promote action bypasses this sequence.

## 8. Next step

The CTO approves publication in the conversation, after whatever independent review the CTO requires. Then one of two things happens:

* the CTO runs the §1 commands, or
* the CTO explicitly authorizes the agent to run them, together with §5 steps 3–4 (watch and smoke).

Either way, the §4 rollback is the CTO's action in the Vercel dashboard. The connector cannot reach `virga-soft`, so the agent has no rollback path.

## 9. Publication record (2026-10-15)

The CTO approved publication and authorized the agent to run it: "Yayını onaylıyorum ve sana yetki veriyorum: main'i 2517369e'ye fast-forward et (önce main'in hala f4f1d4d6 olduğunu doğrula), production deploy'u izle ve smoke betiğini çalıştır."

| Step | Result |
| --- | --- |
| Guard (fresh fetch) | `origin/main` = `f4f1d4d6`; target `2517369e` present; `main` is its ancestor; 0 behind / 6 ahead |
| Push | 13:45:21Z `git push origin 2517369e…:refs/heads/main`, giving `f4f1d4d..2517369` (non-force fast-forward); `origin/main` = `2517369e0f0c4239d72603a3188227554053a6ea` |
| Production deployment | GitHub deployment `7094313382`, environment Production, status **success** at 13:45:33Z (+12 s); `https://orbgss-website-l0hjfxcdh-virga-soft.vercel.app`. The live `index.html` matched `2517369e` at 13:45:40Z. The Vercel `dpl_…` id is not readable here (connector has no team access). |
| HTTP smoke | `evidence/mer219/post_publication_smoke_2026-10-15.txt`: **46 / 46**. Internal paths return 404 on production, so `.vercelignore` is applied to Git deployments (the open MER-237 item, now closed). All routes and the redirects work; the og images are fixed; the hero ladder answers with the right types, 206 ranges and immutable cache; `index.html`, `script.js` and `styles.css` are byte-identical to `2517369e`. |
| Browser checks | `evidence/mer219/post_publication_browser_2026-10-15.txt` (`browser_checks_production.py`): **21 / 21**. Six routes × 1440 and 390 px show 0 console errors, 0 broken images and 0 overflow. On a 50 Mbit/s link the hero chose `md` / WebM, played, and requested one media file. Reduced motion keeps the held still with no video request; no-JS renders; Act 03 switches all three layers; EN → TR translates. |
| Measurement note | A fresh headless profile first estimates ~1.5 Mbit/s. MER-216's network gate then keeps the held still with `data-hero-reason="slow-network"` and requests no video: the designed slow-link fallback, not a defect. The checks cover both paths. |
| Not covered | Physical Safari / Firefox / phone / 4K panels (carried from MER-216). |

**Rollback target**, should one be needed: the previous production deployment `orbgss-website-p0heuwii3-virga-soft.vercel.app` (`f4f1d4d6`), now the immediately previous production deployment, so eligible on any plan. Use Instant Rollback in the Vercel dashboard (§4). None was needed.

**Next:** MER-239 applies §6 against the published `main`.
