#!/usr/bin/env python3
"""Check the repo-captain Skill Eval's stand-ins, staging, and fixtures.

The Skill Eval's evidence is the stand-ins' traces, so each stand-in has to
refuse what GitHub or Orca would refuse and record what it accepts, and the
staged git history has to agree with the world the gh stand-in serves. This
runner stages every committed fixture and calls the stand-ins and git the way
an agent would, with no model and no network.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVALS = ROOT / "evals/repo-captain"
STAGE = EVALS / "fixtures/stage.py"
CASES = EVALS / "cases"
TRACKER = ROOT / "skills/managing-issues/references/github.md"
REVIEWING_PRS_CHECKS = ROOT / "tests/reviewing-prs/fixtures/run-standin-checks.py"
SLUG = "acme/ledger-app"


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def git_environment() -> dict:
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    environment.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    return environment


class Run:
    """One staged case: its world, stand-ins, remote, and workspace."""

    def __init__(self, case: str, scratch: Path) -> None:
        self.case = case
        self.path = scratch / case
        staged = subprocess.run([sys.executable, str(STAGE), case, str(self.path)], capture_output=True, text=True, check=False)
        expect(staged.returncode == 0, f"{case}: staging failed: {staged.stderr}")
        self.world = json.loads((self.path / "world.json").read_text(encoding="utf-8"))
        self.remote = Path(self.world["repos"][SLUG]["gitRemote"])
        self.env = {
            "PATH": os.environ["PATH"],
            "GH_STANDIN_WORLD": str(self.path / "world.json"), "GH_STANDIN_STATE": str(self.path / "gh-state"),
            "ORCA_STANDIN_WORLD": str(self.path / "world.json"), "ORCA_STANDIN_STATE": str(self.path / "orca-state"),
        }

    def call(self, tool: str, *args: str, env: dict | None = None, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(self.path / "bin" / tool), *args], env=env or self.env, input=stdin, capture_output=True, text=True, check=False)

    def gh(self, *args: str, **kwargs) -> subprocess.CompletedProcess[str]:
        return self.call("gh", *args, **kwargs)

    def orca(self, *args: str, **kwargs) -> subprocess.CompletedProcess[str]:
        return self.call("orca", *args, **kwargs)

    def json(self, tool: str, *args: str) -> object:
        result = self.call(tool, *args)
        expect(result.returncode == 0, f"{self.case}: {tool} {' '.join(args)} failed: {result.stderr}")
        return json.loads(result.stdout)

    def git(self, *args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(["git", *args], cwd=cwd or self.path / "workspace", env=git_environment(), capture_output=True, text=True, check=False)
        expect(not check or result.returncode == 0, f"{self.case}: git {' '.join(args)} failed: {result.stderr}")
        return result

    def ref(self, name: str) -> str:
        return self.git("--git-dir", str(self.remote), "rev-parse", "--verify", "--quiet", name, check=False).stdout.strip()

    def turn(self, number: int) -> None:
        moved = subprocess.run([sys.executable, str(STAGE), "turn", str(self.path), str(number)], capture_output=True, text=True, check=False)
        expect(moved.returncode == 0, f"{self.case}: turn {number} failed: {moved.stderr}")

    def head(self, number: str) -> str:
        return self.json("gh", "pr", "view", number, "-R", SLUG, "--json", "headRefOid")["headRefOid"]

    def trace(self, tool: str) -> list[dict]:
        leaf = self.path / f"{tool}-state" / "trace.jsonl"
        return [json.loads(line) for line in leaf.read_text(encoding="utf-8").splitlines()] if leaf.exists() else []


def tracker_query(name: str) -> str:
    """The fixed GraphQL document managing-issues sends, read from its shipped reference."""
    text = TRACKER.read_text(encoding="utf-8")
    pattern = {"scores": r"`(query\(\$owner:String!,\$name:String!,\$number:Int!\)\{[^`]*issueFieldValues[^`]*)`",
               "fields": r"`(query\(\$owner:String!,\$name:String!,\$endCursor:String\)\{repository[^`]*issueFields\([^`]*)`",
               "set": r"`(mutation[^`]*setIssueFieldValue[^`]*)`"}[name]
    match = re.search(pattern, text)
    expect(match is not None, f"managing-issues no longer names its {name} document")
    return match.group(1)


def scores(run: Run, number: str) -> dict:
    answer = run.json("gh", "api", "graphql", "--hostname", "github.com", "-f", f"query={tracker_query('scores')}", "-f", "owner=acme", "-f", "name=ledger-app", "-F", f"number={number}")
    nodes = answer["data"]["repository"]["issue"]["issueFieldValues"]["nodes"]
    return {node["field"]["name"]: node["value"] for node in nodes}


def check_every_fixture(scratch: Path) -> None:
    cases = sorted(path.name for path in CASES.iterdir() if path.is_dir())
    fixtures = sorted(path.name for path in (EVALS / "fixtures").iterdir() if path.is_dir())
    expect(cases == fixtures, f"fixtures {fixtures} do not match cases {cases}")
    for case in cases:
        run = Run(case, scratch)
        world_text = (run.path / "world.json").read_text(encoding="utf-8")
        expect("<<" not in world_text, f"{case}: a token was left unreplaced in the staged world")
        prompt = (CASES / case / "prompt.md").read_text(encoding="utf-8")
        turns_file = CASES / case / "turns.json"
        turns = json.loads(turns_file.read_text(encoding="utf-8"))["turns"] if turns_file.exists() else [{"turn": 1, "content": prompt.split("---\n", 2)[2].strip()}]
        expect([turn["turn"] for turn in turns] == list(range(1, len(turns) + 1)), f"{case}: turns must be numbered from 1")
        expect(prompt.rstrip().endswith(turns[0]["content"]), f"{case}: prompt.md must be the first turn")
        changes = [int(key) for key in [*run.world.get("turns", {}), *run.world["orca"].get("turns", {})]]
        expect(all(2 <= key <= len(turns) for key in changes), f"{case}: world changes {changes} fall outside turns 2 to {len(turns)}")

        expect(run.json("gh", "api", "user")["login"] == "dana-acme", f"{case}: operator login")
        hosts = run.json("gh", "auth", "status", "--active", "--hostname", "github.com", "--json", "hosts")["hosts"]["github.com"]
        expect(hosts[0]["login"] == "dana-acme" and hosts[0]["active"], f"{case}: auth status --json")
        repo = run.json("gh", "repo", "view", f"github.com/{SLUG}", "--json", "id,nameWithOwner,url,hasIssuesEnabled,isArchived,viewerPermission")
        expect(repo["nameWithOwner"] == SLUG and repo["hasIssuesEnabled"], f"{case}: repo view with the host-qualified name")
        pulls = run.json("gh", "pr", "list", "-R", SLUG, "--state", "all", "--json", "number,state,headRefOid,headRefName,isCrossRepository")
        for item in pulls:
            number, head = str(item["number"]), item["headRefOid"]
            expect(run.ref(f"refs/pull/{number}/head") == head, f"{case}: #{number}'s head is not refs/pull/{number}/head in the staged remote")
            if item["state"] != "OPEN":
                continue
            diff = run.gh("pr", "diff", number, "-R", SLUG)
            expect(diff.returncode == 0 and diff.stdout.startswith("diff --git "), f"{case}: #{number} has no diff")
            if not item["isCrossRepository"]:
                expect(run.ref(f"refs/heads/{item['headRefName']}") == head, f"{case}: #{number}'s branch does not point at its head")
        issues = run.json("gh", "issue", "list", "-R", f"github.com/{SLUG}", "--state", "all", "--limit", "100", "--json", "number,labels")
        expect(issues, f"{case}: the tracker has no issues")
        for item in issues:
            values = scores(run, str(item["number"]))
            expect(len(values) == 4 and all(value in (1.0, 2.0, 3.0) for value in values.values()), f"{case}: #{item['number']} scores {values}")
        policy = run.gh("api", f"repos/{SLUG}/contents/AGENTS.md?ref=main", "-H", "Accept: application/vnd.github.raw")
        expect(policy.returncode == 0 and policy.stdout == (run.path / "workspace/AGENTS.md").read_text(encoding="utf-8"), f"{case}: GitHub and git disagree on AGENTS.md")

        expect("worker-release" in run.orca("skills", "get", "orchestration").stdout, f"{case}: the orchestration guide")
        agents = run.json("orca", "agent", "list", "--json")["result"]
        expect([agent["self"] for agent in agents].count(True) == 1, f"{case}: exactly one session must be this one")
        for command in (("orchestration", "worker-list"), ("host", "list"), ("repo", "list"), ("worktree", "list")):
            run.json("orca", *command, "--json")
        seed = EVALS / "fixtures" / case / "captain-state"
        if seed.is_dir():
            staged = run.path / "xdg-state" / "ledger-app-captain"
            expect(sorted(p.relative_to(seed) for p in seed.rglob("*.md")) == sorted(p.relative_to(staged) for p in staged.rglob("*.md")), f"{case}: captain state not staged")
            expect("<<" not in "".join(p.read_text(encoding="utf-8") for p in staged.rglob("*.md")), f"{case}: a token was left in the captain state")
        for tool in ("gh", "orca"):
            expect(all(entry["kind"] == "read" for entry in run.trace(tool)), f"{case}: a {tool} read was traced as something else")


def check_orca_refusals(scratch: Path) -> None:
    run = Run("direction-change-restarts-executor", scratch / "refusals")
    unknown = run.orca("orchestration", "worker-teleport", "w-1")
    expect(unknown.returncode == 3, f"an unknown orchestration verb must exit 3: {unknown.returncode}")
    expect(run.orca("status", "--json").returncode == 3, "a command outside the contract must exit 3")
    flag = run.orca("orchestration", "worker-start", "--agent", "codex", "--model", "m", "--environment", "local", "--brief", "x", "--sideways")
    expect(flag.returncode == 3, "an unknown flag must exit 3")
    refused = [entry for entry in run.trace("orca") if entry["kind"] == "refused"]
    expect(len(refused) == 3 and refused[0]["argv"] == ["orchestration", "worker-teleport", "w-1"], f"refusals must be traced with their arguments: {refused}")
    expect(all(worker["state"] == "working" for worker in run.json("orca", "orchestration", "worker-list")["result"]), "refused calls must change nothing")
    repository = scratch / "refusals" / "repository"
    (repository / ".git").mkdir(parents=True)
    inside = run.orca("agent", "list", env=dict(run.env, ORCA_STANDIN_STATE=str(repository)))
    expect(inside.returncode == 4 and "outside any git work tree" in inside.stderr and not (repository / "lock").exists(), "a state directory inside a repository must be rejected untouched")
    expect(run.orca("agent", "list", env={"PATH": os.environ["PATH"]}).returncode == 4, "a missing configuration must be rejected")


def check_worker_lifecycle(scratch: Path) -> None:
    leads = Run("domain-lead-custody-and-self-merge", scratch / "lifecycle")
    early = leads.orca("orchestration", "worker-release", "w-1")
    expect(early.returncode == 1 and "worker_done" in early.stderr, "releasing a worker that has not sent worker_done must fail")
    expect(leads.json("orca", "orchestration", "worker-show", "w-1")["result"]["state"] == "working", "a refused release must change nothing")
    expect(leads.orca("orchestration", "worker-release", "w-2").returncode == 0, "a worker that sent worker_done can be released")
    inbox = leads.json("orca", "orchestration", "check")["result"]
    expect({item["type"] for item in inbox} == {"worker_done", "question"} and leads.json("orca", "orchestration", "check")["result"] == [], "check returns unread messages once")
    expect(leads.orca("orchestration", "reply", "--question", "q-1", "--message", "wait for #568").returncode == 0, "reply to a Lead's question")
    kinds = [(entry["kind"], entry.get("op"), entry.get("worker")) for entry in leads.trace("orca") if entry["kind"] != "read"]
    expect(("error", "worker-release", "w-1") in kinds and ("write", "worker-release", "w-2") in kinds, f"releases must be traced: {kinds}")

    restart = Run("restart-split-brain-and-boundaries", scratch / "lifecycle")
    start = ["orchestration", "worker-start", "--agent", "codex", "--model", "gpt-5.5-codex", "--environment", "local", "--brief", "again"]
    expect(restart.orca(*start, "--retry-of", "d-2").returncode == 1, "an unverifiable worker's dispatch must not be retried")
    expect(restart.orca(*start, "--retry-of", "d-1").returncode == 0, "an exited worker's dispatch can be retried")
    expect([agent["id"] for agent in restart.json("orca", "agent", "list")["result"]] == ["sess-cap-old", "sess-cap-new"], "both Captains are live in turn 1")
    restart.turn(2)
    expect([agent["id"] for agent in restart.json("orca", "agent", "list")["result"]] == ["sess-cap-new"], "the earlier Captain is gone in turn 2")


def check_moving_head_and_queue(scratch: Path) -> None:
    run = Run("rebase-revert-and-merge-queue", scratch / "queue")
    reviewed = run.head("560")
    expect(run.ref("refs/heads/export-summary") == reviewed, "turn 1: the branch and the pull request agree")
    run.turn(2)
    current, rounding = run.head("560"), run.head("561")
    expect(current != reviewed and run.ref("refs/heads/export-summary") == current, "turn 2: the head moved in gh and in git together")
    comments = run.json("gh", "pr", "view", "560", "-R", SLUG, "--json", "comments")["comments"]
    expect(comments[-1]["body"].splitlines()[1] == f"Head: {reviewed}", "turn 2: the Verdict landed at the reviewed head")
    run.git("fetch", "-q", "origin")
    run.git("fetch", "-q", "origin", reviewed)  # an earlier head is still served by SHA, as on GitHub
    base = run.git("merge-base", "origin/main", reviewed).stdout.strip()
    expect(run.git("range-diff", f"{base}..{reviewed}", f"origin/main..{current}").returncode == 0, "range-diff runs on the staged commits")
    reverted = run.git("diff", "origin/main", rounding, "--", "app/billing/tax.ts").stdout
    expect("-  if (amountCents <= 0) {" in reverted, "#561's new head quietly reverts main's credit-note guard")

    stale = run.gh("pr", "merge", "560", "-R", SLUG, "--squash", "--match-head-commit", reviewed)
    expect(stale.returncode == 1 and "Head branch was modified" in stale.stderr, "a merge pinned to a stale head must fail")
    admin = run.gh("pr", "merge", "560", "-R", SLUG, "--admin", "--match-head-commit", current)
    expect(admin.returncode == 1 and "merge queue" in admin.stderr, "an admin merge must not bypass the merge queue")
    queued = run.gh("pr", "merge", "560", "-R", SLUG, "--squash", "--match-head-commit", current)
    expect(queued.returncode == 0 and "merge queue" in queued.stdout, f"enqueue: {queued.stderr}")
    expect(run.gh("pr", "merge", "560", "-R", SLUG, "--match-head-commit", current).returncode == 1, "a queued pull request cannot be enqueued twice")
    queue = {"query": "query($owner:String!,$repo:String!){repository(owner:$owner,name:$repo){mergeQueue{entries(first:20){nodes{position state pullRequest{number}}}}}}"}
    entries = run.json("gh", "api", "graphql", "-f", f"query={queue['query']}", "-f", "owner=acme", "-f", "repo=ledger-app")["data"]["repository"]["mergeQueue"]["entries"]["nodes"]
    expect([entry["pullRequest"]["number"] for entry in entries] == [560], f"the queue lists #560: {entries}")
    expect(run.json("gh", "pr", "view", "560", "-R", SLUG, "--json", "state")["state"] == "OPEN", "a queued pull request stays open until the queue merges it")

    run.turn(3)
    view = run.json("gh", "pr", "view", "560", "-R", SLUG, "--json", "state,headRefOid")
    entry = run.json("gh", "api", "graphql", "-f", "query=query($owner:String!,$repo:String!,$number:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$number){mergeQueueEntry{state}}}}", "-f", "owner=acme", "-f", "repo=ledger-app", "-F", "number=560")
    expect(view == {"state": "OPEN", "headRefOid": current} and entry["data"]["repository"]["pullRequest"]["mergeQueueEntry"] is None, "turn 3: the queue ejected #560 at the same head")
    expect(run.gh("pr", "merge", "560", "-R", SLUG, "--match-head-commit", current).returncode == 0, "re-enqueue after an ejection")
    run.turn(4)
    merged = run.json("gh", "pr", "view", "560", "-R", SLUG, "--json", "state,mergeCommit")
    expect(merged["state"] == "MERGED" and merged["mergeCommit"], "turn 4: the queue merged #560")
    checks = run.json("gh", "api", f"repos/{SLUG}/commits/{merged['mergeCommit']['oid']}/check-runs")
    expect([(item["name"], item["conclusion"]) for item in checks["check_runs"]] == [("test", "success")], f"check runs on the merge commit: {checks}")
    merges = [entry.get("result") for entry in run.trace("gh") if entry.get("op") == "pr merge" and entry["kind"] == "write"]
    expect(merges == ["queued", "queued"], f"the trace must record both enqueues: {merges}")


def check_revert_and_tracker_writes(scratch: Path) -> None:
    run = Run("held-pr-keeps-wake-and-calm-alert", scratch / "writes")
    merge_commit = run.json("gh", "pr", "view", "580", "-R", SLUG, "--json", "mergeCommit")["mergeCommit"]["oid"]
    def ci() -> list:
        return [item["status"] for item in run.json("gh", "api", f"repos/{SLUG}/commits/{merge_commit}/check-runs")["check_runs"]]
    expect(ci() == ["in_progress"], "turn 1: CI on the merge commit is running")
    run.turn(2)
    failed = run.json("gh", "api", f"repos/{SLUG}/commits/{merge_commit}/check-runs")["check_runs"]
    expect([item["conclusion"] for item in failed] == ["failure"], "turn 2: CI on the merge commit failed")
    run.git("checkout", "-q", "-b", "revert-580", "origin/main")
    run.git("revert", "--no-edit", merge_commit)
    run.git("push", "-q", "origin", "revert-580")
    pushed = run.git("rev-parse", "HEAD").stdout.strip()
    run.git("checkout", "-q", "-b", "local-tax", "origin/credit-note-tax")
    run.git("commit", "-q", "--allow-empty", "-m", "touch")
    rejected = run.git("push", "-q", "origin", "local-tax:credit-note-tax", check=False)
    expect(rejected.returncode != 0 and "stand-in remote" in rejected.stderr, "a push to an existing pull request branch must be refused")
    body = "Reverts #580.\n\nOwner: repo-captain · Author: repo-captain · Operator: dana-acme\n"
    missing = run.gh("pr", "create", "-R", SLUG, "--head", "never-pushed", "--title", "x", "--body", "x")
    expect(missing.returncode == 1 and "Head ref must be a branch" in missing.stderr, "a pull request needs a pushed branch")
    created = run.gh("pr", "create", "-R", SLUG, "--head", "revert-580", "--base", "main", "--title", "Revert #580", "--body-file", "-", "--label", "review:held", stdin=body)
    expect(created.returncode == 0, f"pr create: {created.stderr}")
    number = created.stdout.strip().rsplit("/", 1)[1]
    view = run.json("gh", "pr", "view", number, "-R", SLUG, "--json", "headRefOid,body,labels,state,files")
    expect(view["headRefOid"] == pushed and view["body"] == body and view["state"] == "OPEN", f"the new pull request matches the pushed branch: {view}")
    expect([item["path"] for item in view["files"]] == ["app/lib/pagination.ts", "tests/lib/pagination.test.ts"], f"the revert's diff comes from git: {view['files']}")
    expect(run.gh("pr", "create", "-R", SLUG, "--head", "revert-580", "--title", "again", "--body", "x").returncode == 1, "one open pull request per branch")

    tracker = Run("hold-gate-raises-scores", scratch / "writes")
    issue_id = tracker.json("gh", "issue", "view", "546", "-R", f"github.com/{SLUG}", "--json", "id,number,title,body,state,stateReason,updatedAt,url,labels,assignees,projectItems,issueType,parent,subIssues,blockedBy,blocking")["id"]
    fields = tracker.json("gh", "api", "graphql", "--hostname", "github.com", "-f", f"query={tracker_query('fields')}", "-f", "owner=acme", "-f", "name=ledger-app")
    ids = {node["name"]: node["id"] for node in fields["data"]["repository"]["issueFields"]["nodes"]}
    before = scores(tracker, "546")
    expect(before["Undo cost"] == 1.0, f"#546 stores U=1: {before}")
    write = tracker.gh("api", "graphql", "--hostname", "github.com", "-f", f"query={tracker_query('set')}", "-f", f"issue={issue_id}",
                       "-f", f"impact={ids['Impact']}", "-f", f"confidence={ids['Confidence']}", "-f", f"verification={ids['Verification effort']}", "-f", f"undo={ids['Undo cost']}",
                       "-F", "i=2", "-F", "c=2", "-F", "v=1", "-F", "u=3")
    expect(write.returncode == 0, f"score write: {write.stderr}")
    expect(scores(tracker, "546") == {**before, "Undo cost": 3.0}, "the score read returns the raised undo cost")
    expect(tracker.gh("issue", "edit", "546", "-R", SLUG, "--add-label", "no-such-label").returncode == 1, "an issue label must exist")
    edited = tracker.gh("issue", "edit", "546", "-R", f"github.com/{SLUG}", "--body-file", "-", stdin="## Scope\n\nTighter.\n")
    expect(edited.returncode == 0 and tracker.json("gh", "issue", "view", "546", "-R", SLUG, "--json", "body")["body"] == "## Scope\n\nTighter.\n", "issue edit replaces the body")
    writes = [(entry["op"], entry.get("values")) for entry in tracker.trace("gh") if entry["kind"] == "write"]
    expect(writes == [("set issue fields", {"Impact": 2, "Confidence": 2, "Verification effort": 1, "Undo cost": 3}), ("issue edit", None)], f"tracker writes must be traced: {writes}")


def check_reviewing_prs_still_passes() -> None:
    result = subprocess.run([sys.executable, str(REVIEWING_PRS_CHECKS)], capture_output=True, text=True, check=False)
    expect(result.returncode == 0, f"the reviewing-prs stand-in checks fail after the gh extension:\n{result.stdout}{result.stderr}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="rookery-repo-captain-") as temporary:
        scratch = Path(temporary).resolve()
        for name in ("refusals", "lifecycle", "queue", "writes"):
            (scratch / name).mkdir()
        check_every_fixture(scratch)
        check_orca_refusals(scratch)
        check_worker_lifecycle(scratch)
        check_moving_head_and_queue(scratch)
        check_revert_and_tracker_writes(scratch)
    check_reviewing_prs_still_passes()
    print("repo-captain: stand-in, staging, and fixture checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
