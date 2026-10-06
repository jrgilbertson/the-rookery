# Use Promptfoo for portable skill evaluations

Status: accepted.

The creating-portable-skills suite uses Promptfoo's built-in native providers for execution, result export and review. The five case definitions, synthetic fixtures, read-only file comparator and criterion-specific judge prompts remain the evaluation contract. Promptfoo is pinned so native provider behavior can be checked before dependency upgrades.

The previous bespoke capture checker, native graph parser, private launch controllers and review servers required substantial maintenance unrelated to skill evaluation. Keeping them as an optional second execution path would preserve that burden and make it unclear which results are current. Remove replaced implementations; Git history and private historical evidence preserve past work without creating a runnable legacy dependency.

Native subscription authentication remains distinct from API-key execution. Prepare disposable workspaces and native state outside the repository, use the existing approved credential store, and do not introduce a paid API fallback. Codex and Claude configurations are separate. A configured host is not evidence that its live evaluation succeeded.

The suite uses the stock Codex SDK provider and ordinary Promptfoo assertions.
A final answer is required, and skill-used/not-skill-used observations are checked
against the activation cases. Codex's command-path heuristic does not establish
exact instruction loading, package identity or complete capture. Negative
observations do not prove absence. These limits are reported rather than repaired
with a private upstream fork or a custom trace admission layer.

Native read-only permissions constrain writes, not every read. Strict provenance
is not collected and remains Unmeasured; historical incomplete captures remain
Unmeasured. Remove the replaced parser and admission hooks rather than retaining
a second runnable approach. Generated state and results remain private.

Audit C3 continues to compare the supplied files objectively. Audit C1, C2 and C4 use separate provisional LLM judgments with preserved evidence and synthetic challenges. Human alignment remains Unmeasured until independently labeled held-out examples support calibration. Activation grades do not evaluate the quality of a generated skill.

A dependency upgrade must recheck native authentication, configuration forwarding,
skill-use observations, unavailable-output controls, and private storage behavior.
A future need for strict provenance or additional native harnesses must be assessed
separately. This suite does not own upstream runtime test failures.

Provider references: [Codex SDK](https://www.promptfoo.dev/docs/providers/openai-codex-sdk/) and [Claude Agent SDK](https://www.promptfoo.dev/docs/providers/claude-agent-sdk/). Suite commands and current verification boundaries live in the [suite README](../../tests/creating-portable-skills/README.md).
