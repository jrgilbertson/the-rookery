#!/usr/bin/env python3
"""Exercise Managing Issues provider/config lifecycle contracts."""

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
SKILL_DIR = REPO_ROOT / "skills" / "managing-issues"
SKILL = SKILL_DIR / "SKILL.md"
GITHUB_REF = SKILL_DIR / "references" / "github.md"
LINEAR_REF = SKILL_DIR / "references" / "linear.md"
CONFIG_CHECK = SKILL_DIR / "scripts" / "config_check.py"
GH_TARGET = "github.com/example/project"
GH_REPOSITORY_URL = "https://github.com/example/project"
LINEAR_WORKSPACE = "workspace-fixture"
LINEAR_TEAM = "ENG"
ISSUE_FIELDS = "id,number,title,body,state,stateReason,updatedAt,url,labels,assignees,issueType,parent,subIssues,blockedBy,blocking"
REPOSITORY_FIELDS = "id,nameWithOwner,url,hasIssuesEnabled,isArchived,viewerPermission"


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def run(argv: list[str], env: dict[str, str], *, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, input=stdin, text=True, capture_output=True, check=False, env=env)


def accepted(result: subprocess.CompletedProcess[str], label: str) -> str:
    require(result.returncode == 0, f"{label} failed: {result.stderr.strip()}")
    require(result.stderr == "", f"{label} wrote stderr")
    return result.stdout.strip()


def json_result(result: subprocess.CompletedProcess[str], label: str) -> Any:
    return json.loads(accepted(result, label))


def linear_result(result: subprocess.CompletedProcess[str], label: str) -> dict[str, Any]:
    envelope = json_result(result, label)
    require(set(envelope) == {"id", "ok", "result", "_meta"}, f"{label} envelope differs")
    require(envelope["ok"] is True and isinstance(envelope["result"], dict), f"{label} failed")
    return envelope["result"]


def failed(result: subprocess.CompletedProcess[str], fragment: str, label: str) -> None:
    require(result.returncode != 0, f"{label} unexpectedly succeeded")
    require(fragment in result.stderr, f"{label} failed for wrong reason: {result.stderr.strip()}")


def log_entries(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def positions(entries: list[dict[str, Any]], prefix: list[str]) -> list[int]:
    return [index for index, entry in enumerate(entries) if entry["argv"][: len(prefix)] == prefix]


def assert_once_between(entries: list[dict[str, Any]], write_prefix: list[str], before_prefix: list[str], after_prefix: list[str]) -> None:
    writes = positions(entries, write_prefix)
    require(len(writes) == 1, f"expected one {' '.join(write_prefix)}")
    write = writes[0]
    require(any(index < write for index in positions(entries, before_prefix)), f"missing fresh {' '.join(before_prefix)}")
    require(any(index > write for index in positions(entries, after_prefix)), f"missing readback {' '.join(after_prefix)}")


def add_fixture_metadata(path: Path) -> None:
    state = json.loads(path.read_text(encoding="utf-8"))
    if "repository" in state:
        state["metadata"]["labels"].append({"id": "LA_hostile", "name": "--literal;$(never-run)"})
    else:
        state["labels"].extend([
            {"id": "label-ready", "name": "Ready for implementation"},
            {"id": "label-hostile", "name": "--literal;$(never-run)"},
        ])
        state["fixtureWriteCount"] = 0
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def github_env(root: Path, base: dict[str, str], name: str, **extra: str) -> tuple[dict[str, str], Path, Path]:
    state = root / f"{name}.json"
    log = root / f"{name}.log"
    shutil.copyfile(PROVIDER / "github.json", state)
    add_fixture_metadata(state)
    return base | {"MI_GITHUB_STATE": str(state), "MI_GITHUB_LOG": str(log), **extra}, state, log


def linear_env(root: Path, base: dict[str, str], name: str, **extra: str) -> tuple[dict[str, str], Path, Path]:
    state = root / f"{name}.json"
    log = root / f"{name}.log"
    shutil.copyfile(PROVIDER / "linear.json", state)
    add_fixture_metadata(state)
    return base | {"MI_LINEAR_STATE": str(state), "MI_LINEAR_LOG": str(log), **extra}, state, log


def github_auth_and_target(env: dict[str, str]) -> dict[str, Any]:
    auth = json_result(run(["gh", "auth", "status", "--active", "--hostname", "github.com", "--json", "hosts"], env), "GitHub auth")
    active = [account for account in auth.get("hosts", {}).get("github.com", []) if account.get("active") is True and account.get("state") == "success"]
    require(len(active) == 1, "GitHub auth did not return one active account")
    repository = json_result(run(["gh", "repo", "view", GH_TARGET, "--json", REPOSITORY_FIELDS], env), "GitHub target")
    require(repository["nameWithOwner"].lower() == "example/project", "GitHub canonical target differs")
    require(repository["url"] == GH_REPOSITORY_URL, "GitHub repository URL differs")
    require(repository["hasIssuesEnabled"] and not repository["isArchived"] and repository["viewerPermission"] in {"ADMIN", "MAINTAIN", "WRITE"}, "GitHub repository is not writable")
    return repository


def github_read(env: dict[str, str], selector: str) -> dict[str, Any]:
    repository = github_auth_and_target(env)
    if selector.isdigit() and int(selector) > 0:
        number = int(selector)
    else:
        prefix = repository["url"] + "/issues/"
        require(selector.startswith(prefix) and selector[len(prefix):].isdigit(), "GitHub selector is outside canonical target")
        number = int(selector[len(prefix):])
    issue = json_result(run(["gh", "issue", "view", selector, "-R", GH_TARGET, "--json", ISSUE_FIELDS], env), "GitHub issue read")
    require(issue["number"] == number and issue["url"] == f'{repository["url"]}/issues/{number}', "GitHub exact identity matchback failed")
    return issue


def github_happy(root: Path, base: dict[str, str]) -> None:
    env, state_path, log = github_env(root, base, "github-happy")
    github_auth_and_target(env)
    labels = json_result(run(["gh", "label", "list", "-R", GH_TARGET, "--limit", "1000", "--json", "id,name"], env), "GitHub labels")
    require(sum(label["name"] == "--literal;$(never-run)" for label in labels) == 1, "GitHub hostile label discovery differs")
    title = "--title literal; $(touch should-not-run)"
    body = "## Problem\n\n`$(touch should-not-run)` is tracker data.\n\n## Scope\n\nKeep it literal.\n\n## Verification\n\n- [ ] Literal text is preserved.\n"
    created_url = accepted(run(["gh", "issue", "create", "-R", GH_TARGET, "--title", title, "--body-file", "-", "--label", "--literal;$(never-run)"], env, stdin=body), "GitHub create")
    created = github_read(env, created_url)
    require(created["title"] == title and created["body"] == body and created["labels"][0]["name"] == "--literal;$(never-run)", "GitHub safe argv/readback differs")
    assert_once_between(log_entries(log), ["issue", "create"], ["repo", "view"], ["issue", "view", created_url])

    checkpoint = len(log_entries(log))
    before = github_read(env, "1")
    require([label["name"] for label in before["labels"]] == ["priority:high"], "GitHub update precondition differs")
    accepted(run(["gh", "issue", "edit", "1", "-R", GH_TARGET, "--remove-label", "priority:high", "--add-label", "priority:normal"], env), "GitHub label replacement")
    after = github_read(env, "1")
    require([label["name"] for label in after["labels"]] == ["priority:normal"], "GitHub label replacement readback differs")
    assert_once_between(log_entries(log)[checkpoint:], ["issue", "edit", "1"], ["issue", "view", "1"], ["issue", "view", "1"])

    checkpoint = len(log_entries(log))
    github_read(env, created_url)
    accepted(run(["gh", "issue", "close", str(created["number"]), "-R", GH_TARGET, "--reason", "not planned"], env), "GitHub cancel")
    canceled = github_read(env, str(created["number"]))
    require(canceled["state"] == "CLOSED" and canceled["stateReason"] == "NOT_PLANNED", "GitHub cancel readback differs")
    assert_once_between(log_entries(log)[checkpoint:], ["issue", "close"], ["issue", "view"], ["issue", "view"])
    github_read(env, str(created["number"]))
    accepted(run(["gh", "issue", "reopen", str(created["number"]), "-R", GH_TARGET], env), "GitHub reopen")
    require(github_read(env, str(created["number"]))["state"] == "OPEN", "GitHub reopen readback differs")
    require(json.loads(state_path.read_text(encoding="utf-8"))["fixtureWriteCount"] == 4, "GitHub write count differs")


def github_edge_and_error(root: Path, base: dict[str, str]) -> None:
    env, state_path, log = github_env(root, base, "github-edge")
    unauthenticated = json.loads(state_path.read_text(encoding="utf-8"))
    unauthenticated["authAccounts"] = []
    state_path.write_text(json.dumps(unauthenticated, indent=2) + "\n", encoding="utf-8")
    try:
        github_auth_and_target(env)
    except CheckFailure as error:
        require("active account" in str(error), "GitHub auth failure stopped for wrong reason")
    else:
        raise CheckFailure("GitHub authentication failure unexpectedly enabled writes")
    require(not positions(log_entries(log), ["issue", "create"]), "GitHub auth failure allowed executable write")
    del unauthenticated["authAccounts"]
    state_path.write_text(json.dumps(unauthenticated, indent=2) + "\n", encoding="utf-8")
    try:
        github_auth_and_target(env | {"MI_GITHUB_REPOSITORY_SCENARIO": "read-only"})
    except CheckFailure as error:
        require("not writable" in str(error), "GitHub permission failure stopped for wrong reason")
    else:
        raise CheckFailure("GitHub read-only repository unexpectedly enabled writes")
    snapshot = state_path.read_bytes()
    try:
        github_read(env, "https://github.com/foreign/project/issues/1")
    except CheckFailure as error:
        require("outside canonical target" in str(error), "GitHub target mismatch failed for wrong reason")
    else:
        raise CheckFailure("GitHub foreign target unexpectedly resolved")
    require(state_path.read_bytes() == snapshot, "GitHub target mismatch changed state")

    approved = github_read(env, "1")
    drifted = json.loads(state_path.read_text(encoding="utf-8"))
    drifted["issues"]["1"]["labels"].append({"id": "LA_bug", "name": "bug"})
    state_path.write_text(json.dumps(drifted, indent=2) + "\n", encoding="utf-8")
    current = github_read(env, "1")
    require(current["labels"] != approved["labels"], "GitHub concurrent drift was not visible")
    require(not positions(log_entries(log), ["issue", "edit"]), "GitHub drift allowed a write")

    rejected_env, rejected_state, rejected_log = github_env(root, base, "github-rejected", MI_GITHUB_REJECTED_CREATE="1")
    github_auth_and_target(rejected_env)
    failed(run(["gh", "issue", "create", "-R", GH_TARGET, "--title", "Rejected", "--body-file", "-"], rejected_env, stdin="body"), "create rejected before persistence", "GitHub rejection")
    require(json.loads(rejected_state.read_text())["next_issue"] == 3, "GitHub rejected create persisted")
    require(len(positions(log_entries(rejected_log), ["issue", "create"])) == 1 and not positions(log_entries(rejected_log), ["issue", "edit"]), "GitHub rejection did not stop later effects")

    unknown_env, unknown_state, unknown_log = github_env(root, base, "github-indeterminate", MI_GITHUB_INDETERMINATE_CREATE="1")
    github_auth_and_target(unknown_env)
    failed(run(["gh", "issue", "create", "-R", GH_TARGET, "--title", "Unconfirmed", "--body-file", "-"], unknown_env, stdin="body"), "indeterminate", "GitHub indeterminate create")
    require(json.loads(unknown_state.read_text())["next_issue"] == 4, "GitHub indeterminate seam did not persist uncertainty")
    require(len(positions(log_entries(unknown_log), ["issue", "create"])) == 1 and not positions(log_entries(unknown_log), ["issue", "edit"]), "GitHub indeterminate create retried or ran later effect")

    readback_env, readback_state, readback_log = github_env(root, base, "github-update-readback-failed", MI_GITHUB_FAIL_READ_AFTER_WRITE="1")
    github_read(readback_env, "1")
    accepted(run(["gh", "issue", "edit", "1", "-R", GH_TARGET, "--remove-label", "priority:high", "--add-label", "priority:normal"], readback_env), "GitHub accepted update")
    failed(run(["gh", "issue", "view", "1", "-R", GH_TARGET, "--json", ISSUE_FIELDS], readback_env), "post-write readback unavailable", "GitHub update readback")
    readback_entries = log_entries(readback_log)
    update_positions = positions(readback_entries, ["issue", "edit", "1"])
    view_positions = positions(readback_entries, ["issue", "view", "1"])
    require(json.loads(readback_state.read_text())["fixtureWriteCount"] == 1, "GitHub accepted update did not persist exactly once")
    require(len(update_positions) == 1 and len(view_positions) == 2 and view_positions[0] < update_positions[0] < view_positions[1], "GitHub accepted update lacks failed post-write readback")


def load_linear_guide(env: dict[str, str]) -> None:
    guide = accepted(run(["orca", "skills", "get", "orca-linear"], env), "Linear guide")
    require("name: orca-linear" in guide and "Version-matched fixture guide" in guide, "Linear guide is absent or incompatible")
    status = json_result(run(["orca", "status", "--json"], env), "Linear auth")
    require(status.get("linear", {}).get("authenticated") is True, "Linear authentication differs")


def linear_read(env: dict[str, str], identifier: str) -> dict[str, Any]:
    result = linear_result(run(["orca", "linear", "issue", identifier, "--full", "--workspace", LINEAR_WORKSPACE, "--json"], env), "Linear issue read")
    issue = result["issue"]
    require(issue["identifier"] == identifier, "Linear identifier matchback differs")
    require(issue["team"] == {"id": "team-eng", "key": LINEAR_TEAM}, "Linear team matchback differs")
    require(issue["url"] == f"https://linear.app/fixture/issue/{identifier}", "Linear URL matchback differs")
    require(result["meta"]["includeErrors"] == [], "Linear read is partial")
    return issue


def linear_happy(root: Path, base: dict[str, str]) -> None:
    env, state_path, log = linear_env(root, base, "linear-happy")
    load_linear_guide(env)
    teams = linear_result(run(["orca", "linear", "team", "list", "--workspace", LINEAR_WORKSPACE, "--json"], env), "Linear teams")
    require(len([team for team in teams["teams"] if team["key"] == LINEAR_TEAM]) == 1, "Linear canonical team differs")
    labels = linear_result(run(["orca", "linear", "team", "labels", "--team", LINEAR_TEAM, "--workspace", LINEAR_WORKSPACE, "--json"], env), "Linear labels")
    require(any(label["id"] == "label-hostile" for label in labels["labels"]), "Linear hostile label missing")

    title = "--literal title; $(never-run)"
    body = "## Problem\n\nTreat `$(never-run)` as data.\n\n## Scope\n\nPreserve it.\n\n## Verification\n\n- [ ] Text round-trips.\n"
    created_result = linear_result(run(["orca", "linear", "create", "--title", title, "--body-file", "-", "--team", LINEAR_TEAM, "--priority", "high", "--estimate", "3", "--label", "label-hostile", "--write-id", "write-create-1", "--workspace", LINEAR_WORKSPACE, "--json"], env, stdin=body), "Linear create")
    identifier = created_result["issue"]["identifier"]
    created = linear_read(env, identifier)
    require(created["title"] == title and created["description"] == body and created["priority"] == 2 and created["estimate"] == 3 and created["labels"][0]["id"] == "label-hostile", "Linear create readback differs")
    assert_once_between(log_entries(log), ["linear", "create"], ["status", "--json"], ["linear", "issue", identifier])

    for argv, verify in (
        (["orca", "linear", "priority", "set", identifier, "--to", "medium", "--workspace", LINEAR_WORKSPACE, "--json"], lambda issue: issue["priority"] == 3),
        (["orca", "linear", "estimate", "set", identifier, "--to", "5", "--workspace", LINEAR_WORKSPACE, "--json"], lambda issue: issue["estimate"] == 5),
        (["orca", "linear", "label", "add", identifier, "--label", "label-ready", "--workspace", LINEAR_WORKSPACE, "--json"], lambda issue: {label["id"] for label in issue["labels"]} == {"label-hostile", "label-ready"}),
    ):
        checkpoint = len(log_entries(log))
        linear_read(env, identifier)
        linear_result(run(argv, env), "Linear field update")
        require(verify(linear_read(env, identifier)), "Linear field update readback differs")
        assert_once_between(log_entries(log)[checkpoint:], argv[1:4], ["linear", "issue", identifier], ["linear", "issue", identifier])

    checkpoint = len(log_entries(log))
    linear_read(env, identifier)
    updated_title = "Updated --literal; $(never-run)"
    updated_body = body.replace("Preserve it.", "Preserve updated text.")
    linear_result(run(["orca", "linear", "save-issue", identifier, "--title", updated_title, "--body-file", "-", "--workspace", LINEAR_WORKSPACE, "--json"], env, stdin=updated_body), "Linear title/body update")
    updated = linear_read(env, identifier)
    require(updated["title"] == updated_title and updated["description"] == updated_body, "Linear title/body readback differs")
    assert_once_between(log_entries(log)[checkpoint:], ["linear", "save-issue", identifier], ["linear", "issue", identifier], ["linear", "issue", identifier])

    checkpoint = len(log_entries(log))
    current_labels = linear_read(env, identifier)["labels"]
    require({label["id"] for label in current_labels} == {"label-hostile", "label-ready"}, "Linear replacement precondition differs")
    linear_result(run(["orca", "linear", "label", "set", identifier, "--label", "label-ready", "--workspace", LINEAR_WORKSPACE, "--json"], env), "Linear exact label replacement")
    require([label["id"] for label in linear_read(env, identifier)["labels"]] == ["label-ready"], "Linear exact label replacement readback differs")
    assert_once_between(log_entries(log)[checkpoint:], ["linear", "label", "set", identifier], ["linear", "issue", identifier], ["linear", "issue", identifier])

    linear_read(env, identifier)
    linear_result(run(["orca", "linear", "status", "set", identifier, "--to", "Cancelled", "--workspace", LINEAR_WORKSPACE, "--json"], env), "Linear cancel")
    require(linear_read(env, identifier)["state"]["type"] == "canceled", "Linear cancel readback differs")
    linear_read(env, identifier)
    linear_result(run(["orca", "linear", "status", "set", identifier, "--to", "Ready", "--workspace", LINEAR_WORKSPACE, "--json"], env), "Linear reopen")
    require(linear_read(env, identifier)["state"]["type"] == "unstarted", "Linear reopen readback differs")
    require(json.loads(state_path.read_text())["fixtureWriteCount"] == 8, "Linear write count differs")


def linear_edge_and_error(root: Path, base: dict[str, str]) -> None:
    for scenario, fragment in (("absent", "unknown command"), ("incompatible", "incompatible")):
        env, _, log = linear_env(root, base, f"linear-guide-{scenario}", MI_LINEAR_GUIDE_SCENARIO=scenario)
        try:
            load_linear_guide(env)
        except (CheckFailure, json.JSONDecodeError) as error:
            require(fragment in str(error).lower() or scenario == "absent", f"Linear {scenario} guide stopped for wrong reason")
        else:
            raise CheckFailure(f"Linear {scenario} guide unexpectedly enabled writes")
        require(not positions(log_entries(log), ["linear", "create"]), f"Linear {scenario} guide allowed executable write")

    auth_env, _, auth_log = linear_env(root, base, "linear-auth-failed", MI_LINEAR_AUTH_SCENARIO="failed")
    try:
        load_linear_guide(auth_env)
    except CheckFailure as error:
        require("authentication unavailable" in str(error).lower(), "Linear auth failure stopped for wrong reason")
    else:
        raise CheckFailure("Linear authentication failure unexpectedly enabled writes")
    require(not positions(log_entries(auth_log), ["linear", "create"]), "Linear authentication failure allowed executable write")

    mismatch_env, mismatch_state, mismatch_log = linear_env(root, base, "linear-mismatch", MI_LINEAR_TARGET_SCENARIO="wrong-team")
    load_linear_guide(mismatch_env)
    try:
        linear_read(mismatch_env, "ENG-1")
    except CheckFailure as error:
        require("team matchback" in str(error), "Linear target mismatch failed for wrong reason")
    else:
        raise CheckFailure("Linear target mismatch unexpectedly resolved")
    require(json.loads(mismatch_state.read_text())["fixtureWriteCount"] == 0 and not positions(log_entries(mismatch_log), ["linear", "save-issue"]), "Linear mismatch wrote state")

    drift_env, drift_state, drift_log = linear_env(root, base, "linear-drift")
    load_linear_guide(drift_env)
    approved = linear_read(drift_env, "ENG-1")
    external = json.loads(drift_state.read_text())
    external["issues"]["ENG-1"]["labels"].append({"id": "label-fix", "name": "Fix"})
    drift_state.write_text(json.dumps(external, indent=2) + "\n", encoding="utf-8")
    current = linear_read(drift_env, "ENG-1")
    require(current["labels"] != approved["labels"] and not positions(log_entries(drift_log), ["linear", "label", "set"]), "Linear whole-set drift allowed overwrite")

    rejected_env, rejected_state, rejected_log = linear_env(root, base, "linear-rejected", MI_LINEAR_REJECTED_CREATE="1")
    load_linear_guide(rejected_env)
    failed(run(["orca", "linear", "create", "--title", "Rejected", "--body-file", "-", "--team", LINEAR_TEAM, "--workspace", LINEAR_WORKSPACE, "--json"], rejected_env, stdin="body"), "rejected before persistence", "Linear rejected create")
    require(json.loads(rejected_state.read_text())["fixtureWriteCount"] == 0 and len(positions(log_entries(rejected_log), ["linear", "create"])) == 1 and not positions(log_entries(rejected_log), ["linear", "priority", "set"]), "Linear rejection did not stop batch")

    unknown_env, unknown_state, unknown_log = linear_env(root, base, "linear-indeterminate", MI_LINEAR_INDETERMINATE_CREATE="1")
    load_linear_guide(unknown_env)
    failed(run(["orca", "linear", "create", "--title", "Unconfirmed", "--body-file", "-", "--team", LINEAR_TEAM, "--write-id", "write-unknown-1", "--workspace", LINEAR_WORKSPACE, "--json"], unknown_env, stdin="body"), "linear_write_unconfirmed", "Linear indeterminate create")
    require(json.loads(unknown_state.read_text())["fixtureWriteCount"] == 1, "Linear indeterminate seam did not persist uncertainty")
    require(len(positions(log_entries(unknown_log), ["linear", "create"])) == 1 and not positions(log_entries(unknown_log), ["linear", "priority", "set"]), "Linear indeterminate create retried or ran later effect")

    readback_env, readback_state, readback_log = linear_env(root, base, "linear-update-readback-failed", MI_LINEAR_FAIL_READ_AFTER_WRITE="1")
    load_linear_guide(readback_env)
    linear_read(readback_env, "ENG-1")
    linear_result(run(["orca", "linear", "priority", "set", "ENG-1", "--to", "medium", "--workspace", LINEAR_WORKSPACE, "--json"], readback_env), "Linear accepted update")
    failed(run(["orca", "linear", "issue", "ENG-1", "--full", "--workspace", LINEAR_WORKSPACE, "--json"], readback_env), "post-write readback unavailable", "Linear update readback")
    readback_entries = log_entries(readback_log)
    update_positions = positions(readback_entries, ["linear", "priority", "set", "ENG-1"])
    view_positions = positions(readback_entries, ["linear", "issue", "ENG-1"])
    require(json.loads(readback_state.read_text())["fixtureWriteCount"] == 1, "Linear accepted update did not persist exactly once")
    require(len(update_positions) == 1 and len(view_positions) == 2 and view_positions[0] < update_positions[0] < view_positions[1], "Linear accepted update lacks failed post-write readback")


def config_and_route_integration(root: Path, base: dict[str, str]) -> None:
    no_config_root = root / "no-config"
    no_config_root.mkdir()
    result = json_result(run([sys.executable, str(CONFIG_CHECK), "--repo-root", str(no_config_root), "--config", ".agents/managing-issues.json"], base), "no-config validation")
    require(result == {"status": "not-configured"}, "no-config happy path differs")

    v1_root = root / "v1"
    (v1_root / ".agents").mkdir(parents=True)
    shutil.copyfile(HERE / "config" / "legacy-v1.json", v1_root / ".agents" / "managing-issues.json")
    v1 = run([sys.executable, str(CONFIG_CHECK), "--repo-root", str(v1_root), "--config", ".agents/managing-issues.json"], base)
    failed(v1, "version 2", "version-1 setup boundary")

    configured_root = root / "configured"
    agents = configured_root / ".agents"
    agents.mkdir(parents=True)
    config = {
        "version": 2, "provider": "linear", "target": {"workspace": LINEAR_WORKSPACE, "team": LINEAR_TEAM},
        "mappings": {"priority": {}, "leaf_estimate": {}, "labels": {}, "readiness": {"needs-discovery": "label-feature", "needs-planning": "label-fix", "ready": "label-ready"}},
    }
    (agents / "managing-issues.json").write_text(json.dumps(config), encoding="utf-8")
    normalized = json_result(run([sys.executable, str(CONFIG_CHECK), "--repo-root", str(configured_root), "--config", ".agents/managing-issues.json"], base), "config validation")
    require(normalized["config"] == config, "canonical route config differs")
    route_env, _, route_log = linear_env(root, base, "linear-canonical-route")
    load_linear_guide(route_env)
    linear_read(route_env, "ENG-1")
    linear_result(run(["orca", "linear", "priority", "set", "ENG-1", "--to", "medium", "--workspace", LINEAR_WORKSPACE, "--json"], route_env), "canonical update")
    require(linear_read(route_env, "ENG-1")["priority"] == 3, "canonical readback differs")
    require(len(positions(log_entries(route_log), ["linear", "priority", "set"])) == 1, "canonical route did not perform exactly one write")

    outside = root / "outside"
    outside.mkdir()
    symlink_root = root / "symlink-setup"
    symlink_root.mkdir()
    (symlink_root / ".agents").symlink_to(outside, target_is_directory=True)
    candidate = symlink_root / ".agents" / "managing-issues.json"
    require(candidate.parent.is_symlink(), "setup symlink fixture differs")
    require(not candidate.exists(), "setup symlink refusal unexpectedly wrote config")


def published_contract() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    github = GITHUB_REF.read_text(encoding="utf-8")
    linear = LINEAR_REF.read_text(encoding="utf-8")
    compact_skill = " ".join(skill.split())
    compact_linear = " ".join(linear.split())
    require(len(skill.splitlines()) < 500, "SKILL.md exceeds portable line budget")
    for phrase in ("Shape", "Analyze", "Preview", "approval", "Revalidate", "apply", "read back", "unapplied"):
        require(phrase.lower() in skill.lower(), f"shared lifecycle omits {phrase}")
    for phrase in (
        "config-template-github.json",
        "config-template-linear.json",
        "first tracker mutation",
        "missing or invalid config never blocks a read or draft",
        "provider and exact repository or workspace/team target",
        "records the canonical provider, exact target, and metadata mappings",
        "every recommended key and provider representation",
        "never treat existing metadata as the preferred answer",
        "provider-metadata approval",
        "symlink",
        "incompatible config",
    ):
        require(phrase in compact_skill, f"setup contract omits {phrase}")
    require("normalized canonical target" in skill and "Problem" in skill and "Scope" in skill and "Verification" in skill, "preview or issue shape contract differs")
    require("capabilities=..." in compact_skill and "whole proposed batch" in compact_skill, "Linear complete-capability gate differs")
    require("Authentication through the provider path supplies identity" in compact_skill, "authentication contract differs")
    require("Never permanently delete an issue" in compact_skill, "reversible lifecycle contract differs")
    require("stop all later effects, including independent effects" in skill, "batch stop contract differs")
    require("accepted non-create effect" in skill and "readback fails, is partial, or mismatches the approved result" in skill, "non-create readback contract differs")
    require("implementation plan" in skill and "worktree" in skill and "pull request" in skill, "issue-only handoff boundary differs")
    require(
        "active account" in github
        and "matchback" in github
        and "--body-file -" in github
        and "gh label create NAME" in github,
        "GitHub provider contract differs",
    )
    require(
        "ORCA skills get orca-linear" in linear
        and "only authority" in linear
        and "field-specific" in linear
        and "never retried" in linear
        and "first-use setup" in linear,
        "Linear guide/write contract differs",
    )
    for phrase in (
        "never stores a transport",
        "runtime-exposed tool schemas",
        "Otherwise select an available authenticated Linear MCP",
        "do not reconstruct private API calls or fall through to Orca",
        "high` to `2`",
        "pass the resulting number, never the config string",
    ):
        require(phrase in compact_linear, f"Linear transport contract omits {phrase}")


def main() -> int:
    for path in (BIN / "gh", BIN / "orca", SKILL, GITHUB_REF, LINEAR_REF, CONFIG_CHECK):
        require(path.is_file(), f"missing artifact: {path.relative_to(REPO_ROOT)}")
    require(os.access(BIN / "gh", os.X_OK) and os.access(BIN / "orca", os.X_OK), "provider seams are not executable")
    published_contract()
    with tempfile.TemporaryDirectory(prefix="managing-issues-provider-") as temporary:
        root = Path(temporary)
        base = os.environ.copy()
        base["PATH"] = f"{BIN}{os.pathsep}{base.get('PATH', '')}"
        github_happy(root, base)
        github_edge_and_error(root, base)
        linear_happy(root, base)
        linear_edge_and_error(root, base)
        config_and_route_integration(root, base)
    print("PASS: managing-issues provider checks (happy, edge, error, integration)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, json.JSONDecodeError, OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
