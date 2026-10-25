"""Which accent colours the rendered pages actually use (Violet brand adoption).

    python evidence/violet/measure_accent_colours.py [--base http://127.0.0.1:8766] [--out measurements/accent_colours.json]

Serve the repository root first (python -m http.server). For every element of the 13 routes at 1440 px the script reads the
computed colour, background, border, outline, text-decoration, fill and stroke colours and counts how many elements carry
each of the two interface accents (Violet #854AA6, Violet light #AB7CC7) and each Heat Trace colour that must be gone
(Magma #CD1B74, Magma light #F94997, Heat Trace amber-light #FFAA2E, the logo Magma #E43386 in the interface). Local tooling; not deployed.
"""
import argparse, json, pathlib
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="http://127.0.0.1:8766")
ap.add_argument("--chrome", default="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome")
ap.add_argument("--out", default=str(pathlib.Path(__file__).parent / "measurements" / "accent_colours.json"))
args = ap.parse_args()
routes = ["/index.html", "/solutions/index.html", "/solutions/geothermal/index.html", "/about/index.html", "/partner/index.html",
          "/sources/index.html", "/404.html", "/tr/index.html", "/tr/cozumler/index.html", "/tr/cozumler/jeotermal/index.html",
          "/tr/hakkimizda/index.html", "/tr/is-birligi/index.html", "/tr/kaynaklar/index.html"]
WANT = {"violet": "rgb(133, 74, 166)", "violet_light": "rgb(171, 124, 199)"}
GONE = {"magma": "rgb(205, 27, 116)", "magma_light": "rgb(249, 73, 151)", "heat_trace_amber_light": "rgb(255, 170, 46)", "logo_magma": "rgb(228, 51, 134)"}
JS = """() => {
  const props = ['color','backgroundColor','borderTopColor','borderRightColor','borderBottomColor','borderLeftColor','outlineColor','textDecorationColor','fill','stroke','caretColor'];
  const counts = {};
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    for (const p of props) { const v = cs[p]; if (v) counts[v] = (counts[v] || 0) + 1; }
  }
  return counts;
}"""
res = {"routes": len(routes), "want": WANT, "gone": GONE, "per_route": {}, "totals_want": {k: 0 for k in WANT}, "totals_gone": {k: 0 for k in GONE}}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=args.chrome)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    for r in routes:
        pg.goto(args.base + r)
        pg.wait_for_timeout(500)
        c = pg.evaluate(JS)
        row = {k: c.get(v, 0) for k, v in {**WANT, **GONE}.items()}
        res["per_route"][r] = row
        for k in WANT:
            res["totals_want"][k] += row[k]
        for k in GONE:
            res["totals_gone"][k] += row[k]
    b.close()
pathlib.Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
print("accent in use:", res["totals_want"], "| retired colours still computed:", res["totals_gone"])
