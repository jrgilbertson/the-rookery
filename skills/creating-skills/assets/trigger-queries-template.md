# Trigger query test: [skill-name]

Build 8-10 should-trigger phrasings (include non-obvious ones) and 8-10
near-misses. Run each query 3 times in a fresh agent context with the skill
installed.

Pass rule: each should-trigger query must activate in at least half its runs
(rate of at least 0.5 across the 3 runs — 2 of 3). ANY near-miss activation
fails the whole set.

Date: [YYYY-MM-DD] | Harness: [name] | Model: [name]

## Should-trigger queries

| Query | Run 1 | Run 2 | Run 3 | Rate |
| --- | --- | --- | --- | --- |
| [phrasing 1] | | | | |
| [phrasing 2] | | | | |
| [phrasing 3] | | | | |
| [phrasing 4] | | | | |
| [phrasing 5] | | | | |
| [phrasing 6] | | | | |
| [phrasing 7] | | | | |
| [phrasing 8] | | | | |
| [phrasing 9, optional] | | | | |
| [phrasing 10, optional] | | | | |

## Near-miss queries (expected: no trigger)

| Query | Expected | Run 1 | Run 2 | Run 3 |
| --- | --- | --- | --- | --- |
| [near-miss 1] | no trigger | | | |
| [near-miss 2] | no trigger | | | |
| [near-miss 3] | no trigger | | | |
| [near-miss 4] | no trigger | | | |
| [near-miss 5] | no trigger | | | |
| [near-miss 6] | no trigger | | | |
| [near-miss 7] | no trigger | | | |
| [near-miss 8] | no trigger | | | |
| [near-miss 9, optional] | no trigger | | | |
| [near-miss 10, optional] | no trigger | | | |

## Tuning

Fix failures by front-loading trigger words and describing when to use the
skill — never by summarizing the workflow. A description that summarizes the
steps makes agents follow the summary and skip the body. After tuning,
re-run the full set.
