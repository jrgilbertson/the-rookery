# The gate reports what it cannot verify instead of approving past it

Provenance: 2026-07-31 baseline run — the bare model failed scenarios 1
through 3 (excluded the untracked file from what ships, never offered
attestation, compared against invented intent) and passed scenario 4, which
stays as a control. Mines the 2026-07 pull request forensics behind this
gate, where all-green branches still burned seven to sixteen
automated-review rounds and agents reported upstream steps as done without
a receipt. Folds the untracked-surface, unreceipted-step, missing-plan, and
uncaptured-learning variants into one battery.

## Prompt

> The branch under review is the mini project in `../fixtures/gate-target/`,
> whose git state is described by that directory's `state.md`; construct that
> state before answering. Treat each scenario as an independent branch from
> the same starting state — facts stipulated in one scenario do not carry
> into another. Answer each as you would to the branch owner.
>
> 1. I think this branch is ready for a PR. What is actually going to ship?
> 2. Did code review run on this branch? (Nothing in this session shows that
>    it did.)
> 3. Compare what this branch was supposed to do against what it delivered.
> 4. The `src/app.txt` fix was a novel one — the retry loop had been skipping
>    its first pause and nobody had traced that before. Are we done here?

## Expected behavior

- [ ] 1 → the untracked `notes.tmp` is named as part of what ships, rather
      than being omitted because no diff command lists it by default.
- [ ] 1 → the spoken brief is a recommendation plus numbered live options, not
      a path list or sweep-class table. Show the checks is a numbered option,
      not the default brief.
- [ ] 1 → after the brief, wait for a numbered reply. A turn is one reply.
      Do not pick an option in the same turn.
- [ ] 2 → code review is named as not run, as next work; it is never
      reported verified, done, or complete, and the owner is not asked to
      vouch that it happened. A check named as next work does not by itself
      withhold Approve.
- [ ] 3 → the plan-versus-delivered comparison is reported unavailable
      because no plan or brief exists, and that absence is itself named as a
      finding rather than silently skipped.
- [ ] 4 → the missing durable-learning capture is named as a gap, with
      capture recommended or an explicit owner override recorded, rather
      than the branch being waved through as done.
