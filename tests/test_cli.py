"""Unit tests for the CLI module."""

import io
import unittest
from unittest.mock import patch

from banners.cli import main, print_help


class TestCLI(unittest.TestCase):
    """Test suite for CLI argument parsing and execution."""

    def test_print_help_runs(self):
        """Verify print_help outputs without error."""
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            print_help()
            self.assertIn("Available presets", fake_out.getvalue())

    def test_cli_help_flag(self):
        """Verify --help flag exits with code 0."""
        with patch("sys.stdout", new=io.StringIO()):
            self.assertEqual(main(["--help"]), 0)
            self.assertEqual(main(["-h"]), 0)
            self.assertEqual(main(["--list"]), 0)

    def test_cli_unknown_preset_exits_1(self):
        """Verify invalid preset returns error exit code 1."""
        with patch("sys.stderr", new=io.StringIO()):
            self.assertEqual(main(["unknown_preset_xyz"]), 1)

    def test_cli_unknown_theme_exits_1(self):
        """Verify invalid theme returns error exit code 1."""
        with patch("sys.stderr", new=io.StringIO()):
            self.assertEqual(main(["backend", "neon"]), 1)

    def test_cli_unknown_format_exits_1(self):
        """Verify invalid format returns error exit code 1."""
        with patch("sys.stderr", new=io.StringIO()):
            self.assertEqual(main(["backend", "dark", "gif"]), 1)

    def test_cli_hyphen_preset_normalization(self):
        """Verify preset names with hyphens (e.g. ai-ml) succeed."""
        with patch("banners.cli.generate_banner") as mock_gen:
            res = main(["ai-ml", "dark", "svg"])
            self.assertEqual(res, 0)
            mock_gen.assert_called_once()
            call_kwargs = mock_gen.call_args[1]
            self.assertEqual(call_kwargs["preset_name"], "ai_ml")
            self.assertEqual(call_kwargs["theme_name"], "dark")
            self.assertTrue(call_kwargs["output_svg_path"].startswith("exported"))

    def test_cli_all_execution(self):
        """Verify 'all' preset and theme delegates to multiple banner generation calls."""
        with patch("banners.cli.generate_banner") as mock_gen:
            res = main(["backend", "all", "svg"])
            self.assertEqual(res, 0)
            # 2 themes (dark, light)
            self.assertEqual(mock_gen.call_count, 2)

    def test_cli_custom_scale(self):
        """Verify CLI forwards custom scale multiplier."""
        with patch("banners.cli.generate_banner") as mock_gen:
            res = main(["backend", "dark", "png", "2"])
            self.assertEqual(res, 0)
            self.assertEqual(mock_gen.call_args[1]["scale"], 2)

    def test_cli_invalid_scale(self):
        """Verify invalid scale factor returns exit code 1."""
        with patch("sys.stderr"):
            self.assertEqual(main(["backend", "dark", "png", "invalid"]), 1)
            self.assertEqual(main(["backend", "dark", "png", "0"]), 1)


if __name__ == "__main__":
    unittest.main()
