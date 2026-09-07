# Orchestrator and Worker workflow

This reference reconciles repository, provider, and Worker facts during a
managed run. It complements the policy and area contracts; Repo Gardener
creates neither a host adapter nor a second Git-state system. Orca may supply
the Run interface, but any host that satisfies
the mutation boundary in `SKILL.md` is suitable.

## Pre-open facts

Read the target repository's durable file from the refreshed default branch,
the complete tracker, repository instructions, and the native identities needed
to open safely. Validate the durable file without changing it. A missing,
invalid, or unapproved file takes the entry mode in
`policy-and-entry-modes.md`: interactive first use with an owner, or
caller-only sensing otherwise.

At opening, preserve the exact policy revision; the revision check points
in `policy-and-entry-modes.md` govern every later re-read. Continue safe
sensing and make a truthful close only when the remaining authority still
permits it.

Before another run opens, reconcile any complete tracker `run-opened` without
its matching `run-closed`. For the exact original Orchestrator and its
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
and caller or automation identity for the host liveness lookup; the host's
own dispatch records, reached through that caller identity, are how recovery
enumerates the run's Workers. A run whose Workers cannot be enumerated from
those records has unknown state and keeps later runs caller-only. This remains
host-neutral: use the existing payload and caller-owned recovery mechanisms,
never a Repo Gardener state machine or per-Worker tracker records.

Write and exactly read back `run-opened` before managed sensing. The
caller-only branch performs only the quick five-area
read-only pass. It writes no run records, executes no declared audits, and
does not claim managed closure.

## Declared audits and sensing

For each eligible area, run only its normalized `audit_commands`, in policy
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
executable, confirmed timeout with the complete audit process tree stopped, or
command-local capability refusal is area-local: report it and
continue safe work. A policy or subject change, unexpected worktree change,
uncertain termination, interruption, or unknown provider effect stops the
affected command and dependent work. Leave unexpected changes untouched. Do
not clean, restore, retry, resume, or replace a command automatically.

Complete the quick available-input pass across the five areas before first
dispatch, following `area-contracts.md` for filtered discovery, shared inputs,
remedy ownership, and qualification. Keep source counts and query coverage
separate from qualified candidates. Scouts are read-only and never own a PR.

After that pass, deepen while another investigation could change an assignment
or recommendation, including while selected Workers progress. Prefer credible
critical-flow risks, independent corroboration, and measurement defects.
Retain bounded evidence, findings, uncertainty, and the next useful action;
stop when further investigation cannot change a decision, without claiming
unread work excluded.

## Decide whether to author

Select only non-overlapping, independently deliverable, low-risk, testable
units small enough for one coherent PR. Author only when the opening policy
still proves the five gates in `policy-and-entry-modes.md`. A denial stops
that unit; an honest read-only result is successful operation.
Selection and dispatch for the run never exceed the opening policy's
`maximum_workers` cap; unrelated existing PRs do not consume that cap.
Immediately before every Worker dispatch, pass the revision check point and
read the complete overlap inventory as `worker-contract.md` defines, against
the Worker's planned paths, regardless of discovery filters or pagination
bounds. An unavailable or unknown read, or a current overlap, denies only that
dispatch and its dependents while other Workers and read-only sensing continue.

An existing PR may be a candidate unit. Apply the Adoption section in
`worker-contract.md` and populate its brief before dispatch; that section owns
initial eligibility and continuing permission for the standalone Worker.

For shared-ledger overlap, populate each affected brief and apply the Shared
ledger exception in `worker-contract.md`; that section owns the rule for both
dispatch and publication.

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

After PR creation, report current native PR, check, and review facts. If the
PR is still open and required checks or review are pending when the run
closes, close partial and retain the
Worker; never call it complete. Forward a named Worker-owned gap only when
local head, hosted PR head, and Worker authority still match the assessed
exact head. Safety, authority, protected-path, exact-head, or unknown-provider
facts stop only the affected action. Repo Gardener never merges.

## Close

Pass the revision check point, then close exactly as `SKILL.md` directs: one
`run-closed` record written and exactly read back when the tracker is still
authorized, otherwise the interrupted close.
