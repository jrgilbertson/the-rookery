# Trigger query test: creating-skills

Build 8-10 should-trigger phrasings (include non-obvious ones) and 8-10
near-misses. Run each query 3 times in a fresh agent context with the skill
installed.

Pass rule: each should-trigger query must activate in at least half its runs
(rate of at least 0.5 across the 3 runs — 2 of 3). ANY near-miss activation
fails the whole set.

Date: [YYYY-MM-DD] | Harness: [name] | Model: [name]

## Should-trigger queries

| Query | Run 1 | Run 2 | Run 3 | Rate |
| --- | --- | --- | --- | --- |
| Help me create a new skill for formatting SQL queries | | | | |
| I want to write an agent skill that enforces our commit message style | | | | |
| Review my deploy-checks skill and tell me what's wrong with it | | | | |
| Update the description on my notes skill so it triggers more reliably | | | | |
| Port this skill from my old toolkit repo into this collection | | | | |
| Migrate the data-validation skill over here and fix it up during the move | | | | |
| My skill never fires when I ask about invoices — fix its triggers | | | | |
| Turn this prompt I keep pasting into a proper reusable skill | | | | |
| Is my skill's SKILL.md structured right? Audit it | | | | |
| Make this skill work in Codex too, not just Claude Code | | | | |

## Near-miss queries (expected: no trigger)

| Query | Expected | Run 1 | Run 2 | Run 3 |
| --- | --- | --- | --- | --- |
| Design evals for my dataset | no trigger | | | |
| Create a plugin for my editor that adds a slash command | no trigger | | | |
| Review my README for clarity | no trigger | | | |
| Build a grader and rubric for judging model outputs | no trigger | | | |
| Help me write better prompts for my chatbot | no trigger | | | |
| Set up an MCP server for our internal API | no trigger | | | |
| Create a GitHub Action that lints markdown | no trigger | | | |
| What skills should I install for web development? | no trigger | | | |
| Summarize what this skill does | no trigger | | | |
| Write documentation for our API endpoints | no trigger | | | |

## Tuning

Fix failures by front-loading trigger words and describing when to use the
skill — never by summarizing the workflow. A description that summarizes the
steps makes agents follow the summary and skip the body. After tuning,
re-run the full set.
