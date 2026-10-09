"""
Rasterizer Module.
Converts generated SVG vector banners to PNG raster format using rsvg-convert.
Supports dynamic upscale scaling (default 4x for Ultra-HD Retina fidelity).
"""

import os
import shutil
import subprocess
import sys

from banners.constants import BANNER_HEIGHT, BANNER_SCALE, BANNER_WIDTH


def find_rasterizer_binary() -> str | None:
    """Finds the path to rsvg-convert on the system."""
    rsvg_bin = shutil.which("rsvg-convert")
    if rsvg_bin:
        return rsvg_bin

    known_paths = [
        "/opt/homebrew/bin/rsvg-convert",
        "/usr/local/bin/rsvg-convert",
        "/usr/bin/rsvg-convert",
    ]
    for candidate in known_paths:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def rasterize_svg(
    svg_path: str,
    png_path: str,
    width: int = BANNER_WIDTH,
    height: int = BANNER_HEIGHT,
    scale: int = BANNER_SCALE,
) -> bool:
    """
    Rasterizes an SVG banner to high-resolution PNG format.
    Upscales the raster dimensions by scale factor (default: 4x -> 6336 x 1584 px).
    Returns True on success, False otherwise.
    """
    rsvg_bin = find_rasterizer_binary()
    if not rsvg_bin:
        print(
            f"⚠ Warning: rsvg-convert not found. Cannot rasterize {svg_path} to {png_path}\n"
            "  Install via Homebrew: 'brew install librsvg' or apt: 'sudo apt-get install librsvg2-bin'",
            file=sys.stderr,
        )
        return False

    png_dir = os.path.dirname(png_path)
    if png_dir:
        os.makedirs(png_dir, exist_ok=True)

    target_width = width * scale
    target_height = height * scale

    try:
        cmd = [
            rsvg_bin,
            "-w",
            str(target_width),
            "-h",
            str(target_height),
            svg_path,
            "-o",
            png_path,
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        parts = os.path.normpath(png_dir).split(os.sep) if png_dir else []
        theme_tag = (
            parts[-2].upper()
            if len(parts) >= 2 and parts[-1].lower() in ("png", "svg")
            else (parts[-1].upper() if parts else "ROOT")
        )
        print(f"Rasterized [{theme_tag} PNG ({target_width}x{target_height})]: {png_path}")
        return True
    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.decode("utf-8", errors="ignore")
        print(f"✗ Failed to rasterize {svg_path} to PNG: {err_msg}", file=sys.stderr)
        return False
