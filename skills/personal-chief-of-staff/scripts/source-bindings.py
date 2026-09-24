#!/usr/bin/env python3
"""Read and narrowly update the user-global chief-of-staff source map."""

import fcntl
import hashlib
import json
import os
import re
import secrets
import stat
import sys
from pathlib import Path


PARTS = (".config", "the-rookery", "personal-chief-of-staff")
NAME = "sources.json"
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
                not isinstance(mode, str) or mode not in REVIEW_MODES
                for mode in modes
            ) or len(set(modes)) != len(modes):
                raise ValueError(f"{role}: invalid modes")
            if role in {"strategy", "learning", "tasks"} and (
                entry["condition"] != "baseline" or set(modes) != REVIEW_MODES
            ):
                raise ValueError(f"{role}: required baseline must cover all review modes")


def open_parent(create=False):
    """Anchor traversal to directory descriptors; never follow a map parent link."""
    fd = os.open(Path.home(), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in PARTS:
            if create:
                try:
                    os.mkdir(part, 0o700, dir_fd=fd)
                except FileExistsError:
                    pass
            next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def map_state(parent_fd):
    try:
        fd = os.open(NAME, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
    except FileNotFoundError:
        return None, "absent"
    with os.fdopen(fd, "rb") as source:
        metadata = os.fstat(source.fileno())
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError("map is not a regular file")
        if not stat.S_IMODE(metadata.st_mode) & 0o444:
            raise PermissionError("map has no read permission")
        content = source.read()
    data = json.loads(
        content.decode("utf-8"),
        object_pairs_hook=object_without_duplicates,
        parse_constant=reject_constant,
    )
    validate(data)
    identity = f"{metadata.st_dev}:{metadata.st_ino}:{metadata.st_mode}:{metadata.st_mtime_ns}:{metadata.st_ctime_ns}:{metadata.st_size}:".encode()
    fingerprint = hashlib.sha256(identity + content).hexdigest()
    return data, fingerprint


def read_map():
    parent_fd = open_parent()
    try:
        data, fingerprint = map_state(parent_fd)
        if fingerprint == "absent":
            raise FileNotFoundError("source map is absent")
        return data
    finally:
        os.close(parent_fd)


def snapshot():
    try:
        parent_fd = open_parent()
    except FileNotFoundError:
        return "absent"
    try:
        _, fingerprint = map_state(parent_fd)
        return fingerprint
    finally:
        os.close(parent_fd)


def write_map(payload):
    if not isinstance(payload, dict) or set(payload) != {"role", "bindings", "expected"}:
        raise ValueError("write requires role, bindings, and expected snapshot")
    role, bindings, expected = payload["role"], payload["bindings"], payload["expected"]
    if not isinstance(role, str) or not isinstance(expected, str) or not re.fullmatch(r"absent|[0-9a-f]{64}", expected):
        raise ValueError("invalid role or snapshot")
    validate({"version": 1, "roles": {role: bindings}})
    parent_fd = open_parent(create=True)
    lock_name = NAME + ".lock"
    lock_fd = None
    temp_name = None
    try:
        lock_fd = os.open(lock_name, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600, dir_fd=parent_fd)
        lock_metadata = os.fstat(lock_fd)
        if not stat.S_ISREG(lock_metadata.st_mode):
            raise ValueError("lock is not a regular file")
        if stat.S_IMODE(lock_metadata.st_mode) & 0o077:
            raise PermissionError("lock is not private")
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        current, actual = map_state(parent_fd)
        if actual != expected:
            raise ValueError("source map changed since preview")
        replacement = {"version": 1, "roles": dict(current["roles"]) if current else {}}
        replacement["roles"][role] = bindings
        validate(replacement)
        content = (json.dumps(replacement, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        temp_name = f".{NAME}.{secrets.token_hex(12)}.tmp"
        temp_fd = os.open(temp_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent_fd)
        with os.fdopen(temp_fd, "wb") as target:
            target.write(content)
            target.flush()
            os.fsync(target.fileno())
        if map_state(parent_fd)[1] != expected:
            raise ValueError("source map changed during write")
        os.replace(temp_name, NAME, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
        temp_name = None
        os.fsync(parent_fd)
        saved = read_map()
        if saved != replacement:
            raise ValueError("source map readback differs from approved replacement")
        return saved
    finally:
        try:
            if temp_name is not None:
                os.unlink(temp_name, dir_fd=parent_fd)
        finally:
            if lock_fd is not None:
                os.close(lock_fd)
            os.close(parent_fd)


def reject_constant(value):
    raise ValueError(f"invalid JSON value: {value}")


def main():
    if sys.argv[1:] not in (["read"], ["snapshot"], ["write"]):
        print("usage: source-bindings.py read|snapshot|write", file=sys.stderr)
        return 2
    try:
        command = sys.argv[1]
        if command == "snapshot":
            print(snapshot())
            return 0
        if command == "write":
            payload = json.load(sys.stdin, object_pairs_hook=object_without_duplicates, parse_constant=reject_constant)
            data = write_map(payload)
        else:
            data = read_map()
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"source map unresolved: {error}", file=sys.stderr)
        return 2
    json.dump(data, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
