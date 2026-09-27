# Eval cost accounting

Run skill evaluations through the assigned providers' official CLIs. The agent
prepares cases, saves native transcripts, inspects failures, and obtains blind
grades. Follow [SKILLS.md](../../SKILLS.md) for the validation contract. This
helper only prices isolated calls and checks the authorized allowance; it never
launches a model, grades output, or interprets shell commands.

Use Python 3 and [ccusage](https://github.com/ccusage/ccusage) on PATH (or pass
`--ccusage /path/to/ccusage`). ccusage owns upstream prices and arithmetic;
there are no repository rate tables. Version 20.0.24 was integration-tested.
Amounts are API-equivalent estimates, not subscription charges.

## One sequential call at a time

Keep a private accounting directory outside the repository, containing only
this allowance's cost JSON files. Use the same approved total budget on every
command. The operator owns authorization, directory completeness, and matching
each record to its call. Do not run concurrent calls against this directory.

Before **every** execution, grade, retry, or other separately billed call:

```sh
python3 tools/eval-cost/account.py begin "$cost_dir" case1-executor --budget 8
```

Only proceed if this succeeds. It creates a pending record and refuses another
call while any cost is unknown or the allowance is exhausted. It cannot cap
an in-flight call. A returned record does not authorize unapproved work.

Run the official CLI directly, using subscription authentication and an isolated
session store for this call. Check subscription access before inference, remove
API credentials from the process environment, and stop on quota/auth failures;
never switch to API billing. Save the actual invocation/model/settings, native
transcript, output, and session records, including delegated work. Keep these
outside the repository. Do not point accounting at an account-wide session store.

After the call, including a failed attempt, price the reserved record:

```sh
python3 tools/eval-cost/account.py price "$cost_dir/case1-executor.json" \
  --provider codex --transcript "$call_dir/transcript.jsonl" \
  --sessions "$call_dir/codex-home/sessions"
# For Grok, use --provider grok and its streaming JSON transcript.
python3 tools/eval-cost/account.py status "$cost_dir" --budget 8
```

Codex tool-enabled calls require native sessions. Complete native usage can
price a failed call; transcript-only pricing requires a completed turn. An
explicit session path must be a directory. For a tool-free ephemeral
Codex grader, omit `--sessions` and supply the recorded `--model`. Grok's final
per-model summary includes child usage; the adapter prices it once. Claude
summary accounting is also supported, but this grants no permission to execute
Claude. Future models use the same upstream source; unsupported record formats
or unavailable prices remain unknown until supported, never guessed.

A nonzero exit means stop. Preserve the record and evidence. Repeating `price`
can resolve a missing pricing dependency or recovered usage without another
model call; already-known costs cannot be overwritten. If usage cannot be
recovered, report the blocker. Do not delete a pending or unknown record to
continue. Preserve failed/discarded attempts in the total.

## Evidence and judgment

Use fresh contexts and only the inputs needed for each case. Inspect native
transcripts for access outside the declared inputs, missing outputs, or capture
gaps. Missing proof stays unverified. Prepare privacy-safe blind grading packets
and use a different model for grading. Preserve original grades and apply the
repository's failure-attribution ship criterion. The operator decides whether
another iteration is useful and authorized.

This follows the agent-run evaluation workflow described by
[Agent Skills](https://agentskills.io/skill-creation/evaluating-skills); the
repository's affected-case and diagnostic-baseline rules remain authoritative.
No automatic transcript classifier or generalized execution runner is required.

## Verify

```sh
python3 -m unittest discover -s tools/eval-cost -p 'test_*.py'
```

Tests exercise the production estimator/accounting boundary with synthetic
usage and a fake external ccusage response. Saved native Codex/Grok runs can
also be repriced through real ccusage without invoking a model. Aggregate CLI
summaries lack per-request pricing-tier context; those limits are recorded in
the cost JSON along with the ccusage version, report, and lookup time.
