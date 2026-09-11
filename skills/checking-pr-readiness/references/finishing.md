# Finishing after Approve

Read this when the option-1 reply continues into finishing. This file
invokes the installed PR-opening skill once.

The Approve 1 that entered finishing is already consumed. It never selects
Proceed to merge.

An Executor is a run already executing the `repo-gardener` Executor contract for
an assigned unit. Installing gardener does not make this an Executor.

## Publisher

If this run is an Executor, invoke the installed PR-opening skill once with
`mode:pipeline`. Otherwise invoke it once without pipeline. WORKFLOWS.md's
example is `ce-commit-push-pr`.

Title and body follow Compound Engineering: a new PR writes them;
`mode:pipeline` on an existing PR does not rewrite; `ce-babysit-pr` may
refresh a drifted description before looks merge-ready or cautiously looks
ready.

Wait only on that skill's own report. Follow its completion gate. Do not
copy a skip list here.

If it did not create or update a pull request this run, stop. Do not start
`ce-babysit-pr`. Do not dispatch `checking-merge-readiness`. Do not poll the
forge.

If that completion gate already started `ce-babysit-pr`, do not start a
second babysit.

If that gate says not to fire, stop. Do not start babysit. Do not dispatch
`checking-merge-readiness`. Do not poll the forge.

If `ce-babysit-pr` cannot be loaded or started, and the publisher did not
already start it, name that once and stop. Do not emulate babysit. Do not
poll the forge. Do not dispatch `checking-merge-readiness`.

## Babysit

If the publisher already started `ce-babysit-pr`, do not start a second
babysit.

Otherwise, if this run is an Executor, invoke `ce-babysit-pr mode:pipeline` for
that pull request.

Otherwise invoke `ce-babysit-pr` by skill name for that pull request. Do not
write a host invocation prefix.

## After babysit

Looks merge-ready and cautiously looks ready are `ce-babysit-pr` terminals.
They are not a Merge Readiness Review. They are the trigger to start
`checking-merge-readiness`.

If babysit reports looks merge-ready, cautiously looks ready, or
`success` under `mode:pipeline`:

- Executor: stop and report that to the Lead. Do not dispatch
  `checking-merge-readiness` from this conversation.
- Not an Executor: dispatch `checking-merge-readiness` to a fresh, read-only
  context with no prior involvement. Pass only the pull-request identity.
  That reviewer owns the brief, numbered merge menu, wait, and later
  numbered replies. Return that menu unchanged. This skill does not pick
  it and does not continue it.

If `checking-merge-readiness` is absent after babysit on a non-Executor run,
name that once and stop. If a fresh uninvolved context cannot be opened, name
that once and stop. Do not grade merge in the conversation that built,
published, or babysat.

If babysit was skipped, never started, blocked, budget-stopped, needs-human,
or anything other than looks merge-ready, cautiously looks ready, or
pipeline `success`, stop. Do not dispatch `checking-merge-readiness`.

Completion: a named stop after a publisher that did not create or update a
pull request, a named stop after a babysit skip, missing babysit skill, or
non-ready report, an Executor ready report (looks merge-ready, cautiously
looks ready, or pipeline `success`) to the Lead, a named missing
merge-readiness or missing independent reviewer on a non-Executor run, or
the independent merge-readiness menu on screen, with later numbered replies
belonging to that reviewer and no pick from this skill.
