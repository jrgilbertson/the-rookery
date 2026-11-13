# Optimize CI

Review continuous integration and recommend improvements.

- **Cadence:** Saturday at 09:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-optimize` skill, this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, and access to the target repository's CI configuration. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state). The prompt expects a measurement harness in that repository's `optimize-ci/harness/` folder, with a README naming its commands.

The installed `ce-optimize` workflow builds measurement scaffolding before its
experiment approval gate. This prompt asks for recommendations and leaves that
setup work to the skill.

Orca starts each run in a new worktree, and `ce-optimize` keeps its state in
the checkout unless a durable state root is named. The harness lives in the
automation-state repository, so every host gets the same scripts by pulling.
What they download, such as GitHub API responses, stays in a cache folder on
each host outside any repository, and each host rebuilds it.

Each report measures two things:

- **Hosted:** pull-request runner minutes per merged pull request, by one fixed
  method, so weeks can be compared.
- **Local:** Verify duration per suite, reuse of saved results, and failed
  attempts, read from the task runner's history on the host that ran the
  verifies. The harness this was written for reads Nx's task history, which
  records no run id, so it groups tasks into runs by time gaps. Another host
  has its own history, so its numbers are reported as that host's and are not
  compared with the first host's.

The lessons paragraph in the prompt comes from a series of local Verify fixes:
checks forced to run alone, reruns of passed work, cache keys that missed what a
check reads, hosted jobs that repeated a passed local Verify, and failures a
quick check would have caught sooner.

## Prompt

```text
Use `ce-optimize` to assess CI and recommend improvements. CI includes local Verify as well as hosted runs. Keep experiments within its approval requirements; recommendations do not authorize issue creation, implementation, or PR publication.

Measure with the harness in the history clone's `optimize-ci/harness/`; its README gives the commands. Downloaded GitHub responses and experiment outputs stay in the local cache at $HOME/.local/state/ci-optimize/<repository name>/, which each host rebuilds. If the run changes a harness file, commit and push that change before saving the report. Keep new measurements dated and compare them with earlier run reports.

Every report has two measured sections:
- Hosted: pull-request runner minutes per merged pull request for the reviewed week, from the harness's pull-request minutes command, beside earlier weeks. Name the method of any other hosted figure, and do not compare figures measured by different methods.
- Local: Verify duration per suite, reuse of saved results, and failed attempts, from the harness's local command, with the baseline window its README names beside it when this host has those rows. Name the host; numbers from different hosts are not comparable.

What earlier fixes taught: most local Verify time went to checks forced to run alone without a recorded reason and to reruns of work whose inputs had already passed. A saved result is safe only when its cache key covers everything the check reads. A hosted pull-request job that repeats a check the local Verify already passed can move to the merge queue. Cheap static failures belong in a quick check that runs before Verify. Local timings move with machine load and with verifies that overlap, so say so when a before-and-after rests on them.

Run `checking-simplicity` on each draft recommendation, then run `ce-pov` on the revised recommendations and incorporate its judgment into the final prioritized recommendations for approval. Preserve evidence, tradeoffs, and uncertainty. Report blocked reviews and cases where no change is justified.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `optimize-ci` runs and owner decisions before assessing, and save the final report afterward. Follow the README's storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.
```
