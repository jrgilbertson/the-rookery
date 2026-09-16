# Testing with agents

Fast feedback lets an agent fix a failure while the change is still in context.
Use that advantage locally, keep merge requirements independently enforced in
CI, and put broader validation before the point where a change reaches users.
Each repository owns the commands and the division of work between those
stages.

## Polyglot monorepos

A monorepo can give a team shared company context: code in several languages,
schemas, prompts, documentation, and working files can move through version
control and review together. A change that crosses these boundaries can be
reviewed and committed as one change. That is useful when several agents work
on the same product.

This fits teams that benefit from atomic review across those boundaries; other
organizations may need separate repositories. Shared version control still
needs explicit ownership, appropriate access controls, and ways to find
context. A dependency graph can follow declared packages and supported imports;
it does not understand every HTTP interaction, database contract, or document's
meaning. Runtime-read Markdown and executable documentation belong to
verification inputs. Ordinary team prose need not trigger application tests
when its independence is established.

These principles also fit a small single-language repository. Use the existing
runner directly when a project graph would add little value.

## One project-owned entry point

Give people and agents the same commands for selected verification, full
verification, and inspecting what will run. Keep selection and task ordering
with one coordinator. Nx is one option for a polyglot monorepo; Vitest, pytest,
Playwright, and other runners still execute the tests.

Let package manifests, imports, runner conventions, and executable task
configuration supply dependency and test discovery. Adding a matching test
should not require updating a second file-to-test list. Model necessary service
and runtime boundaries at the suite level. Unknown ownership, missing or
deleted dependency edges, and opaque runtime dependencies must broaden
coverage. Unreadable graphs, unavailable comparison revisions, or failed
discovery must fail visibly, never report a green empty selection.

Start with full suites for affected projects and their dependents. Use a
runner's narrower selection for the edit loop when useful, while keeping the
required project checks clear. A graph gives conservative impact information;
it does not prove that an apparently unrelated change is harmless.

Put deterministic enforcement in repository commands, Git hooks, and CI so
Grok, Claude, Codex, and other harnesses follow the same rules. The
repository's commands work without AI lifecycle hooks. Git hooks can be
bypassed, so required merge guarantees also need independent CI enforcement.

## Local, merge, and release responsibilities

| Stage | Responsibility |
| --- | --- |
| Editing | Run focused checks immediately, then the affected projects’ required suites and checks locally before handoff. |
| Commit | Keep checkpoints cheap enough to use regularly. |
| Merge | Independently enforce the repository's selected requirements in CI. A local success assertion is not a replacement. |
| Release | Run full, fresh validation of the exact candidate before any production mutation. |

For a web product, one allocation is full browser coverage locally and at
release, with selected unit, contract, integration, and security checks in PR
CI. This keeps immediate feedback substantial and merge gates lighter without
letting local results substitute for those gates. The project owns this
allocation and explicitly accepts the detection delay for coverage deferred
from merge.

A team that releases periodically can accept broader discovery at release
preparation. A repository that deploys every merge needs consequential gates
before that deployment. Choose the boundary from the actual delivery model;
weekly releases and scheduled full runs are not universal requirements.

Resolve selection before expensive task-specific setup. Reuse an install,
generated build, or temporary service lifetime where compatible checks can
share it safely. Give that runtime one owner for setup, use, and teardown. A
reusable workflow or composite action shares code, but each job may still pay
the setup cost. Keep separate environments where database state, credentials,
or isolation require them.

## Cache successful computations carefully

Cache deterministic tasks only after proving their inputs and outputs. Include
relevant source, tests, dependency and tool versions, configuration,
environment values, and runtime-read assets. Verify that changed inputs
invalidate the result and that required generated outputs are restored.

Start with isolated local caches. Shared or remote caching is a separate choice
with its own trust and maintenance costs. Stateful checks against changing
external services, database integration, migration replay, and live browser
behavior execute freshly. A cache hit is evidence of an earlier successful
computation, not proof of a fresh run.

Distinguish fresh success, cached success, intentional exclusion, failure,
cancellation, and required work that did not run. Provide a direct cache-bypass
command for diagnosis. An observed unresolved failure stays blocking even when
an older successful cache entry exists. Full release validation executes
freshly; dependency download caches can remain without replacing clean-install
proofs.

## Handle failures without losing ownership

Record the failing command, revision, and relevant environment. Bound diagnosis
by comparing the exact unchanged base under comparable conditions. A matching
base failure establishes a repair candidate; it does not prove the new change
harmless.

Check whether a repair already has an owner. Propose the repair scope and
owner, and obtain separate approval before expanding the work. Independent work
can continue, but merge waits for repair and passing required checks on the
updated branch. Repeated retries and quarantine are policy decisions, not an
agent's way to manufacture success.

## Adopt through a verified cutover

Compare the old and new paths during implementation on the same controlled
revisions. Exercise new tests, new imports, deletions, shared inputs, cache
invalidation, and injected failures. Record intentionally excluded work
separately from missing guarantees.

Measure local cold and warm feedback, CI elapsed time and runner-minutes, setup
cost, and unnecessary investigations. Report ordinary application changes
separately from cheap documentation changes. Bound this comparison within
implementation. Once correctness and the intended improvement are established,
make one permanent cutover: switch entry points and remove the old selectors
and coordination. Acceptance is based on evidence, not a trial period or
recurring execution of both systems. An ordinary version-control revert
provides rollback without a permanent second operating mode.

## Project policy outline

Use this outline in the project's existing testing owner. Fill it with links
and decisions rather than a copied task inventory.

- **Commands:** point to the canonical command and its selected, full, inspect,
  and cache-bypass usage.
- **Executable owners:** point to the coordinator and runner configuration that
  discover projects, dependencies, tests, and cache inputs.
- **Delivery boundary:** name what local work, merge, and release must establish,
  including any deliberately deferred coverage.
- **Resources:** point to the owner of temporary services, worktree isolation,
  and concurrency limits.
- **Failures:** point to the repair owner and the policy for known failures and
  revalidation.

For a TypeScript/Python monorepo, these pointers may lead to one graph and
several native runners. For a small Python library, they may lead to its
existing test command and CI configuration. Neither example needs a second
dependency list in this document.
