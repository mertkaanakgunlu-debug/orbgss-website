"""Focus, hover and rest states of the brand palette (Heat Trace, then Violet, now v6) in a real browser.

    python evidence/heat_trace/measure_states.py [--base http://127.0.0.1:8766] [--out measurements/states.json]

Serve the repository root first (python -m http.server). Tabs through the first 14 keyboard stops of the homepage and records
each focus ring (colour, width), measures the focus ring against the ground it sits on, and records the ghost button and the
navigation link at rest and on hover. Local tooling; not deployed.
"""
import argparse, json, pathlib, re
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="http://127.0.0.1:8766")
ap.add_argument("--chrome", default="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome")
ap.add_argument("--out", default=str(pathlib.Path(__file__).parent / "measurements" / "states.json"))
args = ap.parse_args()


def lum(rgb):
    f = lambda v: (v / 255 / 12.92) if v / 255 <= 0.03928 else (((v / 255) + 0.055) / 1.055) ** 2.4
    return .2126 * f(rgb[0]) + .7152 * f(rgb[1]) + .0722 * f(rgb[2])


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return round((max(la, lb) + .05) / (min(la, lb) + .05), 2)


def rgb(s):
    return tuple(int(float(x)) for x in re.findall(r"[\d.]+", s)[:3])


WHITE, NIGHT = (255, 255, 255), (13, 22, 38)
# The ring colour of the dark scope: Ocean light (the v6 palette; it was Violet light rgb(171, 124, 199) in the Violet palette and
# Magma light rgb(249, 73, 151) in Heat Trace).
DARK_RING = "rgb(84, 164, 251)"
out = {"focus_stops": [], "states": {}}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=args.chrome)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(args.base + "/index.html")
    pg.wait_for_timeout(600)
    for _ in range(14):
        pg.keyboard.press("Tab")
        pg.wait_for_timeout(120)
        d = pg.evaluate("""() => {const e = document.activeElement; const c = getComputedStyle(e);
            const r = e.getBoundingClientRect();
            return {tag: e.tagName, target: (e.getAttribute('href') || e.id || e.className).toString().slice(0, 40),
                    outline: c.outlineStyle, width: c.outlineWidth, colour: c.outlineColor, top: Math.round(r.top)}}""")
        d["ground"] = "night" if d["colour"] == DARK_RING else "light"
        d["ring_contrast"] = ratio(rgb(d["colour"]), NIGHT if d["ground"] == "night" else WHITE)
        out["focus_stops"].append(d)

    def style(sel, props=("color", "backgroundColor", "borderBottomColor")):
        return pg.evaluate("(a)=>{const e=document.querySelector(a[0]);const c=getComputedStyle(e);return Object.fromEntries(a[1].map(p=>[p,c[p]]))}", [sel, list(props)])

    pg.goto(args.base + "/index.html")
    pg.wait_for_timeout(500)
    nav = ".site-header nav a[href='/about/']"
    out["states"]["nav_rest"] = style(nav)
    pg.hover(nav)
    pg.wait_for_timeout(300)
    out["states"]["nav_hover"] = style(nav)
    pg.mouse.move(5, 300)
    btn = ".hero .button"
    out["states"]["ghost_rest"] = style(btn)
    pg.hover(btn)
    pg.wait_for_timeout(300)
    h = style(btn)
    h["label_contrast"] = ratio(rgb(h["color"]), rgb(h["backgroundColor"]))
    out["states"]["ghost_hover"] = h
    b.close()
pathlib.Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
print("focus stops:", len(out["focus_stops"]), "min ring contrast:", min(d["ring_contrast"] for d in out["focus_stops"]))
