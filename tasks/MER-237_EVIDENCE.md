# MER-237 — remove internal repository files from the live site (evidence)

**Linear:** MER-237 "Web sitesi: iç dosyaları canlı yayından kaldır" (Milestone 6, created 2026-10-15 by CTO decision).
**Branch:** `mertkaanakgunlu/mer-237-web-sitesi-ic-dosyalari-canli-yayindan-kaldir`
**Baseline:** `mertkaanakgunlu/mer-218-website-mer-216-canonical-publication-closure@5ca7bdd4167020fc0f7dd5a58b017495de9002fe` (MER-218, accepted)
**State at handoff:** `REVIEW_READY`. Implementation commit `58cbb7b8`; this record is completed by the follow-up commit that adds section 8. Nothing merged, published or deployed by this task (Vercel built a Preview on its own when the branch was pushed); no Vercel setting, DNS, domain or credential touched.

## 1. Problem

Vercel uploads and serves every repository file that `.vercelignore` does not exclude, and the
repository had no `.vercelignore`. On 2026-10-15 production returned HTTP 200 for
`/STATUS.md`, `/CLAUDE.md`, `/docs/HANDOFF.md`, `/tasks/MER-213_POST_LAUNCH_AUDIT_EVIDENCE.md`,
`/scripts/validate_site.py` and `/hero/config/scene.json` (checked with `curl`). `/vercel.json` and
`/.gitignore` returned 404 (Vercel does not serve its own config and ignores dotfiles by default).
A scan of tracked text files for credentials, tokens and private keys found nothing; what was
exposed is internal process, branch names, Vercel deployment ids and the Vercel scope name.

Separately, `/platform/`, `/solutions/`, `/company/` and `/contact/` still declared
`assets/imagery/crater-lake-2023.jpg` as their `og:image` — a scene `sources.json` records as no
longer placed on any route. The validator only checked `/pilot/`'s preview.

## 2. Preflight (2026-10-15, after `git fetch --all --prune`)

| Check | Result |
| --- | --- |
| `origin` | `https://github.com/mertkaanakgunlu-debug/orbgss-website.git` |
| `origin/main` | `f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85` (unchanged) |
| MER-218 remote head | `5ca7bdd4167020fc0f7dd5a58b017495de9002fe` (unchanged) |
| `main` ancestor of `5ca7bdd4` | yes; `main...5ca7bdd4` = 0 behind / 4 ahead |
| MER-216 head `adf08186` ancestor of `5ca7bdd4` | yes |
| Working tree | clean apart from the untracked `AGENTS.md` (not part of this task, not committed) |
| Branch | created from exactly `5ca7bdd4` |

## 3. Changes

| File | Change |
| --- | --- |
| `.vercelignore` (new) | Root allowlist: `/*`, then `!index.html`, `!404.html`, `!styles.css`, `!script.js`, `!site.webmanifest`, `!robots.txt`, `!sitemap.xml`, `!vercel.json`, `!assets`, `!platform`, `!solutions`, `!pilot`, `!company`, `!contact` |
| `platform/`, `solutions/`, `company/`, `contact/` `index.html` | `og:image` → `https://orbgss.com/assets/hero/hero-poster-1600.webp` (the homepage's own preview); one line each |
| `scripts/validate_site.py` | `.vercelignore` is a required file; new `check_deploy_set()` and a route-wide social-preview rule (section 4) |
| `scripts/negative_tests_mer237.py` (new) | 29 deliberate regressions (section 6) |
| `STATUS.md`, `CLAUDE.md`, `README.md` | MER-237 state and the new publication head; the deploy-allowlist rule under "Deployment safety"; the two newest negative suites in the validation list |
| `tasks/MER-237_EVIDENCE.md` | this record |

Not changed: page content and layout, `vercel.json` (headers, cache, clean URLs), routes,
`sitemap.xml`, `robots.txt`, every asset, `sources.json`, `hero/`. `hero/config/lane.json` needed no
change: none of the touched files is a lane-protected path (`validate_hero.py` 420 / 0).

The allowlist was derived from what the public files reference, not assumed: the validator
extracts every reference from each deployed `.html`, `.css`, `.js`, `.webmanifest`, `.xml` and
`.txt` file and requires it to resolve inside the allowlist.

## 4. Validator rules added

`check_deploy_set()` models exactly the allowlist form and refuses any other syntax rather than
guess Vercel's reading of it:

* the first rule must be `/*`; every later rule must be `!<root file or directory>` (no globs, no
  paths, no plain ignore lines), and must name something that exists;
* `index.html`, `404.html` and `vercel.json` must be deployed; every `ROUTES` file must be deployed;
* `STATUS.md`, `CLAUDE.md`, `AGENTS.md`, `README.md`, `CHANGELOG.md`, `IMAGERY_RIGHTS.md`,
  `CLAUDE_SESSION_BOOTSTRAP.txt`, `preview-local.bat`, `.vercelignore`, `docs/`, `tasks/`,
  `evidence/`, `scripts/`, `hero/`, `references/` must not be;
* no `.md`, `.py`, `.pyc`, `.bat`, `.ps1`, `.sh`, `.blend` or `__pycache__` file inside a deployed
  directory;
* every path referenced by a deployed text file — root-relative and absolute `orbgss.com`
  attributes, document-relative attributes resolved against the referring file's directory (as the
  browser does), any `assets/` path including `srcset` tokens and the hero ladder JSON, sitemap
  `<loc>`, the robots `Sitemap:` line and CSS `url()` — must be deployed and must exist.

Route-wide social preview: every route's `og:image` must be a self-hosted
`https://orbgss.com/assets/…` image that exists, is deployed, and is shown by some page (referenced
outside `<meta>` tags). The existing `/pilot/` Kızıldere-specific rule is unchanged.

A deploy-set error is collected, not fatal, so it never hides the rest of the validation.

## 5. Vercel behaviour (documentation)

`https://vercel.com/docs/deployments/vercel-ignore` (last updated 2025-03-12):

* "Add a wildcard `/*` as the first line in `.vercelignore` to ensure all directories and files in
  the project root are ignored. The following lines must then start with a `!`" — the allowlist
  form used here; the page's own example re-includes `vercel.json`.
* Served files: "Non-targeted files are prevented from being deployed and served on Vercel."
* The file "should be placed in the root directory of your project".

The page does not distinguish CLI uploads from Git-integration deployments. Production is
Git-sourced (`main`), so the effect on a Git deployment must be observed, not assumed: on the
branch preview deployment if Vercel's Git integration creates one (section 8), and on production by
the MER-219 smoke checklist, which now lists the internal paths that must return 404.

## 6. Verification

| Command | Result |
| --- | --- |
| `py -3.14 scripts/validate_site.py` (baseline `5ca7bdd4`) | PASS, 0 warnings |
| `py -3.14 scripts/validate_site.py` (this branch) | PASS, 0 warnings; deploy set 14 root entries, 110 files |
| `negative_tests_web005.py` | 72 / 72, restored tree identical (site and hero) |
| `negative_tests_web005b.py` | 55 / 55, restored tree identical |
| `negative_tests_web005c.py` | 18 / 18, restored tree identical |
| `negative_tests_mer216.py` | 19 / 19, restored tree identical |
| `negative_tests_mer237.py` (new) | 29 / 29, restored tree identical |
| `py -3.14 hero/scripts/validate_hero.py` (hero workstation) | 420 checks, 0 failed — before and after |
| `py -3.14 scripts/check_copy_preservation.py 5ca7bdd4…` | 0 visible-copy differences (the tool's default baseline is the older WEB-005A head, against which the accepted site already differs) |

The 29 MER-237 cases: allowlist emptied; `/*` removed; a glob rule; a plain ignore line; a
non-existent entry; each of `STATUS.md`, `CLAUDE.md`, `docs`, `tasks`, `evidence`, `scripts`,
`hero`, `references` re-included; `vercel.json`, `404.html`, a route directory, `styles.css`,
`assets` and `sitemap.xml` dropped; a page linking `/STATUS.md`; the sitemap listing `/docs/`; a
sub-route using a document-relative asset path; a reference to a missing deployed file; a Markdown
note in `assets/`; a Python tool in `contact/`; a route advertising Crater Lake again; a missing,
off-site and non-existent `og:image`. Two first-run findings were fixed in the validator before the
final run: attribute names are matched at a name boundary (`data-i18n-href="mail.partner"` is a
dictionary key, not a link), and the deploy-set check no longer short-circuits the rest of the
validation.

**Deploy-set measurement** (tracked files plus the two new ones): 597 files / 131.9 MiB in the
repository; 110 files / 51.4 MiB deployed; 487 files / 80.5 MiB excluded. Excluded root entries:
`.gitignore`, `.vercelignore`, `CHANGELOG.md`, `CLAUDE.md`, `CLAUDE_SESSION_BOOTSTRAP.txt`,
`IMAGERY_RIGHTS.md`, `README.md`, `STATUS.md`, `docs`, `evidence`, `hero`, `preview-local.bat`,
`references`, `scripts`, `tasks`.

**Local serve of the deploy set:** the 110 files were copied to a scratch directory and served with
`http.server`. All 72 paths the public files reference returned 200, as did `/`, the five routes,
`/404.html` and the new `og:image`. `/STATUS.md`, `/CLAUDE.md`, `/README.md`, `/docs/HANDOFF.md`,
`/tasks/MER-213_POST_LAUNCH_AUDIT_EVIDENCE.md`, `/evidence/`, `/scripts/validate_site.py`,
`/hero/config/scene.json`, `/references/`, `/.vercelignore` and `/AGENTS.md` returned 404. This
proves the allowlist is complete for what the pages use; it does not prove Vercel applies it (section 5).

## 7. Residual risks and notes

* Vercel's application of `.vercelignore` to Git deployments is documented only generally; see
  section 8 and MER-219.
* `assets/` is deployed whole, so files no page references stay public, e.g. the retired
  `crater-lake-2023.*` scene and the GEO-WEB-002 `assets/proof/final/` package.
  `assets/imagery/sources.json` stays public by design (the homepage links it as the provenance
  record). Pruning unreferenced assets belongs to MER-240.
* A future page or top-level file must be added to `.vercelignore`; the validator fails if a public
  reference points at an undeployed path, so a forgotten entry cannot pass silently.
* The hero poster as a social preview is a render; the page states that in its caption, the
  preview image itself carries no caption. This matches the homepage's existing preview.
* `AGENTS.md` (untracked, WEB-001-era rules) is not committed; its fate is a MER-239 decision.

## 8. Branch preview deployment

Pushing the branch made Vercel's Git integration create a Preview deployment on its own; this task
created, promoted or altered no deployment. Read from GitHub (`gh api …/commits/58cbb7b8…/status`,
`…/deployments?sha=…`, `…/deployments/7090277542/statuses`) on 2026-10-15:

| Item | Value |
| --- | --- |
| Commit | `58cbb7b81dc142037b371c22beeb469be60c2783` |
| GitHub deployment | `7090277542`, environment `Preview`, created 2026-10-15T10:37:08Z |
| Vercel status context | `Vercel` — success, "Deployment has completed" |
| Vercel deployment | `dpl_DMRAQX9uTKZDtQTcfqK8WuWeecme`, scope `virga-soft`, project `orbgss-website` |
| Preview URL | `https://orbgss-website-lhsk8ab4d-virga-soft.vercel.app` |

The build with the allowlist completed successfully. Every path on the preview, public or internal,
answers `302` to the Vercel Authentication login, so the served file set cannot be read anonymously.
This environment's Vercel connection is not authorized for the `virga-soft` scope (`403 forbidden`
on `GET /v7/deployments` and on the protection-bypass request), and no Vercel CLI is installed, so
the preview could not be read here. **Open item:** with an authorized Vercel session, open
`<preview>/STATUS.md`, `<preview>/tasks/MER-237_EVIDENCE.md` and `<preview>/scripts/validate_site.py`
(expected 404) and `<preview>/`, `<preview>/pilot/` and `<preview>/assets/hero/hero-poster-1600.webp`
(expected 200). MER-219 must establish the same on production after publication.

Observation for MER-219, not a conclusion: the same GitHub deployment list shows a `Production`
deployment for `f4f1d4d6` (the current `main`) created 2026-10-02T07:43:02Z and a `Preview` for every
pushed task branch head, which is consistent with `main` pushes deploying production automatically.
