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

At opening, preserve the exact policy revision; the revision check points
in `policy-and-entry-modes.md` govern every later re-read. Continue safe
sensing and make a truthful close only when the remaining authority still
permits it.

Before another run opens, reconcile any complete tracker `run-opened` without
its matching `run-closed`, including a legacy record under the pre-version
markers named in `tracker-records.md`. For the exact original Orchestrator and its
Workers, require current caller or host liveness, or proven termination; an
expired lease alone proves neither termination nor loss of mutation ability.
Unknown, unavailable, or still-live state blocks a new opening and new
Workers; the run still performs caller-only sensing and returns that result to
the caller with the stale `run-opened` as owner attention item 1. Recovery may
only verify or finish the original uncertain tracker
effect and prepare one truthful close from retained verifiable facts, recording
unknown dispositions. It never resumes or replays stale declared audits or
Worker mutation, and it preserves pending worktrees and authored state for
inspection. Every later run starts fresh with its own run ID and opening
sequence. This liveness gate is additional to the caller's single-writer
declaration in `tracker-records.md`, never a substitute for it.

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
still proves the five gates in `policy-and-entry-modes.md`. A denial stops
that unit; an honest read-only result is successful operation.
Selection and dispatch for the run never exceed the opening policy's
`maximum_workers` cap; unrelated existing PRs do not consume that cap.
Immediately before every Worker dispatch, pass the revision check point and
read overlap as `policy-and-entry-modes.md` defines.

A candidate unit may be an existing open PR that the Worker adopts. Adopt only
when: the head branch lives in the target repository (on GitHub,
`isCrossRepository: false`); the native read gives head ref, full head OID,
base ref, and changed paths; the PR is not a draft and every commit on its head
beyond the base is authored by a provider-marked bot or app account; and
current native facts (a failing check, a missing changelog entry, pin-mirror
drift, a review finding) name a gap the Worker can close inside scope and
outside protected paths. A PR failing any condition is a recommendation, never
adopted. The captured head ref must belong to that PR alone: if any other
open PR uses the same head ref, deny the unit regardless of changed paths.
Adoption consumes one Worker of `maximum_workers`; no two Workers adopt the
same PR. After the first Worker push an update bot treats the branch
as edited and stops rebasing or updating it, so adopt only when the named gap
is worth that trade (a failing repository gate, not a stale version). Author,
title, and branch prefix prove nothing about the PR's content; the provider's
account type and draft flag bound only who the gardener may push to. The PR
number, head ref, head OID, and changed paths are the identity.

A shared ledger path is the one overlap exception, keyed on
`git check-attr --source=<full base OID> merge -- <path>` reporting `union`,
read by the Orchestrator at assignment and carried to the Worker in its brief.
The `--source` form reads the attribute at the base revision regardless of the
worktree's checkout; a git without it is an unavailable read that denies the
exception. The attribute proves git-local union merge only: hosts that merge
PRs server-side ignore merge drivers, so when two Workers share the path the
second PR to merge may conflict on the host, and that conflict is owner work
named in the brief and morning report. The exception covers only additive
entries: every Worker using it adds only its attributable entry and retains
all base entries; the Orchestrator never writes a ledger line. The exception
applies only between Workers selected in the same assignment decision,
identified by their approved brief identity and branch; any other native
branch or PR touching that path is ordinary overlap. It does not exempt
another path, protected path, authoring scope, or a new or unrelated overlap,
which stops publication. Later native conflicts are for human handling.

Dispatch requires the portable interface and brief in `worker-contract.md`;
that file owns everything the Worker does from setup through publication. The
Orchestrator reads each checking-skill brief and, on a distinct later turn,
authorizes reply 1 only under the boundary sentences in `SKILL.md`.

## Supervision and review

After each supervised completion or Worker response, reread the current branch
and full head, diff, checks, PR, helper brief, and relevant authority. Send
that same Worker every named Worker-owned gap those facts show. If none
remain, the remaining work needs the owner, or a further turn cannot help,
stop direction and explain why. Do not infer success from a missing or unknown
provider fact. The host handles waiting, recovery, and process progress; Repo
Gardener records only the current facts needed to report truthfully.

After PR creation, report current native check and review facts. If required
checks or review are pending when the run closes, close partial and retain the
Worker; never call it complete. Forward a named Worker-owned gap only when
local head, hosted PR head, and Worker authority still match the assessed
exact head. Safety, authority, protected-path, exact-head, or unknown-provider
facts stop only the affected action. Repo Gardener never merges.

## Close

Pass the revision check point, then close exactly as `SKILL.md` directs: one
`run-closed` record written and exactly read back when the tracker is still
authorized, otherwise the interrupted close.
