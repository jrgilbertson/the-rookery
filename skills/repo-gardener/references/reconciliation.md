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

Before another run opens, reconcile any complete tracker `run-opened` without
its matching `run-closed`. For the exact original Orchestrator and its
Workers, require current caller or host liveness, or proven termination; an
expired lease alone proves neither termination nor loss of mutation ability.
Unknown, unavailable, or still-live state blocks a new opening and new
Workers. Recovery may only verify or finish the original uncertain tracker
effect and prepare one truthful close from retained verifiable facts, recording
unknown dispositions. It never resumes or replays stale declared audits or
Worker mutation, and it preserves pending worktrees and authored state for
inspection. Every later run starts fresh with its own run ID and opening
sequence. This liveness gate is additional to, not a replacement for or
authorization from, applying-effects exclusive-writer or atomic-serialization
requirements.

Each `run-opened` payload persists bounded, stable original Orchestrator identity
and caller or automation identity for the host liveness lookup. This remains
host-neutral: use the existing payload and caller-owned recovery mechanisms,
never a Repo Gardener state machine or per-Worker tracker records.

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
gate as pass, failure, or unavailable. Every unattended Worker invokes
`checking-pr-readiness` normally and stops after its brief and numbered menu.
The activating utterance is never approval. Only on a distinct later turn may
that same Worker choose option 1, and only if the menu offered option 1 and the
recommendation was approve and proceed. The checking skill performs its
identity reread before handing its evidence pack to the publication path.

For ownerless publication, all other outcomes fail closed: absent option 1,
non-approving recommendation, incomplete gather, unavailable checking skill,
moved identity, or a later-session claim must preserve the authored commit
without push or PR creation and name the blocking gap. With an owner, normal
publication remains subject to the owner's interactive authorization. After the
later approval, keep the exact head/base, assigned-path, cleanliness, policy,
overlap, provider-read, lease, and one-unmerged-PR gates below; the checking
skill does not replace them.
Immediately before every push and every PR opening, refresh the durable policy
file from the authoritative default branch and require its revision to match
the opening revision. A mismatch, unavailable or unknown refresh/read stops
that publication action and preserves the authored work.
Immediately before every ownerless publication push, including a repaired-head
update, compare the local subject and OID to the subject and OID the checking
skill re-read; for an Orchestrator-authorized repair, compare the current local
subject and full head OID to its exact authorized repaired subject and OID.
Never replace or recapture that authorized identity. Immediately before an
ownerless first push, re-resolve the captured target/base ref and full base OID.
The same target/base reread is required immediately before every repaired-head
update. Reread `git status --porcelain=v1 --untracked-files=all` immediately
before every such push; a failed read or any staged, unstaged, or untracked
non-ignored path stops publication. Immediately before PR-open, re-resolve the
captured target/base ref and full base OID and reread that porcelain status.
Before every push and PR opening,
validate the committed paths against the assignment, identity, scope, protected
paths, and, where relevant, the ledger base diff, then reconcile the current
local head, exact target/base, and native branch and PR overlap. Permit a ledger
overlap only under the same-assignment binding above.

After those gates pass, provider state is exhaustive: an absent provider ref
may be atomically created at the exact authorized head only under an absent-ref
lease, such as Git's `--force-with-lease=<ref>:` form or a proven equivalent;
a provider ref already equal to that head needs no push; and only an
Orchestrator-authorized repair of the same Worker's PR may atomically update its
exact previously observed hosted head to the exact authorized repaired head,
under a lease expecting that old OID. Refuse unavailable or unknown provider
state, any other provider OID, or a lease failure. After a create or update,
read back and require the exact authorized provider OID. Never advance
competing movement implicitly.

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

After PR creation, report current native check and review facts. If required
checks or review are pending when the run closes, close partial and retain the
Worker; never call it complete. For an actionable review finding, first
re-read local head, hosted PR head, and Worker authority. Forward it only when
they still match the assessed exact head. The Worker holds its PR update,
reruns assigned verification, and returns a repaired exact head for the same
validation. Safety, authority, protected-path, exact-head, or unknown-provider
facts stop only the affected action.

The scheduled ownerless run never invokes `checking-merge-readiness`. It leaves
that normal menu and its later owner decision to an owner interaction; Repo
Gardener never merges.

## Close

Immediately before closing, detect whether the durable-file revision changed.
When the tracker is still authorized, write and exactly read back one
`run-closed` record with every lane, depth decision, measurement result or gap,
Worker PR facts or no-Worker reason, owner attention, recommendations, policy
revision, and blocker scope. Otherwise report the interrupted close. Keep the
Orchestrator workspace and any pending Worker worktree available for owner
inspection.
