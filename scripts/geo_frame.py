"""WGS84 <-> UTM zone 35N and the Act 2 master's pixel grid (MER-255; local tooling, pure Python).

The Act 2 master (assets/imagery/kizildere-aoi-context-2025-natural.jpg) is a 3200 x 1800 px, 30 m grid
in EPSG:32635 whose upper-left corner is recorded at web_005b.context.frame.bounds_utm. The interior
crops are boxes in that grid, so the coordinates printed on a crop's image can be checked against the
ground the crop really shows. Kruger series (Karney 2011), good to well under a millimetre inside a
UTM zone; no third-party library.

    python3 scripts/geo_frame.py            # self-check against the recorded frame bounds and AOI centre
"""
from __future__ import annotations

import math

A = 6378137.0
F = 1 / 298.257223563
K0 = 0.9996
FALSE_EASTING = 500000.0
LON0 = 27.0  # central meridian of UTM zone 35N

# web_005b.context.frame: bounds_utm [west, south, east, north], 30 m, 3200 x 1800 px.
FRAME_WEST, FRAME_NORTH = 623040.0, 4232040.0
FRAME_RES = 30.0

_n = F / (2 - F)
_A = A / (1 + _n) * (1 + _n ** 2 / 4 + _n ** 4 / 64 + _n ** 6 / 256)
_ALPHA = (
    _n / 2 - 2 * _n ** 2 / 3 + 5 * _n ** 3 / 16 + 41 * _n ** 4 / 180 - 127 * _n ** 5 / 288,
    13 * _n ** 2 / 48 - 3 * _n ** 3 / 5 + 557 * _n ** 4 / 1440 + 281 * _n ** 5 / 630,
    61 * _n ** 3 / 240 - 103 * _n ** 4 / 140 + 15061 * _n ** 5 / 26880,
    49561 * _n ** 4 / 161280 - 179 * _n ** 5 / 168,
    34729 * _n ** 5 / 80640,
)
_BETA = (
    _n / 2 - 2 * _n ** 2 / 3 + 37 * _n ** 3 / 96 - _n ** 4 / 360 - 81 * _n ** 5 / 512,
    _n ** 2 / 48 + _n ** 3 / 15 - 437 * _n ** 4 / 1440 + 46 * _n ** 5 / 105,
    17 * _n ** 3 / 480 - 37 * _n ** 4 / 840 - 209 * _n ** 5 / 4480,
    4397 * _n ** 4 / 161280 - 11 * _n ** 5 / 504,
    4583 * _n ** 5 / 161280,
)
_E = math.sqrt(F * (2 - F))


def wgs84_to_utm35(lat: float, lon: float) -> tuple[float, float]:
    phi, lam = math.radians(lat), math.radians(lon - LON0)
    t = math.sinh(math.atanh(math.sin(phi)) - _E * math.atanh(_E * math.sin(phi)))
    xi_p = math.atan2(t, math.cos(lam))
    eta_p = math.asinh(math.sin(lam) / math.hypot(t, math.cos(lam)))
    xi = xi_p + sum(a * math.sin(2 * (j + 1) * xi_p) * math.cosh(2 * (j + 1) * eta_p) for j, a in enumerate(_ALPHA))
    eta = eta_p + sum(a * math.cos(2 * (j + 1) * xi_p) * math.sinh(2 * (j + 1) * eta_p) for j, a in enumerate(_ALPHA))
    return FALSE_EASTING + K0 * _A * eta, K0 * _A * xi


def utm35_to_wgs84(easting: float, northing: float) -> tuple[float, float]:
    xi = northing / (K0 * _A)
    eta = (easting - FALSE_EASTING) / (K0 * _A)
    xi_p = xi - sum(b * math.sin(2 * (j + 1) * xi) * math.cosh(2 * (j + 1) * eta) for j, b in enumerate(_BETA))
    eta_p = eta - sum(b * math.cos(2 * (j + 1) * xi) * math.sinh(2 * (j + 1) * eta) for j, b in enumerate(_BETA))
    chi = math.asin(math.sin(xi_p) / math.cosh(eta_p))
    phi = chi
    for _ in range(6):  # conformal -> geodetic latitude
        phi = math.asin(math.tanh(math.atanh(math.sin(chi)) + _E * math.atanh(_E * math.sin(phi))))
    lam = math.atan2(math.sinh(eta_p), math.cos(xi_p))
    return math.degrees(phi), LON0 + math.degrees(lam)


def frame_px_to_utm(x: float, y: float) -> tuple[float, float]:
    """Master pixel (x right, y down; 0, 0 is the frame's upper-left corner) -> UTM 35N metres."""
    return FRAME_WEST + x * FRAME_RES, FRAME_NORTH - y * FRAME_RES


def frame_px_to_wgs84(x: float, y: float) -> tuple[float, float]:
    return utm35_to_wgs84(*frame_px_to_utm(x, y))


def wgs84_to_frame_px(lat: float, lon: float) -> tuple[float, float]:
    easting, northing = wgs84_to_utm35(lat, lon)
    return (easting - FRAME_WEST) / FRAME_RES, (FRAME_NORTH - northing) / FRAME_RES


def _self_check() -> int:
    lat, lon = 37.9794, 28.7907
    easting, northing = wgs84_to_utm35(lat, lon)
    back = utm35_to_wgs84(easting, northing)
    assert abs(back[0] - lat) < 1e-9 and abs(back[1] - lon) < 1e-9, back
    # Zone 35N, central meridian: easting 500000 and northing = k0 * meridian arc.
    assert abs(wgs84_to_utm35(0.0, 27.0)[0] - 500000.0) < 1e-6
    # Recorded frame: bounds_wgs84 [28.3965, 37.7414, 29.5018, 38.2097] is the geographic position of the
    # south-west and north-east corners (west/south from the first, east/north from the second).
    sw = frame_px_to_wgs84(0, 1800)
    ne = frame_px_to_wgs84(3200, 0)
    assert (round(sw[1], 4), round(sw[0], 4), round(ne[1], 4), round(ne[0], 4)) == (28.3965, 37.7414, 29.5018, 38.2097), (sw, ne)
    # The declared AOI centre sits at master pixel (1141, 900), the centre of the 36 km analysis grid.
    px = wgs84_to_frame_px(lat, lon)
    assert abs(px[0] - 1141) < 1.5 and abs(px[1] - 900) < 1.5, px
    print("geo_frame self-check: OK (AOI centre at master px %.2f, %.2f)" % px)
    return 0


if __name__ == "__main__":
    raise SystemExit(_self_check())
