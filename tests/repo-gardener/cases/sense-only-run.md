# Sense-only run

Provenance: a missing or empty policy used to make weeks of runs do
nothing silently.

## Prompt

Work only from these synthetic facts. Do not call tools. Grade the three
situations independently.

> Three independent repo-gardener invokes on this repository.
>
> Situation 1. `.agents/repo-gardener.yaml` is missing. Default-branch
> CI, open pull requests, and open issues are readable. No other policy
> file is present.
>
> Situation 2. `.agents/repo-gardener.yaml` exists and is readable.
> `max_pull_requests` is 0. Two approved scans are listed:
> `["npm", "run", "knip"]` and `["python3", "scripts/lint.py"]`. Both
> scans can run from the repository root. Two otherwise qualified units
> exist.
>
> Situation 3. `.agents/repo-gardener.yaml` is valid and readable.
> `max_pull_requests` is 2. One approved scan exits nonzero and reports
> one unused export at `apps/web/lib/unused.ts`. That path is not protected,
> and otherwise a small testable change. Error tracking
> is not readable in this session. Other sense sources are readable.

## Expected behavior

### Situation 1

- [ ] The run senses with available reads, authors nothing, and names
      the run complete.
- [ ] The report contains a complete proposed policy file.

### Situation 2

- [ ] The run runs both scans and reports each argv with exit status
      and a one-line summary.
- [ ] The run authors nothing and says why: capacity is 0.

### Situation 3

- [ ] The unused export is evidence that may qualify a unit. A nonzero
      scan exit is not a candidate by itself.
- [ ] The report does not paste raw scan output.
- [ ] The unreadable error-tracking source is named as a gap. The pass
      does not stop because of it.
