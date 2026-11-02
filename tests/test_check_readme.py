import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from check_readme import check  # noqa: E402

SITE = '''
export const featured: Project = {
  name: "Big Net",
  stack: ["A"],
  summary:
    "A network summary.",
}
export const projects: Project[] = [
  { name: "Other", summary: "Other summary.", link: "x" },
  { name: "Unused", summary: "Never shown.", },
]
'''

GOOD = '''<picture>
<source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
<source media="(prefers-color-scheme: light)" srcset="assets/header-light.svg">
<img src="assets/header-dark.svg" width="100%" alt="Header">
</picture>

Hello. See [Other](https://github.com/NunoGoncalves06/SpotCast).

Big Net: A network summary.

Other: Other summary.

| a | b |
|---|---|
| 1 | 2 |
'''


def problems(extra="", site=SITE):
    return check(GOOD + "\n" + extra, site)


def has(extra, word, site=SITE):
    return any(word in p for p in problems(extra, site))


def test_accepts_good_readme():
    assert check(GOOD, SITE) == []


def test_flags_em_dash():
    assert has("a — b", "dash")


def test_flags_en_dash():
    assert has("a – b", "dash")


def test_flags_emoji():
    assert has("rocket \U0001F680", "emoji")


def test_flags_ceh_certified():
    assert has("CEH v13 certified", "certified")
    assert has("Certified Ethical Hacker", "certified")
    assert has("AWS Certified", "certified")


def test_flags_ctf_categories():
    assert has("I like forensics", "CTF category")
    assert has("Reverse Engineering", "CTF category")


def test_flags_private_repo_link():
    assert has("github.com/NunoGoncalves06/european-stations-data", "private")
    for ok in ("SpotCast", "Wakecast", "NunoGoncalves06.github.io", "alchemists-arsenal", "NunoGoncalves06"):
        assert not has(f"https://github.com/NunoGoncalves06/{ok}", "private")


def test_flags_wide_table():
    assert has("| a | b | c |\n|---|---|---|\n| 1 | 2 | 3 |", "table")


def test_flags_metrics_image():
    assert has('<img src="metrics.terminal.svg" alt="x">', "metrics")


def test_requires_picture_with_both_headers():
    bad = GOOD.replace("header-light.svg", "other.svg")
    assert any("header" in p for p in check(bad, SITE))
    assert any("header" in p for p in check("no picture", SITE))


def test_requires_site_summaries_verbatim():
    bad = GOOD.replace("A network summary.", "A changed summary.")
    assert any("Big Net" in p for p in check(bad, SITE))
    bad = GOOD.replace("Other summary.", "Different.")
    assert any("Other" in p for p in check(bad, SITE))
    # a project whose name is absent is not required
    assert not any("Unused" in p for p in check(GOOD, SITE))
