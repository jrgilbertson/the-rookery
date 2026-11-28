#!/usr/bin/env python3
"""Offline checks for scripts/changelog-rollup.py and live changelog.d/ fragments."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts/changelog-rollup.py"

SAMPLE_CHANGELOG = """\
# Changelog

Intro text.

## [Unreleased]

### Added

- Existing added entry.

### Fixed

- Existing fixed entry.

## [0.3.0] - 2026-10-15

Snapshot note.

### Added

- Released entry.
"""


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_live_repo() -> None:
    result = run("--check")
    require(result.returncode == 0, f"live changelog.d/ check failed: {result.stderr}")


def check_empty_noop() -> None:
    with tempfile.TemporaryDirectory(prefix="rookery-changelog-empty-") as tmp:
        root = Path(tmp)
        changelog = root / "CHANGELOG.md"
        fragments = root / "changelog.d"
        fragments.mkdir()
        (fragments / "README.md").write_text("# Fragments\n", encoding="utf-8")
        changelog.write_text(SAMPLE_CHANGELOG, encoding="utf-8")

        for extra in (("--check",), ("--dry-run",), ()):
            result = run("--fragments-dir", str(fragments), "--changelog", str(changelog), *extra)
            require(result.returncode == 0, f"empty {extra} failed: {result.stderr}")
            if extra == ("--dry-run",):
                require(result.stdout == SAMPLE_CHANGELOG, "empty --dry-run altered changelog text")
        require(changelog.read_text(encoding="utf-8") == SAMPLE_CHANGELOG, "empty rollup modified CHANGELOG.md")
        require((fragments / "README.md").is_file(), "empty rollup removed README.md")


def check_rollup_and_ordering() -> None:
    with tempfile.TemporaryDirectory(prefix="rookery-changelog-rollup-") as tmp:
        root = Path(tmp)
        changelog = root / "CHANGELOG.md"
        fragments = root / "changelog.d"
        fragments.mkdir()
        (fragments / "README.md").write_text("# Fragments\n", encoding="utf-8")
        changelog.write_text(SAMPLE_CHANGELOG, encoding="utf-8")

        (fragments / "02-second.added.md").write_text(
            "- Second added entry\n  wrapped across two lines.\n",
            encoding="utf-8",
        )
        (fragments / "01-first.added.md").write_text(
            "- First added entry.\n- Companion bullet in the same fragment.\n",
            encoding="utf-8",
        )
        (fragments / "10-change.changed.md").write_text("- Changed behavior.\n", encoding="utf-8")
        (fragments / "20-remove.removed.md").write_text("- Removed legacy flag.\n", encoding="utf-8")
        (fragments / "30-fix.fixed.md").write_text("- Fixed edge case.\n", encoding="utf-8")
        (fragments / "40-sec.security.md").write_text("- Hardened token check.\n", encoding="utf-8")

        expected = """\
# Changelog

Intro text.

## [Unreleased]

### Added

- First added entry.
- Companion bullet in the same fragment.
- Second added entry
  wrapped across two lines.
- Existing added entry.

### Changed

- Changed behavior.

### Removed

- Removed legacy flag.

### Fixed

- Fixed edge case.
- Existing fixed entry.

### Security

- Hardened token check.

## [0.3.0] - 2026-10-15

Snapshot note.

### Added

- Released entry.
"""

        checked = run("--fragments-dir", str(fragments), "--changelog", str(changelog), "--check")
        require(checked.returncode == 0 and "6 fragment(s) valid" in checked.stdout, f"--check failed: {checked.stderr}")
        require(changelog.read_text(encoding="utf-8") == SAMPLE_CHANGELOG, "--check modified CHANGELOG.md")

        dry = run("--fragments-dir", str(fragments), "--changelog", str(changelog), "--dry-run")
        require(dry.returncode == 0, f"--dry-run failed: {dry.stderr}")
        require(dry.stdout == expected, f"--dry-run output mismatch:\n{dry.stdout}\n---\n{expected}")
        require(changelog.read_text(encoding="utf-8") == SAMPLE_CHANGELOG, "--dry-run modified CHANGELOG.md")
        require(len(list(fragments.iterdir())) == 7, "--dry-run deleted fragment files")

        applied = run("--fragments-dir", str(fragments), "--changelog", str(changelog))
        require(applied.returncode == 0, f"rollup failed: {applied.stderr}")
        require(changelog.read_text(encoding="utf-8") == expected, f"rollup output mismatch:\n{changelog.read_text(encoding='utf-8')}")
        remaining = [p.name for p in fragments.iterdir()]
        require(remaining == ["README.md"], f"expected only README.md left, found {remaining}")

        second = run("--fragments-dir", str(fragments), "--changelog", str(changelog))
        require(second.returncode == 0, f"second rollup failed: {second.stderr}")
        require(changelog.read_text(encoding="utf-8") == expected, "second rollup altered CHANGELOG.md")

    # Rolling up into an empty ## [Unreleased] section creates subsections cleanly.
    with tempfile.TemporaryDirectory(prefix="rookery-changelog-fresh-") as tmp:
        root = Path(tmp)
        changelog = root / "CHANGELOG.md"
        fragments = root / "changelog.d"
        fragments.mkdir()
        changelog.write_text("# Changelog\n\n## [Unreleased]\n\n## [0.3.0] - 2026-10-15\n", encoding="utf-8")
        (fragments / "01-item.added.md").write_text("- Fresh entry.\n", encoding="utf-8")
        fresh = run("--fragments-dir", str(fragments), "--changelog", str(changelog))
        require(fresh.returncode == 0, f"fresh Unreleased rollup failed: {fresh.stderr}")
        require(
            changelog.read_text(encoding="utf-8")
            == "# Changelog\n\n## [Unreleased]\n\n### Added\n\n- Fresh entry.\n\n## [0.3.0] - 2026-10-15\n",
            f"fresh Unreleased layout mismatch:\n{changelog.read_text(encoding='utf-8')}",
        )


def check_release_flag() -> None:
    with tempfile.TemporaryDirectory(prefix="rookery-changelog-release-") as tmp:
        root = Path(tmp)
        changelog = root / "CHANGELOG.md"
        fragments = root / "changelog.d"
        fragments.mkdir()
        (fragments / "README.md").write_text("# Fragments\n", encoding="utf-8")
        changelog.write_text(SAMPLE_CHANGELOG, encoding="utf-8")

        # Merge into an existing release section without losing its intro text.
        (fragments / "01-backport.fixed.md").write_text("- Backported fix.\n", encoding="utf-8")
        existing = run(
            "--fragments-dir", str(fragments),
            "--changelog", str(changelog),
            "--release", "0.3.0",
        )
        require(existing.returncode == 0, f"existing --release failed: {existing.stderr}")
        after_existing = changelog.read_text(encoding="utf-8")
        require(
            "## [0.3.0] - 2026-10-15\n\nSnapshot note.\n\n### Added\n\n- Released entry.\n\n### Fixed\n\n- Backported fix.\n"
            in after_existing,
            f"existing --release layout unexpected:\n{after_existing}",
        )

        # Create a new release heading cleanly after Unreleased and before 0.3.0.
        (fragments / "02-new.added.md").write_text("- Release feature.\n", encoding="utf-8")
        created = run(
            "--fragments-dir", str(fragments),
            "--changelog", str(changelog),
            "--release", "[0.4.0] - 2026-11-27",
        )
        require(created.returncode == 0, f"new --release failed: {created.stderr}")
        after_created = changelog.read_text(encoding="utf-8")
        require(
            "- Existing fixed entry.\n\n## [0.4.0] - 2026-11-27\n\n### Added\n\n- Release feature.\n\n## [0.3.0] - 2026-10-15\n"
            in after_created,
            f"new --release layout unexpected:\n{after_created}",
        )


def check_invalid_inputs() -> None:
    bad_cases = (
        ("no-suffix.md", "- Missing section suffix.\n", "expected <slug>.<section>.md"),
        ("stray.txt", "- Wrong extension.\n", "expected <slug>.<section>.md"),
        ("462-bad.bogus.md", "- Unknown section.\n", "expected <slug>.<section>.md"),
        ("462-empty.added.md", "   \n\n", "bullet items"),
        ("462-prose.added.md", "Not a bullet line.\n", "bullet items"),
        ("462-heading.added.md", "- Bullet\n### Added\n- Sneaky heading.\n", "bullet items"),
    )
    for filename, content, expected_err in bad_cases:
        with tempfile.TemporaryDirectory(prefix="rookery-changelog-invalid-") as tmp:
            root = Path(tmp)
            changelog = root / "CHANGELOG.md"
            fragments = root / "changelog.d"
            fragments.mkdir()
            (fragments / "README.md").write_text("# Fragments\n", encoding="utf-8")
            (fragments / filename).write_text(content, encoding="utf-8")
            changelog.write_text(SAMPLE_CHANGELOG, encoding="utf-8")

            res = run("--fragments-dir", str(fragments), "--changelog", str(changelog))
            require(
                res.returncode != 0 and expected_err in res.stderr,
                f"expected failure ({expected_err!r}) for {filename}, got rc={res.returncode} stderr={res.stderr!r}",
            )
            require(changelog.read_text(encoding="utf-8") == SAMPLE_CHANGELOG, f"{filename} modified CHANGELOG.md on error")
            require((fragments / filename).is_file(), f"{filename} was deleted on error")

    with tempfile.TemporaryDirectory(prefix="rookery-changelog-missing-heading-") as tmp:
        root = Path(tmp)
        changelog = root / "CHANGELOG.md"
        fragments = root / "changelog.d"
        fragments.mkdir()
        (fragments / "01-item.added.md").write_text("- Item.\n", encoding="utf-8")
        changelog.write_text("# Changelog\n\n## [0.1.0] - 2026-07-10\n", encoding="utf-8")

        missing = run("--fragments-dir", str(fragments), "--changelog", str(changelog))
        require(
            missing.returncode != 0 and "missing '## [Unreleased]' section" in missing.stderr,
            f"missing Unreleased heading did not fail: {missing.stderr}",
        )
        require((fragments / "01-item.added.md").is_file(), "fragment deleted when Unreleased heading missing")

    with tempfile.TemporaryDirectory(prefix="rookery-changelog-symlink-") as tmp:
        root = Path(tmp)
        changelog = root / "CHANGELOG.md"
        fragments = root / "changelog.d"
        fragments.mkdir()
        outside = root / "outside.md"
        outside.write_text("- Outside.\n", encoding="utf-8")
        (fragments / "01-link.added.md").symlink_to(outside)
        changelog.write_text(SAMPLE_CHANGELOG, encoding="utf-8")

        linked = run("--fragments-dir", str(fragments), "--changelog", str(changelog))
        require(
            linked.returncode != 0 and "regular fragment file" in linked.stderr,
            f"symlink fragment did not fail: {linked.stderr}",
        )


def main() -> int:
    check_live_repo()
    check_empty_noop()
    check_rollup_and_ordering()
    check_release_flag()
    check_invalid_inputs()
    print("PASS: changelog rollup merges fragments deterministically, supports --release/--dry-run/--check, and rejects invalid inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
