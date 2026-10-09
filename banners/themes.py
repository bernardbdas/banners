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
        "contact_text_color": "#E2E8F0",
        "contact_icon_color": "#38BDF8",
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
        "contact_text_color": "#0F172A",
        "contact_icon_color": "#0284C7",
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
        "contact_text_color": "#E2E8F0",
        "contact_icon_color": "#38BDF8",
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
        "contact_text_color": "#0F172A",
        "contact_icon_color": "#0A66C2",
        "accent_stops": [("0%", "#70B5F9"), ("50%", "#FFFFFF"), ("100%", "#38BDF8")],
        "ambient_1": "#70B5F9",
        "ambient_1_op": "0.20",
        "ambient_2": "#0A66C2",
        "ambient_2_op": "0.25",
    },
    "tortoiseshell": {
        "bg_stops": [("0%", "#7C3B0B"), ("50%", "#A55412"), ("100%", "#6E3208")],
        "card_stops": [("0%", "#1C0D05", "0.90"), ("100%", "#0F0702", "0.90")],
        "card_stroke": "#D97706",
        "card_shadow_flood": "#000000",
        "card_shadow_opacity": "0.50",
        "card_shadow_blur": "8",
        "title_color": "#FFFFFF",
        "subtitle_color": "#FEF08A",
        "badge_text_color": "#FEF3C7",
        "contact_text_color": "#FFFFFF",
        "contact_icon_color": "#F59E0B",
        "accent_stops": [("0%", "#FDE047"), ("50%", "#F59E0B"), ("100%", "#D97706")],
        "ambient_1": "#F59E0B",
        "ambient_1_op": "0.18",
        "ambient_2": "#FDE047",
        "ambient_2_op": "0.12",
    },
    "leopard": {
        "bg_stops": [("0%", "#8C5317"), ("50%", "#B87729"), ("100%", "#7F4913")],
        "card_stops": [("0%", "#1F1106", "0.90"), ("100%", "#120A03", "0.90")],
        "card_stroke": "#D97706",
        "card_shadow_flood": "#000000",
        "card_shadow_opacity": "0.50",
        "card_shadow_blur": "8",
        "title_color": "#FFFFFF",
        "subtitle_color": "#FEF08A",
        "badge_text_color": "#FEF3C7",
        "contact_text_color": "#FFFFFF",
        "contact_icon_color": "#F59E0B",
        "accent_stops": [("0%", "#FEF08A"), ("50%", "#F59E0B"), ("100%", "#B45309")],
        "ambient_1": "#F59E0B",
        "ambient_1_op": "0.18",
        "ambient_2": "#FEF08A",
        "ambient_2_op": "0.14",
    },
    "tiger": {
        "bg_stops": [("0%", "#9C440B"), ("50%", "#C75E14"), ("100%", "#8B3A08")],
        "card_stops": [("0%", "#220E04", "0.90"), ("100%", "#130702", "0.90")],
        "card_stroke": "#F97316",
        "card_shadow_flood": "#000000",
        "card_shadow_opacity": "0.50",
        "card_shadow_blur": "8",
        "title_color": "#FFFFFF",
        "subtitle_color": "#FED7AA",
        "badge_text_color": "#FFEDD5",
        "contact_text_color": "#FFFFFF",
        "contact_icon_color": "#F97316",
        "accent_stops": [("0%", "#FDBA74"), ("50%", "#F97316"), ("100%", "#EA580C")],
        "ambient_1": "#EA580C",
        "ambient_1_op": "0.20",
        "ambient_2": "#F97316",
        "ambient_2_op": "0.14",
    },
    "topographical_crimson": {
        "bg_stops": [("0%", "#0B0405"), ("50%", "#160709"), ("100%", "#080203")],
        "card_stops": [("0%", "#18080A", "0.90"), ("100%", "#0D0405", "0.90")],
        "card_stroke": "#991B1B",
        "card_shadow_flood": "#000000",
        "card_shadow_opacity": "0.60",
        "card_shadow_blur": "8",
        "title_color": "#FFFFFF",
        "subtitle_color": "#FECACA",
        "badge_text_color": "#FEE2E2",
        "contact_text_color": "#FFFFFF",
        "contact_icon_color": "#EF4444",
        "accent_stops": [("0%", "#FF2A4D"), ("50%", "#DC2626"), ("100%", "#991B1B")],
        "ambient_1": "#DC2626",
        "ambient_1_op": "0.15",
        "ambient_2": "#FF2A4D",
        "ambient_2_op": "0.10",
    },
    "topographical_crimson_light": {
        "bg_stops": [("0%", "#FFFFFF"), ("50%", "#FFF7F8"), ("100%", "#FFEBEF")],
        "card_stops": [("0%", "#FFFFFF", "0.95"), ("100%", "#FFF5F7", "0.92")],
        "card_stroke": "#FECDD3",
        "card_shadow_flood": "#881337",
        "card_shadow_opacity": "0.10",
        "card_shadow_blur": "10",
        "title_color": "#881337",
        "subtitle_color": "#9F1239",
        "badge_text_color": "#9F1239",
        "contact_text_color": "#881337",
        "contact_icon_color": "#E11D48",
        "accent_stops": [("0%", "#FB7185"), ("50%", "#E11D48"), ("100%", "#9F1239")],
        "ambient_1": "#FB7185",
        "ambient_1_op": "0.08",
        "ambient_2": "#E11D48",
        "ambient_2_op": "0.06",
    },
    "topographical_cyber": {
        "bg_stops": [("0%", "#030712"), ("50%", "#090D1A"), ("100%", "#02040A")],
        "card_stops": [("0%", "#0A0F1F", "0.90"), ("100%", "#040711", "0.90")],
        "card_stroke": "#06B6D4",
        "card_shadow_flood": "#000000",
        "card_shadow_opacity": "0.70",
        "card_shadow_blur": "10",
        "title_color": "#FFFFFF",
        "subtitle_color": "#67E8F9",
        "badge_text_color": "#E0E7FF",
        "contact_text_color": "#F8FAFC",
        "contact_icon_color": "#F43F5E",
        "accent_stops": [("0%", "#06B6D4"), ("50%", "#A855F7"), ("100%", "#F43F5E")],
        "ambient_1": "#06B6D4",
        "ambient_1_op": "0.20",
        "ambient_2": "#F43F5E",
        "ambient_2_op": "0.15",
    },
    "topographical_vintage": {
        "bg_stops": [("0%", "#F7F3EB"), ("50%", "#EDE4D3"), ("100%", "#E2D5BE")],
        "card_stops": [("0%", "#FFFDF9", "0.94"), ("100%", "#F7F2E8", "0.92")],
        "card_stroke": "#D6C7B2",
        "card_shadow_flood": "#44403C",
        "card_shadow_opacity": "0.12",
        "card_shadow_blur": "8",
        "title_color": "#1C1917",
        "subtitle_color": "#57534E",
        "badge_text_color": "#292524",
        "contact_text_color": "#1C1917",
        "contact_icon_color": "#854D0E",
        "accent_stops": [("0%", "#A16207"), ("50%", "#78350F"), ("100%", "#451A03")],
        "ambient_1": "#A16207",
        "ambient_1_op": "0.08",
        "ambient_2": "#78350F",
        "ambient_2_op": "0.06",
    },
}

# Aliases for convenience
THEMES["tortoise"] = THEMES["tortoiseshell"]
THEMES["tortoise_shell"] = THEMES["tortoiseshell"]
THEMES["tortoise_print"] = THEMES["tortoiseshell"]
THEMES["leopard_skin"] = THEMES["leopard"]
THEMES["leopard_print"] = THEMES["leopard"]
THEMES["tiger_skin"] = THEMES["tiger"]
THEMES["tiger_stripes"] = THEMES["tiger"]
THEMES["tiger_print"] = THEMES["tiger"]
THEMES["topographical_blood_red"] = THEMES["topographical_crimson"]
THEMES["topographical_red"] = THEMES["topographical_crimson"]
THEMES["blood_red"] = THEMES["topographical_crimson"]
THEMES["crimson"] = THEMES["topographical_crimson"]
THEMES["topographical_blood_red_light"] = THEMES["topographical_crimson_light"]
THEMES["topographical_red_light"] = THEMES["topographical_crimson_light"]
THEMES["blood_red_light"] = THEMES["topographical_crimson_light"]
THEMES["crimson_light"] = THEMES["topographical_crimson_light"]
THEMES["cyber"] = THEMES["topographical_cyber"]
THEMES["topographical_neon"] = THEMES["topographical_cyber"]
THEMES["neon_topo"] = THEMES["topographical_cyber"]
THEMES["vintage"] = THEMES["topographical_vintage"]
THEMES["topographical_parchment"] = THEMES["topographical_vintage"]
THEMES["parchment_topo"] = THEMES["topographical_vintage"]


def get_available_themes() -> list[str]:
    """Returns a sorted list of all available themes (built-ins + custom backgrounds)."""
    from banners.backgrounds import list_available_backgrounds

    bgs = list_available_backgrounds()
    return sorted(list(dict.fromkeys([*THEMES.keys(), *bgs])))
