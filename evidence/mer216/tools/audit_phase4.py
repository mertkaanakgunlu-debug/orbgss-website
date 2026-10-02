#!/usr/bin/env python3
"""MER-216 Phase 4 terminal browser audit (real Chrome over CDP, evidence tooling only).

    python audit_phase4.py <repo_root> <out.json> [--quick]

Per viewport/DPR class: every route (overflow, broken images, console errors, layout shift),
homepage image selection vs device-pixel demand with transfer bytes, hero state, EN/TR, reduced
motion, no-JS, navigation, evidence radios and the inspection aid.
"""
import json
import sys
import time

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from mer216_harness import Chrome, serve  # noqa: E402
import measure_analytical as ma  # noqa: E402

ROUTES = ["/", "/platform/", "/solutions/", "/pilot/", "/company/", "/contact/", "/404.html"]
CLASSES = [
    ("mobile-375@3x", 375, 812, 3.0, True),
    ("tablet-768@2x", 768, 1024, 2.0, False),
    ("w1024@1x", 1024, 768, 1.0, False),
    ("w1024@2x", 1024, 768, 2.0, False),
    ("w1440@1x", 1440, 900, 1.0, False),
    ("w1440@2x", 1440, 900, 2.0, False),
    ("w1920@1x", 1920, 1080, 1.0, False),
    ("w1920@2x (4K@200%)", 1920, 1080, 2.0, False),
    ("w2560@1.5x (4K@150%)", 2560, 1440, 1.5, False),
    ("w3840@1x (4K@100%)", 3840, 2160, 1.0, False),
]

CLS_INIT = r"""
window.__cls = 0; window.__shifts = [];
try { new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) { window.__cls += e.value; window.__shifts.push(Math.round(e.value*10000)/10000); } }).observe({type: 'layout-shift', buffered: true}); } catch (e) {}
window.__errors = [];
addEventListener('error', (e) => window.__errors.push(String(e.message)));
addEventListener('unhandledrejection', (e) => window.__errors.push('unhandledrejection ' + String(e.reason)));
"""

PAGE_CHECK = r"""
(() => {
  const de = document.documentElement;
  return {
    overflow: de.scrollWidth - de.clientWidth, lang: de.lang, title: document.title,
    h1: Array.from(document.querySelectorAll('h1')).map(h => h.textContent.trim()),
    broken: Array.from(document.images).filter(i => i.complete && i.naturalWidth === 0 && (i.currentSrc || i.src)).map(i => i.currentSrc || i.src),
    cls: Math.round(window.__cls * 10000) / 10000, shifts: window.__shifts.length, errors: window.__errors,
    imgBytes: performance.getEntriesByType('resource').filter(e => /\.(webp|png|jpg|svg)/.test(e.name)).reduce((a, e) => a + e.encodedBodySize, 0),
    videoBytes: performance.getEntriesByType('resource').filter(e => /\.(webm|mp4)/.test(e.name)).reduce((a, e) => a + e.encodedBodySize, 0),
  };
})()
"""

SCROLL = ma.SCROLL


def open_page(chrome, srv, w, h, dpr, mobile, reduced=False, nojs=False, lang=None):
    page = chrome.new_page()
    page.send("Network.setCacheDisabled", {"cacheDisabled": True})
    if nojs:
        page.send("Emulation.setScriptExecutionDisabled", {"value": True})
    else:
        page.send("Page.addScriptToEvaluateOnNewDocument", {"source": CLS_INIT})
        # localhost is excluded from Chrome's network-quality estimator, so a fresh profile reports a
        # conservative default (4g / 1.45 Mbit/s). A real visitor has a measured value; use 10 Mbit/s.
        page.send("Page.addScriptToEvaluateOnNewDocument", {"source": "Object.defineProperty(navigator,'connection',{configurable:true,get:()=>({effectiveType:'4g',downlink:10,rtt:50,saveData:false,addEventListener(){},removeEventListener(){}})});"})
        if lang:
            page.send("Page.addScriptToEvaluateOnNewDocument", {"source": f"try{{localStorage.setItem('orbgss.lang','{lang}')}}catch(e){{}}"})
    page.emulate(w, h, dpr, mobile=mobile, reduced_motion=reduced)
    return page


def main():
    root, out = sys.argv[1], sys.argv[2]
    quick = "--quick" in sys.argv
    srv = serve(root)
    chrome = Chrome()
    result = {"classes": []}
    try:
        for name, w, h, dpr, mobile in (CLASSES[:2] if quick else CLASSES):
            c = {"class": name, "routes": {}}
            for route in ROUTES:
                page = open_page(chrome, srv, w, h, dpr, mobile, reduced=True)
                page.navigate(srv.base + route)
                page.js(SCROLL, timeout=90)
                time.sleep(0.5)
                c["routes"][route] = page.js(PAGE_CHECK)
                if route == "/":
                    c["home_images"] = page.js(ma.PROBE)
                page.close()
            # motion hero (not reduced) on the homepage, then the hero state
            page = open_page(chrome, srv, w, h, dpr, mobile, reduced=False)
            page.navigate(srv.base + "/")
            time.sleep(14 if not mobile else 3)
            c["hero_motion"] = page.js("(()=>{const h=document.querySelector('.hero');const v=document.querySelector('.hero-video');return {state:h.dataset.heroState,reason:h.dataset.heroReason||null,tier:h.dataset.heroTier||null,codec:h.dataset.heroCodec||null,layer:h.dataset.heroLayer||null,src:v.currentSrc.split('/').pop()||null,ended:v.ended,vw:v.videoWidth}})()")
            page.close()
            # EN / TR
            for lang in ("en", "tr"):
                page = open_page(chrome, srv, w, h, dpr, mobile, reduced=True, lang=lang)
                page.navigate(srv.base + "/")
                time.sleep(0.6)
                c[f"lang_{lang}"] = page.js("({lang:document.documentElement.lang,h1:document.querySelector('h1').textContent.trim()})")
                page.close()
            # no-JS
            page = open_page(chrome, srv, w, h, dpr, mobile, nojs=True)
            page.navigate(srv.base + "/")
            time.sleep(1.5)
            c["nojs"] = page.js("({h1:document.querySelector('h1').textContent.trim(),poster:Array.from(document.querySelectorAll('.hero img')).map(i=>({c:i.complete,w:i.naturalWidth,src:(i.currentSrc||'').split('/').pop()}))})", await_promise=False)
            page.close()
            result["classes"].append(c)
            ov = {r: v["overflow"] for r, v in c["routes"].items()}
            cls = {r: v["cls"] for r, v in c["routes"].items()}
            print(name, "overflow", set(ov.values()), "cls", max(cls.values()), "broken", sum(len(v["broken"]) for v in c["routes"].values()),
                  "errors", sum(len(v["errors"]) for v in c["routes"].values()), "hero", c["hero_motion"]["state"], c["hero_motion"]["tier"], flush=True)
    finally:
        chrome.close()
        srv.close()
    json.dump(result, open(out, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
