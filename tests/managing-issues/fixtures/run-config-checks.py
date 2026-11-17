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
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
PRODUCTION = REPO_ROOT / "skills" / "managing-issues" / "scripts" / "config_check.py"
CONFIGS = HERE / "config"
TEMPLATE_LINEAR = REPO_ROOT / "skills" / "managing-issues" / "assets" / "config-template-linear.json"
TEMPLATE_GITHUB = REPO_ROOT / "skills" / "managing-issues" / "assets" / "config-template-github.json"
ACTIVE_CONFIG_RELATIVE = Path(".agents") / "managing-issues.json"
DERIVATION_TABLES = REPO_ROOT / "skills" / "managing-issues" / "references" / "prioritization.md"
MAX_BYTES = 64 * 1024
READINESS_KEYS = {"needs-discovery", "needs-planning", "ready"}
PRIORITY_KEYS = ("urgent", "high", "medium", "low")
ESTIMATE_KEYS = ("1", "2", "3", "5", "8")
SCORE_FACTORS = ("impact", "confidence", "verification_effort", "undo_cost")
SCORE_LEVELS = ("1", "2", "3")
TEMPLATE_KEYS = {
    "priority": set(PRIORITY_KEYS),
    "leaf_estimate": set(ESTIMATE_KEYS),
    "labels": {"bug", "feature", "maintenance", "research", "documentation"},
    "readiness": READINESS_KEYS,
    "scores": set(SCORE_FACTORS),
}
GITHUB_SCORE_FIELDS = {
    "impact": "Impact",
    "confidence": "Confidence",
    "verification_effort": "Verification effort",
    "undo_cost": "Undo cost",
}
TEMPLATE_LINEAR_SCORE_LABELS = {
    "impact": {"1": "impact-1", "2": "impact-2", "3": "impact-3"},
    "confidence": {"1": "confidence-1", "2": "confidence-2", "3": "confidence-3"},
    "verification_effort": {
        "1": "verification-effort-1",
        "2": "verification-effort-2",
        "3": "verification-effort-3",
    },
    "undo_cost": {"1": "undo-cost-1", "2": "undo-cost-2", "3": "undo-cost-3"},
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


def check_cli_surface(repo_root: Path) -> None:
    help_result = subprocess.run(
        [sys.executable, str(PRODUCTION), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    require(help_result.returncode == 0, "config validator --help failed")
    require("--repo-root" in help_result.stdout and "--config" in help_result.stdout, "config CLI differs")
    completed = invoke_validator(
        repo_root,
        repo_root / ACTIVE_CONFIG_RELATIVE,
        extra_args=("--policy", "unused"),
    )
    require(completed.returncode == 2, "removed CLI flag is still accepted: --policy")
    require("unrecognized arguments" in completed.stderr, "removed CLI flag diagnostic differs: --policy")


def base_config(provider: str = "github") -> dict[str, Any]:
    target: str | dict[str, str]
    priority: dict[str, str]
    leaf_estimate: dict[str, str] | dict[str, int]
    scores: dict[str, str] | dict[str, dict[str, str]]
    if provider == "github":
        target = "ExampleOrg/Project"
        priority = {key: f"priority:{key}" for key in PRIORITY_KEYS}
        leaf_estimate = {key: f"estimate:{key}" for key in ESTIMATE_KEYS}
        readiness = {
            "needs-discovery": "readiness:discovery",
            "needs-planning": "readiness:planning",
            "ready": "readiness:ready",
        }
        scores = dict(GITHUB_SCORE_FIELDS)
    else:
        target = {"workspace": "workspace-fixture", "team": "ENG"}
        priority = {key: key for key in PRIORITY_KEYS}
        leaf_estimate = {key: int(key) for key in ESTIMATE_KEYS}
        readiness = {
            "needs-discovery": "label-readiness-discovery",
            "needs-planning": "label-readiness-planning",
            "ready": "label-readiness-ready",
        }
        scores = {
            factor: {level: f"label-{factor}-{level}" for level in SCORE_LEVELS}
            for factor in SCORE_FACTORS
        }
    return {
        "version": 3,
        "provider": provider,
        "target": target,
        "mappings": {
            "priority": priority,
            "leaf_estimate": leaf_estimate,
            "labels": {},
            "readiness": readiness,
            "scores": scores,
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


def check_assignee_and_project(repo_root: Path) -> None:
    for provider, assignee in (("github", "octo-cat"), ("linear", "5f0c1e2a-user-id")):
        configured = base_config(provider)
        configured["assignee"] = {"default": assignee}
        configured["project"] = {"required": True}
        expected = copy.deepcopy(configured)
        if provider == "github":
            expected["target"] = "exampleorg/project"
        expect_valid(configured, repo_root, expected)

        not_required = base_config(provider)
        not_required["project"] = {"required": False}
        expected = copy.deepcopy(not_required)
        if provider == "github":
            expected["target"] = "exampleorg/project"
        expect_valid(not_required, repo_root, expected)

    for value, message in (
        ("default", "assignee must be an object"),
        ({}, "assignee missing key: default"),
        ({"default": "octo-cat", "fallback": "hubot"}, "assignee has unexpected key: fallback"),
        ({"default": ""}, "assignee.default must be nonempty trimmed text"),
        ({"default": " octo-cat"}, "assignee.default must be nonempty trimmed text"),
        ({"default": "REPLACE_WITH_DEFAULT_ASSIGNEE"}, "unresolved REPLACE_WITH placeholder"),
    ):
        invalid = base_config()
        invalid["assignee"] = value
        expect_invalid(invalid, repo_root, message)
    managed_user = base_config()
    managed_user["assignee"] = {"default": "mona-cat_octo"}
    expected_managed_user = copy.deepcopy(managed_user)
    expected_managed_user["target"] = "exampleorg/project"
    expect_valid(managed_user, repo_root, expected_managed_user)
    for login in ("@me", "-octocat", "octocat-", "octo--cat", "a" * 40, "octo cat", "octo_", "_octo", "octo_cat_x"):
        invalid = base_config()
        invalid["assignee"] = {"default": login}
        expect_invalid(invalid, repo_root, "assignee.default must be a GitHub login")
    linear_name = base_config("linear")
    linear_name["assignee"] = {"default": "Ada Lovelace"}
    expect_valid(linear_name, repo_root, linear_name)

    for value, message in (
        (True, "project must be an object"),
        ({}, "project missing key: required"),
        ({"required": True, "default": "Roadmap"}, "project has unexpected key: default"),
        ({"required": "true"}, "project.required must be true or false"),
        ({"required": 1}, "project.required must be true or false"),
    ):
        invalid = base_config()
        invalid["project"] = value
        expect_invalid(invalid, repo_root, message)


def check_templates(repo_root: Path) -> None:
    for provider, template_path in (("github", TEMPLATE_GITHUB), ("linear", TEMPLATE_LINEAR)):
        require(template_path.is_file(), f"missing {provider} config template")
        template = json.loads(template_path.read_text(encoding="utf-8"))
        require(
            set(template) == {"version", "provider", "target", "mappings", "assignee", "project"},
            f"{provider} template keys differ",
        )
        require(
            template["assignee"] == {"default": "REPLACE_WITH_DEFAULT_ASSIGNEE"}
            and template["project"] == {"required": True},
            f"{provider} template assignee or project recommendation differs",
        )
        require(template["version"] == 3 and template["provider"] == provider, f"{provider} template identity differs")
        require(set(template["mappings"]) == set(TEMPLATE_KEYS), f"{provider} template mapping shape differs")
        for family, keys in TEMPLATE_KEYS.items():
            require(set(template["mappings"][family]) == keys, f"{provider} template {family} recommendations differ")
        require(
            template["mappings"]["scores"]
            == (GITHUB_SCORE_FIELDS if provider == "github" else TEMPLATE_LINEAR_SCORE_LABELS),
            f"{provider} template score representations differ",
        )
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
        resolved["assignee"] = {"default": "octo-cat"}
        expected = copy.deepcopy(resolved)
        if provider == "github":
            expected["target"] = "exampleorg/project"
        expect_valid(resolved, repo_root, expected)


def check_fixed_vocabularies(repo_root: Path) -> None:
    for provider, family, key, value in (
        ("github", "priority", "normal", "priority:normal"),
        ("linear", "priority", "normal", "none"),
        ("github", "leaf_estimate", "small", "size:s"),
        ("github", "leaf_estimate", "medium", "size:m"),
        ("linear", "leaf_estimate", "small", 13),
        ("linear", "leaf_estimate", "medium", 21),
    ):
        extra = base_config(provider)
        extra["mappings"][family][key] = value
        expect_invalid(extra, repo_root, f"mappings.{family} has unexpected key: {key}")

    for provider in ("github", "linear"):
        for family, key in (("priority", "urgent"), ("leaf_estimate", "8")):
            missing = base_config(provider)
            del missing["mappings"][family][key]
            expect_invalid(missing, repo_root, f"mappings.{family} missing key: {key}")
        for family, first_missing in (("priority", "high"), ("leaf_estimate", "1")):
            empty = base_config(provider)
            empty["mappings"][family] = {}
            expect_invalid(empty, repo_root, f"mappings.{family} missing key: {first_missing}")


def check_scores(repo_root: Path) -> None:
    no_scores = base_config()
    del no_scores["mappings"]["scores"]
    expect_invalid(no_scores, repo_root, "mappings missing key: scores")
    scores_list = base_config()
    scores_list["mappings"]["scores"] = list(GITHUB_SCORE_FIELDS.values())
    expect_invalid(scores_list, repo_root, "mappings.scores must be an object")

    for provider in ("github", "linear"):
        for factor in SCORE_FACTORS:
            missing = base_config(provider)
            del missing["mappings"]["scores"][factor]
            expect_invalid(missing, repo_root, f"mappings.scores missing key: {factor}")
        fifth = base_config(provider)
        fifth["mappings"]["scores"]["urgency"] = fifth["mappings"]["scores"]["impact"]
        expect_invalid(fifth, repo_root, "mappings.scores has unexpected key: urgency")

    # A GitHub score is an issue field name, not a label: label CSV syntax and
    # label uniqueness do not apply to it.
    comma_field = base_config()
    comma_field["mappings"]["scores"]["impact"] = 'Impact, "expected"'
    expected_comma_field = copy.deepcopy(comma_field)
    expected_comma_field["target"] = "exampleorg/project"
    expect_valid(comma_field, repo_root, expected_comma_field)
    field_named_like_label = base_config()
    field_named_like_label["mappings"]["labels"] = {"impact": "Impact"}
    expected_field_named_like_label = copy.deepcopy(field_named_like_label)
    expected_field_named_like_label["target"] = "exampleorg/project"
    expect_valid(field_named_like_label, repo_root, expected_field_named_like_label)

    shared_field = base_config()
    shared_field["mappings"]["scores"]["confidence"] = "Impact"
    expect_invalid(shared_field, repo_root, "mappings.scores: provider value Impact is mapped more than once")
    for value, message in (
        ("", "mappings.scores.impact must be nonempty trimmed text"),
        (GITHUB_SCORE_FIELDS, "mappings.scores.impact must be text"),
        ("REPLACE_WITH_FIELD_NAME", "mappings.scores.impact has an unresolved REPLACE_WITH placeholder"),
    ):
        invalid = base_config()
        invalid["mappings"]["scores"]["impact"] = value
        expect_invalid(invalid, repo_root, message)

    fourth_level = base_config("linear")
    fourth_level["mappings"]["scores"]["impact"]["4"] = "label-impact-4"
    expect_invalid(fourth_level, repo_root, "mappings.scores.impact has unexpected key: 4")
    missing_level = base_config("linear")
    del missing_level["mappings"]["scores"]["impact"]["2"]
    expect_invalid(missing_level, repo_root, "mappings.scores.impact missing key: 2")
    flat_factor = base_config("linear")
    flat_factor["mappings"]["scores"]["impact"] = "label-impact"
    expect_invalid(flat_factor, repo_root, "mappings.scores.impact must be an object")
    empty_option = base_config("linear")
    empty_option["mappings"]["scores"]["impact"]["1"] = ""
    expect_invalid(empty_option, repo_root, "mappings.scores.impact.1 must be nonempty trimmed text")

    # Linear score options are labels, so they share one namespace with each
    # other and with the general and readiness labels.
    reuses_readiness = base_config("linear")
    reuses_readiness["mappings"]["scores"]["undo_cost"]["3"] = "label-readiness-ready"
    expect_invalid(reuses_readiness, repo_root, "Linear label label-readiness-ready is mapped more than once")
    reuses_general_label = base_config("linear")
    reuses_general_label["mappings"]["labels"] = {"bug": "label-bug"}
    reuses_general_label["mappings"]["scores"]["impact"]["1"] = "label-bug"
    expect_invalid(reuses_general_label, repo_root, "Linear label label-bug is mapped more than once")
    reuses_other_factor = base_config("linear")
    reuses_other_factor["mappings"]["scores"]["confidence"]["1"] = "label-impact-1"
    expect_invalid(reuses_other_factor, repo_root, "Linear label label-impact-1 is mapped more than once")
    reuses_own_level = base_config("linear")
    reuses_own_level["mappings"]["scores"]["impact"]["2"] = "label-impact-1"
    expect_invalid(reuses_own_level, repo_root, "Linear label label-impact-1 is mapped more than once")


def check_tracked_repository_config() -> None:
    completed = invoke_validator(REPO_ROOT, REPO_ROOT / ACTIVE_CONFIG_RELATIVE)
    require(
        completed.returncode == 0,
        f"this repository's {ACTIVE_CONFIG_RELATIVE} is invalid: {completed.stderr.strip()}",
    )
    require(
        json.loads(completed.stdout).get("status") == "valid",
        f"this repository's {ACTIVE_CONFIG_RELATIVE} is missing",
    )


def table_rows(text: str, header: str) -> list[list[str]]:
    """Return the body rows of the Markdown table that starts with this header line."""
    lines = text.splitlines()
    require(lines.count(header) == 1, f"expected one table headed {header!r}")
    rows: list[list[str]] = []
    for line in lines[lines.index(header) + 2:]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    return rows


def derivation_table_errors(text: str) -> list[str]:
    """Compare the shipped lookup tables with the rule they stand for.

    Priority follows leverage, (impact x confidence) / (verification effort x undo cost):
    3 or higher is high, at least 1 is medium, and anything lower is low. A leaf's
    estimate follows verification effort x undo cost on the 1, 2, 3, 5, 8 scale.
    """
    products = sorted({first * second for first in (1, 2, 3) for second in (1, 2, 3)})
    errors: list[str] = []
    priority = table_rows(text, "| impact × confidence | " + " | ".join(map(str, products)) + " |")
    if [row[0] for row in priority] != [str(product) for product in products]:
        errors.append("priority table rows are not the six impact × confidence products")
    for row in priority:
        for denominator, cell in zip(products, row[1:], strict=True):
            leverage = Fraction(int(row[0]), denominator)
            expected = "high" if leverage >= 3 else "medium" if leverage >= 1 else "low"
            if cell != expected:
                errors.append(f"priority for {row[0]} over {denominator} is {cell}, expected {expected}")
    estimate = table_rows(text, "| verification effort × undo cost | estimate |")
    expected_estimates = dict(zip(products, (1, 2, 3, 5, 5, 8), strict=True))
    if {int(row[0]): int(row[1]) for row in estimate} != expected_estimates or len(estimate) != 6:
        errors.append("estimate table does not map 1, 2, 3, 4, 6, 9 to 1, 2, 3, 5, 5, 8")
    return errors


def check_derivation_tables() -> None:
    text = DERIVATION_TABLES.read_text(encoding="utf-8")
    errors = derivation_table_errors(text)
    require(not errors, "derivation tables differ from the rule: " + "; ".join(errors))
    # The comparison must bite: one wrong cell in either table is reported.
    wrong_priority = text.replace("| 3 | high | medium | medium |", "| 3 | high | high | medium |")
    require(wrong_priority != text and derivation_table_errors(wrong_priority),
            "a wrong priority cell was not reported")
    wrong_estimate = text.replace("| 6 | 5 |", "| 6 | 8 |")
    require(wrong_estimate != text and derivation_table_errors(wrong_estimate),
            "a wrong estimate was not reported")


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
        github["mappings"]["labels"] = {"bug": "Bug", "feature": "Feature"}
        expected_github = copy.deepcopy(github)
        expected_github["target"] = "exampleorg/project"
        first = expect_valid(github, repo_root, expected_github)
        second = expect_valid(github, repo_root, expected_github)
        require(first == second, "valid config normalization is not deterministic")

        github_no_labels = base_config("github")
        expected_github_no_labels = copy.deepcopy(github_no_labels)
        expected_github_no_labels["target"] = "exampleorg/project"
        expect_valid(github_no_labels, repo_root, expected_github_no_labels)
        fixture_github = json.loads((CONFIGS / "valid-github.json").read_text(encoding="utf-8"))
        expect_valid(
            CONFIGS / "valid-github.json",
            repo_root,
            {**fixture_github, "target": "exampleorg/project"},
        )

        linear = base_config("linear")
        linear["mappings"]["labels"] = {"bug": "label-bug", "feature": "label-feature"}
        expect_valid(linear, repo_root, linear)
        expect_valid(base_config("linear"), repo_root, base_config("linear"))

        marker = repo_root / "read-only-marker"
        marker.write_text("unchanged\n", encoding="utf-8")
        before = file_digest(marker)
        expect_valid(github, repo_root, expected_github)
        require(file_digest(marker) == before, "validator changed repository content")

        expect_invalid(CONFIGS / "duplicate-key.json", repo_root, "duplicate key 'provider'")
        # An older config is refused on its version alone, before its fields are
        # read: both fixtures would otherwise fail on a field first.
        expect_invalid(
            CONFIGS / "legacy-v1.json",
            repo_root,
            "config version 1 is unsupported; run Managing Issues setup to create version 3",
        )
        for guidance in (
            "config version 2 is unsupported",
            "run Managing Issues setup to create version 3",
            "update the branch from the default branch",
        ):
            expect_invalid(CONFIGS / "legacy-v2.json", repo_root, guidance)
        newer_version = base_config()
        newer_version["version"] = 4
        expect_invalid(newer_version, repo_root, "version must be 3")

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
        mapping_default["mappings"]["labels"] = {"default": "bug"}
        expect_invalid(
            mapping_default,
            repo_root,
            "mappings.labels.default cannot define a default, preferred, or fallback value",
        )

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
        bad_github_value["mappings"]["leaf_estimate"]["1"] = 1
        expect_invalid(bad_github_value, repo_root, "mappings.leaf_estimate.1 must be text")
        bad_linear_priority = base_config("linear")
        bad_linear_priority["mappings"]["priority"]["medium"] = 3
        expect_invalid(bad_linear_priority, repo_root, "mappings.priority.medium must be one of")
        bad_linear_estimate = base_config("linear")
        bad_linear_estimate["mappings"]["leaf_estimate"]["1"] = "1"
        expect_invalid(bad_linear_estimate, repo_root, "mappings.leaf_estimate.1 must be a nonnegative integer")

        duplicate_label = base_config()
        duplicate_label["mappings"]["labels"] = {"ready": "readiness:ready"}
        expect_invalid(duplicate_label, repo_root, "GitHub label readiness:ready is mapped more than once")
        duplicate_label_case = base_config()
        duplicate_label_case["mappings"]["labels"] = {"ready": "READINESS:READY"}
        expect_invalid(duplicate_label_case, repo_root, "GitHub label readiness:ready is mapped more than once")
        duplicate_linear_label = base_config("linear")
        duplicate_linear_label["mappings"]["labels"] = {"ready": "label-readiness-ready"}
        expect_invalid(duplicate_linear_label, repo_root, "Linear label label-readiness-ready is mapped more than once")
        # Linear's priority names are fixed, so a derived priority can never be
        # written as urgent through a swapped mapping.
        swapped_priority = base_config("linear")
        swapped_priority["mappings"]["priority"]["urgent"] = "high"
        swapped_priority["mappings"]["priority"]["high"] = "urgent"
        expect_invalid(swapped_priority, repo_root, "mappings.priority.urgent must be urgent")
        renamed_priority = base_config("linear")
        renamed_priority["mappings"]["priority"]["low"] = "none"
        expect_invalid(renamed_priority, repo_root, "mappings.priority.low must be low")

        for label in ("Bug,Feature", 'Bug"'):
            csv_label = base_config()
            csv_label["mappings"]["labels"] = {"bug": label}
            expect_invalid(csv_label, repo_root, "mappings.labels.bug cannot contain GitHub label CSV syntax")
        control_value = base_config()
        control_value["mappings"]["labels"] = {"bug": "Bug\u0007"}
        expect_invalid(control_value, repo_root, "mappings.labels.bug contains control characters")
        too_many = base_config()
        too_many["mappings"]["labels"] = {f"label-{index}": f"Label {index}" for index in range(65)}
        expect_invalid(too_many, repo_root, "mappings.labels exceeds 64 entries")

        expect_not_configured(repo_root)
        active_config = install_active_config(repo_root, github)
        completed = invoke_validator(repo_root, ".agents/managing-issues.json", repo_root_arg=".", cwd=repo_root)
        require(completed.returncode == 0, f"relative config argument failed: {completed.stderr.strip()}")
        require(json.loads(completed.stdout) == {"config": expected_github, "status": "valid"}, "relative config output differs")
        active_config.unlink()

        check_active_config_filesystem_cases(repo_root, outside)
        check_assignee_and_project(repo_root)
        check_templates(repo_root)
        check_fixed_vocabularies(repo_root)
        check_scores(repo_root)

    check_tracked_repository_config()
    check_derivation_tables()
    print("PASS: managing-issues config contract")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, json.JSONDecodeError, OSError, SyntaxError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
