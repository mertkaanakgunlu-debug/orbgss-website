# MER-279 evidence tooling

Local tooling only (Python, Playwright, Pillow); nothing here runs on the site and `evidence/` is not deployed.
Set `CHROMIUM_PATH` to a Chromium binary if Playwright's own is not installed.

| Script | What it does |
| --- | --- |
| `measure.py ROOT OUT.json [--only layout weight contrast states nav motion]` | Serves a checkout and measures every route: horizontal overflow at 320 / 360 / 390 / 768 / 1024 / 1440, console and network errors, header and footer logo size, icon links, first-load weight, WCAG contrast of every text element on a solid ground, Tab-walk focus rings, the mobile menu, `prefers-reduced-motion`. |
| `states.py ROOT OUT_DIR` | Rest / hover / focus colours with contrast for the navigation, footer, brand link, mailto link and skip link, plus focus crops. |
| `cardstates.py ROOT OUT_DIR` | Hover and keyboard-focus screenshots of the homepage Solutions cards. |
| `capture.py ROOT OUT_DIR` | Homepage by act (hero first frame and settled, Acts 2-4, inspection aid, Solutions, footer), every interior page full length, the open mobile menu and 3x logo close-ups. |
| `compose.py FINAL_DIR OUT_DIR` | Production \| Atlas preview \| Agate comparison sheets from three `capture.py` folders. |

`measurements/` holds the raw results behind `tasks/MER-279_EVIDENCE.md` (Agate branch, Atlas base, production weights; the reduced-motion run of the Atlas base).
The screenshots are in the project's Library under `agate-brand/`, not in the repository.
