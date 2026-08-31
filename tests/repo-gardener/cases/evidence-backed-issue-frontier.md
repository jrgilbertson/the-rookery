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
work. During the run, the caller-authorized U7 refinement changes a blocker
relationship on a third owned record and returns an exact readback.

## Expected behavior

1. The Orchestrator completes one issue identifier census before either lane
   reads bodies, and reports its census separately from candidates.
2. It ranks reads by each lane's purpose, reads the eligible older estimate-2
   record despite its position outside the five newest records, and stops each
   record once current evidence decides admission or exclusion.
3. It excludes the over-estimate, blocked, and agent-self-qualified records
   without treating an unread identifier as an exclusion or using speculative
   refinement to make one eligible.
4. It treats mapped readiness as a prioritization hint, not an admission gate:
   it admits the `needs-planning` estimate-2 record once repository evidence
   supplies the complete safe Worker brief. It preserves numeric estimate,
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
record after it names every required safe-brief and authority gate, excludes
the three disqualified records, and derives the frontier fresh after U7
readback.
