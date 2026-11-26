# Prioritization

Note for maintainers of this skill, not an instruction for using it: the
`Rank by leverage` section below is a copy of the section with the same
heading in PRIORITIZATION.md at the root of this skill's source repository,
kept here so the skill stands alone. Change that file first, then copy its
section here unchanged, so the two stay identical byte for byte.

## Rank by leverage

When you rank findings, ideas, or tasks for me to choose from, order them by leverage, highest first: (impact × confidence) ÷ (verification effort × undo cost). Score each factor 1 to 3.

- Impact, how much better it makes things for users: 1 is barely noticed, 2 is a clear improvement to something users do often, 3 changes whether most users can do a core task or trust the product with their work. Work users don't see takes the impact of the problem it prevents or the feature it unblocks.
- Confidence, how sure we are that we can do it and it will deliver: 1 is a guess, 2 is good reasons but nothing confirmed, 3 is confirmed.
- Verification effort, how hard the result is to confirm: 1 means existing checks prove it, 2 means it needs new tests or one manual check, 3 means only human judgment can, such as a new user-facing view, flow, or concept.
- Undo cost, what it takes to undo: 1 is contained and can be put back as it was, 2 is wide but can be put back as it was, 3 means it can't, because the earlier state is lost or the effect has already reached someone, including any stored or published name (table, column, stored ID or enum value, event name, public API route or field, CLI flag, configuration key, or published package or skill name).

Return the whole list with each item's scores. Keep items you would skip, with a one-line reason. Name every item that scores 3 on impact above the list. When an item has a deadline, give the date beside it and score it as if it had none.

This applies to lists of work to choose from. A skill or workflow that states its own ordering or judgment factors keeps them.

## Who users are

For impact, users are whoever uses what the repository ships. The owner
counts as a user when the repository ships the owner's own tools. Maintainers
count only through what their work unblocks.

## Unclear scores

When the request and evidence do not settle one of the four leverage scores,
propose the value the evidence best supports and mark it `best guess` in the
preview and the result, without asking. A score the evidence settles carries
no mark.

## Derived priority and estimate

`SKILL.md` says when to derive priority and estimate. These tables give the
result, so look it up instead of calculating it.

Priority comes from all four scores. Multiply impact by confidence to find the
row, and verification effort by undo cost to find the column. Each cell is the
band that leverage falls in: 3 or higher is `high`, at least 1 and below 3 is
`medium`, and below 1 is `low`. The table never returns `urgent`.

| impact × confidence | 1 | 2 | 3 | 4 | 6 | 9 |
|---|---|---|---|---|---|---|
| 1 | medium | low | low | low | low | low |
| 2 | medium | medium | low | low | low | low |
| 3 | high | medium | medium | low | low | low |
| 4 | high | medium | medium | medium | low | low |
| 6 | high | high | medium | medium | medium | low |
| 9 | high | high | high | medium | medium | medium |

A leaf's estimate comes from verification effort and undo cost alone. Multiply
them to find the row.

| verification effort × undo cost | estimate |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 5 |
| 6 | 5 |
| 9 | 8 |
