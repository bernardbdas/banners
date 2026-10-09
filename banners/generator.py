"""
Banner Generator Module.
Assembles SVG elements into full LinkedIn banner templates, validates XML markup,
and delegates rasterization to the rasterizer.
"""

import os
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

from banners.constants import (
    BANNER_HEIGHT,
    BANNER_SCALE,
    BANNER_WIDTH,
    CARD_HEIGHT,
    CARD_RADIUS,
    CARD_SPACING,
    CARD_WIDTH,
    ICON_Y,
    START_X,
)
from banners.presets import PRESETS
from banners.rasterizer import rasterize_svg
from banners.svg_processor import process_icon
from banners.themes import THEMES


def build_banner_svg(preset_name: str, theme_name: str) -> str:
    """Constructs the complete XML markup for a LinkedIn banner."""
    preset = PRESETS.get(preset_name)
    if not preset:
        raise ValueError(f"Unknown preset: '{preset_name}'. Available: {', '.join(PRESETS.keys())}")

    theme = THEMES.get(theme_name, THEMES["dark"])

    icons_data = []
    for idx, (label, file_path) in enumerate(preset["icons"]):
        processed = process_icon(label, file_path, idx, theme_name)
        if processed:
            icons_data.append(processed)
        else:
            print(f"⚠ Warning: Icon '{label}' not found at '{file_path}'", file=sys.stderr)

    safe_title = escape(preset["title"])
    safe_subtitle = escape(preset["subtitle"])

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{BANNER_WIDTH}" height="{BANNER_HEIGHT}" viewBox="0 0 {BANNER_WIDTH} {BANNER_HEIGHT}">',
        "  <defs>",
        f'    <linearGradient id="bgGrad_{theme_name}" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="{theme["bg_stops"][0][0]}" stop-color="{theme["bg_stops"][0][1]}" />',
        f'      <stop offset="{theme["bg_stops"][1][0]}" stop-color="{theme["bg_stops"][1][1]}" />',
        f'      <stop offset="{theme["bg_stops"][2][0]}" stop-color="{theme["bg_stops"][2][1]}" />',
        "    </linearGradient>",
        f'    <linearGradient id="cardGrad_{theme_name}" x1="0%" y1="0%" x2="0%" y2="100%">',
        f'      <stop offset="{theme["card_stops"][0][0]}" stop-color="{theme["card_stops"][0][1]}" stop-opacity="{theme["card_stops"][0][2]}" />',
        f'      <stop offset="{theme["card_stops"][1][0]}" stop-color="{theme["card_stops"][1][1]}" stop-opacity="{theme["card_stops"][1][2]}" />',
        "    </linearGradient>",
        f'    <linearGradient id="accentGlow_{theme_name}" x1="0%" y1="0%" x2="100%" y2="0%">',
        f'      <stop offset="{theme["accent_stops"][0][0]}" stop-color="{theme["accent_stops"][0][1]}" />',
        f'      <stop offset="{theme["accent_stops"][1][0]}" stop-color="{theme["accent_stops"][1][1]}" />',
        "    </linearGradient>",
        f'    <filter id="cardShadow_{theme_name}" x="-20%" y="-20%" width="140%" height="140%">',
        f'      <feDropShadow dx="0" dy="3" stdDeviation="{theme["card_shadow_blur"]}" flood-color="{theme["card_shadow_flood"]}" flood-opacity="{theme["card_shadow_opacity"]}" />',
        "    </filter>",
        "  </defs>",
        "  <!-- Background -->",
        f'  <rect width="{BANNER_WIDTH}" height="{BANNER_HEIGHT}" fill="url(#bgGrad_{theme_name})" />',
        "  <!-- Top Accent Bar -->",
        f'  <rect x="0" y="0" width="{BANNER_WIDTH}" height="3.5" fill="url(#accentGlow_{theme_name})" />',
        "  <!-- Ambient Atmospheric Shapes -->",
        f'  <circle cx="1450" cy="80" r="130" fill="{theme["ambient_1"]}" opacity="{theme["ambient_1_op"]}" />',
        f'  <circle cx="950" cy="300" r="190" fill="{theme["ambient_2"]}" opacity="{theme["ambient_2_op"]}" />',
        "",
        "  <!-- Typography: Header & Subtitle -->",
        f'  <text x="{START_X}" y="125" font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="34" font-weight="700" fill="{theme["title_color"]}" letter-spacing="-0.5">{safe_title}</text>',
        f'  <text x="{START_X}" y="165" font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="16" font-weight="400" fill="{theme["subtitle_color"]}">{safe_subtitle}</text>',
        "",
        "  <!-- Tech Stack Container Bar -->",
    ]

    for idx, (label, viewbox, namespaced_inner, disp_w, disp_h) in enumerate(icons_data):
        cx = START_X + idx * (CARD_WIDTH + CARD_SPACING)
        cy = ICON_Y
        safe_label = escape(label)

        icon_offset_x = (CARD_WIDTH - disp_w) / 2
        icon_offset_y = (CARD_HEIGHT - 18 - disp_h) / 2 + 3

        svg_parts.append(f"  <!-- {safe_label} Badge -->")
        svg_parts.append(f'  <g transform="translate({cx}, {cy})">')
        svg_parts.append(
            f'    <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" rx="{CARD_RADIUS}" fill="url(#cardGrad_{theme_name})" stroke="{theme["card_stroke"]}" stroke-width="1" filter="url(#cardShadow_{theme_name})" />'
        )
        svg_parts.append(
            f'    <svg x="{icon_offset_x:.1f}" y="{icon_offset_y:.1f}" width="{disp_w:.1f}" height="{disp_h:.1f}" viewBox="{viewbox}">'
        )
        svg_parts.append(f"      {namespaced_inner}")
        svg_parts.append("    </svg>")
        svg_parts.append(
            f'    <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 7}" font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="9.5" font-weight="500" fill="{theme["badge_text_color"]}" text-anchor="middle">{safe_label}</text>'
        )
        svg_parts.append("  </g>")

    svg_parts.append("</svg>")
    full_svg = "\n".join(svg_parts)

    # Validate XML before returning
    try:
        ET.fromstring(full_svg)
    except Exception as e:
        print(f"✗ XML Validation Error in {preset_name} ({theme_name}): {e}", file=sys.stderr)
        raise

    return full_svg


def generate_banner(
    preset_name: str,
    theme_name: str,
    output_svg_path: str,
    output_png_path: str | None = None,
    gen_svg: bool = True,
    gen_png: bool = True,
    scale: int = BANNER_SCALE,
) -> None:
    """Generates banner files in SVG and/or PNG formats."""
    full_svg = build_banner_svg(preset_name, theme_name)

    # Ensure parent directory exists if specified
    svg_dir = os.path.dirname(output_svg_path)
    if svg_dir:
        os.makedirs(svg_dir, exist_ok=True)

    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write(full_svg)

    if gen_svg:
        print(f"Generated [{theme_name.upper()} SVG]: {output_svg_path}")

    if gen_png and output_png_path:
        rasterize_svg(output_svg_path, output_png_path, scale=scale)

    # Remove SVG if only PNG was requested
    if not gen_svg and os.path.exists(output_svg_path):
        os.remove(output_svg_path)
