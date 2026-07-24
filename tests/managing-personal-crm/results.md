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
- `wc -l` check: `SKILL.md` is 143 lines, below the 500-line hard limit, with
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
- The required `writing-great-skills` review is intentionally deferred to the
  final U5 package review, after the chief-of-staff and meeting integrations
  are complete. The portable-skill checklist was the U1 review floor.
- No live source, account, Person note, Task, or vault mutation was part of U1.
