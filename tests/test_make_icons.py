import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from make_header import contrast  # noqa: E402
from make_icons import ICON_COLOR, build_icon, main  # noqa: E402

NAMES = ("flag", "folder", "terminal", "mail")


def test_icons_contrast_both_themes():
    assert contrast(ICON_COLOR, "#ffffff") >= 3
    assert contrast(ICON_COLOR, "#0d1117") >= 3


def test_icons_are_line_icons():
    for n in NAMES:
        svg = build_icon(n)
        assert 'viewBox="0 0 24 24"' in svg and 'fill="none"' in svg
        assert f'stroke="{ICON_COLOR}"' in svg
        assert "aria-hidden" in svg or "<title" in svg
        assert "—" not in svg and "–" not in svg


def test_main_writes_files(tmp_path):
    assert main(["--out", str(tmp_path)]) == 0
    assert all((tmp_path / f"icon-{n}.svg").exists() for n in NAMES)


def test_icon_colour_comes_from_header_theme():
    from make_header import THEMES
    assert ICON_COLOR == THEMES["light"]["red"] == "#d4153b"
