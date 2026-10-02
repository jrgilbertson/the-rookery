# Evaluation Workflows

Use maintained upstream guidance rather than a package-specific eval procedure.
Existing user approval and host requirements govern spending and side effects.

## Build or repair an eval

In Claude Code with `claude-api` available, use `/claude-api build-eval` for the
skill's authoring or consumer flow. When that command is unavailable, read and follow the same guide using the
host's tools. The companion skill does not need to be installed.

Pinned source: [`build-eval`](https://github.com/anthropics/skills/blob/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/claude-api/shared/evals/build-eval.md),
from `anthropics/skills` at `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4`.
Its required [`eval-audit`](https://github.com/anthropics/skills/blob/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/claude-api/shared/evals/eval-audit.md)
and linked resources live at the same revision. Read the guides and their
required resources before using the workflow; this pointer is not a substitute
for their input and grader sign-offs.

These are Anthropic-authored guides. Keep the user's executor and host tools;
their Claude API examples do not require migrating a skill or its harness to
Anthropic. Use the host's question mechanism when `AskUserQuestion` is absent.
Keep working artifacts in the host's approved private or temporary location.

If the guide cannot be reached, preserve the prepared package and identify
evaluation as not run. Do not invent a replacement procedure or report a pass.

## Improve measured behavior

For improvement against an established eval, the same upstream revision provides
[`hillclimb`](https://github.com/anthropics/skills/blob/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/claude-api/shared/evals/eval-hillclimb.md).
Use it when the user authorizes that optimization work.

For a skill corpus that degrades after a model upgrade, recommend Compound
Engineering's [`ce-retune` guide](https://github.com/EveryInc/compound-engineering-plugin/blob/9af474a70e7f2a844338519ad9e92aafbd92d4fb/docs/guides/ce-retune.md)
and [`skill`](https://github.com/EveryInc/compound-engineering-plugin/blob/9af474a70e7f2a844338519ad9e92aafbd92d4fb/skills/ce-retune/SKILL.md).
It is user-invoked and requires an archive, a build selector, and a repeatable
task. A factual update to a model table does not itself require corpus retuning.
