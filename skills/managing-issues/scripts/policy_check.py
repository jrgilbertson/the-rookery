#!/usr/bin/env python3
"""Validate and normalize the managing-issues repository policy."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MAX_POLICY_BYTES = 64 * 1024
MAX_MAPPING_ENTRIES = 64
MAX_TEXT_LENGTH = 256
TOP_LEVEL_FIELDS = {"version", "provider", "target", "synchronization", "mappings"}
REQUIRED_TOP_LEVEL_FIELDS = {"version", "provider", "target", "mappings"}
MAPPING_FIELDS = ("work_type", "readiness", "priority", "leaf_estimate")
MAPPING_KEY = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
GITHUB_TARGET = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})/[A-Za-z0-9](?:[A-Za-z0-9._-]{0,99})$"
)
LINEAR_TARGET = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._:/-]{0,255})$")


class PolicyError(Exception):
    """The policy cannot safely select managing-issues behavior."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PolicyError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PolicyError(f"duplicate key '{key}'")
        result[key] = value
    return result


def reject_non_finite(value: str) -> None:
    raise PolicyError(f"non-finite JSON value {value} is not allowed")


def load_policy(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    require(path.is_file(), f"policy path is not a file: {path}")
    raw = path.read_bytes()
    require(len(raw) <= MAX_POLICY_BYTES, f"policy exceeds {MAX_POLICY_BYTES} bytes")
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_non_finite,
    )
    require(isinstance(value, dict), "policy must be a JSON object")
    return value


def require_active_policy_path(path: Path, repo_root: Path) -> Path:
    expected = (repo_root / ".agents" / "managing-issues.json").resolve(strict=False)
    try:
        expected.relative_to(repo_root)
    except ValueError as error:
        raise PolicyError("policy path resolves outside the repository") from error
    resolved = path.resolve(strict=False)
    require(resolved == expected, "policy must resolve to .agents/managing-issues.json inside the repository")
    return resolved


def require_exact_fields(
    value: dict[str, Any],
    required: set[str],
    allowed: set[str],
    label: str,
) -> None:
    missing = sorted(required - set(value))
    unexpected = sorted(set(value) - allowed)
    if missing:
        raise PolicyError(f"{label} missing key: {missing[0]}")
    if unexpected:
        raise PolicyError(f"{label} has unexpected key: {unexpected[0]}")


def require_concrete_text(value: Any, label: str) -> str:
    require(isinstance(value, str), f"{label} must be text")
    require(value == value.strip() and bool(value), f"{label} must be nonempty trimmed text")
    require(len(value) <= MAX_TEXT_LENGTH, f"{label} exceeds {MAX_TEXT_LENGTH} characters")
    require(all(character.isprintable() for character in value), f"{label} contains control characters")
    require("REPLACE_WITH" not in value, f"{label} has an unresolved REPLACE_WITH placeholder")
    return value


def normalize_target(provider: str, value: Any) -> str:
    target = require_concrete_text(value, "target")
    if provider == "github":
        require(GITHUB_TARGET.fullmatch(target) is not None, "GitHub target must be owner/repository")
        return target.lower()
    require(LINEAR_TARGET.fullmatch(target) is not None, "Linear target must be a stable team identifier")
    return target


def normalize_mapping(value: Any, label: str) -> dict[str, str | int]:
    require(isinstance(value, dict), f"{label} must be an object")
    require(bool(value), f"{label} must not be empty")
    require(len(value) <= MAX_MAPPING_ENTRIES, f"{label} exceeds {MAX_MAPPING_ENTRIES} entries")
    result: dict[str, str | int] = {}
    for key, provider_value in value.items():
        require(MAPPING_KEY.fullmatch(key) is not None, f"{label}.{key} has an invalid mapping key")
        entry_label = f"{label}.{key}"
        if isinstance(provider_value, str):
            result[key] = require_concrete_text(provider_value, entry_label)
        else:
            require(
                isinstance(provider_value, int)
                and not isinstance(provider_value, bool)
                and 0 <= provider_value <= 2_147_483_647,
                f"{entry_label} must be concrete text or a nonnegative integer",
            )
            result[key] = provider_value
    return dict(sorted(result.items()))


def normalize_mapping_source(value: Any, repo_root: Path) -> str:
    source = require_concrete_text(value, "synchronization.mapping_source")
    require("\\" not in source, "synchronization.mapping_source must use repository-relative POSIX syntax")
    source_path = Path(source)
    require(not source_path.is_absolute(), "synchronization.mapping_source must be repository-relative")
    resolved = (repo_root / source_path).resolve(strict=False)
    try:
        relative = resolved.relative_to(repo_root)
    except ValueError as error:
        raise PolicyError("synchronization.mapping_source resolves outside the repository") from error
    require(relative != Path("."), "synchronization.mapping_source must name a file")
    require(not resolved.exists() or resolved.is_file(), "synchronization.mapping_source must name a file")
    return relative.as_posix()


def normalize_policy(value: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    require_exact_fields(value, REQUIRED_TOP_LEVEL_FIELDS, TOP_LEVEL_FIELDS, "policy")
    version = value["version"]
    require(isinstance(version, int) and not isinstance(version, bool) and version == 1, "version must be 1")
    provider = value["provider"]
    require(provider in {"github", "linear"}, "provider must be github or linear")

    mappings = value["mappings"]
    require(isinstance(mappings, dict), "mappings must be an object")
    require_exact_fields(mappings, set(MAPPING_FIELDS), set(MAPPING_FIELDS), "mappings")
    normalized: dict[str, Any] = {
        "version": version,
        "provider": provider,
        "target": normalize_target(provider, value["target"]),
        "mappings": {
            name: normalize_mapping(mappings[name], f"mappings.{name}") for name in MAPPING_FIELDS
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
        normalized["synchronization"] = {
            "mapping_source": normalize_mapping_source(synchronization["mapping_source"], repo_root)
        }
    return normalized


def compare_sensitive(current: dict[str, Any], trusted: dict[str, Any]) -> None:
    if (current["provider"], current["target"]) != (trusted["provider"], trusted["target"]):
        raise PolicyError("canonical provider or target differs from trusted policy")
    if current.get("synchronization") != trusted.get("synchronization"):
        raise PolicyError("synchronization settings differ from trusted policy")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--trusted-policy", type=Path)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve(strict=False)
    require(repo_root.is_dir(), "repo root must be an existing directory")
    active_policy = require_active_policy_path(args.policy, repo_root)
    current_raw = load_policy(active_policy)
    trusted_raw = load_policy(args.trusted_policy) if args.trusted_policy is not None else None

    if args.trusted_policy is not None and (current_raw is None) != (trusted_raw is None):
        raise PolicyError("current policy presence differs from trusted policy")
    if current_raw is None:
        print(canonical_json({"status": "missing"}))
        return 0

    current = normalize_policy(current_raw, repo_root)
    if args.trusted_policy is not None:
        require(trusted_raw is not None, "trusted policy is missing")
        trusted = normalize_policy(trusted_raw, repo_root)
        compare_sensitive(current, trusted)
    print(canonical_json({"policy": current, "status": "valid"}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        PolicyError,
        RecursionError,
    ) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
