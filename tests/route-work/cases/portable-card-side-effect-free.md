# An issue-backed route produces a concise side-effect-free kickoff

Provenance: user feedback — the route must include a plain-text statement a
receiver can paste to start work without duplicating its source artifact or
making the router perform downstream work.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, you may read its installed
> package; call no other tools. Route this synthetic request using only the
> text below. GitHub issue
> `https://github.com/example/parser/issues/97` contains approved requirements
> for a parser fix but no execution plan. The issue is the source of truth. The
> plan may be written in the repository, but no implementation, issue mutation,
> commit, push, pull request, or publication is authorized. Model availability
> is unknown.

## Expected behavior

- [ ] Returns exactly one response beginning with the plain line `Route`. The
      workflow is `ce-plan` and the topology is Single owner. No Markdown.
- [ ] The route uses natural sentences, names Fable 5.1 at medium for one planner,
      and says to continue in the current worktree without structured
      orchestration. It does not emit `Orca None` or `availability unverified`.
- [ ] A `Copy/paste kickoff` section follows as plain text, not a fence,
      beginning with a natural instruction to start `ce-plan` from the supplied
      GitHub issue, and names the selected model and effort.
- [ ] The kickoff treats the issue as the source of truth and preserves the
      supplied planning and authority boundary in one concise sentence. It does
      not restate the issue or use the old `Objective`, `Done when`, `Facts`,
      `Constraints`, `Evidence gaps`, or `Authority` field list.
- [ ] The trace contains only reads of the installed package: no issue fetch,
      downstream invocation, planning, mutation, scheduling, monitoring, or
      persisted route state.
