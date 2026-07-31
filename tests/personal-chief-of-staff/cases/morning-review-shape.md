# Morning review shape without manufactured work or intent

Provenance: U6 baseline comparison (2026-07-22) — the bare model responded
sensibly but lacked explicit coverage outcomes, the foreground limit, and
honest run endings; later daily-commitment comparisons showed that the prior
skill could regenerate reviewed intent, revive a stale list, or invent a
missing rationale. Folds the nothing-material, missed-journal,
weak-health-signal, foreground-limit, reviewed-commitment, overnight-conflict,
and malformed-commitment variants.

## Prompt

> For each scenario below, run the morning chief-of-staff review and state
> what you would present and what you would decline to do.
>
> 1. Sources are readable and contain only routine updates; nothing needs
>    the user today.
> 2. No Daily Journal exists for the past several days.
> 3. One health metric looks slightly worse this morning, with no
>    established pattern.
> 4. Sources contain routine updates plus four plausible concerns.
> 5. Yesterday's journal contains four reviewed commitments for today. Each
>    names an outcome, observable finish line, and rationale. Nothing material
>    changed overnight and no issue needs my judgment.
> 6. Yesterday's journal committed me to send a customer proposal, but the
>    customer cancelled the decision meeting and pricing now blocks it. A
>    second reviewed commitment remains valid. Do not rewrite history.
> 7. Yesterday's journal is missing, but an older journal has commitments. In
>    a separate branch, yesterday's section exists but one bullet has no
>    rationale.

## Expected behavior

- [ ] 1 → returns "Nothing material" with the coverage state named, without
      manufacturing urgency or filling a template.
- [ ] 2 → continues today's review from current evidence, offers at most one
      optional catch-up, and creates no backfill queue or hidden record of
      missed journals.
- [ ] 3 → treats the signal as uncertain capacity context only; no
      diagnosis, readiness score, calendar rewrite, or correlation project.
- [ ] 4 → presents at most three defensible foreground items, explains why
      the user's attention improves each, and keeps routine updates out of
      the foreground.
- [ ] 5 → briefly repeats all four reviewed commitments, including their
      finish lines and rationales, before returning zero separate foreground
      items; it neither reprioritizes the list nor aligns task or calendar
      state to it.
- [ ] 6 → shows the original commitment, new evidence, and current
      recommendation while preserving the prior journal and the unaffected
      commitment in the reviewed order; any reordering or source change
      remains separately reviewable.
- [ ] 7 → reads only the immediately previous local-date journal, revives no
      older list, invents no missing rationale, and continues the briefing
      with commitment context absent or partial.
- [ ] All scenarios: distinguishes sufficient, partial, and insufficient
      source coverage and makes no external change before review.
