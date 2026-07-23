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

- **[creating-portable-skills](creating-portable-skills/SKILL.md)** — create a new agent skill, or review, update, and migrate an existing one. One loop from intent interview through baseline testing to a packaged skill that works across models and harnesses.

  ```bash
  npx skills add jrgilbertson/the-rookery --skill creating-portable-skills
  ```

- **[personal-chief-of-staff](personal-chief-of-staff/SKILL.md)** — run an
  evidence-based morning review, daily journal and wind-down, weekly review, or
  quarterly review. It works from existing authoritative sources, collaborates
  on judgment, and keeps every durable change reviewable.

  ```bash
  npx skills add jrgilbertson/the-rookery --skill personal-chief-of-staff
  ```

- **[reviewing-meetings](reviewing-meetings/SKILL.md)** — turn newly completed
  meetings from a configured source into grounded, independently reviewable
  notes and follow-up actions. It prevents duplicate work, preserves one
  canonical owner for each outcome, and keeps scheduled runs read-only.

  ```bash
  npx skills add jrgilbertson/the-rookery --skill reviewing-meetings
  ```

More skills are arriving. Watch the [CHANGELOG](../CHANGELOG.md) or releases.
