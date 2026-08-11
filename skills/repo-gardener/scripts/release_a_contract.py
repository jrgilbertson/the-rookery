#!/usr/bin/env python3
"""Deterministic Release A validation and derivation helpers.

The model-facing skill owns judgment and orchestration. This module owns the
mechanical invariants that must have one executable source of truth: bounded
machine data, authenticated history, Scout Receipt shape, effect outcomes,
completion partitions, ordered gates, and policy-derived portfolio capacity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


IDENTITY_LIMIT = 128
DISPLAY_LIMIT = 512
RECEIPT_LIMIT = 16 * 1024
BODY_LIMIT = 48 * 1024
RELEASE_A_PORTFOLIO_LIMIT = 7
RELEASE_A_LANES = (
    "dependency-and-vulnerability",
    "issue-implementation",
    "ci-and-failing-test",
    "repository-test-and-code-health",
    "documentation-changelog-and-release-note",
    "runtime-error-and-alert",
    "risk-scoped-qa-and-regression",
    "security-secret-and-static-analysis",
    "issue-backlog-and-customer-feedback-triage",
)
SCOUT_OUTCOMES = {"complete", "not applicable", "incomplete"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REGISTER_FIELDS = {
    "schema",
    "repository_id",
    "report_id",
    "writer_id",
    "register_revision",
    "last_operation_id",
    "last_operation_fingerprint",
    "history_receipts",
    "history_anchor",
    "rows",
}
ROW_FIELDS = {
    "row_id",
    "source_id",
    "source_revision",
    "description",
    "state",
    "lane",
    "rationale",
    "risk",
    "budget_use",
    "evidence_ids",
    "next_action",
    "row_revision",
}
HISTORY_RECEIPT_FIELDS = {
    "sequence",
    "previous_hash",
    "repository_id",
    "writer_id",
    "provider_receipt_id",
    "operation_id",
    "kind",
    "run_id",
    "receipt_hash",
}
HISTORY_KINDS = {
    "run-start",
    "manifest",
    "scout-summary",
    "reconciliation",
    "decision",
    "effect",
    "report",
    "terminal-run",
}
HISTORY_ANCHOR_FIELDS = {"sequence", "head", "latest_receipt"}
AUTHENTICATED_RECEIPT_FIELDS = {
    "provider_receipt_id",
    "writer_id",
    "receipt_hash",
    "operation_fingerprint",
}
OPERATION_MATERIAL_FIELDS = (
    "repository_id",
    "writer_id",
    "provider_receipt_id",
    "operation_id",
    "kind",
    "run_id",
    "receipt_hash",
)
MANIFEST_FIELDS = {"schema", "repository_id", "run_id", "manifest_id", "policy_revision", "scouts"}
SCOUT_COLLECTION_FIELDS = {"schema", "repository_id", "run_id", "manifest_id", "receipts"}
SCOUT_RECEIPT_FIELDS = {
    "receipt_id",
    "scout_id",
    "outcome",
    "run_id",
    "manifest_id",
    "lane",
    "observed_at",
    "source_id",
    "evidence_references",
    "candidate_count",
}
EFFECT_SCENARIOS = {"operation", "retry", "identity-collision", "terminal-receipt", "repair"}
COMPLETION_SCENARIOS = {"completion-partition", "delegation", "optional-scout", "caller-completion"}
AUTHORITY_FIELDS = (
    "caller_exclusive",
    "wrapper_scope_allowlisted",
    "raw_write_capability_absent_everywhere",
    "continuity_and_retention_valid",
    "intended_receipt_read_back",
)
GATE_ORDER = (
    "current source",
    "policy and authority",
    "evidence",
    "conflict",
    "protected boundary",
    "capability",
)
REQUIRED_EVENTS = (
    "classify-older-run",
    "reconcile-effect-intents",
    "reconcile-current-rows",
    "append-run-start",
    "read-run-start",
    "persist-reconciliation",
    "read-reconciliation",
    "persist-manifest",
    "read-manifest",
    "dispatch-scouts",
    "append-decisions",
    "read-decisions",
    "append-terminal",
    "read-terminal",
    "render-report",
    "read-report",
)
RECONCILIATION_WRITE_PROOFS = (
    "exclusive_executor",
    "wrapper_scope_allowlisted",
    "raw_write_capability_absent_everywhere",
    "continuity_valid",
    "retention_valid",
    "runtime_scope_valid",
    "intended_receipt_read_back",
    "authoritative_post_read_completed",
    "terminal_receipt_read_back",
    "write_requested",
)
RECONCILIATION_AUTHORITY_FIELDS = {
    "schema",
    "repository_id",
    "report_id",
    "writer_id",
    "run_id",
    *RECONCILIATION_WRITE_PROOFS,
}
EFFECT_AUTHORITY_FIELDS = {"repository_id", *AUTHORITY_FIELDS}


class ContractError(Exception):
    """A machine contract is malformed or cannot support the claimed result."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def require_object(value: Any, label: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    require(isinstance(value, list), f"{label} must be a list")
    return value


def require_exact_fields(value: dict[str, Any], fields: set[str], label: str) -> None:
    missing = sorted(fields - set(value))
    unexpected = sorted(set(value) - fields)
    details = []
    if missing:
        details.append(f"missing {', '.join(missing)}")
    if unexpected:
        details.append(f"unexpected {', '.join(unexpected)}")
    require(not details, f"{label} schema mismatch: {'; '.join(details)}")


def require_identity(value: Any, label: str) -> str:
    require(isinstance(value, str) and value, f"{label} is missing")
    try:
        value.encode("ascii")
    except UnicodeEncodeError as error:
        raise ContractError(f"{label} must be ASCII") from error
    require(len(value) <= IDENTITY_LIMIT, f"{label} exceeds {IDENTITY_LIMIT} ASCII characters")
    return value


def require_display(value: Any, label: str) -> str:
    require(isinstance(value, str), f"{label} must be text")
    require(len(value) <= DISPLAY_LIMIT, f"{label} exceeds {DISPLAY_LIMIT} Unicode code points")
    return value


def require_nonempty_display(value: Any, label: str) -> str:
    result = require_display(value, label)
    require(bool(result.strip()), f"{label} is empty")
    return result


def require_sha256(value: Any, label: str) -> str:
    require(isinstance(value, str) and SHA256.fullmatch(value) is not None, f"{label} must be a lowercase SHA-256 digest")
    return value


def require_utc_time(value: Any, label: str) -> str:
    require(isinstance(value, str) and value.endswith("Z"), f"{label} must be an ISO-8601 UTC observation time")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ContractError(f"{label} must be an ISO-8601 UTC observation time") from error
    require(parsed.tzinfo is not None and parsed.utcoffset() == timezone.utc.utcoffset(parsed), f"{label} must be an ISO-8601 UTC observation time")
    return value


def require_payload(value: Any, limit: int, label: str) -> None:
    require(len(canonical_bytes(value)) <= limit, f"{label} exceeds {limit} canonical UTF-8 bytes")


def validate_body(body: Any) -> int:
    require(isinstance(body, str), "managed body must be text")
    size = len(body.encode("utf-8"))
    require(size <= BODY_LIMIT, f"managed body exceeds {BODY_LIMIT} UTF-8 bytes")
    return size


def policy_section(text: str, name: str) -> list[str]:
    lines = text.splitlines()
    starts = [index for index, line in enumerate(lines) if re.fullmatch(rf"{re.escape(name)}:\s*(?:#.*)?", line)]
    require(len(starts) == 1, f"policy must define top-level {name} exactly once")
    result: list[str] = []
    for line in lines[starts[0] + 1 :]:
        if line and not line[0].isspace() and not line.lstrip().startswith("#"):
            break
        result.append(line)
    return result


def portfolio_limit_from_text(text: str) -> int:
    try:
        boundaries = policy_section(text, "boundaries")
    except ContractError as error:
        raise ContractError("policy must define boundaries.repository_portfolio_limit exactly once") from error
    matches = [
        match.group(1)
        for line in boundaries
        if (match := re.fullmatch(r"  repository_portfolio_limit:\s*([0-9]+)\s*(?:#.*)?", line))
    ]
    require(len(matches) == 1, "policy must define boundaries.repository_portfolio_limit exactly once")
    limit = int(matches[0])
    require(limit == RELEASE_A_PORTFOLIO_LIMIT, "boundaries.repository_portfolio_limit must equal the Release A value 7")
    return limit


def installed_lanes_from_text(text: str) -> list[str]:
    lanes = policy_section(text, "lanes")
    lane_starts = [
        (index, match.group(1))
        for index, line in enumerate(lanes)
        if (match := re.fullmatch(r"  ([a-z0-9][a-z0-9-]*):\s*(?:#.*)?", line))
    ]
    result = [lane for _, lane in lane_starts]
    require(bool(result), "policy installed lane inventory is empty")
    require(len(result) == len(set(result)), "policy installed lane inventory contains duplicates")
    require(tuple(result) == RELEASE_A_LANES, "policy installed lane inventory differs from the public Release A contract")
    for position, (start, lane) in enumerate(lane_starts):
        end = lane_starts[position + 1][0] if position + 1 < len(lane_starts) else len(lanes)
        mutations = [
            match.group(1)
            for line in lanes[start + 1 : end]
            if (match := re.fullmatch(r"    mutation:\s*(true|false)\s*(?:#.*)?", line))
        ]
        require(
            mutations == ["false"],
            f"policy lane {lane} mutation must be exactly false",
        )
    return result


def policy_contract(policy_path: Path) -> tuple[int, list[str]]:
    text = policy_path.read_text(encoding="utf-8")
    return portfolio_limit_from_text(text), installed_lanes_from_text(text)


def portfolio_limit(policy_path: Path) -> int:
    return portfolio_limit_from_text(policy_path.read_text(encoding="utf-8"))


def receipt_hash(receipt: dict[str, Any]) -> str:
    hashed = {key: value for key, value in receipt.items() if key != "receipt_hash"}
    return hashlib.sha256(canonical_bytes(hashed)).hexdigest()


def operation_fingerprint(receipt: dict[str, Any]) -> str:
    material = {field: receipt[field] for field in OPERATION_MATERIAL_FIELDS}
    return hashlib.sha256(canonical_bytes(material)).hexdigest()


def validate_manifest(
    manifest: Any,
    repository_id: str | None = None,
    expected_scouts: list[str] | None = None,
) -> dict[str, Any]:
    manifest = require_object(manifest, "manifest")
    require_exact_fields(manifest, MANIFEST_FIELDS, "manifest")
    require(manifest.get("schema") == "repo-gardener-scout-manifest/v1", "manifest schema mismatch")
    manifest_repository = require_identity(manifest.get("repository_id"), "manifest repository_id")
    if repository_id is not None:
        require(manifest_repository == repository_id, "manifest repository mismatch")
    require_identity(manifest.get("manifest_id"), "manifest_id")
    require_identity(manifest.get("run_id"), "manifest run_id")
    require_identity(manifest.get("policy_revision"), "manifest policy_revision")
    scouts = require_list(manifest.get("scouts"), "manifest scouts")
    for index, scout in enumerate(scouts):
        require_identity(scout, f"manifest scout {index}")
    require(len(scouts) == len(set(scouts)), "duplicate manifest scout")
    if expected_scouts is not None:
        require(scouts == expected_scouts, "manifest scouts differ from installed policy lane inventory")
    return manifest


def validate_register(
    records: Any,
    manifest: Any,
    authentication: Any,
    policy_path: Path,
) -> dict[str, Any]:
    records = require_object(records, "register")
    manifest = require_object(manifest, "manifest")
    authentication = require_object(authentication, "provider authentication evidence")
    limit, lanes = policy_contract(policy_path)

    require_exact_fields(records, REGISTER_FIELDS, "register")
    require(records.get("schema") == "repo-gardener-register/v1", "register schema mismatch")
    repository_id = require_identity(records.get("repository_id"), "register repository_id")
    require_identity(records.get("report_id"), "register report_id")
    register_writer = require_identity(records.get("writer_id"), "register writer_id")
    require(type(records.get("register_revision")) is int and records["register_revision"] >= 0, "invalid register revision")

    rows = require_list(records.get("rows"), "register rows")
    require(len(rows) <= limit, f"portfolio exceeds policy limit {limit}")
    row_ids: list[str] = []
    source_ids: list[str] = []
    for index, raw_row in enumerate(rows):
        row = require_object(raw_row, f"row {index}")
        require_exact_fields(row, ROW_FIELDS, f"row {index}")
        row_ids.append(require_identity(row.get("row_id"), f"row {index} row_id"))
        source_ids.append(require_identity(row.get("source_id"), f"row {index} source_id"))
        require_identity(row.get("source_revision"), f"row {index} source_revision")
        require_nonempty_display(row.get("description"), f"row {index} description")
        lane = require_identity(row.get("lane"), f"row {index} lane")
        require(lane in lanes, f"row {index} lane is outside installed policy lane inventory")
        require_nonempty_display(row.get("rationale"), f"row {index} rationale")
        require_nonempty_display(row.get("risk"), f"row {index} risk")
        require_nonempty_display(row.get("budget_use"), f"row {index} budget_use")
        evidence_ids = require_list(row.get("evidence_ids"), f"row {index} evidence_ids")
        require(bool(evidence_ids), f"row {index} evidence_ids are empty")
        for evidence_index, evidence_id in enumerate(evidence_ids):
            require_identity(evidence_id, f"row {index} evidence_id {evidence_index}")
        require(len(evidence_ids) == len(set(evidence_ids)), f"row {index} duplicate evidence identity")
        require_nonempty_display(row.get("next_action"), f"row {index} next_action")
        require(row.get("state") in {"To do", "In process"}, f"invalid row state: {row.get('state')}")
        require(type(row.get("row_revision")) is int and row["row_revision"] >= 0, "invalid row revision")
    require(len(row_ids) == len(set(row_ids)), "duplicate row identity")
    require(len(source_ids) == len(set(source_ids)), "duplicate source identity")

    require_exact_fields(
        authentication,
        {"schema", "repository_id", "history_pages_complete", "authenticated_receipts"},
        "provider authentication evidence",
    )
    require(authentication.get("schema") == "repo-gardener-provider-authentication/v1", "authentication schema mismatch")
    require(authentication.get("repository_id") == repository_id, "authentication repository mismatch")
    require(authentication.get("history_pages_complete") is True, "canonical history pagination is incomplete")
    authenticated = require_list(authentication.get("authenticated_receipts"), "authenticated receipt evidence")
    authenticated_map: dict[str, dict[str, Any]] = {}
    for index, raw_item in enumerate(authenticated):
        item = require_object(raw_item, f"authenticated receipt {index}")
        require_exact_fields(item, AUTHENTICATED_RECEIPT_FIELDS, f"authenticated receipt {index}")
        provider_receipt_id = require_identity(item.get("provider_receipt_id"), f"authenticated receipt {index} provider_receipt_id")
        require(provider_receipt_id not in authenticated_map, "duplicate provider authentication evidence")
        writer_id = require_identity(item.get("writer_id"), f"authenticated receipt {index} writer_id")
        require(writer_id == register_writer, f"authenticated receipt {index} is not bound to dedicated register writer")
        require_sha256(item.get("receipt_hash"), f"authenticated receipt {index} receipt hash")
        require_sha256(item.get("operation_fingerprint"), f"authenticated receipt {index} operation fingerprint")
        authenticated_map[provider_receipt_id] = item

    history = require_list(records.get("history_receipts"), "history receipts")
    previous_hash = "0" * 64
    seen_provider_receipt_ids: set[str] = set()
    last_authenticated_operation_fingerprint: str | None = None
    for index, raw_receipt in enumerate(history, start=1):
        receipt = require_object(raw_receipt, f"history receipt {index}")
        require_exact_fields(receipt, HISTORY_RECEIPT_FIELDS, f"history receipt {index}")
        require_payload(receipt, RECEIPT_LIMIT, f"history receipt {index}")
        require(receipt.get("sequence") == index, f"history receipt {index} sequence discontinuity")
        require(receipt.get("previous_hash") == previous_hash, f"history receipt {index} previous hash mismatch")
        require(receipt.get("repository_id") == repository_id, f"history receipt {index} repository mismatch")
        writer_id = require_identity(receipt.get("writer_id"), f"history receipt {index} writer_id")
        require(writer_id == register_writer, f"history receipt {index} is not bound to dedicated register writer")
        require_identity(receipt.get("operation_id"), f"history receipt {index} operation_id")
        require(receipt.get("kind") in HISTORY_KINDS, f"history receipt {index} kind is invalid")
        require_identity(receipt.get("run_id"), f"history receipt {index} run_id")
        provider_receipt_id = require_identity(receipt.get("provider_receipt_id"), f"history receipt {index} provider_receipt_id")
        require(provider_receipt_id not in seen_provider_receipt_ids, f"history receipt {index} provider receipt replay")
        seen_provider_receipt_ids.add(provider_receipt_id)
        authenticated_receipt = authenticated_map.get(provider_receipt_id)
        require(authenticated_receipt is not None and authenticated_receipt.get("writer_id") == writer_id, f"history receipt {index} writer is not provider-authenticated")
        expected_hash = receipt_hash(receipt)
        require(receipt.get("receipt_hash") == expected_hash, f"history receipt {index} hash mismatch")
        require(authenticated_receipt.get("receipt_hash") == expected_hash, f"history receipt {index} authenticated receipt content mismatch")
        expected_operation_fingerprint = operation_fingerprint(receipt)
        require(
            authenticated_receipt.get("operation_fingerprint") == expected_operation_fingerprint,
            f"history receipt {index} authenticated operation material mismatch",
        )
        last_authenticated_operation_fingerprint = expected_operation_fingerprint
        previous_hash = expected_hash
    require(set(authenticated_map) == seen_provider_receipt_ids, "provider authentication inventory differs from canonical history")

    anchor = require_object(records.get("history_anchor"), "history anchor")
    require_exact_fields(anchor, HISTORY_ANCHOR_FIELDS, "history anchor")
    require(anchor.get("sequence") == len(history), "history anchor sequence mismatch")
    if history:
        require(anchor.get("head") == previous_hash, "history anchor head mismatch")
        require(anchor.get("latest_receipt") == history[-1], "history anchor latest_receipt mismatch")
        require(records.get("last_operation_id") == history[-1].get("operation_id"), "operation marker mismatch")
        require(
            require_sha256(records.get("last_operation_fingerprint"), "last operation fingerprint")
            == last_authenticated_operation_fingerprint,
            "last operation fingerprint does not match authenticated operation material",
        )
    else:
        require(anchor.get("head") == "GENESIS" and anchor.get("latest_receipt") is None, "genesis history anchor mismatch")
        require(records.get("last_operation_id") is None and records.get("last_operation_fingerprint") is None, "genesis operation markers must be null")

    manifest = validate_manifest(manifest, repository_id, lanes)
    return {"manifest": manifest, "portfolio_limit": limit, "history_head": anchor["head"]}


def validate_scout_receipts(
    data: Any,
    manifest: Any,
    *,
    complete: bool = True,
    expected_scouts: list[str] | None = None,
) -> dict[str, dict[str, Any]]:
    data = require_object(data, "Scout Receipt collection")
    require_exact_fields(data, SCOUT_COLLECTION_FIELDS, "Scout Receipt collection")
    require(data.get("schema") == "repo-gardener-scout-receipt-collection/v1", "Scout Receipt collection schema mismatch")
    collection_repository = require_identity(data.get("repository_id"), "Scout Receipt collection repository_id")
    collection_run = require_identity(data.get("run_id"), "Scout Receipt collection run_id")
    manifest = validate_manifest(manifest, collection_repository, expected_scouts)
    require(collection_run == manifest.get("run_id"), "Scout Receipt collection run mismatch")
    require(data.get("manifest_id") == manifest.get("manifest_id"), "Scout Receipt manifest mismatch")
    receipts = require_list(data.get("receipts"), "Scout Receipts")
    scouts = require_list(manifest.get("scouts"), "manifest scouts")
    scout_ids: list[str] = []
    receipt_ids: list[str] = []
    receipt_map: dict[str, dict[str, Any]] = {}
    for index, raw_receipt in enumerate(receipts):
        receipt = require_object(raw_receipt, f"Scout Receipt {index}")
        outcome = receipt.get("outcome")
        expected_fields = set(SCOUT_RECEIPT_FIELDS)
        if outcome == "not applicable":
            expected_fields.add("affirmative_evidence")
        elif outcome == "incomplete":
            expected_fields.add("failure_reason")
        require_exact_fields(receipt, expected_fields, f"Scout Receipt {index}")
        require_payload(receipt, RECEIPT_LIMIT, f"Scout Receipt {index}")
        receipt_id = require_identity(receipt.get("receipt_id"), f"Scout Receipt {index} receipt_id")
        scout_id = require_identity(receipt.get("scout_id"), f"Scout Receipt {index} scout_id")
        require_identity(receipt.get("run_id"), f"Scout Receipt {index} run_id")
        require(receipt.get("run_id") == manifest.get("run_id"), f"Scout Receipt {index} run mismatch")
        require(receipt.get("manifest_id") == manifest.get("manifest_id"), f"Scout Receipt {index} manifest mismatch")
        require(receipt.get("lane") == scout_id, f"Scout Receipt {index} lane mismatch")
        require_utc_time(receipt.get("observed_at"), f"Scout Receipt {index} UTC observation time")
        require_identity(receipt.get("source_id"), f"Scout Receipt {index} source_id")
        evidence = require_list(receipt.get("evidence_references"), f"Scout Receipt {index} evidence_references")
        for evidence_index, evidence_reference in enumerate(evidence):
            require_identity(evidence_reference, f"Scout Receipt {index} evidence reference {evidence_index}")
        require(len(evidence) == len(set(evidence)), f"Scout Receipt {index} duplicate evidence reference")
        candidate_count = receipt.get("candidate_count")
        require(type(candidate_count) is int and candidate_count >= 0, f"Scout Receipt {index} candidate_count is invalid")
        require(outcome in SCOUT_OUTCOMES, f"invalid scout outcome: {outcome}")
        if outcome == "complete":
            require(bool(evidence), f"complete Scout Receipt {index} requires evidence")
        if outcome == "not applicable":
            require_nonempty_display(receipt.get("affirmative_evidence"), "not applicable affirmative evidence")
            require(candidate_count == 0, "not applicable Scout Receipt has candidates")
        if outcome == "incomplete":
            require_nonempty_display(receipt.get("failure_reason"), "incomplete failure reason")
        scout_ids.append(scout_id)
        receipt_ids.append(receipt_id)
        receipt_map[scout_id] = receipt
    if complete:
        require(scout_ids == scouts, "Scout Receipt order/coverage differs from manifest")
    require(len(scout_ids) == len(set(scout_ids)), "duplicate scout identity")
    require(len(receipt_ids) == len(set(receipt_ids)), "duplicate Scout Receipt identity")
    return receipt_map


def effect_authority_complete(scenario: dict[str, Any], repository_id: str) -> bool:
    authority = require_object(scenario.get("authority"), f"{scenario.get('id', 'scenario')} authority")
    require_exact_fields(authority, EFFECT_AUTHORITY_FIELDS, "effect authority")
    authority_repository = require_identity(authority.get("repository_id"), "effect authority repository_id")
    return authority_repository == repository_id and all(authority[field] is True for field in AUTHORITY_FIELDS)


def composite_identity(repository_id: Any, operation_id: Any) -> dict[str, str]:
    return {
        "repository_id": require_identity(repository_id, "operation identity repository_id"),
        "operation_id": require_identity(operation_id, "operation identity operation_id"),
    }


def effect_compatibility(scenario: dict[str, Any]) -> str:
    claimed = scenario.get("compatible_prior_result")
    if claimed == "incompatible":
        return "incompatible"
    if claimed != "compatible":
        return "uncertain"
    prepared_payload = scenario.get("prepared_effect_payload")
    existing_payload = scenario.get("existing_effect_payload")
    prepared_fingerprint = scenario.get("prepared_effect_fingerprint")
    existing_fingerprint = scenario.get("existing_effect_fingerprint")
    if any(
        field not in scenario
        for field in (
            "prepared_effect_payload",
            "existing_effect_payload",
            "prepared_effect_fingerprint",
            "existing_effect_fingerprint",
        )
    ):
        return "uncertain"
    if not isinstance(prepared_payload, dict) or not isinstance(existing_payload, dict):
        return "incompatible"
    try:
        require_payload(prepared_payload, RECEIPT_LIMIT, "prepared effect payload")
        require_payload(existing_payload, RECEIPT_LIMIT, "existing effect payload")
        require_sha256(prepared_fingerprint, "prepared effect fingerprint")
        require_sha256(existing_fingerprint, "existing effect fingerprint")
    except ContractError:
        return "incompatible"
    prepared_bytes = canonical_bytes(prepared_payload)
    existing_bytes = canonical_bytes(existing_payload)
    prepared_digest = hashlib.sha256(prepared_bytes).hexdigest()
    existing_digest = hashlib.sha256(existing_bytes).hexdigest()
    if prepared_fingerprint != prepared_digest or existing_fingerprint != existing_digest:
        return "incompatible"
    if prepared_fingerprint != existing_fingerprint or prepared_bytes != existing_bytes:
        return "incompatible"
    return "compatible"


def evaluate_effect(scenario: Any) -> dict[str, Any]:
    scenario = require_object(scenario, "effect scenario")
    scenario_type = scenario.get("scenario_type")
    if scenario_type == "operation":
        try:
            operation_identity = composite_identity(scenario.get("repository_id"), scenario.get("operation_id"))
        except ContractError:
            return {"terminal_outcome": "failed", "invoke_count": 0, "blind_retry": False, "persistence_claim": False, "identity_valid": False}
        authorized = effect_authority_complete(scenario, operation_identity["repository_id"])
        preconditions_match = scenario.get("preconditions_match") is True
        if not authorized or not preconditions_match:
            return {"terminal_outcome": "failed", "invoke_count": 0, "blind_retry": False, "persistence_claim": False, "all_report_writes_blocked": not authorized, "identity_valid": True}
        terminal_read_back = scenario.get("terminal_receipt_read_back") is True
        if scenario.get("desired_state_preexisting") is True:
            compatibility = effect_compatibility(scenario)
            observed = scenario.get("post_read") == "desired state present"
            if compatibility == "incompatible":
                outcome = "failed"
            elif compatibility == "compatible" and observed and terminal_read_back:
                outcome = "already satisfied"
            else:
                outcome = "ambiguous"
            return {"terminal_outcome": outcome, "invoke_count": 0, "blind_retry": False, "persistence_claim": outcome == "already satisfied"}
        if scenario.get("compatible_prior_result") is not None:
            compatibility = effect_compatibility(scenario)
            outcome = "failed" if compatibility == "incompatible" else "ambiguous"
            return {"terminal_outcome": outcome, "invoke_count": 0, "blind_retry": False, "persistence_claim": False}
        invoke_result = scenario.get("invoke_result")
        post_read = scenario.get("post_read")
        if invoke_result == "accepted" and post_read == "exact effect observed" and terminal_read_back:
            outcome = "observed"
        elif invoke_result in {"denied", "provider error"} and post_read == "unchanged" and terminal_read_back:
            outcome = "failed"
        else:
            outcome = "ambiguous"
        return {"terminal_outcome": outcome, "invoke_count": 1, "blind_retry": False, "persistence_claim": outcome in {"observed", "already satisfied", "failed"}}
    if scenario_type == "retry":
        identity = composite_identity(scenario.get("repository_id"), scenario.get("operation_id"))
        retry_identity = composite_identity(scenario.get("retry_repository_id"), scenario.get("retry_operation_id"))
        reused = identity == retry_identity
        allowed = all((effect_authority_complete(scenario, identity["repository_id"]), scenario.get("source_native_absence") is True, scenario.get("preconditions_match") is True, scenario.get("wrapper_scope_unchanged") is True, reused))
        return {"retry_allowed": allowed, "operation_identity": identity, "retry_operation_identity": retry_identity, "operation_identity_reused": reused, "new_operation_identity": False, "invoke_count": 1 if allowed else 0}
    if scenario_type == "identity-collision":
        identity = composite_identity(scenario.get("repository_id"), scenario.get("operation_id"))
        existing = composite_identity(scenario.get("existing_repository_id"), scenario.get("existing_operation_id"))
        result = require_object(scenario.get("result_operation_identity"), "collision result identity")
        result_identity = composite_identity(result.get("repository_id"), result.get("operation_id"))
        minted = scenario.get("minted_replacement_identity")
        if minted is not None:
            minted = require_object(minted, "minted replacement identity")
            composite_identity(minted.get("repository_id"), minted.get("operation_id"))
        if identity != existing:
            outcome = "failed"
        else:
            compatibility = effect_compatibility(scenario)
            outcome = {
                "compatible": "already satisfied",
                "incompatible": "failed",
                "uncertain": "ambiguous",
            }[compatibility]
        return {"operation_identity": identity, "existing_operation_identity": existing, "operation_identity_preserved": result_identity == identity, "replacement_identity_minted": minted is not None, "terminal_outcome": outcome, "invoke_count": 0}
    if scenario_type == "completion-partition":
        named = require_list(scenario.get("named_work"), "named_work")
        affected = require_list(scenario.get("affected_by_ambiguity"), "affected_work")
        independent = require_list(scenario.get("independent_continued"), "remaining_unblocked_work")
        unique = len(named) == len(set(named)) and len(affected) == len(set(affected)) and len(independent) == len(set(independent))
        affected_set = set(affected)
        remaining_set = set(independent)
        return {
            "affected_work": affected,
            "remaining_unblocked_work": {item: "continued" for item in independent},
            "disjoint_exhaustive": unique
            and affected_set.isdisjoint(remaining_set)
            and affected_set | remaining_set == set(named),
            "whole_run_completion": "withheld",
        }
    if scenario_type == "delegation":
        handoff = require_object(scenario.get("handoff"), "handoff")
        complete = all(handoff.get(field) for field in ("destination", "authorized_executor", "exact_work"))
        return {"remaining_disposition": "delegated" if complete and handoff.get("read_back") is True else "gated"}
    if scenario_type == "optional-scout":
        return {"dependent_work_blocked": bool(scenario.get("missing_scout")), "independent_work": "continued" if scenario.get("independent_work") is True else "gated"}
    if scenario_type == "terminal-receipt":
        return {"persistence_claim": scenario.get("terminal_receipt_persisted") is True and scenario.get("terminal_receipt_read_back") is True}
    if scenario_type == "caller-completion":
        accepted = scenario.get("terminal_capability_active") is True and scenario.get("caller_accepts") is True
        pending = require_list(scenario.get("pending_decision_ids"), "pending decisions")
        assignment = require_list(scenario.get("assignment_persisted_decision_ids"), "assignment-persisted decisions")
        require(len(pending) == len(set(pending)), "duplicate pending decision")
        require(len(assignment) == len(set(assignment)), "duplicate assignment-persisted decision")
        assignment_proven = scenario.get("assignment_persistence_authorized") is True and scenario.get("assignment_persistence_read_back") is True
        assignment_set = set(assignment) if assignment_proven else set()
        require(assignment_set <= set(pending), "assignment persisted an unknown decision")
        caller = [decision for decision in pending if decision not in assignment_set]
        return {
            "terminal_reports": 1 if accepted else 0,
            "assignment_persisted_decisions": len(assignment_set) if accepted else 0,
            "decisions_carried_for_caller": len(caller) if accepted else 0,
            "decision_partition_exact": accepted
            and len(assignment_set) + len(caller) == len(pending),
            "assignment_persistence_proven": assignment_proven,
            "caller_only_allocation_valid": not assignment_set,
            "self_settled_before_acceptance": False,
        }
    if scenario_type == "repair":
        proof = all(scenario.get(field) is True for field in ("complete_integrity_read", "exact_prepared_receipt_reused", "preconditions_match", "anchored_receipt_valid", "history_tail_missing"))
        repository_id = require_identity(scenario.get("repository_id"), "repair repository_id")
        if effect_authority_complete(scenario, repository_id) and proof and scenario.get("body_anchor_ahead_by") == 1:
            return {"append_exact_stored_receipt": 1, "rewrite_body": False, "readback_required": True}
        return {"repair_allowed": False, "invoke_count": 0, "terminal_outcome": "ambiguous"}
    raise ContractError(f"unknown effect scenario type: {scenario_type}")


def evaluate_gates(facts: Any) -> dict[str, Any]:
    facts = require_object(facts, "gate facts")
    require(set(facts) == set(GATE_ORDER), "gate facts do not cover the six ordered gates")
    first_failing = next((gate for gate in GATE_ORDER if facts[gate] is not True), None)
    return {"eligible": first_failing is None, "first_failing_gate": first_failing, "attention_state": "Action required" if facts["protected boundary"] is not True else "Routine", "gate_order": list(GATE_ORDER)}


def require_retained_rows(retained: Any, limit: int) -> list[str]:
    retained = require_list(retained, "retained rows")
    identities = [require_identity(item, f"retained row {index}") for index, item in enumerate(retained)]
    require(len(identities) == len(set(identities)) and len(identities) <= limit, "retained-row order/capacity invalid")
    return identities


def render_capacity_with_limit(retained: Any, candidates: Any, limit: int) -> dict[str, Any]:
    retained = require_retained_rows(retained, limit)
    candidates = require_list(candidates, "eligible candidates")
    eligible = sum(evaluate_gates(require_object(item, "candidate").get("gate_facts"))["eligible"] for item in candidates)
    recommendations = min(limit - len(retained), eligible)
    return {"rendered_slots": limit, "retained_first": True, "available_slots": limit - len(retained) - recommendations, "recommendations": recommendations}


def render_capacity(retained: Any, candidates: Any, policy_path: Path) -> dict[str, Any]:
    return render_capacity_with_limit(retained, candidates, portfolio_limit(policy_path))


def validate_reconciliation_authority(
    scenario: dict[str, Any],
    records: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    authority = require_object(scenario.get("authority"), f"{scenario.get('id', 'scenario')} reconciliation authority")
    require_exact_fields(authority, RECONCILIATION_AUTHORITY_FIELDS, "reconciliation authority")
    require(authority.get("schema") == "repo-gardener-reconciliation-authority/v1", "reconciliation authority schema mismatch")
    require(authority.get("repository_id") == records.get("repository_id"), "reconciliation authority repository mismatch")
    require(authority.get("report_id") == records.get("report_id"), "reconciliation authority report mismatch")
    require(authority.get("writer_id") == records.get("writer_id"), "reconciliation authority writer mismatch")
    require(authority.get("run_id") == manifest.get("run_id"), "reconciliation authority run mismatch")
    for field in RECONCILIATION_WRITE_PROOFS:
        require(type(authority.get(field)) is bool, f"reconciliation authority {field} must be boolean")
    return authority


def reconciliation_write_authorized(authority: dict[str, Any]) -> bool:
    return all(authority[field] is True for field in RECONCILIATION_WRITE_PROOFS)


def evaluate_reconciliation(
    scenario: Any,
    records: dict[str, Any],
    manifest: dict[str, Any],
    receipt_sets: dict[str, dict[str, dict[str, Any]]],
    complete_receipts: dict[str, dict[str, Any]],
    policy_limit: int,
) -> dict[str, Any]:
    scenario = require_object(scenario, "reconciliation scenario")
    scenario_type = scenario.get("scenario_type")
    if scenario_type == "caller-ownership":
        require_exact_fields(scenario, {"id", "scenario_type", "authority"}, "caller-ownership scenario")
        authority = validate_reconciliation_authority(scenario, records, manifest)
        can_write = reconciliation_write_authorized(authority)
        return {"writes": 1 if can_write else 0, "last_safe_stage": "Act" if can_write else "Sense"}
    if scenario_type == "interrupted-run":
        return {"outcome": "interrupted" if scenario.get("older_run_start") == "unmatched" else "current", "uses_elapsed_time": False}
    if scenario_type == "lifecycle":
        events = require_list(scenario.get("events"), "lifecycle events")
        pairs = (("append-run-start", "read-run-start"), ("persist-reconciliation", "read-reconciliation"), ("persist-manifest", "read-manifest"), ("append-decisions", "read-decisions"), ("append-terminal", "read-terminal"), ("render-report", "read-report"))
        all_present = all(item in events for pair in pairs for item in pair)
        return {"ordered": tuple(events) == REQUIRED_EVENTS, "terminal_before_report": events.index("read-terminal") < events.index("render-report") if "read-terminal" in events and "render-report" in events else False, "readback_after_each_write": all(events.index(read) == events.index(write) + 1 for write, read in pairs) if all_present else False}
    if scenario_type == "report-fact-readbacks":
        report_facts = require_list(scenario.get("report_facts"), "report facts")
        names = [require_identity(require_object(item, "report fact").get("fact"), "report fact identity") for item in report_facts]
        require(len(names) == len(set(names)), "duplicate report fact identity")
        persisted = [item["fact"] for item in report_facts if item.get("narrow_wrapper_persisted") is True and item.get("authoritative_readback_completed") is True]
        return {"persistence_claim": bool(persisted), "persisted_report_facts": persisted, "source_fact_persistence_claim": False}
    if scenario_type == "missing-receipt":
        receipts = receipt_sets[scenario["receipt_fixture"]]
        receipt = receipts.get(scenario["expected_scout"])
        if receipt is None:
            return {"coverage": "incomplete (no receipt)", "candidate_count": None}
        if receipt["outcome"] == "incomplete" or (receipt["outcome"] == "not applicable" and not receipt.get("affirmative_evidence")):
            return {"coverage": "incomplete", "candidate_count": None}
        return {"coverage": receipt["outcome"], "candidate_count": receipt.get("candidate_count", 0)}
    if scenario_type == "not-applicable":
        return {"coverage": "not applicable" if scenario.get("affirmative_evidence") else "incomplete"}
    if scenario_type == "untrusted-text":
        return {"derived_effects": 0}
    if scenario_type == "dedupe":
        observations = require_list(scenario.get("observations"), "dedupe observations")
        source_ids = {require_object(item, "dedupe observation").get("source_id") for item in observations}
        require(len(source_ids) == 1, "dedupe observations do not share stable source identity")
        for item in observations:
            receipt = complete_receipts.get(item["lane"])
            require(receipt is not None and receipt["receipt_id"] == item["receipt_id"], "dedupe cites an unknown Scout Receipt")
        return {"candidate_count": 1, "preserved_lanes": len({item["lane"] for item in observations}), "preserved_receipts": len({item["receipt_id"] for item in observations})}
    if scenario_type == "gates":
        result = evaluate_gates(scenario.get("gate_facts"))
        result.pop("eligible")
        return result
    if scenario_type == "shared-candidate":
        gate_facts = dict(require_object(scenario.get("gate_facts"), "gate facts"))
        if scenario.get("security_evidence") != "complete":
            gate_facts["evidence"] = False
        result = evaluate_gates(gate_facts)
        return {"eligible_under_owner_lane": result["eligible"], **({"first_failing_gate": result["first_failing_gate"]} if not result["eligible"] else {})}
    if scenario_type == "capacity":
        return render_capacity_with_limit(scenario.get("retained_rows"), scenario.get("eligible_candidates", []), policy_limit)
    if scenario_type == "critical-capacity":
        limit = policy_limit
        retained = require_retained_rows(scenario.get("retained_rows"), limit)
        require(len(retained) == limit, "critical capacity fixture is not full")
        candidate = require_object(scenario.get("critical_candidate"), "critical candidate")
        eligible = evaluate_gates(candidate.get("gate_facts"))["eligible"]
        return {"rendered_slots": limit, "recommendations": 0, "preemption_proposal": eligible and bool(scenario.get("interruptible_row")), "rows_changed": 0}
    if scenario_type == "disabled-observations":
        ordinary, critical = require_list(scenario.get("observations"), "disabled observations")
        return {"ordinary_attention": "Routine (disabled lane)" if not ordinary["critical"] else "Action required (lane disabled)", "critical_attention": "Action required (lane disabled)" if critical["critical"] and critical.get("applicable") else "Routine (disabled lane)", "rows_changed": 0, "source_mutations": 0}
    if scenario_type == "terminal-row":
        bound = scenario.get("terminal_source_binding") is True
        return {
            "stable_binding_dispositions": ["released-same-update", "action-required-owner-release"],
            "row_action": "release-or-owner-release" if bound else "unchanged-unassociated",
        }
    if scenario_type == "honest-no-op":
        require_exact_fields(
            scenario,
            {"id", "scenario_type", "receipt_fixture", "reconciliation_complete", "gate_passing_candidates", "authority"},
            "honest-no-op scenario",
        )
        authority = validate_reconciliation_authority(scenario, records, manifest)
        require(reconciliation_write_authorized(authority), "honest no-op lacks complete independent write authority")
        receipts = receipt_sets[scenario["receipt_fixture"]]
        complete = set(receipts) == set(manifest["scouts"]) and all(item["outcome"] in {"complete", "not applicable"} for item in receipts.values())
        routine = complete and scenario.get("reconciliation_complete") is True and scenario.get("gate_passing_candidates") == 0
        return {"attention_state": "Routine" if routine else "Action required", "next_owner_action": "none" if routine else "complete missing coverage", "rendered_slots": policy_limit}
    if scenario_type == "history":
        require_exact_fields(scenario, {"id", "scenario_type", "history_pages_complete", "authority"}, "history scenario")
        authority = validate_reconciliation_authority(scenario, records, manifest)
        valid = scenario.get("history_pages_complete") is True
        can_write = valid and reconciliation_write_authorized(authority)
        return {"integrity": "valid" if valid else "unavailable", "writes": 1 if can_write else 0}
    if scenario_type == "reconciliation-order":
        require_exact_fields(
            scenario,
            {"id", "scenario_type", "unmatched_intents", "effect_reconciled", "discovery_started_after_reconciliation"},
            "reconciliation-order scenario",
        )
        unmatched_intents = scenario.get("unmatched_intents")
        require(isinstance(unmatched_intents, int) and not isinstance(unmatched_intents, bool) and unmatched_intents >= 0, "unmatched intent count must be a nonnegative integer")
        reconciled = scenario.get("effect_reconciled") is True
        valid = reconciled and scenario.get("discovery_started_after_reconciliation") is True
        return {
            "ordering_valid": valid,
            "terminal_outcome": "observed" if reconciled else "ambiguous",
            "terminal_receipt_recording": "idempotent" if reconciled else "withheld",
        }
    raise ContractError(f"unknown reconciliation scenario type: {scenario_type}")


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_input(source: str) -> Any:
    if source == "-":
        return json.load(sys.stdin)
    return _load(Path(source))


def _versioned_input(value: Any, schema: str, fields: set[str]) -> dict[str, Any]:
    value = require_object(value, f"{schema} input")
    require_exact_fields(value, {"schema", *fields}, f"{schema} input")
    require(value.get("schema") == schema, f"input schema mismatch: expected {schema}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    register_parser = subparsers.add_parser("validate-register")
    register_parser.add_argument("--register", type=Path, required=True)
    register_parser.add_argument("--manifest", type=Path, required=True)
    register_parser.add_argument("--authentication", type=Path, required=True)
    register_parser.add_argument("--policy", type=Path, required=True)
    receipt_parser = subparsers.add_parser("validate-scout-receipts")
    receipt_parser.add_argument("--receipts", type=Path, required=True)
    receipt_parser.add_argument("--manifest", type=Path, required=True)
    receipt_parser.add_argument("--allow-incomplete-coverage", action="store_true")
    body_parser = subparsers.add_parser("validate-body")
    body_parser.add_argument("--body", type=Path, required=True)
    for command in ("effect-v1", "completion-v1", "gates-v1"):
        input_parser = subparsers.add_parser(command)
        input_parser.add_argument("--input", required=True)
    for command in ("reconciliation-v1", "capacity-v1"):
        input_parser = subparsers.add_parser(command)
        input_parser.add_argument("--input", required=True)
        input_parser.add_argument("--policy", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "validate-register":
        result = validate_register(_load(args.register), _load(args.manifest), _load(args.authentication), args.policy)
    elif args.command == "validate-scout-receipts":
        canonical_policy = Path(__file__).resolve().parent.parent / "assets" / "policy-template.yaml"
        _, expected_scouts = policy_contract(canonical_policy)
        result = {
            "scouts": sorted(
                validate_scout_receipts(
                    _load(args.receipts),
                    _load(args.manifest),
                    complete=not args.allow_incomplete_coverage,
                    expected_scouts=expected_scouts,
                )
            )
        }
    elif args.command == "validate-body":
        body = args.body.read_text(encoding="utf-8")
        result = {"body_bytes": validate_body(body)}
    elif args.command == "effect-v1":
        data = _versioned_input(_load_input(args.input), "repo-gardener-effect-input/v1", {"scenario"})
        scenario = require_object(data["scenario"], "effect scenario")
        require(scenario.get("scenario_type") in EFFECT_SCENARIOS, "effect-v1 received a non-effect scenario")
        result = evaluate_effect(scenario)
    elif args.command == "completion-v1":
        data = _versioned_input(_load_input(args.input), "repo-gardener-completion-input/v1", {"scenario"})
        scenario = require_object(data["scenario"], "completion scenario")
        require(scenario.get("scenario_type") in COMPLETION_SCENARIOS, "completion-v1 received a non-completion scenario")
        result = evaluate_effect(scenario)
    elif args.command == "gates-v1":
        data = _versioned_input(_load_input(args.input), "repo-gardener-gates-input/v1", {"facts"})
        result = evaluate_gates(data["facts"])
    elif args.command == "capacity-v1":
        data = _versioned_input(_load_input(args.input), "repo-gardener-capacity-input/v1", {"retained", "candidates"})
        result = render_capacity(data["retained"], data["candidates"], args.policy)
    else:
        data = _versioned_input(
            _load_input(args.input),
            "repo-gardener-reconciliation-input/v1",
            {"scenario", "register", "authentication", "manifest", "receipt_sets", "complete_receipts"},
        )
        records = require_object(data["register"], "reconciliation register")
        authentication = require_object(data["authentication"], "reconciliation provider authentication evidence")
        register_result = validate_register(records, data["manifest"], authentication, args.policy)
        manifest = register_result["manifest"]
        raw_receipt_sets = require_object(data["receipt_sets"], "reconciliation receipt sets")
        require(bool(raw_receipt_sets), "reconciliation receipt sets are empty")
        receipt_sets: dict[str, dict[str, dict[str, Any]]] = {}
        for label, envelope in raw_receipt_sets.items():
            require_identity(label, "reconciliation receipt-set identity")
            receipt_sets[label] = validate_scout_receipts(envelope, manifest, complete=False)
        complete_receipts = validate_scout_receipts(data["complete_receipts"], manifest, complete=True)
        result = evaluate_reconciliation(
            data["scenario"],
            records,
            manifest,
            receipt_sets,
            complete_receipts,
            register_result["portfolio_limit"],
        )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ContractError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
