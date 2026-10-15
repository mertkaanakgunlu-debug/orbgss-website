# MER-219 — publication and production preflight gate

**Linear:** MER-219 (revised 2026-10-15: the publication head is the accepted MER-237 head).
**Branch:** `mertkaanakgunlu/mer-219-website-mer-218-publication-production-preflight-gate`, created from the publication target `2517369e` so this record sits on the same chain.
**Publication target:** `mertkaanakgunlu/mer-237-web-sitesi-ic-dosyalari-canli-yayindan-kaldir@2517369e0f0c4239d72603a3188227554053a6ea` (MER-237, accepted by the CTO 2026-10-15).
**Date:** 2026-10-15.

## 0. Gate status

**`BLOCKED_LIVE_VERCEL_STATE`** — not `READY_FOR_CTO_APPROVAL`.

* **What is done:**
  * Git preflight: complete and clean.
  * Topology: classified **`COUPLED`** from live, observed behaviour.
  * Production identity: verified.
  * Rollback contract, publication sequence, an executable smoke check with its pre-publication baseline, and the reconciliation plan: all written.
* **What blocks:** this environment cannot read the Vercel project. The Vercel connector is authorized for 0 teams. The built-in browser has no Vercel session, and signing in is not an agent action. No Vercel CLI is installed. Preview deployments sit behind Vercel Authentication.
* **Unread as a result:** the project settings that confirm the observation, and the current production deployment's id and alias state (§2.2). §8 gives three ways to clear the block.

Nothing in Git, Vercel, DNS, domains, credentials or production was changed by this preflight.

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

### 2.2 Not readable from this environment

| Item | Why it matters |
| --- | --- |
| Production Branch setting | Confirms `main` is still the production branch |
| Auto-assignment of production domains | An Instant Rollback since 2026-10-02 would have switched it off, and a `main` push would then not go live |
| Framework preset, build command, output and root directory, ignored-build step | Confirms nothing overrides the repository-root static deploy |
| Current production deployment id and aliases | The exact rollback target |
| Plan tier | Hobby can roll back only to the immediately previous production deployment |
| Deployment file tree | Direct proof that `.vercelignore` is applied to Git deployments. The preview is protected, so the smoke check (§5) proves it after publication instead |

Attempts made: Vercel MCP `list_teams` → 0 teams, and `list_deployments` (scope `virga-soft`) → 403; protection-bypass fetch of the preview → 403; the built-in browser at `vercel.com/virga-soft/orbgss-website/settings/git` → login page (not signed in; signing in is not an agent action); no Vercel CLI.

## 3. Release topology

**`COUPLED`.** Fast-forwarding `main` deploys production by itself. The most recent `main` push produced a production deployment 17 seconds later, and that deployment is what orbgss.com serves today.

This is observed behaviour, not a read of the settings. §2.2 is what would rule out a change since 2026-10-02 (for example a rollback that switched auto-assignment off).

**Consequence:** the `git push` in §1 *is* the production deployment. No separate deploy step exists, and none may be added by an agent.

## 4. Rollback contract (prepared, not executed)

| Layer | Pre-publication state | Rollback |
| --- | --- | --- |
| Production | GitHub deployment `6803748076` → `https://orbgss-website-p0heuwii3-virga-soft.vercel.app` (`f4f1d4d6`; Linear: `dpl_3NNNhqPozget7tpP1XfqCvMqWbJG`), aliased to `orbgss.com` | **Instant Rollback** to that deployment: Vercel dashboard → project → Production Deployment tile → Instant Rollback, or `vercel rollback <url>`. No rebuild, routing-level, seconds. It is eligible because it was aliased to production. On Hobby it qualifies only while it is the immediately previous production deployment, so roll back before anything else deploys to production. |
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

* **§2.2** is unread (the gate blocker).
* **`.vercelignore` on Git deployments** has not been observed directly. The previews are protected and the dashboard is unreadable. The §5 smoke proves it on production within a minute of publication, and §4 restores the previous state if it fails.
* **The GitHub repository is public.** Removing the internal files from orbgss.com (MER-237) does not make them private: `STATUS.md`, `tasks/`, `evidence/` and the rest stay readable on GitHub. Whether the repository should be private is a CTO decision. Vercel can deploy from a private repository, but it is a settings and plan question this preflight does not answer.
* **No physical-device acceptance** (carried from MER-216).
* **Production has been set outside `main` before** (the `79cc2cb` CLI deployment). Any future CLI or promote action bypasses this sequence.

## 8. Clearing the block — the CTO picks one

1. **Authorize the Vercel connector for team `virga-soft`**, then reply "MER-219'a devam et". The agent then reads the §2.2 items (project, settings, current production deployment, plan) and the gate becomes `READY_FOR_CTO_APPROVAL` if they agree with §2.1.
2. **Read the dashboard yourself** and report:
   * Settings → Git → Production Branch;
   * Settings → Build & Deployment → framework preset, build command, output and root directory;
   * the production deployment tile: deployment id, commit `f4f1d4d6`, domains, and whether it shows a rolled-back state;
   * the plan tier.

   The agent records them and closes the gate.
3. **Accept the observed evidence** in §2.1 and §3 as sufficient, and approve publication with Instant Rollback (§4) as the safety net.
