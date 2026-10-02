#!/usr/bin/env python3
"""Act 3 layer-switch and inspection-aid smoothness: frame gaps during switches, per class/CPU rate.

    python measure_switch.py <repo_root> <out.json>
"""
import json
import sys
import time

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from mer216_harness import Chrome, serve  # noqa: E402

CLASSES = [("1440x900@2x-cpu4x", 1440, 900, 2.0, 4), ("1440x900@2x-cpu6x", 1440, 900, 2.0, 6),
           ("390x844@3x-cpu6x", 390, 844, 3.0, 6)]

SCROLL_TO = r"""
(async (sel) => {
  const el = document.querySelector(sel);
  el.scrollIntoView({block: 'center', behavior: 'instant'});
  await new Promise(r => setTimeout(r, 2500));
  const imgs = Array.from(el.querySelectorAll('img'));
  return imgs.map(i => ({src: (i.currentSrc||'').split('/').pop(), complete: i.complete, loading: i.loading}));
})(%s)
"""

SWITCH = r"""
(async (labelSel) => {
  const gaps = [];
  let last = performance.now(), stop = false;
  const tick = (t) => { gaps.push(t - last); last = t; if (!stop) requestAnimationFrame(tick); };
  requestAnimationFrame(tick);
  await new Promise(r => setTimeout(r, 300));
  const t0 = performance.now();
  gaps.length = 0;
  document.querySelector(labelSel).click();
  await new Promise(r => setTimeout(r, 900));
  stop = true;
  const dt = performance.now() - t0;
  return {max_gap_ms: Math.round(Math.max(...gaps)*10)/10, over_20ms: gaps.filter(g => g > 20).length, over_34ms: gaps.filter(g => g > 34).length, frames: gaps.length, span_ms: Math.round(dt)};
})(%s)
"""

DRAG = r"""
(async () => {
  const range = document.querySelector('.inspect-range');
  const gaps = []; let last = performance.now(), stop = false;
  const tick = (t) => { gaps.push(t - last); last = t; if (!stop) requestAnimationFrame(tick); };
  requestAnimationFrame(tick);
  await new Promise(r => setTimeout(r, 200)); gaps.length = 0;
  for (let i = 0; i <= 100; i += 2) { range.value = i; range.dispatchEvent(new Event('input', {bubbles: true})); await new Promise(r => requestAnimationFrame(r)); }
  for (let i = 100; i >= 0; i -= 2) { range.value = i; range.dispatchEvent(new Event('input', {bubbles: true})); await new Promise(r => requestAnimationFrame(r)); }
  stop = true;
  return {max_gap_ms: Math.round(Math.max(...gaps)*10)/10, over_20ms: gaps.filter(g => g > 20).length, over_34ms: gaps.filter(g => g > 34).length, frames: gaps.length};
})()
"""


def main():
    root, out = sys.argv[1], sys.argv[2]
    srv = serve(root)
    chrome = Chrome()
    res = []
    try:
        for name, w, h, dpr, cpu in CLASSES:
            page = chrome.new_page()
            page.send("Network.setCacheDisabled", {"cacheDisabled": True})
            page.emulate(w, h, dpr, mobile=w < 700, reduced_motion=False)
            if cpu > 1:
                page.send("Emulation.setCPUThrottlingRate", {"rate": cpu})
            page.navigate(srv.base + "/")
            r = {"class": name}
            r["act3_images"] = page.js(SCROLL_TO % json.dumps(".evidence-frame"))
            r["act3_switch"] = []
            for lab in ('label[for="ev-thermal"]', 'label[for="ev-alteration"]', 'label[for="ev-terrain"]', 'label[for="ev-thermal"]'):
                r["act3_switch"].append({"label": lab, **page.js(SWITCH % json.dumps(lab))})
            r["inspect_images"] = page.js(SCROLL_TO % json.dumps(".inspect-frame"))
            r["inspect_pair_switch"] = []
            for lab in ('label[for="cp-alteration"]', 'label[for="cp-priority"]', 'label[for="cp-thermal"]'):
                r["inspect_pair_switch"].append({"label": lab, **page.js(SWITCH % json.dumps(lab))})
            r["inspect_drag"] = page.js(DRAG)
            res.append(r)
            print(name, [s["max_gap_ms"] for s in r["act3_switch"]], [s["max_gap_ms"] for s in r["inspect_pair_switch"]], r["inspect_drag"]["max_gap_ms"])
            page.close()
    finally:
        chrome.close()
        srv.close()
    json.dump(res, open(out, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
