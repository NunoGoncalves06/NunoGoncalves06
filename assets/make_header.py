"""Draw assets/header.svg, the banner at the top of the profile README.

Usage:  python make_header.py
"""
import pathlib
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).parent / "header.svg"

NAME = "Nuno Gonçalves"
ROLE = "Informatics engineering student at ISEP. CTF player with CHAØS."

GLAZE, INK, TILE, SOFT, YELLOW = "#EEF3FC", "#12307A", "#2B5FD9", "#4A64A8", "#E9B949"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

W, H = 1200, 220


def tiles(x0, size, cols, rows):
    """An azulejo pattern: each tile is four quarter-circles meeting at the centre."""
    out = []
    for r in range(rows):
        for c in range(cols):
            x, y, s = x0 + c * size, r * size, size
            opacity = 0.15 + 0.75 * (c / max(cols - 1, 1))
            out.append(
                f'<g transform="translate({x} {y})" opacity="{opacity:.2f}" fill="none" stroke="{TILE}">'
                f'<rect width="{s}" height="{s}" stroke-width="1"/>'
                f'<path d="M0 {s/2}A{s/2} {s/2} 0 0 0 {s/2} 0M{s/2} 0A{s/2} {s/2} 0 0 0 {s} {s/2}'
                f'M{s} {s/2}A{s/2} {s/2} 0 0 0 {s/2} {s}M{s/2} {s}A{s/2} {s/2} 0 0 0 0 {s/2}" stroke-width="1.5"/>'
                f'<circle cx="{s/2}" cy="{s/2}" r="{s/8}" fill="{YELLOW if (r + c) % 2 else TILE}" stroke="none"/></g>'
            )
    return "\n    ".join(out)


svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">{escape(NAME)}</title>
  <desc id="d">{escape(ROLE)}</desc>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{GLAZE}"/>
    {tiles(760, 55, 8, 4)}
    <text x="56" y="112" font-family="{SERIF}" font-size="68" font-weight="700" fill="{INK}" letter-spacing="-1">{escape(NAME)}</text>
    <text x="58" y="158" font-family="{SANS}" font-size="24" fill="{SOFT}">{escape(ROLE)}</text>
  </g>
</svg>
"""

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(svg, encoding="utf-8")
print(f"wrote {OUT} ({len(svg)} bytes)")
