# The skills

This directory contains the installable skills. Each skill lives in its own folder as `skills/<name>/SKILL.md` plus any bundled references, and each installs individually. You never need to adopt the whole repo.

```bash
# browse what's available
npx skills add jrgilbertson/the-rookery --list

# install one skill
npx skills add jrgilbertson/the-rookery --skill <name>
```

Skills here follow the [Agent Skills](https://agentskills.io) format and install
in Claude Code, Codex, and other compatible tools that read `SKILL.md`.

## Available skills

- **[creating-portable-skills](creating-portable-skills/SKILL.md)** creates a new
  agent skill or helps review, update, and move an existing one. It starts with
  the intended outcome, validates the package, compares behavior with focused
  tests, and checks installation separately from activation.

  ```bash
  npx skills add jrgilbertson/the-rookery --skill creating-portable-skills
  ```

- **[personal-chief-of-staff](personal-chief-of-staff/SKILL.md)** runs an
  evidence-based morning review, daily journal and wind-down, weekly review, or
  quarterly review. It works from existing authoritative sources, collaborates
  on judgment, and keeps every durable change reviewable.

  ```bash
  npx skills add jrgilbertson/the-rookery --skill personal-chief-of-staff
  ```

- **[managing-personal-crm](managing-personal-crm/SKILL.md)** maintains useful
  relationship context, prepare for one person, find relevant people for
  current work, and clean up Person notes without building a separate CRM
  database. It keeps durable changes reviewable and routes each effect to its
  canonical destination.

  ```bash
  npx skills add jrgilbertson/the-rookery --skill managing-personal-crm
  ```

- **[reviewing-meetings](reviewing-meetings/SKILL.md)** turns newly completed
  meetings from a configured source into grounded, independently reviewable
  notes and follow-up actions. It prevents duplicate work, preserves one
  canonical owner for each outcome, and keeps scheduled runs read-only.

  ```bash
  npx skills add jrgilbertson/the-rookery --skill reviewing-meetings
  ```

More skills are arriving. Watch the [CHANGELOG](../CHANGELOG.md) or releases.
