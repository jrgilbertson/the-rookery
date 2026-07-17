# Trigger query test: creating-portable-skills

Build 8-10 should-trigger phrasings (include non-obvious ones) and 8-10
near-misses. Run each query 3 times in a fresh agent context with the skill
installed.

Pass rule: each should-trigger query must activate in at least half its runs
(rate of at least 0.5 across the 3 runs — 2 of 3). ANY near-miss activation
fails the whole set.

Date: 2026-07-16 | Harness: Claude Code subagents (fresh context per judge) | Model: three families — Haiku 4.5, Sonnet, Fable 5

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
skill — never by summarizing the workflow. A description that summarizes the
steps makes agents follow the summary and skip the body. After tuning,
re-run the full set.
