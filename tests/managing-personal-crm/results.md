# Acceptance results: managing-personal-crm

Date: 2026-07-24

Harness: Codex CLI fresh contexts. Model: session default.

## U1 behavioral evidence

- Three synthetic baseline cases were written before the skill package.
- Three fresh contexts without the skill established the characterization. The
  clearest red behavior offered a provisional triage bundle despite a failed
  required source preflight.
- Three clean fresh contexts then loaded only the package files needed for the
  same scenarios. All passed: direct identity collision remained safely
  unresolved while preserving valid contact semantics, embedded discovery
  stayed inside the caller's bundle, and catch-up stopped before triage.
- One initial embedded evaluator read the test fixture after loading the skill.
  That contaminated observation was discarded and rerun in a fresh context
  restricted to package files.
- Three listing-level judges evaluated all nine should-trigger and nine
  near-miss queries. The final description passed 54 of 54 judgments: every
  should-trigger activated three times and every near-miss was rejected three
  times.

Behavior changed: yes. The package adds explicit direct, embedded, and catch-up
ownership; conservative identity; contact, cadence, and durable-memory
semantics; canonical routing; duplicate suppression; required-source blocking;
mixed-schema transition; review, apply, and readback; recoverable cleanup;
no-hidden-state continuity; and successful no-action behavior.

## Existing tests inspected

- `tests/reviewing-meetings/baseline-cases.md`
- `tests/reviewing-meetings/trigger-queries.md`
- `tests/reviewing-meetings/results.md`
- `tests/personal-chief-of-staff/baseline-cases.md`
- `tests/personal-chief-of-staff/trigger-queries.md`
- `tests/personal-chief-of-staff/results.md`

## Tests added

- `baseline-cases.md`: three compared aggregate cases plus focused synthetic
  trajectories covering AE1-AE13 and the U1 edge conditions.
- `trigger-queries.md`: nine should-trigger and nine near-miss queries with
  three listing-level judgments each.
- This results record contains sanitized process and outcome evidence only.

## U1 focused commands and results

- At the initial U1 package checkpoint, `npx skills-ref validate
  skills/managing-personal-crm` passed with no diagnostics. This result applies
  to that package revision, before the later U5 and U6 changes.
- `wc -l` check: `SKILL.md` is 163 lines, below the 500-line hard limit, with
  branch detail disclosed one level deep.
- At the same U1 checkpoint, an isolated project-level copy under
  `.agents/skills/managing-personal-crm` passed the same validator and matched
  the source package byte for byte.
- Fresh-context baseline comparison: 3 of 3 with-skill cases passed after 3
  without-skill characterization runs.
- Fresh-context trigger judgments: 54 of 54 passed.
- Repository status and package scans were limited to the assigned paths; no
  full repository suite ran.

## Deliberate exceptions

- No script was added. The observed failures were instruction and routing
  gaps, and prose corrected them in fresh-context evaluation.
- The U1 package used the portable-skill checklist as its initial review floor.
- No live source, account, Person note, Task, or vault mutation was part of U1.

## U2 proposal-only live checkpoint

- A recent completed meeting, its canonical Person note, and its existing
  follow-up Task were read only through the Obsidian CLI. The skill recognized
  that the contact date, durable meeting context, and dated commitment were
  already represented, returned zero novel effects, and did not duplicate any
  destination. A legacy follow-up field remains visible for later reviewed
  conversion rather than being silently removed.
- A current writing draft was compared with bounded Person-note evidence. The
  skill found one active relationship with a concrete connection to the topic
  and a plausible request for feedback. It returned a conversation-only
  outreach suggestion, without inventing a wildcard, Task, writing-backlog
  item, or Person-note edit.
- Both cases used live private evidence but record only sanitized pass/fail
  findings here. No vault or source mutation occurred.

Result: passed.

## Proactive review: reversible-probe atomicity

Date: 2026-07-26

- The separately approved reversible trash-capability probe is now the explicit
  exception to the general all-or-nothing single-target action rule.
- Its observable intermediate states remain governed by exact state reporting,
  dependent cleanup **Skipped**, no blind retry, and a bounded repair. The
  exception grants no authority to any other non-atomic effect.
- A focused public-safe regression records the interaction between the general
  atomicity rule and the probe sequence. No live vault or trash operation ran.

Result: passed.

## PR review follow-up: catch-up relationship contract continuity

Date: 2026-07-26

- A catch-up inventory confirmation that passes required preflight now loads
  the relationship contract before inspecting the first Person note for
  stage-one triage.
- A disposition continuation that advances to another triage batch loads the
  same contract before inspecting the next Person note. Blocked inventory-only
  turns may stop without loading it.
- Mixed-schema target fields, conditional tiers, and legacy mappings therefore
  use one contract across first and later bundles. Dispositions remain reviewed
  classifications and authorize no note mutation or cleanup.
- A fresh read-only evaluator passed the focused load-order and no-mutation
  scenario. Public-safe regressions cover both the first and next triage
  transitions.
- No live Person note, source inventory, or vault content was queried or
  changed.

Result: passed.

## PR review follow-up: deferred actions and Messages rechecks

Date: 2026-07-26

- A request to revisit or resume a deferred action from a visible Direct or
  Catch-up CRM bundle now recovers the exact proposal for another decision. It
  is not approval and performs no write, recheck, or new discovery.
- When approval-time source revalidation will query configured Apple Messages
  through `imsg`, the workflow loads the Apple Messages adapter before the
  first read. It does not load the adapter when no Messages query is needed.
- Three fresh listing-level judges invoked for both CRM resume queries and
  rejected an email-owned near-miss, for 9 of 9 passing judgments. Focused
  public-safe regressions cover resume-without-approval plus positive and
  negative adapter-loading paths.
- No live message history, Person note, or destination was queried or changed.

Result: passed.

## PR review follow-up: catch-up continuation routing

Date: 2026-07-26

- The listing metadata now routes confirmations and revisions of a required
  visible catch-up source inventory back to the CRM skill.
- The runtime resolver recognizes source-inventory decisions and stage-one
  dispositions before ordinary action handling or mode selection, then resumes
  the exact visible catch-up stage through the catch-up reference.
- Stage-one `active`, `dormant`, `reference`, `ended`, `merge`, and `delete`
  decisions remain reviewed classifications in the conversational recap. They
  authorize no Person-note change or cleanup; only separately proposed effects
  and reversible cleanup actions enter application handling.
- Three fresh listing-level judges invoked for both catch-up continuation
  queries and rejected a meeting-owned action near-miss, for 9 of 9 passing
  judgments. Focused public-safe regressions cover inventory revision and mixed
  dispositions with no destructive action.
- No live Person note, source inventory, or vault content was queried or
  changed for this review follow-up.

Result: passed.

## PR review follow-up: ownership, approval safeguards, and merge ordering

Date: 2026-07-26

- Direct CRM now routes unrelated work through the configured canonical task
  or issue workflow while retaining CRM bundle numbering, approval handling,
  and completion. Embedded CRM continues to leave that work with its caller.
- Approval-only Direct and Catch-up responses load source behavior before any
  pre-write read or identity judgment, then load the relationship contract
  when Person semantics apply, before application rechecks.
- A fresh backlink, alias, and identity scan that preserves the same-person
  binding is now a shared prerequisite for both merge mutations. New identity
  conflict or indeterminate evidence leaves both notes unchanged; partial
  outcomes remain possible only after the shared prerequisites pass.
- Two independent read-only evaluators passed the ownership, safeguard-loading,
  and merge-ordering expectations, for 3 of 3 passing scenario groups. Focused
  public-safe regressions cover Direct and Embedded ownership, approval-only
  loading, and both merge safe-stop paths.
- No live Person note, source, task, issue, or vault content was queried or
  changed for this review follow-up.

Result: passed.

## PR review follow-up: deletion and catch-up completion

Date: 2026-07-26

- A newly meaningful backlink or material alias or identity signal now
  invalidates a previously approved delete even when no second target needs
  repair. The workflow presents a revised delete and never trashes under stale
  approval.
- A deferred stage-two reconstruction remains outstanding catch-up work for a
  retained relationship. It prevents **Catch-up complete** and ends **Partial**
  or **Paused**, depending on whether the workflow or the user must act next.
- Focused synthetic cases preserve separate numbered repairs, safe stops for
  indeterminate evidence, canonical cleanup readback, and recoverable trash.
- No live Person note, relationship source, or vault content was read or
  changed for this review follow-up.

Result: passed.

## Pre-PR cleanup safety correction

Date: 2026-07-24

- Added focused synthetic checks that require the disposable trash proof to be
  an independently approved numbered prerequisite with an exact absent path,
  complete content, operations, and final recoverable state.
- Added the partial-failure boundary: any failed or indeterminate restore,
  readback, or absence check skips an approved dependent cleanup, keeps new
  cleanup manual until safe proof exists, reports only observed state, and
  cannot overwrite a colliding note or imply broader vault safety.
- A fresh-context comparison confirmed that the prior package could treat one
  merge approval as authority for the hidden probe and had no explicit probe
  outcome. The revised package required separate approval, prevented overwrite,
  and assigned one outcome to the probe and one to the dependent cleanup.

Result: passed. No live vault mutation was performed.

## U2 live Obsidian contract

Date: 2026-07-24

- Read-only discovery immediately before application confirmed 480 legacy
  Person notes, 155 legacy follow-up fields, 94 active cadence exceptions, one
  active cadence record without a contact date, and two effective references.
- The user approved the Person Template, transition-aware Base, and Personal
  CRM structure note as three independent actions.
- The Person Template now writes only the target metadata and includes the four
  relationship prose anchors. The legacy sphere and follow-up fields are no
  longer created by the template.
- The Base was validated as YAML before application. All seven views rendered
  through the Obsidian CLI after readback: 480 All People, 94 Relationship
  Attention, one Active Missing Contact, 480 Catch-up Queue, 155 Legacy
  Commitments, two References, and 305 Dormant and Ended.
- The structure note now documents the target Person contract, canonical task
  routing, review and readback behavior, staged catch-up, and the new views. Its
  existing Company Schema and Typed Structure Notes sections were preserved.
- Every mutation used the Obsidian CLI with an explicit vault and exact target.
  Each artifact was reread immediately before application and read back after
  it. No Person note was migrated, no legacy commitment was removed, and the
  vault was not linted.

Result: passed.

## U5 package and instruction review

- The final `writing-great-skills` review found four actionable issues. The
  corrected package now makes catch-up a true triage-first branch, handles
  visible action decisions before new discovery, treats an existing newer
  contact date as **Already satisfied**, and leaves relationship semantics in
  the CRM companion instead of duplicating them in meeting review.
- A portability audit found and corrected one provider-specific task-routing
  phrase. Runtime instructions now use the configured canonical relationship
  task system; the host may still configure that destination as Obsidian Tasks.
- Three current skill packages passed the official cached Agent Skills
  validator. Repository listing found four public skills, including exactly one
  `managing-personal-crm` package.
- A clean local copied installation found one selected CRM skill and installed
  it for both Codex and Claude Code. Both installed copies matched the source
  package byte for byte at the installation checkpoint.
- Same-door scans found no private source content, account identifiers,
  absolute paths, vault names, retired-system machinery, hidden state,
  executable artifacts, broken references, or unused runtime files.
- Fresh-context companion regression judges passed 15 of 15 chief-of-staff
  expectations and all eight meeting scenarios while preserving caller
  ownership, one bundle, approval safety, canonical routing, and existing
  completion states.

Result: passed after the documented corrections.

## U6 local Messages adapter checkpoint

Date: 2026-07-24

- Installed `imsg` 0.13.3 from its official Homebrew tap.
- Granted the parent desktop application read access through the macOS Full
  Disk Access boundary. This setup did not request or enable Messages
  Automation permission.
- A metadata-only chat probe and a redacted one-message history probe passed.
  Results exposed stable chat and message identifiers, participants, native
  timestamps, group context, reply context, reactions, and attachment metadata
  without recording private message content here.
- A high-limit catch-up probe returned fewer chats than its limit, with stable
  identifiers and participant metadata throughout. Aggregate statistics
  corroborated an accessible history range. One list-only group chat accounted
  for the count difference and returned zero retrievable history rows. Exact
  private counts and dates are intentionally omitted; these are observed local
  bounds, not evidence that another source has no earlier data.
- The adapter reference permits bounded `chats`, `history`, `search`, and
  `stats` reads only. Sending, reactions, read receipts, typing, live watches,
  group mutation, polls, and advanced bridge operations remain outside CRM
  authority.
- A fresh-context comparison found that the previous package preserved generic
  source safety but could not operate or preflight `imsg`. The revised package
  passed the same synthetic case with executable read bounds, exact field
  semantics, permission diagnosis, and fail-closed breadth reconciliation.
- An adversarial portability review found four adapter inconsistencies. The
  corrected reference now proves a high-limit result is untruncated, maps chat
  list `id` to `history --chat-id`, permits aggregate statistics in the
  configured timezone, scopes its pointer specifically to `imsg`, and compares
  count differences symmetrically. The final recheck found no actionable issue.
- The `writing-great-skills` pass found the provider detail correctly disclosed
  behind one exact context pointer, one authoritative command list, and
  checkable completion criteria. No additional split or runtime machinery was
  warranted.
- For the later U6 package revision, the official validator command was
  unavailable under the current external package-execution policy. Manual
  validation passed portable frontmatter, name, description length, body
  length, self-contained references, private path scans, and whitespace
  checks. Three fresh listing-level judges received only the updated name and
  description plus two focused queries. All three routed a direct CRM-bundle
  approve/defer/skip response to this skill and rejected approval of an
  embedded chief-of-staff bundle action, for 6 of 6 passing judgments.

Result: passed.

## PR review follow-up

Date: 2026-07-24

- The listing description now routes decisions from both direct and catch-up
  CRM bundles while leaving embedded relationship actions with the caller.
- Catch-up stage one loads the relationship contract after preflight and before
  Person-note inspection. It uses only the target schema, conditional tier
  requirements, and legacy mappings for triage; rich reconstruction remains a
  stage-two responsibility.
- Immediately before an approved delete, the workflow rechecks backlinks,
  aliases, and identity collisions. New repair needs invalidate the stale
  approval, and indeterminate evidence stops without trashing or claiming
  deletion.
- Three fresh listing-level judges received only the revised skill name and
  description plus a catch-up decision query and an embedded chief-of-staff
  near-miss. All three invoked for the catch-up decision and all three left the
  embedded action with the caller, for 6 of 6 passing judgments.
- Focused synthetic cases record the stage-one contract boundary and the final
  pre-delete relationship check. No live Person note or vault content was
  changed.

Result: passed.
