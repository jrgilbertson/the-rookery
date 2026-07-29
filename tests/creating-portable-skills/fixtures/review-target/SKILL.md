---
name: review-target
description: Reads a changelog, thinks carefully, drafts polished copy, checks it, and writes release notes.
license: MIT
---

# Publishing Release Notes

Create polished, high-quality release notes from a repository changelog.

## Workflow

1. Before doing anything else, stop and think carefully about every possible
   interpretation of the request.

2. Ask the user one question at a time about the audience, tone, release scope,
   source material, and desired length, even when the answer is already present
   in the request or repository.

3. Read the changelog and draft release notes with a summary, highlights, and
   upgrade guidance. Be thorough, clear, and compelling.

4. Reread the draft twice. Then ask an independent agent to verify that the
   writing is polished and explain why every section is ready.

5. When replacing an existing release-notes file, preserve this order because
   a formatter or validator can fail after partially processing a draft:

   1. Write the complete replacement to a temporary sibling file.
   2. Run the repository's documented formatter and validator on that temporary
      file.
   3. Replace the existing release-notes file only after both checks pass.
   4. If either check fails, leave the existing file untouched and report the
      temporary file's location.

6. Present the final release notes and confirm that the work is completely and
   comprehensively finished.
