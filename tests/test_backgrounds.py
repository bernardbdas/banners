"""Unit tests for the backgrounds module."""

import unittest

from banners.backgrounds import (
    list_available_backgrounds,
    load_background_svg,
    resolve_background_path,
)


class TestBackgrounds(unittest.TestCase):
    """Test suite for background discovery, resolution, and SVG loading."""

    def test_list_available_backgrounds(self):
        """Verify that all created background SVGs across subdirectories are discovered."""
        bgs = list_available_backgrounds()
        self.assertGreater(len(bgs), 0)
        # Patterns
        self.assertIn("topographical", bgs)
        self.assertIn("topographical_light", bgs)
        self.assertIn("topographical_pastel", bgs)
        self.assertIn("topographical_dense", bgs)
        self.assertIn("topographical_crimson", bgs)
        self.assertIn("topographical_crimson_light", bgs)
        self.assertIn("topographical_cyber", bgs)
        self.assertIn("topographical_vintage", bgs)
        self.assertIn("topographical_papercut", bgs)
        self.assertIn("topographical_particles", bgs)
        self.assertIn("topographical_midnight", bgs)
        self.assertIn("topographical_oceanic", bgs)
        self.assertIn("topographical_cartographic", bgs)
        self.assertIn("grid_matrix", bgs)
        self.assertIn("circuit_board", bgs)
        self.assertIn("flowing_waves", bgs)
        # Gradients
        self.assertIn("pastel_aurora", bgs)
        self.assertIn("pastel_mesh", bgs)
        self.assertIn("pastel_sunset", bgs)
        self.assertIn("pastel_mint", bgs)
        # Solids
        self.assertIn("solid_lavender", bgs)
        self.assertIn("solid_blush", bgs)
        self.assertIn("solid_peach", bgs)
        self.assertIn("solid_cream", bgs)
        self.assertIn("solid_mint", bgs)
        self.assertIn("solid_sky", bgs)
        self.assertIn("solid_periwinkle", bgs)
        self.assertIn("solid_sand", bgs)

    def test_resolve_background_path(self):
        """Verify resolution by name, subdirectory prefix, hyphen normalization, and extension."""
        p1 = resolve_background_path("topographical")
        self.assertIsNotNone(p1)
        self.assertTrue(p1.is_file())

        # Category prefix resolution
        p1_sub = resolve_background_path("patterns/topographical")
        self.assertEqual(p1, p1_sub)

        # Solid pastel resolution with prefix and direct name
        p_solid = resolve_background_path("solid_lavender")
        self.assertIsNotNone(p_solid)
        p_solid_sub = resolve_background_path("solids/solid_lavender")
        self.assertEqual(p_solid, p_solid_sub)

        p2 = resolve_background_path("topographical.svg")
        self.assertEqual(p1, p2)

        # Hyphen normalization
        p3 = resolve_background_path("pastel-aurora")
        self.assertIsNotNone(p3)
        self.assertEqual(p3.stem, "pastel_aurora")

        # None / default
        self.assertIsNone(resolve_background_path(""))
        self.assertIsNone(resolve_background_path("default"))
        self.assertIsNone(resolve_background_path("none"))
        self.assertIsNone(resolve_background_path("nonexistent_bg_xyz"))

    def test_load_background_svg(self):
        """Verify SVG defs and body extraction."""
        res = load_background_svg("topographical")
        self.assertIsNotNone(res)
        defs_xml, body_xml, is_pastel = res
        self.assertIsInstance(defs_xml, str)
        self.assertIsInstance(body_xml, str)
        self.assertFalse(is_pastel)
        self.assertIn("<linearGradient", defs_xml)
        self.assertIn("<path", body_xml)

    def test_load_pastel_and_solid_background_flag(self):
        """Verify pastel flag detection for pastel gradients and solid pastels."""
        res_mesh = load_background_svg("pastel_mesh")
        self.assertIsNotNone(res_mesh)
        self.assertTrue(res_mesh[2])

        res_solid = load_background_svg("solid_lavender")
        self.assertIsNotNone(res_solid)
        self.assertTrue(res_solid[2])

        res_light = load_background_svg("topographical_light")
        self.assertIsNotNone(res_light)
        self.assertTrue(res_light[2])


if __name__ == "__main__":
    unittest.main()
