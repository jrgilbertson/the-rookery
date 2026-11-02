# Evaluation Workflows

Follow the host's evaluation policy and existing authorization. A new package
alone does not require evaluation infrastructure or a behavioral suite.

## Decide what needs measurement

Start with observed system behavior and error analysis. Fix clear instruction
gaps first; invest in recurring evaluators when the failure and expected value
of repeated checking justify the cost. Prefer deterministic checks for rules
that code can assess. Use a model judge for a concrete failure requiring
judgment, and validate it against independent human labels before trusting it.

Targeted synthetic inputs can support discovery when real traces are scarce
or exercise rare known failures. Run them through the actual system and review
what happened; synthetic data does not establish real-world prevalence. A
precise known constraint can justify an early check. Retain regression checks
that remain useful after a fix, and reduce or retire checks that no longer
provide enough signal for their cost.
[Hamel Husain and Shreya Shankar's evals FAQ](https://hamel.dev/blog/posts/evals-faq/)
explains these tradeoffs.

## Use the maintained workflow

Use the [evals plugin](https://github.com/ai-evals-course/evals-skills)'s
[`evals-start`](https://github.com/ai-evals-course/evals-skills/blob/main/skills/evals-start/SKILL.md)
skill to choose the next step, then follow the targeted skill it selects. If
the evaluation job is already known, load that targeted skill directly. Let the selected workflow choose current tools
and a runner when needed; neither a specific vendor nor a runner is required
by this package. Reuse relevant existing evidence and checks.

Install the skills using the upstream README's installation instructions, or
read `evals-start` and the selected skill directly from that source repository.

If the needed skill or guidance is unavailable, report the limitation and
leave the affected measurement unverified. Package authoring and structural
checks can continue independently.

## Preserve authority and evidence

Obtain approval of actual evaluation inputs and the grading method before
using them. That approval is separate from authorization for model calls or
other side effects. Preserve the host's execution, private-storage, budget,
independent-review, and release requirements.

Distinguish package validation, installation identity, actual skill loading,
input preservation, and successful task behavior. Report only what the
observed evidence supports. An answer, a tool-use observation, or a successful
runner exit alone does not establish task quality. Keep expectations and
grader-only material out of the executor's access.
