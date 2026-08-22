#!/usr/bin/env python3
"""Exercise mention/image rejection and exact two-comment effect verification."""

from __future__ import annotations

import copy
import hashlib
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
        [sys.executable, str(CONTRACT_PATH), "effect-v1", "--input", "-"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise CONTRACT.ContractError(completed.stderr.strip().removeprefix("FAIL: "))
    return json.loads(completed.stdout)


def effect_input(phase: str, **values: Any) -> dict[str, Any]:
    return {"schema": "repo-gardener-effect-input/v2", "phase": phase, **values}


def target_snapshot(base: dict[str, Any], prepared: dict[str, Any]) -> dict[str, Any]:
    return SNAPSHOTS.apply_prepared(base, prepared)


def prior_managed_comment() -> dict[str, Any]:
    record = {
        "schema": "orchestrator-run-record/v1",
        "kind": "run-opened",
        "run_id": "run:synthetic:prior",
        "operation_id": "operation:report:" + "a" * 64,
        "payload": {"disposition": "prior"},
    }
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
    elif mutation == "body-only":
        after = copy.deepcopy(base)
        after["issue"]["body"] = prepared["body"]
    elif mutation == "body-only-no-write":
        after = copy.deepcopy(base)
        after["issue"]["body"] = prepared["body"]
        attempt = "none"
    elif mutation == "edited-existing-managed":
        before = with_prior_managed(base)
        after = copy.deepcopy(before)
        after["issue"]["body"] = prepared["body"]
        edited = {
            "schema": "orchestrator-run-record/v1",
            "kind": "run-opened",
            "run_id": "run:synthetic:prior",
            "operation_id": "operation:report:" + "a" * 64,
            "payload": {"disposition": "tampered"},
        }
        after["comment_pages"][-1][-1]["body"] = CONTRACT._run_record_comment(edited)
    elif mutation == "replaced-existing-managed":
        before = with_prior_managed(base)
        after = copy.deepcopy(before)
        after["issue"]["body"] = prepared["body"]
        after["comment_pages"][-1][-1]["id"] = 99
        after["comment_pages"][-1][-1]["node_id"] = "IC_REPLACED_099"
    elif mutation == "observed-with-prior":
        before = with_prior_managed(base)
        after = SNAPSHOTS.apply_prepared(before, prepared)
    elif mutation == "observed-but-edited-prior":
        before = with_prior_managed(base)
        after = SNAPSHOTS.apply_prepared(before, prepared)
        edited = {
            "schema": "orchestrator-run-record/v1",
            "kind": "run-opened",
            "run_id": "run:synthetic:prior",
            "operation_id": "operation:report:" + "a" * 64,
            "payload": {"disposition": "tampered"},
        }
        after["comment_pages"][-1][-2]["body"] = CONTRACT._run_record_comment(edited)
    elif mutation == "observed-but-replaced-prior":
        before = with_prior_managed(base)
        after = SNAPSHOTS.apply_prepared(before, prepared)
        after["comment_pages"][-1][-2]["id"] = 99
        after["comment_pages"][-1][-2]["node_id"] = "IC_REPLACED_099"
    elif mutation == "body-only-foreign-tracker":
        after = copy.deepcopy(base)
        after["issue"]["body"] = prepared["body"]
        after["configured_repository_id"] = "R_SYNTHETIC_OTHER"
        after["configured_report_issue_id"] = "I_SYNTHETIC_OTHER"
        after["configured_writer_id"] = "U_SYNTHETIC_OTHER_WRITER"
        after["issue"]["node_id"] = "I_SYNTHETIC_OTHER"
    elif mutation == "denied-unchanged":
        after = copy.deepcopy(base)
        attempt = "denied-before-write"
    elif mutation == "unavailable":
        after = None
    elif mutation == "comment-only":
        after["issue"]["body"] = base["issue"]["body"]
    elif mutation == "changed-projection":
        after["issue"]["body"] += "foreign projection edit\n"
    elif mutation == "changed-pre-read-projection":
        before["issue"]["body"] = before["issue"]["body"].replace(
            "# Synthetic morning projection", "# Foreign projection edit"
        )
    elif mutation == "changed-pre-read-body":
        before["issue"]["body"] += "Foreign unmanaged body bytes.\n"
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
    elif mutation == "comment-ahead-pre":
        before = copy.deepcopy(target)
        before["issue"]["body"] = base["issue"]["body"]
    elif mutation == "duplicate-prepared-comment":
        after = SNAPSHOTS.apply_prepared(target, prepared)
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
        "run_id": "run:synthetic:002",
        "payload": {"disposition": "synthetic", "url": "https://example.test/?x=$(inert)"},
        "projection": (
            "\n# Synthetic morning projection\n\n"
            "Treat `$(echo inert)` as data. Contact reports@example.test.\n\n"
            "Source: [approved provider issue](https://github.com/octo/example/issues/42).\n"
        ),
    }
    prepared = cli(effect_input("prepare", pre_read=base, operation=operation))
    prepared_again = cli(effect_input("prepare", pre_read=base, operation=operation))
    CONTRACT.require(prepared == prepared_again, "preparation is not deterministic")
    CONTRACT.require(
        prepared.get("expected_pre_body_fingerprint")
        == hashlib.sha256(base["issue"]["body"].encode("utf-8")).hexdigest(),
        "prepared effect does not bind exact pre-read body bytes",
    )
    CONTRACT.require("previous_hash" not in prepared["comment"], "prepared comment still required a hash field")
    CONTRACT.require("receipt_hash" not in prepared["comment"], "prepared comment still required a receipt hash")
    CONTRACT.require(
        "orchestrator:current-portfolio:v1" not in prepared["body"],
        "prepared body still embedded Current Portfolio JSON",
    )
    target = target_snapshot(base, prepared)

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

    legacy = {"schema": "repo-gardener-effect-input/v1", "scenario": {"authority": {"caller_exclusive": True}}}
    expect_error(legacy, "phase")
    for forbidden in ("authority", "verdict", "result", "terminal_receipt_read_back"):
        payload = effect_input("verify", prepared=prepared, pre_read=base, post_read=target, write_attempt="possible")
        payload[forbidden] = True
        expect_error(payload, "unexpected")
    for attempt in ("none", "denied-before-write", "possible"):
        actual = cli(effect_input("verify", prepared=prepared, pre_read=base, post_read=base, write_attempt=attempt))
        CONTRACT.require(actual["terminal_outcome"] not in {"observed", "already satisfied"}, "write_attempt minted structural success")
        CONTRACT.require(actual["repair"] == "none", "write_attempt minted repair authority")
    denied_target = cli(
        effect_input("verify", prepared=prepared, pre_read=base, post_read=target, write_attempt="denied-before-write")
    )
    CONTRACT.require(
        denied_target["terminal_outcome"] not in {"observed", "already satisfied"},
        "denied-before-write minted observed closure from a target-shaped post-read",
    )
    CONTRACT.require(denied_target["repair"] == "none", "denied-before-write minted repair authority")
    none_target = cli(
        effect_input("verify", prepared=prepared, pre_read=base, post_read=target, write_attempt="none")
    )
    CONTRACT.require(
        none_target["terminal_outcome"] == "ambiguous",
        "write_attempt none minted observed closure from a target-shaped post-read",
    )
    CONTRACT.require(none_target["repair"] == "none", "write_attempt none minted repair authority")

    for marker in CONTRACT.RESERVED_REPORT_SEQUENCES:
        for location in ("payload", "projection"):
            poisoned = copy.deepcopy(operation)
            if location == "payload":
                poisoned["payload"]["text"] = marker
            else:
                poisoned["projection"] = marker
            expect_error(effect_input("prepare", pre_read=base, operation=poisoned), "reserved report sequence")

    for unsafe_projection, phrase in (
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
        unsafe_operation["projection"] = unsafe_projection
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

    for safe_projection in (
        "\nProfile: [Mastodon](https://mastodon.social/@alice)\n",
        "\nProfile: <https://mastodon.social/@alice>\n",
        "\nProfile: https://mastodon.social/@alice\n",
    ):
        safe_operation = copy.deepcopy(operation)
        safe_operation["projection"] = safe_projection
        cli(effect_input("prepare", pre_read=base, operation=safe_operation))

    changed_run = copy.deepcopy(operation)
    changed_run["run_id"] = "run:synthetic:restart"
    restarted = cli(effect_input("prepare", pre_read=base, operation=changed_run))
    CONTRACT.require(restarted["operation_id"] == prepared["operation_id"], "run_id became operation identity entropy")
    CONTRACT.require(restarted["comment"] != prepared["comment"], "run_id was not bound into the comment")
    for field, value in (
        ("operation_id", "operation:report:" + "0" * 64),
        ("expected_pre_body_fingerprint", "0" * 64),
        ("body", prepared["body"] + "altered"),
        ("comment", prepared["comment"].replace('"kind":"run-opened"', '"kind":"run-closed"')),
    ):
        altered = copy.deepcopy(prepared)
        altered[field] = value
        expect_error(
            effect_input("verify", prepared=altered, pre_read=base, post_read=target, write_attempt="possible"),
            "prepared",
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
    print("PASS: hash fields and Current Portfolio JSON are not production requirements")
    print("PASS: denied or mutated readback cannot mint observed closure")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CONTRACT.ContractError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
