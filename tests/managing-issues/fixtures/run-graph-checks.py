#!/usr/bin/env python3
"""Exercise graph command seams without claiming an agent behavioral grade."""

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
REFERENCE = REPO_ROOT / "skills" / "managing-issues" / "references" / "graph-and-completion.md"
CAP = 250
WORKSPACE = "workspace-fixture"
REPOSITORY = "example/project"
GH_REPOSITORY = f"github.com/{REPOSITORY}"


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def run(argv: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, text=True, capture_output=True, check=False, env=env)


def succeeded(result: subprocess.CompletedProcess[str], label: str) -> Any:
    require(result.returncode == 0, f"{label} failed: {result.stderr.strip()}")
    require(result.stderr == "", f"{label} wrote stderr")
    return json.loads(result.stdout)


def linear_result(result: subprocess.CompletedProcess[str], label: str) -> dict[str, Any]:
    response = succeeded(result, label)
    require(
        set(response) == {"id", "ok", "result", "_meta"},
        f"{label} RPC envelope differs",
    )
    require(response["ok"] is True, f"{label} RPC response is not successful")
    require(isinstance(response["result"], dict), f"{label} result differs")
    return response["result"]


def failed(result: subprocess.CompletedProcess[str], fragment: str, label: str) -> None:
    require(result.returncode != 0, f"{label} unexpectedly succeeded")
    require(fragment in result.stderr, f"{label} did not report {fragment!r}")


def accepted(result: subprocess.CompletedProcess[str], label: str) -> None:
    require(result.returncode == 0, f"{label} failed: {result.stderr.strip()}")
    require(result.stderr == "", f"{label} wrote stderr")


def log_entries(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def command_positions(entries: list[dict[str, Any]], prefix: list[str]) -> list[int]:
    return [
        index
        for index, entry in enumerate(entries)
        if entry["argv"][: len(prefix)] == prefix
    ]


def assert_graph_effect(
    entries: list[dict[str, Any]],
    start: int,
    write_prefix: list[str],
    preflight_prefixes: list[list[str]],
    *,
    readbacks: int,
) -> None:
    window = entries[start:]
    writes = command_positions(window, write_prefix)
    require(len(writes) == 1, f"expected one graph write: {' '.join(write_prefix)}")
    write = writes[0]
    for prefix in preflight_prefixes:
        require(
            any(
                index < write and entry["argv"][: len(prefix)] == prefix
                for index, entry in enumerate(window)
            ),
            f"graph write {' '.join(write_prefix)} lacks fresh {' '.join(prefix)} preflight",
        )
    require(
        sum(
            index > write and entry["argv"][:2] in (["issue", "view"], ["linear", "issue"])
            for index, entry in enumerate(window)
        )
        >= readbacks,
        f"graph write {' '.join(write_prefix)} lacks endpoint readback",
    )


def github_preflight(env: dict[str, str], *issues: str) -> None:
    auth = succeeded(
        run(
            [
                "gh", "auth", "status", "--active", "--hostname", "github.com",
                "--json", "hosts",
            ],
            env,
        ),
        "GitHub graph auth preflight",
    )
    active = auth["hosts"]["github.com"]
    require(
        len(active) == 1 and active[0]["active"] and active[0]["state"] == "success",
        "GitHub graph principal is not one active authenticated account",
    )
    repository = succeeded(
        run(
            [
                "gh", "repo", "view", GH_REPOSITORY, "--json",
                "id,nameWithOwner,url,hasIssuesEnabled,isArchived,viewerPermission",
            ],
            env,
        ),
        "GitHub graph repository preflight",
    )
    require(
        repository["nameWithOwner"] == REPOSITORY
        and repository["hasIssuesEnabled"]
        and not repository["isArchived"],
        "GitHub graph repository is not writable",
    )
    for issue in issues:
        succeeded(
            run(
                [
                    "gh", "issue", "view", issue, "-R", GH_REPOSITORY, "--json",
                    "id,number,parent,subIssues,blockedBy,blocking",
                ],
                env,
            ),
            f"GitHub graph issue {issue} preflight",
        )


def github_collection_pages(
    env: dict[str, str], endpoint: str, visited: set[str], per_page: int = 100
) -> tuple[str, list[dict[str, Any]]]:
    nodes: list[dict[str, Any]] = []
    page = 1
    while True:
        result = run(["gh", "api", f"{endpoint}?per_page={per_page}&page={page}", "--hostname", "github.com"], env)
        if result.returncode != 0:
            return "partial", nodes
        page_nodes = json.loads(result.stdout)
        new_nodes = [node for node in page_nodes if node["id"] not in visited]
        remaining = CAP - len(visited)
        if len(new_nodes) > remaining:
            nodes.extend(new_nodes[:remaining])
            visited.update(node["id"] for node in new_nodes[:remaining])
            return "partial", nodes
        nodes.extend(new_nodes)
        visited.update(node["id"] for node in new_nodes)
        if len(visited) == CAP and len(page_nodes) == per_page:
            return "partial", nodes
        if len(page_nodes) < per_page:
            return "complete", nodes
        page += 1


def github_checks(root: Path, base_env: dict[str, str]) -> None:
    state = root / "github.json"
    log = root / "github.log"
    shutil.copyfile(PROVIDER / "github-graph.json", state)
    env = base_env | {"MI_GITHUB_STATE": str(state), "MI_GITHUB_LOG": str(log)}

    visited = {"I_10"}
    coverage, children = github_collection_pages(
        env,
        "repos/example/project/issues/10/sub_issues",
        visited,
    )
    require(coverage == "complete", "GitHub child pagination did not complete")
    require([node["number"] for node in children] == [11, 12], "GitHub pages were not exhausted")

    coverage, blocked_by = github_collection_pages(
        env,
        "repos/example/project/issues/12/dependencies/blocked_by",
        visited,
    )
    require(coverage == "complete", "GitHub blocker pagination did not complete")
    require(blocked_by[0]["number"] == 99, "GitHub one-hop boundary differs")
    boundary = succeeded(
        run(["gh", "issue", "view", "99", "-R", GH_REPOSITORY, "--json", "id,number,title,state"], env),
        "GitHub boundary read",
    )
    require(boundary["number"] == 99, "GitHub boundary identity differs")

    checkpoint = len(log_entries(log))
    github_preflight(env, "11", "12")
    accepted(
        run(["gh", "issue", "edit", "11", "-R", GH_REPOSITORY, "--add-blocking", "12"], env),
        "GitHub relation add",
    )
    source = succeeded(
        run(["gh", "issue", "view", "11", "-R", GH_REPOSITORY, "--json", "id,number,blocking"], env),
        "GitHub relation source readback",
    )
    target = succeeded(
        run(["gh", "issue", "view", "12", "-R", GH_REPOSITORY, "--json", "id,number,blockedBy"], env),
        "GitHub relation target readback",
    )
    require([node["number"] for node in source["blocking"]] == [12], "GitHub blocking direction differs")
    require({node["number"] for node in target["blockedBy"]} == {11, 99}, "GitHub blocked-by direction differs")
    assert_graph_effect(
        log_entries(log),
        checkpoint,
        ["issue", "edit", "11"],
        [
            ["auth", "status"],
            ["repo", "view"],
            ["issue", "view", "11"],
            ["issue", "view", "12"],
        ],
        readbacks=2,
    )

    checkpoint = len(log_entries(log))
    github_preflight(env, "10", "11")
    accepted(run(["gh", "issue", "edit", "11", "-R", GH_REPOSITORY, "--remove-parent"], env), "GitHub parent removal")
    detached = succeeded(
        run(["gh", "issue", "view", "11", "-R", GH_REPOSITORY, "--json", "id,number,parent"], env),
        "GitHub detached child readback",
    )
    detached_parent = succeeded(
        run(["gh", "issue", "view", "10", "-R", GH_REPOSITORY, "--json", "id,number,subIssues"], env),
        "GitHub detached parent readback",
    )
    require(detached["parent"] is None and all(node["number"] != 11 for node in detached_parent["subIssues"]), "GitHub parent removal differs")
    assert_graph_effect(
        log_entries(log),
        checkpoint,
        ["issue", "edit", "11"],
        [
            ["auth", "status"],
            ["repo", "view"],
            ["issue", "view", "10"],
            ["issue", "view", "11"],
        ],
        readbacks=2,
    )
    checkpoint = len(log_entries(log))
    github_preflight(env, "10", "11")
    accepted(run(["gh", "issue", "edit", "11", "-R", GH_REPOSITORY, "--parent", "10"], env), "GitHub parent restore")
    restored = succeeded(
        run(["gh", "issue", "view", "11", "-R", GH_REPOSITORY, "--json", "id,number,parent"], env),
        "GitHub restored child readback",
    )
    require(restored["parent"]["number"] == 10, "GitHub parent direction differs")
    assert_graph_effect(
        log_entries(log),
        checkpoint,
        ["issue", "edit", "11"],
        [
            ["auth", "status"],
            ["repo", "view"],
            ["issue", "view", "10"],
            ["issue", "view", "11"],
        ],
        readbacks=1,
    )

    failed_env = env | {"MI_GITHUB_GRAPH_SCENARIO": "unreadable-boundary"}
    failed(
        run(["gh", "issue", "view", "99", "-R", GH_REPOSITORY, "--json", "id,number,title,state"], failed_env),
        "required boundary is inaccessible",
        "GitHub inaccessible boundary",
    )

    cap_env = env | {"MI_GITHUB_GRAPH_SCENARIO": "cap"}
    cap_visited = {"I_10"}
    coverage, nodes = github_collection_pages(
        cap_env,
        "repos/example/project/issues/10/sub_issues",
        cap_visited,
    )
    require(
        coverage == "partial" and len(nodes) == CAP - 1 and len(cap_visited) == CAP,
        "GitHub node cap did not count the root and stop at partial coverage",
    )


def linear_child_pages(env: dict[str, str], parent: str) -> tuple[str, list[dict[str, Any]]]:
    cursor: str | None = None
    seen_cursors: set[str] = set()
    nodes: list[dict[str, Any]] = []
    visited = {parent}
    while True:
        argv = [
            "orca", "linear", "list-issues", "--parent-id", parent,
            "--limit", "100", "--workspace", WORKSPACE, "--json",
        ]
        if cursor is not None:
            argv.extend(["--cursor", cursor])
        result = run(argv, env)
        if result.returncode != 0:
            return "partial", nodes
        page = linear_result(result, "Linear child page")
        page_info = page.get("meta", {})
        if page_info.get("workspaceErrors") != []:
            return "partial", nodes
        page_nodes = [node for node in page["issues"] if node["identifier"] not in visited]
        remaining = CAP - len(visited)
        if len(page_nodes) > remaining:
            nodes.extend(page_nodes[:remaining])
            visited.update(node["identifier"] for node in page_nodes[:remaining])
            return "partial", nodes
        nodes.extend(page_nodes)
        visited.update(node["identifier"] for node in page_nodes)
        if len(visited) == CAP and page_info["hasMore"]:
            return "partial", nodes
        if not page_info["hasMore"]:
            return "complete", nodes
        next_cursor = page_info.get("nextCursor")
        if not next_cursor or next_cursor in seen_cursors:
            return "partial", nodes
        seen_cursors.add(next_cursor)
        cursor = next_cursor


def linear_checks(root: Path, base_env: dict[str, str]) -> None:
    state = root / "linear.json"
    log = root / "linear.log"
    shutil.copyfile(PROVIDER / "linear-graph.json", state)
    env = base_env | {"MI_LINEAR_STATE": str(state), "MI_LINEAR_LOG": str(log)}

    coverage, children = linear_child_pages(env, "ENG-10")
    require(coverage == "complete", "Linear pagination did not complete")
    require([node["identifier"] for node in children] == ["ENG-11", "ENG-12"], "Linear pages differ")

    teams = linear_result(
        run(["orca", "linear", "team", "list", "--workspace", WORKSPACE, "--json"], env),
        "Linear graph team read",
    )
    require(
        "principal" not in teams
        and teams["teams"][0]["workspace"]["id"] == WORKSPACE,
        "Linear graph workspace metadata differs",
    )
    relation_read = linear_result(
        run(["orca", "linear", "issue", "ENG-12", "--relations", "--workspace", WORKSPACE, "--json"], env),
        "Linear relation read",
    )
    require(
        relation_read["issue"]["relations"][0]["issue"]["identifier"] == "ENG-99"
        and relation_read["meta"]["includeErrors"] == []
        and relation_read["meta"]["sections"]["relations"]["capReached"] is False,
        "Linear boundary differs",
    )

    workspace_error_env = env | {"MI_LINEAR_GRAPH_SCENARIO": "workspace-error"}
    coverage, _ = linear_child_pages(workspace_error_env, "ENG-10")
    require(coverage == "partial", "Linear workspace warning did not produce partial coverage")

    for scenario in ("include-error", "relations-cap"):
        warning = linear_result(
            run(
                ["orca", "linear", "issue", "ENG-12", "--relations", "--workspace", WORKSPACE, "--json"],
                env | {"MI_LINEAR_GRAPH_SCENARIO": scenario},
            ),
            f"Linear {scenario} read",
        )
        complete = (
            warning["meta"].get("includeErrors") == []
            and warning["meta"].get("sections", {}).get("relations", {}).get("capReached") is False
        )
        require(not complete, f"Linear {scenario} warning was classified complete")

    repeated_env = env | {"MI_LINEAR_GRAPH_SCENARIO": "repeated-cursor"}
    coverage, _ = linear_child_pages(repeated_env, "ENG-10")
    require(coverage == "partial", "Repeated Linear cursor did not produce partial coverage")

    failure_env = env | {"MI_LINEAR_GRAPH_SCENARIO": "pagination-failure"}
    coverage, _ = linear_child_pages(failure_env, "ENG-10")
    require(coverage == "partial", "Linear page failure did not produce partial coverage")

    cap_env = env | {"MI_LINEAR_GRAPH_SCENARIO": "cap"}
    coverage, nodes = linear_child_pages(cap_env, "ENG-10")
    require(
        coverage == "partial" and len(nodes) == CAP - 1,
        "Linear node cap did not count the root and stop at partial coverage",
    )
    entries = log_entries(log)
    for prefix in (
        ["linear", "relation", "add"],
        ["linear", "relation", "remove"],
        ["linear", "save-issue"],
    ):
        require(
            not command_positions(entries, prefix),
            f"Release A graph accepted Linear write: {' '.join(prefix)}",
        )
    require(
        json.loads(state.read_text(encoding="utf-8"))
        == json.loads((PROVIDER / "linear-graph.json").read_text(encoding="utf-8")),
        "Linear graph reads changed fixture state",
    )


def check_published_contract() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    require(
        "Release A treats every Linear topology mutation as `manual`" in text,
        "graph reference does not publish the Release A Linear manual boundary",
    )
    for command in (
        "orca linear save-issue",
        "orca linear relation add",
        "orca linear relation remove",
    ):
        require(command not in text, f"graph reference publishes Linear mutation command: {command}")
    for command in (
        "gh issue edit CHILD -R github.com/OWNER/REPO --parent PARENT",
        "gh issue edit BLOCKER -R github.com/OWNER/REPO --add-blocking BLOCKED",
    ):
        require(command in text, f"graph reference lacks host-qualified command: {command}")
    for command in (
        "gh issue edit CHILD --parent PARENT",
        "gh issue edit BLOCKER --add-blocking BLOCKED",
    ):
        require(command not in text, f"graph reference publishes unqualified mutation: {command}")


def main() -> int:
    for required in (REFERENCE, PROVIDER / "github-graph.json", PROVIDER / "linear-graph.json"):
        require(required.is_file(), f"missing U3 artifact: {required.relative_to(REPO_ROOT)}")
    check_published_contract()

    with tempfile.TemporaryDirectory(prefix="managing-issues-graph-") as temporary:
        root = Path(temporary)
        env = os.environ.copy()
        env["PATH"] = f"{BIN}{os.pathsep}{env.get('PATH', '')}"
        env["GH_HOST"] = "example.invalid"
        github_checks(root, env)
        linear_checks(root, env)

    print("PASS: managing-issues graph command seams")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, json.JSONDecodeError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
