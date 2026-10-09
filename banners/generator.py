"""
Banner Generator Module.
Assembles SVG elements into full LinkedIn banner templates, validates XML markup,
and delegates rasterization to the rasterizer.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

from banners.backgrounds import load_background_svg
from banners.config import load_config
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


def estimate_pill_width(text: str) -> int:
    """
    Calculates the exact pill badge width for a given contact string (URL or email),
    accounting for proportional glyph widths at font-size 13.5px, icon width (16px),
    icon left margin (14px), gap (6px), and right breathing margin (16px).
    """
    char_widths: dict[str, float] = {
        "i": 3.5,
        "l": 3.5,
        "j": 3.5,
        "I": 3.5,
        "f": 4.5,
        "t": 4.5,
        "r": 5.2,
        ".": 3.5,
        ":": 3.5,
        ";": 3.5,
        ",": 3.5,
        "!": 3.5,
        "|": 3.5,
        "/": 4.8,
        "-": 5.2,
        " ": 4.5,
        "s": 6.5,
        "c": 6.8,
        "z": 6.8,
        "v": 7.0,
        "x": 7.0,
        "y": 7.0,
        "a": 7.5,
        "b": 7.8,
        "d": 7.8,
        "e": 7.5,
        "g": 7.8,
        "h": 7.8,
        "k": 7.5,
        "n": 7.8,
        "o": 7.8,
        "p": 7.8,
        "q": 7.8,
        "u": 7.8,
        "0": 7.8,
        "1": 5.8,
        "2": 7.8,
        "3": 7.8,
        "4": 8.0,
        "5": 7.8,
        "6": 7.8,
        "7": 7.8,
        "8": 7.8,
        "9": 7.8,
        "m": 11.5,
        "w": 11.0,
        "@": 12.5,
        "_": 7.8,
    }
    raw_width = 0.0
    for ch in text:
        if ch in char_widths:
            raw_width += char_widths[ch]
        elif ch.isupper():
            raw_width += 12.5 if ch in ("M", "W") else 9.0
        elif ch.islower():
            raw_width += 7.5
        else:
            raw_width += 7.8

    # Apply 1.045 calibration factor for kerning and antialiasing, scaled for 14.5px font-size
    text_width = raw_width * 1.045 * (14.5 / 13.5)

    # Icon starts at x=14, width=16, gap=8 -> text starts at x=38.
    # Symmetrical right padding after text is 16px.
    pill_width = round(38 + text_width + 16)
    return max(96, pill_width)


def build_banner_svg(
    preset_name: str,
    theme_name: str,
    website_url: str | None = None,
    email: str | None = None,
    background: str | None = None,
    fade: float | None = None,
    title: str | None = None,
    subtitle: str | None = None,
    icons: list[tuple[str, str]] | list[str] | str | None = None,
) -> str:
    """Constructs the complete XML markup for a LinkedIn banner."""
    base_preset = PRESETS.get(preset_name)
    if (
        not base_preset
        and preset_name not in ("custom", "default", "custom_banner")
        and not (title or icons)
    ):
        raise ValueError(
            f"Unknown preset: '{preset_name}'. Available: {', '.join(PRESETS.keys())} or 'custom'"
        )

    from banners.custom import build_custom_preset, validate_banner_standards

    if (
        title
        or subtitle
        or icons
        or preset_name in ("custom", "default", "custom_banner")
        or not base_preset
    ):
        preset = build_custom_preset(
            title=title,
            subtitle=subtitle,
            icons_spec=icons,
            base_preset=base_preset,
        )
    else:
        preset = dict(base_preset)
        validate_banner_standards(preset["title"], preset["subtitle"], preset["icons"])

    theme = dict(THEMES.get(theme_name, THEMES["dark"]))

    # Load defaults from config if not explicitly provided
    if website_url is None or email is None or fade is None:
        cfg = load_config()
        if website_url is None:
            website_url = cfg.website_url
        if email is None:
            email = cfg.email
        if fade is None:
            fade = cfg.fade

    clean_theme = theme_name.strip().lower().replace("-", "_")

    # If background is not explicitly specified, treat theme_name as background unless it's dark/light
    if background is None:
        if clean_theme not in ("dark", "light"):
            background = clean_theme
        else:
            cfg = load_config()
            background = cfg.background or cfg.theme or None

    bg_data = load_background_svg(background, fade=fade) if background else None

    # Determine base styling: light/pastel vs dark
    if bg_data and bg_data[2]:  # is_pastel or light background
        base_theme = "light"
    elif clean_theme in ("light", "linkedin"):
        base_theme = "light"
    else:
        base_theme = "dark"

    if clean_theme in THEMES:
        theme = dict(THEMES[clean_theme])
    else:
        theme = dict(THEMES[base_theme])

    # Adapt styling for generic themes when rendered over pastel/light backgrounds
    if bg_data and bg_data[2] and (clean_theme in ("dark", "light") or clean_theme not in THEMES):
        theme["title_color"] = "#0F172A"
        theme["subtitle_color"] = "#334155"
        theme["card_stops"] = [("0%", "#FFFFFF", "0.90"), ("100%", "#F8FAFC", "0.80")]
        theme["card_stroke"] = "#E2E8F0"
        theme["badge_text_color"] = "#0F172A"
        theme["contact_text_color"] = "#0F172A"
        theme["contact_icon_color"] = "#0284C7"
        theme["card_shadow_flood"] = "#64748B"
        theme["card_shadow_opacity"] = "0.12"

    icons_data = []
    for idx, (label, file_path) in enumerate(preset["icons"]):
        processed = process_icon(label, file_path, idx, base_theme)
        if processed:
            icons_data.append(processed)
        else:
            print(f"⚠ Warning: Icon '{label}' not found at '{file_path}'", file=sys.stderr)

    safe_title = escape(preset["title"])
    safe_subtitle = escape(preset["subtitle"])

    custom_defs = bg_data[0] if bg_data else ""
    theme_id = re.sub(r"[^a-zA-Z0-9_]", "_", clean_theme)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{BANNER_WIDTH}" height="{BANNER_HEIGHT}" viewBox="0 0 {BANNER_WIDTH} {BANNER_HEIGHT}">',
        "  <defs>",
        f'    <linearGradient id="bgGrad_{theme_id}" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="{theme["bg_stops"][0][0]}" stop-color="{theme["bg_stops"][0][1]}" />',
        f'      <stop offset="{theme["bg_stops"][1][0]}" stop-color="{theme["bg_stops"][1][1]}" />',
        f'      <stop offset="{theme["bg_stops"][2][0]}" stop-color="{theme["bg_stops"][2][1]}" />',
        "    </linearGradient>",
        f'    <linearGradient id="cardGrad_{theme_id}" x1="0%" y1="0%" x2="0%" y2="100%">',
        f'      <stop offset="{theme["card_stops"][0][0]}" stop-color="{theme["card_stops"][0][1]}" stop-opacity="{theme["card_stops"][0][2]}" />',
        f'      <stop offset="{theme["card_stops"][1][0]}" stop-color="{theme["card_stops"][1][1]}" stop-opacity="{theme["card_stops"][1][2]}" />',
        "    </linearGradient>",
        f'    <linearGradient id="accentGlow_{theme_id}" x1="0%" y1="0%" x2="100%" y2="0%">',
        f'      <stop offset="{theme["accent_stops"][0][0]}" stop-color="{theme["accent_stops"][0][1]}" />',
        f'      <stop offset="{theme["accent_stops"][1][0]}" stop-color="{theme["accent_stops"][1][1]}" />',
        "    </linearGradient>",
        f'    <filter id="cardShadow_{theme_id}" x="-20%" y="-20%" width="140%" height="140%">',
        f'      <feDropShadow dx="0" dy="3" stdDeviation="{theme["card_shadow_blur"]}" flood-color="{theme["card_shadow_flood"]}" flood-opacity="{theme["card_shadow_opacity"]}" />',
        "    </filter>",
    ]

    if custom_defs:
        svg_parts.append(f"    {custom_defs}")

    svg_parts.append("  </defs>")

    if bg_data:
        body_xml = bg_data[1]
        svg_parts.extend(
            [
                "  <!-- Custom Background -->",
                f"  {body_xml}",
                "  <!-- Top Accent Bar -->",
                f'  <rect x="0" y="0" width="{BANNER_WIDTH}" height="3.5" fill="url(#accentGlow_{theme_id})" />',
            ]
        )
    else:
        svg_parts.extend(
            [
                "  <!-- Background -->",
                f'  <rect width="{BANNER_WIDTH}" height="{BANNER_HEIGHT}" fill="url(#bgGrad_{theme_id})" />',
                "  <!-- Top Accent Bar -->",
                f'  <rect x="0" y="0" width="{BANNER_WIDTH}" height="3.5" fill="url(#accentGlow_{theme_id})" />',
                f'  <g id="pattern_layer" opacity="{fade:.2f}">',
                "    <!-- Ambient Atmospheric Shapes -->",
                f'    <circle cx="1450" cy="80" r="130" fill="{theme["ambient_1"]}" opacity="{theme["ambient_1_op"]}" />',
                f'    <circle cx="950" cy="300" r="190" fill="{theme["ambient_2"]}" opacity="{theme["ambient_2_op"]}" />',
                "  </g>",
            ]
        )

    svg_parts.extend(
        [
            "",
            "  <!-- Typography: Header & Subtitle -->",
            f'  <text x="{START_X}" y="96" font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="48" font-weight="800" fill="{theme["title_color"]}" letter-spacing="1.5">{safe_title}</text>',
            f'  <text x="{START_X}" y="138" font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="22" font-weight="500" fill="{theme["subtitle_color"]}" letter-spacing="0.5">{safe_subtitle}</text>',
            "",
            "  <!-- Tech Stack Container Bar -->",
        ]
    )

    for idx, (label, viewbox, namespaced_inner, disp_w, disp_h) in enumerate(icons_data):
        cx = START_X + idx * (CARD_WIDTH + CARD_SPACING)
        cy = ICON_Y
        safe_label = escape(label)

        icon_offset_x = (CARD_WIDTH - disp_w) / 2
        icon_offset_y = (CARD_HEIGHT - 24 - disp_h) / 2 + 3

        svg_parts.append(f"  <!-- {safe_label} Badge -->")
        svg_parts.append(f'  <g transform="translate({cx}, {cy})">')
        svg_parts.append(
            f'    <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" rx="{CARD_RADIUS}" fill="url(#cardGrad_{theme_id})" stroke="{theme["card_stroke"]}" stroke-width="1" filter="url(#cardShadow_{theme_id})" />'
        )
        svg_parts.append(
            f'    <svg x="{icon_offset_x:.1f}" y="{icon_offset_y:.1f}" width="{disp_w:.1f}" height="{disp_h:.1f}" viewBox="{viewbox}">'
        )
        svg_parts.append(f"      {namespaced_inner}")
        svg_parts.append("    </svg>")
        svg_parts.append(
            f'    <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 9.5}" font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="12.5" font-weight="600" fill="{theme["badge_text_color"]}" text-anchor="middle">{safe_label}</text>'
        )
        svg_parts.append("  </g>")

    # Contact Details (Website & Email)
    if website_url or email:
        svg_parts.append("")
        svg_parts.append("  <!-- Contact Information -->")
        contact_x = START_X
        contact_text_col = theme.get("contact_text_color", theme.get("badge_text_color", "#FFFFFF"))
        contact_icon_col = theme.get("contact_icon_color", theme.get("ambient_1", "#38BDF8"))

        if website_url:
            safe_website = escape(website_url)
            pill_w = estimate_pill_width(website_url)
            svg_parts.extend(
                [
                    "  <!-- Website -->",
                    f'  <g transform="translate({contact_x}, 318)">',
                    f'    <rect width="{pill_w}" height="36" rx="18" fill="url(#cardGrad_{theme_id})" stroke="{theme["card_stroke"]}" stroke-width="1" filter="url(#cardShadow_{theme_id})" />',
                    '    <g transform="translate(14, 10)">',
                    f'      <circle cx="8" cy="8" r="7.5" fill="none" stroke="{contact_icon_col}" stroke-width="1.4" />',
                    f'      <ellipse cx="8" cy="8" rx="3.3" ry="7.5" fill="none" stroke="{contact_icon_col}" stroke-width="1.3" />',
                    f'      <line x1="0.5" y1="8" x2="15.5" y2="8" stroke="{contact_icon_col}" stroke-width="1.3" />',
                    "    </g>",
                    f'    <text x="38" y="22.5" font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="14.5" font-weight="600" fill="{contact_text_col}">{safe_website}</text>',
                    "  </g>",
                ]
            )
            contact_x += pill_w + 16

        if email:
            safe_email = escape(email)
            pill_w = estimate_pill_width(email)
            svg_parts.extend(
                [
                    "  <!-- Email -->",
                    f'  <g transform="translate({contact_x}, 318)">',
                    f'    <rect width="{pill_w}" height="36" rx="18" fill="url(#cardGrad_{theme_id})" stroke="{theme["card_stroke"]}" stroke-width="1" filter="url(#cardShadow_{theme_id})" />',
                    '    <g transform="translate(14, 10)">',
                    f'      <rect x="0.5" y="2" width="15" height="12" rx="2" fill="none" stroke="{contact_icon_col}" stroke-width="1.4" />',
                    f'      <path d="M1.5 3.5 L8 8.5 L14.5 3.5" fill="none" stroke="{contact_icon_col}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" />',
                    "    </g>",
                    f'    <text x="38" y="22.5" font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="14.5" font-weight="600" fill="{contact_text_col}">{safe_email}</text>',
                    "  </g>",
                ]
            )

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
    website_url: str | None = None,
    email: str | None = None,
    background: str | None = None,
    fade: float | None = None,
    title: str | None = None,
    subtitle: str | None = None,
    icons: list[tuple[str, str]] | list[str] | str | None = None,
) -> None:
    """Generates banner files in SVG and/or PNG formats."""
    full_svg = build_banner_svg(
        preset_name=preset_name,
        theme_name=theme_name,
        website_url=website_url,
        email=email,
        background=background,
        fade=fade,
        title=title,
        subtitle=subtitle,
        icons=icons,
    )

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
