"""
Constants for the LinkedIn Banner Generator.
LinkedIn standard banner size: 1584 x 396 px (4:1 aspect ratio).
Default high-resolution upscale: 4x (6336 x 1584 px) for pixel-crisp Retina / 4K rendering.
"""

from pathlib import Path

# Repository root and standard directories
REPO_ROOT: Path = Path(__file__).resolve().parent.parent
ASSETS_DIR: Path = REPO_ROOT / "assets"
EXPORTED_DIR: Path = REPO_ROOT / "exported"

# Base vector canvas dimensions (LinkedIn standard 4:1 aspect ratio)
BANNER_WIDTH: int = 1584
BANNER_HEIGHT: int = 396

# High-resolution rasterization scale factor (4x -> 6336 x 1584 px)
BANNER_SCALE: int = 4
HIGH_RES_WIDTH: int = BANNER_WIDTH * BANNER_SCALE
HIGH_RES_HEIGHT: int = BANNER_HEIGHT * BANNER_SCALE

# Safe zone offset from left (profile avatar safe margin)
START_X: int = 560

# Badge card dimensions and layout
CARD_WIDTH: int = 72
CARD_HEIGHT: int = 72
CARD_RADIUS: int = 12
CARD_SPACING: int = 18

ICON_SIZE: int = 46
ICON_Y: int = 230
