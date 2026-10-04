# Skills

This file is this repository's convention for writing, evaluating, and
recording evidence for agent skills. It builds on the
[Agent Skills standard](https://agentskills.io), with vendor guidance layered
on top. Where sources conflict, a **Conflict:** note names the conflict and
the choice made. The `creating-portable-skills` skill owns the portable
authoring workflow. This host document owns repository package conventions
and the evaluation workflow; it is not bundled with the skill.

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
then follow the skill it selects. Ground cases in observed failures from local
session logs and prior issues. Claude, Codex, and Grok are the primary hosts;
record which host a result covers rather than treating one host's success as
proof for all three.

`creating-portable-skills` is the first dogfood for this workflow. Its
[bounded replacement suite](tests/creating-portable-skills/README.md) targets
Claude and Codex with activation cases, a read-only portability audit, manual
Claude trace review, automated Codex capture checks and provisional criterion
judges. Independent human calibration
is still required to claim judge alignment; a direct-tool Codex result does not
validate default Code Mode. The other skill packages remain
available and await revalidation in turn. Passing repository
checks does not establish behavioral quality.

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
