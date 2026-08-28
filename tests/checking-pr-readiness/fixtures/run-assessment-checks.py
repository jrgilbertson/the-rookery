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
    ".github/repository-gates.json",
    "CHANGELOG.md",
    "fixture-validation.py",
    "src/app.txt",
    *(f"evidence/{kind}.json" for kind in SPEC["required_receipts"]),
    *(f"results/{kind}.json" for kind in SPEC["required_receipts"]),
}
REVIEWER_CONFIG_PATH = ".github/automated-reviewers.json"
VERIFIED_COMMANDS = {
    "repository-gates": ("fixture-validation.py", "gate"),
    "code-review": ("fixture-validation.py", "review"),
    "code-simplification": ("fixture-validation.py", "simplify"),
    "testing": ("fixture-validation.py", "test"),
}
REPOSITORY_GATES = [
    {
        "name": "fixture-validation",
        "owner": "fixture task runner",
        "command": ["python3", "fixture-validation.py", "gate"],
    },
    {
        "name": "fixture-regression",
        "owner": "fixture task runner",
        "command": ["python3", "fixture-validation.py", "test"],
    },
]
FIXTURE_VALIDATION_SOURCE = b"""#!/usr/bin/env python3
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
"""
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
    "testing": {"result_id", "name", "command", "outcome", "exit_code"},
    "plan-versus-delivered": {"result_id", "outcome", "delivered"},
    "learning-signal": {"result_id", "outcome", "summary"},
    "targeted-sweep": {"result_id", "outcome", "class_count"},
    "preflight": {"result_id", "outcome", "unresolved_count"},
}
RECEIPT_FIELDS = {
    "schema",
    "receipt_id",
    "kind",
    "capability",
    "capability_version",
    "repository",
    "subject",
    "exact_revision",
    "evidence_references",
    "outcome",
    "gaps",
    "observed_at",
}
BUNDLE_FIELDS = {"schema", "assessment", "receipts"}
ASSESSMENT_FIELDS = {
    "schema",
    "capability",
    "capability_version",
    "repository",
    "subject",
    "exact_revision",
    "receipt_references",
    "outcome",
    "gaps",
    "observed_at",
    "mode",
}
EVIDENCE_BLOB_CACHE: dict[tuple[str, str, str], tuple[str, bytes]] = {}
MATERIAL_GAP_FIELDS = {"key", "message"}

# Exact-revision assessment must resolve the recorded objects, never a local
# replacement namespace. Child processes inherit this for every Git read.
os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"


class FixtureError(Exception):
    pass


def material_gap(key: str, message: str) -> dict[str, str]:
    """Create one producer-owned, equality-only material-gap item."""
    return {"key": key, "message": message}


def material_gaps_are_valid(gaps: Any) -> bool:
    if not isinstance(gaps, list):
        return False
    keys: list[str] = []
    for item in gaps:
        if (
            not isinstance(item, dict)
            or set(item) != MATERIAL_GAP_FIELDS
            or not isinstance(item.get("key"), str)
            or not item["key"].strip()
            or not isinstance(item.get("message"), str)
            or not item["message"].strip()
        ):
            return False
        keys.append(item["key"])
    return len(keys) == len(set(keys))


def caller_assessment_is_valid(assessment: Any) -> bool:
    """Validate the caller's v2 claim before using any of its members."""
    if not isinstance(assessment, dict) or set(assessment) != ASSESSMENT_FIELDS:
        return False
    if assessment.get("outcome") not in {"pass", "action-required", "UNKNOWN"}:
        return False
    if not material_gaps_are_valid(assessment.get("gaps")):
        return False
    gaps = assessment["gaps"]
    return (assessment["outcome"] == "pass" and not gaps) or (assessment["outcome"] != "pass" and bool(gaps))


def gap_messages(assessment: dict[str, Any]) -> set[str]:
    return {
        item["message"]
        for item in assessment.get("gaps", [])
        if isinstance(item, dict) and isinstance(item.get("message"), str)
    }


def combine_repeated_obligations(gaps: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep one producer-defined key when several details share one repair."""
    combined: list[dict[str, str]] = []
    for gap in gaps:
        existing = next((item for item in combined if item["key"] == gap["key"]), None)
        if existing is None:
            combined.append(dict(gap))
        elif gap["message"] not in existing["message"]:
            existing["message"] = f"{existing['message']}; {gap['message']}"
    return combined


def complete_assessment(
    assessment: dict[str, Any], gaps: list[dict[str, str]], *, unknown: bool = False
) -> dict[str, Any]:
    if not material_gaps_are_valid(gaps):
        assessment["outcome"] = "UNKNOWN"
        assessment["gaps"] = [material_gap(
            "obligation.producer-gap-integrity",
            "assessment material-gap keys are missing, empty, duplicate, or malformed",
        )]
        return assessment
    assessment["gaps"] = list(gaps)
    assessment["outcome"] = "UNKNOWN" if unknown else ("pass" if not gaps else "action-required")
    return assessment


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


def evidence_documents(
    reviewer_mode: str = "configured", reviewer_name: str = "fixture-reviewer"
) -> dict[str, dict[str, Any]]:
    reviewers = reviewer_records(reviewer_mode, reviewer_name)
    if not isinstance(reviewers, list):
        reviewers = []
    class_11, unresolved = reviewer_sweep_evidence(reviewers, len(EXPECTED_CHANGED_PATHS))
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
            [
                {
                    "result_id": f"gate:{gate['name']}",
                    "outcome": "verified",
                    "summary": f"{gate['name']} passed",
                }
                for gate in REPOSITORY_GATES
            ],
            ["fixture-validation.py", "gate"],
            gates=[
                {
                    "name": gate["name"],
                    "owner": gate["owner"],
                    "command": " ".join(gate["command"]),
                    "outcome": "verified",
                    "status": "verified",
                    "result_reference": f"gate:{gate['name']}",
                }
                for gate in REPOSITORY_GATES
            ],
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
            [{
                "result_id": "test:fixture-validation",
                "name": "fixture-validation",
                "command": "python3 fixture-validation.py test",
                "outcome": "passed",
                "exit_code": 0,
            }],
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
            [{
                "result_id": "sweep:summary",
                "outcome": "clear" if not unresolved else "finding",
                "class_count": 11,
            }],
            verdicts=sweep_verdicts,
            unresolved=unresolved,
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
    reviewer_name: str = "fixture-reviewer",
    evidence_mutator: Callable[[dict[str, dict[str, Any]]], None] | None = None,
    pre_result_mutator: Callable[[dict[str, dict[str, Any]]], None] | None = None,
    validator_source: bytes = FIXTURE_VALIDATION_SOURCE,
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
    (path / "fixture-validation.py").write_bytes(validator_source)
    write_json(path / REVIEWER_CONFIG_PATH, {"automated_reviewers": reviewer_records(reviewer_mode, reviewer_name)})
    write_json(path / ".github" / "repository-gates.json", {"gates": REPOSITORY_GATES})
    documents = evidence_documents(reviewer_mode, reviewer_name)
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
            "schema": "checking-pr-readiness-assessment/v2",
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


def make_outside_tree_bundle(
    repo: Path,
    revision: str,
    bundle_id: str | None = None,
) -> dict[str, Any]:
    """Carry complete evidence and result documents in the selected bundle.

    The transport is intentionally outside the assessed commit.  It models a
    caller-owned same-session handoff, while the receipt and both documents
    still bind the exact repository, subject, and revision.
    """
    bundle = make_bundle(repo, revision)
    bundle_id = bundle_id or f"fixture-session:{revision}"
    for receipt in bundle["receipts"]:
        kind = receipt["kind"]
        _, evidence_content = evidence_blob(repo, revision, f"evidence/{kind}.json")
        _, result_content = evidence_blob(repo, revision, f"results/{kind}.json")
        evidence = json.loads(evidence_content)
        result = json.loads(result_content)
        # The transport deliberately does not rely on published per-kind schema
        # names. Its complete, digest-bound semantics are what the assessment
        # evaluates.
        evidence.pop("schema")
        result.pop("schema")
        transport_identity = {
            "repository": SPEC["repository"],
            "subject": SPEC["subject"],
            "exact_revision": revision,
            "bundle_id": bundle_id,
            "receipt_id": receipt["receipt_id"],
        }
        evidence["transport_identity"] = transport_identity
        result["transport_identity"] = transport_identity
        evidence["result_references"] = [{
            "path": f"outside-tree/results/{kind}.json",
            "sha256": hashlib.sha256(json_bytes(result)).hexdigest(),
        }]
        receipt["evidence_references"] = [{
            "transport": "bundle-inline",
            "exact_revision": revision,
            "bundle_id": bundle_id,
            "evidence": evidence,
            "evidence_sha256": hashlib.sha256(json_bytes(evidence)).hexdigest(),
            "result": result,
            "result_sha256": hashlib.sha256(json_bytes(result)).hexdigest(),
        }]
    return bundle


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
    _, content = evidence_blob(repo, revision, REVIEWER_CONFIG_PATH)
    document = json.loads(content)
    reviewers = document.get("automated_reviewers")
    if not isinstance(reviewers, list):
        raise FixtureError("repository automated-reviewer discovery is invalid")
    return reviewers


def reviewer_records(reviewer_mode: str, reviewer_name: str) -> Any:
    if reviewer_mode == "configured":
        return [{"name": reviewer_name, "cap": SPEC["reviewer_cap"]}]
    if reviewer_mode == "none":
        return []
    if reviewer_mode == "no-cap":
        return [{"name": "no-cap-reviewer", "cap": None}]
    if reviewer_mode == "over-and-no-cap":
        return [
            {"name": "over-cap-reviewer", "cap": 0},
            {"name": "no-cap-reviewer", "cap": None},
        ]
    if reviewer_mode == "missing-cap":
        return [{"name": reviewer_name}]
    if reviewer_mode == "unresolved-identity":
        return [{"cap": SPEC["reviewer_cap"]}]
    if reviewer_mode == "failed-lookup":
        return [{"name": "failed-lookup-reviewer", "cap": "invalid"}]
    if reviewer_mode == "invalid-shape":
        return {}
    raise FixtureError(f"unknown reviewer mode: {reviewer_mode}")


def reviewer_cap_lookups(
    reviewers: list[dict[str, Any]],
) -> tuple[list[tuple[str, int]], list[str], list[str]]:
    """Resolve one exact-head reviewer lookup without treating failures as no-cap."""
    known_caps: list[tuple[str, int]] = []
    no_cap_evidence: list[str] = []
    lookup_failures: list[str] = []
    seen_names: set[str] = set()
    for reviewer in reviewers:
        name = reviewer.get("name") if isinstance(reviewer, dict) else None
        if not isinstance(name, str) or not name.strip():
            lookup_failures.append("automated reviewer identity unresolved")
            continue
        if name in seen_names:
            lookup_failures.append(
                f"automated reviewer cap lookup failed: {name} (source: {REVIEWER_CONFIG_PATH}; lookup: ambiguous)"
            )
            continue
        seen_names.add(name)
        if "cap" not in reviewer:
            lookup_failures.append(
                f"automated reviewer cap lookup failed: {name} (source: {REVIEWER_CONFIG_PATH}; lookup: incomplete)"
            )
        elif reviewer["cap"] is None:
            no_cap_evidence.append(
                f"automated reviewer cap unverified: {name} (source: {REVIEWER_CONFIG_PATH}; lookup: no cap)"
            )
        elif type(reviewer["cap"]) is int and reviewer["cap"] >= 0:
            known_caps.append((name, reviewer["cap"]))
        else:
            lookup_failures.append(
                f"automated reviewer cap lookup failed: {name} (source: {REVIEWER_CONFIG_PATH}; lookup: invalid)"
            )
    return known_caps, no_cap_evidence, lookup_failures


def reviewer_sweep_evidence(reviewers: list[dict[str, Any]], surface_count: int) -> tuple[str, list[str]]:
    known_caps, no_cap_evidence, lookup_failures = reviewer_cap_lookups(reviewers)
    exceeded = [name for name, cap in known_caps if surface_count > cap]
    if not reviewers:
        class_11 = "not applicable"
    elif exceeded:
        class_11 = f"exceeds cap for {exceeded[0]}"
    elif no_cap_evidence or lookup_failures:
        class_11 = "cap unverified"
    else:
        class_11 = "under caps"
    return class_11, [*(f"exceeds cap for {name}" for name in exceeded), *no_cap_evidence, *lookup_failures]


def validate_surface(repo: Path, reviewers: list[dict[str, Any]]) -> tuple[list[dict[str, str]], set[str]]:
    inventory = subprocess.run(
        [str(SURFACE), "--full", "--base", "main"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output = inventory.stdout
    known_caps, no_cap_evidence, lookup_failures = reviewer_cap_lookups(reviewers)
    gaps: list[dict[str, str]] = []
    if no_cap_evidence or lookup_failures:
        gaps.append(material_gap(
            "obligation.reviewer-capability",
            "; ".join([*no_cap_evidence, *lookup_failures]),
        ))
    changed = set(run("git", "diff", "--name-only", "main...HEAD", cwd=repo).splitlines())
    if inventory.returncode != 0 or not output.startswith("verdict: cap unverified\n"):
        gaps.append(material_gap("obligation.surface-helper-verdict", "working surface helper returned an unexpected verdict"))
    for name, cap in known_caps:
        completed = subprocess.run(
            [str(SURFACE), "--full", "--base", "main", "--cap", f"{name}={cap}"],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        expected_verdict = f"exceeds cap for {name}" if len(changed) > cap else "under caps"
        if completed.returncode != 0 or not completed.stdout.startswith(f"verdict: {expected_verdict}\n"):
            gaps.append(material_gap(
                "obligation.surface-helper-verdict",
                f"working surface helper returned an unexpected verdict for {name}",
            ))
        elif len(changed) > cap:
            gaps.append(material_gap("obligation.reviewer-cap-excess", expected_verdict))
    output_lines = output.splitlines()
    if changed != EXPECTED_CHANGED_PATHS or output_lines.count(f"committed: {len(changed)}") != 1:
        gaps.append(material_gap("obligation.surface-inventory", "working surface inventory mismatch"))
    omitted_paths = [relative for relative in changed if f"  {relative}\n" not in f"{output}\n"]
    if omitted_paths:
        gaps.append(material_gap(
            "obligation.surface-coverage",
            f"working surface helper omitted paths: {', '.join(sorted(omitted_paths))}",
        ))
    dirty_categories = [category for category in ("staged", "unstaged", "untracked") if output_lines.count(f"{category}: 0") != 1]
    if dirty_categories:
        gaps.append(material_gap(
            "obligation.clean-working-surface",
            f"dirty working surface categories: {', '.join(dirty_categories)}",
        ))
    return gaps, changed


def bounded_text(value: Any, limit: int = 512) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= limit


def text_set(value: Any) -> set[str] | None:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        return None
    return set(value)


def verify_command_evidence(kind: str, command: dict[str, Any], repo: Path, revision: str) -> list[dict[str, str]]:
    expected = VERIFIED_COMMANDS.get(kind)
    if expected is None:
        return []
    if command != {"id": "python3", "arguments": list(expected)}:
        return [material_gap(f"obligation.command-execution.{kind}", f"command execution not verified: {kind}")]
    try:
        validator = git_blob(repo, revision, "fixture-validation.py")
        app_state = git_blob(repo, revision, "src/app.txt")
        changelog = git_blob(repo, revision, "CHANGELOG.md")
    except subprocess.CalledProcessError:
        return [material_gap(f"obligation.command-execution.{kind}", f"command execution not verified: {kind}")]
    if validator != FIXTURE_VALIDATION_SOURCE:
        return [material_gap(f"obligation.command-execution.{kind}", f"command execution not verified: {kind}")]
    try:
        with tempfile.TemporaryDirectory(prefix="pr-readiness-command-") as temp:
            command_root = Path(temp)
            (command_root / "src").mkdir()
            (command_root / "fixture-validation.py").write_bytes(validator)
            (command_root / "src" / "app.txt").write_bytes(app_state)
            (command_root / "CHANGELOG.md").write_bytes(changelog)
            completed = subprocess.run(
                [sys.executable, *expected],
                cwd=command_root,
                capture_output=True,
                text=True,
                timeout=10,
            )
    except (OSError, subprocess.TimeoutExpired):
        return [material_gap(f"obligation.command-execution.{kind}", f"command execution not verified: {kind}")]
    if completed.returncode != 0 or completed.stdout != f"verified:{expected[1]}\n" or completed.stderr:
        return [material_gap(f"obligation.command-execution.{kind}", f"command execution not verified: {kind}")]
    return []


def discover_repository_gates(repo: Path, revision: str) -> list[dict[str, Any]]:
    try:
        document = json.loads(git_blob(repo, revision, ".github/repository-gates.json"))
    except (subprocess.CalledProcessError, UnicodeDecodeError, json.JSONDecodeError):
        raise FixtureError("repository gate discovery is invalid")
    gates = document.get("gates") if isinstance(document, dict) and set(document) == {"gates"} else None
    if (
        not isinstance(gates, list)
        or not gates
        or any(
            not isinstance(gate, dict)
            or set(gate) != {"name", "owner", "command"}
            or not bounded_text(gate.get("name"))
            or not bounded_text(gate.get("owner"))
            or not isinstance(gate.get("command"), list)
            or not gate["command"]
            or any(not bounded_text(argument) for argument in gate["command"])
            for gate in gates
        )
    ):
        raise FixtureError("repository gate discovery is invalid")
    identities = [(gate["name"], gate["owner"], tuple(gate["command"])) for gate in gates]
    if len(identities) != len(set(identities)):
        raise FixtureError("repository gate discovery is invalid")
    return gates


def verify_repository_gate_command(gate: dict[str, Any], repo: Path, revision: str) -> bool:
    arguments = gate["command"]
    if (
        len(arguments) != 3
        or arguments[0] != "python3"
        or arguments[1] != "fixture-validation.py"
        or arguments[2] not in {"gate", "test"}
    ):
        return False
    try:
        validator = git_blob(repo, revision, "fixture-validation.py")
        app_state = git_blob(repo, revision, "src/app.txt")
        changelog = git_blob(repo, revision, "CHANGELOG.md")
    except subprocess.CalledProcessError:
        return False
    if validator != FIXTURE_VALIDATION_SOURCE:
        return False
    try:
        with tempfile.TemporaryDirectory(prefix="pr-readiness-gate-") as temp:
            command_root = Path(temp)
            (command_root / "src").mkdir()
            (command_root / "fixture-validation.py").write_bytes(validator)
            (command_root / "src" / "app.txt").write_bytes(app_state)
            (command_root / "CHANGELOG.md").write_bytes(changelog)
            completed = subprocess.run(
                [sys.executable, *arguments[1:]],
                cwd=command_root,
                capture_output=True,
                text=True,
                timeout=10,
            )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return completed.returncode == 0 and completed.stdout == f"verified:{arguments[2]}\n" and not completed.stderr


def bundled_transport(
    reference: Any,
    revision: str,
    receipt_id: Any,
) -> tuple[dict[str, Any], bytes, str] | None:
    """Resolve one complete, caller-selected outside-tree evidence transport."""
    if (
        not isinstance(reference, dict)
        or set(reference) != {"transport", "exact_revision", "bundle_id", "evidence", "evidence_sha256", "result", "result_sha256"}
        or reference.get("transport") != "bundle-inline"
        or reference.get("exact_revision") != revision
        or not bounded_text(reference.get("bundle_id"))
        or not bounded_text(receipt_id)
        or not isinstance(reference.get("evidence"), dict)
        or not isinstance(reference.get("result"), dict)
        or not all(
            isinstance(reference.get(field), str) and re.fullmatch(r"[0-9a-f]{64}", reference[field])
            for field in ("evidence_sha256", "result_sha256")
        )
    ):
        return None
    evidence = reference["evidence"]
    result_content = json_bytes(reference["result"])
    if (
        hashlib.sha256(json_bytes(evidence)).hexdigest() != reference["evidence_sha256"]
        or hashlib.sha256(result_content).hexdigest() != reference["result_sha256"]
    ):
        return None
    return evidence, result_content, reference["bundle_id"]


def validate_evidence_document(
    kind: str,
    document: Any,
    repo: Path,
    revision: str,
    surface_paths: set[str],
    live_subject: str | None,
    reviewers: list[dict[str, Any]],
    repository: str | None,
    transported_result: bytes | None = None,
    transport_identity: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    if not isinstance(document, dict):
        return [material_gap(f"obligation.evidence-document.{kind}", f"invalid evidence document: {kind}")]

    expected_fields = EVIDENCE_COMMON_FIELDS | EVIDENCE_KIND_FIELDS[kind]
    transported_fields = (expected_fields - {"schema"}) | {"transport_identity"}
    producer = document.get("producer")
    scope = document.get("scope")
    command = document.get("command")
    references = document.get("result_references")
    common_valid = all(
        (
            (
                set(document) == expected_fields
                and document.get("schema") == f"checking-pr-readiness-{kind}-evidence/v1"
            )
            or (
                transported_result is not None
                and transport_identity is not None
                and set(document) == transported_fields
                and document.get("transport_identity") == transport_identity
            ),
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
        return [material_gap(f"obligation.evidence-contract.{kind}", f"substantive evidence schema mismatch: {kind}")]

    reference = references[0]
    expected_result_path = f"results/{kind}.json"
    if (
        not isinstance(reference, dict)
        or set(reference) != {"path", "sha256"}
        or not isinstance(reference.get("path"), str)
        or not reference["path"]
        or reference["path"].startswith("/")
        or ".." in Path(reference["path"]).parts
        or not isinstance(reference.get("sha256"), str)
        or not re.fullmatch(r"[0-9a-f]{64}", reference["sha256"])
        or (transported_result is None and reference["path"] != expected_result_path)
    ):
        return [material_gap(f"obligation.evidence-contract.{kind}", f"substantive evidence schema mismatch: {kind}")]
    try:
        if transported_result is None:
            mode, result_content = evidence_blob(repo, revision, expected_result_path)
        else:
            mode, result_content = "100644", transported_result
        result_document = json.loads(result_content)
    except (subprocess.CalledProcessError, UnicodeDecodeError, json.JSONDecodeError):
        return [material_gap(f"obligation.evidence-contract.{kind}", f"substantive evidence schema mismatch: {kind}")]
    if (
        mode != "100644"
        or hashlib.sha256(result_content).hexdigest() != reference["sha256"]
        or not isinstance(result_document, dict)
        or (
            (
                set(result_document) == {"schema", "producer", "scope", "command", "outcome", "results"}
                and result_document.get("schema") == f"checking-pr-readiness-{kind}-result/v1"
            )
            or (
                transported_result is not None
                and transport_identity is not None
                and set(result_document) == {"producer", "scope", "command", "outcome", "results", "transport_identity"}
                and result_document.get("transport_identity") == transport_identity
            )
        ) is False
        or result_document.get("producer") != producer
        or result_document.get("scope") != scope
        or result_document.get("command") != command
        or result_document.get("outcome") != document.get("outcome")
    ):
        return [material_gap(f"obligation.evidence-contract.{kind}", f"substantive evidence schema mismatch: {kind}")]

    results = result_document.get("results")
    if not isinstance(results, list) or not (0 < len(results) <= 64):
        return [material_gap(f"obligation.evidence-contract.{kind}", f"substantive evidence schema mismatch: {kind}")]
    result_ids: list[str] = []
    for result in results:
        if (
            not isinstance(result, dict)
            or set(result) != EVIDENCE_RESULT_FIELDS[kind]
            or not bounded_text(result.get("result_id"))
            or not bounded_text(result.get("outcome"))
        ):
            return [material_gap(f"obligation.evidence-contract.{kind}", f"substantive evidence schema mismatch: {kind}")]
        result_ids.append(result["result_id"])
    if len(result_ids) != len(set(result_ids)):
        return [material_gap(f"obligation.evidence-contract.{kind}", f"substantive evidence schema mismatch: {kind}")]

    gaps = verify_command_evidence(kind, command, repo, revision)
    if document.get("repository") != repository or document.get("subject") != live_subject:
        gaps.append(material_gap(f"obligation.evidence-identity.{kind}", f"evidence identity mismatch: {kind}"))
    if document.get("status") != "verified":
        gaps.append(material_gap(f"obligation.evidence-verification.{kind}", f"evidence status not verified: {kind}"))
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
            gaps.append(material_gap("obligation.working-surface-evidence", "working surface evidence inventory mismatch"))
        if any(document.get(category) for category in ("staged", "unstaged", "untracked")):
            gaps.append(material_gap("obligation.working-surface-cleanliness", "working surface evidence reports dirty categories"))
    elif kind == "repository-gates":
        gates = document.get("gates", [])
        try:
            discovered_gates = discover_repository_gates(repo, revision)
        except FixtureError:
            discovered_gates = []
        discovered_inventory = {
            (gate["name"], gate["owner"], " ".join(gate["command"])) for gate in discovered_gates
        }
        supplied_inventory = {
            (gate.get("name"), gate.get("owner"), gate.get("command"))
            for gate in gates
            if isinstance(gate, dict)
        } if isinstance(gates, list) else set()
        if (
            not isinstance(gates, list)
            or not gates
            or supplied_inventory != discovered_inventory
            or len(gates) != len(discovered_inventory)
            or not discovered_gates
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
            gaps.append(material_gap("obligation.repository-gate-inventory", "repository gate inventory incomplete"))
        if any(not verify_repository_gate_command(gate, repo, revision) for gate in discovered_gates):
            gaps.append(material_gap("obligation.repository-gate-execution", "repository gate command execution not verified"))
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
            gaps.append(material_gap(f"obligation.evidence-findings.{kind}", f"unresolved finding: {kind}"))
    elif kind == "testing":
        checks = document.get("checks")
        expected_command = " ".join([command["id"], *command["arguments"]])
        check_references = [
            check.get("result_reference")
            for check in checks
            if isinstance(check, dict)
        ] if isinstance(checks, list) else []
        if (
            not isinstance(checks, list)
            or not checks
            or len(checks) != len(results)
            or len(check_references) != len(set(check_references))
            or any(
                not isinstance(check, dict)
                or set(check) != {"name", "command", "outcome", "result_reference"}
                or not bounded_text(check.get("name"))
                or not bounded_text(check.get("command"))
                or check.get("outcome") != "passed"
                or check.get("result_reference") not in result_by_id
                or result_by_id[check["result_reference"]] != {
                    "result_id": check.get("result_reference"),
                    "name": check.get("name"),
                    "command": check.get("command"),
                    "outcome": "passed",
                    "exit_code": 0,
                }
                or check.get("command") != expected_command
                for check in checks
            )
            or document.get("ui_classification") not in {"applicable", "not applicable"}
        ):
            gaps.append(material_gap("obligation.testing-evidence", "testing evidence incomplete"))
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
            gaps.append(material_gap("obligation.delivery-evidence", "plan-versus-delivered evidence incomplete"))
    elif kind == "learning-signal":
        if not bounded_text(document.get("signal")) or len(results) != 1 or not bounded_text(results[0].get("summary")):
            gaps.append(material_gap("obligation.learning-signal-evidence", "learning-signal evidence incomplete"))
    elif kind == "targeted-sweep":
        expected_class_11, expected_unresolved = reviewer_sweep_evidence(reviewers, len(surface_paths))
        expected_verdicts = {**BASE_SWEEP_VERDICTS, "11": expected_class_11}
        unresolved = document.get("unresolved")
        if (
            document.get("verdicts") != expected_verdicts
            or not isinstance(unresolved, list)
            or unresolved != expected_unresolved
            or len(results) != 1
            or results[0].get("outcome") != ("clear" if not expected_unresolved else "finding")
            or results[0].get("class_count") != 11
        ):
            gaps.append(material_gap("obligation.targeted-sweep-evidence", "pre-PR review checks incomplete"))
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
            gaps.append(material_gap("obligation.preflight-evidence", "preflight evidence incomplete"))
    return gaps


def evaluate(repo: Path, bundle: Any, input_gaps: list[dict[str, str]] | None = None) -> dict[str, Any]:
    revision = run("git", "rev-parse", "HEAD", cwd=repo)
    live_subject, subject_gaps = resolve_live_subject(repo)
    live_repository, repository_gaps = resolve_live_repository(repo)
    assessment = {
        "schema": "checking-pr-readiness-assessment/v2",
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
    gaps = [
        *(input_gaps or []),
        *(material_gap("obligation.live-subject", message) for message in subject_gaps),
        *(material_gap("obligation.live-repository", message) for message in repository_gaps),
    ]
    try:
        reviewers = reviewer_configuration(repo, revision)
    except (FixtureError, json.JSONDecodeError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        reviewers = []
        gaps.append(material_gap(
            "obligation.reviewer-configuration",
            f"repository automated-reviewer discovery is invalid: {type(error).__name__}",
        ))
    surface_gaps, surface_paths = validate_surface(repo, reviewers)
    gaps.extend(surface_gaps)
    commit_time = datetime.fromisoformat(run("git", "show", "-s", "--format=%cI", revision, cwd=repo))
    if not isinstance(bundle, dict):
        gaps.append(material_gap("obligation.bundle-object", "receipt bundle is not an object"))
        bundle = {}
        supplied_assessment: dict[str, Any] = {}
    else:
        supplied_assessment = bundle.get("assessment")
        if not caller_assessment_is_valid(supplied_assessment):
            return complete_assessment(
                assessment,
                [material_gap(
                    "obligation.caller-assessment-integrity",
                    "caller assessment claim must use the complete v2 shape with a valid outcome and unique material-gap keys",
                )],
                unknown=True,
            )
    if set(bundle) != BUNDLE_FIELDS:
        gaps.append(material_gap("obligation.bundle-fields", "receipt bundle fields mismatch"))
    if bundle.get("schema") != "checking-pr-readiness-receipt-bundle/v1":
        gaps.append(material_gap("obligation.bundle-schema", "receipt bundle schema mismatch"))
    receipts = bundle.get("receipts", [])
    if not isinstance(receipts, list):
        gaps.append(material_gap("obligation.bundle-receipts", "receipt bundle did not resolve receipts"))
        receipts = []
    valid_receipts: list[dict[str, Any]] = []
    invalid_receipt_members = 0
    invalid_receipt_kinds = 0
    for receipt in receipts:
        if not isinstance(receipt, dict):
            invalid_receipt_members += 1
        elif not isinstance(receipt.get("kind"), str):
            invalid_receipt_kinds += 1
        else:
            valid_receipts.append(receipt)
    if invalid_receipt_members:
        gaps.append(material_gap(
            "obligation.receipt-members",
            "receipt bundle contains invalid receipt members",
        ))
    if invalid_receipt_kinds:
        gaps.append(material_gap(
            "obligation.receipt-kinds",
            "receipt bundle contains receipts without usable kinds",
        ))
    by_kind = {receipt.get("kind"): receipt for receipt in valid_receipts}
    evidence_documents_by_kind: dict[str, Any] = {}
    transported_results_by_kind: dict[str, bytes] = {}
    transport_identities_by_kind: dict[str, dict[str, Any]] = {}
    inline_bundle_id: str | None = None

    if len(by_kind) != len(valid_receipts):
        gaps.append(material_gap("obligation.receipt-kind-uniqueness", "duplicate receipt kind"))

    for kind in SPEC["required_receipts"]:
        receipt = by_kind.get(kind)
        if receipt is None:
            gaps.append(material_gap(f"obligation.required-receipt.{kind}", f"missing receipt: {kind}"))
            continue
        if set(receipt) != RECEIPT_FIELDS or not isinstance(receipt.get("gaps"), list):
            gaps.append(material_gap(f"obligation.receipt-shape.{kind}", "invalid receipt fields"))
        if receipt.get("schema") != "checking-pr-readiness-evidence/v1":
            gaps.append(material_gap(f"obligation.receipt-schema.{kind}", f"invalid receipt schema: {kind}"))
        if receipt.get("receipt_id") != f"receipt:{kind}":
            gaps.append(material_gap(f"obligation.receipt-identity.{kind}", f"invalid receipt identity: {kind}"))
        if receipt.get("capability") != "checking-pr-readiness" or not receipt.get("capability_version"):
            gaps.append(material_gap(f"obligation.receipt-capability.{kind}", f"invalid receipt capability: {kind}"))
        if receipt.get("repository") != live_repository:
            gaps.append(material_gap(f"obligation.receipt-repository.{kind}", f"cross-repository receipt: {kind}"))
        if receipt.get("subject") != live_subject:
            gaps.append(material_gap(f"obligation.receipt-subject.{kind}", f"cross-subject receipt: {kind}"))
        if receipt.get("exact_revision") != revision:
            gaps.append(material_gap(f"obligation.receipt-revision.{kind}", f"cross-revision receipt: {kind}"))
        try:
            observed = datetime.fromisoformat(receipt["observed_at"])
            if observed < commit_time:
                gaps.append(material_gap(f"obligation.receipt-freshness.{kind}", f"stale receipt: {kind}"))
        except (KeyError, ValueError, TypeError):
            gaps.append(material_gap(f"obligation.receipt-observation.{kind}", f"invalid observation time: {kind}"))
        if receipt.get("outcome") == "bypassed" or receipt.get("bypass_requested"):
            gaps.append(material_gap(f"obligation.receipt-bypass.{kind}", f"bypass request: {kind}"))
        elif receipt.get("outcome") not in {"verified", "not applicable"} or receipt.get("gaps") != []:
            gaps.append(material_gap(f"obligation.receipt-findings.{kind}", f"unresolved finding: {kind}"))
        references = receipt.get("evidence_references", [])
        if not isinstance(references, list) or not references:
            gaps.append(material_gap(f"obligation.evidence-reference.{kind}", f"missing evidence reference: {kind}"))
            references = []
        expected_path = f"evidence/{kind}.json"
        if len(references) != 1:
            gaps.append(material_gap(f"obligation.evidence-reference-inventory.{kind}", f"evidence inventory mismatch: {kind}"))
        for reference in references:
            if not isinstance(reference, dict):
                gaps.append(material_gap(f"obligation.evidence-reference.{kind}", f"invalid evidence reference: {kind}"))
                continue
            transport = bundled_transport(reference, revision, receipt.get("receipt_id"))
            if transport is not None:
                evidence, result_content, reference_bundle_id = transport
                if inline_bundle_id is None:
                    inline_bundle_id = reference_bundle_id
                elif reference_bundle_id != inline_bundle_id:
                    gaps.append(material_gap(f"obligation.inline-bundle-identity.{kind}", f"mixed inline bundle identity: {kind}"))
                evidence_documents_by_kind[kind] = evidence
                transported_results_by_kind[kind] = result_content
                transport_identities_by_kind[kind] = {
                    "repository": live_repository,
                    "subject": live_subject,
                    "exact_revision": revision,
                    "bundle_id": reference_bundle_id,
                    "receipt_id": receipt.get("receipt_id"),
                }
                continue
            relative = reference.get("path")
            if (
                set(reference) != {"path", "sha256"}
                or relative != expected_path
                or not isinstance(relative, str)
                or not relative
                or relative.startswith("/")
                or ".." in Path(relative).parts
            ):
                gaps.append(material_gap(f"obligation.evidence-reference.{kind}", f"invalid evidence reference: {kind}"))
                continue
            try:
                mode, content = evidence_blob(repo, revision, relative)
            except (subprocess.CalledProcessError, IndexError):
                gaps.append(material_gap(f"obligation.evidence-availability.{kind}", f"missing evidence: {kind}"))
                continue
            if mode != "100644":
                gaps.append(material_gap(f"obligation.evidence-file.{kind}", f"non-regular evidence: {kind}"))
            if hashlib.sha256(content).hexdigest() != reference.get("sha256"):
                gaps.append(material_gap(f"obligation.evidence-digest.{kind}", f"evidence digest mismatch: {kind}"))
            if relative == expected_path:
                try:
                    evidence_documents_by_kind[kind] = json.loads(content)
                except (UnicodeDecodeError, json.JSONDecodeError):
                    gaps.append(material_gap(f"obligation.evidence-document.{kind}", f"invalid evidence document: {kind}"))

    for kind in SPEC["required_receipts"]:
        if kind in evidence_documents_by_kind:
            gaps.extend(validate_evidence_document(
                kind,
                evidence_documents_by_kind[kind],
                repo,
                revision,
                surface_paths,
                live_subject,
                reviewers,
                live_repository,
                transported_results_by_kind.get(kind),
                transport_identities_by_kind.get(kind),
            ))

    expected_ids = {f"receipt:{kind}" for kind in SPEC["required_receipts"]}
    raw_receipt_references = supplied_assessment.get("receipt_references", [])
    receipt_inventory_mismatch = not isinstance(raw_receipt_references, list)
    if receipt_inventory_mismatch:
        receipt_references: list[str] = []
    else:
        receipt_references = [reference for reference in raw_receipt_references if isinstance(reference, str)]
        if len(receipt_references) != len(raw_receipt_references):
            gaps.append(material_gap("obligation.assessment-receipt-reference", "invalid assessment receipt reference"))
    if set(receipt_references) != expected_ids:
        receipt_inventory_mismatch = True
    if receipt_inventory_mismatch:
        gaps.append(material_gap("obligation.assessment-receipt-inventory", "assessment receipt inventory mismatch"))
    receipt_ids = [receipt.get("receipt_id") for receipt in valid_receipts]
    if len(receipt_references) != len(set(receipt_references)):
        gaps.append(material_gap("obligation.assessment-receipt-reference-uniqueness", "duplicate assessment receipt reference"))
    if set(receipt_ids) - set(receipt_references):
        gaps.append(material_gap("obligation.unreferenced-receipt", "receipt bundle contains unreferenced receipt"))
    for reference in receipt_references:
        if receipt_ids.count(reference) != 1:
            gaps.append(material_gap(
                "obligation.assessment-receipt-resolution",
                f"unresolved receipt reference: {reference}",
            ))
    if supplied_assessment.get("schema") != "checking-pr-readiness-assessment/v2":
        gaps.append(material_gap("obligation.assessment-schema", "assessment schema mismatch"))
    if supplied_assessment.get("capability") != "checking-pr-readiness":
        gaps.append(material_gap("obligation.assessment-capability", "assessment capability mismatch"))
    if supplied_assessment.get("mode") != "assessment-only":
        gaps.append(material_gap("obligation.assessment-mode", "assessment mode mismatch"))
    if supplied_assessment.get("repository") != live_repository:
        gaps.append(material_gap("obligation.assessment-repository", "assessment repository mismatch"))
    if supplied_assessment.get("subject") != live_subject:
        gaps.append(material_gap("obligation.assessment-subject", "assessment subject mismatch"))
    if supplied_assessment.get("exact_revision") != revision:
        gaps.append(material_gap("obligation.assessment-revision", "assessment revision mismatch"))
    if not OID.fullmatch(revision):
        gaps.append(material_gap("obligation.live-revision", "assessment revision is not a full Git OID"))

    assessment["receipt_references"] = receipt_references
    return complete_assessment(assessment, combine_repeated_obligations(gaps))


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
        "`checking-pr-readiness-assessment/v2`",
        "`checking-pr-readiness-evidence/v1`",
        "`receipt_references`",
        "Resolve every receipt reference exactly once",
        "A detached HEAD cannot support a branch subject",
        "Repository-authored evidence and result JSON cannot authenticate their own execution",
        "same-session bundle",
        "published per-kind JSON Schema document",
        "combine documents from concurrent Workers",
    ):
        require(phrase in assessment_words, f"assessment bundle contract missing: {phrase}")
    for source, phrase in (
        (sweep_words, "no automated reviewer is configured"),
        (sweep_words, "not applicable"),
        (sweep_words, "successful authoritative `no cap` lookup"),
        (assessment_words, "resolved reviewer, source, and lookup outcome"),
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
        require(positive["schema"] == "checking-pr-readiness-assessment/v2", "positive fixture did not emit assessment v2")
        require(material_gaps_are_valid(positive["gaps"]), "positive fixture did not emit valid material gaps")
        require(positive["capability_version"] == package_version(), "assessment capability version was not live-derived")
        require(positive["observed_at"] != bundle["assessment"]["observed_at"], "assessment observation time stayed caller-controlled")

        for malformed_gaps in (
            [{"message": "missing key"}],
            [material_gap("", "empty key")],
            [material_gap("caller-key", "first"), material_gap("caller-key", "second")],
            [{"key": "caller-key", "message": "extra field", "extra": True}],
        ):
            malformed_claim = copy.deepcopy(bundle)
            malformed_claim["assessment"]["gaps"] = malformed_gaps
            malformed_result = evaluate(first, malformed_claim)
            require(
                malformed_result["outcome"] == "UNKNOWN"
                and material_gaps_are_valid(malformed_result["gaps"]),
                "malformed caller assessment gaps did not fail closed at evaluate",
            )

        missing_first = evaluate(first, variants(bundle)["missing-receipt"])
        missing_second = evaluate(second, variants(make_bundle(second, repeated_revision))["missing-receipt"])
        require(
            "missing receipt: code-review" in gap_messages(missing_first)
            and material_gaps_are_valid(missing_first["gaps"]),
            "missing receipt did not emit a valid human-readable gap",
        )
        require(
            {item["key"] for item in missing_first["gaps"]} == {item["key"] for item in missing_second["gaps"]},
            "the same atomic obligation changed keys across identical exact heads",
        )

        null_first = copy.deepcopy(bundle)
        null_first["receipts"][0] = None
        null_last = copy.deepcopy(bundle)
        null_last["receipts"].append(null_last["receipts"].pop(0))
        null_last["receipts"][-1] = None
        null_first_result = evaluate(first, null_first)
        null_last_result = evaluate(first, null_last)
        require(
            {item["key"] for item in null_first_result["gaps"]}
            == {item["key"] for item in null_last_result["gaps"]}
            and material_gaps_are_valid(null_first_result["gaps"])
            and material_gaps_are_valid(null_last_result["gaps"]),
            "moving the same invalid receipt changed its opaque key or envelope shape",
        )

        missing_review = copy.deepcopy(bundle)
        missing_review["receipts"] = [
            receipt for receipt in missing_review["receipts"] if receipt["kind"] != "code-review"
        ]
        missing_review["assessment"]["receipt_references"].remove("receipt:code-review")
        missing_review_result = evaluate(first, missing_review)
        missing_review_keys = {
            item["key"]
            for item in missing_review_result["gaps"]
            if item["message"] == "missing receipt: code-review"
        }

        missing_two = copy.deepcopy(missing_review)
        missing_two["receipts"] = [
            receipt for receipt in missing_two["receipts"] if receipt["kind"] != "code-simplification"
        ]
        missing_two["assessment"]["receipt_references"].remove("receipt:code-simplification")
        missing_two_result = evaluate(first, missing_two)
        missing_two_keys = {
            item["key"]
            for item in missing_two_result["gaps"]
            if item["message"] in {"missing receipt: code-review", "missing receipt: code-simplification"}
        }
        require(
            len(missing_review_keys) == 1
            and len(missing_two_keys) == 2
            and missing_review_keys <= missing_two_keys
            and material_gaps_are_valid(missing_two_result["gaps"]),
            "independent missing receipts did not retain unique atomic obligation keys",
        )

        reordered_missing_two = copy.deepcopy(missing_two)
        reordered_missing_two["receipts"].reverse()
        reordered_missing_two["assessment"]["receipt_references"].reverse()
        reordered_missing_two_result = evaluate(first, reordered_missing_two)
        require(
            missing_two_keys
            == {
                item["key"]
                for item in reordered_missing_two_result["gaps"]
                if item["message"] in {"missing receipt: code-review", "missing receipt: code-simplification"}
            },
            "reordering independent missing receipts changed their opaque keys",
        )

        one_invalid_reference = copy.deepcopy(bundle)
        review_receipt = next(
            receipt for receipt in one_invalid_reference["receipts"] if receipt["kind"] == "code-review"
        )
        review_receipt["evidence_references"] = [{}]
        one_invalid_reference_result = evaluate(first, one_invalid_reference)
        one_reference_keys = {
            item["key"]
            for item in one_invalid_reference_result["gaps"]
            if item["message"] == "invalid evidence reference: code-review"
        }

        combined_invalid_references = copy.deepcopy(one_invalid_reference)
        combined_review_receipt = next(
            receipt for receipt in combined_invalid_references["receipts"] if receipt["kind"] == "code-review"
        )
        combined_review_receipt["evidence_references"] = [{}, {}]
        combined_invalid_references_result = evaluate(first, combined_invalid_references)
        combined_reference_keys = {
            item["key"]
            for item in combined_invalid_references_result["gaps"]
            if item["message"] == "invalid evidence reference: code-review"
        }
        require(
            len(one_reference_keys) == len(combined_reference_keys) == 1
            and one_reference_keys == combined_reference_keys,
            "split and combined details of one obligation changed its key",
        )

        combined_with_missing_receipt = copy.deepcopy(combined_invalid_references)
        combined_with_missing_receipt["receipts"] = [
            receipt for receipt in combined_with_missing_receipt["receipts"]
            if receipt["kind"] != "code-simplification"
        ]
        combined_with_missing_receipt["assessment"]["receipt_references"].remove(
            "receipt:code-simplification"
        )
        combined_with_missing_receipt_result = evaluate(first, combined_with_missing_receipt)
        require(
            combined_reference_keys <= {item["key"] for item in combined_with_missing_receipt_result["gaps"]}
            and any(
                item["message"] == "missing receipt: code-simplification"
                for item in combined_with_missing_receipt_result["gaps"]
            ),
            "combining one obligation suppressed another independent obligation",
        )

        first_missing_cap = root / "first-missing-cap"
        second_missing_cap = root / "second-missing-cap"
        first_missing_cap_revision = build_repository(
            first_missing_cap, "missing-cap", "first-presentation"
        )
        second_missing_cap_revision = build_repository(
            second_missing_cap, "missing-cap", "second-presentation"
        )
        first_missing_cap_result = evaluate(
            first_missing_cap, make_bundle(first_missing_cap, first_missing_cap_revision)
        )
        second_missing_cap_result = evaluate(
            second_missing_cap, make_bundle(second_missing_cap, second_missing_cap_revision)
        )
        first_cap_gaps = [gap for gap in first_missing_cap_result["gaps"] if "cap lookup failed" in gap["message"]]
        second_cap_gaps = [gap for gap in second_missing_cap_result["gaps"] if "cap lookup failed" in gap["message"]]
        require(
            len(first_cap_gaps) == len(second_cap_gaps) == 1
            and first_cap_gaps[0]["key"] == second_cap_gaps[0]["key"]
            and first_cap_gaps[0]["message"] != second_cap_gaps[0]["message"],
            "a real producer message presentation changed an atomic obligation key",
        )

        documented_inline_bundle = json.loads(json.dumps(make_outside_tree_bundle(first, revision)))
        require(
            set(documented_inline_bundle) == {"schema", "assessment", "receipts"},
            "documented inline bundle has an unpublished top-level member",
        )
        outside_tree = evaluate(first, documented_inline_bundle)
        require(
            outside_tree["outcome"] == "pass" and outside_tree["gaps"] == [],
            f"complete outside-tree transport failed: {outside_tree['gaps']}",
        )
        hidden_top_level_bundle = copy.deepcopy(documented_inline_bundle)
        hidden_top_level_bundle["bundle_id"] = "unpublished"
        hidden_top_level_result = evaluate(first, hidden_top_level_bundle)
        require(
            hidden_top_level_result["outcome"] == "action-required"
            and "receipt bundle fields mismatch" in gap_messages(hidden_top_level_result),
            "unpublished top-level bundle member was accepted",
        )
        old_bundle = make_outside_tree_bundle(first, revision)
        later = root / "later"
        later_revision = build_repository(later)
        run(
            "git", "commit", "--allow-empty", "-q", "-m", "later same-surface assessment", cwd=later, env=git_env(COMMIT_TIME)
        )
        later_revision = run("git", "rev-parse", "HEAD", cwd=later)
        missing_later = evaluate(later, variants(make_bundle(later, later_revision))["missing-receipt"])
        require(
            {item["key"] for item in missing_first["gaps"]} == {item["key"] for item in missing_later["gaps"]},
            "the same atomic obligation changed keys across different exact heads",
        )
        transplanted_revision_bundle = make_outside_tree_bundle(later, later_revision)
        target_revision_reference = copy.deepcopy(
            transplanted_revision_bundle["receipts"][2]["evidence_references"][0]
        )
        transplanted_revision_bundle["receipts"][2]["evidence_references"] = copy.deepcopy(
            old_bundle["receipts"][2]["evidence_references"]
        )
        transplanted_revision_bundle["receipts"][2]["evidence_references"][0]["exact_revision"] = later_revision
        transplanted_revision_bundle["receipts"][2]["evidence_references"][0]["bundle_id"] = target_revision_reference["bundle_id"]
        transplanted_revision_result = evaluate(later, transplanted_revision_bundle)
        require(
            transplanted_revision_result["outcome"] == "action-required",
            "same-kind evidence from an older revision satisfied a newer bundle",
        )
        first_worker_bundle = make_outside_tree_bundle(first, revision, "fixture-session:worker-one")
        second_worker_bundle = make_outside_tree_bundle(first, revision, "fixture-session:worker-two")
        second_worker_reference = copy.deepcopy(
            second_worker_bundle["receipts"][2]["evidence_references"][0]
        )
        second_worker_bundle["receipts"][2]["evidence_references"] = copy.deepcopy(
            first_worker_bundle["receipts"][2]["evidence_references"]
        )
        second_worker_bundle["receipts"][2]["evidence_references"][0]["bundle_id"] = second_worker_reference["bundle_id"]
        cross_bundle_result = evaluate(first, second_worker_bundle)
        require(
            cross_bundle_result["outcome"] == "action-required",
            "same-kind evidence from another Worker bundle satisfied this bundle",
        )
        outside_tree_missing = make_outside_tree_bundle(first, revision)
        del outside_tree_missing["receipts"][0]["evidence_references"][0]["result"]
        missing_transport_result = evaluate(first, outside_tree_missing)
        require(
            missing_transport_result["outcome"] == "action-required"
            and "invalid evidence reference: working-surface" in gap_messages(missing_transport_result),
            "missing outside-tree result did not fail closed",
        )
        outside_tree_altered = make_outside_tree_bundle(first, revision)
        outside_tree_altered["receipts"][0]["evidence_references"][0]["result"]["outcome"] = "altered"
        altered_transport_result = evaluate(first, outside_tree_altered)
        require(
            altered_transport_result["outcome"] == "action-required"
            and "invalid evidence reference: working-surface" in gap_messages(altered_transport_result),
            "altered outside-tree result did not fail closed",
        )
        outside_tree_cross_revision = make_outside_tree_bundle(first, revision)
        outside_tree_cross_revision["receipts"][0]["evidence_references"][0]["exact_revision"] = "0" * 40
        cross_transport_result = evaluate(first, outside_tree_cross_revision)
        require(
            cross_transport_result["outcome"] == "action-required"
            and "invalid evidence reference: working-surface" in gap_messages(cross_transport_result),
            "cross-revision outside-tree transport did not fail closed",
        )
        outside_tree_cross_repository = make_outside_tree_bundle(first, revision)
        outside_tree_cross_repository["receipts"][0]["repository"] = "https://example.invalid/other.git"
        cross_repository_result = evaluate(first, outside_tree_cross_repository)
        require(
            cross_repository_result["outcome"] == "action-required"
            and "cross-repository receipt: working-surface" in gap_messages(cross_repository_result),
            "cross-repository outside-tree receipt did not fail closed",
        )
        outside_tree_mixed = make_outside_tree_bundle(first, revision)
        outside_tree_mixed["receipts"][0]["evidence_references"] = copy.deepcopy(
            outside_tree_mixed["receipts"][1]["evidence_references"]
        )
        mixed_transport_result = evaluate(first, outside_tree_mixed)
        require(
            mixed_transport_result["outcome"] == "action-required"
            and "substantive evidence schema mismatch: working-surface" in gap_messages(mixed_transport_result),
            "concurrent bundle evidence satisfied another receipt kind",
        )

        run("git", "checkout", "-q", "-b", "replacement-payload", revision, cwd=first)
        (first / "src" / "app.txt").write_text("replacement\n", encoding="utf-8")
        run("git", "add", "src/app.txt", cwd=first)
        run("git", "commit", "-q", "-m", "create replacement payload", cwd=first, env=git_env(COMMIT_TIME))
        replacement_revision = run("git", "rev-parse", "HEAD", cwd=first)
        run("git", "checkout", "-q", "assessment-target", cwd=first)
        run("git", "replace", revision, replacement_revision, cwd=first)
        replacement_enabled_env = os.environ.copy()
        replacement_enabled_env.pop("GIT_NO_REPLACE_OBJECTS")
        require(
            run("git", "show", f"{revision}:src/app.txt", cwd=first, env=replacement_enabled_env) == "replacement",
            "fixture replacement object did not override the assessed commit",
        )
        replacement_result = evaluate(first, bundle)
        require(
            replacement_result["outcome"] == "pass" and replacement_result["exact_revision"] == revision,
            f"replacement object changed exact-revision assessment: {replacement_result['gaps']}",
        )
        run("git", "replace", "-d", revision, cwd=first)

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
            require(expected_gap in gap_messages(result), f"{name} missing exact gap: {expected_gap}")

        malicious_marker = first / "malicious-validator-executed"
        (first / "fixture-validation.py").write_text(
            "import pathlib, sys\n"
            f"pathlib.Path({str(malicious_marker)!r}).write_text('executed')\n"
            "print(f'verified:{sys.argv[1]}')\n",
            encoding="utf-8",
        )
        malicious_validator_result = evaluate(first, bundle)
        require(
            "dirty working surface categories: unstaged" in gap_messages(malicious_validator_result),
            "dirty validator did not fail the working-surface check",
        )
        require(not malicious_marker.exists(), "repository-controlled validator was executed")
        run("git", "restore", "fixture-validation.py", cwd=first)

        committed_malicious_repo = root / "committed-malicious-validator"
        committed_malicious_marker = root / "committed-malicious-validator-executed"
        committed_malicious_source = (
            "import pathlib, sys\n"
            f"pathlib.Path({str(committed_malicious_marker)!r}).write_text('executed')\n"
            "print(f'verified:{sys.argv[1]}')\n"
        ).encode("utf-8")
        committed_malicious_revision = build_repository(
            committed_malicious_repo,
            validator_source=committed_malicious_source,
        )
        committed_malicious_result = evaluate(
            committed_malicious_repo,
            make_bundle(committed_malicious_repo, committed_malicious_revision),
        )
        require(
            committed_malicious_result["outcome"] == "action-required"
            and any("command execution not verified: testing" in message for message in gap_messages(committed_malicious_result)),
            "committed non-allowlisted validator was not rejected",
        )
        require(not committed_malicious_marker.exists(), "committed non-allowlisted validator was executed")

        malformed_bundle = evaluate(first, None)
        require(malformed_bundle["outcome"] == "action-required", "null bundle did not fail closed")
        require("receipt bundle is not an object" in gap_messages(malformed_bundle), "null bundle returned no normal assessment gap")

        for malformed_outer_assessment in (None, [], "not an assessment"):
            malformed_assessment = copy.deepcopy(bundle)
            malformed_assessment["assessment"] = malformed_outer_assessment
            malformed_assessment_result = evaluate(first, malformed_assessment)
            require(
                malformed_assessment_result["outcome"] == "UNKNOWN"
                and material_gaps_are_valid(malformed_assessment_result["gaps"])
                and len(malformed_assessment_result["gaps"]) == 1,
                "non-object caller assessment did not return one valid UNKNOWN envelope",
            )

        missing_outer_assessment = copy.deepcopy(bundle)
        del missing_outer_assessment["assessment"]
        missing_outer_assessment_result = evaluate(first, missing_outer_assessment)
        require(
            missing_outer_assessment_result["outcome"] == "UNKNOWN"
            and material_gaps_are_valid(missing_outer_assessment_result["gaps"])
            and len(missing_outer_assessment_result["gaps"]) == 1,
            "missing caller assessment did not return one valid UNKNOWN envelope",
        )

        (first / "src" / "app.txt").write_text("staged-only\n", encoding="utf-8")
        run("git", "add", "src/app.txt", cwd=first)
        staged_result = evaluate(first, bundle)
        require("dirty working surface categories: staged" in gap_messages(staged_result), "staged-only dirt passed exact-line parsing")
        run("git", "restore", "--staged", "src/app.txt", cwd=first)
        run("git", "restore", "src/app.txt", cwd=first)

        run("git", "branch", "-m", "renamed-target", cwd=first)
        renamed_result = evaluate(first, bundle)
        require("assessment subject mismatch" in gap_messages(renamed_result), "renamed branch retained a passing subject")
        run("git", "branch", "-m", "assessment-target", cwd=first)

        run("git", "checkout", "--detach", "-q", cwd=first)
        detached_result = evaluate(first, bundle)
        require("live subject unavailable: detached HEAD" in gap_messages(detached_result), "detached HEAD retained a passing subject")
        run("git", "branch", "ambiguous-target", cwd=first)
        ambiguous_result = evaluate(first, bundle)
        require(
            "ambiguous live subject: detached HEAD points at multiple branches" in gap_messages(ambiguous_result),
            "ambiguous live branch state retained a passing subject",
        )
        run("git", "checkout", "-q", "assessment-target", cwd=first)
        run("git", "branch", "-D", "ambiguous-target", cwd=first)

        no_reviewer = root / "no-reviewer"
        no_reviewer_revision = build_repository(no_reviewer, "none")
        no_reviewer_result = evaluate(no_reviewer, make_bundle(no_reviewer, no_reviewer_revision))
        require(no_reviewer_result["outcome"] == "pass", f"no-reviewer class 11 was not applicable: {no_reviewer_result['gaps']}")

        under_cap = root / "under-cap-reviewer"
        under_cap_revision = build_repository(under_cap, "configured", "under-cap-reviewer")
        under_cap_result = evaluate(under_cap, make_bundle(under_cap, under_cap_revision))
        require(
            under_cap_result["outcome"] == "pass",
            f"a known under-cap reviewer did not pass independently: {under_cap_result['gaps']}",
        )

        no_cap = root / "resolved-no-cap"
        no_cap_revision = build_repository(no_cap, "no-cap")
        no_cap_result = evaluate(no_cap, make_bundle(no_cap, no_cap_revision))
        require(
            no_cap_result["outcome"] == "action-required"
            and "automated reviewer cap unverified: no-cap-reviewer (source: .github/automated-reviewers.json; lookup: no cap)" in gap_messages(no_cap_result),
            "a resolved reviewer with an authoritative no-cap result was not recorded as process-only cap-unverified evidence",
        )
        _, no_cap_evidence = evidence_blob(no_cap, no_cap_revision, "evidence/targeted-sweep.json")
        require(
            json.loads(no_cap_evidence)["unresolved"] == [
                "automated reviewer cap unverified: no-cap-reviewer (source: .github/automated-reviewers.json; lookup: no cap)"
            ],
            "exact-head no-cap evidence did not name the reviewer, source, and lookup outcome",
        )

        over_and_no_cap = root / "over-and-no-cap"
        over_and_no_cap_revision = build_repository(over_and_no_cap, "over-and-no-cap")
        over_and_no_cap_result = evaluate(
            over_and_no_cap,
            make_bundle(over_and_no_cap, over_and_no_cap_revision),
        )
        over_and_no_cap_messages = gap_messages(over_and_no_cap_result)
        require(
            "exceeds cap for over-cap-reviewer" in over_and_no_cap_messages
            and "automated reviewer cap unverified: no-cap-reviewer (source: .github/automated-reviewers.json; lookup: no cap)" in over_and_no_cap_messages,
            "a no-cap reviewer hid an independently exceeded known reviewer cap",
        )

        unresolved_identity = root / "unresolved-reviewer-identity"
        unresolved_identity_revision = build_repository(unresolved_identity, "unresolved-identity")
        unresolved_identity_result = evaluate(
            unresolved_identity,
            make_bundle(unresolved_identity, unresolved_identity_revision),
        )
        require(
            unresolved_identity_result["outcome"] == "action-required"
            and "automated reviewer identity unresolved" in gap_messages(unresolved_identity_result),
            "an unresolved reviewer identity was treated as a successful no-cap lookup",
        )

        failed_lookup = root / "failed-reviewer-cap-lookup"
        failed_lookup_revision = build_repository(failed_lookup, "failed-lookup")
        failed_lookup_result = evaluate(
            failed_lookup,
            make_bundle(failed_lookup, failed_lookup_revision),
        )
        require(
            failed_lookup_result["outcome"] == "action-required"
            and "automated reviewer cap lookup failed: failed-lookup-reviewer (source: .github/automated-reviewers.json; lookup: invalid)" in gap_messages(failed_lookup_result),
            "a failed reviewer-cap lookup was treated as a successful no-cap lookup",
        )

        missing_cap = root / "missing-cap"
        missing_cap_revision = build_repository(missing_cap, "missing-cap")
        missing_cap_result = evaluate(missing_cap, make_bundle(missing_cap, missing_cap_revision))
        require(
            missing_cap_result["outcome"] == "action-required"
            and "automated reviewer cap lookup failed: fixture-reviewer (source: .github/automated-reviewers.json; lookup: incomplete)" in gap_messages(missing_cap_result),
            "an incomplete reviewer-cap lookup did not fail closed",
        )

        invalid_reviewer_shape = root / "invalid-reviewer-shape"
        invalid_reviewer_revision = build_repository(invalid_reviewer_shape, "invalid-shape")
        invalid_reviewer_result = evaluate(
            invalid_reviewer_shape,
            make_bundle(invalid_reviewer_shape, invalid_reviewer_revision),
        )
        require(
            invalid_reviewer_result["outcome"] == "action-required"
            and "repository automated-reviewer discovery is invalid: FixtureError" in gap_messages(invalid_reviewer_result),
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

        omitted_gate_repo = root / "omitted-discovered-gate"
        omitted_gate_revision = build_repository(
            omitted_gate_repo,
            evidence_mutator=lambda documents: documents["repository-gates"]["gates"].pop(),
        )
        omitted_gate_result = evaluate(
            omitted_gate_repo,
            make_bundle(omitted_gate_repo, omitted_gate_revision),
        )
        require(
            omitted_gate_result["outcome"] == "action-required"
            and "repository gate inventory incomplete" in gap_messages(omitted_gate_result),
            "evidence omitted one of multiple independently discovered repository gates",
        )

        reused_test_result_repo = root / "reused-test-result"
        def reuse_test_result(documents: dict[str, dict[str, Any]]) -> None:
            documents["testing"]["checks"].append({
                "name": "unexecuted-browser-test",
                "command": "browser test",
                "outcome": "passed",
                "result_reference": "test:fixture-validation",
            })

        reused_test_result_revision = build_repository(
            reused_test_result_repo,
            evidence_mutator=reuse_test_result,
        )
        reused_test_result = evaluate(
            reused_test_result_repo,
            make_bundle(reused_test_result_repo, reused_test_result_revision),
        )
        require(
            reused_test_result["outcome"] == "action-required"
            and "testing evidence incomplete" in gap_messages(reused_test_result),
            "testing check reused unrelated passing execution evidence",
        )

        missing_receipt_gaps_repo = root / "missing-receipt-gaps"
        missing_receipt_gaps_revision = build_repository(missing_receipt_gaps_repo)
        missing_receipt_gaps_bundle = make_bundle(
            missing_receipt_gaps_repo,
            missing_receipt_gaps_revision,
        )
        for receipt in missing_receipt_gaps_bundle["receipts"]:
            del receipt["gaps"]
        missing_receipt_gaps = evaluate(
            missing_receipt_gaps_repo,
            missing_receipt_gaps_bundle,
        )
        require(
            missing_receipt_gaps["outcome"] == "action-required"
            and "invalid receipt fields" in gap_messages(missing_receipt_gaps),
            "receipts without an explicit gaps inventory passed",
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
                f"substantive evidence schema mismatch: {kind}" in gap_messages(weak_result),
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
            any("command execution not verified: testing" in message for message in gap_messages(forged_result)),
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
            "substantive evidence schema mismatch: code-review" in gap_messages(bad_result_reference),
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
                envelope["outcome"] == "action-required" and expected_gap in gap_messages(envelope),
                f"{label} bundle did not name its normal assessment gap",
            )
        print("PASS: assessment receipts bind one deterministic exact subject and revision")
        print("PASS: versioned bundle resolution, staged-only dirt, and live-subject mutations fail closed")
        print("PASS: absent reviewer is not applicable; configured reviewer without a cap fails closed")
        print("PASS: command-backed evidence reruns exact allowlisted commands from isolated exact-revision inputs")
        print("PASS: documented no-top-level inline packaging passes; missing, altered, old-revision, same-head cross-Worker, and mixed bundles fail closed")


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
    input_gaps: list[dict[str, str]] = []
    try:
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    except OSError:
        bundle = None
        input_gaps.append(material_gap("obligation.bundle-read", "receipt bundle is unreadable"))
    except (UnicodeError, json.JSONDecodeError):
        bundle = None
        input_gaps.append(material_gap("obligation.bundle-parse", "receipt bundle is malformed"))
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
