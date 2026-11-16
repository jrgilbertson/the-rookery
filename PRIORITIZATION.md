# How I prioritize

I rank work by leverage: how much good a change does for what it costs to get
it done safely. When I sort a list of findings, ideas, or tasks, I use this
order.

```text
leverage = (impact × confidence) ÷ (effort × fix-risk)
```

This is the ICE score that product and growth teams use (Impact, Confidence,
Ease), with one factor added: the risk that the fix itself breaks something.
Dividing by effort does the same job as multiplying by ease.

## The four factors

Each factor gets a score from 1 to 3.

| Factor | Question | 1 | 3 |
|---|---|---|---|
| Impact | What gets better, or what goes wrong if I leave it? | A small annoyance | Users, data, security, or a lot of future work |
| Confidence | How strong is the evidence? | A hunch that needs investigation | I read the code or reproduced the problem |
| Effort | How much work is it to finish, including tests and review? | Hours | Several days |
| Fix-risk | What could the change break, and how hard is it to undo? | Isolated and easy to revert | Shared state, data, access, or hard to reverse |

Impact already covers the risk of doing nothing. A security hole or a
data-loss bug scores high on impact. Fix-risk covers only the change.

Two examples:

- A serious bug with a clear reproduction and a one-line, isolated fix:
  (3 × 3) ÷ (1 × 1) = **9**.
- A valuable refactor I'm fairly sure about that takes days and touches shared
  state: (3 × 2) ÷ (3 × 3) = **0.67**.

## Why fix-risk

Agents changed what effort costs me. They write the code, run the checks, and
work in parallel worktrees, sometimes unattended from plan to pull request (see
[Build](WORKFLOWS.md#build)). The hours a change takes matter less than they
used to.

What still costs me is attention: how closely I have to read the result before
I trust it. A low-risk change with good checks can run on its own and still be
safe to merge. A high-risk change needs a close read, and some changes, such as
access, money, or deletion, wait for my approval however good the checks are.
Fix-risk measures that difference. Without it, a quick but dangerous change
would rank near the top just because an agent can make it fast.

Risk can also come down. Tests and other checks make a risky change safer
([Testing with agents](TESTING.md)), so the tests that make a refactor safe
often rank above the refactor itself.

## Breaking ties

When two items score about the same:

1. Work that unblocks other items goes first, such as tests a later change
   depends on.
2. A security finding with strong evidence goes above other findings.
3. A change with a clear way to verify it goes above one without.

## Use the score to decide

The scores are coarse. They put a list in a sensible order so I can see
everything at once and choose. I still read the top of the list, check for
dependencies between items, and move an item when the score misses something.

When an agent ranks work for me, I want the whole list in leverage order, with
each item's scores. Items it would skip stay on the list with a one-line reason.
