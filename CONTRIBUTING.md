# Contributing to The Rookery

Thanks for your interest. Seriously. This repo exists because I've learned an enormous amount from people sharing their setups, and contributions that make it better are welcome.

A few ground rules keep this repo healthy and keep me honest as a solo maintainer.

## What's welcome as a pull request

- **Fixes.** Typos, broken links, incorrect instructions, and bugs in a skill's behavior.
- **Portability improvements.** Making a skill work better across harnesses like Claude Code and Codex.
- **Hardening.** Clearer trigger descriptions, better degradation when a capability isn't available, and tightened instructions.

Open a PR directly for any of these. Small and focused beats large and sweeping.

## Proposing a new skill

The Rookery is **curated, not collected**. Every skill here is something I use
and ship as an Agent Skills package for compatible tools. New skills start as
an issue, not a PR.

1. Open a [skill proposal issue](../../issues/new/choose) describing what the skill does and which harnesses you've tested it in.
2. We talk about it.
3. If it fits, we figure out the path in.

There is no merge promise. A great skill might still not fit here, and that is not a judgment on the skill. I'm happy to link out to good work either way.

## What to expect from me

This is a personal project with **no support SLA**. I read issues and PRs, but response times vary with life and work. Kindness in both directions is assumed. See the [Code of Conduct](CODE_OF_CONDUCT.md).

## The rules this repo lives by

- **`main` is the install source.** Installs pull from the default branch, so whatever lands on `main` is instantly what people get, and it stays install-clean. Experiments live on branches.
- **The same-door rule.** I install from this repo the same way you do. Nothing in it may depend on context that exists only on my machine. That means no absolute paths, no private repo names, and no personal-environment assumptions. Contributions are held to the same rule.
- **The README lists every skill.** When a skill lands in `skills/`, it gets a line in the README's skills section in the same change.
- **Docs ship public.** The working documents in `docs/` (plans, learnings) are part of the repo on purpose. The process is part of what's being shared.
