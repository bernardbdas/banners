"""Unit tests for fine-grained banner customization and visual standards."""

import unittest

from banners.custom import (
    MAX_ICONS,
    MAX_SUBTITLE_LENGTH,
    MAX_TITLE_LENGTH,
    MIN_ICONS,
    build_custom_preset,
    parse_icons_arg,
    resolve_icon,
    validate_banner_standards,
)
from banners.generator import build_banner_svg


class TestCustomBanner(unittest.TestCase):
    """Test suite for custom banner specification, icon resolution, and standards."""

    def test_resolve_canonical_icons(self):
        """Verify standard canonical icon names resolve correctly."""
        label, path = resolve_icon("python")
        self.assertEqual(label, "Python")
        self.assertTrue(path.endswith("python.svg"))

        label, path = resolve_icon("docker")
        self.assertEqual(label, "Docker")
        self.assertTrue(path.endswith("docker.svg"))

    def test_resolve_icon_aliases(self):
        """Verify common developer aliases resolve to official icons."""
        label, path = resolve_icon("k8s")
        self.assertEqual(label, "Kubernetes")
        self.assertTrue(path.endswith("kubernetes.svg"))

        label, path = resolve_icon("cpp")
        self.assertEqual(label, "C++")
        self.assertTrue(path.endswith("cplusplus.svg"))

        label, path = resolve_icon("postgres")
        self.assertEqual(label, "PostgreSQL")
        self.assertTrue(path.endswith("postgresql.svg"))

        label, path = resolve_icon("go")
        self.assertEqual(label, "Go")
        self.assertTrue(path.endswith("golang.svg"))

        label, path = resolve_icon("node")
        self.assertEqual(label, "Node.js")
        self.assertTrue(path.endswith("nodejs.svg"))

    def test_resolve_icon_custom_label_override(self):
        """Verify query with 'icon:Label' overrides display label."""
        label, path = resolve_icon("golang:GoLang")
        self.assertEqual(label, "GoLang")
        self.assertTrue(path.endswith("golang.svg"))

    def test_resolve_icon_unknown_suggests_match(self):
        """Verify unknown icon name raises ValueError with close match suggestions."""
        with self.assertRaises(ValueError) as ctx:
            resolve_icon("pythn")
        self.assertIn("Did you mean", str(ctx.exception))
        self.assertIn("python", str(ctx.exception))

    def test_parse_icons_arg(self):
        """Verify parsing comma-separated icon queries."""
        icons = parse_icons_arg("go, k8s, docker, aws, python")
        self.assertEqual(len(icons), 5)
        self.assertEqual(icons[0][0], "Go")
        self.assertEqual(icons[1][0], "Kubernetes")

    def test_standards_icon_count_lower_bound(self):
        """Enforce minimum 3 icons standard."""
        too_few = [
            ("Python", "assets/icons/backend/python.svg"),
            ("Go", "assets/icons/backend/golang.svg"),
        ]
        with self.assertRaises(ValueError) as ctx:
            validate_banner_standards("Software Engineer", "Systems • Architecture", too_few)
        self.assertIn(f"at least {MIN_ICONS} icons", str(ctx.exception))

    def test_standards_icon_count_upper_bound(self):
        """Enforce maximum 8 icons standard (safe-zone constraint)."""
        too_many = [
            ("Python", "assets/icons/backend/python.svg"),
            ("Go", "assets/icons/backend/golang.svg"),
            ("Rust", "assets/icons/backend/rust.svg"),
            ("Java", "assets/icons/backend/java.svg"),
            ("Docker", "assets/icons/cloud-devops/docker.svg"),
            ("K8s", "assets/icons/cloud-devops/kubernetes.svg"),
            ("AWS", "assets/icons/cloud-devops/aws.svg"),
            ("Redis", "assets/icons/databases/redis.svg"),
            ("Kafka", "assets/icons/messaging/kafka.svg"),
        ]
        self.assertEqual(len(too_many), 9)
        with self.assertRaises(ValueError) as ctx:
            validate_banner_standards("Software Engineer", "Systems • Architecture", too_many)
        self.assertIn(f"more than {MAX_ICONS} icons", str(ctx.exception))

    def test_standards_title_length_constraint(self):
        """Enforce title length <= 45 characters."""
        valid_icons = [
            ("Python", "assets/icons/backend/python.svg"),
            ("Go", "assets/icons/backend/golang.svg"),
            ("Docker", "assets/icons/cloud-devops/docker.svg"),
        ]
        long_title = "A" * (MAX_TITLE_LENGTH + 1)
        with self.assertRaises(ValueError) as ctx:
            validate_banner_standards(long_title, "Systems • Architecture", valid_icons)
        self.assertIn("Maximum allowed length is 45 characters", str(ctx.exception))

    def test_standards_subtitle_length_constraint(self):
        """Enforce subtitle length <= 80 characters."""
        valid_icons = [
            ("Python", "assets/icons/backend/python.svg"),
            ("Go", "assets/icons/backend/golang.svg"),
            ("Docker", "assets/icons/cloud-devops/docker.svg"),
        ]
        long_sub = "B" * (MAX_SUBTITLE_LENGTH + 1)
        with self.assertRaises(ValueError) as ctx:
            validate_banner_standards("Software Engineer", long_sub, valid_icons)
        self.assertIn("Maximum allowed length is 80 characters", str(ctx.exception))

    def test_build_custom_preset_and_svg(self):
        """Verify generating a custom banner with fine-grained title and icons."""
        preset = build_custom_preset(
            title="Principal Infrastructure Architect",
            subtitle="Cloud Native • Kubernetes • Distributed Systems",
            icons_spec="go, k8s, terraform, aws, python",
        )
        self.assertEqual(preset["title"], "Principal Infrastructure Architect")
        self.assertEqual(len(preset["icons"]), 5)

        svg = build_banner_svg(
            preset_name="custom",
            theme_name="topographical",
            title=preset["title"],
            subtitle=preset["subtitle"],
            icons=preset["icons"],
        )
        self.assertIn("Principal Infrastructure Architect", svg)
        self.assertIn("Cloud Native • Kubernetes", svg)


if __name__ == "__main__":
    unittest.main()
