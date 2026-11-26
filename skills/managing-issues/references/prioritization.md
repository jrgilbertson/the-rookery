# Prioritization

## Rank by leverage

When you rank findings, ideas, or tasks for me to choose from, order them by leverage, highest first: (impact × confidence) ÷ (verification effort × undo cost). Score each factor 1 to 3.

- Impact, how much better it makes things for users: 1 is no user task you can name gets better, 2 is a named user task gets faster, easier, or more reliable, 3 decides whether users can do a core task or keep their work safe. Work users don't see takes the impact of the problem it prevents or the feature it unblocks.
- Confidence, how sure we are that it will deliver: 1 is a guess, 2 is a concrete reason but nothing confirmed, 3 is evidence that confirms the need or the approach.
- Verification effort, how hard the result is to confirm: 1 means checks that existed before the change, such as tests, types, CI, or a reproduction on record, prove it, 2 means it needs new tests, including the change's own, or a manual check with a known right answer, 3 means only human judgment can, such as a new user-facing view, flow, or concept.
- Undo cost, what it takes to undo: 1 is one revert within one module, 2 can be undone but reaches shared code, shared settings, or many users, or takes more than one revert, 3 can't be undone, because data is lost, a message is sent, money moves, access is exposed, or a stored or published name is added or changed (table, column, stored ID or enum value, event name, public API route or field, CLI flag, configuration key, or published package or skill name).

Return the whole list with each item's scores. Keep items you would skip, with a one-line reason. Name every item that scores 3 on impact above the list. When an item has a deadline, give the date beside it and score it as if it had none.

This applies to lists of work to choose from. A skill or workflow that states its own ordering or judgment factors keeps them.

## Who users are

For impact, users are whoever uses what the repository ships. The owner
counts as a user when the repository ships the owner's own tools. Maintainers
count only through what their work unblocks.

## Scoring rules

Score every issue you draft, create, or update, parents included, on the four
leverage factors (each 1 to 3).

- On an update, keep each stored score unless the request or evidence new in
  this update changes it, and fill any absent score.
- Callers with restricted score authority follow Step 3 of `SKILL.md`: a
  coordinated batch lists missing scores in the preview instead of filling
  them, and a Captain writes only the score edits its standing instruction
  permits.
- Score a leaf that still needs discovery or planning on what is known now;
  planning revises the scores later.
- Store the four scores in the canonical tracker's mapped score fields and
  nowhere else. Store no leverage value, and put no score or score rationale
  in an issue body.
- When the request and evidence do not settle a score, propose the value the
  evidence best supports and mark it `best guess` in the preview and result,
  without asking. A score the evidence settles carries no mark.

## Derived priority and estimate

Priority and estimate follow from the scores; never choose either directly.
Look both up in the tables below instead of calculating them: priority from
all four scores, and an implementation leaf's estimate from verification
effort and undo cost alone.

- Derive priority and estimate on every create and every content or score
  update, in the same previewed batch, whether or not a score changed.
- Derive them only when all four scores are present (each read from the
  tracker or written in this batch). Otherwise leave priority and estimate
  unchanged.
- Derivation never sets, overwrites, or clears urgent (the value mapped under
  `mappings.priority.urgent`). When the request asks for urgent, write urgent.
  When the tracker's current priority is already urgent, leave it. In both
  cases derive only the estimate. Decide this from those two facts alone, not
  from whether the work seems time-sensitive. An urgent issue still gets all
  four scores with the same care. If a request sets urgent and also names an
  estimate, apply the named-estimate rule below.
- When the request removes urgent, derive priority as for any other issue and
  show urgent as the old value.
- An issue with no priority set gets the derived priority. When the current
  priority cannot be read, or the issue carries more than one priority value,
  derive no priority and name the problem in the preview.
- When the request names any other priority, or an estimate, do not write it
  and do not bend a score to reach it. Show the derived value beside the
  requested one and ask which scores should change.

Multiply impact by confidence to find the priority row, and verification
effort by undo cost to find the column. Each cell is the band that leverage
falls in: 3 or higher is `high`, at least 1 and below 3 is `medium`, and
below 1 is `low`. The table never returns `urgent`.

| impact × confidence | 1 | 2 | 3 | 4 | 6 | 9 |
|---|---|---|---|---|---|---|
| 1 | medium | low | low | low | low | low |
| 2 | medium | medium | low | low | low | low |
| 3 | high | medium | medium | low | low | low |
| 4 | high | medium | medium | medium | low | low |
| 6 | high | high | medium | medium | medium | low |
| 9 | high | high | high | medium | medium | medium |

Multiply verification effort by undo cost to find a leaf's estimate row.

| verification effort × undo cost | estimate |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 5 |
| 6 | 5 |
| 9 | 8 |

## Assignee order

On a create, select the assignee in this fixed order:

1. The person the request names.
2. Otherwise the config's `assignee.default`.
3. Otherwise the human who made the request (not the account the run
   authenticates as).

When the request names no one, a scheduled or headless run with no human
requester and no `assignee.default` leaves the assignee empty and says so. If
the selected person cannot be assigned on the target, do not skip to the next
option: leave the assignee empty and name who could not be assigned and why.
