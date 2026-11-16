# How I prioritize

I rank work by leverage: how much good a change does for what it costs to get
it done safely. When I sort a list of findings, ideas, or tasks, I use this
order.

```text
leverage = (impact × confidence) ÷ (effort × fix-risk)
```

This is the ICE score that product and growth teams use (Impact, Confidence,
Ease), with two changes for work that agents do. Effort measures how hard the
result is to verify, not how long it takes to build. A fourth factor,
fix-risk, covers the chance that the fix itself breaks something. Dividing by
effort does the same job as multiplying by ease.

## The four factors

Each factor gets a score from 1 to 3.

| Factor | Question | 1 | 2 | 3 |
|---|---|---|---|---|
| Impact | What gets better, or what goes wrong if I leave it? | A small annoyance | A cost someone pays regularly | Users, data, security, or a lot of future work |
| Confidence | How strong is the evidence? | A hunch that needs investigation | A strong signal I haven't confirmed | I read the code or reproduced the problem |
| Effort | How hard is it to confirm the result is right? | Existing tests, types, or CI prove it | It needs new tests or one targeted manual check | No check can prove it, so it needs judgment, such as taste, UX, performance under real load, or behavior across systems |
| Fix-risk | What could the change break, and how hard is it to undo? | Isolated and easy to revert | Shared code that tests cover, still easy to revert | Shared state, data, access, or hard to reverse |

Impact already covers the risk of doing nothing. A security hole or a
data-loss bug scores high on impact. Fix-risk covers only the change.

Two examples:

- A serious bug with a clear reproduction and a one-line, isolated fix. The
  reproduction becomes a test that proves the fix:
  (3 × 3) ÷ (1 × 1) = **9**.
- A valuable refactor I'm fairly sure about, in code no tests cover, that
  touches shared state: (3 × 2) ÷ (2 × 3) = **1**.

## Why effort means verification

Effort usually means the time a person needs to build something, counted in
hours, days, story points, or T-shirt sizes. I don't measure it that way.
Agents write the code, run the checks, and work in parallel worktrees,
sometimes unattended from plan to pull request (see
[Build](WORKFLOWS.md#build)). Work a person would size at several days can
take an agent far less, so build time ranks agent work badly.

What still takes my time is confirming the result is right. When existing
tests or CI prove a change, I can let it run and read the result quickly. When
no check can prove it, I have to judge it myself, however fast the agent was.
In [Anthropic's study of its own staff](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic),
people handed off tasks that were easy to check. One engineer called Claude
"absolutely amazing for everything where validation effort isn't large in
comparison to creation effort."

I considered two other measures. Human attention, meaning all the time I spend
specifying, steering, and reviewing, is closest to the real cost, but it is
hard to estimate before the work starts. Decision load, meaning the open
questions only I can answer, catches vague work but misses clear work that is
hard to check. Verification difficulty is the easiest of the three to score up
front, and checking the result is where much of my attention goes.

## Why fix-risk

Verification and fix-risk answer different questions. Verification is the
cost of finding out a change is wrong. Fix-risk is the cost if it ships wrong.
A CSS tweak with no visual tests is hard to verify but low risk. A change to
access permissions that the tests fully cover is easy to verify but high risk.

Fix-risk decides how much I can hand off. A low-risk change with good checks
can run on its own and still be safe to merge. Some changes, such as access,
money, or deletion, wait for my approval however good the checks are. Without
fix-risk, a dangerous change would rank near the top just because tests cover
it.

Both scores can come down. New tests make a change easier to verify and safer
to ship ([Testing with agents](TESTING.md)), so the tests that make a refactor
safe often rank above the refactor itself.

## Breaking ties

When two items score about the same:

1. Work that unblocks other items goes first, such as tests a later change
   depends on.
2. A security finding with strong evidence goes above other findings.

## Use the score to decide

The scores are coarse. They put a list in a sensible order so I can see
everything at once and choose. I still read the top of the list, check for
dependencies between items, and move an item when the score misses something.

When an agent ranks work for me, I want the whole list in leverage order, with
each item's scores. Items it would skip stay on the list with a one-line reason.
