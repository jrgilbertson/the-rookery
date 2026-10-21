#!/usr/bin/env python3
"""Check published graph contracts and synthetic provider adapter behavior."""

from __future__ import annotations

import copy
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
SKILL = REPO_ROOT / "skills/managing-issues/SKILL.md"
REFERENCE = REPO_ROOT / "skills/managing-issues/references/graph-and-completion.md"
GITHUB_REFERENCE = REPO_ROOT / "skills/managing-issues/references/github.md"
LINEAR_REFERENCE = REPO_ROOT / "skills/managing-issues/references/linear.md"
WORKSPACE = "workspace-fixture"
GH_REPOSITORY = "github.com/example/project"
GH_BOUNDARY_REPOSITORY = "github.com/example/dependency"


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def run(
    argv: list[str], env: dict[str, str], *, stdin: str | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def succeeded(result: subprocess.CompletedProcess[str], label: str) -> Any:
    return json.loads(accepted(result, label))


def accepted(result: subprocess.CompletedProcess[str], label: str) -> str:
    require(result.returncode == 0, f"{label} failed: {result.stderr.strip()}")
    require(result.stderr == "", f"{label} wrote stderr")
    return result.stdout.strip()


def log_entries(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def github_command_checks(root: Path, base_env: dict[str, str]) -> None:
    state = root / "github.json"
    log = root / "github.log"
    shutil.copyfile(PROVIDER / "github-graph.json", state)
    env = base_env | {"MI_GITHUB_STATE": str(state), "MI_GITHUB_LOG": str(log)}

    succeeded(
        run(["gh", "auth", "status", "--active", "--hostname", "github.com", "--json", "hosts"], env),
        "GitHub auth preflight",
    )
    succeeded(
        run(["gh", "repo", "view", GH_REPOSITORY, "--json", "id,nameWithOwner,url,hasIssuesEnabled,isArchived,viewerPermission"], env),
        "GitHub repository preflight",
    )
    body = "## Problem\nAdd a child.\n\n## Scope\nCreate one leaf.\n\n## Verification\n- Leaf exists.\n"
    url = accepted(
        run(
            ["gh", "issue", "create", "-R", GH_REPOSITORY, "--title", "Add child", "--body-file", "-"],
            env,
            stdin=body,
        ),
        "GitHub node create",
    )
    created = succeeded(
        run(["gh", "issue", "view", url, "-R", GH_REPOSITORY, "--json", "id,number,title,body,url,parent,subIssues,blockedBy,blocking"], env),
        "GitHub node readback",
    )
    number = str(created["number"])
    succeeded(
        run(
            [
                "gh",
                "auth",
                "status",
                "--active",
                "--hostname",
                "github.com",
                "--json",
                "hosts",
            ],
            env,
        ),
        "GitHub edge auth preflight",
    )
    succeeded(
        run(
            [
                "gh",
                "repo",
                "view",
                GH_REPOSITORY,
                "--json",
                "id,nameWithOwner,url,hasIssuesEnabled,isArchived,viewerPermission",
            ],
            env,
        ),
        "GitHub edge repository preflight",
    )
    for issue in ("10", number):
        succeeded(
            run(["gh", "issue", "view", issue, "-R", GH_REPOSITORY, "--json", "id,number,parent,subIssues,blockedBy,blocking"], env),
            f"GitHub endpoint {issue} preflight",
        )
    accepted(
        run(["gh", "issue", "edit", number, "-R", GH_REPOSITORY, "--parent", "10"], env),
        "GitHub parent edge",
    )
    child = succeeded(
        run(["gh", "issue", "view", number, "-R", GH_REPOSITORY, "--json", "id,number,parent"], env),
        "GitHub child edge readback",
    )
    parent = succeeded(
        run(["gh", "issue", "view", "10", "-R", GH_REPOSITORY, "--json", "id,number,subIssues"], env),
        "GitHub parent edge readback",
    )
    require(child["parent"]["number"] == 10, "GitHub child parent differs")
    require(any(item["number"] == created["number"] for item in parent["subIssues"]), "GitHub parent inverse differs")

    canonical = succeeded(
        run(
            [
                "gh",
                "issue",
                "view",
                "12",
                "-R",
                GH_REPOSITORY,
                "--json",
                "id,number,state,stateReason,url,blockedBy",
            ],
            env,
        ),
        "GitHub canonical blocker read",
    )
    require(len(canonical["blockedBy"]) == 1, "GitHub canonical blocker identity differs")
    boundary_url = canonical["blockedBy"][0].get("url")
    require(
        boundary_url == "https://github.com/example/dependency/issues/9",
        "GitHub canonical read lacks the exact boundary URL",
    )
    boundary_page = succeeded(
        run(
            [
                "gh",
                "api",
                "repos/example/project/issues/12/dependencies/blocked_by?per_page=100&page=1",
                "--hostname",
                "github.com",
            ],
            env,
        ),
        "GitHub native blocker page",
    )
    require(
        len(boundary_page) == 1 and boundary_page[0]["url"] == boundary_url,
        "GitHub native blocker page differs from the validated relationship",
    )
    boundary = succeeded(
        run(
            [
                "gh",
                "issue",
                "view",
                boundary_url,
                "-R",
                GH_BOUNDARY_REPOSITORY,
                "--json",
                "id,number,state,stateReason,url,blockedBy,blocking",
            ],
            env,
        ),
        "GitHub cross-repository boundary read",
    )
    require(
        boundary["number"] == 9
        and boundary["url"] == boundary_url
        and boundary["state"] == "CLOSED"
        and boundary["stateReason"] == "COMPLETED",
        "GitHub boundary state or exact identity matchback differs",
    )

    normal_page_argv = [
        "gh",
        "api",
        "repos/example/project/issues/10/sub_issues?per_page=100&page=1",
        "--hostname",
        "github.com",
    ]
    normal_page = succeeded(
        run(normal_page_argv, env),
        "GitHub native child page without relationship URLs",
    )
    require(
        {item["number"] for item in normal_page} >= {11, 12},
        "GitHub normal relationships without URLs were rejected",
    )

    original_state = state.read_bytes()
    identity_state = json.loads(original_state)
    normal_with_url = copy.deepcopy(identity_state)
    normal_with_url["issues"]["10"]["subIssues"][0]["url"] = normal_with_url[
        "issues"
    ]["11"]["url"]
    state.write_text(json.dumps(normal_with_url), encoding="utf-8")
    succeeded(
        run(normal_page_argv, env),
        "GitHub native child page with an exact relationship URL",
    )

    normal_number_mismatch = copy.deepcopy(identity_state)
    normal_number_mismatch["issues"]["11"]["number"] = 111
    normal_url_mismatch = copy.deepcopy(identity_state)
    normal_url_mismatch["issues"]["10"]["subIssues"][0]["url"] = (
        "https://github.com/example/project/issues/111"
    )
    boundary_number_mismatch = copy.deepcopy(identity_state)
    boundary_number_mismatch["issues"]["12"]["blockedBy"][0]["number"] = 99
    boundary_url_mismatch = copy.deepcopy(identity_state)
    boundary_url_mismatch["boundaryIssues"][boundary_url]["url"] = (
        "https://github.com/example/dependency/issues/99"
    )
    boundary_page_argv = [
        "gh",
        "api",
        "repos/example/project/issues/12/dependencies/blocked_by?per_page=100&page=1",
        "--hostname",
        "github.com",
    ]
    for label, argv, altered_state in (
        ("normal number", normal_page_argv, normal_number_mismatch),
        ("normal URL", normal_page_argv, normal_url_mismatch),
        ("boundary number", boundary_page_argv, boundary_number_mismatch),
        ("boundary URL", boundary_page_argv, boundary_url_mismatch),
    ):
        state.write_text(json.dumps(altered_state), encoding="utf-8")
        rejected = run(argv, env)
        require(
            rejected.returncode != 0
            and "related issue identity differs" in rejected.stderr,
            f"GitHub {label} mismatch passed relationship enumeration",
        )
    state.write_bytes(original_state)

    before_foreign_write = state.read_bytes()
    for argv in (
        ["gh", "issue", "edit", boundary_url, "-R", GH_BOUNDARY_REPOSITORY, "--title", "Forbidden"],
        ["gh", "issue", "close", "9", "-R", GH_BOUNDARY_REPOSITORY, "--reason", "completed"],
        ["gh", "issue", "reopen", "9", "-R", GH_BOUNDARY_REPOSITORY],
    ):
        rejected = run(argv, env)
        require(
            rejected.returncode != 0 and "repository identity differs" in rejected.stderr,
            "GitHub boundary node unexpectedly became a write target",
        )
    require(state.read_bytes() == before_foreign_write, "GitHub rejected boundary writes changed state")

    entries = log_entries(log)
    create_index = next(index for index, entry in enumerate(entries) if entry["argv"][:2] == ["issue", "create"])
    create_readback = next(index for index, entry in enumerate(entries) if index > create_index and entry["argv"][:2] == ["issue", "view"] and entry["argv"][2] == url)
    edge_index = next(index for index, entry in enumerate(entries) if entry["argv"][:3] == ["issue", "edit", number])
    require(create_index < create_readback < edge_index, "GitHub edge ran before node readback")
    require(
        any(
            create_readback < index < edge_index
            and entry["argv"][:2] == ["auth", "status"]
            for index, entry in enumerate(entries)
        ),
        "GitHub edge lacks fresh authentication preflight",
    )
    require(
        any(
            create_readback < index < edge_index
            and entry["argv"][:2] == ["repo", "view"]
            for index, entry in enumerate(entries)
        ),
        "GitHub edge lacks fresh repository preflight",
    )
    require(
        sum(1 for entry in entries[edge_index + 1 :] if entry["argv"][:2] == ["issue", "view"]) >= 2,
        "GitHub edge lacks both endpoint readbacks",
    )


def linear_command_checks(root: Path, base_env: dict[str, str]) -> None:
    state = root / "linear.json"
    log = root / "linear.log"
    shutil.copyfile(PROVIDER / "linear-graph.json", state)
    original = state.read_text(encoding="utf-8")
    env = base_env | {"MI_LINEAR_STATE": str(state), "MI_LINEAR_LOG": str(log)}

    guide = accepted(run(["orca", "skills", "get", "orca-linear"], env), "Linear guide")
    require("orca-linear" in guide, "Linear guide identity differs")
    status = succeeded(run(["orca", "status", "--json"], env), "Linear auth preflight")
    require(status["linear"]["authenticated"] is True, "Linear is not authenticated")
    issue = succeeded(
        run(["orca", "linear", "issue", "ENG-10", "--relations", "--workspace", WORKSPACE, "--json"], env),
        "Linear relation read",
    )
    require(issue["ok"] is True, "Linear relation read RPC failed")

    require(
        state.read_text(encoding="utf-8") == original,
        "Linear adapter reads changed fixture state",
    )


def published_contract_checks() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")
    required = (
        "capabilities before showing an executable graph preview",
        "nodes before relationships",
        "latest complete canonical readback",
        "never use a stored readiness representation as evidence",
        "exactly one",
        "Ready Frontier",
        "needs-discovery",
        "needs-planning",
        "`ready`",
        "no estimate",
        "shared lifecycle's first-stop rule",
        "applied",
        "already_satisfied",
        "failed",
        "indeterminate",
        "unapplied",
        "provider reference",
        "Never match by title",
        "separate batch",
        "list every cascade the provider reports as an intended effect",
        "Do not inspect, predict, repair, or block on effects the provider does not report",
    )
    normalized = " ".join(text.split()).casefold()
    for fragment in required:
        require(
            fragment.casefold() in normalized,
            f"graph reference lacks contract: {fragment}",
        )

    normalized_skill = " ".join(skill.split()).casefold()
    for fragment in (
        "independently deliverable",
        "preferences and convenient ordering",
        "expand–migrate–contract",
    ):
        require(
            fragment.casefold() in normalized_skill,
            f"main skill lacks decomposition contract: {fragment}",
        )

    forbidden = (
        "trusted policy",
        "trusted evidence",
        "authority, policy",
        "Release A treats every Linear topology mutation as `manual`",
        "worktree",
        "branch",
        "pull request",
        "worker",
        "model",
        "schedule",
        "orca linear relation",
        "gh issue edit CHILD",
        "succeeded",
    )
    for fragment in forbidden:
        require(
            fragment.casefold() not in normalized,
            f"graph reference retains stale surface: {fragment}",
        )

    github = GITHUB_REFERENCE.read_text(encoding="utf-8")
    require("sub_issues?per_page=100&page=PAGE" in github, "GitHub reference lacks exhaustive child read")
    require("dependencies/blocked_by?per_page=100&page=PAGE" in github, "GitHub reference lacks exhaustive blocker read")
    require(
        "one-hop cross-repository boundary read" in github
        and "never a create, edit, relationship, or lifecycle target" in github,
        "GitHub reference lacks the read-only cross-repository boundary",
    )
    linear = LINEAR_REFERENCE.read_text(encoding="utf-8")
    require("workspaceErrors" in linear and "capReached" in linear, "Linear reference lacks partial-coverage checks")
    normalized_skill_text = " ".join(skill.split())
    for fragment in (
        "The configured provider is canonical and is the only write target",
        "only through one exact provider-native cross-tracker link",
        "Never infer identity, maintain a repository-side mapping, or mutate the noncanonical issue",
    ):
        require(
            fragment in normalized_skill_text,
            f"main skill lacks cross-tracker routing contract: {fragment}",
        )


def main() -> int:
    for required in (
        SKILL,
        REFERENCE,
        GITHUB_REFERENCE,
        LINEAR_REFERENCE,
        PROVIDER / "github-graph.json",
        PROVIDER / "linear-graph.json",
    ):
        require(required.is_file(), f"missing U3 artifact: {required.relative_to(REPO_ROOT)}")
    published_contract_checks()

    with tempfile.TemporaryDirectory(prefix="managing-issues-graph-") as temporary:
        root = Path(temporary)
        env = os.environ.copy()
        env["PATH"] = f"{BIN}{os.pathsep}{env.get('PATH', '')}"
        github_command_checks(root, env)
        linear_command_checks(root, env)

    print("PASS: managing-issues graph text contracts and provider adapters")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, json.JSONDecodeError, OSError, StopIteration) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
