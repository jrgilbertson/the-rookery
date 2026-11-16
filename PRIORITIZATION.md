# How I prioritize

I rank work by leverage: how much good a change does, weighed against what it
costs to check and what it would take to undo. When I sort a list of findings,
ideas, or tasks, I use this order.

```text
leverage = (impact × confidence) ÷ (verification effort × undo cost)
```

This is the traditional ICE score (impact, confidence, ease), modified in two
ways for AI development:

- Verification effort replaces ease. Ease asks how much it takes to do the
  work: the time, the people, the cost, and the complexity. With AI that is
  hard to predict, because work that took a person weeks can take an agent
  hours, or sometimes minutes. How hard the result is to verify is easier to
  estimate, and it is more often what holds a change up.
- Undo cost is added. It covers what the change could break and what it takes
  to undo it.

I can estimate both before the work starts, which is no longer true of the
build itself.

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

Some work changes nothing users see: a refactor, a CI fix, or tests for code
that has none. I score it by the user-facing result it protects or makes
possible. If the save feature has no tests, adding them protects users from
losing work, so they score the same impact as a bug that loses work. A
refactor that a planned feature needs scores the impact of that feature.
Confidence then asks how likely that result is. It is 3 when the feature is
planned or the failure has happened before. It is 1 when either is only
possible someday. Work that leads to no such result scores 1 on impact.

A change includes its own tests. Tests count as separate work only when they
cover code that already exists.

Three examples:

- A bug that loses saved work, with a reproduction I already have and a
  one-line, isolated fix: (3 × 3) ÷ (1 × 1) = **9**.
- A refactor that a planned feature needs, in code many callers use and no
  tests cover. The feature is a clear improvement to something users do
  often, and the refactor needs new tests as part of the work:
  (2 × 3) ÷ (2 × 2) = **1.5**.
- An idea to redesign onboarding. It could change whether new users get
  started at all, but it is a guess, only people can judge the result, and it
  reaches every new user: (3 × 1) ÷ (3 × 2) = **0.5**.

## Why verification effort, not build effort

Effort usually means how much it takes to build something: the time, the
people, the cost, and the complexity. Teams count it in hours, days, story
points, or T-shirt sizes. That worked when people did the building, because a
build estimate covered the whole job. The person writing the code was also
testing it as they went.

AI changed that in two ways. Building still takes real work, but how much is
hard to predict. Work that took a person weeks can take an agent hours, and
sometimes minutes, and I often can't tell which in advance.

Building is also less of the bottleneck than it was. In a
[Harvard study of 655 companies](https://fion.ac/jellyfish.pdf), lines of code
rose 44% after teams adopted agents, but issues resolved rose about 14%. The
authors' summary: "Code review becomes the bottleneck." Anthropic reports the
same about its own engineers. In
[March 2026](https://claude.com/blog/code-review) it said code output per
engineer had grown 200% in a year and that "Code review has become a
bottleneck." By
[October](https://www.anthropic.com/research/employment-at-anthropic), commits
per engineer were five times what they had been six months earlier, and its
report called human attention "a constant bottleneck."

What I can estimate is how hard the result is to verify. Two changes can take
an agent the same time to build. If existing tests prove the first one, it's
done when the build is. If the second needs a person to try it and judge the
result, it takes as long as that judgment takes. Build effort would score the
two the same, and verification effort tells them apart. In
[Anthropic's study of its own staff](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic),
one engineer called Claude "absolutely amazing for everything where validation
effort isn't large in comparison to creation effort."

Judgment is the expensive end of the scale, and a sign-off is a weak check
there. In an
[Anthropic experiment with 50 analysts](https://www.anthropic.com/research/agents-judgment-calls),
each agent's lean on a judgment call was set by a coin flip, and the analysts
"went with their agent's lean 86% of the time."

Verification effort can come down. Give the agent something it can run that
comes back pass or fail, and it can check its own work and keep going
([Anthropic's agent guidance](https://code.claude.com/docs/en/best-practices)
makes the same point). Good tests and CI do that for every later change
([Testing with agents](TESTING.md)). My
[durability ladder](WORKFLOWS.md#maintain) follows the same idea: prefer a
check that runs automatically, and fall back to a written instruction only
when nothing stronger fits.

I considered two other measures. Human attention is all the time I spend
specifying, steering, and reviewing. It is closest to the real cost, but it is
hard to estimate before the work starts. Decision load is the number of open
questions only I can answer. It catches vague work but misses clear work that
is hard to check. Verification effort is the easiest of the three to score up
front, and checking the result is where much of my attention goes.

## Why undo cost

Verification effort and undo cost answer different questions. Verification
effort is the cost of finding out a change is wrong. Undo cost is the cost of
reversing it after it ships. A CSS tweak with no visual tests is hard to
verify but cheap to undo. A change to access permissions that the tests fully
cover is easy to verify, but exposed access can't be undone.

Undo cost decides how much I can hand off. A two-way door is a change a revert
undoes, so an agent can make it on its own. A one-way door is a change a
revert can't undo, such as deleting data or sending a message. It waits for my
approval however good the checks are. Without undo cost, a one-way door would
rank near the top just because tests cover it.

One-way doors are also rare, so stopping for them costs little. When
[Anthropic measured about a million agent actions](https://www.anthropic.com/research/measuring-agent-autonomy),
"only 0.8% of actions appear to be irreversible."

## Breaking ties

When items tie:

1. An item that another item on the list depends on goes first.
2. A security finding with strong evidence goes above other findings.

## Use the score to decide

The scores are coarse. They put a list in a sensible order so I can see
everything at once and choose. I still read the top of the list, check for
dependencies between items, and move an item when the score misses something.

When an agent ranks work for me, I want the whole list in leverage order, highest
first, with each item's scores. Items it would skip stay on the list with a one-line reason.
