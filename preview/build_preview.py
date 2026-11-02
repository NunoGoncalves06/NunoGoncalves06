"""Render README.md with GitHub's markdown API and wrap it in forced light and dark pages.

Read-only: one POST to the markdown renderer. Usage: python preview/build_preview.py
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

CSS = """
body{margin:0;background:%(bg)s;color:%(fg)s;font:16px/1.5 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif}
.markdown-body{box-sizing:border-box;max-width:1012px;margin:0 auto;padding:45px}
@media(max-width:767px){.markdown-body{padding:15px}}
a{color:%(link)s;text-decoration:none}a:hover{text-decoration:underline}
img{max-width:100%%;height:auto}
h2{padding-bottom:.3em;border-bottom:1px solid %(rule)s;font-size:1.5em;margin:24px 0 16px}
h3{font-size:1.25em;margin:24px 0 16px}
p,ul{margin:0 0 16px}ul{padding-left:2em}
code{background:%(code)s;padding:.2em .4em;border-radius:6px;font-size:85%%}
"""
THEMES = {
    "light": dict(bg="#ffffff", fg="#1f2328", link="#0969da", rule="#d1d9e0", code="#818b981f", scheme="light"),
    "dark": dict(bg="#0d1117", fg="#f0f6fc", link="#4493f8", rule="#3d444d", code="#656c7633", scheme="dark"),
}
PICTURE = re.compile(r"<picture>.*?</picture>", re.S)


def preview_only(body: str) -> str:
    """Point asset paths up one folder and open every <details>; the README itself is never touched."""
    body = re.sub(r"""\b(src|srcset)=(["'])assets/""", r"\1=\2../assets/", body)
    return re.sub(r"<details(?![^>]*\bopen\b)", "<details open", body)


def render(readme: Path) -> str:
    r = subprocess.run(
        ["gh", "api", "markdown", "-f", "mode=gfm", "-f", "context=NunoGoncalves06/NunoGoncalves06", "-F", f"text=@{readme}"],
        capture_output=True, text=True, encoding="utf-8", timeout=60, check=True)
    return r.stdout


def build() -> None:
    html = render(ROOT / "README.md")
    alt = re.search(r'alt="([^"]*)"', PICTURE.search(html).group(0)).group(1)
    for name, t in THEMES.items():
        svg = (ROOT / "assets" / f"header-{name}.svg").read_text(encoding="utf-8")
        # An inline <svg> cannot reuse the <picture> alt text, so wrap it with role/aria-label.
        header = f'<div role="img" aria-label="{alt}" style="width:100%">{svg}</div>'
        body = PICTURE.sub(lambda _m: header, html, count=1)
        body = preview_only(body)
        page = (f'<!doctype html><html lang="en" data-theme="{name}"><head><meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<meta name="color-scheme" content="{t["scheme"]}"><title>Preview {name}</title>'
                f'<style>:root{{color-scheme:{t["scheme"]}}}{CSS % t}'
                f'div[role=img]>svg{{display:block;width:100%;height:auto}}</style></head>'
                f'<body><article class="markdown-body">{body}</article></body></html>')
        (OUT / f"{name}.html").write_text(page, encoding="utf-8")
        print("wrote", OUT / f"{name}.html")


if __name__ == "__main__":
    build()
