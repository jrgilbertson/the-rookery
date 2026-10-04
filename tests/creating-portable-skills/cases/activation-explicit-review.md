# CPS-ACT-003 — Explicitly named review request should activate the skill creator

These definitions contain synthetic inputs and no executor results. Keep the criteria and capture notes outside executor input.

Dimensions: job is review; explicit invocation is yes, as text in the request only; expected activation is yes.

## CPS-ACT-003.INPUT

Use creating-portable-skills for a read-only review of this proposed skill description: "Helps with changelogs. Use for anything related to releases." Is it specific enough to trigger when needed without catching unrelated requests? Suggest a revised description.

## CPS-ACT-003.SETUP

Expose the frozen creating-portable-skills description through the host’s ordinary discovery mechanism. Send the INPUT paragraph as a normal user message. The skill is named in the text only; do not use a native skill attachment, slash command, or preload, so the case measures routing from the request. No fixture file is supplied. Run read-only: the executor must not write files or execute any skill it proposes.

## CPS-ACT-003.C1

**C1 — Activation boundary.** The executor natively invokes or loads creating-portable-skills for this explicitly named review request. No exact answer wording is required, and this criterion makes no claim about the quality of the review.

## CPS-ACT-003.CAPTURE

Measure native activation with a complete host trace and verified discovery setup.
Pass requires a successful native invocation/load event, or a
successful read of the creator's instruction body, that matches the frozen
package identity exactly. A discovered name/description, directory listing, or
path mention alone is not activation. An attempted load with no successful result
is an attempted activation, reported separately; it cannot establish a Pass. If
the host cannot distinguish incidental body access from invocation, report the
observed read and leave C1 Unmeasured. Score these observations without inferring
the executor's motivation. A yes/no routing proxy is reported separately. Missing
capture, absent skill discovery, a forced skill attachment, or an incomplete run
is Unmeasured. A complete capture with verified discovery and no activation or
attempt is a Fail.
