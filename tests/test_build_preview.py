import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "preview"))
from build_preview import preview_only  # noqa: E402


def test_preview_only_rewrites_assets_and_opens_details():
    out = preview_only("<img src=\"assets/a.svg\"><img src='assets/b.svg'><source srcset=\"assets/c.svg\">"
                       "<details><details class=\"x\"><details open>")
    assert 'src="../assets/a.svg"' in out and "src='../assets/b.svg'" in out and 'srcset="../assets/c.svg"' in out
    assert out.count("<details open") == 3 and "<details open open" not in out
    assert 'class="x"' in out
