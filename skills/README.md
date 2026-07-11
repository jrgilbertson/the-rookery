# The skills

This directory is the shelf. Each skill lives in its own folder as `skills/<name>/SKILL.md` plus any bundled references, and each installs individually. You never need to adopt the whole repo.

```bash
# browse what's available
npx skills add jrgilbertson/the-rookery --list

# install one skill
npx skills add jrgilbertson/the-rookery --skill <name>
```

Skills here follow the [Agent Skills](https://agentskills.io) format, so they work in Claude Code, Codex, and anything else that reads `SKILL.md`.

## The flock is arriving

The shelf is currently being stocked. Until the first skills land, the install command above reports exactly this, verified against this repo.

```
No skills found
No valid skills found. Skills require a SKILL.md with name and description.
```

That is expected, not broken. Watch the [CHANGELOG](../CHANGELOG.md) or releases for arrivals.
