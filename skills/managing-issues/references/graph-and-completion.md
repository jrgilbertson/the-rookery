# Issue Graphs, Readiness, and Completion

Load this reference before splitting work into multiple issues, or whenever
relationships, readiness, or completion matter. Use the canonical tracker's
native parent and blocker relationships. Keep the derived graph in the current
response; the tracker remains the durable record.

## Decompose only when needed

Decompose only when the outcome needs more than one reviewable deliverable:

- Keep work that fits one independently deliverable, reviewable pull request as
  one implementation leaf. A stacked series is one leaf only when no PR in the
  stack delivers independently observable behavior; otherwise each such PR is
  its own leaf.
- Split larger work into vertical outcomes that each deliver observable
  behavior through every necessary layer. A database, API, UI, or test layer
  alone is not a useful child unless it is independently valuable and
  verifiable.
- Ask what can be demonstrated when each leaf closes. Merge or reshape any
  leaf that has no independent answer.
- Add a blocker only when the blocked issue cannot start or finish safely
  first. Keep preferences and convenient ordering out of the dependency graph.
- For a wide refactor that cannot stay working as vertical slices, use
  expand-migrate-contract: introduce the new form alongside the old, migrate
  consumers in independently safe batches, then remove the old form after
  every migration finishes.

Before accepting a multi-issue shape, show a compact decomposition check for
each leaf: its demonstrable outcome, why it remains separate, and every
genuine blocker with the reason. Merge, reshape, or reconnect any row that
fails the five rules above before previewing tracker effects.

## Shape only the useful graph

Use the issue set that passed the decomposition gate above. Keep a standalone
leaf parentless. When several leaves deliver one whole outcome, attach them to
that outcome's parent. Add another level only when a child owns a distinct
sub-outcome that itself needs several leaves. This is the shallowest useful
graph; it has no fixed depth limit.

Any node with children is a parent (including a nested sub-outcome) and takes
no estimate; only implementation leaves take estimates, following `SKILL.md`.
A childless research, decision, or person-action issue remains a leaf of the
graph without an estimate. Every node still gets its own Problem, Scope,
Verification, four scores, priority, labels, readiness, project, assignee, and
native graph position, leaving project or assignee empty only where `SKILL.md`
and `prioritization.md` allow.

## Establish complete coverage

Start at the requested canonical issue. Walk its parent chain to the top of the
family, then read every descendant and every internal `blocks` or `blocked-by`
edge. For an edge crossing the family boundary, read the one external endpoint
needed to decide whether it remains an unresolved blocker. Do not adopt that
external issue's family. In the same traversal, read each implementation
leaf's four scores through the provider reference's score read. A failed score
read makes that leaf's scores unreadable. It does not make coverage partial.

Track canonical provider identities in a visited set, count each identity once,
preserve cycles as edges, and never revisit a node. Stop at 250 identities,
including one-hop external blockers. Coverage is `partial` when any required
node or page is inaccessible, the limit is reached before exhaustion, a page
fails, or a next cursor is empty or repeats. Name the exact missing node or
page. Partial coverage permits qualified facts but blocks topology changes,
Ready Frontier claims, and parent completion.

Use the selected provider reference for exhaustive native reads. Relationship
arrays embedded in an issue read are facts, not proof that a collection is
exhausted. A current exact endpoint read may prove one requested relationship
`already_satisfied`; that no-op does not authorize other topology changes under
partial coverage.

## Derive readiness from current content

Use the Problem, Scope, and Verification from the latest complete canonical
readback together with the node's current graph role:

- `needs-discovery` when the problem or intended outcome is not understood.
- `needs-planning` when the problem is understood but Scope, Verification,
  decomposition, required metadata choices, or native relationships remain
  unsettled.
- `ready` when Problem, Scope, Verification, decomposition, required metadata
  choices, and native graph position are settled for the issue's role. A parent
  is ready when its whole outcome and child graph are settled; a leaf is ready
  when it can be completed and checked.

Never use a stored readiness label as evidence for derived readiness. Compare
it with the derived result. Intended metadata contains exactly one of the
three configured readiness labels; a missing, duplicate, or stale label is a
separate previewed correction.

The Ready Frontier contains only required, open implementation leaves whose
derived readiness is `ready` and whose native blockers are all resolved.
Parents never enter it, nor do completed or canceled leaves, blocked leaves,
unknown-readiness leaves, or members of an unresolved blocker cycle. Report
it only from complete current coverage, name the set, and list any unattached
intended node separately as unresolved topology.

List the Ready Frontier in leverage order, highest first, showing each leaf's
four scores. Leverage is (impact × confidence) ÷ (verification effort × undo
cost), worked out for the listing from the scores read in this traversal and
never stored. Above the listing, name every ready leaf that scores 3 on
impact, wherever it ranks. A ready leaf with any score absent, unresolved, or
unreadable goes after the ranked leaves, flagged with which of the three
applies to which score; never give it default scores. List leaves that tie on
leverage together in tracker identifier order and say that they tie. List the
flagged leaves in tracker identifier order. Order changes only the
listing. The membership rules above stay as they are, and every qualifying
leaf appears.

## Preview and apply topology

Check capabilities before showing an executable graph preview. Probe every
native relationship the proposed graph needs. If any capability is unavailable,
write no graph node. A smaller standalone set is a new proposal with a new
approval cycle.

Show the complete deterministic effect order. Place all node creates or updates
before relationships. After approval, apply nodes before relationships and
require an exact canonical identity and readback for every new node before any
edge that references it. Immediately before each edge, repeat the provider,
target, endpoint, material-field, and affected-family reads required by the
provider reference. Apply the edge once, read both endpoints back, then
recompute the affected family.

Follow the shared lifecycle's first-stop rule. For graph results, inventory the
confirmed `applied` and `already_satisfied` effects, the stopping `failed` or
`indeterminate` effect, and all `unapplied` effects. Do not roll back or infer
a compensating relationship. `unapplied` says only that this batch did not run
the effect; the latest complete canonical read still determines current graph
state.

An indeterminate create receives no edges. Recover it under `SKILL.md` by
reading any exact canonical identity or receipt returned by that attempt,
without similarity matching.

## Prove completion separately

Use the current approved Verification content from the latest exact canonical
readback. A status, checked box, linked change, or child completion is evidence
to evaluate, never proof by itself. Match every criterion to current provider
state, a current repository check or artifact, or direct owner confirmation.
State each gap as what remains unconfirmed and what would prove it.

A leaf is eligible for a completion effect only when every criterion is proven
and no blocker remains unresolved. A parent also requires complete family
coverage, proven completion of every required leaf, no unresolved required
blocker, every explicit waiver still applicable, and evidence for its own
outcome-level Verification.

A Verification edit is its own visible, approved, read-back effect. It
invalidates the earlier completion assessment. Reassess from the new canonical
readback, then show any lifecycle change in a separate batch with separate
approval.

Before a lifecycle preview, list every cascade the provider reports as an
intended effect, including changes to a parent or child, and any known automatic
metadata change. Apply the shared authorization rule to the complete result.
Read back each reported effect that the provider exposes. Do not inspect,
predict, repair, or block on effects the provider does not report; Managing
Issues writes only the canonical tracker. Reading a canonical issue's own
relationships is ordinary readback, not inspection of an unreported effect.
Never treat a closing keyword as proof of completion.

Return only canonical nodes and edges, coverage, derived readiness, blockers,
the ordered Ready Frontier, exact effect outcomes, and Verification evidence
or gaps, leaving delivery planning and execution handoffs to downstream
workflows.
