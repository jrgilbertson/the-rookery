# Unsupported owners recover through the supported-owner table

Provenance: observed failure — the unrestricted catalog recommendation included
unsupported owners and was misrepresented as the router’s supported choices.

## Prompt

> $route-work If route-work is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Work only from these synthetic facts. Treat
> each item as a separate hypothetical invocation and render every card in
> order. Do not ask which item to assess.
>
> 1. Route this request to a hands-off end-to-end delivery workflow outside
> the supported startup owners.
> 2. The previous routing card asked which supported workflow should start
> and recommended choosing from the public workflow catalog. The operator
> followed that recommendation and selected lfg, which the catalog presents
> as a hands-off plan-to-PR workflow. This selection is outside the seven
> supported startup owners. Continue routing this request.

## Expected behavior

- [ ] Each hypothetical invocation returns exactly one `**Questions**` card.
- [ ] Each recommendation points to the supported starting-owner table at
      `https://github.com/jrgilbertson/the-rookery/blob/main/ROUTING.md#choose-what-needs-to-happen-first`,
      giving a concrete way to choose a supported start.
- [ ] Neither card treats the full workflow catalog as the router’s supported
      choices or repeats an unrestricted catalog selection request.
- [ ] Cards name no workflow, model, profile, or kickoff, invent no facts or
      authority, and begin no work. No eighth owner or fourth card is added.

The second item supplies prior-turn context; these are separate synthetic
invocations, not a persistent multi-turn session.
