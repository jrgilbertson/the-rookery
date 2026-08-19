# Trigger contract: creating-portable-skills

Judged per the protocol in [`tests/README.md`](../README.md): fresh context,
name + description + query only, binary judgment, any near-miss `yes` fails.

## Should trigger

| Query | Reason |
| --- | --- |
| Help me create a new skill for formatting SQL queries | Explicit new-skill creation request. |
| I want to write a skill that enforces our commit message style | Authoring a new skill from a stated behavior. |
| Review my deploy-checks skill and tell me what's wrong with it | Review of an existing skill. |
| Update the description on my notes skill so it triggers more reliably | Description and trigger repair. |
| Port this skill from my old toolkit repo into this collection | Migration between collections. |
| Migrate the data-validation skill over here and fix it up during the move | Migration combined with repair. |
| My skill never fires when I ask about invoices — fix its triggers | Trigger-failure diagnosis on an existing skill. |
| Turn this prompt I keep pasting into a proper reusable skill | Converting a repeated prompt into a skill. |
| Is my skill's SKILL.md structured right? Audit it | Structural audit of a skill package. |
| Make this skill work in Codex too, not just Claude Code | Cross-harness portability request. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Design evals for my dataset | Standalone eval-suite design. |
| Create a plugin for my editor that adds a slash command | Plugin or editor-extension work. |
| Review my README for clarity | Prose review of a non-skill document. |
| Build a grader and rubric for judging model outputs | Eval and grading tooling. |
| Help me write better prompts for my chatbot | Prompt engineering without a skill package. |
| Set up an MCP server for our internal API | MCP or integration work. |
| Create a GitHub Action that lints markdown | CI automation. |
| What skills should I install for web development? | Skill discovery and installation. |
| Teach me a new skill in a role-playing game | General advice or game coaching, not skill-package work. |
| Summarize what this skill does | Explanation-only request. |
| Write documentation for our API endpoints | General documentation work. |
