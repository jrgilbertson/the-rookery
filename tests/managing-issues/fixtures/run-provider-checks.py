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
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
BIN = HERE / "bin"
PROVIDER = HERE / "provider"
POLICIES = HERE / "policy"
SYNC_MAPPINGS = HERE / "sync-mapping"
SKILL = REPO_ROOT / "skills" / "managing-issues" / "SKILL.md"
REFERENCES = SKILL.parent / "references"
POLICY_CHECK = SKILL.parent / "scripts" / "policy_check.py"
REPOSITORY = "example/project"
GH_REPOSITORY = f"github.com/{REPOSITORY}"
WORKSPACE = "workspace-fixture"
TEAM = "ENG"
ISSUE_FIELDS = (
    "id,number,title,body,state,stateReason,updatedAt,url,labels,assignees,"
    "issueType,parent,subIssues,blockedBy,blocking"
)
REPOSITORY_FIELDS = "id,nameWithOwner,url,hasIssuesEnabled,isArchived,viewerPermission"
ISSUE_TYPES_QUERY = (
    "query($owner:String!,$name:String!,$endCursor:String){"
    "repository(owner:$owner,name:$name){issueTypes(first:100,after:$endCursor){"
    "nodes{id name}pageInfo{hasNextPage endCursor}}}}"
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


def succeeded(result: subprocess.CompletedProcess[str], label: str) -> Any:
    require(result.returncode == 0, f"{label} failed: {result.stderr.strip()}")
    require(result.stderr == "", f"{label} wrote stderr")
    return json.loads(result.stdout)


def accepted(result: subprocess.CompletedProcess[str], label: str) -> str:
    require(result.returncode == 0, f"{label} failed: {result.stderr.strip()}")
    require(result.stderr == "", f"{label} wrote stderr")
    return result.stdout.strip()


def failed(result: subprocess.CompletedProcess[str], fragment: str, label: str) -> None:
    require(result.returncode != 0, f"{label} unexpectedly succeeded")
    require(fragment in result.stderr, f"{label} failed for wrong reason: {result.stderr.strip()}")


def rejected_check(action: Callable[[], Any], fragment: str, label: str) -> None:
    try:
        action()
    except CheckFailure as error:
        require(fragment in str(error), f"{label} failed for wrong reason: {error}")
    else:
        raise CheckFailure(f"{label} unexpectedly succeeded")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def log_entries(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def command_positions(entries: list[dict[str, Any]], prefix: list[str]) -> list[int]:
    return [index for index, entry in enumerate(entries) if entry["argv"][: len(prefix)] == prefix]


def assert_effect_sequence(
    entries: list[dict[str, Any]],
    start: int,
    write_prefix: list[str],
    required_prefixes: list[list[str]],
    *,
    readback_prefix: list[str] | None = None,
) -> None:
    window = entries[start:]
    write_positions = command_positions(window, write_prefix)
    require(
        len(write_positions) == 1,
        f"expected one write command after checkpoint: {' '.join(write_prefix)}",
    )
    write = write_positions[0]
    for prefix in required_prefixes:
        require(
            any(
                index < write and entry["argv"][: len(prefix)] == prefix
                for index, entry in enumerate(window)
            ),
            f"write {' '.join(write_prefix)} lacks fresh {' '.join(prefix)} preflight",
        )
    if readback_prefix is not None:
        require(
            any(
                index > write and entry["argv"][: len(readback_prefix)] == readback_prefix
                for index, entry in enumerate(window)
            ),
            f"write {' '.join(write_prefix)} lacks authoritative readback",
        )


def normalized_policy(
    root: Path,
    fixture: Path,
    env: dict[str, str],
    *,
    mapping: Path | None = None,
) -> dict[str, Any]:
    policy_root = root / fixture.stem
    agents = policy_root / ".agents"
    agents.mkdir(parents=True)
    policy = agents / "managing-issues.json"
    shutil.copyfile(fixture, policy)
    if mapping is not None:
        shutil.copyfile(mapping, agents / "linear-sync.json")
    result = succeeded(
        run(
            [
                sys.executable,
                str(POLICY_CHECK),
                "--repo-root",
                str(policy_root),
                "--policy",
                str(policy),
            ],
            env,
        ),
        f"normalize {fixture.name}",
    )
    return result["policy"]


def canonical_issue_number(selector: str, repository_url: str) -> int:
    prefix = f"{repository_url.rstrip('/')}/issues/"
    if selector.isdigit() and int(selector) > 0:
        return int(selector)
    if selector.startswith(prefix):
        suffix = selector[len(prefix):]
        if suffix.isdigit() and int(suffix) > 0:
            return int(suffix)
    raise CheckFailure("GitHub issue repository identity differs")


def github_preflight(
    env: dict[str, str],
    *,
    issue: str | None = None,
    label: str | None = None,
    assignee: str | None = None,
    issue_type: str | None = None,
) -> str:
    auth = succeeded(
        run(
            [
                "gh", "auth", "status", "--active", "--hostname", "github.com",
                "--json", "hosts",
            ],
            env,
        ),
        "GitHub auth",
    )
    accounts = auth.get("hosts", {}).get("github.com", [])
    active = [
        account
        for account in accounts
        if account.get("active") is True and account.get("state") == "success"
    ]
    require(len(active) == 1, "GitHub auth did not return one successful active account")
    principal = active[0].get("login")
    require(principal == "fixture-user", "GitHub auth principal differs")

    repository = succeeded(
        run(
            ["gh", "repo", "view", GH_REPOSITORY, "--json", REPOSITORY_FIELDS],
            env,
        ),
        "GitHub repository identity",
    )
    require(
        repository["nameWithOwner"] == REPOSITORY
        and repository["hasIssuesEnabled"]
        and not repository["isArchived"]
        and repository["viewerPermission"] in {"ADMIN", "MAINTAIN", "WRITE"},
        "GitHub repository preflight differs",
    )
    if label is not None:
        labels = succeeded(
            run(
                ["gh", "label", "list", "-R", GH_REPOSITORY, "--limit", "1000", "--json", "id,name"],
                env,
            ),
            "GitHub label preflight",
        )
        require(len(labels) < 1000, "GitHub label coverage reached the installed limit")
        require(sum(item["name"] == label for item in labels) == 1, "GitHub label differs")
    if issue_type is not None:
        cursor: str | None = None
        seen_cursors: set[str] = set()
        items: list[dict[str, Any]] = []
        while True:
            argv = [
                "gh", "api", "graphql", "--hostname", "github.com",
                "-f", f"query={ISSUE_TYPES_QUERY}",
                "-F", "owner=example", "-F", "name=project",
            ]
            if cursor is not None:
                argv.extend(["-F", f"endCursor={cursor}"])
            page = succeeded(run(argv, env), "GitHub issue-type preflight")
            connection = page["data"]["repository"]["issueTypes"]
            require(connection is not None, "GitHub issue-type coverage differs")
            items.extend(connection["nodes"])
            page_info = connection["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            next_cursor = page_info.get("endCursor")
            require(
                bool(next_cursor) and next_cursor not in seen_cursors,
                "GitHub issue-type cursor differs",
            )
            seen_cursors.add(next_cursor)
            cursor = next_cursor
        matches = [item for item in items if item["name"] == issue_type]
        require(len(matches) == 1, "GitHub issue type differs")
    if assignee is not None:
        accepted(
            run(["gh", "api", f"repos/{REPOSITORY}/assignees/{assignee}", "--hostname", "github.com", "--silent"], env),
            "GitHub assignee preflight",
        )
    if issue is not None:
        expected_number = canonical_issue_number(issue, repository["url"])
        current = succeeded(
            run(["gh", "issue", "view", issue, "-R", GH_REPOSITORY, "--json", ISSUE_FIELDS], env),
            "GitHub issue pre-read",
        )
        require(
            current["number"] == expected_number
            and current["url"] == f"{repository['url'].rstrip('/')}/issues/{expected_number}",
            "GitHub issue repository identity differs",
        )
    return principal


def github_checks(root: Path, env: dict[str, str]) -> None:
    policy = normalized_policy(root, POLICIES / "valid-github.json", env)
    require(
        policy["provider"] == "github" and policy["target"] == REPOSITORY,
        "normalized GitHub policy route differs",
    )
    mappings = policy["mappings"]
    state = root / "github.json"
    log = root / "github.log"
    shutil.copyfile(PROVIDER / "github.json", state)
    github_env = env | {
        "GH_HOST": "example.invalid",
        "MI_GITHUB_STATE": str(state),
        "MI_GITHUB_LOG": str(log),
        "MI_GITHUB_ISSUE_TYPES_SCENARIO": "paged",
    }

    for scenario in ("archived", "issues-disabled", "read-only"):
        rejected_check(
            lambda scenario=scenario: github_preflight(
                github_env | {"MI_GITHUB_REPOSITORY_SCENARIO": scenario}
            ),
            "repository preflight differs",
            f"GitHub {scenario} repository",
        )
    rejected_check(
        lambda: github_preflight(
            github_env | {"MI_GITHUB_LABEL_SCENARIO": "limit-reached"},
            label=mappings["priority"]["high"],
        ),
        "label coverage reached",
        "GitHub label limit",
    )
    rejected_check(
        lambda: github_preflight(
            github_env,
            issue="https://github.com/foreign/project/issues/1",
        ),
        "issue repository identity differs",
        "GitHub foreign issue URL",
    )
    rejected_check(
        lambda: github_preflight(
            github_env | {"MI_GITHUB_ISSUE_TYPES_SCENARIO": "unavailable"},
            issue_type=mappings["work_type"]["bug"],
        ),
        "issue-type coverage differs",
        "GitHub issue-type availability",
    )

    checkpoint = len(log_entries(log))
    github_preflight(
        github_env,
        issue="1",
        label=mappings["readiness"]["ready"],
        assignee="fixture-user",
        issue_type=mappings["work_type"]["bug"],
    )
    accepted(
        run(
            [
                "gh", "issue", "edit", "1", "-R", GH_REPOSITORY,
                "--title", "Updated issue", "--body-file", "-",
                "--add-label", mappings["readiness"]["ready"],
                "--add-assignee", "fixture-user",
                "--type", mappings["work_type"]["bug"],
            ],
            github_env,
            stdin="## Problem\n\nUpdated text\n",
        ),
        "GitHub update",
    )
    after = succeeded(
        run(["gh", "issue", "view", "1", "-R", GH_REPOSITORY, "--json", ISSUE_FIELDS], github_env),
        "GitHub update readback",
    )
    require(
        after["title"] == "Updated issue"
        and "Updated text" in after["body"]
        and any(item["name"] == mappings["readiness"]["ready"] for item in after["labels"])
        and after["assignees"][0]["login"] == "fixture-user"
        and after["issueType"]["name"] == mappings["work_type"]["bug"],
        "GitHub update readback differs",
    )
    assert_effect_sequence(
        log_entries(log),
        checkpoint,
        ["issue", "edit", "1"],
        [
            ["auth", "status"],
            ["repo", "view"],
            ["label", "list"],
            ["api", "graphql"],
            ["api", f"repos/{REPOSITORY}/assignees/fixture-user"],
            ["issue", "view", "1"],
        ],
        readback_prefix=["issue", "view", "1"],
    )

    checkpoint = len(log_entries(log))
    github_preflight(
        github_env,
        issue="1",
        label=mappings["priority"]["high"],
        assignee="fixture-user",
        issue_type=mappings["work_type"]["feature"],
    )
    create_snapshot = state.read_bytes()
    failed(
        run(
            [
                "gh", "issue", "create", "-R", GH_REPOSITORY,
                "--title", "Unsafe bundled edge", "--body-file", "-",
                "--blocked-by", "1",
            ],
            github_env,
            stdin="body\n",
        ),
        "relationship flags are not allowed during create",
        "GitHub create-time relationship",
    )
    require(state.read_bytes() == create_snapshot, "rejected create-time relationship changed state")
    checkpoint = len(log_entries(log))
    github_preflight(
        github_env,
        issue="1",
        label=mappings["priority"]["high"],
        assignee="fixture-user",
        issue_type=mappings["work_type"]["feature"],
    )
    created_url = accepted(
        run(
            [
                "gh", "issue", "create", "-R", GH_REPOSITORY,
                "--title", "Created issue", "--body-file", "-",
                "--label", mappings["priority"]["high"],
                "--assignee", "fixture-user",
                "--type", mappings["work_type"]["feature"],
            ],
            github_env,
            stdin="## Problem\n\nCreated text\n",
        ),
        "GitHub create",
    )
    require(created_url.endswith("/issues/3"), "GitHub create identity differs")
    created = succeeded(
        run(["gh", "issue", "view", created_url, "-R", GH_REPOSITORY, "--json", ISSUE_FIELDS], github_env),
        "GitHub create readback",
    )
    require(
        created["title"] == "Created issue"
        and created["labels"][0]["name"] == mappings["priority"]["high"]
        and created["issueType"]["name"] == mappings["work_type"]["feature"]
        and created["blockedBy"] == [],
        "GitHub created issue differs",
    )
    assert_effect_sequence(
        log_entries(log),
        checkpoint,
        ["issue", "create"],
        [
            ["auth", "status"],
            ["repo", "view"],
            ["label", "list"],
            ["api", "graphql"],
            ["api", f"repos/{REPOSITORY}/assignees/fixture-user"],
            ["issue", "view", "1"],
        ],
        readback_prefix=["issue", "view", created_url],
    )

    checkpoint = len(log_entries(log))
    github_preflight(github_env, issue="3")
    accepted(
        run(["gh", "issue", "close", "3", "-R", GH_REPOSITORY, "--reason", "not planned"], github_env),
        "GitHub cancel",
    )
    canceled = succeeded(
        run(["gh", "issue", "view", "3", "-R", GH_REPOSITORY, "--json", ISSUE_FIELDS], github_env),
        "GitHub cancel readback",
    )
    require(canceled["stateReason"] == "NOT_PLANNED", "GitHub cancel reason differs")
    assert_effect_sequence(
        log_entries(log),
        checkpoint,
        ["issue", "close", "3"],
        [["auth", "status"], ["repo", "view"], ["issue", "view", "3"]],
        readback_prefix=["issue", "view", "3"],
    )
    checkpoint = len(log_entries(log))
    github_preflight(github_env, issue="3")
    accepted(run(["gh", "issue", "reopen", "3", "-R", GH_REPOSITORY], github_env), "GitHub reopen")
    reopened = succeeded(
        run(["gh", "issue", "view", "3", "-R", GH_REPOSITORY, "--json", ISSUE_FIELDS], github_env),
        "GitHub reopen readback",
    )
    require(reopened["state"] == "OPEN" and reopened["stateReason"] is None, "GitHub reopen differs")
    assert_effect_sequence(
        log_entries(log),
        checkpoint,
        ["issue", "reopen", "3"],
        [["auth", "status"], ["repo", "view"], ["issue", "view", "3"]],
        readback_prefix=["issue", "view", "3"],
    )

    snapshot = state.read_bytes()
    failed(
        run(["gh", "issue", "edit", "1", "-R", "github.com/example/shadow", "--title", "Wrong target"], github_env),
        "shadow repository is read-only",
        "GitHub shadow write",
    )
    failed(
        run(["gh", "issue", "edit", "1", "-R", GH_REPOSITORY, "--label", "bug"], github_env),
        "unsupported flag: --label",
        "GitHub create-only edit flag",
    )
    failed(
        run(["gh", "issue", "close", "1", "-R", GH_REPOSITORY], github_env),
        "missing --reason",
        "GitHub bare close",
    )
    failed(run(["gh", "issue", "delete", "1", "-R", GH_REPOSITORY], github_env), "unsupported command", "GitHub delete")
    require(state.read_bytes() == snapshot, "GitHub rejected commands changed state")

    indeterminate_state = root / "github-indeterminate.json"
    indeterminate_log = root / "github-indeterminate.log"
    shutil.copyfile(PROVIDER / "github.json", indeterminate_state)
    indeterminate_env = github_env | {
        "MI_GITHUB_STATE": str(indeterminate_state),
        "MI_GITHUB_LOG": str(indeterminate_log),
        "MI_GITHUB_INDETERMINATE_CREATE": "1",
    }
    checkpoint = len(log_entries(indeterminate_log))
    github_preflight(indeterminate_env)
    failed(
        run(
            ["gh", "issue", "create", "-R", GH_REPOSITORY, "--title", "Unconfirmed", "--body-file", "-"],
            indeterminate_env,
            stdin="body\n",
        ),
        "create outcome is indeterminate",
        "GitHub indeterminate create",
    )
    require(load_json(indeterminate_state)["next_issue"] == 4, "GitHub indeterminate state differs")
    require(
        load_json(indeterminate_state)["issues"]["3"]["blockedBy"] == [],
        "GitHub indeterminate create gained a dependent edge",
    )
    require(
        len(command_positions(log_entries(indeterminate_log), ["issue", "create"])) == 1,
        "GitHub indeterminate create was not exactly one attempt",
    )
    require(
        len(command_positions(log_entries(indeterminate_log), ["issue", "edit"])) == 0,
        "GitHub indeterminate create triggered a dependent relationship",
    )
    assert_effect_sequence(
        log_entries(indeterminate_log),
        checkpoint,
        ["issue", "create"],
        [["auth", "status"], ["repo", "view"]],
    )

    rejected_state = root / "github-rejected.json"
    rejected_log = root / "github-rejected.log"
    shutil.copyfile(PROVIDER / "github.json", rejected_state)
    rejected_env = github_env | {
        "MI_GITHUB_STATE": str(rejected_state),
        "MI_GITHUB_LOG": str(rejected_log),
        "MI_GITHUB_REJECTED_CREATE": "1",
    }
    github_preflight(rejected_env)
    failed(
        run(
            ["gh", "issue", "create", "-R", GH_REPOSITORY, "--title", "Rejected", "--body-file", "-"],
            rejected_env,
            stdin="body\n",
        ),
        "create rejected before persistence",
        "GitHub rejected create",
    )
    require(
        load_json(rejected_state) == load_json(PROVIDER / "github.json"),
        "GitHub rejected create changed state",
    )
    require(
        len(command_positions(log_entries(rejected_log), ["issue", "create"])) == 1,
        "GitHub rejected create was not exactly one attempt",
    )

    drift_state = root / "github-drift.json"
    drift_log = root / "github-drift.log"
    shutil.copyfile(PROVIDER / "github.json", drift_state)
    drift_env = github_env | {
        "MI_GITHUB_STATE": str(drift_state),
        "MI_GITHUB_LOG": str(drift_log),
        "MI_GITHUB_DRIFT_AFTER_WRITES": "1",
    }
    checkpoint = len(log_entries(drift_log))
    github_preflight(drift_env, issue="1")
    accepted(
        run(["gh", "issue", "edit", "1", "-R", GH_REPOSITORY, "--title", "First effect"], drift_env),
        "GitHub drift first effect",
    )
    succeeded(
        run(["gh", "issue", "view", "1", "-R", GH_REPOSITORY, "--json", ISSUE_FIELDS], drift_env),
        "GitHub drift first readback",
    )
    assert_effect_sequence(
        log_entries(drift_log),
        checkpoint,
        ["issue", "edit", "1"],
        [["auth", "status"], ["repo", "view"], ["issue", "view", "1"]],
        readback_prefix=["issue", "view", "1"],
    )
    before_drift_stop = drift_state.read_bytes()
    try:
        github_preflight(drift_env, issue="1")
    except CheckFailure as error:
        require("principal differs" in str(error), "GitHub drift stopped for the wrong reason")
    else:
        raise CheckFailure("GitHub identity drift was not detected")
    require(drift_state.read_bytes() == before_drift_stop, "GitHub drift detection changed state")
    require(
        len(command_positions(log_entries(drift_log), ["issue", "edit"])) == 1,
        "GitHub drift did not stop the later write",
    )



def linear_result(result: subprocess.CompletedProcess[str], label: str) -> dict[str, Any]:
    response = succeeded(result, label)
    require(
        set(response) == {"id", "ok", "result", "_meta"},
        f"{label} RPC envelope differs",
    )
    require(response["ok"] is True, f"{label} RPC response is not successful")
    require(isinstance(response["result"], dict), f"{label} result differs")
    return response["result"]


def linear_priority(value: Any) -> str:
    priorities = {0: "none", 1: "urgent", 2: "high", 3: "medium", 4: "low"}
    require(
        isinstance(value, int) and not isinstance(value, bool) and value in priorities,
        "Linear priority value differs",
    )
    return priorities[value]


def assert_no_linear_mutation(entries: list[dict[str, Any]]) -> None:
    mutation_prefixes = (
        ["linear", "create"],
        ["linear", "save-issue"],
        ["linear", "relation", "add"],
        ["linear", "relation", "remove"],
        ["linear", "status", "set"],
        ["linear", "priority", "set"],
        ["linear", "estimate", "set"],
        ["linear", "assignee", "set"],
        ["linear", "label", "add"],
        ["linear", "label", "remove"],
        ["linear", "comment", "add"],
        ["linear", "attach"],
    )
    for prefix in mutation_prefixes:
        require(
            not command_positions(entries, list(prefix)),
            f"Release A accepted Linear mutation route: {' '.join(prefix)}",
        )


def linear_checks(root: Path, env: dict[str, str]) -> None:
    policy = normalized_policy(
        root,
        POLICIES / "valid-linear-sync.json",
        env,
        mapping=SYNC_MAPPINGS / "valid.json",
    )
    require(
        policy["provider"] == "linear"
        and policy["target"] == {"workspace": WORKSPACE, "team": TEAM},
        "normalized Linear policy route differs",
    )
    state = root / "linear.json"
    log = root / "linear.log"
    shutil.copyfile(PROVIDER / "linear.json", state)
    linear_env = env | {"MI_LINEAR_STATE": str(state), "MI_LINEAR_LOG": str(log)}

    failed(
        run(["orca", "linear", "team", "list", "--workspace", "workspace-other", "--json"], linear_env),
        f"fixture requires --workspace {WORKSPACE}",
        "Linear wrong workspace",
    )
    teams = linear_result(
        run(["orca", "linear", "team", "list", "--workspace", WORKSPACE, "--json"], linear_env),
        "Linear team read",
    )
    require(
        "principal" not in teams
        and "workspace" not in teams
        and teams["meta"]["workspaceErrors"] == []
        and len([team for team in teams["teams"] if team["key"] == TEAM]) == 1
        and teams["teams"][0]["workspace"]["id"] == WORKSPACE,
        "Linear team/workspace metadata differs",
    )
    states = linear_result(
        run(["orca", "linear", "team", "states", "--team", TEAM, "--workspace", WORKSPACE, "--json"], linear_env),
        "Linear states read",
    )
    labels = linear_result(
        run(["orca", "linear", "team", "labels", "--team", TEAM, "--workspace", WORKSPACE, "--json"], linear_env),
        "Linear labels read",
    )
    members = linear_result(
        run(["orca", "linear", "team", "members", "--team", TEAM, "--workspace", WORKSPACE, "--json"], linear_env),
        "Linear members read",
    )
    issue = linear_result(
        run(["orca", "linear", "issue", "ENG-1", "--relations", "--workspace", WORKSPACE, "--json"], linear_env),
        "Linear issue read",
    )
    require(states["team"]["key"] == TEAM and len(states["states"]) == 4, "Linear states differ")
    require(labels["team"]["key"] == TEAM and len(labels["labels"]) == 2, "Linear labels differ")
    require(members["team"]["key"] == TEAM and len(members["members"]) == 2, "Linear members differ")
    require(
        issue["issue"]["identifier"] == "ENG-1"
        and linear_priority(issue["issue"]["priority"]) == policy["mappings"]["priority"]["high"]
        and issue["meta"]["sections"]["relations"]["capReached"] is False,
        "Linear issue metadata differs",
    )
    assert_no_linear_mutation(log_entries(log))
    require(load_json(state) == load_json(PROVIDER / "linear.json"), "Linear reads changed fixture state")


def check_published_contract() -> None:
    text = SKILL.read_text(encoding="utf-8")
    github_text = (REFERENCES / "github.md").read_text(encoding="utf-8")
    linear_text = (REFERENCES / "linear-and-sync.md").read_text(encoding="utf-8")
    enum = "`applied`, `already_satisfied`, `failed`, `indeterminate`, or `manual`"
    require(enum in text, "SKILL.md does not publish the exact effect-outcome enum")
    for legacy in ("`Applied`", "`Already satisfied`", "`Failed`", "`Indeterminate`", "`Manual`"):
        require(legacy not in text, f"SKILL.md retains legacy outcome spelling {legacy}")
    require(
        "Classify every proposed Linear mutation as `manual`" in linear_text
        and "do not construct or invoke a Linear" in linear_text,
        "Linear reference does not publish the Release A manual boundary",
    )
    require(
        "node-only effect" in github_text
        and "only after every new node" in github_text,
        "GitHub reference does not publish create-before-relationship ordering",
    )


def main() -> int:
    for required in (
        BIN / "gh",
        BIN / "orca",
        REFERENCES / "github.md",
        REFERENCES / "linear-and-sync.md",
    ):
        require(required.is_file(), f"missing provider artifact: {required.relative_to(REPO_ROOT)}")
    require(os.access(BIN / "gh", os.X_OK), "fixture gh is not executable")
    require(os.access(BIN / "orca", os.X_OK), "fixture orca is not executable")
    check_published_contract()

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
        print(f"FAIL: {error}", file=os.sys.stderr)
        raise SystemExit(1)
