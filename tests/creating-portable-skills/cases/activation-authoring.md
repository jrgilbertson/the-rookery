# CPS-ACT-002 — Implicit skill authoring request should activate the skill creator

These definitions contain synthetic inputs and no executor results. Keep the criteria and capture notes outside executor input.

Dimensions: job is authoring; explicit invocation is no; expected activation is yes.

## CPS-ACT-002.INPUT

Draft a portable Agent Skill that turns supplied release notes into a short changelog, usable in both Claude Code and Codex. Example notes: version 2.3.0 adds CSV export, fixes a crash when opening an empty project, and deprecates the legacy sync flag. Reply with the draft text only.

## CPS-ACT-002.SETUP

Expose the frozen creating-portable-skills description through the host’s ordinary discovery mechanism. Send the INPUT paragraph as a normal user message; do not explicitly invoke, attach, or preload the skill. Run read-only: the executor may reply with draft text but must not write files or execute any generated skill.

## CPS-ACT-002.C1

**C1 — Activation boundary.** The executor natively invokes or loads creating-portable-skills for this implicit skill-authoring request. No exact answer wording is required, and this criterion makes no claim about the quality of the drafted skill.

## CPS-ACT-002.CAPTURE

Measure native activation with a complete host trace and verified discovery setup.
Pass requires a successful native invocation/load event, or a
successful read of the creator's instruction body, that matches the frozen
package identity exactly. A discovered name/description, directory listing, or
path mention alone is not activation. An attempted load with no successful result
is an attempted activation, reported separately; it cannot establish a Pass. If
the host cannot distinguish incidental body access from invocation, report the
observed read and leave C1 Unmeasured. Score these observations without inferring
the executor's motivation. A yes/no routing proxy is reported separately. Missing
capture, absent skill discovery, or an incomplete run is Unmeasured. A complete
capture with verified discovery and no activation or attempt is a Fail.
