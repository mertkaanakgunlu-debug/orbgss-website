#!/usr/bin/env python3
"""Side-by-side comparison sheets: Production | Atlas preview | Agate (this branch).

usage: compose.py FINAL_DIR OUT_DIR   (FINAL_DIR holds the production/, atlas/ and agate/ folders written by capture.py)
"""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont
SH = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)  # SH holds production/, atlas/ and agate/ capture folders
BUILDS = [("production", "Production (orbgss.com today)"), ("atlas", "Atlas preview (base of this PR)"), ("agate", "Agate brand (this PR)")]
BG = (24, 27, 28); FG = (227, 229, 228); MUTE = (140, 150, 147); GAP = 24; PAD = 28
try:
    F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22); FS = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 17)
except Exception:
    F = FS = ImageFont.load_default()

def load(build, name, colw):
    for ext in ("jpg", "png"):
        p = SH / build / f"{name}.{ext}"
        if p.exists():
            im = Image.open(p).convert("RGB")
            if im.width != colw: im = im.resize((colw, round(im.height * colw / im.width)), Image.LANCZOS)
            return im
    return None

def sheet(title, rows, colw, out, quality=88):
    """rows: list of (label, imagename) ; each image is looked up in every build."""
    cells = [[load(b, n, colw) for b, _ in BUILDS] for _, n in rows]
    W = PAD * 2 + colw * 3 + GAP * 2
    heights = [max([c.height for c in r if c] or [60]) for r in cells]
    H = PAD * 2 + 44 + sum(heights) + sum(34 for _ in rows) + GAP * (len(rows) - 1) + 36
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.text((PAD, PAD - 6), title, font=F, fill=FG)
    y = PAD + 44
    for i, ((label, _), r) in enumerate(zip(rows, cells)):
        for j, (b, bl) in enumerate(BUILDS):
            x = PAD + j * (colw + GAP)
            short = bl.split(" (")[0] if colw < 600 else bl
            d.text((x, y), f"{short}  -  {label}" if (i == 0 and colw >= 600) else (short if colw < 600 else f"{label}"), font=FS, fill=MUTE)
        y += 30
        for j, c in enumerate(r):
            x = PAD + j * (colw + GAP)
            if c: im.paste(c, (x, y))
            else: d.text((x + 8, y + 8), "(no such page in this build)", font=FS, fill=MUTE)
        y += heights[i] + GAP
    im.save(out, "JPEG", quality=quality, optimize=True); print(out.name, im.size, round(out.stat().st_size / 1e6, 1), "MB")

for w, tag in ((1440, "d1440"), (390, "m390")):
    colw = 900 if w == 1440 else 390
    sheet(f"Homepage - hero ({w}px): first frame, then settled", [("hero, 0.9 s after load", f"home-{tag}-hero-t1"), ("hero, sequence settled", f"home-{tag}-hero-settled")], colw, OUT / f"01-home-hero-{tag}.jpg")
    sheet(f"Homepage - header and Acts 2-4 ({w}px)", [("header", f"home-{tag}-header"), ("Act 2 - Kizildere natural-colour band", f"home-{tag}-act2-context"), ("Act 3 - evidence trio", f"home-{tag}-act3-evidence"), ("Act 4 - priority result", f"home-{tag}-act4-priority")], colw, OUT / f"02-home-acts-{tag}.jpg")
    sheet(f"Homepage - inspection aid, Solutions cards, footer ({w}px)", [("inspection aid", f"home-{tag}-inspection"), ("Solutions cards", f"home-{tag}-solutions"), ("footer", f"home-{tag}-footer")], colw, OUT / f"03-home-lower-{tag}.jpg")
sheet("Brand close-ups at 3x: header and footer logo", [("header logo", "logo-header-3x"), ("footer logo", "logo-footer-3x")], 520, OUT / "00-logo-closeups.jpg")
sheet("Mobile menu open (390px)", [("menu open", "home-m390-menu-open")], 390, OUT / "01b-home-menu-open-m390.jpg")
pages = [("solutions", "Solutions"), ("solutions-geothermal", "Solutions / Geothermal"), ("about", "About"), ("partner", "Partner with us"), ("sources", "Sources")]
for i, (slug, label) in enumerate(pages):
    for w, tag, colw in ((1440, "d1440", 700), (390, "m390", 390)):
        sheet(f"{label} ({w}px, full length)", [(label, f"{slug}-{tag}-full")], colw, OUT / f"{4+i:02d}-{slug}-{tag}.jpg")
