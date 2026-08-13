#!/usr/bin/env python3
"""Validate and normalize the managing-issues repository policy."""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any


MAX_POLICY_BYTES = 64 * 1024
MAX_SYNC_MAPPING_BYTES = 64 * 1024
MAX_MAPPING_ENTRIES = 64
MAX_SYNC_MAPPING_ENTRIES = 250
MAX_TEXT_LENGTH = 256
MAX_INTEGER = 2_147_483_647
TOP_LEVEL_FIELDS = {"version", "provider", "target", "synchronization", "mappings"}
REQUIRED_TOP_LEVEL_FIELDS = {"version", "provider", "target", "mappings"}
MAPPING_FIELDS = ("work_type", "readiness", "priority", "leaf_estimate")
LINEAR_TARGET_FIELDS = {"workspace", "team"}
SYNC_MAPPING_FIELDS = {"version", "github_to_linear"}
LINEAR_PRIORITIES = {"none", "low", "medium", "high", "urgent"}
MAPPING_KEY = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
GITHUB_OWNER_REPO = (
    r"^(?P<owner>[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)/"
    r"(?P<repo>[A-Za-z0-9](?:[A-Za-z0-9._-]{0,98}[A-Za-z0-9._-])?)"
)
GITHUB_TARGET = re.compile(GITHUB_OWNER_REPO + r"$")
LINEAR_TARGET_PART = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
MAPPING_SOURCE_PART = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
GITHUB_ISSUE = re.compile(GITHUB_OWNER_REPO + r"#(?P<number>[1-9][0-9]{0,9})$")
LINEAR_ISSUE = re.compile(r"^[A-Z][A-Z0-9]{0,15}-[1-9][0-9]{0,9}$")


class PolicyError(Exception):
    """The policy cannot safely select managing-issues behavior."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PolicyError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PolicyError(f"duplicate key {key!r}")
        result[key] = value
    return result


def reject_non_finite(value: str) -> None:
    raise PolicyError(f"non-finite JSON value {value} is not allowed")


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
        raise PolicyError("repo root must be an existing directory") from error
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
            raise PolicyError(f"{label} is missing") from error
        except OSError as error:
            raise PolicyError(f"{label} cannot be inspected") from error

        require(not stat.S_ISLNK(metadata.st_mode), f"{label} contains a symlink component")
        if index < len(parts) - 1:
            require(stat.S_ISDIR(metadata.st_mode), f"{label} contains a non-directory component")
        else:
            require(stat.S_ISREG(metadata.st_mode), f"{label} must be a regular file")
    return current


def inspect_external_file(path: Path, label: str, *, missing_ok: bool) -> Path | None:
    candidate = path.absolute()
    try:
        metadata = candidate.lstat()
    except FileNotFoundError as error:
        if missing_ok:
            return None
        raise PolicyError(f"{label} is missing") from error
    except OSError as error:
        raise PolicyError(f"{label} cannot be inspected") from error
    require(not stat.S_ISLNK(metadata.st_mode), f"{label} must not be a symlink")
    require(stat.S_ISREG(metadata.st_mode), f"{label} must be a regular file")
    return candidate


def require_active_policy_path(path: str, repo_root: Path) -> Path:
    expected = repo_root / ".agents" / "managing-issues.json"
    require(
        path == str(expected),
        "policy must be the lexical repository path .agents/managing-issues.json",
    )
    return expected


def load_active_policy(path: str, repo_root: Path) -> dict[str, Any] | None:
    require_active_policy_path(path, repo_root)
    checked = inspect_repo_file(
        repo_root,
        (".agents", "managing-issues.json"),
        "active policy path",
        missing_ok=True,
    )
    if checked is None:
        return None
    return parse_json_object(bounded_read(checked, MAX_POLICY_BYTES, "policy"), "policy")


def load_trusted_policy(path: Path) -> dict[str, Any] | None:
    checked = inspect_external_file(path, "trusted policy", missing_ok=True)
    if checked is None:
        return None
    return parse_json_object(bounded_read(checked, MAX_POLICY_BYTES, "trusted policy"), "policy")


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
        raise PolicyError(f"{label} missing key: {missing[0]}")
    if unexpected:
        raise PolicyError(f"{label} has unexpected key: {unexpected[0]}")


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
    require(bool(value), f"{label} must not be empty")
    require(len(value) <= MAX_MAPPING_ENTRIES, f"{label} exceeds {MAX_MAPPING_ENTRIES} entries")
    result: dict[str, str | int] = {}
    for key, provider_value in value.items():
        require(MAPPING_KEY.fullmatch(key) is not None, f"{label}.{key} has an invalid mapping key")
        entry_label = f"{label}.{key}"
        if provider == "github":
            github_value = require_concrete_text(provider_value, entry_label)
            if field != "work_type":
                require(
                    "," not in github_value and '"' not in github_value,
                    f"{entry_label} cannot contain GitHub label CSV syntax",
                )
            result[key] = github_value
        elif field in ("work_type", "readiness"):
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


def normalize_mapping_source(value: Any) -> tuple[str, tuple[str, ...]]:
    source = require_concrete_text(value, "synchronization.mapping_source")
    require(
        "\\" not in source,
        "synchronization.mapping_source must use repository-relative POSIX syntax",
    )
    require(not source.startswith("/"), "synchronization.mapping_source must be repository-relative")
    parts = tuple(source.split("/"))
    require(
        bool(parts) and all(part not in {"", ".", ".."} for part in parts),
        "synchronization.mapping_source must not contain empty, . or .. segments",
    )
    require(
        all(MAPPING_SOURCE_PART.fullmatch(part) is not None for part in parts),
        "synchronization.mapping_source contains an invalid path segment",
    )
    normalized = PurePosixPath(*parts).as_posix()
    require(
        normalized == source,
        "synchronization.mapping_source must use normalized POSIX syntax",
    )
    return normalized, parts


def normalize_policy(value: dict[str, Any]) -> dict[str, Any]:
    require_exact_fields(value, REQUIRED_TOP_LEVEL_FIELDS, TOP_LEVEL_FIELDS, "policy")
    version = value["version"]
    require(isinstance(version, int) and not isinstance(version, bool) and version == 1, "version must be 1")
    provider = value["provider"]
    require(
        isinstance(provider, str) and provider in {"github", "linear"},
        "provider must be github or linear",
    )
    require(
        provider == "linear" or "synchronization" not in value,
        "synchronization requires provider linear",
    )

    mappings = value["mappings"]
    require(isinstance(mappings, dict), "mappings must be an object")
    require_exact_fields(mappings, set(MAPPING_FIELDS), set(MAPPING_FIELDS), "mappings")
    normalized: dict[str, Any] = {
        "version": version,
        "provider": provider,
        "target": normalize_target(provider, value["target"]),
        "mappings": {
            field: normalize_mapping(provider, field, mappings[field]) for field in MAPPING_FIELDS
        },
    }

    if "synchronization" in value:
        synchronization = value["synchronization"]
        require(isinstance(synchronization, dict), "synchronization must be an object")
        require_exact_fields(
            synchronization,
            {"mapping_source"},
            {"mapping_source"},
            "synchronization",
        )
        source, _ = normalize_mapping_source(synchronization["mapping_source"])
        normalized["synchronization"] = {"mapping_source": source}
    return normalized


def normalize_sync_mapping(value: dict[str, Any]) -> dict[str, Any]:
    require_exact_fields(value, SYNC_MAPPING_FIELDS, SYNC_MAPPING_FIELDS, "mapping")
    version = value["version"]
    require(
        isinstance(version, int) and not isinstance(version, bool) and version == 1,
        "mapping version must be 1",
    )
    links = value["github_to_linear"]
    require(isinstance(links, dict), "mapping.github_to_linear must be an object")
    require(
        len(links) <= MAX_SYNC_MAPPING_ENTRIES,
        f"mapping.github_to_linear exceeds {MAX_SYNC_MAPPING_ENTRIES} entries",
    )

    normalized_links: dict[str, str] = {}
    linear_targets: set[str] = set()
    for github_issue, linear_issue in links.items():
        github_text = require_concrete_text(github_issue, "mapping GitHub issue")
        github_match = GITHUB_ISSUE.fullmatch(github_text)
        require(
            github_match is not None,
            "mapping GitHub issue must be OWNER/REPOSITORY#NUMBER",
        )
        normalized_github = (
            f"{github_match.group('owner').lower()}/"
            f"{github_match.group('repo').lower()}#{github_match.group('number')}"
        )
        require(
            normalized_github not in normalized_links,
            "mapping contains a duplicate normalized GitHub issue",
        )

        linear_text = require_concrete_text(linear_issue, f"mapping.{github_text}")
        require(
            LINEAR_ISSUE.fullmatch(linear_text) is not None,
            "mapping Linear issue must be TEAM-NUMBER",
        )
        require(linear_text not in linear_targets, "mapping contains a duplicate Linear target")
        normalized_links[normalized_github] = linear_text
        linear_targets.add(linear_text)

    return {"version": version, "github_to_linear": dict(sorted(normalized_links.items()))}


def load_current_mapping(repo_root: Path, policy: dict[str, Any]) -> dict[str, Any] | None:
    synchronization = policy.get("synchronization")
    if synchronization is None:
        return None
    _, parts = normalize_mapping_source(synchronization["mapping_source"])
    checked = inspect_repo_file(
        repo_root,
        parts,
        "synchronization.mapping_source",
        missing_ok=False,
    )
    require(checked is not None, "synchronization.mapping_source is missing")
    raw = bounded_read(checked, MAX_SYNC_MAPPING_BYTES, "synchronization mapping")
    return normalize_sync_mapping(parse_json_object(raw, "mapping"))


def load_trusted_mapping(path: Path) -> dict[str, Any]:
    checked = inspect_external_file(path, "trusted mapping", missing_ok=False)
    require(checked is not None, "trusted mapping is missing")
    raw = bounded_read(checked, MAX_SYNC_MAPPING_BYTES, "trusted mapping")
    return normalize_sync_mapping(parse_json_object(raw, "mapping"))


def compare_sensitive(current: dict[str, Any], trusted: dict[str, Any]) -> None:
    if (current["provider"], current["target"]) != (trusted["provider"], trusted["target"]):
        raise PolicyError("canonical provider or target differs from trusted policy")
    if current.get("synchronization") != trusted.get("synchronization"):
        raise PolicyError("synchronization settings differ from trusted policy")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":"))


def escape_diagnostic(error: BaseException) -> str:
    return json.dumps(str(error), ensure_ascii=True)[1:-1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--trusted-policy", type=Path)
    parser.add_argument("--trusted-mapping", type=Path)
    args = parser.parse_args()

    require(
        args.trusted_policy is not None or args.trusted_mapping is None,
        "--trusted-mapping requires --trusted-policy",
    )
    repo_root = require_repo_root(args.repo_root)
    current_raw = load_active_policy(args.policy, repo_root)
    trusted_raw = load_trusted_policy(args.trusted_policy) if args.trusted_policy is not None else None

    if args.trusted_policy is not None and (current_raw is None) != (trusted_raw is None):
        raise PolicyError("current policy presence differs from trusted policy")
    if current_raw is None:
        require(
            args.trusted_mapping is None,
            "--trusted-mapping requires trusted synchronization settings",
        )
        print(canonical_json({"status": "missing"}))
        return 0

    current = normalize_policy(current_raw)
    current_mapping = load_current_mapping(repo_root, current)
    if args.trusted_policy is not None:
        require(trusted_raw is not None, "trusted policy is missing")
        trusted = normalize_policy(trusted_raw)
        compare_sensitive(current, trusted)
        if "synchronization" in trusted:
            require(
                args.trusted_mapping is not None,
                "trusted Linear synchronization requires --trusted-mapping",
            )
            trusted_mapping = load_trusted_mapping(args.trusted_mapping)
            require(
                current_mapping == trusted_mapping,
                "synchronization mapping differs from trusted mapping",
            )
        else:
            require(
                args.trusted_mapping is None,
                "--trusted-mapping requires trusted synchronization settings",
            )
    print(canonical_json({"policy": current, "status": "valid"}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        OSError,
        UnicodeError,
        ValueError,
        PolicyError,
        RecursionError,
    ) as error:
        print(f"FAIL: {escape_diagnostic(error)}", file=sys.stderr)
        raise SystemExit(1)
