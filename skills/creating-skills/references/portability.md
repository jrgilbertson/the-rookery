# Portability map

The canonical SKILL.md carries only what every harness understands. Everything harness-specific is an optional adapter layered on top, never something the skill depends on to work.

## Portable core

Frontmatter fields defined by the [Agent Skills specification](https://agentskills.io/specification):

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | ≤64 chars; lowercase alphanumerics and hyphens, no leading/trailing/consecutive hyphens; must match the directory name |
| `description` | Yes | 1–1024 chars; what the skill does and when to use it |
| `license` | No | License covering the skill's contents |
| `compatibility` | No | ≤500 chars; real environment requirements only, and the spec notes most skills do not need it |
| `metadata` | No | Arbitrary string map for vendor extensions |

`allowed-tools` is in the spec but marked experimental, and support varies across harnesses ([spec](https://agentskills.io/specification)). Keep it out of canonical skills; a harness that wants tool pre-approval can add it to its own copy.

Any other field you see in the wild is vendor-specific. Claude Code, for example, extends the standard with invocation control, subagent execution, and dynamic context injection ([Claude Code skills docs](https://code.claude.com/docs/en/skills)). Those extensions belong in a harness-local copy, not the canonical skill.

## Adapter notes per harness

Each of these is optional. A canonical skill works on the harness without it; the adapter only improves the experience there.

### Anthropic / Claude Code

House rules from [Anthropic's skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

- Write the `description` in third person ("Processes Excel files..."). First or second person hurts discovery.
- Prefer gerund-form names (`processing-pdfs`, `writing-documentation`); avoid `helper`, `utils`, and vague names.
- The reserved words "anthropic" and "claude" are banned in `name`, and XML tags are not allowed.

These are good hygiene everywhere, so a canonical skill usually satisfies them already. Nothing extra is required for the skill to load in Claude Code.

### OpenAI / Codex

From the [Codex skills docs](https://developers.openai.com/codex/skills):

- An optional `agents/openai.yaml` beside SKILL.md adds display metadata (`display_name`, `short_description`, icons, `brand_color`, `default_prompt`), the `allow_implicit_invocation` policy (default true), and MCP dependency declarations. The skill works without it.
- The initial skill listing is budgeted at 2% of the model's context window or 8,000 characters, whichever is smaller. Over budget, descriptions get truncated or skills omitted. Front-load the key use case and trigger words so a shortened description still matches.
- Users can invoke a skill explicitly with `$skill-name` or browse with `/skills`.

## Discovery paths

Where each harness looks for installed skills. Note that `.agents/skills` is emerging as the cross-tool convention: native for Codex, an interoperable alias in Gemini CLI, and scanned by OpenCode.

| Harness | Project-level | User-level | Source |
|---|---|---|---|
| Claude Code | `.claude/skills/` (plus nested and parent directories) | `~/.claude/skills/` | [docs](https://code.claude.com/docs/en/skills) |
| OpenAI Codex | `.agents/skills/` (cwd, parents, repo root) | `~/.agents/skills/` | [docs](https://developers.openai.com/codex/skills) |
| Gemini CLI | `.gemini/skills/` and the `.agents/skills/` alias (alias wins) | `~/.gemini/skills/` and `~/.agents/skills/` | [docs](https://geminicli.com/docs/cli/skills/) |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | [docs](https://opencode.ai/docs/skills/) |
| Grok CLI | `.grok/skills/` (cwd, then repo root) | `~/.grok/skills/`, plus `~/.claude/skills/` for Claude compatibility | Bundled README at `~/.grok/README.md`, no public page found; verify your Grok version's skill directory |

Grok CLI's paths come from the README its installer places in the harness home, which also states that same-named skills deduplicate with higher-priority locations winning. That file ships with the CLI rather than a public site, so re-check it after upgrading.

## The rule

Adapters add convenience on exactly one harness. The canonical SKILL.md must work with none of them present: portable frontmatter only, and no body instruction that assumes a particular harness's tools, paths, or invocation syntax. If removing every adapter breaks the skill, the skill is not canonical yet.
