# Sessions audit

Review recent AI sessions with the installed `retro` skill.

| Orca job | Cadence | Timezone |
|---|---|---|
| Sessions audit (local) | Daily at 05:00 | America/Chicago |
| Sessions audit (remote) | Daily at 03:00 | America/Chicago |

- **Requires:** Matt Pocock's [`retro`](https://github.com/mattpocock/skills/tree/main/skills/engineering/retro) and [`writing-for-agents`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) skills installed for the selected agent, access to that machine's AI session histories, and access to the repository's current guidance.

Before scheduling, follow the
[upstream installation instructions](https://github.com/mattpocock/skills#installation-30-second-setup)
for the agent selected in Orca, or run `npx skills@latest add mattpocock/skills`
and select `retro` and `writing-for-agents` for that agent. Repeat the
installation on each host where a session audit will run.

Both jobs use the same prompt. Create each job on the Orca host whose sessions
it should review; a job on one host does not establish coverage of the other.
Replace The Rookery with the repository whose skills, workflows, guidance, and
configuration you want reviewed.

The prompt reviews the previous 24 hours on every run. Widen the review window
after missed runs to cover sessions from when the host was unavailable.

## Prompt

```text
/retro all my AI sessions for the past 24 hours, together with The Rookery repository's skills, workflows, guidance, and related configuration.
```
