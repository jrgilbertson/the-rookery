#!/usr/bin/env python3
"""Exercise the shipped managing-issues policy validator as a subprocess."""

from __future__ import annotations

import ast
import copy
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
SYNC_MAPPINGS = HERE / "sync-mapping"
TEMPLATE = REPO_ROOT / "skills" / "managing-issues" / "assets" / "policy-template.json"
ACTIVE_POLICY_RELATIVE = Path(".agents") / "managing-issues.json"
ACTIVE_MAPPING_RELATIVE = Path(".agents") / "linear-sync.json"
MAX_BYTES = 64 * 1024
FORBIDDEN_PROCESS_OR_NETWORK_IMPORTS = {
    "ftplib",
    "github",
    "http",
    "imaplib",
    "linear",
    "multiprocessing",
    "poplib",
    "pty",
    "requests",
    "smtplib",
    "socket",
    "ssl",
    "subprocess",
    "telnetlib",
    "urllib",
    "webbrowser",
    "xmlrpc",
}
FORBIDDEN_WRITE_METHODS = {
    "chmod",
    "copy",
    "copy2",
    "copyfile",
    "copytree",
    "hardlink_to",
    "link_to",
    "makedirs",
    "mkdir",
    "mknod",
    "move",
    "remove",
    "removedirs",
    "rename",
    "renames",
    "replace",
    "rmdir",
    "rmtree",
    "symlink_to",
    "touch",
    "truncate",
    "unlink",
    "write_bytes",
    "write_text",
}


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def write_fixture(destination: Path, source: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())


def install_active_policy(repo_root: Path, policy: Path | None) -> Path:
    active_policy = repo_root / ACTIVE_POLICY_RELATIVE
    active_policy.parent.mkdir(parents=True, exist_ok=True)
    if active_policy.exists() or active_policy.is_symlink():
        active_policy.unlink()
    if policy is not None and policy.exists():
        active_policy.write_bytes(policy.read_bytes())
    return active_policy


def install_current_mapping(repo_root: Path, mapping: Path | None) -> Path:
    active_mapping = repo_root / ACTIVE_MAPPING_RELATIVE
    if active_mapping.exists() or active_mapping.is_symlink():
        active_mapping.unlink()
    if mapping is not None:
        write_fixture(active_mapping, mapping)
    return active_mapping


def invoke_validator(
    repo_root: Path,
    active_policy: str | Path,
    trusted_policy: Path | None = None,
    trusted_mapping: Path | None = None,
) -> subprocess.CompletedProcess[str]:
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
    if trusted_mapping is not None:
        command.extend(["--trusted-mapping", str(trusted_mapping)])
    return subprocess.run(command, check=False, capture_output=True, text=True)


def run_validator(
    policy: Path | None,
    repo_root: Path,
    *,
    current_mapping: Path | None = None,
    trusted_policy: Path | None = None,
    trusted_mapping: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    active_policy = install_active_policy(repo_root, policy)
    install_current_mapping(repo_root, current_mapping)
    return invoke_validator(repo_root, active_policy, trusted_policy, trusted_mapping)


def require_printable_ascii_diagnostic(completed: subprocess.CompletedProcess[str]) -> None:
    require(completed.stderr.endswith("\n"), "diagnostic is not newline terminated")
    require(
        all(0x20 <= ord(character) <= 0x7E for character in completed.stderr[:-1]),
        f"diagnostic contains non-printable or non-ASCII content: {completed.stderr!r}",
    )


def expect_completed_invalid(
    completed: subprocess.CompletedProcess[str],
    message_fragment: str,
) -> None:
    require(completed.returncode == 1, f"expected rejection, got exit {completed.returncode}")
    require(completed.stdout == "", "rejected policy wrote normalized output")
    require_printable_ascii_diagnostic(completed)
    require(
        completed.stderr.startswith("FAIL: ") and message_fragment in completed.stderr,
        f"unexpected rejection: {completed.stderr.strip()}",
    )


def expect_valid(
    policy: Path,
    repo_root: Path,
    expected_policy: dict[str, Any],
    *,
    current_mapping: Path | None = None,
    trusted_policy: Path | None = None,
    trusted_mapping: Path | None = None,
) -> str:
    completed = run_validator(
        policy,
        repo_root,
        current_mapping=current_mapping,
        trusted_policy=trusted_policy,
        trusted_mapping=trusted_mapping,
    )
    require(completed.returncode == 0, f"expected valid policy: {completed.stderr.strip()}")
    require(completed.stderr == "", "valid policy wrote to stderr")
    parsed = json.loads(completed.stdout)
    require(parsed == {"policy": expected_policy, "status": "valid"}, "normalized policy differs")
    require(
        completed.stdout == json.dumps(parsed, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n",
        "normalized output is not canonical compact ASCII JSON",
    )
    return completed.stdout


def expect_missing(
    repo_root: Path,
    *,
    trusted_policy: Path | None = None,
) -> None:
    completed = run_validator(None, repo_root, trusted_policy=trusted_policy)
    require(completed.returncode == 0, f"expected missing status: {completed.stderr.strip()}")
    require(completed.stderr == "", "missing policy wrote to stderr")
    require(completed.stdout == '{"status":"missing"}\n', "missing policy output differs")


def expect_invalid(
    policy: Path | None,
    repo_root: Path,
    message_fragment: str,
    *,
    current_mapping: Path | None = None,
    trusted_policy: Path | None = None,
    trusted_mapping: Path | None = None,
) -> None:
    completed = run_validator(
        policy,
        repo_root,
        current_mapping=current_mapping,
        trusted_policy=trusted_policy,
        trusted_mapping=trusted_mapping,
    )
    expect_completed_invalid(completed, message_fragment)


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
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            require(node.func.id != "open", "production validator contains built-in open")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            require(
                node.func.attr not in FORBIDDEN_WRITE_METHODS,
                f"production validator contains filesystem write method {node.func.attr}",
            )
            if node.func.attr == "open":
                require(
                    bool(node.args)
                    and isinstance(node.args[0], ast.Constant)
                    and node.args[0].value == "rb",
                    "production validator contains a non-binary-read Path.open call",
                )
    non_standard = sorted(
        name for name in imported if name != "__future__" and name not in sys.stdlib_module_names
    )
    require(not non_standard, f"production validator imports non-standard modules: {non_standard}")
    unsafe_imports = sorted(imported & FORBIDDEN_PROCESS_OR_NETWORK_IMPORTS)
    require(not unsafe_imports, f"production validator imports process/network modules: {unsafe_imports}")


def check_active_policy_filesystem_cases(repo_root: Path, outside: Path) -> None:
    active_policy = install_active_policy(repo_root, POLICIES / "valid-github.json")
    foreign = repo_root / "nested" / ".." / ".agents" / "managing-issues.json"
    expect_completed_invalid(
        invoke_validator(repo_root, foreign),
        "policy must be the lexical repository path .agents/managing-issues.json",
    )
    expect_completed_invalid(
        invoke_validator(repo_root, POLICIES / "valid-github.json"),
        "policy must be the lexical repository path .agents/managing-issues.json",
    )

    active_policy.unlink()
    in_repo_policy = repo_root / "policy-copy.json"
    write_fixture(in_repo_policy, POLICIES / "valid-github.json")
    active_policy.symlink_to(in_repo_policy)
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        "active policy path contains a symlink component",
    )
    active_policy.unlink()
    active_policy.symlink_to(active_policy)
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        "active policy path contains a symlink component",
    )
    active_policy.unlink()
    active_policy.symlink_to(outside / "missing-policy.json")
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        "active policy path contains a symlink component",
    )
    active_policy.unlink()
    active_policy.mkdir()
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        "active policy path must be a regular file",
    )
    active_policy.rmdir()

    agents = active_policy.parent
    agents.rmdir()
    agents.symlink_to(outside, target_is_directory=True)
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        "active policy path contains a symlink component",
    )
    agents.unlink()
    active_policy.parent.mkdir()

    active_policy.write_bytes(b"{" + b" " * MAX_BYTES + b"}")
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        f"policy exceeds {MAX_BYTES} bytes",
    )
    active_policy.unlink()


def check_mapping_filesystem_cases(repo_root: Path, outside: Path) -> None:
    active_policy = install_active_policy(repo_root, POLICIES / "valid-linear-sync.json")
    active_mapping = install_current_mapping(repo_root, None)
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        "synchronization.mapping_source is missing",
    )

    in_repo_mapping = repo_root / "mapping-copy.json"
    write_fixture(in_repo_mapping, SYNC_MAPPINGS / "valid.json")
    active_mapping.symlink_to(in_repo_mapping)
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        "synchronization.mapping_source contains a symlink component",
    )
    active_mapping.unlink()
    active_mapping.symlink_to(outside / "missing-mapping.json")
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        "synchronization.mapping_source contains a symlink component",
    )
    active_mapping.unlink()
    active_mapping.mkdir()
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        "synchronization.mapping_source must be a regular file",
    )
    active_mapping.rmdir()
    active_mapping.write_bytes(b"{" + b" " * MAX_BYTES + b"}")
    expect_completed_invalid(
        invoke_validator(repo_root, active_policy),
        f"synchronization mapping exceeds {MAX_BYTES} bytes",
    )
    active_mapping.unlink()


def main() -> int:
    check_script_surface()
    expected_github = {
        "version": 1,
        "provider": "github",
        "target": "example/project",
        "mappings": {
            "work_type": {"bug": "Bug", "feature": "Feature"},
            "readiness": {"blocked": "readiness:blocked", "ready": "readiness:ready"},
            "priority": {"high": "priority:high", "normal": "priority:normal"},
            "leaf_estimate": {"medium": "size:m", "small": "size:s"},
        },
    }
    expected_linear = {
        "version": 1,
        "provider": "linear",
        "target": {"workspace": "workspace-fixture", "team": "ENG"},
        "synchronization": {"mapping_source": ".agents/linear-sync.json"},
        "mappings": {
            "work_type": {"bug": "label-fix", "feature": "label-feature"},
            "readiness": {"blocked": "Blocked", "ready": "Ready"},
            "priority": {"high": "high", "normal": "medium", "urgent": "urgent"},
            "leaf_estimate": {"large": 5, "medium": 3, "small": 1},
        },
    }

    with tempfile.TemporaryDirectory(prefix="managing-issues-policy-") as temporary:
        temporary_root = Path(temporary)
        repo_root = temporary_root / "repo"
        outside = temporary_root / "outside"
        trusted_missing = temporary_root / "trusted-missing.json"
        repo_root.mkdir()
        outside.mkdir()

        first = expect_valid(POLICIES / "valid-github.json", repo_root, expected_github)
        second = expect_valid(POLICIES / "valid-github.json", repo_root, expected_github)
        require(first == second, "valid policy normalization is not deterministic")
        expect_valid(
            POLICIES / "valid-linear-sync.json",
            repo_root,
            expected_linear,
            current_mapping=SYNC_MAPPINGS / "valid.json",
        )
        expect_valid(
            POLICIES / "valid-linear-sync.json",
            repo_root,
            expected_linear,
            current_mapping=SYNC_MAPPINGS / "equivalent-normalized.json",
            trusted_policy=POLICIES / "valid-linear-sync.json",
            trusted_mapping=SYNC_MAPPINGS / "valid.json",
        )

        marker = repo_root / "read-only-marker"
        marker.write_text("unchanged\n", encoding="utf-8")
        before = file_digest(marker)
        expect_valid(POLICIES / "valid-github.json", repo_root, expected_github)
        require(file_digest(marker) == before, "validator changed repository content")

        expect_invalid(POLICIES / "duplicate-key.json", repo_root, "duplicate key 'provider'")
        expect_invalid(POLICIES / "huge-integer.json", repo_root, "Exceeds the limit (4300 digits)")
        expect_invalid(POLICIES / "unknown-key.json", repo_root, "unexpected key: authority")
        expect_invalid(POLICIES / "control-key.json", repo_root, r"bad\u0007key")
        expect_invalid(POLICIES / "invalid-provider.json", repo_root, "provider must be github or linear")
        expect_invalid(POLICIES / "bad-mappings.json", repo_root, "mappings.work_type.bug")
        expect_invalid(POLICIES / "invalid-linear-target-keys.json", repo_root, "target has unexpected key")
        expect_invalid(
            POLICIES / "invalid-linear-target-text.json",
            repo_root,
            "target.workspace must be a connected workspace ID",
        )
        expect_invalid(POLICIES / "invalid-linear-work-type.json", repo_root, "mappings.work_type.bug must be text")
        expect_invalid(POLICIES / "invalid-linear-readiness.json", repo_root, "mappings.readiness.ready must be text")
        expect_invalid(
            POLICIES / "invalid-linear-priority.json",
            repo_root,
            "mappings.priority.normal must be one of",
        )
        expect_invalid(
            POLICIES / "invalid-linear-priority-name.json",
            repo_root,
            "mappings.priority.normal must be one of",
        )
        expect_invalid(
            POLICIES / "invalid-linear-leaf-estimate.json",
            repo_root,
            "mappings.leaf_estimate.small must be a nonnegative integer",
        )
        expect_invalid(
            POLICIES / "invalid-linear-negative-estimate.json",
            repo_root,
            "mappings.leaf_estimate.small must be a nonnegative integer",
        )
        expect_invalid(
            POLICIES / "invalid-github-numeric-mapping.json",
            repo_root,
            "mappings.leaf_estimate.small must be text",
        )
        expect_invalid(
            POLICIES / "invalid-github-csv-label.json",
            repo_root,
            "mappings.readiness.ready cannot contain GitHub label CSV syntax",
        )
        expect_invalid(
            POLICIES / "invalid-github-quoted-label.json",
            repo_root,
            "mappings.readiness.ready cannot contain GitHub label CSV syntax",
        )
        expect_invalid(
            POLICIES / "github-synchronization.json",
            repo_root,
            "synchronization requires provider linear",
        )
        expect_invalid(
            POLICIES / "hostile-path.json",
            repo_root,
            "mapping_source must not contain empty, . or .. segments",
        )
        expect_invalid(
            POLICIES / "dot-mapping-source.json",
            repo_root,
            "mapping_source must not contain empty, . or .. segments",
        )
        expect_invalid(
            POLICIES / "absolute-mapping-source.json",
            repo_root,
            "mapping_source must be repository-relative",
        )
        expect_invalid(
            POLICIES / "windows-mapping-source.json",
            repo_root,
            "mapping_source must use repository-relative POSIX syntax",
        )

        agents = repo_root / ".agents"
        (agents / "escape").symlink_to(outside, target_is_directory=True)
        expect_invalid(
            POLICIES / "hostile-symlink.json",
            repo_root,
            "synchronization.mapping_source contains a symlink component",
        )
        (agents / "escape").unlink()

        expected_github_mapping_update = copy.deepcopy(expected_github)
        expected_github_mapping_update["mappings"]["work_type"]["maintenance"] = "Maintenance"
        expect_valid(
            POLICIES / "valid-github-mapping-update.json",
            repo_root,
            expected_github_mapping_update,
            trusted_policy=POLICIES / "valid-github.json",
        )
        expect_invalid(
            POLICIES / "valid-github.json",
            repo_root,
            "--trusted-mapping requires trusted synchronization settings",
            trusted_policy=POLICIES / "valid-github.json",
            trusted_mapping=SYNC_MAPPINGS / "valid.json",
        )
        expected_linear_mapping_update = copy.deepcopy(expected_linear)
        expected_linear_mapping_update["mappings"]["work_type"]["maintenance"] = "label-maintenance"
        expect_valid(
            POLICIES / "valid-linear-sync-mapping-update.json",
            repo_root,
            expected_linear_mapping_update,
            current_mapping=SYNC_MAPPINGS / "valid.json",
            trusted_policy=POLICIES / "valid-linear-sync.json",
            trusted_mapping=SYNC_MAPPINGS / "valid.json",
        )
        expect_invalid(
            POLICIES / "valid-linear-sync-mapping-update.json",
            repo_root,
            "synchronization mapping differs from trusted mapping",
            current_mapping=SYNC_MAPPINGS / "changed.json",
            trusted_policy=POLICIES / "valid-linear-sync.json",
            trusted_mapping=SYNC_MAPPINGS / "valid.json",
        )
        expect_invalid(
            POLICIES / "drift-target.json",
            repo_root,
            "canonical provider or target differs from trusted policy",
            current_mapping=SYNC_MAPPINGS / "valid.json",
            trusted_policy=POLICIES / "valid-linear-sync.json",
            trusted_mapping=SYNC_MAPPINGS / "valid.json",
        )
        active_policy = install_active_policy(repo_root, POLICIES / "drift-sync.json")
        install_current_mapping(repo_root, None)
        write_fixture(repo_root / ".agents" / "other-sync.json", SYNC_MAPPINGS / "valid.json")
        expect_completed_invalid(
            invoke_validator(
                repo_root,
                active_policy,
                POLICIES / "valid-linear-sync.json",
                SYNC_MAPPINGS / "valid.json",
            ),
            "synchronization settings differ from trusted policy",
        )
        expect_invalid(
            POLICIES / "valid-linear-sync.json",
            repo_root,
            "trusted Linear synchronization requires --trusted-mapping",
            current_mapping=SYNC_MAPPINGS / "valid.json",
            trusted_policy=POLICIES / "valid-linear-sync.json",
        )
        expect_invalid(
            POLICIES / "valid-linear-sync.json",
            repo_root,
            "--trusted-mapping requires --trusted-policy",
            current_mapping=SYNC_MAPPINGS / "valid.json",
            trusted_mapping=SYNC_MAPPINGS / "valid.json",
        )

        for fixture, fragment in (
            ("duplicate-key.json", "duplicate key 'ExampleOrg/Project#12'"),
            ("duplicate-normalized-github.json", "duplicate normalized GitHub issue"),
            ("duplicate-linear.json", "duplicate Linear target"),
            ("invalid-github.json", "mapping GitHub issue must be OWNER/REPOSITORY#NUMBER"),
            ("invalid-linear.json", "mapping Linear issue must be TEAM-NUMBER"),
            ("unknown-key.json", "mapping has unexpected key: reverse"),
            ("control-key.json", "mapping GitHub issue contains control characters"),
        ):
            expect_invalid(
                POLICIES / "valid-linear-sync.json",
                repo_root,
                fragment,
                current_mapping=SYNC_MAPPINGS / fixture,
            )

        expect_valid(
            POLICIES / "valid-linear-sync.json",
            repo_root,
            expected_linear,
            current_mapping=SYNC_MAPPINGS / "empty.json",
        )

        capped_mapping = temporary_root / "capped-mapping.json"
        capped_mapping.write_text(
            json.dumps(
                {
                    "version": 1,
                    "github_to_linear": {
                        f"ExampleOrg/Project#{number}": f"ENG-{number}"
                        for number in range(1, 252)
                    },
                }
            ),
            encoding="utf-8",
        )
        expect_invalid(
            POLICIES / "valid-linear-sync.json",
            repo_root,
            "mapping.github_to_linear exceeds 250 entries",
            current_mapping=capped_mapping,
        )

        oversized_mapping = temporary_root / "oversized-mapping.json"
        oversized_mapping.write_bytes(b"{" + b" " * MAX_BYTES + b"}")
        expect_invalid(
            POLICIES / "valid-linear-sync.json",
            repo_root,
            f"synchronization mapping exceeds {MAX_BYTES} bytes",
            current_mapping=oversized_mapping,
        )

        expect_missing(repo_root)
        expect_missing(repo_root, trusted_policy=trusted_missing)
        expect_invalid(
            None,
            repo_root,
            "--trusted-mapping requires trusted synchronization settings",
            trusted_policy=trusted_missing,
            trusted_mapping=SYNC_MAPPINGS / "valid.json",
        )
        expect_invalid(
            None,
            repo_root,
            "current policy presence differs from trusted policy",
            trusted_policy=POLICIES / "valid-linear-sync.json",
        )
        expect_invalid(
            POLICIES / "valid-github.json",
            repo_root,
            "current policy presence differs from trusted policy",
            trusted_policy=trusted_missing,
        )

        (repo_root / ".agents" / "other-sync.json").unlink(missing_ok=True)
        check_active_policy_filesystem_cases(repo_root, outside)
        check_mapping_filesystem_cases(repo_root, outside)

        require(TEMPLATE.is_file(), "missing policy template")
        template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        require(template["provider"] == "linear", "policy template provider differs")
        require(
            set(template["target"]) == {"workspace", "team"},
            "policy template Linear target differs",
        )
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
            template["mappings"]["priority"]
            == {"urgent": "urgent", "high": "high", "medium": "medium", "low": "low", "none": "none"},
            "policy template priority starter differs",
        )
        require(
            template["mappings"]["leaf_estimate"]
            == {"1": 1, "2": 2, "3": 3, "5": 5, "8": 8},
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
