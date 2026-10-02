#!/usr/bin/env python3
"""Rendered CSS width of every analytical <img> across viewport widths/heights (layout only)."""
import json
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from mer216_harness import Chrome, serve  # noqa: E402

PROBE = r"""
(() => {
  const q = (s) => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().width*10)/10 : null; };
  return {
    act3: q('.evidence-plate[data-layer="terrain"] img'),
    result: q('.sec-result .panel-image, .sec-result img[src*="priority"]'),
    inspectLayer: q('.inspect-layer[data-pair="priority"] img'),
    inspectBase: q('.inspect-base img'),
    context: q('#context img, .sec-context img'),
  };
})()
"""

root = sys.argv[1]
widths = [320, 360, 375, 390, 414, 480, 560, 561, 600, 700, 701, 768, 820, 900, 1000, 1001, 1024, 1100, 1200, 1280, 1366, 1440, 1600, 1920, 2560]
heights = [700, 800, 900, 1080]
srv = serve(root)
chrome = Chrome()
out = []
try:
    page = chrome.new_page()
    for h in heights:
        for w in widths:
            page.emulate(w, h, 1.0, mobile=False, reduced_motion=True)
            page.navigate(srv.base + "/")
            r = page.js(PROBE)
            r.update(w=w, h=h)
            out.append(r)
finally:
    chrome.close()
    srv.close()
json.dump(out, open(sys.argv[2], "w"), indent=0)
print(len(out))
