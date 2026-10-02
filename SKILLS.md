# Skills

This file is this repository's convention for writing, evaluating, and
recording evidence for agent skills. It builds on the
[Agent Skills standard](https://agentskills.io), with vendor guidance layered
on top. Where sources conflict, a **Conflict:** note names the conflict and
the choice made. The `creating-portable-skills` skill owns the portable
authoring workflow. This host document owns the repository's eval formats,
value assessment, regression checks, trigger evidence, and ship rules; it is
not bundled with the skill.

## Package format

A skill is a directory that holds a `SKILL.md` file and, optionally,
`scripts/`, `references/`, and `assets/`. `SKILL.md` starts with YAML
frontmatter and continues with a Markdown body.

| Field | Required | Rule |
| --- | --- | --- |
| `name` | Yes | 1–64 lowercase letters, digits, and hyphens; no leading, trailing, or doubled hyphen; equals the directory name |
| `description` | Yes | 1–1024 characters |
| `license` | No | Text |
| `compatibility` | No | At most 500 characters; real environment requirements only |
| `metadata` | No | Map of string keys to string values |
| `allowed-tools` | No | Experimental; support varies by harness |

Keep the body at or under 500 lines, with about 5,000 tokens as a target.
Keep file references one level deep from `SKILL.md`, and make every
referenced file resolve inside the skill directory. Harness files such as
Codex's `agents/openai.yaml` stay out of the canonical package unless the
skill needs a capability only that harness provides. A host repository may
allow fewer fields than this table.

**Conflict: `compatibility`.** The standard and Anthropic's skill-creator
validator accept the field. Claude Code accepts it but does not act on it. The
Codex system skill-creator validator rejects it. The standard wins, so expect
Codex's validator to flag the field.

## Descriptions and triggering

Follow the [Agent Skills specification](https://agentskills.io/specification#description-field):
the description is 1–1024 characters and describes what the skill does and
when to use it. Include specific keywords that help agents identify relevant
tasks. Trigger evidence follows the rules below.

## Where evals live

Eval files live in an `evals/` directory inside the skill directory:

```text
<skill>/SKILL.md
<skill>/evals/evals.json
<skill>/evals/eval_queries.json
<skill>/evals/files/         inputs that evals.json names
<skill>/evals/benchmarks/    committed benchmark files
```

`SKILL.md` never references `evals/`, so evals cost no context at run time.
They do ship with any install that copies the whole directory, so eval inputs
stay synthetic and public-safe. Raw run results go to the **Run archive**,
never to `evals/`.

## Eval definitions: `evals/evals.json`

```json
{
  "skill_name": "csv-report",
  "evals": [
    {
      "id": 1,
      "prompt": "Which month in evals/files/sales.csv had the highest total?",
      "expected_output": "Names the highest month and its total.",
      "files": ["evals/files/sales.csv"],
      "assertions": ["The answer names 2026-02 as the highest month"],
      "provenance": "A baseline run named the first row instead of the maximum.",
      "regression_control": false
    }
  ]
}
```

- `skill_name` equals the skill's directory name, and each `id` is a unique
  integer.
- `prompt` is a natural task a user would give, with explicit synthetic
  data. It carries the concrete evidence that task needs and every
  constraint the user requires. Put a short design, snippet, or example
  in the prompt when that is enough to do the task. `files` is optional,
  and only for an input the task needs as a file, with paths relative to
  the skill root. Name a file or document only when the packet contains
  it. The hoped-for conclusion stays out of the prompt, as do instructions
  whose only job is to stage, hint, or grade the eval.
- The executor receives the prompt and any named files. `expected_output`
  describes success for a human reader. `expected_output` and `assertions`
  stay out of the executor packet. Human inspection shows them, and the
  grader receives the assertions with the blind packet under **Grading and
  independence**.
- `assertions` are binary, verifiable statements of the required outcome:
  one or two sharp assertions per eval, or one per numbered independent
  scenario. Freeze them before the check. An eval fails when any assertion
  fails. Another design, implementation, or phrasing that meets the outcome
  passes. Require a particular phrase, structure, or data shape only when
  that shape is itself a fixed requirement. Put deterministic mechanical
  checks in scripts rather than asking a model to grade them.
- `provenance` is an extension. It names the observed failure or baseline gap
  the eval protects, or the contract a regression control guards.
- `regression_control` is an extension. `true` marks a regression control,
  kept to guard one named contract; it never shows an improvement. `false`
  marks a targeted eval. Neither label establishes improvement by itself;
  **Arms and runs** governs failure attribution and shipping.

An eval covers realistic required behavior, an observed failure, or a named
contract. These prompt and assertion rules apply to a new case and to a case
reused from an earlier round. Start a new skill with two or three realistic
evals; a failing no-skill baseline is not a prerequisite. Fold near-duplicate
scenarios into one eval, with numbered scenarios in the prompt and one
assertion for each.

**Conflict: field names.** The standard uses `assertions` here and
`assertion_results` in grading. Anthropic's skill-creator uses `expectations`
for both. Anthropic's platform example uses `query`, `skills`, and
`expected_behavior`. The standard wins, so skill-creator's viewer and
aggregator do not read these files unmodified.

## Trigger evals: `evals/eval_queries.json`

```json
[
  { "query": "which month sold the most in this csv?", "should_trigger": true },
  { "query": "chart these sales by month", "should_trigger": false, "owner": "charting-data" }
]
```

- Write about 20 queries: 8–10 that should trigger and 8–10 near misses.
  Seed them by crossing dimensions where misrouting is likely, such as
  intent, phrasing, and context. Draft the tuples first, then write one query
  for each tuple.
- A near miss shares the skill's topic or wording but belongs elsewhere. Its
  `owner` field, an extension, names the skill or workflow that should take
  it.
- Run each query once by default in a harness with the skill installed and
  retain its activation trace. A native session makes the skill available
  through the harness's ordinary discovery and asks the task without telling
  the model to load the skill. Record the other skills available in that
  session. A query passes when that observed activation matches
  `should_trigger`. Inspect every failure under **Arms and runs**. Record an
  unavailable or inconclusive observation as unverified; it does not pass
  the query.
- To tune a description, split the set 60/40 into train and validation
  queries, and keep both files in the run archive. Revise from train failures
  only. Further rounds follow **Repeats**. Check the selected description on
  5–10 fresh queries. A query used for tuning or selection stays out of the
  fresh check. Label each native observation training, validation, or fresh.
  A validation observation used to select the description remains a selection
  result. Rerun the whole set after any description edit. Keep activation
  results in their own record, apart from output-quality results.
- For a description-only change, check the revised description on the query
  set and use the prior description only on failing queries to diagnose the
  change. This diagnostic subset establishes no overall improvement.

A fresh-context judge that sees only the name, the description, and one query
is a cheap first screen. Label its result a listing proxy. Native activation
evidence is the harness trace from the session above.

## Arms and runs

**Value assessment.** Use this when the question is whether the skill helps,
including a skill that already exists. Run one matched `with_skill` and
`without_skill` pair for each approved case on each declared Executor target.
Each run starts in a fresh context. The `with_skill` trace shows the intended
skill loaded. The `without_skill` trace shows that skill absent. Record the
actual model, harness, and material settings. The result speaks only for those
matched cases, targets, and settings. An inconclusive comparison stays
inconclusive. Record it separately from the ship decision.

A regression check runs each affected eval once per declared Executor target
with the changed skill (`with_skill`). Each run starts in a fresh context and
its trace confirms that the intended variant loaded. New skills check
realistic cases. A behavior check does not wait on a no-skill baseline. On
this path, use a `without_skill` run to diagnose a failure. A cosmetic change
may skip behavioral evaluation.

Inspect **every failure** against the original transcript. Distinguish a
behavior failure from a grader/assertion error or a capture gap. Retain the
original grades and explain corrections in benchmark notes, with the source
evidence. Missing capture leaves the outcome unverified.

Compare or rerun the frozen prior skill (`old_skill`) only on failing evals
to attribute the change. Reuse prior evidence only when its package, prompt,
inputs, assertions, target, and settings match the diagnostic question; retain
its original revision label and original blind grades. If attribution remains
unresolved, the result stays unverified.

**Repeats.** Before another behavioral round, inspect the existing evidence.
Repair a grading, assertion, or capture problem first. Handle an attributable
skill failure through a correction and its affected regression check. The
operator then decides whether another comparative round runs. Before it runs,
name the decision it could change, the result that would change that decision,
the cases, and a spending limit inside the authorized budget. Keep every
earlier result, and report a repeated subset as a subset. The operator may
stop on the current evidence, including an explicit unresolved failure.

**Ship rule.** Ship when the required checks and independent review are
complete and no failure is attributable to the change under test. Known
pre-existing failures remain visible with their evidence and disposition.
An unresolved hold stays unresolved. Record the value conclusion separately.
A new skill must meet its required outcomes; a no-skill failure does not
excuse its own failure. Each substantive edit gets its affected regression
check.

**Execution boundary.** Before native executor, trigger, grader, or reviewer
calls, declare the tool and filesystem boundary. Executors and trigger probes
receive the approved disposable workspace, skill catalog, resources, and
effects. Graders receive the blind packet and no tools. Reviewers are
read-only: they may read the package and evidence, and they do not write,
execute, or modify either. Record the effective settings. The authorized smoke
includes one harmless rejected operation against a disposable fixture. When
the native controls cannot show that boundary, stop further calls for that
role and report the limitation.

A single-arm check or a diagnostic baseline subset supports no improvement
claim. Compare only matched eval sets, inputs, assertions, targets, settings,
and run counts. Never compute an aggregate delta between a full candidate
cohort and a failing-only baseline subset. Periodic broader cross-model sweeps
are separate work with their own authorization.

## Targets

A target is one model in one harness. Use the caller's declared Executor
targets, or the host repository's testing default when the caller supplies
none. Explicit caller restrictions override host defaults. Record the actual
model, harness, and material settings such as reasoning effort for every run.
Structural portability does not require expanding the target set. The portable
skill pins no model names and bundles no runner; the host owns CLI automation
and configuration.

## Cost and budget

The caller must authorize model spend and one budget across all providers
before calls begin. Use `ccusage --mode calculate` with its upstream-maintained
pricing as the single automated price source for current and future models.
These are API-equivalent estimates, not actual subscription debits. Keep
CLI-reported dollar amounts secondary; do not maintain repository rate tables
or use account-wide usage or credit deltas as per-call cost.

Isolate usage records per call and include execution, delegation, grading,
and failed attempts in the budget. A partial or unpriced estimate, or one using an unidentified model, is unknown, not zero or a usable total. Unavailable prices or usage,
exhausted budget, or subscription quota stop further calls. Report the gap;
never fall back to API-key billing. The host implements collection and cost
calculation; this host document defines the evidence contract.

## Grading and independence

Each run's `grading.json` uses the standard's shape:

```json
{
  "assertion_results": [
    { "text": "The answer names 2026-02 as the highest month", "evidence": "\"2026-02 had the highest total, 12\"", "passed": true }
  ],
  "summary": { "passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0 }
}
```

- Scripts grade mechanical assertions. A grader grades the rest. For each
  assertion it first writes its evidence and reasoning, quoting the output
  span or trace line, and then gives the verdict, so `evidence` comes before
  `passed`.
- An example that appears in a grader prompt or in the skill's own text never
  appears in a graded round.
- An independent grader on a different model from the executor grades the
  check blind. For comparisons, one grader grades both arms. Its packet
  contains the final answer, all tool names and inputs, relevant observations
  and artifacts, and all available child readouts, with variant labels removed.
  Replace sensitive values throughout the packet with typed placeholders before
  sending it to the selected grader, preserving the action and evidence needed
  to grade. Exclude private reasoning and author conclusions. If a missing
  trace or safe redaction removes evidence needed to decide an assertion,
  record a capture gap and leave the outcome unverified.
- One independent review checks the package and evidence using the
  `creating-portable-skills` checklist. There is no mandatory pre-spend review
  plus final-review cycle. An unavailable independent grader or reviewer
  leaves the required judgment unverified; author inspection cannot replace it.
- Qualities that binary assertions cannot carry go to specific human
  feedback or a blind comparison of two outputs. Record the result as a note,
  never as a pass or a fail. Agreement with a graded assertion follows
  **Human inspection**.

## Human inspection

Before calls on a value assessment, or on a round whose cases are newly
proposed, the human inspects each case's prompt, inputs, expected outcome,
assertions, and provenance. The approved definitions stay frozen for that
round. An affected regression of an already frozen case set reuses that set.
This inspection is the human's look at the cases. It is separate from the
one independent review.

After the runs, the human can open each case's paired results, original
grades, quality, time, tokens, cost, and available traces. Activation
evidence stays in its own record, apart from output-quality comparisons.

Feedback records agreement or disagreement with one identified grade, and
may include a note. A note may be saved before any grade exists. Agreement
requires an identified grade. Absent feedback stays absent. A later round
or a changed grade starts without the earlier agreement.

Keep the original grade. Record one evidence-backed disposition: evaluation
correction, skill correction, or unresolved. The note and the disposition
explain the grade. A skill correction then takes the affected regression
check. An unresolved disposition stays unverified.

When the inspection surface is unavailable, human review is incomplete.
Keep saved feedback, and leave the step incomplete.

## Run archive

Raw results live in one machine-local archive directory outside every
repository, with one `iteration-<N>` directory per graded round and one
directory per target inside it. Keep the archive after the work ends.

```text
<archive>/<repo>/<skill>/iteration-<N>/<target>/
  eval-<id>-<name>/<arm>/run-<k>/
    outputs/
    transcript       the raw session, including the skill load trace
    timing.json      { "total_tokens": 84852, "duration_ms": 23332 }
    grading.json
    metrics.json     tool calls, steps, and errors in skill-creator's shape
    build.json       { "skill_revision": "abc1234", "package_hash": "sha256:…", "install_path": "…" }
```

- `<target>` names the target, matching the benchmark file's target suffix
  when the file has one, and `<name>` is a short kebab-case label for the
  eval.
- `build.json` identifies the build each run loaded. `skill_revision` is the
  commit under test, or its parent when the change is uncommitted.
  `package_hash` covers the installed package. `install_path` is the
  disposable install the harness loaded. Installation and discovery evidence
  names that `package_hash` and `install_path`. Evidence recorded for a
  different hash applies to that other package.
- Failed runs and partial outputs stay as evidence. Nothing in the archive is
  committed, because transcripts and outputs can hold private data.

## Committed evidence: `evals/benchmarks/`

Each graded round commits one file named `<date>-<short-rev>.json`, for the
date and the revision it tested. When a round covers several targets, commit
one file per target named `<date>-<short-rev>-<target>.json`. Distinct rounds
on the same date, revision, and target use `--iteration-<N>` before the target
suffix to keep both records, where `<N>` matches the archive's `iteration-<N>`
directory: `<date>-<short-rev>--iteration-<N>[-<target>].json`.

```json
{
  "metadata": {
    "skill_name": "csv-report",
    "executor_model": "model-id",
    "timestamp": "2026-09-24T12:00:00Z",
    "runs_per_configuration": 1,
    "harness": "harness-name version",
    "grader": "different model, blind packet",
    "final_reviewer": "separate fresh session",
    "archive_ref": "the-repo/csv-report/iteration-2/model-id",
    "cost_available": false
  },
  "run_summary": {
    "with_skill": {
      "pass_rate": { "mean": 1.0, "stddev": 0.0 },
      "time_seconds": { "mean": 40.5, "stddev": 0.0 },
      "tokens": { "mean": 21000, "stddev": 0.0 }
    }
  },
  "notes": ["Eval 1 ran once; pricing was unavailable, so further calls stopped."]
}
```

- `run_summary` holds one object per arm. A regression check has `with_skill`
  only and no `delta`. A value assessment has matched `with_skill` and
  `without_skill` and may include `delta`. A separate diagnostic round may
  have only `old_skill` or `without_skill`, also without `delta`. Notes
  identify the evals and the diagnostic question. Only matched cohorts may
  share a two-arm summary with a numeric `delta`: changed arm minus baseline.
  `runs_per_configuration` is a positive integer.
- `metadata` requires `skill_name`, `executor_model`, `timestamp`,
  `runs_per_configuration`, `harness`, `grader`, and `archive_ref` (the
  round's target path inside the archive). Record `final_reviewer` when the
  independent review is complete; an earlier round has none.
- Record the complete API-equivalent estimate as `cost_usd`, with its source
  and scope in notes. Otherwise set `cost_available` to `false` and explain
  the unknown estimate. **Cost and budget** governs further calls.
- A `runs[]` array in skill-creator's per-run shape may list each graded run.
  A `notes[]` array holds smoke-check results and blind-comparison
  preferences.
- Preserve original grades; `notes[]` explains every correction, failure
  classification, attribution, feedback disposition, capture limitation, and
  carried-forward result.
- A benchmark states only what its runs checked.

**Conflict: delta and location.** The standard writes numeric deltas to
`iteration-N/benchmark.json` in its workspace. skill-creator writes signed
strings such as `"+0.50"`. The standard's numeric form wins, and the committed
copy lives in `evals/benchmarks/`.

## `claude plugin eval`

Claude Code's `claude plugin eval` runs a plugin's cases in isolated sessions
with and without the plugin, 3 times each by default, and exits non-zero
below a threshold. It is not the runner for this convention:

- It evaluates plugins, not standalone skills.
- Its cases are `evals/<case>/prompt.md` plus `graders/*.md` at the plugin
  root. Claude Code's documentation says that format is not interchangeable
  with `evals/evals.json`.
- It runs Claude only, so it cannot cover targets in other harnesses.

A repository that ships plugin manifests may add it as a Claude-side CI gate
beside this format.

## Enforcement

Commands check these rules:

- `skills-ref validate <skill-directory>` checks frontmatter and naming.
- `python3 scripts/checks/evals.py <skill-directory> [...]` is this
  repository's eval-file check. For the skill directories it is given, it
  checks every field, type, name, and count rule
  this file states for `evals.json`, `eval_queries.json`, and benchmark files,
  plus two consistency rules: `delta` equals the changed arm minus the
  baseline, and a file's target suffix matches `archive_ref`. It checks no
  value ranges and makes no judgment calls, such as whether an assertion is
  decidable, compared cohorts match, a carry-forward is legitimate, or a
  benchmark states only what its runs checked. The catalog check runs it for
  every published skill directory.

No command checks grading quality, blinding, independence, whether a run used
its stated target, or private names. A public repository cannot list the
private names it must not contain, so people and agents check for them before
each push. Claim automated coverage only for the commands above.

## Sources

- Agent Skills specification: https://agentskills.io/specification
- Evaluating skills: https://agentskills.io/skill-creation/evaluating-skills
- Optimizing descriptions: https://agentskills.io/skill-creation/optimizing-descriptions
- Anthropic skill best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude Code skills: https://code.claude.com/docs/en/skills
- Anthropic skill-creator: https://github.com/anthropics/skills/tree/main/skills/skill-creator
- Codex skills: https://learn.chatgpt.com/docs/build-skills
- Critique before verdict: https://github.com/ai-evals-course/evals-skills/blob/main/skills/write-judge-prompt/SKILL.md
- Leakage and target thresholds: https://github.com/ai-evals-course/evals-skills/blob/main/skills/validate-evaluator/SKILL.md
- Dimension tuples: https://github.com/ai-evals-course/evals-skills/blob/main/skills/generate-synthetic-data/SKILL.md
