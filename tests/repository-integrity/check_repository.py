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

    print("PASS: repository checker accepts large JSON integers and rejects malformed JSON or unsafe links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
