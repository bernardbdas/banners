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
        from banners.themes import get_available_themes

        with patch("banners.cli.generate_banner") as mock_gen:
            res = main(["backend", "all", "svg"])
            self.assertEqual(res, 0)
            self.assertEqual(mock_gen.call_count, len(get_available_themes()))

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

    def test_cli_uses_banner_name_from_config(self):
        """Verify that when no CLI args are given, BANNER_NAME and THEME from config are used."""
        with (
            patch("banners.cli.load_config") as mock_cfg,
            patch("banners.cli.generate_banner") as mock_gen,
        ):
            mock_cfg.return_value.banner_name = "fullstack"
            mock_cfg.return_value.theme = "topographical"
            mock_cfg.return_value.background = "topographical"
            mock_cfg.return_value.website_url = "https://portfolio.dev"
            mock_cfg.return_value.email = "dev@portfolio.dev"
            res = main([])
            self.assertEqual(res, 0)
            mock_gen.assert_called_once()
            call_kwargs = mock_gen.call_args[1]
            self.assertEqual(call_kwargs["preset_name"], "fullstack")
            self.assertEqual(call_kwargs["theme_name"], "topographical")
            self.assertEqual(
                call_kwargs["output_png_path"], "exported/topographical/png/banner_fullstack.png"
            )
            self.assertEqual(call_kwargs["website_url"], "https://portfolio.dev")
            self.assertEqual(call_kwargs["email"], "dev@portfolio.dev")

    def test_cli_theme_argument(self):
        """Verify theme argument directly accepts any custom background theme."""
        with patch("banners.cli.generate_banner") as mock_gen:
            res = main(["backend", "topographical_light", "png"])
            self.assertEqual(res, 0)
            mock_gen.assert_called_once()
            call_kwargs = mock_gen.call_args[1]
            self.assertEqual(call_kwargs["preset_name"], "backend")
            self.assertEqual(call_kwargs["theme_name"], "topographical_light")
            self.assertEqual(
                call_kwargs["output_png_path"],
                "exported/topographical_light/png/banner_backend.png",
            )

    def test_cli_bg_flag_override(self):
        """Verify --bg and --background override config background setting."""
        with patch("banners.cli.generate_banner") as mock_gen:
            res = main(["backend", "dark", "svg", "--bg", "topographical_light"])
            self.assertEqual(res, 0)
            mock_gen.assert_called_once()
            self.assertEqual(mock_gen.call_args[1]["background"], "topographical_light")

    def test_cli_fade_flag_override(self):
        """Verify --fade flag forwards parsed opacity float to generate_banner."""
        with patch("banners.cli.generate_banner") as mock_gen:
            res = main(["backend", "topographical", "svg", "--fade", "40%"])
            self.assertEqual(res, 0)
            mock_gen.assert_called_once()
            self.assertAlmostEqual(mock_gen.call_args[1]["fade"], 0.40)

        with patch("banners.cli.generate_banner") as mock_gen:
            res = main(["backend", "topographical", "svg", "--fade=65"])
            self.assertEqual(res, 0)
            mock_gen.assert_called_once()
            self.assertAlmostEqual(mock_gen.call_args[1]["fade"], 0.65)

    def test_cli_fade_positional_arg(self):
        """Verify 5th positional argument is parsed as fade percentage."""
        with patch("banners.cli.generate_banner") as mock_gen:
            res = main(["backend", "topographical", "png", "4", "30%"])
            self.assertEqual(res, 0)
            mock_gen.assert_called_once()
            self.assertAlmostEqual(mock_gen.call_args[1]["fade"], 0.30)


if __name__ == "__main__":
    unittest.main()
