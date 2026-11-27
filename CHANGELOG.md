# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Added

- A canonical Claude-only Promptfoo Skill Eval starter template under
  `evals/_template/` (`anthropic:claude-agent-sdk` with
  `apiKeyRequired: false`, `Write`/`Edit` offered and denied in `dontAsk`
  mode, no `Bash`, no Git repo, in-config auto-memory disabling, per-run
  timeout, isolated temporary `HOME`, committed `package-lock.json` installed
  with `npm ci`, and offline `check-fixtures.mjs`). `SKILLS.md` now documents
  this consolidated setup and optional additive `llm-rubric` judging,
  `evals/active-learning/` is hardened to match it, and the repository
  verification gate (`tests/evals/fixtures/run-eval-checks.py`) automatically
  runs every `evals/*/check-fixtures.mjs` offline with negative mutation tests.
- `repo-captain`, a skill that runs one persistent Captain per repository
  in Orca. It plans with the operator, dispatches Executors directly or
  through Domain Leads, serializes overlapping files and database
  migrations, and keeps tracker issues current through `managing-issues`.
  It is the only session that merges in its repository: it merges routine
  pull requests once their evidence is shown, holds the rest for the
  operator's Review Round, and carries out each verdict, judging any change
  since review on its own. Its behavior rests only on the operator's
  recorded words and on live facts it rereads at every wake, so a restart
  runs the same routine as any wake. It never blocks on the operator, never
  triggers a review bot, and interrupts only for an exposure or a Captain
  merge gone wrong. One Captain per repository can dispatch to any paired
  machine. Synthetic Skill Eval cases are under `evals/repo-captain/`.
- A review contract shared by `reviewing-prs` and `repo-captain`, shipped
  as an identical copy in each skill. The repository checks fail when the
  two copies differ.
- `CONCEPTS.md` defines Captain and Domain Lead.
- `reviewing-prs`, a skill that runs one Review Round across every
  repository the operator can merge in, including repositories shared with
  them as a collaborator, plus every pull request that asks for their
  review. It reads each open pull request from
  its raw diff at a fixed head commit, scores verification effort and undo
  cost from what the diff shows, lists stored and published names, flags
  claims the diff does not support and missing screenshots, and checks
  interface changes against the repository's design system when it has one.
  It fills a page template it ships with the round: a risk overview ranked
  by verification effort times undo cost and split at the hold line, then
  one block per pull request showing what changes for a user, as a table of
  situations before and after or as screens side by side. Shipped risk, such
  as a merge without the operator, is counted in the headline. A rail on wide
  screens, a progress count, and keyboard keys move through the round, and
  choices survive a reload in that browser. The page follows the system's
  light or dark setting, carries a strict Content Security Policy, and
  renders pull request text as text. It records each verdict on
  the pull request as a three-line comment naming the reviewed commit, and
  answers a review request with a review. A `not applicable` verdict posts
  nothing and removes the operator from a review request. It never merges or
  changes a label: the session that owns a pull request acts on its verdict.
  Synthetic Skill Eval cases are under `evals/reviewing-prs/`.
- `CONCEPTS.md` is rewritten in plainer words, with every entry readable on
  its own and no meaning changed. It adds Knowledge Frontier, the ideas just
  beyond what a learner's notes cover, and renames the model-routing Frontier
  to Pareto Frontier.
- `CONCEPTS.md` defines Review Round, verdict, and PR Review Labels
  (`review:held`, `review:auto-merged`, `review:human-merged`).
- `docs/adr/001-verdict-trust-by-convention.md` records why a verdict comment
  and a pull request's `Owner:` line are trusted by convention while every
  agent shares the operator's GitHub login, and what would replace them.
- `active-learning`, a portable learning-coach skill and paired daily Orca
  automation (`automations/daily-learning.md`). The skill talks each idea
  through with the user, checks it against a primary source, and has
  `atomic-note` write the notes and cards they approve. It takes recent
  activity, a source the user hands over, a topic (a frontier of what they
  don't know yet, or picks for free time), a single concept, or a failing
  flashcard. The automation reads the last day's vault changes from an
  Obsidian Headless copy on a paired remote host, local and remote AI
  sessions, and Anki status, uses the shared run history to see patterns
  across days, and takes replies in the run's own chat.
  Its Skill Eval, in `evals/active-learning/`, runs five synthetic cases
  through Promptfoo on macOS. The model is offered write tools but allowed
  only to read, so any attempt to change a file fails the case.
- A chart in `ROUTING.md` of combined quality against cost at each effort
  setting, with each model's best-value effort marked. `scripts/routing/evidence.py`
  computes the figures and draws the chart from the committed data, and the
  repository checks fail when a chart is stale.
- `checking-skill-portability`, a read-only check that a skill package works
  the same in any harness and with any agent that supports the Agent Skills
  specification. It runs the specification's reference validator, then checks
  for single-harness tool names, required harness-only files, missing
  dependencies, and anything tied to the author's machine.
- `PRIORITIZATION.md` explains how the maintainer ranks work by leverage: the
  ICE score with verification effort in place of ease, plus the cost of
  undoing the change, and why both matter when agents do the work unattended.
  Its "Rank by leverage" section is the short rule agents apply. The global
  agent guidance and `managing-issues` each carry a copy, and the repository
  check fails when a copy differs.
- `INSTALLED-SKILLS.md` lists the skills the maintainer installs on every
  machine, with install commands by source and a check that compares a
  machine's lock file against the list.
- Repository text checks reject concrete local home-directory paths, with
  file-scoped exceptions for reviewed portable setup examples.
- `coordinating-work`, an optional Orca-first skill for collaboration setup and
  revive, with editable approval, task-scoped PR workers, and recovery of
  context, communication, and supervision through existing native workflows.
- An automation catalog with prompts, schedules, prerequisites, and Orca setup
  instructions for session, test, CI, codebase design, and coding standards
  reviews. README, workflow, testing, product, and contribution guidance now
  explain how scheduled reviews fit into the working system.
- Shared run state for the automations: every prompt reads and writes one
  private Git repository, cloned on each host, so runs on different machines
  see earlier findings and the owner's decisions. `automations/README.md`
  explains why and carries the run contract as a template to copy.
- A Design system audit automation. Each week it reviews every page, public
  and signed-in, against the design contract using `impeccable`, rendering
  signed-in pages on a throwaway local stack. It recommends drift fixes,
  shared components or page templates, an exact sidecar patch, separately
  labeled design-contract upgrades, and new automated checks for findings
  that keep recurring.
- An Improve audit automation. Each week it surveys the whole codebase with
  shadcn's `improve` skill, run as written across all of its categories, and
  returns every vetted finding in leverage order. Independent review runs
  only on the findings the owner picks in reply.

### Changed

- `repo-captain` now defaults UI/UX briefs (from the Captain or a Domain or
  Design Lead) to `impeccable` (`impeccable context`, `craft-floor.md`, and
  `DESIGN.md`) alongside any applicable platform or framework skills, and adds
  an unattended post-`lfg` `impeccable audit` pass before `worker_done` (no
  user-question pauses, auto-fix verified P0/P1 objective technical findings,
  record the audit result plus any remaining P2/P3 and subjective tradeoffs in
  the pull request body, never commit `.impeccable/` snapshots, and push one
  verified follow-up commit through `ce-babysit-pr` when fixes apply). The
  Captain waits for the recorded audit result for the current head before
  judging a UI/UX pull request ready to merge or hold, and interactive
  `impeccable critique` and `/impeccable live` stay with the Captain or a
  Design Lead rather than unattended Executors.
- Rename `CONCEPTS.md` to `GLOSSARY.md` (with `# Glossary` as the heading) and
  add a root `CONCEPTS.md -> GLOSSARY.md` compatibility symlink so Compound
  Engineering's `ce-compound` reads and updates the same file. Repository
  checks allow only that exact root symlink and continue rejecting symbolic
  links everywhere else.
- The `reviewing-prs` review page stays usable on a large round. Open pull
  requests fall into four groups: held for review, under the hold line,
  dependency bots, and in-flight fleet pull requests, which a worker may
  still be updating. Each overview row shows failing checks, conflicts, a
  hold violation, and the diff's size, and the same marks sit beside the
  Verdict controls on each block. Filters narrow the round to one group or
  to the broken and conflicting pull requests. The sticky bar has a
  `Copy Verdicts` button with a count. `Your Verdicts` now comes before the
  merged lists, which collapse on a large round, and more than five merges
  without the operator share one notice. Routine `review:auto-merged`
  merges are listed apart from unapproved ones, without the orange seal.
  The round's data gains `bucket`, `checks`, `conflict`, `holdViolation`,
  and `merged.autoMerged`; a round without them still renders.
- `reviewing-prs` classifies a trusted-owner pull request with finished
  checks and no hold as in flight, and counts a `Fleet: hold` receipt as
  held.
- Sessions audit is one job on the primary host instead of a remote job
  followed two hours later by a local consolidation job. When a second host
  is paired, the job starts a read-only worker there right after reading
  history, with the agent, model, and effort the job is saved with, and waits
  up to 30 minutes for its summary. The primary host is the only writer of
  `sessions-audit` history, tracks each host's review window separately, and
  judges both hosts' merged findings once. An unreachable or late paired host
  is reported as drift while the primary host's report is still saved, and
  the next run widens only the paired host's window. A single-host setup
  deletes the prompt's paired-host block. Replace both saved Sessions audit
  jobs with one job from the definition.
- `SKILLS.md` now instructs skill authors to ask for approval for authoring's
  model test runs when the work starts, or name the approval in the brief, and
  to stop and ask rather than skip the runs silently when approval is missing.
- `WORKFLOWS.md` and `scripts/sync-global-agents.sh` state that global-guidance
  changes ship as their own small PR right away, never inside other work. When
  `scripts/sync-global-agents.sh --check` fails on a branch that does not edit
  `GLOBAL-AGENTS.md`, its message now tells that branch not to copy the change
  in, without changing when the check passes or fails.
- Improve audit checks the repository's tracker read-only with
  `managing-issues` before saving its report and names each covering open issue
  beside its finding, reporting a coverage gap if the tracker is unreachable or
  results are truncated. Update saved Improve audit jobs from the definition.
- `managing-personal-crm` drops the Grok X sandbox-retry recovery path from
  `references/grok-x-source.md`, so a sandbox network or session-state denial
  marks X unavailable and dependent conclusions `Partial` rather than
  instructing a host-approved retry (which Snyk Agent Scan flagged as `E004`
  Critical Risk on `skills.sh`).
- `reviewing-prs` reads its formats, trust rules, scores, and hold tests
  from the shared review contract. It now posts a verdict even when the
  pull request's head moved after review, naming the reviewed commit and
  telling the operator. It leaves the review request on such a pull request
  open, because GitHub would attach the review to the unreviewed head, and it
  holds an edit to the design system itself.
- The leverage rule's levels are now facts an agent can check. Impact
  scores by severity, with a core task defined as one most users rely on.
  Confidence grades the evidence that the work will deliver its impact, from
  a hypothesis to indirect evidence to direct confirmation. Tests a
  change adds count as new checks. Undo cost 2 means the change reaches shared
  code, shared settings, or many users, or takes more than one revert, and
  undo cost 3 names every stored or published name. The review contract's
  scoring rules are the rule's own four lines, and the repository checks fail
  when they differ. Skill prose now writes "verdict" in lower case and keeps
  `Verdict:` only in the comment format.
- `managing-issues` lets a Captain, under its standing instruction, update
  readiness and workflow labels, tighten Scope and Verification, raise
  verification effort or undo cost, and change confidence from code
  evidence. Lowering either score, changing impact, cancelling, and
  creating follow-ups still need fresh approval.
- `CONCEPTS.md` Merge Approval covers a Captain's charter, and Held Changes
  and verdict point to the review contract.
- ADR 001 pins a merge under a verdict to the head last judged, which may be
  a later head whose change since review the contract judged routine.
- Leverage scoring has two fixed anchors. A new user-facing view, flow, or
  concept scores 3 on verification effort, and any stored or published name
  (table, column, stored ID, event name, or public API) scores 3 on undo
  cost. `PRIORITIZATION.md`'s factor table and the "Rank by leverage" rule in
  `PRIORITIZATION.md`, `GLOBAL-AGENTS.md`, and `managing-issues` carry both.
- Held Changes in `CONCEPTS.md` are now decided by two tests: a list of
  sensitive kinds, which gains CI workflows and composite actions, git-hook
  and secret-scanner configuration, and dependency lockfiles; and a score
  line, verification effort times undo cost of 3 or more, or a diff the
  reviewer cannot read clearly. The higher of the issue's stored scores and
  what the diff shows counts, and repo policy is read from the default
  branch.
- `WORKFLOWS.md` Ship describes Review Rounds and verdicts through
  `reviewing-prs`, the two hold tests, and the three PR review labels.
  `coordinating-work` is unchanged: it still holds on its earlier list and
  writes no labels.
- `managing-issues` asks for a Verification criterion that requires
  before-and-after screenshots, or a named preview walkthrough, on a change
  users will see.
- Sessions audit covers every configured harness, reading Antigravity, Grok,
  and other JSONL transcripts that `ce-retro`'s extractors do not recognize
  through `ce-retro`'s raw-JSONL fallback. Each host now also checks for
  operational drift: failed or missed automations, reverts and same-day fixups
  of `review:auto-merged` changes, crashed or stalled orchestrator sessions,
  expired sign-ins, and installed skills or a main checkout that differ from
  the repository. The new check renumbers the prompt's later steps, so update
  saved jobs from the definition.
- `ROUTING.md` weighs each preference row's sources equally instead of
  following one board. Design/taste averages Arena WebDev, Design Arena,
  21st.dev Design System Bench, and the new Frontier Design benchmark, where
  professional designers vote blind; Writing averages Arena creative writing
  and Lechmazur. Every base suite and preference source is now standardized on
  its own over the charted models it tested, with no anchor suite, and the
  step limit is rescaled from 40% to 20% a point to keep the same trade-off on
  that scale. A setting's score is a plain mean of the suites that tested it,
  with no logit or curve shift, and the page drops the frontier, per-pass cost,
  and two secondary charts. The Team lead row now goes by quality, and the
  Executor row keeps the price order. The better-sibling rule compares two settings only
  on the base suites that tested both, and lists the sibling at its best-value
  effort when that is higher. The routing checks now cover every row, and the
  data is refreshed to 2026-11-24.
- `coordinating-work` ends each standing rule by its own end observation,
  which the Team lead records with the rule and checks at each periodic check,
  retiring the rule by a dated amendment once the observation holds. Workers
  submit heavy jobs straight to a project gate that already queues and admits
  them, and the Team lead limits only heavy work that gate does not meter. A
  worker's merge-ready report now ends its assignment: the worker no longer
  waits for a merged, held, or findings reply. The Team lead sends findings
  and merge-queue ejections as a follow-up to the worker's dispatch, starts a
  new worker in the same worktree when Orca refuses that follow-up, and keeps
  the worktree until the pull request reads merged.
- `MACHINE-SETUP.md` now also verifies Antigravity's `.gemini/config/skills`
  directory alongside Codex and Claude Code.
- `coordinating-work` aligns setup, operation, and revive with Orca v1.4.272
  behavior: recognizing runtime-fixed chat surfaces under persistent agent
  homes, holding still-starting and dialog-withheld workers without treating
  them as failed starts, checking live state on non-stop retry and wait
  notices, respecting automatic restart recovery and restart offers, and
  checking live worker state before replying to unread questions after a
  Team lead replacement. It also simplifies the package by moving worker brief
  rules into `references/briefs.md`, co-locating workspace parentage
  verification and merge defaults in `SKILL.md`, deduplicating shared rules,
  breaking up dense guardrail blocks, and operationalizing vague qualifiers,
  and strengthens the Team lead's batch-level role: settling shared
  cross-issue design constraints before dispatch (recorded alongside standing
  rules and enforced via Verification), checking workers' declared PR choices
  against recorded constraints and open or upcoming assumptions before merge,
  and proposing an optional lower-cost worker tier with an explicit selection
  rule when a batch mixes straightforward and open-ended work.
- `coordinating-work` drops the worker reversibility decision rule in favor of
  `lfg`'s headless behavior, and leaves open-PR branch currency to
  `ce-babysit-pr` and the repository's merge rules.
- The routing checks fail when an Executor or Team lead pick in
  `recommendations.csv` names a different model or effort from the rows the
  method computes, unless the pick is marked as judgment.
- `coordinating-work` records and verifies the Coordinator's workspace as the
  cross-machine parent when Orca cannot create a remote worker workspace as
  a child.
- `ROUTING.md` recommends models for the Team lead, Executor, Design/taste,
  and Writing roles by a written method, reviewed against data read
  2026-11-19. Five benchmark suites from five operators form a measured base
  that covers coding and general work. The page covers four providers:
  Anthropic, OpenAI, Google, and xAI. Each model is listed at its best-value effort, the last
  effort before a step costs more than 40% extra per added point of quality.
  The Executor row starts from each vendor's everyday model and the Team
  lead row from its flagship. Design/taste follows Arena WebDev and Writing
  follows Arena's creative-writing board, each with recorded checks. The
  maintainer's judgment comes last and is marked with an asterisk. The
  Reviewer role leaves the page, since `ce-code-review` covers review in the
  Ship workflow.
- The evidence lives in `docs/routing/`. `results.csv` is append-only: an
  import adds a read and keeps earlier ones, `report --as-of` shows the
  figures as they stood on a date, and `changes` lists what moved since the
  previous read. `role-inputs.csv` records what each source says, and
  `recommendations.csv` holds the picks with their model ids.
- The page shows the recommendations as a figure drawn from
  `recommendations.csv`, whose alt text names every pick; a check fails when
  the two disagree. The charts show combined cost relative to a typical
  FrontierCode setting, name the base suites in a footnote, colour each
  provider by its logo, and mark each best-value effort with a soft ring in
  its line's colour.
- `coordinating-work` leaves branch currency to the repository and holds
  merges while the default branch's latest required checks are failing.
- `CONCEPTS.md` defines one eval vocabulary, shared with Corvly: Product Eval,
  Skill Eval, Eval Case, Eval Label, Eval Record, and Baseline. They replace
  "kept case" and "run record". Tests never call a model; evals always do, so
  Skill Evals run when a skill is created or revised and when a model changes,
  never on every pull request. Skill Evals live in `evals/<skill>/` instead of
  `tests/<skill>/cases/`. `SKILLS.md` lists what each Eval Record holds,
  including models, skill revision, Baseline, cost, each Eval Label, and the
  transcript, so contributors can see why a case passed or failed. Eval Cases
  stay synthetic, and real-use traces stay outside the public repository.
- Renamed the installed skills inventory to `MACHINE-SETUP.md` and added
  install commands and a drift check for Claude Code and Codex plugins and
  MCP servers. Updated the Stripe skills list to match current installs.
- `GLOBAL-AGENTS.md` shapes the 3P update: each bullet opens with its key
  takeaway in bold, each section holds at most three bullets, and each
  problem names what would unblock it and the decision the owner must make.
- `CONCEPTS.md` widens Product Eval to cover a whole conversation, such as a
  live voice practice session, as well as a single reply, matching Corvly.

- The section of `ROUTING.md` on delegating and handing off moved to
  `WORKFLOWS.md`.
- `ROUTING.md` renames the Planner role to Team lead. The role owns the
  outcome: it thinks through the hard parts, hands the rest to Executors, and
  answers for their quality.
- `coordinating-work` calls its lead session the Team lead instead of the
  Coordinator, and says up front that the Team lead is accountable for the
  quality and output of every worker. When a worker's output falls short, the
  Team lead amends the brief, reassigns the work, or does it itself, once,
  before holding. When it does the work itself, it runs the merge-ready watch
  on the new head. Orca's "coordinator" and older records that say
  Coordinator mean the same session.

### Removed

- `docs/model-evaluations.md`. `ROUTING.md` now carries the short version of
  how its table gets updated, so the two files no longer repeat each other.
- `creating-portable-skills`, its signal scanner, and the scanner's tests.
  Claude Code's and Codex's own `skill-creator` now write and revise skills,
  and `checking-skill-portability` keeps the cross-harness check they lack. Its
  evaluation policy and the evidence-integrity rule moved to `SKILLS.md`.
  Uninstall installed copies with
  `npx skills remove creating-portable-skills -g`.
- `checking-simplicity`. In blind tests it added nothing over the global agent
  guidance, and every use started an extra subagent. Agents apply the global
  "Simplicity first" ladder directly, and `ce-pov` gives an independent
  verdict when one is wanted. Update every saved automation job to the new
  prompts first, because a job that still lists the skill as required stops
  when it is missing. Then uninstall installed copies with
  `npx skills remove checking-simplicity -g`.
- `creating-portable-skills`'s `references/evaluation.md` and its routing to
  the evals plugin. Installed copies keep the file until they are updated.
- The scenario table in the `managing-issues` test README. Like the
  `coordinating-work` scenarios, its rows restated the skill's rules, none came
  from an observed failure, and none was ever run. The guard on both skills is
  the skill text plus pull request review.
- The `coordinating-work` scenarios file, `tests/coordinating-work/README.md`.
  A behavioral eval for the skill will be built from real failure traces.
- Two `coordinating-work` worker-brief rules, on repeated review findings and
  security re-review. Each traced to one incident or none.
- The `coordinating-work` incidental-work class. The Coordinator drafts work
  outside the batch's scope as an issue and lists it for the operator.
- Matt Pocock's `retro` from the installed-skills list.
- `repo-gardener`; recurring repository reviews now use Orca automations, and
  approved changes use the existing Compound Engineering workflow.
- Repository-specific GitHub issue forms and the pull request template, so
  issues and pull requests can use freeform bodies.
- `reviewing-ai-sessions`; the Sessions audit automation supplies the recurring
  review prompt directly.
- The custom `creating-portable-skills` evaluation harness, exporter, dedicated
  tests, and runner-specific instructions, along with the speculative cases
  and judges.
- The global agent guidance rule requiring an independent review from a
  different model family for changes to authorization, approval,
  destructive-action guards, money, data deletion, privacy boundaries, or
  release gates. It forced hand-written cross-model reviews, two of which hung
  for 30 minutes waiting on stdin on 2026-11-08, on hosts where Compound
  Engineering's own review already selects a cross-model pass by consequence.
  Projects that need the rule now carry it in their own guidance.

### Changed

- `SKILLS.md` gives a routine for creating a skill and one for when a model
  changes, with a table of the tools each step uses. Creating a skill now
  tests it on three to five realistic requests with and without it, using the
  harness's `skill-creator`, then checks portability. Those requests are kept
  as Eval Cases under `evals/<skill>/` and run again when a model changes.
- Modern Web Guidance telemetry stays on, because its only switch also turns
  off Claude Code feature flags. Supabase's Postgres guidance comes from the
  Supabase plugin instead of a second skills-CLI copy.
- `managing-issues` lists a missing score in the preview, rather than filling
  it, when the caller may not write scores, as in a coordinated batch.
  `managing-personal-crm` and `reviewing-meetings` describe their follow-up
  triggers as one intent instead of a list of verbs.
- `SKILLS.md` owns authoring, evaluation policy, and evidence rules. It names
  the `skill-creator` to use in each harness, warns that the `anthropics/skills`
  copy on GitHub is older than the one claude.ai syncs, and keeps eval cases out
  of the shipped package until a failure returns.
- `coordinating-work` gives each worker one rule for reaching the Coordinator
  instead of three overlapping ones, trims waiting guidance that `lfg` and
  `ce-babysit-pr` already give, and declares where Orca, the Compound
  Engineering skills, and `impeccable` come from, plus the timer that wakes
  the Coordinator's own session.
- `coordinating-work` revive states its default first: each participant resumes
  where it is, with the same workspace, conversation, provider, model, and
  effort. It calls an account change a resume rather than a move, and lets a
  participant stopped by a short limit continue on its own unless the wait
  costs more than a restart.
- The global agent guidance replaces "Choose the best complete solution" with
  "Simplicity first": a three-rung ladder that removes the need first
  (retiring a whole skill, script, workflow, or document you would not add
  today), then uses what exists without extending tech debt, then builds the
  clearest design, judged by the system left behind rather than its size.
- Automations judge their own recommendations and keep the same approval
  list, without a simplicity review per set or a final `ce-pov` call. One
  `ce-pov` call could not reliably return a separate verdict for each
  recommendation in a list.
- `creating-portable-skills` replaces its evaluation workflow with one short
  section, "Improve from real use". The first time a failure appears, the
  author fixes the instruction and the commit says what was observed. A
  pass/fail case is kept only when the same failure returns after that fix.
  Checks test observable behavior, never wording. A skill whose wrong run
  would be costly can get one forward test from a fresh agent, and no runner
  is required. The skill opens with its purpose, working the same across
  harnesses and agents, and credits Anthropic's and Codex's `skill-creator`
  skills. Its audit checklist reports a behavioral case that cannot name the
  failure it came from. `SKILLS.md` asks for trigger validation only after an
  observed routing failure.
- `coordinating-work` describes the Coordinator as a team lead the operator
  talks to. It plans from the tracker's Ready Frontier, makes sure each
  issue's Verification can be proven before dispatch, and may add, replace, or
  narrow an issue's Scope and Verification, listing every edit. A merged pull
  request means its issue is done, so partial work no longer merges with the
  issue left open. An issue scored 3 on verification effort is a held change.
  Workers decide reversible questions themselves and declare deviations in
  the pull request body. A Coordinator acts on another Coordinator's message
  only when it could decide the action alone. Scope is what the operator
  handed over, and a later child of an epic enters it only when the operator
  names or approves it. `managing-issues` is now required.
- `managing-issues` accepts a recorded standing instruction for a coordinated
  batch as authorization for Scope and Verification edits, with stored scores
  kept.
- Automation prompts say what to look for and leave earlier findings to the
  history repository. Optimize CI no longer carries a paragraph of lessons
  from past fixes, which could steer a run toward the answers it was given,
  and the automations README states the rule.
- `coordinating-work` brings in the default branch's merged fixes before
  verification only as the repository's merge policy allows, with examples
  for unpushed and pushed branches.
- `personal-chief-of-staff` keeps only the Frontier Round rules a review
  needs. Questions keep their own order, those whose answers could change the
  recommendation most, rather than leverage order, because a round is not a
  list of work to choose from. A prose pass across the skill removes
  sentences that restated a rule another loaded file owns and clarifies two
  unclear passages, with no change to any rule, limit, order, or approval
  boundary.
- `managing-issues` and the leverage rule settle the passages agents guessed
  at when scoring and creating issues. Undo cost is defined as whether a
  change can be put back as it was, with no git verb in any copy of the rule.
  For impact, users are whoever uses what the repository ships, including the
  owner when it ships the owner's own tools. An agent takes the higher
  value only for undo cost, and scores verification effort by the evidence,
  marked `best guess` when torn. Urgent issues are scored with the same care
  as any other. Only an implementation leaf gets an estimate, so a research,
  decision, or action issue gets none even without children. A create
  recommends the open project that fits best instead of forcing one, and the
  assignee follows a fixed order: the person the request names, then
  `assignee.default`, then the human requester.
- `coordinating-work` builds amendments, as well as briefs and replies, from
  the project's own instructions and the installed guides, so an amendment
  also names only commands confirmed on the worker's host and prefers the
  project's existing helpers to ad hoc tools.
- `coordinating-work` briefs end a worker's assignment and its pull request
  watch, including a delegated watch, on any reply that holds the pull
  request, and no watch runs on a held pull request. A worker waits on its
  watch the way `ce-babysit-pr` says, and ends its turn on any other job only
  when something it armed will wake it.
- `coordinating-work` requires Impeccable within LFG for assignments that
  create or improve UX and UI, including assignments the Coordinator executes
  itself.
- `coordinating-work` requires new task worker workspaces, including later
  waves, to be direct children of the Coordinator workspace and verifies the
  recorded parent after creation, preserving explicit placement and existing
  workspaces while reporting unsupported hierarchy as an exception.
- The final `ce-pov` review in each automation judges every recommendation as
  its own decision. The approval list keeps only the recommendations it
  supports, in leverage order; each one it rejects appears in one line with
  its reason, outside the list, so nothing is dropped silently.
- Automation setup uses Chat mode and explicit model and effort selections
  guided by `ROUTING.md`; the Design system audit follows its Design/taste row.
- `checking-simplicity` readouts allow evidence and protected behavior to use
  clear sentences or short lists, and name the gain and additional work of
  larger redesigns. The compact clean result, three grouped reasons, and
  observable tests for protected behavior remain. Duplicated prose-style rules
  are removed; assessment-only boundaries remain.
- Automations stop and report a missing or unloadable required skill. Skill
  and plugin installation and updates are outside their scope; setup notes
  no longer include installation commands.
- Automation definitions use a consistent opening, with setup instructions
  before the prompt and longer operating notes after it. Sessions audit keeps
  separate remote, local, and single-host instructions. Executable prompts
  are unchanged.
- `checking-simplicity` also triggers before a third fix round for the same
  kind of problem in one mechanism, extending the existing coordinated-work
  trigger to other development sessions.
- Checking Simplicity asks for evidence appropriate to the subject, including
  current implementation or source material for non-code work.
- Automation prompts read private history before assessment and save their
  reviewed reports afterward, preserving each audit's scope and authority.
- Personal CRM routes deferred actions separately from deferred person
  reconstruction and keeps catch-up procedures together. Managing Issues and
  Personal Chief of Staff load setup procedures only on the paths that need
  them, preserving their approval, source-access, and completion requirements.
- Reference documentation separates glossary definitions from owned procedures,
  makes model-selection reasons easier to scan, and marks retired learning
  examples without changing their historical evidence.
- The Design system audit recommends root-cause fixes for recurring findings,
  then suitable safeguards where needed. It recommends lint rules or validators
  only when they can check the corrected behavior reliably.
- Global agent guidance and `checking-simplicity` judge the resulting system
  rather than the smallest patch. They allow wider root-cause fixes when the
  evidence supports a concrete, meaningful improvement, while preserving
  scope and verification requirements. Workflow guidance distinguishes reviewable
  increments and durable safeguards from limits on the solution itself.
  The simplicity skill description explicitly lists “can this be simpler?”, “is this
  simple enough?”, “keep it simple”, and “check for simplicity”; it also names
  workflow reviews and distinguishes assessment from requests for a simple
  explanation. State-machine audit and Coordinator guidance allow complete
  root-cause fixes within approved scope without treating patch size as the
  default. The skill defines elegant design through ownership, data flow,
  and state and branches tied to required behavior, and identifies redundant
  state and design workarounds as candidates for removal.
- The installed-skills list includes Modern Web Guidance with instructions
  to disable telemetry in the installer and agent environment.

- `coordinating-work` routes a planned move of a worker to another provider or
  model to Revive's existing fresh handoff, which carries the brief and its
  amendments after the operator approves the move.
- `coordinating-work` suggests 30 minutes as the starting check interval in
  the setup proposal; the operator still approves the interval. `CONCEPTS.md`
  and `WORKFLOWS.md` now spell "pre-authorized" like the skill.
- `coordinating-work` follows the project's own rule for linking a pull
  request to its issue, and keeps the old no-closing-keyword reference only
  where the project has none. Because a merge may now close the issue, the
  merge checklist compares the pull request's evidence with each verification
  criterion as written, and a criterion met only in part blocks the merge
  unless the issue is linked as unfinished. After a merge the Coordinator
  reads and records the issue's state and closes it through the completion
  check only when the tracker left it open. Workers settle every unapplied
  review finding before asking for a merge, leaving only product or design
  calls for the operator, and the setup proposal names the tracker closing
  the issue among what a merge starts.
- Global agent guidance keeps a pause or hold in force until whoever set it
  lifts it, attributes to the user only their own quoted words and decisions,
  and gives times in the user's named local time zone.
- `coordinating-work` now runs a coordinated batch unattended. Setup proposes
  a merge bar and held changes, and the operator's approval is the
  Coordinator's merge approval. Workers run `lfg` and then `ce-babysit-pr`.
  The Coordinator merges a PR that passes its merge checklist, and leaves
  changes to access, money, deletion, privacy, email, and release gates open,
  along with any PR that carries unapplied review findings. It never waits for
  an answer, keeps one record on its own host, and resumes conversations after
  a same-provider account switch. The Planner role is removed, and a new
  `references/operate.md` covers running the batch.
- Sessions audit uses Compound Engineering's `ce-retro` assessment-only path,
  with host-wide discovery and private shared history owned by the automation.
  It reads history before assessment, carries unread sessions forward, confirms
  causes against transcript evidence and current source, and keeps local CE Retro
  ledgers out of project repositories. Recommendations pass through
  `checking-simplicity` and `ce-pov`; relayed owner answers do not authorize fixes.
- The Analytics gap audit loads `instrument-product-analytics` through the
  PostHog MCP instead of an installed plugin skill.
- Automation prompts review related recommendations together with
  `checking-simplicity`, then use `ce-pov` for the final judgment.
  Recommendations receive fresh review each run, and Improve reviews the ones
  the owner picks; empty
  sets skip simplicity review, and missing reviews remain explicit. The skill
  clarifies coverage of every recommendation in a submitted set and their
  interactions while preserving its independent reviewer and compact readout.
- The two Sessions audit jobs consolidate. The remote job saves its report with
  its Orca session ID and stops; the local job reads it, becomes the remote
  workspace's parent in Orca, and brings the owner one prioritized list across
  both hosts. Only the local job runs the final `ce-pov` after consolidation;
  remote recommendations remain provisional until then. Substantively new
  recommendations created during consolidation receive independent simplicity
  review or remain marked review pending.
- Agents no longer install a skill candidate locally before merge. The
  `coordinating-work` test notes drop their pre-merge install step, the Install
  Probe runs after merge as a maintainer step, and the release checklist has
  the maintainer install from `main` and confirm every bundled helper is still
  executable in the installed copy.
- Global agent guidance permits Compound Engineering reviews through existing
  sign-in accounts after naming the model, while excluding credentials and
  personal data.
- Test audit recommendations have no fixed finding limit, so material findings
  are not omitted to keep the report small.
- Design system audit lists every issue in leverage order instead of the top
  five, and State-machine audit ranks its fixes by leverage.
- `personal-chief-of-staff` weighs how hard a choice is to undo among its
  judgment factors for deciding what deserves attention.
- `managing-issues` scores every issue it drafts or updates on impact,
  confidence, verification effort, and undo cost, shows the scores in the
  approval preview, and stores them in the tracker: Number issue fields on
  GitHub and single-select label groups on Linear. Priority and a leaf's
  estimate are derived from the scores, and derivation never sets, changes, or
  clears urgent. The Ready Frontier is listed in leverage order.
  `.agents/managing-issues.json` moves to version 3: it adds a `scores`
  mapping and fixes the priority and estimate names, so neither may be empty.
  On Linear each priority name maps to itself.
  A version 2 config is not migrated. Reads and drafts keep working, and the
  first write asks for setup to replace the file.
- Global agent guidance lets an agent merge a pull request when the user asked
  for the merge, in the task or in standing instructions, and its required
  checks pass with no open review thread. Deploying and force-pushing still
  need the user, and repository guidance can grant exceptions only for spending.
- `coordinating-work` assignment briefs name only commands confirmed on the
  worker's host, carry current decisions rather than declined proposals, and
  ask workers to wait for long-running checks inside their own turn. Operator
  decisions go to their owning record before the Coordinator acts on them.
- `coordinating-work` starts task workers through Orca's supervised launch,
  so the runtime can flag a worker that stops without reporting, and revive
  tells a worker with an open assignment to continue it in the same turn.
- `coordinating-work` freezes an assignment's brief once it is dispatched.
  Only the Coordinator changes it, through a dated amendment that names what
  it supersedes, and each worker re-reads its amendments at every step
  boundary and names in its reports the latest one its work follows. Revive
  carries the brief with its amendments, and the resumed worker confirms the
  latest one.
- `coordinating-work` starts each assignment on a fresh branch from the
  latest default branch and has workers update their branch before each
  verification run, names the message type for questions, blockers,
  completions, and progress.
- `coordinating-work` uses one session-owned periodic check to reconcile
  worker state, answer questions, resume waits that ended, and dispatch ready
  work. It preserves operator holds and creates no second Coordinator. It
  confirms that an idle participant read a message and reads the effective
  account from the running agent rather than launch metadata. Briefs say a
  returning helper skill does not end a worker's turn, and on a shared host
  heavy jobs are limited by measured CPU and memory. Cleanup checks unpushed
  work against the default branch and pull request head, not the upstream
  alone. Revive lists background jobs and relaunches only those confirmed
  stopped unfinished, lets running paid work reach an idle point, and checks a
  usage-limited participant's background jobs before reassigning it.
- `coordinating-work` briefs ask that a security re-review prompt state its
  threat model, and that a worker whose last two review rounds found only new
  instances of one class fix that class structurally or ask the Coordinator,
  instead of patching each new instance.
- `coordinating-work` setup adopts an agent already working on the objective,
  such as a chat started for a batch. When the guide cannot attach a
  supervised Task to it, the Coordinator keeps it as a message-assigned worker
  reached through the guide's reference lookup and includes it in the periodic
  check.
- `coordinating-work` setup inspects every execution host the guide can reach
  and recommends where heavy workers run, preferring a reachable host kept for
  development work over the operator's own machine. The proposal shows the
  measured CPU and memory behind the recommendation, and the operator chooses
  the placement.
- `coordinating-work` briefs invoke the CE skill that owns an assignment by
  name instead of restating its steps, and say that the task asks for the
  subagents and helpers that skill starts. A runtime's worker instructions can
  forbid subagents unless the task asks, which made a worker skip the skill's
  own reviewers.
- `personal-chief-of-staff` finds a source map moved into a designated vault
  or workspace through an approved pointer in an instruction or configuration
  file the host loads for that workspace, after any location the caller
  supplies. A named location that cannot be read is a gap rather than a
  reason to use the default, and moving the map proposes removing the previous
  copy. Vault-owned maps are `.json` files read
  and saved through the Obsidian CLI, and `reviewing-meetings` reads a supplied
  map through its owning system the same way.
- Global agent guidance tells a delegating agent to rely on a delegate's watch
  and to report a merge-queue enqueue instead of polling it. The paid-call
  exception for live browser testing moves to the repositories that grant it;
  the rule to mock models in automated tests stays global.
- Repository agent guidance points skill changes to the package and evaluation
  policy, and directs implementation and debugging to relevant prior solutions.
- Managing Issues explicitly checks a newly created Linear issue's parent,
  direct children, and other relationships before continuing an approved batch.
- Model routing explains cost per pass and effort gains, separates evaluation
  sources from role selection, and distinguishes calculation inputs from
  supporting evidence. Current recommendations record subscription and access
  overrides and identify provisional Planner choices.
- Setup and automation guidance calls for initial setup or recovery and repeat
  operation checks in the first implementation slice, with pending activation
  tracked explicitly.
- Testing guidance names the repository-owned commands as completion evidence
  and asks filtered check output to keep the check's own exit status.
- Checking Simplicity no longer requires four options for every question.
- Creating Portable Skills reviews flag opaque prose: instructions a new reader
  cannot follow, internal classifications, and security jargon.
- Managing Issues tests no longer match the skill's text. The phrase checks and
  the graph and lifecycle case rows are removed, and the configuration
  validator test stays.
- `GLOBAL-AGENTS.md` matches the maintainer's current global guidance.
  Non-trivial work names a verifiable end state without a completion
  template. Long work uses the workflow's durable task state, and scratch
  work stays disposable. The published copy no longer specifies a work-folder
  checklist, a headless `ce-compound` pass, or a version-control section.
- `GLOBAL-AGENTS.md` asks agents to judge a check by its own exit status,
  since a filtered pipeline such as `check | tail` reports the filter's status
  unless `pipefail` is set.
- `SKILLS.md` lists what retiring a skill includes, including closing or
  re-scoping its open issues in the same change.
- Personal Chief of Staff fixture checks validate the shipped source-map
  sample directly instead of a test-only copy of the schema.
- Repository docs keep one owner per rule. `creating-portable-skills` owns
  evaluation policy, and the other docs link to it; `SKILLS.md` keeps only this repository's evidence rules. `CONCEPTS.md`
  drops ten terms used in at most one other file and states what checks
  Installation Parity. Stale pointers, a restated sync-script header, and a
  duplicate `checking-simplicity` summary are gone. `SKILLS.md` notes that
  this repository rejects `allowed-tools` and adds uninstalling from each host
  to retiring a skill.
- Automation schedules all use America/Los_Angeles, and starts on the same
  host sit at least an hour apart (Weekly codebase design moves to Saturday
  04:00). Test audit runs `ce-simplify-code` as a report of what it would
  change, ordered by priority, instead of applying fixes. The README lists
  Analytics gap audit. CI no longer installs PyYAML, which no
  Python check imports.
- `managing-issues` analyzes the project for every issue with priority,
  labels, estimate, and readiness, and fills the assignee in a fixed order.
  It leaves either one empty only with a stated reason. When the request and
  evidence do not settle an input, it asks the requester, naming the field,
  the candidates, and its lean. A run that cannot ask applies the lean and
  marks it `best guess` for a person to correct. An implementation leaf gets
  an estimate whatever its readiness, and a create preview is not executable
  while a leaf's estimate, the project, or the assignee is empty without a
  stated reason.
  `.agents/managing-issues.json` accepts two optional keys,
  `"assignee": { "default": "<login or user>" }` and
  `"project": { "required": true }`. A config without them stays valid; no
  configured default assignee applies and a project is not required.
- The Optimize CI prompt counts local Verify as part of CI. Each report now
  carries a hosted section, pull-request runner minutes per merged pull request
  by one fixed method, and a local section, Verify duration per suite, reuse of
  saved results and failed attempts on the host that ran them. The measurement
  harness moves into the private automation-state repository so every host
  gets it by pulling, while its downloaded responses stay in a per-host cache.
  The prompt also records what a series of local Verify fixes taught.

### Fixed

- A double quote inside a Verdict note no longer ends the posted
  `Notes: "..."` line early. The review page and step 5 of `reviewing-prs`
  change inner double quotes to single quotes.
- `reviewing-prs` settles a question for the operator during the round and
  keeps it out of the posted `Notes:` line.
- The review page says so when a note is typed with no Verdict chosen,
  instead of dropping it silently, and no longer scrolls sideways on a
  narrow or zoomed screen.
- `repo-captain`'s wake timer no longer leaves the Captain looking busy in
  Orca between wakes. Orca keeps a session `working` while its harness
  reports unfinished timer work, so operator messages waited for Steer, which
  could cancel the timer. Antigravity now arms a daemon cron. Claude Code and
  Codex, whose own timers all count as unfinished work, run a detached loop
  that types the wake prompt into the Captain's own terminal. The timer is
  recurring, so each wake checks it is still running instead of re-arming it.
- The `reviewing-prs` review page no longer shows a V × U of 9 for a pull
  request missing a score. It still holds that pull request at the top of the
  held group, shows the real verification effort × undo cost or `?`, and says
  the pull request is held because a score is missing.
- The Verification effort row in `PRIORITIZATION.md`'s factor table again
  lists a new user-facing view, flow, or concept as an example of a 3, matching
  the `Rank by leverage` copies, instead of saying it always scores 3.
- `reviewing-meetings` accepts a Granola-returned meeting URL when its scheme,
  host, and path match the canonical `https://notes.granola.ai/d/{native_id}`
  URL, ignoring any query string or fragment (such as `?utm_source=mcp`), while
  still rejecting a different scheme, host, or path as contradictory and keeping
  the canonical URL without query string or fragment as the stored source URL.
- Coordination guidance distinguishes an operator-approved proposal amendment
  from a worker-brief amendment, identifies the replacement-Coordinator
  confirmation by name, and puts non-consuming inbox reads in the periodic
  check. Storm Research uses one placement rule for research limitations,
  preserves calibrated uncertainty, and identifies who maps confidence levels.
- The opt-in `GLOBAL-AGENTS.md` freshness check compares the configured source
  with the copy on `origin/main`, and with `HEAD` only when the branch edits the
  copy. Branches started before the copy was refreshed on `main` no longer fail.
- `coordinating-work` asks for operator decisions to be recorded in their
  owning record, says a worker's question is sent with the `ask` command, and
  has workers wait for long-running checks with a tracked background wait.
  The automation run contract template no longer calls itself canonical.
- Automation prompts now tell each run to update the shared run-state
  repository and follow its README, which owns the run contract. The README
  template names reports in UTC with seconds, matching the live contract.
- Repository verification bounds malformed inline-link scanning and treats YAML
  filenames as data. Guidance synchronization replaces destination symlinks
  safely, skill scans preserve pathname boundaries, and evaluation imports
  reject nonregular or oversized setup records.
- Managing Issues reads back a new Linear issue's relationships. A
  relationship Linear adds on its own, which nobody approved, stops the batch
  before the next write and comes with a removal preview awaiting approval.
- Repository verification rejects tracked files under the root `outputs/`
  and `tmp/` directories, which may hold private generated artifacts, and
  `.gitignore` ignores both.
- Repository tests now fail when the issue-configuration label, duplicate,
  control-character, or size guards are removed, when the README skill list
  or a skill name drifts from `skills/`, or when a test runner is missing from
  the fixture roster.

## [0.3.0] - 2026-10-15

This Release Snapshot records the catalog at one validated state. Ordinary
installs continue to follow rolling `main`. Before `1.0.0`, skill interfaces
and workflows may change between releases.

### Added

- `checking-simplicity` assesses safe ways to simplify a design, plan, codebase,
  or in-progress approach through one independent, read-only reviewer. It also
  handles explicit mid-build simplicity checks and proposed durable machinery
  that is not justified by the current need.
- `reviewing-ai-sessions` reviews session history for recurring friction and
  proposes evidence-backed changes to skills, rules, and enforcement. Maintain
  includes the review; applying specific proposals requires approval.
- `GLOBAL-AGENTS.md` publishes the maintainer's global guidance. The one-way
  sync script and opt-in pre-push freshness check keep it aligned with the
  configured local source.
- `SKILLS.md` defines repository package conventions and the evaluation workflow.
  A bounded `creating-portable-skills` suite uses stock Promptfoo providers for
  activation and a read-only portability audit in Claude and Codex. Subjective
  judgments remain provisional; strict capture and human calibration remain
  Unmeasured, and other packages await revalidation.
- `TESTING.md` explains project-owned verification, agent permissions,
  end-to-end checks, independent review, cache boundaries, and durable safeguards.
  New README and workflow illustrations introduce Huginn and Muninn and show
  delivery, maintenance, and learning.

### Changed

- `managing-issues` uses one canonical GitHub or Linear tracker for issue
  updates, parent and blocker relationships, readiness, and completion.
  First-use setup recommends an exclusive Linear readiness group and GitHub
  prefixed labels; existing configurations are not migrated. Explicit prior
  approval can cover routine reversible bookkeeping and predictable provider
  automation, while complete previews, readback, and approval for expanded
  scope remain required.
- `personal-chief-of-staff` provides guided source setup and a fictional starter
  map through host file tools. Version 3 maps roles to sources with optional
  harness access overrides; existing version 1 and 2 restrictions remain until
  an approved upgrade. Source examples distinguish templates, completed reviews,
  meeting evidence, approved notes, contact lookup, and durable records.
- Chief-of-staff wind-down separates approved corrections from tomorrow's
  planning and journal drafting. Daily and weekly reviews reconcile overdue,
  waiting, carried-over, and conflicting commitments; upcoming work feeds the
  plan. Coaching uses bounded Frontier Rounds, and Source Access Audits give
  concise coverage and claim limits.
- `creating-portable-skills` follows the Agent Skills format and delegates
  evaluation and corpus retuning to pinned upstream `build-eval` and `ce-retune`
  guides. Repository conventions remain in `SKILLS.md`. The review checklist
  and bundled signal scan support portable guidance without importing host
  procedure; required independent judgments cannot be supplied by the author.
- Repo Gardener uses a short policy with `protected_paths`, `max_pull_requests`,
  `scans`, `verify`, and optional `report_issue`. It senses one repository and
  dispatches bounded Executors through Compound Engineering publication and
  babysit; humans merge. Missing policy yields sense-only operation and an
  interactive setup proposal, with a later approval required before writing.
- Public X reads in CRM and chief-of-staff prefer Grok CLI when it provides the
  required capability and accept user-confirmed handles. A configured read-only
  API remains an alternative within the caller's limits.
- `ROUTING.md` is a human-facing role playbook; `WORKFLOWS.md` owns the workflow
  walkthroughs and `docs/model-evaluations.md` owns model-evaluation procedure.
  Ranked rows offer at most one model per provider. Gemini 4 Argon is provisional
  for Planner and Design/taste; Executor retains Opus 5.5 and Sol 6.1 without a
  tertiary. Evaluated effort and the maintainer's usual usage stay distinct.
- Working plans, brainstorms, raw dogfood notes, and point-in-time reports stay
  ignored. Durable outcomes belong in code, canonical docs, issues, ADRs, or
  maintained solutions. CI tool bootstrapping runs from a script to avoid an
  actionlint/ShellCheck pipe-buffer deadlock.

### Fixed

- Chief-of-staff reviews keep supplied results unverified, explain excluded
  source calls, and finish relationship judgment, task and inbox reconciliation,
  action dispositions, and calendar decisions before claiming completion.
- CRM uses bounded supported contact lookup after an empty unsupported phone
  search without weakening identity binding. Public X sandbox recovery requires
  fresh host approval and unchanged public query scope; turn exhaustion remains
  final, and unavailable reads retain Partial coverage.
- The portable-skill signal scan detects attached pressure markers, preserves
  whole-word text matching, and counts each matching line once. Unreadable
  inputs or reference traversal failures return errors instead of incomplete
  successful scans. The checklist keeps factual domain sentences even when
  they contain change words.

### Removed

- `checking-pr-readiness` and `checking-merge-readiness`, their helpers, and
  dedicated tests. Use Compound Engineering publication and babysit directly;
  Repo Gardener preserves verification, allowed-file boundaries, and human merge.
- `route-work`, introduced and retired between snapshots, and its bundled routing
  contract. Use `ROUTING.md` and invoke the chosen workflow or orchestration tools
  directly. For these three retired skills, interactive `npx skills update`
  detects upstream removals and offers to remove tracked local installations.
  Manually installed copies require separate removal.
- Repo Gardener's managed-run protocol, tracker records, scripts, and separate
  Executor contract. Existing `.agents/repo-gardener.yaml` files need the new
  policy keys; `maximum_workers` becomes `max_pull_requests`.
- Legacy behavioral suites, trigger lists, benchmarks, custom eval runners,
  schema checks, review server, cost tools, and simulators. Historical evidence
  remains in Git, but does not validate the replacement suite. Deterministic
  shipped-helper checks and safe synthetic fixtures remain.

## [0.2.0] - 2026-08-14

### Added

- Added the public OSS foundation: documentation, an MIT license, community
  templates, private security reporting, and a maintainer release checklist.
- Added a shared Lefthook `pre-push` check group and a read-only GitHub Actions
  workflow with the required check name `Tests Status`.
- Added repository and workflow banners with optimized GitHub display assets.
- Added `managing-issues` for GitHub and Linear issue relationships, readiness,
  approved updates, and evidence-based completion checks.
- Added `repo-gardener` for scheduled repository-health reviews that may carry
  one bounded improvement to an unmerged pull request.
- Added `storm-research` for source-backed research through independent
  practitioner, academic, skeptic, economist, and historian perspectives.
- Added `checking-merge-readiness` for a read-only whole-change review and a
  merge, debug, or do-not-merge recommendation.
- Added `checking-pr-readiness` for comparing a finished branch with its plan,
  checking the evidence, and surfacing unresolved risks before a pull request.
- Added `creating-portable-skills` for creating, revising, testing, and
  verifying the installation of skills across supported agent tools.
- Added `personal-chief-of-staff` for daily wind-down, weekly, and quarterly
  reviews with source checks and approval before changes are written.
- Added `managing-personal-crm` for relationship context, conversation prep,
  follow-ups, and staged note cleanup without a separate CRM database.
- Added `reviewing-meetings` for turning completed meetings into grounded notes
  and independently approved follow-up actions.

### Changed

- Expanded `WORKFLOWS.md` into the seven-job playbook and made the README the
  single public catalog for individually installable skills.
- Standardized skill tests around trigger contracts, runnable behavioral cases,
  concise run logs, matched comparisons, and per-tool installation checks.
- Defined `main` as the rolling install source and semantic-version Release
  Snapshots as immutable historical checkpoints rather than install pins.

## [0.1.0] - 2026-07-10

### Added

- Repository scaffolding: community files, issue and pull-request templates,
  the skills catalog layout, and the seven-job workflow map.
- The first repository rules for a curated catalog, rolling `main`, and
  installation parity.
