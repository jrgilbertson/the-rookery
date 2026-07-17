# Baseline test: [skill-name]

Mode rule. Pick the mode that matches the flow:

- **New skill:** run each prompt with and without the skill.
- **Revision:** run each prompt with the prior version and the revised version.

Run every prompt in a fresh agent context with the right variant loaded.
Use the harness's native mechanism for a clean context (a subagent, a CLI
exec, a new session). Never compare inside one warm session; carried-over
context contaminates the baseline.

Use 2-3 realistic prompts, ideally from tasks the user has actually done.

## Case 1: [one-line prompt summary]

Date: [YYYY-MM-DD] | Harness: [name] | Model: [name]

| Prompt | Baseline behavior (observed) | With-skill behavior (observed) | Verdict |
| --- | --- | --- | --- |
| [full prompt text] | [what happened without / with prior version] | [what happened with / with revised version] | [better / same / worse] |

## Case 2: [one-line prompt summary]

Date: [YYYY-MM-DD] | Harness: [name] | Model: [name]

| Prompt | Baseline behavior (observed) | With-skill behavior (observed) | Verdict |
| --- | --- | --- | --- |
| [full prompt text] | [observed] | [observed] | [verdict] |

## Case 3 (optional): [one-line prompt summary]

Date: [YYYY-MM-DD] | Harness: [name] | Model: [name]

| Prompt | Baseline behavior (observed) | With-skill behavior (observed) | Verdict |
| --- | --- | --- | --- |
| [full prompt text] | [observed] | [observed] | [verdict] |

## Waiver (only when shipping without the comparison)

A substantive change must not ship without the comparison above or an
explicit waiver from the user, recorded here. Substantive means any change
to instruction semantics, the trigger description, or bundled resources.
Typo, formatting, and link-only fixes are exempt and need no waiver.

- Waived by the user: [yes, quote or paraphrase the user's explicit waiver]
- Reason: [why the comparison was skipped]
- Date: [YYYY-MM-DD]
