#!/usr/bin/env python3
"""Validate and normalize managing-issues repository configuration."""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
from pathlib import Path
from typing import Any


MAX_CONFIG_BYTES = 64 * 1024
MAX_MAPPING_ENTRIES = 64
MAX_TEXT_LENGTH = 256
MAX_INTEGER = 2_147_483_647
TOP_LEVEL_FIELDS = {"version", "provider", "target", "synchronization", "mappings"}
MAPPING_FIELDS = ("priority", "leaf_estimate", "labels", "readiness")
READINESS_FIELDS = {
    "needs-discovery",
    "needs-planning",
    "ready",
}
LINEAR_TARGET_FIELDS = {"workspace", "team"}
LINEAR_PRIORITIES = {"none", "low", "medium", "high", "urgent"}
RESERVED_MAPPING_KEYS = {"default", "defaults", "fallback", "preferred"}
MAPPING_KEY = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
GITHUB_OWNER_REPO = (
    r"^(?P<owner>[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)/"
    r"(?P<repo>(?!\.\.?(?:$|#))[A-Za-z0-9._-]{1,100})"
)
GITHUB_TARGET = re.compile(GITHUB_OWNER_REPO + r"$")
LINEAR_TARGET_PART = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")


class ConfigError(Exception):
    """The repository configuration is invalid or unsafe to read."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ConfigError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ConfigError(f"duplicate key {key!r}")
        result[key] = value
    return result


def reject_non_finite(value: str) -> None:
    raise ConfigError(f"non-finite JSON value {value} is not allowed")


def parse_json_object(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_non_finite,
    )
    require(isinstance(value, dict), f"{label} must be a JSON object")
    return value


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
    expected = repo_root / ".agents" / "managing-issues.json"
    relative = ".agents/managing-issues.json"
    require(
        path in (str(expected), relative, str(Path(relative))),
        "config must be the lexical repository path .agents/managing-issues.json, "
        "either absolute (repo-root-joined) or repository-relative",
    )
    return expected


def load_active_config(path: str, repo_root: Path) -> dict[str, Any] | None:
    require_active_config_path(path, repo_root)
    checked = inspect_repo_file(
        repo_root,
        (".agents", "managing-issues.json"),
        "active config path",
        missing_ok=True,
    )
    if checked is None:
        return None
    return parse_json_object(bounded_read(checked, MAX_CONFIG_BYTES, "config"), "config")


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


def normalize_target(provider: str, value: Any) -> str | dict[str, str]:
    if provider == "github":
        target = require_concrete_text(value, "target")
        match = GITHUB_TARGET.fullmatch(target)
        require(match is not None, "GitHub target must be owner/repository")
        return target.lower()

    require(isinstance(value, dict), "Linear target must be an object")
    require_exact_fields(value, LINEAR_TARGET_FIELDS, LINEAR_TARGET_FIELDS, "target")
    workspace = require_concrete_text(value["workspace"], "target.workspace")
    team = require_concrete_text(value["team"], "target.team")
    require(
        LINEAR_TARGET_PART.fullmatch(workspace) is not None,
        "target.workspace must be a connected workspace ID",
    )
    require(
        LINEAR_TARGET_PART.fullmatch(team) is not None,
        "target.team must be a Linear team key or ID",
    )
    return {"workspace": workspace, "team": team}


def normalize_mapping(
    provider: str,
    field: str,
    value: Any,
) -> dict[str, str | int]:
    label = f"mappings.{field}"
    require(isinstance(value, dict), f"{label} must be an object")
    require(len(value) <= MAX_MAPPING_ENTRIES, f"{label} exceeds {MAX_MAPPING_ENTRIES} entries")
    result: dict[str, str | int] = {}
    for key, provider_value in value.items():
        require(MAPPING_KEY.fullmatch(key) is not None, f"{label}.{key} has an invalid mapping key")
        require(
            key not in RESERVED_MAPPING_KEYS,
            f"{label}.{key} cannot define a default, preferred, or fallback value",
        )
        entry_label = f"{label}.{key}"
        if provider == "github":
            github_value = require_concrete_text(provider_value, entry_label)
            require(
                "," not in github_value and '"' not in github_value,
                f"{entry_label} cannot contain GitHub label CSV syntax",
            )
            result[key] = github_value
        elif field in ("labels", "readiness"):
            result[key] = require_concrete_text(provider_value, entry_label)
        elif field == "priority":
            require(
                isinstance(provider_value, str) and provider_value in LINEAR_PRIORITIES,
                f"{entry_label} must be one of none, low, medium, high, urgent",
            )
            result[key] = provider_value
        else:
            require(
                isinstance(provider_value, int)
                and not isinstance(provider_value, bool)
                and 0 <= provider_value <= MAX_INTEGER,
                f"{entry_label} must be a nonnegative integer",
            )
            result[key] = provider_value
    return dict(sorted(result.items()))


def require_unique_values(mapping: dict[str, str | int], label: str) -> None:
    seen: set[str | int] = set()
    for value in mapping.values():
        require(value not in seen, f"{label}: provider value {value} is mapped more than once")
        seen.add(value)


def require_unique_label_representations(provider: str, mappings: dict[str, Any]) -> None:
    label_fields = MAPPING_FIELDS if provider == "github" else ("labels", "readiness")
    provider_name = "GitHub" if provider == "github" else "Linear"
    seen: set[str] = set()
    for field in label_fields:
        for value in mappings[field].values():
            require(
                value not in seen,
                f"{provider_name} label {value} is mapped more than once",
            )
            seen.add(value)


def normalize_config(value: dict[str, Any]) -> dict[str, Any]:
    require_exact_fields(value, TOP_LEVEL_FIELDS, TOP_LEVEL_FIELDS, "config")
    version = value["version"]
    if isinstance(version, int) and not isinstance(version, bool) and version == 1:
        raise ConfigError(
            "config version 1 is unsupported; run Managing Issues setup to create version 2"
        )
    require(
        isinstance(version, int) and not isinstance(version, bool) and version == 2,
        "version must be 2",
    )
    provider = value["provider"]
    require(
        isinstance(provider, str) and provider in {"github", "linear"},
        "provider must be github or linear",
    )
    synchronization = value["synchronization"]
    require(isinstance(synchronization, bool), "synchronization must be true or false")

    mappings = value["mappings"]
    require(isinstance(mappings, dict), "mappings must be an object")
    require_exact_fields(mappings, set(MAPPING_FIELDS), set(MAPPING_FIELDS), "mappings")
    readiness = mappings["readiness"]
    require(isinstance(readiness, dict), "mappings.readiness must be an object")
    require_exact_fields(readiness, READINESS_FIELDS, READINESS_FIELDS, "mappings.readiness")
    normalized_mappings = {
        field: normalize_mapping(provider, field, mappings[field]) for field in MAPPING_FIELDS
    }
    for field in MAPPING_FIELDS:
        require_unique_values(normalized_mappings[field], f"mappings.{field}")
    require_unique_label_representations(provider, normalized_mappings)

    normalized: dict[str, Any] = {
        "version": version,
        "provider": provider,
        "target": normalize_target(provider, value["target"]),
        "synchronization": synchronization,
        "mappings": normalized_mappings,
    }
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
