import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import generate


def luminance(color):
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return sum(weight * (c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4)
               for weight, c in zip((.2126, .7152, .0722), channels))


def contrast(a, b):
    low, high = sorted((luminance(a), luminance(b)))
    return (high + .05) / (low + .05)


class Themes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = generate.palette()
        cls.theme = json.loads((ROOT / "extras/opencode/kiahgawa.json").read_text())

    def test_generated_files_are_current(self):
        for name, expected in generate.outputs(self.p).items():
            with self.subTest(name=name):
                self.assertEqual((ROOT / name).read_text(), expected)

    def test_opencode_token_tree_is_complete(self):
        base = self.theme["base"]
        self.assertTrue(base["categorical"])
        for group in ("text", "background"):
            self.assertIn("base", base[group])
            for variant in ("primary", "secondary", "destructive"):
                self.assertIn("base", base[group]["action"][variant])
            self.assertIn("base", base[group]["formfield"])
            for state in ("error", "warning", "success", "info"):
                self.assertIn("base", base[group]["feedback"][state])
        self.assertEqual(set(base["background"]["raised"]), {"base", "high", "max"})
        self.assertEqual(set(base["syntax"]), {
            "comment", "keyword", "function", "variable", "string", "number", "type", "operator", "punctuation",
        })
        self.assertEqual(set(base["markdown"]), {
            "text", "heading", "link", "linkText", "code", "blockQuote", "emphasis", "strong",
            "horizontalRule", "listItem", "listEnumeration", "image", "imageText", "codeBlock",
        })
        for name in ("gray", "red", "orange", "yellow", "green", "cyan", "blue", "purple"):
            self.assertEqual(set(self.theme["dark"]["hue"][name]), set(map(str, range(100, 1000, 100))))
        for alias in ("accent", "interactive", "neutral"):
            self.assertIn(alias, self.theme["dark"]["hue"])

    def test_opencode_references_resolve_without_cycles(self):
        root = {**self.theme["base"], **self.theme["dark"]}

        def check(value, seen=()):
            if isinstance(value, str) and value.startswith("$"):
                self.assertNotIn(value, seen, f"Cyclic reference: {value}")
                target = root
                for segment in value[1:].split("."):
                    self.assertIsInstance(target, dict)
                    self.assertIn(segment, target, f"Unresolved reference: {value}")
                    target = target[segment]
                check(target, (*seen, value))
            elif isinstance(value, dict):
                for item in value.values():
                    check(item, seen)
            elif isinstance(value, list):
                for item in value:
                    check(item, seen)

        check(root)

    def test_rex_and_lua_share_the_entire_ansi_palette(self):
        rex = (ROOT / "extras/rex/kiahgawa").read_text()
        actual = {int(i): color for i, color in re.findall(r"^palette = (\d+)=(#[0-9a-f]{6})$", rex, re.M)}
        self.assertEqual(actual, {i: self.p[key] for i, key in enumerate(generate.ANSI)})
        lua = (ROOT / "lua/kiahgawa/palette.lua").read_text()
        ansi = re.search(r"  ansi = \{(.*?)\n  \},", lua, re.S).group(1)
        self.assertEqual(re.findall(r'"(#[0-9a-f]{6})"', ansi), list(actual.values()))
        for key, value in generate.derived(self.p).items():
            self.assertIn(f'{key} = "{value}"', lua)

    def test_important_text_has_readable_contrast(self):
        for surface in ("background", "inset", "panel", "raised", "selection", "terminalBackground"):
            with self.subTest(surface=surface):
                self.assertGreaterEqual(contrast(self.p["foreground"], self.p[surface]), 7)
                self.assertGreaterEqual(contrast(self.p["muted"], self.p[surface]), 4.5)
        for token in self.theme["base"]["syntax"].values():
            self.assertGreaterEqual(contrast(token, self.p["panel"]), 4.5)
        self.assertGreaterEqual(contrast(self.p["border"], self.p["background"]), 3)
        self.assertGreaterEqual(contrast(self.p["background"], self.p["yellow"]), 7)

    def test_dragon_surfaces_are_preserved(self):
        self.assertEqual(self.p["background"], "#181616")
        self.assertEqual(self.p["terminalBackground"], "#141313")
        self.assertEqual(self.theme["base"]["background"]["raised"], {
            "base": self.p["panel"], "high": self.p["raised"], "max": self.p["selection"],
        })


if __name__ == "__main__":
    unittest.main()
