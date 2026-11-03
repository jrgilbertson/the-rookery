# Creating Portable Skills checks

The deterministic fixtures exercise the shipped
[`signal-scan.sh`](../../skills/creating-portable-skills/scripts/signal-scan.sh)
helper against clean, planted, and pressure examples. Run them with:

```sh
bash tests/creating-portable-skills/fixtures/run-signal-scan-checks.sh
```

Run the complete repository gate before shipping:

```sh
lefthook run pre-push --force
```

These checks make no model calls and do not establish skill activation or task
quality. For behavioral evaluation, follow the
[SKILLS.md evaluation workflow](../../SKILLS.md#evaluation-workflow).
