#!/usr/bin/env python3
"""Phase 1 / 4 probe: rendered boxes vs device-pixel demand vs decoded size for every analytical
and context image on the homepage, per viewport / DPR class, in a real Chrome.

    python measure_analytical.py <repo_root> <out.json> [--classes all|quick]
"""
import json
import sys
import time

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from mer216_harness import Chrome, serve  # noqa: E402

CLASSES = [
    ("mobile-375@3x", 375, 812, 3.0, True),
    ("mobile-390@3x", 390, 844, 3.0, True),
    ("tablet-768@2x", 768, 1024, 2.0, False),
    ("w1024@2x", 1024, 768, 2.0, False),
    ("w1024@1x", 1024, 768, 1.0, False),
    ("w1280@1x", 1280, 800, 1.0, False),
    ("w1440@1x", 1440, 900, 1.0, False),
    ("w1440@2x", 1440, 900, 2.0, False),
    ("w1920@1x", 1920, 1080, 1.0, False),
    ("w1920@2x (4K @200%)", 1920, 1080, 2.0, False),
    ("w2560@1.5x (4K @150%)", 2560, 1440, 1.5, False),
    ("w3840@1x (4K @100%)", 3840, 2160, 1.0, False),
]

PROBE = r"""
(async () => {
  const sel = 'img';
  const imgs = Array.from(document.querySelectorAll(sel));
  const out = [];
  for (const img of imgs) {
    const r = img.getBoundingClientRect();
    const cs = getComputedStyle(img);
    const src = img.currentSrc || img.src;
    out.push({
      alt: (img.getAttribute('alt')||'').slice(0,40),
      cls: img.className,
      parent: img.closest('[data-layer],[data-pair],.inspect-base,.hero-visual,.act-4,.sec')?.id || img.closest('[data-layer],[data-pair]')?.getAttribute('data-layer') || img.closest('[data-pair]')?.getAttribute('data-pair') || '',
      src: src.replace(location.origin + '/', ''),
      loading: img.loading,
      complete: img.complete,
      natural: [img.naturalWidth, img.naturalHeight],
      box: [Math.round(r.width*100)/100, Math.round(r.height*100)/100],
      display: cs.display, visibility: cs.visibility, opacity: cs.opacity,
      objectFit: cs.objectFit,
      sizes: img.sizes || '',
    });
  }
  const res = performance.getEntriesByType('resource').filter(e => e.initiatorType === 'img' || /\.(webp|png|jpg)/.test(e.name))
    .map(e => ({name: e.name.replace(location.origin + '/', ''), encoded: e.encodedBodySize, transfer: e.transferSize, decoded: e.decodedBodySize}));
  return {imgs: out, resources: res, dpr: devicePixelRatio, vw: innerWidth, vh: innerHeight,
          scrollW: document.documentElement.scrollWidth, scrollH: document.documentElement.scrollHeight};
})()
"""

SCROLL = r"""
(async () => {
  const H = document.documentElement.scrollHeight;
  const step = Math.max(300, Math.floor(innerHeight * 0.6));
  for (let y = 0; y < H; y += step) {
    window.scrollTo({top: y, behavior: 'instant'});
    await new Promise(r => setTimeout(r, 120));
  }
  window.scrollTo({top: 0, behavior: 'instant'});
  const imgs = Array.from(document.images);
  await Promise.race([Promise.all(imgs.map(i => i.complete ? 1 : new Promise(r => { i.addEventListener('load', r, {once:true}); i.addEventListener('error', r, {once:true}); }))),
                      new Promise(r => setTimeout(r, 8000))]);
  return H;
})()
"""


def main():
    root, out_path = sys.argv[1], sys.argv[2]
    quick = len(sys.argv) > 3 and sys.argv[3] == "quick"
    srv = serve(root)
    chrome = Chrome()
    results = []
    try:
        for name, w, h, dpr, mobile in (CLASSES[:3] if quick else CLASSES):
            page = chrome.new_page()
            page.send("Network.setCacheDisabled", {"cacheDisabled": True})
            page.emulate(w, h, dpr, mobile=mobile, reduced_motion=True)
            page.navigate(srv.base + "/")
            page.js(SCROLL, timeout=90)
            time.sleep(0.8)
            data = page.js(PROBE)
            data["class"] = name
            results.append(data)
            page.close()
            print("done", name, data["scrollW"], "x", data["scrollH"])
    finally:
        chrome.close()
        srv.close()
    json.dump(results, open(out_path, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
