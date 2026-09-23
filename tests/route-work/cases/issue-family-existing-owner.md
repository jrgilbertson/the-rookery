# Issue families and existing owners route from supplied state

Provenance: PR review found approval routed to implementation without authority
and owner-only Resume required an unsupplied locator. A later run treated
unnamed units as a bounded piece and unknown ownership as vacant. Independent
review then found an approved, authorized parent plan that proves no units,
integrator, or write boundaries had no selectable pattern, so item 9 covers
that gap. Regression controls cover supplied family state, direct
implementation authority, and proven ownership. On 2026-09-22 the default
changed to Single owner, so items 6 and 9 now guard that occupancy or bare
implementation authority does not add Executors.

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
> 9. The parent has an approved plan and the operator says: "Implementation is
>    authorized; route the kickoff." Nothing names units, an integrator, or
>    write scopes.

## Expected behavior

- [ ] The final answer contains only the requested cards, in item order,
      with no preamble or closing narration. Index labels identifying the
      hypothetical items are allowed in this batch; the exact-card cases own
      single-response formatting. Cards invent no concrete artifact, locator,
      owner, permission, unit count, or scope boundary. Generic instructions
      to honor supplied constraints and labeled contract defaults are allowed.
- [ ] Items 1 and 2 start with `managing-issues` and `ce-plan`, respectively;
      item 1 chooses no leaf and certifies no frontier. Item 3 returns Questions
      asking whether implementation is authorized, with a concrete recommendation
      and no workflow, model, profile, or kickoff.
- [ ] Item 8 starts with `ce-work` and uses Coordinator + Executors, because
      the approved plan states independent units: a coordinator on Opus 5.5 at
      medium (the Executor profile, which dispatching does not change) and
      Executors on Opus 5.5 at medium, up to three since the prompt names no
      unit count.
- [ ] Item 9 starts with `ce-work` as Single owner: the coordinator alone on
      Opus 5.5 at medium. Nothing establishes independent units, so the card
      adds no Executors, invents no units, integrator, or write scopes, and
      invites adding Executors if the plan names independent units.
- [ ] Item 4 starts the child with `ce-plan` because planning is what needs to
      happen first.
- [ ] Item 5 returns a `**Resume**` card naming Jordan with no kickoff or
      roster, continues the implementation phase, and requests or invents no
      locator.
- [ ] Item 6 starts with `ce-work` as Single owner: the coordinator alone on
      Opus 5.5 at medium. A named worktree and pull request are occupancy
      evidence, not independent units. Setup and the
      kickoff last sentence each include: No named owner was proven for this
      phase; this start is still allowed. They do not emit a stored-status
      occupancy label or a halt. A kickoff may tell the receiver to verify
      ownership before writing. The shared side-effect-free case owns the
      package-read-only trace check.
- [ ] Item 7 starts the child with `ce-plan`; the supplied non-blocking family
      gap does not displace the directly named child.
- [ ] All conclusions use supplied family and ownership state only. Missing
      owner evidence leaves ownership unknown; it does not prove a vacant phase.
- [ ] Only items 6, 8, and 9 implement, from their direct implementation
      requests. They state no grant sentence, end the
      kickoff's authority text with "Don't merge without human approval.", and add
      no commit, push, PR, or other external authority. Artifact approval alone
      never becomes permission to implement.
- [ ] Every route has a bold first line, one decision sentence naming the
      starting workflow and the coordinator's model and effort, and bold Why, Setup,
      and Copy/paste kickoff labels. Setup lists every role with model and
      effort. Default routes name no IDE and no availability, and name no
      worktree isolation.
