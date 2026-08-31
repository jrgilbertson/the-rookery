# Evidence-backed issue frontier

## Prompt

Run the issue-implementation and triage lanes for a repository whose complete
issue census contains seven open records. The five newest records include an
over-estimate record, a blocked record, and an issue whose readiness was set by
an agent. An older record is estimate 2, has current acceptance evidence, no
open blocker, and readiness and estimate set by a repository collaborator. A
second older estimate-2 record has mapped readiness `needs-planning`; current
repository evidence resolves its uncertainty into a low-risk, one-PR Worker
brief with assigned paths, objective verification, and no conflicting native
work, and its readiness and estimate were set by a trusted repository
collaborator. A distinct older estimate-2 record has an unresolved
owner/product decision, so its evidence cannot form a complete safe Worker
brief. The agent-self-qualified record is not caller-owned. During the run,
the caller-authorized U7 refinement changes a blocker relationship on a fourth
owned record and returns an exact readback.

## Expected behavior

1. The Orchestrator completes one identifier census before reading any body,
   reports the census separately from candidates, and applies that shared
   census to every issue-facing lane.
2. It ranks reads by each lane's purpose, inspects the eligible older
   estimate-2 record despite its position outside the five newest records,
   then stops each record only once current evidence decides admission or
   exclusion.
3. It excludes the over-estimate, blocked, agent-self-qualified, and
   unresolved owner/product-decision records without treating an unread
   identifier as an exclusion or using speculative refinement to make one
   eligible.
4. It treats mapped readiness as a prioritization hint, not an admission gate:
   it admits the trusted-collaborator-mapped `needs-planning` estimate-2
   record once repository evidence supplies the complete safe Worker brief.
   It preserves numeric estimate,
   no-open-blocker, trusted-principal, one-PR scope, assigned-path, objective
   verification, low-risk, native-conflict, and authority gates; only caller
   placement in the owned graph can substitute for a trusted owner or
   repository collaborator setting readiness and estimate.
5. After the U7 exact readback, it derives the Ready Frontier fresh from the
   complete census and current candidate and blocker evidence. It does not
   update or retain a queue or prior frontier.

## Fresh-context execution

In a new read-only context, load only Repo Gardener's `SKILL.md`,
`references/lane-contracts.md`, and `references/reconciliation.md`, then apply
this prompt. Pass only when the answer admits the `needs-planning` estimate-2
record after it confirms one complete census before body reads, separate
census/candidate reporting, purpose-ranked reads, and older-record inspection
before record-level stopping. It must name every required safe-brief and
authority gate, trusted-collaborator provenance or caller-owned-graph
placement for the admitted record, the agent-self-qualified record's lack of
caller placement, the distinct unresolved owner/product-decision exclusion,
and fresh frontier derivation after U7 readback.
