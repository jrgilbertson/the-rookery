# Skills

This file is the convention for writing, evaluating, and recording evidence
for agent skills. It builds on the [Agent Skills standard](https://agentskills.io),
with vendor guidance layered on top. Where sources conflict, a **Conflict:**
note names the conflict and the choice made. The `creating-portable-skills`
skill ships a byte-equal copy as `references/skills.md`. That skill owns the
authoring workflow and the choice between full validation and a focused check.
This file owns the formats and rules the workflow produces.

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

The name and description are the only skill text an agent reads when it
decides whether to load the skill. Write the description as an imperative
"Use when…" clause. Put the words a user would type in the first sentence,
because harnesses budget the skill listing. Claude Code caps each entry at
1,536 characters, and Codex caps the whole listing at 2% of the context window
and shortens descriptions first. Say when to use the skill, not how it works.

Err on the side of a pushy description that names the phrasings the skill
should catch. Add an exclusion only where trigger runs show the skill taking
work that belongs to another skill.

**Conflict: voice.** Anthropic's best practices ask for the third person
("Processes Excel files…"). The standard recommends the imperative ("Use this
skill when…"). This convention uses the imperative.

**Conflict: pushiness.** The standard and Anthropic's skill-creator favor
pushy descriptions. The Codex skill-creator warns against catch-all lists.
This convention takes the pushy side and lets trigger runs catch
over-triggering.

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
- `prompt` is a realistic task with synthetic data, and `expected_output`
  describes success for a human reader. `files` is optional, with paths
  relative to the skill root.
- `assertions` are binary, verifiable statements. Write them after seeing a
  first round of outputs, then freeze them before the runs that decide. That
  draft round runs at most once per eval, inside the approved budget. An eval
  fails when any assertion fails.
- `provenance` is an extension. It names the observed failure or baseline gap
  the eval protects, or the contract a regression control guards.
- `regression_control` is an extension. `true` marks a regression control,
  kept to guard one named contract; it never shows an improvement. `false`
  marks a targeted eval, which measures the change. **Arms and runs** says
  when a control is valid and when it blocks shipping.

An eval enters only when a baseline run showed the gap, an observed failure
motivated it, or it is a regression control guarding a named contract. Start a
new skill with two or three evals. Fold near-duplicate scenarios into one
eval, with numbered scenarios in the prompt and one assertion for each.

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
- Run each query 3 times in a harness with the skill installed, and record
  whether the skill activated. A should-trigger query passes when it
  activates on at least 2 of 3 runs. A near miss passes only when it never
  activates. The set passes when every query passes.
- To tune a description, split the set 60/40 into train and validation
  queries, and keep both files in the run archive. Revise from train failures
  only, for at most about 5 rounds. Keep the description with the best
  validation pass rate, then check it on 5–10 fresh queries. A query used for
  tuning never appears in the validation set or the fresh check. Rerun the
  whole set after any description edit.
- For a description-only change, compare the prior and revised descriptions
  on the same query set.

A fresh-context judge that sees only the name, the description, and one query
is a cheap first screen. Label its result a listing proxy, never activation
evidence.

## Arms and runs

A new skill compares `with_skill` against `without_skill`. A revision compares
`with_skill` against `old_skill`, a snapshot of the prior version.
`with_skill` is the changed arm; the other arm is the baseline. Each run
starts in a fresh context, and its trace confirms that the intended variant
loaded.

Full validation runs each arm 3 times. The `creating-portable-skills` workflow
defines the focused check, which has one arm and supports no comparative
claim.

A targeted eval meets its minimum when the changed arm passes at least 2 of 3
runs on each target and beats the baseline by at least 2 runs. An eval uses a
different threshold only when one is written down before the runs.

**Regression controls.** A regression control blocks shipping when the
changed arm passes fewer runs than the baseline. At 3 runs, a gap of exactly
one run extends both arms once, to 8 runs each, and the 8-run counts decide.
A valid control's baseline passes at least 2 of 3 runs; the workflow's
pre-spend review fixes a control that falls short before the deciding runs. If a
control's baseline still passes fewer than 2 of 3 runs in the round, the
control neither blocks nor counts. The benchmark notes it, and the control is
fixed before the next round.

**Ship rule.** A change ships when every targeted eval meets its minimum, no
regression control blocks it, and the gain is worth its measured token and
time cost. The change is worth its cost when the mean tokens and the mean time
on the targeted evals each rise by at most 30% on each target; a larger rise
needs a written reason from the independent final reviewer. Claim an
improvement only on the targets that showed it.

## Targets

A target is one model in one harness. Run full validation on the current
model and harness, plus every target the caller declares. A host repository
may declare a default target set in its own testing documentation. Record the
actual model, harness, and material settings such as reasoning effort for
every run.

**Conflict: model matrix.** Anthropic's checklist asks for tests on Haiku,
Sonnet, and Opus, which is a Claude-only matrix. skill-creator's trigger loop
uses the session's own model. The standard and OpenAI set no matrix. This
convention adopts no fixed matrix; the caller declares the targets.

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
- One grader grades every arm of an eval on a target, using a different model
  from the executor when one is available. The grader sees final outputs and
  tool observations with arm names removed, and never the author's reasoning
  or conclusions.
- The `creating-portable-skills` workflow defines an independent reviewer. It
  requires an independent grader and a different independent final reviewer
  for full validation. It also says when that reviewer acts and what happens
  when a required independent context is unavailable.
- Qualities that binary assertions cannot carry go to specific human
  feedback or a blind comparison of two outputs. Record the result as a note,
  never as a pass or a fail.

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

- `<target>` matches the target suffix of the round's benchmark file, and
  `<name>` is a short kebab-case label for the eval.
- `build.json` identifies the build each run loaded. `skill_revision` is the
  commit under test, or its parent when the change is uncommitted.
  `package_hash` covers the installed package. `install_path` is the
  disposable install the harness loaded.
- Failed runs and partial outputs stay as evidence. Nothing in the archive is
  committed, because transcripts and outputs can hold private data.

## Committed evidence: `evals/benchmarks/`

Each graded round commits one file named `<date>-<short-rev>.json`, for the
date and the revision it tested. When a round covers several targets, commit
one file per target named `<date>-<short-rev>-<target>.json`.

```json
{
  "metadata": {
    "skill_name": "csv-report",
    "executor_model": "model-id",
    "timestamp": "2026-09-24T12:00:00Z",
    "runs_per_configuration": 3,
    "harness": "harness-name version",
    "grader": "different model, blind packet",
    "final_reviewer": "separate fresh session",
    "archive_ref": "the-repo/csv-report/iteration-2/model-id",
    "cost_available": false
  },
  "run_summary": {
    "with_skill": {
      "pass_rate": { "mean": 1.0, "stddev": 0.0 },
      "time_seconds": { "mean": 40.5, "stddev": 3.2 },
      "tokens": { "mean": 21000, "stddev": 900 }
    },
    "without_skill": {
      "pass_rate": { "mean": 0.5, "stddev": 0.0 },
      "time_seconds": { "mean": 31.0, "stddev": 2.1 },
      "tokens": { "mean": 17000, "stddev": 700 }
    },
    "delta": { "pass_rate": 0.5, "time_seconds": 9.5, "tokens": 4000 }
  }
}
```

- `run_summary` holds one object per arm and a numeric `delta`: the changed
  arm minus the baseline arm. A focused check has one arm and no `delta`.
- `metadata` requires `skill_name`, `timestamp`, `runs_per_configuration`,
  `harness`, and `grader`. Add `executor_model`, `archive_ref` (the round's
  target path inside the archive), and, for full validation, `final_reviewer`.
- Record `cost_usd` when the harness reports dollar cost. Otherwise set
  `cost_available` to `false`.
- A `runs[]` array in skill-creator's per-run shape may list each graded run.
  A `notes[]` array holds smoke-check results and blind-comparison
  preferences.
- When a regression control extends to 8 runs, `runs_per_configuration` and
  `run_summary` still cover the planned runs. Add one `notes[]` entry for each
  extended control that gives, for each arm, how many of its 8 runs passed
  every assertion. List the extra runs in `runs[]` when the file has one. The
  extension adds no other file.
- A benchmark states only what its runs checked.

When a repository replaces an older evidence format, keep a one-line pointer
to the last commit that holds it. Git is the archive for committed history.

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
- `creating-portable-skills` bundles `scripts/check-evals.py`, which checks
  the shapes of `evals.json`, `eval_queries.json`, and each benchmark file in
  the skill directories it is given. Run it from the host repository's
  existing checks.

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
