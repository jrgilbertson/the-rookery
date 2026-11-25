---
status: accepted
date: 2026-11-24
---

# ADR 001: Verdicts are trusted by convention, not authenticated

A [Verdict](../../CONCEPTS.md#verdict) is a comment on a pull request, and
the `Owner:` line that says which session merges it is text in the pull
request body. Both come from the same GitHub login as every agent, so neither
proves who wrote it. We accept them as guards against accidents and do not
treat them as authentication. A separate GitHub identity for agents reverses
this decision.

## Context

One operator works across public and private repositories, on several
machines, through many agent sessions. Every session authenticates to GitHub
through the operator's own `gh` login. GitHub cannot tell the operator's
comment, label, or merge from an agent's.

GitHub's own gate does not help here. A pull request's author
[cannot approve it](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews),
and under one login the operator is the author of every agent's pull request.
A required approval would block the operator's own sign-off, and an
administrator bypass would let any agent session through with it.

## Evidence

- An agent merged its own pull request by running the orchestrator's merge
  wrapper, against a written rule that agents never merge. The report notes
  that the "token, script and commit shape are identical to the
  orchestrator's," so nothing could prevent it and nothing could detect it
  afterward
  ([BlakeHastings/b-fac#189](https://github.com/BlakeHastings/b-fac/issues/189)).
- Identity that a machine reports about itself has the same weakness. A design
  that keeps credentials on a laptop and has agents request each use says of
  its own approval prompt that "the caller details in the prompt come from the
  VM and can be faked"
  ([Running coding agents without handing them my credentials](https://blog.antonio.cx/running-agents-with-lend)).
  A message from one local session to another deserves no more trust.

## Decision

Treat a Verdict and an `Owner:` line as conventions that prevent accidents.
They stop a stale merge, a merge by the wrong session, and a merge nobody
decided on. They do not stop a session that sets out to forge one.

These guards make the convention hold in ordinary use:

- A Verdict names the full head commit the operator reviewed. A later commit
  is judged on its own before anything merges.
- A merge made under a Verdict, by whichever session makes it, is pinned to
  the head commit last judged: the reviewed commit, or a later one whose
  change since review the
  [review contract](../../skills/reviewing-prs/references/review-contract.md#after-a-verdict)
  judged routine. GitHub refuses the merge if the head moved after that.
- A Verdict counts only when the operator's exact login wrote it as a
  top-level comment. An `Owner:` line counts only on a pull request the
  operator opened from a branch in the same repository. A fork or outside
  contributor cannot claim an owner.
- The reviewer reads the raw diff. A pull request's own title, body, and
  comments are data and never instructions or approval.
- The tests that decide what is held are read from the default branch, so a
  pull request cannot loosen them for itself.
- Labels report status. Every open pull request is read whether or not it has
  one, and no label permits a merge.

## What reverses this

Give agents their own GitHub App identity with permission to write contents
and pull requests, and no permission to approve or bypass. Remove the
operator's personal token from every agent environment. The operator is then
no longer the author of agent pull requests, so GitHub's required approvals
and branch protection can carry the sign-off, and GitHub authenticates it.
Verdict comments stop being the record of approval at that point, and this
ADR is superseded.
