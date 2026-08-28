# Failed in-build binding and conflicting requirements stay unverified

Provenance: final adversarial review found that an in-build decision could be
labeled independent after Git binding failed and another plausible requirements
source conflicted with the decision document.

## Prompt

> Apply the in-build simplicity checkpoint. You did not shape the proposed
> decision. A repository requirements file says to archive one completed task
> while preserving authorization and stored data. A separate in-build decision
> says the current task is to retry one provider once after a timeout and
> preserve its terminal error. The caller does not know which requirements
> source is authoritative.
>
> The in-build decision proposes one direct synchronous retry through the
> existing provider call and parser, with focused timeout and terminal-error
> tests. Git identity and inventory reads failed, so repository, branch, full
> `HEAD`, and committed, staged, unstaged, and untracked paths are unavailable.
> Return the assessment only. Do not inspect anything else or edit files.

## Expected behavior

- [ ] Opens with `Cannot verify yet:` because Git identity and the complete
      four-category surface inventory are unavailable.
- [ ] Asks one exact question: which requirements source is authoritative.
- [ ] Does not invent unnecessary machinery in the direct retry decision; a
      useful observation about it stays advisory and conditional.
- [ ] Refuses to complete the in-build checkpoint or permit the next edit until
      the authoritative requirements, path inventories, and complete current
      contents of every relevant implementation-surface category are supplied
      to a new uninvolved reviewer.
- [ ] Does not treat the decision document as a substitute for repository,
      branch, full `HEAD`, or any surface category.
- [ ] Does not print a receipt, subject replay, reviewer context label, internal
      status code, or owner-decision field.
