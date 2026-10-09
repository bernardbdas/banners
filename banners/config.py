"""
Configuration and Environment Variable Loader for LinkedIn Banner Generator.
Supports loading dynamic settings (website URL, contact email, banner preset, background)
from 'local.env', 'env.local', or environment variables with zero external dependencies.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from banners.constants import REPO_ROOT


@dataclass
class BannerConfig:
    """Holds banner customization settings loaded from local.env or environment."""

    website_url: str = ""
    email: str = ""
    banner_name: str = ""
    background: str = ""
    theme: str = ""
    fade: float = 1.0


def parse_fade_percentage(val: str | float | int | None) -> float:
    """
    Parses a fade/opacity percentage value into a float between 0.0 and 1.0.
    Supports formats:
      - '40%' -> 0.40
      - '40' -> 0.40 (values > 1.0 are treated as percentages out of 100)
      - '0.4' -> 0.40
      - '100%' / '1.0' / '1' -> 1.00
      - '0%' / '0' -> 0.00
    Defaults to 1.0 if None or empty string.
    """
    if val is None:
        return 1.0
    if isinstance(val, int | float):
        f_val = float(val)
        if f_val > 1.0:
            f_val = f_val / 100.0
        return max(0.0, min(1.0, f_val))

    s = str(val).strip()
    if not s:
        return 1.0

    if s.endswith("%"):
        s = s[:-1].strip()
        try:
            return max(0.0, min(1.0, float(s) / 100.0))
        except ValueError:
            return 1.0

    try:
        f_val = float(s)
        if f_val > 1.0:
            f_val = f_val / 100.0
        return max(0.0, min(1.0, f_val))
    except ValueError:
        return 1.0


def parse_env_file(filepath: Path | str) -> dict[str, str]:
    """
    Parses a simple .env file into a dictionary of key-value pairs.
    Handles quotes, inline comments, and empty lines.
    """
    path = Path(filepath)
    if not path.is_file():
        return {}

    env_vars: dict[str, str] = {}
    with open(path, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()

            # Strip matching quotes
            if (val.startswith('"') and val.endswith('"')) or (
                val.startswith("'") and val.endswith("'")
            ):
                val = val[1:-1]
            else:
                # Remove trailing inline comment if not quoted
                if " #" in val:
                    val = val.split(" #", 1)[0].strip()

            env_vars[key] = val

    return env_vars


def load_config(env_path: Path | str | None = None) -> BannerConfig:
    """
    Loads BannerConfig from local.env, env.local, .env, or system environment variables.
    Searches for 'local.env' and 'env.local' in the repository root by default.
    """
    env_data: dict[str, str] = {}

    if env_path is not None:
        target = Path(env_path)
        if target.is_file():
            env_data = parse_env_file(target)
    else:
        # Check local.env, env.local, .env.local, then .env fallback
        candidates = [
            REPO_ROOT / "local.env",
            REPO_ROOT / "env.local",
            REPO_ROOT / ".env.local",
            REPO_ROOT / ".env",
        ]
        for candidate in candidates:
            if candidate.is_file():
                env_data = parse_env_file(candidate)
                break

    # Prioritize system environment variables over file values
    website_url = os.environ.get("WEBSITE_URL") or env_data.get("WEBSITE_URL", "")
    email = os.environ.get("EMAIL") or env_data.get("EMAIL", "")
    banner_name = os.environ.get("BANNER_NAME") or env_data.get("BANNER_NAME", "")
    # Theme and background are unified concepts
    theme_val = (
        os.environ.get("THEME")
        or env_data.get("THEME")
        or os.environ.get("BACKGROUND")
        or os.environ.get("BACKGROUND_NAME")
        or os.environ.get("BACKGROUND_STYLE")
        or env_data.get("BACKGROUND")
        or env_data.get("BACKGROUND_NAME")
        or env_data.get("BACKGROUND_STYLE")
        or ""
    ).strip()

    # Fade percentage for background pattern
    fade_raw = (
        os.environ.get("FADE")
        or env_data.get("FADE")
        or os.environ.get("BACKGROUND_FADE")
        or env_data.get("BACKGROUND_FADE")
        or os.environ.get("PATTERN_FADE")
        or env_data.get("PATTERN_FADE")
        or os.environ.get("PATTERN_OPACITY")
        or env_data.get("PATTERN_OPACITY")
        or None
    )
    fade_val = parse_fade_percentage(fade_raw)

    return BannerConfig(
        website_url=website_url.strip(),
        email=email.strip(),
        banner_name=banner_name.strip(),
        background=theme_val,
        theme=theme_val,
        fade=fade_val,
    )
