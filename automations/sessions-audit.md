# Sessions audit

Review recent AI sessions and recommend improvements to skills, workflows,
guidance, and configuration. The remote audit runs first; the local audit
combines both hosts' findings into one list.

- **Cadence:** Daily, remote at 01:00 and local at 03:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The [Compound Engineering plugin](https://github.com/EveryInc/compound-engineering-plugin), including `ce-retro` and `ce-pov`, and this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill for the selected agent on each host. Each run needs access to that host's AI session histories, the repositories' current guidance, and a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Setup

Create each job on the host whose sessions it will review. Each job covers
only its own host. Copy the shared prompt below and replace step 5 with the
matching [consolidation instructions](#consolidation). For a single-host job,
keep the shared prompt as written.

Replace The Rookery with the repository whose skills, workflows, guidance,
and configuration you want reviewed. Fill in the private history repository.

Use the selected harness's supported invocation for `ce-retro`. The automation
owns session discovery and private history; CE Retro supplies the assessment.
Its default discovery covers one repository, and its local ledger is not used
here. Keep the installed plugin unchanged.

## Prompt

```text
Before assessing, confirm the required skills are available to the selected agent. If a required skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

Review this host's AI sessions from the past 24 hours alongside The Rookery's skills, workflows, guidance, and configuration. Widen the window after missed runs to cover the gap. This scheduled request authorizes the named host-wide session reads. This assessment ends with a report and recorded owner decisions. Issue creation, implementation, PR publication, and configuration changes are separate work through their owning workflows after an explicit instruction; do not start them from a finding decision in this run.

1. Read history first. Clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Follow its README's storage instructions, using its helper when available or its documented Git steps otherwise. Read `sessions-audit` owner decisions and recent runs, plus this host's latest report even if it is older than the three newest reports overall. Inherit only this host's still-unread sessions from that report, including when it contains both hosts. Resolve known host-name changes from existing host metadata and history; disclose uncertain identity instead of silently choosing a different host. Distinguish unavailable history from no prior history and report any resulting limits on deduplication, grading, or unread-session carry-forward. An earlier report without an unread list leaves that coverage unknown. Revisit declined findings only with materially new evidence, labeled as previously declined.

2. Discover actual transcripts across this host's configured agents, account homes, and repositories. Verify the account homes from the host's available interfaces. Select by modification time, follow symlinks, deduplicate real paths, and cross-check Orca's session journal; it does not cover all terminal or external-app sessions. Add inherited unread sessions to the window's new sessions. Report each harness and account as searched, present but unread or unsupported, or absent. Exclude this audit, synthetic evaluations, prior retros and their transcript readers. Count child transcripts with their parent. Describe personal threads by category only; keep private evidence outside public repositories.

3. Invoke `ce-retro` on those selected sessions and the relevant repositories' current source, using only its no-user branch: steps 1–4, then its candidates-only report. Apply nothing and record no decisions through CE Retro, even if the owner later replies. Supply the host-wide inventory explicitly; its repo-filtered `sessions` helper cannot establish this coverage. The discovered sessions, including inherited unread work, are the read set: batch them across readers rather than applying CE Retro's default sample of about 20. Use its extractors on those files. If an execution limit prevents reading them all, report the incomplete coverage and carry every unread session forward. If there are no eligible local sessions, skip local mining and still complete consolidation and reporting. Use the private history already read for prior decisions and grading, rather than its local ledger. Skip `store`, `record`, and `record-run`: `store` creates local state even without decision writes. Add no ledger directory or ignore rule. Keep extracts and `candidates.md` in temporary storage outside the repositories.

4. Confirm each finding's cause in the transcript lines it cites, including findings returned by delegated readers, and check that the cause remains in current source. Quantify time and effort only where events support it; silence in a log does not establish waiting time. When extracts omit causal detail, read the relevant original events or leave the claim uncertain. Identify the owner: a Rookery-owned source change, another project's change, or a third-party skill proposal. Compare complete root-cause solutions, then recommend any safeguard still needed. Group related draft recommendations into coherent sets; split those needing materially different context. Include recommendations to leave a confirmed finding unchanged. Each run, invoke `checking-simplicity` afresh on each set, covering every recommendation and their interactions. Skip it for an empty set; incomplete assessment remains a coverage gap. If independent review cannot finish, retain the assessment and label affected recommendations `review pending`; do not substitute self-review. A clean result is valid.

5. Prepare this host's recommendations for the final review. After that review and the report save in step 7, bring its list to the owner and record the exact decisions in private history.

6. Run `ce-pov` once on the revised recommendations as a whole, including review-pending items and interactions across sets. Have it judge each recommendation as its own decision against current evidence. The approval list holds only the recommendations it supports, most impactful first, each with its evidence, tradeoffs, uncertainty, and any pending-review label. List each recommendation it rejects in one line with its reason, outside the approval list. If either review cannot finish, save useful assessment work and name the missing review; without a completed `ce-pov`, keep the list provisional.

7. Save the report through the private history repository's storage procedure before presenting the list to the owner or waiting for answers. If saving fails, retain the report in temporary storage outside the repositories, report the failure, its cause, and that path, then stop. Do not mark it saved or consolidated; complete storage before collecting owner decisions. Append decisions when the owner answers. Include the window, host, repositories and accounts covered, coverage gaps, prior-change grading where evidence allows, and every still-unread session for this host. Carry that list forward cumulatively, including inherited items, until each is read or explicitly disposed of by the owner. State why each remains unread. Apply step 5's reporting and reply instructions. The job that presents the list to the owner records the exact decisions, including each finding's host. For a combined list, the local job is the sole decision writer. History instructions govern storage, not authority to implement; a recorded answer does not authorize this assessment run to implement a fix.
```

## Consolidation

The remote job runs two hours before the local one and saves its report without
asking the owner. Its recommendations remain provisional until the local job
combines both hosts' findings, runs the final `ce-pov`, and brings the owner
one list. If local consolidation does not finish, the saved remote report
still awaits that judgment. Each host's evidence can support or
contradict the other's.

### Remote job

Replace step 5 with:

```text
5. Skip step 6: the local job owns the final `ce-pov` judgment after consolidation. Save this host's recommendations as provisional until that judgment, preserving any `review pending` labels. When saving the report in step 7, include this session's Orca session ID and workspace. After that save, stop without asking the owner. The local Sessions audit reads the report and becomes this workspace's parent in Orca. Answer its evidence questions. The local job records owner decisions for the combined list; do not append those decisions again. Relayed replies do not authorize implementation, issue creation, publication, or configuration changes.
```

### Local job

Replace step 5 with:

```text
5. Read each remote report not yet included in a successful local consolidation, using the remote report paths recorded in prior local reports. Widen retrieval after missed or late runs; if prior consolidation coverage is unknown, disclose that gap and use the widened review window. Make this workspace the parent of each relevant remote workspace in Orca. Merge its recommendations with this host's revised recommendations into one prioritized list before `ce-pov` judges it: combine matching findings, say where the two hosts' evidence conflicts, and mark each item's host. Independently assess any substantively new recommendation first drafted during consolidation with `checking-simplicity` before the final `ce-pov`, or label it `review pending` if review cannot finish. Deduplication and presentation changes alone do not require another simplicity review. Preserve pending-review labels from both hosts through the final judgment. Count consolidation as successful only after that judgment completes and the combined report is saved. Preserve each host's coverage and unread-session list in the combined report and identify the remote report paths included. After the final review and the report save in step 7, bring the combined list to the owner here and record each exact answer once in private history, labeled by host. Relay an answer to a remote session only when needed to clarify its evidence; the remote must not record it again. With no remote report, say so and report this host only. Do not resume CE Retro's apply phase after an answer.
```

### Single-host job

A job on one host uses the shared prompt without either replacement and brings
that host's reviewed list to the owner.

## Verify setup

Before activating a revised prompt, run it manually. For two hosts, run the
remote audit first and confirm its report is saved before running the local
audit and verifying consolidation of both reports. Verify skill
loading, account-home coverage, assessment-only behavior, unread-session
carry-forward, private report storage, and absence of new local CE Retro state.
Check the filesystem before and after; an existing `.context` directory is not
proof that the run created one. Confirm each saved Orca job's prompt matches the
reviewed definition before reporting it updated. Preserve its schedule and enabled
state unless the owner requests a change.
