#!/usr/bin/env python3
"""Run offline check-fixtures.mjs checks for Promptfoo Skill Eval suites."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REQUIRED_SUITES = (
    "evals/_template/check-fixtures.mjs",
    "evals/active-learning/check-fixtures.mjs",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def discover_check_scripts() -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            "evals/*/check-fixtures.mjs",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    scripts: list[Path] = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(os.fsdecode(raw_path))
        if len(relative.parts) != 3:
            continue
        candidate = ROOT / relative
        if not candidate.exists() and not candidate.is_symlink():
            continue
        current = ROOT
        for part in relative.parts:
            current /= part
            if current.is_symlink():
                raise AssertionError(
                    f"eval checks: symbolic link is not allowed: {relative.as_posix()}"
                )
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(ROOT)
        require(
            resolved.is_file(),
            f"eval checks: not a regular file: {relative.as_posix()}",
        )
        scripts.append(relative)
    scripts.sort()
    return scripts


def run_node_check(script_path: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["node", str(script_path)],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def verify_mutations_fail(suite_dir: Path) -> None:
    """Confirm check-fixtures.mjs fails when key template invariants break."""
    suite_name = suite_dir.name
    mutations: list[tuple[str, str, str, str]] = [
        (
            "auto-memory enabled",
            "promptfooconfig.cjs",
            "autoMemoryEnabled: false",
            "autoMemoryEnabled: true",
        ),
        (
            "auto-memory env removed",
            "promptfooconfig.cjs",
            "CLAUDE_CODE_DISABLE_AUTO_MEMORY: '1',",
            "",
        ),
        (
            "Bash added to tools",
            "promptfooconfig.cjs",
            "tools: [...readTools, 'Write', 'Edit'],",
            "tools: [...readTools, 'Write', 'Edit', 'Bash'],",
        ),
        (
            "NotebookEdit added to allowed tools",
            "promptfooconfig.cjs",
            "const readTools = ['Read', 'Glob', 'Grep', 'Skill'",
            "const readTools = ['Read', 'Glob', 'Grep', 'Skill', 'NotebookEdit'",
        ),
        (
            "timeout disabled",
            "promptfooconfig.cjs",
            "timeoutMs: 300000,",
            "timeoutMs: 0,",
        ),
        (
            "apiKeyRequired flipped",
            "promptfooconfig.cjs",
            "apiKeyRequired: false,",
            "apiKeyRequired: true,",
        ),
        (
            "permission_mode weakened",
            "promptfooconfig.cjs",
            "permission_mode: 'dontAsk',",
            "permission_mode: 'default',",
        ),
        (
            "write-tool check weakened",
            "checks.mjs",
            "return Array.isArray(allowed) && Array.isArray(calls)\n"
            "    && calls.every((call) => typeof call?.name === 'string' && allowed.includes(call.name));",
            "return true;",
        ),
        (
            "prepare.sh uses npm install",
            "prepare.sh",
            "ci --no-audit --no-fund",
            "install --no-audit --no-fund",
        ),
        (
            "run.sh exposes real HOME via run_home",
            "run.sh",
            'run_home="$work/home"',
            'run_home="$HOME"',
        ),
        (
            "run.sh exposes real CLAUDE_CONFIG_DIR via claude_home",
            "run.sh",
            'claude_home="$work/claude-home"',
            'claude_home="$HOME/.claude"',
        ),
    ]

    with tempfile.TemporaryDirectory(prefix=f"rookery-eval-check-{suite_name}-") as tmp:
        tmp_root = Path(tmp)
        for label, rel_file, old, new in mutations:
            copy_dir = tmp_root / label.replace(" ", "-")
            shutil.copytree(suite_dir, copy_dir)
            target = copy_dir / rel_file
            original = target.read_text(encoding="utf-8")
            require(
                old in original,
                f"{suite_name}: expected pattern missing in {rel_file} for mutation {label!r}",
            )
            target.write_text(original.replace(old, new, 1), encoding="utf-8")
            result = run_node_check(copy_dir / "check-fixtures.mjs", cwd=copy_dir)
            require(
                result.returncode != 0,
                f"{suite_name}: check-fixtures.mjs unexpectedly passed after breaking {label!r}",
            )

        missing_lock_dir = tmp_root / "missing-lockfile"
        shutil.copytree(suite_dir, missing_lock_dir)
        (missing_lock_dir / "package-lock.json").unlink()
        missing_lock = run_node_check(
            missing_lock_dir / "check-fixtures.mjs", cwd=missing_lock_dir
        )
        require(
            missing_lock.returncode != 0,
            f"{suite_name}: check-fixtures.mjs unexpectedly passed without package-lock.json",
        )


def main() -> int:
    node = shutil.which("node")
    require(node is not None, "eval checks: required tool 'node' is not installed")

    scripts = discover_check_scripts()
    discovered_names = {path.as_posix() for path in scripts}
    for required in REQUIRED_SUITES:
        require(
            required in discovered_names,
            f"eval checks: required suite check missing: {required}",
        )

    for relative in scripts:
        result = run_node_check(ROOT / relative, cwd=ROOT)
        if result.returncode != 0:
            sys.stderr.write(f"eval checks: {relative.as_posix()} failed\n")
            if result.stdout:
                sys.stderr.write(result.stdout)
            if result.stderr:
                sys.stderr.write(result.stderr)
            return 1
        print(f"eval checks: {relative.as_posix()} passed")

    for required in REQUIRED_SUITES:
        verify_mutations_fail((ROOT / required).parent)

    print(
        f"PASS: {len(scripts)} Skill Eval suite check(s) and negative mutation checks passed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
