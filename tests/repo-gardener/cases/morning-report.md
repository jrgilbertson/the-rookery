# Morning report

Provenance: the report is the only durable artifact of a run and must
be readable in one screen.

## Prompt

Work only from these synthetic facts. Do not call tools. Treat the
configured-issue run and the no-issue variant independently.

> Two independent repo-gardener invokes on this repository. Policy is
> otherwise valid.
>
> One Executor published a pull request. CI is green. Babysit terminal
> is looks merge-ready. A fresh Reviewer's merge-readiness verdict is
> merge, with one low Risk Driver.
>
> One other Executor stopped with a preserved commit and no pull
> request, because a gap needed the owner.
>
> Two approved scans ran: `["npm", "run", "knip"]` exited 0, and
> `["python3", "scripts/lint.py"]` exited 0. Captured output for each
> is many lines long.
>
> Three recommendations exist, including one bot update PR to adopt
> and two protected-path items. One policy proposal exists.
>
> First invoke: `report_issue` is 3521.
>
> Second invoke: the same authored work, scans, recommendations, and
> policy proposal, except `report_issue` is absent.

## Expected behavior

- [ ] Exactly one comment is posted to issue 3521.
- [ ] Report sections appear in this order: pull requests, scans run,
      findings not authored and why, proposed policy changes.
- [ ] The PR row shows URL, CI state, babysit terminal, merge-readiness
      verdict, and Risk Drivers.
- [ ] The preserved commit is named with its reason.
- [ ] The report has no raw scan output, secrets, customer identities,
      or `@` mentions.
- [ ] When `report_issue` is absent, the same report is the run's final
      output and no issue is written.
