# Personal Chief of Staff Results

## U3 connector acceptance — 2026-07-22

Harness: Codex desktop

Configuration:

- One Google identity is connected across Gmail, Calendar, Drive, and
  Contacts.
- A separate work calendar is shared into that connected Calendar identity and
  is both readable and writable.
- The corresponding work mailbox is unavailable. Conclusions that require it
  must use partial coverage rather than infer complete email access.
- Meeting notes, product analytics, database health, and payment sources were
  readable during preflight. Other optional connected sources were not queried
  without a bounded review question.
- No account identifiers, record contents, credentials, or private source data
  are recorded here.

### Approved mutation results

| Interface and target | Approved test | Observed result | V1 support |
| --- | --- | --- | --- |
| Gmail, connected identity | Create one unsent self-addressed draft and read it by the returned message ID | Acting identity, recipient, subject, body, token, and `DRAFT` state matched; no send action ran | Draft creation is proven after exact review. The retained test draft requires manual deletion. |
| Calendar, personal primary | Create a private transparent event without attendees, reminders, or conferencing; read, rename, read, and delete | Create and update readbacks matched. Delete returned success and the event disappeared from bounded search, but direct ID reads still returned a cached-looking representation | Create and update are proven after exact review. Delete remains indeterminate and manual; it was not retried. |
| Calendar, shared work calendar | Run the same lifecycle with a separate target-coded event and event ID | The shared calendar accepted create and update, proving write access. Delete showed the same search-versus-direct-read inconsistency | Create and update are proven after exact review. Delete remains indeterminate and manual; it was not retried. |

### Explicitly unproven or manual

- Gmail sending, replying, forwarding, draft updates, labels, archive, Trash,
  and draft deletion.
- Calendar invitations, responses, recurring-event changes, conference
  creation, and deletion.
- Any write whose acting identity, destination, exact target, content, or
  resulting object cannot be revalidated through its authoritative interface.

No mutation outside the approved Gmail draft and two temporary calendar
lifecycles was attempted. No failed or indeterminate write was retried.

## U4 immediate mode checkpoints

### Wind-down — 2026-07-22

A fresh-context, read-only evaluation used a scenario with verifiable meetings,
commits, and calendar changes plus existing manual Daily Journal prose. The
loaded skill passed every expected behavior: it used the live template through
the Obsidian CLI, preserved manual content, separated facts from subjective
meaning, began with one broad reflection prompt, kept subjective synthesis and
every write reviewable, separated task/calendar/CRM updates, planned tomorrow,
and made no write during proposal generation.

The adversarial scan found no direct filesystem fallback, hidden state, privacy
assumption, overformalized questionnaire, or premature-completion path. No live
journal mutation was performed during this checkpoint.

### Morning — 2026-07-22

A fresh-context, read-only evaluation covered a nothing-material day, several
missed journals, mixed fixed and flexible calendar commitments with an
overnight preparation need, and one weak health signal. The mode preserved the
zero-to-three foreground limit, continued today with at most one optional
catch-up, kept weak health evidence uncertain, and required every external
change to remain separately approvable.

The adversarial scan identified and closed two ambiguities before acceptance:
the mode now requires each visible personal and work calendar to be queried
separately, and it explicitly preserves commitments established as fixed while
asking when flexibility is unknown. No live source mutation was performed
during this checkpoint.

### Weekly — 2026-07-22

A fresh-context, read-only evaluation covered several skipped reviews, broad
cross-source evidence, a repeated writing insight, weak health evidence, and a
consequential event suitable for a short after-action discussion. The mode
prepared one current review without backfill, led with an executive synthesis,
progressively disclosed evidence, and kept causal lessons, strategy, central
writing claims, and publication decisions under user control.

The checkpoint also confirmed that personal and work calendars remain distinct,
the available personal mailbox is not treated as work-email coverage,
current external research is limited to named editorial questions, health
analysis requires a decision and observation window, scheduled runs do not
write, and all durable changes remain independently approvable. No live source
mutation was performed.

### Quarterly — 2026-07-22

A fresh-context, read-only evaluation covered lapsed reviews, an incomplete
quarter, strategic and causal judgments, longer health evidence, writing, and
next-quarter commitments. The mode prepared one current review without
backfill, led with an executive synthesis, progressively disclosed support, and
kept strategy, causality, tradeoffs, central writing claims, and forward
commitments under user control.

The adversarial scan led to two clarifications before acceptance. Each visible
personal and work calendar is now queried separately without implying work-mail
coverage, and descriptive health patterns are distinguished from causal or
correlation analysis, which requires a named decision, agreed window, and
action-relevant evidence. Scheduled preparation performs no write, the review
uses the Obsidian CLI only, and related changes remain independent. No live
source mutation was performed.

## U5 automation acceptance — 2026-07-22

Read-only discovery found no existing Codex automation records. Calendar
availability was checked separately for the configured personal and work
calendars before the weekly and quarterly times were proposed. The reviewed
schedule bundle was then approved and created against this repository as four
active local Codex automations:

| Mode | Schedule in Pacific time | Readback |
| --- | --- | --- |
| Morning | Daily at 7:00 AM | Active, correct local project, morning-only prompt |
| Wind-down | Daily at 8:30 PM | Active, correct local project, wind-down-only prompt |
| Weekly | Sunday at 11:00 AM | Active, correct local project, weekly-only prompt |
| Quarterly | First Saturday of January, April, July, and October at 10:00 AM | Active, correct local project, quarterly-only prompt |

App-owned records were read back after creation. Exactly four stable automation
IDs exist, all use local execution from this repository, and every prompt loads
the versioned skill, distinguishes personal and work calendar coverage, limits
email evidence to the connected mailbox, requires the Obsidian CLI, rejects
direct vault access, prepares one review bundle, and prohibits a
durable change merely because the schedule fired.

The versioned specification contains generic source roles and no account,
vault, connector, project, automation, credential, or local-path identifiers.
A sleeping or offline Mac does not count as a completed run and creates no
automatic backfill. No scheduled job was forced to run during setup; first-run
behavior remains part of U6 acceptance.

The user later approved shorter display names for all four jobs. Native
readback verified that only the names changed to the `CoS` convention; the
existing automation IDs, schedules, active status, and prompts were preserved.

## U6 launch-readiness acceptance — 2026-07-22

Harness: Codex fresh-context subagents and an isolated project-level Codex
installation. Model: session default.

### Behavioral evidence

- The final trigger gate passed 21 of 21 synthetic queries. All four review
  modes invoked correctly, eight adjacent workflows remained with their
  narrower owners, and a downstream email workflow retained ownership while
  requesting morning-mode priority context.
- Three realistic prompts ran in fresh contexts with and without the skill.
  The bare responses were generally sensible but lacked the skill's explicit
  coverage outcomes, Pyramid-first synthesis, canonical Obsidian CLI boundary,
  exact approval binding, readback classifications, and run endings. The
  with-skill responses supplied those behaviors.
- All 13 synthetic trajectory cases passed with the complete package. These
  cover no-filler mornings, user-owned reflection and strategy, partial email
  coverage with valid shared-calendar evidence, retrieved-content isolation,
  identity drift, indeterminate writes, Obsidian preservation, missed-review
  recovery, fixed calendar commitments, uncertain health evidence, the morning
  foreground limit, and weekly and quarterly resumption without backfill.

### Review and portability

- The final `writing-great-skills` and portable-skill review passed after four
  fixes: scheduled runs now finish and present the read-only bundle before
  waiting, every trigger routes to a mode, current-events research has no
  external-skill dependency, and Obsidian sources resolve by configured role
  rather than fixed note title.
- Official static validation passed. The package, tests, and automation
  specification contain no private identifiers, absolute paths, credentials,
  local IDs, or references to the retired system.
- A clean copied installation into an isolated Codex project found exactly the
  intended skill package. The installed copy passed official validation and
  matched the source package byte for byte.

### Trial launch

The reviewed two-week evaluation task was created through the Obsidian CLI and
verified by note readback and the canonical All tasks Base. It is due August 5,
2026, and measures two separate seven-day journal-continuity periods plus no
more than three user-confirmed evidence packets before a keep, change, or stop
decision. The task prohibits new telemetry, scoring, backfill pressure, and
success claims based on agent activity volume.

The trial's future product outcome is intentionally not claimed here. Scheduled
first runs and the August 5 decision will supply the real evidence and any
redacted escaped failure can become a regression case.

## Personal CRM soft-companion integration — 2026-07-24

Harness: static contract review against synthetic cases 14 through 18. No live
private source was queried and no destination mutation was attempted.

- Morning and weekly now perform bounded relationship cadence and contextual
  discovery only when the companion capability is available. A crossed cadence
  threshold alone cannot create outreach work, and no suggestion is a valid
  result.
- Wind-down now separates a supported contact-date proposal from any distinct
  relationship-load-bearing prose, Task, or communication effect.
- Every relationship effect stays inside the caller's existing action numbers,
  approval flow, and completion state. No nested CRM bundle, catch-up launch,
  or second completion state was introduced.
- Missing companion behavior degrades only relationship-dependent conclusions
  and cannot block the broader review or justify invented CRM data.
- Quarterly behavior remains contextual through the shared source contract. It
  does not perform deliberate cadence scanning or add a separate CRM ritual.

The focused static checks passed for the five new cases and the existing 13
case headings remained present. A final fresh-context judge then passed all 15
expectations across cases 14 through 18, including the corrected
**Already satisfied** contact-date path. Existing ownership, one-bundle,
no-write, foreground-limit, trigger, and completion contracts remained intact.
No live source was queried.

## Pre-PR quarterly relationship boundary correction

Date: 2026-07-24

- Added a negative quarterly case proving that an overdue cadence threshold
  alone cannot create outreach work.
- Added a positive quarterly case allowing one contextual relationship effect
  only when evidence already used by the quarterly review makes the person
  relevant.
- Both paths preserve the existing quarterly bundle, approval flow, and
  no-write preparation boundary without launching broad CRM discovery.
- A fresh-context evaluation passed both cases. Cadence alone produced no
  outreach, while current quarterly evidence supported one independently
  reviewable contextual effect without a broad relationship scan.

Result: passed.
