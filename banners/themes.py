"""
Theme configurations for Dark and Light banner rendering.
"""

from typing import Any

THEMES: dict[str, dict[str, Any]] = {
    "dark": {
        "bg_stops": [("0%", "#090D16"), ("50%", "#0F172A"), ("100%", "#020617")],
        "card_stops": [("0%", "#1E293B", "0.85"), ("100%", "#0F172A", "0.85")],
        "card_stroke": "#334155",
        "card_shadow_flood": "#000000",
        "card_shadow_opacity": "0.5",
        "card_shadow_blur": "6",
        "title_color": "#F8FAFC",
        "subtitle_color": "#94A3B8",
        "badge_text_color": "#CBD5E1",
        "accent_stops": [("0%", "#38BDF8"), ("100%", "#818CF8")],
        "ambient_1": "#38BDF8",
        "ambient_1_op": "0.04",
        "ambient_2": "#818CF8",
        "ambient_2_op": "0.03",
    },
    "light": {
        "bg_stops": [("0%", "#FFFFFF"), ("50%", "#F8FAFC"), ("100%", "#F1F5F9")],
        "card_stops": [("0%", "#FFFFFF", "0.95"), ("100%", "#F8FAFC", "0.95")],
        "card_stroke": "#E2E8F0",
        "card_shadow_flood": "#0F172A",
        "card_shadow_opacity": "0.07",
        "card_shadow_blur": "5",
        "title_color": "#0F172A",
        "subtitle_color": "#64748B",
        "badge_text_color": "#334155",
        "accent_stops": [("0%", "#0284C7"), ("100%", "#6366F1")],
        "ambient_1": "#0284C7",
        "ambient_1_op": "0.05",
        "ambient_2": "#6366F1",
        "ambient_2_op": "0.04",
    },
    "network_nodes": {
        "bg_stops": [("0%", "#001428"), ("50%", "#002447"), ("100%", "#001020")],
        "card_stops": [("0%", "#002D5C", "0.90"), ("100%", "#001E3D", "0.90")],
        "card_stroke": "#0D5294",
        "card_shadow_flood": "#000814",
        "card_shadow_opacity": "0.60",
        "card_shadow_blur": "7",
        "title_color": "#FFFFFF",
        "subtitle_color": "#93C5FD",
        "badge_text_color": "#E2E8F0",
        "accent_stops": [("0%", "#0A66C2"), ("50%", "#38BDF8"), ("100%", "#60A5FA")],
        "ambient_1": "#0A66C2",
        "ambient_1_op": "0.10",
        "ambient_2": "#38BDF8",
        "ambient_2_op": "0.08",
    },
    "linkedin": {
        "bg_stops": [("0%", "#003870"), ("35%", "#0A66C2"), ("100%", "#002447")],
        "card_stops": [("0%", "#FFFFFF", "0.96"), ("100%", "#F4F7FB", "0.92")],
        "card_stroke": "#C2DCF7",
        "card_shadow_flood": "#001E3D",
        "card_shadow_opacity": "0.32",
        "card_shadow_blur": "8",
        "title_color": "#FFFFFF",
        "subtitle_color": "#E0F2FE",
        "badge_text_color": "#0F172A",
        "accent_stops": [("0%", "#70B5F9"), ("50%", "#FFFFFF"), ("100%", "#38BDF8")],
        "ambient_1": "#70B5F9",
        "ambient_1_op": "0.20",
        "ambient_2": "#0A66C2",
        "ambient_2_op": "0.25",
    },
}


def get_available_themes() -> list[str]:
    """Returns a sorted list of all available themes (built-ins + custom backgrounds)."""
    from banners.backgrounds import list_available_backgrounds

    bgs = list_available_backgrounds()
    return sorted(list(dict.fromkeys([*THEMES.keys(), *bgs])))
