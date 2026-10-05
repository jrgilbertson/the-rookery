# Use Promptfoo for portable skill evaluations

Status: accepted.

The creating-portable-skills suite uses Promptfoo's built-in native providers for execution, result export and review. The five case definitions, synthetic fixtures, read-only file comparator and criterion-specific judge prompts remain the evaluation contract. Promptfoo is pinned so native provider behavior can be checked before dependency upgrades.

The previous bespoke capture checker, native graph parser, private launch controllers and review servers required substantial maintenance unrelated to skill evaluation. Keeping them as an optional second execution path would preserve that burden and make it unclear which results are current. Remove replaced implementations; Git history and private historical evidence preserve past work without creating a runnable legacy dependency.

Native subscription authentication remains distinct from API-key execution. Prepare disposable workspaces and native state outside the repository, use the existing approved credential store, and do not introduce a paid API fallback. Codex and Claude configurations are separate. A configured host is not evidence that its live evaluation succeeded.

Capture validity precedes behavioral grading. A missing or incomplete trace is Unmeasured, including for a case expecting no activation. Discovery metadata and failed loads do not prove activation. A successful instruction-body read must identify the exact frozen package. Promptfoo's path-based skill-used assertion is a useful observation, but alone does not establish package identity or capture completeness. Unsupported tool evidence remains Unmeasured.

This boundary measures the case's observable native execution; it does not certify all filesystem reads or authenticate operator-supplied artifacts against a malicious recorder. Native read-only permissions constrain writes, not every read. Report those limits instead of importing the old recorder's receipt schema into the replacement.

Audit C3 continues to compare the supplied files objectively. Audit C1, C2 and C4 use separate provisional LLM judgments with preserved evidence and synthetic challenges. Human alignment remains Unmeasured until independently labeled held-out examples support calibration. Activation grades do not evaluate the quality of a generated skill.

A dependency upgrade must recheck native authentication, configuration forwarding, raw event retention, exact body-load evidence, missing-capture controls, and private storage behavior. A future need for container benchmarks or additional native harnesses should be evaluated separately rather than adding another custom runner here.

Provider references: [Codex app-server](https://www.promptfoo.dev/docs/providers/openai-codex-app-server/) and [Claude Agent SDK](https://www.promptfoo.dev/docs/providers/claude-agent-sdk/). Suite commands and current verification boundaries live in the [suite README](../../tests/creating-portable-skills/README.md).
