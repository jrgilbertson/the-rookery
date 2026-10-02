# Portable Package Format

The [Agent Skills specification](https://agentskills.io/specification) is the
format authority. A package contains `SKILL.md` with YAML frontmatter and a
Markdown body, plus any resources it needs.

| Field | Required | Specification |
| --- | --- | --- |
| `name` | Yes | 1–64 lowercase ASCII letters, digits, and hyphens; no leading, trailing, or consecutive hyphens; matches the package directory |
| `description` | Yes | 1–1024 characters describing what the skill does and when to use it |
| `license` | No | License name or a reference to a bundled license file |
| `compatibility` | No | 1–500 characters describing actual environment requirements |
| `metadata` | No | Map of string keys to string values |
| `allowed-tools` | No | Space-separated string; experimental and dependent on harness support |

The specification recommends a body under 500 lines and about 5,000 tokens.
Use relative links from `SKILL.md` to package resources and keep references one
level deep. Every local link must resolve inside the package. Additional files
and directories are allowed by the specification.

## Dependencies and harness adapters

Use the host's documented installation path. Core instructions describe the
capabilities needed to do the job. If a skill depends on a command, SDK, service,
credential, or another external resource, declare that requirement and its
source. A script copied from a project must carry its imports and resources or
document an intentional installed dependency.

Keep harness-specific frontmatter and invocation controls in an optional
adapter supported by that harness. The canonical package should remain useful
without that adapter. Do not replace real authorization boundaries with tool
pre-approval metadata.

An installed companion skill is a convenience, not a prerequisite for reading a
public workflow guide. When a guide or required tool cannot be accessed, report
the unavailable step rather than claiming it ran.

## What validation establishes

`skills-ref validate <skill-directory>` checks naming and frontmatter. Also
inspect local links and dependency declarations, and exercise bundled helpers.
An install or structural pass establishes only the checks observed. Behavioral
claims name the cases, revision, model, and harness actually exercised.
