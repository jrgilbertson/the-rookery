# Optimize CI

Review continuous integration and recommend improvements.

- **Cadence:** Saturday at 09:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-optimize` skill and access to the target repository's CI configuration. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state). The prompt expects a measurement harness in that repository's `optimize-ci/harness/` folder, with a README naming its commands.

## Setup

The installed `ce-optimize` workflow builds measurement scaffolding before its
experiment approval gate. This prompt asks for recommendations and leaves that
setup work to the skill.

Orca starts each run in a new worktree, and `ce-optimize` keeps its state in
the checkout unless a durable state root is named. The harness lives in the
automation-state repository, so every host gets the same scripts by pulling.
What they download, such as GitHub API responses, stays in a cache folder on
each host outside any repository, and each host rebuilds it.

## Prompt

```text
Before assessing, confirm the required skills are available to the selected agent. If a required skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `optimize-ci-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `ce-optimize` to assess CI and recommend improvements. CI includes local Verify as well as hosted runs. Keep experiments within its approval requirements; recommendations do not authorize issue creation, implementation, or PR publication.

Measure with the harness in the history clone's `optimize-ci/harness/`; its README gives the commands. Downloaded GitHub responses and experiment outputs stay in the local cache at $HOME/.local/state/ci-optimize/<repository name>/, which each host rebuilds. If the run changes a harness file, commit and push that change before saving the report. Keep new measurements dated and compare them with earlier run reports.

Every report has two measured sections:
- Hosted: pull-request runner minutes per merged pull request for the reviewed week, from the harness's pull-request minutes command, beside earlier weeks. Name the method of any other hosted figure, and do not compare figures measured by different methods.
- Local: Verify duration per suite, reuse of saved results, and failed attempts, from the harness's local command, with the baseline window its README names beside it when this host has those rows. Name the host; numbers from different hosts are not comparable. Local timings move with machine load and with verifies that overlap, so say so when a before-and-after rests on them.

Look for where Verify and hosted time goes: checks run serially, work rerun on unchanged inputs, hosted jobs that repeat local checks, and failures caught later than a cheaper check could catch them. Any recommendation to reuse a saved result shows that its cache key covers every input the check reads.

Judge each draft recommendation as its own decision against current evidence, including recommendations to leave a confirmed finding unchanged and how the recommendations interact. The approval list holds only the recommendations you support, in leverage order, highest first, each with its evidence, tradeoffs, and uncertainty. List each recommendation you reject in one line with its reason, outside the approval list.

Save the final report afterward.
```

## Measurement notes

Each report measures two things:

- **Hosted:** pull-request runner minutes per merged pull request, by one fixed
  method, so weeks can be compared.
- **Local:** Verify duration per suite, reuse of saved results, and failed
  attempts, read from the task runner's history on the host that ran the
  verifies. The harness this was written for reads Nx's task history, which
  records no run id, so it groups tasks into runs by time gaps. Another host
  has its own history, so its numbers are reported as that host's and are not
  compared with the first host's.
