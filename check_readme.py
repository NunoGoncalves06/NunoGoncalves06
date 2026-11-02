"""Rule checker for the profile README. Usage: python check_readme.py README.md ../portfolio/src/data.ts"""
import re
import sys
from pathlib import Path

PUBLIC_REPOS = {"NunoGoncalves06", "NunoGoncalves06.github.io", "SpotCast", "Wakecast", "alchemists-arsenal"}
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⭐⭕️‍]")
CTF_WORDS = re.compile(r"\b(forensics|reverse engineering|pwn|misc)\b", re.I)
# shortcut: regex over data.ts, not a TS parser; fine while summaries stay plain double-quoted strings.
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
    for name, summary in PROJECT.findall(site_data):
        if name in readme and summary not in readme:
            out.append(f"summary for {name} is not verbatim from data.ts")
    return out


if __name__ == "__main__":
    probs = check(Path(sys.argv[1]).read_text(encoding="utf-8"), Path(sys.argv[2]).read_text(encoding="utf-8"))
    for p in probs:
        print(p)
    sys.exit(1 if probs else 0)
