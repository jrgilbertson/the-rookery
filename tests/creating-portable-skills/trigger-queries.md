# Trigger query test: creating-portable-skills

Build 8-10 should-trigger phrasings (include non-obvious ones) and 8-10
near-misses. Judge each query 3 times at the listing level in a fresh agent
context: show the context only the skill's name and description alongside
the query and ask whether it would activate, requiring a plain yes, no, or
unsure. Live harness-native discovery is recorded separately (see
`results.md`) as stronger evidence.

Pass rule: each should-trigger query must activate in at least half its runs,
meaning 2 of 3. Any near-miss activation fails the whole set.

Date: 2026-07-16 | Harness: Claude Code subagents (fresh context per judge) | Models: Haiku 4.5, Sonnet, Fable 5

Re-run 2026-07-16 after the description revision from the writing-great-skills review (workflow-summary sentence removed, migrate/port branch collapsed): identical results, every should-trigger at rate 1.0, zero near-miss activations.

Re-run 2026-07-16 after the rename to creating-portable-skills: identical results again, full-rigor tier, three model families.

## Should-trigger queries

| Query | Run 1 | Run 2 | Run 3 | Rate |
| --- | --- | --- | --- | --- |
| Help me create a new skill for formatting SQL queries | yes | yes | yes | 1.0 |
| I want to write an agent skill that enforces our commit message style | yes | yes | yes | 1.0 |
| Review my deploy-checks skill and tell me what's wrong with it | yes | yes | yes | 1.0 |
| Update the description on my notes skill so it triggers more reliably | yes | yes | yes | 1.0 |
| Port this skill from my old toolkit repo into this collection | yes | yes | yes | 1.0 |
| Migrate the data-validation skill over here and fix it up during the move | yes | yes | yes | 1.0 |
| My skill never fires when I ask about invoices — fix its triggers | yes | yes | yes | 1.0 |
| Turn this prompt I keep pasting into a proper reusable skill | yes | yes | yes | 1.0 |
| Is my skill's SKILL.md structured right? Audit it | yes | yes | yes | 1.0 |
| Make this skill work in Codex too, not just Claude Code | yes | yes | yes | 1.0 |

## Near-miss queries (expected: no trigger)

| Query | Expected | Run 1 | Run 2 | Run 3 |
| --- | --- | --- | --- | --- |
| Design evals for my dataset | no trigger | no trigger | no trigger | no trigger |
| Create a plugin for my editor that adds a slash command | no trigger | no trigger | no trigger | no trigger |
| Review my README for clarity | no trigger | no trigger | no trigger | no trigger |
| Build a grader and rubric for judging model outputs | no trigger | no trigger | no trigger | no trigger |
| Help me write better prompts for my chatbot | no trigger | no trigger | no trigger | no trigger |
| Set up an MCP server for our internal API | no trigger | no trigger | no trigger | no trigger |
| Create a GitHub Action that lints markdown | no trigger | no trigger | no trigger | no trigger |
| What skills should I install for web development? | no trigger | no trigger | no trigger | no trigger |
| Summarize what this skill does | no trigger | no trigger | no trigger | no trigger |
| Write documentation for our API endpoints | no trigger | no trigger | no trigger | no trigger |

## Tuning

Fix failures by front-loading trigger words and describing when to use the
skill. Do not summarize the workflow. A description that summarizes the steps
makes agents follow the summary and skip the body. After tuning, rerun the full
set.

## 2026-07-27 frontier-retune case definitions

These are predeclared checks, not run results. Keep the 2026-07-16 observations
above unchanged. Append actual states and evidence after running against the
final description and local-source package revision.

### Declared current target set

| Target cell | Exact model | Harness and configuration | Query set |
| --- | --- | --- | --- |
| opus-5 | `claude-opus-5` | Resolve and record exact harness, version, and configuration before running | Reuse the ten should-trigger and ten near-miss queries above |
| sol-5.6 | `gpt-5.6-sol` | Resolve and record exact harness, version, and configuration before running | Reuse the ten should-trigger and ten near-miss queries above |

For each target, judge every unchanged query three times in a fresh context
that sees only the final skill name and description. This is a listing proxy:
it passes when every should-trigger query receives at least two `yes` judgments
and no near-miss receives any `yes`. It does not satisfy a native check.

### Separate evidence states to record

| Check | Attribution | State to append after execution | Required evidence |
| --- | --- | --- | --- |
| Structural validation | Final package revision | [passed / failed / unverified] | Validator, version, command, and output or limitation |
| Listing proxy | Each model-harness target cell | [passed / failed / unverified] | Per-query judgments and exact target metadata |
| Native discovery | Each package-harness cell | [passed / failed / unverified] | Native discovery observation or limitation |
| Local-source install | Each package-harness cell | [passed / failed / unverified] | Local source revision and install output or limitation |
| Installed-content identity | Each package-harness cell | [passed / failed / unverified] | Diff, checksum, or equivalent source-identity proof |
| Native load | Each model-harness target cell | [passed / failed / unverified] | Exact target metadata and native load observation |
| Native trigger | Each model-harness target cell | [passed / failed / unverified] | Representative query and native activation observation |

Discovery, installation, and identity evidence may be shared only when target
cells use the same package revision and harness. Load and trigger evidence stay
separate for `opus-5` and `sol-5.6`.

### TR-P1: Listing/native split

- Input: every listing-proxy query passes, but native trigger access is
  unavailable for one declared target.
- Expected transition: listing proxy is passed for that target and native
  trigger remains unverified. Overall status cannot claim native activation or
  behavioral compatibility for the missing cell.

### TR-P2: Waiver

- Input: the user explicitly waives the unavailable native check for shipment.
- Expected transition: shipment may proceed only as an unverified candidate.
  The waiver changes no evidence state, raises no label, and cannot support an
  unrelated instruction removal.

### TR-P3: Three-target split

- Input: a future declared set contains three target cells where native trigger
  passes in one, fails in one, and is unavailable in one.
- Expected transition: record passed, failed, and unverified separately. Do not
  collapse them into a harness-wide or cross-target pass.

## 2026-07-27 listing-proxy observations

Final listing at revision `c1ec71a` was judged in three fresh, tool-less
contexts per target. Each context saw the candidate name, final description,
and the unchanged twenty-query set above. This is listing-proxy evidence only.

Actual targets:

- `gpt-5.6-sol`, Codex CLI 0.145.0, high reasoning, ephemeral read-only
  execution with user config ignored. The colliding user-level
  `creating-portable-skills` path was disabled for these listing judgments.
- `claude-opus-5`, Claude Code 2.1.220, high effort, no session persistence,
  no tools, project setting source in an empty disposable repository.

### Should-trigger judgments

| Query | Sol 1/2/3 | Opus 1/2/3 | State |
| --- | --- | --- | --- |
| Help me create a new skill for formatting SQL queries | yes / yes / yes | yes / yes / yes | passed |
| I want to write an agent skill that enforces our commit message style | yes / yes / yes | yes / yes / yes | passed |
| Review my deploy-checks skill and tell me what's wrong with it | yes / yes / yes | yes / yes / yes | passed |
| Update the description on my notes skill so it triggers more reliably | yes / yes / yes | yes / yes / yes | passed |
| Port this skill from my old toolkit repo into this collection | yes / yes / yes | yes / yes / yes | passed |
| Migrate the data-validation skill over here and fix it up during the move | yes / yes / yes | yes / yes / yes | passed |
| My skill never fires when I ask about invoices — fix its triggers | yes / yes / yes | yes / yes / yes | passed |
| Turn this prompt I keep pasting into a proper reusable skill | yes / yes / yes | yes / yes / yes | passed |
| Is my skill's SKILL.md structured right? Audit it | yes / yes / yes | yes / yes / yes | passed |
| Make this skill work in Codex too, not just Claude Code | yes / yes / yes | yes / yes / yes | passed |

### Near-miss judgments

| Query | Sol 1/2/3 | Opus 1/2/3 | State |
| --- | --- | --- | --- |
| Design evals for my dataset | no / no / no | no / no / no | passed |
| Create a plugin for my editor that adds a slash command | no / no / no | no / no / no | passed |
| Review my README for clarity | no / no / no | no / no / no | passed |
| Build a grader and rubric for judging model outputs | no / no / no | no / no / no | passed |
| Help me write better prompts for my chatbot | no / no / no | no / no / no | passed |
| Set up an MCP server for our internal API | no / no / no | no / no / no | passed |
| Create a GitHub Action that lints markdown | no / no / no | no / no / no | passed |
| What skills should I install for web development? | no / no / no | no / no / no | passed |
| Summarize what this skill does | no / no / no | unsure / unsure / no | passed; no activation, with two borderline judgments recorded |
| Write documentation for our API endpoints | no / no / no | no / no / no | passed |

Every should-trigger received three of three `yes` judgments in both targets.
No near-miss received a `yes`. The listing proxy is **passed** for both target
cells; native discovery, loading, and triggering remain separate states in
`results.md`.

### Final evidence states

| Check | Codex / `gpt-5.6-sol` | Claude Code / `claude-opus-5` |
| --- | --- | --- |
| Structural validation | passed (shared final package) | passed (shared final package) |
| Listing proxy | passed | passed |
| Local-source install | passed | passed |
| Installed-content identity | passed | passed |
| Native discovery | passed | passed |
| Native load | passed | passed |
| Native trigger | passed | passed |

The detailed commands, paths, hashes, target configuration, and Claim Ceiling
are recorded in `results.md`. No proxy result was used to fill a native state.
