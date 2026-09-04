# Worker contract

A Worker owns one unit: an isolated worktree, one branch, and at most one
unmerged pull request. It does not survey lanes, change the durable policy,
or write tracker records. Everything below is the whole of what a Worker must
follow; the Orchestrator's brief supplies the facts.

## Portable interface

Before dispatch the host provides:

1. an isolated Worker worktree at the authoritative base (for an adopted PR:
   that PR's head branch checked out at the hosted head OID captured at
   dispatch);
2. repository-native setup when the host supplies it;
3. supervision before mutation and through Worker completion; and
4. a Worker-owned branch with at most one unmerged PR.

The host owns how it provisions setup and supervision. If the host cannot
safely provide the interface, the Worker does not mutate; it finishes a
read-only report naming the unavailable capability.

## The brief

The brief names the authoritative base, policy revision, Worker identity and
branch, scope, protected paths, lane grant, assigned slice, and the exact
caller-approved verification command argv list. For an adopted PR it also
names the PR number, head ref, captured head OID, base ref and full base OID,
the named gap(s), and that the update bot will stop maintaining the branch
after the first Worker push. It includes the ledger attribute read and
base-diff rule only when that exception applies.

## Before the first mutation

Wait for host setup to succeed. Run `git status --porcelain=v1
--untracked-files=all`; a failed read or any staged, unstaged, or untracked
non-ignored path stops dependent work, names the affected paths (or the
assigned slice when status is unreadable), and leaves unexpected material
untouched. For an adopted PR, also require local HEAD to equal the captured
hosted head OID, and re-read every named gap from native facts now and again
before publication; if a gap is gone, changed, or ambiguous, stop the unit
and report it without publishing.

Authoring is allowed only inside the five gates in `policy-and-entry-modes.md`. For an adopted PR the gates apply to the paths the Worker's
own commits change; the adopted PR's existing diff is native state, reported,
not authored. A rename counts both its old and new path.

## Completion

The Worker owns planning, implementation, simplification, review, repository
verification, its coherent commit, and its branch/PR. It reports each assigned
gate as pass, failure, or unavailable. Every unattended Worker invokes
`checking-pr-readiness` normally on the exact head in its worktree (for an
adopted PR, with the PR base passed as `--base`) and stops after its brief and
numbered menu. After a Worker PR exists, the scheduled ownerless run has that
Worker invoke `checking-merge-readiness` on that PR and stops after its brief
and numbered menu. The activating utterance is never approval. On a distinct
later turn, the Orchestrator authorizes that Worker to reply 1 only when the
menu offered option 1 and the recommendation was approve and proceed for that
same exact head. The Worker never chooses option 1 on its own. The
Orchestrator never authorizes Proceed to merge. The checking skill then
performs its identity reread, instantiates its evidence pack as silent
pull-request-body input, and continues into the publication path below; for
an adopted PR that path is the existing-PR update, not an absent-ref create.
Do not also dispatch an owner publisher. Direct assessment of native facts is
not a publish path. With an owner, publication remains subject to the owner's
interactive authorization.

When a brief names Worker-owned gaps, the Orchestrator sends every named
Worker-owned gap to the same Worker, even when the brief also names owner
work. After a repair of an existing PR, publish the repaired exact head under
the existing lease before the next helper gather, then re-run that helper on
the current exact head. Stop when only owner-needed work remains or a further
turn cannot help. An unavailable checking skill, moved identity, or a
later-session claim must preserve the authored commit without push or PR
creation and name the blocking gap.

## Publication gates

Immediately before an ownerless first push, re-resolve the captured
target/base ref and full base OID. Immediately before PR-open, re-resolve the
captured target/base ref and full base OID; the same reread precedes every
repaired-head update. At each of those points also: re-read `.agents/repo-gardener.yaml` from
the refreshed default branch and require the opening policy revision from the
brief (a changed, unavailable, or unknown revision stops the action); reread
the porcelain status above; and validate the committed paths against the
assignment, identity, scope, and protected paths. Scope is exclude-wins: each
committed path must match at least one include glob and no exclude glob, and
no path may be protected. For an adopted PR the committed paths are the
Worker-authored diff from the captured hosted OID. Then read overlap: the
intersection of the committed paths with the changed paths of every other
current native branch and open PR, excluding the Worker's own adopted PR; a
shared path is permitted only when the brief names it as a union-merged
ledger and the Worker's diff adds only its own entry while retaining every
base entry. Any other intersection stops the action. An
ownerless first push must match the subject and OID the checking skill
re-read; a repaired-head update must match only its exact
Orchestrator-authorized repaired subject and OID. Never replace or recapture
that authorized identity. A mismatch, unavailable or unknown read, base
movement, unauthorized path, or native overlap stops that action and
preserves the authored work.

After those gates pass, provider state is exhaustive:

- an absent provider ref may be atomically created at the exact authorized
  head only under an absent-ref lease (`--force-with-lease=<ref>:` or a
  proven equivalent);
- a provider ref already equal to that head needs no push;
- only an Orchestrator-authorized update of the same Worker's PR, including
  the first push to an adopted PR, may atomically update its exact previously
  observed hosted head to the exact authorized head under a lease expecting
  that old OID (for an adopted PR, the OID captured at dispatch). A moved
  hosted head, for example a bot rebase, fails the lease, stops that
  publication, preserves the local commit, and is named; never recapture and
  retry.

Refuse unavailable or unknown provider state, any other provider OID, or a
lease failure. After a create or update, read back and require the exact
authorized provider OID. After a successful first push to an adopted PR, the
report names that PR as owner-maintained from that push ("adopted; bot
automation may no longer update this branch"). Never advance competing
movement implicitly, never merge, and never write a release, deployment,
protected path, or unapproved follow-up issue. Report native PR, check, and
review facts.
