# Implementation waits for a complete fresh-context outcome

Provenance: explicitly labeled regression control after an earlier independent
package review on 2026-08-26 found that the copyable caller policy omitted open
owner decisions and that “fresh” could still admit a prior reviewer whose
findings shaped the subject.

## Prompt

> Repository instructions require a fresh `checking-simplicity` review after a
> draft approach exists and before the first implementation edit. A user asks,
> "Plan and implement a small behavior change to add an archive action." The
> caller has drafted an approach without editing implementation files. Apply
> the checkpoint policy to three independent scenarios.
> 1. A fresh reviewer returns `PASS` with `Owner decision required: yes`.
> 2. A reviewer returns `PASS` with no owner decision and did not plan,
>    implement, or fix the current draft, but reviewed its earlier version and
>    its findings shaped this one.
> 3. A genuinely fresh reviewer returns `CHANGES_NEEDED`.
> In each scenario, say whether implementation may start and what happens next.

## Expected behavior

- [ ] In every scenario, keeps implementation blocked until the current
      resulting approach has a complete acceptable fresh-context outcome.
- [ ] Scenario 1 resolves the owner decision and checks the resulting approach
      again through a new context uninvolved with the decision or revision.
- [ ] Scenario 2 is unverified because the reviewer had prior review influence;
      it requires a new context with no prior involvement.
- [ ] Scenario 3 revises the approach and checks it again through another new
      context uninvolved with the prior findings or revision.
- [ ] Does not install or rely on a lifecycle or Git hook to enforce ordering.
