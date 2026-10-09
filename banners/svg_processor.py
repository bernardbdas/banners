"""
SVG Processing Module.
Extracts SVG markup, namespaces local IDs, calculates balanced visual proportions,
and applies dynamic theme color adaptations.
"""

import os
import re

from banners.color_adapter import ColorAdapter
from banners.constants import REPO_ROOT


def extract_svg_content(path: str) -> tuple[str, str] | None:
    """Reads SVG file, extracts viewBox and inner XML markup."""
    target_path = path
    if not os.path.exists(target_path):
        clean_rel = path.replace("assets/icons/", "").replace("assets/", "").replace("icons/", "")
        candidates = [
            REPO_ROOT / path,
            REPO_ROOT / "assets" / path,
            REPO_ROOT / "assets" / "icons" / path,
            REPO_ROOT / "assets" / "icons" / clean_rel,
        ]
        found = False
        for cand in candidates:
            if cand.exists():
                target_path = str(cand)
                found = True
                break
        if not found:
            return None

    with open(target_path, encoding="utf-8", errors="ignore") as f:
        data = f.read()

    # Strip XML declarations and DOCTYPEs
    data = re.sub(r"<\?xml[^>]*\?>", "", data)
    data = re.sub(r"<!DOCTYPE[^>]*>", "", data)

    # Extract viewBox
    vb_match = re.search(r"viewBox=[\"\']([^\"\']+)[\"\']", data)
    if vb_match:
        viewbox = vb_match.group(1)
    else:
        # Fallback to width and height attributes if viewBox is not defined
        w_match = re.search(r"\bwidth=[\"\']([0-9.]+)p?x?[\"\']", data)
        h_match = re.search(r"\bheight=[\"\']([0-9.]+)p?x?[\"\']", data)
        if w_match and h_match:
            viewbox = f"0 0 {w_match.group(1)} {h_match.group(1)}"
        else:
            viewbox = "0 0 100 100"

    # Extract inside of <svg ...> ... </svg>
    inner_match = re.search(r"<svg[^>]*>(.*)</svg>", data, re.DOTALL)
    inner = inner_match.group(1) if inner_match else data
    return viewbox, inner


def namespace_svg_ids(inner: str, prefix: str) -> str:
    """Namespaces IDs and references to prevent collisions across icons in the master SVG."""
    ids = set(re.findall(r"id=[\"\']([^\"\']+)[\"\']", inner))
    namespaced = inner
    for orig_id in ids:
        new_id = f"{prefix}{orig_id}"
        namespaced = re.sub(
            r"id=[\"\']" + re.escape(orig_id) + r"[\"\']", f'id="{new_id}"', namespaced
        )
        namespaced = re.sub(r"url\(#" + re.escape(orig_id) + r"\)", f"url(#{new_id})", namespaced)
        namespaced = re.sub(
            r"href=[\"\']#" + re.escape(orig_id) + r"[\"\']", f'href="#{new_id}"', namespaced
        )
        namespaced = re.sub(
            r"xlink:href=[\"\']#" + re.escape(orig_id) + r"[\"\']",
            f'xlink:href="#{new_id}"',
            namespaced,
        )
    return namespaced


def calculate_icon_dimensions(viewbox: str) -> tuple[float, float]:
    """Dynamically sizes icons to balance visual weights across different aspect ratios."""
    vb_tokens = viewbox.split()
    aspect = 1.0
    if len(vb_tokens) == 4:
        try:
            vw = float(vb_tokens[2])
            vh = float(vb_tokens[3])
            aspect = vw / vh if vh != 0 else 1.0
        except ValueError:
            aspect = 1.0

    if aspect > 1.35:
        # Wide icons (e.g. JAX, TensorFlow): expand width up to 70px
        disp_w = min(70.0, 52.0 * aspect)
        disp_h = disp_w / aspect
    elif aspect < 0.75:
        # Tall icons: maximize height
        disp_h = 54.0
        disp_w = disp_h * aspect
    else:
        # Standard square-proportioned icons
        disp_w = 56.0
        disp_h = 56.0

    return disp_w, disp_h


def process_icon(
    label: str, file_path: str, idx: int, theme: str
) -> tuple[str, str, str, float, float] | None:
    """
    Extracts, color-adapts, namespaces, and dimensions an icon for a badge.
    Returns: (label, viewbox, namespaced_inner, disp_w, disp_h) or None.
    """
    res = extract_svg_content(file_path)
    if not res:
        return None
    viewbox, inner = res

    # Apply color adaptation for current theme
    filename = os.path.basename(file_path)
    adapted_inner = ColorAdapter.adapt(inner, theme, filename)

    # Namespace IDs to prevent conflict in master SVG
    prefix = f"b{idx}_"
    namespaced_inner = namespace_svg_ids(adapted_inner, prefix)

    disp_w, disp_h = calculate_icon_dimensions(viewbox)
    return label, viewbox, namespaced_inner, disp_w, disp_h
