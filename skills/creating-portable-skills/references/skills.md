# Skills

This file is the convention for writing, evaluating, and recording evidence
for agent skills. It builds on the [Agent Skills standard](https://agentskills.io),
with vendor guidance layered on top. Where sources conflict, a **Conflict:**
note names the conflict and the choice made. The `creating-portable-skills`
skill ships a byte-equal copy as `references/skills.md`. That skill owns the
authoring workflow and affected regression checks.
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
- `assertions` are binary, verifiable statements: one or two sharp assertions
  per eval, or one per numbered independent scenario. Freeze them before the
  check. An eval fails when any assertion fails. Put deterministic mechanical
  checks in scripts rather than asking a model to grade them.
- `provenance` is an extension. It names the observed failure or baseline gap
  the eval protects, or the contract a regression control guards.
- `regression_control` is an extension. `true` marks a regression control,
  kept to guard one named contract; it never shows an improvement. `false`
  marks a targeted eval. Neither label establishes improvement by itself;
  **Arms and runs** governs failure attribution and shipping.

An eval covers realistic required behavior, an observed failure, or a named
contract. Start a new skill with two or three realistic evals; a failing
no-skill baseline is not a prerequisite. Fold near-duplicate scenarios into one
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
- Run each query once by default in a harness with the skill installed and
  retain its activation trace. A query passes when activation matches
  `should_trigger`. Inspect every failure under **Arms and runs**; an
  unavailable or inconclusive observation is unverified, never a pass.
- To tune a description, split the set 60/40 into train and validation
  queries, and keep both files in the run archive. Revise from train failures
  only. The operator decides whether to iterate or stop within the authorized
  budget. Check the selected description on 5–10 fresh queries. A query used for
  tuning never appears in the validation set or the fresh check. Rerun the
  whole set after any description edit.
- For a description-only change, check the revised description on the query
  set and use the prior description only on failing queries to diagnose the
  change. This diagnostic subset establishes no overall improvement.

A fresh-context judge that sees only the name, the description, and one query
is a cheap first screen. Label its result a listing proxy, never activation
evidence.

## Arms and runs

A regression check runs each affected eval once per declared Executor target
with the changed skill (`with_skill`). Each run starts in a fresh context and
its trace confirms that the intended variant loaded. New skills check
realistic cases; a `without_skill` comparison is used only when needed for
diagnosis. A cosmetic change may skip behavioral evaluation.

Inspect **every failure** against the original transcript. Distinguish a
behavior failure from a grader/assertion error or a capture gap. Retain the
original grades and explain corrections in benchmark notes, with the source
evidence. Missing capture is not proof of correct behavior.

Compare or rerun the frozen prior skill (`old_skill`) only on failing evals
to attribute the change. Reuse prior evidence only when its package, prompt,
inputs, assertions, target, and settings match the diagnostic question; retain
its original revision label and original blind grades. If
attribution remains unresolved, the result stays unverified.

**Ship rule.** Ship when the required checks and independent PR review are
complete and no failure is attributable to changed text. Known pre-existing
failures remain visible with their evidence and disposition. A new skill must
meet its required outcomes; a no-skill failure does not excuse its own failure.
The operator owns iteration and stopping within the authorized budget; there
is no fixed iteration limit or forced ship/revert cycle. Each substantive edit
gets its affected regression check.

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
calculation; this portable package defines the evidence contract.

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
  Exclude private reasoning and author conclusions. A missing trace needed to
  decide an assertion is a capture gap, not a pass.
- One independent PR review checks the package and evidence using the
  `creating-portable-skills` checklist. There is no mandatory pre-spend review
  plus final-review cycle. An unavailable independent grader or reviewer
  leaves the required judgment unverified; author inspection cannot replace it.
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

- `<target>` names the target, matching the benchmark file's target suffix
  when the file has one, and `<name>` is a short kebab-case label for the
  eval.
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
  only and no `delta`. A separate diagnostic round may have only `old_skill`
  or `without_skill`, also without `delta`. Notes identify the evals and the
  diagnostic question. Only matched cohorts may share a two-arm summary
  with a numeric `delta`: changed arm minus baseline. Historical multi-run
  records remain valid; `runs_per_configuration` is a positive integer.
- `metadata` requires `skill_name`, `executor_model`, `timestamp`,
  `runs_per_configuration`, `harness`, `grader`, and `archive_ref` (the
  round's target path inside the archive). Record `final_reviewer` when the
  independent PR review is complete; an earlier round has none.
- Record the complete API-equivalent estimate as `cost_usd`, with its source
  and scope in notes. Otherwise set `cost_available` to `false` and explain
  the unknown estimate. Historical CLI cost records keep their original
  meaning. **Cost and budget** governs further calls.
- A `runs[]` array in skill-creator's per-run shape may list each graded run.
  A `notes[]` array holds smoke-check results and blind-comparison
  preferences.
- Preserve original grades; `notes[]` explains every correction, failure
  classification, attribution, capture limitation, and carried-forward result.
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
- `creating-portable-skills` bundles `scripts/check-evals.py`. For the skill
  directories it is given, it checks every field, type, name, and count rule
  this file states for `evals.json`, `eval_queries.json`, and benchmark files,
  plus two consistency rules: `delta` equals the changed arm minus the
  baseline, and a file's target suffix matches `archive_ref`. It checks no
  value ranges and makes no judgment calls, such as whether an assertion is
  decidable, compared cohorts match, a carry-forward is legitimate, or a
  benchmark states only what its runs checked. Run it from the host repository's existing checks.

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
