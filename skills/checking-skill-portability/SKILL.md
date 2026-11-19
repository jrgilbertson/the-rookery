---
name: checking-skill-portability
description: Check whether an Agent Skills package works the same in any harness and with any agent that supports the specification. Use when asked whether a skill is portable or cross-harness, before publishing or sharing a skill written with one harness's skill-creator, or when moving a skill between Claude Code, Codex, or another agent. Writing the skill and testing its behavior stay with that harness's own skill-creator.
license: MIT
compatibility: Needs a shell to read the package. The specification validator runs through uv's uvx and needs network access the first time; without it, check the frontmatter rules by hand and report that the validator did not run.
---

# Checking Skill Portability

A portable skill works the same in any harness and with any agent that supports
the [Agent Skills specification](https://agentskills.io/specification). Check
one or more packages and return a verdict with findings. This is read-only:
fixing a package belongs to whoever writes it.

## Run the specification validator

Run the reference validator from the specification's repository, pinned to a
reviewed commit:

```bash
uvx --from "git+https://github.com/agentskills/agentskills@f130f348f502d9804278a617f86929846896d2e9#subdirectory=skills-ref" skills-ref validate <skill-directory>
```

It checks the name, the directory match, and the frontmatter fields. If it
cannot run, check these rules by hand and say the validator did not run:

- `name`: 1–64 lowercase letters, digits, and hyphens, with no leading,
  trailing, or doubled hyphen, and equal to the directory name.
- `description`: 1–1024 characters.
- `compatibility`, when present: at most 500 characters.
- No frontmatter fields other than `name`, `description`, `license`,
  `compatibility`, `metadata`, and `allowed-tools`.

## Check what the validator cannot

1. **One instruction set for every harness.** The instructions name the
   capability they need, such as asking the user, starting a subagent, or
   tracking tasks, rather than one harness's tool for it. Claude Code's
   `AskUserQuestion`, `Agent`, or `TodoWrite` and Codex's `request_user_input`,
   `spawn_agent`, or `update_plan` are findings when they are the only way the
   skill says to do the step. Listing each harness's equivalent is fine, and so
   is invocation syntax such as `/name` or `$name` shown as one harness's form.
2. **Harness extras are optional.** A field or file that only one harness reads,
   such as Codex's `agents/openai.yaml` or a tool pre-approval list, is not
   needed for the skill to work, and it never stands in for a real permission
   or approval boundary.
3. **The package is self-contained.** Every local link resolves inside the
   package, no more than one level below `SKILL.md`. Bundled scripts carry
   their imports and resources or name the installed dependency they use. Any
   external command, service, or credential the skill needs is declared, with
   where to get it, in `compatibility` or the instructions.
4. **Every installer gets the same skill.** Nothing depends on the author's
   machine or accounts: no absolute path to a home directory, private name,
   personal alias, vault or account detail, or credential the instructions do
   not declare.

## Report

Lead with the verdict: portable, portable after the listed fixes, or not
portable. Give each finding its file and line, the check it fails, and the
smallest fix. Say whether the validator ran. These checks read the package;
they do not show that it behaves the same in each harness. When that matters,
say so, and suggest running the skill once in each harness the user cares about
with the same realistic request and comparing what each did.
