# Morning review shape without manufactured work

Provenance: U6 baseline comparison (2026-07-22) — the bare model responded
sensibly but lacked explicit coverage outcomes, the foreground limit, and
honest run endings; folds the nothing-material, missed-journal,
weak-health-signal, and foreground-limit variants.

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
- [ ] All scenarios: distinguishes sufficient, partial, and insufficient
      source coverage and makes no external change before review.
