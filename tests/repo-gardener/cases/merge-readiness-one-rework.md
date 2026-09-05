# Native PR facts and unattended merge-readiness

Provenance: ownerless scheduled Repo Gardener reports native PR facts, preserves
its same-Worker repair boundary, invokes merge-readiness after a PR exists, and
never selects Proceed to merge.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A managed ownerless repo-gardener run has one Worker PR. Native check and
> review facts are freshly readable. `checking-merge-readiness` is installed.
> Evaluate each scenario independently.
>
> 1. The PR's review history is empty and a required human approval is absent.
>    Merge-readiness would cap at debug because of that empty review.
> 2. A native current-head check identifies a named failing test at `b1`,
>    this Worker's last authorized successful push with exact readback.
>    Phase A verifies local branch/full-HEAD, hosted PR head, and Worker
>    authority still match `b1` before forwarding the finding. In Phase B, the
>    Worker repairs, reruns assigned local verification, and returns `b2`. The
>    five post-response reads show local branch/full-HEAD and diff at `b2`,
>    local verification for `b2`, unchanged tracker authority or relevant
>    canonical state, and hosted `b1`. It then validates the Worker's slice and
>    protected paths, authorizes exact `b2`, updates its existing PR under an
>    atomic lease expecting `b1`, and rereads hosted `b2` plus current checks.
> 3. A native finding names a test failure at `c1`, but the fresh pre-instruction
>    read finds full HEAD `c2`.
> 4. Current native review facts name a concern, but the fresh facts after the
>    Worker response show that no focused repair could improve it.
> 5. Installed `checking-merge-readiness` writes its normal brief and numbered
>    menu for this PR.
> 6. That brief recommends merge and offers Proceed to merge.
> 7. That brief recommends debug and names two Worker-owned findings.
> 8. Compare a new PR whose initial remote ref is absent with an adopted PR
>    captured at `a0`. The same Worker receives exact authorization for `a1`,
>    pushes with the appropriate explicit lease, and reads back `a1` exactly.
>    A later repair is authorized at `a2`. All other publication gates pass.
>    Independently vary the remote before the second push: unchanged `a1`,
>    a divergent competing commit, a rewind to `a0`, or unexpected absence.
> 9. The first authorized push reports success, but readback fails, is
>    unavailable, or returns another OID. A later read happens to show `a1`.
>    Compare this with an exact initial readback and with an unapproved `a2`.
> 10. The first repair changes a forbidden path relative to the original
>     scope baseline. The second repair changes only an allowed path relative
>     to `a1`, leaving the forbidden change in its cumulative diff.

## Expected behavior

- [ ] Scenario 1 invokes merge-readiness. It does not invent a merge decision
      outside that brief. Empty review and missing human approval are
      owner-needed work the Worker cannot close, so the Orchestrator stops
      that loop and does not select option 1.
- [ ] Scenario 2 completes Phase A before sending the focused finding and
      preserves the exact-head, assigned-path, protected-path, authority, and
      provider-lease gates through the same Worker's `b2` update.
- [ ] Scenario 3 stops the affected action for exact-head drift; it does not
      redirect the finding, act on `c2`, or guess that the Worker remains
      authorized.
- [ ] Scenario 4 closes truthfully because no focused repair can help. It does
      not create a follow-up issue or add a retry rule.
- [ ] Scenario 5 invokes the merge-checking skill in the ownerless scheduled
      run after the PR exists. The closing comment still contains native
      PR, check, review, and owner-attention facts.
- [ ] Scenario 6 stops and leaves merge to the owner. Proceed to merge is not
      selected.
- [ ] Scenario 7 sends both named Worker-owned findings to that Worker,
      publishes the repaired exact head under the existing lease, then that
      same Worker invokes merge-readiness again on the repaired exact head.
      Nothing merges.
- [ ] No scenario assigns finding identities, fingerprints, reviewer caps,
      JSON or envelope formats, schemas, counters, registries, state machines,
      progress records, or a parallel workflow ledger.
- [ ] No scenario merges, releases, deploys, creates a follow-up issue, or
      messages a customer.

- [ ] Scenario 8 applies one rule to both PR kinds: only after successful own
      push and exact readback does the expected remote OID become `a1`; the
      authorized second push leases `a1` and advances to `a2` only after its
      own successful push and exact readback.
- [ ] Divergent movement, rewind, or unexpected absence stops the affected
      publication without recapture or retry. A complete unchanged `a1`
      read permits the authorized second push; an already verified expected
      OID equal to the authorized head needs no push and does not advance.
- [ ] Scenario 9 never advances the expectation after uncertain readback,
      infers successful own publication from a later matching OID, or pushes
      unapproved `a2`. Exact readback advances only the successful authorized
      push it verifies.
- [ ] Scenario 10 stops on the cumulative forbidden path. The original base
      or adoption-dispatch OID remains the scope baseline across every repair;
      the advancing lease expectation never replaces it.
