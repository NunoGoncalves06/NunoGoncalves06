"""Draw assets/header.svg, the banner at the top of the profile README: a terminal
window in the same green and black as the metrics card further down the page.

Usage:  python make_header.py
"""
import pathlib
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).parent / "header.svg"

NAME = "Nuno Gonçalves"
ROLE = "Informatics engineering student at ISEP. CTF player with CHAØS."

BLACK, BAR, BORDER, DIM, GREEN, BRIGHT = "#000000", "#04261a", "#1f7a4d", "#1f9d5c", "#35d07f", "#7dffb0"
MONO = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, 'Courier New', monospace"

W, H, BAR_H = 1200, 240, 40

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">{escape(NAME)}</title>
  <desc id="d">{escape(ROLE)}</desc>
  <clipPath id="frame"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>
  <g clip-path="url(#frame)" font-family="{MONO}">
    <rect width="{W}" height="{H}" fill="{BLACK}"/>
    <rect width="{W}" height="{BAR_H}" fill="{BAR}"/>
    <rect y="{BAR_H}" width="{W}" height="1" fill="#0f4a30"/>
    <circle cx="28" cy="{BAR_H / 2}" r="7" fill="#ff5f56"/>
    <circle cx="52" cy="{BAR_H / 2}" r="7" fill="#ffbd2e"/>
    <circle cx="76" cy="{BAR_H / 2}" r="7" fill="#27c93f"/>
    <text x="102" y="{BAR_H / 2 + 6}" font-size="18" fill="{GREEN}">nuno@kali ~</text>
    <text x="40" y="88" font-size="20" fill="{DIM}">nuno@kali:~$ whoami</text>
    <text x="38" y="158" font-size="64" font-weight="700" fill="{BRIGHT}" letter-spacing="-1">{escape(NAME)}</text>
    <text x="40" y="204" font-size="22" fill="{GREEN}">{escape(ROLE)}</text>
  </g>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{BORDER}" stroke-width="2"/>
</svg>
"""

OUT.write_text(svg, encoding="utf-8")
print(f"wrote {OUT} ({len(svg)} bytes)")
