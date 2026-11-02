import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from check_readme import check  # noqa: E402

NAMES = ["Big Net", "Other", "P3", "P4", "P5", "P6", "P7"]
SITE = """export const featured: Project = {
  name: "Big Net",
  stack: ["A"],
  summary:
    "Summary of Big Net.",
}
export const projects: Project[] = [
""" + "".join(f'  {{ name: "{n}", summary: "Summary of {n}.", link: "x" }},' + chr(10) for n in NAMES[1:]) + "]"

GOOD = """<picture>
<source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
<source media="(prefers-color-scheme: light)" srcset="assets/header-light.svg">
<img src="assets/header-dark.svg" width="100%" alt="Header">
</picture>

Hello. See [Other](https://github.com/NunoGoncalves06/SpotCast).

""" + (chr(10)*2).join(f'## <img src="assets/icon-{i}.svg" width="20" height="20" alt=""> {h}' for i, h in (("flag", "Highlights"), ("folder", "Projects"), ("terminal", "Skills"), ("mail", "Contact"))) + """

""" + (chr(10) * 2).join(f"### {n}" + chr(10) * 2 + f"Summary of {n}." for n in NAMES) + """

| a | b |
|---|---|
| 1 | 2 |

<table>
<tr><td><b>Security</b></td><td><img src="https://img.shields.io/badge/Nmap-x" alt="Nmap"></td></tr>
</table>
"""


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
    bad = GOOD.replace("Summary of Big Net.", "A changed summary.")
    assert any("Big Net" in p for p in check(bad, SITE))
    bad = GOOD.replace("Summary of Other.", "Different.")
    assert any("Other" in p for p in check(bad, SITE))


def test_requires_dark_source():
    bad = GOOD.replace('srcset="assets/header-dark.svg"', 'srcset="assets/other.svg"', 1)
    assert any("dark" in p for p in check(bad, SITE))


def test_flags_unparseable_site_data():
    assert any("data.ts" in p for p in check(GOOD, "export const x = 1"))
    assert any("data.ts" in p for p in check(GOOD, SITE.replace('name: "P7"', "nome: 'P7'")))


def test_flags_project_missing_from_readme():
    bad = GOOD.replace("### P7" + chr(10) * 2 + "Summary of P7.", "")
    assert any("P7" in p and "missing" in p for p in check(bad, SITE))


def test_omitted_allowlist_excuses_missing_project(monkeypatch):
    import check_readme
    monkeypatch.setattr(check_readme, "OMITTED_PROJECTS", {"P7"})
    bad = GOOD.replace("### P7" + chr(10) * 2 + "Summary of P7.", "")
    assert check(bad, SITE) == []


def test_project_name_must_be_a_heading_or_list_lead():
    bad = GOOD.replace("### P7", "P7 is mentioned here")
    assert any("P7" in p and "missing" in p for p in check(bad, SITE))
    assert check(GOOD.replace("### P7", "- P7."), SITE) == []
    assert check(GOOD.replace("### P7", "### [P7](https://x)"), SITE) == []
    assert any("P3" in p for p in check(GOOD.replace("### P3", "### P3x"), SITE))


def test_flags_wider_emoji_ranges():
    for ch in ("→", "⤴", "⭐", "〰", "©️", "®️"):
        assert has(f"x {ch}", "emoji"), hex(ord(ch[0]))
    assert not has("plain © and ç", "emoji")


def test_flags_img_without_alt():
    assert has('<img src="x.svg" width="100" alt="">', "alt")
    assert has('<img src="x.svg">', "alt")
    assert has("![](x.svg)", "alt")
    assert not has('<img src="x.svg" width="24" height="24" alt="">', "alt")
    assert has('<img src="x.svg" width="25" alt="">', "alt")


def test_flags_summary_only_in_alt():
    bad = GOOD.replace("Summary of P7.", "", 1) + '<img src="x.svg" alt="Summary of P7.">'
    assert any("P7" in p and "verbatim" in p for p in check(bad, SITE))


def test_flags_wide_html_table():
    assert has("<table><tr><td>a</td><td>b</td><td>c</td></tr></table>", "table")
    assert has("<table><tr><th>a</th><td>b</td><td>c</td></tr></table>", "table")


def test_requires_section_headings():
    for h in ("Highlights", "Projects", "Skills", "Contact"):
        bad = GOOD.replace(f"> {h}", f"> {h}x")
        assert any(h in p and "heading" in p for p in check(bad, SITE)), h
    assert any("Skills" in p for p in check(GOOD.replace("## <img", "### <img"), SITE))


def test_usage_exit_2():
    import subprocess, sys
    r = subprocess.run([sys.executable, str(Path(__file__).resolve().parent.parent / "check_readme.py")], capture_output=True, text=True)
    assert r.returncode == 2 and "usage" in r.stderr
