# Issue families and existing owners route from supplied state

Provenance: explicit safety invariant — the router must not traverse a graph,
certify readiness, or duplicate a proven phase owner.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Use only these synthetic facts. Treat each item
> as a separate hypothetical invocation and render every terminal card in
> order. Do not ask which item to assess.
>
> 1. A parent issue is supplied, but descendant coverage is incomplete.
> 2. A complete current family is supplied, but integration planning is absent.
> 3. The parent has an approved plan with independent units and safe writes.
> 4. A child is named directly; its accepted outcome lacks an execution plan.
> 5. The operator says Jordan owns the in-flight implementation phase.
> 6. An approved implementation is in flight, and its worktree and pull request
>    are named, but no phase owner is identified.
> 7. A child is named directly and its accepted outcome lacks an execution
>    plan. Family coverage is incomplete, but supplied evidence says that gap
>    does not block planning this child.

## Expected behavior

- [ ] Items 1–3 select `managing-issues`, `ce-plan`, and `ce-work`,
      respectively; item 1 chooses no leaf and certifies no frontier.
- [ ] Item 4 routes the child to `ce-plan` because planning is what needs to
      happen first, while preserving supplied parent constraints.
- [ ] Item 5 returns a continuation naming Jordan and no duplicate kickoff.
- [ ] Item 6 returns the normal route with `Active ownership unverified` and
      performs no ownership discovery or monitoring.
- [ ] Item 7 routes the child to `ce-plan` because planning is what needs to
      happen first; the supplied non-blocking family gap does not displace the
      directly named child.
- [ ] All conclusions use supplied family and ownership state only.
- [ ] Every ready route includes a concise, source-led plain-text kickoff with
      natural setup language; continuation remains compact and contains no
      duplicate kickoff. Default routes name no IDE and omit unknown
      availability.
