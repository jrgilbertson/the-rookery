# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Jason is the primary operator and maintainer. He uses The Rookery as the public, up-to-date record of how he builds software with AI and improves that system over time.

Visitors are practitioners and AI builders who find the repository through social media or shared links and want to understand, install, or adapt the workflows, skills, and scheduled automations.

## Product Purpose

The Rookery documents Jason's working system for building software with AI so others can read how it works, adapt the workflows, and install the skills they need. It combines the open-source tools and plugins he relies on, workflow playbooks refined through daily work, and custom skills written only when existing tools leave a recurring gap.

A visitor should be able to see how the parts fit together, follow a workflow, and install a skill without reading a wall of text first. For Jason, the repository succeeds when it stays his live working reference instead of falling behind what he actually runs.

## Positioning

The Rookery is a working field guide to the open-source tools, workflows, skills, and scheduled automations Jason runs across Claude Code, Codex, Cursor, Gemini CLI, and other compatible agents. It credits existing open-source work, explains how the pieces connect, and adds a custom skill only when daily use exposes a recurring gap. When his setup or judgment changes, the repository changes with it.

## Operating Context

The repository is experienced primarily through GitHub-rendered Markdown, shared repository links, and individually installable skills. `README.md` introduces the system, `WORKFLOWS.md` explains its five core jobs and two feedback loops, `GLOSSARY.md` defines project-specific language, the `skills/` catalog contains the executable instructions, and `automations/` holds recurring review prompts with schedules and setup instructions.

The five core workflow jobs are Research, Plan, Design, Build, and Ship. Maintain and Learn are the two feedback loops. Visual explanations are most valuable where process, handoffs, loops, or system relationships would otherwise become text-heavy.

## Capabilities and Constraints

- Skills install individually and should remain useful across Claude Code, Codex, Cursor, Gemini CLI, and other compatible tools.
- The system avoids depending on one vendor, keeps the skill catalog small, and improves from use.
- Automation definitions are reusable prompts and schedules configured manually in Orca. Local repository bindings and account identifiers stay in the scheduler; reports and owner decisions stay in the private shared history repository.
- The repository is designed for public, open-source use and is MIT licensed. Visuals must not imply private customer evidence, adoption metrics, endorsements, or commercial proof that the repository does not contain.
- Repository banners and social previews are separate but coordinated assets. Explanatory illustrations and diagrams already appear across the root documentation (including `README.md`, `WORKFLOWS.md`, `TESTING.md`, `PRIORITIZATION.md`, and `ROUTING.md`), and new visuals follow the shared system in `DESIGN.md`.
- Huginn and Muninn explain the repository and its workflows through their actions. Huginn brings back new findings; Muninn preserves useful lessons and returns them to the work.

## Brand Commitments

- Preserve the name **The Rookery** and its corvid meaning: a place where corvids gather and return.
- The confirmed repository-level message is **"A field guide to how I build with AI."** Supporting copy may expand it as **"Open-source tools, practical workflows, and portable skills refined through use."**
- Use the standardized names **Huginn** and **Muninn**, Odin's ravens associated with thought and memory. The raven story explains the name; it does not imply that the workflows learn autonomously.
- The work should be technically clear while remaining warm, memorable, and fun.
- Visual personality must make technical concepts easier to understand. Characters, metaphors, or motion should perform the idea rather than decorate it.
- Avoid generic corporate diagrams, sterile consulting-deck visuals, novelty mascots, and Norse-fantasy pastiche that overwhelms the technical substance.

## Evidence on Hand

- `README.md` contains the public product story, installation path, guiding principles, skill catalog, the existing Huginn-and-Muninn narrative, and explicit credit for the open-source work the system builds upon.
- `WORKFLOWS.md` contains the five core jobs, two feedback loops, and detailed process explanations suitable for visual translation.
- `GLOSSARY.md` contains the project's canonical vocabulary.
- `skills/`, `tests/`, and `docs/solutions/` provide real examples of the system's capabilities and quality practices.
- No testimonials, customer logos, adoption metrics, or commercial performance claims are present and none should be fabricated.

## Product Principles

1. Prefer adopting and adapting strong existing work over rebuilding it, and credit the people who made it possible.
2. Explain the mechanism before adding personality.
3. Make rigorous technical work approachable without making it simplistic.
4. Make characters essential to the explanation: removing them should break the explanation, not merely reduce decoration.
5. Preserve the system's personal, continuously improving character while keeping every workflow and skill portable across agents and harnesses.

## Accessibility & Inclusion

Public visuals need strong contrast, meaningful alt text, and legibility at GitHub and social-preview sizes. A concept must not depend on color, character identity, or animation alone; diagrams and motion need a clear static reading and a text equivalent.
