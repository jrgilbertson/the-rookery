# CPS-ACT-004 — Reusable meeting instructions should not activate the skill creator

These definitions contain synthetic inputs and no executor results. Keep the criteria and capture notes outside executor input.

Dimensions: job is ordinary prose writing; explicit invocation is no; expected activation is no.

## CPS-ACT-004.INPUT

Write reusable instructions for attendees of our weekly planning meeting: what to read beforehand, which updates to bring, and how to keep each update under two minutes.

## CPS-ACT-004.SETUP

Expose the frozen creating-portable-skills description through the host’s ordinary discovery mechanism. Send the INPUT paragraph as a normal user message; do not explicitly invoke the skill. Run read-only: the executor may reply with text but must not write files. The writing task may be answered or clarified through another appropriate workflow.

## CPS-ACT-004.C1

**C1 — Activation boundary.** The executor does not invoke creating-portable-skills for this ordinary writing request. Clarifying questions and different general solutions are allowed. No exact answer wording is required.

## CPS-ACT-004.CAPTURE

Measure native activation with a complete host trace and verified discovery setup.
Count a native skill invocation/load event, an explicit skill tool request, or a
successful read of the creator's instruction body as activation. A discovered
name/description, directory listing, or path mention alone is not activation.
An attempted load with no successful result is an attempted activation, reported
separately; it cannot establish either a completed invocation or a Pass. If the
host cannot distinguish incidental body access from invocation, report the
observed read and leave C1 Unmeasured. Score these observations without inferring
the executor's motivation. A yes/no routing proxy is reported separately. Missing capture, absent skill discovery, or an incomplete run is unmeasured, never an automatic Pass. This negative case alone does not establish reliable positive activation.
