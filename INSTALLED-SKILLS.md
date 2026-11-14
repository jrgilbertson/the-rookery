# Installed skills

The skills I install on every machine, so a new environment can be set up from
one list. It records names and sources only; each install takes the source's
current version.

## Install with the skills CLI

Each line installs the listed skills from one source for the whole machine.

```bash
npx skills add ai-evals-course/evals-skills -g -y --skill build-review-interface error-discovery eval-audit evals-start evaluate-rag generate-synthetic-data validate-evaluator write-code-eval write-judge-prompt
npx skills add cathrynlavery/diagram-design -g -y --skill diagram-design
npx skills add emilkowalski/skills -g -y --skill break-ui mobile-native
npx skills add github/gh-stack -g -y --skill gh-stack
npx skills add harshaneel/humanize -g -y --skill ai-check
npx skills add https://docs.stripe.com -g -y --skill connect-recommend connect-required-verification-information metronome stripe-apps stripe-best-practices stripe-directory stripe-docs stripe-pay stripe-projects upgrade-stripe
npx skills add jrgilbertson/networked-thinking-skills -g -y --skill atomic-note atomic-note-audit managing-obsidian-tasks
npx skills add jrgilbertson/the-rookery -g -y --skill checking-simplicity coordinating-work creating-portable-skills managing-issues managing-personal-crm personal-chief-of-staff reviewing-meetings storm-research
npx skills add kepano/obsidian-skills -g -y --skill defuddle json-canvas obsidian-bases obsidian-cli obsidian-markdown
npx skills add livekit/agent-skills -g -y --skill building-livekit-agents debugging-livekit-agents operating-livekit-agents reading-livekit-docs running-livekit-simulations testing-livekit-agents writing-livekit-scenarios
npx skills add mattpocock/skills -g -y --skill codebase-design domain-modeling grill-me grill-with-docs grilling improve-codebase-architecture retro setup-matt-pocock-skills writing-for-agents
npx skills add millionco/react-doctor -g -y --skill react-doctor
npx skills add morluto/rea -g -y --skill reverse-engineer-anything
npx skills add mvanhorn/cli-printing-press -g -y --skill printing-press printing-press-amend printing-press-import printing-press-output-review printing-press-polish printing-press-publish printing-press-reprint printing-press-retro printing-press-score
npx skills add mvanhorn/last30days-skill -g -y --skill last30days
npx skills add shadcn/improve -g -y --skill improve
npx skills add supabase/agent-skills -g -y --skill supabase-postgres-best-practices
npx skills add tmchow/illo-skill -g -y --skill illo
npx skills add vercel-labs/agent-skills -g -y --skill vercel-react-best-practices
npx skills add vercel-labs/skills -g -y --skill find-skills
npx skills add wheresryan22/anatomy -g -y --skill anatomy
```

## Installed another way

[Impeccable](https://github.com/pbakaus/impeccable) has its own installer and
updater:

```bash
npx impeccable install --global
npx impeccable update --global
```

## Not on this list

- Orca's own skills (`orca-cli`, `orca-linear`, `orchestration`). Orca installs
  them and matches them to the app version, so the skills CLI should not track
  them.
- Agent plugins such as Compound Engineering, which each harness installs
  through its own plugin manager.

## Check a machine against this list

This prints nothing when the machine's lock file and the list above name the
same skills. A line starting with `<` is installed but not listed; a line
starting with `>` is listed but not installed.

```bash
diff <(jq -r '.skills | keys[]' "$HOME/.agents/.skill-lock.json" | sort) \
  <(grep '^npx skills add' INSTALLED-SKILLS.md | sed 's/.*--skill //' | tr ' ' '\n' | sort)
```
