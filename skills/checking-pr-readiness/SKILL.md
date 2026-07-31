---
name: checking-pr-readiness
description: Use when branch work looks complete and the next step is opening a pull request, or when asked whether the branch is ready to ship, ready for review, ready for CI, or ready for a PR — including phrasings like present your work, final approval on this branch, run the pre-PR checklist, or gate this change before it goes out. Reports the full working surface, confirms the planned work was delivered, verifies that code review, simplification, UI checks, and learnings capture actually ran, sweeps the branch for the finding classes that drive repeated review rounds, and ends in one owner decision plus an evidence pack for the pull request body. Do not use for resolving feedback on a pull request that already exists, for performing a code review or simplification pass, for reviewing a plan or other document, for opening or creating the pull request itself, or for merging.
license: MIT
compatibility: Requires a git worktree and read access to the host repository. Companion checks degrade to named skips when their skills or tooling are absent.
---

# Checking PR Readiness

Check whether a branch is ready to enter the pull request and
continuous-integration process, then take one owner decision. The gate reports
the full working surface, verifies that the shipping workflow's upstream steps
actually ran, compares what was planned against what was delivered, sweeps the
branch for the finding classes that drive repeated automated-review rounds, and
confirms a durable learning was captured or explicitly planned. "Ready" means
exactly one thing here: every check below carries a status word, every finding
has a disposition, and the owner approved that readout.

The gate reads. It never edits, stages, commits, pushes, or opens a pull
request, and it never re-runs a deterministic check the host repository's own
hooks or task runners already own. It reimplements no companion either: code
review, code simplification, browser testing, design critique, and learnings
capture are verified from receipts or dispatched to the skill that owns them.

Every run ends in exactly one explicit owner decision, taken against a readout
that matches the working surface at that moment; if the surface moves while a
menu option runs, the readout is recomposed before the decision is taken.
Nothing is reported as done without evidence named inline. Every check reports
with one word from this list, used consistently and without synonyms:

- **verified** — a named receipt supports the claim, and the readout names it.
- **attested** — the owner states it happened and no receipt exists; recorded
  as attestation, never as evidence.
- **failed** — the check ran and did not pass.
- **not run** — the check did not execute, because a helper, tool, or context
  it needs was unavailable.
- **not verified** — no receipt exists and no attestation was given.
- **skipped** — deliberately not run because a companion is absent or the class
  has no target in the working surface.
- **unavailable** — the input the check reads does not exist, such as a missing
  plan or changelog.
- **bypassed** — a check that fired was overridden by the owner, recorded with
  the reason.
- **not applicable** — the working surface contains nothing this check covers.

## Workflow

### 1. Report the working surface

Report the branch's full working surface before any other check, because that
surface is what the finishing path will stage and what the owner is approving.
Run [scripts/surface-report.sh](scripts/surface-report.sh) when it is present
and executable; otherwise gather the same four categories directly with git:

- committed on this branch, compared against the merge base with the default
  branch the pull request will target (resolve it from the remote's HEAD, and
  ask the owner when the target is ambiguous),
- staged, unstaged, and untracked paths.

List untracked paths with the same weight as tracked ones. Finishing tools stage
them, so they ship with the change even though no diff command shows them by
default. If the working tree is not a git repository, or git is unavailable,
stop and say so rather than composing a readout from a surface you could not
read.

Completion: every path in all four categories appears in the readout, or the
run stopped because the working surface could not be read from git.

### 2. Report repository gates

Discover the host repository's own deterministic gates and report each one
before any model-judgment check runs. Read the repository's agent-instruction
and contribution documents and its conventional hook and task-runner
configuration — git hook configuration and hook-manager files, task-runner and
package manifests, and continuous-integration workflow definitions — and take
the gates they name.

Report each discovered gate with a status word and with what owns it. Never
re-run a check a repository hook already owns: report the hook's coverage and
whether it has run on the current surface, and leave the running to the hook.
When discovery finds no repository-owned gates, that emptiness is itself a
reported finding — report it as unavailable and say the branch has no
repository-owned deterministic coverage, rather than letting silence read as a
pass.

Completion: every discovered gate carries one status word and its owner, and an
empty discovery is reported as a named finding.

### 3. Verify upstream steps from receipts

Report each expected upstream step with a status word: code review, code
simplification, browser testing, design critique or audit, and learnings
capture. Browser testing and design critique apply only to diffs that touch
user-interface files; record how that classification was decided from the paths
in the working surface, and surface an uncertain classification for the owner to
decide rather than resolving it silently.

Use this receipt inventory to decide between verified and the honest
alternatives:

- Durable receipts: design-critique snapshots (for example
  `.impeccable/critique/` frontmatter carrying a score and P0/P1 counts) and
  solutions documents present in the working surface.
- Browser testing leaves a receipt only when its output or screenshots were
  saved; otherwise it has none.
- Code review and code simplification leave no durable artifact today, so
  outside the session that ran them they are attestation-only.

Never write verified without naming the evidence in the same line. Where no
receipt exists, report not verified and offer the owner the chance to attest;
record an attestation as attested, not as evidence. When the companion skill or
tooling a check depends on is absent — no compound engineering plugin, no
design-critique tooling — report that check skipped, name what was missing, and
run the rest of the checklist.

Completion: each of the five steps carries one status word, every verified step
names its receipt, and the user-interface classification and its basis are
stated.

### 4. Compare the plan to what was delivered

Find the branch's source plan or brief — a plan document in the working surface,
a linked issue or ticket, or the brief the work started from — and compare it
against what the surface actually contains. List planned-but-not-delivered items
first: that is the primary finding class this comparison exists to catch. Note
work delivered beyond the plan second, as intent drift for the owner to judge,
not as a violation; plans legitimately adjust during execution.

When no source plan or brief exists, report the comparison unavailable, name
that absence itself as a finding, and take the owner's direct attestation of
what the branch was meant to do, recorded as attested.

Completion: every planned item is marked delivered or not delivered, or the
comparison is reported unavailable with the owner's attestation of intent
recorded.

### 5. Check the learning signal

Carry exactly one durable-learning signal into the readout:

- a solutions document covering this branch's work exists in the working
  surface, named in the readout; or
- an explicit capture plan or follow-up exists, named in the readout; or
- the readout states why this branch produced no durable learning.

Capture is the recommended path, and the decision menu offers running the
capture step now. Approving past an uncaptured and unplanned learning requires
an explicit owner override, reported as bypassed and recorded with the owner's
stated reason in the evidence pack.

Completion: the readout carries exactly one of the three signals, and any
approval past an uncaptured learning carries the owner's recorded reason.

### 6. Run the targeted sweep

Read [references/sweep-classes.md](references/sweep-classes.md) and work its
classes in the order listed there — observed frequency order from the pull
request forensics behind this gate — then surface findings in that same order.

Mechanical classes run through the bundled helpers:

- [scripts/surface-report.sh](scripts/surface-report.sh) for diff size against
  automated-reviewer file caps,
- [scripts/evidence-freshness.sh](scripts/evidence-freshness.sh) for records
  predating the final edit they describe, and for plan-named artifacts that no
  longer match what shipped,
- [scripts/changelog-union.sh](scripts/changelog-union.sh) for whether the
  branch's own work appears in the repository's changelog.

Each helper defers when the host repository owns an equivalent check: report
that class as covered by the repository gate rather than running both. When a
helper cannot run, report its class not run and cover it with the
model-instruction fallback the reference gives for that class. Every remaining
class runs by model instruction from the reference. A file-cap finding names the
affected reviewer and the source of the cap, or says the cap is unverified when
the source cannot be confirmed.

Completion: every class in the reference carries a status word, and each class
that fired names the file and line where it fired.

### 7. Compose the readout and take the owner decision

Compose an executive readout that fits on one screen: what changed in plain
language, the working surface, repository gates and upstream steps with their
status words, plan-versus-delivered, sweep findings in the reference's order,
the learning signal, and the risks that remain. Supporting detail stays out of
the readout and is rendered as an appendix only if the owner asks for it.

Scale the readout to the change surface by applicability, never by how large the
diff feels. A check is collapsed to one line or reported not applicable or
skipped only when the working surface holds no path it covers — no
user-interface files means browser testing and design critique are not
applicable. Name every collapsed check with its status word; none is dropped
silently. Paths touching authentication, authorization, payments, data
migrations, secrets handling, or a published API contract are never collapsed.

Then present exactly one decision menu:

1. Approve and proceed to the finishing path.
2. Request changes.
3. Run a flagged missing step now — one option per gap found in steps 2 through
   6, each dispatching the skill that owns that step.
4. Have the change or a concept behind it explained, through the available
   explanation capability (the `ce-explain` skill where the compound
   engineering plugin is installed). Omit this option and say it is unavailable
   when no such capability is present.
5. Stop and file follow-up work.

Options 3 and 4 are non-terminal: when one finishes, re-read the working surface
from step 1, re-run step 6 if that surface changed, recompose the readout, and
present the menu again. Approval binds to the surface the owner was shown.

On approval, fill
[assets/evidence-pack-template.md](assets/evidence-pack-template.md) and compose
it into the readout: plan-versus-delivered status, checks run with their status
words and results, the explicit not-verified and attested list, sweep findings
with their dispositions, design-critique scores when present, and the learning
signal with any recorded override. Hand the pack to the finishing path inside
the readout so that path renders it into the pull request body. Write nothing to
the repository tree and open no pull request.

Completion: the owner made exactly one decision from the menu against a readout
matching the current working surface, and an approval carries the composed
evidence pack in that readout.

## Gotchas

- Untracked paths are part of what the owner approves, because finishing tools
  stage them. A readout built from tracked changes alone approves less than what
  ships.
- Writing verified without a named receipt is the exact failure this gate
  exists to prevent. When a receipt cannot be found, report not verified and
  offer attestation.
- A green continuous-integration run is not evidence that the upstream steps
  ran. The forensics behind this gate are all-green branches that still burned
  seven to sixteen automated-review rounds.
- Dispatching a missing step from the menu is the one path in this workflow that
  changes files, and the dispatched skill owns those changes. The gate itself
  still writes nothing.
- Findings the owner declines still belong in the evidence pack with their
  disposition. A dropped finding reappears as a review comment on the pull
  request.

## Credits

This gate succeeds a private `pre-pr-approval` skill, whose
readout-then-one-decision shape and no-mutation posture carry forward here. Its
checklist order, learnings-capture step, and preference for named receipts over
assertions come from the compound engineering ecosystem and its published
shipping loop.
