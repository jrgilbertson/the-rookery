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
CURRENT_PORTFOLIO_BEGIN = "<!-- orchestrator:current-portfolio:v1:begin -->"
CURRENT_PORTFOLIO_END = "<!-- orchestrator:current-portfolio:v1:end -->"
HISTORY_RECEIPT_BEGIN = "<!-- orchestrator:history-receipt:v1:begin -->"
HISTORY_RECEIPT_END = "<!-- orchestrator:history-receipt:v1:end -->"
GITHUB_SNAPSHOT_FIELDS = {
    "schema",
    "configured_repository_id",
    "configured_report_issue_id",
    "configured_writer_id",
    "issue",
    "comment_pages_complete",
    "comment_pages",
}
ORCHESTRATOR_REGISTER_FIELDS = {
    "schema",
    "repository_id",
    "report_issue_id",
    "writer_id",
    "register_revision",
    "last_operation_id",
    "last_operation_fingerprint",
    "history_anchor",
    "rows",
}
ORCHESTRATOR_REGISTER_FIELD_ORDER = (
    "schema",
    "repository_id",
    "report_issue_id",
    "writer_id",
    "register_revision",
    "last_operation_id",
    "last_operation_fingerprint",
    "history_anchor",
    "rows",
)
ORCHESTRATOR_ROW_FIELDS = {
    "row_id",
    "source_id",
    "source_revision",
    "description",
    "work_state",
    "lane",
    "outcome",
    "rationale",
    "risk",
    "budget_use",
    "evidence",
    "next_action",
    "row_revision",
}
ORCHESTRATOR_ROW_FIELD_ORDER = (
    "row_id",
    "source_id",
    "source_revision",
    "description",
    "work_state",
    "lane",
    "outcome",
    "rationale",
    "risk",
    "budget_use",
    "evidence",
    "next_action",
    "row_revision",
)
ORCHESTRATOR_RECEIPT_FIELDS = {
    "schema",
    "sequence",
    "previous_hash",
    "receipt_hash",
    "operation_id",
    "kind",
    "run_id",
    "payload",
}
ORCHESTRATOR_RECEIPT_FIELD_ORDER = (
    "schema",
    "sequence",
    "previous_hash",
    "receipt_hash",
    "operation_id",
    "kind",
    "run_id",
    "payload",
)
ORCHESTRATOR_HISTORY_KINDS = {
    "decision",
    "effect",
    "evidence",
    "manifest",
    "release",
    "run",
    "run-closed",
    "run-opened",
    "scout",
}
HISTORY_ANCHOR_FIELDS = {"sequence", "head", "latest_receipt"}
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
COMPLETION_SCENARIOS = {"completion-partition", "delegation", "optional-scout", "caller-completion"}
GATE_ORDER = (
    "current source",
    "policy and authority",
    "evidence",
    "conflict",
    "protected boundary",
    "capability",
)
RECONCILIATION_WORK_FIELDS = {"repository_id", "operation_id", "lane", "dependencies"}
EFFECT_OPERATION_FIELDS = {"kind", "run_id", "payload", "rows", "projection"}
EFFECT_PREPARED_FIELDS = {
    "schema",
    "repository_id",
    "report_issue_id",
    "writer_id",
    "operation",
    "operation_id",
    "operation_fingerprint",
    "expected_pre_body_fingerprint",
    "expected_pre_revision",
    "expected_pre_head",
    "expected_post_revision",
    "expected_post_head",
    "receipt_hash",
    "body",
    "comment",
}
RESERVED_REPORT_SEQUENCES = (
    CURRENT_PORTFOLIO_BEGIN,
    CURRENT_PORTFOLIO_END,
    HISTORY_RECEIPT_BEGIN,
    HISTORY_RECEIPT_END,
)


class ContractError(Exception):
    """A machine contract is malformed or cannot support the claimed result."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except ValueError as error:
        raise ContractError("canonical JSON contains a non-finite number") from error


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
    require(all(0x20 <= ord(character) <= 0x7E for character in value), f"{label} must contain only printable ASCII")
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
        parsed = datetime.fromisoformat(f"{value[:-1]}+00:00")
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
    for line in lanes:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        require(
            re.fullmatch(r"  [a-z0-9][a-z0-9-]*:\s*(?:#.*)?", line) is not None
            or re.fullmatch(r"    mutation:\s*(?:true|false)\s*(?:#.*)?", line) is not None,
            "policy lanes contain an unparsed or inline entry",
        )
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


def orchestrator_receipt_hash(
    receipt: dict[str, Any],
    repository_id: str,
    report_issue_id: str,
) -> str:
    """Hash one live-shaped receipt without conferring provider provenance."""
    receipt_without_hash = {
        field: receipt[field]
        for field in ORCHESTRATOR_RECEIPT_FIELD_ORDER
        if field != "receipt_hash"
    }
    material = b"\0".join(
        (
            b"orchestrator-history/v1",
            repository_id.encode("ascii"),
            report_issue_id.encode("ascii"),
            json.dumps(receipt_without_hash, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        )
    )
    return hashlib.sha256(material).hexdigest()


def _extract_marked_json(body: str, begin: str, end: str, label: str, *, fenced: bool) -> tuple[str, dict[str, Any]]:
    require(body.count(begin) == 1 and body.count(end) == 1, f"{label} markers must appear exactly once")
    start = body.find(begin)
    finish = body.find(end)
    require(start < finish, f"{label} markers are reordered")
    before = body[:start]
    after = body[finish + len(end) :]
    require(begin not in before + after and end not in before + after, f"{label} contains extra markers")
    raw = body[start + len(begin) : finish]
    if fenced:
        require(raw.startswith("\n```json\n") and raw.endswith("\n```\n"), f"{label} must contain one fenced canonical JSON object")
        raw_json = raw[len("\n```json\n") : -len("\n```\n")]
    else:
        terminal = body[finish + len(end) :]
        require(start == 0 and terminal in {"", "\n"}, f"{label} contains surrounding text")
        require(raw.startswith("\n") and raw.endswith("\n"), f"{label} must contain canonical JSON on one bounded block")
        raw_json = raw[1:-1]
    try:
        value = json.loads(raw_json)
    except json.JSONDecodeError as error:
        raise ContractError(f"{label} JSON is invalid") from error
    value = require_object(value, f"{label} JSON")
    try:
        compact_json = json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except ValueError as error:
        raise ContractError(f"{label} JSON contains a non-finite number") from error
    require(compact_json == raw_json.encode("utf-8"), f"{label} JSON is not canonical")
    return raw_json, value


def _validate_orchestrator_receipt(
    receipt: dict[str, Any],
    *,
    index: int,
    previous_hash: str,
    repository_id: str,
    report_issue_id: str,
) -> str:
    label = f"history receipt {index}"
    require_exact_fields(receipt, ORCHESTRATOR_RECEIPT_FIELDS, label)
    require(tuple(receipt) == ORCHESTRATOR_RECEIPT_FIELD_ORDER, f"{label} field order mismatch")
    require(receipt.get("schema") == "orchestrator-history/v1", f"{label} schema mismatch")
    require(type(receipt.get("sequence")) is int and receipt["sequence"] == index, f"{label} sequence discontinuity")
    require(receipt.get("previous_hash") == previous_hash, f"{label} previous hash mismatch")
    require_identity(receipt.get("operation_id"), f"{label} operation_id")
    kind = require_identity(receipt.get("kind"), f"{label} kind")
    require(kind in ORCHESTRATOR_HISTORY_KINDS, f"{label} kind is invalid")
    require_identity(receipt.get("run_id"), f"{label} run_id")
    require_object(receipt.get("payload"), f"{label} payload")
    require_payload(receipt, RECEIPT_LIMIT, label)
    expected_hash = orchestrator_receipt_hash(receipt, repository_id, report_issue_id)
    require(receipt.get("receipt_hash") == expected_hash, f"{label} hash mismatch")
    return expected_hash


def _validate_orchestrator_register(
    register: dict[str, Any],
    *,
    repository_id: str,
    report_issue_id: str,
    writer_id: str,
) -> None:
    require_exact_fields(register, ORCHESTRATOR_REGISTER_FIELDS, "register")
    require(tuple(register) == ORCHESTRATOR_REGISTER_FIELD_ORDER, "register field order mismatch")
    require(register.get("schema") == "orchestrator-register/v1", "register schema mismatch")
    require(register.get("repository_id") == repository_id, "register repository mismatch")
    require(register.get("report_issue_id") == report_issue_id, "register report mismatch")
    require(register.get("writer_id") == writer_id, "configured writer mismatch")
    require(type(register.get("register_revision")) is int and register["register_revision"] >= 0, "invalid register revision")
    last_operation_id = register.get("last_operation_id")
    last_operation_fingerprint = register.get("last_operation_fingerprint")
    require(last_operation_id is None or require_identity(last_operation_id, "last operation_id"), "invalid last operation_id")
    require(last_operation_fingerprint is None or SHA256.fullmatch(last_operation_fingerprint) is not None, "invalid last operation fingerprint")

    rows = require_list(register.get("rows"), "register rows")
    require(len(rows) <= RELEASE_A_PORTFOLIO_LIMIT, f"portfolio exceeds policy limit {RELEASE_A_PORTFOLIO_LIMIT}")
    row_ids: list[str] = []
    source_ids: list[str] = []
    for index, raw_row in enumerate(rows):
        row = require_object(raw_row, f"row {index}")
        require_exact_fields(row, ORCHESTRATOR_ROW_FIELDS, f"row {index}")
        require(tuple(row) == ORCHESTRATOR_ROW_FIELD_ORDER, f"row {index} field order mismatch")
        row_ids.append(require_identity(row.get("row_id"), f"row {index} row_id"))
        source_ids.append(require_identity(row.get("source_id"), f"row {index} source_id"))
        require_identity(row.get("source_revision"), f"row {index} source_revision")
        require_nonempty_display(row.get("description"), f"row {index} description")
        require(row.get("work_state") in {"To do", "In process"}, f"invalid row work state: {row.get('work_state')}")
        require(require_identity(row.get("lane"), f"row {index} lane") in RELEASE_A_LANES, f"row {index} lane is outside installed inventory")
        for field in ("outcome", "rationale", "risk", "budget_use", "next_action"):
            require_nonempty_display(row.get(field), f"row {index} {field}")
        evidence = require_list(row.get("evidence"), f"row {index} evidence")
        require(bool(evidence), f"row {index} evidence is empty")
        for evidence_index, evidence_item in enumerate(evidence):
            require_identity(evidence_item, f"row {index} evidence {evidence_index}")
        require(len(evidence) == len(set(evidence)), f"row {index} duplicate evidence")
        require(type(row.get("row_revision")) is int and row["row_revision"] >= 0, f"row {index} invalid revision")
    require(len(row_ids) == len(set(row_ids)), "duplicate row identity")
    require(len(source_ids) == len(set(source_ids)), "duplicate source identity")


def normalize_github_register_snapshot(snapshot: Any) -> dict[str, Any]:
    """Normalize supplied GitHub bytes; do not claim freshness or provenance."""
    snapshot = require_object(snapshot, "GitHub register snapshot")
    require_exact_fields(snapshot, GITHUB_SNAPSHOT_FIELDS, "GitHub register snapshot")
    require(snapshot.get("schema") == "repo-gardener-github-register-snapshot/v1", "GitHub register snapshot schema mismatch")
    repository_id = require_identity(snapshot.get("configured_repository_id"), "configured repository_id")
    report_issue_id = require_identity(snapshot.get("configured_report_issue_id"), "configured report issue_id")
    writer_id = require_identity(snapshot.get("configured_writer_id"), "configured writer_id")

    issue = require_object(snapshot.get("issue"), "GitHub issue")
    require(type(issue.get("id")) is int and issue["id"] > 0, "GitHub issue numeric id is invalid")
    require(issue.get("node_id") == report_issue_id, "issue report mismatch")
    provider_comment_count = issue.get("comments")
    require(
        type(provider_comment_count) is int and provider_comment_count >= 0,
        "GitHub issue comment total is invalid",
    )
    body = issue.get("body")
    validate_body(body)
    body_machine_json, register = _extract_marked_json(
        body,
        CURRENT_PORTFOLIO_BEGIN,
        CURRENT_PORTFOLIO_END,
        "managed body",
        fenced=True,
    )
    _validate_orchestrator_register(
        register,
        repository_id=repository_id,
        report_issue_id=report_issue_id,
        writer_id=writer_id,
    )

    require(snapshot.get("comment_pages_complete") is True, "comment pagination is incomplete")
    pages = require_list(snapshot.get("comment_pages"), "comment pages")
    require(bool(pages), "comment page sequence is incomplete")
    page_size = len(require_list(pages[0], "comment page 1"))
    require(page_size <= 100, "comment page 1 exceeds the configured page size")
    if len(pages) > 1:
        require(page_size > 0, "comment page sequence is incomplete")
    history_receipts: list[dict[str, Any]] = []
    ordinary_comment_ids: list[str] = []
    provider_comment_fingerprints: list[str] = []
    seen_comment_ids: set[str] = set()
    seen_numeric_comment_ids: set[int] = set()
    previous_hash = "GENESIS"
    for expected_page, raw_page in enumerate(pages, start=1):
        comments = require_list(raw_page, f"comment page {expected_page}")
        require(len(comments) <= 100, f"comment page {expected_page} exceeds the configured page size")
        require(
            expected_page == len(pages) or len(comments) == page_size,
            "comment page sequence is incomplete",
        )
        require(
            len(pages) == 1 or expected_page < len(pages) or len(comments) <= page_size,
            "comment page sequence is incomplete",
        )
        for raw_comment in comments:
            comment = require_object(raw_comment, "provider comment")
            numeric_comment_id = comment.get("id")
            require(type(numeric_comment_id) is int and numeric_comment_id > 0, "provider comment numeric id is invalid")
            comment_id = require_identity(comment.get("node_id"), "provider comment node_id")
            require(
                comment_id not in seen_comment_ids and numeric_comment_id not in seen_numeric_comment_ids,
                "duplicate provider comment identity",
            )
            seen_comment_ids.add(comment_id)
            seen_numeric_comment_ids.add(numeric_comment_id)
            user = require_object(comment.get("user"), "provider comment user")
            author_id = require_identity(user.get("node_id"), "provider comment author node_id")
            comment_body = comment.get("body")
            require(isinstance(comment_body, str), "provider comment body must be text")
            require(len(comment_body.encode("utf-8")) <= BODY_LIMIT, f"provider comment body exceeds {BODY_LIMIT} UTF-8 bytes")
            provider_comment_fingerprints.append(hashlib.sha256(canonical_bytes(comment)).hexdigest())
            has_reserved_marker = HISTORY_RECEIPT_BEGIN in comment_body or HISTORY_RECEIPT_END in comment_body
            if not has_reserved_marker:
                ordinary_comment_ids.append(comment_id)
                continue
            require(author_id == writer_id, "reserved receipt marker from non-writer comment")
            raw_receipt_json, receipt = _extract_marked_json(
                comment_body,
                HISTORY_RECEIPT_BEGIN,
                HISTORY_RECEIPT_END,
                f"writer comment {comment_id}",
                fenced=False,
            )
            sequence = len(history_receipts) + 1
            previous_hash = _validate_orchestrator_receipt(
                receipt,
                index=sequence,
                previous_hash=previous_hash,
                repository_id=repository_id,
                report_issue_id=report_issue_id,
            )
            history_receipts.append(
                {
                    "provider_comment_id": comment_id,
                    "raw_receipt_json": raw_receipt_json,
                    "receipt": receipt,
                }
            )

    require(
        len(seen_comment_ids) == provider_comment_count,
        "comment pagination count does not match provider total",
    )

    anchor = require_object(register.get("history_anchor"), "body history anchor")
    require_exact_fields(anchor, HISTORY_ANCHOR_FIELDS, "body history anchor")
    require(tuple(anchor) == ("sequence", "head", "latest_receipt"), "body history anchor field order mismatch")
    sequence = len(history_receipts)
    anchor_sequence = anchor.get("sequence")
    require(type(anchor_sequence) is int and anchor_sequence >= 0, "body history anchor sequence is invalid")
    require(
        register["register_revision"] == anchor_sequence,
        "register revision does not match body history anchor sequence",
    )
    if anchor_sequence == sequence:
        require(anchor.get("head") == previous_hash, "body history anchor head mismatch")
        expected_latest = history_receipts[-1]["receipt"] if history_receipts else None
        require(anchor.get("latest_receipt") == expected_latest, "body history anchor latest receipt mismatch")
        anchor_status = "exact"
    elif anchor_sequence == sequence + 1:
        latest = require_object(anchor.get("latest_receipt"), "body history anchor latest receipt")
        anchored_hash = _validate_orchestrator_receipt(
            latest,
            index=anchor_sequence,
            previous_hash=previous_hash,
            repository_id=repository_id,
            report_issue_id=report_issue_id,
        )
        require(anchor.get("head") == anchored_hash, "body history anchor head mismatch")
        anchor_status = "one-receipt-ahead"
    else:
        raise ContractError("body history anchor sequence mismatch")
    if anchor_sequence == 0:
        require(register.get("last_operation_id") is None and register.get("last_operation_fingerprint") is None, "genesis operation markers must be null")
    else:
        latest = require_object(anchor.get("latest_receipt"), "body history anchor latest receipt")
        require(tuple(latest) == ORCHESTRATOR_RECEIPT_FIELD_ORDER, "body history anchor receipt field order mismatch")
        require(register.get("last_operation_id") == latest.get("operation_id"), "last operation marker mismatch")
        require_sha256(register.get("last_operation_fingerprint"), "last operation fingerprint")

    return {
        "schema": "repo-gardener-github-register-view/v1",
        "repository_id": repository_id,
        "report_issue_id": report_issue_id,
        "writer_id": writer_id,
        "body": body,
        "body_machine_json": body_machine_json,
        "body_fingerprint": hashlib.sha256(body_machine_json.encode("utf-8")).hexdigest(),
        "register": register,
        "history_sequence": sequence,
        "history_head": previous_hash,
        "anchor_status": anchor_status,
        "history_receipts": history_receipts,
        "ordinary_comment_ids": ordinary_comment_ids,
        "comment_snapshot_fingerprint": hashlib.sha256(canonical_bytes(provider_comment_fingerprints)).hexdigest(),
        "comment_pages_complete": True,
        "structural_integrity": "valid",
        "provenance": "unverified",
    }


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


def composite_identity(repository_id: Any, operation_id: Any) -> dict[str, str]:
    return {
        "repository_id": require_identity(repository_id, "operation identity repository_id"),
        "operation_id": require_identity(operation_id, "operation identity operation_id"),
    }


def _reject_reserved_report_content(value: Any, label: str) -> None:
    if isinstance(value, str):
        require(
            not any(marker in value for marker in RESERVED_REPORT_SEQUENCES),
            f"{label} contains a reserved report sequence",
        )
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_reserved_report_content(item, f"{label}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            _reject_reserved_report_content(key, f"{label} key")
            _reject_reserved_report_content(item, f"{label}.{key}")


def _effect_operation(operation: Any) -> dict[str, Any]:
    operation = require_object(operation, "effect operation")
    require_exact_fields(operation, EFFECT_OPERATION_FIELDS, "effect operation")
    require(require_identity(operation.get("kind"), "effect kind") in ORCHESTRATOR_HISTORY_KINDS, "effect kind is invalid")
    require_identity(operation.get("run_id"), "effect run_id")
    require_object(operation.get("payload"), "effect payload")
    require_list(operation.get("rows"), "effect rows")
    require(isinstance(operation.get("projection"), str), "effect projection must be text")
    require_payload(operation, BODY_LIMIT, "effect operation")
    _reject_reserved_report_content(operation, "effect operation")
    rows = []
    for index, raw_row in enumerate(operation["rows"]):
        row = require_object(raw_row, f"effect row {index}")
        require_exact_fields(row, ORCHESTRATOR_ROW_FIELDS, f"effect row {index}")
        rows.append({field: row[field] for field in ORCHESTRATOR_ROW_FIELD_ORDER})
    return {
        "kind": operation["kind"],
        "run_id": operation["run_id"],
        "payload": operation["payload"],
        "rows": rows,
        "projection": operation["projection"],
    }


def _effect_operation_id(
    *,
    repository_id: str,
    report_issue_id: str,
    writer_id: str,
    expected_pre_revision: int,
    expected_pre_head: str,
    operation: dict[str, Any],
) -> str:
    identity_material = {
        "repository_id": repository_id,
        "report_issue_id": report_issue_id,
        "writer_id": writer_id,
        "expected_pre_revision": expected_pre_revision,
        "expected_pre_head": expected_pre_head,
        "kind": operation["kind"],
        "payload": operation["payload"],
    }
    return f"operation:report:{hashlib.sha256(canonical_bytes(identity_material)).hexdigest()}"


def _effect_operation_fingerprint(
    *,
    repository_id: str,
    report_issue_id: str,
    writer_id: str,
    operation_id: str,
    receipt_hash: str,
    expected_pre_body_fingerprint: str,
    operation: dict[str, Any],
) -> str:
    fingerprint_material = {
        "repository_id": repository_id,
        "report_issue_id": report_issue_id,
        "writer_id": writer_id,
        "operation_id": operation_id,
        "kind": operation["kind"],
        "run_id": operation["run_id"],
        "receipt_hash": receipt_hash,
        "expected_pre_body_fingerprint": expected_pre_body_fingerprint,
        "rows": operation["rows"],
        "projection": operation["projection"],
    }
    return hashlib.sha256(canonical_bytes(fingerprint_material)).hexdigest()


def prepare_report_effect(pre_read: Any, operation: Any) -> dict[str, Any]:
    view = normalize_github_register_snapshot(pre_read)
    require(view["anchor_status"] == "exact", "effect pre-read is not at an exact history anchor")
    operation = _effect_operation(operation)
    register = view["register"]
    require(operation["rows"] != register["rows"] or operation["projection"], "effect operation has no report material")
    operation_id = _effect_operation_id(
        repository_id=view["repository_id"],
        report_issue_id=view["report_issue_id"],
        writer_id=view["writer_id"],
        expected_pre_revision=register["register_revision"],
        expected_pre_head=register["history_anchor"]["head"],
        operation=operation,
    )
    expected_pre_body_fingerprint = hashlib.sha256(view["body"].encode("utf-8")).hexdigest()
    receipt = {
        "schema": "orchestrator-history/v1",
        "sequence": register["register_revision"] + 1,
        "previous_hash": register["history_anchor"]["head"],
        "receipt_hash": "",
        "operation_id": operation_id,
        "kind": operation["kind"],
        "run_id": operation["run_id"],
        "payload": operation["payload"],
    }
    receipt["receipt_hash"] = orchestrator_receipt_hash(
        receipt, view["repository_id"], view["report_issue_id"]
    )
    _validate_orchestrator_receipt(
        receipt,
        index=receipt["sequence"],
        previous_hash=register["history_anchor"]["head"],
        repository_id=view["repository_id"],
        report_issue_id=view["report_issue_id"],
    )
    operation_fingerprint_value = _effect_operation_fingerprint(
        repository_id=view["repository_id"],
        report_issue_id=view["report_issue_id"],
        writer_id=view["writer_id"],
        operation_id=operation_id,
        receipt_hash=receipt["receipt_hash"],
        expected_pre_body_fingerprint=expected_pre_body_fingerprint,
        operation=operation,
    )
    next_register = {
        "schema": "orchestrator-register/v1",
        "repository_id": view["repository_id"],
        "report_issue_id": view["report_issue_id"],
        "writer_id": view["writer_id"],
        "register_revision": receipt["sequence"],
        "last_operation_id": operation_id,
        "last_operation_fingerprint": operation_fingerprint_value,
        "history_anchor": {
            "sequence": receipt["sequence"],
            "head": receipt["receipt_hash"],
            "latest_receipt": receipt,
        },
        "rows": operation["rows"],
    }
    _validate_orchestrator_register(
        next_register,
        repository_id=view["repository_id"],
        report_issue_id=view["report_issue_id"],
        writer_id=view["writer_id"],
    )
    body = (
        f"{CURRENT_PORTFOLIO_BEGIN}\n```json\n"
        f"{json.dumps(next_register, ensure_ascii=False, separators=(',', ':'))}\n```\n"
        f"{CURRENT_PORTFOLIO_END}\n{operation['projection']}"
    )
    validate_body(body)
    comment = (
        f"{HISTORY_RECEIPT_BEGIN}\n"
        f"{json.dumps(receipt, ensure_ascii=False, separators=(',', ':'))}\n"
        f"{HISTORY_RECEIPT_END}"
    )
    return {
        "schema": "repo-gardener-prepared-report-effect/v1",
        "repository_id": view["repository_id"],
        "report_issue_id": view["report_issue_id"],
        "writer_id": view["writer_id"],
        "operation": operation,
        "operation_id": operation_id,
        "operation_fingerprint": operation_fingerprint_value,
        "expected_pre_body_fingerprint": expected_pre_body_fingerprint,
        "expected_pre_revision": register["register_revision"],
        "expected_pre_head": register["history_anchor"]["head"],
        "expected_post_revision": receipt["sequence"],
        "expected_post_head": receipt["receipt_hash"],
        "receipt_hash": receipt["receipt_hash"],
        "body": body,
        "comment": comment,
    }


def _prepared_effect(prepared: Any) -> dict[str, Any]:
    prepared = require_object(prepared, "prepared report effect")
    require_exact_fields(prepared, EFFECT_PREPARED_FIELDS, "prepared report effect")
    require(prepared.get("schema") == "repo-gardener-prepared-report-effect/v1", "prepared report effect schema mismatch")
    operation = _effect_operation(prepared.get("operation"))
    composite_identity(prepared.get("repository_id"), prepared.get("operation_id"))
    require_identity(prepared.get("report_issue_id"), "prepared report issue_id")
    require_identity(prepared.get("writer_id"), "prepared writer_id")
    require_sha256(prepared.get("operation_fingerprint"), "prepared operation fingerprint")
    require_sha256(prepared.get("expected_pre_body_fingerprint"), "prepared pre body fingerprint")
    if prepared.get("expected_pre_head") != "GENESIS":
        require_sha256(prepared.get("expected_pre_head"), "prepared pre head")
    require_sha256(prepared.get("expected_post_head"), "prepared post head")
    require_sha256(prepared.get("receipt_hash"), "prepared receipt hash")
    require(type(prepared.get("expected_pre_revision")) is int and prepared["expected_pre_revision"] >= 0, "prepared pre revision is invalid")
    require(prepared.get("expected_post_revision") == prepared["expected_pre_revision"] + 1, "prepared revision transition is invalid")
    validate_body(prepared.get("body"))
    require(isinstance(prepared.get("comment"), str), "prepared comment must be text")
    expected_operation_id = _effect_operation_id(
        repository_id=prepared["repository_id"],
        report_issue_id=prepared["report_issue_id"],
        writer_id=prepared["writer_id"],
        expected_pre_revision=prepared["expected_pre_revision"],
        expected_pre_head=prepared["expected_pre_head"],
        operation=operation,
    )
    require(prepared["operation_id"] == expected_operation_id, "prepared operation_id mismatch")
    _, receipt = _extract_marked_json(
        prepared["comment"],
        HISTORY_RECEIPT_BEGIN,
        HISTORY_RECEIPT_END,
        "prepared receipt comment",
        fenced=False,
    )
    require(receipt.get("sequence") == prepared["expected_post_revision"], "prepared receipt sequence mismatch")
    require(receipt.get("previous_hash") == prepared["expected_pre_head"], "prepared receipt previous hash mismatch")
    require(receipt.get("operation_id") == prepared["operation_id"], "prepared receipt operation_id mismatch")
    require(receipt.get("kind") == operation["kind"] and receipt.get("run_id") == operation["run_id"], "prepared receipt metadata mismatch")
    require(receipt.get("payload") == operation["payload"], "prepared receipt payload mismatch")
    _validate_orchestrator_receipt(
        receipt,
        index=prepared["expected_post_revision"],
        previous_hash=prepared["expected_pre_head"],
        repository_id=prepared["repository_id"],
        report_issue_id=prepared["report_issue_id"],
    )
    expected_receipt_hash = orchestrator_receipt_hash(
        receipt, prepared["repository_id"], prepared["report_issue_id"]
    )
    require(receipt.get("receipt_hash") == expected_receipt_hash == prepared["receipt_hash"], "prepared receipt hash mismatch")
    require(prepared["expected_post_head"] == expected_receipt_hash, "prepared post head mismatch")
    require(
        prepared["operation_fingerprint"]
        == _effect_operation_fingerprint(
            repository_id=prepared["repository_id"],
            report_issue_id=prepared["report_issue_id"],
            writer_id=prepared["writer_id"],
            operation_id=prepared["operation_id"],
            receipt_hash=prepared["receipt_hash"],
            expected_pre_body_fingerprint=prepared["expected_pre_body_fingerprint"],
            operation=operation,
        ),
        "prepared operation fingerprint mismatch",
    )
    _, register = _extract_marked_json(
        prepared["body"],
        CURRENT_PORTFOLIO_BEGIN,
        CURRENT_PORTFOLIO_END,
        "prepared managed body",
        fenced=True,
    )
    _validate_orchestrator_register(
        register,
        repository_id=prepared["repository_id"],
        report_issue_id=prepared["report_issue_id"],
        writer_id=prepared["writer_id"],
    )
    expected_register = {
        "schema": "orchestrator-register/v1",
        "repository_id": prepared["repository_id"],
        "report_issue_id": prepared["report_issue_id"],
        "writer_id": prepared["writer_id"],
        "register_revision": prepared["expected_post_revision"],
        "last_operation_id": prepared["operation_id"],
        "last_operation_fingerprint": prepared["operation_fingerprint"],
        "history_anchor": {
            "sequence": prepared["expected_post_revision"],
            "head": prepared["expected_post_head"],
            "latest_receipt": receipt,
        },
        "rows": operation["rows"],
    }
    require(register == expected_register, "prepared body register mismatch")
    expected_body = (
        f"{CURRENT_PORTFOLIO_BEGIN}\n```json\n"
        f"{json.dumps(expected_register, ensure_ascii=False, separators=(',', ':'))}\n```\n"
        f"{CURRENT_PORTFOLIO_END}\n{operation['projection']}"
    )
    require(
        prepared["body"] == expected_body,
        "prepared body material mismatch "
        f"({hashlib.sha256(prepared['body'].encode('utf-8')).hexdigest()} != "
        f"{hashlib.sha256(expected_body.encode('utf-8')).hexdigest()})",
    )
    return prepared


def _view_matches_pre(view: dict[str, Any], prepared: dict[str, Any]) -> bool:
    return (
        view["repository_id"] == prepared["repository_id"]
        and view["report_issue_id"] == prepared["report_issue_id"]
        and view["writer_id"] == prepared["writer_id"]
        and hashlib.sha256(view["body"].encode("utf-8")).hexdigest()
        == prepared["expected_pre_body_fingerprint"]
        and view["register"]["register_revision"] == prepared["expected_pre_revision"]
        and view["register"]["history_anchor"]["head"] == prepared["expected_pre_head"]
    )


def _view_matches_post(view: dict[str, Any], prepared: dict[str, Any]) -> bool:
    if view["body"] != prepared["body"] or view["anchor_status"] != "exact":
        return False
    if view["repository_id"] != prepared["repository_id"] or view["report_issue_id"] != prepared["report_issue_id"] or view["writer_id"] != prepared["writer_id"]:
        return False
    if view["register"]["register_revision"] != prepared["expected_post_revision"] or view["register"]["history_anchor"]["head"] != prepared["expected_post_head"]:
        return False
    receipts = view["history_receipts"]
    if not receipts:
        return False
    latest = receipts[-1]
    return (
        latest["receipt"]["operation_id"] == prepared["operation_id"]
        and latest["receipt"]["receipt_hash"] == prepared["receipt_hash"]
        and f"{HISTORY_RECEIPT_BEGIN}\n{latest['raw_receipt_json']}\n{HISTORY_RECEIPT_END}" == prepared["comment"]
        and view["register"]["last_operation_fingerprint"] == prepared["operation_fingerprint"]
    )


def verify_run_records(run_id: Any, closed: Any, post_read: Any) -> dict[str, Any]:
    """Verify one exact opening/closing receipt pair after complete readback."""
    run_id = require_identity(run_id, "run record run_id")
    closed = _prepared_effect(closed)
    require(closed["operation"]["kind"] == "run-closed", "closing material must be run-closed")
    require(closed["operation"]["run_id"] == run_id, "closing material run_id mismatch")

    view = normalize_github_register_snapshot(post_read)
    require(view["anchor_status"] == "exact", "run record requires an exact post-read")
    for field in ("repository_id", "report_issue_id", "writer_id"):
        require(view[field] == closed[field], f"post-read {field} mismatch")
    matching = [
        item
        for item in view["history_receipts"]
        if item["receipt"]["run_id"] == run_id
    ]
    require(len(matching) == 2, "run_id must have exactly two managed receipts")
    opened_item, closed_item = matching
    opened_receipt = opened_item["receipt"]
    closed_receipt = closed_item["receipt"]
    require(opened_receipt["kind"] == "run-opened", "run receipt order must be run-opened")
    require(closed_receipt["kind"] == "run-closed", "run receipt order must be run-closed")
    require(
        closed_receipt["sequence"] == opened_receipt["sequence"] + 1,
        "run receipt sequences are not contiguous",
    )
    require(
        closed_receipt["previous_hash"] == opened_receipt["receipt_hash"],
        "run receipt history heads are not contiguous",
    )
    require(
        closed["expected_pre_revision"] == opened_receipt["sequence"]
        and closed["expected_pre_head"] == opened_receipt["receipt_hash"],
        "closing material does not follow the durable opening receipt",
    )
    require(closed_receipt["sequence"] == closed["expected_post_revision"], "run-closed sequence mismatch")
    require(closed_receipt["operation_id"] == closed["operation_id"], "run-closed operation_id mismatch")
    require(closed_receipt["receipt_hash"] == closed["receipt_hash"], "run-closed receipt hash mismatch")
    exact_comment = f"{HISTORY_RECEIPT_BEGIN}\n{closed_item['raw_receipt_json']}\n{HISTORY_RECEIPT_END}"
    require(exact_comment == closed["comment"], "run-closed comment material mismatch")
    require(_view_matches_post(view, closed), "closing body and receipt were not read back exactly")
    return {
        "schema": "repo-gardener-run-records-result/v1",
        "register_closed_consistently": True,
        "repository_id": view["repository_id"],
        "report_issue_id": view["report_issue_id"],
        "writer_id": view["writer_id"],
        "run_id": run_id,
        "opened_operation_id": opened_receipt["operation_id"],
        "closed_operation_id": closed["operation_id"],
        "opened_sequence": opened_receipt["sequence"],
        "closed_sequence": closed["expected_post_revision"],
    }


def verify_report_effect(prepared: Any, pre_read: Any, post_read: Any, write_attempt: Any) -> dict[str, Any]:
    prepared = _prepared_effect(prepared)
    require(write_attempt in {"none", "denied-before-write", "possible"}, "write_attempt is invalid")
    try:
        before = normalize_github_register_snapshot(pre_read)
    except ContractError:
        return {"terminal_outcome": "ambiguous", "matched_parts": None, "repair": "none", "provenance": "unverified"}
    if post_read is None:
        return {"terminal_outcome": "ambiguous", "matched_parts": None, "repair": "none", "provenance": "unverified"}
    try:
        after = normalize_github_register_snapshot(post_read)
    except ContractError:
        return {"terminal_outcome": "ambiguous", "matched_parts": None, "repair": "none", "provenance": "unverified"}
    before_is_base = _view_matches_pre(before, prepared)
    before_is_target = _view_matches_post(before, prepared)
    after_is_target = _view_matches_post(after, prepared)
    if write_attempt == "none" and before_is_target and after_is_target:
        return {"terminal_outcome": "already satisfied", "matched_parts": 2, "repair": "none", "provenance": "unverified"}
    if before_is_base and after_is_target:
        return {"terminal_outcome": "observed", "matched_parts": 2, "repair": "none", "provenance": "unverified"}
    if write_attempt == "denied-before-write" and before_is_base and before == after:
        return {"terminal_outcome": "failed", "matched_parts": 0, "repair": "none", "provenance": "unverified"}
    body_only = (
        before_is_base
        and after["body"] == prepared["body"]
        and after["anchor_status"] == "one-receipt-ahead"
        and after["history_sequence"] == prepared["expected_pre_revision"]
    )
    return {
        "terminal_outcome": "ambiguous",
        "matched_parts": 1 if body_only else None,
        "repair": "append-exact-prepared-comment" if body_only else "none",
        "provenance": "unverified",
    }


def evaluate_effect(scenario: Any) -> dict[str, Any]:
    scenario = require_object(scenario, "effect scenario")
    scenario_type = scenario.get("scenario_type")
    if scenario_type == "completion-partition":
        operation_id = require_identity(scenario.get("operation_id"), "completion partition operation_id")
        named = [
            require_identity(item, f"named_work {index}")
            for index, item in enumerate(require_list(scenario.get("named_work"), "named_work"))
        ]
        affected = [
            require_identity(item, f"affected_by_ambiguity {index}")
            for index, item in enumerate(require_list(scenario.get("affected_by_ambiguity"), "affected_work"))
        ]
        independent = [
            require_identity(item, f"independent_continued {index}")
            for index, item in enumerate(require_list(scenario.get("independent_continued"), "remaining_unblocked_work"))
        ]
        require(operation_id in named and operation_id in affected, "ambiguous operation is missing from the completion partition")
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
        require_identity(handoff.get("destination"), "handoff destination")
        require_identity(handoff.get("authorized_executor"), "handoff authorized_executor")
        require_nonempty_display(handoff.get("exact_work"), "handoff exact_work")
        return {"remaining_disposition": "delegated" if handoff.get("read_back") is True else "gated"}
    if scenario_type == "optional-scout":
        return {"dependent_work_blocked": bool(scenario.get("missing_scout")), "independent_work": "continued" if scenario.get("independent_work") is True else "gated"}
    if scenario_type == "caller-completion":
        accepted = scenario.get("terminal_capability_active") is True and scenario.get("caller_accepts") is True
        pending = [
            require_identity(item, f"pending_decision_ids {index}")
            for index, item in enumerate(require_list(scenario.get("pending_decision_ids"), "pending decisions"))
        ]
        assignment = [
            require_identity(item, f"assignment_persisted_decision_ids {index}")
            for index, item in enumerate(
                require_list(scenario.get("assignment_persisted_decision_ids"), "assignment-persisted decisions")
            )
        ]
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
    raise ContractError(f"unknown completion scenario type: {scenario_type}")


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
    candidates = [
        require_object(item, f"candidate {index}")
        for index, item in enumerate(require_list(candidates, "eligible candidates"))
    ]
    source_ids = [require_identity(item.get("source_id"), f"candidate {index} source_id") for index, item in enumerate(candidates)]
    require(len(source_ids) == len(set(source_ids)), "duplicate candidate source identity")
    eligible = sum(evaluate_gates(item.get("gate_facts"))["eligible"] for item in candidates)
    recommendations = min(limit - len(retained), eligible)
    return {"rendered_slots": limit, "retained_first": True, "available_slots": limit - len(retained) - recommendations, "recommendations": recommendations}


def render_capacity(retained: Any, candidates: Any, policy_path: Path) -> dict[str, Any]:
    return render_capacity_with_limit(retained, candidates, portfolio_limit(policy_path))


def dedupe_scout_observations(observations: Any, receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Collapse one stable source while retaining every usable contributing receipt."""
    observations = [
        require_object(item, f"dedupe observation {index}")
        for index, item in enumerate(require_list(observations, "dedupe observations"))
    ]
    require(bool(observations), "dedupe observations are empty")
    source_ids = {
        require_identity(item.get("source_id"), f"dedupe observation {index} source_id")
        for index, item in enumerate(observations)
    }
    require(len(source_ids) == 1, "dedupe observations do not share stable source identity")
    lanes: list[str] = []
    receipt_ids: list[str] = []
    for index, item in enumerate(observations):
        require_exact_fields(item, {"source_id", "lane", "receipt_id"}, f"dedupe observation {index}")
        lane = require_identity(item.get("lane"), f"dedupe observation {index} lane")
        receipt_id = require_identity(item.get("receipt_id"), f"dedupe observation {index} receipt_id")
        receipt = receipts.get(lane)
        require(
            receipt is not None
            and receipt.get("receipt_id") == receipt_id
            and receipt.get("source_id") == item.get("source_id")
            and receipt.get("outcome") in {"complete", "not applicable"},
            "dedupe cites an unknown or unusable Scout Receipt",
        )
        lanes.append(lane)
        receipt_ids.append(receipt_id)
    return {
        "candidate_count": 1,
        "source_id": next(iter(source_ids)),
        "contributing_lanes": list(dict.fromkeys(lanes)),
        "receipt_ids": list(dict.fromkeys(receipt_ids)),
    }


def reconcile_report_effect(
    prepared: Any,
    pre_read: Any,
    post_read: Any,
    write_attempt: Any,
    manifest: Any,
    receipt_collection: Any,
    work: Any,
    policy_path: Path,
) -> dict[str, Any]:
    """Derive reconciliation state from raw report material and terminal lane receipts."""
    prepared = _prepared_effect(prepared)
    _, installed_lanes = policy_contract(policy_path)
    manifest = validate_manifest(manifest, prepared["repository_id"], installed_lanes)
    require(manifest["run_id"] == prepared["operation"]["run_id"], "reconciliation run mismatch")
    receipts = validate_scout_receipts(
        receipt_collection,
        manifest,
        complete=True,
        expected_scouts=installed_lanes,
    )
    effect = verify_report_effect(prepared, pre_read, post_read, write_attempt)

    raw_work = require_list(work, "reconciliation work")
    require(len(raw_work) == len(installed_lanes), "reconciliation work must represent every installed lane exactly once")
    work_by_lane: dict[str, dict[str, Any]] = {}
    work_by_identity: dict[tuple[str, str], dict[str, Any]] = {}
    for index, raw_item in enumerate(raw_work):
        item = require_object(raw_item, f"reconciliation work {index}")
        require_exact_fields(item, RECONCILIATION_WORK_FIELDS, f"reconciliation work {index}")
        identity = composite_identity(item.get("repository_id"), item.get("operation_id"))
        require(identity["repository_id"] == prepared["repository_id"], f"reconciliation work {index} repository mismatch")
        lane = require_identity(item.get("lane"), f"reconciliation work {index} lane")
        require(lane in installed_lanes and lane not in work_by_lane, "reconciliation work must represent every installed lane exactly once")
        dependencies = [
            composite_identity(
                require_object(value, f"reconciliation work {index} dependency {dependency_index}").get("repository_id"),
                value.get("operation_id"),
            )
            for dependency_index, value in enumerate(require_list(item.get("dependencies"), f"reconciliation work {index} dependencies"))
        ]
        dependency_keys = [(value["repository_id"], value["operation_id"]) for value in dependencies]
        require(len(dependency_keys) == len(set(dependency_keys)), f"reconciliation work {index} has duplicate dependencies")
        normalized = {**identity, "lane": lane, "dependencies": dependencies}
        key = (identity["repository_id"], identity["operation_id"])
        require(key not in work_by_identity, "duplicate reconciliation work identity")
        work_by_lane[lane] = normalized
        work_by_identity[key] = normalized
    require(set(work_by_lane) == set(installed_lanes), "reconciliation work must represent every installed lane exactly once")

    report_identity = (prepared["repository_id"], prepared["operation_id"])
    require(report_identity not in work_by_identity, "lane work identity collides with prepared report identity")
    known_identities = {*work_by_identity, report_identity}
    for item in work_by_lane.values():
        for dependency in item["dependencies"]:
            require(
                (dependency["repository_id"], dependency["operation_id"]) in known_identities,
                "unknown completion dependency",
            )

    effect_positive = effect["terminal_outcome"] in {"observed", "already satisfied"}
    dispositions = {
        lane: (receipt["outcome"] if receipt["outcome"] != "incomplete" else "incomplete")
        for lane, receipt in receipts.items()
    }
    terminal_by_identity = {
        (item["repository_id"], item["operation_id"]): dispositions[lane]
        for lane, item in work_by_lane.items()
    }
    terminal_by_identity[report_identity] = effect["terminal_outcome"]

    changed = True
    while changed:
        changed = False
        for lane, item in work_by_lane.items():
            if dispositions[lane] not in {"complete", "not applicable"}:
                continue
            dependency_outcomes = [
                terminal_by_identity[(dependency["repository_id"], dependency["operation_id"])]
                for dependency in item["dependencies"]
            ]
            disposition = dispositions[lane]
            if any(value in {"ambiguous", "preserved"} for value in dependency_outcomes):
                disposition = "preserved"
            elif any(value in {"failed", "incomplete", "closed", "blocked"} for value in dependency_outcomes):
                disposition = "closed" if "failed" in dependency_outcomes else "blocked"
            if disposition != dispositions[lane]:
                dispositions[lane] = disposition
                terminal_by_identity[(item["repository_id"], item["operation_id"])] = disposition
                changed = True

    partition = {"completed": [], "blocked": [], "preserved": [], "closed": []}
    lane_dispositions = []
    for lane in installed_lanes:
        item = work_by_lane[lane]
        disposition = dispositions[lane]
        lane_dispositions.append({"lane": lane, "receipt_id": receipts[lane]["receipt_id"], "disposition": disposition})
        bucket = {
            "complete": "completed",
            "not applicable": "completed",
            "blocked": "blocked",
            "preserved": "preserved",
            "incomplete": "closed",
            "closed": "closed",
        }[disposition]
        partition[bucket].append({"repository_id": item["repository_id"], "operation_id": item["operation_id"]})

    report_bucket = {
        "observed": "completed",
        "already satisfied": "completed",
        "ambiguous": "preserved",
        "failed": "closed",
    }[effect["terminal_outcome"]]
    partition[report_bucket].append(
        {"repository_id": prepared["repository_id"], "operation_id": prepared["operation_id"]}
    )
    partition_identities = [
        (item["repository_id"], item["operation_id"])
        for bucket in partition.values()
        for item in bucket
    ]
    require(
        len(partition_identities) == len(set(partition_identities)) == len(installed_lanes) + 1,
        "completion partition is not disjoint and exhaustive",
    )

    all_lanes_complete = all(value in {"complete", "not applicable"} for value in dispositions.values())
    run_closed = prepared["operation"]["kind"] == "run-closed"
    overall_complete = effect_positive and run_closed and all_lanes_complete
    last_safe_stage = "Learn" if overall_complete else "Verify" if effect_positive else "Act"
    return {
        "schema": "repo-gardener-reconciliation-result/v2",
        "effect_outcome": effect["terminal_outcome"],
        "repair": effect["repair"],
        "report_fact_persistence": effect_positive,
        "last_safe_stage": last_safe_stage,
        "overall_dogfood_complete": overall_complete,
        "unmatched_intent": effect["terminal_outcome"] == "ambiguous",
        "blind_retry": False,
        "lane_dispositions": lane_dispositions,
        "completion_partition": partition,
        "granted_capabilities": [],
        "provenance": effect["provenance"],
    }


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
    receipt_parser = subparsers.add_parser("validate-scout-receipts")
    receipt_parser.add_argument("--receipts", type=Path, required=True)
    receipt_parser.add_argument("--manifest", type=Path, required=True)
    receipt_parser.add_argument("--allow-incomplete-coverage", action="store_true")
    body_parser = subparsers.add_parser("validate-body")
    body_parser.add_argument("--body", type=Path, required=True)
    snapshot_parser = subparsers.add_parser("normalize-github-register")
    snapshot_parser.add_argument("--input", required=True)
    for command in ("effect-v1", "run-records-v1", "completion-v1", "gates-v1"):
        input_parser = subparsers.add_parser(command)
        input_parser.add_argument("--input", required=True)
    for command in ("reconciliation-v2", "capacity-v1"):
        input_parser = subparsers.add_parser(command)
        input_parser.add_argument("--input", required=True)
        input_parser.add_argument("--policy", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "validate-scout-receipts":
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
    elif args.command == "normalize-github-register":
        result = normalize_github_register_snapshot(_load_input(args.input))
    elif args.command == "effect-v1":
        data = require_object(_load_input(args.input), "effect input")
        phase = data.get("phase")
        if phase == "prepare":
            require_exact_fields(data, {"schema", "phase", "pre_read", "operation"}, "effect input")
            require(data.get("schema") == "repo-gardener-effect-input/v2", "effect input schema mismatch")
            result = prepare_report_effect(data["pre_read"], data["operation"])
        elif phase == "verify":
            require_exact_fields(
                data,
                {"schema", "phase", "prepared", "pre_read", "post_read", "write_attempt"},
                "effect input",
            )
            require(data.get("schema") == "repo-gardener-effect-input/v2", "effect input schema mismatch")
            result = verify_report_effect(
                data["prepared"], data["pre_read"], data["post_read"], data["write_attempt"]
            )
        else:
            raise ContractError("effect input phase must be prepare or verify")
    elif args.command == "run-records-v1":
        data = _versioned_input(
            _load_input(args.input),
            "repo-gardener-run-records-input/v1",
            {"run_id", "closed", "post_read"},
        )
        result = verify_run_records(data["run_id"], data["closed"], data["post_read"])
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
    elif args.command == "reconciliation-v2":
        data = _versioned_input(
            _load_input(args.input),
            "repo-gardener-reconciliation-input/v2",
            {"prepared", "pre_read", "post_read", "write_attempt", "manifest", "receipts", "work"},
        )
        result = reconcile_report_effect(
            data["prepared"],
            data["pre_read"],
            data["post_read"],
            data["write_attempt"],
            data["manifest"],
            data["receipts"],
            data["work"],
            args.policy,
        )
    else:
        raise ContractError(f"unknown command: {args.command}")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ContractError, OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
