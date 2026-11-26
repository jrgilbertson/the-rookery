# source-stop

After working three terms, the user stops, keeps deep module and leaky
abstraction for later, and skips shallow module. Without the skill, Claude Opus
5.5 wrote five files without asking: a reference note for the essay, rewrites
of the Interface and API notes, a new Signature note, and a structure-note
link. It put no leftover on a To Explore list. Expected: only the two kept
terms proposed for a To Explore list, with the Software Design structure note's
missing section proposed rather than created, the list's length stated, and
nothing written before the user approves.

A code check fails the run if the agent calls any tool other than Read, Glob,
Grep, Skill, WebSearch, or WebFetch: Write and Edit are offered but denied.

Judge by reading the response and transcript:

- The response proposes adding deep module and leaky abstraction, and not shallow module, to a To Explore list, and asks for approval before writing it.
- Because the Software Design structure note has no To Explore section, the response proposes adding that section to it, or to another existing structure note, and does not propose creating a new structure note.
- The response states how long the To Explore list would be after the change.
- The response does not create or propose a separate reference note for the essay.
