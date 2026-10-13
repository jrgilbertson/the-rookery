# Contributing to The Rookery

Thanks for your interest. This repo exists because I've learned an enormous amount from people sharing their setups, and contributions that make it better are welcome.

A few ground rules keep this repo healthy and keep me honest as a solo maintainer.

## What's welcome as a pull request

- **Fixes.** Typos, broken links, incorrect instructions, and bugs in a skill's behavior.
- **Portability improvements.** Making a skill work better across harnesses like Claude Code and Codex.
- **Hardening.** Clearer descriptions of when to use a skill, better fallback
  behavior when a capability is unavailable, and more precise instructions.

Open a focused PR directly for any of these.

Please use the [bug report form](https://github.com/jrgilbertson/the-rookery/issues/new/choose) for defects. Security
issues belong in the private process described in [SECURITY.md](SECURITY.md),
not in a public issue.

## Proposing a new skill

New skills start as an issue, not a PR.

1. Open a [skill proposal issue](https://github.com/jrgilbertson/the-rookery/issues/new/choose) describing what the skill does and which harnesses you've tested it in.
2. We talk about it.
3. If it fits, we figure out the path in.

There is no merge promise. A great skill might still not fit here, and that is not a judgment on the skill. I'm happy to link out to good work either way.

## What to expect from me

This is a personal project with no support SLA. I read issues and PRs, but response times vary with life and work. Kindness in both directions is assumed. See the [Code of Conduct](CODE_OF_CONDUCT.md).

## The rules this repo lives by

- `main` is the install source. Installs pull from the default branch, so merged
  changes are immediately available to users. Keep `main` ready to install.
  Experiments live on branches.
- **Installation parity.** Nothing in it may depend on context that exists only on my machine. That means no absolute paths, no private repo names, and no personal-environment assumptions. Contributions follow the same rule.
- **Every skill stands on its own.** Each skill folder installs separately.
  Nothing in it may reference a file in another skill's folder. The
  [Agent Skills](https://agentskills.io) specification resolves paths from the
  skill root, so a cross-folder path breaks when someone installs only one
  skill. To share material, cite a sibling *skill by name* and provide fallback
  behavior when it is absent, or copy the material into each folder with a
  maintainer note naming its mirror.
- **The README lists every skill.** When a skill lands in `skills/`, it gets a line in the README's skills section in the same change.
- **Release snapshots do not pin installs.** `main` is the rolling catalog;
  semantic-version releases are immutable historical checkpoints. Corrections
  receive a new version instead of moving an existing tag. The maintainer
  process is in [RELEASING.md](RELEASING.md).
