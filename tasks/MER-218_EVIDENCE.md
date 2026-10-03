# MER-218 — Website: MER-216 canonical publication closure — evidence

**Linear:** MER-218 (related: MER-216, MER-143)
**State:** `REVIEW_READY` — the implementation agent does not self-accept or close the issue.
**Branch:** `mertkaanakgunlu/mer-218-website-mer-216-canonical-publication-closure` (the Linear branch name), created from exactly the accepted MER-216 head `adf08186d3ee4a438bda73886272d05c970e670a`
**Kind:** documentation only. No product, runtime, science or media byte changed.
**Not done, by design:** no `main` update, merge, rebase, squash or cherry-pick of MER-216 history, deploy, Vercel / DNS / domain / credential change, force-push, or Linear close.

---

## 1. Preflight (2026-10-03, fresh `git fetch origin --prune`)

| Fact | Required | Observed |
| --- | --- | --- |
| Repository | `mertkaanakgunlu-debug/orbgss-website` | `origin` = `https://github.com/mertkaanakgunlu-debug/orbgss-website.git` |
| `origin/main` | `f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85` | `f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85` |
| Accepted MER-216 branch | `claude/mer-216-s1r628` | present on `origin` |
| Accepted MER-216 HEAD | `adf08186d3ee4a438bda73886272d05c970e670a` | `origin/claude/mer-216-s1r628` = local = `adf08186d3ee4a438bda73886272d05c970e670a` |
| Linear MER-216 | Done | Done (completed 2026-10-03T14:05:53Z; final independent acceptance comment "MER-216 accepted") |
| Working tree | clean (tracked) | clean; one pre-existing **untracked** `AGENTS.md` (not part of this task, not touched, not committed) |

All facts matched, so the task proceeded. Baseline validator before any edit: `py -3.14 scripts/validate_site.py` → `RESULT: PASS`, 0 warnings.

## 2. Ancestry / fast-forward proof

| Check | Result |
| --- | --- |
| `git merge-base --is-ancestor f4f1d4d6… adf08186…` | exit 0 — `main` is an ancestor of the accepted MER-216 head |
| `git merge-base f4f1d4d adf0818` | `f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85` (= `main` itself) |
| `git rev-list --left-right --count f4f1d4d...adf0818` | `0  3` — 0 behind, 3 ahead |
| `f4f1d4d..adf0818`, linear, no merge commits | `1e58031c` (parent `f4f1d4d6`) → `ef51cdb2` (parent `1e58031c`) → `adf08186` (parent `ef51cdb2`) |
| MER-218 | one commit whose parent is exactly `adf08186`; reported SHA in the Linear handoff |

So `main@f4f1d4d6` → MER-216 `adf08186` → MER-218 closure head is one linear chain, and publishing it is a pure fast-forward. No MER-216 commit was rewritten, merged, rebased, squashed or cherry-picked.

## 3. What was stale, and what changed

Only demonstrably stale **current-state** text was changed. Historical / provenance sections are left verbatim.

| File | Stale current-state text | Reconciled to |
| --- | --- | --- |
| `STATUS.md` | Stage line and MER-216 section header: MER-216 `REVIEW_READY`; open gate 1 "after the independent review"; gate 5 and "Next canonical task" naming MER-216 as awaiting review; production row only carrying the older MER-213 record (`dpl_FmP…@79cc2cb`, source `cli`); task-branch row saying new work branches from `main` | MER-216 Done (accepted 2026-10-03) at `adf08186`, not published; `main` unchanged at `f4f1d4d6` (re-verified); a separate **accepted, unpublished artifact** row; production row adds the newer Linear record from the MER-216 review (`dpl_3NNNhqPozget7tpP1XfqCvMqWbJG`, READY, production, source `git`, `githubCommitRef=main`, SHA `f4f1d4d6`, code-identical to `79cc2cb`) and keeps the MER-213 record as the earlier one; branch rule = the baseline the Linear issue names; MER-218 is the next task; two History bullets appended. The MER-216 phase table is kept as the handoff state, with the guard count corrected to its own evidence (16 / 16 at the first reviewed head, 19 / 19 after the revision) |
| `CLAUDE.md` | Branching block: "Branch new work from this exact commit" `79cc2cb`; MER-216 `REVIEW_READY` | Three separately named states — Git `main` `f4f1d4d6`, accepted unpublished MER-216 artifact `adf08186`, production (launched code, not MER-216) — and the branching rule; `79cc2cb` and `00af0f2` moved into the provenance list, not deleted |
| `README.md` | "Current state" paragraph: `main@00af0f2` stale ancestor; MER-213 `REVIEW_READY`; MER-143 / MER-144 next | `main@f4f1d4d6`; MER-216 Done, not published; MER-218 `REVIEW_READY`; publication and deploy are CTO gates |
| `docs/HANDOFF.md` | "Where things stand": `main@00af0f2` ancestor, ahead 25; "not done": MER-143 / MER-144 blocked behind MER-213 | `main@f4f1d4d6` over the launched code; MER-216 accepted at `adf08186`, 3 ahead / 0 behind, unpublished; MER-143..146 canceled into MER-216 |
| `tasks/MER-218_EVIDENCE.md` | — | this record (new) |

Deliberately **not** changed (history / provenance, or outside the canonical set):

- `tasks/MER-216_EVIDENCE.md` — MER-216's own handoff record; its `REVIEW_READY` header is the state at its handoff. Acceptance is recorded in Linear, `STATUS.md` and here.
- `STATUS.md` below "Superseded pre-launch status (kept as history)", including the long *Tracking* line that still reads MER-216 `REVIEW_READY`; that section's own preamble says the sections above win where they disagree.
- `STATUS.md` "Validators (baseline `79cc2cb`, run 2026-09-29 for MER-213)" — a dated MER-213 result; current results are in §5 below.
- The existing MER-216 History bullet (`REVIEW_READY` on its branch, 2026-10-02 / 2026-10-03) — kept; a new dated bullet records the acceptance.
- `CLAUDE_SESSION_BOOTSTRAP.txt` and `CHANGELOG.md` — no stale current-state pointer to MER-216 or a stale baseline.

## 4. Zero product / runtime / science / media change

Changed-file inventory versus the accepted MER-216 head (`git diff --name-status adf08186 <MER-218 head>`):

```
M	CLAUDE.md
M	README.md
M	STATUS.md
M	docs/HANDOFF.md
A	tasks/MER-218_EVIDENCE.md
```

Protected-surface proof:

```
git diff --quiet adf08186d3ee4a438bda73886272d05c970e670a <MER-218 head> -- \
  assets script.js styles.css index.html 404.html platform solutions pilot company contact \
  hero scripts evidence vercel.json robots.txt sitemap.xml site.webmanifest IMAGERY_RIGHTS.md references
```

→ exit 0, empty diff. That covers every route HTML file, `assets/` (including `assets/imagery/sources.json` and every analytical derivative and hero encode), `hero/` (config, renders, evidence, scripts), the validators and the deployment config. `scripts/check_copy_preservation.py adf08186…` reports 0 visible-copy differences.

## 5. Validators (run on the MER-218 tree, 2026-10-03, CTO workstation)

| Command | Exit | Result |
| --- | --- | --- |
| `py -3.14 scripts/validate_site.py` (before edits) | 0 | `RESULT: PASS`, 0 warnings |
| `py -3.14 scripts/validate_site.py` | 0 | `RESULT: PASS` — 4 scenes, 29 html images, 6 routes, 268 i18n keys, 6 geo-web-002 assets / 19 files, 0 warnings |
| `py -3.14 scripts/negative_tests_web005.py` | 0 | 72 / 72 deliberate regressions caught; restored site and hero trees identical to baseline |
| `py -3.14 scripts/negative_tests_web005b.py` | 0 | 55 / 55 caught; restored tree identical |
| `py -3.14 scripts/negative_tests_web005c.py` | 0 | 18 / 18 caught; restored tree identical |
| `py -3.14 scripts/negative_tests_mer216.py` | 0 | 19 / 19 caught; restored tree identical |
| `py -3.14 hero/scripts/validate_hero.py` | 0 | 420 checks, 0 failed (hero workstation, local source textures present) |
| `py -3.14 scripts/check_copy_preservation.py adf08186d3ee4a438bda73886272d05c970e670a` | 0 | 0 visible-copy differences |
| `git diff --check` | 0 | clean |

No browser preview was run: nothing the dev server renders changed.

## 6. Future `main` publication operation — documented, **not executed**

To be run only on explicit CTO authorization, after MER-218 is accepted. `H` is the reviewed MER-218 head reported in the Linear handoff.

```bash
H=<reviewed MER-218 head from the Linear handoff>
git fetch origin --prune
test "$(git rev-parse origin/main)" = f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85
test "$(git rev-parse origin/mertkaanakgunlu/mer-218-website-mer-216-canonical-publication-closure)" = "$H"
git merge-base --is-ancestor origin/main "$H"
git merge-base --is-ancestor adf08186d3ee4a438bda73886272d05c970e670a "$H"
git push origin "$H":refs/heads/main
git ls-remote origin refs/heads/main
```

- The push carries **no** `--force` / `--force-with-lease`; GitHub rejects it unless it is a fast-forward, and every `test` / `--is-ancestor` line must exit 0 first. If `origin/main` has moved, stop and re-resolve the authority.
- The last line must print `H`. `main` then contains `79cc2cb` → `f4f1d4d6` → MER-216 (`1e58031c`, `ef51cdb2`, `adf08186`) → MER-218 unchanged.
- **Coupling risk for the CTO:** the latest production record is a Vercel deployment with `source=git` and `githubCommitRef=main`. If the Vercel Git integration still auto-deploys `main`, this push will itself start a production build of the MER-216 site. Decide the deployment gate before the push (or confirm auto-deploy is off), rather than treating the two as automatically separate.
- After publication, the current-state lines in `STATUS.md`, `CLAUDE.md`, `README.md` and `docs/HANDOFF.md` that say `main` is `f4f1d4d6` and MER-216 is unpublished become stale and need their own bounded reconciliation.

## 7. Residual risks

- The production state is Linear-sourced (MER-216 review record); MER-218 deliberately does not read or touch Vercel, so it is not independently re-verified here.
- MER-216's own residuals stand: no physical Safari / Firefox / phone / 4K-panel acceptance; production Vercel behaviour of the ladder not exercised.
- The untracked `AGENTS.md` on the workstation is outside every task and is not committed.
