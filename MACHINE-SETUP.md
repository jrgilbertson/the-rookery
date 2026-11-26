# Machine setup

The global agent instructions, skills, plugins, and MCP servers I set up on
every machine. The install commands below use each source's current version.

## Global agent instructions

Keep one canonical global instructions file on each machine (for example,
`~/.codex/AGENTS.md`) and point every harness you use to it, so changes stay in
one place instead of drifting across tools. [GLOBAL-AGENTS.md](GLOBAL-AGENTS.md)
is a published reference copy; agents in this repository do not load it
directly.

| Harness | Global instructions path | How to connect |
|---|---|---|
| Codex | `~/.codex/AGENTS.md` | Canonical file (or symlink to it) |
| Claude Code | `~/.claude/CLAUDE.md` | Single `@~/.codex/AGENTS.md` import line (or symlink) |
| Antigravity | `~/.gemini/config/AGENTS.md` | Symlink to the canonical file |
| Grok | `~/.grok/AGENTS.md` | Symlink to the canonical file |
| Cursor | `~/.cursor/rules/global-agents.mdc` | `.mdc` rule with `alwaysApply: true` YAML frontmatter (sync or wrap the canonical file) |

## Install with the skills CLI

Each line installs the listed skills from one source for the whole machine.

```bash
npx skills add ai-evals-course/evals-skills -g -y --skill build-review-interface error-discovery eval-audit evals-start evaluate-rag generate-synthetic-data validate-evaluator write-code-eval write-judge-prompt
npx skills add cathrynlavery/diagram-design -g -y --skill diagram-design
npx skills add emilkowalski/skills -g -y --skill break-ui mobile-native
npx skills add github/gh-stack -g -y --skill gh-stack
npx skills add GoogleChrome/modern-web-guidance -g -y --skill modern-web-guidance
npx skills add harshaneel/humanize -g -y --skill ai-check
npx skills add https://docs.stripe.com -g -y --skill connect-recommend connect-required-verification-information metronome stripe-apps stripe-best-practices stripe-directory stripe-docs stripe-implementation-planner stripe-pay stripe-projects
npx skills add jrgilbertson/networked-thinking-skills -g -y --skill atomic-note atomic-note-audit managing-obsidian-tasks
npx skills add jrgilbertson/the-rookery -g -y --skill checking-skill-portability coordinating-work daily-learning managing-issues managing-personal-crm personal-chief-of-staff repo-captain reviewing-meetings reviewing-prs storm-research
npx skills add livekit/agent-skills -g -y --skill building-livekit-agents debugging-livekit-agents operating-livekit-agents reading-livekit-docs running-livekit-simulations testing-livekit-agents writing-livekit-scenarios
npx skills add mattpocock/skills -g -y --skill codebase-design domain-modeling grill-me grill-with-docs grilling improve-codebase-architecture setup-matt-pocock-skills writing-for-agents
npx skills add millionco/react-doctor -g -y --skill react-doctor
npx skills add morluto/rea -g -y --skill reverse-engineer-anything
npx skills add mvanhorn/cli-printing-press -g -y --skill printing-press printing-press-amend printing-press-import printing-press-output-review printing-press-polish printing-press-publish printing-press-reprint printing-press-retro printing-press-score
npx skills add mvanhorn/last30days-skill -g -y --skill last30days
npx skills add obsidianmd/obsidian-skills -g -y --skill defuddle json-canvas knap obsidian-bases obsidian-cli obsidian-headless obsidian-markdown
npx skills add shadcn/improve -g -y --skill improve
npx skills add tmchow/illo-skill -g -y --skill illo
npx skills add vercel-labs/agent-skills -g -y --skill vercel-react-best-practices
npx skills add vercel-labs/skills -g -y --skill find-skills
npx skills add wheresryan22/anatomy -g -y --skill anatomy
```

Modern Web Guidance sends anonymous usage telemetry, including the search
queries agents write. These machines accept it. Its only switch,
`DISABLE_TELEMETRY=1`, also turns off Claude Code's feature flags, which
`/skill-doctor` needs.

## Impeccable

[Impeccable](https://github.com/pbakaus/impeccable) has its own installer and
updater:

```bash
npx impeccable install --global
npx impeccable update --global
```

## Claude Code plugins

Add the Compound Engineering marketplace. The official marketplace is built
into Claude Code. These commands install the plugins in user scope.

```bash
claude plugin marketplace add EveryInc/compound-engineering-plugin
claude plugin install compound-engineering@compound-engineering-plugin
claude plugin install playwright@claude-plugins-official
claude plugin install pyright-lsp@claude-plugins-official
claude plugin install security-guidance@claude-plugins-official
claude plugin install supabase@claude-plugins-official
claude plugin install typescript-lsp@claude-plugins-official
claude plugin install vercel@claude-plugins-official
```

## Codex plugins

```bash
codex plugin marketplace add EveryInc/compound-engineering-plugin
codex plugin marketplace add PostHog/ai-plugin
codex plugin add compound-engineering@compound-engineering-plugin
codex plugin add posthog@posthog
```

## Antigravity plugins

Antigravity (`agy plugin`) has no built-in `update` command or marketplace
auto-update, so a standalone install stays pinned at the version cloned at
install time and can silently drift behind Claude Code.

On machines with Claude Code, symlink Antigravity's Compound Engineering plugin
to Claude Code's auto-updating marketplace checkout, which ships a root-native
`plugin.json` and `skills/` bundle that passes `agy plugin validate`. If you
previously installed a standalone copy, run
`agy plugin uninstall compound-engineering` first so `ln -s` does not place the
symlink inside the existing directory.

```bash
mkdir -p ~/.gemini/config/plugins
ln -s ~/.claude/plugins/marketplaces/compound-engineering-plugin ~/.gemini/config/plugins/compound-engineering
agy plugin validate ~/.gemini/config/plugins/compound-engineering
```

On machines without Claude Code, install the standalone copy directly and
reinstall (`agy plugin uninstall compound-engineering`, then install again)
when you want to update:

```bash
agy plugin install https://github.com/EveryInc/compound-engineering-plugin
```

## Claude Code MCP servers

Run these in addition to installing the plugins, which register their bundled
servers. The stdio commands require `npx` and `uvx`.

Linear and PostHog are left out on purpose. Claude Code gets both from the
claude.ai account's connectors, which sign in once for every machine, so a
Linear plugin or a user-scope PostHog server here would load the same tools a
second time.

```bash
claude mcp add --scope user --transport http ai-elements https://registry.ai-sdk.dev/api/mcp
claude mcp add --scope user --transport http livekit-docs https://docs.livekit.io/mcp
claude mcp add --scope user --transport stdio shadcn -- npx shadcn@latest mcp
claude mcp add --scope user --transport stdio gemini-docs -- uvx --from git+https://github.com/philschmid/gemini-api-docs-mcp gemini-docs-mcp
```

## Codex MCP servers

Linear, Supabase, and Vercel are left out on purpose. Codex gets them from the
apps linked to the ChatGPT account, which follow the account to Codex desktop
and the CLI.

```bash
codex mcp add ai-elements --url https://registry.ai-sdk.dev/api/mcp
codex mcp add gemini-docs -- uvx --from git+https://github.com/philschmid/gemini-api-docs-mcp gemini-docs-mcp
codex mcp add livekit-docs --url https://docs.livekit.io/mcp
codex mcp add posthog --url https://mcp.posthog.com/mcp
codex mcp add shadcn -- npx shadcn@latest mcp
codex mcp add lennysdata --url https://mcp.lennysdata.com/mcp
codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp
codex mcp add playwright -- npx @playwright/mcp@latest
```

## Check a machine against this list

Run this from the repository root with Python 3.9 or later and the harness CLIs
(`claude`, `codex`, and `agy`). It prints nothing when all listed skills,
plugins, and MCP servers are present, Antigravity's Compound Engineering plugin
matches Claude Code's installed version, and there are no extra skills managed
by the skills CLI or extra enabled Claude Code user plugins. Global agent
instructions above are not checked by this script. Additional Codex plugins and
MCP servers, and additional Antigravity plugins, can come from the harness or
local configuration. The check compares names without starting MCP servers. It
also checks for `SKILL.md` in the Codex, Claude Code, and Antigravity global
skill directories for listed skills in the lock and for Impeccable.

```bash
python3 - <<'PYTHON'
import json
import os
from pathlib import Path
import subprocess

home = Path.home()
lines = Path("MACHINE-SETUP.md").read_text().splitlines()

def documented(prefix):
    return [line.removeprefix(prefix).split() for line in lines if line.startswith(prefix)]

def config_json(path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return {}

def cli_json(*command):
    return json.loads(subprocess.check_output(command))

def report(label, expected, installed, *, show_extra=False):
    for name in sorted(expected - installed):
        print(f"Missing {label}: {name}")
    if show_extra:
        for name in sorted(installed - expected):
            print(f"Unlisted {label}: {name}")

xdg_state_home = os.environ.get("XDG_STATE_HOME")
skill_lock_dir = Path(xdg_state_home) / "skills" if xdg_state_home else home / ".agents"
skill_lock = config_json(skill_lock_dir / ".skill-lock.json")
claude_config = config_json(home / ".claude.json")
claude_plugins = cli_json("claude", "plugin", "list", "--json")
codex_plugins = cli_json("codex", "plugin", "list", "--json")["installed"]
agy_plugins = cli_json("agy", "plugin", "list", "--json")
codex_servers = cli_json("codex", "mcp", "list", "--json")

expected_skills = {name for args in documented("npx skills add ")
                   for name in args[args.index("--skill") + 1:]}
locked_skills = set(skill_lock.get("skills", {}))
report("skill", expected_skills, locked_skills, show_extra=True)

skills_to_check = (expected_skills & locked_skills) | {"impeccable"}
for harness, skill_dir in (("Codex", ".agents/skills"), ("Claude Code", ".claude/skills"), ("Antigravity", ".gemini/config/skills")):
    present = {name for name in skills_to_check
               if (home / skill_dir / name / "SKILL.md").is_file()}
    report(f"{harness} skill", skills_to_check, present)

claude_user_plugins = {
    p["id"]: p for p in claude_plugins if p["scope"] == "user" and p["enabled"]
}
agy_enabled_plugins = {
    p["name"]: p for p in agy_plugins if p.get("enabled")
}

report("Claude Code plugin", {args[0] for args in documented("claude plugin install ")},
       set(claude_user_plugins), show_extra=True)
report("Codex plugin", {args[0] for args in documented("codex plugin add ")},
       {p["pluginId"] for p in codex_plugins if p["enabled"]})
report("Antigravity plugin", {"compound-engineering"}, set(agy_enabled_plugins))

claude_ce = claude_user_plugins.get("compound-engineering@compound-engineering-plugin")
agy_ce = agy_enabled_plugins.get("compound-engineering")
if claude_ce and agy_ce:
    agy_version = agy_ce.get("version")
    claude_version = claude_ce.get("version")
    if not agy_version or not claude_version or agy_version != claude_version:
        print(
            f"Antigravity plugin version mismatch: compound-engineering "
            f"({agy_version or 'unknown'}) != Claude Code ({claude_version or 'unknown'})"
        )

report("Claude Code MCP server",
       {args[1] for args in documented("claude mcp add --scope user --transport ")},
       set(claude_config.get("mcpServers", {})))
report("Codex MCP server", {args[0] for args in documented("codex mcp add ")},
       {server["name"] for server in codex_servers if server["enabled"]})
PYTHON
```
