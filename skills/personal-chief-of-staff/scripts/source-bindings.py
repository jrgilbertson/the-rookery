#!/usr/bin/env python3
"""Read the one user-global chief-of-staff source map, rejecting ambiguous JSON."""

import json
import os
import re
import stat
import sys
from pathlib import Path


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
    if type(data["version"]) is not int or data["version"] != 1:
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
            if (
                not isinstance(entry, dict)
                or not required <= entry.keys()
                or not entry.keys() <= required | optional
            ):
                raise ValueError(f"{role}: invalid binding fields")
            if ("locator" in entry) == ("query" in entry):
                raise ValueError(f"{role}: specify one locator or query")
            for key in required - {"modes", "condition"} | (entry.keys() & optional):
                if not nonempty_string(entry[key]):
                    raise ValueError(f"{role}: {key} must be nonempty text")
            if not isinstance(entry["condition"], str) or entry["condition"] not in {
                "baseline", "bounded", "mode-specific", "conditional"
            }:
                raise ValueError(f"{role}: invalid read condition")
            modes = entry["modes"]
            if not isinstance(modes, list) or not modes or any(
                not isinstance(mode, str) or mode not in {"wind-down", "weekly", "quarterly"}
                for mode in modes
            ) or len(set(modes)) != len(modes):
                raise ValueError(f"{role}: invalid modes")
            if role in {"strategy", "learning", "tasks"} and (
                entry["condition"] != "baseline" or set(modes) != {"wind-down", "weekly", "quarterly"}
            ):
                raise ValueError(f"{role}: required baseline must cover all review modes")


def read_map():
    path = Path.home() / ".config/the-rookery/personal-chief-of-staff/sources.json"
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "r", encoding="utf-8") as source:
        if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
            raise ValueError("map is not a regular file")
        data = json.load(
            source,
            object_pairs_hook=object_without_duplicates,
            parse_constant=reject_constant,
        )
    validate(data)
    return data


def reject_constant(value):
    raise ValueError(f"invalid JSON value: {value}")


def main():
    if sys.argv[1:] != ["read"]:
        print("usage: source-bindings.py read", file=sys.stderr)
        return 2
    try:
        data = read_map()
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"source map unresolved: {error}", file=sys.stderr)
        return 2
    json.dump(data, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
