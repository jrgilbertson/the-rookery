#!/usr/bin/env python3
"""Exercise the shipped repo-gardener config validator as a subprocess."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
PRODUCTION = REPO_ROOT / "skills" / "repo-gardener" / "scripts" / "config_check.py"
TEMPLATE = REPO_ROOT / "skills" / "repo-gardener" / "assets" / "policy-template.yaml"
ACTIVE_CONFIG_RELATIVE = Path(".agents") / "repo-gardener.yaml"
MAX_BYTES = 64 * 1024
AUTHORING_LANES = (
    "dependency-and-vulnerability",
    "issue-implementation",
    "ci-and-failing-test",
    "repository-test-and-code-health",
    "documentation-changelog-and-release-note",
    "runtime-error-and-alert",
    "risk-scoped-qa-and-regression",
    "security-secret-and-static-analysis",
)
TRIAGE_LANE = "issue-backlog-and-customer-feedback-triage"
LANES = (*AUTHORING_LANES, TRIAGE_LANE)
AUDIT_ELIGIBLE_LANES = (
    "dependency-and-vulnerability",
    "repository-test-and-code-health",
    "documentation-changelog-and-release-note",
    "risk-scoped-qa-and-regression",
    "security-secret-and-static-analysis",
)
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
ALLOWED_THIRD_PARTY_IMPORTS = {"yaml"}
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
REMOVED_FILE_KNOBS = (
    "version:",
    "status:",
    "report_write",
    "repository_portfolio_limit",
    "maximum_deep_targets",
    "maximum_new_child_prs",
    "source_mutation",
)


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def dump_yaml(value: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines: list[str] = []
        for key, item in value.items():
            rendered = dump_yaml(item, indent + 2)
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{prefix}{key}:\n")
                lines.append(rendered if rendered.endswith("\n") else rendered + "\n")
            else:
                lines.append(f"{prefix}{key}: {rendered}\n")
        return "".join(lines)
    if isinstance(value, list):
        if not value:
            return "[]"
        lines = []
        for item in value:
            rendered = dump_yaml(item, indent + 2)
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{prefix}-\n")
                lines.append(rendered if rendered.endswith("\n") else rendered + "\n")
            else:
                lines.append(f"{prefix}- {rendered}\n")
        return "".join(lines)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, str):
        if value == "" or value != value.strip() or any(ch in value for ch in ":#{}[]&*!|>%@`") or value in {"true", "false", "null", "Null", "NULL", "~"}:
            return json.dumps(value)
        return value
    raise CheckFailure(f"unsupported YAML dump type: {type(value)!r}")


def write_yaml(path: Path, value: Any | str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value if isinstance(value, str) else dump_yaml(value)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def install_active_config(repo_root: Path, config: Path | dict[str, Any] | str | None) -> Path:
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
        write_yaml(active_config, config)
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
    config: Path | dict[str, Any] | str | None,
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
    config: Path | dict[str, Any] | str,
    repo_root: Path,
    expected_config: dict[str, Any],
) -> str:
    completed = run_validator(config, repo_root)
    require(completed.returncode == 0, f"expected valid config: {completed.stderr.strip()}")
    require(completed.stderr == "", "valid config wrote to stderr")
    parsed = json.loads(completed.stdout)
    require(parsed == {"config": expected_config, "status": "valid"}, "normalized config differs")
    require(
        completed.stdout
        == json.dumps(parsed, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n",
        "normalized output is not canonical compact ASCII JSON",
    )
    return completed.stdout


def expect_invalid(
    config: Path | dict[str, Any] | str | None,
    repo_root: Path,
    message_fragment: str,
) -> None:
    expect_completed_invalid(run_validator(config, repo_root), message_fragment)


def expect_not_configured(repo_root: Path) -> None:
    completed = run_validator(None, repo_root)
    require(completed.returncode == 0, f"expected no-config outcome: {completed.stderr.strip()}")
    require(completed.stderr == "", "no-config outcome wrote to stderr")
    require(completed.stdout == '{"status":"not-configured"}\n', "no-config output differs")


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authoring_lanes(mutation: bool) -> dict[str, Any]:
    lanes: dict[str, Any] = {lane: {"mutation": mutation} for lane in AUTHORING_LANES}
    lanes[TRIAGE_LANE] = {}
    return lanes


def base_config() -> dict[str, Any]:
    return {
        "repository": {
            "identity": "R_kgDOEXAMPLE001",
            "default_branch": "main",
            "scope": {"include": ["**"], "exclude": []},
        },
        "protected_paths": ["AGENTS.md", ".github/workflows/**"],
        "maximum_workers": 20,
        "setup_command": ["npm", "run", "repo-gardener:setup"],
        "tracker": {"identity": "I_kwDOEXAMPLE001"},
        "lanes": authoring_lanes(True),
    }


def normalized_config(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    for lane in AUDIT_ELIGIBLE_LANES:
        result["lanes"][lane].setdefault("audit_commands", [])
    return result


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
        name
        for name in imported
        if name != "__future__"
        and name not in sys.stdlib_module_names
        and name not in ALLOWED_THIRD_PARTY_IMPORTS
    )
    require(not non_standard, f"config validator imports non-standard modules: {non_standard}")
    require("yaml" in imported, "config validator must use PyYAML")
    require(
        not imported & FORBIDDEN_PROCESS_OR_NETWORK_IMPORTS,
        f"config validator imports process/network modules: {sorted(imported & FORBIDDEN_PROCESS_OR_NETWORK_IMPORTS)}",
    )


def check_cli_surface(repo_root: Path) -> None:
    help_result = subprocess.run(
        [sys.executable, str(PRODUCTION), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    require(help_result.returncode == 0, "config validator --help failed")
    require(
        "--repo-root" in help_result.stdout and "--config" in help_result.stdout,
        "config CLI differs",
    )
    for removed_flag in ("--policy", "--trusted-policy"):
        require(removed_flag not in help_result.stdout, f"removed CLI flag remains: {removed_flag}")
        completed = invoke_validator(
            repo_root,
            repo_root / ACTIVE_CONFIG_RELATIVE,
            extra_args=(removed_flag, "unused"),
        )
        require(completed.returncode == 2, f"removed CLI flag is still accepted: {removed_flag}")
        require(
            "unrecognized arguments" in completed.stderr,
            f"removed CLI flag diagnostic differs: {removed_flag}",
        )


def check_starter_shape() -> None:
    require(TEMPLATE.is_file(), "missing policy starter")
    text = TEMPLATE.read_text(encoding="utf-8")
    require("maximum_workers: 0" in text, "starter is not fail-closed on maximum_workers")
    require("setup_command: []" in text, "starter must show an unapproved setup command")
    require(text.count("mutation: false") == 8, "starter authoring-lane mutation count differs")
    require("mutation: true" not in text, "starter grants an authoring lane")
    require(
        text.count("audit_commands: []") == len(AUDIT_ELIGIBLE_LANES),
        "starter must show an empty audit declaration only on each eligible lane",
    )
    require(
        re.search(
            r"issue-backlog-and-customer-feedback-triage:\s*\{\}\s*(?:#.*)?$",
            text,
            re.MULTILINE,
        )
        is not None,
        "starter triage lane must be an empty mapping with no mutation key",
    )
    require("REPLACE_WITH_STABLE_REPOSITORY_IDENTITY" in text, "starter identity placeholder missing")
    require("REPLACE_WITH_DEFAULT_BRANCH" in text, "starter branch placeholder missing")
    require("REPLACE_WITH_PROTECTED_PATH" in text, "starter protected-path placeholder missing")
    require("REPLACE_WITH_TRACKER_IDENTITY" in text, "starter tracker placeholder missing")
    for knob in REMOVED_FILE_KNOBS:
        require(knob not in text, f"starter retains removed file knob {knob}")


def check_active_config_filesystem_cases(repo_root: Path, outside: Path) -> None:
    active_config = install_active_config(repo_root, base_config())
    expect_completed_invalid(
        invoke_validator(repo_root, repo_root / "nested" / ".." / ACTIVE_CONFIG_RELATIVE),
        "config must be the lexical repository path .agents/repo-gardener.yaml",
    )
    expect_completed_invalid(
        invoke_validator(repo_root, TEMPLATE),
        "config must be the lexical repository path .agents/repo-gardener.yaml",
    )

    active_config.unlink()
    in_repo_config = repo_root / "config-copy.yaml"
    write_yaml(in_repo_config, base_config())
    active_config.symlink_to(in_repo_config)
    expect_completed_invalid(
        invoke_validator(repo_root, active_config),
        "active config path contains a symlink component",
    )
    active_config.unlink()
    active_config.mkdir()
    expect_completed_invalid(
        invoke_validator(repo_root, active_config),
        "active config path must be a regular file",
    )
    active_config.rmdir()

    agents = active_config.parent
    agents.rmdir()
    agents.symlink_to(outside, target_is_directory=True)
    expect_completed_invalid(
        invoke_validator(repo_root, active_config),
        "active config path contains a symlink component",
    )
    agents.unlink()
    agents.mkdir()

    active_config.write_bytes(b"{" + b" " * MAX_BYTES + b"}")
    expect_completed_invalid(invoke_validator(repo_root, active_config), f"config exceeds {MAX_BYTES} bytes")
    active_config.unlink()


def main() -> int:
    check_script_surface()
    check_starter_shape()
    with tempfile.TemporaryDirectory(prefix="repo-gardener-config-") as temporary:
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
        require(
            no_agents.returncode == 0,
            f"missing config directory failed: {no_agents.stderr.strip()}",
        )
        require(no_agents.stdout == '{"status":"not-configured"}\n', "missing config directory output differs")

        repo_link = temporary_root / "repo-link"
        repo_link.symlink_to(repo_root, target_is_directory=True)
        expect_completed_invalid(
            invoke_validator(repo_link, repo_link / ACTIVE_CONFIG_RELATIVE),
            "repo root must not be a symlink",
        )
        check_cli_surface(repo_root)

        expected = normalized_config(base_config())
        first = expect_valid(base_config(), repo_root, expected)
        second = expect_valid(base_config(), repo_root, expected)
        require(first == second, "valid config normalization is not deterministic")

        commented = """# Live gardener file
repository:
  identity: R_kgDOEXAMPLE001  # node id
  default_branch: main
  scope:
    include:
      - "**"
    exclude: []
protected_paths:
  - AGENTS.md
  - .github/workflows/**
maximum_workers: 20
setup_command: [npm, run, repo-gardener:setup]
tracker:
  identity: I_kwDOEXAMPLE001
lanes:
  dependency-and-vulnerability:
    mutation: true
  issue-implementation:
    mutation: true
  ci-and-failing-test:
    mutation: true
  repository-test-and-code-health:
    mutation: true
  documentation-changelog-and-release-note:
    mutation: true
  runtime-error-and-alert:
    mutation: true
  risk-scoped-qa-and-regression:
    mutation: true
  security-secret-and-static-analysis:
    mutation: true
  issue-backlog-and-customer-feedback-triage: {}
"""
        expect_valid(commented, repo_root, expected)

        with_sources = copy.deepcopy(base_config())
        with_sources["evidence_sources"] = {"posthog": {"identity": "phc_example"}}
        expected_sources = normalized_config(with_sources)
        expect_valid(with_sources, repo_root, expected_sources)

        marker = repo_root / "read-only-marker"
        marker.write_text("unchanged\n", encoding="utf-8")
        before = file_digest(marker)
        expect_valid(base_config(), repo_root, expected)
        require(file_digest(marker) == before, "validator changed repository content")

        expect_invalid(TEMPLATE, repo_root, "REPLACE_WITH")

        missing_tracker = copy.deepcopy(base_config())
        del missing_tracker["tracker"]
        expect_invalid(missing_tracker, repo_root, "missing key: tracker")
        missing_tracker_identity = copy.deepcopy(base_config())
        del missing_tracker_identity["tracker"]["identity"]
        expect_invalid(missing_tracker_identity, repo_root, "tracker missing key: identity")

        wrong_section = copy.deepcopy(base_config())
        del wrong_section["maximum_workers"]
        wrong_section["repository"]["maximum_workers"] = 20
        expect_invalid(wrong_section, repo_root, "maximum_workers")

        nested_workers = copy.deepcopy(base_config())
        nested_workers["repository"]["maximum_workers"] = 20
        expect_invalid(nested_workers, repo_root, "repository has unexpected key: maximum_workers")

        bool_workers = copy.deepcopy(base_config())
        bool_workers["maximum_workers"] = True
        expect_invalid(bool_workers, repo_root, "maximum_workers must be a nonnegative integer")

        zero_workers = copy.deepcopy(base_config())
        zero_workers["maximum_workers"] = 0
        expect_valid(zero_workers, repo_root, normalized_config(zero_workers))

        setup_command = base_config()
        setup_command["setup_command"] = ["npm", "run", "prepare-repository"]
        expected_setup_command = normalized_config(setup_command)
        expect_valid(setup_command, repo_root, expected_setup_command)
        require(
            expected_setup_command["setup_command"] == ["npm", "run", "prepare-repository"],
            "setup command tokens changed during normalization",
        )
        literal_setup_arguments = base_config()
        literal_setup_arguments["setup_command"] = [
            "env",
            "MODE=setup",
            "repo-setup",
            "--literal=-c",
        ]
        expect_valid(
            literal_setup_arguments,
            repo_root,
            normalized_config(literal_setup_arguments),
        )

        malformed_setup_commands: tuple[tuple[Any, str], ...] = (
            ("npm run prepare-repository", "setup_command must be a sequence"),
            ([], "setup_command must not be empty"),
            (["npm", ""], "setup_command[1] must be nonempty trimmed text"),
            (["npm", 7], "setup_command[1] must be text"),
            (["npm", "&&", "prepare-repository"], "setup_command[1] contains forbidden shell syntax"),
            (["npm", "$(pwd)"], "setup_command[1] contains forbidden shell syntax"),
            (["npm", ">result.txt"], "setup_command[1] contains forbidden shell syntax"),
            (["REPLACE_WITH_APPROVED_SETUP"], "setup_command[0] has an unresolved REPLACE_WITH placeholder"),
            (["sh", "-c", "repo-setup"], "setup_command contains forbidden command-string wrapper"),
            (["python3", "-c", "repo-setup"], "setup_command contains forbidden command-string wrapper"),
            (["env", "MODE=setup", "bash", "-lc", "repo-setup"], "setup_command contains forbidden command-string wrapper"),
            (["env", "--", "node", "--eval=repo-setup"], "setup_command contains forbidden command-string wrapper"),
            (["env", "-S", "sh -c repo-setup"], "setup_command contains forbidden command-string wrapper"),
        )
        for command, message in malformed_setup_commands:
            malformed_setup_command = base_config()
            malformed_setup_command["setup_command"] = command
            expect_invalid(malformed_setup_command, repo_root, message)

        for lane in AUDIT_ELIGIBLE_LANES:
            declared = base_config()
            declared["lanes"][lane]["audit_commands"] = [["npm", "run", "audit"]]
            expect_valid(declared, repo_root, normalized_config(declared))
            declared["lanes"][lane]["audit_commands"].append(
                ["npm", "run", "audit", "--", "--strict"]
            )
            expected_declared = normalized_config(declared)
            expect_valid(declared, repo_root, expected_declared)
            require(
                expected_declared["lanes"][lane]["audit_commands"]
                == [
                    ["npm", "run", "audit"],
                    ["npm", "run", "audit", "--", "--strict"],
                ],
                f"{lane} declaration order changed",
            )

        explicit_empty = base_config()
        for lane in AUDIT_ELIGIBLE_LANES:
            explicit_empty["lanes"][lane]["audit_commands"] = []
        require(
            expect_valid(explicit_empty, repo_root, normalized_config(explicit_empty))
            == expect_valid(base_config(), repo_root, expected),
            "absent and explicit-empty audit declarations normalized differently",
        )

        same_executable = base_config()
        same_executable["lanes"]["repository-test-and-code-health"]["audit_commands"] = [
            ["npm", "run", "lint"],
            ["npm", "run", "test"],
        ]
        expect_valid(same_executable, repo_root, normalized_config(same_executable))

        ten_declared = base_config()
        for lane in AUDIT_ELIGIBLE_LANES:
            ten_declared["lanes"][lane]["audit_commands"] = [
                ["scanner", lane],
                ["scanner", "summary", lane],
            ]
        expect_valid(ten_declared, repo_root, normalized_config(ten_declared))
        eleven_declared = copy.deepcopy(ten_declared)
        eleven_declared["lanes"]["dependency-and-vulnerability"]["audit_commands"].append(
            ["scanner", "overflow"]
        )
        expect_invalid(eleven_declared, repo_root, "exceeds 10 total entries")

        owner_approved_tool_semantics = base_config()
        owner_approved_tool_semantics["lanes"]["repository-test-and-code-health"][
            "audit_commands"
        ] = [
            ["scanner", "scripts/audit.py", "--language=python3"],
            ["awk", "BEGIN { system(\"touch /tmp/marker\") }"],
            ["curl", "-u", "example-user:example-value", "https://example.test"],
            ["git", "-C", "/tmp", "status"],
            ["npx", "--yes", "unreviewed-audit@latest"],
            ["npm", "exec", "--package=unreviewed-audit@latest", "unreviewed-audit"],
            ["python3", "scripts/audit.py"],
            ["env", "MODE=audit", "scanner"],
        ]
        expect_valid(
            owner_approved_tool_semantics,
            repo_root,
            normalized_config(owner_approved_tool_semantics),
        )

        malformed_declarations: tuple[tuple[Any, str], ...] = (
            ("npm run audit", "audit_commands must be a sequence"),
            (["npm run audit"], "audit_commands[0] must be a sequence"),
            ([[]], "audit_commands[0] must not be empty"),
            ([[], ["npm", "run", "audit"]], "audit_commands[0] must not be empty"),
            ([["npm", ""]], "audit_commands[0][1] must be nonempty trimmed text"),
            ([["npm", "   "]], "audit_commands[0][1] must be nonempty trimmed text"),
            ([["npm", 7]], "audit_commands[0][1] must be text"),
            ([["x" * 257]], "audit_commands[0][0] exceeds 256 characters"),
            ([["npm", "&&", "other"]], "contains forbidden shell syntax"),
            ([["npm", "$(pwd)"]], "contains forbidden shell syntax"),
            ([["npm", "${HOME}"]], "contains forbidden shell syntax"),
            ([["npm", ">", "result.txt"]], "contains forbidden shell syntax"),
            ([["npm", "2>result.txt"]], "contains forbidden shell syntax"),
        )
        for declaration, message in malformed_declarations:
            malformed = base_config()
            malformed["lanes"]["dependency-and-vulnerability"]["audit_commands"] = declaration
            expect_invalid(malformed, repo_root, message)

        one_bad_among_valid = base_config()
        one_bad_among_valid["lanes"]["dependency-and-vulnerability"]["audit_commands"] = [
            ["npm", "run", "audit"],
            ["npm", "&&", "other"],
            ["npm", "run", "audit", "--", "--strict"],
        ]
        expect_invalid(one_bad_among_valid, repo_root, "contains forbidden shell syntax")

        for lane in set(LANES) - set(AUDIT_ELIGIBLE_LANES):
            ineligible = base_config()
            ineligible["lanes"][lane]["audit_commands"] = [["npm", "run", "audit"]]
            expect_invalid(ineligible, repo_root, f"lanes.{lane} has unexpected key: audit_commands")

        placeholder = copy.deepcopy(base_config())
        placeholder["repository"]["identity"] = "REPLACE_WITH_STABLE_REPOSITORY_IDENTITY"
        expect_invalid(placeholder, repo_root, "unresolved REPLACE_WITH placeholder")

        triage_mutation = copy.deepcopy(base_config())
        triage_mutation["lanes"][TRIAGE_LANE] = {"mutation": True}
        expect_invalid(triage_mutation, repo_root, f"lanes.{TRIAGE_LANE} has unexpected key: mutation")

        reordered_lanes = copy.deepcopy(base_config())
        lane_items = list(reordered_lanes["lanes"].items())
        lane_items[0], lane_items[1] = lane_items[1], lane_items[0]
        reordered_lanes["lanes"] = dict(lane_items)
        expect_invalid(reordered_lanes, repo_root, "lanes must name every contracted lane in order")

        absolute_protected = copy.deepcopy(base_config())
        absolute_protected["protected_paths"] = ["/etc/**"]
        expect_invalid(absolute_protected, repo_root, "must be a repository-relative path")
        drive_protected = copy.deepcopy(base_config())
        drive_protected["protected_paths"] = [r"C:\outside\**"]
        expect_invalid(drive_protected, repo_root, "must be a repository-relative path")

        quoted_trailing = dump_yaml(base_config()).replace(
            "  - AGENTS.md\n",
            '  - "AGENTS.md" trailing "\n',
        )
        expect_invalid(quoted_trailing, repo_root, "YAML is invalid")

        yes_mutation = dump_yaml(base_config()).replace("    mutation: true\n", "    mutation: yes\n", 1)
        expect_invalid(yes_mutation, repo_root, "mutation must be a boolean")

        four_space_lines = []
        in_lanes = False
        for line in dump_yaml(base_config()).splitlines():
            if line.startswith("lanes:"):
                in_lanes = True
                four_space_lines.append(line)
                continue
            if in_lanes and line and not line[0].isspace():
                in_lanes = False
            four_space_lines.append("  " + line if in_lanes and line else line)
        expect_valid("\n".join(four_space_lines) + "\n", repo_root, expected)

        mapping_path = dump_yaml(base_config()).replace(
            "  - AGENTS.md\n",
            "  - AGENTS.md: true\n",
        )
        expect_invalid(mapping_path, repo_root, "protected_paths[0] must be text")

        nested_sequence = dump_yaml(base_config()).replace(
            "  - AGENTS.md\n",
            "  - - AGENTS.md\n",
        )
        expect_invalid(nested_sequence, repo_root, "protected_paths[0] must be text")

        dotted_glob = dump_yaml(base_config()).replace(
            "  - AGENTS.md\n",
            "  - ./AGENTS.md\n",
        )
        expected_dotted = copy.deepcopy(expected)
        expected_dotted["protected_paths"] = ["AGENTS.md", ".github/workflows/**"]
        expect_valid(dotted_glob, repo_root, expected_dotted)

        windows_glob = dump_yaml(base_config()).replace(
            "  - AGENTS.md\n",
            "  - src\\private\\**\n",
        )
        expected_windows = copy.deepcopy(expected)
        expected_windows["protected_paths"] = ["src/private/**", ".github/workflows/**"]
        expect_valid(windows_glob, repo_root, expected_windows)

        for null_spelling in ("NULL", "Null"):
            null_identity = dump_yaml(base_config()).replace(
                "  identity: I_kwDOEXAMPLE001\n",
                f"  identity: {null_spelling}\n",
            )
            expect_invalid(null_identity, repo_root, "YAML null values are not allowed")

        issue_selector = copy.deepcopy(base_config())
        issue_selector["tracker"]["identity"] = "#3336"
        expect_invalid(issue_selector, repo_root, "tracker.identity must be a live tracker identity")
        quoted_issue_selector = dump_yaml(base_config()).replace(
            "tracker:\n  identity: I_kwDOEXAMPLE001\n",
            'tracker:\n  identity: "#3336"\n',
        )
        expect_invalid(quoted_issue_selector, repo_root, "tracker.identity must be a live tracker identity")

        trailing_exclude = dump_yaml(base_config()).replace(
            "    exclude: []\n",
            "    exclude: [tmp/**,]\n",
        )
        expected_trailing = copy.deepcopy(expected)
        expected_trailing["repository"]["scope"]["exclude"] = ["tmp/**"]
        expect_valid(trailing_exclude, repo_root, expected_trailing)

        flow_lane = dump_yaml(base_config()).replace(
            "  dependency-and-vulnerability:\n    mutation: true\n",
            "  dependency-and-vulnerability: {mutation: true}\n",
        )
        expect_valid(flow_lane, repo_root, expected)
        flow_lane_comma = dump_yaml(base_config()).replace(
            "  dependency-and-vulnerability:\n    mutation: true\n",
            "  dependency-and-vulnerability: {mutation: true,}\n",
        )
        expect_valid(flow_lane_comma, repo_root, expected)

        for key in ("repository", "protected_paths", "maximum_workers", "setup_command", "tracker", "lanes"):
            missing = copy.deepcopy(base_config())
            del missing[key]
            expect_invalid(missing, repo_root, f"missing key: {key}")

        for key in ("identity", "default_branch", "scope"):
            missing = copy.deepcopy(base_config())
            del missing["repository"][key]
            expect_invalid(missing, repo_root, f"repository missing key: {key}")

        for key in ("version", "status", "authority", "boundaries", "caller_roles"):
            invalid = copy.deepcopy(base_config())
            invalid[key] = "unexpected"
            expect_invalid(invalid, repo_root, f"config has unexpected key: {key}")

        alias = copy.deepcopy(base_config())
        alias_text = dump_yaml(alias).replace(
            "identity: R_kgDOEXAMPLE001",
            "identity: &id R_kgDOEXAMPLE001",
        )
        expect_invalid(alias_text, repo_root, "YAML aliases")
        tagged = dump_yaml(base_config()).replace(
            "identity: R_kgDOEXAMPLE001",
            "identity: !!str R_kgDOEXAMPLE001",
        )
        expect_invalid(tagged, repo_root, "YAML tags")
        merge_key = (
            dump_yaml(base_config()).rstrip()
            + "\nextra:\n  <<: {identity: merged}\n"
        )
        expect_invalid(merge_key, repo_root, "YAML merge keys")
        duplicate = dump_yaml(base_config()) + "maximum_workers: 1\n"
        expect_invalid(duplicate, repo_root, "duplicate key")

        expect_not_configured(repo_root)
        active_config = install_active_config(repo_root, base_config())
        completed = invoke_validator(
            repo_root,
            ".agents/repo-gardener.yaml",
            repo_root_arg=".",
            cwd=repo_root,
        )
        require(completed.returncode == 0, f"relative config argument failed: {completed.stderr.strip()}")
        require(
            json.loads(completed.stdout) == {"config": expected, "status": "valid"},
            "relative config output differs",
        )
        active_config.unlink()

        check_active_config_filesystem_cases(repo_root, outside)

    print("PASS: repo-gardener config contract")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, json.JSONDecodeError, OSError, SyntaxError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
