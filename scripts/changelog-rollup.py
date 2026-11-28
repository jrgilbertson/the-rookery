#!/usr/bin/env python3
"""Roll up changelog.d/ fragments into CHANGELOG.md."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = {
    "added": "Added", "changed": "Changed", "deprecated": "Deprecated",
    "removed": "Removed", "fixed": "Fixed", "security": "Security",
}
ORDER = tuple(SECTIONS.values())
FRAGMENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.([a-z]+)\.md$")


def trim(lines: list[str]) -> list[str]:
    i = next((n for n, s in enumerate(lines) if s), len(lines))
    j = next((n for n in range(len(lines), i, -1) if lines[n - 1]), i)
    return lines[i:j]


def load_fragments(directory: Path) -> tuple[list[Path], dict[str, list[str]]]:
    if not directory.is_dir():
        raise ValueError(f"{directory}: fragments directory not found")
    files, grouped = [], {}
    for path in sorted(directory.iterdir(), key=lambda p: p.name):
        if path.name == "README.md":
            continue
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"{path.name}: expected a regular fragment file")
        match = FRAGMENT_RE.match(path.name)
        if not match or match.group(1) not in SECTIONS:
            raise ValueError(f"{path.name}: expected <slug>.<section>.md ({', '.join(SECTIONS)})")
        body = path.read_text(encoding="utf-8").strip()
        if not body.startswith("- ") or any(ln.startswith(("## ", "### ")) for ln in body.splitlines()):
            raise ValueError(f"{path.name}: must hold '- ' bullet items with no '##'/'###' headings")
        files.append(path)
        grouped.setdefault(SECTIONS[match.group(1)], []).append(body)
    return files, grouped


def merge_changelog(text: str, grouped: dict[str, list[str]], release: str | None) -> str:
    lines = text.splitlines()
    if release:
        bracketed = release.startswith("[") and "]" in release
        prefix = f"## {release.split(']', 1)[0]}]" if bracketed else f"## [{release}]"
        heading = f"## {release}" if bracketed else f"## [{release}] - {date.today().isoformat()}"
        start = next((i for i, ln in enumerate(lines) if ln == prefix or ln.startswith(f"{prefix} ")), None)
        if start is None:
            unrel = next((i for i, ln in enumerate(lines) if ln == "## [Unreleased]"), -1)
            at = next((i for i in range(unrel + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
            while at > 0 and not lines[at - 1]:
                at -= 1
            lead = [""] if at > 0 else []
            lines[at:at], start = [*lead, heading, ""], at + len(lead)
    else:
        start = next((i for i, ln in enumerate(lines) if ln == "## [Unreleased]"), None)
        if start is None:
            raise ValueError("CHANGELOG.md: missing '## [Unreleased]' section")

    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    preamble, subsections = [], []
    for ln in lines[start + 1 : end]:
        if ln.startswith("### "):
            subsections.append((ln[4:].strip(), []))
        else:
            (subsections[-1][1] if subsections else preamble).append(ln)

    for section in ORDER:
        if not (entries := grouped.get(section)):
            continue
        new_lines = "\n".join(entries).splitlines()
        idx = next((i for i, (name, _) in enumerate(subsections) if name == section), None)
        if idx is not None:
            subsections[idx] = (section, new_lines + trim(subsections[idx][1]))
        else:
            rank = ORDER.index(section)
            pos = next((i for i, (n, _) in enumerate(subsections) if n in ORDER and ORDER.index(n) > rank), len(subsections))
            subsections.insert(pos, (section, new_lines))

    rebuilt = [lines[start], *(("", *t) if (t := trim(preamble)) else ())]
    for name, body in subsections:
        rebuilt.extend(["", f"### {name}", *(("", *t) if (t := trim(body)) else ())])
    return "\n".join(lines[:start] + rebuilt + ([""] if end < len(lines) else []) + lines[end:]) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Roll up changelog.d/ fragments into CHANGELOG.md.")
    ap.add_argument("--fragments-dir", type=Path, default=ROOT / "changelog.d")
    ap.add_argument("--changelog", type=Path, default=ROOT / "CHANGELOG.md")
    ap.add_argument("--release", help="Target release heading (e.g. 0.4.0) instead of Unreleased")
    ap.add_argument("--dry-run", action="store_true", help="Print updated changelog without writing or deleting")
    ap.add_argument("--check", action="store_true", help="Validate fragments and target section without writing")
    args = ap.parse_args(argv)
    try:
        files, grouped = load_fragments(args.fragments_dir)
        text = args.changelog.read_text(encoding="utf-8")
        updated = merge_changelog(text, grouped, args.release) if files or args.check else text
    except (OSError, ValueError) as exc:
        print(f"changelog-rollup: {exc}", file=sys.stderr)
        return 1
    if args.check:
        print(f"changelog-rollup: {len(files)} fragment(s) valid" if files else "changelog-rollup: no fragments")
    elif args.dry_run:
        sys.stdout.write(updated)
    elif not files:
        print("changelog-rollup: no fragments to roll up")
    else:
        args.changelog.write_text(updated, encoding="utf-8")
        for path in files:
            path.unlink()
        print(f"changelog-rollup: rolled up {len(files)} fragment(s) into {args.changelog}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
