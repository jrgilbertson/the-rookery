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

- **verified** — a named receipt supports the claim in the captured gather,
  or, for solution simplicity only, a matching recorded identity on a clean
  result does.
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
executable. Pass `--full` so the listing written to temp includes every path.
The same run supplies step 6's informational size diagnostics; optional
`--cap` values and their interpretation live in
[references/sweep-classes.md](references/sweep-classes.md) class 11. Always
produce the surface report on this run (omit `--defer` even when a repository
gate owns a size check).

Otherwise gather the same four categories directly with git: committed on this
branch against the merge base with the default branch the pull request will
target (resolve it from the remote's HEAD, and ask when the target is
ambiguous), plus staged, unstaged, and untracked paths.

List untracked paths with the same weight as tracked ones. Finishing tools
stage them, so they ship with the change even though no diff command shows
them by default. If the working tree is not a git repository, or git is
unavailable, stop rather than composing a brief from a surface you could
not read. An unresolved base, unmeasurable committed category, failed git
enumeration, or omitted path leaves the gather incomplete and withholds
Approve, regardless of any size verdict.

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

Record the working-surface identity in this step's temp directory for every
gather, including when `checking-simplicity` is not dispatched, and do not
print it. [references/identity-and-argv.md](references/identity-and-argv.md)
defines that record. Approve, recompose, and the simplicity check compare it.

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
review, code simplification, solution simplicity, browser testing, design
critique or audit, and learnings capture. Solution simplicity is the
independent, approach-level result from `checking-simplicity`. It is primarily
user-requested and may also run before ungrounded durable machinery enters
implementation; its place here is a late backstop, not the recommended first
checkpoint. Before dispatching it, resolve the intent source step 4 uses and
supply the reviewer with the objective, required behavior, hard constraints,
and verification criteria. Browser testing and design critique apply only to
diffs that touch user-interface files; record how that classification was
decided from the paths in the working surface, and surface an uncertain
classification rather than resolving it silently.

Use this receipt inventory to decide between verified and the honest
alternatives:

- Durable receipts: design-critique snapshots (for example
  `.impeccable/critique/` frontmatter carrying a score and P0/P1 counts) and
  solutions documents present in the working surface. A receipt counts only
  when it identifies this branch's change; a document that covers unrelated
  work is not a receipt for it.
- Browser testing leaves a receipt only when its output or screenshots were
  saved; otherwise it has none.
- Solution simplicity is verified by this gate's own dispatch, not by a
  receipt. Compare the working-surface identity recorded at the end of step 1.
  [references/identity-and-argv.md](references/identity-and-argv.md) defines
  the record: the head OID, plus for staged, unstaged, and untracked paths
  only, each path, mode, and content digest. Store a symlink as its link text
  and never follow it. Do not hash every committed blob. The committed
  category is the head OID. A new head, including a message-only amend,
  restarts the check.
  [scripts/surface-report.sh](scripts/surface-report.sh) lists paths and does
  not emit content digests; do not treat its path lists as this identity. An
  in-place edit of an already-listed path does not change that listing, which
  is why the digest is required. Then dispatch `checking-simplicity` with the
  resolved intent source, the repository, branch, and full `HEAD`, and the
  four path categories. That skill owns the reviewer's independence and how it
  reads the subject. Compare the identity again when the result returns, so an
  in-place edit during the check is caught. When the recorded head OID and the
  staged, unstaged, and untracked path, mode, and content digest match, the
  clean result counts, including a same-context result, and file bodies are
  not re-read to prove it. The readout does not contain the digest or the
  commit hash. A mismatch restarts the check. If the result returns after an
  in-place edit of an already-listed path, that second compare restarts the
  check. The result is verified only when it recommends keeping the current
  approach, no user question remains, and the identity matches. A result that
  recommends simplifying first, or that needs a user decision, is failed until
  the subject is revised or the decision made and the dispatch repeated. A
  result that cannot assess yet is not verified. The simplicity result does
  not replace the whole-change grade.
- Code review, code simplification, and solution simplicity leave no durable
  artifact today, so outside the session that ran them they are not verified.
  Outside the session the simplicity result stays not verified, and it is
  never verified by attestation.

Write verified only with the receipt named in the gather, or for solution
simplicity when the recorded identity matches. Where neither exists, record
not verified. Do not ask anyone to vouch that it happened. When the companion
skill or tooling a check depends on is absent (no compound engineering plugin,
no `checking-simplicity`, no design-critique tooling), record that check
skipped, name what was missing, and run the rest of the checks.

Completion: each of the six steps carries one status word in the captured
gather, every verified step names its receipt or, for solution simplicity,
that the recorded identity matched, and the user-interface classification and
its basis are stated.

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
  11): reuse step 1's run. Class 11 owns optional cap diagnostics and their
  distinction from actual review coverage.
- [scripts/evidence-freshness.sh](scripts/evidence-freshness.sh) for stale
  records and plan-named artifacts (classes 4 and 2 support).
- [scripts/changelog-union.sh](scripts/changelog-union.sh) for branch
  changelog entry (class 3).

`changelog-union.sh` and `evidence-freshness.sh` defer when the host
repository owns an equivalent check: invoke them as `<helper> --defer
<gate-name>` with the gate step 2 found, and record that class as covered by
that gate. When a repository gate owns the size check, record class 11 as
covered by that gate; its actual result remains in step 2.
When step 1 already resolved the target branch or merge base, pass it through
to `surface-report.sh` and `changelog-union.sh` (`--base <ref>` or
`--merge-base <sha>`). `evidence-freshness.sh` resolves no base and accepts
neither flag.

Every remaining class runs by model instruction from the reference, in one
pass: read the branch diff once, write that reading into the step 1 `mktemp -d`
directory outside the target repository, and apply every judgment class to
that single reading rather than re-reading the diff per class. That directory
lives only until the same-session later gate has read its diff file for the
live head. Remove it when that gate has finished, or as soon as that handoff
cannot happen. The later gate reads that diff file, not the surface-report
listing. The file is the diff already read for this grade. It is not a durable
receipt. Do not put raw forge JSON into the merge skill's waiting directory.

Map helper exit codes and `verdict:` lines to status words using the table in
[references/sweep-classes.md](references/sweep-classes.md).

Completion: every class in the reference carries one verdict from that
class's enumerated set in the captured gather, and each class that fired
names where it fired: the file and line for a line-scoped finding, the file
alone for a file-level one, and the repository surface for a repository-level
one.

### 7. Present the recommendation

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
  numbers. Print only the live ones, numbered from 2 without gaps. The
  spoken answer on every wait is that wait's own prose and numbered options. This skill,
  its headings, its file path, and why the run is waiting stay out of it. Nothing follows the last option.
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

Present exactly one decision menu, then wait for a numbered reply. Do not pick an option in the same turn that wrote the menu. A turn is one reply. Print only the brief and the numbered options, then stop. The next message in the conversation, from whoever is talking, is the pick. A reply of `1`,
"Approve", or "approve and proceed" counts as that choice only after the
menu offered Approve, not after it printed a withheld option-1 row. A `1`
on a withheld row is not Approve. Name that the action cannot be taken and
wait again. Do not enter the finishing path. The activating
utterance never authorizes Approve.

Print order, not menu numbers. Number 1 is the reserved Approve-and-proceed
slot. When that action can be taken, print it. When it cannot, keep number
1 and name why. Number the remaining live actions from 2 without gaps.

- Approve and proceed to the finishing path. Offer only when gather is
  complete and the recommendation is approve and proceed. A check named as next work does not by itself withhold Approve.
- Address remaining changes. Offer on every menu, including an approve
  recommendation. This is the numbered alternative to Approve, not a
  fixed slot. On approve it declines Approve rather than inventing
  leftover changes. On request changes, picking it does not start work.
  Print every remaining item that drove that recommendation in one
  follow-up. That follow-up is a question, not the decision menu: a reply
  of 1 is not Approve. Follow-up actions are that remaining work.
  Unrun code review or simplify appear here only when they drove the
  recommendation. Option 1 does all recommended remaining items and
  names them in that sentence. Later options are the same items as
  individual actions, grouped by similar work, ordered by impact. Skip
  an individual option that would repeat option 1. Offer leaving the
  remaining changes last. Picking a follow-up action starts that work. If nothing remains
  to do in this session, the remaining work is the outcome and this gate
  ends.
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
Approve is blocked, Address remaining changes is live, and Explain and
leftover work to file are not:

```text
1. This branch is not ready because remaining source findings still block it.
2. Address the remaining changes on this branch.
3. Show the checks this PR-readiness review ran.
```

Example when Approve is live and Address remaining changes is the
alternative:

```text
1. Approve and proceed to the finishing path.
2. Address the remaining changes on this branch.
3. Show the checks this PR-readiness review ran.
```

Example after option 2 on a request-changes recommendation. This wait is
the follow-up question, not the decision menu:

```text
Remaining work: resolve the CHANGELOG conflict with main, align README
terminology with CHANGELOG.md:20, and finish the stopped actionlint check.

1. Do all remaining work: resolve the CHANGELOG conflict, align README
   terminology, and finish the stopped actionlint check.
2. Resolve the CHANGELOG conflict and README terminology mismatch.
3. Finish the stopped actionlint check now.
4. Leave these remaining changes for a later fix.
```

Show the checks is non-terminal: print the list from the captured gather, then the brief and numbered options again. Starting remaining work from the follow-up, and Explain, are non-terminal: when one finishes, **recompose**. Compare the working-surface identity recorded at the end of step 1 and, when it differs, re-run the steps whose inputs the change touches. A returned `checking-simplicity` result whose recorded identity matches counts and does not start the check over; that skill is read-only and returns its finding to this gate. A mismatch restarts the check. When that result is a question for the user, print the question with its options and wait; the next reply answers it and goes back to the same reviewer, and only the readout that follows is compared, counts when the identity matches, and recomposes this menu.

Completion of this turn: the brief and numbered live options are on screen,
and the run is waiting. Identity re-read and the evidence pack belong to a
later reply of 1.

### On a later reply of 1

If the run is waiting on the remaining-changes follow-up, a reply of 1 is
do-all remaining work, not Approve. Do not apply the withheld-1 rule to
that wait.

If the menu printed a withheld option-1 row, do not approve. Name that
Approve cannot be taken and wait again. Do not enter the finishing path.

Before accepting Approve, re-read HEAD, the merge-base, and the working-surface
identity recorded at the end of step 1, not the file bodies, per
[references/identity-and-argv.md](references/identity-and-argv.md). That
identity is the head OID and the staged, unstaged, and untracked path, mode,
and digest. A same-name
base OID change names the new base in one sentence and keeps Approve. There
is no GitHub mergeability object yet; do not invent a conflict check. A
subject change, a head change, a base-ref rename, or a dirty surface that differs from the recorded surface still rejects and rebuilds.
A change to staged, unstaged, or untracked files restarts this grade even when the head commit is unchanged. A changed digest on that dirty surface restarts the PR-readiness grade and the simplicity check. A finished merge-readiness grade is about the pull-request head, so this dirty-surface change does not restart it. A new head, including a message-only amend, restarts the simplicity check. A new commit on the branch restarts the simplicity check.
The already-typed 1 does not approve that rebuilt gather. Any other matching
re-read is silent. The one-sentence base naming is not a rebuild.

Discover the installed skill that owns opening a pull request the same way
`ce-explain` is: when that skill is present. WORKFLOWS.md's example is
`ce-commit-push-pr`. Then follow
[references/finishing.md](references/finishing.md), which invokes that skill
once. An Executor is a run already executing the `repo-gardener` Executor
contract; that file branches on that fact. Do not keep a second
gardener-only publisher.

If this conversation has no finishing path, name that once and stop. Do not
re-ask Approve. Do not fill or print a pack. Option 1 accepted readiness;
publishing still needs an installed finishing companion.

When finishing is present, instantiate
[assets/evidence-pack-template.md](assets/evidence-pack-template.md)
in-process: the recommendation, material next work after the pull request
exists (or `none`), a coverage close, and the learning signal with any
recorded override. Do not write the
filled pack back to that asset. Do not print `## Evidence pack` as a
readout. Pass the pack to the selected finishing path, which owns its
destination: ordinary
publication writes it into the pull request description.
Continue into that path in this same conversation. That path must not re-ask the same Approve. This
skill still does not itself stage, commit, push, open, or merge a pull request.
The Approve 1 is consumed when finishing starts. It never selects Proceed to merge.

Sanitize the pack for durable use. Summarize intent from the selected durable
intent source: a linked issue or ticket, a brief, or a maintained repository
plan. When step 4 found no durable source, summarize the recorded intent
attestation instead. Do not copy ignored-plan paths or contents, local-only
paths, credentials, or unnecessary personal data.

Completion: a matching re-read, with one sentence when the same-name base
moved, then silent pack plus continue into finishing, including finishing.md,
a named missing-path stop with no pack, or a named rebuild with no pack.
This skill wrote nothing to the
repository. Remove the step 1 temp directory when the same-session later gate
has finished reading its diff file, or as soon as that handoff cannot happen.
This gate ending keeps the file only while this session can still hand it to
that gate for the live head.

## Gotchas

- Untracked paths ship with finishing tools; include them in what option 1
  approves.
- Green CI is not evidence that upstream steps ran.
- Work that may change files is limited to a remaining-changes follow-up
  pick and the option-1 finishing dispatch. A companion skill or repository gate
  owns those writes. The gate itself still does not stage, commit, push, open,
  or merge a pull request.
- A dead session needs a fresh gate. There is no pasteable pack to restock.
- When `checking-merge-readiness` is also installed, a non-Executor option-1
  reply continues into it only after babysit looks merge-ready or cautiously
  looks ready, in a fresh uninvolved context. Pass the temp path and the
  written grade only when this session still holds the diff file for the live
  head. A new session receives the pull-request identity only. An Executor
  option-1 reply does not dispatch it; the Coordinator starts that Reviewer
  after looks merge-ready, cautiously looks ready, or pipeline `success`. This
  gate still does not merge. If merge-readiness is absent after babysit on a
  non-Executor run, name that once and stop.
