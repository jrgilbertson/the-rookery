#!/usr/bin/env python3
"""Dependency-free checks for repository text, JSON, and relative links."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from bisect import bisect_left
from itertools import chain
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
TEXT_EXTENSIONS = frozenset(
    {
        ".ambiguous",
        ".empty",
        ".failure",
        ".json",
        ".markdown",
        ".md",
        ".partial",
        ".py",
        ".rb",
        ".sh",
        ".svg",
        ".trace",
        ".txt",
        ".yaml",
        ".yml",
    }
)
TEXT_FILENAMES = frozenset({".gitignore", ".gitleaksignore", "LICENSE"})
TRANSIENT_PATHS = (
    ":(top)plans/**",
    ":(top)docs/plans/**",
    ":(top)docs/brainstorms/**",
    ":(top)docs/ideation/**",
    ":(top)docs/dogfood-reports/**",
    ":(top)docs/reports/**",
    ":(top)docs/pulse-reports/**",
    ":(top)outputs/**",
    ":(top)tmp/**",
)
MARKDOWN_REFERENCE = re.compile(
    r"^\s{0,3}\[(?:[^\]\\]|\\.)+\]:\s*(<[^>]*>|\S+)",
    re.MULTILINE,
)
HOME_PATH = re.compile(
    r"(?<![\w./\\-])(?:(?i:file://(?:localhost)?)?/(?:Users|home)/[\w.@-]+|"
    r"(?i:[A-Z]:[/\\]+Users[/\\]+)[\w.@-]+|~/[\w.@-]+)"
    r"(?:[/\\][^\s<>\"'`|,;:!?()\[\]{}]*)?"
)
# Reviewed portable setup examples, scoped to their owning file and exact path.
# Split the home prefix so the allowlist itself contains no local-path literals.
HOME_PATH_EXAMPLES = {
    "automations/README.md": {"~" + "/.local/state/automation-runs"},
    "automations/agent-entropy-audit.md": {"~" + "/.local/state/automation-runs"},
    "automations/daily-learning.md": {"~" + "/.local/state/automation-runs"},
    "evals/active-learning/records/2026-11-25-opus-5-5-active-learning/single-note-with_skill-round1.json": {"~" + "/.obsidian-cli.sock"},
    "automations/analytics-gap-audit.md": {"~" + "/.local/state/automation-runs"},
    "automations/design-system-audit.md": {"~" + "/.local/state/automation-runs"},
    "automations/improve-audit.md": {"~" + "/.local/state/automation-runs"},
    "automations/optimize-ci.md": {"~" + "/.local/state/automation-runs"},
    "automations/sessions-audit.md": {"~" + "/.local/state/automation-runs"},
    "automations/state-machine-audit.md": {"~" + "/.local/state/automation-runs"},
    "automations/test-audit.md": {"~" + "/.local/state/automation-runs"},
    "automations/weekly-codebase-design.md": {"~" + "/.local/state/automation-runs"},
    "MACHINE-SETUP.md": {
        "~" + "/.codex/AGENTS.md",
        "~" + "/.codex/config.toml",
        "~" + "/.claude/CLAUDE.md",
        "~" + "/.claude/plugins/marketplaces/compound-engineering-plugin",
        "~" + "/.gemini/config/AGENTS.md",
        "~" + "/.gemini/config/plugins",
        "~" + "/.gemini/config/plugins/compound-engineering",
        "~" + "/.grok/AGENTS.md",
        "~" + "/.local",
        "~" + "/.cursor/rules/global-agents.mdc",
    },
    "WORKFLOWS.md": {"~" + "/.codex/AGENTS.md"},
    "scripts/sync-global-agents.sh": {"~" + "/.codex/AGENTS.md"},
    "docs/solutions/best-practices/blind-cross-model-grading-through-native-schema-flags.md": {
        "~" + "/.grok/auth.json",
    },
    "skills/personal-chief-of-staff/references/source-bindings.md": {
        "~" + "/.config/the-rookery/personal-chief-of-staff/sources.json",
    },
}


RULE_HEADING = "## Rank by leverage"
RULE_SOURCE = "PRIORITIZATION.md"
RULE_COPIES = (
    "GLOBAL-AGENTS.md",
    "skills/managing-issues/references/prioritization.md",
)

# Each skill ships its own copy of the review contract, because a package
# cannot read another package's files. The copies must stay byte-identical.
CONTRACT_COPIES = (
    "skills/reviewing-prs/references/review-contract.md",
    "skills/repo-captain/references/review-contract.md",
)


def candidate_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / path.decode() for path in result.stdout.split(b"\0") if path]


def check_tracked_transient_paths(errors: list[str]) -> None:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "-z", "--", *TRANSIENT_PATHS],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    for raw_path in result.stdout.split(b"\0"):
        if raw_path:
            errors.append(
                f"{raw_path.decode()}: transient working artifact must not be tracked"
            )


# Root compatibility symlink for Compound Engineering's ce-compound, which
# hardcodes CONCEPTS.md. Symbolic links remain forbidden everywhere else.
ALLOWED_ROOT_SYMLINKS = {
    "CONCEPTS.md": "GLOSSARY.md",
}


def allowed_root_symlink(path: Path, relative: Path) -> bool:
    if len(relative.parts) != 1:
        return False
    expected_target = ALLOWED_ROOT_SYMLINKS.get(relative.name)
    if expected_target is None:
        return False
    try:
        if os.readlink(path) != expected_target:
            return False
        target = ROOT / expected_target
        if target.is_symlink():
            return False
        resolved = path.resolve(strict=True)
        resolved.relative_to(ROOT)
        return resolved == target.resolve(strict=True) and resolved.is_file()
    except (FileNotFoundError, OSError, ValueError):
        return False


def safe_regular_file(path: Path, errors: list[str]) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        errors.append(f"{path!s}: repository path escapes the repository")
        return False
    current = ROOT
    for component in relative.parts:
        current /= component
        if current.is_symlink():
            if current == path and allowed_root_symlink(path, relative):
                return False
            errors.append(f"{relative}: symbolic link is not allowed")
            return False
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(ROOT)
    except FileNotFoundError:
        return False
    except (OSError, ValueError):
        errors.append(f"{relative}: resolved path leaves repository or cannot be verified")
        return False
    return resolved.is_file()


def readable_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def check_text(path: Path, text: str, errors: list[str]) -> None:
    relative = path.relative_to(ROOT)
    home_path_examples = HOME_PATH_EXAMPLES.get(relative.as_posix(), ())
    if text and not text.endswith("\n"):
        errors.append(f"{relative}: missing final newline")
    for number, line in enumerate(text.splitlines(), start=1):
        if line.endswith((" ", "\t")):
            errors.append(f"{relative}:{number}: trailing whitespace")
        for match in HOME_PATH.finditer(line):
            if match.group() not in home_path_examples:
                errors.append(f"{relative}:{number}: local home-directory path is not allowed")


def reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant: {value}")


def check_json(path: Path, text: str, errors: list[str]) -> None:
    if path.suffix != ".json":
        return
    try:
        # Preserve Python's integer-conversion safety limit while accepting
        # deliberate large-integer parser fixtures as syntactically valid JSON.
        json.loads(
            text,
            parse_int=str,
            parse_constant=reject_json_constant,
        )
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}:{exc.lineno}:{exc.colno}: {exc.msg}")
    except ValueError as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")


def link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def inline_links(text: str):
    """Yield the existing inline-link grammar without rescanning failed suffixes."""
    position = 0
    while True:
        opening = text.find("[", position)
        if opening < 0:
            return
        closing = text.find("]", opening + 1)
        if closing < 0:
            return
        if text[closing + 1 : closing + 2] == "(":
            end = text.find(")", closing + 2)
            if end < 0:
                return
            if end > closing + 2:
                start = opening - 1 if opening > position and text[opening - 1] == "!" else opening
                yield start, text[closing + 2 : end]
                position = end + 1
                continue
        # All opening brackets before this closing bracket share its failed suffix.
        position = closing + 1


def check_links(path: Path, text: str, errors: list[str]) -> None:
    if path.suffix.lower() not in {".md", ".markdown"}:
        return
    newlines = [offset for offset, character in enumerate(text) if character == "\n"]
    for start, raw_target in chain(
        inline_links(text),
        ((match.start(), match.group(1)) for match in MARKDOWN_REFERENCE.finditer(text)),
    ):
        target = link_target(raw_target)
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
            line = bisect_left(newlines, start) + 1
            errors.append(f"{path.relative_to(ROOT)}:{line}: relative link leaves repository: {target}")
            continue
        if not resolved.exists():
            line = bisect_left(newlines, start) + 1
            errors.append(f"{path.relative_to(ROOT)}:{line}: broken relative link: {target}")


def rule_section(text: str) -> str | None:
    lines = text.splitlines()
    if lines.count(RULE_HEADING) != 1:
        return None
    start = lines.index(RULE_HEADING)
    end = next(
        (index for index in range(start + 1, len(lines)) if re.match(r"#{1,2} ", lines[index])),
        len(lines),
    )
    return "\n".join(lines[start:end]).rstrip()


def check_rule_copies(errors: list[str]) -> None:
    source = ROOT / RULE_SOURCE
    copies = [ROOT / copy for copy in RULE_COPIES]
    if not any(path.exists() for path in (source, *copies)):
        return

    def section_of(path: Path) -> str | None:
        relative = path.relative_to(ROOT)
        if path.is_symlink():
            return None  # main() reports the symbolic link itself
        if not path.is_file():
            errors.append(f"{relative}: missing; it must hold the '{RULE_HEADING}' section")
            return None
        text = readable_text(path)
        section = rule_section(text) if text is not None else None
        if section is None:
            errors.append(f"{relative}: expected exactly one '{RULE_HEADING}' section")
        return section

    source_section = section_of(source)
    for copy, path in zip(RULE_COPIES, copies):
        section = section_of(path)
        if source_section is not None and section is not None and section != source_section:
            errors.append(f"{copy}: '{RULE_HEADING}' section differs from {RULE_SOURCE}")


def check_contract_copies(errors: list[str]) -> None:
    paths = [ROOT / copy for copy in CONTRACT_COPIES]
    if not any(path.exists() for path in paths):
        return
    contents: list[bytes | None] = []
    for copy, path in zip(CONTRACT_COPIES, paths):
        if path.is_symlink():
            contents.append(None)  # main() reports the symbolic link itself
        elif not path.is_file():
            errors.append(f"{copy}: missing; it must be a copy of the shared review contract")
            contents.append(None)
        else:
            contents.append(path.read_bytes())
    first = contents[0]
    for copy, content in zip(CONTRACT_COPIES[1:], contents[1:]):
        if first is not None and content is not None and content != first:
            errors.append(f"{copy}: differs from {CONTRACT_COPIES[0]}")


def check_contract_factor_lines(errors: list[str]) -> None:
    source = ROOT / RULE_SOURCE
    if source.is_symlink() or not source.is_file():
        return
    text = readable_text(source)
    section = rule_section(text) if text is not None else None
    if section is None:
        return  # check_rule_copies reports a missing or repeated section
    factors = [line for line in section.splitlines() if line.startswith("- ")]
    for copy in CONTRACT_COPIES:
        path = ROOT / copy
        if path.is_symlink() or not path.is_file():
            continue
        contract = readable_text(path)
        if contract is not None and any(line not in contract.splitlines() for line in factors):
            errors.append(f"{copy}: its factor lines differ from the '{RULE_HEADING}' section of {RULE_SOURCE}")


def main() -> int:
    errors: list[str] = []
    check_tracked_transient_paths(errors)
    check_rule_copies(errors)
    check_contract_copies(errors)
    check_contract_factor_lines(errors)
    for path in candidate_files():
        if not safe_regular_file(path, errors):
            continue
        text = readable_text(path)
        if text is None:
            if path.suffix.lower() in TEXT_EXTENSIONS or path.name in TEXT_FILENAMES:
                errors.append(f"{path.relative_to(ROOT)}: invalid UTF-8")
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
