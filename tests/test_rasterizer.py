"""Unit tests for rasterizer module."""

import unittest
from unittest.mock import patch

from banners.rasterizer import find_rasterizer_binary, rasterize_svg


class TestRasterizer(unittest.TestCase):
    """Test suite for rasterization binary lookup and execution."""

    def test_find_rasterizer_binary(self):
        """Verify binary lookup returns either string path or None."""
        binary = find_rasterizer_binary()
        if binary is not None:
            self.assertIsInstance(binary, str)

    @patch("banners.rasterizer.find_rasterizer_binary", return_value=None)
    def test_rasterize_svg_missing_binary(self, _mock_find):
        """Verify graceful failure when rsvg-convert is not found."""
        success = rasterize_svg("dummy.svg", "dummy.png")
        self.assertFalse(success)

    @patch("subprocess.run")
    @patch("banners.rasterizer.find_rasterizer_binary", return_value="/usr/bin/rsvg-convert")
    def test_rasterize_svg_upscale_command(self, _mock_bin, mock_run):
        """Verify scale multiplier is applied to output dimensions."""
        rasterize_svg("input.svg", "output.png", width=1584, height=396, scale=4)
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        self.assertIn("-w", cmd)
        self.assertIn("6336", cmd)
        self.assertIn("-h", cmd)
        self.assertIn("1584", cmd)


if __name__ == "__main__":
    unittest.main()
