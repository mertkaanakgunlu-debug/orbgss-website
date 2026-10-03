# OrbGSS Website

Minimal, static public landing page for **OrbGSS — Orbital Geo-Spatial Solutions**.

The repository is the authority for the current website. Development continues in Claude Code / Claude Projects without reconstructing context from chat history; Linear owns task status and order.

## Start here

Claude Code should automatically inspect `CLAUDE.md`. The canonical manual bootstrap is:

1. `CLAUDE.md`
2. `STATUS.md`
3. `docs/WEB_VNEXT_AUTHORITY.md`
4. `docs/DESIGN_AUTHORITY.md`
5. `docs/PRODUCT_AND_CONTENT_AUTHORITY.md`
6. `IMAGERY_RIGHTS.md`
7. `assets/imagery/sources.json`
8. task named by `STATUS.md`

For a fresh Claude session, `CLAUDE_SESSION_BOOTSTRAP.txt` contains a copy/paste bootstrap prompt.

## Local validation

```bash
python3 scripts/validate_site.py                 # site: must PASS with 0 warnings
python3 scripts/negative_tests_web005.py         # 72/72 deliberate regressions caught
python3 scripts/negative_tests_web005b.py        # 55/55
python3 scripts/negative_tests_web005c.py        # 18/18
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

Git `main` is `f4f1d4d6cb6ff4acd4ad02129bb9ec13a50ade85` (the MER-213 documentation commit over the launched code `79cc2cb`). MER-216 (media fidelity and runtime hardening; supersedes MER-143..146) is accepted and Done at `claude/mer-216-s1r628@adf08186d3ee4a438bda73886272d05c970e670a` but not yet published; its docs-only publication closure MER-218 is `REVIEW_READY`. Fast-forwarding `main` and any deployment are separate CTO gates. `STATUS.md` is the current-state record. Work starts only from an explicit `MER-###'e başla` (rule in `CLAUDE.md`), from the exact baseline the issue names. No feature work on `main`.

## Deployment target

- Git source repository
- Vercel hosting
- Squarespace registrar/DNS
- `orbgss.com`

See `docs/DEPLOYMENT_SQUARESPACE_VERCEL.md` before any external deployment/DNS change.
