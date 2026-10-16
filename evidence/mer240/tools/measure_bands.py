"""MER-240: measure the drawn width of the /solutions/ band photographs (19 widths x DPR 1 and 2) and the
Geothermal locator map. The maxima are recorded in sources.json (scenes -> web_m6_placement.rendered).

    py -3.14 evidence/mer240/tools/measure_bands.py <repo root>
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "evidence" / "mer216" / "tools"))
from mer216_harness import serve, Chrome  # noqa: E402

WIDTHS = [360, 390, 414, 600, 768, 820, 900, 1000, 1100, 1280, 1366, 1440, 1536, 1680, 1920, 2048, 2560, 3200, 3840]
srv = serve(ROOT)
chrome = Chrome()
page = chrome.new_page()
out = {}
try:
    for dpr in (1, 2):
        for w in WIDTHS:
            page.emulate(w, 900, dpr=dpr, mobile=w < 768)
            page.navigate(srv.base + "/solutions/")
            page.wait_load()
            r = page.js("""(() => {
              const res = {};
              document.querySelectorAll('.domain-band').forEach(b => {
                const img = b.querySelector('img');
                const box = b.getBoundingClientRect();
                const nat = img.naturalWidth / img.naturalHeight || 1.6;
                // object-fit: cover draws the image at max(box.w, box.h * aspect)
                const drawn = Math.max(box.width, box.height * nat);
                res[b.id] = {band_w: box.width, band_h: box.height, drawn_w: drawn, current: img.currentSrc.split('/').pop()};
              });
              return res;
            })()""")
            out[f"{w}@{dpr}"] = r
    page.emulate(1440, 900, dpr=1)
    page.navigate(srv.base + "/solutions/geothermal/")
    page.wait_load()
    out["locator@1440"] = page.js("(() => { const i = document.querySelector('.locator-figure img'); const r = i.getBoundingClientRect(); return {w: r.width, h: r.height}; })()")
finally:
    page.close()
    chrome.close()
    srv.close()

mx = {}
for key, bands in out.items():
    if not key.startswith("locator"):
        for bid, v in bands.items():
            mx[bid] = max(mx.get(bid, 0), v["drawn_w"])
print(json.dumps({"max_drawn_css": mx, "samples": {k: out[k] for k in ("390@2", "1440@2", "3840@1", "3840@2")}, "locator": out["locator@1440"]}, indent=1))
