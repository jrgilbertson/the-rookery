# Skills

This file defines how this repository packages skills, evaluates them, and
records evidence. It follows the [Agent Skills standard](https://agentskills.io)
and adds vendor guidance. Where sources conflict, a **Conflict:** note names the
conflict and the choice made. The `creating-portable-skills` skill owns the
portable authoring workflow and evaluation policy. This document owns the
repository's package conventions and evidence rules. It is not bundled with the
skill.

## Package format

A skill is a directory that holds a `SKILL.md` file and, optionally,
`scripts/`, `references/`, and `assets/`. `SKILL.md` starts with YAML
frontmatter and continues with a Markdown body.

| Field | Required | Rule |
| --- | --- | --- |
| `name` | Yes | 1–64 lowercase letters, digits, and hyphens; no leading, trailing, or doubled hyphen; equals the directory name |
| `description` | Yes | 1–1024 characters; see the [description field](https://agentskills.io/specification#description-field) |
| `license` | No | Text |
| `compatibility` | No | At most 500 characters; real environment requirements only |
| `metadata` | No | Map of string keys to string values |
| `allowed-tools` | No | Experimental; support varies by harness. This repository rejects it: `CANONICAL_FIELDS` in `scripts/checks/skill_packages.rb` omits it |

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

Validate triggering through the evaluation workflow below.

## Evaluation workflow

[`references/evaluation.md`](skills/creating-portable-skills/references/evaluation.md)
in `creating-portable-skills` owns evaluation policy and routing. This
repository adds these evidence rules:

- Record the exact skill revision, host, provider, inputs, and behavior
  observed for each claim.
- Keep private logs, generated review pages, and raw run artifacts outside this
  public repository. Any fixtures committed here must be synthetic and safe to
  publish.
- Use the user's approved execution and budget limits before paid runs.

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
longer exists. Afterward, uninstall the skill from each host where it was
installed, such as with `npx skills remove <name>`, so no agent keeps loading a
retired copy.
