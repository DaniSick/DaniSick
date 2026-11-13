"""Stack table with a stats panel beside it -> assets/stack-overview[-dark].svg

Reads icons.json (paths/colors from simple-icons) and stats.json (from stats.py).
"""
import json
import os
from xml.sax.saxutils import escape
from theme import THEMES, HEAD, HERE, svg_open, panel, write

ICONS = json.load(open(os.path.join(HERE, "icons.json")))
# simple-icons has no C# or Dokploy mark: C# gets a plain hexagon (its logo shape), Dokploy a square
ICONS["csharp"] = {"d": "M12 1 21.5 6.5v11L12 23 2.5 17.5v-11z", "hex": "512BD4"}
ICONS["dokploy"] = {"d": "M3 3h18v18H3z", "hex": "3B82F6"}
STATS = json.load(open(os.path.join(HERE, "stats.json")))

ROWS = [
    ("Languages", [("PHP", "php"), ("TypeScript", "typescript"), ("JavaScript", "javascript"), ("Python", "python"), ("C#", "csharp"), ("Dart", "dart")]),
    ("Backend", [("Laravel", "laravel"), ("Node.js", "nodedotjs")]),
    ("Frontend", [("React", "react"), ("Next.js", "nextdotjs"), ("Livewire", "livewire"), ("Tailwind CSS", "tailwindcss")]),
    ("Infra & DevOps", [("Docker", "docker"), ("Linux", "linux"), ("Cloudflare", "cloudflare"), ("GitHub Actions", "githubactions"), ("Dokploy", "dokploy")]),
    ("Databases", [("PostgreSQL", "postgresql"), ("MySQL", "mysql"), ("Redis", "redis")]),
]


def days(n):
    return f"{n} day" if n == 1 else f"{n} days"


GRID = [
    ("current streak", days(STATS["current_streak"])),
    ("longest streak", days(STATS["longest_streak"])),
    ("followers", f'{STATS["followers"]:,}'),
    ("on GitHub since", STATS["since"]),
]

TW, GAP, SW = 1002, 14, 680          # total width, gap, stack panel width
XW = TW - SW - GAP                    # stats panel width
PAD, ROW, CHIP_H, LABEL_W, CW, ICON = 20, 46, 24, 120, 6.7, 12
H = HEAD + len(ROWS) * ROW + 10


def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def stats_panel(C):
    x0, inner = SW + GAP + PAD, XW - 2 * PAD
    out = [
        f'<text x="{x0}" y="{HEAD + 44}" font-size="34" font-weight="700" fill="{C["accent"]}">{STATS["contributions"]:,}</text>',
        f'<text x="{x0}" y="{HEAD + 63}" font-size="12" fill="{C["text"]}">contributions in the last 12 months</text>',
    ]
    # weekly activity bars
    weeks, top, bh = STATS["weeks"], HEAD + 76, 40
    step, peak = inner / len(weeks), max(STATS["weeks"]) or 1
    for k, n in enumerate(weeks):
        h = max(2, round(n / peak * bh, 1))
        fill = C["accent"] if n else C["head"]
        out.append(f'<rect x="{x0 + k * step:.1f}" y="{top + bh - h}" width="{step * 0.7:.1f}" height="{h}" fill="{fill}"/>')
    # 2x2 grid
    gy = top + bh + 12
    out.append(f'<line x1="{x0}" y1="{gy}" x2="{TW - PAD}" y2="{gy}" stroke="{C["head"]}"/>')
    for k, (label, value) in enumerate(GRID):
        cx, cy = x0 + (k % 2) * inner / 2, gy + 30 + (k // 2) * 46
        out.append(f'<text x="{cx}" y="{cy}" font-size="17" font-weight="700" fill="{C["title"]}">{escape(value)}</text>')
        out.append(f'<text x="{cx}" y="{cy + 16}" font-size="11" fill="{C["text"]}">{escape(label)}</text>')
    assert gy + 30 + 46 + 16 <= H - 8, "stats panel overflows"
    return out


for theme, C in THEMES.items():
    out = [svg_open(TW, H), *panel(C, 0, SW, H, "STACK", PAD), *panel(C, SW + GAP, XW, H, "STATS", PAD)]
    for i, (label, items) in enumerate(ROWS):
        top = HEAD + 5 + i * ROW
        mid = top + ROW / 2
        if i:
            out.append(f'<line x1="{PAD}" y1="{top}" x2="{SW - PAD}" y2="{top}" stroke="{C["head"]}"/>')
        # stack row
        out.append(f'<text x="{PAD}" y="{mid + 5}" font-size="13" font-weight="600" fill="{C["title"]}">{escape(label)}</text>')
        x = PAD + LABEL_W
        for name, slug in items:
            ic = ICONS[slug]
            color = C["title"] if theme == "dark" and lum(ic["hex"]) < 0.15 else "#" + ic["hex"]
            w = round(9 + ICON + 6 + len(name) * CW + 9)
            out.append(f'<rect x="{x}" y="{mid - CHIP_H / 2}" width="{w}" height="{CHIP_H}" fill="{C["chip"]}" stroke="{C["head"]}"/>')
            out.append(f'<path transform="translate({x + 9},{mid - ICON / 2}) scale({ICON / 24:.4f})" fill="{color}" d="{ic["d"]}"/>')
            out.append(f'<text x="{x + 9 + ICON + 6}" y="{mid + 4}" font-size="12" fill="{C["text"]}">{escape(name)}</text>')
            x += w + 6
        assert x - 6 <= SW - PAD, f"row '{label}' overflows the stack panel"
    out += stats_panel(C)
    out.append("</svg>")
    write("stack-overview", theme, out)
