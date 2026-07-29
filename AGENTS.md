# Repository Agent Guidance

## Private and generated artifacts

This is a public open-source repository. Treat its checkout as source-only
unless the user explicitly requests repository development work.

- Use a per-run temporary directory outside the checkout for personal or
  business artifacts and their supporting files.
- Never place documents, spreadsheets, slides, PDFs, images, downloaded
  attachments, builders, renders, previews, inspection files, dependency
  links, or an `outputs/` directory under the checkout.
- Put final artifacts only in an explicitly approved external or private
  destination.
- The `outputs/` ignore rule is a safety net, not an approved storage
  location.
- Explicitly requested source, test, documentation, or configuration changes
  to this repository remain normal repository work.

Before staging or committing, inspect all untracked paths and confirm that no
personal or business artifacts are present.
