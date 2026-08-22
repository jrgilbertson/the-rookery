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


MAX_CONFIG_BYTES = 64 * 1024
MAX_TEXT_LENGTH = 256
MAX_INTEGER = 2_147_483_647
MAX_LIST_ENTRIES = 256
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
TOP_LEVEL_REQUIRED = {
    "repository",
    "protected_paths",
    "maximum_workers",
    "tracker",
    "lanes",
}
TOP_LEVEL_ALLOWED = TOP_LEVEL_REQUIRED | {"evidence_sources"}
REPOSITORY_FIELDS = {"identity", "default_branch", "scope"}
SCOPE_FIELDS = {"include", "exclude"}
TRACKER_FIELDS = {"identity"}
AUTHORING_LANE_FIELDS = {"mutation"}
EVIDENCE_SOURCE_FIELDS = {"identity"}
EVIDENCE_SOURCE_NAME = re.compile(r"^[a-z][a-z0-9_-]{0,63}$")
MAPPING_KEY = re.compile(r"^[A-Za-z0-9_.-][A-Za-z0-9_./-]*$")
INTEGER_SCALAR = re.compile(r"^-?(0|[1-9][0-9]*)$")
FLOAT_SCALAR = re.compile(r"^-?(?:0|[1-9][0-9]*)\.[0-9]+([eE][-+]?[0-9]+)?$")
SCIENTIFIC_SCALAR = re.compile(r"^-?(?:0|[1-9][0-9]*)[eE][-+]?[0-9]+$")


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
    require(not text.startswith(("/", "\\")), f"{label} must be a repository-relative path")
    parts = tuple(part for part in "/".join(text.split("\\")).split("/") if part not in {"", "."})
    require(".." not in parts, f"{label} must not contain path traversal")
    return text


def require_glob_list(value: Any, label: str, *, nonempty: bool) -> list[str]:
    require(isinstance(value, list), f"{label} must be a sequence")
    require(len(value) <= MAX_LIST_ENTRIES, f"{label} exceeds {MAX_LIST_ENTRIES} entries")
    require(not nonempty or bool(value), f"{label} must not be empty")
    return [require_path_glob(item, f"{label}[{index}]") for index, item in enumerate(value)]


def skip_ws(text: str, index: int) -> int:
    while index < len(text) and text[index] in " \t":
        index += 1
    return index


def strip_comment(text: str) -> str:
    in_single = False
    in_double = False
    index = 0
    while index < len(text):
        char = text[index]
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
        if char == "'":
            in_single = True
        elif char == '"':
            in_double = True
        elif char == "#" and (index == 0 or text[index - 1].isspace()):
            return text[:index].rstrip()
        index += 1
    return text.rstrip()


def reject_unsupported_yaml(content: str) -> None:
    require(content not in {"---", "..."} and not content.startswith("%"), "YAML documents and directives are not allowed")
    index = 0
    in_single = False
    in_double = False
    while index < len(content):
        char = content[index]
        prev = content[index - 1] if index else " "
        if in_single:
            if char == "'" and index + 1 < len(content) and content[index + 1] == "'":
                index += 2
                continue
            if char == "'":
                in_single = False
            index += 1
            continue
        if in_double:
            if char == "\\" and index + 1 < len(content):
                index += 2
                continue
            if char == '"':
                in_double = False
            index += 1
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
            nxt = content[index + 1] if index + 1 < len(content) else ""
            if nxt.isalnum() or nxt == "_":
                raise ConfigError("YAML aliases and anchors are not allowed")
        if content.startswith("<<", index) and (index == 0 or prev.isspace() or prev in "{,"):
            end = index + 2
            if end == len(content) or content[end] in " :},":
                raise ConfigError("YAML merge keys are not allowed")
        index += 1


def decode_quoted(token: str) -> str:
    require(len(token) >= 2 and token[0] == token[-1] and token[0] in {"'", '"'}, "YAML string is unterminated")
    if token[0] == "'":
        inner = token[1:-1]
        chars: list[str] = []
        index = 0
        while index < len(inner):
            if inner[index] == "'" and index + 1 < len(inner) and inner[index + 1] == "'":
                chars.append("'")
                index += 2
                continue
            chars.append(inner[index])
            index += 1
        return "".join(chars)
    inner = token[1:-1]
    chars: list[str] = []
    index = 0
    escapes = {"n": "\n", "t": "\t", "\\": "\\", '"': '"', "/": "/"}
    while index < len(inner):
        char = inner[index]
        if char == "\\":
            require(index + 1 < len(inner), "YAML string is unterminated")
            escaped = inner[index + 1]
            require(escaped in escapes, "YAML string has an unknown escape")
            chars.append(escapes[escaped])
            index += 2
            continue
        chars.append(char)
        index += 1
    return "".join(chars)


def read_quoted(text: str, index: int) -> tuple[str, int]:
    quote = text[index]
    start = index
    index += 1
    if quote == "'":
        while index < len(text):
            char = text[index]
            if char == "'":
                if index + 1 < len(text) and text[index + 1] == "'":
                    index += 2
                    continue
                return text[start : index + 1], index + 1
            index += 1
        raise ConfigError("YAML string is unterminated")
    require(quote == '"', "YAML string is unterminated")
    while index < len(text):
        char = text[index]
        if char == "\\":
            require(index + 1 < len(text), "YAML string is unterminated")
            index += 2
            continue
        index += 1
        if char == '"':
            return text[start:index], index
    raise ConfigError("YAML string is unterminated")


def parse_scalar(token: str) -> Any:
    text = token.strip()
    require(bool(text), "YAML scalar is empty")
    if text[0] in {"'", '"'}:
        return decode_quoted(text)
    if text in {"true", "false"}:
        return text == "true"
    if text in {"null", "~"}:
        raise ConfigError("YAML null values are not allowed")
    if INTEGER_SCALAR.fullmatch(text):
        value = int(text)
        require(abs(value) <= MAX_INTEGER, "YAML integer is out of range")
        return value
    if FLOAT_SCALAR.fullmatch(text) or SCIENTIFIC_SCALAR.fullmatch(text):
        raise ConfigError("YAML floats are not allowed")
    return text


def parse_flow_scalar(text: str, index: int) -> tuple[Any, int]:
    index = skip_ws(text, index)
    require(index < len(text), "YAML flow value is empty")
    if text[index] in {"'", '"'}:
        token, end = read_quoted(text, index)
        return parse_scalar(token), end
    start = index
    while index < len(text) and text[index] not in ",]}#":
        index += 1
    return parse_scalar(text[start:index].rstrip()), index


def parse_flow(text: str, index: int, depth: int) -> tuple[Any, int]:
    require(depth <= MAX_YAML_DEPTH, "YAML nesting exceeds the allowed depth")
    index = skip_ws(text, index)
    require(index < len(text), "YAML flow value is empty")
    if text[index] == "[":
        return parse_flow_sequence(text, index, depth)
    if text[index] == "{":
        return parse_flow_mapping(text, index, depth)
    return parse_flow_scalar(text, index)


def parse_flow_sequence(text: str, index: int, depth: int) -> tuple[list[Any], int]:
    index = skip_ws(text, index + 1)
    items: list[Any] = []
    if index < len(text) and text[index] == "]":
        return items, index + 1
    while True:
        value, index = parse_flow(text, index, depth + 1)
        items.append(value)
        index = skip_ws(text, index)
        if index < len(text) and text[index] == ",":
            index += 1
            continue
        if index < len(text) and text[index] == "]":
            return items, index + 1
        raise ConfigError("YAML flow sequence is malformed")


def parse_flow_mapping(text: str, index: int, depth: int) -> tuple[dict[str, Any], int]:
    index = skip_ws(text, index + 1)
    result: dict[str, Any] = {}
    if index < len(text) and text[index] == "}":
        return result, index + 1
    while True:
        key_value, index = parse_flow_scalar(text, index)
        require(isinstance(key_value, str) and bool(key_value), "YAML mapping key must be text")
        key = key_value
        index = skip_ws(text, index)
        require(index < len(text) and text[index] == ":", "YAML flow mapping is missing a colon")
        value, index = parse_flow(text, index + 1, depth + 1)
        require(key not in result, f"duplicate key {key!r}")
        require(key != "<<", "YAML merge keys are not allowed")
        result[key] = value
        index = skip_ws(text, index)
        if index < len(text) and text[index] == ",":
            index += 1
            continue
        if index < len(text) and text[index] == "}":
            return result, index + 1
        raise ConfigError("YAML flow mapping is malformed")


def split_mapping_entry(content: str) -> tuple[str, str]:
    in_single = False
    in_double = False
    index = 0
    while index < len(content):
        char = content[index]
        if in_single:
            if char == "'" and index + 1 < len(content) and content[index + 1] == "'":
                index += 2
                continue
            if char == "'":
                in_single = False
            index += 1
            continue
        if in_double:
            if char == "\\" and index + 1 < len(content):
                index += 2
                continue
            if char == '"':
                in_double = False
            index += 1
            continue
        if char == "'":
            in_single = True
        elif char == '"':
            in_double = True
        elif char == ":":
            key = content[:index].strip()
            rest = content[index + 1 :].strip()
            require(bool(key), "YAML mapping entry is missing a key")
            if key[0] in {"'", '"'}:
                key = decode_quoted(key)
            require(MAPPING_KEY.fullmatch(key) is not None, f"YAML mapping key {key!r} is invalid")
            return key, rest
        index += 1
    raise ConfigError("YAML mapping entry is missing a colon")


class YamlLoader:
    def __init__(self, text: str) -> None:
        require("\t" not in text, "YAML tabs are not allowed")
        self.lines: list[tuple[int, int, str]] = []
        for number, raw in enumerate(text.splitlines(), start=1):
            stripped = raw.lstrip(" ")
            if stripped == "" or stripped.startswith("#"):
                continue
            indent = len(raw) - len(stripped)
            content = strip_comment(raw[indent:])
            if content == "":
                continue
            reject_unsupported_yaml(content)
            self.lines.append((number, indent, content))
        self.index = 0

    def parse_document(self) -> dict[str, Any]:
        require(bool(self.lines), "config must be a mapping")
        _, indent, content = self.lines[0]
        require(indent == 0, "YAML document must start at column 0")
        require(not content.startswith("-"), "config must be a mapping")
        value = self.parse_mapping(0, 0)
        require(self.index >= len(self.lines), "YAML document has trailing content")
        return value

    def parse_mapping(self, indent: int, depth: int) -> dict[str, Any]:
        require(depth <= MAX_YAML_DEPTH, "YAML nesting exceeds the allowed depth")
        require(
            self.index < len(self.lines) and self.lines[self.index][1] == indent,
            "YAML mapping is empty",
        )
        result: dict[str, Any] = {}
        while self.index < len(self.lines):
            _, line_indent, content = self.lines[self.index]
            if line_indent < indent:
                break
            require(line_indent == indent, "YAML indentation is inconsistent")
            require(not content.startswith("-"), "YAML mapping entry must be a key")
            key, rest = split_mapping_entry(content)
            require(key not in result, f"duplicate key {key!r}")
            require(key != "<<", "YAML merge keys are not allowed")
            self.index += 1
            result[key] = self.parse_value(indent, rest, depth + 1)
        return result

    def parse_sequence(self, indent: int, depth: int) -> list[Any]:
        require(depth <= MAX_YAML_DEPTH, "YAML nesting exceeds the allowed depth")
        result: list[Any] = []
        while self.index < len(self.lines):
            _, line_indent, content = self.lines[self.index]
            if line_indent < indent:
                break
            require(line_indent == indent, "YAML indentation is inconsistent")
            if content == "-":
                rest = ""
            elif content.startswith("- "):
                rest = content[2:]
            else:
                break
            self.index += 1
            result.append(self.parse_value(indent, rest, depth + 1))
        require(bool(result), "YAML block sequence is empty")
        return result

    def parse_value(self, parent_indent: int, rest: str, depth: int) -> Any:
        require(depth <= MAX_YAML_DEPTH, "YAML nesting exceeds the allowed depth")
        if rest == "":
            require(
                self.index < len(self.lines) and self.lines[self.index][1] > parent_indent,
                "YAML null values are not allowed",
            )
            child_indent = self.lines[self.index][1]
            content = self.lines[self.index][2]
            if content == "-" or content.startswith("- "):
                return self.parse_sequence(child_indent, depth)
            return self.parse_mapping(child_indent, depth)
        if rest[0] in "|>":
            raise ConfigError("YAML block scalars are not allowed")
        if rest[0] in "[{":
            value, end = parse_flow(rest, 0, depth)
            require(rest[end:].strip() == "", "YAML flow value has trailing content")
            return value
        return parse_scalar(rest)


def parse_yaml_mapping(text: str) -> dict[str, Any]:
    value = YamlLoader(text).parse_document()
    require(isinstance(value, dict), "config must be a mapping")
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
    return {"identity": require_concrete_text(value["identity"], "tracker.identity")}


def normalize_lanes(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), "lanes must be a mapping")
    require_exact_fields(value, set(LANE_ORDER), set(LANE_ORDER), "lanes")
    require(tuple(value) == LANE_ORDER, "lanes must name every contracted lane in order")
    lanes: dict[str, Any] = {}
    for lane in AUTHORING_LANES:
        entry = value[lane]
        require(isinstance(entry, dict), f"lanes.{lane} must be a mapping")
        require_exact_fields(entry, AUTHORING_LANE_FIELDS, AUTHORING_LANE_FIELDS, f"lanes.{lane}")
        mutation = entry["mutation"]
        require(isinstance(mutation, bool), f"lanes.{lane}.mutation must be a boolean")
        lanes[lane] = {"mutation": mutation}
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
        RecursionError,
    ) as error:
        print(f"FAIL: {escape_diagnostic(error)}", file=sys.stderr)
        raise SystemExit(1)
