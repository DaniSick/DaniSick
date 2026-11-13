"""Full-width About card -> assets/about-card[-dark].svg"""
import textwrap
from xml.sax.saxutils import escape
from theme import THEMES, HEAD, svg_open, panel, write

HEADLINE = ("I build and maintain complete software systems — backend, APIs, infrastructure and delivery — "
            "with correctness, maintainability and security as the baseline, not the goal.")
PARA = ("Most of my work is multi-tenant SaaS: products where data isolation, authorization and predictable "
        "performance are requirements from day one. I take them from the first data model to production, "
        "and keep them running there.")
BOLD = "multi-tenant SaaS"
W, PAD = 1002, 24

for theme, C in THEMES.items():
    hl, pl = textwrap.wrap(HEADLINE, 88), textwrap.wrap(PARA, 115)
    assert sum(BOLD in l for l in pl) == 1, "bold phrase split across lines"
    body, y = [], HEAD + PAD + 22
    for l in hl:
        body.append(f'<text x="{PAD}" y="{y}" font-size="19" font-weight="600" fill="{C["title"]}">{escape(l)}</text>')
        y += 28
    y += 14
    for l in pl:
        e = escape(l).replace(BOLD, f'<tspan font-weight="700" fill="{C["title"]}">{BOLD}</tspan>')
        body.append(f'<text x="{PAD}" y="{y}" font-size="15" fill="{C["text"]}">{e}</text>')
        y += 24
    H = y - 24 + PAD + 6
    write("about-card", theme, [svg_open(W, H), *panel(C, 0, W, H, "ABOUT", PAD), *body, "</svg>"])
