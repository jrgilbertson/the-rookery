#!/usr/bin/env python3
"""Check the shapes of a skill's eval files against references/skills.md.

Usage: check-evals.py <skill-directory> [<skill-directory> ...]

For each skill directory (one holding SKILL.md), validates whichever of
evals/evals.json, evals/eval_queries.json, and evals/benchmarks/*.json exist,
so a skill without evals passes. Prints one "path: message" line per
violation. Writes nothing to disk.

Exit status: 0 when every file is valid, 1 on any violation, 2 on bad
invocation, a path without SKILL.md, or unreadable input.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Callable


BENCHMARK_NAME = re.compile(
    r"^\d{4}-\d{2}-\d{2}-[0-9a-f]{7,40}(?:-[a-z0-9]+(?:[.-][a-z0-9]+)*)?\.json$"
)
SUMMARY_METRICS = ("pass_rate", "time_seconds", "tokens")
REQUIRED_METADATA_TEXT = (
    "skill_name", "executor_model", "timestamp", "harness", "grader", "archive_ref"
)
BASELINE_ARMS = ("old_skill", "without_skill")


class Unreadable(Exception):
    """An input file could not be read or parsed as JSON."""


def reject_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant {value}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"), parse_constant=reject_constant
        )
    except (OSError, UnicodeDecodeError, ValueError) as error:
        raise Unreadable(f"{path}: cannot read JSON: {error}") from error


def is_text(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def reporter(path: Path, report: list[str]) -> Callable[[str], None]:
    def fail(message: str) -> None:
        report.append(f"{path}: {message}")

    return fail


def check_evals(skill: Path, path: Path, report: list[str]) -> None:
    fail = reporter(path, report)

    data = load_json(path)
    if not isinstance(data, dict):
        fail("must be a JSON object")
        return
    root = skill.resolve()
    if data.get("skill_name") != root.name:
        fail(f"skill_name {data.get('skill_name')!r} does not match directory {root.name!r}")
    evals = data.get("evals")
    if not isinstance(evals, list):
        fail("evals must be an array")
        return
    seen_ids: set[int] = set()
    for index, case in enumerate(evals):
        where = f"evals[{index}]"
        if not isinstance(case, dict):
            fail(f"{where}: must be an object")
            continue
        case_id = case.get("id")
        if not is_integer(case_id):
            fail(f"{where}.id: must be an integer")
        elif case_id in seen_ids:
            fail(f"{where}.id: duplicate id {case_id}")
        else:
            seen_ids.add(case_id)
        if not is_text(case.get("prompt")):
            fail(f"{where}.prompt: must be a non-empty string")
        if not isinstance(case.get("expected_output"), str):
            fail(f"{where}.expected_output: must be a string")
        if "files" in case:
            files = case["files"]
            if not isinstance(files, list):
                fail(f"{where}.files: must be an array of paths")
                files = []
            for file_index, entry in enumerate(files):
                file_where = f"{where}.files[{file_index}]"
                if not is_text(entry):
                    fail(f"{file_where}: must be a non-empty string")
                    continue
                target = (root / entry).resolve()
                if Path(entry).is_absolute() or not target.is_relative_to(root):
                    fail(f"{file_where}: {entry!r} leaves the skill directory")
                elif not target.exists():
                    fail(f"{file_where}: {entry!r} does not exist")
                elif not target.is_file():
                    fail(f"{file_where}: {entry!r} is not a file")
        assertions = case.get("assertions")
        if not isinstance(assertions, list):
            fail(f"{where}.assertions: must be an array of strings")
        else:
            if not assertions and case.get("regression_control") is True:
                fail(f"{where}.assertions: a regression control needs at least one assertion")
            for assertion_index, assertion in enumerate(assertions):
                if not is_text(assertion):
                    fail(f"{where}.assertions[{assertion_index}]: must be a non-empty string")
        if "provenance" in case and not isinstance(case["provenance"], str):
            fail(f"{where}.provenance: must be a string")
        if "regression_control" in case and not isinstance(case["regression_control"], bool):
            fail(f"{where}.regression_control: must be a boolean")


def check_queries(path: Path, report: list[str]) -> None:
    fail = reporter(path, report)

    data = load_json(path)
    if not isinstance(data, list):
        fail("must be a JSON array")
        return
    for index, query in enumerate(data):
        where = f"[{index}]"
        if not isinstance(query, dict):
            fail(f"{where}: must be an object")
            continue
        if not is_text(query.get("query")):
            fail(f"{where}.query: must be a non-empty string")
        if not isinstance(query.get("should_trigger"), bool):
            fail(f"{where}.should_trigger: must be a boolean")
        if "owner" in query and not is_text(query["owner"]):
            fail(f"{where}.owner: must be a non-empty string")


def check_benchmark(directory: str, path: Path, report: list[str]) -> None:
    fail = reporter(path, report)

    if not BENCHMARK_NAME.match(path.name):
        fail("file name must be <YYYY-MM-DD>-<short-rev>[-<target>].json")
    data = load_json(path)
    if not isinstance(data, dict):
        fail("must be a JSON object")
        return

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        fail("metadata: must be an object")
    else:
        for field in REQUIRED_METADATA_TEXT:
            if not is_text(metadata.get(field)):
                fail(f"metadata.{field}: must be a non-empty string")
        if is_text(metadata.get("skill_name")) and metadata["skill_name"] != directory:
            fail(f"metadata.skill_name {metadata['skill_name']!r} does not match directory {directory!r}")
        runs = metadata.get("runs_per_configuration")
        if not is_integer(runs) or runs < 1:
            fail("metadata.runs_per_configuration: must be a positive integer")

    summary = data.get("run_summary")
    if not isinstance(summary, dict):
        fail("run_summary: must be an object")
        return
    configurations = {name: value for name, value in summary.items() if name != "delta"}
    if not configurations:
        fail("run_summary: must contain at least one configuration")
    for name in configurations:
        if name != "with_skill" and name not in BASELINE_ARMS:
            fail(f"run_summary.{name}: unknown arm; use with_skill, old_skill, or without_skill")
    if configurations and "with_skill" not in configurations:
        fail("run_summary: must include with_skill")
    if all(arm in configurations for arm in BASELINE_ARMS):
        fail("run_summary: compare with_skill against one baseline, not both old_skill and without_skill")
    for name, configuration in configurations.items():
        where = f"run_summary.{name}"
        if not isinstance(configuration, dict):
            fail(f"{where}: must be an object")
            continue
        for metric in SUMMARY_METRICS:
            values = configuration.get(metric)
            if not isinstance(values, dict):
                fail(f"{where}.{metric}: must be an object with mean and stddev")
                continue
            for statistic in ("mean", "stddev"):
                if not is_number(values.get(statistic)):
                    fail(f"{where}.{metric}.{statistic}: must be a number")

    if len(configurations) < 2:
        if "delta" in summary:
            fail("run_summary.delta: needs at least two configurations to compare")
        return
    delta = summary.get("delta")
    if not isinstance(delta, dict):
        fail("run_summary.delta: must be an object when two or more configurations are compared")
        return
    for metric in SUMMARY_METRICS:
        if not is_number(delta.get(metric)):
            fail(f"run_summary.delta.{metric}: must be a number")


def check_skill(skill: Path, report: list[str]) -> None:
    evals_dir = skill / "evals"
    evals_file = evals_dir / "evals.json"
    queries_file = evals_dir / "eval_queries.json"
    if evals_file.is_file():
        check_evals(skill, evals_file, report)
    if queries_file.is_file():
        check_queries(queries_file, report)
    benchmarks = evals_dir / "benchmarks"
    if benchmarks.is_dir():
        directory = skill.resolve().name
        for benchmark in sorted(benchmarks.glob("*.json")):
            check_benchmark(directory, benchmark, report)


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: check-evals.py <skill-directory> [<skill-directory> ...]", file=sys.stderr)
        return 2
    report: list[str] = []
    unreadable = False
    for raw in argv:
        skill = Path(raw)
        if not (skill / "SKILL.md").is_file():
            print(f"{raw}: not a skill directory (no SKILL.md)", file=sys.stderr)
            unreadable = True
            continue
        try:
            check_skill(skill, report)
        except Unreadable as error:
            print(error, file=sys.stderr)
            unreadable = True
    for line in report:
        print(line)
    if unreadable:
        return 2
    return 1 if report else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
