# Skills

This file defines how this repository packages skills, evaluates them, and
records evidence. It follows the [Agent Skills standard](https://agentskills.io)
and adds vendor guidance. Where sources conflict, a **Conflict:** note names the
conflict and the choice made. This document owns the repository's package
conventions, evaluation policy, and evidence rules. It is not bundled with any
skill.

## Tools

| Tool | What it does | When |
| --- | --- | --- |
| `anthropic-skills:skill-creator` (Claude Code) | Drafts a package, runs test requests with and without it, compares two versions blind, and tunes the description | Creating or substantially revising a skill |
| [`checking-skill-portability`](skills/checking-skill-portability/SKILL.md) | Validates the package against the standard and finds anything tied to one harness or one machine | Every change, before it ships |
| `/doctor prompt-audit` (Claude Code) | Reads instruction files, skills, and agents for patterns written for older models, dead references, and contradictions | When a model changes |
| `/skill-doctor` (Claude Code) | Reports each skill's listing cost and use | When a model changes, or when pruning |
| [Promptfoo](https://www.promptfoo.dev) | Runs Eval Cases on Claude and Codex, with and without a skill, and checks each result | The runner for Skill Evals; [`evals/managing-issues/`](evals/managing-issues/README.md) shows the setup |

`/skill-doctor` needs Claude Code's feature flags, which
`DISABLE_TELEMETRY=1` turns off. Its use counts include skills that were only
loaded, and they miss skills run through a CLI, so read "never used" as a lead
to check. The `/claude-api` commands `build-eval`, `hillclimb`, and
`cost-optimize` target apps that call the Claude API, not skill packages.

## Creating a skill

The model test runs in this section are part of authoring, so ask for approval
to run them when the work starts, or name the approval in the brief. If approval
is missing, stop and ask; never skip the runs silently.

First check that a skill is needed. An installed skill, a plugin, or the model
on its own may already do the job. Run two or three realistic requests without
a skill and note what goes wrong or is missing. If nothing does, stop.

Otherwise build the skill in Claude Code with `anthropic-skills:skill-creator`
(switch to or delegate to Claude Code when working from a harness that does not
have it, such as Antigravity):

- **Claude Code:** `anthropic-skills:skill-creator`, which claude.ai syncs and
  keeps current. The copy in `anthropics/skills` on GitHub is older, so do not
  install it with `npx skills add`.
- **Codex (if used instead):** the built-in `skill-creator`, which updates with
  `codex-cli`. Its starter adds `agents/openai.yaml`; keep that file out of the
  canonical package as the package format below requires.

Then:

1. **Draft** the smallest `SKILL.md` that closes the gaps you saw.
2. **Test it on realistic requests.** Use those requests plus one ambiguous
   or edge request, three to five in all. Run each one twice, in a fresh
   context each time: once with the skill and once without it. The run
   without it is the no-skill Baseline. Read the outputs and transcripts
   yourself. Name each failure in plain words before writing any check.
3. **Check with code only what code can decide**, such as a file written or a
   command run. Judge tone and reasoning by reading. Use the creator's blind
   comparison only to choose between two versions.
4. **Tune the description** with a few requests that should trigger the skill
   and a few near misses that should not.
5. **Check portability.** Run `checking-skill-portability`, then run one test
   request in Codex and in any other harness or model the skill must serve.
6. **Keep the Eval Cases.** Move the test requests and their checks to
   `evals/<skill>/`, outside the package, as a Promptfoo suite laid out like
   [`evals/managing-issues/`](evals/managing-issues/README.md). They become
   the skill's Skill Eval, which runs again when a model changes.
   Drop an Eval Case that passes with and without the skill, because it
   measures nothing. Eval Cases in this public repository must be synthetic
   and safe to publish.

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

When a routing failure has been observed, check the description change against
the requests that misrouted, as described under improving from real use below.

## Improving from real use

After a skill ships, improve it from real use and demonstrated failures. The
first time a failure appears, fix the instruction and say what was observed in
the fix's commit message. Add an Eval Case to the skill's Skill Eval only when
the same failure returns after that fix. Check observable behavior, never
wording, headings, or text patterns. Correct one failure with a narrow fix
rather than a universal requirement.

When a wrong run of the skill would be costly, such as one that merges,
deletes, spends, or sends, run a forward test: give a fresh agent a realistic
request and the skill, without the expected answer, in a disposable workspace,
then read what it did. One forward test inside the current session with no
outside effects needs no separate approval. A batch of runs, a run billed per
call, or a run against a live system needs the skill owner's approval first.

### Evidence integrity

Inspect outputs directly. A judgment cites evidence for the outcome rather than
a heading or claimed filename. An Eval Case names the observed failure it came
from; one that cannot is a finding.

## Skill Evals

Tests never call a model; evals always do. The repository gate runs only
tests, so it never spends money on a model. A Skill Eval calls a model on
every Eval Case, so it runs when a skill is created or revised and when a
model changes, never on every pull request. The Rookery ships no AI feature,
so it has no Product Evals. [CONCEPTS.md](CONCEPTS.md#evaluation) defines the
eval terms.

Each skill's Skill Eval lives in `evals/<skill>/` at the repository root,
outside the skill package. That directory holds the skill's Eval Cases and the
Eval Records of their runs. Create it when the skill gets its first Eval Case.

### Eval Records

Commit an Eval Record for every run. Each record holds:

- The model ID and effort for the agent, and for any judge model
- The skill revision, as a commit
- The Eval Case IDs and a hash of the case set
- The Baseline arm: no skill, the previous version of the skill, or the
  previous model
- The date
- The runner's name and version
- The number of repeats, and whether the run finished
- Tokens and cost
- Each Eval Label, with its reason and its labeler, a person or a model
- The full transcript, saved beside the record

Raw runner output and caches stay local and never enter the repository.

### Evidence rules

- Record the exact skill revision, host, provider, inputs, and behavior
  observed for each claim.
- Run Eval Cases with synthetic inputs and sources.
- Read the full transcript, including tool results and session context, and
  check that the Eval Record contains no private data before committing it.
- Keep real-use traces, private logs, and generated review pages outside this
  public repository. Several skills read personal data. When a real-use
  failure qualifies as an Eval Case, rebuild it with invented data, then
  commit the synthetic Eval Case and its Eval Record.
- Use the user's approved execution and budget limits before paid runs.

## When a model changes

When a new model becomes the default in either harness:

1. Read the vendor's guide for the model, such as Anthropic's
   [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)
   or OpenAI's [latest-model guide](https://developers.openai.com/api/docs/guides/latest-model).
2. Run each skill's Eval Cases on the new model before editing anything, with
   the effort level set explicitly. Compare the result with the last Eval
   Record on the previous model, which is its Baseline. This run then becomes
   the Baseline for every fix that follows.
3. Run `/doctor prompt-audit` in Claude Code. Codex has no equivalent, so
   review the corpus against OpenAI's guide by hand.
4. Run `/skill-doctor` to see what the always-loaded skill listing costs.
5. Fix one kind of problem at a time, rerun the Eval Cases, and keep what
   holds up.
   Tuning specific to one model or vendor belongs in that harness's global
   instructions, not in a portable skill.
6. Run `checking-skill-portability` on each changed skill, and record what
   changed in the changelog.

If skills stall, halt early, or skip steps after an upgrade and the cause is
unclear, Compound Engineering's `ce-retune` runs a measured retune. It needs a
run archive and many paid runs, so it needs approval like any batch run.

## Repository checks

Run `lefthook run pre-push --force` before shipping. The gate validates package
structure and catalog membership, repository text and links, secrets, and
deterministic tests of shipped helpers. See [TESTING.md](TESTING.md) and
[tests/README.md](tests/README.md) for the check commands and fixture boundaries.
The gate never runs Skill Evals, because tests never call a model. Skill Evals
follow the [Skill Evals](#skill-evals) section instead.

## Retiring a skill

Retire a skill in one pull request. Remove its package, its dedicated tests,
and its Skill Eval in `evals/<skill>/`, record the removal in the changelog,
and mark each `docs/solutions/` learning about it as historical, naming what
replaced it. In the same change, close or
re-scope its open issues so the tracker offers no work against a skill that no
longer exists. Afterward, uninstall the skill from each host where it was
installed, such as with `npx skills remove <name>`, so no agent keeps loading a
retired copy.
