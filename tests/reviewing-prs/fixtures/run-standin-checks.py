#!/usr/bin/env python3
"""Check the reviewing-prs Skill Eval's GitHub stand-in and its fixtures.

The Skill Eval's evidence is the stand-in's trace, so the stand-in has to
refuse what GitHub would refuse and record what it accepts. This runner calls
it the way an agent would, against every committed fixture, with no model.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STAND_IN = ROOT / "evals/reviewing-prs/stand-ins/gh"
FIXTURES = ROOT / "evals/reviewing-prs/fixtures"
CASES = ROOT / "evals/reviewing-prs/cases"
SKILL = ROOT / "skills/reviewing-prs/SKILL.md"


class Run:
    """One staged world with its own state directory."""

    def __init__(self, fixture: str, scratch: Path) -> None:
        self.state = scratch / fixture
        self.state.mkdir()
        self.env = {
            "PATH": os.environ["PATH"],
            "GH_STANDIN_WORLD": str(FIXTURES / fixture / "world.json"),
            "GH_STANDIN_STATE": str(self.state),
        }

    def gh(self, *args: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(STAND_IN), *args], env=env or self.env, capture_output=True, text=True, check=False)

    def json(self, *args: str) -> object:
        result = self.gh(*args)
        if result.returncode != 0:
            raise AssertionError(f"gh {' '.join(args)} failed: {result.stderr}")
        return json.loads(result.stdout)

    def trace(self) -> list[dict]:
        return [json.loads(line) for line in (self.state / "trace.jsonl").read_text(encoding="utf-8").splitlines()]


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_every_fixture(scratch: Path) -> None:
    fixtures = sorted(path.name for path in FIXTURES.iterdir() if path.is_dir())
    cases = sorted(path.name for path in CASES.iterdir() if path.is_dir())
    expect(fixtures == cases, f"fixtures {fixtures} do not match cases {cases}")
    for fixture in fixtures:
        run = Run(fixture, scratch)
        expect(run.json("api", "user")["login"] == "dana-acme", f"{fixture}: operator login")
        found = run.json("search", "prs", "--owner", "acme", "--state", "open", "--draft=false", "--archived=false", "--limit", "1000", "--json", "repository,number")
        expect(len(found) >= 2, f"{fixture}: expected open pull requests")
        for item in found:
            slug, number = item["repository"]["nameWithOwner"], str(item["number"])
            view = run.json("pr", "view", number, "-R", slug, "--json", "headRefOid,additions,changedFiles,isCrossRepository,author,body")
            expect(len(view["headRefOid"]) == 40 and view["changedFiles"] >= 1, f"{fixture}: {slug}#{number} has no usable diff")
            diff = run.gh("pr", "diff", number, "-R", slug)
            expect(diff.returncode == 0 and diff.stdout.startswith("diff --git "), f"{fixture}: {slug}#{number} diff")
            repo = run.json("repo", "view", slug, "--json", "viewerPermission,visibility,defaultBranchRef")
            policy = run.gh("api", f"repos/{slug}/contents/AGENTS.md?ref={repo['defaultBranchRef']['name']}")
            expect(policy.returncode == 0, f"{fixture}: {slug} default-branch policy read")
        expect(all(entry["kind"] == "read" for entry in run.trace()), f"{fixture}: a read was traced as something else")


def check_writes_and_refusals(scratch: Path) -> None:
    run = Run("owner-routing-and-scrubbing", scratch / "writes")
    slug = "acme/ledger-app"
    head = run.json("pr", "view", "423", "-R", slug, "--json", "headRefOid")["headRefOid"]

    stale = run.gh("pr", "merge", "423", "-R", slug, "--squash", "--match-head-commit", "0" * 40)
    expect(stale.returncode == 1 and "Head branch was modified" in stale.stderr, "a merge pinned to the wrong commit must fail")
    expect(run.gh("pr", "merge", "423", "-R", slug).returncode == 1, "a merge without a method must fail")
    expect(run.json("pr", "view", "423", "-R", slug, "--json", "state")["state"] == "OPEN", "a refused merge must not merge")

    missing = run.gh("pr", "edit", "423", "-R", slug, "--add-label", "review:human-merged")
    expect(missing.returncode == 1 and "not found" in missing.stderr, "adding a label the repository lacks must fail")
    expect(run.gh("label", "create", "review:human-merged", "-R", slug, "--color", "5319E7", "--description", "x").returncode == 0, "label create")

    body = scratch / "verdict.txt"
    body.write_text(f'Verdict: merge\nHead: {head}\nNotes: ""\n', encoding="utf-8")
    expect(run.gh("pr", "comment", "423", "-R", slug, "--body-file", str(body)).returncode == 0, "comment")
    expect(run.gh("pr", "merge", "423", "-R", slug, "--squash", "--match-head-commit", head).returncode == 0, "pinned merge")
    after = run.json("pr", "view", "423", "-R", slug, "--json", "state,comments")
    expect(after["state"] == "MERGED" and after["comments"][-1]["body"].splitlines()[1] == f"Head: {head}", "merge and comment must persist")
    expect(run.gh("pr", "edit", "423", "-R", slug, "--add-label", "review:human-merged", "--remove-label", "review:held").returncode == 0, "label swap")

    expect(run.gh("api", "-X", "PUT", f"repos/{slug}/pulls/421/merge").returncode == 3, "a REST write must be refused")
    expect(run.gh("pr", "close", "421", "-R", slug).returncode == 3, "a command outside the contract must be refused")
    expect(run.gh("pr", "review", "421", "-R", slug, "--approve").returncode == 1, "approving your own pull request must fail")
    expect(run.gh("api", "graphql", "-f", "query=mutation { enqueuePullRequest(input: {}) { clientMutationId } }").returncode == 1, "no fixture has a merge queue")
    expect(run.json("pr", "view", "421", "-R", slug, "--json", "state")["state"] == "OPEN", "refused writes must change nothing")

    kinds = [(entry["kind"], entry.get("op")) for entry in run.trace() if entry["kind"] != "read"]
    expect(kinds.count(("write", "pr merge")) == 1, f"exactly one merge must be traced as a write: {kinds}")
    expect(("refused", "api write") in kinds and ("refused", "pr close") in kinds, f"refusals must be traced: {kinds}")
    merge = next(entry for entry in run.trace() if entry["kind"] == "write" and entry.get("op") == "pr merge")
    expect(merge["match_head_commit"] == head, "the trace must record the pinned commit")


def check_conflict_and_digest(scratch: Path) -> None:
    run = Run("conflicts-impact-digest-html", scratch / "conflicts")
    slug = "acme/ledger-app"
    commented = run.json("search", "prs", "--owner", "acme", "--commenter", "dana-acme", "--sort", "updated", "--json", "repository,number,updatedAt")
    stamps = [item["updatedAt"] for item in commented]
    expect(stamps == sorted(stamps, reverse=True) and {419, 420} <= {item["number"] for item in commented}, f"commenter search, newest first: {commented}")
    expect(all(item["number"] not in (416, 418) for item in commented), "a pull request the operator never commented on must not match --commenter")
    # The window starts 24 hours before the newest Verdict; #416 merged six hours earlier the same day.
    merged = run.json("search", "prs", "--owner", "acme", "--merged", "--merged-at", ">=2026-11-18T18:00:00Z", "--json", "repository,number")
    found = sorted((item["repository"]["nameWithOwner"], item["number"]) for item in merged)
    expected = [("acme/handbook", 7)] + [(slug, number) for number in (411, 417, 418, 419, 420)]
    expect(found == expected, f"merged-window search must compare full timestamps: {found}")
    expect(len(run.json("search", "prs", "--owner", "acme", "--merged", "--merged-at", ">=2026-11-18", "--json", "number")) == 7, "a bare date covers its whole day")
    comments = run.json("pr", "view", "419", "-R", slug, "--json", "comments")["comments"]
    expect(any(comment["body"].startswith("Fleet: verdict-delta") for comment in comments), "the verdict-delta receipt must be readable")
    head = run.json("pr", "view", "426", "-R", slug, "--json", "headRefOid")["headRefOid"]
    expect(run.gh("pr", "merge", "426", "-R", slug, "--squash", "--match-head-commit", head).returncode == 0, "merge 426")
    expect(run.json("pr", "view", "427", "-R", slug, "--json", "mergeStateStatus")["mergeStateStatus"] == "DIRTY", "merging one side of a conflict must dirty the other")
    for flags in ([], ["--admin"]):
        expect(run.gh("pr", "merge", "427", "-R", slug, "--squash", *flags).returncode == 1, f"a conflicted pull request must not merge {flags}")
    body = scratch / "review.txt"
    body.write_text("Verdict: merge", encoding="utf-8")
    expect(run.gh("pr", "review", "139", "-R", "acme/cli-kit", "--comment", "--body-file", str(body)).returncode == 0, "review on a fork pull request")
    review = next(entry for entry in run.trace() if entry.get("op") == "pr review")
    expect(review["kind"] == "write" and review["body"] == "Verdict: merge", "a Verdict posted as a review must be visible in the trace")


def check_review_threads(scratch: Path) -> None:
    """The skill reads review threads through one GraphQL query; the stand-in must answer it."""
    run = Run("risk-overview-and-situations", scratch / "threads")
    query = re.search(r"gh api graphql -f query='([^']*reviewThreads[^']*)'", SKILL.read_text(encoding="utf-8"))
    expect(query is not None, "the skill must name its review-thread query")
    answer = run.json("api", "graphql", "-f", f"query={query.group(1)}", "-f", "owner=acme", "-f", "repo=ledger-app", "-F", "number=441")
    nodes = answer["data"]["repository"]["pullRequest"]["reviewThreads"]["nodes"]
    expect(len(nodes) == 2 and all(node["isResolved"] for node in nodes), f"review threads: {nodes}")
    expect(nodes[0]["comments"]["nodes"][-1]["body"] == "Out of scope for this fix.", "the declined answer must be readable")
    missing = run.gh("api", "graphql", "-f", f"query={query.group(1)}", "-f", "owner=acme", "-f", "repo=ledger-app", "-F", "number=999")
    expect(missing.returncode == 1, "a review-thread query for a missing pull request must fail")


def check_shipped_commands(scratch: Path) -> None:
    """Every --json field list the shipped skill names must be answered, so the two cannot drift."""
    run = Run("owner-routing-and-scrubbing", scratch / "shipped")
    targets = {"search prs": ["--owner", "acme"], "repo view": ["acme/cli-kit"], "pr view": ["134", "-R", "acme/cli-kit"], "label list": ["-R", "acme/cli-kit"]}
    found = re.findall(r"gh (search prs|repo view|pr view|label list)\b[^`]*?--json ([A-Za-z,]+)", SKILL.read_text(encoding="utf-8"))
    expect({command for command, _ in found} == set(targets), f"expected the skill to name --json fields for {sorted(targets)}: {found}")
    for command, fields in found:
        data = run.json(*command.split(), *targets[command], "--json", fields)
        for item in data if isinstance(data, list) else [data]:
            expect(set(item) == set(fields.split(",")), f"gh {command} --json {fields}: got {sorted(item)}")
    expect(run.gh("pr", "view", "134", "-R", "acme/cli-kit", "--json", "noSuchField").returncode == 1, "an unknown JSON field must fail")
    expect(run.json("pr", "list", "-R", "acme/payroll-internal", "--json", "headRefOid") == [], "an empty list must still accept valid fields")
    root = run.json("api", "repos/acme/cli-kit/contents?ref=main")
    expect([entry["name"] for entry in root] == ["AGENTS.md"], f"root listing: {root}")
    expect(shutil.which("jq") is not None, "jq is required: the skill's commands use --jq")
    login = run.gh("api", "user", "--jq", ".login")
    expect(login.returncode == 0 and login.stdout.strip() == "dana-acme", f"--jq: {login.stderr}")


def check_parallel_calls(scratch: Path) -> None:
    run = Run("owner-routing-and-scrubbing", scratch / "parallel")
    command = [sys.executable, str(STAND_IN), "pr", "comment", "423", "-R", "acme/ledger-app", "--body"]
    processes = [subprocess.Popen([*command, f"note {index}"], env=run.env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True) for index in range(8)]
    errors = [process.communicate()[1] for process in processes]
    expect(all(process.returncode == 0 for process in processes), f"parallel writes failed: {errors}")
    comments = run.json("pr", "view", "423", "-R", "acme/ledger-app", "--json", "comments")["comments"]
    expect(len(comments) == 8, f"parallel writes lost comments: {len(comments)} of 8")


def check_unsafe_configuration(scratch: Path) -> None:
    # A real fixture, so only the guard can reject; a throwaway work tree, so a broken guard writes nothing here.
    run = Run("risk-overview-and-situations", scratch / "unsafe")
    repository = scratch / "unsafe" / "repository"
    (repository / ".git").mkdir(parents=True)
    inside = run.gh("api", "user", env=dict(run.env, GH_STANDIN_STATE=str(repository)))
    expect(inside.returncode == 4 and "outside any git work tree" in inside.stderr, "a state directory inside a repository must be rejected")
    expect(not (repository / "lock").exists(), "a rejected state directory must stay untouched")
    unset = run.gh("api", "user", env={"PATH": os.environ["PATH"]})
    expect(unset.returncode == 4 and "not configured" in unset.stderr, "a missing configuration must be rejected")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="rookery-reviewing-prs-") as temporary:
        scratch = Path(temporary).resolve()
        for name in ("writes", "conflicts", "threads", "unsafe", "shipped", "parallel"):
            (scratch / name).mkdir()
        check_every_fixture(scratch)
        check_writes_and_refusals(scratch)
        check_conflict_and_digest(scratch)
        check_review_threads(scratch)
        check_shipped_commands(scratch)
        check_parallel_calls(scratch)
        check_unsafe_configuration(scratch)
    print("reviewing-prs: stand-in and fixture checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
