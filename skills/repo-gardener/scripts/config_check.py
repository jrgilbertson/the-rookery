#!/usr/bin/env python3
"""Validate and normalize repo-gardener repository configuration."""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
from pathlib import Path
from typing import Any

import yaml


MAX_CONFIG_BYTES = 64 * 1024
MAX_TEXT_LENGTH = 256
MAX_INTEGER = 2_147_483_647
MAX_LIST_ENTRIES = 256
MAX_AUDIT_COMMANDS = 10
MAX_YAML_DEPTH = 16
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
LANE_ORDER = (*AUTHORING_LANES, TRIAGE_LANE)
AUDIT_ELIGIBLE_LANES = (
    "dependency-and-vulnerability",
    "repository-test-and-code-health",
    "documentation-changelog-and-release-note",
    "risk-scoped-qa-and-regression",
    "security-secret-and-static-analysis",
)
TOP_LEVEL_REQUIRED = {
    "repository",
    "protected_paths",
    "maximum_workers",
    "setup_command",
    "tracker",
    "lanes",
}
TOP_LEVEL_ALLOWED = TOP_LEVEL_REQUIRED | {"evidence_sources"}
REPOSITORY_FIELDS = {"identity", "default_branch", "scope"}
SCOPE_FIELDS = {"include", "exclude"}
TRACKER_FIELDS = {"identity"}
AUTHORING_LANE_FIELDS = {"mutation"}
AUDIT_LANE_FIELDS = AUTHORING_LANE_FIELDS | {"audit_commands"}
EVIDENCE_SOURCE_FIELDS = {"identity"}
EVIDENCE_SOURCE_NAME = re.compile(r"^[a-z][a-z0-9_-]{0,63}$")
MAPPING_KEY = re.compile(r"^[A-Za-z0-9_.-][A-Za-z0-9_./-]*$")
ROOTED_OR_DRIVE_PATH = re.compile(r"^(?:[A-Za-z]:[/\\]|[/\\])")
ISSUE_NUMBER_SELECTOR = re.compile(r"^#\d+$")
INTEGER_SCALAR = re.compile(r"^-?(0|[1-9][0-9]*)$")
BOOLEAN_SCALAR = re.compile(r"^(?:true|false)$")
NULL_SCALAR = re.compile(r"^(?:~|null|Null|NULL|)$")
SHELL_INTERPOLATION = re.compile(r"(?:`|\$(?:[A-Za-z_][A-Za-z0-9_]*|[0-9@*#?!$-]|\(|\{))")
SHELL_REDIRECTION = re.compile(r"^(?:[0-9]*|&)(?:>>?|<<?|<>|>&|<&).*$|^(?:>>?|<<?|<>).*$")
SHELL_OPERATOR_TOKENS = {"&&", "||", "|", ";", "&"}
SHELL_COMMANDS = {
    "bash",
    "cmd",
    "csh",
    "dash",
    "fish",
    "ksh",
    "powershell",
    "pwsh",
    "sh",
    "tcsh",
    "zsh",
}


class ConfigError(Exception):
    """The repository configuration is invalid or unsafe to read."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ConfigError(message)


def bounded_read(path: Path, maximum: int, label: str) -> bytes:
    with path.open("rb") as handle:
        raw = handle.read(maximum + 1)
    require(len(raw) <= maximum, f"{label} exceeds {maximum} bytes")
    return raw


def require_repo_root(path: Path) -> Path:
    root = path.absolute()
    try:
        metadata = root.lstat()
    except OSError as error:
        raise ConfigError("repo root must be an existing directory") from error
    require(not stat.S_ISLNK(metadata.st_mode), "repo root must not be a symlink")
    require(stat.S_ISDIR(metadata.st_mode), "repo root must be an existing directory")
    return root


def inspect_repo_file(
    repo_root: Path,
    parts: tuple[str, ...],
    label: str,
    *,
    missing_ok: bool,
) -> Path | None:
    current = repo_root
    for index, part in enumerate(parts):
        current /= part
        try:
            metadata = current.lstat()
        except FileNotFoundError as error:
            if missing_ok:
                return None
            raise ConfigError(f"{label} is missing") from error
        except OSError as error:
            raise ConfigError(f"{label} cannot be inspected") from error

        require(not stat.S_ISLNK(metadata.st_mode), f"{label} contains a symlink component")
        if index < len(parts) - 1:
            require(stat.S_ISDIR(metadata.st_mode), f"{label} contains a non-directory component")
        else:
            require(stat.S_ISREG(metadata.st_mode), f"{label} must be a regular file")
    return current


def require_active_config_path(path: str, repo_root: Path) -> Path:
    expected = repo_root / ".agents" / "repo-gardener.yaml"
    relative = ".agents/repo-gardener.yaml"
    require(
        path in (str(expected), relative, str(Path(relative))),
        "config must be the lexical repository path .agents/repo-gardener.yaml, "
        "either absolute (repo-root-joined) or repository-relative",
    )
    return expected


def load_active_config(path: str, repo_root: Path) -> dict[str, Any] | None:
    require_active_config_path(path, repo_root)
    checked = inspect_repo_file(
        repo_root,
        (".agents", "repo-gardener.yaml"),
        "active config path",
        missing_ok=True,
    )
    if checked is None:
        return None
    raw = bounded_read(checked, MAX_CONFIG_BYTES, "config")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ConfigError("config is not valid UTF-8") from error
    return parse_yaml_mapping(text)


def require_exact_fields(
    value: dict[str, Any],
    required: set[str],
    allowed: set[str],
    label: str,
) -> None:
    keys = set(value)
    missing = sorted(required - keys)
    unexpected = sorted(keys - allowed)
    if missing:
        raise ConfigError(f"{label} missing key: {missing[0]}")
    if unexpected:
        raise ConfigError(f"{label} has unexpected key: {unexpected[0]}")


def require_concrete_text(value: Any, label: str) -> str:
    require(isinstance(value, str), f"{label} must be text")
    require(value == value.strip() and bool(value), f"{label} must be nonempty trimmed text")
    require(len(value) <= MAX_TEXT_LENGTH, f"{label} exceeds {MAX_TEXT_LENGTH} characters")
    require(value.isprintable(), f"{label} contains control characters")
    require("REPLACE_WITH" not in value, f"{label} has an unresolved REPLACE_WITH placeholder")
    return value


def require_path_glob(value: Any, label: str) -> str:
    text = require_concrete_text(value, label)
    require(ROOTED_OR_DRIVE_PATH.match(text) is None, f"{label} must be a repository-relative path")
    canonical = "/".join(
        part for part in "/".join(text.split("\\")).split("/") if part not in {"", "."}
    )
    require(bool(canonical), f"{label} must be a repository-relative path")
    require(".." not in canonical.split("/"), f"{label} must not contain path traversal")
    return canonical


def require_glob_list(value: Any, label: str, *, nonempty: bool) -> list[str]:
    require(isinstance(value, list), f"{label} must be a sequence")
    require(len(value) <= MAX_LIST_ENTRIES, f"{label} exceeds {MAX_LIST_ENTRIES} entries")
    require(not nonempty or bool(value), f"{label} must not be empty")
    return [require_path_glob(item, f"{label}[{index}]") for index, item in enumerate(value)]


def yaml_error_message(error: yaml.YAMLError) -> str:
    problem = getattr(error, "problem", None)
    if isinstance(problem, str):
        text = " ".join(problem.split())
        if text and all(0x20 <= ord(character) <= 0x7E for character in text):
            return f"YAML is invalid: {text}"
    return "YAML is invalid"


def reject_unsupported_yaml(text: str) -> None:
    require("\t" not in text, "YAML tabs are not allowed")
    index = 0
    in_single = False
    in_double = False
    at_line_start = True
    while index < len(text):
        char = text[index]
        prev = text[index - 1] if index else "\n"
        if in_single:
            if char == "'" and index + 1 < len(text) and text[index + 1] == "'":
                index += 2
                continue
            if char == "'":
                in_single = False
            index += 1
            continue
        if in_double:
            if char == "\\" and index + 1 < len(text):
                index += 2
                continue
            if char == '"':
                in_double = False
            index += 1
            continue
        if char == "\n":
            at_line_start = True
            index += 1
            continue
        if at_line_start and char in " ":
            index += 1
            continue
        if at_line_start and char == "%":
            raise ConfigError("YAML documents and directives are not allowed")
        if at_line_start and text.startswith(("---", "..."), index):
            end = index + 3
            nxt = text[end] if end < len(text) else "\n"
            if nxt in " \n":
                raise ConfigError("YAML documents and directives are not allowed")
        at_line_start = False
        if char == "#" and prev.isspace():
            newline = text.find("\n", index)
            index = len(text) if newline < 0 else newline
            continue
        if char == "'":
            in_single = True
            index += 1
            continue
        if char == '"':
            in_double = True
            index += 1
            continue
        boundary = prev.isspace() or prev in ":,[]{}"
        if char == "!" and (index == 0 or boundary):
            raise ConfigError("YAML tags are not allowed")
        if char == "&" and (index == 0 or boundary):
            raise ConfigError("YAML aliases and anchors are not allowed")
        if char == "*" and (index == 0 or boundary):
            nxt = text[index + 1] if index + 1 < len(text) else ""
            if nxt.isalnum() or nxt == "_":
                raise ConfigError("YAML aliases and anchors are not allowed")
        if text.startswith("<<", index) and (index == 0 or prev.isspace() or prev in "{,"):
            end = index + 2
            if end == len(text) or text[end] in " :},\n":
                raise ConfigError("YAML merge keys are not allowed")
        index += 1


def reject_disallowed_values(value: Any, *, depth: int = 0) -> None:
    require(depth <= MAX_YAML_DEPTH, "YAML nesting exceeds the allowed depth")
    if value is None:
        raise ConfigError("YAML null values are not allowed")
    if isinstance(value, bool) or isinstance(value, str):
        return
    if isinstance(value, int):
        require(abs(value) <= MAX_INTEGER, "YAML integer is out of range")
        return
    if isinstance(value, float):
        raise ConfigError("YAML floats are not allowed")
    if isinstance(value, list):
        require(len(value) <= MAX_LIST_ENTRIES, f"YAML sequence exceeds {MAX_LIST_ENTRIES} entries")
        for item in value:
            reject_disallowed_values(item, depth=depth + 1)
        return
    if isinstance(value, dict):
        require(len(value) <= MAX_LIST_ENTRIES, f"YAML mapping exceeds {MAX_LIST_ENTRIES} entries")
        for key, item in value.items():
            require(isinstance(key, str) and bool(key), "YAML mapping key must be text")
            require(MAPPING_KEY.fullmatch(key) is not None, f"YAML mapping key {key!r} is invalid")
            require(key != "<<", "YAML merge keys are not allowed")
            reject_disallowed_values(item, depth=depth + 1)
        return
    raise ConfigError("YAML value type is not allowed")


class PolicyLoader(yaml.SafeLoader):
    yaml_implicit_resolvers: dict[Any, Any] = {}

    def __init__(self, stream: Any) -> None:
        super().__init__(stream)
        self._policy_depth = 0

    def construct_object(self, node: Any, deep: bool = False) -> Any:
        if isinstance(node, (yaml.MappingNode, yaml.SequenceNode)):
            self._policy_depth += 1
            try:
                require(self._policy_depth <= MAX_YAML_DEPTH, "YAML nesting exceeds the allowed depth")
                return super().construct_object(node, deep=deep)
            finally:
                self._policy_depth -= 1
        return super().construct_object(node, deep=deep)

    def construct_mapping(self, node: Any, deep: bool = False) -> dict[str, Any]:
        if not isinstance(node, yaml.MappingNode):
            raise ConfigError("config must be a mapping")
        result: dict[str, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            require(isinstance(key, str) and bool(key), "YAML mapping key must be text")
            require(MAPPING_KEY.fullmatch(key) is not None, f"YAML mapping key {key!r} is invalid")
            require(key != "<<", "YAML merge keys are not allowed")
            require(key not in result, f"duplicate key {key!r}")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


PolicyLoader.add_implicit_resolver("tag:yaml.org,2002:bool", BOOLEAN_SCALAR, list("tf"))
PolicyLoader.add_implicit_resolver("tag:yaml.org,2002:int", INTEGER_SCALAR, list("-+0123456789"))
PolicyLoader.add_implicit_resolver("tag:yaml.org,2002:null", NULL_SCALAR, ["~", "n", "N", ""])


def parse_yaml_mapping(text: str) -> dict[str, Any]:
    reject_unsupported_yaml(text)
    try:
        documents = list(yaml.load_all(text, Loader=PolicyLoader))
    except yaml.YAMLError as error:
        raise ConfigError(yaml_error_message(error)) from error
    require(len(documents) == 1, "YAML documents and directives are not allowed")
    value = documents[0]
    require(isinstance(value, dict), "config must be a mapping")
    reject_disallowed_values(value)
    return value


def normalize_scope(value: Any) -> dict[str, list[str]]:
    require(isinstance(value, dict), "repository.scope must be a mapping")
    require_exact_fields(value, SCOPE_FIELDS, SCOPE_FIELDS, "repository.scope")
    return {
        "include": require_glob_list(value["include"], "repository.scope.include", nonempty=True),
        "exclude": require_glob_list(value["exclude"], "repository.scope.exclude", nonempty=False),
    }


def normalize_repository(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "repository must be a mapping")
    require_exact_fields(value, REPOSITORY_FIELDS, REPOSITORY_FIELDS, "repository")
    return {
        "identity": require_concrete_text(value["identity"], "repository.identity"),
        "default_branch": require_concrete_text(value["default_branch"], "repository.default_branch"),
        "scope": normalize_scope(value["scope"]),
    }


def normalize_tracker(value: Any) -> dict[str, str]:
    require(isinstance(value, dict), "tracker must be a mapping")
    require_exact_fields(value, TRACKER_FIELDS, TRACKER_FIELDS, "tracker")
    identity = require_concrete_text(value["identity"], "tracker.identity")
    require(
        ISSUE_NUMBER_SELECTOR.fullmatch(identity) is None,
        "tracker.identity must be a live tracker identity",
    )
    return {"identity": identity}


def normalize_audit_commands(value: Any, label: str) -> list[list[str]]:
    require(isinstance(value, list), f"{label} must be a sequence")
    require(len(value) <= MAX_LIST_ENTRIES, f"{label} exceeds {MAX_LIST_ENTRIES} entries")
    result: list[list[str]] = []
    for command_index, value_command in enumerate(value):
        command_label = f"{label}[{command_index}]"
        result.append(normalize_direct_argv(value_command, command_label))
    return result


def normalize_direct_argv(value: Any, label: str) -> list[str]:
    require(isinstance(value, list), f"{label} must be a sequence")
    require(bool(value), f"{label} must not be empty")
    require(len(value) <= MAX_LIST_ENTRIES, f"{label} exceeds {MAX_LIST_ENTRIES} entries")
    command = [
        require_concrete_text(token, f"{label}[{token_index}]")
        for token_index, token in enumerate(value)
    ]
    for token_index, token in enumerate(command):
        require(
            token not in SHELL_OPERATOR_TOKENS
            and SHELL_INTERPOLATION.search(token) is None
            and SHELL_REDIRECTION.fullmatch(token) is None,
            f"{label}[{token_index}] contains forbidden shell syntax",
        )
    return command


def executable_name(token: str) -> str:
    executable = re.split(r"[/\\\\]", token)[-1].lower()
    return executable[:-4] if executable.endswith(".exe") else executable


def command_after_env(command: list[str]) -> list[str] | None:
    if executable_name(command[0]) != "env":
        return command
    index = 1
    options_ended = False
    while index < len(command):
        token = command[index]
        if not options_ended:
            if token in {"--", "-"}:
                options_ended = True
                index += 1
                continue
            if (
                token in {"-S", "--split-string"}
                or token.startswith("-S")
                or token.startswith("--split-string=")
            ):
                return None
            if token in {"-C", "--chdir", "-u", "--unset", "-a", "--argv0"}:
                index += 2
                continue
            if token.startswith("--argv0=") or (token.startswith("-a") and token != "-a"):
                index += 1
                continue
            if token.startswith("-"):
                index += 1
                continue
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", token) is not None:
            index += 1
            continue
        return command[index:]
    return []


def powershell_option_name(option: str) -> str:
    marker_length = 2 if option.startswith("--") else 1
    return re.split(r"[=:]", option[marker_length:], maxsplit=1)[0].casefold()


def powershell_option_matches(option: str, spelling: str, minimum: int) -> bool:
    name = powershell_option_name(option)
    return len(name) >= minimum and spelling.startswith(name)


def is_executable_option(executable: str, argument: str) -> bool:
    if argument.startswith("-"):
        return True
    if executable == "cmd":
        return argument.startswith("/")
    if executable in {"powershell", "pwsh"}:
        return (
            option_uses_command_string(executable, argument)
            or option_opens_file_mode(executable, argument)
            or option_consumes_operand(executable, argument)
            or option_is_no_operand(executable, argument)
        )
    return False


def option_consumes_operand(executable: str, option: str) -> bool:
    if executable in {"powershell", "pwsh"}:
        name = powershell_option_name(option)
        return (
            powershell_option_matches(option, "executionpolicy", 2)
            or name == "ep"
            or powershell_option_matches(option, "inputformat", 3)
            or name == "if"
            or powershell_option_matches(option, "outputformat", 1)
            or powershell_option_matches(option, "workingdirectory", 2)
            or name == "wd"
            or powershell_option_matches(option, "configurationname", 6)
            or name == "configurationfile"
            or powershell_option_matches(option, "windowstyle", 1)
            or powershell_option_matches(option, "settingsfile", 8)
            or name in {"version", "psconsolefile"}
            or powershell_option_matches(option, "custompipename", 3)
        )
    if executable in SHELL_COMMANDS:
        return option in {"-o", "-O", "--rcfile", "--init-file"}
    if re.fullmatch(r"python(?:\d+(?:\.\d+)*)?", executable) is not None:
        return option in {"-W", "-X", "--check-hash-based"}
    if executable in {"node", "nodejs"}:
        return option in {
            "-C",
            "-r",
            "--conditions",
            "--diagnostic-dir",
            "--env-file",
            "--env-file-if-exists",
            "--experimental-config-file",
            "--experimental-default-type",
            "--experimental-loader",
            "--experimental-sea-config",
            "--heap-prof-dir",
            "--heap-prof-interval",
            "--heap-prof-name",
            "--heapsnapshot-near-heap-limit",
            "--heapsnapshot-signal",
            "--icu-data-dir",
            "--import",
            "--input-type",
            "--inspect-port",
            "--loader",
            "--localstorage-file",
            "--max-http-header-size",
            "--network-family-autoselection-attempt-timeout",
            "--openssl-config",
            "--redirect-warnings",
            "--report-dir",
            "--report-directory",
            "--report-filename",
            "--report-signal",
            "--require",
            "--secure-heap",
            "--secure-heap-min",
            "--snapshot-blob",
            "--test-concurrency",
            "--test-coverage-branches",
            "--test-name-pattern",
            "--test-reporter",
            "--test-reporter-destination",
            "--test-shard",
            "--test-skip-pattern",
            "--title",
            "--tls-cipher-list",
            "--tls-keylog",
            "--trace-event-categories",
            "--trace-event-file-pattern",
            "--unhandled-rejections",
            "--use-largepages",
            "--v8-pool-size",
            "--watch-kill-signal",
            "--watch-path",
        }
    return False


def option_has_inline_operand(executable: str, option: str) -> bool:
    if executable in {"powershell", "pwsh"}:
        return re.match(r"^[-/][^=:]+[=:]", option) is not None
    return option.startswith("--") and "=" in option


def option_is_no_operand(executable: str, option: str) -> bool:
    if executable in {"powershell", "pwsh"}:
        name = powershell_option_name(option)
        return (
            powershell_option_matches(option, "login", 1)
            or powershell_option_matches(option, "noexit", 3)
            or powershell_option_matches(option, "noprofile", 3)
            or powershell_option_matches(option, "nologo", 3)
            or powershell_option_matches(option, "noninteractive", 4)
            or powershell_option_matches(option, "interactive", 1)
            or name in {"noprofileloadtime", "sta", "mta", "help"}
        )
    if executable in SHELL_COMMANDS:
        return option in {
            "--help",
            "--login",
            "--noediting",
            "--noprofile",
            "--norc",
            "--posix",
            "--restricted",
            "--verbose",
            "--version",
        }
    if re.fullmatch(r"python(?:\d+(?:\.\d+)*)?", executable) is not None:
        return option in {
            "-b",
            "-B",
            "-d",
            "-E",
            "-h",
            "-i",
            "-I",
            "-O",
            "-OO",
            "-q",
            "-s",
            "-S",
            "-u",
            "-v",
            "-V",
            "-x",
            "--bytes-warning",
            "--dev",
            "--dont-write-bytecode",
            "--help",
            "--help-all",
            "--help-env",
            "--help-xoptions",
            "--ignore-environment",
            "--isolated",
            "--no-site",
            "--no-user-site",
            "--quiet",
            "--safe-path",
            "--verbose",
            "--version",
        }
    if executable in {"node", "nodejs"}:
        return option in {
            "--abort-on-uncaught-exception",
            "--build-snapshot",
            "--disable-sigusr1",
            "--enable-etw-stack-walking",
            "--enable-fips",
            "--enable-network-family-autoselection",
            "--enable-source-maps",
            "--experimental-async-context-frame",
            "--experimental-default-config-file",
            "--experimental-eventsource",
            "--experimental-import-meta-resolve",
            "--experimental-print-required-tla",
            "--experimental-require-module",
            "--experimental-sqlite",
            "--experimental-strip-types",
            "--experimental-transform-types",
            "--experimental-vm-modules",
            "--experimental-wasm-modules",
            "--experimental-webstorage",
            "--expose-gc",
            "--force-context-aware",
            "--force-fips",
            "--force-node-api-uncaught-exceptions-policy",
            "--frozen-intrinsics",
            "--heap-prof",
            "--help",
            "--insecure-http-parser",
            "--jitless",
            "--napi-modules",
            "--no-addons",
            "--no-deprecation",
            "--no-experimental-detect-module",
            "--no-experimental-global-navigator",
            "--no-experimental-repl-await",
            "--no-experimental-require-module",
            "--no-experimental-sqlite",
            "--no-experimental-websocket",
            "--no-extra-info-on-fatal-exception",
            "--no-force-async-hooks-checks",
            "--no-global-search-paths",
            "--no-network-family-autoselection",
            "--no-warnings",
            "--node-memory-debug",
            "--openssl-legacy-provider",
            "--openssl-shared-config",
            "--pending-deprecation",
            "--permission",
            "--permission-audit",
            "--preserve-symlinks",
            "--preserve-symlinks-main",
            "--prof",
            "--report-compact",
            "--report-exclude-env",
            "--report-exclude-network",
            "--report-on-fatalerror",
            "--report-on-signal",
            "--report-uncaught-exception",
            "--test",
            "--test-force-exit",
            "--test-only",
            "--throw-deprecation",
            "--trace-deprecation",
            "--trace-sync-io",
            "--trace-tls",
            "--trace-uncaught",
            "--trace-warnings",
            "--track-heap-objects",
            "--use-bundled-ca",
            "--use-openssl-ca",
            "--v8-options",
            "--verify-base-objects",
            "--version",
            "--watch",
            "--watch-preserve-output",
            "--zero-fill-buffers",
        }
    return False


def option_opens_file_mode(executable: str, option: str) -> bool:
    if executable not in {"powershell", "pwsh"}:
        return False
    return powershell_option_matches(option, "file", 1)


def options_before_file_mode(executable: str, arguments: list[str]) -> list[str]:
    options: list[str] = []
    index = 0
    ambiguous_option = False
    while index < len(arguments):
        argument = arguments[index]
        if argument == "--":
            break
        if not is_executable_option(executable, argument):
            if not ambiguous_option:
                break
            index += 1
            continue
        options.append(argument)
        if option_opens_file_mode(executable, argument):
            break
        if option_has_inline_operand(executable, argument) or option_is_no_operand(
            executable, argument
        ):
            index += 1
            continue
        if option_consumes_operand(executable, argument):
            index += 2
            continue
        # An unknown leading wrapper option may consume the following token.
        # Keep scanning until a known file-mode boundary so that its operand
        # cannot hide a later command-string option.
        ambiguous_option = True
        index += 1
    return options


def windows_powershell_uses_positional_command(arguments: list[str]) -> bool:
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument == "--":
            return index + 1 < len(arguments)
        if not is_executable_option("powershell", argument):
            return True
        if option_opens_file_mode("powershell", argument):
            return False
        if option_has_inline_operand("powershell", argument) or option_is_no_operand(
            "powershell", argument
        ):
            index += 1
            continue
        if option_consumes_operand("powershell", argument):
            index += 2
            continue
        # An unknown switch cannot establish a safe script boundary. If it is
        # followed by positional input before explicit -File, Windows PowerShell
        # treats that input as command text.
        index += 1
    return False


def option_uses_command_string(executable: str, option: str) -> bool:
    if executable == "cmd":
        return re.match(r"^/[ck]", option, re.IGNORECASE) is not None
    if executable in {"powershell", "pwsh"}:
        name = powershell_option_name(option)
        return (
            powershell_option_matches(option, "command", 1)
            or name == "ec"
            or powershell_option_matches(option, "encodedcommand", 1)
            or (executable == "pwsh" and name in {"cwa", "commandwithargs"})
        )
    if executable == "fish" and (
        option.startswith("-C") or option.lower().startswith("--init-command")
    ):
        return True
    if executable in SHELL_COMMANDS:
        return option.lower().startswith("--command") or (
            option.startswith("-") and not option.startswith("--") and "c" in option[1:]
        )
    if re.fullmatch(r"python(?:\d+(?:\.\d+)*)?", executable) is not None:
        return re.match(
            r"^(?:-c|-[bBdEhiIOPqRsSuvV]*c)", option, re.IGNORECASE
        ) is not None
    if executable in {"node", "nodejs"}:
        return re.match(r"^(?:-[ep]|--(?:eval|print)(?:$|[=:]))", option, re.IGNORECASE) is not None
    if executable == "ruby":
        return re.match(r"^-[acdlmnpsvwx]*e", option, re.IGNORECASE) is not None
    if executable == "perl":
        return re.match(r"^-[acdlnpstTuvwxW]*[eE]", option) is not None
    if executable == "php":
        return re.match(r"^-[nq]*r", option, re.IGNORECASE) is not None
    if executable == "lua":
        return re.match(r"^-e", option, re.IGNORECASE) is not None
    return False


def is_command_string_wrapper(command: list[str]) -> bool:
    executable_and_args = command_after_env(command)
    if executable_and_args is None:
        return True
    if not executable_and_args:
        return False
    executable = executable_name(executable_and_args[0])
    arguments = executable_and_args[1:]
    return any(
        option_uses_command_string(executable, option)
        for option in options_before_file_mode(executable, arguments)
    ) or (
        executable == "powershell"
        and windows_powershell_uses_positional_command(arguments)
    )


def normalize_setup_command(value: Any) -> list[str]:
    command = normalize_direct_argv(value, "setup_command")
    require(
        not is_command_string_wrapper(command),
        "setup_command contains forbidden command-string wrapper",
    )
    return command


def normalize_lanes(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "lanes must be a mapping")
    require_exact_fields(value, set(LANE_ORDER), set(LANE_ORDER), "lanes")
    require(tuple(value) == LANE_ORDER, "lanes must name every contracted lane in order")
    lanes: dict[str, Any] = {}
    for lane in AUTHORING_LANES:
        entry = value[lane]
        require(isinstance(entry, dict), f"lanes.{lane} must be a mapping")
        allowed_fields = AUDIT_LANE_FIELDS if lane in AUDIT_ELIGIBLE_LANES else AUTHORING_LANE_FIELDS
        require_exact_fields(entry, AUTHORING_LANE_FIELDS, allowed_fields, f"lanes.{lane}")
        mutation = entry["mutation"]
        require(isinstance(mutation, bool), f"lanes.{lane}.mutation must be a boolean")
        lanes[lane] = {"mutation": mutation}
        if lane in AUDIT_ELIGIBLE_LANES:
            lanes[lane]["audit_commands"] = normalize_audit_commands(
                entry.get("audit_commands", []),
                f"lanes.{lane}.audit_commands",
            )
    require(
        sum(len(lanes[lane]["audit_commands"]) for lane in AUDIT_ELIGIBLE_LANES)
        <= MAX_AUDIT_COMMANDS,
        f"lanes.audit_commands exceeds {MAX_AUDIT_COMMANDS} total entries",
    )
    triage = value[TRIAGE_LANE]
    require(isinstance(triage, dict), f"lanes.{TRIAGE_LANE} must be a mapping")
    require_exact_fields(triage, set(), set(), f"lanes.{TRIAGE_LANE}")
    lanes[TRIAGE_LANE] = {}
    return lanes


def normalize_evidence_sources(value: Any) -> dict[str, dict[str, str]]:
    require(isinstance(value, dict), "evidence_sources must be a mapping")
    require(len(value) <= MAX_LIST_ENTRIES, f"evidence_sources exceeds {MAX_LIST_ENTRIES} entries")
    result: dict[str, dict[str, str]] = {}
    for name, source in value.items():
        require(
            isinstance(name, str) and EVIDENCE_SOURCE_NAME.fullmatch(name) is not None,
            f"evidence_sources.{name} has an invalid name",
        )
        require(isinstance(source, dict), f"evidence_sources.{name} must be a mapping")
        require_exact_fields(source, EVIDENCE_SOURCE_FIELDS, EVIDENCE_SOURCE_FIELDS, f"evidence_sources.{name}")
        result[name] = {
            "identity": require_concrete_text(source["identity"], f"evidence_sources.{name}.identity")
        }
    return result


def normalize_config(value: dict[str, Any]) -> dict[str, Any]:
    require_exact_fields(value, TOP_LEVEL_REQUIRED, TOP_LEVEL_ALLOWED, "config")
    workers = value["maximum_workers"]
    require(
        isinstance(workers, int) and not isinstance(workers, bool) and 0 <= workers <= MAX_INTEGER,
        "maximum_workers must be a nonnegative integer",
    )
    normalized: dict[str, Any] = {
        "repository": normalize_repository(value["repository"]),
        "protected_paths": require_glob_list(value["protected_paths"], "protected_paths", nonempty=False),
        "maximum_workers": workers,
        "setup_command": normalize_setup_command(value["setup_command"]),
        "tracker": normalize_tracker(value["tracker"]),
        "lanes": normalize_lanes(value["lanes"]),
    }
    if "evidence_sources" in value:
        normalized["evidence_sources"] = normalize_evidence_sources(value["evidence_sources"])
    return normalized


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":"))


def escape_diagnostic(error: BaseException) -> str:
    return json.dumps(str(error), ensure_ascii=True)[1:-1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    repo_root = require_repo_root(args.repo_root)
    raw = load_active_config(args.config, repo_root)
    if raw is None:
        print(canonical_json({"status": "not-configured"}))
        return 0

    config = normalize_config(raw)
    print(canonical_json({"config": config, "status": "valid"}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        OSError,
        UnicodeError,
        ValueError,
        ConfigError,
        yaml.YAMLError,
        RecursionError,
    ) as error:
        print(f"FAIL: {escape_diagnostic(error)}", file=sys.stderr)
        raise SystemExit(1)
