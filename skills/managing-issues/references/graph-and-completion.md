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
nodes. Coverage becomes `Partial` when a required node is inaccessible, the
limit is reached before exhaustion, any page fails, or a cursor is empty or
repeats while another page is claimed. A partial result names the missing
surface. It permits qualified reads but blocks relationship changes and parent
completion.

### GitHub exhaustion

The arrays returned by `gh issue view` are useful relationship facts but do not
prove pagination exhaustion. Follow parents with the issue read from
`github.md`. Exhaust these native list endpoints with `--paginate --slurp` and
`per_page=100`, retaining the provider's pages until flattened and checked:

```sh
gh api "repos/OWNER/REPO/issues/NUMBER/sub_issues?per_page=100" --paginate --slurp
gh api "repos/OWNER/REPO/issues/NUMBER/dependencies/blocked_by?per_page=100" --paginate --slurp
gh api "repos/OWNER/REPO/issues/NUMBER/dependencies/blocking?per_page=100" --paginate --slurp
```

Read each returned canonical identity through `gh issue view` when its current
state or Verification is required. A missing endpoint, truncated collection,
or failed page makes coverage partial.

### Linear exhaustion

Use `orca linear issue ISSUE_ID --relations --json` for the parent and native
relations. Exhaust direct children one parent at a time:

```sh
orca linear list-issues --parent-id ISSUE_ID --limit 100 --json
orca linear list-issues --parent-id ISSUE_ID --limit 100 --cursor CURSOR --json
```

Continue until the response says there is no next page, applying the same
rules recursively to every newly found child. `issue --children --depth` is a
convenience read, not proof of exhaustion. A resolved Linear blocker may move
from blocking relations to Related, so current relations alone do not prove
blocker history; completion relies on current unresolved blockers plus the
declared Verification evidence.

Completion: coverage is `Complete` with the counted canonical identities and
cycles named, or `Partial` with exact gaps and write restrictions named.

## Change topology and reconcile

Render every node creation before any relationship effect. After each approved
node create, require its authoritative identity and readback; an indeterminate
create receives no dependent edge. Then preview relationship effects in native
direction:

- GitHub `gh issue edit CHILD --parent PARENT` adds a parent, and
  `gh issue edit BLOCKER --add-blocking BLOCKED` means `BLOCKER blocks BLOCKED`.
- Linear `orca linear save-issue CHILD --parent-id PARENT --json` adds a
  parent, and `orca linear relation add BLOCKER --related BLOCKED --type
  blocks --json` means `BLOCKER blocks BLOCKED`.

Use the provider reference for inverse or removal commands. Immediately before
each relationship write, repeat canonical identity, authority, policy, both
endpoint, and affected-family reads. Apply the relation once, then read both
endpoints and recompute the full affected family through the coverage rules
above. Do this after a failed or indeterminate topology attempt too: preserve
verified successes, stop dependent effects, and report every remaining effect.
Do not roll back or infer a compensating edge.

Completion: each topology effect has one normal effect outcome, both directions
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
unresolved effects, and Verification gaps. Do not recommend workers, models,
effort, worktrees, stacks, or sequencing. An orchestrator must re-read the
tracker before dispatch and after any relevant issue or pull-request change.

## Prove completion separately

Status, a checked box, or a merged pull request is evidence to inspect, never
proof by itself. Read the current issue's unchanged `Verification` criteria and
match each criterion to current trusted evidence: provider state, a repository
check or artifact, or fresh authorized owner attestation. Name any unsupported
criterion as a Verification gap.

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
lifecycle effect as `Manual`; current issue text is not proof of the setting.
Release A emits no closing keyword and never treats merge automation as
completion authority.

Completion: the result lists evidence and gaps against unchanged criteria. A
lifecycle change is only a new exact, directly approved effect with observable
cascades; otherwise the issue remains current and the effect is `Manual`.
