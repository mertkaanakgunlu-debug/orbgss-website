#!/usr/bin/env python3
"""Evidence capture of one build: homepage by act, interior pages full-length, header/footer close-ups.

usage: capture.py ROOT OUT [--routes ...] [--widths 1440,390]
Writes <OUT>/<slug>-<d|m><width>-<part>.<jpg|png>. Section crops use the same element ids in every build.
"""
import os
import argparse, functools, http.server, pathlib, socketserver, threading, sys
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("out")
ap.add_argument("--routes", default="/,/solutions/,/solutions/geothermal/,/about/,/partner/,/sources/")
ap.add_argument("--widths", default="1440,390"); a = ap.parse_args()
root = pathlib.Path(a.root).resolve(); out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x): pass
class TS(socketserver.ThreadingTCPServer): allow_reuse_address = True; daemon_threads = True
srv = TS(("127.0.0.1", 0), functools.partial(Q, directory=str(root))); base = f"http://127.0.0.1:{srv.server_address[1]}"
threading.Thread(target=srv.serve_forever, daemon=True).start()
slug = lambda r: "home" if r == "/" else r.strip("/").replace("/", "-")
SECTIONS = [("header", ".site-header"), ("act2-context", "#context"), ("act3-evidence", "#evidence"), ("act4-priority", "#priority"), ("inspection", "#inspect"), ("solutions", "#solutions"), ("footer", ".site-footer")]
def sweep(pg):
    h = pg.evaluate("document.documentElement.scrollHeight"); y = 0
    while y < h:
        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(160); y += 500
        h = pg.evaluate("document.documentElement.scrollHeight")
    pg.wait_for_timeout(400)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None, args=["--no-sandbox"])
    for w in [int(x) for x in a.widths.split(",")]:
        tag = "d" if w >= 1000 else "m"; h = 900 if w >= 1000 else 844
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
        for r in a.routes.split(","):
            pg = ctx.new_page(); errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            try:
                resp = pg.goto(base + r, wait_until="load")
            except Exception as e:
                print("skip", r, e); pg.close(); continue
            if resp.status >= 400: print("skip", r, resp.status); pg.close(); continue
            pg.add_style_tag(content=".skip-link{display:none!important}")
            pg.wait_for_timeout(900)
            name = f"{slug(r)}-{tag}{w}"
            if r == "/":
                pg.screenshot(path=str(out / f"{name}-hero-t1.png"))
                pg.wait_for_timeout(12500)
                pg.screenshot(path=str(out / f"{name}-hero-settled.png"))
                sweep(pg)
                for part, sel in SECTIONS:
                    loc = pg.locator(sel).first
                    if loc.count() == 0: print("missing", sel); continue
                    loc.scroll_into_view_if_needed(); pg.wait_for_timeout(700)
                    loc.screenshot(path=str(out / f"{name}-{part}.jpg"), type="jpeg", quality=92)
            else:
                sweep(pg); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(600)
                pg.screenshot(path=str(out / f"{name}-full.jpg"), type="jpeg", quality=92, full_page=True)
            if r == "/" and w < 1000:
                pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
                pg.locator(".menu-toggle").click(); pg.wait_for_timeout(400)
                pg.screenshot(path=str(out / f"{name}-menu-open.png"))
            if errs: print("console errors", r, w, errs[:3], file=sys.stderr)
            pg.close()
        ctx.close()
    # logo close-ups at 3x: header (left 560 px) and footer brand, desktop
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=3)
    pg = ctx.new_page(); pg.goto(base + "/about/", wait_until="load"); pg.add_style_tag(content=".skip-link{display:none!important}"); pg.wait_for_timeout(900)
    pg.screenshot(path=str(out / "logo-header-3x.png"), clip={"x": 0, "y": 0, "width": 520, "height": 88})
    f = pg.locator(".site-footer").first; f.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
    bb = f.bounding_box(); pg.screenshot(path=str(out / "logo-footer-3x.png"), clip={"x": 0, "y": bb["y"], "width": 520, "height": bb["height"]})
    ctx.close()
    b.close()
srv.shutdown(); print("done", out)
