"""
Background Management Module.
Loads and processes custom SVG backgrounds (patterns, pastel gradients, solid pastels)
from assets/backgrounds/.
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from banners.constants import BACKGROUNDS_DIR, REPO_ROOT


def list_available_backgrounds() -> list[str]:
    """Returns a sorted list of all available background names across all background subdirectories."""
    if not BACKGROUNDS_DIR.exists():
        return []
    return sorted(p.stem for p in BACKGROUNDS_DIR.rglob("*.svg") if p.is_file())


def resolve_background_path(name_or_path: str) -> Path | None:
    """
    Resolves a background identifier to a file Path.
    Supports names like 'topographical', 'patterns/topographical', 'solid_lavender', etc.
    """
    if not name_or_path or name_or_path.lower() in ("none", "default", "standard"):
        return None

    clean_name = name_or_path.strip().lower().replace("-", "_")

    # 1. Direct match with or without .svg in BACKGROUNDS_DIR
    for cand in [
        BACKGROUNDS_DIR / f"{clean_name}.svg",
        BACKGROUNDS_DIR / clean_name,
    ]:
        if cand.is_file():
            return cand

    # 2. Check standard subdirectories (patterns, gradients, solids)
    subdirs = ["patterns", "gradients", "solids"]
    for sub in subdirs:
        for cand in [
            BACKGROUNDS_DIR / sub / f"{clean_name}.svg",
            BACKGROUNDS_DIR / sub / clean_name,
        ]:
            if cand.is_file():
                return cand

    # 3. Recursive lookup by stem name
    for p in BACKGROUNDS_DIR.rglob("*.svg"):
        if p.stem.lower() == clean_name:
            return p

    # 4. Check relative to repository root
    cand_root = REPO_ROOT / name_or_path
    if cand_root.is_file():
        return cand_root

    # 5. Check absolute path
    cand_abs = Path(name_or_path)
    if cand_abs.is_file():
        return cand_abs

    print(
        f"⚠ Warning: Background '{name_or_path}' not found. Available: {', '.join(list_available_backgrounds())}",
        file=sys.stderr,
    )
    return None


def load_background_svg(name_or_path: str, fade: float = 1.0) -> tuple[str, str, bool] | None:
    """
    Loads background SVG, separating <defs> from visual body elements.
    Wraps pattern and ambient overlay elements in an opacity-controlled group
    according to the specified fade percentage (0.0 to 1.0).
    Returns: (defs_xml, body_xml, is_pastel) or None if background is disabled/invalid.
    """
    path = resolve_background_path(name_or_path)
    if not path:
        return None

    try:
        with open(path, encoding="utf-8") as f:
            data = f.read()

        # Strip XML declaration and DOCTYPE if present
        data = re.sub(r"<\?xml[^>]*\?>", "", data)
        data = re.sub(r"<!DOCTYPE[^>]*>", "", data)

        # Strip xmlns temporarily so ElementTree doesn't inject ns0: prefixes
        cleaned_data = re.sub(r'\s+xmlns="[^"]*"', "", data)
        cleaned_data = re.sub(r'\s+xmlns:xlink="[^"]*"', "", cleaned_data)
        cleaned_data = re.sub(r"\s+xmlns:xlink='[^']*'", "", cleaned_data)

        root = ET.fromstring(cleaned_data)

        defs_parts: list[str] = []
        base_parts: list[str] = []
        pattern_parts: list[str] = []

        is_first_visual = True
        for child in root:
            if child.tag == "defs":
                for def_elem in child:
                    defs_parts.append(ET.tostring(def_elem, encoding="unicode").strip())
            else:
                if is_first_visual and child.tag == "rect":
                    base_parts.append(ET.tostring(child, encoding="unicode").strip())
                    is_first_visual = False
                else:
                    pattern_parts.append(ET.tostring(child, encoding="unicode").strip())

        defs_xml = "\n".join(defs_parts)

        body_lines: list[str] = []
        if base_parts:
            body_lines.extend(base_parts)
        if pattern_parts:
            pattern_content = "\n  ".join(pattern_parts)
            body_lines.append(
                f'  <g id="pattern_layer" opacity="{fade:.2f}">\n    {pattern_content}\n  </g>'
            )
        elif not base_parts:
            for child in root:
                if child.tag != "defs":
                    body_lines.append(ET.tostring(child, encoding="unicode").strip())

        body_xml = "\n".join(body_lines)

        # Detect pastel / light backgrounds to trigger high-contrast typography
        is_pastel = (
            "pastel" in path.stem.lower()
            or "solid" in path.stem.lower()
            or "solids" in str(path).lower()
            or "light" in path.stem.lower()
            or "white" in path.stem.lower()
        )

        return defs_xml, body_xml, is_pastel
    except Exception as e:
        print(f"⚠ Warning: Failed to parse background '{path}': {e}", file=sys.stderr)
        return None
