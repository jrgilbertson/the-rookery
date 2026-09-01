---
name: checking-pr-readiness
description: Use when branch work looks complete and needs a readiness decision before another workflow opens a pull request, when asked whether the branch is ready to ship, or when a caller requests an assessment-only exact-subject and exact-revision PR-readiness receipt. Interactive runs end in one owner decision plus an evidence pack; assessment-only runs return one machine-readable pass or action-required receipt without a menu. A direct request to write, open, create, or submit a pull request belongs to PR publishing, not this skill. Do not use for existing-PR feedback, the pre-merge whole-change review, code review, simplification, plan review, general library production-readiness questions, or merging.
license: MIT
compatibility: Requires a git worktree and read access to the host repository. Companion checks degrade to named skips when their skills or tooling are absent.
---
# Checking PR Readiness

Check whether a branch is ready to enter the pull request and
continuous-integration process, then take one owner decision. Internally the
gate gathers the full working surface, upstream-step evidence,
plan-versus-delivered, pre-PR review checks, and learning signal. The spoken readout
uses a Minto pyramid readout for the ship decision (shape in step 7). A
branch is ready when every check below carries a status word, every
finding has a disposition, and the owner has approved that readout.

## Route assessment-only requests first

When the request explicitly asks for assessment-only, headless, unattended, or
machine-readable PR readiness bound to one exact subject and full commit OID,
follow [references/assessment-mode.md](references/assessment-mode.md) instead
of the interactive decision path below. The assessment branch reuses the
current surface, gate discovery, intent, learning, helper exit/status mapping,
and sweep behavior, but its versioned exact-revision chain owns its upstream
receipt inventory. The interactive simplicity backstop in step 3 is not added
to or inferred into the v1 receipt chain. Assessment-only never substitutes
attestation for a receipt and never presents the Minto readout or owner menu.

The gate is read-only. Companion skills own edits, reviews, and capture; the host
repository's hooks and task runners own deterministic re-runs. This skill
verifies those from receipts or dispatches the skill that owns them.

Every interactive run ends in exactly one explicit owner decision, taken
against a readout that matches the working surface at that moment. Options that
change the surface apply the recompose rule before the next decision. Nothing
is reported as done without evidence named inline.

## Status words

Every check reports with one word from this closed set, used consistently and
without synonyms:

- **verified** — the check's defined evidence supports the claim, and the
  readout names it.
- **attested** — the owner statement is permitted evidence for that check;
  record it as attestation, not independent verification.
- **not verified** — the check's required evidence is absent or insufficient,
  and no permitted attestation resolves it.

Also in the set (same one-token rule): **failed**, **not run**, **skipped**,
**unavailable**, **bypassed**, **not applicable**. Use the ordinary meaning of
each word; **bypassed** always records the owner's reason.

## Workflow

### 1. Report the working surface

Report the branch's full working surface before any other check, because that
surface is what the finishing path will stage and what the owner is approving.
Run [scripts/surface-report.sh](scripts/surface-report.sh) when it is present
and executable — it also carries step 6's size check, so pass the cap values
resolved per [references/sweep-classes.md](references/sweep-classes.md) class
11 for every configured automated reviewer and read both results from one run,
statuses per the reference's helper exit map. When discovery proves no
automated reviewer is configured, run without `--cap` for inventory and record
class 11 as `not applicable` rather than treating the helper's `cap unverified`
line as a gap. Always produce the surface report on this run (omit `--defer` even
when step 6 later treats size as covered by a repository gate), and pass
`--full` so the listing is not capped, because this step's completion contract
requires every path to appear in the readout. Otherwise gather the same four
categories directly with git:

- committed on this branch, compared against the merge base with the default
  branch the pull request will target (resolve it from the remote's HEAD, and
  ask the owner when the target is ambiguous),
- staged, unstaged, and untracked paths.

List untracked paths with the same weight as tracked ones. Finishing tools
stage them, so they ship with the change even though no diff command shows
them by default. If the working tree is not a git repository, or git is
unavailable, stop and say so rather than composing a readout from a surface
you could not read.

Completion: every path in all four categories appears in the readout, or the
run stopped because the working surface could not be read from git.

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

This is part of the surface check, not a new sweep class. Completion: the
tracked and ignored enumerations cover every resolved family; every transient
hit is classified as ignored working material, cleanup, or a finding; and
every durable citation is accounted for. If either enumeration is incomplete,
stop rather than treating an incomplete inventory as clean.

### 2. Report repository gates

Discover the host repository's own deterministic gates and report each one
before any model-judgment check runs. Read the repository's agent-instruction
and contribution documents and its conventional hook and task-runner
configuration (git hook and hook-manager files, task-runner and package
manifests, and continuous-integration workflow definitions), and take
the gates they name. List the conventional paths first and read only the
sections that define gates — a search for hook, script, and job names before
any full-file read — rather than pulling whole workflow files into the
conversation.

Report each discovered gate with a status word and with what owns it. Report
hook coverage and whether it has run on the current surface; leave re-running
to the hook. When discovery finds no repository-owned gates, report that
emptiness as unavailable and say the branch has no repository-owned
deterministic coverage, rather than letting silence read as a pass.

Completion: every discovered gate carries one status word and its owner, and an
empty discovery is reported as a named finding.

### 3. Verify upstream steps from evidence

Report each expected upstream step with a status word: code review, code
simplification, solution simplicity, browser testing, design critique or
audit, and learnings capture. Solution simplicity is the independent,
approach-level result from `checking-simplicity`; it is primarily user-requested
and may also run before ungrounded durable machinery enters implementation.
Its presence here is a late backstop, not the recommended first checkpoint.
Browser testing
and design critique apply only to diffs that touch user-interface files; record
how that classification was decided from the paths in the working surface, and
surface an uncertain classification for the owner to decide rather than
resolving it silently.

Before dispatching solution simplicity, resolve the requirements source:
linked issue or ticket, then the brief, then a repository plan only when the
repository maintains plans as durable documentation. When none exists, take
the owner's direct intent attestation now. Extract the
objective, required behavior, hard constraints, and verification criteria for
the simplicity reviewer. Step 4 reuses this source and attestation rather than
resolving them again.

Use this evidence inventory to decide between verified and the honest
alternatives:

- Durable receipts: design-critique snapshots (for example
  `.impeccable/critique/` frontmatter carrying a score and P0/P1 counts) and
  solutions documents present in the working surface. A receipt counts only when
  it identifies this branch's change; a document that covers unrelated work is
  not a receipt for it.
- Browser testing leaves a receipt only when its output or screenshots were
  saved; otherwise it has none.
- A `checking-simplicity` result counts only when this gate dispatches the
  review after step 1 against the complete surface it just inventoried. Supply
  resolved requirements source, objective, required behavior, hard constraints,
  verification criteria, repository, branch, full `HEAD`, and all four path
  categories with their complete current contents. Do not require the reviewer
  to replay that binding in the human readout; this gate owns it through the
  dispatch and continuity checks. Use a fresh context with no planning,
  authorship, implementation, earlier review or findings, or review fixes that
  shaped the subject. When returning a proposed dispatch instead of executing
  it, include or attach the literal complete contents in that dispatch; a
  reference to contents elsewhere in the current conversation is not a
  fresh-context handoff. A result beginning `Proceed with the current approach.`
  is verified only when this dispatch meets that independence rule, no owner
  question remains, and the continuity checks below pass. `Simplify before
  proceeding.` is failed until the approach is revised and checked again.
  `Decide before proceeding` is failed until the decision is resolved and the
  resulting approach is checked again. `Cannot assess yet` remains not
  verified. Keep the dispatch and return uninterrupted by requirements,
  implementation, or other surface-changing work. When it returns, re-read the
  complete requirements and re-run step 1, then re-read the full committed,
  staged, unstaged, and untracked content supplied to the reviewer. Any content
  change makes the result stale and triggers recomposition. Matching paths alone
  are insufficient. An older or same-context result is advisory, never
  verified.
- Code review, code simplification, and solution simplicity leave no durable
  artifact today. Outside the session that ran them, code review and code
  simplification are attestation-only; solution simplicity is not verified by
  owner attestation because its fresh dispatch and subject continuity are part
  of the check.

Write verified only with its evidence named on the same line: a durable receipt
where one exists, or the live fresh dispatch and unchanged subject for solution
simplicity. Otherwise report not verified and offer the owner the chance to
attest where the check permits it; record an attestation as attested. For
solution simplicity, offer a fresh-context `checking-simplicity` run instead.
When the companion skill or tooling a check depends on is absent (no compound
engineering plugin, no `checking-simplicity`, no design-critique tooling),
report that check skipped, name what was missing, and run the rest of the
checklist.

Completion: each of the six steps carries one status word, every verified step
names its supporting evidence, and the user-interface classification and its
basis are stated.

### 4. Compare intent to what was delivered

Use the requirements source and any owner attestation already resolved in step
3. An ignored working plan may help the current comparison, but it is not a
durable source and must not appear in pull-request evidence. Compare the source
against the working surface. List intended items not delivered first, then work
delivered beyond the source as intent drift for the owner to judge. A linked
issue or brief is sufficient; the absence of a separate plan is not a finding.

When step 3 found no issue, brief, or durable repository plan, report the
comparison unavailable, name that absence as a finding, and record the owner's
direct intent attestation as attested.

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

### 6. Run the Pre-PR Review Checks

Read [references/sweep-classes.md](references/sweep-classes.md) and work its
classes in the order listed there, then surface findings in that same order.

Mechanical classes run through the bundled helpers:

- [scripts/surface-report.sh](scripts/surface-report.sh) for diff size (class
  11): one `--cap <reviewer>=<n>` per configured reviewer, values resolved in
  the reference. With no configured automated reviewer, pass no cap and record
  the class as `not applicable`; a configured reviewer without a
  repository-resolved cap remains fail-closed.
- [scripts/evidence-freshness.sh](scripts/evidence-freshness.sh) for stale
  records and plan-named artifacts (classes 4 and 2 support).
- [scripts/changelog-union.sh](scripts/changelog-union.sh) for branch
  changelog entry (class 3).

`changelog-union.sh` and `evidence-freshness.sh` defer when the host
repository owns an equivalent check: invoke them as `<helper> --defer
<gate-name>` with the gate step 2 found, and report that class as covered by
that gate. Surface-report always measures for step 1 (see step 1). When a
repository gate owns the size check, pass no `--cap` for the reviewers that
gate covers and report class 11 as covered by that gate from step 2's
discovery. When step 1's run already resolved the target branch or merge
base, pass it through to `surface-report.sh` and `changelog-union.sh`
(`--base <ref>` or `--merge-base <sha>`) so those two skip re-resolving it.
`evidence-freshness.sh` resolves no base and accepts neither flag.

Every remaining class runs by model instruction from the reference, in one
pass: read the branch diff once and apply every judgment class to that single
reading rather than re-reading the diff per class.

Map helper exit codes and `verdict:` lines to status words using the table in
[references/sweep-classes.md](references/sweep-classes.md) (helper exit →
status word). Script headers are SSOT for each helper's verdict vocabulary.

Completion: every class in the reference carries one verdict from that class's
enumerated set, and each class that fired names where it fired — the file and
line for a line-scoped finding, the file alone for a file-level one, and the
repository surface for a repository-level one, such as a missing changelog
entry or an aggregate file-cap excess.

### 7. Compose the readout and take the owner decision

Complete steps 1 through 6 fully first (they are the evidence). Then brief
the owner: continuous prose shaped by Barbara Minto's pyramid principle —
answer first, then the grouped reasons that support it, then only the evidence
those reasons need.

#### Minto pyramid readout (binding shape)

<!-- Maintainers: this readout shape is mirrored in
checking-merge-readiness/SKILL.md step 6. Skills stay self-contained, so edit
both copies together. -->

Authoring labels (ANSWER / WHY / EVIDENCE / MENU) structure the brief; the
spoken readout is continuous prose without those labels or analysis-bucket
titles.

**ANSWER**
- One recommendation (approve and proceed; request changes; or stop and file
  follow-up, as fits the evidence).
- Short cause clause naming what produced it (gaps, verified checks, or the
  domain producer).
- Name the producers here; argue them under Why. Fold branch identity into the
  opening. Open on the decision, not the working-surface inventory.

**WHY**
- Reasons the answer is true: arguments, one idea each, MECE, jointly
  justifying the call.
- Most decision-relevant first (material gaps first: failed or not-verified
  upstream steps, plan-not-delivered items, open sweep findings, uncaptured
  learning that needs bypass, empty gate discovery).
- Only decision-relevant supports.
- Clean outcome: one affirmative residual that grading found nothing material
  (what the branch does, surface complete including untracked if any, material
  checks verified or attested, plan-versus-delivered clean or accepted drift
  once, learning signal present).

**EVIDENCE**
- Under only the reasons that drove the call.
- Inline in those sentences, with source pointers (receipts, status words,
  paths, helper verdicts). Parentheses are fine for pointers.

**MENU**
- After the pyramid body.
- Options aligned to the answer. Unavailable options say "not offered" or
  "unavailable" in plain words.

**Prose shape**
- Full sentences and short paragraphs. Prefer periods and commas.
- Write enough that a sharp colleague can follow without decoding.
- Prefer continuous sentences over telegram compression (em dash stacks and
  colon reveals that smash a claim into a fragment).
- Supporting detail that did not drive the decision stays out of the spoken
  readout. Offer an appendix only if the owner asks for the full status-word
  inventory.

**Print budgets**
- Clean green (approve and proceed, nothing material): final readout plus menu
  at most about 12 non-blank short lines. Pre-readout dialogue is outside
  this budget.
- Gap-grown: expand Why and Evidence only around the producers of the
  recommendation. Summarize residual clean checks in a short clause when
  needed.

Scale which checks appear by applicability, never by how large the diff feels.
A check is omitted from the spoken readout when the working surface holds no
path it covers (for example no user-interface files means browser testing and
design critique are not spoken). Paths touching authentication, authorization,
payments, data migrations, secrets handling, or a published API contract stay
visible when they have a finding or an incomplete check.

**Done when**
- Exactly one recommendation appears, with its producers named.
- Every printed support answers "Why this recommendation?" and is
  decision-relevant.
- Evidence sits only under supports that need it, with pointers.
- Menu options match the recommendation.

#### Decision menu

Present exactly one decision menu:

1. Approve and proceed to the finishing path.
2. Request changes.
3. Run a flagged missing step now — one option per gap found in steps 2 through
   6 that a present skill owns, each dispatching that skill. A gap with no
   owning skill available — a missing intent source, empty gate discovery — is
   not a dispatch option; it is resolved through attestation where a step
   defines one, or filed through option 5.
4. Have the change or a concept behind it explained, through the available
   explanation capability (the `ce-explain` skill where the compound
   engineering plugin is installed). Omit this option and say it is unavailable
   when no such capability is present.
5. Stop and file follow-up work.

Options 3 and 4 are non-terminal: when one finishes, **recompose** — re-read
the working surface from step 1 and, when it changed, re-run the steps whose
inputs the change touches: the surface report always, and each of steps 2–6
only where a changed path feeds it (a newly captured solutions document
re-runs the learning signal, not gate discovery; a changed hook config
re-runs gate discovery). Re-run all of steps 2–6 when the change's reach is
unclear. A read-only dispatch can change a check without changing a path; rerun
the step that consumes its conversational result. In particular, a returned
`checking-simplicity` result always refreshes step 3 after the surface is
confirmed unchanged. Then present the pyramid readout and menu again. Approval
binds to the surface the owner was shown.

On approval, fill
[assets/evidence-pack-template.md](assets/evidence-pack-template.md) and compose
it into the handoff for the finishing path (not as a second bottom-up readout
before the decision): plan-versus-delivered status, checks run with their
status words and results, the explicit not-verified and attested list, sweep
findings with their dispositions, design-critique scores when present, and the
learning signal with any recorded override. Hand the pack to the finishing path
so that path renders it into the pull request body. Write nothing to the
repository tree and open no pull request.

Sanitize the pack for durable use. Summarize intent and outcomes from the
selected durable intent source: a linked issue or ticket, a brief, or a
maintained repository plan. When step 4 found no durable source, summarize the
owner's recorded intent attestation instead. Do not copy ignored-plan paths or
contents, local-only paths, credentials, or unnecessary personal data. A
transient artifact may inform the run, but the pull request must stand without
it.

Completion: the owner made exactly one decision from the menu against a
pyramid-shaped readout matching the current working surface, and an approval
carries the composed evidence pack for the finishing path.

## Gotchas

- Untracked paths ship with finishing tools; include them in what the owner
  approves.
- Verified requires named supporting evidence on the same line. Solution
  simplicity uses the live fresh dispatch and unchanged subject; other checks
  use their defined receipt or attestation rules.
- Green CI is not evidence that upstream steps ran.
- A dispatched missing step owns its effects. Most may change files;
  `checking-simplicity` is read-only and returns its finding to the caller. The
  gate itself still writes nothing.
- Findings the owner declines still belong in the evidence pack with their
  disposition.
- Ignored working plans are allowed. Tracked transient content and durable
  citations to ignored artifacts are findings.
- The pack reaches the finishing path only through conversation. If the
  session breaks before PR creation, recompose or supply the pack again; it
  exists durably only once the pull request body carries it.
- When `checking-merge-readiness` is also installed, roles stay complementary:
  this gate optimizes entry to review; merge-readiness owns the pre-merge
  whole-change review. Neither requires the other at runtime. An evidence pack is
  optional enrichment for merge-readiness, never a required input.
- A bottom-up inventory, evidence dump, or a menu that contradicts the
  recommendation fails this skill even when the checks are right. The Minto
  pyramid readout is part of the contract.
