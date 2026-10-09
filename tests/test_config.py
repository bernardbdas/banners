"""Unit tests for config and local.env loader module."""

import os
import tempfile
import unittest
from unittest.mock import patch

from banners.config import BannerConfig, load_config, parse_env_file


class TestConfig(unittest.TestCase):
    """Test suite for environment and local.env parsing."""

    def test_parse_env_file_valid(self):
        """Verify parsing of valid key-value pairs, comments, and quotes."""
        content = """
# Comment line
WEBSITE_URL="https://example.dev"
EMAIL = 'dev@example.dev'
BANNER_NAME=ai_ml # inline comment
EMPTY_LINE=

# Another section
UNQUOTED_VAL=simple_val
"""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".env") as f:
            f.write(content)
            temp_path = f.name

        try:
            parsed = parse_env_file(temp_path)
            self.assertEqual(parsed["WEBSITE_URL"], "https://example.dev")
            self.assertEqual(parsed["EMAIL"], "dev@example.dev")
            self.assertEqual(parsed["BANNER_NAME"], "ai_ml")
            self.assertEqual(parsed["UNQUOTED_VAL"], "simple_val")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_parse_env_file_nonexistent(self):
        """Verify nonexistent file returns empty dict."""
        self.assertEqual(parse_env_file("nonexistent_env_file_12345.env"), {})

    def test_load_config_with_custom_file(self):
        """Verify load_config reads values from a provided env file."""
        content = "WEBSITE_URL=https://myportfolio.io\nEMAIL=me@myportfolio.io\nBANNER_NAME=devops\nBACKGROUND=topographical\n"
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".env") as f:
            f.write(content)
            temp_path = f.name

        try:
            with patch.dict(os.environ, {}, clear=True):
                cfg = load_config(temp_path)
                self.assertIsInstance(cfg, BannerConfig)
                self.assertEqual(cfg.website_url, "https://myportfolio.io")
                self.assertEqual(cfg.email, "me@myportfolio.io")
                self.assertEqual(cfg.banner_name, "devops")
                self.assertEqual(cfg.background, "topographical")
                self.assertEqual(cfg.theme, "topographical")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_parse_fade_percentage(self):
        """Verify parsing of various percentage, float, and edge case fade inputs."""
        from banners.config import parse_fade_percentage

        self.assertAlmostEqual(parse_fade_percentage("40%"), 0.40)
        self.assertAlmostEqual(parse_fade_percentage("40"), 0.40)
        self.assertAlmostEqual(parse_fade_percentage("0.4"), 0.40)
        self.assertAlmostEqual(parse_fade_percentage("100%"), 1.00)
        self.assertAlmostEqual(parse_fade_percentage("100"), 1.00)
        self.assertAlmostEqual(parse_fade_percentage("1"), 1.00)
        self.assertAlmostEqual(parse_fade_percentage("0%"), 0.00)
        self.assertAlmostEqual(parse_fade_percentage("0"), 0.00)
        self.assertAlmostEqual(parse_fade_percentage(None), 1.00)
        self.assertAlmostEqual(parse_fade_percentage(""), 1.00)
        self.assertAlmostEqual(parse_fade_percentage(0.75), 0.75)
        self.assertAlmostEqual(parse_fade_percentage(50), 0.50)
        self.assertAlmostEqual(parse_fade_percentage("invalid"), 1.00)

    def test_load_config_fade_setting(self):
        """Verify load_config reads FADE from env file and respects environment overrides."""
        content = "WEBSITE_URL=https://test.io\nFADE=35%\n"
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".env") as f:
            f.write(content)
            temp_path = f.name

        try:
            with patch.dict(os.environ, {}, clear=True):
                cfg = load_config(temp_path)
                self.assertAlmostEqual(cfg.fade, 0.35)

            with patch.dict(os.environ, {"FADE": "60%"}, clear=True):
                cfg = load_config(temp_path)
                self.assertAlmostEqual(cfg.fade, 0.60)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
