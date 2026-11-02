import re
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from make_header import build_svg, contrast, light_bg, light_title, main  # noqa: E402


def test_both_variants_embed_the_font_and_title():
    for theme in ("dark", "light"):
        svg = build_svg(theme)
        assert 'viewBox="0 0 1200 300"' in svg
        assert "@font-face" in svg and "base64," in svg
        assert "Offensive security" in svg and "Nuno Gonçalves" in svg
        assert "<title" in svg and "<desc" in svg
        assert "Informatics Engineering" not in svg
        assert "—" not in svg and "–" not in svg


def test_dark_uses_site_palette():
    svg = build_svg("dark")
    assert "#0a0a0c" in svg and "#ff2a4f" in svg


def test_light_has_light_background_with_aa_title():
    svg = build_svg("light")
    bg = re.search(r'<rect id="bg"[^>]*fill="(#[0-9a-f]{6})"', svg).group(1)
    assert bg == light_bg() and bg != "#0a0a0c"
    assert contrast(light_bg(), light_title()) >= 4.5
    for c in re.findall(r"#[0-9a-f]{6}", svg):
        if c in ("#d4153b", "#0a8a96"):
            assert contrast(light_bg(), c) >= 3
    assert "Looking for" not in svg
    assert max(int(n) for n in re.findall(r"translateX\(-?(\d+)px\)", svg)) <= 4


def test_animation_only_when_motion_allowed():
    svg = build_svg("dark")
    assert "@keyframes" in svg
    outside = re.sub(r"@media \(prefers-reduced-motion: no-preference\) \{.*?\n\s*\}\n", "", svg, flags=re.S)
    assert "animation" not in outside


def test_main_png_fallback_renders_2x(tmp_path):
    assert main(["--png", "--out", str(tmp_path)]) == 0
    assert (tmp_path / "header-light.svg").exists()
    assert Image.open(tmp_path / "header-dark.png").size == (2400, 600)


def test_png_without_edge_fails_cleanly(tmp_path, monkeypatch, capsys):
    import make_header
    monkeypatch.setattr(make_header, "find_edge", lambda: None)
    assert main(["--png", "--out", str(tmp_path)]) == 1
    assert "Edge not found" in capsys.readouterr().err
