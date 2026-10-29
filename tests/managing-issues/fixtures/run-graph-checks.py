#!/usr/bin/env python3
"""Check the published Managing Issues graph contracts."""

from __future__ import annotations

import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
SKILL = REPO_ROOT / "skills/managing-issues/SKILL.md"
REFERENCE = REPO_ROOT / "skills/managing-issues/references/graph-and-completion.md"
GITHUB_REFERENCE = REPO_ROOT / "skills/managing-issues/references/github.md"
LINEAR_REFERENCE = REPO_ROOT / "skills/managing-issues/references/linear.md"


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def published_contract_checks() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")
    required = (
        "capabilities before showing an executable graph preview",
        "nodes before relationships",
        "latest complete canonical readback",
        "never use a stored readiness representation as evidence",
        "exactly one",
        "Ready Frontier",
        "needs-discovery",
        "needs-planning",
        "`ready`",
        "no estimate",
        "shared lifecycle's first-stop rule",
        "applied",
        "already_satisfied",
        "failed",
        "indeterminate",
        "unapplied",
        "provider reference",
        "Never match by title",
        "separate batch",
        "list every cascade the provider reports as an intended effect",
        "Do not inspect, predict, repair, or block on effects the provider does not report",
        "Do not add implementation recommendations or persist an execution handoff",
    )
    normalized = " ".join(text.split()).casefold()
    for fragment in required:
        require(
            fragment.casefold() in normalized,
            f"graph reference lacks contract: {fragment}",
        )

    normalized_skill = " ".join(skill.split()).casefold()
    for fragment in (
        "independently deliverable",
        "preferences and convenient ordering",
        "expand–migrate–contract",
    ):
        require(
            fragment.casefold() in normalized_skill,
            f"main skill lacks decomposition contract: {fragment}",
        )

    forbidden = (
        "trusted policy",
        "trusted evidence",
        "authority, policy",
        "Release A treats every Linear topology mutation as `manual`",
        "orca linear relation",
        "gh issue edit CHILD",
    )
    for fragment in forbidden:
        require(
            fragment.casefold() not in normalized,
            f"graph reference retains stale surface: {fragment}",
        )

    github = GITHUB_REFERENCE.read_text(encoding="utf-8")
    require("sub_issues?per_page=100&page=PAGE" in github, "GitHub reference lacks exhaustive child read")
    require("dependencies/blocked_by?per_page=100&page=PAGE" in github, "GitHub reference lacks exhaustive blocker read")
    require(
        "one-hop cross-repository boundary read" in github
        and "never a create, edit, relationship, or lifecycle target" in github,
        "GitHub reference lacks the read-only cross-repository boundary",
    )
    linear = LINEAR_REFERENCE.read_text(encoding="utf-8")
    require("workspaceErrors" in linear and "capReached" in linear, "Linear reference lacks partial-coverage checks")
    normalized_skill_text = " ".join(skill.split())
    for fragment in (
        "The configured provider is canonical and is the only write target",
        "only through one exact provider-native cross-tracker link",
        "Never infer identity, maintain a repository-side mapping, or mutate the noncanonical issue",
    ):
        require(
            fragment in normalized_skill_text,
            f"main skill lacks cross-tracker routing contract: {fragment}",
        )


def main() -> int:
    for required in (SKILL, REFERENCE, GITHUB_REFERENCE, LINEAR_REFERENCE):
        require(required.is_file(), f"missing artifact: {required.relative_to(REPO_ROOT)}")
    published_contract_checks()
    print("PASS: managing-issues graph text contracts")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
