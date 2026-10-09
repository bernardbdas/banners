"""Unit tests for SVG processor module."""

import unittest

from banners.svg_processor import (
    calculate_icon_dimensions,
    extract_svg_content,
    namespace_svg_ids,
    process_icon,
)


class TestSvgProcessor(unittest.TestCase):
    """Test suite for SVG parsing, namespacing, and sizing."""

    def test_extract_svg_content_valid(self):
        """Verify extraction from an existing icon with assets/ prefix and fallback."""
        res = extract_svg_content("assets/backend/golang.svg")
        self.assertIsNotNone(res)
        viewbox, inner = res
        self.assertIsInstance(viewbox, str)
        self.assertIsInstance(inner, str)
        self.assertTrue(len(inner) > 0)

        # Also verify fallback resolution when given without assets/
        res_fallback = extract_svg_content("backend/golang.svg")
        self.assertIsNotNone(res_fallback)

    def test_extract_svg_content_nonexistent(self):
        """Verify extraction returns None for nonexistent files."""
        res = extract_svg_content("nonexistent/path/icon.svg")
        self.assertIsNone(res)

    def test_namespace_svg_ids(self):
        """Verify ID namespacing and reference substitution."""
        svg = '<g id="grad1"><rect fill="url(#grad1)" xlink:href="#grad1" href="#grad1"/></g>'
        prefixed = namespace_svg_ids(svg, "prefix_")
        self.assertIn('id="prefix_grad1"', prefixed)
        self.assertIn("url(#prefix_grad1)", prefixed)
        self.assertIn('xlink:href="#prefix_grad1"', prefixed)
        self.assertIn('href="#prefix_grad1"', prefixed)

    def test_calculate_icon_dimensions(self):
        """Verify dynamic scaling based on aspect ratio."""
        # Standard square (enlarged for mobile readability)
        w, h = calculate_icon_dimensions("0 0 100 100")
        self.assertEqual(w, 56.0)
        self.assertEqual(h, 56.0)

        # Wide aspect ratio (> 1.35)
        w, h = calculate_icon_dimensions("0 0 200 100")
        self.assertTrue(w <= 70.0)
        self.assertAlmostEqual(w / h, 2.0, places=2)

        # Tall aspect ratio (< 0.75)
        w, h = calculate_icon_dimensions("0 0 50 100")
        self.assertEqual(h, 54.0)
        self.assertAlmostEqual(w / h, 0.5, places=2)

    def test_process_icon(self):
        """Verify process_icon pipeline."""
        res = process_icon("Golang", "backend/golang.svg", 0, "dark")
        self.assertIsNotNone(res)
        label, _viewbox, _namespaced_inner, disp_w, disp_h = res
        self.assertEqual(label, "Golang")
        self.assertTrue(disp_w > 0)
        self.assertTrue(disp_h > 0)


if __name__ == "__main__":
    unittest.main()
