import re
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from make_header import build_svg, contrast, light_bg, light_title, main  # noqa: E402


PAGE = {"dark": "#0d1117", "light": "#ffffff"}


def test_both_variants_embed_the_font_and_title():
    for theme in ("dark", "light"):
        svg = build_svg(theme)
        assert "@font-face" in svg and "base64," in svg
        assert "Offensive security" in svg and "Nuno Gonçalves" in svg
        assert "<title" in svg and "<desc" in svg
        assert "Informatics Engineering" not in svg
        assert "—" not in svg and "–" not in svg


def test_header_is_thin():
    for theme in PAGE:
        assert 'viewBox="0 0 800 150"' in build_svg(theme)


def test_header_text_readable_on_phone():
    for theme in PAGE:
        svg = build_svg(theme)
        sizes = [int(n) for n in re.findall(r"font(?:-size)?:[^;}]*?(\d+)px", svg)]
        assert sizes and min(sizes) >= 28


def test_header_has_no_panel_background():
    for theme in PAGE:
        assert '<rect width="800" height="150"' not in build_svg(theme)
        assert 'id="bg"' not in build_svg(theme)


def test_text_colours_pass_aa_on_page_background():
    from make_header import THEMES
    for theme, page in PAGE.items():
        assert light_bg() == "#ffffff"
        for key in ("ink", "body"):
            assert contrast(THEMES[theme][key], page) >= 4.5, (theme, key)
    assert contrast(light_title(), "#ffffff") >= 4.5
    assert 'fill="#d4153b"' in build_svg("light") and "#ff2a4f" in build_svg("dark")


def test_animation_only_when_motion_allowed():
    svg = build_svg("dark")
    assert "@keyframes" in svg
    outside = re.sub(r"@media \(prefers-reduced-motion: no-preference\) \{.*?\n\s*\}\n", "", svg, flags=re.S)
    assert "animation" not in outside


def test_main_png_fallback_renders_2x(tmp_path):
    assert main(["--png", "--out", str(tmp_path)]) == 0
    assert (tmp_path / "header-light.svg").exists()
    assert Image.open(tmp_path / "header-dark.png").size == (1600, 300)


def test_png_without_edge_fails_cleanly(tmp_path, monkeypatch, capsys):
    import make_header
    monkeypatch.setattr(make_header, "find_edge", lambda: None)
    assert main(["--png", "--out", str(tmp_path)]) == 1
    assert "Edge not found" in capsys.readouterr().err


def test_missing_font_is_a_clean_error(tmp_path, monkeypatch, capsys):
    import make_header
    monkeypatch.setattr(make_header, "FONT", tmp_path / "nope.woff2")
    assert main(["--out", str(tmp_path)]) == 1
    err = capsys.readouterr().err
    assert str(tmp_path / "nope.woff2") in err and "npm i @fontsource/barlow-condensed" in err


def test_edge_timeout_is_a_clean_error(tmp_path, monkeypatch, capsys):
    import make_header
    import subprocess
    def boom(*a, **k):
        raise subprocess.TimeoutExpired("edge", 60)
    monkeypatch.setattr(make_header, "find_edge", lambda: "edge")
    monkeypatch.setattr(subprocess, "run", boom)
    assert main(["--png", "--out", str(tmp_path)]) == 1
    assert "timed out" in capsys.readouterr().err


def test_font_encoded_once():
    import make_header
    make_header.font_b64.cache_clear()
    build_svg("dark"); build_svg("light")
    assert make_header.font_b64.cache_info().hits >= 1 and make_header.font_b64.cache_info().misses == 1
