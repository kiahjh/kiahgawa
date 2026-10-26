#!/usr/bin/env python3
"""Build portable theme files from palette/kiahgawa.json. No dependencies."""

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ANSI = (
    "black", "red", "green", "yellow", "blue", "purple", "cyan", "foreground",
    "muted", "brightRed", "brightGreen", "brightYellow", "brightBlue",
    "brightPurple", "brightCyan", "brightForeground",
)
COLORS = {
    "background", "terminalBackground", "inset", "panel", "raised", "selection",
    "foreground", "brightForeground", "subtle", "muted", "disabled", "border",
    "scrollbar", "black", "red", "orange", "yellow", "green", "cyan", "blue",
    "purple", "keyword", "property", "error", "warning", "brightRed",
    "brightGreen", "brightYellow", "brightBlue", "brightPurple", "brightCyan",
}


def palette():
    p = json.loads((ROOT / "palette/kiahgawa.json").read_text())
    if p.get("name") != "kiahgawa" or set(p) != COLORS | {"name"}:
        raise ValueError("Unexpected palette name or color keys")
    for key in COLORS:
        if not isinstance(p[key], str) or not re.fullmatch(r"#[0-9a-f]{6}", p[key]):
            raise ValueError(f"Invalid RGB color for {key}: {p[key]!r}")
    return p


def mix(a, b, amount):
    return "#" + "".join(
        f"{round(int(a[i:i + 2], 16) * (1 - amount) + int(b[i:i + 2], 16) * amount):02x}"
        for i in (1, 3, 5)
    )


def derived(p):
    return {
        **p,
        "diffAdded": mix(p["background"], p["green"], .14),
        "diffRemoved": mix(p["background"], p["red"], .14),
        "diffAddedLine": mix(p["background"], p["green"], .10),
        "diffRemovedLine": mix(p["background"], p["red"], .10),
        "search": mix(p["background"], p["cyan"], .22),
    }


def opencode(p):
    p = derived(p)
    feedback = {key: {"base": p[color]} for key, color in (
        ("error", "error"), ("warning", "warning"), ("success", "green"), ("info", "blue"),
    )}
    hue = {
        "gray": dict(zip(map(str, range(100, 1000, 100)), (
            p["brightForeground"], p["foreground"], p["subtle"], p["muted"],
            p["selection"], p["raised"], p["panel"], p["background"], p["black"],
        ))),
    }
    for name in ("red", "orange", "yellow", "green", "cyan", "blue", "purple"):
        shades = [mix(p[name], "#ffffff", .25), p[name]]
        shades += [mix(p["black"], p[name], a) for a in (.85, .70, .55, .40, .28, .17, .08)]
        hue[name] = dict(zip(map(str, range(100, 1000, 100)), shades))
    hue.update(accent="$hue.yellow", interactive="$hue.yellow", neutral="$hue.gray")
    return {
        "$schema": "https://opencode.ai/theme.json",
        "base": {
            "categorical": ["yellow", "blue", "green", "purple", "red", "cyan"],
            "text": {
                "base": p["foreground"], "muted": p["muted"],
                "action": {
                    "primary": {
                        "base": "$text.base", "$hovered": p["yellow"],
                        "$focused": p["background"], "$selected": p["brightForeground"],
                        "$disabled": p["disabled"],
                    },
                    "secondary": {"base": "$text.muted", "$hovered": "$text.base"},
                    "destructive": {"base": p["background"], "$disabled": p["disabled"]},
                },
                "formfield": {
                    "base": "$text.base", "$hovered": p["blue"], "$focused": p["blue"],
                    "$pressed": p["blue"], "$selected": p["brightForeground"],
                    "$disabled": p["disabled"],
                },
                "feedback": feedback,
            },
            "background": {
                "base": p["background"],
                "raised": {"base": p["panel"], "high": p["raised"], "max": p["selection"]},
                "action": {
                    "primary": {
                        "base": "transparent", "$hovered": p["raised"],
                        "$focused": p["yellow"], "$selected": p["selection"],
                    },
                    "secondary": {"base": "transparent", "$hovered": p["raised"]},
                    "destructive": {"base": p["red"], "$hovered": p["brightRed"]},
                },
                "formfield": {"base": p["inset"], "$disabled": p["panel"]},
                "feedback": {key: {"base": "$background.base"} for key in feedback},
            },
            "border": {"base": p["border"]},
            "scrollbar": {"base": p["scrollbar"]},
            "diff": {
                "text": {"added": p["green"], "removed": p["red"], "context": p["muted"], "hunkHeader": p["purple"]},
                "background": {"added": p["diffAdded"], "removed": p["diffRemoved"], "context": "$background.base"},
                "highlight": {"added": p["brightGreen"], "removed": p["brightRed"]},
                "lineNumber": {"text": p["muted"], "background": {"added": p["diffAddedLine"], "removed": p["diffRemovedLine"]}},
            },
            "syntax": {
                key: p[color] for key, color in (
                    ("comment", "muted"), ("keyword", "keyword"), ("function", "blue"),
                    ("variable", "foreground"), ("string", "green"), ("number", "purple"),
                    ("type", "cyan"), ("operator", "orange"), ("punctuation", "cyan"),
                )
            },
            "markdown": {
                key: p[color] for key, color in (
                    ("text", "foreground"), ("heading", "yellow"), ("link", "blue"),
                    ("linkText", "cyan"), ("code", "green"), ("blockQuote", "muted"),
                    ("emphasis", "yellow"), ("strong", "brightForeground"),
                    ("horizontalRule", "border"), ("listItem", "yellow"),
                    ("listEnumeration", "yellow"), ("image", "blue"),
                    ("imageText", "cyan"), ("codeBlock", "foreground"),
                )
            },
            "@dialog": {"background": {"base": "$background.raised.base", "action": {"primary": {"$hovered": "$background.raised.high"}}}},
        },
        "dark": {"hue": hue},
    }


def rex(p):
    lines = [
        "# Kiahgawa — generated from palette/kiahgawa.json.",
        "# See the Kiahgawa repository for sources and MIT notices.",
        f"background = {p['terminalBackground']}", f"foreground = {p['foreground']}",
        f"cursor-color = {p['yellow']}", f"cursor-text = {p['terminalBackground']}",
        f"selection-background = {p['selection']}", f"selection-foreground = {p['brightForeground']}",
    ]
    lines += [f"palette = {i}={p[key]}" for i, key in enumerate(ANSI)]
    return "\n".join(lines) + "\n"


def lua(p):
    lines = ["-- Generated by scripts/generate.py; edit palette/kiahgawa.json instead.", "return {"]
    lines += [f'  {key} = "{value}",' for key, value in derived(p).items()]
    lines += ["  ansi = {"] + [f'    "{p[key]}",' for key in ANSI] + ["  },", "}"]
    return "\n".join(lines) + "\n"


def outputs(p):
    return {
        "extras/opencode/kiahgawa.json": json.dumps(opencode(p), indent=2) + "\n",
        "extras/rex/kiahgawa": rex(p),
        "lua/kiahgawa/palette.lua": lua(p),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="regenerate committed assets")
    mode.add_argument("--check", action="store_true", help="check assets (default)")
    args = parser.parse_args()
    failed = False
    for name, expected in outputs(palette()).items():
        path = ROOT / name
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
            print(f"Generated {name}")
        elif not path.exists() or path.read_text() != expected:
            print(f"Out of date: {name}; run python3 scripts/generate.py --write")
            failed = True
        else:
            print(f"OK {name}")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
