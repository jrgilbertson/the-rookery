# Wind-down captures concrete intent without another task system

Provenance: daily-commitment baseline comparison (2026-07-31) — the prior
skill could propose tomorrow's critical path but did not guarantee three to
five complete commitment bullets, reject activity labels, or preserve ordinary
planning when the configured forward section was absent. The frozen prior also
did not make the current state, user-owned desired outcome, and future
observable evidence independently recoverable for each commitment.

## Prompt

> Treat these as independent wind-down scenarios.
>
> 1. Tomorrow has a broad development block, two fixed meetings, unresolved
>    work, and mixed personal capacity. My configured Daily Journal template
>    contains `## Tomorrow’s Meaningful Commitments`. Help me choose and
>    prepare tomorrow's commitments, but write nothing until I approve the
>    exact journal action.
> 2. The configured template has no forward-commitment section. Prepare
>    tomorrow's plan, but do not invent a journal structure or write anything.
> 3. I explicitly approve keeping “Development” as one bullet even after you
>    explain that it has no concrete outcome or finish line.

## Expected behavior

- [ ] 1 → proposes a flexible list of three to five concrete outcomes after
      considering today's outcomes, unresolved work, capacity, fixed
      commitments, current strategy, and the user's judgment.
- [ ] 1 → each one-to-three-sentence bullet naturally includes an observable
      finish line and a concise, user-approved rationale; labels such as
      “development” or “meetings” are refined before being called complete.
- [ ] 1 → for every independent commitment, the grader can point to the exact
      response spans that establish the current situation, the outcome the user
      is choosing, and the future observable signal that would show closure;
      source activity or an access disclosure does not substitute for that
      signal, and literal `Current`, `Desired`, or `Evidence` headings are not
      required.
- [ ] 1 → presents the exact journal change separately for approval and
      creates no score, lifecycle field, task duplicate, or calendar mapping.
- [ ] 2 → continues ordinary next-day planning, invents no section, and keeps
      every possible task, calendar, or journal effect separate.
- [ ] 3 → preserves the approved wording verbatim, reports the missing
      elements, and does not claim the bullet satisfies the completion
      condition.
- [ ] The answer-first planning remains legible before any source-access
      disclosure, and no rationale, meaning, or desired outcome is silently
      promoted from agent inference to the user's intention.
