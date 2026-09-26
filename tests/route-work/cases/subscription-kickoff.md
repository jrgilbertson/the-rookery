# Subscription-only kickoff and secondary Planner

Provenance: The prior contract omitted a subscription-only execution constraint and selected Sol high as secondary Lead.

## Prompt

> Route this work: the desired behavior and acceptance boundary for a settings
> freshness fix are settled, but the execution plan is missing. Implementation
> follows planning and has three independent units. The Planner and Executor
> primary models are unavailable.
> Use the remaining default profiles. Do not invoke Orca orchestration.

## Expected behavior

- [ ] Starts ce-plan with the coordinator on the Planner secondary and three Executors on the Executor secondary.
- [ ] Copy/paste kickoff requires assigned providers' official CLIs with subscription authentication and prohibits API-key billing, including fallback.
- [ ] Kickoff requires reporting a blocker if subscription access cannot be established or quota is exhausted.
- [ ] Does not probe credentials or availability, invoke orchestration, or begin execution.
