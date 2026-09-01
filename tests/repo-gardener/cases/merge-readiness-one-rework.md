# Native PR facts and same-Worker repair

Provenance: ownerless scheduled Repo Gardener reports native PR facts and
preserves its same-Worker repair boundary; merge readiness remains a later
owner interaction.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A managed ownerless repo-gardener run has one Worker PR. Native check and
> review facts are freshly readable. Evaluate each scenario independently.
>
> 1. The PR's review history is empty and a required human approval is absent.
> 2. A native current-head check identifies a named failing test at `b1`.
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
> 5. `checking-merge-readiness` is installed and would present its normal menu.

## Expected behavior

- [ ] Scenario 1 reports the native absence and owner attention without trying
      to synthesize a merge decision.
- [ ] Scenario 2 completes Phase A before sending the focused finding and
      preserves the exact-head, assigned-path, protected-path, authority, and
      provider-lease gates through the same Worker's `b2` update.
- [ ] Scenario 3 stops the affected action for exact-head drift; it does not
      redirect the finding, act on `c2`, or guess that the Worker remains
      authorized.
- [ ] Scenario 4 closes truthfully because no focused repair can help. It does
      not create a follow-up issue or add a retry rule.
- [ ] Scenario 5 does not invoke the merge-checking skill in the ownerless
      scheduled run. The morning projection contains native PR, check, review,
      and owner-attention facts, leaving that skill's normal menu to a later
      owner interaction.
- [ ] No scenario assigns finding identities, fingerprints, reviewer caps,
      JSON or envelope formats, schemas, counters, registries, state machines,
      progress records, or a parallel workflow ledger.
- [ ] No scenario merges, releases, deploys, creates a follow-up issue, or
      messages a customer.
