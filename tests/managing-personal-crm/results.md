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

## Focused commands and results

- `npx skills-ref validate skills/managing-personal-crm`: passed with no
  diagnostics.
- `wc -l` check: `SKILL.md` is 163 lines, below the 500-line hard limit, with
  branch detail disclosed one level deep.
- An isolated project-level copy under `.agents/skills/managing-personal-crm`
  passed the same validator and matched the source package byte for byte.
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
