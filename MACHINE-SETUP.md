# Machine setup

This file documents my full personal machine manifest: the global agent
instructions, ~80 skills, plugins, MCP servers, and three-harness
(`claude`, `codex`, and `agy`) verification script I keep in sync across my
machines. If you want a minimal single-harness setup with only the Rookery
skills you need, start with [README.md#install](README.md#install) instead.

The install commands below use each source's current version.

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
npx skills add jrgilbertson/the-rookery -g -y --skill active-learning checking-skill-portability managing-issues managing-personal-crm personal-chief-of-staff repo-captain reviewing-meetings reviewing-prs storm-research
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
queries agents write. I leave telemetry on. Its only switch,
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

The two language server plugins only connect Claude Code to a language server.
They do nothing until the servers themselves are on the `PATH`, so install
those too. The prefix puts them in a folder that is already on the `PATH` and
does not change when the Node version does.

```bash
npm install -g --prefix ~/.local typescript-language-server typescript pyright
```

## Codex plugins

PostHog's `posthog@posthog` plugin (`PostHog/ai-plugin`) is left out on purpose.
It bundles a local shell hook whose content hash drifts whenever Codex refreshes
its plugin cache, stalling headless Codex workers on startup for hook review.
Codex connects to PostHog directly through the HTTP MCP server below instead.

```bash
codex plugin marketplace add EveryInc/compound-engineering-plugin
codex plugin add compound-engineering@compound-engineering-plugin
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

Linear, Supabase, and Vercel are left out on purpose because Codex gets them
from the apps linked to the ChatGPT account, which follow the account to Codex
desktop and the CLI.

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

`codex mcp add` has no `--header` flag, so after adding `posthog` (and signing
in via OAuth), add the static consumer header under `[mcp_servers.posthog]` in
`~/.codex/config.toml` so `learn posthog:instrument-product-analytics` works for
[automations/analytics-gap-audit.md](automations/analytics-gap-audit.md):

```toml
[mcp_servers.posthog]
url = "https://mcp.posthog.com/mcp"
http_headers = { "x-posthog-mcp-consumer" = "plugin-learn" }
```

## Antigravity MCP servers

Antigravity has no `claude.ai` connectors or ChatGPT linked apps, so Linear and
PostHog are registered directly with `agy mcp add`. The `x-posthog-mcp-consumer`
header keeps `learn posthog:instrument-product-analytics` working for
[automations/analytics-gap-audit.md](automations/analytics-gap-audit.md), giving
Claude Code (connector), Codex (HTTP MCP), and Antigravity (HTTP MCP) consistent
PostHog access across machines. Extra Antigravity MCP servers from local
configuration are allowed by the check below, just like Codex MCP servers.

```bash
agy mcp add linear https://mcp.linear.app/mcp
agy mcp add --header "x-posthog-mcp-consumer: plugin-learn" posthog https://mcp.posthog.com/mcp
```

## GitHub CLI

Install the `gh-stack` extension used for stacked pull requests:

```bash
gh extension install github/gh-stack
```

Set `GH_PROMPT_DISABLED=1` in non-interactive and agent shell environments (for
example, in your shell profile or service environment) so `gh` fails fast
instead of hanging on interactive prompts:

```bash
export GH_PROMPT_DISABLED=1
```

## Check a machine against this list

Run this from the repository root with Python 3.9 or later, all three harness
CLIs (`claude`, `codex`, and `agy`), and `gh`. It prints nothing when the
machine matches this manifest:

- Every listed skill is in the skills CLI lock, with no unlisted skills managed by the skills CLI.
- `SKILL.md` exists in the Codex, Claude Code, and Antigravity global skill directories for each listed locked skill and for Impeccable.
- Every listed Claude Code user plugin is enabled, with no extra enabled Claude Code user plugins (built-in `@builtin` plugins are ignored).
- Every listed Codex plugin and Antigravity's `compound-engineering` plugin are enabled, and Antigravity's `compound-engineering` version matches Claude Code's installed version.
- `typescript-language-server` and `pyright-langserver` are on `PATH`.
- Every listed Claude Code, Codex, and Antigravity MCP server is registered (and enabled in Codex and Antigravity), compared by name without starting servers.
- Every listed `gh` extension (such as `github/gh-stack`) is installed.

What the script leaves out:

- Global agent instructions and shell environment variables (such as `GH_PROMPT_DISABLED`) are not checked.
- Extra Codex plugins, Codex MCP servers, Antigravity plugins, Antigravity MCP servers, and `gh` extensions are allowed because they can come from the harness or local configuration.

```bash
python3 - <<'PYTHON'
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess

home = Path.home()
lines = Path("MACHINE-SETUP.md").read_text().splitlines()

def documented(prefix):
    return [shlex.split(line.removeprefix(prefix)) for line in lines if line.startswith(prefix)]

def agy_mcp_name(args):
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--":
            return args[i + 1] if i + 1 < len(args) else None
        if arg in {"-H", "--header", "-e", "--env", "-t", "--type"}:
            i += 2
            continue
        if arg.startswith("-"):
            i += 1
            continue
        return arg
    return None

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
agy_mcp_config = config_json(home / ".gemini/config/mcp_config.json")
claude_plugins = cli_json("claude", "plugin", "list", "--json")
codex_plugins = cli_json("codex", "plugin", "list", "--json")["installed"]
agy_plugins = cli_json("agy", "plugin", "list", "--json")
codex_servers = cli_json("codex", "mcp", "list", "--json")
gh_extensions = {
    parts[1]
    for line in subprocess.check_output(["gh", "extension", "list"], text=True).splitlines()
    if len(parts := line.split("\t")) >= 2 and parts[1]
}

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
    p["id"]: p
    for p in claude_plugins
    if p["scope"] == "user"
    and p["enabled"]
    and not p["id"].endswith("@builtin")
}
agy_enabled_plugins = {
    p["name"]: p for p in agy_plugins if p.get("enabled")
}

report("Claude Code plugin", {args[0] for args in documented("claude plugin install ")},
       set(claude_user_plugins), show_extra=True)
report("Codex plugin", {args[0] for args in documented("codex plugin add ")},
       {p["pluginId"] for p in codex_plugins if p["enabled"]})
report("Antigravity plugin", {"compound-engineering"}, set(agy_enabled_plugins))

for server in ("typescript-language-server", "pyright-langserver"):
    if not shutil.which(server):
        print(f"Missing language server: {server}")

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

agy_mcp_servers = agy_mcp_config.get("mcpServers")
agy_enabled_servers = (
    {
        name
        for name, server in agy_mcp_servers.items()
        if not (isinstance(server, dict) and server.get("disabled"))
    }
    if isinstance(agy_mcp_servers, dict)
    else set()
)

report("Claude Code MCP server",
       {args[1] for args in documented("claude mcp add --scope user --transport ")},
       set(claude_config.get("mcpServers", {})))
report("Codex MCP server", {args[0] for args in documented("codex mcp add ")},
       {server["name"] for server in codex_servers if server["enabled"]})
report("Antigravity MCP server",
       {name for args in documented("agy mcp add ") if (name := agy_mcp_name(args))},
       agy_enabled_servers)
report("gh extension",
       {args[0] for args in documented("gh extension install ")},
       gh_extensions)
PYTHON
```

## Optional host-specific setup

### Obsidian Headless

Optional Linux systemd setup for a paired dev machine that runs the
[Daily learning automation](automations/daily-learning.md), reading the vault
from an Obsidian Headless copy so the desktop app need not be open. Set
Headless up on the dev machine only, because the desktop app's Sync and
Headless Sync must not run on the same device. Follow the `obsidian-headless`
skill to log in, connect a copy outside every repository, and sync it. Before
starting continuous sync, set the copy to `mirror-remote` mode with
`ob sync-config --path <copy> --mode mirror-remote`. That mode downloads every
change and reverts any change made on the dev machine, so the copy stays an
exact mirror of the vault. Then keep it syncing with `ob sync --continuous` as
a user service, and run `loginctl enable-linger` so the service starts at boot
and keeps running when you are logged out. Notes are written on the
workstation through the Obsidian CLI, because only the desktop app updates
links when a note is renamed.

The mode is a guard against mistakes, not a security boundary. The
automation's worker runs as the same user as the sync service, so an agent
steered by a planted instruction could change the mode back. The worker
reports the mode it finds, and Obsidian Sync's version history can restore
changed or deleted notes.

### Linux headless Chromium (AppArmor)

Unattended `impeccable audit` runs on interactive web UI leaves (and other
Playwright browser checks) launch Playwright's bundled headless Chromium. On
Ubuntu 24.04 and later Linux hosts where AppArmor restricts unprivileged user
namespaces (`kernel.apparmor_restrict_unprivileged_userns=1`), Chromium's
sandbox fails at startup unless an AppArmor profile grants `userns` to the
Playwright Chromium binaries.

Create `/etc/apparmor.d/playwright-chromium` with a portable user-cache glob:

```text
# Allow Playwright's bundled Chromium to use unprivileged user namespaces on Ubuntu 24.04+
abi <abi/4.0>,
include <tunables/global>

profile playwright-chromium /home/*/.cache/ms-playwright/**/chrome* flags=(unconfined) {
  userns,
}
```

Load the profile with:

```bash
sudo apparmor_parser -r /etc/apparmor.d/playwright-chromium
```

If Playwright browsers live under a custom `PLAYWRIGHT_BROWSERS_PATH` outside
the default user cache directory, adjust the binary path glob in the profile to
match that location.
