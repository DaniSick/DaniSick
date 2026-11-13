"""Four focus-area cards in a row -> assets/focus-cards[-dark].svg"""
import textwrap
from xml.sax.saxutils import escape
from theme import THEMES, HEAD, svg_open, panel, write

CARDS = [
    ("BACKEND", ["REST APIs & integrations", "Queues & background jobs", "Query performance"]),
    ("ARCHITECTURE", ["Domain modelling", "Clear module boundaries", "Contracts that survive the next feature"]),
    ("INFRASTRUCTURE", ["Docker & reproducible builds", "CI/CD pipelines", "Monitored production deploys"]),
    ("SECURITY", ["Authorization on every state change", "Input validated at every boundary", "Tenant isolation by default"]),
]
W, GAP, ITEM, LINE, WRAP = 240, 14, 10, 19, 27


def layout(items):
    rows, y = [], HEAD + 30
    for it in items:
        lines = textwrap.wrap(it, WRAP)
        rows.append((y, lines))
        y += len(lines) * LINE + ITEM
    return rows, y - ITEM - LINE + 26


laid = [layout(items) for _, items in CARDS]
H = max(h for _, h in laid)
TW = W * 4 + GAP * 3
for theme, C in THEMES.items():
    out = [svg_open(TW, H)]
    for i, ((title, _), (rows, _)) in enumerate(zip(CARDS, laid)):
        x = i * (W + GAP)
        out += panel(C, x, W, H, title, 18)
        for y, lines in rows:
            out.append(f'<rect x="{x + 18}" y="{y - 8}" width="5" height="5" fill="{C["dot"]}"/>')
            for k, ln in enumerate(lines):
                out.append(f'<text x="{x + 32}" y="{y + k * LINE}" font-size="14" fill="{C["text"]}">{escape(ln)}</text>')
    out.append("</svg>")
    write("focus-cards", theme, out)
