#!/usr/bin/env python3
"""Measure how wide the interior-page photographs are actually drawn, in a real browser (MER-255).

    python3 scripts/measure_interior_renders.py            # measure and print
    python3 scripts/measure_interior_renders.py --write    # ... and record it in sources.json

Local QA tooling (Playwright + Chromium), never a site runtime dependency and never run on Vercel.
It serves the working tree with Vercel's cleanUrls/trailingSlash behaviour, loads each English
interior route at four viewports and two device pixel ratios, and for every recorded photograph reads
the rendered CSS width, the candidate the browser actually selected (`currentSrc`) and that file's
native width. The result is written to the records the validator holds to a bound:

  * web_m6.interior_crops[].rendered           (the MER-255 Kızıldere crops)
  * scenes[].web_m6_placement.rendered         (the Solutions photographs)

Index thumbnails (class "thumb") and the layer-diagram frames are not placements and are skipped.
Class A photography may be stretched, but the validator refuses a layout that draws a candidate wider
than its own pixels at 1x or by more than MAX_UPSCALE at 2x.
"""
from __future__ import annotations

import http.server
import json
import math
import os
import pathlib
import sys
import threading
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "imagery" / "sources.json"
ROUTES = {"solutions": "/solutions/", "solutions/geothermal": "/solutions/geothermal/",
          "about": "/about/", "partner": "/partner/"}
# 19 widths from a small phone to a 4K monitor; the height is a typical window for that width.
VIEWPORTS = [(w, 844 if w < 600 else 1112 if w < 1000 else 900) for w in
             (360, 390, 414, 600, 768, 834, 1024, 1180, 1280, 1366, 1440, 1536, 1680, 1920, 2200, 2560,
              3000, 3440, 3840)]
DPRS = (1, 2)


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return str(ROOT / urllib.parse.unquote(path.split("?")[0].split("#")[0]).lstrip("/"))

    def log_message(self, *args):
        pass

    def do_GET(self):
        path = urllib.parse.urlsplit(self.path).path
        fs = ROOT / path.lstrip("/")
        if path.endswith("/") and (fs / "index.html").exists():
            self.path = path + "index.html"
        return super().do_GET()


def serve() -> tuple[http.server.ThreadingHTTPServer, str]:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def main(argv: list[str]) -> int:
    from playwright.sync_api import sync_playwright

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    crops = manifest["web_m6"]["interior_crops"]
    scenes = [s for s in manifest["scenes"] if s.get("web_m6_placement")]
    # file name -> (kind, id, pixel width). The pixel width comes from the record, not from the
    # element: `img.naturalWidth` is the width in CSS px at the density of the selected candidate,
    # so it reads half the real width for a 2x candidate.
    owner: dict[str, tuple[str, str, int, float]] = {}
    for crop in crops:
        for deriv in crop["derivatives"]:
            owner[pathlib.PurePosixPath(deriv["path"]).name] = ("crop", crop["id"], deriv["width_px"],
                                                                deriv["width_px"] / deriv["height_px"])
    for scene in scenes:
        for deriv in scene["derivatives"]:
            owner[pathlib.PurePosixPath(deriv["path"]).name] = ("scene", scene["id"], deriv["width_px"],
                                                                deriv["width_px"] / deriv["height_px"])

    server, base = serve()
    worst: dict[tuple[str, str], dict] = {}
    try:
        with sync_playwright() as pw:
            kwargs = {"args": ["--no-sandbox"]}
            exe = os.environ.get("CHROMIUM_PATH") or ("/opt/pw-browsers/chromium"
                                                      if pathlib.Path("/opt/pw-browsers/chromium").exists() else None)
            if exe:
                kwargs["executable_path"] = exe
            browser = pw.chromium.launch(**kwargs)
            for width, height in VIEWPORTS:
                for dpr in DPRS:
                    ctx = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=dpr,
                                              is_mobile=width < 600, has_touch=width < 1000)
                    for route, url in ROUTES.items():
                        page = ctx.new_page()
                        page.goto(base + url, wait_until="load")
                        page.add_style_tag(content="html{scroll-behavior:auto!important}")
                        total = page.evaluate("document.documentElement.scrollHeight")
                        y = 0
                        while y < total:
                            page.evaluate(f"window.scrollTo(0,{y})")
                            page.wait_for_timeout(80)
                            y += int(height * 0.8)
                        page.wait_for_function("[...document.images].every(i => i.complete)", timeout=20000)
                        rows = page.evaluate("""() => [...document.images]
                            .filter(i => !i.classList.contains('thumb') && !i.closest('.plane'))
                            .map(i => { const r = i.getBoundingClientRect();
                                        return {src: i.currentSrc, css: r.width, h: r.height, nat: i.naturalWidth,
                                                fit: getComputedStyle(i).objectFit}; })""")
                        for row in rows:
                            name = pathlib.PurePosixPath(urllib.parse.urlsplit(row["src"]).path).name
                            if name not in owner or row["nat"] == 0:
                                continue
                            kind, ident, pixels, aspect = owner[name]
                            key = (kind, ident)
                            # object-fit: cover draws the image at the larger of the box width and the
                            # box height times the image aspect; the box alone would under-report it.
                            if row["fit"] == "cover":
                                row["css"] = max(row["css"], row["h"] * aspect)
                            upscale = row["css"] * dpr / pixels
                            rec = worst.setdefault(key, {"max_css": 0.0, "max_upscale": 0.0, "at": "", "selected": "",
                                                         "selected_at_max": ""})
                            if row["css"] > rec["max_css"]:
                                rec["max_css"] = row["css"]
                                rec["selected_at_max"] = urllib.parse.urlsplit(row["src"]).path.lstrip("/")
                                rec["at_max_css"] = f"{width}x{height} @{dpr}x"
                            if upscale > rec["max_upscale"]:
                                rec["max_upscale"] = upscale
                                rec["at"] = f"{width}x{height} @{dpr}x"
                                rec["selected"] = urllib.parse.urlsplit(row["src"]).path.lstrip("/")
                        page.close()
                    ctx.close()
            browser.close()
    finally:
        server.shutdown()

    viewports = [f"{w}x{h}" for w, h in VIEWPORTS]
    for (kind, ident), rec in sorted(worst.items()):
        print(f"{kind:5} {ident:22} max {rec['max_css']:.0f} CSS px ({rec['at_max_css']}), "
              f"worst upscale {rec['max_upscale']:.2f}x at {rec['at']}")
    if "--write" not in argv:
        return 0

    def rendered_record(rec: dict, derivatives: list[dict]) -> dict:
        widths = {d["path"]: d["width_px"] for d in derivatives}
        widest = max(widths.values())
        css = math.ceil(rec["max_css"])
        return {
            "tool": "scripts/measure_interior_renders.py",
            "measurement_method": "Headless Chromium on the English route at 19 viewport widths from 360 to 3840 CSS px at "
                                  "DPR 1 and 2; the drawn width of the image (for object-fit: cover, the larger of the box "
                                  "width and the box height times the image aspect) and the candidate the browser selected "
                                  "(currentSrc) are recorded, never the sizes attribute.",
            "viewports_measured": viewports,
            "device_pixel_ratios_measured": list(DPRS),
            "max_css_width": css,
            "device_pixel_ratio_considered": 2,
            "max_device_px": css * 2,
            "widest_candidate_px": widest,
            "selected_derivative": rec["selected_at_max"],
            "max_upscale_factor": round(rec["max_upscale"], 3),
            "max_upscale_at": rec["at"],
        }

    missing = [c["id"] for c in crops if ("crop", c["id"]) not in worst]
    missing += [s["id"] for s in scenes if ("scene", s["id"]) not in worst]
    if missing:
        print(f"not measured on any page: {missing}", file=sys.stderr)
        return 1
    for crop in crops:
        crop["rendered"] = rendered_record(worst[("crop", crop["id"])], crop["derivatives"])
    for scene in scenes:
        rendered = scene["web_m6_placement"].setdefault("rendered", {})
        rendered.pop("measured_max_css_width", None)  # superseded by max_css_width below
        rendered.update(rendered_record(worst[("scene", scene["id"])], scene["derivatives"]))
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("sources.json updated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
