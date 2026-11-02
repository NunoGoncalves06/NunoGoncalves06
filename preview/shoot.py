"""Screenshot light/dark previews at 1440 and 375 px with headless Edge, and report horizontal overflow."""
import re
import subprocess
import sys
import tempfile

from PIL import Image
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from make_header import find_edge  # noqa: E402

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots"
# Edge headless has a ~492 px minimum layout width, so each page is shown in an iframe of the exact width.
# srcdoc iframes share the parent origin, so the parent can read the framed document's scrollWidth.
HARNESS = """<!doctype html><meta charset=utf-8><body style="margin:0;background:#888">
<iframe id=f style="border:0;display:block;width:%dpx;height:100px" srcdoc="%s"></iframe>
<script>f.onload=()=>{const d=f.contentDocument.documentElement;f.style.height=d.scrollHeight+'px';
document.title='SW='+d.scrollWidth+';IW='+f.contentWindow.innerWidth}</script>"""


def harness(theme, width):
    page = (HERE / f"{theme}.html").read_text(encoding="utf-8").replace("&", "&amp;").replace('"', "&quot;")
    path = HERE / f"_h-{theme}-{width}.html"
    path.write_text(HARNESS % (width, page), encoding="utf-8")
    return path


def edge(*args):
    return subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={PROFILE}", *args],
                          capture_output=True, text=True, encoding="utf-8", timeout=60)


def overflow(h, width):
    """Return (scrollWidth, innerWidth) of the framed page."""
    out = edge(f"--window-size={width},4000", "--virtual-time-budget=5000", "--dump-dom", h.as_uri()).stdout
    m = re.search(r"<title>SW=(\d+);IW=(\d+)</title>", out)
    return (int(m[1]), int(m[2])) if m else None


if __name__ == "__main__":
    EDGE = find_edge()
    if not EDGE:
        sys.exit("Edge not found")
    SHOTS.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as PROFILE:
        for theme in ("light", "dark"):
            for width in (1440, 375):
                path = SHOTS / f"{theme}-{width}.png"
                h = harness(theme, width)
                edge(f"--screenshot={path}", f"--window-size={width},4000", "--virtual-time-budget=8000", h.as_uri())
                sw = overflow(h, width)
                h.unlink()
                im = Image.open(path).convert("RGB")  # crop the grey harness background below the iframe
                y = next((y for y in range(im.height - 1, 0, -1) if im.getpixel((0, y)) != (136, 136, 136)), im.height - 1)
                im.crop((0, 0, im.width, y + 1)).save(path)
                print(path.name, "exists" if path.exists() else "MISSING", "scrollWidth/innerWidth:", sw,
                      "OK" if sw and sw[0] <= sw[1] else "OVERFLOW?")
