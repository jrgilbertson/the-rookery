#!/usr/bin/env python3
"""Exercise exact mechanical closure of two-comment run records."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
FIXTURES = Path(__file__).resolve().parent
CONTRACT_PATH = ROOT / "skills/repo-gardener/scripts/release_a_contract.py"
SNAPSHOT_RUNNER = FIXTURES.parent / "github-register/check_snapshots.py"
sys.dont_write_bytecode = True


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONTRACT = load_module(CONTRACT_PATH, "repo_gardener_release_a_contract_run_records")
SNAPSHOTS = load_module(SNAPSHOT_RUNNER, "repo_gardener_github_snapshots_for_run_records")


def invoke(command: str, payload: dict[str, Any]) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(CONTRACT_PATH), command, "--input", "-"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode:
        raise CONTRACT.ContractError(completed.stderr.strip().removeprefix("FAIL: "))
    return json.loads(completed.stdout)


def prepare(
    snapshot: dict[str, Any],
    kind: str,
    run_id: str,
    *,
    variant: str | None = None,
) -> dict[str, Any]:
    view = CONTRACT.normalize_github_register_snapshot(snapshot)
    payload = {"parent_id": "parent:synthetic:001", "status": kind}
    if variant is not None:
        payload["variant"] = variant
    return invoke(
        "effect-v1",
        {
            "schema": "repo-gardener-effect-input/v2",
            "phase": "prepare",
            "pre_read": snapshot,
            "operation": {
                "kind": kind,
                "run_id": run_id,
                "payload": payload,
                "rows": view["register"]["rows"],
                "projection": (
                    f"\n# Synthetic nightly report\n\nLatest record: `{kind}`."
                    f" Variant: `{variant or 'default'}`.\n"
                ),
            },
        },
    )


def apply_prepared(snapshot: dict[str, Any], prepared: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(snapshot)
    result["issue"]["body"] = prepared["body"]
    comments = [item for page in result["comment_pages"] for item in page]
    result["comment_pages"][-1].append(
        {
            "id": max((item["id"] for item in comments), default=0) + 1,
            "node_id": f"IC_RUN_RECORD_{prepared['expected_post_revision']:03d}",
            "user": {"node_id": SNAPSHOTS.WRITER_ID, "login": "synthetic-writer"},
            "body": prepared["comment"],
        }
    )
    result["issue"]["comments"] += 1
    return result


def add_ordinary_comment(snapshot: dict[str, Any]) -> None:
    comments = [item for page in snapshot["comment_pages"] for item in page]
    numeric_id = max(item["id"] for item in comments) + 1
    snapshot["comment_pages"][-1].append(
        {
            "id": numeric_id,
            "node_id": f"IC_RUN_RECORD_ORDINARY_{numeric_id}",
            "user": {"node_id": SNAPSHOTS.OTHER_WRITER_ID, "login": "synthetic-owner"},
            "body": "A marker-free owner note between the run records.",
        }
    )
    snapshot["issue"]["comments"] += 1


def genesis_with_identity(
    *,
    repository_id: str = SNAPSHOTS.REPOSITORY_ID,
    report_issue_id: str = SNAPSHOTS.REPORT_ID,
    writer_id: str = SNAPSHOTS.WRITER_ID,
) -> dict[str, Any]:
    snapshot = SNAPSHOTS.base_snapshot("genesis")
    register = SNAPSHOTS.make_register([], genesis=True)
    register["repository_id"] = repository_id
    register["report_issue_id"] = report_issue_id
    register["writer_id"] = writer_id
    snapshot["configured_repository_id"] = repository_id
    snapshot["configured_report_issue_id"] = report_issue_id
    snapshot["configured_writer_id"] = writer_id
    snapshot["issue"]["node_id"] = report_issue_id
    SNAPSHOTS.rewrite_body(snapshot, register)
    return snapshot


def rewrite_receipt_comment(snapshot: dict[str, Any], run_id: str, kind: str) -> None:
    for page in snapshot["comment_pages"]:
        for comment in page:
            body = comment["body"]
            if CONTRACT.HISTORY_RECEIPT_BEGIN not in body:
                continue
            raw = body.split(f"{CONTRACT.HISTORY_RECEIPT_BEGIN}\n", 1)[1].split(
                f"\n{CONTRACT.HISTORY_RECEIPT_END}", 1
            )[0]
            receipt = json.loads(raw)
            if receipt["run_id"] == run_id and receipt["kind"] == kind:
                comment["body"] = (
                    f"{CONTRACT.HISTORY_RECEIPT_BEGIN}\n"
                    f"{json.dumps(receipt, ensure_ascii=False, indent=2)}\n"
                    f"{CONTRACT.HISTORY_RECEIPT_END}"
                )
                return
    raise CONTRACT.ContractError(f"missing {kind} receipt for {run_id}")


def corrupt_receipt_hash(snapshot: dict[str, Any], run_id: str, kind: str) -> None:
    for page in snapshot["comment_pages"]:
        for comment in page:
            body = comment["body"]
            if CONTRACT.HISTORY_RECEIPT_BEGIN not in body:
                continue
            raw = body.split(f"{CONTRACT.HISTORY_RECEIPT_BEGIN}\n", 1)[1].split(
                f"\n{CONTRACT.HISTORY_RECEIPT_END}", 1
            )[0]
            receipt = json.loads(raw)
            if receipt["run_id"] == run_id and receipt["kind"] == kind:
                receipt["receipt_hash"] = "0" * 64
                comment["body"] = (
                    f"{CONTRACT.HISTORY_RECEIPT_BEGIN}\n"
                    f"{json.dumps(receipt, ensure_ascii=False, separators=(',', ':'))}\n"
                    f"{CONTRACT.HISTORY_RECEIPT_END}"
                )
                return
    raise CONTRACT.ContractError(f"missing {kind} receipt for {run_id}")


def run_input(
    run_id: str,
    closed: dict[str, Any],
    post_read: Any,
) -> dict[str, Any]:
    return {
        "schema": "repo-gardener-run-records-input/v1",
        "run_id": run_id,
        "closed": closed,
        "post_read": post_read,
    }


def expect_error(payload: dict[str, Any], phrase: str) -> None:
    try:
        invoke("run-records-v1", payload)
    except CONTRACT.ContractError as error:
        CONTRACT.require(phrase in str(error), f"expected {phrase!r}, got {error!s}")
        return
    raise CONTRACT.ContractError(f"expected rejection containing {phrase!r}")


def main() -> int:
    run_id = "run:synthetic:two-comments"
    base = SNAPSHOTS.base_snapshot("provider-page-30")
    opened = prepare(base, "run-opened", run_id)
    after_open = apply_prepared(base, opened)
    add_ordinary_comment(after_open)
    closed = prepare(after_open, "run-closed", run_id)
    exact_post = apply_prepared(after_open, closed)

    expected = {
        "schema": "repo-gardener-run-records-result/v1",
        "register_closed_consistently": True,
        "repository_id": opened["repository_id"],
        "report_issue_id": opened["report_issue_id"],
        "writer_id": opened["writer_id"],
        "run_id": run_id,
        "opened_operation_id": opened["operation_id"],
        "closed_operation_id": closed["operation_id"],
        "opened_sequence": opened["expected_post_revision"],
        "closed_sequence": closed["expected_post_revision"],
    }
    actual = invoke("run-records-v1", run_input(run_id, closed, exact_post))
    CONTRACT.require(actual == expected, f"exact closure result mismatch: {actual!r}")

    expect_error(run_input(run_id, closed, after_open), "exactly two")
    expect_error(run_input(run_id, closed, base), "exactly two")

    reversed_first = prepare(base, "run-closed", run_id)
    after_reversed_first = apply_prepared(base, reversed_first)
    reversed_second = prepare(after_reversed_first, "run-opened", run_id)
    reversed_post = apply_prepared(after_reversed_first, reversed_second)
    expect_error(run_input(run_id, reversed_first, reversed_post), "run-opened")

    other_closed = prepare(after_open, "run-closed", "run:synthetic:other")
    expect_error(
        run_input(run_id, other_closed, apply_prepared(after_open, other_closed)),
        "closing material run_id mismatch",
    )

    alternate_base = genesis_with_identity(repository_id="R_SYNTHETIC_REPOSITORY_002")
    alternate_opened = prepare(alternate_base, "run-opened", run_id)
    alternate_after_open = apply_prepared(alternate_base, alternate_opened)
    alternate_closed = prepare(alternate_after_open, "run-closed", run_id)
    alternate_post = apply_prepared(alternate_after_open, alternate_closed)
    alternate_expected = dict(expected)
    alternate_expected.update(
        {
            "repository_id": alternate_opened["repository_id"],
            "report_issue_id": alternate_opened["report_issue_id"],
            "writer_id": alternate_opened["writer_id"],
            "opened_operation_id": alternate_opened["operation_id"],
            "closed_operation_id": alternate_closed["operation_id"],
            "opened_sequence": alternate_opened["expected_post_revision"],
            "closed_sequence": alternate_closed["expected_post_revision"],
        }
    )
    alternate_actual = invoke("run-records-v1", run_input(run_id, alternate_closed, alternate_post))
    CONTRACT.require(alternate_actual == alternate_expected, "snapshot identity was not bound durably")
    expect_error(run_input(run_id, closed, alternate_post), "post-read repository_id mismatch")

    stale_closed = prepare(base, "run-closed", run_id)
    expect_error(run_input(run_id, stale_closed, exact_post), "durable opening receipt")

    different_opened = prepare(base, "run-opened", run_id, variant="different-head")
    after_different_open = apply_prepared(base, different_opened)
    different_closed = prepare(after_different_open, "run-closed", run_id)
    different_post = apply_prepared(after_different_open, different_closed)
    different_expected = dict(expected)
    different_expected.update(
        {
            "opened_operation_id": different_opened["operation_id"],
            "closed_operation_id": different_closed["operation_id"],
        }
    )
    different_actual = invoke("run-records-v1", run_input(run_id, different_closed, different_post))
    CONTRACT.require(different_actual == different_expected, "durable opening variant was not accepted")
    expect_error(run_input(run_id, closed, different_post), "durable opening receipt")

    changed_body = copy.deepcopy(after_open)
    changed_body["issue"]["body"] += "\nOwner-only projection note.\n"
    changed_body_closed = prepare(changed_body, "run-closed", run_id)
    CONTRACT.require(
        changed_body_closed["expected_pre_body_fingerprint"]
        != closed["expected_pre_body_fingerprint"],
        "recovery fixture did not change the opening-state body fingerprint",
    )
    changed_body_actual = invoke(
        "run-records-v1",
        run_input(run_id, changed_body_closed, apply_prepared(changed_body, changed_body_closed)),
    )
    changed_body_expected = dict(expected)
    changed_body_expected["closed_operation_id"] = changed_body_closed["operation_id"]
    CONTRACT.require(
        changed_body_actual == changed_body_expected,
        "recovery closure incorrectly depended on the ephemeral opening body",
    )

    tampered = copy.deepcopy(closed)
    tampered["receipt_hash"] = "0" * 64
    expect_error(run_input(run_id, tampered, exact_post), "prepared receipt hash mismatch")

    duplicate = prepare(exact_post, "run-closed", run_id)
    expect_error(run_input(run_id, closed, apply_prepared(exact_post, duplicate)), "exactly two")

    intermediate = prepare(after_open, "evidence", "run:synthetic:intermediate")
    after_intermediate = apply_prepared(after_open, intermediate)
    late_closed = prepare(after_intermediate, "run-closed", run_id)
    late_post = apply_prepared(after_intermediate, late_closed)
    expect_error(run_input(run_id, late_closed, late_post), "sequences are not contiguous")

    reformatted = copy.deepcopy(exact_post)
    rewrite_receipt_comment(reformatted, run_id, "run-opened")
    expect_error(run_input(run_id, closed, reformatted), "JSON is not canonical")

    bad_hash = copy.deepcopy(exact_post)
    corrupt_receipt_hash(bad_hash, run_id, "run-closed")
    expect_error(run_input(run_id, closed, bad_hash), "hash mismatch")

    wrong_count = copy.deepcopy(exact_post)
    wrong_count["issue"]["comments"] += 1
    expect_error(run_input(run_id, closed, wrong_count), "count does not match")

    incomplete_pages = copy.deepcopy(exact_post)
    incomplete_pages["comment_pages_complete"] = False
    expect_error(run_input(run_id, closed, incomplete_pages), "pagination is incomplete")

    interrupted = copy.deepcopy(after_open)
    interrupted["issue"]["body"] = closed["body"]
    expect_error(run_input(run_id, closed, interrupted), "exact post-read")
    expect_error(run_input(run_id, closed, None), "must be an object")

    unrelated_after = copy.deepcopy(exact_post)
    add_ordinary_comment(unrelated_after)
    actual = invoke("run-records-v1", run_input(run_id, closed, unrelated_after))
    CONTRACT.require(actual == expected, "unrelated comments changed mechanical closure")

    for forbidden in (
        "opened",
        "candidates",
        "plan",
        "score",
        "pr_readiness",
        "policy",
        "authority",
        "effect_safety",
    ):
        poisoned = run_input(run_id, closed, exact_post)
        poisoned[forbidden] = True
        expect_error(poisoned, "unexpected")

    print("PASS: exact two-comment run closure and unrelated comments")
    print("PASS: identity, lineage, sequence, operation, comment, hash, pagination, and count mutations fail closed")
    print("PASS: missing, duplicate, reversed, mismatched, tampered, stale, ambiguous, and interrupted records fail closed")
    print("PASS: checker surface excludes qualitative work, policy, authority, readiness, and effect-safety inputs")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CONTRACT.ContractError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
