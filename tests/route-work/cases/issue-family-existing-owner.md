# Issue families and existing owners route from supplied state

Provenance: PR review found approval routed to implementation without authority
and owner-only Resume required an unsupplied locator. Regression controls cover
supplied family state, direct implementation authority, and proven ownership.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Use only these synthetic facts. Treat each item
> as a separate hypothetical invocation and render every card in order. Do not
> ask which item to assess.
>
> 1. A parent issue is supplied, but descendant coverage is incomplete.
> 2. A complete current family is supplied, but integration planning is absent.
> 3. The parent has an approved plan with independent units, one integrator,
>    and safe writes.
> 4. A child is named directly; its accepted outcome lacks an execution plan.
> 5. The operator says Jordan owns the in-flight implementation phase.
> 6. An approved implementation is in flight, and its worktree and pull request
>    are named, but no phase owner is identified. The operator asks to
>    implement the accepted change.
> 7. A child is named directly and its accepted outcome lacks an execution
>    plan. Family coverage is incomplete, but supplied evidence says that gap
>    does not block planning this child.
> 8. The parent has an approved plan with independent units, one integrator,
>    and safe writes. The operator says: "Route the kickoff to implement it."

## Expected behavior

- [ ] The final answer contains only the requested cards, in item order,
      with no preamble or closing narration. Cards assert no artifact, locator, or
      task fact that the prompt did not supply.
- [ ] Items 1 and 2 start with `managing-issues` and `ce-plan`, respectively;
      item 1 chooses no leaf and certifies no frontier. Item 3 returns Questions
      asking whether implementation is authorized, with a concrete recommendation
      and no workflow, model, role profile, or kickoff.
- [ ] Item 8 starts with `ce-work` and uses Lead + Executors with a Lead on
      Fable 5.1 at medium and Executors on Grok 4.6 at high, up to three since
      the prompt names no
      unit count.
- [ ] Item 4 starts the child with `ce-plan` because planning is what needs to
      happen first, while preserving supplied parent constraints.
- [ ] Item 5 returns a `**Resume**` card naming Jordan with no kickoff or
      roster, continues the implementation phase, and requests or invents no
      locator.
- [ ] Item 6 returns the normal route with `Active ownership unverified` in
      its copy/paste kickoff, and the router itself performs no ownership discovery or monitoring in the
      trace. A kickoff may tell the receiver to verify ownership before writing.
- [ ] Item 7 starts the child with `ce-plan`; the supplied non-blocking family
      gap does not displace the directly named child.
- [ ] All conclusions use supplied family and ownership state only.
- [ ] Only items 6 and 8 carry implementation authority, supplied by their
      direct implementation requests. Their Setup and standalone kickoff
      preserve it without adding commit, push, PR, or other external authority.
      Artifact approval alone never becomes permission to implement.
- [ ] Every route has a bold first line, one decision sentence naming the
      starting workflow and the lead's model and effort, and bold Why, Setup,
      and Copy/paste kickoff labels. Setup lists every role with model and
      effort. Default routes name no IDE and no availability, and name a
      worktree only where parallel Executors write concurrently.
