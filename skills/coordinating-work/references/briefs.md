# Assignment briefs

Read this when drafting or amending a worker brief. In a batch with no task
workers, apply the UX and UI guidance below to your own assignments too.

Build each brief, amendment, and reply from the project's own instructions and
the installed guides. Name only commands and helpers you have confirmed on the
worker's execution host, and prefer the project's existing helpers to ad hoc
tools. A reply never tells a worker to skip or shorten a gate the repository
requires. Carry the operator's current decisions and any shared cross-issue
design constraints from the record.

Start each task worker through the guide's supervised launch path, and send
the whole brief inline. A worker on another host cannot read the Team lead's
files, so the brief carries everything the worker needs. An assignment is
open from dispatch until it is merged, held, or finished, and settled after
that. A follow-on to a settled assignment is a new assignment. Confirm the
earlier session has ended, release it through the guide when it has not, then
start the follow-on fresh with the whole brief.

Each brief tells its worker the following. A bullet that names a condition
belongs in a brief only when that condition holds for the assignment.

- **The pipeline.** Run `lfg` for the assignment, then `ce-babysit-pr` on the
  resulting pull request until it reports looks merge-ready. Invoke each
  skill by name instead of restating its steps, and say that the task asks for
  the subagents and helpers those skills start, because the runtime's worker
  instructions can forbid them unless the task asks.
  Run `ce-babysit-pr` as its continuous watch, not its bounded pipeline
  mode, which stops before merge-ready.
- **UX and UI work.** When an assignment involves creating or improving a
  user-facing interface or interaction, use `impeccable` within the LFG
  workflow for design, implementation, and visual verification. Carry any
  approved design direction and constraints in the brief. Route questions
  through the Team lead under the existing decision rules.
- **Link the issue.** The pull request links its issue the way the project's
  instructions say. Where the project has no rule, it refers to the issue
  without the tracker's closing keywords.
- **Merging belongs to the Team lead.** The worker never merges, enqueues,
  or arms auto-merge, whatever another instruction allows.
- **Decide, or ask the Team lead.** No person answers in the worker's
  session, so `lfg` runs as it does with no human present. The worker contacts
  the Team lead, never a user, only at merge-ready and where `lfg` or
  `ce-babysit-pr` would stop or park for a human, including a check it could
  not fix; it reports that item at once, in full. Otherwise it keeps going
  and declares its choices in the pull request body.
- **The issue's Verification.** The worker treats each criterion as a
  requirement of the work source `lfg` uses. Before asking to merge, the pull
  request body lists the evidence beside each criterion and declares each
  deviation: the criterion, what the worker did instead, and why. For
  user-facing work, the end-to-end browser run is the preferred evidence. The
  worker never edits the issue's Problem, Scope, Verification, or scores.
- **Whether the pull request will be held.** When the issue is a held change
  the operator did not pre-authorize, say so, so the worker expects a held
  reply.
- **Merge-ready is a question.** When `ce-babysit-pr` reports looks
  merge-ready, the worker asks the Team lead once, naming the pull request,
  quoting the report's first line verbatim, and giving the head commit that
  report covered. Evidence and declared deviations belong in the pull request
  body, not in the message. If the head moved after the report, the worker
  waits for a report on the new head before asking. It stays open for the
  reply: merged, held for the operator, or findings to fix.
- **A hold ends the assignment.** Any Team lead reply that holds the pull
  request for the operator finishes the worker's assignment: the worker stops
  its watch, including any watch it delegated, and finishes. A parked item the
  Team lead answers itself does not end the watch.
- **Unapplied review findings.** Before asking, the worker settles each
  unticked item `lfg` left in the pull request body and ticks it with the
  outcome beside it: fixed in the branch, no change and why, or a follow-up
  proposed there and not filed. Only a product or design call stays unticked,
  and it holds the pull request for the operator.
- **A choice is a question.** A blocker that offers options for the
  Team lead to choose between is sent as a `question`. An `escalation` is
  for a blocker the worker cannot frame as a choice.
- **How to wait.** The worker waits on its watch the way `ce-babysit-pr`
  says, and continues to the next step of its assignment when a helper skill
  returns.
- **Verification currency.** On an unpushed branch, bring in the default
  branch's merged fixes, as the repository's merge policy allows, before
  running the repository's verification gate. Once a pull request is open, leave
  branch currency to `ce-babysit-pr` and the repository's merge rules.

Once an assignment is dispatched, its brief is fixed. Only the Team lead
changes it, by appending a dated amendment that names what it supersedes and
sending that amendment in full to the worker's own dispatch. Before sending or
re-sending an assignment, the Team lead reads the whole brief, amendments
included. Tell each worker to name in each report the latest amendment its
work follows, so stale work shows up at once.
