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
    "tests/managing-issues/fixtures/run-policy-checks.py",
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
        (repository / "README.md").write_text("[target](target.md)\n", encoding="utf-8")
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

        broken_link = repository / "broken.md"
        broken_link.write_text("[missing](missing.md)\n", encoding="utf-8")
        broken = run_checker(repository)
        require(
            broken.returncode == 1 and "broken.md" in broken.stderr,
            "broken relative link did not fail with its path",
        )
        broken_link.unlink()

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
