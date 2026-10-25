#!/usr/bin/env python3
"""Measurement-led checks of a served checkout (MER-279 evidence).

usage: measure.py ROOT OUT.json [--only weight|layout|contrast|states|nav|motion ...]

Serves ROOT, then for every route measures:
  layout   - horizontal overflow at 320/360/390/768/1024/1440, console errors, failed requests, header and footer logo
             rendered size (min 120 px wide), favicon / touch-icon link targets that resolve
  weight   - sum of response bytes (body) for the homepage and Solutions at 1440 and 390, first load
  contrast - every visible text node whose background is solid (not over an image/video) at 1440 and 390,
             WCAG contrast of computed colour (alpha blended) against the nearest solid background
  states   - keyboard Tab walk: focus outline colour/width vs its background; hover colour of nav links and buttons
  nav      - mobile menu at 390: opens, closes (button and Escape), links reachable, touch target heights
  motion   - prefers-reduced-motion: reduce -> running animations, transitions longer than 10 ms, hero video attached
"""
import os
import argparse, functools, http.server, json, pathlib, socketserver, sys, threading
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("root"); ap.add_argument("out")
ap.add_argument("--only", nargs="*", default=["layout", "weight", "contrast", "states", "nav", "motion"])
a = ap.parse_args()

root = pathlib.Path(a.root).resolve()
EN = ["/", "/solutions/", "/solutions/geothermal/", "/about/", "/partner/", "/sources/"]
TR = ["/tr/", "/tr/cozumler/", "/tr/cozumler/jeotermal/", "/tr/hakkimizda/", "/tr/is-birligi/", "/tr/kaynaklar/"]
ROUTES = EN + TR + ["/404.html"]
WIDTHS = [320, 360, 390, 768, 1024, 1440]


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x):
        pass


class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


srv = TS(("127.0.0.1", 0), functools.partial(Q, directory=str(root)))
base = f"http://127.0.0.1:{srv.server_address[1]}"
threading.Thread(target=srv.serve_forever, daemon=True).start()

CONTRAST_JS = r"""
() => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(s => parseFloat(s)); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const blend = (f, b) => ({r: f.r*f.a + b.r*(1-f.a), g: f.g*f.a + b.g*(1-f.a), b: f.b*f.a + b.b*(1-f.a), a: 1});
  const lin = v => { v/=255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
  const lum = c => 0.2126*lin(c.r) + 0.7152*lin(c.g) + 0.0722*lin(c.b);
  const ratio = (x, y) => { const a = lum(x), b = lum(y); return (Math.max(a,b)+0.05)/(Math.min(a,b)+0.05); };
  const solidBg = el => {
    // walk up; give up (null) when an image/video/canvas/svg-image or a background-image sits in the chain
    let layers = [];
    for (let e = el; e; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;
      const c = parse(cs.backgroundColor);
      if (c && c.a > 0) { layers.push(c); if (c.a === 1) break; }
    }
    let bg = {r:23, g:26, b:27, a:1};
    for (let i = layers.length - 1; i >= 0; i--) bg = blend(layers[i], bg);
    return bg;
  };
  const overMedia = el => {
    // text that sits inside a positioned scene (caption on imagery) is judged on its own tone logic
    for (let e = el; e; e = e.parentElement) {
      if (e.matches && e.matches('.scene-label, .hero, .hero *, .page-hero.is-stage .scene-label, video, picture, .domain-band .domain-copy, [data-label-tone] .scene-label')) {
        if (e.matches('.scene-label, .hero')) return true;
      }
    }
    return false;
  };
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const n = walker.currentNode;
    if (!n.nodeValue.trim()) continue;
    const el = n.parentElement;
    if (!el || seen.has(el)) continue;
    seen.add(el);
    if (['SCRIPT','STYLE','NOSCRIPT','TITLE'].includes(el.tagName)) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    // clipped sr-only
    if (cs.clip === 'rect(0px, 0px, 0px, 0px)' || (r.width <= 1 && r.height <= 1)) continue;
    // an ancestor with opacity < 1 or a hidden overflow container would change the result; report opacity
    let op = 1; for (let e = el; e; e = e.parentElement) op *= parseFloat(getComputedStyle(e).opacity);
    if (op < 0.05) continue;
    if (overMedia(el)) { out.push({text: n.nodeValue.trim().slice(0, 40), skip: 'over-media'}); continue; }
    const bg = solidBg(el);
    if (!bg) { out.push({text: n.nodeValue.trim().slice(0, 40), skip: 'bg-image'}); continue; }
    let fg = parse(cs.color); if (!fg) continue;
    fg = blend({...fg, a: fg.a * op}, bg);
    const size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight, 10);
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3 : 4.5;
    out.push({text: n.nodeValue.trim().slice(0, 40), cls: (el.className && el.className.baseVal === undefined ? el.className : '') || el.tagName.toLowerCase(),
              fg: cs.color, ratio: +ratio(fg, bg).toFixed(2), need, size, ok: ratio(fg, bg) >= need});
  }
  return out;
}
"""

FOCUS_JS = r"""
() => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(s => parseFloat(s)); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const lin = v => { v/=255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
  const lum = c => 0.2126*lin(c.r) + 0.7152*lin(c.g) + 0.0722*lin(c.b);
  const ratio = (x, y) => { const a = lum(x), b = lum(y); return (Math.max(a,b)+0.05)/(Math.min(a,b)+0.05); };
  const e = document.activeElement; if (!e || e === document.body) return null;
  const cs = getComputedStyle(e);
  let ow = parseFloat(cs.outlineWidth), os = cs.outlineStyle, oc = parse(cs.outlineColor);
  // pseudo outline on the card links
  const af = getComputedStyle(e, '::after');
  let pseudo = false;
  if ((os === 'none' || ow === 0) && af.outlineStyle !== 'none' && parseFloat(af.outlineWidth) > 0) { ow = parseFloat(af.outlineWidth); os = af.outlineStyle; oc = parse(af.outlineColor); pseudo = true; }
  let bgc = null;
  for (let x = e; x; x = x.parentElement) { const c = parse(getComputedStyle(x).backgroundColor); if (c && c.a === 1) { bgc = c; break; } }
  if (!bgc) bgc = {r:23, g:26, b:27, a:1};
  const r = e.getBoundingClientRect();
  return {tag: e.tagName.toLowerCase(), cls: String(e.className || '').slice(0, 40), text: (e.textContent || '').trim().slice(0, 30), outlineWidth: ow, outlineStyle: os, outlineColor: cs.outlineColor, pseudo,
          ratio: oc ? +ratio(oc, bgc).toFixed(2) : null, visible: r.width > 0 && r.height > 0, onScreen: r.bottom > 0 && r.top < innerHeight};
}
"""

results = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None, args=["--no-sandbox"])

    if "layout" in a.only:
        lay = []
        for r in ROUTES:
            for w in WIDTHS:
                ctx = b.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1)
                pg = ctx.new_page()
                errs, bad = [], []
                pg.on("console", lambda m, errs=errs: errs.append(m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda e, errs=errs: errs.append(str(e)))
                pg.on("response", lambda resp, bad=bad: bad.append(f"{resp.status} {resp.url.replace(base,'')}") if resp.status >= 400 else None)
                pg.goto(base + r, wait_until="load")
                pg.wait_for_timeout(500)
                m = pg.evaluate("""() => {
                  const de = document.documentElement;
                  const logos = [...document.querySelectorAll('img.brand-logo, .footer-brand img, .site-footer img[src*="orbgss-logo"]')].map(i => ({where: i.closest('footer') ? 'footer' : 'header', w: Math.round(i.getBoundingClientRect().width), h: Math.round(i.getBoundingClientRect().height), natural: i.naturalWidth, src: i.getAttribute('src'), visible: i.getBoundingClientRect().width > 0}));
                  const links = [...document.querySelectorAll('link[rel~="icon"], link[rel="apple-touch-icon"], link[rel="manifest"]')].map(l => l.getAttribute('href'));
                  return {scrollW: de.scrollWidth, clientW: de.clientWidth, logos, links, theme: document.querySelector('meta[name="theme-color"]')?.content};
                }""")
                lay.append({"route": r, "w": w, "overflow": m["scrollW"] > m["clientW"], "scrollW": m["scrollW"], "clientW": m["clientW"], "logos": m["logos"], "theme": m["theme"], "errors": errs[:3], "badResponses": bad[:3]})
                if w == 1440:
                    # icon links resolve
                    for href in m["links"]:
                        u = href if href.startswith("/") else "/" + href if not r.startswith("/tr") else "/" + href
                        resp = pg.request.get(base + (href if href.startswith("/") else "/" + href))
                        lay[-1].setdefault("iconStatus", {})[href] = resp.status
                ctx.close()
        results["layout"] = lay

    if "weight" in a.only:
        wt = {}
        for r in ["/", "/solutions/", "/solutions/geothermal/", "/about/", "/partner/"]:
            for w in (1440, 390):
                ctx = b.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1)
                pg = ctx.new_page()
                tot = {"n": 0, "bytes": 0, "byType": {}}
                def on_resp(resp, tot=tot):
                    try:
                        body = resp.body()
                    except Exception:
                        return
                    t = (resp.headers.get("content-type") or "").split(";")[0]
                    tot["n"] += 1; tot["bytes"] += len(body); tot["byType"][t] = tot["byType"].get(t, 0) + len(body)
                pg.on("response", on_resp)
                pg.goto(base + r, wait_until="load"); pg.wait_for_timeout(1500)
                wt[f"{r}@{w}"] = tot
                ctx.close()
        results["weight"] = wt

    if "contrast" in a.only:
        con = {}
        for r in ROUTES:
            for w in (1440, 390):
                ctx = b.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1)
                pg = ctx.new_page()
                pg.goto(base + r, wait_until="load"); pg.wait_for_timeout(600)
                # reveal scroll-triggered content
                h = pg.evaluate("document.documentElement.scrollHeight")
                y = 0
                while y < h:
                    pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(120); y += 700
                pg.wait_for_timeout(500)
                rows = pg.evaluate(CONTRAST_JS)
                bad = [x for x in rows if x.get("ok") is False]
                con[f"{r}@{w}"] = {"checked": len([x for x in rows if "ratio" in x]), "skippedOverMedia": len([x for x in rows if x.get("skip") == "over-media"]),
                                   "skippedBgImage": len([x for x in rows if x.get("skip") == "bg-image"]),
                                   "min": min([x["ratio"] for x in rows if "ratio" in x], default=None), "failures": bad[:12]}
                ctx.close()
        results["contrast"] = con

    if "states" in a.only:
        st = {}
        for r in ["/", "/solutions/", "/solutions/geothermal/", "/about/", "/partner/", "/sources/", "/tr/"]:
            ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
            pg = ctx.new_page()
            pg.goto(base + r, wait_until="load"); pg.wait_for_timeout(800)
            seen = []
            for i in range(60):
                pg.keyboard.press("Tab")
                pg.wait_for_timeout(40)
                f = pg.evaluate(FOCUS_JS)
                if f and f["visible"]:
                    seen.append(f)
            weak = [f for f in seen if f["outlineStyle"] == "none" or f["outlineWidth"] < 2 or (f["ratio"] is not None and f["ratio"] < 3)]
            st[r] = {"tabStops": len(seen), "minOutlineRatio": min([f["ratio"] for f in seen if f["ratio"] is not None], default=None), "weak": weak[:8]}
            ctx.close()
        results["states"] = st

        # hover: header nav links, buttons, footer links, a card link
        hov = {}
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        pg = ctx.new_page(); pg.goto(base + "/", wait_until="load"); pg.wait_for_timeout(800)
        for sel in [".main-nav > a:nth-of-type(2)", ".main-nav .nav-trigger", ".lang-switch button, .lang-switch a", ".site-footer a"]:
            loc = pg.locator(sel).first
            if loc.count() == 0:
                hov[sel] = "not found"; continue
            before = loc.evaluate("e => getComputedStyle(e).color")
            loc.hover(); pg.wait_for_timeout(350)
            after = loc.evaluate("e => getComputedStyle(e).color")
            hov[sel] = {"before": before, "after": after}
        ctx.close()
        results["hover"] = hov

    if "nav" in a.only:
        nv = {}
        for r in ["/", "/solutions/", "/tr/"]:
            ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
            pg = ctx.new_page(); pg.goto(base + r, wait_until="load"); pg.wait_for_timeout(700)
            tog = pg.locator(".menu-toggle")
            rec = {"toggleVisible": tog.is_visible(), "navHiddenInitially": not pg.locator(".main-nav").is_visible()}
            tog.click(); pg.wait_for_timeout(300)
            rec["expandedAfterClick"] = tog.get_attribute("aria-expanded")
            rec["navVisible"] = pg.locator(".main-nav").is_visible()
            rec["linkHeights"] = pg.evaluate("[...document.querySelectorAll('.main-nav a')].filter(a => a.getBoundingClientRect().height > 0).map(a => Math.round(a.getBoundingClientRect().height))")
            rec["navBg"] = pg.evaluate("getComputedStyle(document.querySelector('.main-nav')).backgroundColor")
            pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
            rec["closedByEscape"] = not pg.locator(".main-nav").is_visible()
            rec["expandedAfterEscape"] = tog.get_attribute("aria-expanded")
            tog.click(); pg.wait_for_timeout(200); tog.click(); pg.wait_for_timeout(200)
            rec["closedByToggle"] = not pg.locator(".main-nav").is_visible()
            hdr = pg.locator("img.brand-logo")
            bb = hdr.bounding_box()
            rec["headerLogoPx"] = [round(bb["width"]), round(bb["height"])]
            nv[r] = rec
            ctx.close()
        results["nav"] = nv

    if "motion" in a.only:
        mo = {}
        for r in ["/", "/solutions/", "/solutions/geothermal/"]:
            ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
            pg = ctx.new_page(); pg.goto(base + r, wait_until="load"); pg.wait_for_timeout(1500)
            mo[r] = pg.evaluate("""() => {
              const anim = document.getAnimations().filter(a => a.playState === 'running').length;
              const slow = [...document.querySelectorAll('*')].filter(e => { const cs = getComputedStyle(e); return cs.transitionDuration.split(',').some(d => parseFloat(d) > 0.01) || (cs.animationName !== 'none' && parseFloat(cs.animationDuration) > 0.01); }).length;
              const v = document.querySelector('video');
              return {runningAnimations: anim, elementsWithMotion: slow, videoSources: v ? v.querySelectorAll('source').length + (v.getAttribute('src') ? 1 : 0) : null, videoPaused: v ? v.paused : null};
            }""")
            ctx.close()
        results["motion"] = mo

    b.close()
srv.shutdown()
pathlib.Path(a.out).write_text(json.dumps(results, indent=1, ensure_ascii=False))
print("wrote", a.out)
