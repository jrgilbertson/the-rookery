# Repository Agent Guidance

## Private and generated artifacts

This is a public open-source repository. Its working directory holds only this
repository's own source, tests, docs, and configuration. Anything generated for
the user rather than for the repo, along with its supporting files (builders,
renders, previews, inspection files, dependency links), goes in a per-run
temporary directory outside the working directory, and final artifacts go only
to an explicitly approved external or private destination.

The root `outputs/` directory remains ignored as a privacy safeguard for older
Codex Desktop and similar tooling that may write generated artifacts there. It
is not part of the current workflow or an approved storage location.

Before staging or committing, inspect all untracked paths and confirm that no
personal or business artifacts are present.

## Working artifacts

Keep plans, brainstorms, ideation, raw dogfood notes, and point-in-time reports
in the ignored working paths named in `.gitignore`. They may live for the life
of a worktree, but the final pull request and default branch must not contain
or depend on them. Preserve the outcome in its canonical home: code and tests
for behavior, an ADR for a lasting architectural choice, `docs/solutions/` for
a reusable learning, or the current root `RELEASING.md` for operating and
shipping procedures.

Research is durable only when the repository will maintain it as a current
source. Keep temporary audits and findings with the issue, pull request, or
other reporting system. When a source issue exists, record material scope
changes and follow-up work there before merge; a routine completion summary or
copy of the plan is unnecessary.

## Documented solutions and vocabulary

`docs/solutions/` holds documented solutions to past problems, covering bugs,
best practices, and workflow learnings, organized by category with YAML
frontmatter (`module`, `tags`, `problem_type`). Relevant when implementing or
debugging in an area a learning already covers.

`CONCEPTS.md` holds the shared vocabulary for this project: the entities,
named processes, and status concepts that carry a specific meaning here.
Relevant when orienting to the repo or discussing its concepts.
