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


def github_checks(root: Path, base_env: dict[str, str]) -> None:
    state = root / "github.json"
    log = root / "github.log"
    shutil.copyfile(PROVIDER / "github-graph.json", state)
    env = base_env | {"MI_GITHUB_STATE": str(state), "MI_GITHUB_LOG": str(log)}

    children = succeeded(
        run(
            [
                "gh",
                "api",
                "repos/example/project/issues/10/sub_issues?per_page=100",
                "--paginate",
                "--slurp",
            ],
            env,
        ),
        "GitHub descendant pages",
    )
    flattened = [node for page in children for node in page]
    require([node["number"] for node in flattened] == [11, 12], "GitHub pages were not exhausted")

    blocked_by = succeeded(
        run(
            [
                "gh",
                "api",
                "repos/example/project/issues/12/dependencies/blocked_by?per_page=100",
                "--paginate",
                "--slurp",
            ],
            env,
        ),
        "GitHub blocker pages",
    )
    require(blocked_by[0][0]["number"] == 99, "GitHub one-hop boundary differs")
    boundary = succeeded(
        run(["gh", "issue", "view", "99", "-R", "example/project", "--json", "id,number,title,state"], env),
        "GitHub boundary read",
    )
    require(boundary["number"] == 99, "GitHub boundary identity differs")

    accepted(
        run(["gh", "issue", "edit", "11", "-R", "example/project", "--add-blocking", "12"], env),
        "GitHub relation add",
    )
    source = succeeded(
        run(["gh", "issue", "view", "11", "-R", "example/project", "--json", "id,number,blocking"], env),
        "GitHub relation source readback",
    )
    target = succeeded(
        run(["gh", "issue", "view", "12", "-R", "example/project", "--json", "id,number,blockedBy"], env),
        "GitHub relation target readback",
    )
    require([node["number"] for node in source["blocking"]] == [12], "GitHub blocking direction differs")
    require({node["number"] for node in target["blockedBy"]} == {11, 99}, "GitHub blocked-by direction differs")
    entries = log_entries(log)
    edits = command_positions(entries, ["issue", "edit"])
    views = command_positions(entries, ["issue", "view"])
    require(len(edits) == 1, "GitHub graph write was not exactly one attempt")
    require(sum(position > edits[0] for position in views) >= 2, "GitHub graph write lacks endpoint readbacks")

    accepted(run(["gh", "issue", "edit", "11", "-R", "example/project", "--remove-parent"], env), "GitHub parent removal")
    detached = succeeded(
        run(["gh", "issue", "view", "11", "-R", "example/project", "--json", "id,number,parent"], env),
        "GitHub detached child readback",
    )
    detached_parent = succeeded(
        run(["gh", "issue", "view", "10", "-R", "example/project", "--json", "id,number,subIssues"], env),
        "GitHub detached parent readback",
    )
    require(detached["parent"] is None and all(node["number"] != 11 for node in detached_parent["subIssues"]), "GitHub parent removal differs")
    accepted(run(["gh", "issue", "edit", "11", "-R", "example/project", "--parent", "10"], env), "GitHub parent restore")
    restored = succeeded(
        run(["gh", "issue", "view", "11", "-R", "example/project", "--json", "id,number,parent"], env),
        "GitHub restored child readback",
    )
    require(restored["parent"]["number"] == 10, "GitHub parent direction differs")

    failed_env = env | {"MI_GITHUB_GRAPH_SCENARIO": "unreadable-boundary"}
    failed(
        run(["gh", "issue", "view", "99", "-R", "example/project", "--json", "id,number,title,state"], failed_env),
        "required boundary is inaccessible",
        "GitHub inaccessible boundary",
    )


def linear_child_pages(env: dict[str, str], parent: str) -> tuple[str, list[dict[str, Any]]]:
    cursor: str | None = None
    seen_cursors: set[str] = set()
    nodes: list[dict[str, Any]] = []
    while True:
        argv = ["orca", "linear", "list-issues", "--parent-id", parent, "--limit", "100", "--json"]
        if cursor is not None:
            argv.extend(["--cursor", cursor])
        result = run(argv, env)
        if result.returncode != 0:
            return "partial", nodes
        page = json.loads(result.stdout)
        page_nodes = page["issues"]
        if len(nodes) + len(page_nodes) > CAP:
            return "partial", nodes
        nodes.extend(page_nodes)
        page_info = page["pageInfo"]
        if len(nodes) == CAP and page_info["hasNextPage"]:
            return "partial", nodes
        if not page_info["hasNextPage"]:
            return "complete", nodes
        next_cursor = page_info.get("endCursor")
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

    relation_read = succeeded(
        run(["orca", "linear", "issue", "ENG-12", "--relations", "--json"], env),
        "Linear relation read",
    )
    require(relation_read["issue"]["relations"][0]["issue"]["identifier"] == "ENG-99", "Linear boundary differs")

    succeeded(
        run(
            ["orca", "linear", "relation", "add", "ENG-11", "--related", "ENG-12", "--type", "blocks", "--json"],
            env,
        ),
        "Linear relation add",
    )
    source = succeeded(run(["orca", "linear", "issue", "ENG-11", "--relations", "--json"], env), "Linear source readback")
    target = succeeded(run(["orca", "linear", "issue", "ENG-12", "--relations", "--json"], env), "Linear target readback")
    require(any(edge["type"] == "blocks" and edge["issue"]["identifier"] == "ENG-12" for edge in source["issue"]["relations"]), "Linear blocks direction differs")
    require(any(edge["type"] == "blocked-by" and edge["issue"]["identifier"] == "ENG-11" for edge in target["issue"]["relations"]), "Linear blocked-by direction differs")
    entries = log_entries(log)
    relations = command_positions(entries, ["linear", "relation", "add"])
    reads = command_positions(entries, ["linear", "issue"])
    require(len(relations) == 1, "Linear graph write was not exactly one attempt")
    require(sum(position > relations[0] for position in reads) >= 2, "Linear graph write lacks endpoint readbacks")

    succeeded(
        run(["orca", "linear", "save-issue", "ENG-11", "--parent-id", "null", "--json"], env),
        "Linear parent removal",
    )
    detached = succeeded(run(["orca", "linear", "issue", "ENG-11", "--json"], env), "Linear detached child readback")
    detached_parent = succeeded(run(["orca", "linear", "issue", "ENG-10", "--json"], env), "Linear detached parent readback")
    require(detached["issue"]["parent"] is None, "Linear child still has parent")
    require(all(node["identifier"] != "ENG-11" for node in detached_parent["issue"]["children"]), "Linear parent still has child")
    succeeded(
        run(["orca", "linear", "save-issue", "ENG-11", "--parent-id", "ENG-10", "--json"], env),
        "Linear parent restore",
    )
    restored = succeeded(run(["orca", "linear", "issue", "ENG-11", "--json"], env), "Linear restored child readback")
    require(restored["issue"]["parent"]["identifier"] == "ENG-10", "Linear parent direction differs")

    repeated_env = env | {"MI_LINEAR_GRAPH_SCENARIO": "repeated-cursor"}
    coverage, _ = linear_child_pages(repeated_env, "ENG-10")
    require(coverage == "partial", "Repeated Linear cursor did not produce partial coverage")

    failure_env = env | {"MI_LINEAR_GRAPH_SCENARIO": "pagination-failure"}
    coverage, _ = linear_child_pages(failure_env, "ENG-10")
    require(coverage == "partial", "Linear page failure did not produce partial coverage")

    cap_env = env | {"MI_LINEAR_GRAPH_SCENARIO": "cap"}
    coverage, nodes = linear_child_pages(cap_env, "ENG-10")
    require(coverage == "partial" and len(nodes) == CAP, "Node cap did not stop at partial coverage")


def main() -> int:
    for required in (REFERENCE, PROVIDER / "github-graph.json", PROVIDER / "linear-graph.json"):
        require(required.is_file(), f"missing U3 artifact: {required.relative_to(REPO_ROOT)}")

    with tempfile.TemporaryDirectory(prefix="managing-issues-graph-") as temporary:
        root = Path(temporary)
        env = os.environ.copy()
        env["PATH"] = f"{BIN}{os.pathsep}{env.get('PATH', '')}"
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
