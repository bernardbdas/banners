"""Unit tests for banner generator module."""

import os
import tempfile
import unittest
import xml.etree.ElementTree as ET

from banners.constants import BANNER_HEIGHT, BANNER_WIDTH
from banners.generator import build_banner_svg, estimate_pill_width, generate_banner
from banners.presets import PRESETS
from banners.themes import THEMES


class TestGenerator(unittest.TestCase):
    """Test suite for SVG assembly and file generation."""

    def test_build_banner_svg_all_presets_and_themes(self):
        """Ensure build_banner_svg produces valid XML for all presets across all themes."""
        for theme_name in THEMES:
            for preset_name in PRESETS:
                svg_content = build_banner_svg(preset_name, theme_name)
                self.assertIsInstance(svg_content, str)
                root = ET.fromstring(svg_content)
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
                self.assertEqual(root.attrib.get("width"), str(BANNER_WIDTH))
                self.assertEqual(root.attrib.get("height"), str(BANNER_HEIGHT))

    def test_build_banner_svg_unknown_preset_raises(self):
        """Ensure unknown preset raises ValueError."""
        with self.assertRaises(ValueError):
            build_banner_svg("nonexistent_preset", "dark")

    def test_generate_banner_file_output(self):
        """Verify generate_banner writes SVG file properly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            svg_file = os.path.join(tmpdir, "test_banner.svg")
            generate_banner(
                preset_name="backend",
                theme_name="dark",
                output_svg_path=svg_file,
                gen_svg=True,
                gen_png=False,
            )
            self.assertTrue(os.path.exists(svg_file))
            with open(svg_file, encoding="utf-8") as f:
                content = f.read()
            self.assertTrue(content.startswith("<svg"))

    def test_build_banner_svg_with_contact_info(self):
        """Verify that website_url and email are rendered in SVG and form valid XML."""
        svg_content = build_banner_svg(
            preset_name="backend",
            theme_name="dark",
            website_url="https://janedoe.dev",
            email="jane@doe.dev",
        )
        self.assertIn("https://janedoe.dev", svg_content)
        self.assertIn("jane@doe.dev", svg_content)
        root = ET.fromstring(svg_content)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_build_banner_svg_typography_and_badge_sizing(self):
        """Verify that title, subtitle, and badge labels use enlarged font sizes with letter spacing."""
        svg_content = build_banner_svg("backend", "dark", website_url="", email="")
        self.assertIn('font-size="48"', svg_content)
        self.assertIn('letter-spacing="1.5"', svg_content)
        self.assertIn('font-size="22"', svg_content)
        self.assertIn('letter-spacing="0.5"', svg_content)
        self.assertIn('font-size="12.5"', svg_content)

    def test_build_banner_svg_with_pattern_fade(self):
        """Verify that pattern fade opacity is applied to the pattern layer."""
        svg_content = build_banner_svg(
            preset_name="backend",
            theme_name="dark",
            background="topographical",
            fade=0.45,
        )
        self.assertIn('id="pattern_layer" opacity="0.45"', svg_content)
        root = ET.fromstring(svg_content)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_build_banner_svg_with_custom_background(self):
        """Verify custom background elements are embedded and produce valid XML."""
        svg_content = build_banner_svg(
            preset_name="backend",
            theme_name="dark",
            background="topographical",
        )
        self.assertIn("Custom Background", svg_content)
        root = ET.fromstring(svg_content)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_build_banner_svg_with_pastel_background_contrast(self):
        """Verify pastel background triggers high-contrast dark text adaptation."""
        svg_content = build_banner_svg(
            preset_name="backend",
            theme_name="dark",
            background="pastel_mesh",
        )
        # Should have dark slate title color for high contrast against pastel background
        self.assertIn('fill="#0F172A"', svg_content)
        root = ET.fromstring(svg_content)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_estimate_pill_width_resizing(self):
        """Verify that contact pill width dynamically scales with URL/email length and characters."""
        short_w = estimate_pill_width("short.io")
        medium_w = estimate_pill_width("bernardbdas@gmail.com")
        long_w = estimate_pill_width("https://bernardbdas.github.io")

        self.assertGreater(medium_w, short_w)
        self.assertGreater(long_w, medium_w)
        # Verify minimum bounds and compact snug fit
        self.assertGreaterEqual(short_w, 90)
        self.assertLess(long_w, 260)  # Snugger than the old 296px over-estimation

    def test_build_banner_svg_with_theme_name_as_background(self):
        """Verify passing a background name as theme_name automatically loads it."""
        svg_content = build_banner_svg("backend", "topographical")
        self.assertIn("Custom Background", svg_content)
        root = ET.fromstring(svg_content)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")


if __name__ == "__main__":
    unittest.main()
