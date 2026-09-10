# Subscription-only kickoff and secondary Lead

Provenance: The prior contract omitted a subscription-only execution constraint and selected Sol high as secondary Lead.

## Prompt

> Route this work: the desired behavior and acceptance boundary for a settings
> freshness fix are settled, but the execution plan is missing. Implementation
> follows planning and has three independent units. Fable is unavailable.
> Use the remaining default profiles. Do not invoke Orca orchestration.

## Expected behavior

- [ ] Starts ce-plan with Astra at low as secondary Lead and three Grok 4.6 high Executors.
- [ ] Copy/paste kickoff requires assigned providers' official CLIs with subscription authentication and prohibits API-key billing, including fallback.
- [ ] Kickoff requires reporting a blocker if subscription access cannot be established or quota is exhausted.
- [ ] Does not probe credentials or availability, invoke orchestration, or begin execution.
