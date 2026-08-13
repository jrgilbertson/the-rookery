#!/usr/bin/env python3
"""Exercise the exact provider command paths shipped by managing-issues."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
BIN = HERE / "bin"
PROVIDER = HERE / "provider"
REFERENCES = REPO_ROOT / "skills" / "managing-issues" / "references"
ISSUE_FIELDS = (
    "id,number,title,body,state,stateReason,updatedAt,url,labels,assignees,"
    "issueType,parent,subIssues,blockedBy,blocking"
)


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def run(
    argv: list[str],
    env: dict[str, str],
    *,
    stdin: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def succeeded(result: subprocess.CompletedProcess[str], label: str) -> dict[str, Any]:
    require(result.returncode == 0, f"{label} failed: {result.stderr.strip()}")
    require(result.stderr == "", f"{label} wrote stderr")
    return json.loads(result.stdout)


def failed(result: subprocess.CompletedProcess[str], fragment: str, label: str) -> None:
    require(result.returncode != 0, f"{label} unexpectedly succeeded")
    require(fragment in result.stderr, f"{label} failed for wrong reason: {result.stderr.strip()}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def log_entries(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def command_positions(entries: list[dict[str, Any]], prefix: list[str]) -> list[int]:
    return [index for index, entry in enumerate(entries) if entry["argv"][: len(prefix)] == prefix]


def github_checks(root: Path, env: dict[str, str]) -> None:
    state = root / "github.json"
    log = root / "github.log"
    shutil.copyfile(PROVIDER / "github.json", state)
    github_env = env | {"MI_GITHUB_STATE": str(state), "MI_GITHUB_LOG": str(log)}

    auth = succeeded(run(["gh", "auth", "status", "--active", "--hostname", "github.com"], github_env), "GitHub auth")
    require(auth["principal"] == "fixture-user", "GitHub auth principal differs")
    repository = succeeded(
        run(
            [
                "gh", "repo", "view", "example/project", "--json",
                "id,nameWithOwner,url,hasIssuesEnabled,isArchived,viewerPermission",
            ],
            github_env,
        ),
        "GitHub repository identity",
    )
    require(repository["nameWithOwner"] == "example/project", "GitHub repository differs")
    before = succeeded(
        run(["gh", "issue", "view", "1", "-R", "example/project", "--json", ISSUE_FIELDS], github_env),
        "GitHub pre-read",
    )
    require(before["title"] == "Existing issue", "GitHub fixture pre-state differs")

    update = run(
        ["gh", "issue", "edit", "1", "-R", "example/project", "--title", "Updated issue", "--body-file", "-"],
        github_env,
        stdin="## Problem\n\nUpdated text\n",
    )
    require(update.returncode == 0, f"GitHub update failed: {update.stderr.strip()}")
    after = succeeded(
        run(["gh", "issue", "view", "1", "-R", "example/project", "--json", ISSUE_FIELDS], github_env),
        "GitHub update readback",
    )
    require(after["title"] == "Updated issue" and "Updated text" in after["body"], "GitHub readback differs")

    created = run(
        ["gh", "issue", "create", "-R", "example/project", "--title", "Created issue", "--body-file", "-"],
        github_env,
        stdin="## Problem\n\nCreated text\n",
    )
    require(created.returncode == 0, f"GitHub create failed: {created.stderr.strip()}")
    created_url = created.stdout.strip()
    require(created_url.endswith("/issues/3"), "GitHub create identity differs")
    created_readback = succeeded(
        run(["gh", "issue", "view", created_url, "-R", "example/project", "--json", ISSUE_FIELDS], github_env),
        "GitHub create readback",
    )
    require(created_readback["title"] == "Created issue", "GitHub created issue differs")

    snapshot = state.read_bytes()
    failed(
        run(["gh", "issue", "edit", "1", "-R", "example/shadow", "--title", "Wrong target"], github_env),
        "shadow repository is read-only",
        "GitHub shadow write",
    )
    require(state.read_bytes() == snapshot, "GitHub shadow rejection changed state")
    failed(run(["gh", "issue", "delete", "1", "-R", "example/project"], github_env), "unsupported command", "GitHub delete")

    indeterminate_state = root / "github-indeterminate.json"
    indeterminate_log = root / "github-indeterminate.log"
    shutil.copyfile(PROVIDER / "github.json", indeterminate_state)
    indeterminate_env = github_env | {
        "MI_GITHUB_STATE": str(indeterminate_state),
        "MI_GITHUB_LOG": str(indeterminate_log),
        "MI_GITHUB_INDETERMINATE_CREATE": "1",
    }
    failed(
        run(["gh", "issue", "create", "-R", "example/project", "--title", "Unconfirmed", "--body-file", "-"], indeterminate_env, stdin="body\n"),
        "create outcome is indeterminate",
        "GitHub indeterminate create",
    )
    require(load_json(indeterminate_state)["next_issue"] == 4, "GitHub indeterminate create did not expose possible state")
    require(len(command_positions(log_entries(indeterminate_log), ["issue", "create"])) == 1, "GitHub indeterminate create was not exactly one attempt")

    entries = log_entries(log)
    edits = command_positions(entries, ["issue", "edit"])
    views = command_positions(entries, ["issue", "view"])
    require(len(edits) == 2, "GitHub log should contain one accepted and one rejected edit")
    require(any(position > edits[0] for position in views), "GitHub update lacks later readback")
    creates = command_positions(entries, ["issue", "create"])
    require(len(creates) == 1 and any(position > creates[0] for position in views), "GitHub create/readback ordering differs")


def linear_checks(root: Path, env: dict[str, str]) -> None:
    state = root / "linear.json"
    log = root / "linear.log"
    shutil.copyfile(PROVIDER / "linear.json", state)
    linear_env = env | {"MI_LINEAR_STATE": str(state), "MI_LINEAR_LOG": str(log)}

    teams = succeeded(run(["orca", "linear", "team", "list", "--workspace", "all", "--json"], linear_env), "Linear team preflight")
    require(teams["principal"] == "fixture-user" and teams["teams"][0]["key"] == "ENG", "Linear identity differs")
    succeeded(run(["orca", "linear", "team", "states", "--team", "ENG", "--json"], linear_env), "Linear states")
    succeeded(run(["orca", "linear", "team", "labels", "--team", "ENG", "--json"], linear_env), "Linear labels")
    before = succeeded(run(["orca", "linear", "issue", "ENG-1", "--relations", "--json"], linear_env), "Linear pre-read")
    require(before["issue"]["title"] == "Existing issue", "Linear fixture pre-state differs")

    update = run(["orca", "linear", "save-issue", "ENG-1", "--title", "Updated issue", "--body-file", "-", "--json"], linear_env, stdin="## Problem\n\nUpdated text\n")
    succeeded(update, "Linear update")
    after = succeeded(run(["orca", "linear", "issue", "ENG-1", "--relations", "--json"], linear_env), "Linear update readback")
    require(after["issue"]["title"] == "Updated issue" and "Updated text" in after["issue"]["description"], "Linear readback differs")

    succeeded(run(["orca", "linear", "priority", "set", "ENG-1", "--to", "urgent", "--json"], linear_env), "Linear priority")
    priority_readback = succeeded(run(["orca", "linear", "issue", "ENG-1", "--json"], linear_env), "Linear priority readback")
    require(priority_readback["issue"]["priority"] == "urgent", "Linear priority readback differs")

    created = succeeded(
        run(["orca", "linear", "create", "--team", "ENG", "--title", "Created issue", "--body-file", "-", "--json"], linear_env, stdin="## Problem\n\nCreated text\n"),
        "Linear create",
    )
    identifier = created["issue"]["identifier"]
    require(identifier == "ENG-3", "Linear create identity differs")
    created_readback = succeeded(run(["orca", "linear", "issue", identifier, "--json"], linear_env), "Linear create readback")
    require(created_readback["issue"]["title"] == "Created issue", "Linear created issue differs")

    failed(run(["orca", "linear", "delete", "ENG-1", "--json"], linear_env), "unsupported command", "Linear delete")

    indeterminate_state = root / "linear-indeterminate.json"
    indeterminate_log = root / "linear-indeterminate.log"
    shutil.copyfile(PROVIDER / "linear.json", indeterminate_state)
    indeterminate_env = linear_env | {
        "MI_LINEAR_STATE": str(indeterminate_state),
        "MI_LINEAR_LOG": str(indeterminate_log),
        "MI_LINEAR_INDETERMINATE_CREATE": "1",
    }
    failed(
        run(["orca", "linear", "create", "--team", "ENG", "--title", "Unconfirmed", "--body-file", "-", "--json"], indeterminate_env, stdin="body\n"),
        "linear_write_unconfirmed",
        "Linear indeterminate create",
    )
    require(load_json(indeterminate_state)["next_issue"] == 4, "Linear indeterminate create did not expose possible state")
    require(len(command_positions(log_entries(indeterminate_log), ["linear", "create"])) == 1, "Linear indeterminate create was not exactly one attempt")

    entries = log_entries(log)
    saves = command_positions(entries, ["linear", "save-issue"])
    reads = command_positions(entries, ["linear", "issue"])
    require(len(saves) == 1 and any(position > saves[0] for position in reads), "Linear update/readback ordering differs")
    creates = command_positions(entries, ["linear", "create"])
    require(len(creates) == 1 and any(position > creates[0] for position in reads), "Linear create/readback ordering differs")


def main() -> int:
    for required in (
        BIN / "gh",
        BIN / "orca",
        REFERENCES / "github.md",
        REFERENCES / "linear-and-sync.md",
    ):
        require(required.is_file(), f"missing U2 artifact: {required.relative_to(REPO_ROOT)}")
    require(os.access(BIN / "gh", os.X_OK), "fixture gh is not executable")
    require(os.access(BIN / "orca", os.X_OK), "fixture orca is not executable")

    with tempfile.TemporaryDirectory(prefix="managing-issues-provider-") as temporary:
        root = Path(temporary)
        env = os.environ.copy()
        env["PATH"] = f"{BIN}{os.pathsep}{env.get('PATH', '')}"
        github_checks(root, env)
        linear_checks(root, env)

    print("PASS: managing-issues provider command paths")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, json.JSONDecodeError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
