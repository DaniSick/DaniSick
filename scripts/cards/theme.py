"""Shared palette and helpers for the README cards."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = os.path.join(ROOT, "assets")
HERE = os.path.dirname(os.path.abspath(__file__))

THEMES = {
    "light": dict(body="#F1EEF9", head="#CDC6E8", title="#2E2A47", text="#3F3A5C", chip="#E2DCF3", dot="#8B80B8"),
    "dark":  dict(body="#17151F", head="#2C2840", title="#E2DCF7", text="#BDB6D6", chip="#221F30", dot="#8B80B8"),
}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
HEAD = 44


def svg_open(w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">'


def panel(C, x, w, h, title, pad=24):
    """Bordered card with a header band, positioned at x."""
    return [
        f'<rect x="{x + 0.5}" y="0.5" width="{w - 1}" height="{h - 1}" fill="{C["body"]}" stroke="{C["head"]}"/>',
        f'<rect x="{x}" width="{w}" height="{HEAD}" fill="{C["head"]}"/>',
        f'<text x="{x + pad}" y="28" font-size="13" font-weight="700" letter-spacing="1.4" fill="{C["title"]}">{title}</text>',
    ]


def write(name, theme, lines):
    suffix = "-dark" if theme == "dark" else ""
    path = os.path.join(ASSETS, f"{name}{suffix}.svg")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path
