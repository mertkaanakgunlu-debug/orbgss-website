# OrbGSS Website

Minimal, static public landing page for **OrbGSS — Orbital Geo-Spatial Solutions**.

The repository is the authority for the current website. Development continues in Claude Code / Claude Projects without reconstructing context from chat history; Linear owns task status and order.

## Start here

Claude Code should automatically inspect `CLAUDE.md`. The canonical manual bootstrap is:

1. `CLAUDE.md`
2. `STATUS.md`
3. `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md` (Milestone 6 pages, navigation and content rules)
4. `docs/WEB_VNEXT_AUTHORITY.md`
5. `docs/DESIGN_AUTHORITY.md`
6. `docs/PRODUCT_AND_CONTENT_AUTHORITY.md`
7. `IMAGERY_RIGHTS.md`
8. `assets/imagery/sources.json`
9. task named by `STATUS.md`

For a fresh Claude session, `CLAUDE_SESSION_BOOTSTRAP.txt` contains a copy/paste bootstrap prompt.

## Local validation

```bash
python3 scripts/validate_site.py                 # site: must PASS with 0 warnings
python3 scripts/negative_tests_web005.py         # 72/72 deliberate regressions caught
python3 scripts/negative_tests_web005b.py        # 55/55
python3 scripts/negative_tests_web005c.py        # 18/18
python3 scripts/negative_tests_mer216.py         # 19/19
python3 scripts/negative_tests_mer237.py         # 29/29 (deploy allowlist, social previews)
python3 scripts/negative_tests_mer240.py         # 46/46 (Milestone 6 pages, navigation, redirects)
python3 scripts/negative_tests_mer241.py         # 44/44 (static Turkish pages, language switch, sitemap)
python3 scripts/build_tr_pages.py --check        # /tr/, sitemap.xml and the 404 Turkish line are generated: exit 0 when current
python3 hero/scripts/validate_hero.py            # hero workstation: 420/0
```

On Windows machines where `python` is only the Store alias, use `py -3.14 scripts/validate_site.py`. The hero validator needs the git-ignored local source textures under `hero/assets/source/`; in a fresh clone exactly 13 of its checks fail for that reason alone, and any other failure is real. Errors from the site validator are never acceptable.

## Local preview

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Rebuilding production imagery

The four scene images are OrbGSS composites generated from public-domain USGS Landsat Collection 2 Level-2 data. To rebuild them exactly as pinned in `assets/imagery/sources.json`:

```bash
python -m venv .venv
.venv/Scripts/pip install "numpy>=2" rasterio pillow pyproj pystac-client planetary-computer
.venv/Scripts/python scripts/build_imagery.py --record
```

Use an isolated environment: recent rasterio wheels require numpy 2.

## Current state and next task

Production serves the MER-240 English Milestone 6 pages, `main@a2045344f4cc70fe189160ffd7254fe61020cad9`, live on orbgss.com since 2026-10-16: Home, Solutions (Geothermal, Mining, Marine), About and Partner with us, with 301s from the retired `/platform/`, `/pilot/`, `/company/` and `/contact/`. Vercel deploys `main` to production automatically, so fast-forwarding `main` is a production deployment and a separate CTO gate. The rest of Milestone 6 is in `docs/WEB_M6_IA_AND_CONTENT_AUTHORITY.md`; MER-241 (static `/tr/` pages, generated from the `script.js` dictionary by `scripts/build_tr_pages.py`) is `REVIEW_READY` on `claude/mer-241-turkish-static-pages-sihwiy` and not published. `STATUS.md` is the current-state record. Work starts only from an explicit `MER-###'e başla` (rule in `CLAUDE.md`), from the exact baseline the issue names. No feature work on `main`.

## Deployment target

- Git source repository
- Vercel hosting
- Squarespace registrar/DNS
- `orbgss.com`

See `docs/DEPLOYMENT_SQUARESPACE_VERCEL.md` before any external deployment/DNS change.
