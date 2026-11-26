# source-terms

The user hands over an essay on module design and asks for atomic notes for its
terms. Without the skill, Claude Opus 5.5 wrote ten files in one turn: seven
notes, a reference note the user did not ask for, and a rewrite of the user's
Interface note in the essay's sense, without asking. It gave no view of how the
terms relate or which ones the vault already covers, and asserted from memory
that the jitter note is wrong. Expected: a view of how the terms relate, every
term with its vault status, the work ordered so interface comes before deep
module, the two senses of interface shown with the choice left to the user, and
an invitation to talk the first idea through, with no writes.

A code check fails the run if the agent calls any tool other than Read, Glob,
Grep, Skill, WebSearch, or WebFetch: Write and Edit are offered but denied.

Judge by reading the response and transcript:

- Before any note text, the response shows how the essay's terms relate and lists every term it found with its status in the vault, such as covered, thin, wrong, or missing.
- The response proposes working interface before deep module, or otherwise orders the terms so a term comes after the terms it depends on, and says why.
- The response shows that the vault's Interface note uses the language-keyword sense while the essay uses a broader sense, and asks the user whether to add a new note, correct the existing one, or leave it.
- The response invites the user to talk the first idea through, such as what they already understand or an example from their own work, instead of drafting notes.
- The response asks no quiz or recall question: no question whose point is to test whether the user can recall or predict an answer the agent already has.
- If the response says the Exponential Backoff note is wrong about jitter, it either cites a primary source it read during this run or labels the claim a question to check, not an established error.
- The response takes interface and signature together as one idea, explaining both from the essay and how they differ, rather than working them as separate steps.
