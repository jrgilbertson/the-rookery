#!/usr/bin/env python3
"""Two-comment tracker helpers for repo-gardener.

The skill owns judgment. This module owns the mechanical invariants that still
have one executable source of truth: mention and image rejection, exact
opened/closed identity for one run ID, and the public nine-lane inventory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


IDENTITY_LIMIT = 128
RECEIPT_LIMIT = 16 * 1024
BODY_LIMIT = 48 * 1024
INPUT_LIMIT = 8 * 1024 * 1024
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
TRIAGE_LANE = "issue-backlog-and-customer-feedback-triage"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
NOTIFICATION_CAPABLE_MENTION = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"@[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?"
    r"(?:/[A-Za-z0-9](?:[A-Za-z0-9_-]{0,98}[A-Za-z0-9_])?)?"
)
HTTP_URL = re.compile(r"https?://[^\s<>\"')\]]+", re.IGNORECASE)
HTML_IMAGE = re.compile(r"<\s*img\b", re.IGNORECASE)
RUN_RECORD_BEGIN = "<!-- orchestrator:run-record:v1:begin -->"
RUN_RECORD_END = "<!-- orchestrator:run-record:v1:end -->"
GITHUB_SNAPSHOT_FIELDS = {
    "schema",
    "configured_repository_id",
    "configured_report_issue_id",
    "configured_writer_id",
    "issue",
    "comment_pages_complete",
    "comment_pages",
}
RUN_RECORD_FIELDS = {"schema", "kind", "run_id", "operation_id", "payload"}
RUN_RECORD_FIELD_ORDER = ("schema", "kind", "run_id", "operation_id", "payload")
RUN_RECORD_KINDS = {"run-opened", "run-closed"}
EFFECT_OPERATION_FIELDS = {"kind", "run_id", "payload", "projection"}
EFFECT_PREPARED_FIELDS = {
    "schema",
    "repository_id",
    "report_issue_id",
    "writer_id",
    "operation",
    "operation_id",
    "expected_pre_body_fingerprint",
    "body",
    "comment",
}
RESERVED_REPORT_SEQUENCES = (RUN_RECORD_BEGIN, RUN_RECORD_END)
LANE_HEADER = re.compile(
    r"  ([a-z0-9][a-z0-9-]*):\s*(?:\{\s*(?:mutation\s*:\s*(true|false)\s*,?\s*)?\}\s*)?(?:#.*)?$"
)
LANE_MUTATION = re.compile(r"    mutation:\s*(true|false)\s*(?:#.*)?$")


class ContractError(Exception):
    """A machine contract is malformed or cannot support the claimed result."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def read_bounded_text(path: Path, label: str, limit: int = INPUT_LIMIT) -> str:
    with path.open("rb") as source:
        raw = source.read(limit + 1)
    require(len(raw) <= limit, f"{label} exceeds {limit} UTF-8 bytes")
    return raw.decode("utf-8")


def read_bounded_stdin(limit: int = INPUT_LIMIT) -> str:
    raw = sys.stdin.buffer.read(limit + 1)
    require(len(raw) <= limit, f"standard input exceeds {limit} UTF-8 bytes")
    return raw.decode("utf-8")


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


def require_sha256(value: Any, label: str) -> str:
    require(isinstance(value, str) and SHA256.fullmatch(value) is not None, f"{label} must be a lowercase SHA-256 digest")
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


def installed_lanes_from_text(text: str) -> list[str]:
    require(isinstance(text, str), "policy must be text")
    lanes = policy_section(text, "lanes")
    for line in lanes:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        require(
            LANE_HEADER.fullmatch(line) is not None or LANE_MUTATION.fullmatch(line) is not None,
            "policy lanes contain an unparsed or inline entry",
        )
    lane_starts: list[tuple[int, str]] = []
    inline_mutations: dict[str, str] = {}
    for index, line in enumerate(lanes):
        match = LANE_HEADER.fullmatch(line)
        if match is None:
            continue
        lane = match.group(1)
        lane_starts.append((index, lane))
        if match.group(2) is not None:
            inline_mutations[lane] = match.group(2)
    result = [lane for _, lane in lane_starts]
    require(bool(result), "policy installed lane inventory is empty")
    require(len(result) == len(set(result)), "policy installed lane inventory contains duplicates")
    require(tuple(result) == RELEASE_A_LANES, "policy installed lane inventory differs from the public nine-lane contract")
    for position, (start, lane) in enumerate(lane_starts):
        end = lane_starts[position + 1][0] if position + 1 < len(lane_starts) else len(lanes)
        mutations = []
        if lane in inline_mutations:
            mutations.append(inline_mutations[lane])
        mutations.extend(
            match.group(1)
            for line in lanes[start + 1 : end]
            if (match := LANE_MUTATION.fullmatch(line))
        )
        if lane == TRIAGE_LANE:
            require(mutations == [], f"policy lane {lane} must not declare mutation")
        else:
            require(
                mutations in (["true"], ["false"]),
                f"policy lane {lane} mutation must be exactly true or false",
            )
    return result


def _extract_marked_json(body: str, begin: str, end: str, label: str) -> tuple[str, dict[str, Any]]:
    require(body.count(begin) == 1 and body.count(end) == 1, f"{label} markers must appear exactly once")
    start = body.find(begin)
    finish = body.find(end)
    require(start < finish, f"{label} markers are reordered")
    terminal = body[finish + len(end) :]
    require(start == 0 and terminal in {"", "\n"}, f"{label} contains surrounding text")
    raw = body[start + len(begin) : finish]
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


def _validate_run_record(record: dict[str, Any], label: str) -> dict[str, Any]:
    require_exact_fields(record, RUN_RECORD_FIELDS, label)
    require(tuple(record) == RUN_RECORD_FIELD_ORDER, f"{label} field order mismatch")
    require(record.get("schema") == "orchestrator-run-record/v1", f"{label} schema mismatch")
    kind = require_identity(record.get("kind"), f"{label} kind")
    require(kind in RUN_RECORD_KINDS, f"{label} kind is invalid")
    require_identity(record.get("run_id"), f"{label} run_id")
    require_identity(record.get("operation_id"), f"{label} operation_id")
    require_object(record.get("payload"), f"{label} payload")
    require_payload(record, RECEIPT_LIMIT, label)
    return record


def normalize_github_tracker_snapshot(snapshot: Any) -> dict[str, Any]:
    """Normalize supplied GitHub bytes; do not claim freshness or provenance."""
    snapshot = require_object(snapshot, "GitHub tracker snapshot")
    require_exact_fields(snapshot, GITHUB_SNAPSHOT_FIELDS, "GitHub tracker snapshot")
    require(snapshot.get("schema") == "repo-gardener-github-tracker-snapshot/v1", "GitHub tracker snapshot schema mismatch")
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

    require(snapshot.get("comment_pages_complete") is True, "comment pagination is incomplete")
    pages = require_list(snapshot.get("comment_pages"), "comment pages")
    require(bool(pages), "comment page sequence is incomplete")
    page_size = len(require_list(pages[0], "comment page 1"))
    require(page_size <= 100, "comment page 1 exceeds the configured page size")
    if len(pages) > 1:
        require(page_size > 0, "comment page sequence is incomplete")
    managed_records: list[dict[str, Any]] = []
    ordinary_comment_ids: list[str] = []
    seen_comment_ids: set[str] = set()
    seen_numeric_comment_ids: set[int] = set()
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
            comment_body = comment.get("body")
            require(isinstance(comment_body, str), "provider comment body must be text")
            require(len(comment_body.encode("utf-8")) <= BODY_LIMIT, f"provider comment body exceeds {BODY_LIMIT} UTF-8 bytes")
            has_reserved_marker = RUN_RECORD_BEGIN in comment_body or RUN_RECORD_END in comment_body
            if not has_reserved_marker:
                ordinary_comment_ids.append(comment_id)
                continue
            user = require_object(comment.get("user"), "provider comment user")
            author_id = require_identity(user.get("node_id"), "provider comment author node_id")
            require(author_id == writer_id, "reserved run-record marker from non-writer comment")
            raw_record_json, record = _extract_marked_json(
                comment_body,
                RUN_RECORD_BEGIN,
                RUN_RECORD_END,
                f"writer comment {comment_id}",
            )
            _validate_run_record(record, f"writer comment {comment_id}")
            managed_records.append(
                {
                    "provider_comment_id": comment_id,
                    "raw_record_json": raw_record_json,
                    "record": record,
                    "comment_body": comment_body,
                }
            )

    require(
        len(seen_comment_ids) == provider_comment_count,
        "comment pagination count does not match provider total",
    )
    return {
        "schema": "repo-gardener-github-tracker-view/v1",
        "repository_id": repository_id,
        "report_issue_id": report_issue_id,
        "writer_id": writer_id,
        "body": body,
        "managed_records": managed_records,
        "ordinary_comment_ids": ordinary_comment_ids,
        "comment_pages_complete": True,
        "provenance": "unverified",
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


def _validate_report_rendering(rendering: str) -> None:
    """Reject tracker rendering that can notify accounts or load image content."""
    require(
        NOTIFICATION_CAPABLE_MENTION.search(HTTP_URL.sub("", rendering)) is None,
        "effect report contains a notification-capable mention",
    )
    require(
        "![" not in rendering and HTML_IMAGE.search(rendering) is None,
        "effect report contains image embedding syntax",
    )


def _effect_operation(operation: Any) -> dict[str, Any]:
    operation = require_object(operation, "effect operation")
    require_exact_fields(operation, EFFECT_OPERATION_FIELDS, "effect operation")
    kind = require_identity(operation.get("kind"), "effect kind")
    require(kind in RUN_RECORD_KINDS, "effect kind is invalid")
    require_identity(operation.get("run_id"), "effect run_id")
    require_object(operation.get("payload"), "effect payload")
    require(isinstance(operation.get("projection"), str), "effect projection must be text")
    require_payload(operation, BODY_LIMIT, "effect operation")
    _reject_reserved_report_content(operation, "effect operation")
    return {
        "kind": operation["kind"],
        "run_id": operation["run_id"],
        "payload": operation["payload"],
        "projection": operation["projection"],
    }


def _effect_operation_id(
    *,
    repository_id: str,
    report_issue_id: str,
    writer_id: str,
    expected_pre_body_fingerprint: str,
    operation: dict[str, Any],
) -> str:
    identity_material = {
        "repository_id": repository_id,
        "report_issue_id": report_issue_id,
        "writer_id": writer_id,
        "expected_pre_body_fingerprint": expected_pre_body_fingerprint,
        "kind": operation["kind"],
        "payload": operation["payload"],
    }
    return f"operation:report:{hashlib.sha256(canonical_bytes(identity_material)).hexdigest()}"


def _run_record_comment(record: dict[str, Any]) -> str:
    return (
        f"{RUN_RECORD_BEGIN}\n"
        f"{json.dumps(record, ensure_ascii=False, separators=(',', ':'))}\n"
        f"{RUN_RECORD_END}"
    )


def _comment_bodies_equal(actual: str, expected: str) -> bool:
    return actual == expected or actual == f"{expected}\n"


def prepare_report_effect(pre_read: Any, operation: Any) -> dict[str, Any]:
    view = normalize_github_tracker_snapshot(pre_read)
    operation = _effect_operation(operation)
    expected_pre_body_fingerprint = hashlib.sha256(view["body"].encode("utf-8")).hexdigest()
    operation_id = _effect_operation_id(
        repository_id=view["repository_id"],
        report_issue_id=view["report_issue_id"],
        writer_id=view["writer_id"],
        expected_pre_body_fingerprint=expected_pre_body_fingerprint,
        operation=operation,
    )
    record = {
        "schema": "orchestrator-run-record/v1",
        "kind": operation["kind"],
        "run_id": operation["run_id"],
        "operation_id": operation_id,
        "payload": operation["payload"],
    }
    _validate_run_record(record, "prepared run record")
    body = operation["projection"]
    validate_body(body)
    comment = _run_record_comment(record)
    _validate_report_rendering(body)
    _validate_report_rendering(comment)
    return {
        "schema": "repo-gardener-prepared-tracker-effect/v1",
        "repository_id": view["repository_id"],
        "report_issue_id": view["report_issue_id"],
        "writer_id": view["writer_id"],
        "operation": operation,
        "operation_id": operation_id,
        "expected_pre_body_fingerprint": expected_pre_body_fingerprint,
        "body": body,
        "comment": comment,
    }


def _prepared_effect(prepared: Any) -> dict[str, Any]:
    prepared = require_object(prepared, "prepared tracker effect")
    require_exact_fields(prepared, EFFECT_PREPARED_FIELDS, "prepared tracker effect")
    require(prepared.get("schema") == "repo-gardener-prepared-tracker-effect/v1", "prepared tracker effect schema mismatch")
    operation = _effect_operation(prepared.get("operation"))
    require_identity(prepared.get("repository_id"), "prepared repository_id")
    require_identity(prepared.get("report_issue_id"), "prepared report issue_id")
    require_identity(prepared.get("writer_id"), "prepared writer_id")
    require_identity(prepared.get("operation_id"), "prepared operation_id")
    require_sha256(prepared.get("expected_pre_body_fingerprint"), "prepared pre body fingerprint")
    validate_body(prepared.get("body"))
    require(isinstance(prepared.get("comment"), str), "prepared comment must be text")
    require(prepared["body"] == operation["projection"], "prepared body material mismatch")
    _validate_report_rendering(prepared["body"])
    _validate_report_rendering(prepared["comment"])
    expected_operation_id = _effect_operation_id(
        repository_id=prepared["repository_id"],
        report_issue_id=prepared["report_issue_id"],
        writer_id=prepared["writer_id"],
        expected_pre_body_fingerprint=prepared["expected_pre_body_fingerprint"],
        operation=operation,
    )
    require(prepared["operation_id"] == expected_operation_id, "prepared operation_id mismatch")
    _, record = _extract_marked_json(
        prepared["comment"],
        RUN_RECORD_BEGIN,
        RUN_RECORD_END,
        "prepared run-record comment",
    )
    _validate_run_record(record, "prepared run record")
    require(record.get("operation_id") == prepared["operation_id"], "prepared record operation_id mismatch")
    require(record.get("kind") == operation["kind"] and record.get("run_id") == operation["run_id"], "prepared record metadata mismatch")
    require(record.get("payload") == operation["payload"], "prepared record payload mismatch")
    require(prepared["comment"] == _run_record_comment(record), "prepared comment material mismatch")
    return prepared


def _identities_match(view: dict[str, Any], prepared: dict[str, Any]) -> bool:
    return (
        view["repository_id"] == prepared["repository_id"]
        and view["report_issue_id"] == prepared["report_issue_id"]
        and view["writer_id"] == prepared["writer_id"]
    )


def _view_matches_pre(view: dict[str, Any], prepared: dict[str, Any]) -> bool:
    return (
        _identities_match(view, prepared)
        and hashlib.sha256(view["body"].encode("utf-8")).hexdigest()
        == prepared["expected_pre_body_fingerprint"]
        and not _prepared_comment_present(view, prepared)
    )


def _prepared_comment_count(view: dict[str, Any], prepared: dict[str, Any]) -> int:
    return sum(
        1
        for item in view["managed_records"]
        if _comment_bodies_equal(item["comment_body"], prepared["comment"])
    )


def _prepared_comment_present(view: dict[str, Any], prepared: dict[str, Any]) -> bool:
    return _prepared_comment_count(view, prepared) > 0


def _managed_record_lists_equal(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> bool:
    if len(left) != len(right):
        return False
    for first, second in zip(left, right):
        if first["provider_comment_id"] != second["provider_comment_id"]:
            return False
        if not _comment_bodies_equal(first["comment_body"], second["comment_body"]):
            return False
    return True


def _managed_records_unchanged(before: dict[str, Any], after: dict[str, Any]) -> bool:
    return _managed_record_lists_equal(before["managed_records"], after["managed_records"])


def _history_matches_prepared_transition(
    before: dict[str, Any],
    after: dict[str, Any],
    prepared: dict[str, Any],
) -> bool:
    after_records = after["managed_records"]
    before_records = before["managed_records"]
    if len(after_records) != len(before_records) + 1:
        return False
    remaining = [
        item
        for item in after_records
        if not _comment_bodies_equal(item["comment_body"], prepared["comment"])
    ]
    return _managed_record_lists_equal(before_records, remaining)


def _view_matches_post(view: dict[str, Any], prepared: dict[str, Any]) -> bool:
    return (
        _identities_match(view, prepared)
        and view["body"] == prepared["body"]
        and _prepared_comment_count(view, prepared) == 1
    )


def verify_run_records(run_id: Any, closed: Any, post_read: Any) -> dict[str, Any]:
    """Verify one exact opening/closing comment pair after complete readback."""
    run_id = require_identity(run_id, "run record run_id")
    closed = _prepared_effect(closed)
    require(closed["operation"]["kind"] == "run-closed", "closing material must be run-closed")
    require(closed["operation"]["run_id"] == run_id, "closing material run_id mismatch")

    view = normalize_github_tracker_snapshot(post_read)
    for field in ("repository_id", "report_issue_id", "writer_id"):
        require(view[field] == closed[field], f"post-read {field} mismatch")
    matching = [item for item in view["managed_records"] if item["record"]["run_id"] == run_id]
    require(len(matching) == 2, "run_id must have exactly two managed records")
    opened_item, closed_item = matching
    opened_record = opened_item["record"]
    closed_record = closed_item["record"]
    require(opened_record["kind"] == "run-opened", "run record order must be run-opened")
    require(closed_record["kind"] == "run-closed", "run record order must be run-closed")
    require(closed_record["operation_id"] == closed["operation_id"], "run-closed operation_id mismatch")
    require(_comment_bodies_equal(closed_item["comment_body"], closed["comment"]), "run-closed comment material mismatch")
    require(_view_matches_post(view, closed), "closing body and comment were not read back exactly")
    return {
        "schema": "repo-gardener-run-records-result/v1",
        "repository_id": view["repository_id"],
        "report_issue_id": view["report_issue_id"],
        "writer_id": view["writer_id"],
        "run_id": run_id,
        "opened_operation_id": opened_record["operation_id"],
        "closed_operation_id": closed["operation_id"],
    }


def verify_report_effect(prepared: Any, pre_read: Any, post_read: Any, write_attempt: Any) -> dict[str, Any]:
    prepared = _prepared_effect(prepared)
    require(write_attempt in {"none", "denied-before-write", "possible"}, "write_attempt is invalid")
    try:
        before = normalize_github_tracker_snapshot(pre_read)
    except ContractError:
        return {"terminal_outcome": "ambiguous", "matched_parts": None, "repair": "none", "provenance": "unverified"}
    if post_read is None:
        return {"terminal_outcome": "ambiguous", "matched_parts": None, "repair": "none", "provenance": "unverified"}
    try:
        after = normalize_github_tracker_snapshot(post_read)
    except ContractError:
        return {"terminal_outcome": "ambiguous", "matched_parts": None, "repair": "none", "provenance": "unverified"}
    before_is_base = _view_matches_pre(before, prepared)
    before_is_target = _view_matches_post(before, prepared)
    after_is_target = _view_matches_post(after, prepared)
    if write_attempt == "none" and before_is_target and after_is_target:
        return {"terminal_outcome": "already satisfied", "matched_parts": 2, "repair": "none", "provenance": "unverified"}
    if write_attempt == "denied-before-write":
        if before_is_base and pre_read == post_read:
            return {"terminal_outcome": "failed", "matched_parts": 0, "repair": "none", "provenance": "unverified"}
        return {"terminal_outcome": "ambiguous", "matched_parts": None, "repair": "none", "provenance": "unverified"}
    if (
        write_attempt == "possible"
        and before_is_base
        and after_is_target
        and _history_matches_prepared_transition(before, after, prepared)
    ):
        return {"terminal_outcome": "observed", "matched_parts": 2, "repair": "none", "provenance": "unverified"}
    body_only = (
        write_attempt == "possible"
        and before_is_base
        and _identities_match(after, prepared)
        and after["body"] == prepared["body"]
        and not _prepared_comment_present(after, prepared)
        and _managed_records_unchanged(before, after)
    )
    return {
        "terminal_outcome": "ambiguous",
        "matched_parts": 1 if body_only else None,
        "repair": "append-exact-prepared-comment" if body_only else "none",
        "provenance": "unverified",
    }


def _load(path: Path) -> Any:
    return json.loads(read_bounded_text(path, "JSON input"))


def _load_input(source: str) -> Any:
    if source == "-":
        return json.loads(read_bounded_stdin())
    return _load(Path(source))


def _versioned_input(value: Any, schema: str, fields: set[str]) -> dict[str, Any]:
    value = require_object(value, f"{schema} input")
    require_exact_fields(value, {"schema", *fields}, f"{schema} input")
    require(value.get("schema") == schema, f"input schema mismatch: expected {schema}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    body_parser = subparsers.add_parser("validate-body")
    body_parser.add_argument("--body", type=Path, required=True)
    snapshot_parser = subparsers.add_parser("normalize-github-tracker")
    snapshot_parser.add_argument("--input", required=True)
    for command in ("effect-v1", "run-records-v1"):
        input_parser = subparsers.add_parser(command)
        input_parser.add_argument("--input", required=True)
    lanes_parser = subparsers.add_parser("lanes-v1")
    lanes_parser.add_argument("--policy", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "validate-body":
        body = read_bounded_text(args.body, "managed body", BODY_LIMIT)
        result = {"body_bytes": validate_body(body)}
    elif args.command == "normalize-github-tracker":
        result = normalize_github_tracker_snapshot(_load_input(args.input))
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
    elif args.command == "lanes-v1":
        result = {
            "schema": "repo-gardener-lanes-result/v1",
            "lanes": installed_lanes_from_text(read_bounded_text(args.policy, "policy")),
        }
    else:
        raise ContractError(f"unknown command: {args.command}")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        ContractError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
        RecursionError,
    ) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
