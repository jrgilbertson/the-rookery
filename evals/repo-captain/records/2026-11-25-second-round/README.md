# Repo Captain Eval Record · 2026-11-25, second round

The four cases whose skill arm failed in
[the first round](../2026-11-25-first-round/README.md), rerun after the fixes.
Two failures had instruction causes: the skill now says to plan every coupled
leaf before the first dispatch, and to reply to a wake with nothing new in
one line. The other two had fixture causes: pull request bodies claimed tests
their diffs lacked, and the fixtures now include those tests.

- **Host, date, model, effort, runner, and labels** as in the first round:
  `claude-opus-5-5` at high effort, one `claude -p --safe-mode` process per
  turn, and a `claude-sonnet-5-5` grader subagent.
- **Skill revision** `skills/repo-captain` at commit `b4e6b671`.
- **Cases** coupled-plan-versus-uniform-backlog and
  held-pr-keeps-wake-and-calm-alert at commit `b4e6b671`, and
  domain-lead-custody-and-self-merge and overlap-and-one-migration at commit
  `480f33e7`. The case-set SHA-256 at `480f33e7` was
  `2c22126b92dbf2d44941dd5124fa8813e4da6933c4aed841e9e69bd83ad6b9c8`.
- **Baseline** `skills/coordinating-work`, rerun only on the two cases whose
  fixtures changed. The two cases whose fixtures did not change keep their
  first-round Baseline.
- **Repeats and completion** one run per case and arm. All six finished.

A first attempt at the two fixture cases is not recorded. That fixture edit
added each claimed test file twice, once through the staged commit and once
in the diff text, so each diff listed the file twice with different blobs.
The Captain held those pull requests as unreadable, which was correct for
the world it saw. Commit `480f33e7` removed the duplicate, and the runs below
use it.

## Results

| Case | `repo-captain` | Baseline | Output tokens, skill / Baseline |
| --- | --- | --- | ---: |
| [coupled-plan-versus-uniform-backlog](../../cases/coupled-plan-versus-uniform-backlog/case.yaml) | 4/5 | first round: 2/5, 2 unmeasured | 17,459 / – |
| [held-pr-keeps-wake-and-calm-alert](../../cases/held-pr-keeps-wake-and-calm-alert/case.yaml) | 3/5, 1 unmeasured | first round: 1/5 | 8,648 / – |
| [domain-lead-custody-and-self-merge](../../cases/domain-lead-custody-and-self-merge/case.yaml) | 3/4 | 0/4 | 17,171 / 11,060 |
| [overlap-and-one-migration](../../cases/overlap-and-one-migration/case.yaml) | 3/4 | 0/4, 2 unmeasured | 23,169 / 23,730 |

The six runs used 101,237 output tokens, 5,757,905 cache-read tokens, and
346,096 cache-write tokens over 1,389 seconds. The unrecorded attempt used
63,580 output tokens. Cost is unknown, as in the first round.

## What the round shows

- **Neither instruction fix took.** The coupled-plan run again wrote the
  later leaves' briefs after starting the first worker. The held-pull-request
  run again gave a full report on a wake with nothing new, and its check that
  a wake was armed is unmeasured because the runner has no timer. Under
  [SKILLS.md](../../../../SKILLS.md#improving-from-real-use), a failure that
  returns after its fix is kept as an Eval Case, which both already are.
- **The fixed migration case now runs the queue.** The Captain enqueued #531
  pinned to its head, enqueued #532 after #531 merged, and swapped labels
  only after the merges. Its one failure is the overlap check: it held #525
  as stacked on #520 and never named the shared `app/billing/invoice.ts`.
- **The Domain Lead case has a second fixture flaw.** The Captain again
  declined to merge #570, this time because the `Invoice` type on `main` has
  no `dueDate` field, so the sort changes nothing and its test passes only
  through a type cast. Merging would have closed #567 without delivering it.
  That refusal is right, so the case's premise that #570 is routine is wrong.
  The label stays a Fail here; the fixture needs a `dueDate` field on
  `main` before this check can measure the Captain.
- **The Baseline still does nothing in either fixture case.** It proposed a
  setup and made no writes.

Limits are those of the first round, including the Orca stand-in that hid
worker worktrees.
