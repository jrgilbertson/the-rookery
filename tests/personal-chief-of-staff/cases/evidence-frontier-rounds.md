# Follow-up questions arrive as bounded evidence-frontier rounds

Provenance: issue #131 — follow-ups either stopped at a single shallow question
or expanded into a questionnaire, asked for facts the sources already held,
dropped questions a partial reply left unanswered, and delivered coaching whose
recommendation rested on a comparison the evidence could not support. Scenario
5 covers a gap review found later: an overdue task's disposition belongs to its
sweep row, and no case held both surfaces in one run to catch it migrating into
a round.

## Setup

Run each scenario in a fresh executor using only the supplied test sources. Create a fresh temporary directory outside the repository, set
`PCOS_FIXTURE_ROOT` to it, set `PCOS_FIXTURE_TRACE` to
`<temporary-directory>/trace.jsonl`, prepend
`tests/personal-chief-of-staff/fixtures/bin` to `PATH`, and select the specimen
below with `PCOS_FIXTURE_SPECIMEN`. Scenarios 1 and 2 continue in their
original live executors after each response is captured.

Follow [the execution protocol](../execution-protocol.md) for skill loading,
fixture use, and independent response/trace grading.

Canonical roles are read through `pcos-source read role=<role>`, exactly once
per role per run, before the round is composed. Prompt premises are not a
traced source read. The CRM companion is unavailable in every scenario.

| Scenario | Mode | Specimen | Required bounded role reads |
| --- | --- | --- | --- |
| 1 | Wind-down | `f4r1` | `tasks`, `calendar` |
| 2 | Weekly | `f4r2` | `current_weekly_review`, `tasks`, `calendar` |
| 3 | Wind-down | `f4r3` | `tasks`, `calendar`, `daily_journals`, `strategy`, `learning` |
| 4 | Wind-down | `f4r4` | `tasks`, `calendar`, `daily_journals`, `learning` |
| 5 | Wind-down | `f4r5` | `tasks`, `calendar`, `daily_journals`, `strategy`, `learning` |

In scenario 2 the Weekly run also requires the `weekly_template`,
`last_weekly_review`, `daily_journals`, `strategy`, and `learning` canonical
roles; none has a configured binding, so each is reported **Not configured**
without attempting a fixture command. Scenario 4 has no configured `strategy`
binding and reports it **Not configured**. No daily-journal, journal-template,
or Obsidian binding is configured in any scenario, so each such canonical role
is reported **Not configured** without attempting a fixture command, and no
journal is drafted or written.

Give the grader the evidence required by
[the execution protocol](../execution-protocol.md), including the fixture trace. Remove
each temporary directory afterward.

## Prompt

> Treat each numbered scenario as an independent run in its own context. The
> configured vault timezone is `America/Los_Angeles`. Ask questions only in
> plain chat.
>
> 1. Wind-down closing 2026-09-02, target day 2026-09-03. Eight matters could
>    change tomorrow's plan or the coaching judgment. One is whether tomorrow's
>    customer review already has preparation time set aside. Seven remain as
>    candidate questions: whether the afternoon build block should protect the
>    migration work or the customer proof; whether the two open design
>    questions should be settled by me or delegated; whether the standup should
>    stay daily this month; whether the unfinished writing seed is still worth
>    pursuing; how long the protected block should run, which depends on the
>    build-block answer; whether the following morning should be held clear
>    too, which also depends on it; and whether the standup should move to the
>    afternoon, which depends on whether it stays daily. Start the wind-down.
> 2. Weekly review for the week ending 2026-09-06, coming week starting
>    2026-09-07. Six independent matters could change next week's
>    recommendation: which of the two stalled initiatives to restart first; how
>    much of next week to reserve for the release; whether the recurring
>    partner sync still earns its slot; whether to keep or drop the Friday
>    review block; whether to bring in help for the incident follow-through;
>    and whether to move the quarterly planning kickoff a week later. Lead with
>    the executive synthesis, then ask.
> 3. Wind-down closing 2026-09-02, target day 2026-09-03. The evening block
>    that the journals record being displaced is the release critical path, and
>    the displacement is equally consistent with avoiding that work and with
>    deliberately deferring it because the evening meetings were genuinely
>    valuable; the two readings call for different recommendations. Run the
>    close through the coaching judgment and stop before the journal.
> 4. Wind-down closing 2026-09-02, target day 2026-09-03. I want to know
>    whether the no-meetings-before-11:00 boundary I adopted on 2026-08-24 is
>    working better than what I had before, and whether to keep it. Run the
>    close through the coaching judgment and stop before the journal.
> 5. Wind-down closing 2026-09-02, target day 2026-09-03. You have presented
>    the reconstruction, I have given my free-form reflection, and the Phase 1
>    bundle proposed one row: the overdue partner onboarding deck, with a
>    recommended resolution you labeled an inference because nothing explains
>    what happened to it. I am deferring that row for now. Continue the close
>    through the coaching judgment and stop before the journal.

## Follow-up

For scenario 1 only, after the first response is captured, send this exact
message as a later user turn in the same live context:

> Today felt scattered. I kept switching between the migration work and the
> customer proof and finished neither.

For scenario 2 only, after the round is captured, send this exact message as a
later user turn in the same live context:

> Answering two of them: restart the billing initiative first, and keep the
> Friday review block. Separately, should I hand the partner sync to someone
> else entirely?

## Expected behavior

- [ ] 1 → the first response presents the reconstruction and one broad
      free-form reflection invitation, and it contains no numbered round of
      questions.
- [ ] 1 → the numbered round appears only in the response after the user's
      free-form reply.
- [ ] 1 → that round is one numbered plain-chat list of exactly four questions,
      each with its own recommended answer, asked as one reply covering the
      whole round, with no host question tool and no form.
- [ ] 1 → the four questions in the round are the four independent candidates,
      and the three dependent candidates are named as held for the next round
      rather than asked now.
- [ ] 1 → the preparation-time matter is asked as no question anywhere, and the
      response states the answer read from the calendar, namely the 13:00
      preparation block before the 14:00 customer review.
- [ ] 2 → the round contains exactly five of the six matters, ordered by how
      much each answer would change next week's recommendation, and names the
      sixth as carried to the next round.
- [ ] 2 → after the partial reply, the next round asks or explicitly carries
      forward every unanswered question and previously over-cap matter, re-asks
      neither the billing restart nor the Friday block, and either admits the new question about handing off the partner
      sync with a stated reason it could change the recommendation or holds it
      out with a stated reason it does not clear the bar.
- [ ] 2 → exactly one question step runs before coaching, and any recurring
      thread candidate enters that same round rather than a second round.
- [ ] 3 → one question in the round asks which of avoidance and deliberate
      deferral is present, and its recommended answer is marked as the agent's
      inference.
- [ ] 3 → the coaching names the pattern as the three dated evening
      displacements, states what it costs the user, recommends a boundary or
      decision, names the smallest change to tomorrow's plan, and names the
      future evidence that would show whether it worked.
- [ ] 3 → that boundary is proposed and left unapplied, with no strategy,
      learning, calendar, or task write performed, and the trace shows no
      `pcos-action` operation.
- [ ] 4 → the coaching names the missing evidence, namely that no durable
      record measures the outcome before or after 2026-08-24, names the
      existing Wednesday-afternoon boundary as the comparison, and keeps the
      keep-or-drop recommendation explicitly conditional.
- [ ] 4 → no comparative claim is asserted as established, and no score,
      streak, or grade is produced for either boundary.
- [ ] 5 → no question in the round asks whether the deferred partner onboarding
      deck is still relevant, still wanted, worth keeping, or should be
      dropped, even though its disposition is now the one open matter about it.
- [ ] 5 → the deferred row is reported as deferred and left unapplied, and the
      response says its disposition returns as that sweep row rather than
      becoming a coaching question.
- [ ] 5 → the round still runs and asks the morning-triage question the three
      dated journals support, so the absent overdue-task question is the entry
      bar working rather than an empty round.
- [ ] Every scenario → no question asks for a fact available from a read
      canonical role, no decision already settled in that scenario's session is
      re-asked, and no round exceeds five questions.
- [ ] Every scenario → the questions asked are the ones whose answers would
      change a plan, an interpretation, or a recommendation, and no fixed
      questionnaire, template question set, or repeated form appears.
- [ ] Every scenario → the response leads with its answer, then renders one
      Source Access Audit paragraph naming every configured role considered for
      that response, with a "so" clause on each claim-limiting result and
      unresolved required roles reported not configured. There is no table and
      no HTML details.
