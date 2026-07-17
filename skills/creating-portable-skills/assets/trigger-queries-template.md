# Trigger query test: [skill-name]

Build 5 should-trigger phrasings (include at least one non-obvious wording)
and 5 near-misses. Judge each once at the listing level in a fresh agent
context: show the context only the skill's name and description alongside
the query and ask whether it would activate, requiring a plain yes, no, or
unsure.

Pass rule: every should-trigger activates and no near-miss does. An unsure
or hedged judgment counts as borderline. On a miss or a borderline call,
tune the description, then re-judge the entire should-trigger and
near-miss set, since an edit can newly activate a near-miss. Give any
query that stays borderline two extra runs (majority wins).

Full-rigor tier, for skills shipping to a public collection or where
triggering is unusually load-bearing: extend both tables to 8-10 queries
and run every query 3 times. A should-trigger then passes at 2 of 3, and
any near-miss activation still fails the whole set.

Date: [YYYY-MM-DD] | Harness: [name] | Model: [name]

## Should-trigger queries

| Query | Judgment | Extra runs (borderline only) |
| --- | --- | --- |
| [phrasing 1] | | |
| [phrasing 2] | | |
| [phrasing 3] | | |
| [phrasing 4] | | |
| [phrasing 5, non-obvious] | | |

Add rows up to 10 for the full-rigor tier.

## Near-miss queries (expected: no trigger)

| Query | Judgment | Extra runs (borderline only) |
| --- | --- | --- |
| [near-miss 1] | | |
| [near-miss 2] | | |
| [near-miss 3] | | |
| [near-miss 4] | | |
| [near-miss 5] | | |

Add rows up to 10 for the full-rigor tier.

## Tuning

Fix failures by front-loading trigger words and describing when to use the
skill, never by summarizing the workflow. A description that summarizes the
steps makes agents follow the summary and skip the body. After tuning,
re-judge the affected queries.
