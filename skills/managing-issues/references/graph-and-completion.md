# Issue graphs, readiness, and completion

Load this reference only when relationships, readiness, or completion matter.
Use the canonical tracker's native parent and blocker relationships. Keep the
derived graph in the current response; the tracker remains the durable record.

## Shape only the useful graph

Use the issue set that passed the main workflow's decomposition gates. Keep a
standalone leaf parentless. When several leaves deliver one whole outcome,
attach them to that outcome's parent. Add another level only when a child owns a
distinct sub-outcome that itself needs several leaves. This is the shallowest
useful graph; it has no fixed depth limit.

Any node with children is a parent, including a nested sub-outcome, and carries
no estimate. Only childless implementation leaves receive analyzed estimates.
Every node still receives its own Problem, Scope, Verification, priority,
labels, readiness, and native graph position.

## Establish complete coverage

Start at the requested canonical issue. Walk its parent chain to the top of the
family, then read every descendant and every internal `blocks` or `blocked-by`
edge. For an edge crossing the family boundary, read the one external endpoint
needed to decide whether it remains an unresolved blocker. Do not adopt that
external issue's family.

Track canonical provider identities in a visited set, count each identity once,
preserve cycles as edges, and never revisit a node. Stop at 250 identities,
including one-hop external blockers. Coverage is `partial` when any required
node or page is inaccessible, the limit is reached before exhaustion, a page
fails, or a next cursor is empty or repeats. Name the exact missing surface.
Partial coverage permits qualified facts but blocks topology changes, Ready
Frontier claims, and parent completion.

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

Never use a stored readiness representation as evidence for the derived
posture. Compare it with the derived result. Intended metadata contains exactly
one of the three configured readiness representations; a missing, duplicate, or
stale representation is a separate previewed correction.

The Ready Frontier contains only required, open implementation leaves whose
derived posture is `ready` and whose native blockers are all resolved. Parents
never enter it. Neither do completed or canceled leaves,
blocked leaves, unknown-readiness leaves, or members of an unresolved blocker
cycle. Report it only from complete current coverage, name the set explicitly,
and list an unattached intended node separately as unresolved topology.

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

An indeterminate create receives no edge. Before a new proposal, read any exact
canonical identity or provider receipt returned by that one attempt. Never
match by title, body, author, time, or similarity.

## Synchronization

For native-link resolution, canonical-provider write direction, and projection
behavior, see [the provider/sync reference](linear-and-sync.md#provider-managed-synchronization).

## Prove completion separately

Use the current approved Verification content from the latest exact canonical
readback. A status, checked box, linked change, or child completion is evidence
to evaluate, never proof by itself. Match every criterion to current provider
state, a current repository check or artifact, or direct owner confirmation.
State each gap as what remains unconfirmed and what would prove it.

A leaf is eligible for a completion effect only when every criterion is proven
and no blocker remains unresolved. A parent additionally requires complete
family coverage, proven completion of every required leaf, no unresolved
required blocker, every explicit waiver still applicable, and evidence for its
own outcome-level Verification.

A Verification edit is its own visible, approved, read-back effect. It
invalidates the earlier completion assessment. Reassess from the new canonical
readback, then show any lifecycle change in a separate batch with separate
approval.

Before a lifecycle preview, discover every provider or provider-managed
synchronization cascade that can change a parent, child, or projection. List
each observable cascade as an intended effect even though Managing Issues writes
only the canonical tracker. If the cascade posture cannot be observed, stop
before an executable lifecycle preview. Never use a closing keyword as
completion authority.

Return only canonical nodes and edges, coverage, derived readiness, blockers,
Ready Frontier, exact effect outcomes, and Verification evidence or gaps. Do
not add implementation recommendations or persist an execution handoff.
