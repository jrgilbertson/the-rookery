---
name: personal-chief-of-staff
description: Run a daily wind-down or journal, weekly or quarterly chief-of-staff review, or cross-source context; set up or manage source maps; or approve, resume, or decide visible chief-of-staff actions or question rounds. Not for morning briefings, same-day triage, standalone meeting or CRM work, or isolated task, issue, email, or calendar edits.
license: MIT
compatibility: Requires access to the user's designated source map and authoritative systems. Obsidian workflows require a running Obsidian app and its CLI.
---

# Personal Chief of Staff

Help the user review current evidence, correct their sources, and choose what
comes next. Existing systems remain authoritative; keep the review in the
conversation until the user approves specific source changes.

## Route the current message

Read [source-access.md](references/source-access.md) before the first source
access or write on every path. Load other resources only when the matched path
below names them. If any path needs first setup, a proposed map change (including a location or
access repair or a version 3 upgrade), or Obsidian sandbox recovery, also read
[source-setup.md](references/source-setup.md) before acting.
Resolve the message in this order:

1. **Visible review action decisions:** bind approvals, edits, deferrals, and
   skips to the exact displayed bundle and its originating mode. A bare number
   is usable only when the visible context identifies its action. Load that
   mode's reference and [action-application.md](references/action-application.md),
   plus [crm-companion.md](references/crm-companion.md) for a
   relationship-derived effect. For a Wind-down Phase 1 bundle, load
   [wind-down.md](references/wind-down.md) to resolve Phase 1 and, once Phase 1
   is resolved, load [wind-down-phase-2.md](references/wind-down-phase-2.md)
   (plus [review-reasoning.md](references/review-reasoning.md) and
   [review-bundle.md](assets/review-bundle.md) if not already loaded) to
   continue directly into Phase 2. For a Wind-down Phase 2 bundle, load
   [wind-down-phase-2.md](references/wind-down-phase-2.md) so its journal and
   template-drift checks run before writing. Perform current pre-write checks
   and readback without new review discovery (other than Phase 2 discovery after
   Phase 1 resolves, or later-day recomputation). Load
   [source-bindings.md](references/source-bindings.md) only when the approved
   target cannot otherwise be resolved or when continuing into Phase 2 without
   it loaded; stop that action if its binding remains unresolved.
2. **Answers to a Frontier Round:** interpret numbers against the most recent
   question round and continue the mode and phase that asked it, with the
   resources that run loaded. For a Wind-down Phase 2 round, load
   [wind-down-phase-2.md](references/wind-down-phase-2.md) (plus
   [review-reasoning.md](references/review-reasoning.md) and
   [review-bundle.md](assets/review-bundle.md) if not already loaded).
3. **Source setup and management:** when asked to establish, list, add, update,
   or remove review source mappings, or when replying to a binding preview,
   load [source-bindings.md](references/source-bindings.md) and
   [source-setup.md](references/source-setup.md), then resolve the requested
   mapping operation with the user. Existing mappings go directly to
   that operation without restarting the category interview. This path opens
   no mode; finish it under
   [Finish standalone setup](references/source-setup.md#finish-standalone-setup).
4. **A new review:** select one mode below. An explicit mode wins. Load
   [source-bindings.md](references/source-bindings.md) and resolve the private
   map before the mode's source retrieval. Before retrieval, also load
   [review-reasoning.md](references/review-reasoning.md), the mode reference,
   and [review-bundle.md](assets/review-bundle.md). For Wind-down, start with
   [wind-down.md](references/wind-down.md) (Phase 1) and load
   [wind-down-phase-2.md](references/wind-down-phase-2.md) only after Phase 1
   resolves (including an interactive zero-row Phase 1 sweep). Load
   [action-application.md](references/action-application.md) before proposing
   the first action, and [crm-companion.md](references/crm-companion.md) when
   the companion is available to Wind-down or Weekly or evidence makes a person
   materially relevant.
5. **Cross-source context for another workflow:** load
   [source-bindings.md](references/source-bindings.md) for only the roles that
   caller's decision needs. Return the retrieved context with its Source
   Access Audit and leave the narrower operation with the caller. This path
   opens no mode.

A reply to an earlier bundle in an unfinished run continues that run:
Wind-down Phase 1 decisions lead into Phase 2 via
[wind-down-phase-2.md](references/wind-down-phase-2.md) without a new review
request, loading any path-4 resource not already loaded.

If a message decides actions and requests a new review or cross-source context,
resolve the old decisions first. Finish Phase 2 when the decisions belong to a
Wind-down Phase 1 bundle. Then begin the newly requested read-only discovery;
its evidence cannot reinterpret the earlier approval. Use one paragraph audit,
separating Action access from Review discovery or Context discovery.

| Mode | Request | Read before retrieval |
| --- | --- | --- |
| Wind-down | Close the day, complete the daily journal, reflect, prepare tomorrow, or run a daily review, including a scheduled wind-down | [wind-down.md](references/wind-down.md) (Phase 1); load [wind-down-phase-2.md](references/wind-down-phase-2.md) only after Phase 1 resolves |
| Weekly | Complete or discuss a weekly review | [weekly.md](references/weekly.md) |
| Quarterly | Complete or discuss a quarterly review | [quarterly.md](references/quarterly.md) |

Generic daily review wording selects Wind-down. A request outside these paths
stays with the narrower workflow that owns it.

Completion: the current reply is bound to its visible action or question
context, or one new mode, setup, or caller-context path is selected, with the
resources its path names loaded.

## Review together

Follow the selected mode interactively. Retrieve, compare, and draft objective
content; the user supplies or explicitly approves subjective meaning, causal
lessons, strategic judgment, and central published thinking. Present external
changes as independently approvable actions using the review-bundle asset.

Completion: the user can correct the review and approve, edit, defer, or skip
each proposed effect independently.

## End explicitly

Use exactly one run ending. A standalone setup run conducts no review; judge
its ending by
[Finish standalone setup](references/source-setup.md#finish-standalone-setup).

- **Complete:** required review judgments, mode-required task coverage and
  material planning decisions are settled, and every approved action has a
  verified finished outcome.
- **Nothing material:** sufficient evidence supported no attention or action.
- **Partial:** a useful review finished with named material evidence limits.
- **Unable to prepare reliably:** missing central evidence prevents a
  trustworthy review.
- **Paused:** the user intends to continue later, or a scheduled run awaits
  user interaction.
- **Skipped:** the user chose not to conduct the review.

Close with verified effects, reviewed intent, unresolved decisions, material
coverage limits, and every unapplied or unconfirmed action across all bundles.
For an open required judgment, approval or calendar placement, ask for its
disposition or report the blocked or limited state. Apply the shared
[resumption rules](references/source-access.md#end-and-resume-honestly) when
continuing later.

Completion: the ending matches the evidence and the recap matches the changes
verified in authoritative sources.
