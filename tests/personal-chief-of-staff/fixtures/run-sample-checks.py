#!/usr/bin/env python3
"""Check the shipped source-map sample against the documented version 3 shape."""

import json
import re
import sys
from pathlib import Path

SAMPLE = Path(__file__).resolve().parents[3] / "skills/personal-chief-of-staff/assets/sources.example.json"
REQUIRED_FIELDS = {"area", "source", "interface", "identity"}
OPTIONAL_FIELDS = {"locator", "query", "window", "filter", "gap_effect", "access_overrides"}
OVERRIDE_SHAPES = ({"interface", "identity", "locator"}, {"interface", "identity", "query"})


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def reject_duplicates(pairs):
    keys = [key for key, _ in pairs]
    require(len(keys) == len(set(keys)), f"duplicate key in sample: {keys}")
    return dict(pairs)


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def check_overrides(role, overrides):
    require(isinstance(overrides, dict) and overrides, f"{role}: access_overrides must be a nonempty object")
    for harness, access in overrides.items():
        require(re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", harness) is not None, f"{role}: invalid harness key {harness}")
        require(isinstance(access, dict) and set(access) in OVERRIDE_SHAPES
                and all(nonempty_text(value) for value in access.values()),
                f"{role}: {harness} override needs interface, identity, and one locator or query")


def main():
    sample = json.loads(SAMPLE.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(set(sample) == {"version", "roles"} and sample["version"] == 3, "sample is not a version 3 map")
    roles = sample["roles"]
    require({"strategy", "learning", "tasks", "templates", "meetings"} <= roles.keys(), "sample lacks a core role")
    entries = []
    for role, bindings in roles.items():
        require(re.fullmatch(r"[a-z][a-z0-9_]*", role) is not None, f"{role}: invalid role key")
        require(isinstance(bindings, list) and bindings, f"{role}: expected a nonempty binding list")
        for entry in bindings:
            require(isinstance(entry, dict) and REQUIRED_FIELDS <= entry.keys() <= REQUIRED_FIELDS | OPTIONAL_FIELDS,
                    f"{role}: invalid binding fields")
            require(("locator" in entry) != ("query" in entry), f"{role}: specify one locator or query")
            for field in entry.keys() - {"access_overrides"}:
                require(nonempty_text(entry[field]), f"{role}: {field} must be nonempty text")
            if "access_overrides" in entry:
                check_overrides(role, entry["access_overrides"])
            entries.append(entry)

    require({entry["area"] for entry in entries} == {
        "direction", "commitments", "relationships", "reflection", "resources", "health", "leisure",
    }, "sample areas differ")
    for role, area in (("reviews", "reflection"), ("templates", "reflection"), ("meetings", "relationships")):
        require(all(entry["area"] == area for entry in roles[role]), f"{role} entries are not in {area}")
    require({entry["locator"] for entry in roles["reviews"]}.isdisjoint(
        entry["locator"] for entry in roles["templates"]), "review and template locators overlap")
    print("PASS: personal-chief-of-staff source-map sample")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, ValueError, KeyError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
