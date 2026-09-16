"""Tile rendered frames into one reviewable contact sheet, inside Blender.

    blender -b -P hero/scripts/contact_sheet.py -- --out sheet.png --columns 4 a.png b.png ...

The lane policy is not to commit frame sequences or video as progress evidence,
but a sequence of stills is the only way to show that a move holds together --
that the AOI never jumps, re-centres or changes size between frames. A single
tiled sheet keeps that reviewable in the repository at a bounded size.

Uses Blender's own image loader and scaler, so it adds no Python dependency and
no external encoder to the lane.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy  # noqa: E402

import hero_common as hc  # noqa: E402


def build_sheet(paths, out_path: Path, columns: int, tile_width: int, gap: int, background):
    tiles = []
    tile_height = None
    for path in paths:
        image = bpy.data.images.load(str(path))
        aspect = image.size[1] / image.size[0]
        height = int(round(tile_width * aspect))
        image.scale(tile_width, height)
        tiles.append(list(image.pixels))
        tile_height = height
        bpy.data.images.remove(image)

    rows = (len(tiles) + columns - 1) // columns
    sheet_w = columns * tile_width + (columns + 1) * gap
    sheet_h = rows * tile_height + (rows + 1) * gap

    # Blender image pixel buffers are bottom-up, RGBA, scene-linear floats.
    buffer = []
    for _ in range(sheet_w * sheet_h):
        buffer.extend(background)

    for index, tile in enumerate(tiles):
        column = index % columns
        row = index // columns
        x0 = gap + column * (tile_width + gap)
        # Fill top-to-bottom visually, which is bottom-to-top in buffer space.
        y0 = sheet_h - gap - (row + 1) * tile_height - row * gap

        for ty in range(tile_height):
            src = ty * tile_width * 4
            dst = ((y0 + ty) * sheet_w + x0) * 4
            buffer[dst:dst + tile_width * 4] = tile[src:src + tile_width * 4]

    sheet = bpy.data.images.new("contact_sheet", width=sheet_w, height=sheet_h, alpha=False)
    sheet.pixels = buffer
    sheet.file_format = "PNG"
    hc.ensure_dir(out_path.parent)
    scene = bpy.context.scene
    # The tiles are finished, display-referred renders. Saving them through the scene's default
    # view transform would tone-map them a second time and darken every tile, so the sheet is
    # written through Standard/None -- the same rule the production encoder applies.
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_depth = "8"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.compression = 30
    sheet.save_render(filepath=str(out_path), scene=scene)
    bpy.data.images.remove(sheet)
    return {"tiles": len(tiles), "columns": columns, "resolution": [sheet_w, sheet_h]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Tile frames into a contact sheet.")
    parser.add_argument("frames", nargs="+", help="input image paths, in order")
    parser.add_argument("--out", required=True)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--tile-width", type=int, default=440)
    parser.add_argument("--gap", type=int, default=8)
    args = parser.parse_args(hc.argv_after_double_dash())

    out = Path(args.out)
    # Deep navy gutters, matching the scene's own space value rather than a
    # bright border that would misrepresent the exposure of every tile.
    record = build_sheet(
        [Path(p) for p in args.frames], out, args.columns, args.tile_width, args.gap,
        (0.0035, 0.007, 0.014, 1.0),
    )
    record["output_path"] = hc.relpath(out)
    record["sha256"] = hc.sha256_file(out) if out.exists() else None
    record["bytes"] = out.stat().st_size if out.exists() else 0
    print("[hero] contact sheet -> " + hc.relpath(out) + " " + repr(record))


if __name__ == "__main__":
    main()
