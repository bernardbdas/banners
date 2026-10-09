"""Unit tests for presets and themes configuration."""

import unittest

from banners.constants import REPO_ROOT
from banners.presets import PRESETS
from banners.themes import THEMES


class TestPresets(unittest.TestCase):
    """Test suite for PRESETS data structures and file references."""

    def test_presets_exist(self):
        """Verify that role presets are populated."""
        self.assertGreater(len(PRESETS), 0)

    def test_preset_structure(self):
        """Ensure all presets have title, subtitle, and non-empty icons list."""
        for name, preset in PRESETS.items():
            self.assertIn("title", preset, f"Preset '{name}' missing 'title'")
            self.assertIn("subtitle", preset, f"Preset '{name}' missing 'subtitle'")
            self.assertIn("icons", preset, f"Preset '{name}' missing 'icons'")
            self.assertIsInstance(preset["icons"], list)
            self.assertGreater(len(preset["icons"]), 0, f"Preset '{name}' has no icons")

            for item in preset["icons"]:
                self.assertEqual(len(item), 2, f"Invalid icon tuple in preset '{name}': {item}")
                label, icon_path = item
                self.assertIsInstance(label, str)
                self.assertIsInstance(icon_path, str)

    def test_all_preset_icons_exist_on_disk(self):
        """Verify that every icon file referenced in PRESETS exists in the repository."""
        missing = []
        for preset_name, data in PRESETS.items():
            for label, icon_rel_path in data["icons"]:
                full_path = REPO_ROOT / icon_rel_path
                if not full_path.exists():
                    missing.append((preset_name, label, str(full_path)))

        self.assertEqual(missing, [], f"Missing icon files referenced in PRESETS: {missing}")


class TestThemes(unittest.TestCase):
    """Test suite for THEMES definitions."""

    def test_required_themes_exist(self):
        """Verify standard themes (dark, light) are configured."""
        self.assertIn("dark", THEMES)
        self.assertIn("light", THEMES)

    def test_theme_attributes(self):
        """Verify all themes define necessary styling tokens."""
        required_keys = [
            "bg_stops",
            "card_stops",
            "card_stroke",
            "card_shadow_flood",
            "card_shadow_opacity",
            "card_shadow_blur",
            "title_color",
            "subtitle_color",
            "badge_text_color",
            "accent_stops",
            "ambient_1",
            "ambient_1_op",
            "ambient_2",
            "ambient_2_op",
        ]
        for theme_name, theme in THEMES.items():
            for key in required_keys:
                self.assertIn(key, theme, f"Theme '{theme_name}' is missing '{key}'")


if __name__ == "__main__":
    unittest.main()
