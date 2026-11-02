# Skills

This file defines how this repository packages skills, evaluates them, and
records evidence. It follows the [Agent Skills standard](https://agentskills.io)
and adds vendor guidance. Where sources conflict, a **Conflict:** note names the
conflict and the choice made. The `creating-portable-skills` skill owns the
portable authoring workflow. This document owns the repository's package
conventions and evaluation workflow. It is not bundled with the skill.

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
tasks. Validate triggering through the evaluation workflow below.

## Evaluation workflow

Use the [evals plugin](https://github.com/ai-evals-course/evals-skills)'s
`evals-start` skill to choose the next evaluation step, then follow the targeted
skill it selects. When the specific evaluation job is already known, use that
targeted skill directly. Choose a runner for the actual need through that
workflow; this repository does not prescribe one.

Start with error analysis of observed system behavior and fix clear instruction
gaps first. A new skill does not require a corpus, grader, fixed case count, or
evaluation sign-off merely to be delivered. Invest in recurring evaluators when
a failure's consequence and likelihood of recurrence justify their cost.
Prefer a code check to a model judge.

When real traces are scarce, bounded synthetic discovery can reveal failures
by exercising the actual system. Synthetic examples can also target a rare
known failure; they do not establish its prevalence in real use. A precise
known constraint may justify a check before failure discovery. Keep useful
regression checks after a fix, and reduce or retire checks that no longer
provide enough signal for their cost.
[Hamel Husain and Shreya Shankar's evals FAQ](https://hamel.dev/blog/posts/evals-faq/)
explains these tradeoffs.

Record the exact skill revision, host, provider, inputs, and behavior observed
for each claim. Installation, native skill loading, input preservation, and
successful task completion are separate claims. Missing outputs, provider
errors, and unavailable observations remain unverified. Before trusting a
model judge, validate it against independent human judgments. Package checks
and apparent skill use do not establish behavioral quality.

Keep private logs, generated review pages, and raw run artifacts outside this
public repository. Any fixtures committed here must be synthetic and safe to
publish. Input and grading approval required by the selected workflow is
separate from authorization for model calls or other side effects. Use the
user's approved execution and budget limits before paid runs.

## Repository checks

Run `lefthook run pre-push --force` before shipping. The gate validates package
structure and catalog membership, repository text and links, secrets, and
deterministic tests of shipped helpers. See [TESTING.md](TESTING.md) and
[tests/README.md](tests/README.md) for the check commands and fixture boundaries.
Behavioral evaluation follows the workflow above; it is separate from these
code and package checks.

## Retiring a skill

Retire a skill in one pull request. Remove its package and dedicated tests,
record the removal in the changelog, and mark each `docs/solutions/` learning
about it as historical, naming what replaced it. In the same change, close or
re-scope its open issues so the tracker offers no work against a skill that no
longer exists.
