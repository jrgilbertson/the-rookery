#!/usr/bin/env python3
"""Two-comment tracker helpers for repo-gardener.

The skill owns judgment. This module owns the mechanical invariants that still
have one executable source of truth: mention and image rejection, exact
opened/closed identity for one run ID, and append-only comment readback.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


IDENTITY_LIMIT = 128
RECEIPT_LIMIT = 16 * 1024
BODY_LIMIT = 48 * 1024
INPUT_LIMIT = 8 * 1024 * 1024
NOTIFICATION_CAPABLE_MENTION = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"@[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?"
    r"(?:/[A-Za-z0-9](?:[A-Za-z0-9_-]{0,98}[A-Za-z0-9_])?)?"
)
HTTP_URL = re.compile(r"https?://[^\s<>\"')\]]+", re.IGNORECASE)
HTML_IMAGE = re.compile(r"<\s*img\b", re.IGNORECASE)
RUN_RECORD_BEGIN = "<!-- orchestrator:run-record:begin -->"
RUN_RECORD_END = "<!-- orchestrator:run-record:end -->"
GITHUB_SNAPSHOT_FIELDS = {
    "schema",
    "configured_repository_id",
    "configured_report_issue_id",
    "configured_writer_id",
    "issue",
    "comment_pages_complete",
    "comment_pages",
}
RUN_RECORD_SCHEMA = "orchestrator-run-record"
PREPARED_EFFECT_SCHEMA = "repo-gardener-prepared-tracker-effect"
EFFECT_INPUT_SCHEMA = "repo-gardener-effect-input"
RUN_RECORD_FIELDS = {"schema", "kind", "run_id", "payload"}
RUN_RECORD_FIELD_ORDER = ("schema", "kind", "run_id", "payload")
RUN_RECORD_KINDS = {"run-opened", "run-closed"}
EFFECT_OPERATION_FIELDS = {"kind", "run_id", "payload", "report"}
EFFECT_PREPARED_FIELDS = {
    "schema",
    "repository_id",
    "report_issue_id",
    "writer_id",
    "operation",
    "comment",
}
RESERVED_REPORT_SEQUENCES = (RUN_RECORD_BEGIN, RUN_RECORD_END)


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


def require_payload(value: Any, limit: int, label: str) -> None:
    require(len(canonical_bytes(value)) <= limit, f"{label} exceeds {limit} canonical UTF-8 bytes")


def validate_body(body: Any) -> int:
    require(isinstance(body, str), "tracker body must be text")
    size = len(body.encode("utf-8"))
    require(size <= BODY_LIMIT, f"tracker body exceeds {BODY_LIMIT} UTF-8 bytes")
    return size


def _extract_marked_json(body: str, begin: str, end: str, label: str) -> tuple[str, dict[str, Any]]:
    require(body.count(begin) == 1 and body.count(end) == 1, f"{label} markers must appear exactly once")
    start = body.find(begin)
    finish = body.find(end)
    require(start < finish, f"{label} markers are reordered")
    terminal = body[finish + len(end) :]
    require(start == 0 and (terminal in {"", "\n"} or terminal.startswith("\n\n")), f"{label} contains surrounding text")
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
    require(record.get("schema") == RUN_RECORD_SCHEMA, f"{label} schema mismatch")
    kind = require_identity(record.get("kind"), f"{label} kind")
    require(kind in RUN_RECORD_KINDS, f"{label} kind is invalid")
    require_identity(record.get("run_id"), f"{label} run_id")
    require_object(record.get("payload"), f"{label} payload")
    require_payload(record, RECEIPT_LIMIT, label)
    return record


def normalize_github_tracker_snapshot(snapshot: Any) -> dict[str, Any]:
    """Normalize supplied GitHub bytes; do not claim freshness or provenance."""
    snapshot = require_object(snapshot, "GitHub tracker snapshot")
    require_exact_fields(snapshot, GITHUB_SNAPSHOT_FIELDS, "GitHub tracker snapshot")
    require(snapshot.get("schema") == "repo-gardener-github-tracker-snapshot", "GitHub tracker snapshot schema mismatch")
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
        "schema": "repo-gardener-github-tracker-view",
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
    require(isinstance(operation.get("report"), str) and operation["report"].strip(), "effect report must be nonempty text")
    require_payload(operation, BODY_LIMIT, "effect operation")
    _reject_reserved_report_content(operation, "effect operation")
    return operation


def _run_record_comment(record: dict[str, Any], report: str = "") -> str:
    marked = (
        f"{RUN_RECORD_BEGIN}\n"
        f"{json.dumps(record, ensure_ascii=False, separators=(',', ':'))}\n"
        f"{RUN_RECORD_END}"
    )
    return f"{marked}\n\n{report}" if report else marked


def _comment_bodies_equal(actual: str, expected: str) -> bool:
    return actual == expected or actual == f"{expected}\n"


def _prepared_material(identity_source: dict[str, Any], operation: Any) -> dict[str, Any]:
    operation = _effect_operation(operation)
    record = {
        "schema": RUN_RECORD_SCHEMA,
        "kind": operation["kind"],
        "run_id": operation["run_id"],
        "payload": operation["payload"],
    }
    _validate_run_record(record, "prepared run record")
    comment = _run_record_comment(record, operation["report"])
    require(len(comment.encode("utf-8")) <= BODY_LIMIT, f"prepared comment exceeds {BODY_LIMIT} UTF-8 bytes")
    _validate_report_rendering(comment)
    return {
        "schema": PREPARED_EFFECT_SCHEMA,
        "repository_id": identity_source["repository_id"],
        "report_issue_id": identity_source["report_issue_id"],
        "writer_id": identity_source["writer_id"],
        "operation": operation,
        "comment": comment,
    }


def prepare_report_effect(pre_read: Any, operation: Any) -> dict[str, Any]:
    view = normalize_github_tracker_snapshot(pre_read)
    prepared = _prepared_material(view, operation)
    require(
        _run_state_matches(view, prepared, present=False) or _run_state_matches(view, prepared, present=True),
        "run records conflict with the prepared event or lack its opening",
    )
    if operation["kind"] == "run-opened" and _run_state_matches(view, prepared, present=False):
        require(
            len(json.dumps(pre_read, ensure_ascii=True).encode("ascii")) <= INPUT_LIMIT // 4,
            "tracker exceeds new-run capacity; remain caller-only until the owner configures a fresh tracker",
        )
    return prepared


def _prepared_effect(prepared: Any) -> dict[str, Any]:
    prepared = require_object(prepared, "prepared tracker effect")
    require_exact_fields(prepared, EFFECT_PREPARED_FIELDS, "prepared tracker effect")
    for field in ("repository_id", "report_issue_id", "writer_id"):
        require_identity(prepared.get(field), f"prepared {field}")
    expected = _prepared_material(prepared, prepared.get("operation"))
    require(canonical_bytes(prepared) == canonical_bytes(expected), "prepared comment material mismatch")
    return prepared


def _identities_match(view: dict[str, Any], prepared: dict[str, Any]) -> bool:
    return (
        view["repository_id"] == prepared["repository_id"]
        and view["report_issue_id"] == prepared["report_issue_id"]
        and view["writer_id"] == prepared["writer_id"]
    )


def _run_state_matches(view: dict[str, Any], prepared: dict[str, Any], *, present: bool) -> bool:
    operation = prepared["operation"]
    records = [item for item in view["managed_records"] if item["record"]["run_id"] == operation["run_id"]]
    expected_kinds = [] if operation["kind"] == "run-opened" else ["run-opened"]
    if present:
        expected_kinds.append(operation["kind"])
    return (
        [item["record"]["kind"] for item in records] == expected_kinds
        and (not present or _comment_bodies_equal(records[-1]["comment_body"], prepared["comment"]))
    )


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
    return (
        bool(after_records)
        and _comment_bodies_equal(after_records[-1]["comment_body"], prepared["comment"])
        and _managed_record_lists_equal(before["managed_records"], after_records[:-1])
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
    require(opened_record["kind"] == "run-opened", "run record order must be run-opened")
    require(closed_item["record"]["kind"] == "run-closed", "run record order must be run-closed")
    require(_comment_bodies_equal(closed_item["comment_body"], closed["comment"]), "run-closed comment material mismatch")
    return {
        "schema": "repo-gardener-run-records-result",
        "repository_id": view["repository_id"],
        "report_issue_id": view["report_issue_id"],
        "writer_id": view["writer_id"],
        "run_id": run_id,
    }


def verify_report_effect(prepared: Any, pre_read: Any, post_read: Any, write_attempt: Any) -> dict[str, Any]:
    prepared = _prepared_effect(prepared)
    require(write_attempt in {"none", "denied-before-write", "possible"}, "write_attempt is invalid")
    outcome = "ambiguous"
    try:
        before = normalize_github_tracker_snapshot(pre_read)
        after = normalize_github_tracker_snapshot(post_read)
    except ContractError:
        return {"terminal_outcome": outcome, "provenance": "unverified"}
    if _identities_match(before, prepared) and _identities_match(after, prepared):
        before_is_base = _run_state_matches(before, prepared, present=False)
        before_is_target = _run_state_matches(before, prepared, present=True)
        after_is_target = _run_state_matches(after, prepared, present=True)
        if write_attempt == "none" and before_is_target and after_is_target and _managed_records_unchanged(before, after):
            outcome = "already satisfied"
        elif write_attempt == "denied-before-write" and before_is_base and pre_read == post_read:
            outcome = "failed"
        elif write_attempt == "possible" and before_is_base and after_is_target and _history_matches_prepared_transition(before, after, prepared):
            outcome = "observed"
    return {"terminal_outcome": outcome, "provenance": "unverified"}


def _load(path: Path) -> Any:
    return json.loads(read_bounded_text(path, "JSON input"))


def _load_input(source: str) -> Any:
    if source == "-":
        return json.loads(read_bounded_stdin())
    return _load(Path(source))


def _schema_input(value: Any, schema: str, fields: set[str]) -> dict[str, Any]:
    value = require_object(value, f"{schema} input")
    require_exact_fields(value, {"schema", *fields}, f"{schema} input")
    require(value.get("schema") == schema, f"input schema mismatch: expected {schema}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    snapshot_parser = subparsers.add_parser("normalize-github-tracker")
    snapshot_parser.add_argument("--input", required=True)
    for command in ("effect", "run-records"):
        input_parser = subparsers.add_parser(command)
        input_parser.add_argument("--input", required=True)
    args = parser.parse_args()
    if args.command == "normalize-github-tracker":
        result = normalize_github_tracker_snapshot(_load_input(args.input))
    elif args.command == "effect":
        data = require_object(_load_input(args.input), "effect input")
        phase = data.get("phase")
        if phase == "prepare":
            require_exact_fields(data, {"schema", "phase", "pre_read", "operation"}, "effect input")
            require(data.get("schema") == EFFECT_INPUT_SCHEMA, "effect input schema mismatch")
            result = prepare_report_effect(data["pre_read"], data["operation"])
        elif phase == "verify":
            require_exact_fields(
                data,
                {"schema", "phase", "prepared", "pre_read", "post_read", "write_attempt"},
                "effect input",
            )
            require(data.get("schema") == EFFECT_INPUT_SCHEMA, "effect input schema mismatch")
            result = verify_report_effect(
                data["prepared"], data["pre_read"], data["post_read"], data["write_attempt"]
            )
        else:
            raise ContractError("effect input phase must be prepare or verify")
    elif args.command == "run-records":
        data = _schema_input(
            _load_input(args.input),
            "repo-gardener-run-records-input",
            {"run_id", "closed", "post_read"},
        )
        result = verify_run_records(data["run_id"], data["closed"], data["post_read"])
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
