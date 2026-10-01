# Reviewer follows the selected implementer, not a static ranking

Provenance: regression control for the maintainer-approved Executor-derived
Reviewer rule, preserving operator choices, listed effort, and fallback disclosure.

## Prompt

> `$route-work` If the skill is unavailable, stop rather than reconstructing it.
> Otherwise read only its installed package and call no other tools. Treat each
> item as a separate hypothetical invocation; render the cards in order.
>
> 1. Route a diagnosed parser fix ready for implementation with a separate
>    correctness Reviewer. No model overrides or availability limits.
> 2. Same fix and review. I choose the first Executor-listed model from a
>    different provider than the Executor primary, at its listed effort, as
>    the implementing coordinator. Other listed models remain available.
> 3. Route an approved parent implementation plan with two independent units
>    and a separate correctness Reviewer. I choose the first Executor-listed
>    model from a different provider than the Executor primary, at its listed
>    effort, as coordinator, and the Executor primary at its listed effort as
>    both implementing workers. All models are available.
> 4. Same parser fix and review. Only the Executor secondary is available.
> 5. Same parser fix and review. The Executor primary implements at its listed
>    effort. All Executor-listed models from other providers are unavailable;
>    a model from a provider absent from the Executor row is available.
> 6. Same parser fix and review. Every Executor-listed model is unavailable.

## Expected behavior

- [ ] Item 1 assigns the Executor primary to implementation and the first
      available different-provider Executor model to review, naming concrete
      settings at their listed efforts in Setup and kickoff.
- [ ] Item 2 preserves the selected implementer and assigns the Executor
      primary at its listed effort to review in Setup and kickoff.
- [ ] Item 3 preserves the chosen coordinator and two Executor assignments;
      Reviewer is the first available Executor model from a different provider
      than the actual implementers, not the non-implementing coordinator, at
      its listed effort in Setup and kickoff.
- [ ] Item 4 assigns the Executor secondary at its listed effort to both roles,
      disclosing the same-provider fallback and fresh review session in Setup
      and kickoff.
- [ ] Item 5 assigns the Executor primary at its listed effort to review in a
      fresh session and discloses the same-provider fallback in Setup and
      kickoff. The unlisted model is not invented as a review alternative.
- [ ] Item 6 returns Questions to unblock availability rather than inventing
      a model or switching billing methods.
