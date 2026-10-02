#!/usr/bin/env python3
"""Hero playback probe in a real Chrome: selected source, bytes, startup, dropped frames, state
timeline and blank-frame check, per viewport / DPR / network / CPU class.

    python measure_hero.py <repo_root> <out.json> [--only name1,name2] [--hold 14]
"""
import argparse
import base64
import io
import json
import sys
import time

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from mer216_harness import Chrome, serve  # noqa: E402

NET = {
    "none": None,
    "fast-4g": {"offline": False, "latency": 60, "downloadThroughput": 9 * 1024 * 1024 / 8, "uploadThroughput": 4 * 1024 * 1024 / 8},
    "slow-4g": {"offline": False, "latency": 150, "downloadThroughput": 1.6 * 1024 * 1024 / 8, "uploadThroughput": 750 * 1024 / 8},
    "dsl-4mbps": {"offline": False, "latency": 40, "downloadThroughput": 4 * 1024 * 1024 / 8, "uploadThroughput": 1024 * 1024 / 8},
}

CLASSES = {
    "1280x720@1x": (1280, 720, 1.0, "none", 1),
    "1366x768@1x": (1366, 768, 1.0, "none", 1),
    "1440x900@1x": (1440, 900, 1.0, "none", 1),
    "1440x900@2x": (1440, 900, 2.0, "none", 1),
    "1920x1080@1x": (1920, 1080, 1.0, "none", 1),
    "1920x1080@2x": (1920, 1080, 2.0, "none", 1),
    "2560x1440@1.5x": (2560, 1440, 1.5, "none", 1),
    "3840x2160@1x": (3840, 2160, 1.0, "none", 1),
    "1920x1080@1x-dsl4": (1920, 1080, 1.0, "dsl-4mbps", 1),
    "1920x1080@1x-slow4g": (1920, 1080, 1.0, "slow-4g", 1),
    "1440x900@2x-cpu4x": (1440, 900, 2.0, "none", 4),
    "1920x1080@1x-cpu6x": (1920, 1080, 1.0, "none", 6),
}

INIT = r"""
(() => {
  window.__hero = {events: [], t0: performance.now(), rvfc: [], waiting: 0};
  const log = (name, extra) => window.__hero.events.push(Object.assign({t: Math.round(performance.now()), name}, extra||{}));
  const onReady = () => {
    const hero = document.querySelector('.hero');
    const video = document.querySelector('.hero-video');
    if (!hero || !video) return;
    new MutationObserver((muts) => {
      for (const m of muts) log('attr:' + m.attributeName, {v: hero.getAttribute(m.attributeName)});
    }).observe(hero, {attributes: true, attributeFilter: ['data-hero-state', 'data-hero-reason', 'data-hero-layer', 'data-hero-payoff']});
    ['loadstart','loadedmetadata','loadeddata','canplay','canplaythrough','playing','waiting','stalled','pause','ended','error','suspend','emptied'].forEach(e =>
      video.addEventListener(e, () => { if (e === 'waiting') window.__hero.waiting++; log('video:' + e, {rs: video.readyState, ct: Math.round(video.currentTime*1000)/1000}); }));
    if (video.requestVideoFrameCallback) {
      let n = 0;
      const cb = (now, md) => { if (n++ < 4) window.__hero.rvfc.push({t: Math.round(now), mediaTime: md.mediaTime, w: md.width, h: md.height}); video.requestVideoFrameCallback(cb); };
      video.requestVideoFrameCallback(cb);
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', onReady); else onReady();
})();
"""

SNAP = r"""
(() => {
  const v = document.querySelector('.hero-video');
  const h = document.querySelector('.hero');
  const q = v && v.getVideoPlaybackQuality ? v.getVideoPlaybackQuality() : null;
  const c = navigator.connection || {};
  return {
    state: h.getAttribute('data-hero-state'), reason: h.getAttribute('data-hero-reason'),
    layer: h.getAttribute('data-hero-layer'), payoff: h.getAttribute('data-hero-payoff'),
    src: v ? v.currentSrc : null, videoW: v ? v.videoWidth : null, videoH: v ? v.videoHeight : null,
    ct: v ? v.currentTime : null, paused: v ? v.paused : null, ended: v ? v.ended : null,
    quality: q ? {total: q.totalVideoFrames, dropped: q.droppedVideoFrames, corrupted: q.corruptedVideoFrames} : null,
    opacity: v ? getComputedStyle(v).opacity : null,
    conn: {type: c.effectiveType, downlink: c.downlink, rtt: c.rtt, saveData: c.saveData},
    dpr: devicePixelRatio, vw: innerWidth, vh: innerHeight,
    tiers: h.querySelector('.hero-video')?.getAttribute('data-hero-tiers') ? 'declared' : 'none',
  };
})()
"""


def luminance(png_b64):
    from PIL import Image
    im = Image.open(io.BytesIO(base64.b64decode(png_b64))).convert("L").resize((64, 36))
    px = list(im.getdata())
    return round(sum(px) / len(px), 1), min(px), max(px)


DOWNLINK = {"none": 10, "fast-4g": 9, "dsl-4mbps": 4, "slow-4g": 1.6}


def conn_override(net, eff="4g", saveData=False):
    d = DOWNLINK[net]
    return ("Object.defineProperty(navigator,'connection',{configurable:true,get:()=>({effectiveType:'%s',downlink:%s,rtt:50,saveData:%s,"
            "addEventListener(){},removeEventListener(){}})});" % (eff, d, str(saveData).lower()))


def run_class(chrome, srv, name, spec, hold, reduced=False, extra_init=None):
    w, h, dpr, net, cpu = spec
    if extra_init is None:
        extra_init = conn_override(net)
    page = chrome.new_page()
    page.send("Network.setCacheDisabled", {"cacheDisabled": True})
    page.send("Page.addScriptToEvaluateOnNewDocument", {"source": INIT})
    if extra_init:
        page.send("Page.addScriptToEvaluateOnNewDocument", {"source": extra_init})
    page.emulate(w, h, dpr, mobile=False, reduced_motion=reduced)
    if NET[net]:
        page.send("Network.emulateNetworkConditions", dict(NET[net]))
    if cpu > 1:
        page.send("Emulation.setCPUThrottlingRate", {"rate": cpu})
    t_nav = time.time()
    page.navigate(srv.base + "/", wait=False)
    page.events.clear()
    samples = []
    shots = []
    end = t_nav + hold
    next_shot = [0.4, 1.5, 4, 8, 12]
    lum = []
    while time.time() < end:
        page.pump(0.25)
        el = time.time() - t_nav
        if next_shot and el >= next_shot[0]:
            next_shot.pop(0)
            try:
                r = page.send("Page.captureScreenshot", {"format": "png", "clip": {"x": 0, "y": 0, "width": min(w, 640), "height": min(h, 360), "scale": 0.25}}, timeout=20)
                lum.append({"t": round(el, 2), "lum_min_max": luminance(r["data"])})
            except Exception as e:  # noqa: BLE001
                lum.append({"t": round(el, 2), "error": str(e)[:80]})
    snap = page.js(SNAP)
    hero = page.js("window.__hero")
    # network bytes for video resources
    video_bytes = {}
    reqs = {}
    for ev in page.events:
        m, p = ev.get("method"), ev.get("params", {})
        if m == "Network.requestWillBeSent":
            reqs[p["requestId"]] = p["request"]["url"]
        elif m == "Network.loadingFinished" and p["requestId"] in reqs:
            u = reqs[p["requestId"]]
            if u.endswith((".webm", ".mp4")):
                video_bytes[u.split("/")[-1]] = video_bytes.get(u.split("/")[-1], 0) + int(p["encodedDataLength"])
        elif m == "Network.dataReceived" and p["requestId"] in reqs:
            u = reqs[p["requestId"]]
            if u.endswith((".webm", ".mp4")):
                video_bytes.setdefault("_recv_" + u.split("/")[-1], 0)
                video_bytes["_recv_" + u.split("/")[-1]] += int(p["dataLength"])
    res = page.js("performance.getEntriesByType('resource').filter(e=>/\\.(webm|mp4)/.test(e.name)).map(e=>({n:e.name.split('/').pop(),enc:e.encodedBodySize,tr:e.transferSize,start:Math.round(e.startTime),end:Math.round(e.responseEnd)}))")
    page.close()
    return {"class": name, "spec": {"w": w, "h": h, "dpr": dpr, "net": net, "cpu": cpu}, "snapshot": snap,
            "events": hero["events"], "rvfc": hero["rvfc"], "waiting_events": hero["waiting"],
            "video_bytes": video_bytes, "video_resources": res, "luminance_samples": lum}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("out")
    ap.add_argument("--only")
    ap.add_argument("--hold", type=float, default=14)
    ap.add_argument("--headful", action="store_true")
    a = ap.parse_args()
    srv = serve(a.root)
    chrome = Chrome(headless=not a.headful)
    out = []
    try:
        names = a.only.split(",") if a.only else list(CLASSES)
        for n in names:
            r = run_class(chrome, srv, n, CLASSES[n], a.hold)
            out.append(r)
            s = r["snapshot"]
            print(n, s["state"], s["reason"], (s["src"] or "").split("/")[-1], s["quality"], r["video_bytes"])
    finally:
        chrome.close()
        srv.close()
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
