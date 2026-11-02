import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import apply_repo_changes as arc  # noqa: E402

SITE = "https://nunogoncalves06.github.io"
CHANGES = arc.load(ROOT / "repo-changes.json")


def test_descriptions_max_120():
    for repo, c in CHANGES.items():
        if c["description"] is not None:
            assert len(c["description"]) <= 120, repo


def test_no_dashes_in_descriptions():
    for repo, c in CHANGES.items():
        assert not set(c["description"] or "") & {"—", "–"}, repo


def test_homepage_is_site_for_listed_repos():
    for repo in ("SpotCast", "Wakecast", "NunoGoncalves06.github.io", "NunoGoncalves06"):
        assert CHANGES[repo]["homepage"] == SITE


def test_alchemist_description_exact():
    assert CHANGES["alchemists-arsenal"]["description"] == "Unity game in C#, built on my own."


def test_dry_run_runs_nothing(capsys):
    with mock.patch.object(subprocess, "run") as run:
        arc.main(["--dry-run"])
        arc.main([])
    assert not run.called
    assert "gh repo edit" in capsys.readouterr().out


def test_commands_pass_separate_argv():
    cmds = arc.commands({"R": {"description": "a b; c", "homepage": None, "topics": ["x", "y"]}})
    assert cmds == [["gh", "repo", "edit", "NunoGoncalves06/R", "--description", "a b; c",
                     "--add-topic", "x", "--add-topic", "y"]]
    assert arc.commands({"R": {"description": None, "homepage": None, "topics": None}}) == []


def test_apply_uses_check_and_timeout():
    with mock.patch.object(subprocess, "run") as run:
        arc.main(["--apply"])
    assert run.call_args.kwargs == {"check": True, "timeout": 60}
