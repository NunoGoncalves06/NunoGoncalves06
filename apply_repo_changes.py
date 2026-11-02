"""Build and (optionally) run the `gh repo edit` calls for the public repos.

Default is --dry-run: print the commands. --apply runs them (needs Nuno's approval first).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

OWNER = "NunoGoncalves06"
DEFAULT = Path(__file__).with_name("repo-changes.json")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def commands(changes):
    out = []
    for repo, c in changes.items():
        args = []
        if c.get("description") is not None:
            args += ["--description", c["description"]]
        if c.get("homepage") is not None:
            args += ["--homepage", c["homepage"]]
        for t in c.get("topics") or []:
            args += ["--add-topic", t]
        if args:
            out.append(["gh", "repo", "edit", f"{OWNER}/{repo}", *args])
    return out


def main(argv=None):
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", help="print commands (default)")
    g.add_argument("--apply", action="store_true", help="run the commands")
    ap = p.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")  # Windows console default would garble the ç
    cmds = commands(load(DEFAULT))
    if not ap.apply:
        for cmd in cmds:
            print(subprocess.list2cmdline(cmd))
        return 0
    done, failed = [], []
    for cmd in cmds:
        try:
            subprocess.run(cmd, check=True, timeout=60)
            done.append(cmd[3])
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            failed.append(cmd[3])
    print(f"applied: {', '.join(done) or 'none'}")
    print(f"failed: {', '.join(failed) or 'none'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
