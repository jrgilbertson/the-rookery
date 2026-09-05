#!/usr/bin/env python3
"""Exercise mention/image rejection and exact two-comment effect verification."""

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
SNAPSHOT_HELPER = FIXTURES.parent / "tracker_snapshots.py"
sys.dont_write_bytecode = True


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONTRACT = load_module(CONTRACT_PATH, "repo_gardener_release_a_contract_effects")
SNAPSHOTS = load_module(SNAPSHOT_HELPER, "repo_gardener_tracker_snapshots_for_effects")


def cli(payload: dict[str, Any]) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(CONTRACT_PATH), "effect", "--input", "-"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise CONTRACT.ContractError(completed.stderr.strip().removeprefix("FAIL: "))
    return json.loads(completed.stdout)


def effect_input(phase: str, **values: Any) -> dict[str, Any]:
    return {"schema": "repo-gardener-effect-input", "phase": phase, **values}


def target_snapshot(base: dict[str, Any], prepared: dict[str, Any]) -> dict[str, Any]:
    return SNAPSHOTS.apply_prepared(base, prepared)


def prior_record(disposition: str) -> dict[str, Any]:
    return {
        "schema": "orchestrator-run-record",
        "kind": "run-opened",
        "run_id": "run:synthetic:prior",
        "payload": {"disposition": disposition},
    }


def prior_managed_comment() -> dict[str, Any]:
    record = prior_record("prior")
    return {
        "id": 1,
        "node_id": "IC_PRIOR_001",
        "user": {"node_id": SNAPSHOTS.WRITER_ID, "login": "synthetic-writer"},
        "body": CONTRACT._run_record_comment(record),
    }


def with_prior_managed(snapshot: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(snapshot)
    result["comment_pages"][-1].append(prior_managed_comment())
    result["issue"]["comments"] = len([item for page in result["comment_pages"] for item in page])
    return result


def mutate(base: dict[str, Any], target: dict[str, Any], prepared: dict[str, Any], mutation: str) -> tuple[dict[str, Any], Any, str]:
    before = copy.deepcopy(base)
    after: Any = copy.deepcopy(target)
    attempt = "possible"
    if mutation == "exact-post-read":
        pass
    elif mutation == "preexisting":
        before = copy.deepcopy(target)
        attempt = "none"
    elif mutation == "missing-comment":
        after = copy.deepcopy(base)
    elif mutation == "observed-with-prior":
        before = with_prior_managed(base)
        after = SNAPSHOTS.apply_prepared(before, prepared)
    elif mutation == "observed-but-edited-prior":
        before = with_prior_managed(base)
        after = SNAPSHOTS.apply_prepared(before, prepared)
        edited = prior_record("tampered")
        after["comment_pages"][-1][-2]["body"] = CONTRACT._run_record_comment(edited)
    elif mutation == "observed-but-replaced-prior":
        before = with_prior_managed(base)
        after = SNAPSHOTS.apply_prepared(before, prepared)
        after["comment_pages"][-1][-2]["id"] = 99
        after["comment_pages"][-1][-2]["node_id"] = "IC_REPLACED_099"
    elif mutation == "foreign-tracker":
        after["configured_repository_id"] = "R_SYNTHETIC_OTHER"
    elif mutation == "denied-unchanged":
        after = copy.deepcopy(base)
        attempt = "denied-before-write"
    elif mutation == "unavailable":
        after = None
    elif mutation == "changed-static-body":
        after["issue"]["body"] += "Owner edited tracker description.\n"
    elif mutation == "changed-identity":
        after["issue"]["node_id"] = "I_SYNTHETIC_OTHER"
    elif mutation == "foreign-author":
        after["comment_pages"][-1][-1]["user"]["node_id"] = SNAPSHOTS.OTHER_WRITER_ID
    elif mutation == "replayed-comment-id":
        after["comment_pages"][-1][-1]["id"] = 7
        after["comment_pages"][-1].insert(
            0,
            {
                "id": 7,
                "node_id": "IC_SYNTHETIC_REPLAY",
                "user": {"node_id": SNAPSHOTS.WRITER_ID, "login": "synthetic-writer"},
                "body": "Ordinary duplicate-id decoy.",
            },
        )
        after["issue"]["comments"] += 1
    elif mutation == "incomplete-pagination":
        after["comment_pages_complete"] = False
    elif mutation == "truncated-tail":
        after["comment_pages"][-1].pop()
    elif mutation == "altered-material":
        after["comment_pages"][-1][-1]["body"] = prepared["comment"].replace(
            '"kind":"run-opened"', '"kind":"run-closed"'
        )
    elif mutation == "duplicate-prepared-comment":
        after = SNAPSHOTS.apply_prepared(target, prepared)
    elif mutation == "already-satisfied-but-edited-prior":
        before = with_prior_managed(target)
        after = copy.deepcopy(before)
        edited = prior_record("tampered")
        after["comment_pages"][-1][-1]["body"] = CONTRACT._run_record_comment(edited)
        attempt = "none"
    elif mutation == "already-satisfied-but-replaced-prior":
        before = with_prior_managed(target)
        after = copy.deepcopy(before)
        after["comment_pages"][-1][-1]["id"] = 99
        after["comment_pages"][-1][-1]["node_id"] = "IC_REPLACED_099"
        attempt = "none"
    elif mutation == "already-satisfied-but-removed-prior":
        before = with_prior_managed(target)
        after = copy.deepcopy(before)
        after["comment_pages"][-1].pop()
        after["issue"]["comments"] = len(
            [item for page in after["comment_pages"] for item in page]
        )
        attempt = "none"
    elif mutation == "already-satisfied-but-added-other":
        before = copy.deepcopy(target)
        after = with_prior_managed(target)
        attempt = "none"
    else:
        raise AssertionError(mutation)
    return before, after, attempt


def expect_error(payload: dict[str, Any], phrase: str) -> None:
    try:
        cli(payload)
    except CONTRACT.ContractError as error:
        CONTRACT.require(phrase in str(error), f"expected {phrase!r}, got {error!s}")
        return
    raise CONTRACT.ContractError(f"expected rejection containing {phrase!r}")


def main() -> int:
    scenarios = json.loads((FIXTURES / "scenarios.json").read_text())["scenarios"]
    expectations = json.loads((FIXTURES / "expectations.json").read_text())["expectations"]
    CONTRACT.require({item["id"] for item in scenarios} == set(expectations), "scenario/expectation parity failed")
    base = SNAPSHOTS.empty_tracker()
    operation = {
        "kind": "run-opened",
        "run_id": "run:5b43f68f-7892-4872-a72a-4865412a25a7",
        "payload": {"disposition": "synthetic", "url": "https://example.test/?x=$(inert)"},
        "report": (
            "\n# Synthetic morning projection\n\n"
            "Treat `$(echo inert)` as data. Contact reports@example.test.\n\n"
            "Source: [approved provider issue](https://github.com/octo/example/issues/42).\n"
        ),
    }
    prepared = cli(effect_input("prepare", pre_read=base, operation=operation))
    prepared_again = cli(effect_input("prepare", pre_read=base, operation=operation))
    CONTRACT.require(prepared == prepared_again, "preparation is not deterministic")
    CONTRACT.require(set(prepared) == {"schema", "repository_id", "report_issue_id", "writer_id", "operation", "comment"}, "prepared effect contains body or transaction machinery")
    CONTRACT.require(prepared["comment"].endswith(operation["report"]), "report is absent from the comment")
    target = target_snapshot(base, prepared)
    CONTRACT.require(target["issue"]["body"] == base["issue"]["body"], "append changed the static issue body")

    for scenario in scenarios:
        before, after, attempt = mutate(base, target, prepared, scenario["mutation"])
        actual = cli(
            effect_input(
                "verify",
                prepared=prepared,
                pre_read=before,
                post_read=after,
                write_attempt=attempt,
            )
        )
        for key, expected in expectations[scenario["id"]].items():
            CONTRACT.require(actual.get(key) == expected, f"{scenario['id']} {key}: {actual.get(key)!r} != {expected!r}")
        CONTRACT.require(actual.get("provenance") == "unverified", f"{scenario['id']} invented provenance")

    # Preparation admits only an opening or a close with a durable opening.
    closing_operation = dict(operation, kind="run-closed", report="# Morning report\n\nRun outcome: complete.\n")
    expect_error(effect_input("prepare", pre_read=base, operation=closing_operation), "lack its opening")
    closed = cli(effect_input("prepare", pre_read=target, operation=closing_operation))
    after_close = target_snapshot(target, closed)
    CONTRACT.require(after_close["issue"]["body"] == base["issue"]["body"], "closure mutated issue body")
    observed_close = cli(effect_input("verify", prepared=closed, pre_read=target, post_read=after_close, write_attempt="possible"))
    CONTRACT.require(observed_close["terminal_outcome"] == "observed", "closing comment was not verified")
    lost_response = cli(effect_input("verify", prepared=closed, pre_read=after_close, post_read=after_close, write_attempt="none"))
    CONTRACT.require(lost_response["terminal_outcome"] == "already satisfied", "lost response demanded another comment")
    # A second run on the same tracker needs no clock tick, but cannot reuse a closed ID.
    expect_error(effect_input("prepare", pre_read=after_close, operation=operation), "conflict")
    next_snapshot = after_close
    for next_operation in (operation, closing_operation):
        next_operation = dict(next_operation, run_id="run:ab1898d2-34e1-49a8-b068-c5858a32a2d9")
        next_prepared = cli(effect_input("prepare", pre_read=next_snapshot, operation=next_operation))
        next_post_read = target_snapshot(next_snapshot, next_prepared)
        next_result = cli(effect_input("verify", prepared=next_prepared, pre_read=next_snapshot, post_read=next_post_read, write_attempt="possible"))
        CONTRACT.require(next_result["terminal_outcome"] == "observed", "sequential run did not verify")
        next_snapshot = next_post_read
    for run_id, closing in ((operation["run_id"], closed), (next_operation["run_id"], next_prepared)):
        CONTRACT.verify_run_records(run_id, closing, next_snapshot)
    for conflicting in (dict(operation, report="Changed opening"), dict(closing_operation, report="Changed closing")):
        expect_error(effect_input("prepare", pre_read=after_close, operation=conflicting), "conflict")
    for over_limit in (dict(operation, report="x" * CONTRACT.BODY_LIMIT), dict(operation, payload={"text": "x" * CONTRACT.RECEIPT_LIMIT})):
        expect_error(effect_input("prepare", pre_read=base, operation=over_limit), "exceeds")

    missing_phase = {"schema": "repo-gardener-effect-input", "scenario": {"authority": {"caller_exclusive": True}}}
    expect_error(missing_phase, "phase")
    for forbidden in ("authority", "verdict", "result", "terminal_receipt_read_back"):
        payload = effect_input("verify", prepared=prepared, pre_read=base, post_read=target, write_attempt="possible")
        payload[forbidden] = True
        expect_error(payload, "unexpected")
    for attempt in ("none", "denied-before-write", "possible"):
        actual = cli(effect_input("verify", prepared=prepared, pre_read=base, post_read=base, write_attempt=attempt))
        CONTRACT.require(actual["terminal_outcome"] not in {"observed", "already satisfied"}, "write_attempt minted structural success")
        CONTRACT.require(set(actual) == {"terminal_outcome", "provenance"}, "verification invented repair machinery")
    denied_target = cli(
        effect_input("verify", prepared=prepared, pre_read=base, post_read=target, write_attempt="denied-before-write")
    )
    CONTRACT.require(
        denied_target["terminal_outcome"] not in {"observed", "already satisfied"},
        "denied-before-write minted observed closure from a target-shaped post-read",
    )
    none_target = cli(
        effect_input("verify", prepared=prepared, pre_read=base, post_read=target, write_attempt="none")
    )
    CONTRACT.require(
        none_target["terminal_outcome"] == "ambiguous",
        "write_attempt none minted observed closure from a target-shaped post-read",
    )

    for marker in CONTRACT.RESERVED_REPORT_SEQUENCES:
        for location in ("payload", "report"):
            poisoned = copy.deepcopy(operation)
            if location == "payload":
                poisoned["payload"]["text"] = marker
            else:
                poisoned["report"] = marker
            expect_error(effect_input("prepare", pre_read=base, operation=poisoned), "reserved report sequence")

    for unsafe_report, phrase in (
        ("\nOwner: @octocat\n", "notification-capable mention"),
        ("\nReviewers: @octo-org/security-team\n", "notification-capable mention"),
        ("\nDependency: @types/node\n", "notification-capable mention"),
        (
            "\nOwner: [@octocat](https://github.com/octocat)\n",
            "notification-capable mention",
        ),
        (
            "\nSee [notes](https://example.com)(@octocat)\n",
            "notification-capable mention",
        ),
        ("\n![tracking pixel](https://attacker.example/pixel.png)\n", "image embedding"),
        (
            "\n![tracking pixel][pixel]\n\n[pixel]: https://attacker.example/pixel.png\n",
            "image embedding",
        ),
        ('\n<img src="https://attacker.example/pixel.png" alt="">\n', "image embedding"),
    ):
        unsafe_operation = copy.deepcopy(operation)
        unsafe_operation["report"] = unsafe_report
        expect_error(effect_input("prepare", pre_read=base, operation=unsafe_operation), phrase)

    for unsafe_payload, phrase in (
        ("@octocat", "notification-capable mention"),
        ("@octo-org/security-team", "notification-capable mention"),
        ("![tracking pixel](https://attacker.example/pixel.png)", "image embedding"),
        ('<img src="https://attacker.example/pixel.png" alt="">', "image embedding"),
    ):
        unsafe_operation = copy.deepcopy(operation)
        unsafe_operation["payload"]["text"] = unsafe_payload
        expect_error(effect_input("prepare", pre_read=base, operation=unsafe_operation), phrase)

    unsafe_comment_operation = copy.deepcopy(operation)
    unsafe_comment_operation["payload"]["package"] = "@types/node"
    expect_error(
        effect_input("prepare", pre_read=base, operation=unsafe_comment_operation),
        "notification-capable mention",
    )

    for safe_report in (
        "\nProfile: [Mastodon](https://mastodon.social/@alice)\n",
        "\nProfile: <https://mastodon.social/@alice>\n",
        "\nProfile: https://mastodon.social/@alice\n",
    ):
        safe_operation = copy.deepcopy(operation)
        safe_operation["report"] = safe_report
        cli(effect_input("prepare", pre_read=base, operation=safe_operation))

    changed_run = copy.deepcopy(operation)
    changed_run["run_id"] = "run:synthetic:restart"
    restarted = cli(effect_input("prepare", pre_read=base, operation=changed_run))
    CONTRACT.require(restarted["comment"] != prepared["comment"], "run_id was not bound into the comment")
    for field, value in (
        ("comment", prepared["comment"].replace('"kind":"run-opened"', '"kind":"run-closed"')),
    ):
        altered = copy.deepcopy(prepared)
        altered[field] = value
        expect_error(
            effect_input("verify", prepared=altered, pre_read=base, post_read=target, write_attempt="possible"),
            "prepared",
        )

    bool_operation = copy.deepcopy(operation)
    bool_operation["payload"] = {"approved": True}
    bool_prepared = cli(effect_input("prepare", pre_read=base, operation=bool_operation))
    _, bool_record = CONTRACT._extract_marked_json(
        bool_prepared["comment"],
        CONTRACT.RUN_RECORD_BEGIN,
        CONTRACT.RUN_RECORD_END,
        "prepared run-record comment",
    )
    confused = copy.deepcopy(bool_prepared)
    confused_record = copy.deepcopy(bool_record)
    confused_record["payload"] = {"approved": 1}
    confused["comment"] = CONTRACT._run_record_comment(confused_record)
    expect_error(
        effect_input(
            "verify",
            prepared=confused,
            pre_read=base,
            post_read=target_snapshot(base, bool_prepared),
            write_attempt="possible",
        ),
        "prepared comment material mismatch",
    )

    source = CONTRACT_PATH.read_text(encoding="utf-8")
    CONTRACT.require("import requests" not in source and "import urllib" not in source and "import subprocess" not in source, "effect executable gained provider/network code")
    for obsolete in (
        "normalize-github-register",
        "register_closed_consistently",
        "orchestrator-register/v1",
        "current-portfolio:v1",
        "overall_dogfood_complete",
        "RELEASE_A_PORTFOLIO_LIMIT",
    ):
        CONTRACT.require(obsolete not in source, f"obsolete register-machine production path remains: {obsolete}")

    foreign_base = SNAPSHOTS.add_ordinary_comment(base)
    foreign_prepared = cli(effect_input("prepare", pre_read=foreign_base, operation=operation))
    for changed_field in ("body", "author"):
        foreign_after = copy.deepcopy(foreign_base)
        comment = foreign_after["comment_pages"][-1][-1]
        if changed_field == "body":
            comment["body"] = "Foreign comment changed after denied write."
        else:
            comment["user"]["node_id"] = "U_SYNTHETIC_FOREIGN_CHANGED"
        actual = cli(
            effect_input(
                "verify",
                prepared=foreign_prepared,
                pre_read=foreign_base,
                post_read=foreign_after,
                write_attempt="denied-before-write",
            )
        )
        CONTRACT.require(actual["terminal_outcome"] == "ambiguous", f"foreign comment {changed_field} edit was misclassified")

    nonfinite_operation = copy.deepcopy(operation)
    nonfinite_operation["payload"] = {"invalid": float("nan")}
    expect_error(effect_input("prepare", pre_read=base, operation=nonfinite_operation), "non-finite")

    register_snapshot = copy.deepcopy(base)
    register_snapshot["schema"] = "repo-gardener-github-register-snapshot/v1"
    expect_error(effect_input("prepare", pre_read=register_snapshot, operation=operation), "tracker snapshot schema")

    print(f"PASS: {len(scenarios)} exact two-comment prepare/verify scenarios")
    print("PASS: mention and image embedding in prepared tracker content fail closed")
    print("PASS: one immutable comment contains the report; the issue body stays unchanged")
    print("PASS: denied or mutated readback cannot mint observed closure")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CONTRACT.ContractError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
