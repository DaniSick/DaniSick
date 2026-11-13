"""Shared palette and helpers for the README cards."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = os.path.join(ROOT, "assets")
HERE = os.path.dirname(os.path.abspath(__file__))

THEMES = {
    "light": dict(body="#EEF2FA", head="#C3CEEB", title="#1E2A48", text="#36425E", chip="#DAE2F5", dot="#7C8FC6", accent="#4A68D2"),
    "dark":  dict(body="#131720", head="#232C44", title="#DAE3FB", text="#B2BDD9", chip="#1B2133", dot="#7C8FC6", accent="#8CA6F6"),
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
