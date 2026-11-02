"""Generate the profile header SVGs (dark and light) in the style of the portfolio site."""
import argparse
import base64
import functools
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT = HERE / "../portfolio/node_modules/@fontsource/barlow-condensed/files/barlow-condensed-latin-800-normal.woff2"
EDGE_PATHS = (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe")


def find_edge() -> str | None:
    return shutil.which("msedge") or next((p for p in EDGE_PATHS if Path(p).exists()), None)

NAME = "Nuno Gonçalves"
TITLE = "Offensive security"

# bg, title ink, name/body ink, red, cyan (light variants darkened for AA on the light background)
THEMES = {
    "dark": dict(bg="#0a0a0c", ink="#f4f4f6", body="#a8a8b2", red="#ff2a4f", cyan="#28dceb"),
    "light": dict(bg="#f4f4f6", ink="#0a0a0c", body="#3a3a44", red="#d4153b", cyan="#0a8a96"),
}


def light_bg() -> str:
    return THEMES["light"]["bg"]


def light_title() -> str:
    return THEMES["light"]["ink"]


def _lum(hex_color: str) -> float:
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


@functools.cache
def font_b64() -> str:
    return base64.b64encode(FONT.read_bytes()).decode()


def build_svg(theme: str) -> str:
    t = THEMES[theme]
    font = font_b64()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-labelledby="t d">
<title id="t">{NAME}: {TITLE}</title>
<desc id="d">Profile header for {NAME}, {TITLE}.</desc>
<style>
@font-face {{ font-family: "Barlow Condensed"; font-weight: 800; src: url(data:font/woff2;base64,{font}) format("woff2"); }}
.name {{ font: 500 32px "Segoe UI", Helvetica, Arial, sans-serif; fill: {t["body"]}; }}
.title {{ font: 800 130px "Barlow Condensed", Impact, sans-serif; text-transform: uppercase; }}
#r {{ fill: {t["red"]}; transform: translateX(-2px); }}
#c {{ fill: {t["cyan"]}; transform: translateX(2px); }}
#m {{ fill: {t["ink"]}; }}
@media (prefers-reduced-motion: no-preference) {{
  #r {{ animation: tear-a 1.1s steps(1) 1 both; }}
  #c {{ animation: tear-b 1.1s steps(1) 1 both; }}
}}
@keyframes tear-a {{
  0% {{ clip-path: inset(10% 0 70% 0); transform: translateX(-4px); }}
  30% {{ clip-path: inset(30% 0 45% 0); transform: translateX(-4px); }}
  60% {{ clip-path: inset(5% 0 85% 0); transform: translateX(-3px); }}
  100% {{ clip-path: inset(0 0 0 0); transform: translateX(-2px); }}
}}
@keyframes tear-b {{
  0% {{ clip-path: inset(60% 0 15% 0); transform: translateX(4px); }}
  30% {{ clip-path: inset(15% 0 60% 0); transform: translateX(4px); }}
  60% {{ clip-path: inset(70% 0 10% 0); transform: translateX(3px); }}
  100% {{ clip-path: inset(0 0 0 0); transform: translateX(2px); }}
}}
</style>
<rect id="bg" width="1200" height="300" fill="{t["bg"]}"/>
<rect x="0" y="0" width="8" height="300" fill="{t["red"]}"/>
<text x="60" y="105" class="name">{NAME}</text>
<text id="c" x="60" y="220" class="title">{TITLE}</text>
<text id="r" x="60" y="220" class="title">{TITLE}</text>
<text id="m" x="60" y="220" class="title">{TITLE}</text>
</svg>
'''


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", action="store_true", help="also render 2400x600 PNG fallbacks with Edge")
    ap.add_argument("--out", default=str(HERE / "assets"))
    args = ap.parse_args(argv)
    if not FONT.exists():
        print(f"error: font not found at {FONT.resolve()}; run `npm i @fontsource/barlow-condensed` in ../portfolio", file=sys.stderr)
        return 1
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    edge = find_edge() if args.png else None
    if args.png and not edge:
        print("error: Microsoft Edge not found (needed for --png)", file=sys.stderr)
        return 1
    for theme in THEMES:
        svg = out / f"header-{theme}.svg"
        svg.write_text(build_svg(theme), encoding="utf-8")
        if args.png:
            cmd = [edge, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                   "--window-size=1200,300", f"--screenshot={out / f'header-{theme}.png'}", svg.resolve().as_uri(),
                   f"--user-data-dir={tempfile.mkdtemp()}"]
            try:
                ok = subprocess.run(cmd, timeout=60, capture_output=True).returncode == 0
            except subprocess.TimeoutExpired:
                ok = False
            if not ok:
                print(f"error: Edge failed or timed out rendering header-{theme}.png", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
