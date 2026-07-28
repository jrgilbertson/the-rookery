# Portability Map

Portability here means a canonical, self-contained Agent Skills package that compatible harnesses can discover and install. It does not promise equivalent behavior across every model, harness, configuration, or task. Behavioral claims require evidence from the exact declared target cells and cases they name.

## Canonical structure

Frontmatter fields used by this skill collection from the [Agent Skills specification](https://agentskills.io/specification):

| Field | Required | Constraints |
| --- | --- | --- |
| `name` | Yes | At most 64 characters; lowercase alphanumerics and hyphens, no leading, trailing, or consecutive hyphens; matches the directory name |
| `description` | Yes | 1 to 1024 characters; states what the skill does and when to use it |
| `license` | No | Covers the skill's contents |
| `compatibility` | No | At most 500 characters; real environment requirements only |
| `metadata` | No | String map for optional metadata |

`allowed-tools` is experimental in the specification and support varies. Keep it out of the canonical package; tool pre-approval can be added to a harness-local copy when needed.

The package may contain `references/`, `assets/`, and `scripts/`, but every referenced resource must resolve inside the skill directory. Canonical instructions use capabilities rather than assuming proprietary tools, private paths, or owner-specific configuration.

## Structural checks and behavioral evidence

Keep these conclusions separate:

| Observation | Supports | Does not support by itself |
| --- | --- | --- |
| Structural validation passes | The package follows the checked Agent Skills schema | Discovery, installation, triggering, or useful execution |
| Local-source installation and content identity pass | That exact package revision installed in the named harness | Load, trigger, or behavior in another target |
| Native discovery and load pass | The named harness exposed the installed skill to the named model cell | Correct activation or task behavior |
| Listing judgment passes | A proxy judgment of the name-and-description routing contract | Native triggering |
| Native trigger is observed | Triggering in that exact model-harness configuration and query | Other configurations, queries, or equivalent downstream behavior |
| A small matched comparison passes | The bounded conclusion in its completed baseline record | Reliability, non-regression, causal improvement, or universal compatibility |

Use the model and harness target set declared in the completed baseline record.
That record owns case construction and per-target observation handling.

## Optional harness metadata

The canonical package must not require vendor extensions. A harness-local copy may add optional metadata supported by that harness, but resulting claims stay scoped to observed checks.

### Claude Code

Claude Code supports additional invocation controls, subagent execution, and dynamic context injection described in its [skills documentation](https://code.claude.com/docs/en/skills). Keep those fields out of the canonical package unless they fit under portable `metadata` without becoming a runtime dependency.

Its authoring guidance favors third-person descriptions and gerund-form names, reserves `anthropic` and `claude` in names, and disallows XML tags. These conventions are safe hygiene when they do not conflict with the host collection.

### OpenAI Codex

The [Codex skills documentation](https://developers.openai.com/codex/skills) describes optional display metadata and invocation policy in `agents/openai.yaml`. The package must remain usable without that file.

Codex budgets the initial skill listing, so put the key use case and trigger words early in the description. Users may also invoke skills explicitly.

## Discovery paths

Use the host repository's documented path first. These are common project and user locations; confirm the installed harness version before relying on them.

| Harness | Project-level | User-level | Source |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | [docs](https://code.claude.com/docs/en/skills) |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` | [docs](https://developers.openai.com/codex/skills) |
| Gemini CLI | `.gemini/skills/` and `.agents/skills/` | `~/.gemini/skills/` and `~/.agents/skills/` | [docs](https://geminicli.com/docs/cli/skills/) |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | [docs](https://opencode.ai/docs/skills/) |
| Grok CLI | `.grok/skills/` | `~/.grok/skills/` and `~/.claude/skills/` | Confirm with the README bundled by the installed CLI |

## Rule

A canonical package passes without optional harness metadata. Structural validation establishes canonical form; a clean local-source install establishes installability only for the checked package-harness cell. Describe behavioral support only at the evidence level earned by separately recorded model-harness cases.
