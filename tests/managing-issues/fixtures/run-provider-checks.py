#!/usr/bin/env python3
"""Check the published Managing Issues setup, provider, and lifecycle contracts."""

from __future__ import annotations

import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "managing-issues"
SKILL = SKILL_DIR / "SKILL.md"
GITHUB_REF = SKILL_DIR / "references" / "github.md"
LINEAR_REF = SKILL_DIR / "references" / "linear.md"
GRAPH_REF = SKILL_DIR / "references" / "graph-and-completion.md"


class CheckFailure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def published_contract() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    github = GITHUB_REF.read_text(encoding="utf-8")
    linear = LINEAR_REF.read_text(encoding="utf-8")
    compact_skill = " ".join(skill.split())
    compact_linear = " ".join(linear.split())
    require(len(skill.splitlines()) < 500, "SKILL.md exceeds portable line budget")
    for phrase in ("Shape", "Analyze", "Preview", "approval", "Revalidate", "apply", "read back", "unapplied"):
        require(phrase.lower() in skill.lower(), f"shared lifecycle omits {phrase}")
    for phrase in (
        "config-template-github.json",
        "config-template-linear.json",
        "first tracker mutation",
        "missing or invalid config never blocks a read or draft",
        "provider and exact repository or workspace/team target",
        "records the canonical provider, exact target, and metadata mappings",
        "every recommended key and provider representation",
        "never treat existing metadata as the preferred answer",
        "provider-metadata approval",
        "symlink",
        "incompatible config",
    ):
        require(phrase in compact_skill, f"setup contract omits {phrase}")
    require("normalized canonical target" in skill and "Problem" in skill and "Scope" in skill and "Verification" in skill, "preview or issue shape contract differs")
    require("capabilities=..." in compact_skill and "whole proposed batch" in compact_skill, "Linear complete-capability gate differs")
    require("Authentication through the provider path supplies identity" in compact_skill, "authentication contract differs")
    require("Never permanently delete an issue" in compact_skill, "reversible lifecycle contract differs")
    require("stop all later effects, including independent effects" in skill, "batch stop contract differs")
    require(
        "relationship on a newly created issue that the approved batch did not include" in compact_skill
        and "complete preview of the effect that removes the relationship" in compact_skill
        and "The create stays `applied`; stop before the next effect, mark later effects `unapplied`" in compact_skill
        and "it needs fresh approval like any other effect" in compact_skill,
        "unexpected create relationship contract differs",
    )
    compact_graph = " ".join(GRAPH_REF.read_text(encoding="utf-8").split())
    require(
        "relationships is ordinary readback, not inspection of an unreported effect" in compact_graph,
        "create relationship readback conflicts with cascade rule",
    )
    require("accepted non-create effect" in skill and "readback fails, is partial, or mismatches the approved result" in skill, "non-create readback contract differs")
    require("implementation plan" in skill and "worktree" in skill and "pull request" in skill, "issue-only handoff boundary differs")
    require(
        "Linear recommends an exclusive readiness group" in compact_skill,
        "setup recommendation rationale differs",
    )
    require(
        "active account" in github
        and "matchback" in github
        and "--body-file -" in github
        and "gh label create NAME" in github
        and "no grouping surface" in github,
        "GitHub provider contract differs",
    )
    require(
        "ORCA skills get orca-linear" in linear
        and "only authority" in linear
        and "field-specific" in linear
        and "never retried" in linear
        and "first-use setup" in linear,
        "Linear guide/write contract differs",
    )
    for phrase in (
        "never stores a transport",
        "runtime-exposed tool schemas",
        "Otherwise select an available authenticated Linear MCP",
        "do not reconstruct private API calls or fall through to Orca",
        "high` to `2`",
        "pass the resulting number, never the config string",
        "workspace-scoped readiness group",
        "any missing children",
        "Apply a child, never the parent",
        "manual cleanup",
        "create_issue_label",
        "list_issue_labels",
        "the provider may add relationships on its own",
        "explicitly request the created issue's relationships",
        "Relationships the readback does not return are unknown",
        "the create stays `applied` and later effects are `unapplied`",
    ):
        require(phrase in compact_linear, f"Linear transport contract omits {phrase}")


def main() -> int:
    for path in (SKILL, GITHUB_REF, LINEAR_REF, GRAPH_REF):
        require(path.is_file(), f"missing artifact: {path.relative_to(REPO_ROOT)}")
    published_contract()
    print("PASS: managing-issues setup, provider, and lifecycle text contracts")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
