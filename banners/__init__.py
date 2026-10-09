"""
banners: Tech Stacks Icon Repository & LinkedIn Banner Generator.
"""

__version__ = "0.1.0"

from banners.cli import main
from banners.color_adapter import ColorAdapter
from banners.generator import build_banner_svg, generate_banner
from banners.presets import PRESETS
from banners.themes import THEMES

__all__ = [
    "PRESETS",
    "THEMES",
    "ColorAdapter",
    "__version__",
    "build_banner_svg",
    "generate_banner",
    "main",
]
