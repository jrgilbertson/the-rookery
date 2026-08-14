#!/usr/bin/env python3
"""Dependency-free checks for repository text, JSON, and relative links."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

def candidate_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / path.decode() for path in result.stdout.split(b"\0") if path]


def readable_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def check_text(path: Path, text: str, errors: list[str]) -> None:
    relative = path.relative_to(ROOT)
    if text and not text.endswith("\n"):
        errors.append(f"{relative}: missing final newline")
    for number, line in enumerate(text.splitlines(), start=1):
        if line.endswith((" ", "\t")):
            errors.append(f"{relative}:{number}: trailing whitespace")


def check_json(path: Path, text: str, errors: list[str]) -> None:
    if path.suffix != ".json":
        return
    try:
        # Preserve Python's integer-conversion safety limit while accepting
        # deliberate large-integer parser fixtures as syntactically valid JSON.
        json.loads(text, parse_int=str)
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}:{exc.lineno}:{exc.colno}: {exc.msg}")


def link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def check_links(path: Path, text: str, errors: list[str]) -> None:
    if path.suffix.lower() not in {".md", ".markdown"}:
        return
    for match in MARKDOWN_LINK.finditer(text):
        target = link_target(match.group(1))
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not target or "{" in target:
            continue
        resolved = (
            ROOT / target.lstrip("/") if target.startswith("/") else path.parent / target
        ).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{path.relative_to(ROOT)}:{line}: relative link leaves repository: {target}")
            continue
        if not resolved.exists():
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{path.relative_to(ROOT)}:{line}: broken relative link: {target}")


def main() -> int:
    errors: list[str] = []
    for path in candidate_files():
        if not path.is_file():
            continue
        text = readable_text(path)
        if text is None:
            continue
        check_text(path, text, errors)
        check_json(path, text, errors)
        check_links(path, text, errors)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("repository: text, JSON, and relative-link checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
