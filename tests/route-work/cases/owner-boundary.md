# What needs to happen first determines the starting workflow

Provenance: explicit routing-safety invariant — a carrier or eventual workflow
must not displace the work that needs to happen first.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Work only from these synthetic facts. Treat each
> item as a separate hypothetical invocation and render every card in order.
> Do not ask which item to assess.
>
> 1. A feature issue still disputes the intended user behavior.
> 2. A supplied decision document needs one dependency-ordered pressure test.
> 3. Approved requirements have no execution plan. Implementation is
>    authorized.
> 4. A command fails and the cause is unknown.
> 5. The cause and fix are established; implementation is authorized.
> 6. An issue family's descendant coverage and blockers are uncertain.
> 7. A settings issue has unresolved visual and interaction design direction.
> 8. The operator requests a hands-off delivery workflow outside the supported
>    startup owners.

## Expected behavior

- [ ] The final answer contains only the requested cards, in item order,
      with no preamble or closing narration. Cards assert no artifact, locator, or
      task fact that the prompt did not supply.
- [ ] Items 1–3 start with `ce-brainstorm`, `grill-with-docs`, and `ce-plan`,
      respectively, each with a coordinator on Opus 5.5 at high; item 2 uses the
      Planner profile, not Critic.
- [ ] Items 1–3 are Single owner with the coordinator alone. Item 3 adds no
      Executors: implementation is authorized, but no independent units are
      established.
- [ ] Items 4–5 start with `ce-debug` on GPT-6 Sol at high and `ce-work` on
      Opus 5.5 at medium, respectively, each as the coordinator alone.
- [ ] Items 6–7 start with `managing-issues` and `impeccable`, despite their
      issue carriers, each as the coordinator alone. Item 7's kickoff ends
      with "Don't merge without human approval."
- [ ] Item 8 returns a `**Questions**` card that includes the absolute public
      supported-owner table URL from `ROUTING.md`, names no workflow, and emits
      no kickoff.
- [ ] Every supported item begins no downstream work and names one starting
      workflow.
- [ ] Every supported item has a bold first line, one decision sentence, and
      bold Why, Setup, and Copy/paste kickoff labels, with a kickoff naming the
      starting workflow, the coordinator's model and effort, every other role with
      model and effort, the supplied source, and preserved authority. Default
      routes name no IDE or pseudo-spec; isolation may be named for
      concurrent Executor writes.
