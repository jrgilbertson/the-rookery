# Graph coverage and completion proof

Load this reference only for relationship, readiness, or completion work. Use
native tracker relationships as the graph. Keep traversal facts in the current
response only; do not create a graph file, claim, queue, schedule, or execution
plan.

## Establish complete coverage

Start at the requested canonical node. Walk its parent chain to the top family,
then read every descendant of that top node. Read every internal `blocks` and
`blocked-by` edge. For an edge that crosses the family boundary, read the
one-hop external node needed to know whether it still blocks; do not recursively
adopt that node's family.

Track each canonical provider identity in a visited set and count it once.
Preserve cycles as edges and stop following an already visited identity. The
conservative limit is 250 canonical nodes, including required one-hop boundary
nodes. Coverage becomes `partial` when a required node is inaccessible, the
limit is reached before exhaustion, any page fails, or a cursor is empty or
repeats while another page is claimed. A partial result names the missing
surface. It permits qualified reads but blocks relationship changes and parent
completion. Narrowing the question to known nodes does not waive required
family coverage for a topology write.

If a current authoritative endpoint read proves the exact requested relation
already exists, return `already_satisfied` and perform no relationship write.
Partial family coverage still blocks any different topology mutation or repair;
the no-op does not grant authority to reshape adjacent edges.

### GitHub exhaustion

The arrays returned by `gh issue view` are useful relationship facts but do not
prove pagination exhaustion. Follow parents with the issue read from
`github.md`. Read these native list endpoints one page at a time with
`per_page=100` and an increasing `page` value:

```text
gh api "repos/OWNER/REPO/issues/NUMBER/sub_issues?per_page=100&page=PAGE" --hostname github.com
gh api "repos/OWNER/REPO/issues/NUMBER/dependencies/blocked_by?per_page=100&page=PAGE" --hostname github.com
gh api "repos/OWNER/REPO/issues/NUMBER/dependencies/blocking?per_page=100&page=PAGE" --hostname github.com
```

Process each page before requesting the next. A page shorter than `per_page`
proves that collection exhausted; when a full page would cross the 250-node
cap, retain only the bounded facts and return `partial` without fetching more.
Read each returned canonical identity through `gh issue view` when its current
state or Verification is required. A missing endpoint, truncated collection,
or failed page makes coverage partial.

### Linear exhaustion

Use `orca linear issue ISSUE_ID --relations --workspace WORKSPACE_ID --json`
for the parent and native
relations. Exhaust direct children one parent at a time:

```text
orca linear list-issues --parent-id ISSUE_ID --limit 100 --workspace WORKSPACE_ID --json
orca linear list-issues --parent-id ISSUE_ID --limit 100 --cursor CURSOR --workspace WORKSPACE_ID --json
```

Continue until the response says there is no next page, applying the same
rules recursively to every newly found child. `issue --children --depth` is a
convenience read, not proof of exhaustion. A resolved Linear blocker may move
from blocking relations to Related, so current relations alone do not prove
blocker history; completion relies on current unresolved blockers plus the
declared Verification evidence.

For every child page, require `result.meta.workspaceErrors` to exist and be an
empty array. For every `issue --relations` read, require
`result.meta.includeErrors` to exist and be empty and require
`result.meta.sections.relations.capReached` to be exactly `false`. A missing
field, nonempty warning array, or reached cap makes coverage `partial` even
when the RPC envelope says `ok` and pagination says no next page.

Completion: coverage is `complete` with the counted canonical identities and
cycles named, or `partial` with exact gaps and write restrictions named.

## Change topology and reconcile

Release A treats every Linear topology mutation as `manual`. Complete Linear
coverage may establish the requested relationship and current graph facts, but
it does not make a create, parent, blocker, or removal effect writable. Do not
present a Linear topology effect for approval and do not construct a Linear
write command.

For GitHub, render every node creation before any relationship effect. After
each approved node create, require its authoritative identity and readback; an
indeterminate create receives no dependent edge. Then preview relationship
effects in native direction:

- `gh issue edit CHILD -R github.com/OWNER/REPO --parent PARENT` adds a parent.
- `gh issue edit BLOCKER -R github.com/OWNER/REPO --add-blocking BLOCKED` means
  `BLOCKER blocks BLOCKED`.

Use the GitHub provider reference for inverse or removal commands. Immediately
before each GitHub relationship write, repeat canonical identity, authority,
policy, both endpoint, and affected-family reads. Apply the relation once, then
read both endpoints and recompute the full affected family through the coverage
rules above. Do this after a failed or indeterminate topology attempt too:
preserve verified successes, stop dependent effects, and report every
remaining effect. Do not roll back or infer a compensating edge.

Completion: each topology effect has one exact effect outcome, both directions
agree when applied, and the returned family is a fresh complete reconciliation
or an explicitly partial read-only result.

## Derive the current Ready Frontier

Ready Frontier is the current set of required open leaves that have no current
unresolved blocker and satisfy the repository's readiness mapping. Derive it
only from the complete canonical read. Exclude parents, completed or canceled
nodes, leaves with unmet required predecessors, and any node whose readiness is
unknown. Keep cycles visible; no member of an unresolved native blocker cycle
is ready.

Return canonical nodes and edges, Ready Frontier, current blockers, coverage,
unresolved effects, and Verification gaps only. Do not add repair suggestions,
operator-choice menus, workers, models, effort, worktrees, stacks, or
sequencing. An orchestrator must re-read the tracker before dispatch and after
any relevant issue or pull-request change.

In the returned report, lead with one plain summary sentence that restates the
facts and adds nothing, and present the Ready Frontier under the heading
"Ready to start now", listing issues by reference and title. The term and its
derivation rules stay internal.

## Prove completion separately

Status, a checked box, or a merged pull request is evidence to inspect, never
proof by itself. Read the current issue's unchanged `Verification` criteria and
match each criterion to current trusted evidence: provider state, a repository
check or artifact, or fresh authorized owner attestation. Name any unsupported
criterion as a Verification gap. When reporting, phrase each gap as what is
still unproven and what would prove it: "Not yet confirmed: [criterion]. Would
be proven by [check, artifact, or owner confirmation]." Keep "attestation",
"trusted evidence", and "unsupported criterion" out of the report itself.

A leaf may receive a separately approved completion preview only when its own
criteria have evidence and it has no current unresolved blocker. A parent also
requires complete family coverage, every required leaf completed with its own
proof, no unresolved required blocker, every waiver explicitly approved and
still applicable, and evidence for the parent's outcome-level Verification.

Editing Verification invalidates the issue's completion analysis. Preview and
apply that edit as its own effect, read it back, then start a new completion
analysis, preview, and approval round. Never combine the edit and lifecycle
change in one batch.

Before a lifecycle effect in a synchronized repository, name every known
shadow, parent, and child status cascade. Linear teams may optionally complete
a parent when all sub-issues complete or complete remaining children when a
parent completes, and GitHub synchronization can propagate status changes. If
the applicable automation posture or cascade cannot be observed, return the
lifecycle effect as `manual`; current issue text is not proof of the setting.
Release A emits no closing keyword and never treats merge automation as
completion authority.

Synchronization evidence is not limited to declared policy. When the current
canonical readback or issue content of a GitHub-canonical issue carries
synchronization markers — a synced-copy banner, a tracker cross-link block, or
integration-authored sync metadata — treat the repository as synchronized for
lifecycle purposes even though Release A trusted policy cannot declare a
GitHub-canonical mapping. The markers are facts to inspect, never route or
authority selectors: name the apparent shadow in the preview, and because the
cascade posture of an undeclared synchronization cannot be observed, return
that lifecycle effect as `manual`.

Completion: the result lists evidence and gaps against unchanged criteria. A
lifecycle change is only a new exact, directly approved effect with observable
cascades; otherwise the issue remains current and the effect is `manual`.
