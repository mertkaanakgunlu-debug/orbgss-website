"""MER-240 acceptance sweep: horizontal overflow and broken images on every page at 375-3840 CSS px and
DPR 1, 2 and 3, plus the homepage's cumulative layout shift at desktop and phone widths.

    py -3.14 evidence/mer240/tools/sweep_mer240.py <repo root>

Headless Chrome over CDP (evidence/mer216/tools/mer216_harness.py); local QA tooling only.
Writes evidence/mer240/sweep_report.json.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "evidence" / "mer216" / "tools"))
from mer216_harness import Chrome, serve  # noqa: E402

PAGES = ["/", "/solutions/", "/solutions/geothermal/", "/about/", "/partner/", "/404.html"]
WIDTHS = [375, 390, 414, 768, 1024, 1280, 1440, 1920, 2560, 3840]
DPRS = [1, 2, 3]

srv = serve(ROOT)
chrome = Chrome()
rows, failures = [], []
try:
    page = chrome.new_page()
    for path in PAGES:
        for dpr in DPRS:
            for w in WIDTHS:
                page.emulate(w, 900, dpr=dpr, mobile=w < 768, reduced_motion=True)
                page.navigate(srv.base + path)
                page.js("""(async()=>{const h=document.documentElement.scrollHeight;
                  for(let y=0;y<h+900;y+=700){scrollTo({top:y,behavior:'instant'});await new Promise(r=>setTimeout(r,40))}
                  scrollTo({top:0,behavior:'instant'});
                  await Promise.race([Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r}))),new Promise(r=>setTimeout(r,6000))]);})()""")
                r = page.js("""(()=>({ox: document.documentElement.scrollWidth - innerWidth,
                  broken: [...document.images].filter(i=>i.complete && i.naturalWidth===0 && i.currentSrc).length}))()""")
                rows.append({"page": path, "width": w, "dpr": dpr, **r})
                if r["ox"] > 0 or r["broken"]:
                    failures.append(rows[-1])
    page.close()

    cls = {}
    for w, mobile in ((1440, False), (390, True)):
        page = chrome.new_page()
        page.send("Page.addScriptToEvaluateOnNewDocument", {"source": """
          window.__cls = 0;
          new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; })
            .observe({type: 'layout-shift', buffered: true});"""})
        page.emulate(w, 900, dpr=1, mobile=mobile, reduced_motion=True)
        page.navigate(srv.base + "/")
        page.pump(3.0)
        page.js("""(async()=>{const h=document.documentElement.scrollHeight;
          for(let y=0;y<h+900;y+=600){scrollTo({top:y,behavior:'instant'});await new Promise(r=>setTimeout(r,120))}})()""")
        page.pump(1.0)
        cls[str(w)] = round(page.js("window.__cls"), 4)
        page.close()
finally:
    chrome.close()
    srv.close()

report = {"loads": len(rows), "failures": failures, "homepage_cls": cls,
          "pages": PAGES, "widths": WIDTHS, "dprs": DPRS}
(ROOT / "evidence" / "mer240" / "sweep_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: report[k] for k in ("loads", "failures", "homepage_cls")}, indent=1))
