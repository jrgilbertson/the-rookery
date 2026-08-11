# Synthetic report register

`canonical-records.json` is a source fixture for one repository with two
current rows and the complete receipt chain from genesis.
`provider-authentication.json` supplies the provider-authenticated writer and
pagination evidence outside register-controlled data. The executable contract
recomputes every receipt hash and validates the final anchor.
`manifest.json` declares the expected ordered scouts. `expectations.json` is
grader-only expected data.

The reconciliation checker executes the shipped contract to validate schema,
stable identities, history continuity, policy-derived row bounds, manifest
order, Scout Receipt shape, machine-data limits, and exact scenario parity. All
identities are synthetic.
