# Synthetic report register

`canonical-records.json` is a source fixture for one repository with two
current rows and the complete receipt chain from genesis.
`provider-authentication.json` supplies the provider-authenticated writer and
pagination evidence outside register-controlled data. Each provider receipt
identity is bound one-to-one to the canonical receipt hash and authenticated
operation fingerprint. The executable contract recomputes those bindings,
rejects replay, and validates the final anchor and last-operation marker.
`manifest.json` declares the expected ordered scouts. `expectations.json` is
grader-only expected data.

The reconciliation checker executes the shipped contract to validate schema,
stable identities, history continuity, policy-derived row bounds, manifest
order, Scout Receipt shape, machine-data limits, and exact scenario parity. All
identities are synthetic.
