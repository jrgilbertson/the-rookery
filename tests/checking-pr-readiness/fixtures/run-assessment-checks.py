#!/usr/bin/env python3
"""Exercise same-session exact-head assessment facts in disposable Git repos."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
SURFACE = REPO_ROOT / "skills" / "checking-pr-readiness" / "scripts" / "surface-report.sh"
OID = re.compile(r"^[0-9a-f]{40,64}$")
COMMIT_TIME = "2026-01-02T00:00:00+00:00"
ACCEPTED_CHECK_RESULTS = {"verified", "not applicable"}
CALLER_AUTHORIZED_ARGV = (("checks/fixture-quality.sh",),)
BASE_REF = "refs/heads/main"
NONDEFAULT_BASE_REF = "refs/heads/assessment-target"
FAIL_CLOSED_CHECK_RESULTS = (
    "failed",
    "unavailable",
    "not verified",
    "not run",
    "skipped",
    "bypassed",
    "attested",
)
RETIRED_MACHINERY = {
    "versioned readiness schema": re.compile(r"checking-pr-readiness-[a-z-]+/v1"),
    "receipt identity": re.compile(r"\breceipt_id\b"),
    "receipt reference": re.compile(r"\breceipt_references\b"),
    "receipt bundle": re.compile(r"\breceipt bundle\b"),
    "receipt artifact": re.compile(r"\bassessment-receipts\.json\b"),
    "capability version": re.compile(r"\bcapability_version\b"),
    "JSON schema field": re.compile(r'"schema"\s*:'),
}
FROZEN_RETIRED_ASSESSMENT = """
checking-pr-readiness-gates-evidence/v1
checking-pr-readiness-testing-result/v1
checking-pr-readiness-receipt-bundle/v1
receipt_id
receipt_references
receipt bundle
assessment-receipts.json
capability_version
"schema": "checking-pr-readiness-receipt-bundle/v1"
"""


class FixtureError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FixtureError(message)


def run(*command: str, cwd: Path, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def git_env(timestamp: str = COMMIT_TIME) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": "Synthetic Fixture",
            "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Synthetic Fixture",
            "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            "GIT_AUTHOR_DATE": timestamp,
            "GIT_COMMITTER_DATE": timestamp,
            "LC_ALL": "C",
        }
    )
    return env


def full_head(repo: Path) -> str:
    head = run("git", "rev-parse", "--verify", "HEAD^{commit}", cwd=repo)
    require(bool(OID.fullmatch(head)), f"Git did not return a full commit OID: {head!r}")
    return head


def full_base_oid(repo: Path, base_ref: str) -> str:
    base_oid = run("git", "rev-parse", "--verify", f"{base_ref}^{{commit}}", cwd=repo)
    require(bool(OID.fullmatch(base_oid)), f"Git did not return a full base OID: {base_oid!r}")
    return base_oid


def base_selector(base_ref: str) -> str:
    for prefix in ("refs/remotes/origin/", "refs/heads/"):
        if base_ref.startswith(prefix):
            selector = base_ref.removeprefix(prefix)
            require(selector, f"captured base ref has no branch selector: {base_ref!r}")
            return selector
    raise FixtureError(f"captured base ref is not a supported branch namespace: {base_ref!r}")


def current_subject(repo: Path) -> str | None:
    completed = subprocess.run(
        ("git", "symbolic-ref", "-q", "HEAD"),
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    require(completed.returncode in {0, 1}, f"Git could not read the current subject: {completed.stderr!r}")
    if completed.returncode == 1:
        return None
    subject = completed.stdout.strip()
    require(subject.startswith("refs/heads/"), f"Git did not return a branch subject: {subject!r}")
    return subject


def read_provider_head(repo: Path, remote: str, subject: str) -> str | None:
    completed = subprocess.run(
        ("git", "ls-remote", "--exit-code", remote, subject),
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    require(completed.returncode in {0, 2}, f"provider ref read failed: {completed.stderr!r}")
    if completed.returncode == 2:
        return None
    fields = completed.stdout.strip().split("\t")
    require(len(fields) == 2 and fields[1] == subject, f"provider ref read was ambiguous: {completed.stdout!r}")
    require(bool(OID.fullmatch(fields[0])), f"provider ref did not return a full OID: {fields[0]!r}")
    return fields[0]


def push_captured_oid(repo: Path, remote: str, subject: str, captured_head: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (
            "git",
            "push",
            "--porcelain",
            f"--force-with-lease={subject}:",
            remote,
            f"{captured_head}:{subject}",
        ),
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )


def build_repository(repo: Path, *, include_unassigned_check: bool = False) -> str:
    repo.mkdir()
    run("git", "init", "-q", cwd=repo)
    (repo / "README.md").write_text("fixture base\n", encoding="utf-8")
    run("git", "add", "README.md", cwd=repo)
    run("git", "commit", "-q", "-m", "fixture base", cwd=repo, env=git_env())
    run("git", "branch", "-M", "main", cwd=repo)
    run("git", "checkout", "-q", "-b", "assessment-subject", cwd=repo)

    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / ".github" / "workflows" / "quality.yml").write_text(
        "name: fixture-quality\non: [push]\n",
        encoding="utf-8",
    )
    (repo / "checks").mkdir()
    check = repo / "checks" / "fixture-quality.sh"
    check.write_text("#!/bin/sh\nprintf 'fixture-quality: verified\\n'\n", encoding="utf-8")
    check.chmod(0o755)
    if include_unassigned_check:
        unassigned = repo / "checks" / "unassigned.sh"
        unassigned.write_text(
            "#!/bin/sh\nprintf 'unassigned executed\\n' > unassigned-executed.txt\nprintf 'unassigned: verified\\n'\n",
            encoding="utf-8",
        )
        unassigned.chmod(0o755)
    (repo / "CHANGELOG.md").write_text("# Fixture changelog\n", encoding="utf-8")
    (repo / "src").mkdir()
    (repo / "src" / "app.txt").write_text("ready\n", encoding="utf-8")
    run("git", "add", ".", cwd=repo)
    run(
        "git",
        "commit",
        "-q",
        "-m",
        "fixture assessment subject",
        cwd=repo,
        env=git_env("2026-01-02T00:01:00+00:00"),
    )
    return full_head(repo)


def build_nondefault_target_repository(repo: Path) -> str:
    build_repository(repo)
    run("git", "branch", base_selector(NONDEFAULT_BASE_REF), "main", cwd=repo)
    run("git", "checkout", "-q", "main", cwd=repo)
    (repo / "src").mkdir()
    (repo / "src" / "inherited-from-default.txt").write_text("inherited\n", encoding="utf-8")
    run("git", "add", "src/inherited-from-default.txt", cwd=repo)
    run(
        "git",
        "commit",
        "-q",
        "-m",
        "advance default branch",
        cwd=repo,
        env=git_env("2026-01-02T00:01:30+00:00"),
    )
    run("git", "checkout", "-q", "assessment-subject", cwd=repo)
    run("git", "rebase", "-q", "main", cwd=repo, env=git_env("2026-01-02T00:02:00+00:00"))
    return full_head(repo)


def listed_paths(report: str, category: str) -> set[str]:
    lines = report.splitlines()
    header = next((index for index, line in enumerate(lines) if line.startswith(f"{category}: ")), None)
    require(header is not None, f"surface report omitted {category} inventory")
    paths: set[str] = set()
    for line in lines[header + 1 :]:
        if re.match(r"^(committed|staged|unstaged|untracked): ", line):
            break
        if line.startswith("  "):
            paths.add(line[2:])
    return paths


def discover_relevant_checks(repo: Path) -> dict[str, tuple[str, ...]]:
    checks = {
        path.stem: (path.relative_to(repo).as_posix(),)
        for path in sorted((repo / "checks").glob("*.sh"))
    }
    require(checks, "repository check discovery found no relevant checks")
    return checks


def run_assigned_checks(
    repo: Path,
    discovered_checks: dict[str, tuple[str, ...]],
    caller_authorized_argv: tuple[tuple[str, ...], ...],
) -> dict[str, str]:
    results: dict[str, str] = {}
    for argv in caller_authorized_argv:
        check = next((name for name, discovered_argv in discovered_checks.items() if argv == discovered_argv), None)
        require(check is not None, f"caller-authorized argv is not a discovered repository check: {argv!r}")
        output = run(*argv, cwd=repo)
        name, separator, result = output.partition(": ")
        require(separator and name == check and result, f"assigned check result was malformed: {output!r}")
        results[check] = result
    return results


def report_check_results(discovered_checks: dict[str, tuple[str, ...]], executed_checks: dict[str, str]) -> dict[str, str]:
    return {check: executed_checks.get(check, "not verified") for check in discovered_checks}


def assessment_decision(
    *,
    captured_subject: str,
    current_subject: str | None,
    captured_head: str,
    current_head: str,
    captured_base_ref: str,
    current_base_ref: str,
    captured_base_oid: str,
    current_base_oid: str,
    expected_paths: set[str],
    inspected_paths: set[str],
    expected_checks: set[str],
    check_results: dict[str, str],
    dirty_paths: dict[str, set[str]],
    deferred_sweep_gates: dict[str, str] | None = None,
) -> tuple[str, tuple[str, ...]]:
    gaps: list[str] = []
    if captured_subject != current_subject:
        current_label = current_subject if current_subject is not None else "detached HEAD"
        gaps.append(f"subject moved: {captured_subject} -> {current_label}")
    if captured_head != current_head:
        gaps.append(f"head moved: {captured_head} -> {current_head}")
    if (captured_base_ref, captured_base_oid) != (current_base_ref, current_base_oid):
        gaps.append(
            "base moved: "
            f"{captured_base_ref}@{captured_base_oid} -> {current_base_ref}@{current_base_oid}"
        )
    if inspected_paths != expected_paths:
        missing = sorted(expected_paths - inspected_paths)
        unexpected = sorted(inspected_paths - expected_paths)
        gaps.append(f"inspected-path inventory mismatch: missing {missing}; unexpected {unexpected}")
    if set(check_results) != expected_checks:
        missing = sorted(expected_checks - set(check_results))
        unexpected = sorted(set(check_results) - expected_checks)
        gaps.append(f"relevant-check inventory mismatch: missing {missing}; unexpected {unexpected}")
    for check, result in sorted(check_results.items()):
        if result == "skipped" and deferred_sweep_gates is not None:
            equivalent_gate = deferred_sweep_gates.get(check)
            if equivalent_gate and check_results.get(equivalent_gate) == "verified":
                result = "verified"
        if result not in ACCEPTED_CHECK_RESULTS:
            gaps.append(f"{check}: {result}")
    surface: list[str] = []
    for category in ("staged", "unstaged", "untracked"):
        for path in sorted(dirty_paths.get(category, set())):
            surface.append(f"{category} dirty path: {path}")
    # Dirt is gather surface that ships on later option 1. It does not omit Approve.
    # Identity, inventory, and check gaps omit Approve. Publication helpers below
    # still return ready/action-required; those tokens are not the skill product.
    decision = "omit-Approve" if gaps else "offer-option-1"
    return (decision, tuple(gaps + surface))


def local_publication_gaps(
    *,
    captured_subject: str,
    current_subject: str | None,
    captured_head: str,
    current_head: str,
    captured_base_ref: str,
    current_base_ref: str,
    captured_base_oid: str,
    current_base_oid: str,
    dirty_paths: dict[str, set[str]],
) -> list[str]:
    gaps: list[str] = []
    if captured_subject != current_subject:
        current_label = current_subject if current_subject is not None else "detached HEAD"
        gaps.append(f"subject moved: {captured_subject} -> {current_label}")
    if captured_head != current_head:
        gaps.append(f"head moved: {captured_head} -> {current_head}")
    if (captured_base_ref, captured_base_oid) != (current_base_ref, current_base_oid):
        gaps.append(
            "base moved: "
            f"{captured_base_ref}@{captured_base_oid} -> {current_base_ref}@{current_base_oid}"
        )
    for category in ("staged", "unstaged", "untracked"):
        for path in sorted(dirty_paths.get(category, set())):
            gaps.append(f"{category} dirty path: {path}")
    return gaps


def ownerless_first_push_decision(
    *,
    captured_subject: str,
    current_subject: str | None,
    captured_head: str,
    current_head: str,
    captured_base_ref: str,
    current_base_ref: str,
    captured_base_oid: str,
    current_base_oid: str,
    dirty_paths: dict[str, set[str]],
    provider_readable: bool,
    provider_head: str | None,
) -> tuple[str, tuple[str, ...]]:
    publication_gaps = local_publication_gaps(
        captured_subject=captured_subject,
        current_subject=current_subject,
        captured_head=captured_head,
        current_head=current_head,
        captured_base_ref=captured_base_ref,
        current_base_ref=current_base_ref,
        captured_base_oid=captured_base_oid,
        current_base_oid=current_base_oid,
        dirty_paths=dirty_paths,
    )
    if not provider_readable:
        publication_gaps.append("provider ref is unavailable or indeterminate")
    elif provider_head is not None and provider_head != captured_head:
        publication_gaps.append(f"provider ref conflicts: {provider_head} != {captured_head}")
    return ("ready" if not publication_gaps else "action-required", tuple(publication_gaps))


def pre_pr_decision(
    *,
    captured_subject: str,
    current_subject: str | None,
    captured_head: str,
    current_head: str,
    captured_base_ref: str,
    current_base_ref: str,
    captured_base_oid: str,
    current_base_oid: str,
    dirty_paths: dict[str, set[str]],
    provider_readable: bool,
    provider_head: str | None,
) -> tuple[str, tuple[str, ...]]:
    publication_gaps = local_publication_gaps(
        captured_subject=captured_subject,
        current_subject=current_subject,
        captured_head=captured_head,
        current_head=current_head,
        captured_base_ref=captured_base_ref,
        current_base_ref=current_base_ref,
        captured_base_oid=captured_base_oid,
        current_base_oid=current_base_oid,
        dirty_paths=dirty_paths,
    )
    if not provider_readable:
        publication_gaps.append("provider ref is unavailable or indeterminate")
    elif provider_head != captured_head:
        publication_gaps.append(f"provider ref does not equal captured OID: {provider_head} != {captured_head}")
    return ("ready" if not publication_gaps else "action-required", tuple(publication_gaps))


def inspect_stable_session(
    repo: Path,
    caller_authorized_argv: tuple[tuple[str, ...], ...],
    base_ref: str = BASE_REF,
) -> tuple[str, str, str, str, set[str], dict[str, str]]:
    subject = current_subject(repo)
    require(subject is not None, "fixture checkout is detached")
    captured = full_head(repo)
    captured_base_ref = base_ref
    captured_base_selector = base_selector(captured_base_ref)
    base_oid = full_base_oid(repo, captured_base_ref)
    require(not run("git", "status", "--porcelain", cwd=repo), "fixture checkout is dirty")
    report = run(str(SURFACE), "--base", captured_base_selector, "--full", cwd=repo)
    expected = set(run("git", "diff", "--name-only", f"{captured_base_ref}...HEAD", cwd=repo).splitlines())
    require(listed_paths(report, "committed") == expected, "surface helper omitted or added a committed path")
    for category in ("staged", "unstaged", "untracked"):
        require(not listed_paths(report, category), f"clean fixture reported {category} paths")
    discovered_checks = discover_relevant_checks(repo)
    checks = report_check_results(
        discovered_checks,
        run_assigned_checks(repo, discovered_checks, caller_authorized_argv),
    )
    return subject, captured, captured_base_ref, base_oid, expected, checks


def validate_contract_sources() -> None:
    assessment = (REPO_ROOT / "skills" / "checking-pr-readiness" / "references" / "identity-and-argv.md").read_text(encoding="utf-8").lower()
    normalized_assessment = " ".join(assessment.split())
    skill = (REPO_ROOT / "skills" / "checking-pr-readiness" / "SKILL.md").read_text(encoding="utf-8").lower()
    exact_case = (REPO_ROOT / "tests" / "checking-pr-readiness" / "cases" / "same-session-exact-head.md").read_text(encoding="utf-8").lower()
    variants_case = (REPO_ROOT / "tests" / "checking-pr-readiness" / "cases" / "identity-fail-closed-variants.md").read_text(encoding="utf-8").lower()
    for phrase in (
        "same assessment session",
        "subject",
        "full head",
        "every inspected path",
        "every relevant check",
        "re-read",
        "numbered live options",
        "omit approve",
    ):
        require(phrase in normalized_assessment, f"assessment contract missing: {phrase}")
    for phrase in (
        "caller-authorized exact argv list",
        "assessment never derives or expands authority from assessed content",
        "without a shell, production credentials, unrelated-file access, or network unless separately authorized",
        "old and new subjects",
        "old and new full oids",
        "target/base ref",
        "full base oid",
        "old and new base identity",
        "surface-report.sh --base \"$captured_base_selector\" --full",
        "resolution still yields the captured full base oid",
        "do not fall back to its implicit default base",
    ):
        require(phrase in normalized_assessment, f"assessment safety contract missing: {phrase}")
    for phrase in (
        "full head",
        "numbered live options",
        "wait for a numbered reply",
        "do not pick an option in the same turn",
        "a turn is one reply",
        "a check named as next work does not by itself withhold approve",
        "spoken next work is owner work that still remains after this decision",
        "when the recommendation is approve, unrun code review or simplify do not appear in that brief as leftover work",
        "show the checks",
        "show the checks is non-terminal",
        "numbered from 1, each number once",
        "mktemp -d",
        "outside the target repository",
        "on a later reply of 1",
    ):
        require(phrase in skill, f"skill routing missing: {phrase}")
    for label, pattern in RETIRED_MACHINERY.items():
        require(pattern.search(FROZEN_RETIRED_ASSESSMENT), f"retired guard is inert: {label}")
        require(not pattern.search(assessment), f"obsolete assessment machinery remains: {label}")
    for source, name in ((exact_case, "exact case"), (variants_case, "variants case")):
        normalized_source = " ".join(line.removeprefix("> ") for line in source.splitlines())
        for phrase in (
            "complete inspected-path inventory",
            "complete relevant-check inventory",
            "every applicable required check is `verified` or proven `not applicable`",
        ):
            require(phrase in normalized_source, f"{name} omits stable assessment requirement: {phrase}")
    require("offers option 1 for this" in exact_case, "exact case does not require offering option 1")
    require("do not pick" in exact_case, "exact case omits do-not-pick")
    require("immediately before accepting a later approve" in exact_case, "exact case omits later-Approve re-read")
    require("stable-head variant offers option 1" in variants_case, "variants case does not require stable option 1")
    require("re-reads immediately before accepting a later 1" in variants_case, "variants case pins offer-time re-read")
    require("picks an option in the same turn" in variants_case, "variants case omits do-not-pick")
    for phrase in (
        "moved-head variant omits approve",
        "moved-base variant omits approve",
        "branch-rename variant omits approve",
        "detached-head variant omits approve",
        "dirty-surface variants name every",
        "inventories omit approve",
    ):
        require(phrase in variants_case, f"variants case does not preserve fail-closed result: {phrase}")
    for phrase in (
        "exact named equivalent repository gate",
        "present and `verified` in the same complete assessment session",
        "bare, missing, unrelated, mismatched, unavailable, or not verified gate",
    ):
        require(phrase in normalized_assessment, f"assessment contract omits deferred-gate safety: {phrase}")
    for source, name in (
        ((REPO_ROOT / "skills" / "repo-gardener" / "SKILL.md").read_text(encoding="utf-8").lower(), "repo-gardener skill"),
        ((REPO_ROOT / "skills" / "repo-gardener" / "references" / "reconciliation.md").read_text(encoding="utf-8").lower(), "reconciliation reference"),
    ):
        normalized_source = " ".join(source.split())
        require("compare them to the captured subject and oid that received `ready`" in normalized_source, f"{name} can rebind the ready identity")
        require("never replace or recapture that authorized identity" in normalized_source, f"{name} can replace the ready identity")
        require("exact caller-approved verification command argv list" in normalized_source, f"{name} omits the caller-owned argv assignment")
        require("same assignment-owned exact argv list" in normalized_source, f"{name} omits the argv handoff to assessment")
        require("target/base ref" in normalized_source and "full base oid" in normalized_source, f"{name} omits the base binding")
        require(
            "immediately before an ownerless first push, re-resolve the captured target/base ref and full base oid"
            in normalized_source,
            f"{name} omits the pre-push base re-read",
        )
        require(
            "immediately before pr-open, re-resolve the captured target/base ref and full base oid" in normalized_source,
            f"{name} omits the pre-PR base re-read",
        )
        require(
            "persistent state, configuration, schema, receipt, ledger, or audit-command reuse" not in normalized_source,
            f"{name} retains unnecessary assignment denial prose",
        )
    for source, name in (
        (assessment, "assessment contract"),
        ((REPO_ROOT / "skills" / "repo-gardener" / "references" / "reconciliation.md").read_text(encoding="utf-8").lower(), "reconciliation reference"),
    ):
        require("not verified" in source and "not run" in source, f"{name} omits canonical check statuses")
        require("unverified" not in source and "not-run" not in source, f"{name} retains noncanonical check statuses")
    require(
        "an unresolved finding is named as next work attached to an allowed status, for example `code review: not verified`."
        in normalized_assessment,
        "assessment contract does not distinguish unresolved findings from check statuses",
    )
    require("unresolved" not in FAIL_CLOSED_CHECK_RESULTS, "unresolved remains a canonical check status")


def run_suite() -> None:
    validate_contract_sources()
    with tempfile.TemporaryDirectory(prefix="pr-readiness-assessment-") as temporary:
        stable_repo = Path(temporary) / "stable"
        stable_head = build_repository(stable_repo)
        captured_subject, captured, captured_base_ref, captured_base_oid, paths, check_results = inspect_stable_session(
            stable_repo,
            CALLER_AUTHORIZED_ARGV,
        )
        require(captured == stable_head == full_head(stable_repo), "stable native head changed during assessment")
        require(
            paths == {".github/workflows/quality.yml", "CHANGELOG.md", "checks/fixture-quality.sh", "src/app.txt"},
            "fixture surface changed unexpectedly",
        )
        require(check_results == {"fixture-quality": "verified"}, "fixture repository check did not verify")
        stable_arguments = {
            "captured_subject": captured_subject,
            "current_subject": current_subject(stable_repo),
            "captured_head": captured,
            "current_head": full_head(stable_repo),
            "captured_base_ref": captured_base_ref,
            "current_base_ref": captured_base_ref,
            "captured_base_oid": captured_base_oid,
            "current_base_oid": full_base_oid(stable_repo, captured_base_ref),
            "expected_paths": paths,
            "inspected_paths": paths,
            "dirty_paths": {},
        }
        for label, deferred_results, deferred_sweep_gates, expected_checks, expected_decision, expected_gap in (
            (
                "stable deterministic slice",
                check_results,
                None,
                set(check_results),
                "omit-Approve",
                "steps 3-6 judgment checks: not run",
            ),
            (
                "exact verified deferred gate",
                {
                    "fixture-quality": "verified",
                    "changelog": "skipped",
                    "ci-changelog": "verified",
                },
                {"changelog": "ci-changelog"},
                {"fixture-quality", "changelog", "ci-changelog"},
                "omit-Approve",
                "steps 3-6 judgment checks: not run",
            ),
            (
                "missing named gate",
                {"fixture-quality": "verified", "changelog": "skipped"},
                {"changelog": "ci-changelog"},
                {"fixture-quality", "changelog"},
                "omit-Approve",
                "changelog: skipped",
            ),
            (
                "mismatched gate",
                {
                    "fixture-quality": "verified",
                    "changelog": "skipped",
                    "ci-size": "verified",
                },
                {"changelog": "ci-changelog"},
                {"fixture-quality", "changelog", "ci-size"},
                "omit-Approve",
                "changelog: skipped",
            ),
            (
                "failed named gate",
                {
                    "fixture-quality": "verified",
                    "changelog": "skipped",
                    "ci-changelog": "failed",
                },
                {"changelog": "ci-changelog"},
                {"fixture-quality", "changelog", "ci-changelog"},
                "omit-Approve",
                "changelog: skipped",
            ),
            (
                "unavailable gate",
                {
                    "fixture-quality": "verified",
                    "changelog": "skipped",
                    "ci-changelog": "unavailable",
                },
                {"changelog": "ci-changelog"},
                {"fixture-quality", "changelog", "ci-changelog"},
                "omit-Approve",
                "changelog: skipped",
            ),
            (
                "unverified gate",
                {
                    "fixture-quality": "verified",
                    "changelog": "skipped",
                    "ci-changelog": "not verified",
                },
                {"changelog": "ci-changelog"},
                {"fixture-quality", "changelog", "ci-changelog"},
                "omit-Approve",
                "changelog: skipped",
            ),
            (
                "incomplete relevant-check inventory",
                {},
                None,
                {"fixture-quality"},
                "omit-Approve",
                "missing ['fixture-quality']",
            ),
            (
                "ordinary skipped check",
                {
                    "fixture-quality": "verified",
                    "ordinary-check": "skipped",
                    "ci-quality": "verified",
                },
                {"another-deferred-check": "ci-quality"},
                {"fixture-quality", "ordinary-check", "ci-quality"},
                "omit-Approve",
                "ordinary-check: skipped",
            ),
        ):
            deferred_results["steps 3-6 judgment checks"] = "not run"
            expected_checks.add("steps 3-6 judgment checks")
            decision, gaps = assessment_decision(
                **stable_arguments,
                expected_checks=expected_checks,
                check_results=deferred_results,
                deferred_sweep_gates=deferred_sweep_gates,
            )
            require(decision == expected_decision, f"{label} returned {decision} instead of {expected_decision}")
            if expected_gap is not None:
                require(any(expected_gap in gap for gap in gaps), f"{label} did not name its gap")
            if label == "exact verified deferred gate":
                require("changelog: skipped" not in gaps, "exact verified deferred gate did not normalize the skipped changelog")
        nondefault_target_repo = Path(temporary) / "nondefault-target"
        build_nondefault_target_repository(nondefault_target_repo)
        captured_nondefault_base_oid = full_base_oid(nondefault_target_repo, NONDEFAULT_BASE_REF)
        implicit_report = run(str(SURFACE), "--full", cwd=nondefault_target_repo)
        bound_report = run(
            str(SURFACE),
            "--base",
            base_selector(NONDEFAULT_BASE_REF),
            "--full",
            cwd=nondefault_target_repo,
        )
        implicit_paths = listed_paths(implicit_report, "committed")
        bound_paths = listed_paths(bound_report, "committed")
        expected_bound_paths = set(
            run("git", "diff", "--name-only", f"{NONDEFAULT_BASE_REF}...HEAD", cwd=nondefault_target_repo).splitlines()
        )
        inherited_default_path = "src/inherited-from-default.txt"
        require(
            inherited_default_path not in implicit_paths,
            "implicit default-base surface did not omit the inherited default path",
        )
        require(
            inherited_default_path in bound_paths,
            "captured non-default-base surface did not include the inherited default path",
        )
        require(bound_paths == expected_bound_paths, "captured-base surface inventory did not match the selected target")
        require(
            f"default branch: {NONDEFAULT_BASE_REF} (from --base)" in bound_report,
            "surface helper did not consume the captured non-default base selector",
        )
        require(
            full_base_oid(nondefault_target_repo, NONDEFAULT_BASE_REF) == captured_nondefault_base_oid,
            "captured non-default base OID changed during surface inspection",
        )

        unassigned_repo = Path(temporary) / "unassigned"
        build_repository(unassigned_repo, include_unassigned_check=True)
        unassigned_subject, unassigned_head, unassigned_base_ref, unassigned_base_oid, unassigned_paths, unassigned_results = inspect_stable_session(
            unassigned_repo,
            CALLER_AUTHORIZED_ARGV,
        )
        require(
            set(unassigned_results) == set(discover_relevant_checks(unassigned_repo)),
            "unassigned repository check was not independently discovered",
        )
        require(
            unassigned_results == {"fixture-quality": "verified", "unassigned": "not verified"},
            "discovered unassigned check was not reported as not verified",
        )
        require(
            not (unassigned_repo / "unassigned-executed.txt").exists(),
            "unassigned repository check executed outside the caller-authorized argv list",
        )
        decision, gaps = assessment_decision(
            captured_subject=unassigned_subject,
            current_subject=current_subject(unassigned_repo),
            captured_head=unassigned_head,
            current_head=full_head(unassigned_repo),
            captured_base_ref=unassigned_base_ref,
            current_base_ref=unassigned_base_ref,
            captured_base_oid=unassigned_base_oid,
            current_base_oid=full_base_oid(unassigned_repo, unassigned_base_ref),
            expected_paths=unassigned_paths,
            inspected_paths=unassigned_paths,
            expected_checks=set(unassigned_results),
            check_results=unassigned_results,
            dirty_paths={},
        )
        require(decision == "omit-Approve", "unassigned repository check did not fail closed")
        require("unassigned: not verified" in gaps, "unassigned repository check did not name its gap")

        moved_repo = Path(temporary) / "moved"
        build_repository(moved_repo)
        captured_subject, captured, captured_base_ref, captured_base_oid, paths, check_results = inspect_stable_session(
            moved_repo,
            CALLER_AUTHORIZED_ARGV,
        )
        (moved_repo / "src" / "app.txt").write_text("moved\n", encoding="utf-8")
        run("git", "add", "src/app.txt", cwd=moved_repo)
        run(
            "git",
            "commit",
            "-q",
            "-m",
            "advance native head",
            cwd=moved_repo,
            env=git_env("2026-01-02T00:02:00+00:00"),
        )
        head_b = full_head(moved_repo)
        decision, gaps = assessment_decision(
            captured_subject=captured_subject,
            current_subject=current_subject(moved_repo),
            captured_head=captured,
            current_head=head_b,
            captured_base_ref=captured_base_ref,
            current_base_ref=captured_base_ref,
            captured_base_oid=captured_base_oid,
            current_base_oid=full_base_oid(moved_repo, captured_base_ref),
            expected_paths=paths,
            inspected_paths=paths,
            expected_checks=set(check_results),
            check_results=check_results,
            dirty_paths={},
        )
        require(decision == "omit-Approve", "moved head did not return omit-Approve")
        require(f"head moved: {captured} -> {head_b}" in gaps, "moved head did not name both full OIDs")

        moved_base_repo = Path(temporary) / "moved-base"
        build_repository(moved_base_repo)
        captured_subject, captured, captured_base_ref, captured_base_oid, paths, check_results = inspect_stable_session(
            moved_base_repo,
            CALLER_AUTHORIZED_ARGV,
        )
        run("git", "checkout", "-q", "main", cwd=moved_base_repo)
        (moved_base_repo / "README.md").write_text("fixture base advanced\n", encoding="utf-8")
        run("git", "add", "README.md", cwd=moved_base_repo)
        run(
            "git",
            "commit",
            "-q",
            "-m",
            "advance fixture base",
            cwd=moved_base_repo,
            env=git_env("2026-01-02T00:02:00+00:00"),
        )
        run("git", "checkout", "-q", "assessment-subject", cwd=moved_base_repo)
        moved_base_oid = full_base_oid(moved_base_repo, captured_base_ref)
        require(current_subject(moved_base_repo) == captured_subject, "base movement changed the native subject")
        require(full_head(moved_base_repo) == captured, "base movement changed the native head")
        decision, gaps = assessment_decision(
            captured_subject=captured_subject,
            current_subject=current_subject(moved_base_repo),
            captured_head=captured,
            current_head=full_head(moved_base_repo),
            captured_base_ref=captured_base_ref,
            current_base_ref=captured_base_ref,
            captured_base_oid=captured_base_oid,
            current_base_oid=moved_base_oid,
            expected_paths=paths,
            inspected_paths=paths,
            expected_checks=set(check_results),
            check_results=check_results,
            dirty_paths={},
        )
        require(decision == "omit-Approve", "moved base did not return omit-Approve")
        require(
            f"base moved: {captured_base_ref}@{captured_base_oid} -> {captured_base_ref}@{moved_base_oid}" in gaps,
            "moved base did not name both base identities",
        )

        renamed_repo = Path(temporary) / "renamed"
        build_repository(renamed_repo)
        captured_subject, captured, captured_base_ref, captured_base_oid, paths, check_results = inspect_stable_session(
            renamed_repo,
            CALLER_AUTHORIZED_ARGV,
        )
        run("git", "branch", "-m", "assessment-renamed", cwd=renamed_repo)
        decision, gaps = assessment_decision(
            captured_subject=captured_subject,
            current_subject=current_subject(renamed_repo),
            captured_head=captured,
            current_head=full_head(renamed_repo),
            captured_base_ref=captured_base_ref,
            current_base_ref=captured_base_ref,
            captured_base_oid=captured_base_oid,
            current_base_oid=full_base_oid(renamed_repo, captured_base_ref),
            expected_paths=paths,
            inspected_paths=paths,
            expected_checks=set(check_results),
            check_results=check_results,
            dirty_paths={},
        )
        require(decision == "omit-Approve", "constant-OID branch rename did not return omit-Approve")
        require(
            f"subject moved: {captured_subject} -> refs/heads/assessment-renamed" in gaps,
            "branch rename did not name both subjects",
        )

        detached_repo = Path(temporary) / "detached"
        build_repository(detached_repo)
        captured_subject, captured, captured_base_ref, captured_base_oid, paths, check_results = inspect_stable_session(
            detached_repo,
            CALLER_AUTHORIZED_ARGV,
        )
        run("git", "checkout", "-q", "--detach", captured, cwd=detached_repo)
        decision, gaps = assessment_decision(
            captured_subject=captured_subject,
            current_subject=current_subject(detached_repo),
            captured_head=captured,
            current_head=full_head(detached_repo),
            captured_base_ref=captured_base_ref,
            current_base_ref=captured_base_ref,
            captured_base_oid=captured_base_oid,
            current_base_oid=full_base_oid(detached_repo, captured_base_ref),
            expected_paths=paths,
            inspected_paths=paths,
            expected_checks=set(check_results),
            check_results=check_results,
            dirty_paths={},
        )
        require(decision == "omit-Approve", "constant-OID detached HEAD did not return omit-Approve")
        require(
            f"subject moved: {captured_subject} -> detached HEAD" in gaps,
            "detached HEAD did not name the missing subject",
        )

        for category in ("staged", "unstaged", "untracked"):
            decision, gaps = assessment_decision(
                captured_subject=captured_subject,
                current_subject=captured_subject,
                captured_head=stable_head,
                current_head=stable_head,
                captured_base_ref=captured_base_ref,
                current_base_ref=captured_base_ref,
                captured_base_oid=captured_base_oid,
                current_base_oid=full_base_oid(detached_repo, captured_base_ref),
                expected_paths=paths,
                inspected_paths=paths,
                expected_checks=set(check_results),
                check_results=check_results,
                dirty_paths={category: {f"{category}.txt"}},
            )
            require(decision == "offer-option-1", f"{category} dirt omitted Approve")
            require(f"{category} dirty path: {category}.txt" in gaps, f"{category} dirt did not name its path")

        decision, gaps = assessment_decision(
            captured_subject=captured_subject,
            current_subject=captured_subject,
            captured_head=stable_head,
            current_head=stable_head,
            captured_base_ref=captured_base_ref,
            current_base_ref=captured_base_ref,
            captured_base_oid=captured_base_oid,
            current_base_oid=full_base_oid(detached_repo, captured_base_ref),
            expected_paths=paths,
            inspected_paths=paths - {"src/app.txt"},
            expected_checks=set(check_results),
            check_results=check_results,
            dirty_paths={},
        )
        require(decision == "omit-Approve", "incomplete inspected-path inventory did not fail closed")
        require("missing ['src/app.txt']" in gaps[0], "incomplete inspected-path inventory did not name its gap")

        for result in FAIL_CLOSED_CHECK_RESULTS:
            decision, gaps = assessment_decision(
                captured_subject=captured_subject,
                current_subject=captured_subject,
                captured_head=stable_head,
                current_head=stable_head,
                captured_base_ref=captured_base_ref,
                current_base_ref=captured_base_ref,
                captured_base_oid=captured_base_oid,
                current_base_oid=full_base_oid(detached_repo, captured_base_ref),
                expected_paths=paths,
                inspected_paths=paths,
                expected_checks=set(check_results),
                check_results={"fixture-quality": result},
                dirty_paths={},
            )
            require(decision == "omit-Approve", f"{result} check did not fail closed")
            require(f"fixture-quality: {result}" in gaps, f"{result} check did not name its gap")

        provider_subject = "refs/heads/assessment-provider"
        provider = Path(temporary) / "provider.git"
        run("git", "init", "-q", "--bare", str(provider), cwd=stable_repo)
        run("git", "remote", "add", "provider", str(provider), cwd=stable_repo)
        provider_head = read_provider_head(stable_repo, "provider", provider_subject)
        decision, gaps = ownerless_first_push_decision(
            captured_subject=provider_subject,
            current_subject=provider_subject,
            captured_head=stable_head,
            current_head=stable_head,
            captured_base_ref=captured_base_ref,
            current_base_ref=captured_base_ref,
            captured_base_oid=captured_base_oid,
            current_base_oid=captured_base_oid,
            dirty_paths={},
            provider_readable=True,
            provider_head=provider_head,
        )
        require(decision == "ready" and not gaps, "absent provider ref did not permit the first push")
        pushed = push_captured_oid(stable_repo, "provider", provider_subject, stable_head)
        require(pushed.returncode == 0, f"captured-OID first push failed: {pushed.stderr!r}")
        provider_head = read_provider_head(stable_repo, "provider", provider_subject)
        require(provider_head == stable_head, "first push did not create the exact captured provider ref")
        decision, gaps = pre_pr_decision(
            captured_subject=provider_subject,
            current_subject=provider_subject,
            captured_head=stable_head,
            current_head=stable_head,
            captured_base_ref=captured_base_ref,
            current_base_ref=captured_base_ref,
            captured_base_oid=captured_base_oid,
            current_base_oid=captured_base_oid,
            dirty_paths={},
            provider_readable=True,
            provider_head=provider_head,
        )
        require(decision == "ready" and not gaps, "post-push provider ref did not match the captured OID")
        decision, gaps = pre_pr_decision(
            captured_subject=provider_subject,
            current_subject=provider_subject,
            captured_head=stable_head,
            current_head=stable_head,
            captured_base_ref=captured_base_ref,
            current_base_ref=captured_base_ref,
            captured_base_oid=captured_base_oid,
            current_base_oid=captured_base_oid,
            dirty_paths={},
            provider_readable=True,
            provider_head=None,
        )
        require(decision == "action-required", "absent provider ref permitted PR creation")

        raced_provider = Path(temporary) / "raced-provider.git"
        run("git", "init", "-q", "--bare", str(raced_provider), cwd=stable_repo)
        run("git", "remote", "add", "raced-provider", str(raced_provider), cwd=stable_repo)
        require(
            read_provider_head(stable_repo, "raced-provider", provider_subject) is None,
            "race fixture provider ref was not initially absent",
        )
        base_head = run("git", "rev-parse", "HEAD^", cwd=stable_repo)
        seeded = subprocess.run(
            ("git", "push", "--porcelain", "raced-provider", f"{base_head}:{provider_subject}"),
            cwd=stable_repo,
            check=False,
            capture_output=True,
            text=True,
        )
        require(seeded.returncode == 0, f"race fixture could not create competing provider ref: {seeded.stderr!r}")
        raced_push = push_captured_oid(stable_repo, "raced-provider", provider_subject, stable_head)
        require(raced_push.returncode != 0, "absence lease allowed an intervening provider ref to fast-forward")
        require(
            read_provider_head(stable_repo, "raced-provider", provider_subject) == base_head,
            "failed absence lease changed the competing provider ref",
        )
        for label, overrides in (
            ("conflicting provider ref", {"provider_head": "0" * 40}),
            ("unavailable provider ref", {"provider_readable": False}),
            ("moved local subject", {"current_subject": "refs/heads/other"}),
            ("moved local OID", {"current_head": "1" * 40}),
            ("dirty local surface", {"dirty_paths": {"unstaged": {"changed.txt"}}}),
        ):
            values = {
                "captured_subject": provider_subject,
                "current_subject": provider_subject,
                "captured_head": stable_head,
                "current_head": stable_head,
                "captured_base_ref": captured_base_ref,
                "current_base_ref": captured_base_ref,
                "captured_base_oid": captured_base_oid,
                "current_base_oid": captured_base_oid,
                "dirty_paths": {},
                "provider_readable": True,
                "provider_head": stable_head,
            }
            values.update(overrides)
            decision, gaps = ownerless_first_push_decision(**values)
            require(decision == "action-required", f"{label} did not stop publication")

        pre_push_base_repo = Path(temporary) / "pre-push-base"
        build_repository(pre_push_base_repo)
        captured_subject, captured_head, captured_base_ref, captured_base_oid, _, _ = inspect_stable_session(
            pre_push_base_repo,
            CALLER_AUTHORIZED_ARGV,
        )
        pre_push_provider = Path(temporary) / "pre-push-provider.git"
        run("git", "init", "-q", "--bare", str(pre_push_provider), cwd=pre_push_base_repo)
        run("git", "remote", "add", "pre-push-provider", str(pre_push_provider), cwd=pre_push_base_repo)
        run("git", "checkout", "-q", "main", cwd=pre_push_base_repo)
        (pre_push_base_repo / "README.md").write_text("base advanced before push\n", encoding="utf-8")
        run("git", "add", "README.md", cwd=pre_push_base_repo)
        run(
            "git",
            "commit",
            "-q",
            "-m",
            "advance base before first push",
            cwd=pre_push_base_repo,
            env=git_env("2026-01-02T00:03:00+00:00"),
        )
        moved_base_oid = full_base_oid(pre_push_base_repo, captured_base_ref)
        run("git", "checkout", "-q", "assessment-subject", cwd=pre_push_base_repo)
        decision, gaps = ownerless_first_push_decision(
            captured_subject=captured_subject,
            current_subject=current_subject(pre_push_base_repo),
            captured_head=captured_head,
            current_head=full_head(pre_push_base_repo),
            captured_base_ref=captured_base_ref,
            current_base_ref=captured_base_ref,
            captured_base_oid=captured_base_oid,
            current_base_oid=moved_base_oid,
            dirty_paths={},
            provider_readable=True,
            provider_head=read_provider_head(pre_push_base_repo, "pre-push-provider", provider_subject),
        )
        require(decision == "action-required", "base movement before first push did not stop publication")
        require(
            f"base moved: {captured_base_ref}@{captured_base_oid} -> {captured_base_ref}@{moved_base_oid}" in gaps,
            "base movement before first push did not name old/new base identity",
        )

        post_push_base_repo = Path(temporary) / "post-push-base"
        build_repository(post_push_base_repo)
        captured_subject, captured_head, captured_base_ref, captured_base_oid, _, _ = inspect_stable_session(
            post_push_base_repo,
            CALLER_AUTHORIZED_ARGV,
        )
        post_push_provider = Path(temporary) / "post-push-provider.git"
        run("git", "init", "-q", "--bare", str(post_push_provider), cwd=post_push_base_repo)
        run("git", "remote", "add", "post-push-provider", str(post_push_provider), cwd=post_push_base_repo)
        require(
            push_captured_oid(post_push_base_repo, "post-push-provider", provider_subject, captured_head).returncode == 0,
            "post-push base fixture could not push the captured OID",
        )
        run("git", "checkout", "-q", "main", cwd=post_push_base_repo)
        (post_push_base_repo / "README.md").write_text("base advanced after push\n", encoding="utf-8")
        run("git", "add", "README.md", cwd=post_push_base_repo)
        run(
            "git",
            "commit",
            "-q",
            "-m",
            "advance base before PR open",
            cwd=post_push_base_repo,
            env=git_env("2026-01-02T00:04:00+00:00"),
        )
        moved_base_oid = full_base_oid(post_push_base_repo, captured_base_ref)
        run("git", "checkout", "-q", "assessment-subject", cwd=post_push_base_repo)
        decision, gaps = pre_pr_decision(
            captured_subject=captured_subject,
            current_subject=current_subject(post_push_base_repo),
            captured_head=captured_head,
            current_head=full_head(post_push_base_repo),
            captured_base_ref=captured_base_ref,
            current_base_ref=captured_base_ref,
            captured_base_oid=captured_base_oid,
            current_base_oid=moved_base_oid,
            dirty_paths={},
            provider_readable=True,
            provider_head=read_provider_head(post_push_base_repo, "post-push-provider", provider_subject),
        )
        require(decision == "action-required", "base movement before PR open did not stop publication")
        require(
            f"base moved: {captured_base_ref}@{captured_base_oid} -> {captured_base_ref}@{moved_base_oid}" in gaps,
            "base movement before PR open did not name old/new base identity",
        )

    print("PASS: stable deterministic slice ran fixture-quality but omitted Approve for unexecuted steps 3-6 judgment checks")
    print("PASS: captured non-default base inspection includes a committed path omitted by implicit default inspection")
    print("PASS: discovered repository checks outside the caller-authorized argv list remain not verified and omit Approve")
    print("PASS: stable subject/head with a changed base OID omits Approve and names old/new base identity")
    print("PASS: subject movement, moved head, incomplete inventories, and disallowed checks omit Approve; dirt still offers option 1")
    print("PASS: an absent provider ref permits first push only when its exact captured OID is present before PR creation")
    print("PASS: only an exact verified equivalent gate normalizes a deferred sweep class to verified evidence")
    print("PASS: base movement before first push or PR open stops publication and names old/new base identity")


def materialize(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    repo = destination / "checkout"
    head = build_repository(repo)
    _, _, base_ref, base_oid, paths, check_results = inspect_stable_session(repo, CALLER_AUTHORIZED_ARGV)
    print(f"checkout: {repo}")
    print("subject: assessment-subject")
    print(f"full head: {head}")
    print(f"base: {base_ref}@{base_oid}")
    print(f"inspected paths: {', '.join(sorted(paths))}")
    print(f"relevant checks: {', '.join(f'{check}: {result}' for check, result in sorted(check_results.items()))}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--materialize", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.materialize:
        materialize(args.materialize)
    else:
        run_suite()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FixtureError, OSError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
