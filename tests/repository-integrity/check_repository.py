#!/usr/bin/env python3
"""Exercise failure paths in the dependency-free repository checker."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/checks/repository.py"
LINT = ROOT / "scripts/checks/lint.sh"
FIXTURES = ROOT / "scripts/checks/fixtures.sh"

FIXTURE_RUNNERS = (
    "tests/checking-merge-readiness/fixtures/run-fetch-checks.sh",
    "tests/checking-merge-readiness/fixtures/run-stub-checks.sh",
    "tests/checking-pr-readiness/fixtures/run-assessment-checks.py",
    "tests/checking-pr-readiness/fixtures/run-helper-checks.sh",
    "tests/managing-issues/fixtures/run-graph-checks.py",
    "tests/managing-issues/fixtures/run-config-checks.py",
    "tests/managing-issues/fixtures/run-provider-checks.py",
    "tests/personal-chief-of-staff/fixtures/run-fixture-checks.sh",
    "tests/repository-integrity/check_catalog.py",
    "tests/repository-integrity/check_repository.py",
    "tests/repo-gardener/fixtures/effects/check_effects.py",
    "tests/repo-gardener/fixtures/github-register/check_snapshots.py",
    "tests/repo-gardener/fixtures/reconciliation/check_decisions.py",
    "tests/repo-gardener/fixtures/run-records/check_run_records.py",
)


def run_checker(repository: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/checks/repository.py"],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="rookery-repository-check-") as temporary:
        temporary_root = Path(temporary)
        repository = temporary_root / "repository"
        checker = repository / "scripts/checks/repository.py"
        checker.parent.mkdir(parents=True)
        shutil.copy2(CHECKER, checker)
        subprocess.run(["git", "init", "-q", repository], check=True)

        (repository / "target.md").write_text("# Target\n", encoding="utf-8")
        (repository / "README.md").write_text(
            "[target](target.md)\n\n[target-reference]: target.md\n",
            encoding="utf-8",
        )
        (repository / "large.json").write_text(
            '{"large": ' + "9" * 5000 + "}\n",
            encoding="utf-8",
        )
        clean = run_checker(repository)
        require(clean.returncode == 0, f"clean repository failed: {clean.stderr}")

        invalid_json = repository / "invalid.json"
        invalid_json.write_text('{"broken": }\n', encoding="utf-8")
        invalid = run_checker(repository)
        require(
            invalid.returncode == 1 and "invalid.json" in invalid.stderr,
            "invalid JSON did not fail with its path",
        )
        invalid_json.unlink()

        invalid_utf8_json = repository / "invalid-utf8.json"
        invalid_utf8_json.write_bytes(b'{"broken": "\xff"}\n')
        invalid_utf8 = run_checker(repository)
        require(
            invalid_utf8.returncode == 1 and "invalid-utf8.json" in invalid_utf8.stderr,
            "invalid UTF-8 JSON did not fail with its path",
        )
        invalid_utf8_json.unlink()

        readme = repository / "README.md"
        readme_contents = readme.read_bytes()
        readme.write_bytes(b"# Invalid UTF-8\n\xff\n")
        invalid_utf8_markdown = run_checker(repository)
        require(
            invalid_utf8_markdown.returncode == 1
            and "README.md: invalid UTF-8" in invalid_utf8_markdown.stderr,
            "invalid UTF-8 Markdown did not fail with its path",
        )
        readme.write_bytes(readme_contents)

        for filename in ("LICENSE", ".gitignore", ".gitleaksignore"):
            public_text = repository / filename
            public_text.write_bytes(b"invalid UTF-8: \xff\n")
            invalid_utf8_public_text = run_checker(repository)
            require(
                invalid_utf8_public_text.returncode == 1
                and f"{filename}: invalid UTF-8" in invalid_utf8_public_text.stderr,
                f"invalid UTF-8 {filename} did not fail with its path",
            )
            public_text.unlink()

        extensionless_binary = repository / "opaque-binary"
        extensionless_binary.write_bytes(b"\x00\xff\x00")
        extensionless_binary_result = run_checker(repository)
        require(
            extensionless_binary_result.returncode == 0,
            "unrelated extensionless binary was treated as repository text: "
            f"{extensionless_binary_result.stderr}",
        )
        extensionless_binary.unlink()

        binary_asset = repository / "asset.webp"
        binary_asset.write_bytes(b"RIFF\xffWEBP")
        binary = run_checker(repository)
        require(
            binary.returncode == 0,
            f"binary asset was treated as repository text: {binary.stderr}",
        )
        binary_asset.unlink()

        nonstandard_paths = []
        for name, constant in (
            ("nan", "NaN"),
            ("infinity", "Infinity"),
            ("negative-infinity", "-Infinity"),
        ):
            nonstandard_json = repository / f"nonstandard-{name}.json"
            nonstandard_json.write_text(
                f'{{"value": {constant}}}\n',
                encoding="utf-8",
            )
            nonstandard_paths.append(nonstandard_json)
        nonstandard = run_checker(repository)
        for nonstandard_json in nonstandard_paths:
            require(
                nonstandard.returncode == 1
                and nonstandard_json.name in nonstandard.stderr,
                f"non-standard JSON file {nonstandard_json.name} was accepted",
            )
            nonstandard_json.unlink()

        broken_link = repository / "broken.md"
        broken_link.write_text("[missing](missing.md)\n", encoding="utf-8")
        broken = run_checker(repository)
        require(
            broken.returncode == 1 and "broken.md" in broken.stderr,
            "broken relative link did not fail with its path",
        )
        broken_link.unlink()

        broken_reference = repository / "broken-reference.md"
        broken_reference.write_text(
            "[missing][guide]\n\n[guide]: missing.md\n",
            encoding="utf-8",
        )
        broken_reference_result = run_checker(repository)
        require(
            broken_reference_result.returncode == 1
            and "broken-reference.md" in broken_reference_result.stderr,
            "broken reference-style relative link did not fail with its path",
        )
        broken_reference.unlink()

        (temporary_root / "outside.md").write_text("private sibling\n", encoding="utf-8")
        escaping_link = repository / "escaping.md"
        escaping_link.write_text("[outside](../outside.md)\n", encoding="utf-8")
        escaping = run_checker(repository)
        require(
            escaping.returncode == 1 and "relative link leaves repository" in escaping.stderr,
            "repository-escaping link was accepted",
        )
        escaping_link.unlink()

        outside_text = temporary_root / "outside.txt"
        outside_text.write_text("private sibling\n", encoding="utf-8")
        (repository / "linked.txt").symlink_to(outside_text)
        linked = run_checker(repository)
        require(
            linked.returncode == 1 and "symbolic link is not allowed" in linked.stderr,
            "repository checker followed a symbolic link",
        )
        (repository / "linked.txt").unlink()

        lint = repository / "scripts/checks/lint.sh"
        shutil.copy2(LINT, lint)
        outside_shell = temporary_root / "outside.sh"
        outside_shell.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        (repository / "linked.sh").symlink_to(outside_shell)
        lint_result = subprocess.run(
            ["bash", "scripts/checks/lint.sh"],
            cwd=repository,
            capture_output=True,
            text=True,
            check=False,
        )
        require(
            lint_result.returncode != 0 and "symbolic link is not allowed" in lint_result.stderr,
            "lint accepted a symbolic-link source file",
        )
        (repository / "linked.sh").unlink()

        checker.unlink()
        checker_marker = temporary_root / "checker-executed"
        outside_checker = temporary_root / "outside-checker.py"
        outside_checker.write_text(
            f"from pathlib import Path\nPath({str(checker_marker)!r}).touch()\n",
            encoding="utf-8",
        )
        checker.symlink_to(outside_checker)
        lint_checker_result = subprocess.run(
            ["bash", "scripts/checks/lint.sh"],
            cwd=repository,
            capture_output=True,
            text=True,
            check=False,
        )
        require(
            lint_checker_result.returncode != 0 and not checker_marker.exists(),
            "lint executed a symlinked repository checker before validating it",
        )

        fixture_repository = temporary_root / "fixture-repository"
        fixture_repository.mkdir()
        subprocess.run(["git", "init", "-q", fixture_repository], check=True)
        fixture_script = fixture_repository / "scripts/checks/fixtures.sh"
        fixture_script.parent.mkdir(parents=True)
        shutil.copy2(FIXTURES, fixture_script)
        marker = temporary_root / "runner-executed"
        outside_runner = temporary_root / "outside-runner.sh"
        outside_runner.write_text(
            f"#!/usr/bin/env bash\nprintf ran >{marker}\n",
            encoding="utf-8",
        )
        for runner_name in FIXTURE_RUNNERS:
            runner = fixture_repository / runner_name
            runner.parent.mkdir(parents=True, exist_ok=True)
            if runner_name == FIXTURE_RUNNERS[0]:
                runner.symlink_to(outside_runner)
            elif runner.suffix == ".sh":
                runner.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
            else:
                runner.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        fixture_result = subprocess.run(
            ["bash", "scripts/checks/fixtures.sh"],
            cwd=fixture_repository,
            capture_output=True,
            text=True,
            check=False,
        )
        require(
            fixture_result.returncode != 0 and not marker.exists(),
            "fixture check executed a symbolic-link runner",
        )

    print("PASS: repository checks reject malformed content, unsafe links, and symlinked inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
