#!/usr/bin/env python3
"""Build and grade exact-revision PR-readiness receipt fixtures."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
SPEC = json.loads((HERE / "assessment-spec.json").read_text(encoding="utf-8"))
SURFACE = REPO_ROOT / "skills" / "checking-pr-readiness" / "scripts" / "surface-report.sh"
COMMIT_TIME = "2026-01-02T00:00:00+00:00"
OBSERVED_TIME = "2026-01-02T00:00:10+00:00"
OID = re.compile(r"^[0-9a-f]{40,64}$")
BASE_SWEEP_VERDICTS = {
    "1": "clear",
    "2": "consistent",
    "3": "present",
    "4": "fresh",
    "5": "single-sourced",
    "6": "handled",
    "7": "truthful",
    "8": "exercises production artifact",
    "9": "clean",
    "10": "enforced",
}
EXPECTED_CHANGED_PATHS = {
    ".github/automated-reviewers.json",
    "CHANGELOG.md",
    "fixture-validation.py",
    "src/app.txt",
    *(f"evidence/{kind}.json" for kind in SPEC["required_receipts"]),
    *(f"results/{kind}.json" for kind in SPEC["required_receipts"]),
}
VERIFIED_COMMANDS = {
    "repository-gates": ("fixture-validation.py", "gate"),
    "code-review": ("fixture-validation.py", "review"),
    "code-simplification": ("fixture-validation.py", "simplify"),
    "testing": ("fixture-validation.py", "test"),
}
EVIDENCE_COMMON_FIELDS = {
    "schema",
    "repository",
    "subject",
    "status",
    "producer",
    "scope",
    "command",
    "outcome",
    "result_references",
}
EVIDENCE_KIND_FIELDS = {
    "working-surface": {"committed", "staged", "unstaged", "untracked"},
    "repository-gates": {"gates"},
    "code-review": {"finding_count", "findings"},
    "code-simplification": {"finding_count", "findings"},
    "testing": {"checks", "ui_classification"},
    "plan-versus-delivered": {"planned", "not_delivered"},
    "learning-signal": {"signal"},
    "targeted-sweep": {"verdicts", "unresolved"},
    "preflight": {"unresolved", "bypass_requested"},
}
EVIDENCE_RESULT_FIELDS = {
    "working-surface": {"result_id", "outcome", "paths"},
    "repository-gates": {"result_id", "outcome", "summary"},
    "code-review": {"result_id", "outcome", "reviewed_paths"},
    "code-simplification": {"result_id", "outcome", "reviewed_paths"},
    "testing": {"result_id", "outcome", "exit_code"},
    "plan-versus-delivered": {"result_id", "outcome", "delivered"},
    "learning-signal": {"result_id", "outcome", "summary"},
    "targeted-sweep": {"result_id", "outcome", "class_count"},
    "preflight": {"result_id", "outcome", "unresolved_count"},
}
EVIDENCE_BLOB_CACHE: dict[tuple[str, str, str], tuple[str, bytes]] = {}


class FixtureError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FixtureError(message)


def run(*command: str, cwd: Path, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value))


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def package_version() -> str:
    skill_root = REPO_ROOT / "skills" / "checking-pr-readiness"
    digest = hashlib.sha256()
    for path in sorted(item for item in skill_root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(skill_root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"working-tree@{digest.hexdigest()}"


def observed_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git_env(timestamp: str) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": "Synthetic Fixture",
            "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Synthetic Fixture",
            "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            "GIT_AUTHOR_DATE": timestamp,
            "GIT_COMMITTER_DATE": timestamp,
            "LC_ALL": "C",
        }
    )
    return env


def evidence_documents(reviewer_mode: str = "configured") -> dict[str, dict[str, Any]]:
    if reviewer_mode == "configured":
        class_11 = "under caps"
    elif reviewer_mode == "none":
        class_11 = "not applicable"
    elif reviewer_mode in {"missing-cap", "invalid-shape"}:
        class_11 = "cap unverified"
    else:
        raise FixtureError(f"unknown reviewer mode: {reviewer_mode}")
    sweep_verdicts = {**BASE_SWEEP_VERDICTS, "11": class_11}
    def evidence(
        kind: str,
        command_id: str,
        results: list[dict[str, Any]],
        command_arguments: list[str] | None = None,
        **substantive: Any,
    ) -> dict[str, Any]:
        return {
            "schema": f"checking-pr-readiness-{kind}-evidence/v1",
            "repository": SPEC["repository"],
            "subject": SPEC["subject"],
            "status": "verified",
            "producer": {"id": f"fixture:{kind}", "version": "fixture-v1"},
            "scope": {
                "repository": SPEC["repository"],
                "subject": SPEC["subject"],
                "base": "main",
                "surface": "full",
            },
            "command": {"id": command_id, "arguments": command_arguments or []},
            "outcome": "verified",
            "results": results,
            "result_references": [],
            **substantive,
        }

    changed_paths = sorted(EXPECTED_CHANGED_PATHS)
    return {
        "working-surface": evidence(
            "working-surface",
            "surface-report",
            [{"result_id": "surface:inventory", "outcome": "clean", "paths": changed_paths}],
            committed=changed_paths,
            staged=[],
            unstaged=[],
            untracked=[],
        ),
        "repository-gates": evidence(
            "repository-gates",
            "python3",
            [{"result_id": "gate:fixture-validation", "outcome": "verified", "summary": "fixture validation passed"}],
            ["fixture-validation.py", "gate"],
            gates=[{
                "name": "fixture-validation",
                "owner": "fixture task runner",
                "command": "python3 fixture-validation.py gate",
                "outcome": "verified",
                "status": "verified",
                "result_reference": "gate:fixture-validation",
            }],
        ),
        "code-review": evidence(
            "code-review",
            "python3",
            [{"result_id": "review:summary", "outcome": "clear", "reviewed_paths": changed_paths}],
            ["fixture-validation.py", "review"],
            finding_count=0,
            findings=[],
        ),
        "code-simplification": evidence(
            "code-simplification",
            "python3",
            [{"result_id": "simplification:summary", "outcome": "clear", "reviewed_paths": changed_paths}],
            ["fixture-validation.py", "simplify"],
            finding_count=0,
            findings=[],
        ),
        "testing": evidence(
            "testing",
            "python3",
            [{"result_id": "test:fixture-validation", "outcome": "passed", "exit_code": 0}],
            ["fixture-validation.py", "test"],
            checks=[{
                "name": "fixture-validation",
                "command": "python3 fixture-validation.py test",
                "outcome": "passed",
                "result_reference": "test:fixture-validation",
            }],
            ui_classification="not applicable",
        ),
        "plan-versus-delivered": evidence(
            "plan-versus-delivered",
            "plan-delivery-comparison",
            [{"result_id": "delivery:summary", "outcome": "complete", "delivered": ["change synthetic app state"]}],
            planned=["change synthetic app state"],
            not_delivered=[],
        ),
        "learning-signal": evidence(
            "learning-signal",
            "learning-signal-assessment",
            [{"result_id": "learning:summary", "outcome": "no-learning", "summary": "synthetic change only"}],
            signal="no durable learning; synthetic change only",
        ),
        "targeted-sweep": evidence(
            "targeted-sweep",
            "targeted-sweep",
            [{"result_id": "sweep:summary", "outcome": "clear", "class_count": 11}],
            verdicts=sweep_verdicts,
            unresolved=[] if reviewer_mode != "missing-cap" else ["automated reviewer cap unresolved: fixture-reviewer"],
        ),
        "preflight": evidence(
            "preflight",
            "checking-pr-readiness-preflight",
            [{"result_id": "preflight:summary", "outcome": "converged", "unresolved_count": 0}],
            unresolved=[],
            bypass_requested=False,
        ),
    }


def build_repository(
    path: Path,
    reviewer_mode: str = "configured",
    evidence_mutator: Callable[[dict[str, dict[str, Any]]], None] | None = None,
    pre_result_mutator: Callable[[dict[str, dict[str, Any]]], None] | None = None,
) -> str:
    path.mkdir(parents=True)
    run("git", "init", "-q", "-b", "main", cwd=path)
    run("git", "config", "user.name", "Synthetic Fixture", cwd=path)
    run("git", "config", "user.email", "fixture@example.invalid", cwd=path)
    run("git", "config", "commit.gpgsign", "false", cwd=path)
    run("git", "remote", "add", "origin", SPEC["repository"], cwd=path)
    (path / "src").mkdir()
    (path / "src" / "app.txt").write_text("seed\n", encoding="utf-8")
    (path / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
    run("git", "add", "src/app.txt", "CHANGELOG.md", cwd=path)
    run("git", "commit", "-q", "-m", "seed", cwd=path, env=git_env("2026-01-01T00:00:00+00:00"))
    run("git", "checkout", "-q", "-b", "assessment-target", cwd=path)
    (path / "src" / "app.txt").write_text("ready\n", encoding="utf-8")
    (path / "CHANGELOG.md").write_text("# Changelog\n\n- Prepared synthetic assessment.\n", encoding="utf-8")
    (path / "fixture-validation.py").write_text(
        """#!/usr/bin/env python3
import pathlib
import sys

mode = sys.argv[1] if len(sys.argv) == 2 else ""
if mode not in {"gate", "review", "simplify", "test"}:
    raise SystemExit(2)
if pathlib.Path("src/app.txt").read_text(encoding="utf-8") != "ready\\n":
    raise SystemExit(1)
if "Prepared synthetic assessment." not in pathlib.Path("CHANGELOG.md").read_text(encoding="utf-8"):
    raise SystemExit(1)
print(f"verified:{mode}")
""",
        encoding="utf-8",
    )
    if reviewer_mode == "configured":
        reviewer_configuration_document = {"automated_reviewers": [{"name": "fixture-reviewer", "cap": SPEC["reviewer_cap"]}]}
    elif reviewer_mode == "none":
        reviewer_configuration_document = {"automated_reviewers": []}
    elif reviewer_mode == "missing-cap":
        reviewer_configuration_document = {"automated_reviewers": [{"name": "fixture-reviewer"}]}
    else:
        reviewer_configuration_document = {"automated_reviewers": {}}
    write_json(path / ".github" / "automated-reviewers.json", reviewer_configuration_document)
    documents = evidence_documents(reviewer_mode)
    if pre_result_mutator is not None:
        pre_result_mutator(documents)
    for kind, document in documents.items():
        results = document.pop("results")
        result_document = {
            "schema": f"checking-pr-readiness-{kind}-result/v1",
            "producer": document["producer"],
            "scope": document["scope"],
            "command": document["command"],
            "outcome": document["outcome"],
            "results": results,
        }
        relative = f"results/{kind}.json"
        content = json_bytes(result_document)
        write_json(path / relative, result_document)
        document["result_references"] = [{"path": relative, "sha256": hashlib.sha256(content).hexdigest()}]
    if evidence_mutator is not None:
        evidence_mutator(documents)
    for kind, document in documents.items():
        write_json(path / "evidence" / f"{kind}.json", document)
    run("git", "add", "src/app.txt", "CHANGELOG.md", "fixture-validation.py", ".github", "evidence", "results", cwd=path)
    run("git", "commit", "-q", "-m", "prepare synthetic assessment", cwd=path, env=git_env(COMMIT_TIME))
    revision = run("git", "rev-parse", "HEAD", cwd=path)
    require(bool(OID.fullmatch(revision)), "fixture did not produce a full Git OID")
    require(run("git", "status", "--porcelain", cwd=path) == "", "fixture checkout is dirty")
    return revision


def git_blob(repo: Path, revision: str, relative: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{relative}"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    return completed.stdout


def evidence_blob(repo: Path, revision: str, relative: str) -> tuple[str, bytes]:
    key = (str(repo.resolve()), revision, relative)
    if key not in EVIDENCE_BLOB_CACHE:
        tree_entry = run("git", "ls-tree", revision, "--", relative, cwd=repo).split()
        if not tree_entry:
            raise subprocess.CalledProcessError(1, ["git", "ls-tree", revision, "--", relative])
        EVIDENCE_BLOB_CACHE[key] = (tree_entry[0], git_blob(repo, revision, relative))
    return EVIDENCE_BLOB_CACHE[key]


def make_bundle(repo: Path, revision: str) -> dict[str, Any]:
    receipts = []
    for kind in SPEC["required_receipts"]:
        relative = f"evidence/{kind}.json"
        _, content = evidence_blob(repo, revision, relative)
        digest = hashlib.sha256(content).hexdigest()
        receipts.append(
            {
                "schema": "checking-pr-readiness-evidence/v1",
                "receipt_id": f"receipt:{kind}",
                "kind": kind,
                "capability": "checking-pr-readiness",
                "capability_version": "fixture-v1",
                "repository": SPEC["repository"],
                "subject": SPEC["subject"],
                "exact_revision": revision,
                "evidence_references": [{"path": relative, "sha256": digest}],
                "outcome": "verified",
                "gaps": [],
                "observed_at": OBSERVED_TIME,
            }
        )
    return {
        "schema": "checking-pr-readiness-receipt-bundle/v1",
        "assessment": {
            "schema": "checking-pr-readiness-assessment/v1",
            "capability": "checking-pr-readiness",
            "capability_version": "fixture-v1",
            "repository": SPEC["repository"],
            "subject": SPEC["subject"],
            "exact_revision": revision,
            "receipt_references": [receipt["receipt_id"] for receipt in receipts],
            "outcome": "pass",
            "gaps": [],
            "observed_at": OBSERVED_TIME,
            "mode": "assessment-only",
        },
        "receipts": receipts,
    }


def receipt_by_kind(bundle: dict[str, Any], kind: str) -> dict[str, Any]:
    for receipt in bundle["receipts"]:
        if receipt.get("kind") == kind:
            return receipt
    raise FixtureError(f"missing fixture receipt: {kind}")


def resolve_live_subject(repo: Path) -> tuple[str | None, list[str]]:
    completed = subprocess.run(
        ["git", "symbolic-ref", "--quiet", "--short", "HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if completed.returncode == 0:
        branch = completed.stdout.strip()
        if branch:
            return f"branch:{branch}", []
    branches = [
        line
        for line in run("git", "for-each-ref", "--format=%(refname:short)", "--points-at", "HEAD", "refs/heads", cwd=repo).splitlines()
        if line
    ]
    if len(branches) > 1:
        return None, ["ambiguous live subject: detached HEAD points at multiple branches"]
    return None, ["live subject unavailable: detached HEAD"]


def resolve_live_repository(repo: Path) -> tuple[str | None, list[str]]:
    try:
        repository = run("git", "remote", "get-url", "origin", cwd=repo)
    except subprocess.CalledProcessError:
        return None, ["live repository identity unavailable: origin remote missing"]
    if not repository:
        return None, ["live repository identity unavailable: origin remote empty"]
    return repository, []


def reviewer_configuration(repo: Path, revision: str) -> list[dict[str, Any]]:
    _, content = evidence_blob(repo, revision, ".github/automated-reviewers.json")
    document = json.loads(content)
    reviewers = document.get("automated_reviewers")
    if not isinstance(reviewers, list):
        raise FixtureError("repository automated-reviewer discovery is invalid")
    return reviewers


def validate_surface(repo: Path, reviewers: list[dict[str, Any]]) -> tuple[list[str], set[str]]:
    command = [str(SURFACE), "--full", "--base", "main"]
    missing_caps: list[str] = []
    for reviewer in reviewers:
        name = reviewer.get("name") if isinstance(reviewer, dict) else None
        cap = reviewer.get("cap") if isinstance(reviewer, dict) else None
        if not isinstance(name, str) or not name:
            missing_caps.append("automated reviewer identity unresolved")
        elif not isinstance(cap, int) or cap < 0:
            missing_caps.append(f"automated reviewer cap unresolved: {name}")
        else:
            command.extend(["--cap", f"{name}={cap}"])
    completed = subprocess.run(
        command,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output = completed.stdout
    gaps: list[str] = list(missing_caps)
    changed = set(run("git", "diff", "--name-only", "main...HEAD", cwd=repo).splitlines())
    expected_verdict = "under caps" if reviewers and not missing_caps else "cap unverified"
    if completed.returncode != 0 or not output.startswith(f"verdict: {expected_verdict}\n"):
        gaps.append("working surface helper returned an unexpected verdict")
    output_lines = output.splitlines()
    if changed != EXPECTED_CHANGED_PATHS or output_lines.count(f"committed: {len(changed)}") != 1:
        gaps.append("working surface inventory mismatch")
    for relative in changed:
        if f"  {relative}\n" not in f"{output}\n":
            gaps.append(f"working surface helper omitted path: {relative}")
    for category in ("staged", "unstaged", "untracked"):
        if output_lines.count(f"{category}: 0") != 1:
            gaps.append(f"dirty working surface: {category}")
    return gaps, changed


def bounded_text(value: Any, limit: int = 512) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= limit


def text_set(value: Any) -> set[str] | None:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        return None
    return set(value)


def verify_command_evidence(kind: str, command: dict[str, Any], repo: Path, revision: str) -> list[str]:
    expected = VERIFIED_COMMANDS.get(kind)
    if expected is None:
        return []
    if command != {"id": "python3", "arguments": list(expected)}:
        return [f"command execution not verified: {kind}"]
    try:
        app_state = git_blob(repo, revision, "src/app.txt")
        changelog = git_blob(repo, revision, "CHANGELOG.md")
    except subprocess.CalledProcessError:
        return [f"command execution not verified: {kind}"]
    if app_state != b"ready\n" or b"Prepared synthetic assessment." not in changelog:
        return [f"command execution not verified: {kind}"]
    return []


def validate_evidence_document(
    kind: str,
    document: Any,
    repo: Path,
    revision: str,
    surface_paths: set[str],
    live_subject: str | None,
    reviewers: list[dict[str, Any]],
    repository: str | None,
) -> list[str]:
    if not isinstance(document, dict):
        return [f"invalid evidence document: {kind}"]

    expected_fields = EVIDENCE_COMMON_FIELDS | EVIDENCE_KIND_FIELDS[kind]
    producer = document.get("producer")
    scope = document.get("scope")
    command = document.get("command")
    references = document.get("result_references")
    common_valid = all(
        (
            set(document) == expected_fields,
            document.get("schema") == f"checking-pr-readiness-{kind}-evidence/v1",
            isinstance(producer, dict) and set(producer) == {"id", "version"},
            isinstance(producer, dict) and bounded_text(producer.get("id")) and bounded_text(producer.get("version")),
            isinstance(scope, dict) and set(scope) == {"repository", "subject", "base", "surface"},
            isinstance(scope, dict)
            and scope.get("repository") == repository
            and scope.get("subject") == live_subject
            and scope.get("base") == "main"
            and scope.get("surface") == "full",
            isinstance(command, dict) and set(command) == {"id", "arguments"},
            isinstance(command, dict) and bounded_text(command.get("id")),
            isinstance(command, dict)
            and isinstance(command.get("arguments"), list)
            and len(command["arguments"]) <= 32
            and all(bounded_text(argument) for argument in command["arguments"]),
            document.get("outcome") == "verified",
            isinstance(references, list) and len(references) == 1,
        )
    )
    if not common_valid:
        return [f"substantive evidence schema mismatch: {kind}"]

    reference = references[0]
    expected_result_path = f"results/{kind}.json"
    if (
        not isinstance(reference, dict)
        or set(reference) != {"path", "sha256"}
        or reference.get("path") != expected_result_path
        or not isinstance(reference.get("sha256"), str)
        or not re.fullmatch(r"[0-9a-f]{64}", reference["sha256"])
    ):
        return [f"substantive evidence schema mismatch: {kind}"]
    try:
        mode, result_content = evidence_blob(repo, revision, expected_result_path)
        result_document = json.loads(result_content)
    except (subprocess.CalledProcessError, UnicodeDecodeError, json.JSONDecodeError):
        return [f"substantive evidence schema mismatch: {kind}"]
    if (
        mode != "100644"
        or hashlib.sha256(result_content).hexdigest() != reference["sha256"]
        or not isinstance(result_document, dict)
        or set(result_document) != {"schema", "producer", "scope", "command", "outcome", "results"}
        or result_document.get("schema") != f"checking-pr-readiness-{kind}-result/v1"
        or result_document.get("producer") != producer
        or result_document.get("scope") != scope
        or result_document.get("command") != command
        or result_document.get("outcome") != document.get("outcome")
    ):
        return [f"substantive evidence schema mismatch: {kind}"]

    results = result_document.get("results")
    if not isinstance(results, list) or not (0 < len(results) <= 64):
        return [f"substantive evidence schema mismatch: {kind}"]
    result_ids: list[str] = []
    for result in results:
        if (
            not isinstance(result, dict)
            or set(result) != EVIDENCE_RESULT_FIELDS[kind]
            or not bounded_text(result.get("result_id"))
            or not bounded_text(result.get("outcome"))
        ):
            return [f"substantive evidence schema mismatch: {kind}"]
        result_ids.append(result["result_id"])
    if len(result_ids) != len(set(result_ids)):
        return [f"substantive evidence schema mismatch: {kind}"]

    gaps: list[str] = verify_command_evidence(kind, command, repo, revision)
    if document.get("repository") != repository or document.get("subject") != live_subject:
        gaps.append(f"evidence identity mismatch: {kind}")
    if document.get("status") != "verified":
        gaps.append(f"evidence status not verified: {kind}")
    result_by_id = {result["result_id"]: result for result in results}

    if kind == "working-surface":
        committed = document.get("committed")
        inventory = result_by_id.get("surface:inventory", {})
        if (
            not isinstance(committed, list)
            or any(not isinstance(item, str) for item in committed)
            or set(committed) != surface_paths
            or inventory.get("outcome") != "clean"
            or text_set(inventory.get("paths")) != surface_paths
        ):
            gaps.append("working surface evidence inventory mismatch")
        if any(document.get(category) for category in ("staged", "unstaged", "untracked")):
            gaps.append("working surface evidence reports dirty categories")
    elif kind == "repository-gates":
        gates = document.get("gates", [])
        if (
            not isinstance(gates, list)
            or not gates
            or any(
                not isinstance(gate, dict)
                or set(gate) != {"name", "owner", "command", "outcome", "status", "result_reference"}
                or not all(bounded_text(gate.get(field)) for field in ("name", "owner", "command", "result_reference"))
                or gate.get("outcome") != "verified"
                or gate.get("status") != "verified"
                or gate.get("result_reference") not in result_by_id
                or result_by_id[gate["result_reference"]].get("outcome") != "verified"
                for gate in gates
            )
        ):
            gaps.append("repository gate inventory incomplete")
    elif kind in {"code-review", "code-simplification"}:
        summary = results[0]
        if (
            type(document.get("finding_count")) is not int
            or document["finding_count"] != 0
            or document.get("findings") != []
            or len(results) != 1
            or summary.get("outcome") != "clear"
            or text_set(summary.get("reviewed_paths")) != surface_paths
        ):
            gaps.append(f"unresolved finding: {kind}")
    elif kind == "testing":
        checks = document.get("checks")
        if (
            not isinstance(checks, list)
            or not checks
            or any(
                not isinstance(check, dict)
                or set(check) != {"name", "command", "outcome", "result_reference"}
                or not bounded_text(check.get("name"))
                or not bounded_text(check.get("command"))
                or check.get("outcome") != "passed"
                or check.get("result_reference") not in result_by_id
                or result_by_id[check["result_reference"]].get("outcome") != "passed"
                or result_by_id[check["result_reference"]].get("exit_code") != 0
                for check in checks
            )
            or document.get("ui_classification") not in {"applicable", "not applicable"}
        ):
            gaps.append("testing evidence incomplete")
    elif kind == "plan-versus-delivered":
        planned = document.get("planned")
        not_delivered = document.get("not_delivered")
        if (
            not isinstance(planned, list)
            or not planned
            or text_set(planned) is None
            or len(planned) != len(set(planned))
            or not isinstance(not_delivered, list)
            or not_delivered
            or len(results) != 1
            or results[0].get("outcome") != "complete"
            or results[0].get("delivered") != planned
        ):
            gaps.append("plan-versus-delivered evidence incomplete")
    elif kind == "learning-signal":
        if not bounded_text(document.get("signal")) or len(results) != 1 or not bounded_text(results[0].get("summary")):
            gaps.append("learning-signal evidence incomplete")
    elif kind == "targeted-sweep":
        expected_class_11 = "not applicable" if not reviewers else "under caps"
        expected_verdicts = {**BASE_SWEEP_VERDICTS, "11": expected_class_11}
        unresolved = document.get("unresolved")
        if (
            document.get("verdicts") != expected_verdicts
            or not isinstance(unresolved, list)
            or unresolved
            or len(results) != 1
            or results[0].get("outcome") != "clear"
            or results[0].get("class_count") != 11
        ):
            gaps.append("targeted sweep evidence incomplete")
    elif kind == "preflight":
        unresolved = document.get("unresolved")
        if (
            not isinstance(unresolved, list)
            or unresolved
            or document.get("bypass_requested") is not False
            or len(results) != 1
            or results[0].get("outcome") != "converged"
            or results[0].get("unresolved_count") != 0
        ):
            gaps.append("preflight evidence incomplete")
    return gaps


def evaluate(repo: Path, bundle: Any, input_gaps: list[str] | None = None) -> dict[str, Any]:
    revision = run("git", "rev-parse", "HEAD", cwd=repo)
    live_subject, subject_gaps = resolve_live_subject(repo)
    live_repository, repository_gaps = resolve_live_repository(repo)
    assessment = {
        "schema": "checking-pr-readiness-assessment/v1",
        "capability": "checking-pr-readiness",
        "capability_version": package_version(),
        "repository": live_repository,
        "subject": live_subject,
        "exact_revision": revision,
        "receipt_references": [],
        "outcome": "action-required",
        "gaps": [],
        "observed_at": observed_now(),
        "mode": "assessment-only",
    }
    gaps: list[str] = [*(input_gaps or []), *subject_gaps, *repository_gaps]
    try:
        reviewers = reviewer_configuration(repo, revision)
    except (FixtureError, json.JSONDecodeError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        reviewers = []
        gaps.append(f"repository automated-reviewer discovery is invalid: {type(error).__name__}")
    surface_gaps, surface_paths = validate_surface(repo, reviewers)
    gaps.extend(surface_gaps)
    commit_time = datetime.fromisoformat(run("git", "show", "-s", "--format=%cI", revision, cwd=repo))
    if not isinstance(bundle, dict):
        gaps.append("receipt bundle is not an object")
        bundle = {}
    if bundle.get("schema") != "checking-pr-readiness-receipt-bundle/v1":
        gaps.append("receipt bundle schema mismatch")
    supplied_assessment = bundle.get("assessment")
    if not isinstance(supplied_assessment, dict):
        gaps.append("assessment member is not an object")
        supplied_assessment = {}
    receipts = bundle.get("receipts", [])
    if not isinstance(receipts, list):
        gaps.append("receipt bundle did not resolve receipts")
        receipts = []
    valid_receipts: list[dict[str, Any]] = []
    for index, receipt in enumerate(receipts):
        if not isinstance(receipt, dict):
            gaps.append(f"invalid receipt element: {index}")
        elif not isinstance(receipt.get("kind"), str):
            gaps.append(f"invalid receipt kind: {index}")
        else:
            valid_receipts.append(receipt)
    by_kind = {receipt.get("kind"): receipt for receipt in valid_receipts}
    evidence_documents_by_kind: dict[str, Any] = {}

    if len(by_kind) != len(valid_receipts):
        gaps.append("duplicate receipt kind")

    for kind in SPEC["required_receipts"]:
        receipt = by_kind.get(kind)
        if receipt is None:
            gaps.append(f"missing receipt: {kind}")
            continue
        if receipt.get("schema") != "checking-pr-readiness-evidence/v1":
            gaps.append(f"invalid receipt schema: {kind}")
        if receipt.get("receipt_id") != f"receipt:{kind}":
            gaps.append(f"invalid receipt identity: {kind}")
        if receipt.get("capability") != "checking-pr-readiness" or not receipt.get("capability_version"):
            gaps.append(f"invalid receipt capability: {kind}")
        if receipt.get("repository") != live_repository:
            gaps.append(f"cross-repository receipt: {kind}")
        if receipt.get("subject") != live_subject:
            gaps.append(f"cross-subject receipt: {kind}")
        if receipt.get("exact_revision") != revision:
            gaps.append(f"cross-revision receipt: {kind}")
        try:
            observed = datetime.fromisoformat(receipt["observed_at"])
            if observed < commit_time:
                gaps.append(f"stale receipt: {kind}")
        except (KeyError, ValueError, TypeError):
            gaps.append(f"invalid observation time: {kind}")
        if receipt.get("outcome") == "bypassed" or receipt.get("bypass_requested"):
            gaps.append(f"bypass request: {kind}")
        elif receipt.get("outcome") not in {"verified", "not applicable"} or receipt.get("gaps"):
            gaps.append(f"unresolved finding: {kind}")
        references = receipt.get("evidence_references", [])
        if not isinstance(references, list) or not references:
            gaps.append(f"missing evidence reference: {kind}")
            references = []
        expected_path = f"evidence/{kind}.json"
        if len(references) != 1 or any(not isinstance(reference, dict) or reference.get("path") != expected_path for reference in references):
            gaps.append(f"evidence inventory mismatch: {kind}")
        for reference in references:
            if not isinstance(reference, dict):
                gaps.append(f"invalid evidence reference: {kind}")
                continue
            relative = reference.get("path")
            if not isinstance(relative, str) or not relative or relative.startswith("/") or ".." in Path(relative).parts:
                gaps.append(f"invalid evidence reference: {kind}")
                continue
            try:
                mode, content = evidence_blob(repo, revision, relative)
            except (subprocess.CalledProcessError, IndexError):
                gaps.append(f"missing evidence: {kind}")
                continue
            if mode != "100644":
                gaps.append(f"non-regular evidence: {kind}")
            if hashlib.sha256(content).hexdigest() != reference.get("sha256"):
                gaps.append(f"evidence digest mismatch: {kind}")
            if relative == expected_path:
                try:
                    evidence_documents_by_kind[kind] = json.loads(content)
                except (UnicodeDecodeError, json.JSONDecodeError):
                    gaps.append(f"invalid evidence document: {kind}")

    for kind in SPEC["required_receipts"]:
        if kind in evidence_documents_by_kind:
            gaps.extend(
                validate_evidence_document(
                    kind,
                    evidence_documents_by_kind[kind],
                    repo,
                    revision,
                    surface_paths,
                    live_subject,
                    reviewers,
                    live_repository,
                )
            )

    expected_ids = {f"receipt:{kind}" for kind in SPEC["required_receipts"]}
    raw_receipt_references = supplied_assessment.get("receipt_references", [])
    if not isinstance(raw_receipt_references, list):
        gaps.append("assessment receipt inventory mismatch")
        receipt_references: list[str] = []
    else:
        receipt_references = [reference for reference in raw_receipt_references if isinstance(reference, str)]
        if len(receipt_references) != len(raw_receipt_references):
            gaps.append("invalid assessment receipt reference")
    if set(receipt_references) != expected_ids:
        gaps.append("assessment receipt inventory mismatch")
    receipt_ids = [receipt.get("receipt_id") for receipt in valid_receipts]
    if len(receipt_references) != len(set(receipt_references)):
        gaps.append("duplicate assessment receipt reference")
    if set(receipt_ids) - set(receipt_references):
        gaps.append("receipt bundle contains unreferenced receipt")
    for reference in receipt_references:
        if receipt_ids.count(reference) != 1:
            gaps.append(f"unresolved receipt reference: {reference}")
    if supplied_assessment.get("schema") != "checking-pr-readiness-assessment/v1":
        gaps.append("assessment schema mismatch")
    if supplied_assessment.get("capability") != "checking-pr-readiness":
        gaps.append("assessment capability mismatch")
    if supplied_assessment.get("mode") != "assessment-only":
        gaps.append("assessment mode mismatch")
    if supplied_assessment.get("repository") != live_repository:
        gaps.append("assessment repository mismatch")
    if supplied_assessment.get("subject") != live_subject:
        gaps.append("assessment subject mismatch")
    if supplied_assessment.get("exact_revision") != revision:
        gaps.append("assessment revision mismatch")
    if not OID.fullmatch(revision):
        gaps.append("assessment revision is not a full Git OID")

    assessment["receipt_references"] = receipt_references
    assessment["gaps"] = sorted(set(gaps))
    assessment["outcome"] = "pass" if not assessment["gaps"] else "action-required"
    return assessment


def variants(bundle: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    missing = copy.deepcopy(bundle)
    missing["receipts"] = [receipt for receipt in missing["receipts"] if receipt["kind"] != "code-review"]
    result["missing-receipt"] = missing

    unresolved_reference = copy.deepcopy(bundle)
    unresolved_reference["assessment"]["receipt_references"][0] = "receipt:does-not-exist"
    result["missing-receipt-resolution"] = unresolved_reference

    unreferenced = copy.deepcopy(bundle)
    extra_receipt = copy.deepcopy(unreferenced["receipts"][0])
    extra_receipt["receipt_id"] = "receipt:unreferenced"
    extra_receipt["kind"] = "unreferenced"
    unreferenced["receipts"].append(extra_receipt)
    result["unreferenced-receipt"] = unreferenced

    duplicate_kind = copy.deepcopy(bundle)
    duplicate = copy.deepcopy(duplicate_kind["receipts"][0])
    duplicate["receipt_id"] = "receipt:duplicate-kind"
    duplicate_kind["receipts"].append(duplicate)
    duplicate_kind["assessment"]["receipt_references"].append(duplicate["receipt_id"])
    result["duplicate-receipt-kind"] = duplicate_kind

    missing_reference = copy.deepcopy(bundle)
    receipt_by_kind(missing_reference, "code-review")["evidence_references"] = []
    result["missing-evidence-reference"] = missing_reference

    stale = copy.deepcopy(bundle)
    receipt_by_kind(stale, "code-simplification")["observed_at"] = "2025-01-01T00:00:00+00:00"
    result["stale-receipt"] = stale

    cross_subject = copy.deepcopy(bundle)
    receipt_by_kind(cross_subject, "testing")["subject"] = "branch:another-subject"
    result["cross-subject"] = cross_subject

    cross_revision = copy.deepcopy(bundle)
    receipt_by_kind(cross_revision, "plan-versus-delivered")["exact_revision"] = "0" * 40
    result["cross-revision"] = cross_revision

    unresolved = copy.deepcopy(bundle)
    receipt_by_kind(unresolved, "targeted-sweep")["outcome"] = "failed"
    receipt_by_kind(unresolved, "targeted-sweep")["gaps"] = ["class finding remains"]
    result["unresolved-finding"] = unresolved

    bypass = copy.deepcopy(bundle)
    receipt_by_kind(bypass, "preflight")["outcome"] = "bypassed"
    receipt_by_kind(bypass, "preflight")["bypass_requested"] = True
    result["bypass-request"] = bypass

    null_receipt = copy.deepcopy(bundle)
    null_receipt["receipts"][0] = None
    result["null-receipt-element"] = null_receipt

    invalid_kind = copy.deepcopy(bundle)
    invalid_kind["receipts"][0]["kind"] = []
    result["invalid-receipt-kind"] = invalid_kind

    invalid_path = copy.deepcopy(bundle)
    invalid_path["receipts"][0]["evidence_references"][0]["path"] = []
    result["invalid-evidence-path"] = invalid_path

    invalid_assessment_reference = copy.deepcopy(bundle)
    invalid_assessment_reference["assessment"]["receipt_references"][0] = {}
    result["invalid-assessment-reference"] = invalid_assessment_reference
    return result


def validate_contract_sources() -> None:
    assessment_mode = (REPO_ROOT / "skills" / "checking-pr-readiness" / "references" / "assessment-mode.md").read_text(encoding="utf-8")
    sweep_classes = (REPO_ROOT / "skills" / "checking-pr-readiness" / "references" / "sweep-classes.md").read_text(encoding="utf-8")
    skill = (REPO_ROOT / "skills" / "checking-pr-readiness" / "SKILL.md").read_text(encoding="utf-8")
    assessment_words = " ".join(assessment_mode.split())
    sweep_words = " ".join(sweep_classes.split())
    skill_words = " ".join(skill.split())
    for phrase in (
        "`checking-pr-readiness-receipt-bundle/v1`",
        "`checking-pr-readiness-evidence/v1`",
        "`checking-pr-readiness-<kind>-result/v1`",
        "`receipt_references`",
        "Resolve every receipt reference exactly once",
        "A detached HEAD cannot support a branch subject",
        "Repository-authored evidence and result JSON cannot authenticate their own execution",
    ):
        require(phrase in assessment_words, f"assessment bundle contract missing: {phrase}")
    for source, phrase in (
        (sweep_words, "no automated reviewer is configured"),
        (sweep_words, "not applicable"),
        (skill_words, "configured automated reviewer"),
    ):
        require(phrase in source, f"automated-reviewer class contract missing: {phrase}")


def run_suite() -> None:
    validate_contract_sources()
    with tempfile.TemporaryDirectory(prefix="pr-readiness-assessment-") as temp:
        root = Path(temp)
        first = root / "first"
        second = root / "second"
        revision = build_repository(first)
        repeated_revision = build_repository(second)
        require(revision == repeated_revision, "fixed fixture did not reproduce the same revision")
        bundle = make_bundle(first, revision)
        positive = evaluate(first, bundle)
        require(positive["outcome"] == "pass" and positive["gaps"] == [], f"positive fixture failed: {positive['gaps']}")
        require(positive["capability_version"] == package_version(), "assessment capability version was not live-derived")
        require(positive["observed_at"] != bundle["assessment"]["observed_at"], "assessment observation time stayed caller-controlled")

        spoofed_provenance = copy.deepcopy(bundle)
        spoofed_provenance["assessment"]["capability_version"] = "caller-controlled-spoof"
        spoofed_provenance["assessment"]["observed_at"] = "1900-01-01T00:00:00Z"
        spoofed_result = evaluate(first, spoofed_provenance)
        require(spoofed_result["outcome"] == "pass", f"ignored caller provenance changed the outcome: {spoofed_result['gaps']}")
        require(spoofed_result["capability_version"] != "caller-controlled-spoof", "caller controlled assessment capability version")
        require(spoofed_result["observed_at"] != "1900-01-01T00:00:00Z", "caller controlled assessment observation time")
        for name, variant in variants(bundle).items():
            result = evaluate(first, variant)
            expected_gap = SPEC["negative_variants"][name]
            require(result["outcome"] == "action-required", f"{name} did not fail closed")
            require(expected_gap in result["gaps"], f"{name} missing exact gap: {expected_gap}")

        malicious_marker = first / "malicious-validator-executed"
        (first / "fixture-validation.py").write_text(
            "import pathlib, sys\n"
            f"pathlib.Path({str(malicious_marker)!r}).write_text('executed')\n"
            "print(f'verified:{sys.argv[1]}')\n",
            encoding="utf-8",
        )
        malicious_validator_result = evaluate(first, bundle)
        require(
            "dirty working surface: unstaged" in malicious_validator_result["gaps"],
            "dirty validator did not fail the working-surface check",
        )
        require(not malicious_marker.exists(), "repository-controlled validator was executed")
        run("git", "restore", "fixture-validation.py", cwd=first)

        malformed_bundle = evaluate(first, None)
        require(malformed_bundle["outcome"] == "action-required", "null bundle did not fail closed")
        require("receipt bundle is not an object" in malformed_bundle["gaps"], "null bundle returned no normal assessment gap")

        malformed_assessment = copy.deepcopy(bundle)
        malformed_assessment["assessment"] = None
        malformed_assessment_result = evaluate(first, malformed_assessment)
        require("assessment member is not an object" in malformed_assessment_result["gaps"], "null assessment member did not fail closed")

        (first / "src" / "app.txt").write_text("staged-only\n", encoding="utf-8")
        run("git", "add", "src/app.txt", cwd=first)
        staged_result = evaluate(first, bundle)
        require("dirty working surface: staged" in staged_result["gaps"], "staged-only dirt passed exact-line parsing")
        run("git", "restore", "--staged", "src/app.txt", cwd=first)
        run("git", "restore", "src/app.txt", cwd=first)

        run("git", "branch", "-m", "renamed-target", cwd=first)
        renamed_result = evaluate(first, bundle)
        require("assessment subject mismatch" in renamed_result["gaps"], "renamed branch retained a passing subject")
        run("git", "branch", "-m", "assessment-target", cwd=first)

        run("git", "checkout", "--detach", "-q", cwd=first)
        detached_result = evaluate(first, bundle)
        require("live subject unavailable: detached HEAD" in detached_result["gaps"], "detached HEAD retained a passing subject")
        run("git", "branch", "ambiguous-target", cwd=first)
        ambiguous_result = evaluate(first, bundle)
        require(
            "ambiguous live subject: detached HEAD points at multiple branches" in ambiguous_result["gaps"],
            "ambiguous live branch state retained a passing subject",
        )
        run("git", "checkout", "-q", "assessment-target", cwd=first)
        run("git", "branch", "-D", "ambiguous-target", cwd=first)

        no_reviewer = root / "no-reviewer"
        no_reviewer_revision = build_repository(no_reviewer, "none")
        no_reviewer_result = evaluate(no_reviewer, make_bundle(no_reviewer, no_reviewer_revision))
        require(no_reviewer_result["outcome"] == "pass", f"no-reviewer class 11 was not applicable: {no_reviewer_result['gaps']}")

        missing_cap = root / "missing-cap"
        missing_cap_revision = build_repository(missing_cap, "missing-cap")
        missing_cap_result = evaluate(missing_cap, make_bundle(missing_cap, missing_cap_revision))
        require(
            "automated reviewer cap unresolved: fixture-reviewer" in missing_cap_result["gaps"],
            "configured reviewer without a repository-resolved cap did not fail closed",
        )

        invalid_reviewer_shape = root / "invalid-reviewer-shape"
        invalid_reviewer_revision = build_repository(invalid_reviewer_shape, "invalid-shape")
        invalid_reviewer_result = evaluate(
            invalid_reviewer_shape,
            make_bundle(invalid_reviewer_shape, invalid_reviewer_revision),
        )
        require(
            invalid_reviewer_result["outcome"] == "action-required"
            and "repository automated-reviewer discovery is invalid: FixtureError" in invalid_reviewer_result["gaps"],
            "invalid automated-reviewers shape did not return a normal action-required envelope",
        )

        _, no_reviewer_evidence = evidence_blob(
            no_reviewer,
            no_reviewer_revision,
            "evidence/targeted-sweep.json",
        )
        require(
            json.loads(no_reviewer_evidence)["verdicts"]["11"] == "not applicable",
            "no-reviewer profile did not anchor class 11 as not applicable",
        )

        weak_documents = {
            "repository-gates": {
                "repository": SPEC["repository"],
                "subject": SPEC["subject"],
                "status": "verified",
                "gates": [{"name": "fixture-validation", "owner": "fixture task runner", "status": "verified"}],
            },
            "code-review": {
                "repository": SPEC["repository"],
                "subject": SPEC["subject"],
                "status": "verified",
                "finding_count": 0,
            },
            "testing": {
                "repository": SPEC["repository"],
                "subject": SPEC["subject"],
                "status": "verified",
                "checks": ["fixture-validation"],
                "ui_classification": "not applicable",
            },
        }
        for kind, weak_document in weak_documents.items():
            weak_repo = root / f"weak-{kind}"
            weak_revision = build_repository(
                weak_repo,
                evidence_mutator=lambda documents, kind=kind, weak_document=weak_document: documents.__setitem__(
                    kind, weak_document
                ),
            )
            weak_result = evaluate(weak_repo, make_bundle(weak_repo, weak_revision))
            require(
                f"substantive evidence schema mismatch: {kind}" in weak_result["gaps"],
                f"self-asserted {kind} evidence passed without producer, scope, command, outcome, and result references",
            )

        forged_result_repo = root / "forged-command-result"
        def forge_unrun_command(documents: dict[str, dict[str, Any]]) -> None:
            documents["testing"]["command"] = {"id": "python3", "arguments": ["does-not-exist.py"]}
            documents["testing"]["checks"][0]["command"] = "python3 does-not-exist.py"

        forged_result_revision = build_repository(
            forged_result_repo,
            pre_result_mutator=forge_unrun_command,
        )
        forged_result = evaluate(forged_result_repo, make_bundle(forged_result_repo, forged_result_revision))
        require(forged_result["outcome"] == "action-required", "structurally complete forged command result passed")
        require(
            "command execution not verified: testing" in forged_result["gaps"],
            "structurally complete forged command result did not fail at the owning-runner boundary",
        )

        bad_result_reference_repo = root / "bad-result-reference"
        bad_result_reference_revision = build_repository(
            bad_result_reference_repo,
            evidence_mutator=lambda documents: documents["code-review"]["result_references"][0].__setitem__(
                "sha256", "0" * 64
            ),
        )
        bad_result_reference = evaluate(
            bad_result_reference_repo,
            make_bundle(bad_result_reference_repo, bad_result_reference_revision),
        )
        require(
            "substantive evidence schema mismatch: code-review" in bad_result_reference["gaps"],
            "unresolvable code-review result reference passed as inspectable evidence",
        )

        partial_destination = root / "partial-materialization"
        def fail_bundle_write(path: Path, value: Any) -> None:
            raise OSError("forced bundle write failure")
        try:
            materialize(partial_destination, fail_bundle_write)
            raise FixtureError("forced materialization failure unexpectedly succeeded")
        except OSError:
            require(not partial_destination.exists(), "partial materialization destination survived failure")

        malformed_bundle_path = root / "malformed-bundle.json"
        malformed_bundle_path.write_text("{", encoding="utf-8")
        for label, bundle_path, expected_gap in (
            ("malformed", malformed_bundle_path, "receipt bundle is malformed"),
            ("unreadable", root / "missing-bundle.json", "receipt bundle is unreadable"),
        ):
            completed = subprocess.run(
                [sys.executable, str(Path(__file__).resolve()), "--check", str(first), str(bundle_path)],
                capture_output=True,
                text=True,
            )
            require(completed.returncode == 1 and not completed.stderr, f"{label} bundle did not fail through the normal envelope")
            envelope = json.loads(completed.stdout)
            require(
                envelope["outcome"] == "action-required" and expected_gap in envelope["gaps"],
                f"{label} bundle did not name its normal assessment gap",
            )
        print("PASS: assessment receipts bind one deterministic exact subject and revision")
        print("PASS: versioned bundle resolution, staged-only dirt, and live-subject mutations fail closed")
        print("PASS: absent reviewer is not applicable; configured reviewer without a cap fails closed")
        print("PASS: command-backed evidence effects are verified at the exact revision without executing repository code")


def materialize(destination: Path, bundle_writer: Any = write_json) -> None:
    try:
        destination.mkdir(parents=True, exist_ok=False)
    except FileExistsError as error:
        raise FixtureError(f"destination already exists: {destination}") from error
    try:
        repo = destination / "repo"
        revision = build_repository(repo)
        bundle_path = destination / "assessment-receipts.json"
        bundle_writer(bundle_path, make_bundle(repo, revision))
    except Exception:
        shutil.rmtree(destination)
        raise
    print(json.dumps({"checkout": str(repo), "repository": SPEC["repository"], "receipt_bundle": str(bundle_path), "subject": SPEC["subject"], "exact_revision": revision}, sort_keys=True))


def check_materialized(repo: Path, bundle_path: Path) -> int:
    input_gaps: list[str] = []
    try:
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    except OSError:
        bundle = None
        input_gaps.append("receipt bundle is unreadable")
    except (UnicodeError, json.JSONDecodeError):
        bundle = None
        input_gaps.append("receipt bundle is malformed")
    result = evaluate(repo, bundle, input_gaps)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["outcome"] == "pass" else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--materialize", type=Path)
    group.add_argument("--check", nargs=2, metavar=("REPO", "RECEIPT_BUNDLE"), type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.materialize:
        materialize(args.materialize)
        return 0
    if args.check:
        return check_materialized(args.check[0], args.check[1])
    run_suite()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FixtureError, KeyError, TypeError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
