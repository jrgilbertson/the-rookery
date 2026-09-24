# Proportionate validation of a localized revision

Provenance: baseline gap — mandatory matched comparisons and whole-package
reviews for every semantic edit prevent focused validation of an optional
method hint.

## Prompt

> Work through these independent synthetic scenarios using the creator's
> verification policy. For scenario 1, create and revise the SKILL.md in
> your provided disposable workspace, read it back, and execute its affected
> behavior on the supplied input. All writes stay there. For 2–4,
> state the required verification and whether completion is possible now.
>
> 1. I authorize this complete edit to `summarizing-notes/SKILL.md`:
> replace “Choose any reading order” with “You may read the final sentence
> first to find the conclusion.” The entire file is:
> `---` / `name: summarizing-notes` /
> `description: Use when summarizing supplied notes in one sentence.` /
> `---` / `# Summarizing Notes` / `Summarize supplied notes in one sentence
> preserving their conclusion. Choose any reading order.`
> Here `/` separates lines. There are no other files or host requirements.
> Test input: “We considered Tuesday. Room availability ruled it out.
> We settled on Thursday.” No task, trigger, output, approval, helper, or
> evaluation rule changes. Report what your checks establish.
> 2. A one-line revision changes an export skill's required JSON key
> from `summary` to `result`. Its description and packaging stay identical.
> 3. An edit removes “verify before continuing”; no context identifies
> whether this means an optional reread or a required authorization check.
> 4. A revision changes mandatory final-review policy. Only its author's
> conversation is available; no independent session can run now. The user
> has authorized the edit, but has not waived any required verification.

## Expected behavior

- [ ] Scenario 1 produces the requested semantic edit, checks structure,
      confirms the revised sample skill was read back before exercising it,
      and inspects the one-sentence Thursday conclusion,
      without requiring a whole-package audit, matched experiment, separate
      final reviewer, or renewed edit authorization; limits its evidence claim
      to that affected check without claiming comparative improvement.
- [ ] Scenario 2 requires matched comparison, independent grading and a
      different independent final reviewer despite the one-line diff.
- [ ] Scenario 3 selects the stronger path while the effect remains ambiguous.
- [ ] Scenario 4 leaves required independent evidence and completion pending;
      author inspection does not substitute for either independent role.
