# How I prioritize

I rank work by leverage: how much good a change does for what it costs to get
it done safely. When I sort a list of findings, ideas, or tasks, I use this
order.

```text
leverage = (impact × confidence) ÷ (verification effort × undo cost)
```

This is the ICE score that product and growth teams use (Impact, Confidence,
Ease), changed in two ways for work that agents do:

- Verification effort replaces ease. It measures how hard the result is to
  verify, not how long it takes to build.
- Undo cost is added. It covers what the change could break and what it takes
  to undo it.

## The four factors

Each factor gets a score from 1 to 3.

| Factor | Question | 1 | 2 | 3 |
|---|---|---|---|---|
| Impact | How much better does this make things for users? | Users would barely notice | A clear improvement to something users do often | Changes whether most users can do a core task, or whether they can trust the product with their work |
| Confidence | How sure am I that we can do this and it will deliver the impact? | A guess. The problem or the approach is unproven | Good reasons to expect it, but nothing confirmed | Confirmed. I verified the problem, or the approach has worked before |
| Verification effort | How hard is it to confirm the result is right? | Existing tests, types, CI, or a reproduction I already have prove it | It needs new tests or one targeted manual check | No check can prove it, so it needs judgment, such as taste, UX, performance under real load, or behavior across systems |
| Undo cost | If this change is wrong, what does it take to undo it? | Two-way door, contained. It touches one place, and a revert undoes it | Two-way door, wide. Many callers or users are affected, but a revert undoes it | One-way door. A revert can't undo it: deleted or migrated data, money moved, messages sent, access exposed, a published contract |

Impact already covers the harm of doing nothing. A security hole or a
data-loss bug scores high on impact, because users can't trust the product
with their work. Undo cost covers only the change.

Users are whoever the product is for. When the product is a tool or a skill,
that includes the developers and agents who use it.

Tests, CI, refactoring, and a repo's internal tooling usually change nothing
users see. I score that work by the user-facing result it protects or makes
possible. A test that protects saving gets the impact a bug in saving would
have. A refactor gets the impact of the change it makes possible. Confidence
then asks how likely that result is. It is 3 when the change is planned or
already on the list, or the failure has happened before. It is 1 when the
change or the failure is only possible someday. Work that leads to no such
result scores 1 on impact.

Three examples:

- A bug that loses saved work, with a reproduction I already have and a
  one-line, isolated fix: (3 × 3) ÷ (1 × 1) = **9**.
- A refactor that a planned feature needs, in code many callers use and no
  tests cover. The feature is a clear improvement to something users do
  often: (2 × 3) ÷ (2 × 2) = **1.5**.
- The tests for that code. They take the same impact and confidence, CI
  proves them, and they change no product code: (2 × 3) ÷ (1 × 1) = **6**.
  Once they merge, the refactor's verification effort drops to 1 and it scores
  3.

## Why verification effort, not build time

Effort usually means the time a person needs to build something, counted in
hours, days, story points, or T-shirt sizes. I don't measure it that way.
Agents write the code, run the checks, and work in parallel worktrees,
sometimes unattended from plan to pull request (see
[Build](WORKFLOWS.md#build)). Work a person would size at several days can
take an agent far less, so build time says little about what the work costs
me.

What still takes my time is confirming the result is right. When existing
tests or CI prove a change, I can let it run and read the result quickly. When
no check can prove it, I have to judge it myself, however fast the agent was.
In [Anthropic's study of its own staff](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic),
people handed off tasks that were easy to check. One engineer called Claude
"absolutely amazing for everything where validation effort isn't large in
comparison to creation effort."

I considered two other measures. Human attention is all the time I spend
specifying, steering, and reviewing. It is closest to the real cost, but it is
hard to estimate before the work starts. Decision load is the number of open
questions only I can answer. It catches vague work but misses clear work that
is hard to check. Verification effort is the easiest of the three to score up
front, and checking the result is where much of my attention goes.

## Why undo cost

Verification effort and undo cost answer different questions. Verification
effort is the cost of finding out a change is wrong. Undo cost is what it
takes to undo it. A CSS tweak with no visual tests is hard to verify but cheap
to undo. A change to access permissions that the tests fully cover is easy to
verify, but exposed access can't be undone.

Undo cost decides how much I can hand off. An agent can take a two-way door on
its own: if the change is wrong, a revert undoes it. A one-way door waits for
my approval however good the checks are, because a revert can't bring back
deleted data or unsend a message. Without undo cost, a one-way door would rank
near the top just because tests cover it.

Verification effort can come down. New tests make a change easier to verify
([Testing with agents](TESTING.md)), which is why the tests in the example
above rank higher than the refactor they protect.

## Breaking ties

When items tie:

1. An item that another item on the list depends on goes first.
2. A security finding with strong evidence goes above other findings.

## Use the score to decide

The scores are coarse. They put a list in a sensible order so I can see
everything at once and choose. I still read the top of the list, check for
dependencies between items, and move an item when the score misses something.

When an agent ranks work for me, I want the whole list in leverage order, with
each item's scores. Items it would skip stay on the list with a one-line reason.
