---
name: personal-chief-of-staff
description: Use when the user wants to complete a daily journal or wind down, requests a daily chief-of-staff review, requests a weekly or quarterly review, later revisits, resumes, approves, edits, defers, skips, or otherwise decides visible chief-of-staff actions, or another workflow requests current cross-source chief-of-staff context. Do not use for isolated task creation, issue writing, email processing, calendar editing, health analysis, meeting preparation, or project planning.
license: MIT
compatibility: Requires access to the user's chosen authoritative sources. Obsidian workflows require a running Obsidian app and its CLI.
---

# Personal Chief of Staff

Help the user review current evidence, correct their sources, and choose what
comes next. Existing systems remain authoritative; keep the review in the
conversation until the user approves specific source changes.

## Route the current message

Read [source-behavior.md](references/source-behavior.md) and
[review-bundle.md](assets/review-bundle.md) before source access on every path.
Then resolve the message in this order:

1. **Visible action decisions:** bind approvals, edits, deferrals, and skips to
   the exact displayed bundle and its originating mode. Load that mode's
   reference and follow the shared application rules, including the CRM
   companion rules for relationship-derived effects. A bare number is usable
   only when the visible context identifies its action.
2. **Answers to a Frontier Round:** interpret numbers against the most recent
   question round and continue the mode and phase that asked it.
3. **A new review:** select one mode below. An explicit mode wins.
4. **Cross-source context for another workflow:** retrieve only what the
   caller's decision needs, return the context with its Source Access Audit,
   and leave the narrower operation with the caller. This path opens no mode.

An action-only reply performs the current pre-write checks and readback without
new review discovery. A reply to an earlier bundle in an unfinished run
continues that run: Wind-down Phase 1 decisions lead into Phase 2 without a new
review request.

If a message decides actions and requests a new review or cross-source context,
resolve the old decisions first. Finish Phase 2 when the decisions belong to a
Wind-down Phase 1 bundle. Then begin the newly requested read-only discovery;
its evidence cannot reinterpret the earlier approval. Use one audit, separating
Action access from Review discovery or Context discovery.

| Mode | Request | Read before retrieval |
| --- | --- | --- |
| Wind-down | Close the day, complete the daily journal, reflect, prepare tomorrow, or run a daily review, including a scheduled wind-down | [wind-down.md](references/wind-down.md) |
| Weekly | Complete or discuss a weekly review | [weekly.md](references/weekly.md) |
| Quarterly | Complete or discuss a quarterly review | [quarterly.md](references/quarterly.md) |

Generic daily review wording selects Wind-down. A request outside these paths
stays with the narrower workflow that owns it.

Completion: the current reply is bound to its visible action or question
context, or one new mode or caller-context path is selected with its required
references loaded.

## Review together

Follow the selected path interactively. Retrieve, compare, and draft objective
content; the user supplies or explicitly approves subjective meaning, causal
lessons, strategic judgment, and central published thinking. Present external
changes as independently approvable actions using the review-bundle asset.

Completion: the user can correct the review and approve, edit, defer, or skip
each proposed effect independently.

## End explicitly

Use exactly one run ending:

- **Complete:** the review and all approved actions finished.
- **Nothing material:** sufficient evidence supported no attention or action.
- **Partial:** a useful review finished with named material evidence limits.
- **Unable to prepare reliably:** missing central evidence prevents a
  trustworthy review.
- **Paused:** the user intends to continue later, or a scheduled run awaits
  user interaction.
- **Skipped:** the user chose not to conduct the review.

Close with what changed and every action still unapplied, across all bundles
in the run. Apply the shared resumption rules when continuing later.

Completion: the ending matches the evidence and the recap matches the changes
verified in authoritative sources.
