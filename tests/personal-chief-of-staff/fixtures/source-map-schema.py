#!/usr/bin/env python3
"""Repository-only source-map schema checks; never writes or resolves sources."""

import json
import re
import sys
from pathlib import Path


REVIEW_MODES = {"wind-down", "weekly", "quarterly"}


def object_without_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def validate(data):
    if not isinstance(data, dict) or set(data) != {"version", "roles"}:
        raise ValueError("map must contain version and roles")
    if type(data["version"]) is not int or data["version"] not in {1, 2}:
        raise ValueError("unsupported map version")
    roles = data["roles"]
    if not isinstance(roles, dict):
        raise ValueError("roles must be an object")
    for role, entries in roles.items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*", role):
            raise ValueError("invalid role key")
        if not isinstance(entries, list) or not entries:
            raise ValueError(f"{role}: expected a nonempty binding list")
        for entry in entries:
            required = {"area", "interface", "identity", "condition", "modes"}
            optional = {"locator", "query", "window", "filter", "gap_effect"}
            if data["version"] == 2:
                optional |= {"source", "access_overrides"}
            if (
                not isinstance(entry, dict)
                or not required <= entry.keys()
                or not entry.keys() <= required | optional
            ):
                raise ValueError(f"{role}: invalid binding fields")
            if ("locator" in entry) == ("query" in entry):
                raise ValueError(f"{role}: specify one locator or query")
            for key in required - {"modes", "condition"} | (entry.keys() & (optional - {"access_overrides"})):
                if not nonempty_string(entry[key]):
                    raise ValueError(f"{role}: {key} must be nonempty text")
            if "access_overrides" in entry:
                overrides = entry["access_overrides"]
                if not nonempty_string(entry.get("source")):
                    raise ValueError(f"{role}: overrides require source")
                if not isinstance(overrides, dict) or not overrides:
                    raise ValueError(f"{role}: overrides must be a nonempty object")
                for harness, access in overrides.items():
                    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", harness):
                        raise ValueError(f"{role}: invalid harness key")
                    if not isinstance(access, dict) or set(access) not in (
                        {"interface", "identity", "locator"},
                        {"interface", "identity", "query"},
                    ) or not all(nonempty_string(value) for value in access.values()):
                        raise ValueError(f"{role}: override requires a complete access description")
            if not isinstance(entry["condition"], str) or entry["condition"] not in {
                "baseline", "bounded", "mode-specific", "conditional"
            }:
                raise ValueError(f"{role}: invalid read condition")
            modes = entry["modes"]
            if not isinstance(modes, list) or not modes or any(
                not isinstance(mode, str) or mode not in REVIEW_MODES
                for mode in modes
            ) or len(set(modes)) != len(modes):
                raise ValueError(f"{role}: invalid modes")
            if role in {"strategy", "learning", "tasks"} and (
                entry["condition"] != "baseline" or set(modes) != REVIEW_MODES
            ):
                raise ValueError(f"{role}: required baseline must cover all review modes")


def reject_constant(value):
    raise ValueError(f"invalid JSON value: {value}")


def read_map(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=object_without_duplicates,
                      parse_constant=reject_constant)
    validate(data)
    return data


if __name__ == "__main__":
    try:
        data = read_map(sys.argv[1])
    except (OSError, UnicodeError, ValueError) as error:
        print(f"invalid source map: {error}", file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps(data, ensure_ascii=False))
