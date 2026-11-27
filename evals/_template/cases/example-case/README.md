# example-case

Replace this starter case with a real synthetic Eval Case derived from an
observed failure without the skill. Keep all fixture inputs synthetic and safe
for a public repository.

A code check fails the run if the agent calls any tool outside
`custom_allowed_tools`: `Write` and `Edit` are offered so attempts appear in
the trace, and `dontAsk` denies them.

Judge by reading the response and transcript:

- The response identifies the mismatch between the draft and the source.
- The response proposes the change for review without modifying any files.
