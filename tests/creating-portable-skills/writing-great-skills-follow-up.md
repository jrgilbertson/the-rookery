# Writing-great-skills follow-up

Date: 2026-07-28

This record covers the surgical revision prompted by a fresh-context
`writing-great-skills` review. The frozen prior package is commit `bc36fe1`.
Its `SKILL.md` SHA-256 is
`a466934c86175d84fddfa611dd0fdce8f39c8ee8e3142128aac3ca63871812bd`.
The revised package `SKILL.md` SHA-256 is
`4693702db6766235049e34df7bf95baea77c1de24108307c09e0da5a809754fe`.

The behavior target was `gpt-5.6-sol` in fresh Codex agent contexts. Every
executor and grader started without inherited conversation turns. The initial
executors were `great_skills_prior` and `great_skills_revised`; the independent
grader was `great_skills_grader`. The read-only rerun used
`read_only_revised_rerun` and `read_only_grader_rerun`. Mechanical validation
and file identity used deterministic commands.

## Predeclared cases

| Case | Intended change | Hard constraint |
| --- | --- | --- |
| Read-only audit | End after findings and verdict instead of asking for edit approval | Preserve prioritized findings, verdict, and no-edit behavior |
| Generated trigger contract | Use a positive description and omit a body-level trigger echo | Preserve owned invoice-audit branches and observable output |
| Evidence doctrine | Define and record Claim Ceiling, give trigger evidence one owner, and reserve labels for matched evidence | Preserve directional comparison for a small matched prior and revised run |
| Matched-comparison ownership | Give routine comparison policy one authoritative home | Preserve separate trigger/native ownership and the resource-placement control |
| Resource placement control | Keep copied output in `assets/`, branch reading in `references/`, deterministic helpers in `scripts/`, and `skills-ref` validation | No material change |

## Results

### Read-only audit

The first prior and revised executors each returned prioritized findings and a
verdict. Their terminal excerpts were:

> Prior: “Terminal next action: approve or reject the proposed material fix
> scope ... before any editing. Because this request is read-only, no files
> were edited.”

> First revised run: “The read-only audit is complete and no files were
> changed. I am returning control to you; approve or reject the material fix
> scope before any revision begins.”

The grader marked that pair `same` because both invited approval. It found the
no-edit statements stable but noted that the summaries did not independently
prove filesystem state. The completion condition was then tightened.

The next revised executor ran in a fresh context and ended with a scoped review
limitation. It did not ask for approval, editing, or revision. The new grader
compared that artifact with the prior terminal excerpt and concluded:

> “The improper approval handoff was removed while the core review deliverable
> remained intact.”

That grader found no demonstrated invariant loss. It also limited the result:
the supplied artifacts did not independently prove finding quality or actual
filesystem state. A later read-only Codex CLI probe addressed the latter point.
The prior and revised executors both ran under a read-only sandbox, loaded the
declared hashes, and made no write-capable calls. Both happened to end without
an approval prompt, so that additional pair was recorded as `same` and did not
raise the evidence label. It shows ordinary run variation and one directly
observed no-edit execution for each variant.

### Generated trigger contract

The prior executor produced this description and body routing:

```markdown
description: Use when auditing vendor invoices for duplicate charges, purchase-order mismatches, or tax errors. Produces invoice-audit findings. Do not use for paying invoices or negotiating with vendors.

## When to use
## Outcome and constraints
## Workflow
## Gotchas
## Verification
```

The revised executor produced:

```markdown
description: Use when auditing vendor invoices for duplicate charges, PO mismatches, or tax errors. Reports supported invoice discrepancies.

## Outcome and constraints
## Workflow
## Verification
```

The grader found the intended delta: owned branches and the observable output
remained, while the negative exclusion and default body-level trigger echo were
removed. It found no observed loss and limited the result to one generated
skeleton without listing judgments.

### Evidence doctrine and control

The prior executor identified the trigger template as the operational owner of
listing construction, gave one execution a `smoke-tested` label, and found no
Claim Ceiling definition or record field. The revised executor identified the
completed trigger record as the listing owner, assigned no label to one
execution, reserved `directional comparison` for matched evidence, defined the
Claim Ceiling, and named its baseline-record field. The grader confirmed each
textual change from the owning files and found no loss. It noted that no
completed evidence record was adjudicated in this case.

A later ownership case addressed a final-review finding. The frozen-prior
executor found routine matched-comparison policy split across `SKILL.md` and
the review checklist, with no single owner. The revised executor identified
`assets/baseline-test-template.md` as the sole owner of case construction,
candidate decisions, evidence labels, matched-comparison waivers, and Claim
Ceiling recording. A separate fresh-context grader inspected the five current
policy files and concluded `intended delta observed`. It found the trigger
template limited to listing and native checks, the other files pointing to the
baseline record, and no observed loss. Its limitation was that this textual
case did not independently establish behavioral effectiveness.

For the control, both executors mapped copied workflow output to `assets/`,
branch-specific reading to `references/`, deterministic helpers to `scripts/`,
and validation to `npx skills-ref validate <skill-directory>`. The grader found
the control materially stable.

| Case | Independent conclusion | Evidence limit |
| --- | --- | --- |
| Read-only audit | Intended delta observed after one revision and rerun; a later read-only probe was `same` | Finding quality and repeatability remain unverified |
| Generated trigger contract | Intended delta observed | One generated skeleton does not prove activation |
| Evidence doctrine | Intended delta observed | Doctrine was inspected, but no completed evidence record was adjudicated |
| Matched-comparison ownership | Intended delta observed | Textual ownership does not prove behavioral effectiveness |
| Resource placement control | Materially stable | Abstract mapping and command only |

## Claim Ceiling

These matched cases support a directional comparison for the named instruction
changes only. They do not establish general reliability, causal improvement,
non-regression, repeatability, or behavior outside these cases. The later
read-only probe does not strengthen the label. Structural validation, listing
judgments, installation, content identity, and native activation are recorded
separately in `results.md` and `trigger-queries.md`.
