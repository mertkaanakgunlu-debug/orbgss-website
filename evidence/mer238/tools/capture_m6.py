"""Full-page desktop and mobile captures of the MER-238 mockups, plus broken-image / console / overflow checks."""
import io
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = ROOT / "evidence" / "mer238"
sys.path.insert(0, str(ROOT / "evidence" / "mer216" / "tools"))
from mer216_harness import Chrome, serve  # noqa: E402
from PIL import Image  # noqa: E402

PAGES = ["home", "solutions", "geothermal", "about", "partner"]
VIEWS = [("desktop-1440", 1440, 900, False), ("mobile-390", 390, 844, True)]

OUT.mkdir(parents=True, exist_ok=True)
srv = serve(ROOT)
chrome = Chrome()
report = {}
try:
    for name in PAGES:
        for label, w, h, mobile in VIEWS:
            page = chrome.new_page()
            page.emulate(w, h, 1.0, mobile=mobile, reduced_motion=True)
            page.navigate(f"{srv.base}/docs/mockups/m6/{name}.html")
            total = page.js("document.documentElement.scrollHeight")
            for y in range(0, int(total) + h, int(h * 0.8)):
                page.js(f"window.scrollTo({{top:{y},behavior:'instant'}})")
                page.pump(0.15)
            page.js("window.scrollTo({top:0,behavior:'instant'})")
            page.js("""Promise.race([
                Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r}))),
                new Promise(r=>setTimeout(r,8000))])""")
            page.pump(0.6)
            info = page.js("""(()=>({
                height: document.documentElement.scrollHeight,
                overflowX: document.documentElement.scrollWidth - innerWidth,
                broken: [...document.images].filter(i=>i.complete && i.naturalWidth===0 && i.currentSrc).map(i=>i.currentSrc),
            }))()""")
            errors = [e["params"]["entry"]["text"] for e in page.events
                      if e.get("method") == "Log.entryAdded" and e["params"]["entry"]["level"] == "error"]
            errors += [e["params"]["exceptionDetails"]["text"] for e in page.events
                       if e.get("method") == "Runtime.exceptionThrown"]
            # Stitch viewport-sized captures: growing the viewport to the page height would stretch
            # the 100svh hero over the whole page.
            page.js("(()=>{const h=document.querySelector('.site-header');const p=getComputedStyle(h).position;if(p==='fixed'||p==='sticky'){h.style.setProperty('position','absolute','important');h.style.setProperty('left','0','important');h.style.setProperty('right','0','important')}})()")
            height = min(int(page.js("document.documentElement.scrollHeight")), 16000)
            canvas = Image.new("RGB", (w, height))
            y = 0
            while True:
                page.js(f"window.scrollTo({{top:{y},behavior:'instant'}})")
                page.pump(0.35)
                sy = int(page.js("Math.round(scrollY)"))
                png = OUT / f"_{name}-{label}.png"
                page.screenshot(png)
                canvas.paste(Image.open(png).convert("RGB"), (0, sy))
                png.unlink()
                if sy + h >= height:
                    break
                y = sy + h
            canvas.save(OUT / f"{name}-{label}.webp", "WEBP", quality=78, method=6)
            report[f"{name}/{label}"] = {"height": info["height"], "overflow_x": info["overflowX"],
                                         "broken_images": info["broken"], "console_errors": errors}
            page.close()
            print(name, label, report[f"{name}/{label}"])
finally:
    chrome.close()
    srv.close()
(OUT / "capture_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
