# The assessment runs in a subagent

Provenance: the owner asked that the skill run as a subagent instead of in
the current context, after finding a separate-session or other-model menu
confusing. The frozen prior version failed this case 2/5 in a matched
comparison by assessing in the current context and listing subagent, separate
session, or other model invocation as equal choices.

## Prompt

> You loaded this skill after a request to simplify a plan you authored in
> this context. How does this skill run the assessment, and which model does
> the reviewer use? Return the answer only.

## Expected behavior

- [ ] Dispatches one subagent and does not assess in the current context.
- [ ] Does not start a separate session or present a choice among subagent,
      separate session, and other model invocation.
- [ ] Uses the current model unless the caller names a different one.
- [ ] Gives the reviewer the subject in full and the available decision frame.
- [ ] Does not require tracking files, extra reviewers, a separate workspace
      used only to prove the review, or a named model catalog.
