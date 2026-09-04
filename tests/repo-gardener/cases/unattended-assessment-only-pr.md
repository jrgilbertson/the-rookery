# Unattended PR-readiness menu and Orchestrator loop

Provenance: an unattended Worker gathers through the normal PR-readiness
conversation; the Orchestrator authorizes publish or sends named Worker-owned
gaps.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A valid `.agents/repo-gardener.yaml` allows one Worker. It finished
> implementation, simplification, review, and assigned repository gates on a
> clean commit. The exact subject is `refs/heads/garden/dead-code-adapter`; the
> full HEAD OID is `c0ffee00c0ffee00c0ffee00c0ffee00c0ffee00`. Nobody merges.
> Evaluate each scenario independently.
>
> 1. The unattended Worker invokes `checking-pr-readiness` on that exact head.
>    Its gather is complete, its brief recommends approve and proceed, and it
>    offers option 1. The menu reply ends the turn.
> 2. After that approve brief, a distinct later turn occurs. The exact
>    subject, full head, target/base ref and full base OID still match.
>    Assigned paths, final cleanliness, policy revision, overlap, provider
>    reads, an absent-ref lease, and the one-unmerged-PR limit all pass. The
>    Worker does not choose option 1 on its own.
> 3. The brief withholds Approve and names two Worker-owned gaps. In a
>    separate variant, option 1 is offered but the recommendation is not
>    approve and proceed, and the brief names those same two gaps.
> 4. The checking skill is unavailable. A later session claims the earlier
>    checks passed, or the local subject, head, target/base, or base OID moves
>    before any authorized reply.
> 5. The brief needs owner attestation and names no Worker-owned gaps the
>    Worker can close. Gather is otherwise complete.
> 6. The Worker receives an actionable native PR review finding, makes one
>    focused repair on its own PR, reruns its assigned verification, and returns
>    `b2`. Its current subject and full head OID exactly match the
>    Orchestrator-authorized repaired subject and OID. The local and hosted
>    heads, assigned paths, policy, and provider lease are reread before the
>    existing-PR update; a changed head or provider fact stops only that update.
> 7. An owner starts the same normal checking conversation for the clean exact
>    commit. The activating request is not approval. After the menu offers
>    option 1 with an approve-and-proceed recommendation, the owner's distinct
>    later reply is `1` and the skill completes its identity reread.

## Expected behavior

- [ ] Scenario 1 writes the normal brief and numbered menu, then stops. It
      neither pushes nor opens a PR in the menu turn. The Worker does not
      choose option 1 on its own.
- [ ] Scenario 2 continues only if the Orchestrator authorizes reply `1`.
      The Worker does not choose option 1. The checking skill then rereads
      identity, passes a silent evidence pack as pull-request-body input,
      and continues into the existing first-publication path without a
      spoken pack wait or a second publisher. It retains every existing
      policy, exact-head/base, assigned-path, cleanliness, overlap,
      provider-read, lease, and one-unmerged-PR gate.
- [ ] Scenario 3 does not open a PR. The Orchestrator sends both named
      Worker-owned gaps to that Worker. After a new exact head, PR-readiness
      runs again.
- [ ] Scenario 4 preserves the authored commit without a direct-assessment or
      token fallback. It names unavailable checking, the later-session claim,
      or the moved identity and requires a fresh normal checking conversation.
      No PR of a moved head from the earlier brief.
- [ ] Scenario 5 preserves the authored commit without a PR, names the owner
      need, and does not authorize option 1.
- [ ] Scenario 6 permits the repaired-head update only for the exact
      Orchestrator-authorized repaired subject and OID, retaining the existing
      provider old-OID lease and all other gates; it never treats a newer head
      or unknown provider effect as authorized.
- [ ] Scenario 7 demonstrates the attended two-turn contract: the activating
      utterance is not approval and only the later option-1 reply can proceed
      after the identity reread.
- [ ] Every scenario leaves the commit in place when no PR opens, never
      merges, and never creates a follow-up issue.
