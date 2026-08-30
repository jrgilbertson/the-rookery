# Report-only readiness and same-Worker repair

Provenance: the prior package reached an interactive merge-readiness menu and
then imposed a fixed extra-rework rule instead of judging the current Worker
and current facts.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A managed repo-gardener run has one Worker PR that has reached `pr_ready`.
> Native checks pass. Evaluate each scenario independently. A direct readiness
> assessment and an installed report-only `checking-merge-readiness` assessment
> both return a recommendation and ordinary prose findings for the exact head.
>
> 1. A direct assessment of head `a1` reports `debug` because review history is
>    empty and required human approval is absent.
> 2. A report-only assessment of current head `b1` reports `debug` with a named
>    failing test in the diff. Worker W still has the opening authority. W fixes
>    it without updating its existing PR, reruns its assigned local verification,
>    and responds with repaired head `b2`. The hosted PR remains at `b1` before
>    authorization. The fresh local branch/full-HEAD, diff, assigned local
>    verification, and tracker reads identify `b2`, while the hosted PR still
>    reads `b1`; the repaired paths remain inside W's slice and outside
>    protected paths. After exact `b2` authorization, W updates its existing PR;
>    native reads confirm hosted `b2` and fresh checks before reassessment.
> 3. A report-only assessment names an actionable test failure on head `c1`,
>    but a fresh read before the Worker instruction finds full HEAD `c2`.
> 4. A report-only assessment names a concern, but the fresh facts after the
>    Worker response show no focused repair could improve it.
> 5. `checking-merge-readiness` is unavailable, while direct current-head facts
>    suffice to recommend `merge` with no actionable finding.

## Expected behavior

- [ ] Scenario 1 records the process caps and does not chase either one.
- [ ] Scenario 2 sends the named test finding in plain prose to Worker W. W
      holds the PR update and reruns assigned local verification before
      returning `b2`. At pre-authorization, all five native fact reads show
      the local branch/full-HEAD, diff, and assigned local verification at
      `b2`; tracker reads confirm unchanged Worker authority or relevant
      canonical state; and the hosted PR still reads `b1`. The Orchestrator
      revalidates W's slice and protected paths, authorizes exact head `b2`,
      then W updates its existing PR. Native reads then confirm hosted `b2`
      and fresh checks before reassessment. The report neither shows a menu
      nor merges.
- [ ] Scenario 3 stops the affected action for exact-head drift; it does not
      redirect the finding, act on `c2`, or guess that W remains authorized.
- [ ] Scenario 4 closes truthfully in plain prose because no focused repair can
      help. It does not create a follow-up issue or add a retry rule.
- [ ] Scenario 5 uses direct assessment as the fallback and names no absent
      helper gap because the current facts are sufficient.
- [ ] No scenario assigns finding identities, fingerprints, reviewer caps,
      JSON or envelope formats, schemas, counters, registries, state machines,
      progress records, or a parallel workflow ledger.
- [ ] No scenario merges, releases, deploys, creates a follow-up issue, or
      messages a customer.
