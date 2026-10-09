"""Unit tests for banner generator module."""

import os
import tempfile
import unittest
import xml.etree.ElementTree as ET

from banners.constants import BANNER_HEIGHT, BANNER_WIDTH
from banners.generator import build_banner_svg, generate_banner
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


if __name__ == "__main__":
    unittest.main()
