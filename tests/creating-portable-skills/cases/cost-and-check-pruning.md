# A comparison reports cost and drops checks that do not discriminate

Provenance: 2026-09-19 comparison against the vendor-neutral Agent Skills
evaluation guide — the baseline comparison recorded pass results only, so
a skill that doubled token use for no gain looked the same as a cheap one,
and items that passed both halves still counted as evidence.

## Prompt

> I ran a baseline comparison for my revised `summarizing-changelogs` skill.
> Three cases, each with and without the revision, each graded by a fresh
> context.
>
> Harness A reported cost. Without the revision: 3 of 3 cases passed, mean
> 21,000 tokens and 48 seconds. With it: 3 of 3 passed, mean 39,000 tokens
> and 95 seconds. Harness B reported no token or timing data; results there
> were 2 of 3 without and 3 of 3 with.
>
> Every case includes the item "The summary is written in English", which
> passed in all twelve runs. One reviewer also said the revised summaries
> "read nicer". Write the decision and the log lines.

## Expected behavior

- [ ] States harness A's cost change beside its pass result, with figures
      consistent with the prompt (21,000 to 39,000 tokens, 48 to 95
      seconds). A difference, a ratio, or both pairs side by side all
      count; the pass result alone does not.
- [ ] Concludes harness A shows no improvement for that added cost, and does
      not call the revision proven there.
- [ ] Records harness B's cost as not available and still reaches a decision
      for it.
- [ ] Removes the "written in English" item or relabels its case as a
      control, and does not count it as evidence of improvement.
- [ ] Routes "read nicer" to human feedback or a blind comparison of the two
      versions, and does not log it as a pass or a fail.
- [ ] Does not call the revision better in general, or on harnesses or
      models that did not run.
