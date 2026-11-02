"""Generate the section line icons (24x24, one red stroke that works on both GitHub themes)."""
import argparse
from pathlib import Path

from make_header import THEMES

HERE = Path(__file__).resolve().parent
ICON_COLOR = THEMES["light"]["red"]
PATHS = {
    "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    "folder": '<path d="M3 7h6l2 2h10v10H3z"/>',
    "terminal": '<path d="M4 6l5 6-5 6M12 18h8"/>',
    "mail": '<rect x="3" y="6" width="18" height="12" rx="1"/><path d="M3 7l9 6 9-6"/>',
}


def build_icon(name: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" '
            f'stroke="{ICON_COLOR}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{PATHS[name]}</svg>\n')


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "assets"))
    out = Path(ap.parse_args(argv).out)
    out.mkdir(parents=True, exist_ok=True)
    for name in PATHS:
        (out / f"icon-{name}.svg").write_text(build_icon(name), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
