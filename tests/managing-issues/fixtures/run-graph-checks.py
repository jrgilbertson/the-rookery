#!/usr/bin/env python3
"""Exercise the managing-issues graph contract and provider seams."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
BIN = HERE / "bin"
PROVIDER = HERE / "provider"
SKILL = REPO_ROOT / "skills/managing-issues/SKILL.md"
REFERENCE = REPO_ROOT / "skills/managing-issues/references/graph-and-completion.md"
GITHUB_REFERENCE = REPO_ROOT / "skills/managing-issues/references/github.md"
LINEAR_REFERENCE = REPO_ROOT / "skills/managing-issues/references/linear-and-sync.md"
WORKSPACE = "workspace-fixture"
GH_REPOSITORY = "github.com/example/project"
GH_BOUNDARY_REPOSITORY = "github.com/example/dependency"
READINESS = {
    "needs-discovery": "readiness:discovery",
    "needs-planning": "readiness:planning",
    "ready-for-implementation": "readiness:ready",
}
EFFECT_OUTCOMES = frozenset(
    {"applied", "already_satisfied", "failed", "indeterminate", "unapplied"}
)
PROCESSED_EFFECT_OUTCOMES = EFFECT_OUTCOMES - {"unapplied"}


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


def heading(body: str, name: str) -> str | None:
    lines = body.splitlines()
    wanted = f"## {name}".casefold()
    for index, line in enumerate(lines):
        if line.strip().casefold() != wanted:
            continue
        value: list[str] = []
        for candidate in lines[index + 1 :]:
            if candidate.startswith("## "):
                break
            value.append(candidate)
        rendered = "\n".join(value).strip()
        return rendered or None
    return None


def derive_readiness(body: str) -> str:
    if not heading(body, "Problem"):
        return "needs-discovery"
    if not heading(body, "Scope") or not heading(body, "Verification"):
        return "needs-planning"
    return "ready-for-implementation"


def intended_readiness_labels(labels: set[str], posture: str) -> set[str]:
    require(posture in READINESS, f"unknown readiness posture: {posture}")
    return (labels - set(READINESS.values())) | {READINESS[posture]}


@dataclass(frozen=True)
class Node:
    key: str
    body: str
    state: str = "open"
    children: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    estimate: int | None = None


def ready_frontier(nodes: dict[str, Node]) -> list[str]:
    return sorted(
        node.key
        for node in nodes.values()
        if node.state == "open"
        and not node.children
        and derive_readiness(node.body) == "ready-for-implementation"
        and all(nodes.get(blocker, Node(blocker, "")).state in {"completed", "canceled"} for blocker in node.blockers)
    )


def require_estimate_shape(nodes: dict[str, Node]) -> None:
    for node in nodes.values():
        require(
            not node.children or node.estimate is None,
            f"node with children has estimate: {node.key}",
        )


def coverage(
    pages: list[dict[str, Any]], *, accessible_boundary: bool = True, cap: int = 250
) -> tuple[str, list[str], str | None]:
    visited: set[str] = {"root"}
    seen_cursors: set[str] = set()
    for page in pages:
        for identity in page["identities"]:
            visited.add(identity)
            if len(visited) >= cap and page["has_more"]:
                return "partial", sorted(visited), "node limit reached before exhaustion"
        if not accessible_boundary:
            return "partial", sorted(visited), "required one-hop blocker inaccessible"
        if not page["has_more"]:
            return "complete", sorted(visited), None
        cursor = page.get("next_cursor")
        if not cursor or cursor in seen_cursors:
            return "partial", sorted(visited), "empty or repeated cursor"
        seen_cursors.add(cursor)
    return "partial", sorted(visited), "page sequence ended before exhaustion"


def graph_preview(
    provider: str,
    capabilities: set[str],
    effects: list[dict[str, str]],
) -> list[dict[str, str]]:
    required = {effect["capability"] for effect in effects}
    if not required <= capabilities:
        return []
    require(
        all(effect["kind"] == "node" for effect in effects[: sum(e["kind"] == "node" for e in effects)]),
        f"{provider} graph does not place nodes before edges",
    )
    return effects


def graph_execution(
    provider: str,
    capabilities: set[str],
    *,
    node_outcome: str = "applied",
) -> list[str]:
    events = [f"{provider}:capability-preflight"]
    if not {"create", "parent"} <= capabilities:
        return events
    events.append(f"{provider}:node-write")
    if node_outcome != "applied":
        events.append(f"{provider}:node-{node_outcome}")
        return events
    events.extend(
        [
            f"{provider}:node-readback",
            f"{provider}:edge-preflight",
            f"{provider}:edge-write",
            f"{provider}:endpoint-readbacks",
        ]
    )
    return events


def execute_batch(
    effects: list[str], outcomes: dict[str, str]
) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    stopped = False
    for effect in effects:
        if stopped:
            result.append((effect, "unapplied"))
            continue
        outcome = outcomes[effect]
        require(
            outcome in PROCESSED_EFFECT_OUTCOMES,
            f"unknown effect result: {outcome}",
        )
        result.append((effect, outcome))
        stopped = outcome in {"failed", "indeterminate"}
    return result


def canonical_identity(
    canonical: str,
    pairs: list[tuple[str, str]],
    selector: str,
) -> str | None:
    if canonical == "github":
        matches = [github for github, linear in pairs if selector in {github, linear}]
    else:
        matches = [linear for github, linear in pairs if selector in {github, linear}]
    return matches[0] if len(matches) == 1 else None


def synchronized_write(
    canonical: str,
    pairs: list[tuple[str, str]],
    selector: str,
) -> list[str]:
    target = canonical_identity(canonical, pairs, selector)
    return [] if target is None else [f"write:{canonical}:{target}"]


def completion_gaps(
    verification: tuple[str, ...], evidence: set[str]
) -> list[str]:
    return [criterion for criterion in verification if criterion not in evidence]


def lifecycle_preview(cascades: tuple[str, ...] | None) -> list[str]:
    if cascades is None:
        return []
    return ["canonical lifecycle change", *cascades]


def semantic_checks() -> None:
    complete = """## Problem
Users cannot save.
## Scope
Fix save and add a regression test.
## Verification
- The regression test passes.
"""
    missing_problem = """## Scope
Investigate the affected path.
## Verification
- The failure is reproduced.
"""
    missing_verification = """## Problem
Users cannot save.
## Scope
Fix the save path.
"""
    require(derive_readiness(complete) == "ready-for-implementation", "complete issue was not ready")
    require(derive_readiness(missing_problem) == "needs-discovery", "missing Problem was not discovery")
    require(derive_readiness(missing_verification) == "needs-planning", "missing Verification was not planning")

    corrected = intended_readiness_labels(
        {"bug", READINESS["needs-planning"]}, derive_readiness(complete)
    )
    require(
        corrected == {"bug", READINESS["ready-for-implementation"]},
        "stale planning label overrode derived ready posture",
    )
    corrected = intended_readiness_labels(
        {READINESS["ready-for-implementation"]}, derive_readiness(missing_verification)
    )
    require(
        corrected == {READINESS["needs-planning"]},
        "stale ready label overrode derived planning posture",
    )

    nodes = {
        "P": Node("P", complete, children=("A", "S")),
        "A": Node("A", complete, estimate=2),
        "S": Node("S", complete, children=("B", "C")),
        "B": Node("B", complete, estimate=3),
        "C": Node("C", complete, blockers=("A",), estimate=1),
    }
    require_estimate_shape(nodes)
    require(ready_frontier(nodes) == ["A", "B"], "Ready Frontier differs")
    require(
        ready_frontier({"solo": Node("solo", complete, estimate=1)}) == ["solo"],
        "standalone leaf acquired graph ceremony",
    )

    status, identities, gap = coverage(
        [
            {"identities": ["A", "B"], "has_more": True, "next_cursor": "c2"},
            {"identities": ["C"], "has_more": True, "next_cursor": "c2"},
        ]
    )
    require(status == "partial" and gap == "empty or repeated cursor", "repeated cursor was not partial")
    status, _, gap = coverage(
        [{"identities": ["A"], "has_more": False}], accessible_boundary=False
    )
    require(status == "partial" and "blocker" in (gap or ""), "missing boundary was not partial")
    status, identities, gap = coverage(
        [{"identities": [f"N-{index}" for index in range(249)], "has_more": True, "next_cursor": "more"}]
    )
    require(status == "partial" and len(identities) == 250 and "limit" in (gap or ""), "node cap was not partial")

    effects = [
        {"kind": "node", "capability": "create", "name": "parent"},
        {"kind": "node", "capability": "create", "name": "leaf"},
        {"kind": "edge", "capability": "parent", "name": "attach"},
        {"kind": "edge", "capability": "blocked-by", "name": "block"},
    ]
    for provider in ("github", "linear"):
        require(
            graph_preview(provider, {"create", "parent", "blocked-by"}, effects) == effects,
            f"{provider} supported graph did not preview",
        )
        require(
            graph_preview(provider, {"create", "parent"}, effects) == [],
            f"{provider} unsupported capability allowed a partial graph preview",
        )
        events = graph_execution(provider, {"create", "parent"})
        require(
            events.index(f"{provider}:node-readback")
            < events.index(f"{provider}:edge-write"),
            f"{provider} edge preceded exact node readback",
        )
        require(
            graph_execution(provider, {"create"})
            == [f"{provider}:capability-preflight"],
            f"{provider} unsupported edge capability allowed a node write",
        )
        require(
            f"{provider}:edge-write"
            not in graph_execution(
                provider, {"create", "parent"}, node_outcome="indeterminate"
            ),
            f"{provider} indeterminate node received an edge",
        )

    applied_then_failed = execute_batch(
        ["parent", "leaf", "attach", "independent-edge"],
        {
            "parent": "applied",
            "leaf": "applied",
            "attach": "failed",
            "independent-edge": "applied",
        },
    )
    require(
        applied_then_failed[-2:] == [("attach", "failed"), ("independent-edge", "unapplied")],
        "failed effect did not stop independent later effect",
    )
    indeterminate = execute_batch(
        ["create", "edge", "update"],
        {"create": "indeterminate", "edge": "applied", "update": "applied"},
    )
    require(
        indeterminate == [("create", "indeterminate"), ("edge", "unapplied"), ("update", "unapplied")],
        "indeterminate create did not stop all later effects",
    )
    require(
        execute_batch(
            ["create", "attach", "independent-edge"],
            {
                "create": "applied",
                "attach": "indeterminate",
                "independent-edge": "applied",
            },
        )
        == [
            ("create", "applied"),
            ("attach", "indeterminate"),
            ("independent-edge", "unapplied"),
        ],
        "indeterminate edge did not stop independent later effect",
    )
    already_satisfied = execute_batch(
        ["existing-edge", "next-effect"],
        {"existing-edge": "already_satisfied", "next-effect": "applied"},
    )
    require(
        already_satisfied == [
            ("existing-edge", "already_satisfied"),
            ("next-effect", "applied"),
        ],
        "already_satisfied effect did not retain the shared lifecycle outcome",
    )
    try:
        execute_batch(["legacy-effect"], {"legacy-effect": "succeeded"})
    except CheckFailure:
        pass
    else:
        require(False, "stale succeeded effect outcome was accepted")

    pairs = [("example/project#11", "ENG-11")]
    require(
        synchronized_write("github", pairs, "ENG-11")
        == ["write:github:example/project#11"],
        "Linear-to-GitHub route differs",
    )
    require(
        synchronized_write("linear", pairs, "example/project#11")
        == ["write:linear:ENG-11"],
        "GitHub-to-Linear route differs",
    )
    require(
        synchronized_write("github", [], "ENG-11") == [],
        "missing map allowed a synchronized write",
    )
    require(
        synchronized_write(
            "linear",
            [("example/project#11", "ENG-11"), ("example/other#7", "ENG-11")],
            "ENG-11",
        )
        == [],
        "ambiguous map allowed a synchronized write",
    )

    latest_verification = ("children are completed", "support confirms outcome")
    require(
        completion_gaps(latest_verification, {"children are completed"})
        == ["support confirms outcome"],
        "closed children incorrectly proved parent outcome",
    )
    require(
        execute_batch(
            ["edit-verification", "complete-parent"],
            {"edit-verification": "indeterminate", "complete-parent": "applied"},
        )[-1]
        == ("complete-parent", "unapplied"),
        "Verification edit and lifecycle change were combined after an unresolved readback",
    )
    require(
        lifecycle_preview(("complete parent", "close projection"))
        == [
            "canonical lifecycle change",
            "complete parent",
            "close projection",
        ],
        "observable lifecycle cascades were not explicit effects",
    )
    require(
        lifecycle_preview(None) == [],
        "unknown lifecycle cascades allowed an executable preview",
    )


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
    status, identities, gap = coverage(
        [{"identities": [boundary["url"]], "has_more": False}],
        accessible_boundary=True,
    )
    require(
        status == "complete" and boundary_url in identities and gap is None,
        "GitHub resolved cross-repository blocker did not complete coverage",
    )

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

    # The fixture guide deliberately does not specify graph mutation syntax.
    # Capability preflight therefore stops before any node or edge write.
    entries = log_entries(log)
    for prefix in (
        ("linear", "create"),
        ("linear", "save-issue"),
        ("linear", "relation"),
    ):
        require(
            all(tuple(entry["argv"][: len(prefix)]) != prefix for entry in entries),
            "unsupported Linear graph capability allowed a write",
        )
    require(state.read_text(encoding="utf-8") == original, "Linear capability probe changed state")


def published_contract_checks() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")
    required = (
        "shallowest useful",
        "capabilities before showing an executable graph preview",
        "nodes before relationships",
        "latest complete canonical readback",
        "never use a stored readiness representation as evidence",
        "exactly one",
        "Ready Frontier",
        "no estimate",
        "shared lifecycle's first-stop rule",
        "applied",
        "already_satisfied",
        "failed",
        "indeterminate",
        "unapplied",
        "provider/sync reference",
        "Never match by title",
        "separate batch",
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
        "vertical outcomes",
        "what can be demonstrated",
        "preferences and convenient ordering",
        "expand–migrate–contract",
        "compact decomposition check",
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
    normalized_linear = " ".join(linear.split())
    for fragment in (
        "Resolve one exact mapping entry",
        "top-level config provider alone selects write direction",
        "projection may be read for identity or lag evidence but never mutated",
    ):
        require(
            fragment in normalized_linear,
            f"Linear reference lacks synchronization contract: {fragment}",
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
    semantic_checks()
    published_contract_checks()

    with tempfile.TemporaryDirectory(prefix="managing-issues-graph-") as temporary:
        root = Path(temporary)
        env = os.environ.copy()
        env["PATH"] = f"{BIN}{os.pathsep}{env.get('PATH', '')}"
        github_command_checks(root, env)
        linear_command_checks(root, env)

    print("PASS: managing-issues graph contract")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, json.JSONDecodeError, OSError, StopIteration) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
