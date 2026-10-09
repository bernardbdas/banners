"""
Command-Line Interface for the LinkedIn Banner Generator.
Usage:
  banners [preset] [theme] [format] [scale]
  uv run banners --help
"""

import os
import sys

from banners.config import load_config, parse_fade_percentage
from banners.constants import BANNER_SCALE
from banners.generator import generate_banner
from banners.presets import PRESETS
from banners.themes import get_available_themes


def print_help() -> None:
    """Displays available presets, CLI usage, themes, and env config status."""
    cfg = load_config()
    themes = get_available_themes()
    print("LinkedIn Banner Generator (1584 x 396 px vector, upscaled to 6336 x 1584 px Ultra-HD)")
    print("\nUsage:")
    print("  banners [preset] [theme] [format] [scale] [--fade <value>]")
    print("  python3 -m banners [preset] [theme] [format] [scale] [--fade <value>]")
    print("\nEnvironment Customization (via local.env or env.local):")
    print(f"  BANNER_NAME: {cfg.banner_name or 'all'} (default preset)")
    print(f"  THEME:       {cfg.theme or cfg.background or 'dark'}")
    print(f"  FADE:        {int(cfg.fade * 100)}% (pattern fade / opacity)")
    print(f"  TITLE:       {cfg.title or '(default from preset)'}")
    print(f"  SUBTITLE:    {cfg.subtitle or '(default from preset)'}")
    print(f"  ICONS:       {cfg.icons or '(default from preset)'}")
    print(f"  WEBSITE_URL: {cfg.website_url or '(not configured)'}")
    print(f"  EMAIL:       {cfg.email or '(not configured)'}")
    print("\nArguments & Flags:")
    print(
        f"  preset: Specific role preset name, 'custom', or 'all' (default: '{cfg.banner_name or 'all'}')"
    )
    print(
        f"  theme:  Theme name (e.g. 'topographical', 'linkedin', 'dark', etc.), or 'all' (default: '{cfg.theme or cfg.background or 'dark'}')"
    )
    print("  format: 'png', 'svg', or 'all' (default: 'all')")
    print("  scale:  Integer upscale multiplier (default: 4 -> 6336x1584 px)")
    print("  --fade: Pattern fade/opacity percentage (e.g. '50%', '40', '0.5', default: 100%)")
    print(
        "  --title <text>:    Custom role title (3-45 chars, e.g. 'Staff Infrastructure Engineer')"
    )
    print("  --subtitle <text>: Custom tagline/subtitle (3-70 chars)")
    print(
        "  --icons <list>:    Comma-separated tech icons (3-8 icons, e.g. 'go, k8s, docker, aws, python')"
    )
    print("\nDesign Standards & Guardrails:")
    print("  - Icon Count: 3 to 8 icons maximum (guarantees safe-zone alignment without clipping)")
    print("  - Title Length: 3 to 45 characters maximum")
    print("  - Subtitle Length: 3 to 70 characters maximum")
    print("\nAvailable presets:")
    for key, val in PRESETS.items():
        print(f"  - {key:<16}: {val['title']}")
    print("\nAvailable themes (exported to exported/<theme>/svg/ and /png/):")
    for t_name in themes:
        print(f"  - {t_name}")
    print("\nExamples:")
    print(
        "  banners backend topographical png               # Generate high-res topographical PNG for Backend"
    )
    print(
        "  banners custom topographical png --title 'Lead Cloud Architect' --icons 'go,k8s,docker,aws,python'"
    )
    print("  banners backend --title 'Distributed Systems Lead' # Override title on backend preset")


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point. Returns exit status code."""
    if argv is None:
        argv = sys.argv[1:]

    config = load_config()
    available_themes = get_available_themes()

    background_override = None
    fade_override = None
    title_override = None
    subtitle_override = None
    icons_override = None
    clean_argv = []
    i = 0
    while i < len(argv):
        if argv[i] in ("--bg", "--background") and i + 1 < len(argv):
            background_override = argv[i + 1]
            i += 2
        elif argv[i].startswith("--bg="):
            background_override = argv[i].split("=", 1)[1]
            i += 1
        elif argv[i].startswith("--background="):
            background_override = argv[i].split("=", 1)[1]
            i += 1
        elif argv[i] in ("--fade", "-f") and i + 1 < len(argv):
            fade_override = argv[i + 1]
            i += 2
        elif argv[i].startswith("--fade="):
            fade_override = argv[i].split("=", 1)[1]
            i += 1
        elif argv[i].startswith("-f="):
            fade_override = argv[i].split("=", 1)[1]
            i += 1
        elif argv[i] in ("--title", "--role") and i + 1 < len(argv):
            title_override = argv[i + 1]
            i += 2
        elif argv[i].startswith(("--title=", "--role=")):
            title_override = argv[i].split("=", 1)[1]
            i += 1
        elif argv[i] in ("--subtitle", "--tagline") and i + 1 < len(argv):
            subtitle_override = argv[i + 1]
            i += 2
        elif argv[i].startswith(("--subtitle=", "--tagline=")):
            subtitle_override = argv[i].split("=", 1)[1]
            i += 1
        elif argv[i] in ("--icons", "--skills", "--stack") and i + 1 < len(argv):
            icons_override = argv[i + 1]
            i += 2
        elif argv[i].startswith(("--icons=", "--skills=", "--stack=")):
            icons_override = argv[i].split("=", 1)[1]
            i += 1
        else:
            clean_argv.append(argv[i])
            i += 1
    argv = clean_argv

    custom_title = title_override or config.title or None
    custom_subtitle = subtitle_override or config.subtitle or None
    custom_icons = icons_override or config.icons or None
    has_customization = bool(custom_title or custom_subtitle or custom_icons)

    default_preset = (
        config.banner_name if config.banner_name else ("custom" if has_customization else "all")
    )
    preset_raw = argv[0] if len(argv) > 0 else default_preset

    if preset_raw.lower() in ("--list", "-l", "list", "--help", "-h", "help"):
        print_help()
        return 0

    default_theme = config.theme or config.background or "dark"
    theme_raw = argv[1] if len(argv) > 1 else (background_override or default_theme)
    format_arg = argv[2].lower() if len(argv) > 2 else "all"

    # Support both underscore and hyphen preset names (e.g., ai-ml -> ai_ml)
    preset_arg = preset_raw.lower().replace("-", "_")

    if preset_arg not in ("all", "--all", "custom") and preset_arg not in PRESETS:
        if has_customization:
            preset_arg = "custom"
        else:
            print(
                f"Error: Unknown preset '{preset_raw}'. Available:\n  {', '.join(PRESETS.keys())}, 'custom', or 'all'",
                file=sys.stderr,
            )
            return 1

    selected_presets = list(PRESETS.keys()) if preset_arg in ("all", "--all") else [preset_arg]

    theme_clean = theme_raw.lower().replace("-", "_")
    if theme_clean in ("all", "--all"):
        selected_themes = available_themes
    elif theme_clean in available_themes:
        selected_themes = [theme_clean]
    else:
        print(
            f"Error: Unknown theme '{theme_raw}'. Available: 'all', or:\n  {', '.join(available_themes)}",
            file=sys.stderr,
        )
        return 1

    if format_arg not in ("all", "--all", "svg", "png"):
        print(
            f"Error: Unknown format '{format_arg}'. Available: 'svg', 'png', or 'all'",
            file=sys.stderr,
        )
        return 1

    scale_val = BANNER_SCALE
    if len(argv) > 3:
        try:
            scale_val = int(argv[3])
            if scale_val <= 0:
                raise ValueError
        except ValueError:
            print(
                f"Error: Invalid scale factor '{argv[3]}'. Must be a positive integer.",
                file=sys.stderr,
            )
            return 1

    fade_val = config.fade
    if fade_override is not None:
        fade_val = parse_fade_percentage(fade_override)
    elif len(argv) > 4:
        fade_val = parse_fade_percentage(argv[4])

    gen_svg = format_arg in ("all", "--all", "svg")
    gen_png = format_arg in ("all", "--all", "png")

    for theme in selected_themes:
        for preset in selected_presets:
            svg_path = os.path.join("exported", theme, "svg", f"banner_{preset}.svg")
            png_path = os.path.join("exported", theme, "png", f"banner_{preset}.png")
            try:
                generate_banner(
                    preset_name=preset,
                    theme_name=theme,
                    output_svg_path=svg_path,
                    output_png_path=png_path,
                    gen_svg=gen_svg,
                    gen_png=gen_png,
                    scale=scale_val,
                    website_url=config.website_url,
                    email=config.email,
                    background=theme if theme not in ("dark", "light") else background_override,
                    fade=fade_val,
                    title=custom_title,
                    subtitle=custom_subtitle,
                    icons=custom_icons,
                )
            except (ValueError, FileNotFoundError) as e:
                print(f"Error: {e}", file=sys.stderr)
                return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
