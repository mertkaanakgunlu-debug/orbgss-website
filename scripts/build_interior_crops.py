#!/usr/bin/env python3
"""Build the interior-page crops of the Kızıldere natural-colour master and record them (MER-255).

    py -3.14 scripts/build_interior_crops.py            # write the files and sources.json -> web_m6.interior_crops
    py -3.14 scripts/build_interior_crops.py --check    # exit 1 if the files or the record differ from a fresh build

Local production tooling (Pillow), never a site runtime dependency; nothing runs on Vercel.

What it makes. The WEB-005B Act 2 master (`assets/imagery/kizildere-aoi-context-2025-natural.jpg`,
3200 x 1800 px, native 30 m, USGS Landsat 8 OLI, public domain) is cropped four ways for the redesigned
interior pages. Class-A natural-colour photography: a crop and an encode, nothing else. No tone, colour,
sharpening or resampling step touches a pixel inside a crop; a derivative narrower than its crop is a
Lanczos downscale, the same operation as every other responsive derivative on the site, and no
derivative is ever wider than its crop (nothing is upscaled).

Why crops rather than the Act 2 frame. The homepage shows the whole 96 x 54 km frame; M6 rule R2 keeps
one full-size appearance per visual. Each crop here is a different framing of the same ground, recorded
as its own visual with its own parent checksum, crop box and file checksums, and each is shown on exactly
one interior page.

File names carry the first 8 hex digits of a hash of the crop's pixels and encode settings, because
`/assets/` is served immutable for a year: a re-cropped file is a new name, never a silent overwrite.
"""
from __future__ import annotations

import hashlib
import io
import json
import pathlib
import sys

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import geo_frame  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "imagery" / "sources.json"
MASTER = "assets/imagery/kizildere-aoi-context-2025-natural.jpg"
WEBP_QUALITY = 82  # the same encode as the Act 2 derivatives (scripts/build_web005b_context.py)
OUT_DIR = "assets/imagery"

# id, page, crop box (left, top, right, bottom) in master pixels, derivative widths, role, and the point the
# caption on the image names ("label"). The caption's coordinates must lie inside the crop's own ground:
# the declared pilot centre where the crop contains it, otherwise the centre of the crop (MER-255 review B3).
# The pilot (AOI) centre is the centre of the analysis grid, master pixel (1141, 900).
# The AOI box is the recorded 36 x 36 km analysis grid inside the frame:
# web_005b.context.frame.aoi_in_frame x 0.169063-0.544063, y 0.166667-0.833333 of 3200 x 1800.
AOI_BOX = (541, 300, 1741, 1500)
PILOT_CENTRE_PX = (1141.0, 900.0)
PILOT_BASIS = "the declared pilot (AOI) centre, which lies inside this crop"
CENTRE_BASIS = "the centre of this crop; the crop does not contain the pilot centre"
CROPS = (
    {
        "id": "kizildere-stage",
        "page": "solutions/geothermal",
        "box": (0, 380, 3200, 1480),
        "widths": (3200, 2400, 1600),
        "role": "Geothermal page stage: a wide strip of the Büyük Menderes graben behind the headline.",
        "caption": ("scene.context.place", "scene.context.coords"),
        "label": (PILOT_CENTRE_PX, PILOT_BASIS),
    },
    {
        "id": "kizildere-aoi",
        "page": "solutions/geothermal",
        "box": (541, 300, 1741, 1500),
        "widths": (1200, 800),
        "role": "Geothermal page, the analysis area: the 36 x 36 km grid (1,200 x 1,200 cells) in natural colour.",
        "caption": ("scene.aoi.place", "scene.aoi.coords"),
        "label": (PILOT_CENTRE_PX, PILOT_BASIS),
    },
    {
        "id": "kizildere-terrain",
        "page": "about",
        "box": (1741, 0, 3200, 897),
        "widths": (1459, 1000),
        "role": "About page: eroded ground north-east of the pilot area, beyond the east edge of the analysis grid.",
        "caption": ("scene.terrain.place", "scene.terrain.coords"),
        "label": (None, CENTRE_BASIS),
    },
    {
        "id": "kizildere-valley",
        "page": "partner",
        "box": (0, 800, 1000, 1800),
        "widths": (1000, 700),
        "role": "Partner page: the cultivated graben floor in the south-west of the context frame; its eastern third overlaps the western edge of the analysis grid.",
        "caption": ("scene.valley.place", "scene.valley.coords"),
        "label": (None, CENTRE_BASIS),
    },
)


def overlap_px(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    """Area, in master pixels, shared by two (left, top, right, bottom) boxes."""
    width = min(a[2], b[2]) - max(a[0], b[0])
    height = min(a[3], b[3]) - max(a[1], b[1])
    return max(width, 0) * max(height, 0)


def label_point(box: tuple[int, int, int, int], point_px: tuple[float, float] | None, basis: str) -> dict:
    """The point the image caption names, in master pixels and as the 4-decimal WGS84 pair printed on the image."""
    px = point_px if point_px is not None else ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
    if not (box[0] <= px[0] <= box[2] and box[1] <= px[1] <= box[3]):
        raise SystemExit(f"caption point {px} lies outside the crop box {box}")
    lat, lon = geo_frame.frame_px_to_wgs84(*px)
    return {"master_px": [px[0], px[1]], "lat": round(lat, 4), "lon": round(lon, 4), "basis": basis}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build(root: pathlib.Path = ROOT) -> tuple[dict[str, bytes], list[dict]]:
    master_path = root / MASTER
    master_bytes = master_path.read_bytes()
    master = Image.open(io.BytesIO(master_bytes)).convert("RGB")
    if master.size != (3200, 1800):
        raise SystemExit(f"{MASTER} is {master.size}, expected 3200 x 1800")
    files: dict[str, bytes] = {}
    records: list[dict] = []
    for spec in CROPS:
        left, top, right, bottom = spec["box"]
        crop = master.crop(spec["box"])
        pixel_hash = sha256_bytes(crop.tobytes() + f"|webp|{WEBP_QUALITY}|m6".encode())[:8]
        derivatives = []
        for width in spec["widths"]:
            if width > crop.width:
                raise SystemExit(f"{spec['id']}: {width} px would upscale a {crop.width} px crop")
            height = round(crop.height * width / crop.width)
            image = crop if width == crop.width else crop.resize((width, height), Image.LANCZOS)
            buf = io.BytesIO()
            image.save(buf, "WEBP", quality=WEBP_QUALITY, method=6)
            data = buf.getvalue()
            rel = f"{OUT_DIR}/{spec['id']}-{pixel_hash}-{width}.webp"
            files[rel] = data
            derivatives.append({
                "path": rel,
                "width_px": width,
                "height_px": height,
                "format": "image/webp",
                "operation": (f"WebP quality {WEBP_QUALITY} encode of the crop at its native {width} px; no resize"
                              if width == crop.width else
                              f"Lanczos3 downscale of the crop to {width} px, then WebP quality {WEBP_QUALITY}"),
                "bytes": len(data),
                "sha256": sha256_bytes(data),
            })
        records.append({
            "id": spec["id"],
            "page": spec["page"],
            "role": spec["role"],
            "asset_class": "A - OrbGSS natural-colour Landsat composite, cropped",
            "parent": {
                "path": MASTER,
                "sha256": sha256_bytes(master_bytes),
                "record": "web_005b.context.master",
                "scene_id": "kizildere-aoi-context-2025",
            },
            "crop_box_px": [left, top, right, bottom],
            "crop_size_px": [crop.width, crop.height],
            "analysis_grid_box_px": list(AOI_BOX),
            "analysis_grid_overlap_px2": overlap_px(spec["box"], AOI_BOX),
            "ground_resolution_m": 30.0,
            "pixel_hash8": pixel_hash,
            "operations": ["crop of the accepted master", "Lanczos3 downscale where a derivative is narrower than the crop",
                           "WebP encode"],
            "operations_not_used": ["tone or colour change", "sharpening", "upscaling", "generative or AI step"],
            "derivatives": derivatives,
            "max_safe_rendered_px": {
                "device_px": crop.width,
                "basis": "native 30 m Landsat at the crop's own pixel width; nothing is upscaled at or below that many device px",
            },
            "rights_basis": "USGS Landsat data are in the public domain; permission is not required and there are no "
                            "restrictions on use or redistribution. Only the crop, tone rendering (in the parent) and encoding are OrbGSS work.",
            "attribution_requirement": "Landsat data courtesy of the U.S. Geological Survey.",
            "caption_i18n_keys": [*spec["caption"], "scene.kind.naturalColor"],
            "label_point": label_point(spec["box"], *spec["label"]),
            "rendered": None,
        })
    return files, records


def merged_manifest(records: list[dict], root: pathlib.Path) -> dict:
    manifest = json.loads((root / "assets" / "imagery" / "sources.json").read_text(encoding="utf-8"))
    existing = {r["id"]: r for r in manifest.get("web_m6", {}).get("interior_crops", [])}
    for record in records:
        # Keep the measured placement (written by the validation tooling after a browser run).
        record["rendered"] = existing.get(record["id"], {}).get("rendered")
    web_m6 = manifest.setdefault("web_m6", {})
    web_m6["interior_crops"] = records
    return manifest


def main(argv: list[str]) -> int:
    check = "--check" in argv
    files, records = build()
    manifest = merged_manifest(records, ROOT)
    text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    drift = []
    for rel, data in files.items():
        path = ROOT / rel
        if not path.is_file() or path.read_bytes() != data:
            drift.append(rel)
    if MANIFEST.read_text(encoding="utf-8") != text:
        drift.append("assets/imagery/sources.json")
    if check:
        for rel in drift:
            print(f"differs from a fresh build: {rel}")
        print("build_interior_crops --check: " + ("OK" if not drift else "DRIFT"))
        return 1 if drift else 0
    for rel, data in files.items():
        (ROOT / rel).write_bytes(data)
    MANIFEST.write_text(text, encoding="utf-8")
    for rel in sorted(files):
        print(f"{rel}  {len(files[rel]) / 1024:.0f} KiB")
    print("sources.json -> web_m6.interior_crops updated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
