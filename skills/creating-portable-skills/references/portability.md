# Portability Map

Portability here means a canonical, self-contained Agent Skills package that compatible harnesses can discover and install. It does not promise equivalent behavior across every model, harness, configuration, or task. Behavioral claims require evidence from the exact models, harnesses, and cases they name.

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
| Trigger-suite judgments pass | A listing proxy for the name-and-description routing contract | Native triggering in a harness |
| A smoke check passes | That package revision installed and activated in that harness, on that query | Other harnesses, queries, or task behavior |
| Graded behavioral cases pass | Those cases, in those contexts, at that revision | Reliability, non-regression, causal improvement, or universal compatibility |

The baseline comparison template owns case construction and grading; the
trigger contract owns the query set and smoke-check protocol.

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

A harness may discover the same skill name in several locations with
version-specific precedence. Before recording native load or trigger evidence,
inventory every applicable location. A native load pass requires deterministic
runtime provenance tied to the installed source: a native trace naming the
exact installed path or base directory, or equivalent runtime evidence linked
to the installed content hash. Distinctive output may corroborate that
provenance, but cannot independently prove which copy loaded. If deterministic
runtime provenance is unavailable, keep native load unverified rather than
failed. Native trigger for the declared package revision is also unverified
when loaded-copy identity is unverified; record an unattributed invocation only
as an observation. Record source-to-install identity, native discovery, native
load, native trigger, and behavioral evidence separately.

| Harness | Project-level | User-level | Source |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | [docs](https://code.claude.com/docs/en/skills) |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` | [docs](https://developers.openai.com/codex/skills) |
| Gemini CLI | `.gemini/skills/` and `.agents/skills/` | `~/.gemini/skills/` and `~/.agents/skills/` | [docs](https://geminicli.com/docs/cli/skills/) |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | [docs](https://opencode.ai/docs/skills/) |
| Grok CLI | `.grok/skills/` | `~/.grok/skills/` and `~/.claude/skills/` | Confirm with the README bundled by the installed CLI |

## Rule

A canonical package passes without optional harness metadata. Structural validation establishes canonical form; a passing smoke check establishes installability and activation only for that harness. Describe behavioral support only at the evidence level earned by separately graded cases.
