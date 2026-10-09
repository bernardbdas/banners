"""
Constants for the LinkedIn Banner Generator.
LinkedIn standard banner size: 1584 x 396 px (4:1 aspect ratio).
Default high-resolution upscale: 4x (6336 x 1584 px) for pixel-crisp Retina / 4K rendering.
"""

from pathlib import Path

# Repository root and standard directories
REPO_ROOT: Path = Path(__file__).resolve().parent.parent
ASSETS_DIR: Path = REPO_ROOT / "assets"
ICONS_DIR: Path = ASSETS_DIR / "icons"
BACKGROUNDS_DIR: Path = ASSETS_DIR / "backgrounds"
EXPORTED_DIR: Path = REPO_ROOT / "exported"

# Base vector canvas dimensions (LinkedIn standard 4:1 aspect ratio)
BANNER_WIDTH: int = 1584
BANNER_HEIGHT: int = 396

# High-resolution rasterization scale factor (4x -> 6336 x 1584 px)
BANNER_SCALE: int = 4
HIGH_RES_WIDTH: int = BANNER_WIDTH * BANNER_SCALE
HIGH_RES_HEIGHT: int = BANNER_HEIGHT * BANNER_SCALE

# Safe zone offset from left (profile avatar safe margin)
START_X: int = 520

# Badge card dimensions and layout (enlarged for crisp mobile readability)
CARD_WIDTH: int = 100
CARD_HEIGHT: int = 100
CARD_RADIUS: int = 16
CARD_SPACING: int = 16

ICON_SIZE: int = 60
ICON_Y: int = 170
