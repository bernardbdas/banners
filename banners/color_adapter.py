"""
Color Adapter Module.
Handles dynamic color modifications for SVG icons between Dark and Light modes:
- In Dark Mode: Black / near-black / un-filled monochromatic elements are converted to white (#FFFFFF).
- In Light Mode: Pure white / un-filled monochromatic elements are converted to dark slate (#0F172A).
- Multi-colored icons with internal white/black layered elements (e.g., C++, React, ArgoCD pupils)
  preserve their internal contrast.
"""

import re

# Common black hex / keyword variants
BLACK_VALUES: set[str] = {
    "#000",
    "#000000",
    "black",
    "rgb(0,0,0)",
    "rgb(0, 0, 0)",
    "#010101",
    "#111",
    "#111111",
    "#181717",
    "#0f172a",
    "#161f34",
}

# Common white hex / keyword variants
WHITE_VALUES: set[str] = {"#fff", "#ffffff", "white", "rgb(255,255,255)", "rgb(255, 255, 255)"}


class ColorAdapter:
    """Adapts SVG icon colors to maintain optimal contrast across themes."""

    @classmethod
    def adapt(cls, inner_svg: str, theme: str, filename: str = "") -> str:
        """Main entry point to adapt SVG content for the requested theme."""
        if theme == "dark":
            return cls.adapt_for_dark_mode(inner_svg, filename)
        elif theme == "light":
            return cls.adapt_for_light_mode(inner_svg, filename)
        return inner_svg

    @classmethod
    def adapt_for_dark_mode(cls, inner_svg: str, filename: str = "") -> str:
        """
        Modifies black/dark logo elements to white for dark mode rendering.
        Ensures high visibility against dark card backgrounds (#1E293B / #0F172A).
        """
        lower_name = filename.lower()

        # Special Case: Next.js badge inversion
        if "nextjs" in lower_name:
            return cls._adapt_nextjs_dark(inner_svg)

        # 1. Convert currentColor to white
        inner_svg = re.sub(
            r"fill=[\"\']currentColor[\"\']", 'fill="#FFFFFF"', inner_svg, flags=re.IGNORECASE
        )
        inner_svg = re.sub(
            r"stroke=[\"\']currentColor[\"\']", 'stroke="#FFFFFF"', inner_svg, flags=re.IGNORECASE
        )

        # 2. Known standalone text / monochrome elements (like scikit-learn text)
        if "scikitlearn" in lower_name:
            inner_svg = re.sub(r"fill=[\"\']#010101[\"\']", 'fill="#FFFFFF"', inner_svg)
            return inner_svg

        # 3. Monochromatic icons or icons with unfilled paths (OpenAI, Ollama, Apple, Express, Flask)
        if cls._is_monochrome_or_unfilled(inner_svg):
            inner_svg = cls._convert_all_black_to_white(inner_svg)
            inner_svg = cls._fill_unfilled_shapes(inner_svg, "#FFFFFF")
        else:
            # Multi-colored icons: only convert explicit black fills that are not masked
            # (e.g. black outlines or text)
            inner_svg = cls._convert_standalone_black(inner_svg)

        return inner_svg

    @classmethod
    def adapt_for_light_mode(cls, inner_svg: str, filename: str = "") -> str:
        """
        Modifies white logo elements to dark slate for light mode rendering.
        Ensures high visibility against light card backgrounds (#FFFFFF / #F8FAFC).
        """
        lower_name = filename.lower()

        # Special Case: Next.js badge in light mode (classic dark circle with white N)
        if "nextjs" in lower_name:
            return cls._adapt_nextjs_light(inner_svg)

        # 1. Convert currentColor to dark slate
        inner_svg = re.sub(
            r"fill=[\"\']currentColor[\"\']", 'fill="#0F172A"', inner_svg, flags=re.IGNORECASE
        )
        inner_svg = re.sub(
            r"stroke=[\"\']currentColor[\"\']", 'stroke="#0F172A"', inner_svg, flags=re.IGNORECASE
        )

        # 2. For shapes with no fill (default black in SVG), ensure crisp rendering
        if cls._has_unfilled_shapes(inner_svg):
            inner_svg = cls._fill_unfilled_shapes(inner_svg, "#0F172A")

        # 3. For pure monochromatic white icons (if any), convert white to dark slate
        if cls._is_pure_white_icon(inner_svg):
            inner_svg = cls._convert_all_white_to_dark(inner_svg, "#0F172A")

        return inner_svg

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    @classmethod
    def _is_monochrome_or_unfilled(cls, svg: str) -> bool:
        """Detects if an icon is primarily monochrome or lacks explicit fills."""
        # Find all distinct fill and stroke colors
        fills = set(re.findall(r"fill=[\"\']([^\"\']+)[\"\']", svg, re.IGNORECASE))
        strokes = set(re.findall(r"stroke=[\"\']([^\"\']+)[\"\']", svg, re.IGNORECASE))
        colors = fills.union(strokes)

        # Remove url(#...) gradients/patterns and 'none'
        solid_colors = {c for c in colors if not c.startswith("url(") and c.lower() != "none"}

        if not solid_colors:
            # No solid colors specified -> unfilled shapes (defaults to black)
            return True

        # Check if all solid colors are black variants
        return all(c.lower() in BLACK_VALUES or c.lower() == "currentcolor" for c in solid_colors)

    @classmethod
    def _is_pure_white_icon(cls, svg: str) -> bool:
        """Detects if an icon only contains white fills on transparent canvas."""
        fills = set(re.findall(r"fill=[\"\']([^\"\']+)[\"\']", svg, re.IGNORECASE))
        solid_colors = {c for c in fills if not c.startswith("url(") and c.lower() != "none"}
        if not solid_colors:
            return False
        return all(c.lower() in WHITE_VALUES for c in solid_colors)

    @classmethod
    def _has_unfilled_shapes(cls, svg: str) -> bool:
        """Checks if SVG contains shape tags with no fill attribute."""
        pattern = r"<(path|polygon|polyline|circle|rect|ellipse)\b(?![^>]*\bfill=)[^>]*>"
        return bool(re.search(pattern, svg, re.IGNORECASE))

    @classmethod
    def _fill_unfilled_shapes(cls, svg: str, target_color: str) -> str:
        """Injects fill attribute into shape tags that lack fill and style."""

        def repl(match: re.Match) -> str:
            tag = match.group(0)
            if "fill=" not in tag and "style=" not in tag:
                if tag.endswith("/>"):
                    return tag[:-2] + f' fill="{target_color}"/>'
                elif tag.endswith(">"):
                    return tag[:-1] + f' fill="{target_color}">'
            return tag

        return re.sub(
            r"<(path|polygon|polyline|circle|rect|ellipse)\b[^>]*>", repl, svg, flags=re.IGNORECASE
        )

    @classmethod
    def _convert_all_black_to_white(cls, svg: str) -> str:
        """Converts all black fills and strokes to white."""
        pattern = r"(fill|stroke)=[\"\'](?:#000000|#000|black|rgb\(0,\s*0,\s*0\)|#010101|#111111|#111|#181717)[\"\']"

        def repl(m: re.Match) -> str:
            attr = m.group(1)
            return f'{attr}="#FFFFFF"'

        return re.sub(pattern, repl, svg, flags=re.IGNORECASE)

    @classmethod
    def _convert_all_white_to_dark(cls, svg: str, dark_color: str = "#0F172A") -> str:
        """Converts all white fills and strokes to dark slate."""
        pattern = r"(fill|stroke)=[\"\'](?:#ffffff|#fff|white|rgb\(255,\s*255,\s*255\))[\"\']"

        def repl(m: re.Match) -> str:
            attr = m.group(1)
            return f'{attr}="{dark_color}"'

        return re.sub(pattern, repl, svg, flags=re.IGNORECASE)

    @classmethod
    def _convert_standalone_black(cls, svg: str) -> str:
        """Converts standalone black elements while preserving masked/layered details."""
        # Convert explicit fill="#000" or fill="black"
        pattern = r"fill=[\"\'](?:#000000|#000|black|#010101|#111111)[\"\']"
        return re.sub(pattern, 'fill="#FFFFFF"', svg, flags=re.IGNORECASE)

    @classmethod
    def _adapt_nextjs_dark(cls, svg: str) -> str:
        """Next.js dark mode: white background circle with crisp dark N."""
        # Change circle fill to white
        svg = re.sub(
            r"<circle\s+cx=[\"\']64[\"\']\s+cy=[\"\']64[\"\']\s+r=[\"\']64[\"\'][^>]*\/?>",
            '<circle cx="64" cy="64" r="64" fill="#FFFFFF"/>',
            svg,
            flags=re.IGNORECASE,
        )
        # Invert the N gradient stop colors to black
        svg = re.sub(
            r"stop-color=[\"\']#fff[\"\']", 'stop-color="#000000"', svg, flags=re.IGNORECASE
        )
        svg = re.sub(
            r"stop-color=[\"\']white[\"\']", 'stop-color="#000000"', svg, flags=re.IGNORECASE
        )
        return svg

    @classmethod
    def _adapt_nextjs_light(cls, svg: str) -> str:
        """Next.js light mode: classic dark circle with white N."""
        # Ensure circle has explicit dark fill
        svg = re.sub(
            r"<circle\s+cx=[\"\']64[\"\']\s+cy=[\"\']64[\"\']\s+r=[\"\']64[\"\'][^>]*\/?>",
            '<circle cx="64" cy="64" r="64" fill="#000000"/>',
            svg,
            flags=re.IGNORECASE,
        )
        return svg
