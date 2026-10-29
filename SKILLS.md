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

Use the evals plugin's `evals-start` skill to choose the next evaluation step,
then follow the skill it selects. Start with error analysis: build a case only
from a specific failure observed in real use, such as local session logs and
prior issues, and only when it persists after fixing the skill's instructions.
Prefer a code check to a model judge, and retire a case that stops catching
anything. [Hamel Husain's evals FAQ](https://hamel.dev/blog/posts/evals-faq/)
explains the reasoning. Claude, Codex, and Grok are the primary hosts; record
which host a result covers rather than treating one host's success as proof
for all three.

The [`creating-portable-skills` harness](tests/creating-portable-skills/README.md)
prepares one case at a time for Claude and Codex through Promptfoo's native
providers. It has no committed cases. The providers' built-in assertions check
final answers and observations of skill use. The Codex SDK detects skill paths
heuristically. That detection does not prove which skill was loaded or that
every required file was read. An optional deterministic check confirms that
supplied input files stay unchanged. Missing answers, provider errors, and
unavailable file snapshots do not pass. Strict capture is not collected and
remains Unmeasured. Before claiming that a model judge agrees with human
reviewers, independently calibrate it against human judgments. Passing
repository checks does not establish behavioral quality.

The previous behavioral suites, benchmarks, custom runners, review server,
cost tools, and eval schemas have been retired. Committed versions remain
available in Git history. This repository no longer prescribes their formats
or requires their tooling. Follow the selected evaluation skill when designing
cases, collecting human feedback, and validating evaluators. Do not treat the
retired suite's scores as validation of a replacement suite.

Keep private logs, generated review pages, and raw run artifacts outside this
public repository. Any fixtures committed here must be synthetic and safe to
publish. Use the user's approved execution and budget limits before paid runs.

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
