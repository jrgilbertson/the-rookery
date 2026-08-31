# Evidence-backed issue frontier

## Prompt

Run the issue-implementation and triage lanes for a repository whose complete
issue census contains exactly eight open records: five newest and three older.
The five newest include an over-estimate record; a caller-owned estimate-2
record that is otherwise eligible but has one current native blocker; and an
issue whose readiness and estimate were set by an agent. An older record is
estimate 2, has current acceptance evidence, no open blocker, and mapped
readiness and estimate whose current effective label setters are proven
repository collaborators by a complete paginated GitHub issue-event history.
A second older estimate-2 record has mapped readiness `needs-planning`;
current repository evidence resolves its uncertainty into a low-risk, one-PR
Worker brief with assigned paths, objective verification, and no conflicting
native work, and the same complete history proves its current effective label
setters are trusted repository collaborators. A distinct older estimate-2
record has an unresolved owner/product decision, so its evidence cannot form a
complete safe Worker brief. The agent-self-qualified record is not
caller-owned. During the run, the caller-authorized U7 refinement removes the
blocker from the caller-owned otherwise eligible record and returns an exact
readback.

## Expected behavior

1. The Orchestrator completes one identifier census before reading any body,
   reports the census separately from candidates, and applies that shared
   census to every issue-facing lane.
2. Each non-empty issue-facing lane performs its own purpose-ranked current
   body or relationship read from the shared census. It inspects the eligible
   older estimate-2 record despite its position outside the five newest
   records, then stops each record only once current evidence decides admission
   or exclusion.
3. Before U7, it excludes the over-estimate, blocked, agent-self-qualified,
   and unresolved owner/product-decision records without treating an unread
   identifier as an exclusion or using speculative refinement to make one
   eligible.
4. It treats mapped readiness as a prioritization hint, not an admission gate:
   it admits the trusted-collaborator-mapped `needs-planning` estimate-2
   record once repository evidence supplies the complete safe Worker brief.
   It preserves numeric estimate,
   no-open-blocker, trusted-principal, one-PR scope, assigned-path, objective
   verification, low-risk, native-conflict, and authority gates. Provenance
   requires a complete provider-native metadata history or audit read that
   proves the current effective mapping setter trusted; for GitHub labels this
   is the complete paginated issue-event history. Only caller placement in the
   owned graph can substitute for that proof.
5. After the U7 exact readback, it derives the Ready Frontier fresh from the
   complete census and current candidate and blocker evidence, and includes
   the formerly blocked caller-owned otherwise eligible record. It does not
   update or retain a queue or prior frontier.

## Fresh-context execution

In a new read-only context, load only Repo Gardener's `SKILL.md`,
`references/lane-contracts.md`, and `references/reconciliation.md`, then apply
this prompt. Grade the five numbered checks above. Pass only when the answer
admits the `needs-planning` estimate-2 record after it confirms one complete
census before body reads, separate census/candidate reporting, and each
non-empty issue-facing lane's own purpose-ranked body or relationship read,
including older-record inspection before record-level stopping. It must name
every required safe-brief and authority gate; complete provider-native
provenance proving the current effective trusted mapping setter or
caller-owned-graph placement for the admitted record; the agent-self-qualified
record's lack of caller placement; the distinct unresolved owner/product
decision exclusion; and fresh post-readback inclusion of the formerly blocked
caller-owned otherwise eligible record in a newly derived frontier.
