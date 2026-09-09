# Finishing after the PR-opening skill

Read this after the option-1 reply continues into the installed PR-opening
skill.

The Approve 1 that entered finishing is already consumed. It never selects
Proceed to merge.

A Worker is a run already executing the `repo-gardener` Worker contract for
an assigned unit. Installing gardener does not make this a Worker.

## Publisher

If this run is a Worker, invoke the installed PR-opening skill with
`mode:pipeline`. Otherwise invoke it without pipeline. WORKFLOWS.md's
example is `ce-commit-push-pr`.

Title and body follow Compound Engineering: a new PR writes them;
`mode:pipeline` on an existing PR does not rewrite; `ce-babysit-pr` may
refresh a drifted description before looks-ready.

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

Otherwise, if this run is a Worker, invoke `ce-babysit-pr mode:pipeline` for
that pull request.

Otherwise invoke `ce-babysit-pr` by skill name for that pull request. Do not
write a host invocation prefix.

## After babysit

Looks merge-ready and cautiously looks ready are `ce-babysit-pr` terminals.
They are not a Merge Readiness Review. They are the trigger to start
`checking-merge-readiness`.

If babysit reports looks merge-ready or cautiously looks ready:

- Worker: stop and report that to the Orchestrator. Do not dispatch
  `checking-merge-readiness` from this conversation.
- Not a Worker: dispatch `checking-merge-readiness` to a fresh, read-only
  context with no prior involvement. Pass only the pull-request identity.
  Return that reviewer's brief and numbered merge menu unchanged. This
  skill does not pick it.

If `checking-merge-readiness` is absent after babysit on a non-Worker run,
name that once and stop. If a fresh uninvolved context cannot be opened, name
that once and stop. Do not grade merge in the conversation that built,
published, or babysat.

If babysit was skipped, never started, blocked, budget-stopped, needs-human,
or anything other than looks merge-ready or cautiously looks ready, stop. Do
not dispatch `checking-merge-readiness`.

Completion: a named stop after a publisher that did not create or update a
pull request, a named stop after a babysit skip, missing babysit skill, or
non-ready report, a Worker looks-ready report to the Orchestrator, a named
missing merge-readiness or missing independent reviewer on a non-Worker run,
or the independent merge-readiness menu on screen with no pick from this
skill.
