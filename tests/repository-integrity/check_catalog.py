#!/usr/bin/env python3
"""Prove the catalog door rejects a malformed skill package."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG_CHECK = ROOT / "scripts/checks/catalog.sh"
PACKAGE_CHECK = ROOT / "scripts/checks/skill_packages.rb"


def run_catalog(repository: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "scripts/checks/catalog.sh"],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="rookery-catalog-check-") as temporary:
        repository = Path(temporary) / "repository"
        check_directory = repository / "scripts/checks"
        skill_directory = repository / "skills/example-skill"
        check_directory.mkdir(parents=True)
        skill_directory.mkdir(parents=True)
        shutil.copy2(CATALOG_CHECK, check_directory / "catalog.sh")
        shutil.copy2(PACKAGE_CHECK, check_directory / "skill_packages.rb")
        subprocess.run(["git", "init", "-q", repository], check=True)
        (repository / "README.md").write_text(
            "- [example-skill](skills/example-skill/SKILL.md).\n",
            encoding="utf-8",
        )

        valid_skill = "---\nname: example-skill\ndescription: Use for a fixture.\n---\n\n# Example\n"
        (skill_directory / "SKILL.md").write_text(valid_skill, encoding="utf-8")
        valid = run_catalog(repository)
        if valid.returncode != 0:
            raise AssertionError(f"valid package failed: {valid.stderr}")

        malformed_skill = valid_skill.replace("description:", "owner: synthetic\ndescription:")
        (skill_directory / "SKILL.md").write_text(malformed_skill, encoding="utf-8")
        malformed = run_catalog(repository)
        if malformed.returncode != 1 or "unexpected frontmatter field" not in malformed.stderr:
            raise AssertionError("malformed package did not fail the catalog door")

        invalid_optional_fields = (
            ("license: false", "license must be text when present"),
            ("license: null", "license must be text when present"),
            ("license: 123", "license must be text when present"),
            (
                "compatibility: false",
                "compatibility must be text of at most 500 characters",
            ),
            (
                "compatibility: null",
                "compatibility must be text of at most 500 characters",
            ),
            (
                "compatibility: 123",
                "compatibility must be text of at most 500 characters",
            ),
            ("metadata: false", "metadata must contain only string keys and values"),
            ("metadata: null", "metadata must contain only string keys and values"),
            ("metadata: []", "metadata must contain only string keys and values"),
        )
        for field, expected_error in invalid_optional_fields:
            invalid_skill = valid_skill.replace("---\n\n# Example", f"{field}\n---\n\n# Example")
            (skill_directory / "SKILL.md").write_text(invalid_skill, encoding="utf-8")
            invalid = run_catalog(repository)
            if invalid.returncode != 1 or expected_error not in invalid.stderr:
                raise AssertionError(f"invalid optional field passed: {field}")

        external_skill = Path(temporary) / "external-SKILL.md"
        external_skill.write_text(valid_skill, encoding="utf-8")
        (skill_directory / "SKILL.md").unlink()
        (skill_directory / "SKILL.md").symlink_to(external_skill)
        symlinked = run_catalog(repository)
        if symlinked.returncode != 1 or "must not be a symlink" not in symlinked.stderr:
            raise AssertionError("symlinked skill package did not fail the catalog door")

    print("PASS: catalog door rejects malformed and symlinked skill packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
