#!/usr/bin/env python3
"""Check the shipped daily-learning config sample against its documented schema."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
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

FORBIDDEN_GRANT_SUFFIXES = ("_enabled", "_available", "_installed", "_allowed", "_reachable")
TAG_PATTERN = re.compile(r"^#[A-Za-z0-9][A-Za-z0-9/_-]*$")
SSH_REMOTE_PATTERN = re.compile(r"^(?:ssh://[^/\s]+/.+|[^:\s/]+@[^:\s/]+:[^\s]+)$")
LOCAL_HOME_PATTERNS = (
    re.compile(r"(?:^|[\s\"'(=])~/(?!<|\$)"),
    re.compile(r"/" + r"Users/(?!<|\$)"),
    re.compile(r"/" + r"home/(?!<|\$)"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\(?![<%])", re.IGNORECASE),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    keys = [key for key, _ in pairs]
    require(len(keys) == len(set(keys)), f"duplicate key in config: {keys}")
    return dict(pairs)


def nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def reject_local_home_paths(value: object, context: str) -> None:
    if isinstance(value, str):
        for pattern in LOCAL_HOME_PATTERNS:
            require(pattern.search(value) is None, f"{context}: local home path is not allowed: {value!r}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_local_home_paths(item, f"{context}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            reject_local_home_paths(item, f"{context}.{key}")


def reject_capability_grants(value: object, context: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, bool) and key.endswith(FORBIDDEN_GRANT_SUFFIXES):
                raise AssertionError(f"{context}.{key}: capability boolean is not allowed")
            reject_capability_grants(item, f"{context}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_capability_grants(item, f"{context}[{index}]")


def check_remote_url(url: object) -> None:
    require(nonempty_text(url), "vault.git_backup_mirror.remote_url must be nonempty text")
    assert isinstance(url, str)
    lowered = url.lower()
    require(not lowered.startswith(("ext::", "file://")), f"unsafe mirror remote_url scheme: {url!r}")
    require(not url.startswith(("/", ".", "~")), f"local path mirror remote_url is not allowed: {url!r}")
    if lowered.startswith("https://"):
        parsed = urlparse(url)
        require(bool(parsed.netloc) and bool(parsed.path.strip("/")), f"invalid https remote_url: {url!r}")
    else:
        require(SSH_REMOTE_PATTERN.fullmatch(url) is not None, f"mirror remote_url must be ssh or https: {url!r}")


def check_loopback_url(url: object) -> None:
    require(nonempty_text(url), "anki.connect_url must be nonempty text")
    assert isinstance(url, str)
    parsed = urlparse(url)
    require(parsed.scheme == "http", f"anki.connect_url must use http: {url!r}")
    require(parsed.hostname in {"127.0.0.1", "localhost"}, f"anki.connect_url must target loopback: {url!r}")
    require(parsed.port is not None and 1 <= parsed.port <= 65535, f"anki.connect_url must include a valid port: {url!r}")
    require(parsed.path in {"", "/"} and not parsed.query and not parsed.fragment, f"anki.connect_url must not carry path/query: {url!r}")


def check_vault_relative(path: object, field: str, suffix: str | None = None) -> None:
    require(nonempty_text(path), f"{field} must be nonempty text")
    assert isinstance(path, str)
    require(not path.startswith(("/", "~")) and ".." not in Path(path).parts, f"{field} must be vault-relative: {path!r}")
    if suffix is not None:
        require(
            not path.endswith("/") and path.endswith(suffix) and len(Path(path).name) > len(suffix),
            f"{field} must be a vault-relative {suffix} file path: {path!r}",
        )


def validate_config(raw_text: str) -> None:
    def reject_constant(token: str) -> None:
        raise ValueError(f"nonstandard JSON constant: {token}")

    config = json.loads(raw_text, object_pairs_hook=reject_duplicates, parse_constant=reject_constant)
    require(isinstance(config, dict), "config root must be an object")
    require({"version", "vault"} <= config.keys() <= TOP_KEYS, f"invalid top-level keys: {sorted(config)}")
    require(type(config["version"]) is int and config["version"] == 1, "version must be integer 1")

    reject_capability_grants(config, "config")
    reject_local_home_paths(config, "config")

    vault = config["vault"]
    require(isinstance(vault, dict) and {"name", "reference_tags"} <= vault.keys() <= VAULT_KEYS, "invalid vault object")
    require(nonempty_text(vault["name"]), "vault.name must be nonempty text")

    tags = vault["reference_tags"]
    require(isinstance(tags, dict) and set(tags) == TAG_KEYS, "vault.reference_tags must define in_progress and completed")
    for tag_field in TAG_KEYS:
        tag_val = tags[tag_field]
        require(nonempty_text(tag_val) and TAG_PATTERN.fullmatch(str(tag_val)) is not None, f"invalid tag {tag_field}: {tag_val!r}")
    require(str(tags["in_progress"]).lower() != str(tags["completed"]).lower(), "reference_tags must be distinct")

    if "git_backup_mirror" in vault:
        mirror = vault["git_backup_mirror"]
        require(isinstance(mirror, dict) and set(mirror) == MIRROR_KEYS, "invalid vault.git_backup_mirror keys")
        check_remote_url(mirror["remote_url"])
        require(nonempty_text(mirror["cache_dir"]), "vault.git_backup_mirror.cache_dir must be nonempty text")

    for list_field, suffix in (("reference_note_paths", None), ("queue_notes", ".md")):
        if list_field in vault:
            entries = vault[list_field]
            require(isinstance(entries, list) and bool(entries), f"vault.{list_field} must be a nonempty list")
            for item in entries:
                check_vault_relative(item, f"vault.{list_field}", suffix=suffix)

    if "strategy_and_learning" in config:
        strat = config["strategy_and_learning"]
        require(isinstance(strat, dict) and set(strat) <= STRATEGY_KEYS and len(strat) == 1,
                "strategy_and_learning must set exactly one of personal_chief_of_staff_map or direct_paths")
        if "personal_chief_of_staff_map" in strat:
            cos_map = strat["personal_chief_of_staff_map"]
            require(isinstance(cos_map, dict) and set(cos_map) == COS_MAP_KEYS, "invalid personal_chief_of_staff_map keys")
            require(cos_map["locator_kind"] in {"host-file", "vault-file"}, "locator_kind must be host-file or vault-file")
            require(nonempty_text(cos_map["path"]), "personal_chief_of_staff_map.path must be nonempty text")
            if cos_map["locator_kind"] == "vault-file":
                check_vault_relative(cos_map["path"], "personal_chief_of_staff_map.path", suffix=".json")
            require(isinstance(cos_map["allow_cross_mode_read"], bool), "allow_cross_mode_read must be boolean")
        else:
            direct = strat["direct_paths"]
            require(isinstance(direct, dict) and bool(direct) and set(direct) <= DIRECT_KEYS, "invalid direct_paths")
            if "strategy" in direct:
                check_vault_relative(direct["strategy"], "direct_paths.strategy", suffix=".md")
            if "learning" in direct:
                learning = direct["learning"]
                if isinstance(learning, list):
                    require(bool(learning), "direct_paths.learning list must be nonempty")
                    for item in learning:
                        check_vault_relative(item, "direct_paths.learning", suffix=".md")
                else:
                    check_vault_relative(learning, "direct_paths.learning", suffix=".md")

    if "remote_environments" in config:
        remotes = config["remote_environments"]
        require(isinstance(remotes, list), "remote_environments must be a list")
        seen_names: set[str] = set()
        for entry in remotes:
            require(
                isinstance(entry, dict) and REMOTE_REQUIRED_KEYS <= set(entry) <= REMOTE_KEYS,
                "remote environment requires name, workspace_selector, agent (and optional scan_timeout_minutes)",
            )
            for field in REMOTE_REQUIRED_KEYS:
                require(nonempty_text(entry[field]), f"remote_environments.{field} must be nonempty text")
            if "scan_timeout_minutes" in entry:
                timeout = entry["scan_timeout_minutes"]
                require(
                    type(timeout) is int and timeout >= 1,
                    f"remote_environments.scan_timeout_minutes must be a positive integer: {timeout!r}",
                )
            require(str(entry["workspace_selector"]).strip().lower() != "current", "workspace_selector must not be current")
            name = str(entry["name"])
            require(name not in seen_names, f"duplicate remote environment name: {name}")
            seen_names.add(name)

    if "automation_runs" in config:
        runs = config["automation_runs"]
        require(isinstance(runs, dict) and set(runs) == RUNS_KEYS, "invalid automation_runs keys")
        require(nonempty_text(runs["repo_path"]), "automation_runs.repo_path must be nonempty text")

    if "anki" in config:
        anki = config["anki"]
        require(isinstance(anki, dict) and set(anki) <= ANKI_KEYS and bool(anki), "invalid anki keys")
        if "connect_url" in anki:
            check_loopback_url(anki["connect_url"])


def expect_failure(label: str, raw_text: str) -> None:
    try:
        validate_config(raw_text)
    except (AssertionError, ValueError):
        return
    raise AssertionError(f"negative fixture unexpectedly passed: {label}")


def main() -> int:
    sample_text = SAMPLE.read_text(encoding="utf-8")
    validate_config(sample_text)
    base = json.loads(sample_text)

    bad_grant = copy.deepcopy(base)
    bad_grant["anki_enabled"] = True
    expect_failure("forbidden capability boolean", json.dumps(bad_grant))

    bad_url = copy.deepcopy(base)
    bad_url["anki"]["connect_url"] = "http://192.0.2.10:8765"
    expect_failure("non-loopback anki.connect_url", json.dumps(bad_url))

    bad_ext = copy.deepcopy(base)
    bad_ext["vault"]["git_backup_mirror"]["remote_url"] = "ext::sh -c id"
    expect_failure("ext:: git remote_url", json.dumps(bad_ext))

    bad_file_url = copy.deepcopy(base)
    bad_file_url["vault"]["git_backup_mirror"]["remote_url"] = "file:///tmp/vault.git"
    expect_failure("file:// git remote_url", json.dumps(bad_file_url))

    bad_tags = copy.deepcopy(base)
    bad_tags["vault"]["reference_tags"] = {"in_progress": "reading", "completed": "#reviewed"}
    expect_failure("missing # prefix on tag", json.dumps(bad_tags))

    dup_tags = copy.deepcopy(base)
    dup_tags["vault"]["reference_tags"] = {"in_progress": "#reviewed", "completed": "#Reviewed"}
    expect_failure("duplicate reference tags", json.dumps(dup_tags))

    bad_home = copy.deepcopy(base)
    bad_home["automation_runs"]["repo_path"] = "/" + "Users/fixture-account/runs"
    expect_failure("literal local home path", json.dumps(bad_home))

    bad_current = copy.deepcopy(base)
    bad_current["remote_environments"][0]["workspace_selector"] = "current"
    expect_failure("remote workspace_selector current", json.dumps(bad_current))

    good_default_timeout = copy.deepcopy(base)
    del good_default_timeout["remote_environments"][0]["scan_timeout_minutes"]
    validate_config(json.dumps(good_default_timeout))

    for label, bad_timeout in (
        ("zero scan_timeout_minutes", 0),
        ("negative scan_timeout_minutes", -5),
        ("float scan_timeout_minutes", 10.0),
        ("bool scan_timeout_minutes", True),
        ("string scan_timeout_minutes", "10"),
    ):
        bad_remote_timeout = copy.deepcopy(base)
        bad_remote_timeout["remote_environments"][0]["scan_timeout_minutes"] = bad_timeout
        expect_failure(label, json.dumps(bad_remote_timeout))

    bad_version_float = copy.deepcopy(base)
    bad_version_float["version"] = 1.0
    expect_failure("float version 1.0", json.dumps(bad_version_float))

    bad_queue_ext = copy.deepcopy(base)
    bad_queue_ext["vault"]["queue_notes"] = ["To Explore.txt"]
    expect_failure("non-.md queue_notes path", json.dumps(bad_queue_ext))

    good_vault_map = copy.deepcopy(base)
    good_vault_map["strategy_and_learning"] = {
        "personal_chief_of_staff_map": {
            "locator_kind": "vault-file",
            "path": "System/sources.json",
            "allow_cross_mode_read": True,
        }
    }
    validate_config(json.dumps(good_vault_map))

    bad_vault_map_ext = copy.deepcopy(good_vault_map)
    bad_vault_map_ext["strategy_and_learning"]["personal_chief_of_staff_map"]["path"] = "System/sources.yaml"
    expect_failure("non-.json vault-file map path", json.dumps(bad_vault_map_ext))

    good_direct = copy.deepcopy(base)
    good_direct["strategy_and_learning"] = {
        "direct_paths": {
            "strategy": "Strategy/Personal Strategy.md",
            "learning": ["Learning/Core Learnings.md"],
        }
    }
    validate_config(json.dumps(good_direct))

    bad_direct_strategy_ext = copy.deepcopy(good_direct)
    bad_direct_strategy_ext["strategy_and_learning"]["direct_paths"]["strategy"] = "Strategy/Personal Strategy.txt"
    expect_failure("non-.md direct_paths.strategy", json.dumps(bad_direct_strategy_ext))

    bad_direct_learning_ext = copy.deepcopy(good_direct)
    bad_direct_learning_ext["strategy_and_learning"]["direct_paths"]["learning"] = ["Learning/Core Learnings.txt"]
    expect_failure("non-.md direct_paths.learning", json.dumps(bad_direct_learning_ext))

    expect_failure("duplicate JSON keys", '{"version": 1, "version": 1, "vault": {"name": "v", "reference_tags": {"in_progress": "#reading", "completed": "#reviewed"}}}')

    print("PASS: daily-learning config sample and negative schema checks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, ValueError, KeyError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
