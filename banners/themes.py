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
}
