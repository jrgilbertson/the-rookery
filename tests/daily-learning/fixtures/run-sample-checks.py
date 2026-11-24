#!/usr/bin/env python3
"""Check the shipped daily-learning config sample against its documented schema."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import TypeGuard
from urllib.parse import urlparse

SAMPLE = Path(__file__).resolve().parents[3] / "skills/daily-learning/assets/config.example.json"

TOP_KEYS = {
    "version",
    "vault",
    "strategy_and_learning",
    "remote_environments",
    "automation_runs",
    "anki",
}
VAULT_KEYS = {
    "name",
    "git_backup_mirror",
    "reference_note_paths",
    "queue_notes",
    "reference_tags",
}
MIRROR_KEYS = {"remote_url", "cache_dir"}
TAG_KEYS = {"in_progress", "completed"}
STRATEGY_KEYS = {"personal_chief_of_staff_map", "direct_paths"}
COS_MAP_KEYS = {"locator_kind", "path", "allow_cross_mode_read"}
DIRECT_KEYS = {"strategy", "learning"}
REMOTE_REQUIRED_KEYS = {"name", "workspace_selector", "agent"}
REMOTE_KEYS = REMOTE_REQUIRED_KEYS | {"scan_timeout_minutes"}
RUNS_KEYS = {"repo_path"}
ANKI_KEYS = {"connect_url"}

TAG_PATTERN = re.compile(r"^#[A-Za-z0-9][A-Za-z0-9/_-]*$")
SSH_REMOTE_PATTERN = re.compile(r"^(?:ssh://[^/\s]+/.+|[^:\s/]+@[^:\s/]+:[^\s]+)$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    keys = [key for key, _ in pairs]
    require(len(keys) == len(set(keys)), f"duplicate key in config: {keys}")
    return dict(pairs)


def nonempty_text(value: object) -> TypeGuard[str]:
    return isinstance(value, str) and bool(value.strip())


def require_nonempty_text(value: object, field: str) -> str:
    require(nonempty_text(value), f"{field} must be nonempty text")
    return value


def check_remote_url(value: object) -> None:
    url = require_nonempty_text(value, "vault.git_backup_mirror.remote_url")
    lowered = url.lower()
    require(not lowered.startswith(("ext::", "file://")), f"unsafe mirror remote_url scheme: {url!r}")
    require(not url.startswith(("/", ".", "~")), f"local path mirror remote_url is not allowed: {url!r}")
    if lowered.startswith("https://"):
        parsed = urlparse(url)
        require(bool(parsed.netloc) and bool(parsed.path.strip("/")), f"invalid https remote_url: {url!r}")
    else:
        require(SSH_REMOTE_PATTERN.fullmatch(url) is not None, f"mirror remote_url must be ssh or https: {url!r}")


def check_loopback_url(value: object) -> None:
    url = require_nonempty_text(value, "anki.connect_url")
    parsed = urlparse(url)
    require(parsed.scheme == "http", f"anki.connect_url must use http: {url!r}")
    require(parsed.hostname in {"127.0.0.1", "localhost"}, f"anki.connect_url must target loopback: {url!r}")
    require(parsed.port is not None and 1 <= parsed.port <= 65535, f"anki.connect_url must include a valid port: {url!r}")
    require(parsed.path in {"", "/"} and not parsed.query and not parsed.fragment, f"anki.connect_url must not carry path/query: {url!r}")


def check_vault_relative(value: object, field: str, suffix: str | None = None) -> None:
    path = require_nonempty_text(value, field)
    require(not path.startswith(("/", "~")) and ".." not in Path(path).parts, f"{field} must be vault-relative: {path!r}")
    if suffix is not None:
        require(
            not path.endswith("/") and path.endswith(suffix) and len(Path(path).name) > len(suffix),
            f"{field} must be a vault-relative {suffix} file path: {path!r}",
        )


def check_strategy_and_learning(strat: object) -> None:
    require(
        isinstance(strat, dict) and set(strat) <= STRATEGY_KEYS and len(strat) == 1,
        "strategy_and_learning must set exactly one of personal_chief_of_staff_map or direct_paths",
    )
    if "personal_chief_of_staff_map" in strat:
        cos_map = strat["personal_chief_of_staff_map"]
        require(isinstance(cos_map, dict) and set(cos_map) == COS_MAP_KEYS, "invalid personal_chief_of_staff_map keys")
        require(cos_map["locator_kind"] in {"host-file", "vault-file"}, "locator_kind must be host-file or vault-file")
        if cos_map["locator_kind"] == "vault-file":
            check_vault_relative(cos_map["path"], "personal_chief_of_staff_map.path", suffix=".json")
        else:
            require_nonempty_text(cos_map["path"], "personal_chief_of_staff_map.path")
        require(isinstance(cos_map["allow_cross_mode_read"], bool), "allow_cross_mode_read must be boolean")
        return

    direct = strat["direct_paths"]
    require(isinstance(direct, dict) and bool(direct) and set(direct) <= DIRECT_KEYS, "invalid direct_paths")
    if "strategy" in direct:
        check_vault_relative(direct["strategy"], "direct_paths.strategy", suffix=".md")
    if "learning" in direct:
        learning = direct["learning"]
        items = learning if isinstance(learning, list) else [learning]
        require(bool(items), "direct_paths.learning list must be nonempty")
        for item in items:
            check_vault_relative(item, "direct_paths.learning", suffix=".md")


def validate_config(raw_text: str) -> None:
    def reject_constant(token: str) -> None:
        raise ValueError(f"nonstandard JSON constant: {token}")

    config = json.loads(raw_text, object_pairs_hook=reject_duplicates, parse_constant=reject_constant)
    require(isinstance(config, dict), "config root must be an object")
    require({"version", "vault"} <= config.keys() <= TOP_KEYS, f"invalid top-level keys: {sorted(config)}")
    require(type(config["version"]) is int and config["version"] == 1, "version must be integer 1")

    vault = config["vault"]
    require(isinstance(vault, dict) and {"name", "reference_tags"} <= vault.keys() <= VAULT_KEYS, "invalid vault object")
    require_nonempty_text(vault["name"], "vault.name")

    tags = vault["reference_tags"]
    require(isinstance(tags, dict) and set(tags) == TAG_KEYS, "vault.reference_tags must define in_progress and completed")
    validated_tags: dict[str, str] = {}
    for tag_field in TAG_KEYS:
        tag_val = tags[tag_field]
        require(nonempty_text(tag_val) and TAG_PATTERN.fullmatch(tag_val) is not None, f"invalid tag {tag_field}: {tag_val!r}")
        validated_tags[tag_field] = tag_val
    require(validated_tags["in_progress"].lower() != validated_tags["completed"].lower(), "reference_tags must be distinct")

    if "git_backup_mirror" in vault:
        mirror = vault["git_backup_mirror"]
        require(isinstance(mirror, dict) and set(mirror) == MIRROR_KEYS, "invalid vault.git_backup_mirror keys")
        check_remote_url(mirror["remote_url"])
        require_nonempty_text(mirror["cache_dir"], "vault.git_backup_mirror.cache_dir")

    for list_field, suffix in (("reference_note_paths", None), ("queue_notes", ".md")):
        if list_field in vault:
            entries = vault[list_field]
            require(isinstance(entries, list) and bool(entries), f"vault.{list_field} must be a nonempty list")
            for item in entries:
                check_vault_relative(item, f"vault.{list_field}", suffix=suffix)

    if "strategy_and_learning" in config:
        check_strategy_and_learning(config["strategy_and_learning"])

    if "remote_environments" in config:
        remotes = config["remote_environments"]
        require(isinstance(remotes, list), "remote_environments must be a list")
        seen_names: set[str] = set()
        for entry in remotes:
            require(
                isinstance(entry, dict) and REMOTE_REQUIRED_KEYS <= entry.keys() <= REMOTE_KEYS,
                "remote environment requires name, workspace_selector, agent (and optional scan_timeout_minutes)",
            )
            name = require_nonempty_text(entry["name"], "remote_environments.name")
            selector = require_nonempty_text(entry["workspace_selector"], "remote_environments.workspace_selector")
            require_nonempty_text(entry["agent"], "remote_environments.agent")
            if "scan_timeout_minutes" in entry:
                timeout = entry["scan_timeout_minutes"]
                require(
                    type(timeout) is int and timeout >= 1,
                    f"remote_environments.scan_timeout_minutes must be a positive integer: {timeout!r}",
                )
            require(selector.strip().lower() != "current", "workspace_selector must not be current")
            require(name not in seen_names, f"duplicate remote environment name: {name}")
            seen_names.add(name)

    if "automation_runs" in config:
        runs = config["automation_runs"]
        require(isinstance(runs, dict) and set(runs) == RUNS_KEYS, "invalid automation_runs keys")
        require_nonempty_text(runs["repo_path"], "automation_runs.repo_path")

    if "anki" in config:
        anki = config["anki"]
        require(isinstance(anki, dict) and set(anki) == ANKI_KEYS, "invalid anki keys")
        check_loopback_url(anki["connect_url"])


def main() -> int:
    validate_config(SAMPLE.read_text(encoding="utf-8"))
    print("PASS: daily-learning config sample")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, ValueError, KeyError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
