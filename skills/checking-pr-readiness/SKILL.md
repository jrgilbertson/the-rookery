---
name: checking-pr-readiness
description: Use when branch work looks complete and the next step is opening a pull request, or when asked whether the branch is ready to ship, ready for review, ready for CI, or ready for a PR — including phrasings like present your work, final approval on this branch, run the pre-PR checklist, or gate this change before it goes out. Gathers the full working surface, upstream-step receipts, plan-versus-delivered, targeted sweep, and learning signal, then briefs the owner with a Minto pyramid decision readout (recommended action first) and ends in one owner decision plus an evidence pack for the pull request body. Do not use for resolving feedback on a pull request that already exists, for the pre-merge global pass on a reviewed PR (use checking-merge-readiness for birth-to-tip design health, redesign pressure, and host merge rules), for performing a code review or simplification pass, for reviewing a plan or other document, for opening or creating the pull request itself, or for merging.
license: MIT
compatibility: Requires a git worktree and read access to the host repository. Companion checks degrade to named skips when their skills or tooling are absent.
---
# Checking PR Readiness

Check whether a branch is ready to enter the pull request and
continuous-integration process, then take one owner decision. Internally the
gate still gathers the full working surface, upstream-step receipts,
plan-versus-delivered, targeted sweep, and learning signal. The spoken readout
uses Barbara Minto's **pyramid** for an executive at the ship gate. Pyramid is
logic order in natural prose, not labeled blocks or analysis-bucket headers.
A branch is ready when every check below carries a status word, every finding
has a disposition, and the owner has approved that readout.

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
and executable — it also carries step 6's size check, so pass the cap values
step 6 resolves here and read both results from one run, statuses per step 6's
verdict-and-status mapping. Never pass `--defer` on this run, even when step 6
defers the size class to a repository gate: a deferred run measures nothing,
and this step's surface report must always be produced. Otherwise gather the same four categories directly
with git:

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
solutions documents present in the working surface. A receipt counts only when
it identifies this branch's change; a document that covers unrelated work is
not a receipt for it.
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
automated-reviewer file caps, invoked with one cap per reviewer configured on
the host repository, each value resolved per the reference's class 11:
`scripts/surface-report.sh --cap <reviewer>=<n>`,
- [scripts/evidence-freshness.sh](scripts/evidence-freshness.sh) for records
predating the final edit they describe
(`scripts/evidence-freshness.sh <record> <described-path>...`), and for
plan-named artifacts that no longer match what shipped
(`scripts/evidence-freshness.sh --check-name <name> <search-root>`),
- [scripts/changelog-union.sh](scripts/changelog-union.sh) for whether the
branch's own work appears in the repository's changelog.

`changelog-union.sh` and `evidence-freshness.sh` defer when the host
repository owns an equivalent check: invoke them as `<helper> --defer
<gate-name>` with the gate step 2 found, and report that class as covered by
that gate rather than running both. `surface-report.sh` is the exception,
because step 1's run of it must always produce the surface report: never pass
it `--defer`. When a repository gate owns the size check, pass no `--cap` for
the reviewers that gate covers and report class 11 as covered by that gate
directly from step 2's discovery. Every remaining class
runs by model instruction from the reference. A file-cap finding names the
affected reviewer and the source of the cap, or says the cap is unverified when
the source cannot be confirmed.

A helper's verdict and the gate's status words are two layers: the verdict says
what the class found, the status word says whether the check happened. Read both
off the helper's exit code and its `verdict:` line. On exit 0 the class carries
that verdict from its enumerated set, and the check's status word is verified
with the verdict line as the named evidence, or failed when the verdict is a
finding. On exit 2 with an absent-input verdict — `no changelog`, `no records` —
the check is unavailable. On exit 3 it is skipped, naming the repository gate the
helper deferred to. On exit 4, and on the `not run` verdict a usage error emits
with exit 2, the check is not run and its class falls back to the
model-instruction check the reference gives for that class.

Completion: every class in the reference carries one verdict from that class's
enumerated set, and each class that fired names where it fired — the file and
line for a line-scoped finding, the file alone for a file-level one, and the
repository surface for a repository-level one, such as a missing changelog
entry or an aggregate file-cap excess.

### 7. Compose the readout and take the owner decision

Complete steps 1 through 6 fully first (they are the evidence). Then speak
only what the owner needs for the ship decision.

#### Pyramid (binding shape)

Pyramid is logic order in natural prose, not labeled blocks or analysis-bucket
headers. Do not print Apex, Level 1, Level 2, Surface, Gates, Upstream, Sweep,
or Learning as headers on the page.

```text
Apex     → governing thought: one recommendation + short cause clause
           (producers named, not argued)
Level 1  → Why?: MECE arguments, most decision-relevant first;
           silence non-drivers; on clean approve, one affirmative residual
Level 2  → How know?: evidence only under arguments that need it (inline)
Then     → decision menu (protocol after the pyramid, not a pyramid layer)
```

**Apex.** One recommended owner decision plus a short cause clause that names
producers without arguing them. Typical shapes: approve and proceed to the
finishing path (all material checks clean or explicitly accepted); request
changes (named blocking gap); or stop and file follow-up (owner should not
ship this surface). Fold branch identity into that opening. Apex is at most
two short sentences. Do not open with the working-surface inventory.

**Level 1.** Reasons the apex is true. Each paragraph is one idea. Order
material gaps first: failed or not-verified upstream steps, plan-not-delivered
items, sweep findings that still need a disposition, uncaptured learning that
would require bypass, missing repository gates when discovery found none.
Silence non-drivers: do not dump every status word or every sweep class that
passed. On clean approve, Level 1 is one affirmative residual: what the branch
does in plain language, surface complete (including untracked if any),
material checks verified or attested, plan-versus-delivered clean or accepted
drift named once, learning signal present.

**Level 2.** How you know, nested only under Level 1 arguments that need it:
receipts, status words, paths, or helper verdicts in those sentences. Never a
separate Evidence section. Never a full checklist tour on approve.

**Then.** Decision menu: options aligned to the answer; actions only, no
re-arguing Level 1. Unavailable options say "not offered" or "unavailable" in
plain words, not strikethrough as the only cue.

#### Register and harness-safe prose

- Prefer plain continuous prose that stays legible when markdown is flattened
  or ignored: no em dashes; no markdown heading markers.
- Supporting detail that did not drive the decision stays out of the spoken
  readout. Offer an appendix only if the owner asks for the full status-word
  inventory.

Scale which checks appear by applicability, never by how large the diff feels.
A check is omitted from the spoken readout when the working surface holds no
path it covers (for example no user-interface files means browser testing and
design critique are not spoken). Paths touching authentication, authorization,
payments, data migrations, secrets handling, or a published API contract are
never silent when they have a finding or an incomplete check.

#### Decision menu

Present exactly one decision menu:

1. Approve and proceed to the finishing path.
2. Request changes.
3. Run a flagged missing step now — one option per gap found in steps 2 through
 6 that a present skill owns, each dispatching that skill. A gap with no
 owning skill available — a missing plan, empty gate discovery — is not a
 dispatch option; it is resolved through attestation where a step defines
 one, or filed through option 5.
4. Have the change or a concept behind it explained, through the available
 explanation capability (the `ce-explain` skill where the compound
 engineering plugin is installed). Omit this option and say it is unavailable
 when no such capability is present.
5. Stop and file follow-up work.

Options 3 and 4 are non-terminal: when one finishes, apply the opening's
recompose rule — re-read the working surface from step 1 and, when it changed,
re-run every step that read that surface — repository gates (step 2), upstream
receipts (step 3), the plan comparison (step 4), the learning signal (step 5),
and the sweep (step 6) — then present the pyramid readout and menu again.
Approval binds to the surface the owner was shown.

On approval, fill
[assets/evidence-pack-template.md](assets/evidence-pack-template.md) and compose
it into the handoff for the finishing path (not as a second bottom-up readout
before the decision): plan-versus-delivered status, checks run with their
status words and results, the explicit not-verified and attested list, sweep
findings with their dispositions, design-critique scores when present, and the
learning signal with any recorded override. Hand the pack to the finishing path
so that path renders it into the pull request body. Write nothing to the
repository tree and open no pull request.

Completion: the owner made exactly one decision from the menu against a
pyramid-shaped readout matching the current working surface, and an approval
carries the composed evidence pack for the finishing path.

## Gotchas

- Untracked paths are part of what the owner approves, because finishing tools
stage them. A readout built from tracked changes alone approves less than what
ships.
- Writing verified without a named receipt is the failure this gate exists to
prevent. When a receipt cannot be found, report not verified and offer
attestation.
- A green continuous-integration run is not evidence that the upstream steps
ran. The forensics behind this gate are all-green branches that still burned
seven to sixteen automated-review rounds.
- Dispatching a missing step from the menu is the one path in this workflow that
changes files, and the dispatched skill owns those changes. The gate itself
still writes nothing.
- Findings the owner declines still belong in the evidence pack with their
disposition. A dropped finding reappears as a review comment on the pull
request.
- The pack reaches the finishing path only through the readout, which is  
conversation, not a file. If the session breaks between approval and pull  
request creation, the readout carrying the pack has to be recomposed or  
supplied again; the pack exists durably only once the pull request body  
carries it.
- When `checking-merge-readiness` is also installed, roles stay complementary:
this gate optimizes entry to review; merge-readiness owns the pre-merge
global pass (intent drift, accretion, redesign). Neither skill requires the
other at runtime. An evidence pack in the PR body is optional enrichment for
merge-readiness, never a required input.
- A bottom-up inventory (surface, then gates, then every status word, then the
decision) fails this skill even when the checks are right. Pyramid order is
part of the contract.

