"""Rule checker for the profile README. Usage: python check_readme.py README.md ../portfolio/src/data.ts"""
import re
import sys
from pathlib import Path

PUBLIC_REPOS = {"NunoGoncalves06", "NunoGoncalves06.github.io", "SpotCast", "Wakecast", "alchemists-arsenal"}
MIN_PROJECTS = 7  # featured plus the six in projects
OMITTED_PROJECTS: set[str] = set()  # data.ts projects deliberately left out of the README
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿←-⇿⤴⤵⬀-⯿〰⭕️‍]|[©®]\ufe0f")
CTF_WORDS = re.compile(r"\b(forensics|reverse engineering|pwn|misc)\b", re.I)
# shortcut: regex over data.ts, not a TS parser; fine while summaries stay plain double-quoted strings.
ATTR = r"""(?:"([^"]*)"|'([^']*)'|([^\s>"']+))"""  # double-quoted, single-quoted or unquoted attribute value
PROJECT = re.compile(r'name:\s*"([^"]+)"[^{}]*?summary:\s*"((?:[^"\\]|\\.)*)"')


def check(readme: str, site_data: str) -> list[str]:
    out = []
    for ch, label in (("—", "em dash"), ("–", "en dash")):
        if ch in readme:
            out.append(f"contains {label} (U+{ord(ch):04X}); dashes are not allowed")
    if EMOJI.search(readme):
        out.append("contains emoji")
    for line in readme.splitlines():
        if re.search(r"certified", line, re.I) and re.search(r"\b(CEH|AWS)\b|ethical hacker", line, re.I):
            out.append(f"says certified for CEH or AWS: {line.strip()}")
    for m in CTF_WORDS.finditer(readme):
        out.append(f"names a CTF category: {m.group(0)}")
    for m in re.finditer(r"github\.com/NunoGoncalves06/([\w.\-]+)", readme):
        repo = m.group(1).rstrip(".")
        if repo not in PUBLIC_REPOS:
            out.append(f"links private or unknown repo: {repo}")
    for line in readme.splitlines():
        s = line.strip()
        if s.startswith("|") and len(re.findall(r"(?<!\\)\|", s)) - 1 > 2:
            out.append(f"table wider than 2 columns: {s[:60]}")
    if re.search(r'(src=|\]\()"?[^\s")]*metrics\.', readme):
        out.append("references a metrics image")
    pic = re.search(r"<picture>.*?</picture>", readme, re.S)
    if not pic:
        out.append("missing header <picture>")
    else:
        p = pic.group(0)
        for theme in ("dark", "light"):
            if not re.search(rf'<source[^>]*prefers-color-scheme:\s*{theme}[^>]*srcset="assets/header-{theme}\.svg"', p):
                out.append(f"header <picture> lacks the {theme} source")
        if not re.search(r"<img\b(?=[^>]*\balt=\"[^\"]+\")(?=[^>]*width=\"100%\")", p):
            out.append("header <img> needs alt text and width=\"100%\"")
    for m in re.finditer(r"<img\b[^>]*>", readme):
        tag = m.group(0)
        alt = re.search(rf"\balt={ATTR}", tag)
        width = re.search(rf"\bwidth={ATTR}", tag)
        a = next((g for g in alt.groups() if g is not None), "") if alt else ""
        w = next((g for g in width.groups() if g is not None), "") if width else ""
        if not alt or (not a.strip() and not (w.isdigit() and int(w) <= 24)):
            out.append(f"img needs alt text (empty alt only on icons 24 px wide or smaller): {tag[:60]}")
    if re.search(r"!\[\s*\]\(", readme):
        out.append("markdown image has empty alt text")
    for row in re.findall(r"<tr\b.*?</tr>", readme, re.S | re.I):
        if len(re.findall(r"<t[dh]\b", row, re.I)) > 2:
            out.append(f"html table row wider than 2 columns: {row[:60]}")
    for m in re.finditer(r"\bcolspan\s*=\s*[\"']?(\d+)", readme, re.I):
        if int(m.group(1)) > 2:
            out.append(f"html table cell with colspan {m.group(1)}, wider than 2 columns")
    if re.search(r"<td\b(?:(?!</td>).)*<table\b", readme, re.S | re.I):
        out.append("html table nested inside a cell")
    for h in ("Highlights", "Projects", "Skills", "Contact"):
        if not re.search(rf"^##[ \t]+(?:<img\b[^>]*>[ \t]*)?{h}[ \t]*$", readme, re.M):
            out.append(f"missing ## heading: {h}")
    # a summary counts only as visible text, not inside alt attributes or markdown alt
    visible = re.sub(r"<!--.*?-->", "", readme, flags=re.S)
    visible = re.sub(rf"\b(?:alt|title)={ATTR}", "", visible)
    visible = re.sub(r"!\[[^\]]*\]", "", visible)
    found = PROJECT.findall(site_data)
    if len(found) < MIN_PROJECTS:
        out.append(f"parsed only {len(found)} projects from data.ts, expected at least {MIN_PROJECTS}")
    for name, summary in found:
        lead = rf"^(?:#{{1,6}}\s+|[-*]\s+)\[?{re.escape(name)}(?!\w)"
        if not re.search(lead, readme, re.M):
            if name not in OMITTED_PROJECTS:
                out.append(f"project {name} from data.ts is missing from the README")
        elif summary not in visible:
            out.append(f"summary for {name} is not verbatim from data.ts")
    return out


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python check_readme.py README.md data.ts", file=sys.stderr)
        sys.exit(2)
    probs = check(Path(sys.argv[1]).read_text(encoding="utf-8"), Path(sys.argv[2]).read_text(encoding="utf-8"))
    for p in probs:
        print(p)
    sys.exit(1 if probs else 0)
