"""Horizontal overflow, console errors, failed requests and header geometry on every route at six widths.

    python evidence/heat_trace/measure_overflow.py [--base http://127.0.0.1:8766] [--out measurements/overflow.json]

Serve the repository root first (python -m http.server). Local tooling; not deployed.
"""
import argparse, json, pathlib
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="http://127.0.0.1:8766")
ap.add_argument("--chrome", default="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome")
ap.add_argument("--out", default=str(pathlib.Path(__file__).parent / "measurements" / "overflow.json"))
args = ap.parse_args()
routes = ["/index.html", "/solutions/index.html", "/solutions/geothermal/index.html", "/about/index.html", "/partner/index.html",
          "/sources/index.html", "/404.html", "/tr/index.html", "/tr/cozumler/index.html", "/tr/cozumler/jeotermal/index.html",
          "/tr/hakkimizda/index.html", "/tr/is-birligi/index.html", "/tr/kaynaklar/index.html"]
widths = [320, 360, 390, 768, 1024, 1440]
res = {"widths": widths, "routes": len(routes), "overflow": [], "console_errors": [], "failed_requests": [], "header": {}}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=args.chrome)
    for w in widths:
        ctx = b.new_context(viewport={"width": w, "height": 900})
        pg = ctx.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("requestfailed", lambda r: errs.append("FAILED " + r.url))
        for r in routes:
            pg.goto(args.base + r)
            pg.wait_for_timeout(350)
            d = pg.evaluate("""() => {const h=document.querySelector('.site-header'); const l=document.querySelector('.brand-logo');
                const lr=l.getBoundingClientRect(); const hr=h.getBoundingClientRect();
                return {sw: document.documentElement.scrollWidth, iw: window.innerWidth, logoW: Math.round(lr.width*10)/10, logoH: Math.round(lr.height*10)/10, headerH: Math.round(hr.height)}}""")
            if d["sw"] > d["iw"]:
                res["overflow"].append({"w": w, "route": r, "scrollWidth": d["sw"]})
            if r == "/index.html":
                res["header"][str(w)] = {"logo": [d["logoW"], d["logoH"]], "header_height": d["headerH"]}
        res["console_errors"] += [{"w": w, "msg": e} for e in errs if not e.startswith("FAILED")]
        res["failed_requests"] += [{"w": w, "msg": e} for e in errs if e.startswith("FAILED")]
        ctx.close()
    b.close()
pathlib.Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
print({k: (len(v) if isinstance(v, list) else v) for k, v in res.items() if k != "header"})
print(res["header"])
