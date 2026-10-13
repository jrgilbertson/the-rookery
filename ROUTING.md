# Match the model to the work

Choose models and effort for the work, using the tools and subscriptions available to you. [WORKFLOWS.md](WORKFLOWS.md) covers the workflows themselves.

## What each role needs

### Planner

Settle scope, dependencies, and acceptance criteria. The session planning the work can also coordinate it; Planner names a model profile, not an extra agent.

### Executor

Implement or debug work against concrete checks. Balanced effort is the starting point; more thinking needs a workload-specific reason.

### Reviewer

Judge the result against the criteria in a fresh context. For correctness review, use the first available Executor model from a different provider than the implementer, keeping its Executor effort. If only one provider is available, use a fresh review context. Taste-led review follows the Design/taste recommendations.

### Design/taste

Judge the finished interface. Visual-preference evidence informs the choice; inspect the actual result rather than assuming higher effort improves it.

## Model recommendations

**Last reviewed: 2026-10-13**

| Work | Primary or rule | Secondary | Tertiary |
|---|---|---|---|
| Planner | Anthropic / `claude-opus-5-5` / high | OpenAI / `gpt-6.1-sol` / high | Google / `gemini-4-argon` / high |
| Executor | Anthropic / `claude-opus-5-5` / medium | OpenAI / `gpt-6.1-sol` / medium | — |
| Reviewer | [Different-provider Executor](#reviewer) | — | — |
| Design/taste | Anthropic / `claude-opus-5-5` / max | OpenAI / `gpt-6.1-sol` / max | Google / `gemini-4-argon` / high |

Design/taste recommendations follow available evals and list tested efforts, though I typically run these models at their Executor or Planner effort levels.

Argon's Planner and Design/taste recommendations are provisional. Each ranked row contains at most one model from each provider; empty slots are allowed.

## Work alone, delegate, or hand off

One session usually owns the work and stays accountable for completion. Add Executors when the work has independent units. Use the installed orchestration tools when those units need supervision; use a handoff when another session should take ownership.

## Adjust effort and availability

Choose models for how success will be judged, then adjust for the tools and subscriptions available to you. Planning needs reasoning and decomposition; execution needs correct changes; review needs independent judgment; design needs a finished result worth using.

Start with the table's effort and adjust deliberately. Higher effort needs to earn its time and usage. API benchmark costs do not predict subscription quotas. My preference is to use official provider tools with subscription authentication.

## Evidence and upkeep

- Planner: Opus high and Sol high retain a useful reasoning/cost balance. Argon high adds an alternative provider; direct planning evidence remains limited.
- Executor: Opus medium and Sol medium balance repository quality, cost, and time. Argon's observed coding cost does not justify an unconditional fallback slot.
- Design/taste: Opus max and Sol max reflect evaluated visual-preference configurations. Argon high has preliminary frontend evidence. Matched quality, cost, and time across effort levels remain incomplete.

Current evidence includes [FrontierCode](https://cognition.com/frontiercode), [AA coding-agent comparisons](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-codex), and [Arena Frontend](https://arena.ai/leaderboard/code/webdev/frontend).

Recheck exact releases against independent evaluations relevant to the role. Compare quality, task cost, and time; do not treat missing results as poor performance or maximum effort as automatically best.

Update the table, review date, and rationale together. The [evaluation procedure](docs/model-evaluations.md) covers sources, effort comparisons, and provisional choices.
