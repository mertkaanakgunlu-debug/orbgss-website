"""MER-240 visual QA: stitched full-page captures of every page (desktop 1440 / phone 390, EN and TR),
plus per-page checks a headless browser can observe: broken images, console errors, horizontal
overflow, the language actually applied, the current-page marker, and a JavaScript-disabled pass.

    py -3.14 evidence/mer240/tools/capture_mer240.py <repo root>

Local QA tooling only (headless Chrome over CDP, evidence/mer216/tools/mer216_harness.py); never a
site dependency. Captures land in evidence/mer240/ as WebP, the findings in capture_report.json.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = ROOT / "evidence" / "mer240"
sys.path.insert(0, str(ROOT / "evidence" / "mer216" / "tools"))
from mer216_harness import Chrome, serve  # noqa: E402
from PIL import Image  # noqa: E402

PAGES = [("home", "/"), ("solutions", "/solutions/"), ("geothermal", "/solutions/geothermal/"),
         ("about", "/about/"), ("partner", "/partner/"), ("404", "/404.html")]
VIEWS = [("desktop-1440", 1440, 900, False), ("mobile-390", 390, 844, True)]
LANGS = ["en", "tr"]

PROBE = """(()=>({
  height: document.documentElement.scrollHeight,
  overflowX: document.documentElement.scrollWidth - innerWidth,
  broken: [...document.images].filter(i=>i.complete && i.naturalWidth===0 && i.currentSrc).map(i=>i.currentSrc),
  lang: document.documentElement.lang,
  title: document.title,
  current: [...document.querySelectorAll('.main-nav [aria-current="page"]')].map(e=>e.getAttribute('href')||'menu'),
  h1: (document.querySelector('h1')||{}).textContent || '',
  untranslated: document.documentElement.lang === 'tr'
    ? [...document.querySelectorAll('[data-i18n]')].filter(e => e.textContent.trim() && e.textContent.trim() === e.dataset.enText).map(e => e.dataset.i18n).slice(0, 40)
    : [],
}))()"""


def settle(page, h):
    total = page.js("document.documentElement.scrollHeight")
    for y in range(0, int(total) + h, int(h * 0.8)):
        page.js(f"window.scrollTo({{top:{y},behavior:'instant'}})")
        page.pump(0.15)
    page.js("window.scrollTo({top:0,behavior:'instant'})")
    page.js("""Promise.race([
        Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r}))),
        new Promise(r=>setTimeout(r,8000))])""")
    page.pump(0.6)


def stitch(page, w, h, path):
    # Stitch viewport-sized captures: growing the viewport to the page height would stretch the
    # 100svh hero over the whole page.
    height = min(int(page.js("document.documentElement.scrollHeight")), 16000)
    canvas = Image.new("RGB", (w, height))
    y = 0
    while True:
        page.js(f"window.scrollTo({{top:{y},behavior:'instant'}})")
        page.pump(0.35)
        sy = int(page.js("Math.round(scrollY)"))
        tmp = OUT / "_tile.png"
        page.screenshot(tmp)
        canvas.paste(Image.open(tmp).convert("RGB"), (0, sy))
        tmp.unlink()
        if sy + h >= height:
            break
        y = sy + h
    canvas.save(path, "WEBP", quality=78, method=6)


OUT.mkdir(parents=True, exist_ok=True)
srv = serve(ROOT)
chrome = Chrome()
report = {}
try:
    for name, path in PAGES:
        for label, w, h, mobile in VIEWS:
            for lang in LANGS:
                page = chrome.new_page()
                page.emulate(w, h, 1.0, mobile=mobile, reduced_motion=True)
                page.navigate(f"{srv.base}{path}")
                # Remember the English static text, then switch the way a visitor does.
                page.js("document.querySelectorAll('[data-i18n]').forEach(e=>e.dataset.enText=e.textContent.trim())")
                if lang == "tr":
                    page.js("document.querySelector('.lang-btn[data-lang=\"tr\"]').click()")
                    page.pump(0.3)
                settle(page, h)
                info = page.js(PROBE)
                errors = [e["params"]["entry"]["text"] for e in page.events
                          if e.get("method") == "Log.entryAdded" and e["params"]["entry"]["level"] == "error"]
                errors += [e["params"]["exceptionDetails"]["text"] for e in page.events
                           if e.get("method") == "Runtime.exceptionThrown"]
                stitch(page, w, h, OUT / f"{name}-{label}-{lang}.webp")
                info["console_errors"] = errors
                report[f"{name}/{label}/{lang}"] = info
                print(name, label, lang, {k: info[k] for k in ("overflowX", "broken", "lang", "current", "untranslated")}, errors)
                page.js("try{localStorage.removeItem('orbgss.lang')}catch(e){}")
                page.close()
        # No JavaScript: the static HTML alone must read correctly (English, links native).
        page = chrome.new_page()
        page.send("Emulation.setScriptExecutionDisabled", {"value": True})
        page.emulate(1440, 900, 1.0, reduced_motion=True)
        page.navigate(f"{srv.base}{path}")
        page.pump(1.0)
        nojs = page.send("Runtime.evaluate", {"expression": "JSON.stringify({h1:(document.querySelector('h1')||{}).textContent||'', links:document.querySelectorAll('a[href]').length, overflowX: document.documentElement.scrollWidth - innerWidth})", "returnByValue": True})
        report[f"{name}/nojs"] = json.loads(nojs["result"]["value"]) if "result" in nojs else {"error": str(nojs)}
        print(name, "nojs", report[f"{name}/nojs"])
        page.close()
finally:
    chrome.close()
    srv.close()
(OUT / "capture_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
