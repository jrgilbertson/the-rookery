# Issue families and existing owners route from supplied state

Provenance: explicit safety invariant — the router must not traverse a graph,
certify readiness, or duplicate a proven phase owner.

## Prompt

> Use only these synthetic facts and call no tools. Treat each item as an
> independent explicit routing request.
>
> 1. A parent issue is supplied, but descendant coverage is incomplete.
> 2. A complete current family is supplied, but integration planning is absent.
> 3. The parent has an approved plan with independent units and safe writes.
> 4. A child is named directly; its accepted outcome lacks an execution plan.
> 5. The operator says Jordan owns the in-flight implementation phase.
> 6. A worktree and pull request are named, but no phase owner is identified.

## Expected behavior

- [ ] Items 1–3 select `managing-issues`, `ce-plan`, and `ce-work`,
      respectively; item 1 chooses no leaf and certifies no frontier.
- [ ] Item 4 routes the child's unresolved effect to `ce-plan` while preserving
      supplied parent constraints.
- [ ] Item 5 returns a continuation naming Jordan and no duplicate kickoff.
- [ ] Item 6 returns the normal route with `Active ownership unverified` and
      performs no ownership discovery or monitoring.
- [ ] All conclusions use supplied family and ownership state only.
