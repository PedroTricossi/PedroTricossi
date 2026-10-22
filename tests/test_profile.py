"""Checks for the profile README and its generated pixel-art assets.

Run with: python3 -m unittest discover -s tests
"""

import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build_assets  # noqa: E402

ASSETS = ROOT / "assets"
README = ROOT / "README.md"
SVG_NS = "{http://www.w3.org/2000/svg}"


def svg_files():
    return sorted(ASSETS.glob("*.svg"))


class FontTest(unittest.TestCase):
    def test_every_glyph_is_seven_rows_of_equal_width(self):
        for char, rows in build_assets.FONT.items():
            with self.subTest(char=char):
                self.assertEqual(len(rows), 7)
                self.assertEqual(len({len(r) for r in rows}), 1)
                self.assertTrue(set("".join(rows)) <= {".", "#"})

    def test_all_text_used_in_assets_is_drawable(self):
        for text in build_assets.ALL_TEXT:
            with self.subTest(text=text):
                missing = {c for c in text if c not in build_assets.FONT}
                self.assertEqual(missing, set())

    def test_text_width_matches_glyphs_plus_spacing(self):
        # "AB" = 5 + 1 (gap) + 5 pixels wide.
        self.assertEqual(build_assets.text_width("AB", scale=1), 11)
        self.assertEqual(build_assets.text_width("AB", scale=3), 33)


class SpriteTest(unittest.TestCase):
    def test_sprites_are_rectangular_and_use_known_keys(self):
        for name, (rows, colors) in build_assets.SPRITES.items():
            with self.subTest(sprite=name):
                self.assertEqual(len({len(r) for r in rows}), 1)
                keys = set("".join(rows)) - {"."}
                self.assertTrue(keys <= set(colors), keys - set(colors))


class GeneratedAssetsTest(unittest.TestCase):
    def test_committed_assets_match_the_generator(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_assets.build(Path(tmp))
            fresh = {p.name: p.read_text() for p in Path(tmp).glob("*.svg")}
        committed = {p.name: p.read_text() for p in svg_files()}
        self.assertEqual(sorted(fresh), sorted(committed),
                         "run: python3 tools/build_assets.py")
        for name, text in fresh.items():
            with self.subTest(svg=name):
                self.assertEqual(committed[name], text,
                                 "stale asset, run: python3 tools/build_assets.py")


class SvgTest(unittest.TestCase):
    def test_svgs_exist(self):
        self.assertGreater(len(svg_files()), 0)

    def test_each_svg_parses_and_has_viewbox_and_title(self):
        for path in svg_files():
            with self.subTest(svg=path.name):
                root = ET.parse(path).getroot()
                self.assertEqual(root.tag, SVG_NS + "svg")
                self.assertIn("viewBox", root.attrib)
                self.assertEqual(root.get("role"), "img")
                title = root.find(SVG_NS + "title")
                self.assertIsNotNone(title)
                self.assertTrue(title.text and title.text.strip())

    def test_no_scripts_or_external_references(self):
        banned = re.compile(r"<script|<foreignObject|@import|url\(\s*['\"]?http"
                            r"|href=\"http|xlink:href=\"http", re.I)
        for path in svg_files():
            with self.subTest(svg=path.name):
                self.assertIsNone(banned.search(path.read_text()))

    def test_only_palette_colors_are_used(self):
        palette = {c.lower() for c in build_assets.PALETTE.values()}
        for path in svg_files():
            with self.subTest(svg=path.name):
                used = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", path.read_text())}
                self.assertTrue(used <= palette, used - palette)

    def test_animated_svgs_respect_reduced_motion(self):
        for path in svg_files():
            text = path.read_text()
            if "animation" in text:
                with self.subTest(svg=path.name):
                    self.assertIn("prefers-reduced-motion", text)


class ReadmeTest(unittest.TestCase):
    def setUp(self):
        self.text = README.read_text()

    def test_every_local_image_exists_and_has_alt_text(self):
        imgs = re.findall(r"<img\b[^>]*>", self.text)
        self.assertGreater(len(imgs), 0)
        for tag in imgs:
            with self.subTest(img=tag):
                src = re.search(r'src="([^"]+)"', tag).group(1)
                alt = re.search(r'alt="([^"]*)"', tag)
                self.assertFalse(src.startswith("http"), "keep images in the repo")
                self.assertTrue((ROOT / src).is_file(), src)
                self.assertTrue(alt and alt.group(1).strip(), "missing alt text")

    def test_every_generated_asset_is_used(self):
        for path in svg_files():
            with self.subTest(svg=path.name):
                self.assertIn(f"assets/{path.name}", self.text)

    def test_contact_links(self):
        for link in ("mailto:pedrodtricossi@gmail.com",
                     "https://www.linkedin.com/in/pedro-tricossi-90a297168/",
                     "https://orcid.org/0009-0002-4751-5805"):
            with self.subTest(link=link):
                self.assertIn(link, self.text)

    def test_research_topics(self):
        for topic in ("Post-quantum cryptography", "Applied cryptography",
                      "Attribute-based encryption", "V2X"):
            with self.subTest(topic=topic):
                self.assertIn(topic, self.text)


if __name__ == "__main__":
    unittest.main()
