# The skills

This directory is the shelf. Each skill lives in its own folder as `skills/<name>/SKILL.md` plus any bundled references, and each installs individually. You never need to adopt the whole repo.

```bash
# browse what's available
npx skills add jrgilbertson/the-rookery --list

# install one skill
npx skills add jrgilbertson/the-rookery --skill <name>
```

Skills here follow the [Agent Skills](https://agentskills.io) format, so they work in Claude Code, Codex, and anything else that reads `SKILL.md`.

## On the shelf

- **[creating-skills](creating-skills/SKILL.md)** — create a new agent skill, or review, update, and migrate an existing one. One loop from intent interview through baseline testing to a packaged skill that works across models and harnesses.

  ```bash
  npx skills add jrgilbertson/the-rookery --skill creating-skills
  ```

More skills are arriving. Watch the [CHANGELOG](../CHANGELOG.md) or releases.
