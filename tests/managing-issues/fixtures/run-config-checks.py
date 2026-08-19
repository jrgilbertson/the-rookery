#!/usr/bin/env python3
"""Exercise the shipped managing-issues config validator as a subprocess."""

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
PRODUCTION = REPO_ROOT / "skills" / "managing-issues" / "scripts" / "config_check.py"
CONFIGS = HERE / "config"
TEMPLATE_LINEAR = REPO_ROOT / "skills" / "managing-issues" / "assets" / "config-template-linear.json"
TEMPLATE_GITHUB = REPO_ROOT / "skills" / "managing-issues" / "assets" / "config-template-github.json"
ACTIVE_CONFIG_RELATIVE = Path(".agents") / "managing-issues.json"
MAX_BYTES = 64 * 1024
READINESS_KEYS = {"needs-discovery", "needs-planning", "ready"}
RECOMMENDED_KEYS = {
    "priority": {"urgent", "high", "medium", "low"},
    "leaf_estimate": {"1", "2", "3", "5", "8"},
    "labels": {"bug", "feature", "maintenance", "research", "documentation"},
    "readiness": READINESS_KEYS,
}
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


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def install_active_config(repo_root: Path, config: Path | dict[str, Any] | None) -> Path:
    active_config = repo_root / ACTIVE_CONFIG_RELATIVE
    active_config.parent.mkdir(parents=True, exist_ok=True)
    if active_config.exists() or active_config.is_symlink():
        if active_config.is_dir() and not active_config.is_symlink():
            active_config.rmdir()
        else:
            active_config.unlink()
    if isinstance(config, Path):
        active_config.write_bytes(config.read_bytes())
    elif config is not None:
        write_json(active_config, config)
    return active_config


def invoke_validator(
    repo_root: Path,
    active_config: str | Path,
    *,
    repo_root_arg: str | Path | None = None,
    cwd: Path | None = None,
    extra_args: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(PRODUCTION),
        "--repo-root",
        str(repo_root_arg) if repo_root_arg is not None else str(repo_root),
        "--config",
        str(active_config),
        *extra_args,
    ]
    return subprocess.run(command, check=False, capture_output=True, text=True, cwd=cwd)


def run_validator(
    config: Path | dict[str, Any] | None,
    repo_root: Path,
) -> subprocess.CompletedProcess[str]:
    active_config = install_active_config(repo_root, config)
    return invoke_validator(repo_root, active_config)


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
    require(completed.stdout == "", "rejected config wrote normalized output")
    require_printable_ascii_diagnostic(completed)
    require(
        completed.stderr.startswith("FAIL: ") and message_fragment in completed.stderr,
        f"unexpected rejection: {completed.stderr.strip()}",
    )


def expect_valid(
    config: Path | dict[str, Any],
    repo_root: Path,
    expected_config: dict[str, Any],
) -> str:
    completed = run_validator(config, repo_root)
    require(completed.returncode == 0, f"expected valid config: {completed.stderr.strip()}")
    require(completed.stderr == "", "valid config wrote to stderr")
    parsed = json.loads(completed.stdout)
    require(parsed == {"config": expected_config, "status": "valid"}, "normalized config differs")
    require(
        completed.stdout == json.dumps(parsed, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n",
        "normalized output is not canonical compact ASCII JSON",
    )
    return completed.stdout


def expect_invalid(
    config: Path | dict[str, Any] | None,
    repo_root: Path,
    message_fragment: str,
) -> None:
    expect_completed_invalid(
        run_validator(config, repo_root),
        message_fragment,
    )


def expect_not_configured(repo_root: Path) -> None:
    completed = run_validator(None, repo_root)
    require(completed.returncode == 0, f"expected no-config outcome: {completed.stderr.strip()}")
    require(completed.stderr == "", "no-config outcome wrote to stderr")
    require(completed.stdout == '{"status":"not-configured"}\n', "no-config output differs")


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_script_surface() -> None:
    require(PRODUCTION.is_file(), "missing config validator")
    require(os.access(PRODUCTION, os.X_OK), "config validator is not executable")
    source = PRODUCTION.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".", 1)[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            require(node.func.id != "open", "config validator contains built-in open")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            require(
                node.func.attr not in FORBIDDEN_WRITE_METHODS,
                f"config validator calls forbidden write-capable method {node.func.attr}",
            )
            if node.func.attr == "open":
                require(
                    bool(node.args)
                    and isinstance(node.args[0], ast.Constant)
                    and node.args[0].value == "rb",
                    "config validator contains a non-binary-read Path.open call",
                )
    non_standard = sorted(
        name for name in imported if name != "__future__" and name not in sys.stdlib_module_names
    )
    require(not non_standard, f"config validator imports non-standard modules: {non_standard}")
    require(
        not imported & FORBIDDEN_PROCESS_OR_NETWORK_IMPORTS,
        f"config validator imports process/network modules: {sorted(imported & FORBIDDEN_PROCESS_OR_NETWORK_IMPORTS)}",
    )
    lowered = source.lower()
    for removed_term in ("trusted", "principal", "default_branch", "default-branch"):
        require(removed_term not in lowered, f"config validator retains removed surface: {removed_term}")


def check_cli_surface(repo_root: Path) -> None:
    help_result = subprocess.run(
        [sys.executable, str(PRODUCTION), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    require(help_result.returncode == 0, "config validator --help failed")
    require("--repo-root" in help_result.stdout and "--config" in help_result.stdout, "config CLI differs")
    for removed_flag in ("--policy", "--trusted-policy", "--trusted-mapping", "--default-branch", "--expected-principal"):
        require(removed_flag not in help_result.stdout, f"removed CLI flag remains: {removed_flag}")
        completed = invoke_validator(
            repo_root,
            repo_root / ACTIVE_CONFIG_RELATIVE,
            extra_args=(removed_flag, "unused"),
        )
        require(completed.returncode == 2, f"removed CLI flag is still accepted: {removed_flag}")
        require("unrecognized arguments" in completed.stderr, f"removed CLI flag diagnostic differs: {removed_flag}")


def base_config(provider: str = "github") -> dict[str, Any]:
    target: str | dict[str, str]
    if provider == "github":
        target = "ExampleOrg/Project"
        readiness = {
            "needs-discovery": "readiness:discovery",
            "needs-planning": "readiness:planning",
            "ready": "readiness:ready",
        }
    else:
        target = {"workspace": "workspace-fixture", "team": "ENG"}
        readiness = {
            "needs-discovery": "label-readiness-discovery",
            "needs-planning": "label-readiness-planning",
            "ready": "label-readiness-ready",
        }
    return {
        "version": 2,
        "provider": provider,
        "target": target,
        "mappings": {
            "priority": {},
            "leaf_estimate": {},
            "labels": {},
            "readiness": readiness,
        },
    }


def check_active_config_filesystem_cases(repo_root: Path, outside: Path) -> None:
    active_config = install_active_config(repo_root, base_config())
    expect_completed_invalid(
        invoke_validator(repo_root, repo_root / "nested" / ".." / ACTIVE_CONFIG_RELATIVE),
        "config must be the lexical repository path .agents/managing-issues.json",
    )
    expect_completed_invalid(
        invoke_validator(repo_root, CONFIGS / "valid-github.json"),
        "config must be the lexical repository path .agents/managing-issues.json",
    )

    active_config.unlink()
    in_repo_config = repo_root / "config-copy.json"
    write_json(in_repo_config, base_config())
    active_config.symlink_to(in_repo_config)
    expect_completed_invalid(invoke_validator(repo_root, active_config), "active config path contains a symlink component")
    active_config.unlink()
    active_config.mkdir()
    expect_completed_invalid(invoke_validator(repo_root, active_config), "active config path must be a regular file")
    active_config.rmdir()

    agents = active_config.parent
    agents.rmdir()
    agents.symlink_to(outside, target_is_directory=True)
    expect_completed_invalid(invoke_validator(repo_root, active_config), "active config path contains a symlink component")
    agents.unlink()
    agents.mkdir()

    active_config.write_bytes(b"{" + b" " * MAX_BYTES + b"}")
    expect_completed_invalid(invoke_validator(repo_root, active_config), f"config exceeds {MAX_BYTES} bytes")
    active_config.unlink()


def check_templates(repo_root: Path) -> None:
    for provider, template_path in (("github", TEMPLATE_GITHUB), ("linear", TEMPLATE_LINEAR)):
        require(template_path.is_file(), f"missing {provider} config template")
        template = json.loads(template_path.read_text(encoding="utf-8"))
        require(
            set(template) == {"version", "provider", "target", "mappings"},
            f"{provider} template keys differ",
        )
        require(template["version"] == 2 and template["provider"] == provider, f"{provider} template identity differs")
        require(set(template["mappings"]) == {"priority", "leaf_estimate", "labels", "readiness"}, f"{provider} template mapping shape differs")
        for family, keys in RECOMMENDED_KEYS.items():
            require(set(template["mappings"][family]) == keys, f"{provider} template {family} recommendations differ")
        expected_readiness = (
            {
                "needs-discovery": "readiness:needs-discovery",
                "needs-planning": "readiness:needs-planning",
                "ready": "readiness:ready",
            }
            if provider == "github"
            else {
                "needs-discovery": "needs-discovery",
                "needs-planning": "needs-planning",
                "ready": "ready",
            }
        )
        require(
            template["mappings"]["readiness"] == expected_readiness,
            f"{provider} template readiness representations differ",
        )
        expect_invalid(template_path, repo_root, "unresolved REPLACE_WITH placeholder")
        resolved = copy.deepcopy(template)
        resolved["target"] = (
            "ExampleOrg/Project"
            if provider == "github"
            else {"workspace": "workspace-fixture", "team": "ENG"}
        )
        expected = copy.deepcopy(resolved)
        if provider == "github":
            expected["target"] = "exampleorg/project"
        expect_valid(resolved, repo_root, expected)

def main() -> int:
    check_script_surface()
    with tempfile.TemporaryDirectory(prefix="managing-issues-config-") as temporary:
        temporary_root = Path(temporary)
        repo_root = temporary_root / "repo"
        outside = temporary_root / "outside"
        repo_root.mkdir()
        outside.mkdir()

        no_agents_root = temporary_root / "no-agents"
        no_agents_root.mkdir()
        no_agents = invoke_validator(
            no_agents_root,
            no_agents_root / ACTIVE_CONFIG_RELATIVE,
        )
        require(no_agents.returncode == 0, f"missing config directory failed: {no_agents.stderr.strip()}")
        require(no_agents.stdout == '{"status":"not-configured"}\n', "missing config directory output differs")

        repo_link = temporary_root / "repo-link"
        repo_link.symlink_to(repo_root, target_is_directory=True)
        expect_completed_invalid(
            invoke_validator(repo_link, repo_link / ACTIVE_CONFIG_RELATIVE),
            "repo root must not be a symlink",
        )
        check_cli_surface(repo_root)

        github = base_config("github")
        github["mappings"]["priority"] = {"high": "priority:high", "normal": "priority:normal"}
        github["mappings"]["leaf_estimate"] = {"medium": "size:m", "small": "size:s"}
        github["mappings"]["labels"] = {"bug": "Bug", "feature": "Feature"}
        expected_github = copy.deepcopy(github)
        expected_github["target"] = "exampleorg/project"
        first = expect_valid(github, repo_root, expected_github)
        second = expect_valid(github, repo_root, expected_github)
        require(first == second, "valid config normalization is not deterministic")

        github_empty = base_config("github")
        expected_github_empty = copy.deepcopy(github_empty)
        expected_github_empty["target"] = "exampleorg/project"
        expect_valid(github_empty, repo_root, expected_github_empty)

        linear = base_config("linear")
        linear["mappings"]["priority"] = {"high": "high", "normal": "medium"}
        linear["mappings"]["leaf_estimate"] = {"medium": 3, "small": 1}
        linear["mappings"]["labels"] = {"bug": "label-bug", "feature": "label-feature"}
        expect_valid(linear, repo_root, linear)
        expect_valid(base_config("linear"), repo_root, base_config("linear"))

        marker = repo_root / "read-only-marker"
        marker.write_text("unchanged\n", encoding="utf-8")
        before = file_digest(marker)
        expect_valid(github, repo_root, expected_github)
        require(file_digest(marker) == before, "validator changed repository content")

        expect_invalid(CONFIGS / "duplicate-key.json", repo_root, "duplicate key 'provider'")
        expect_invalid(CONFIGS / "legacy-v1.json", repo_root, "run Managing Issues setup to create version 2")

        control_key = temporary_root / "control-key.json"
        control_key.write_text(
            json.dumps({**base_config(), "bad\u0007key": True}),
            encoding="utf-8",
        )
        expect_invalid(control_key, repo_root, r"bad\u0007key")
        non_finite = temporary_root / "non-finite.json"
        non_finite.write_text('{"version":NaN}', encoding="utf-8")
        expect_invalid(non_finite, repo_root, "non-finite JSON value NaN is not allowed")

        for key in (
            "authority",
            "api_token",
            "principal",
            "default_branch",
            "defaults",
            "transport",
        ):
            invalid = base_config()
            invalid[key] = "unexpected"
            expect_invalid(invalid, repo_root, f"config has unexpected key: {key}")

        for key in ("work_type", "defaults", "relationships", "status"):
            invalid = base_config()
            invalid["mappings"][key] = {}
            expect_invalid(invalid, repo_root, f"mappings has unexpected key: {key}")

        mapping_default = base_config()
        mapping_default["mappings"]["priority"] = {"default": "priority:normal"}
        expect_invalid(mapping_default, repo_root, "cannot define a default, preferred, or fallback value")

        missing_readiness = base_config()
        del missing_readiness["mappings"]["readiness"]["needs-planning"]
        expect_invalid(missing_readiness, repo_root, "mappings.readiness missing key: needs-planning")
        extra_readiness = base_config()
        extra_readiness["mappings"]["readiness"]["ready-for-implementation"] = "readiness:legacy"
        expect_invalid(
            extra_readiness,
            repo_root,
            "mappings.readiness has unexpected key: ready-for-implementation",
        )

        invalid_nested = base_config("linear")
        invalid_nested["target"]["organization"] = "unexpected"
        expect_invalid(invalid_nested, repo_root, "target has unexpected key: organization")
        for target in ("owner", "owner/.", "owner/..", "https://github.com/owner/repo", "owner/repo/extra"):
            invalid = base_config()
            invalid["target"] = target
            expect_invalid(invalid, repo_root, "GitHub target must be owner/repository")
        invalid_linear = base_config("linear")
        invalid_linear["target"]["workspace"] = "../workspace"
        expect_invalid(invalid_linear, repo_root, "target.workspace must be a connected workspace ID")

        bad_provider = base_config()
        bad_provider["provider"] = "jira"
        expect_invalid(bad_provider, repo_root, "provider must be github or linear")
        bad_github_value = base_config()
        bad_github_value["mappings"]["leaf_estimate"] = {"small": 1}
        expect_invalid(bad_github_value, repo_root, "mappings.leaf_estimate.small must be text")
        bad_linear_priority = base_config("linear")
        bad_linear_priority["mappings"]["priority"] = {"normal": 3}
        expect_invalid(bad_linear_priority, repo_root, "mappings.priority.normal must be one of")
        bad_linear_estimate = base_config("linear")
        bad_linear_estimate["mappings"]["leaf_estimate"] = {"small": "1"}
        expect_invalid(bad_linear_estimate, repo_root, "mappings.leaf_estimate.small must be a nonnegative integer")

        duplicate_label = base_config()
        duplicate_label["mappings"]["labels"] = {"ready": "readiness:ready"}
        expect_invalid(duplicate_label, repo_root, "GitHub label readiness:ready is mapped more than once")
        duplicate_label_case = base_config()
        duplicate_label_case["mappings"]["labels"] = {"ready": "READINESS:READY"}
        expect_invalid(duplicate_label_case, repo_root, "GitHub label readiness:ready is mapped more than once")
        duplicate_linear_label = base_config("linear")
        duplicate_linear_label["mappings"]["labels"] = {"ready": "label-readiness-ready"}
        expect_invalid(duplicate_linear_label, repo_root, "Linear label label-readiness-ready is mapped more than once")

        expect_not_configured(repo_root)
        active_config = install_active_config(repo_root, github)
        completed = invoke_validator(repo_root, ".agents/managing-issues.json", repo_root_arg=".", cwd=repo_root)
        require(completed.returncode == 0, f"relative config argument failed: {completed.stderr.strip()}")
        require(json.loads(completed.stdout) == {"config": expected_github, "status": "valid"}, "relative config output differs")
        active_config.unlink()

        check_active_config_filesystem_cases(repo_root, outside)
        check_templates(repo_root)

    print("PASS: managing-issues config contract")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, json.JSONDecodeError, OSError, SyntaxError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
