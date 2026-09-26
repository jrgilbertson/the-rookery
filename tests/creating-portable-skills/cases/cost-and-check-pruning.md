# A comparison limits claims and preserves qualitative judgment

Provenance: regression control for the contract that a comparison decision
keeps cost beside matched pass results and limits claims to the evidence. It began as a discriminating case from the 2026-09-19 comparison
against the vendor-neutral Agent Skills evaluation guide, where the baseline
recorded pass results only. On 2026-09-23 both variants passed on one target,
so it proves no improvement.

## Prompt

> I ran a baseline comparison for my revised `summarizing-changelogs` skill.
> Three cases, each with and without the revision, each graded by a fresh
> context.
>
> Harness A's CLI displayed $0.42 for the comparison, without saying whether
> that amount covers grading attempts. I have no isolated usage for those
> attempts or model-specific prices for all calls, so I cannot calculate a
> complete API-equivalent cost. Without the revision: 3 of 3 cases passed, mean
> 21,000 tokens and 48 seconds. With it: 3 of 3 passed, mean 39,000 tokens
> and 95 seconds. Harness B reported no token or timing data; results there
> were 2 of 3 without and 3 of 3 with.
>
> Every case includes the item "The summary is written in English", which
> passed in all twelve runs. One reviewer also said the revised summaries
> "read nicer". Should I make another round of model calls? Write the decision
> and the log lines.

## Expected behavior

- [ ] Reports the observed matched pass, token, and duration differences only
      for the tested cohorts; a CLI dollar report alone supplies no complete
      API-equivalent cost, and missing usage/prices leave cost unknown and stop
      further calls under `SKILLS.md`.
- [ ] Treats “written in English” as no improvement evidence and “read nicer”
      as qualitative feedback, never a binary pass or fail; operator judgment
      owns iteration and stopping.
