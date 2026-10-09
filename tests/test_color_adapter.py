"""Unit tests for ColorAdapter module."""

import unittest

from banners.color_adapter import ColorAdapter


class TestColorAdapter(unittest.TestCase):
    """Test suite for ColorAdapter dynamic SVG styling."""

    def test_current_color_dark_mode(self):
        """Verify currentColor is adapted to white in dark mode."""
        svg = '<path fill="currentColor" stroke="currentColor"/>'
        adapted = ColorAdapter.adapt_for_dark_mode(svg)
        self.assertIn('fill="#FFFFFF"', adapted)
        self.assertIn('stroke="#FFFFFF"', adapted)

    def test_current_color_light_mode(self):
        """Verify currentColor is adapted to slate in light mode."""
        svg = '<path fill="currentColor" stroke="currentColor"/>'
        adapted = ColorAdapter.adapt_for_light_mode(svg)
        self.assertIn('fill="#0F172A"', adapted)
        self.assertIn('stroke="#0F172A"', adapted)

    def test_monochrome_black_to_white_dark_mode(self):
        """Verify pure black monochrome SVG paths get converted to white in dark mode."""
        svg = '<path fill="#000000" d="M0 0h10v10H0z"/>'
        adapted = ColorAdapter.adapt_for_dark_mode(svg)
        self.assertIn('fill="#FFFFFF"', adapted)

    def test_nextjs_dark_mode(self):
        """Verify Next.js special handling in dark mode."""
        svg = '<circle cx="64" cy="64" r="64"/><stop stop-color="#fff"/>'
        adapted = ColorAdapter.adapt(svg, "dark", filename="nextjs.svg")
        self.assertIn('<circle cx="64" cy="64" r="64" fill="#FFFFFF"/>', adapted)
        self.assertIn('stop-color="#000000"', adapted)

    def test_nextjs_light_mode(self):
        """Verify Next.js special handling in light mode."""
        svg = '<circle cx="64" cy="64" r="64"/>'
        adapted = ColorAdapter.adapt(svg, "light", filename="nextjs.svg")
        self.assertIn('<circle cx="64" cy="64" r="64" fill="#000000"/>', adapted)

    def test_unknown_theme_passthrough(self):
        """Verify unrecognized theme returns SVG unaltered."""
        svg = '<path fill="red"/>'
        self.assertEqual(ColorAdapter.adapt(svg, "custom"), svg)


if __name__ == "__main__":
    unittest.main()
