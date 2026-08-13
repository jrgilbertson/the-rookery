#!/usr/bin/env python3
"""Exercise the shipped managing-issues policy validator as a subprocess."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
PRODUCTION = REPO_ROOT / "skills" / "managing-issues" / "scripts" / "policy_check.py"
POLICIES = HERE / "policy"
TEMPLATE = REPO_ROOT / "skills" / "managing-issues" / "assets" / "policy-template.json"
FORBIDDEN_PROCESS_OR_NETWORK_IMPORTS = {
    "http",
    "requests",
    "socket",
    "subprocess",
    "urllib",
}
FORBIDDEN_WRITE_METHODS = {
    "chmod",
    "mkdir",
    "rename",
    "replace",
    "rmdir",
    "symlink_to",
    "touch",
    "unlink",
    "write_bytes",
    "write_text",
}


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def run_validator(
    policy: Path,
    repo_root: Path,
    trusted_policy: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    active_policy = repo_root / ".agents" / "managing-issues.json"
    active_policy.parent.mkdir(parents=True, exist_ok=True)
    if active_policy.exists() or active_policy.is_symlink():
        active_policy.unlink()
    if policy.exists():
        active_policy.write_bytes(policy.read_bytes())
    command = [
        sys.executable,
        str(PRODUCTION),
        "--repo-root",
        str(repo_root),
        "--policy",
        str(active_policy),
    ]
    if trusted_policy is not None:
        command.extend(["--trusted-policy", str(trusted_policy)])
    return subprocess.run(command, check=False, capture_output=True, text=True)


def expect_foreign_policy_path_rejected(policy: Path, repo_root: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(PRODUCTION),
            "--repo-root",
            str(repo_root),
            "--policy",
            str(policy),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    require(completed.returncode == 1, "foreign active policy path was accepted")
    require(
        "policy must resolve to .agents/managing-issues.json inside the repository"
        in completed.stderr,
        f"foreign policy path failed for the wrong reason: {completed.stderr.strip()}",
    )


def expect_valid(
    policy: Path,
    repo_root: Path,
    expected_policy: dict[str, Any],
    trusted_policy: Path | None = None,
) -> str:
    completed = run_validator(policy, repo_root, trusted_policy)
    require(completed.returncode == 0, f"expected valid policy: {completed.stderr.strip()}")
    require(completed.stderr == "", "valid policy wrote to stderr")
    parsed = json.loads(completed.stdout)
    require(parsed == {"policy": expected_policy, "status": "valid"}, "normalized policy differs")
    require(
        completed.stdout == json.dumps(parsed, sort_keys=True, separators=(",", ":")) + "\n",
        "normalized output is not canonical JSON",
    )
    return completed.stdout


def expect_missing(policy: Path, repo_root: Path, trusted_policy: Path | None = None) -> None:
    completed = run_validator(policy, repo_root, trusted_policy)
    require(completed.returncode == 0, f"expected missing status: {completed.stderr.strip()}")
    require(completed.stderr == "", "missing policy wrote to stderr")
    require(completed.stdout == '{"status":"missing"}\n', "missing policy output differs")


def expect_invalid(
    policy: Path,
    repo_root: Path,
    message_fragment: str,
    trusted_policy: Path | None = None,
) -> None:
    completed = run_validator(policy, repo_root, trusted_policy)
    require(completed.returncode == 1, f"expected rejection, got exit {completed.returncode}")
    require(completed.stdout == "", "rejected policy wrote normalized output")
    require(
        completed.stderr.startswith("FAIL: ") and message_fragment in completed.stderr,
        f"unexpected rejection: {completed.stderr.strip()}",
    )


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_script_surface() -> None:
    require(PRODUCTION.is_file(), "missing production validator at skills/managing-issues/scripts/policy_check.py")
    require(os.access(PRODUCTION, os.X_OK), "production validator is not executable")
    tree = ast.parse(PRODUCTION.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".", 1)[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            require(
                node.func.attr not in FORBIDDEN_WRITE_METHODS,
                f"production validator contains filesystem write method {node.func.attr}",
            )
    non_standard = sorted(
        name for name in imported if name != "__future__" and name not in sys.stdlib_module_names
    )
    require(not non_standard, f"production validator imports non-standard modules: {non_standard}")
    unsafe_imports = sorted(imported & FORBIDDEN_PROCESS_OR_NETWORK_IMPORTS)
    require(not unsafe_imports, f"production validator imports process/network modules: {unsafe_imports}")


def main() -> int:
    check_script_surface()
    expected_github = {
        "version": 1,
        "provider": "github",
        "target": "exampleorg/project",
        "mappings": {
            "work_type": {"bug": "type:bug", "feature": "type:feature"},
            "readiness": {"blocked": "state:blocked", "ready": "state:ready"},
            "priority": {"high": "priority:high", "normal": "priority:normal"},
            "leaf_estimate": {"medium": "size:m", "small": "size:s"},
        },
    }
    expected_linear = {
        "version": 1,
        "provider": "linear",
        "target": "ENG",
        "synchronization": {"mapping_source": ".agents/linear-sync.json"},
        "mappings": {
            "work_type": {"bug": "label-bug-id", "feature": "label-feature-id"},
            "readiness": {"blocked": "state-blocked-id", "ready": "state-ready-id"},
            "priority": {"high": 2, "normal": 3, "urgent": 1},
            "leaf_estimate": {"large": 5, "medium": 3, "small": 1},
        },
    }

    with tempfile.TemporaryDirectory(prefix="managing-issues-policy-") as temporary:
        temporary_root = Path(temporary)
        repo_root = temporary_root / "repo"
        outside = temporary_root / "outside"
        repo_root.mkdir()
        outside.mkdir()

        first = expect_valid(POLICIES / "valid-github.json", repo_root, expected_github)
        second = expect_valid(POLICIES / "valid-github.json", repo_root, expected_github)
        require(first == second, "valid policy normalization is not deterministic")
        expect_valid(POLICIES / "valid-linear-sync.json", repo_root, expected_linear)

        marker = repo_root / "read-only-marker"
        marker.write_text("unchanged\n", encoding="utf-8")
        before = file_digest(marker)
        expect_valid(POLICIES / "valid-github.json", repo_root, expected_github)
        require(file_digest(marker) == before, "validator changed repository content")

        expect_invalid(POLICIES / "duplicate-key.json", repo_root, "duplicate key 'provider'")
        expect_invalid(POLICIES / "unknown-key.json", repo_root, "unexpected key: authority")
        expect_invalid(POLICIES / "invalid-provider.json", repo_root, "provider must be github or linear")
        expect_invalid(POLICIES / "bad-mappings.json", repo_root, "mappings.work_type.bug")
        expect_invalid(POLICIES / "hostile-path.json", repo_root, "resolves outside the repository")
        expect_foreign_policy_path_rejected(POLICIES / "valid-github.json", repo_root)

        agents = repo_root / ".agents"
        (agents / "escape").symlink_to(outside, target_is_directory=True)
        expect_invalid(POLICIES / "hostile-symlink.json", repo_root, "resolves outside the repository")

        symlink_repo = temporary_root / "symlink-repo"
        symlink_repo.mkdir()
        external_agents = outside / "agents"
        external_agents.mkdir()
        (symlink_repo / ".agents").symlink_to(external_agents, target_is_directory=True)
        expect_invalid(
            POLICIES / "valid-github.json",
            symlink_repo,
            "policy path resolves outside the repository",
        )

        expected_mapping_update = json.loads(json.dumps(expected_linear))
        expected_mapping_update["mappings"]["work_type"]["maintenance"] = "label-maintenance-id"
        expect_valid(
            POLICIES / "valid-linear-sync-mapping-update.json",
            repo_root,
            expected_mapping_update,
            POLICIES / "valid-linear-sync.json",
        )
        expect_invalid(
            POLICIES / "drift-target.json",
            repo_root,
            "canonical provider or target differs from trusted policy",
            POLICIES / "valid-linear-sync.json",
        )
        expect_invalid(
            POLICIES / "drift-sync.json",
            repo_root,
            "synchronization settings differ from trusted policy",
            POLICIES / "valid-linear-sync.json",
        )

        missing = repo_root / ".agents" / "managing-issues.json"
        missing_trusted = temporary_root / "trusted-missing.json"
        expect_missing(missing, repo_root)
        expect_missing(missing, repo_root, missing_trusted)
        expect_invalid(
            missing,
            repo_root,
            "current policy presence differs from trusted policy",
            POLICIES / "valid-linear-sync.json",
        )
        expect_invalid(
            POLICIES / "valid-github.json",
            repo_root,
            "current policy presence differs from trusted policy",
            missing_trusted,
        )

        require(TEMPLATE.is_file(), "missing policy template")
        template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        require(
            set(template["mappings"]["work_type"])
            == {"feature", "fix", "docs", "research", "experiment", "optimization", "maintenance"},
            "policy template work-type starter differs",
        )
        require(
            set(template["mappings"]["readiness"]) == {"triage", "ready"},
            "policy template readiness starter differs",
        )
        require(
            set(template["mappings"]["priority"]) == {"urgent", "high", "medium", "low", "none"},
            "policy template priority starter differs",
        )
        require(
            set(template["mappings"]["leaf_estimate"]) == {"1", "2", "3", "5", "8"},
            "policy template leaf-estimate starter differs",
        )
        expect_invalid(TEMPLATE, repo_root, "unresolved REPLACE_WITH placeholder")

    print("PASS: managing-issues policy contract")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, json.JSONDecodeError, OSError, SyntaxError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
