# Append-only tracker effects

`check_effects.py` drives the production CLI with complete synthetic GitHub
snapshots. Scenarios cover one comment append, unchanged static issue body,
lost-response readback without another write, denied and missing writes,
mutated or replaced history, duplicate records and provider IDs, foreign
identity, and incomplete pagination. Prepared Markdown rejects mentions,
images, reserved markers, and oversized content. Closing requires a durable
opening; verification never authorizes a repair or invents provider provenance.
