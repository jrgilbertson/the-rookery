#!/usr/bin/env python3
"""Exercise exact two-comment identity without a hash-register."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
FIXTURES = Path(__file__).resolve().parent
CONTRACT_PATH = ROOT / "skills/repo-gardener/scripts/release_a_contract.py"
POLICY_PATH = ROOT / "skills/repo-gardener/assets/policy-template.yaml"
SNAPSHOT_HELPER = FIXTURES.parent / "tracker_snapshots.py"
sys.dont_write_bytecode = True


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONTRACT = load_module(CONTRACT_PATH, "repo_gardener_release_a_contract_run_records")
SNAPSHOTS = load_module(SNAPSHOT_HELPER, "repo_gardener_tracker_snapshots_for_run_records")


def invoke(command: str, payload: dict[str, Any], extra: list[str] | None = None) -> dict[str, Any]:
    arguments = [sys.executable, str(CONTRACT_PATH), command]
    if extra:
        arguments.extend(extra)
    else:
        arguments.extend(["--input", "-"])
    completed = subprocess.run(
        arguments,
        input="" if extra else json.dumps(payload),
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
                "projection": (
                    f"\n# Synthetic morning report\n\nLatest record: `{kind}`."
                    f" Variant: `{variant or 'default'}`.\n"
                ),
            },
        },
    )


def apply_prepared(snapshot: dict[str, Any], prepared: dict[str, Any]) -> dict[str, Any]:
    return SNAPSHOTS.apply_prepared(snapshot, prepared)


def extract_record(comment: str) -> dict[str, Any]:
    raw = comment.split(f"{CONTRACT.RUN_RECORD_BEGIN}\n", 1)[1].split(
        f"\n{CONTRACT.RUN_RECORD_END}", 1
    )[0]
    return json.loads(raw)


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
    base = SNAPSHOTS.empty_tracker()
    opened = prepare(base, "run-opened", run_id)
    after_open = SNAPSHOTS.add_ordinary_comment(apply_prepared(base, opened))
    closed = prepare(after_open, "run-closed", run_id)
    exact_post = apply_prepared(after_open, closed)

    for prepared in (opened, closed):
        record = extract_record(prepared["comment"])
        CONTRACT.require("previous_hash" not in record, "production comment still required previous_hash")
        CONTRACT.require("receipt_hash" not in record, "production comment still required receipt_hash")
        CONTRACT.require(
            set(record) == set(CONTRACT.RUN_RECORD_FIELDS),
            f"production comment fields drifted: {sorted(record)}",
        )
        CONTRACT.require(
            "orchestrator:current-portfolio:v1" not in prepared["body"],
            "production body still embedded Current Portfolio JSON",
        )

    expected = {
        "schema": "repo-gardener-run-records-result/v1",
        "repository_id": opened["repository_id"],
        "report_issue_id": opened["report_issue_id"],
        "writer_id": opened["writer_id"],
        "run_id": run_id,
        "opened_operation_id": opened["operation_id"],
        "closed_operation_id": closed["operation_id"],
    }
    actual = invoke("run-records-v1", run_input(run_id, closed, exact_post))
    CONTRACT.require(actual == expected, f"exact closure result mismatch: {actual!r}")
    CONTRACT.require("register_closed_consistently" not in actual, "closure still returned a register-quality claim")

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

    alternate_base = SNAPSHOTS.empty_tracker(repository_id="R_SYNTHETIC_REPOSITORY_002")
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
        }
    )
    alternate_actual = invoke("run-records-v1", run_input(run_id, alternate_closed, alternate_post))
    CONTRACT.require(alternate_actual == alternate_expected, "snapshot identity was not bound durably")
    expect_error(run_input(run_id, closed, alternate_post), "post-read repository_id mismatch")

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
    expect_error(run_input(run_id, closed, different_post), "run-closed operation_id mismatch")

    stale_closed = prepare(base, "run-closed", run_id)
    expect_error(run_input(run_id, stale_closed, exact_post), "run-closed operation_id mismatch")

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

    duplicate = prepare(exact_post, "run-closed", run_id)
    expect_error(run_input(run_id, closed, apply_prepared(exact_post, duplicate)), "exactly two")

    reformatted = copy.deepcopy(exact_post)
    for page in reformatted["comment_pages"]:
        for comment in page:
            if CONTRACT.RUN_RECORD_BEGIN not in comment["body"]:
                continue
            record = extract_record(comment["body"])
            if record["run_id"] == run_id and record["kind"] == "run-opened":
                comment["body"] = (
                    f"{CONTRACT.RUN_RECORD_BEGIN}\n"
                    f"{json.dumps(record, ensure_ascii=False, indent=2)}\n"
                    f"{CONTRACT.RUN_RECORD_END}"
                )
    expect_error(run_input(run_id, closed, reformatted), "JSON is not canonical")

    hashed = copy.deepcopy(exact_post)
    for page in hashed["comment_pages"]:
        for comment in page:
            if CONTRACT.RUN_RECORD_BEGIN not in comment["body"]:
                continue
            record = extract_record(comment["body"])
            if record["run_id"] == run_id and record["kind"] == "run-closed":
                record["receipt_hash"] = "0" * 64
                comment["body"] = (
                    f"{CONTRACT.RUN_RECORD_BEGIN}\n"
                    f"{json.dumps(record, ensure_ascii=False, separators=(',', ':'))}\n"
                    f"{CONTRACT.RUN_RECORD_END}"
                )
    expect_error(run_input(run_id, closed, hashed), "unexpected receipt_hash")

    wrong_count = copy.deepcopy(exact_post)
    wrong_count["issue"]["comments"] += 1
    expect_error(run_input(run_id, closed, wrong_count), "count does not match")

    incomplete_pages = copy.deepcopy(exact_post)
    incomplete_pages["comment_pages_complete"] = False
    expect_error(run_input(run_id, closed, incomplete_pages), "pagination is incomplete")

    interrupted = copy.deepcopy(after_open)
    interrupted["issue"]["body"] = closed["body"]
    expect_error(run_input(run_id, closed, interrupted), "exactly two")
    expect_error(run_input(run_id, closed, None), "must be an object")

    unrelated_after = SNAPSHOTS.add_ordinary_comment(exact_post)
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

    lanes = invoke("lanes-v1", {}, extra=["--policy", str(POLICY_PATH)])
    CONTRACT.require(
        lanes == {"schema": "repo-gardener-lanes-result/v1", "lanes": list(CONTRACT.RELEASE_A_LANES)},
        f"nine-lane inventory drifted: {lanes!r}",
    )
    flow_policy = POLICY_PATH.read_text(encoding="utf-8").replace(
        "  dependency-and-vulnerability:\n    mutation: false\n",
        "  dependency-and-vulnerability: {mutation: false}\n",
    )
    with tempfile.TemporaryDirectory() as directory:
        flow_path = Path(directory) / "policy.yaml"
        flow_path.write_text(flow_policy, encoding="utf-8")
        flow_lanes = invoke("lanes-v1", {}, extra=["--policy", str(flow_path)])
        CONTRACT.require(
            flow_lanes == {"schema": "repo-gardener-lanes-result/v1", "lanes": list(CONTRACT.RELEASE_A_LANES)},
            f"flow-style lanes inventory drifted: {flow_lanes!r}",
        )
        four_space_lines = []
        in_lanes = False
        for line in POLICY_PATH.read_text(encoding="utf-8").splitlines():
            if line.startswith("lanes:"):
                in_lanes = True
                four_space_lines.append(line)
                continue
            if in_lanes and line and not line[0].isspace():
                in_lanes = False
            four_space_lines.append("  " + line if in_lanes and line else line)
        four_space_path = Path(directory) / "four-space-policy.yaml"
        four_space_path.write_text("\n".join(four_space_lines) + "\n", encoding="utf-8")
        four_space_lanes = invoke("lanes-v1", {}, extra=["--policy", str(four_space_path)])
        CONTRACT.require(
            four_space_lanes == {"schema": "repo-gardener-lanes-result/v1", "lanes": list(CONTRACT.RELEASE_A_LANES)},
            f"four-space lanes inventory drifted: {four_space_lanes!r}",
        )

    removed = subprocess.run(
        [sys.executable, str(CONTRACT_PATH), "normalize-github-register", "--input", "-"],
        input="{}",
        capture_output=True,
        text=True,
        check=False,
    )
    CONTRACT.require(removed.returncode != 0 and "invalid choice" in removed.stderr, "normalize-github-register remains public")
    for obsolete in ("completion-v1", "gates-v1", "capacity-v1", "reconciliation-v2"):
        completed = subprocess.run(
            [sys.executable, str(CONTRACT_PATH), obsolete, "--input", "-"],
            input="{}",
            capture_output=True,
            text=True,
            check=False,
        )
        CONTRACT.require(completed.returncode != 0 and "invalid choice" in completed.stderr, f"{obsolete} remains public")

    normalized = invoke("normalize-github-tracker", exact_post)
    CONTRACT.require(normalized["provenance"] == "unverified", "tracker snapshot invented provenance")
    CONTRACT.require(len(normalized["managed_records"]) == 2, "tracker snapshot lost the two run records")
    CONTRACT.require(len(normalized["ordinary_comment_ids"]) == 1, "ordinary comments were not preserved")

    authorless = SNAPSHOTS.add_ordinary_comment(exact_post)
    authorless["comment_pages"][-1][-1]["user"] = None
    authorless_normalized = invoke("normalize-github-tracker", authorless)
    CONTRACT.require(
        authorless["comment_pages"][-1][-1]["node_id"] in authorless_normalized["ordinary_comment_ids"],
        "authorless ordinary comment was not preserved",
    )
    managed_authorless = copy.deepcopy(exact_post)
    managed_authorless["comment_pages"][-1][-1]["user"] = None
    try:
        invoke("normalize-github-tracker", managed_authorless)
    except CONTRACT.ContractError as error:
        CONTRACT.require(
            "provider comment user must be an object" in str(error),
            f"authorless managed comment diagnostic differs: {error!s}",
        )
    else:
        raise CONTRACT.ContractError("authorless managed comment was accepted")

    paged = SNAPSHOTS.split_comment_pages(exact_post, [2, 1])
    paged_normalized = invoke("normalize-github-tracker", paged)
    CONTRACT.require(
        len(paged_normalized["managed_records"]) == 2,
        "uniform first page plus short final page lost managed records",
    )
    CONTRACT.require(
        len(paged_normalized["ordinary_comment_ids"]) == 1,
        "uniform first page plus short final page lost ordinary comments",
    )
    four_comments = SNAPSHOTS.add_ordinary_comment(exact_post)
    short_middle = SNAPSHOTS.split_comment_pages(four_comments, [2, 1, 1])
    try:
        invoke("normalize-github-tracker", short_middle)
    except CONTRACT.ContractError as error:
        CONTRACT.require(
            "comment page sequence is incomplete" in str(error),
            f"short intermediate page diagnostic differs: {error!s}",
        )
    else:
        raise CONTRACT.ContractError("short intermediate comment page was accepted")

    nested = "[" * 2000 + "]" * 2000
    recursion = subprocess.run(
        [sys.executable, str(CONTRACT_PATH), "normalize-github-tracker", "--input", "-"],
        input=nested,
        capture_output=True,
        text=True,
        check=False,
    )
    CONTRACT.require(
        recursion.returncode == 1
        and recursion.stderr.startswith("FAIL: ")
        and "Traceback" not in recursion.stderr,
        "deeply nested JSON leaked a traceback instead of a contract failure",
    )

    oversized = subprocess.run(
        [sys.executable, str(CONTRACT_PATH), "normalize-github-tracker", "--input", "-"],
        input="x" * (CONTRACT.INPUT_LIMIT + 1),
        capture_output=True,
        text=True,
        check=False,
    )
    CONTRACT.require(
        oversized.returncode == 1 and "standard input exceeds" in oversized.stderr,
        "oversized provider input was not rejected before JSON parsing",
    )
    with tempfile.TemporaryDirectory(prefix="repo-gardener-input-limit-") as temporary:
        oversized_body = Path(temporary) / "oversized-body.md"
        oversized_body.write_text("x" * (CONTRACT.BODY_LIMIT + 1), encoding="utf-8")
        body_file = subprocess.run(
            [sys.executable, str(CONTRACT_PATH), "validate-body", "--body", str(oversized_body)],
            capture_output=True,
            text=True,
            check=False,
        )
        CONTRACT.require(
            body_file.returncode == 1 and "managed body exceeds" in body_file.stderr,
            "oversized managed body was not rejected before decoding",
        )

    print("PASS: exact two-comment run identity without hash fields")
    print("PASS: denied close cannot mint a closed run")
    print("PASS: mention-free identity, pagination, count, duplicate, reversed, and interrupted records fail closed")
    print("PASS: checker surface excludes qualitative work, policy, authority, readiness, and register-quality claims")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CONTRACT.ContractError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
