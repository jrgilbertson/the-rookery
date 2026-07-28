# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Added

- `creating-portable-skills` is the first published skill. It creates new Agent
  Skills and helps review, update, or move existing skills. It starts from the
  user's goal, checks the package structure, compares behavior with focused
  tests, and verifies installation separately from activation. It works
  without companion skills.
- `personal-chief-of-staff` guides morning, wind-down, weekly, and quarterly
  reviews using current data from the user's connected sources. It requires
  review before writing changes, handles Obsidian CLI operations, tests its
  behavior, and includes a versioned specification for four local Codex
  schedules.
- `managing-personal-crm` keeps relationship context in canonical Person notes
  and Tasks. It captures updates, finds relevant context, prepares for
  conversations with one person, and proposes cleanup in stages. It matches
  identities carefully, proposes changes before writing them, handles mixed
  schemas during migration, and stores no hidden CRM state.
- `reviewing-meetings` reviews completed meeting evidence from any supported
  source. It prevents duplicate notes and tasks, sends each outcome to one
  canonical system, and applies only actions that the user approves
  independently. It also includes behavior tests with sanitized data and a
  versioned specification for the `CoS Meetings` schedule.

### Changed

- `creating-portable-skills` now grounds guidance in real project evidence,
  uses separate fresh-context agents for reviews and grading, inspects artifacts
  and execution traces directly, and tests activation with more realistic
  queries.
- `creating-portable-skills` now ends read-only audits after delivering the
  review, keeps trigger descriptions positive, defines the Claim Ceiling, and
  centralizes trigger scoring and evidence states in one record.
- `personal-chief-of-staff` can now include relationship check-ins and timely
  opportunities in its morning, wind-down, and weekly reviews when Personal CRM
  is available.
- `reviewing-meetings` can now suggest contact dates, save useful relationship
  context, capture personal follow-ups, and surface relevant connections. Each
  meeting still produces one review bundle, and every approved action goes to
  one canonical destination.

## [0.1.0] - 2026-07-10

### Added

- Repository scaffolding. Community files (MIT license, contributing guide, code of conduct, security policy), issue and PR templates, the skills catalog layout, and the seven-job workflow map across README and WORKFLOWS.md.
- The rules the repo lives by. Curated not collected, main is the install source, and the same-door rule.
