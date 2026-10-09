"""
Command-Line Interface for the LinkedIn Banner Generator.
Usage:
  banners [preset] [theme] [format] [scale]
  uv run banners --help
"""

import os
import sys

from banners.constants import BANNER_SCALE
from banners.generator import generate_banner
from banners.presets import PRESETS
from banners.themes import THEMES


def print_help() -> None:
    """Displays available presets and CLI usage."""
    print("LinkedIn Banner Generator (1584 x 396 px vector, upscaled to 6336 x 1584 px Ultra-HD)")
    print("\nUsage:")
    print("  banners [preset] [theme] [format] [scale]")
    print("  python3 -m banners [preset] [theme] [format] [scale]")
    print("\nArguments:")
    print("  preset: Specific role preset name, or 'all' (default: 'all')")
    print("  theme:  'dark', 'light', or 'all' (default: 'all')")
    print("  format: 'svg', 'png', or 'all' (default: 'all')")
    print("  scale:  Integer upscale multiplier (default: 4 -> 6336x1584 px)")
    print("\nAvailable presets:")
    for key, val in PRESETS.items():
        print(f"  - {key:<16}: {val['title']}")
    print("\nExamples:")
    print("  banners backend dark png        # Generate high-res dark PNG for Backend (6336x1584)")
    print("  banners ai-ml all svg           # Generate SVGs (both themes) for AI/ML")
    print("  banners all all all             # Generate all banners in all themes & formats at 4x")
    print("  banners backend dark png 2      # Generate 2x Retina PNG (3168x792)")


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point. Returns exit status code."""
    if argv is None:
        argv = sys.argv[1:]

    preset_raw = argv[0] if len(argv) > 0 else "all"
    theme_arg = argv[1].lower() if len(argv) > 1 else "all"
    format_arg = argv[2].lower() if len(argv) > 2 else "all"

    if preset_raw.lower() in ("--list", "-l", "list", "--help", "-h", "help"):
        print_help()
        return 0

    # Support both underscore and hyphen preset names (e.g., ai-ml -> ai_ml)
    preset_arg = preset_raw.lower().replace("-", "_")

    if preset_arg not in ("all", "--all") and preset_arg not in PRESETS:
        print(
            f"Error: Unknown preset '{preset_raw}'. Available:\n  {', '.join(PRESETS.keys())} or 'all'",
            file=sys.stderr,
        )
        return 1

    selected_presets = list(PRESETS.keys()) if preset_arg in ("all", "--all") else [preset_arg]

    if theme_arg not in ("all", "--all") and theme_arg not in THEMES:
        print(
            f"Error: Unknown theme '{theme_arg}'. Available: 'dark', 'light', or 'all'",
            file=sys.stderr,
        )
        return 1

    selected_themes = ["dark", "light"] if theme_arg in ("all", "--all") else [theme_arg]

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

    gen_svg = format_arg in ("all", "--all", "svg")
    gen_png = format_arg in ("all", "--all", "png")

    for theme in selected_themes:
        for preset in selected_presets:
            svg_path = os.path.join("exported", "svg", theme, f"banner_{preset}.svg")
            png_path = os.path.join("exported", "png", theme, f"banner_{preset}.png")
            generate_banner(
                preset_name=preset,
                theme_name=theme,
                output_svg_path=svg_path,
                output_png_path=png_path,
                gen_svg=gen_svg,
                gen_png=gen_png,
                scale=scale_val,
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
