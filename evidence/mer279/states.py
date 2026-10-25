#!/usr/bin/env python3
"""Interaction states: hover/focus colours with contrast, and crops saved for the evidence sheet."""
import os
import functools, http.server, json, pathlib, socketserver, sys, threading
from playwright.sync_api import sync_playwright
root = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x): pass
class TS(socketserver.ThreadingTCPServer): allow_reuse_address = True; daemon_threads = True
srv = TS(("127.0.0.1", 0), functools.partial(Q, directory=str(root))); base = f"http://127.0.0.1:{srv.server_address[1]}"
threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = r"""
(el) => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(s => parseFloat(s)); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const blend = (f, b) => ({r: f.r*f.a + b.r*(1-f.a), g: f.g*f.a + b.g*(1-f.a), b: f.b*f.a + b.b*(1-f.a), a: 1});
  const lin = v => { v/=255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
  const lum = c => 0.2126*lin(c.r) + 0.7152*lin(c.g) + 0.0722*lin(c.b);
  const ratio = (x, y) => { const a = lum(x), b = lum(y); return +((Math.max(a,b)+0.05)/(Math.min(a,b)+0.05)).toFixed(2); };
  const bgOf = (start) => { let layers = []; for (let e = start; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0) { layers.push(c); if (c.a === 1) break; } } let bg = {r:23,g:26,b:27,a:1}; for (let i = layers.length-1; i>=0; i--) bg = blend(layers[i], bg); return bg; };
  const cs = getComputedStyle(el); const bg = bgOf(el);
  const fg = parse(cs.color); const fgb = blend(fg, bg);
  const oc = parse(cs.outlineColor); const parent = bgOf(el.parentElement || el);
  return {color: cs.color, bg: `rgb(${Math.round(bg.r)},${Math.round(bg.g)},${Math.round(bg.b)})`, textRatio: ratio(fgb, bg), outline: cs.outlineStyle === 'none' ? 'none' : `${cs.outlineWidth} ${cs.outlineStyle} ${cs.outlineColor} off ${cs.outlineOffset}`, outlineVsBackdrop: (cs.outlineStyle !== 'none' && oc) ? ratio(oc, parent) : null};
}
"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None, args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    pg = ctx.new_page(); pg.goto(base + "/about/", wait_until="load"); pg.wait_for_timeout(700)
    targets = {
        "nav link (About, current)": "header .main-nav a[href='/about/']",
        "nav link (Partner)": "header .main-nav a[href='/partner/']",
        "nav trigger (Solutions)": "header .nav-trigger",
        "language TR link": "header .lang-switch a[hreflang='tr'], header .lang-switch button:nth-of-type(2), header .lang-switch a:nth-of-type(2)",
        "footer link": ".site-footer a",
        "brand logo link": "header .brand",
    }
    for name, sel in targets.items():
        loc = pg.locator(sel).first
        if loc.count() == 0: res[name] = "selector not found"; continue
        rest = loc.evaluate(JS)
        loc.hover(); pg.wait_for_timeout(400)
        hov = loc.evaluate(JS)
        pg.mouse.move(5, 500)
        loc.focus(); pg.keyboard.press("Shift+Tab"); pg.keyboard.press("Tab"); pg.wait_for_timeout(250)
        foc = loc.evaluate(JS)
        res[name] = {"rest": rest, "hover": hov, "focus": foc}
        if name in ("nav link (Partner)", "brand logo link"):
            box = loc.bounding_box()
            pg.screenshot(path=str(out / f"focus-{name.split('(')[0].strip().replace(' ','-')}.png"), clip={"x": max(0, box["x"]-24), "y": 0, "width": min(520, 1440-max(0, box["x"]-24)), "height": 96})
    # buttons / cards on /partner/ and /
    pg.goto(base + "/partner/", wait_until="load"); pg.wait_for_timeout(600)
    for name, sel in {"mailto link (Partner)": "a[href^='mailto:']"}.items():
        loc = pg.locator(sel).first
        if loc.count():
            rest = loc.evaluate(JS); loc.hover(); pg.wait_for_timeout(400); hov = loc.evaluate(JS); pg.mouse.move(5, 500)
            loc.focus(); pg.keyboard.press("Shift+Tab"); pg.keyboard.press("Tab"); pg.wait_for_timeout(250)
            res[name] = {"rest": rest, "hover": hov, "focus": loc.evaluate(JS)}
    pg.goto(base + "/", wait_until="load"); pg.wait_for_timeout(800)
    pg.evaluate("window.scrollTo(0, document.querySelector('.domain-link, .domain-card, [data-domain]')?.getBoundingClientRect().top + scrollY - 200 || 0)")
    pg.wait_for_timeout(700)
    loc = pg.locator("a.domain-link").first
    if loc.count():
        loc.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
        res["homepage Solutions card"] = {"rest": loc.evaluate(JS)}
        loc.hover(); pg.wait_for_timeout(500)
        pg.screenshot(path=str(out / "hover-solutions-card.png"))
        pg.mouse.move(5, 5)
        loc.focus(); pg.keyboard.press("Shift+Tab"); pg.keyboard.press("Tab"); pg.wait_for_timeout(300)
        res["homepage Solutions card"]["focus"] = loc.evaluate(JS)
        pg.screenshot(path=str(out / "focus-solutions-card.png"))
    # skip link
    pg.goto(base + "/about/", wait_until="load"); pg.wait_for_timeout(500)
    pg.keyboard.press("Tab"); pg.wait_for_timeout(400)
    res["skip link"] = pg.locator(".skip-link").evaluate(JS)
    pg.screenshot(path=str(out / "focus-skip-link.png"), clip={"x": 0, "y": 0, "width": 640, "height": 120})
    b.close()
srv.shutdown()
(out / "states.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps(res, indent=1, ensure_ascii=False))
