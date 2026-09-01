---
name: checking-pr-readiness
description: Use when branch work looks complete and needs a readiness decision before another workflow opens a pull request, or when asked to assess a specific head for PR readiness. Gathers the working surface and checks, then briefs a recommendation plus numbered live options and waits for a numbered reply. Option 1 is Approve. A request to write, open, create, or submit a pull request belongs to PR publishing. For an existing PR about to merge, use checking-merge-readiness.
license: MIT
compatibility: Requires a git worktree and read access to the host repository. Companion checks degrade to named skips when their skills or tooling are absent.
---
# Checking PR Readiness

Check whether a branch is ready to enter the pull request and
continuous-integration process. Internally the gate gathers the full working
surface, upstream-step receipts, plan-versus-delivered, pre-PR review checks,
and learning signal. Then brief a recommendation plus numbered live options
and wait for a numbered reply from whoever is talking.

The gate is read-only. Companion skills own edits, reviews, and capture; the
host repository's hooks and task runners own deterministic re-runs. This skill
verifies those from receipts or dispatches the skill that owns them. Nothing
is done without evidence in the captured gather. Incomplete gather cannot
offer Approve.

## Status words

Every check reports with one word from this closed set, used consistently and
without synonyms:

- **verified** — a named receipt supports the claim in the captured gather.
- **attested** — the owner states missing intent (step 4) and no durable
  source exists; recorded as attestation, not as evidence. Do not use this
  word to vouch that a missing review or simplify step happened.
- **not verified** — no receipt exists and no attestation was given.

Also in the set (same one-token rule): **failed**, **not run**, **skipped**,
**unavailable**, **bypassed**, **not applicable**. Use the ordinary meaning of
each word; **bypassed** always records the owner's reason.

## Workflow

Bind identity first. Read
[references/identity-and-argv.md](references/identity-and-argv.md) when capturing
the native subject, full head, target/base ref, and full base OID, when
proving helper `--base` binding, when rerunning a repository-authored check,
and immediately before accepting option 1.

### 1. Gather the working surface

The finishing path will stage this surface. Create an owner-only `mktemp -d`
directory outside the target repository first; capture helper stdout there and
do not echo the inventory into chat. Do not remove that directory while the
run is waiting for a numbered reply. Run
[scripts/surface-report.sh](scripts/surface-report.sh) when it is present and
executable. It also carries step 6's size check, so pass the cap values
resolved per [references/sweep-classes.md](references/sweep-classes.md) class
11 for every configured automated reviewer and read both results from one run,
statuses per the reference's helper exit map. Pass `--full` so the listing
written to temp is not capped. Resolve caps per class 11; one surface-report
run.

When discovery proves no automated reviewer is configured, run without
`--cap` for inventory and record class 11 as `not applicable`. Always produce
the surface report on this run (omit `--defer` even when step 6 later treats
size as covered by a repository gate).

Otherwise gather the same four categories directly with git: committed on this
branch against the merge base with the default branch the pull request will
target (resolve it from the remote's HEAD, and ask when the target is
ambiguous), plus staged, unstaged, and untracked paths.

List untracked paths with the same weight as tracked ones. Finishing tools
stage them, so they ship with the change even though no diff command shows
them by default. If the working tree is not a git repository, or git is
unavailable, stop rather than composing a brief from a surface you could
not read.

Completion: every path in all four categories is in the captured surface
report, or the run stopped because the working surface could not be read from
git.

Then apply the repository's transient-artifact policy. Resolve its path
families from repository instructions and ignore rules. Enumerate the final
tracked contents of those families with `git ls-files --cached`, and enumerate
their ignored working contents with
`git ls-files --others --ignored --exclude-standard`. Pass the same
content-scoped pathspecs after `--` to both commands, such as
`:(top)docs/plans/**`; do not enumerate unrelated ignored trees. Use
`git check-ignore -v` to identify the owning ignore rule for ignored files.
Search durable files for citations to every named transient family, including
families with no current file.

- An ignored file with no index entry or branch addition is working material.
  It does not ship and is allowed.
- A transient file present in the final tracked tree, staged as content, or
  added on the branch is a blocking finding. Remove it before approval; an
  owner disposition that accepts the file does not clear readiness. A branch
  deletion that removes old transient content is cleanup, not a finding.
- A durable file that cites or depends on ignored working material is a
  finding until the dependency is removed or the durable conclusion is moved
  to its canonical home.

Completion: the tracked and ignored enumerations cover every resolved family;
every transient hit is classified as ignored working material, cleanup, or a
finding; and every durable citation is accounted for. If either enumeration is
incomplete, stop rather than treating an incomplete inventory as clean.

### 2. Gather repository gates

Discover the host repository's own deterministic gates before any
model-judgment check. Read the repository's agent-instruction and contribution
documents and its conventional hook and task-runner configuration (git hook
and hook-manager files, task-runner and package manifests, and
continuous-integration workflow definitions), and take the gates they name.
List the conventional paths first and read only the sections that define
gates. Search for hook, script, and job names before any full-file read
rather than pulling whole workflow files into the conversation.

Record each discovered gate with a status word and with what owns it, off
chat. Record hook coverage and whether it has run on the current surface;
leave re-running to the hook. When discovery finds no repository-owned gates,
record that emptiness as unavailable. Silence is not a pass.

Completion: every discovered gate carries one status word and its owner, and
an empty discovery is a named finding in the gather.

### 3. Verify upstream steps from receipts

Record each expected upstream step with a status word in the gather: code
review, code simplification, browser testing, design critique or audit, and
learnings capture. Browser testing and design critique apply only to diffs
that touch user-interface files; record how that classification was decided
from the paths in the working surface, and surface an uncertain classification
rather than resolving it silently.

Use this receipt inventory to decide between verified and the honest
alternatives:

- Durable receipts: design-critique snapshots (for example
  `.impeccable/critique/` frontmatter carrying a score and P0/P1 counts) and
  solutions documents present in the working surface. A receipt counts only
  when it identifies this branch's change; a document that covers unrelated
  work is not a receipt for it.
- Browser testing leaves a receipt only when its output or screenshots were
  saved; otherwise it has none.
- Code review and code simplification leave no durable artifact today, so
  outside the session that ran them they are not verified.

Write verified only with the receipt named in the gather. Where no receipt
exists, record not verified. Do not ask anyone to vouch that it happened.
When the companion skill or tooling a check depends on is absent (no compound
engineering plugin, no design-critique tooling), record that check skipped,
name what was missing, and run the rest of the checks.

Completion: each of the five steps carries one status word in the captured
gather, every verified step names its receipt, and the user-interface
classification and its basis are stated.

### 4. Compare intent to what was delivered

Use the linked issue or ticket first, then the brief the work started from. A
repository plan is optional and counts only when that repository maintains
plans as durable documentation. An ignored working plan may help the current
comparison, but it is not a durable source and must not appear in
pull-request evidence. Compare the source against the working surface in the
gather. Intended items not delivered and work delivered beyond the source are
intent drift.

A linked issue or brief is sufficient; the absence of a separate plan is not
a finding. When no issue, brief, or durable repository plan exists, record
the comparison unavailable, name that absence as a finding, and take a direct
attestation of what the branch was meant to do, recorded as attested.

Completion: every planned item is marked delivered or not delivered in the
gather, or the comparison is recorded unavailable with intent attestation.

### 5. Check the learning signal

Carry exactly one durable-learning signal in the gather:

- a solutions document covering this branch's work exists in the working
  surface; or
- an explicit capture plan or follow-up exists; or
- a recorded reason this branch produced no durable learning.

Capture is the recommended path. Approving past an uncaptured and unplanned learning requires
an explicit override, reported as bypassed and recorded with the stated
reason in the evidence pack.

Completion: the gather carries exactly one of the three signals, and any
approval past an uncaptured learning carries the recorded reason.

### 6. Run the Pre-PR Review Checks

Read [references/sweep-classes.md](references/sweep-classes.md) and work every
class in the order listed there. Record verdicts in the captured gather in
that order.

Mechanical classes run through the bundled helpers:

- [scripts/surface-report.sh](scripts/surface-report.sh) for diff size (class
  11): reuse step 1's run. Caps and the no-reviewer case live in class 11.
- [scripts/evidence-freshness.sh](scripts/evidence-freshness.sh) for stale
  records and plan-named artifacts (classes 4 and 2 support).
- [scripts/changelog-union.sh](scripts/changelog-union.sh) for branch
  changelog entry (class 3).

`changelog-union.sh` and `evidence-freshness.sh` defer when the host
repository owns an equivalent check: invoke them as `<helper> --defer
<gate-name>` with the gate step 2 found, and record that class as covered by
that gate. When a repository gate owns the size check, pass no `--cap` for
the reviewers that gate covers and record class 11 as covered by that gate.
When step 1 already resolved the target branch or merge base, pass it through
to `surface-report.sh` and `changelog-union.sh` (`--base <ref>` or
`--merge-base <sha>`). `evidence-freshness.sh` resolves no base and accepts
neither flag.

Every remaining class runs by model instruction from the reference, in one
pass: read the branch diff once and apply every judgment class to that single
reading rather than re-reading the diff per class.

Map helper exit codes and `verdict:` lines to status words using the table in
[references/sweep-classes.md](references/sweep-classes.md).

Completion: every class in the reference carries one verdict from that
class's enumerated set in the captured gather, and each class that fired
names where it fired: the file and line for a line-scoped finding, the file
alone for a file-level one, and the repository surface for a repository-level
one.

### 7. Brief, then wait for a numbered reply

Complete steps 1 through 6 fully first. Then brief in continuous prose:
recommendation first, then only the reasons that make it true, then evidence
under those reasons. Numbered live options follow the brief.

<!-- Maintainers: this readout shape is mirrored in
checking-merge-readiness/SKILL.md step 6. Skills stay self-contained, so edit
both copies together. -->

- One recommendation (approve and proceed; request changes; or stop and file
  follow-up). Open on the decision, not the working-surface inventory.
- Reasons, one idea each, most decision-relevant first. Reasons are about
  the change under review, not how this gate runs. A clean outcome is
  one residual clause that grading found nothing material.
- Evidence sits only under the reasons that drove the call, with source
  pointers. The check inventory is Show the checks, not the default brief.
- Numbered live options after the brief. Only option 1 is reserved. Print
  Approve and proceed when that action can be taken; otherwise keep number
  1 and name why. The remaining actions have a print order, not menu
  numbers. Print only the live ones, numbered from 2 without gaps.
- Clean green (approve and proceed, nothing material): final brief plus
  menu at most about 12 non-blank short lines.
- A coverage close: gather completed, and every applicable check is
  verified, not applicable, or recorded without a receipt. Incomplete gather cannot
  offer Approve.
- Name a check in the brief only when it drives the recommendation.
  Spoken next work is owner work that still remains after this decision.
  When the recommendation is approve, that remaining path is opening the
  pull request and babysitting it. When the recommendation is approve, unrun code review or simplify do not appear in that brief as leftover work.
  Untracked or blocking paths appear when they drive the call. Paths
  touching authentication, authorization, payments, data migrations,
  secrets handling, or a published API contract stay visible when they
  have a finding or an incomplete check.

#### Decision menu

Present exactly one decision menu, then wait for a numbered reply. Do not pick an option in the same turn that wrote the menu. A turn is one reply. Print only the brief and the numbered options, then stop. Do not explain turns, later `1`, or the identity re-read in the brief. The next message in the conversation, from whoever is talking, is the pick. A reply of `1`,
"Approve", or "approve and proceed" after the menu has offered option 1
counts as that choice. The activating utterance never authorizes Approve.

Print order, not menu numbers. Number 1 is always Approve and proceed.
Number the remaining live actions from 2 without gaps.

- Approve and proceed to the finishing path. Offer only when gather is
  complete and the recommendation is approve and proceed. A check named as next work does not by itself withhold Approve.
- Request changes. Offer on every menu, including an approve
  recommendation. This is the numbered alternative to Approve, not a
  fixed slot. The spoken line matches the brief. On request changes it
  names the remaining work. On approve it declines Approve rather than
  inventing leftover changes.
- Run a missing step now. One menu line. Offer when the recommendation is
  request changes and a present skill owns a gap. After it is picked,
  dispatch that skill.
- Explain the change, when `ce-explain` is present.
- Show the checks. Offer when a captured gather exists. List each
  applicable check and its status word from that gather: repository gates,
  upstream steps, sweep classes that applied, and the learning signal.
  Then present the brief and numbered options again. The spoken line names
  the checks this PR-readiness review ran.
- Stop and file follow-up work. Offer when the recommendation is stop and
  file follow-up, or the brief named leftover work to file. This ends the
  finishing path and parks that leftover in the tracker instead of opening
  a pull request. Skip it when there is nothing to file.

Print option 1 on every menu. When Approve cannot be taken, keep number 1
and name why in a natural sentence; that withheld row does not print the
Approve action. Do not reuse option 1 for another action. Number the
remaining live actions from 2 without gaps, in the print order above.
Write each option as a sentence, not a label then a colon. Example when
Approve is blocked, Request changes is live, and a missing step, Explain,
and leftover work to file are not:

```text
1. This branch is not ready to enter the pull request process.
2. Request the remaining changes on this branch.
3. Show the checks this PR-readiness review ran.
```

Example when Approve is live and Request changes is the alternative:

```text
1. Approve and proceed to the finishing path.
2. Decline Approve and request changes on this branch.
3. Show the checks this PR-readiness review ran.
```

Show the checks is non-terminal: print the list from the captured gather, then the brief and numbered options again. Run a missing step and Explain are non-terminal: when one finishes, **recompose**. Re-read the working surface from step 1 and, when it changed, re-run the steps whose inputs the change touches.

Completion of this turn: the brief and numbered live options are on screen,
and the run is waiting. It did not pick. It did not re-read identity for
Approve and did not fill an evidence pack.

### On a later reply of 1

Before accepting Approve, re-read HEAD, the merge-base, and staged, unstaged,
and untracked content per
[references/identity-and-argv.md](references/identity-and-argv.md). If any of
those moved, name what moved, rebuild, and do not hand a pack as if the old
surface were still current. A matching re-read is silent.

On approval, fill
[assets/evidence-pack-template.md](assets/evidence-pack-template.md) and
compose it into the handoff for the finishing path: the recommendation,
material next work, a coverage close, and the learning signal with any
recorded override. Hand the pack to the finishing path so that path renders
it into the pull request body. Write nothing to the repository tree and open
no pull request.

Sanitize the pack for durable use. Summarize intent from the selected durable
intent source: a linked issue or ticket, a brief, or a maintained repository
plan. When step 4 found no durable source, summarize the recorded intent
attestation instead. Do not copy ignored-plan paths or contents, local-only
paths, credentials, or unnecessary personal data.

Completion: a matching silent re-read, then the pack in the finishing-path
handoff, or a named rebuild with no pack. The run wrote nothing to the
repository. Remove the step 1 temp directory after this later turn, when a
non-1 later turn ends the run, or on failure.

## Gotchas

- Untracked paths ship with finishing tools; include them in what option 1
  approves.
- Green CI is not evidence that upstream steps ran.
- Dispatching a missing step from the menu is the one path that changes
  files, and the dispatched skill owns those changes. The gate itself still
  writes nothing.
- The pack reaches the finishing path only through conversation. If the
  session breaks before PR creation, recompose or supply the pack again.
- When `checking-merge-readiness` is also installed, this gate owns entry to
  review; merge-readiness owns the pre-merge whole-change review. Neither
  requires the other at runtime.
