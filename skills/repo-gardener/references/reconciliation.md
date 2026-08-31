# Orchestrator and Worker workflow

This reference reconciles repository, provider, and Worker facts during a
managed run. It complements the policy and lane contracts; Repo Gardener
creates neither a host adapter nor a second Git-state system. Orca may supply
the Run interface, but any host that satisfies
the mutation boundary in `SKILL.md` is suitable.

## Pre-open facts

Read the target repository's durable file from the refreshed default branch,
the complete tracker, repository instructions, and the native identities needed
to open safely. Validate the durable file without changing it. A missing,
invalid, or unapproved file takes the entry mode in
`policy-and-entry-modes.md`: interactive first use with an owner, or blocked
or read-only sensing otherwise.

At opening, preserve the exact policy revision. A later policy change stops
all remaining declared audits and source mutation, push, and PR opening. It
does not relitigate unchanged grants or erase already-authored work. Continue
safe sensing and make a truthful close only when the remaining authority still
permits it.

Write and exactly read back `run-opened` before managed sensing. The
caller-only branch performs only the required identifier census and nine-lane
read-only survey. It writes no run records, executes no declared audits, and
does not claim managed closure.

## Declared audits and sensing

For each eligible lane, run only its normalized `audit_commands`, in policy
order, using the approved direct argv. Check capability, protected policy,
subject revision, and clean worktree immediately before the command. Keep
raw stdout and stderr in bounded private capture. When files are needed, use a
fresh canonical non-symlink per-run temporary directory outside the repository
with mode `0700` and regular files with mode `0600` only; drain and discard
excess.
Sanitize and redact only bounded inert evidence, promptly delete captures, and
best-effort clean them up on interruption. Raw output never enters repository
source, trackers, reports, logs, or recovery state. A command result is
evidence, not an admission verdict or mutation grant.

A finished command, ordinary failure, missing runner, missing nested
executable, or command-local capability refusal is lane-local: report it and
continue safe work. A policy or subject change, unexpected worktree change,
uncertain termination, interruption, or unknown provider effect stops the
affected command and dependent work. Leave unexpected changes untouched. Do
not clean, restore, retry, resume, or replace a command automatically.

Complete every installed lane once after its required census. Separate source
census, evidence-qualified lane candidates, and normalized candidates. For
issue lanes, use purpose-bounded reads and derive the Ready Frontier fresh from
the complete census and current evidence; mapped readiness ranks reads but
does not decide admission. Scouts are read-only and never own a PR.

Deepen while another investigation could change an assignment or
recommendation, then stop. Prefer credible critical-flow risks, independent
corroboration, measurement defects, overdue coverage with a current signal,
and then the strongest remaining finding. For each investigation, state the
evidence, bounded slice, questions, checks, findings, uncertainty, and
issue-ready next action.

## Decide whether to author

Select only non-overlapping, independently deliverable, low-risk, testable
units small enough for one coherent PR. Author only when the opening policy
still has the exact repository identity, allowed path scope, positive
`maximum_workers`, enabled lane mutation, and no protected path. A denial
stops that unit; an honest read-only result is successful operation.
Selection and dispatch for the run never exceed the opening policy's
`maximum_workers` cap; unrelated existing PRs do not consume that cap.

`shared_ledger_paths` is an assignment-only exception for the same originally
approved siblings, and only when the opening policy and repository proof
establish a conflict-safe additive merge check. Their Worker briefs bind the
same Worker identity, branch, and disjoint slices: a native branch or PR
overlap may proceed only when those facts still prove that binding and the same
ledger path. It does not exempt another path, protected path, authoring scope,
or a new or unrelated overlap, which stops publication. Every Worker using it
adds only its attributable entry and retains all base entries; later native
conflicts are for human handling.

Before dispatch, require the portable mutation interface:

1. an isolated Worker worktree at the authoritative base;
2. repository-native setup when the host supplies it;
3. supervision before mutation and through Worker completion; and
4. a Worker-owned branch with at most one unmerged PR.

The host owns how it provisions setup and supervision. Do not add a
Repo Gardener setup command, startup configuration, receipt, waiting loop,
recovery path, progress record, registry, schema, or state machine. If the
host cannot safely provide the interface, do not mutate; finish the read-only
report and name the unavailable capability.

Wait for any host-provided repository setup to succeed before
repository-dependent inspection, tests, or mutation. Immediately before the
first mutation, run ordinary native `git status --porcelain=v1
--untracked-files=all`. A failed read or any staged, unstaged, or untracked
non-ignored path stops only dependent work, names the affected paths (or the
assigned slice when status is unreadable), and leaves unexpected material
untouched without restoring, staging, or committing it.

The Worker brief names the authoritative base, policy revision, Worker identity
and branch, scope, protected paths, lane grant, assigned slice, and exact
caller-approved verification command argv list. Include the ledger proof and
base-diff rule only when that exception applies. Workers do not run the nine
lanes, change the durable policy, or write tracker records.

## Worker completion and publication

Each Worker owns planning, implementation, simplification, review, repository
verification, its coherent commit, and its branch/PR. It reports each assigned
gate as passed, failed, or unavailable. Assess the clean exact commit directly
by default. When a compatible readiness helper is available and useful, use it
only noninteractively for a report; it never adds execution or publication
authority. Either path produces the same-session, human-readable `ready` or
`action-required` result for the exact subject, full head OID, target/base ref
and OID, inspected paths, relevant checks, and final cleanliness. The
assessment uses the same assignment-owned exact argv list and cannot expand
execution authority.

For ownerless publication, bind the exact subject, full head OID, target/base
ref, and full base OID to one same-session readable `ready` or
`action-required` assessment. `ready` must cover those exact identities,
inspected paths, relevant checks, and final cleanliness. Any failure,
unavailable or incomplete evidence, drift, dirt, or unknown state is
`action-required`; preserve the authored commit, do not push or open a PR,
name the blocking gap, and require a fresh exact assessment before any later
publication attempt. With an owner, normal publication remains subject to the
owner's interactive authorization.
Immediately before every push and every PR opening, refresh the durable policy
file from the authoritative default branch and require its revision to match
the opening revision. A mismatch, unavailable or unknown refresh/read stops
that publication action and preserves the authored work.
The assessment records `not verified` and `not run` rather than inventing
success. Immediately before an ownerless first push, compare them to the
captured subject and OID that received `ready`; never replace or recapture that
authorized identity. Immediately before an ownerless first push, re-resolve
the captured target/base ref and full base OID. Immediately before PR-open,
re-resolve the captured target/base ref and full base OID.

Immediately before an ownerless first push and immediately before PR creation,
reread `git status --porcelain=v1 --untracked-files=all`; a failed read or any
staged, unstaged, or untracked non-ignored path stops publication. Immediately
before push and before PR opening, validate the committed paths against the
assignment, identity, scope, protected paths, and, where relevant, the ledger
base diff. Reconcile the current local head, exact target/base, native branch
and PR overlap, and provider branch. A provider branch may be absent for the
first push or must match the authorized OID exactly; permit a ledger overlap
only under the same-assignment binding above. After observing an absent provider
ref, atomically create it only with an explicitly absent expected ref, using
Git's `--force-with-lease=<ref>:` form or a proven equivalent, then read back
the exact provider OID. Never advance a competing branch implicitly.

Any mismatch, base movement, unauthorized path, native overlap, provider
conflict, unavailable fact, or unknown provider effect stops publication and
preserves the authored commit. Never recapture, substitute, or redirect an
assessment to a later head. Never merge; no Worker may write a release,
deployment, protected path, or unapproved follow-up issue.

## Supervision and review

After each supervised completion or Worker response, reread the current branch
and full head, diff, checks, PR, and relevant authority. If they show one
specific actionable gap, give that same Worker a focused instruction. If not,
stop direction and explain why. Do not infer success from a missing or unknown
provider fact. The host handles waiting, recovery, and process progress; Repo
Gardener records only the current facts needed to report truthfully.

After PR creation, report current checks and review as ready, blocked, or
pending. If the run must close while they are pending, close partial and retain
the Worker; never call it complete. For an actionable review finding, first
re-read local head, hosted PR head, and Worker authority. Forward it only when
they still match the assessed exact head. The Worker holds its PR update,
reruns assigned verification, and returns a repaired exact head for the same
validation. Safety, authority, protected-path, exact-head, or unknown-provider
facts stop only the affected action.

Use `checking-merge-readiness` only in report-only form when a whole-change
review helps. Its result informs the Worker and owner; it never merges or
replaces the owner's later gate.

## Close

Immediately before closing, detect whether the durable-file revision changed.
When the tracker is still authorized, write and exactly read back one
`run-closed` record with every lane, depth decision, measurement result or gap,
Worker PR facts or no-Worker reason, owner attention, recommendations, policy
revision, and blocker scope. Otherwise report the interrupted close. Keep the
Orchestrator workspace and any pending Worker worktree available for owner
inspection.
