# Briefs and Leads

Load this reference before writing or amending a worker brief or starting,
retiring, or replacing a Domain or Design Lead. Shared custody, overlap,
worktree, and alert rules stay in `SKILL.md`.

## Worker brief template

Every brief carries:

- the leaf, its file list, and its Verification
- the model picked
- the ownership line on its own line starting at column 0 in the pull request
  body, with `repo-captain` as the `Owner:` role and the worker's own role as
  `Author:`
- the stacking rule: build on at most one held pull request whose checks
  pass, using `gh-stack`, never on a chain of unreviewed pull requests
- the bot rule and the scrub rule from `SKILL.md`'s Rules for every step
- the instruction to show evidence beside each Verification item in the pull
  request body
- the instruction to keep local service and database stacks running through
  `ce-babysit-pr` (until initial review and CI settle, rather than tearing
  them down before `gh pr create`), tear them down right before sending
  `worker_done`, keep the worktree, and never push to a held pull request

## UI/UX briefs

Any brief for a UI/UX leaf, sent by the Captain or by a Domain or Design
Lead, adds these instructions without changing how `lfg` runs:

- **Default UI/UX skill.** Name `impeccable` (`impeccable context`,
  `craft-floor.md`, and `DESIGN.md`) as the default UI/UX design skill
  alongside any applicable platform or framework skills (such as
  `modern-web-guidance`, `mobile-native`, `break-ui`, or React guidance), so
  `impeccable` adds to rather than suppresses them.
- **Unattended `impeccable audit` after `lfg` (interactive UI/UX web pages
  only).** Scope this gate strictly to interactive UI/UX web pages. Do not
  require `impeccable audit` for static diagram or image plates; verify those
  via before-and-after renders instead. For interactive UI/UX web pages, once
  stock `lfg` finishes (including `ce-test-browser` and its initial
  `ce-babysit-pr`) and before sending `worker_done`, run an unattended
  `impeccable audit` on the pull request branch:
  - Proceed without pausing for user questions.
  - Auto-fix verified P0 and P1 objective technical findings (accessibility,
    contrast, responsive or zoom overflow, touch targets, design tokens, and
    `DESIGN.md` integrity).
  - Record the audit result and audited head commit in the pull request body,
    including any remaining P2 and P3 findings or subjective design tradeoffs
    instead of redesigning unasked.
  - Keep transient `.impeccable/` audit and critique snapshots out of git
    (never commit them), while leaving any intentionally tracked
    `.impeccable/design.json` intact. When fixes land, run local checks, push
    one follow-up commit, record the audit result for that head in the pull
    request body, and confirm CI settles through `ce-babysit-pr` before
    sending `worker_done`.
- **Interactive UX judgment stays out of Executors.** Executors stay
  asynchronous. Interactive `impeccable critique` and `/impeccable live` run
  only with the Captain or a Design Lead, either pre-build on mocks or
  prototypes or post-PR in the kept worktree for `V = 3` UI work (a new
  user-facing view, flow, or visual direction that needs human judgment).

## Domain and Design Leads

Start a Domain Lead on the Captain's own machine with
`worker-start --environment local --worktree new-top-level --keep-open`. The
Lead makes its own child Run with `run-create --environment local` and starts
its Executors there.

- **Fixed leaves.** Give the Lead a set of leaves and their file lists. For
  any new leaf, including a design-system seam, the Lead asks the Captain with
  `orca orchestration ask`, and the Captain answers from the overlap check.
- **Models.** The Lead picks its Executors' models by the same rule as the
  Captain.
- **No merging.** The Lead's hand-up is the pull request on GitHub. The
  Captain judges it from the raw diff like any other.
- **Design Lead.** A Design Lead keeps sibling UI pull requests consistent
  with the design system. When siblings need a token or component the system
  lacks, it opens one seam pull request that adds it. That pull request is a
  sensitive kind, so it is held, and siblings may stack on it.
- **Retiring.** The Lead sends `worker_done` when it has no active Executors.
  Release it with `worker-release` and delete its state file
  (`leads/<name>.md`). Later rework on one of its pull requests is grouped
  afresh.
- **Dropped Leads.** Replace a Lead that `exited` from its state file. Leave
  one that reads `unverifiable` or `lost` without a replacement, keep its
  files reserved, and list its group in the catch-up.
