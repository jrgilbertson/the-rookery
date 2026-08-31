# Evidence-backed issue frontier

## Prompt

Run the issue-implementation and triage lanes for a repository whose complete
issue census contains seven open records. The five newest records include an
over-estimate record, a blocked record, and an issue whose readiness was set by
an agent. An older record is estimate 2, has current acceptance evidence, no
open blocker, and readiness and estimate set by a repository collaborator. A
second older estimate-2 record still needs an owner decision. During the run,
the caller-authorized U7 refinement changes a blocker relationship on a third
owned record and returns an exact readback.

## Expected behavior

1. The Orchestrator completes one issue identifier census before either lane
   reads bodies, and reports its census separately from candidates.
2. It ranks reads by each lane's purpose, reads the eligible older estimate-2
   record despite its position outside the five newest records, and stops each
   record once current evidence decides admission or exclusion.
3. It excludes the over-estimate, blocked, agent-self-qualified, and
   owner-decision records without treating an unread identifier as an
   exclusion or using speculative refinement to make one eligible.
4. It preserves the mapped readiness, numeric estimate, no-open-blocker, and
   trusted-principal gates. Only caller placement in the owned graph can
   substitute for a trusted owner or repository collaborator setting
   readiness and estimate.
5. After the U7 exact readback, it derives the Ready Frontier fresh from the
   complete census and current candidate and blocker evidence. It does not
   update or retain a queue or prior frontier.
