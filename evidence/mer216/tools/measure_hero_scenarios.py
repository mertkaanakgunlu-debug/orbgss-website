#!/usr/bin/env python3
"""Hero fallback / resilience scenarios in a real Chrome.

    python measure_hero_scenarios.py <repo_root> <out.json> [--only a,b]

Each scenario injects one condition before page script runs (or via CDP), loads the homepage, lets
the hero run, and records final state/reason, chosen tier/codec, video bytes and requests, and a
luminance series of the hero (blank/black detection).
"""
import argparse
import json
import sys
import time

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
import measure_hero as mh  # noqa: E402
from mer216_harness import Chrome, serve  # noqa: E402

NO_WEBM = "(()=>{const o=HTMLMediaElement.prototype.canPlayType;HTMLMediaElement.prototype.canPlayType=function(t){return /webm/.test(t)?'':o.call(this,t)}})();"
PLAY_REJECT = "HTMLMediaElement.prototype.play=function(){return Promise.reject(new DOMException('blocked','NotAllowedError'))};"
NO_MC = "Object.defineProperty(navigator,'mediaCapabilities',{configurable:true,get:()=>undefined});"
MC_UNSUPPORTED = "Object.defineProperty(navigator,'mediaCapabilities',{configurable:true,get:()=>({decodingInfo:()=>Promise.resolve({supported:false,smooth:false,powerEfficient:false})})});"
MC_NOT_SMOOTH_HI = ("Object.defineProperty(navigator,'mediaCapabilities',{configurable:true,get:()=>({decodingInfo:(c)=>Promise.resolve("
                    "{supported:true,smooth:c.video.width<=1280,powerEfficient:false})})});")
MC_HANG = "Object.defineProperty(navigator,'mediaCapabilities',{configurable:true,get:()=>({decodingInfo:()=>new Promise(()=>{})})});"
DROPS = ("HTMLVideoElement.prototype.getVideoPlaybackQuality=function(){return {totalVideoFrames:Math.round(this.currentTime*24),"
         "droppedVideoFrames:Math.round(this.currentTime*24*0.6),corruptedVideoFrames:0,creationTime:performance.now()}};")
ZERO_W = "Object.defineProperty(HTMLVideoElement.prototype,'videoWidth',{configurable:true,get:()=>0});"


def conn(eff="4g", down=10, save=False):
    return ("Object.defineProperty(navigator,'connection',{configurable:true,get:()=>({effectiveType:'%s',downlink:%s,rtt:50,saveData:%s,"
            "addEventListener(){},removeEventListener(){}})});" % (eff, down, str(save).lower()))


# name -> (viewport w,h,dpr, init_js, net profile, reduced, cpu, blocked_urls, script_disabled, hold)
S = {
    "baseline-1920@1x-fast": (1920, 1080, 1.0, conn(), "none", False, 1, None, False, 15),
    "mp4-only (no WebM support)": (1920, 1080, 1.0, NO_WEBM + conn(), "none", False, 1, None, False, 15),
    "mp4-only 1280": (1280, 720, 1.0, NO_WEBM + conn(), "none", False, 1, None, False, 15),
    "downlink 4 Mbps": (1920, 1080, 1.0, conn(down=4), "dsl-4mbps", False, 1, None, False, 24),
    "downlink 1.6 Mbps (-> sm)": (1920, 1080, 1.0, conn(down=1.6), "slow-4g", False, 1, None, False, 20),
    "downlink 1.0 Mbps (-> still)": (1920, 1080, 1.0, conn(down=1.0), "none", False, 1, None, False, 8),
    "effectiveType 3g (-> still)": (1920, 1080, 1.0, conn(eff="3g", down=1.6), "none", False, 1, None, False, 8),
    "Save-Data (-> still)": (1920, 1080, 1.0, conn(save=True), "none", False, 1, None, False, 8),
    "reduced motion (-> still)": (1920, 1080, 1.0, conn(), "none", True, 1, None, False, 8),
    "phone 375@3x (-> still)": (375, 812, 3.0, conn(), "none", False, 1, None, False, 8),
    "no JavaScript": (1920, 1080, 1.0, "", "none", False, 1, None, True, 6),
    "video blocked (404/encode error)": (1920, 1080, 1.0, conn(), "none", False, 1, ["*.webm", "*.mp4"], False, 8),
    "autoplay refused": (1920, 1080, 1.0, PLAY_REJECT + conn(), "none", False, 1, None, False, 8),
    "decoder: unsupported": (1920, 1080, 1.0, MC_UNSUPPORTED + conn(), "none", False, 1, None, False, 8),
    "decoder: 1920 not smooth (-> sm)": (1920, 1080, 1.0, MC_NOT_SMOOTH_HI + conn(), "none", False, 1, None, False, 15),
    "mediaCapabilities absent": (1920, 1080, 1.0, NO_MC + conn(), "none", False, 1, None, False, 15),
    "mediaCapabilities never answers": (1920, 1080, 1.0, MC_HANG + conn(), "none", False, 1, None, False, 15),
    "dropped frames 60%": (1920, 1080, 1.0, DROPS + conn(), "none", False, 1, None, False, 12),
    "decoder paints nothing (videoWidth 0)": (1920, 1080, 1.0, ZERO_W + conn(), "none", False, 1, None, False, 8),
    "mid-play network collapse": (1920, 1080, 1.0, conn(), "none", False, 1, None, False, 30),
}
mh.NET["stall"] = {"offline": False, "latency": 400, "downloadThroughput": 8 * 1024, "uploadThroughput": 8 * 1024}
mh.DOWNLINK["stall"] = 10


def run(chrome, srv, name, spec):
    from mer216_harness import Handler
    Handler.video_throttle = (400_000, 15_000) if name == "mid-play network collapse" else None
    w, h, dpr, init, net, reduced, cpu, blocked, nojs, hold = spec
    page = chrome.new_page()
    page.send("Network.setCacheDisabled", {"cacheDisabled": True})
    if nojs:
        page.send("Emulation.setScriptExecutionDisabled", {"value": True})
    else:
        page.send("Page.addScriptToEvaluateOnNewDocument", {"source": mh.INIT})
        if init:
            page.send("Page.addScriptToEvaluateOnNewDocument", {"source": init})
    page.emulate(w, h, dpr, mobile=False, reduced_motion=reduced)
    if blocked:
        page.send("Network.setBlockedURLs", {"urls": blocked})
    if net not in ("none", "stall"):
        page.send("Network.emulateNetworkConditions", dict(mh.NET[net]))
    stalled = False
    t0 = time.time()
    page.navigate(srv.base + "/", wait=False)
    page.events.clear()
    reqs, lum, snaps = {}, [], []
    shots = [0.5, 2, 5, 8, 12, 16, 20]
    while time.time() - t0 < hold:
        page.pump(0.25)
        if net == "stall" and not stalled and not nojs:
            try:
                if page.js("document.querySelector('.hero').dataset.heroTier || ''"):
                    page.send("Network.emulateNetworkConditions", dict(mh.NET["stall"]))
                    stalled = True
                    out_t = round(time.time() - t0, 1)
            except Exception:
                pass
        el = time.time() - t0
        if shots and el >= shots[0]:
            shots.pop(0)
            try:
                r = page.send("Page.captureScreenshot", {"format": "png", "clip": {"x": 0, "y": 0, "width": min(w, 640), "height": min(h, 360), "scale": 0.25}}, timeout=20)
                lum.append({"t": round(el, 1), "mean_min_max": mh.luminance(r["data"])})
            except Exception as e:  # noqa: BLE001
                lum.append({"t": round(el, 1), "err": str(e)[:60]})
    out = {"scenario": name}
    if not nojs:
        snap = page.js(mh.SNAP)
        out["state"] = snap["state"]
        out["reason"] = snap["reason"]
        out["layer"] = snap["layer"]
        out["video_opacity"] = snap["opacity"]
        out["quality"] = snap["quality"]
        hero = page.js("window.__hero")
        out["tier"] = page.js("document.querySelector('.hero').dataset.heroTier||null")
        out["codec"] = page.js("document.querySelector('.hero').dataset.heroCodec||null")
        out["waiting_events"] = hero["waiting"]
        out["state_timeline"] = [e for e in hero["events"] if e["name"].startswith("attr:")][:12]
    for ev in page.events:
        m, p = ev.get("method"), ev.get("params", {})
        if m == "Network.requestWillBeSent":
            u = p["request"]["url"]
            if u.endswith((".webm", ".mp4")):
                reqs[p["requestId"]] = {"file": u.split("/")[-1], "range": p["request"]["headers"].get("Range"), "bytes": 0}
        elif m == "Network.dataReceived" and p["requestId"] in reqs:
            reqs[p["requestId"]]["bytes"] += int(p["dataLength"])
    out["video_requests"] = list(reqs.values())
    out["video_bytes_total"] = sum(r["bytes"] for r in reqs.values())
    out["luminance"] = lum
    out["blank_samples"] = [x for x in lum if "mean_min_max" in x and x["mean_min_max"][0] < 6]
    page.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("out")
    ap.add_argument("--only")
    a = ap.parse_args()
    srv = serve(a.root)
    chrome = Chrome()
    res = []
    try:
        for name in (a.only.split("|") if a.only else S):
            r = run(chrome, srv, name, S[name])
            res.append(r)
            print(f"{name:42s} state={r.get('state')} reason={r.get('reason')} tier={r.get('tier')} codec={r.get('codec')} "
                  f"vbytes={r['video_bytes_total']} reqs={len(r['video_requests'])} blank={len(r['blank_samples'])}", flush=True)
    finally:
        chrome.close()
        srv.close()
    json.dump(res, open(a.out, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
