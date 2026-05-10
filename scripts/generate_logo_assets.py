#!/usr/bin/env python3
"""Generate minimal valid PNG assets for Buildozer (stdlib only)."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path


def write_rgb_png(path: Path, width: int, height: int, rgb: tuple[int, int, int]) -> None:
    r, g, b = rgb
    raw_rows = []
    for _ in range(height):
        raw_rows.append(b"\x00" + bytes([r, g, b]) * width)
    raw = b"".join(raw_rows)
    compressed = zlib.compress(raw, level=9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", compressed)
        + chunk(b"IEND", b"")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    logo_dir = root / "data" / "logo"
    # Orange theme matches MDApp primary_palette Orange
    accent = (255, 152, 0)
    darker = (230, 126, 0)
    write_rgb_png(logo_dir / "logo_512_min.png", 512, 512, accent)
    write_rgb_png(logo_dir / "presplash_512_kivy_min.png", 512, 512, darker)
    write_rgb_png(logo_dir / "menu_icon_192_min.png", 192, 192, accent)


if __name__ == "__main__":
    main()
