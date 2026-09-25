# Portability Map

Portability here means a canonical, self-contained skill package that compatible harnesses can discover and install. Behavioral claims require evidence from the exact models, harnesses, and cases they name.

## Canonical structure

The frontmatter fields, their limits, and the Codex validator's conflict over `compatibility` are in the **Package format** section of [skills.md](skills.md). The **canonical-package rule** is stricter than that table: canonical packages leave out `allowed-tools`, and a harness-local copy may add tool pre-approval when needed.

## Structural checks and behavioral evidence

Keep these conclusions separate:

| Observation | Supports | Does not support by itself |
| --- | --- | --- |
| Structural validation passes | The package follows the checked schema | Discovery, installation, triggering, or useful execution |
| Trigger-suite judgments pass | A listing proxy for the name-and-description routing contract | Native triggering in a harness |
| A smoke check passes | That package revision installed and activated in that harness, on that query | Other harnesses, queries, or task behavior |
| Graded behavioral cases pass | Those cases, in those contexts, at that revision | Reliability, non-regression, causal improvement, or universal compatibility |

## Optional harness metadata

The canonical package works without vendor extensions, apart from a harness file that the **Package format** section of [skills.md](skills.md) admits. A harness-local copy may add optional metadata supported by that harness.

### Claude Code

Claude Code supports additional invocation controls, subagent execution, and dynamic context injection described in its [skills documentation](https://code.claude.com/docs/en/skills). Keep those fields out of the canonical package unless they fit under portable `metadata` without becoming a runtime dependency.

Its authoring guidance favors gerund-form names, reserves `anthropic` and `claude` in names, and disallows XML tags in the name and description. These conventions are safe hygiene when they do not conflict with the host collection. Its third-person description voice yields to the imperative voice chosen in **Descriptions and triggering** of [skills.md](skills.md).

### OpenAI Codex

The [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills) describes optional display metadata and invocation policy in `agents/openai.yaml`. That file stays out of the canonical package unless the skill needs a capability only Codex provides.

## Discovery paths

Use the host repository's documented path first. These are common project and user locations; confirm the installed harness version before relying on them.

| Harness | Project-level | User-level | Source |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | [docs](https://code.claude.com/docs/en/skills) |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` | [docs](https://learn.chatgpt.com/docs/build-skills) |
| Gemini CLI | `.gemini/skills/` and `.agents/skills/` | `~/.gemini/skills/` and `~/.agents/skills/` | [docs](https://geminicli.com/docs/cli/skills/) |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | [docs](https://opencode.ai/docs/skills/) |
| Grok CLI | `.grok/skills/` | `~/.grok/skills/` and `~/.claude/skills/` | Confirm with the README bundled by the installed CLI |
