"""Build the Kızıldere locator map (MER-240, visual need V1) from Natural Earth.

The map is a class-A cartographic illustration, not product proof: Türkiye and its neighbours
from the Natural Earth Admin 0 countries layer (public domain), with the 36 km pilot area of
interest drawn at its declared centre. It carries no text; the page caption names the place.

Usage (the GeoJSON is a download, so it is read as data and passed by path):

    py -3.14 -I scripts/build_locator_map.py --source <ne_50m_admin_0_countries.geojson>

The output is content-hash named (`/assets/` is immutable-cached), older builds are removed, and
the source and output SHA-256 are printed for `assets/imagery/sources.json` -> `web_m6`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "maps"
STEM = "kizildere-locator"

# Extent (degrees) and projection: equirectangular, true to scale at the AOI's latitude band.
LON_MIN, LON_MAX = 24.6, 45.6
LAT_MIN, LAT_MAX = 35.0, 42.8
STANDARD_PARALLEL = 39.0
WIDTH = 1200

# The pilot AOI: a 36 km square on the declared centre (assets/imagery/sources.json).
AOI_LAT, AOI_LON = 37.9794, 28.7907
AOI_HALF_KM = 18.0
KM_PER_DEG_LAT = 111.32

FOCUS_A3 = "TUR"
# Violet map colours (brand package Final_v4). The brand rule is that no brand colour is drawn on a map (the scientific
# ramps run through violet and yellow, so Violet or Amber there would read as data): the area of interest is a white dashed
# line (--ogs-map-callout, #FFFFFF) with a dark halo (--ogs-map-callout-halo, Night at 70 %); everything else is a neutral
# of the brand's dark theme (Obsidian: orbgss-tokens.css, bg-app, bg-surface, bg-raised, border-strong).
SEA = "#110C12"
LAND = "#1C161D"
FOCUS_FILL = "#241E25"
FOCUS_LINE = "#69646A"
AOI_LINE = "#FFFFFF"
AOI_HALO = "#160A19"
AOI_HALO_OPACITY = ".7"
AOI_FILL_OPACITY = ".14"
AOI_DASH = "6 3"

SIMPLIFY = 0.7    # drop a vertex closer than this (viewBox units) to the last kept one
MIN_AREA = 1.5    # drop rings smaller than this (square viewBox units)
CLIP_MARGIN = 24  # clip outside the viewBox so no clip edge is ever visible

COS = math.cos(math.radians(STANDARD_PARALLEL))
SCALE = WIDTH / ((LON_MAX - LON_MIN) * COS)
HEIGHT = round((LAT_MAX - LAT_MIN) * SCALE)


def project(lon: float, lat: float) -> tuple[float, float]:
    return (lon - LON_MIN) * COS * SCALE, (LAT_MAX - lat) * SCALE


def clip(ring: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Sutherland-Hodgman against the margin-expanded viewBox."""
    lo_x, lo_y, hi_x, hi_y = -CLIP_MARGIN, -CLIP_MARGIN, WIDTH + CLIP_MARGIN, HEIGHT + CLIP_MARGIN
    edges = (
        (lambda p: p[0] >= lo_x, lambda a, b: _cut_x(a, b, lo_x)),
        (lambda p: p[0] <= hi_x, lambda a, b: _cut_x(a, b, hi_x)),
        (lambda p: p[1] >= lo_y, lambda a, b: _cut_y(a, b, lo_y)),
        (lambda p: p[1] <= hi_y, lambda a, b: _cut_y(a, b, hi_y)),
    )
    out = ring
    for inside, cut in edges:
        if not out:
            break
        src, out = out, []
        prev = src[-1]
        for cur in src:
            if inside(cur):
                if not inside(prev):
                    out.append(cut(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(cut(prev, cur))
            prev = cur
    return out


def _cut_x(a, b, x):
    t = (x - a[0]) / (b[0] - a[0])
    return x, a[1] + t * (b[1] - a[1])


def _cut_y(a, b, y):
    t = (y - a[1]) / (b[1] - a[1])
    return a[0] + t * (b[0] - a[0]), y


def simplify(ring):
    kept = [ring[0]]
    for p in ring[1:]:
        if math.dist(p, kept[-1]) >= SIMPLIFY:
            kept.append(p)
    return kept


def area(ring) -> float:
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:] + ring[:1]))) / 2


def path_data(polygons) -> str:
    parts = []
    for rings in polygons:
        for ring in rings:
            pts = clip([project(lon, lat) for lon, lat in ring[:-1]])
            if len(pts) < 3:
                continue
            pts = simplify(pts)
            if len(pts) < 3 or area(pts) < MIN_AREA:
                continue
            head, *tail = pts
            parts.append(f"M{head[0]:.1f} {head[1]:.1f}" + "".join(f"L{x:.1f} {y:.1f}" for x, y in tail) + "Z")
    return "".join(parts)


def polygons_of(geometry):
    kind, coords = geometry["type"], geometry["coordinates"]
    if kind == "Polygon":
        return [coords]
    if kind == "MultiPolygon":
        return coords
    return []


def in_extent(polygons) -> bool:
    lons = [p[0] for rings in polygons for ring in rings for p in ring]
    lats = [p[1] for rings in polygons for ring in rings for p in ring]
    return bool(lons) and min(lons) < LON_MAX + 1 and max(lons) > LON_MIN - 1 \
        and min(lats) < LAT_MAX + 1 and max(lats) > LAT_MIN - 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source", required=True, type=pathlib.Path)
    args = ap.parse_args()

    raw = args.source.read_bytes()
    features = json.loads(raw.decode("utf-8"))["features"]

    focus, neighbours = [], []
    for feature in features:
        polygons = polygons_of(feature.get("geometry") or {"type": "", "coordinates": []})
        if not in_extent(polygons):
            continue
        props = feature.get("properties", {})
        is_focus = FOCUS_A3 in (props.get("ADM0_A3"), props.get("ISO_A3"))
        (focus if is_focus else neighbours).append(path_data(polygons))
    if len(focus) != 1:
        print(f"expected exactly one {FOCUS_A3} feature, found {len(focus)}", file=sys.stderr)
        return 1

    cx, cy = project(AOI_LON, AOI_LAT)
    half_y = AOI_HALF_KM / KM_PER_DEG_LAT * SCALE
    half_x = AOI_HALF_KM / (KM_PER_DEG_LAT * math.cos(math.radians(AOI_LAT))) * COS * SCALE

    # Neighbours are filled and stroked in the same colour, so no third-country border is drawn:
    # the map says where Türkiye is and where the pilot sits in it, nothing else.
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}">'
        "<!-- Natural Earth Admin 0 countries 1:50m v5.1.2 (public domain). OrbGSS locator map. -->"
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{SEA}"/>'
        f'<path d="{"".join(neighbours)}" fill="{LAND}" stroke="{LAND}" stroke-width="0.8" '
        'stroke-linejoin="round" fill-rule="evenodd"/>'
        f'<path d="{focus[0]}" fill="{FOCUS_FILL}" stroke="{FOCUS_LINE}" stroke-width="1.2" '
        'stroke-linejoin="round" fill-rule="evenodd"/>'
        f'<rect x="{cx - half_x:.1f}" y="{cy - half_y:.1f}" width="{2 * half_x:.1f}" '
        f'height="{2 * half_y:.1f}" fill="none" stroke="{AOI_HALO}" stroke-opacity="{AOI_HALO_OPACITY}" stroke-width="5"/>'
        f'<rect x="{cx - half_x:.1f}" y="{cy - half_y:.1f}" width="{2 * half_x:.1f}" '
        f'height="{2 * half_y:.1f}" fill="{AOI_LINE}" fill-opacity="{AOI_FILL_OPACITY}" stroke="{AOI_LINE}" stroke-width="2" stroke-dasharray="{AOI_DASH}"/>'
        "</svg>\n"
    ).encode("utf-8")

    digest = hashlib.sha256(svg).hexdigest()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob(f"{STEM}-*.svg"):
        old.unlink()
    out = OUT_DIR / f"{STEM}-{digest[:8]}.svg"
    out.write_bytes(svg)
    print(json.dumps({
        "path": out.relative_to(ROOT).as_posix(),
        "bytes": len(svg),
        "sha256": digest,
        "viewbox": [WIDTH, HEIGHT],
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "aoi_box_viewbox_units": [round(2 * half_x, 1), round(2 * half_y, 1)],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
