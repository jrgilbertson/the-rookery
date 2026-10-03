# CPS-ACT-001 — Generic grader request should not activate the skill creator

These definitions contain synthetic inputs and no executor results. Keep the criteria and capture notes outside executor input.

## CPS-ACT-001.INPUT

Build a grader and rubric for judging model outputs.

## CPS-ACT-001.SETUP

Expose the frozen creating-portable-skills description through the host’s ordinary discovery mechanism. Do not explicitly invoke the skill. The generic task may be answered or clarified through another appropriate workflow.

## CPS-ACT-001.C1

**C1 — Activation boundary.** The executor does not invoke creating-portable-skills solely because the request mentions a grader. Clarifying questions and different general solutions are allowed. No exact answer wording is required.

## CPS-ACT-001.CAPTURE

Measure native activation with a complete host trace and verified discovery setup. A yes/no routing proxy is reported separately. Missing capture, absent skill discovery, or an incomplete run is unmeasured, never an automatic Pass. This negative case alone does not establish reliable positive activation.
