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

The accepted, launched baseline is `feat/web-005c-public-domain-taxonomy-parity@79cc2cb82a4542461cbbfc1d0c349cf02b861084`; `main@00af0f2` is a stale ancestor of it until the CTO authorizes a fast-forward. `STATUS.md` is the current-state record. Work starts only from an explicit `MER-###'e başla` (rule in `CLAUDE.md`): MER-213 (post-launch audit) is `REVIEW_READY`; WEB-007 / MER-143 and WEB-008 / MER-144 follow only after its review. No feature work on `main`.

## Deployment target

- Git source repository
- Vercel hosting
- Squarespace registrar/DNS
- `orbgss.com`

See `docs/DEPLOYMENT_SQUARESPACE_VERCEL.md` before any external deployment/DNS change.
