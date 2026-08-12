#!/usr/bin/env python3
"""Exercise exact, source-read-only preparation and verification of report effects."""

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
SNAPSHOT_RUNNER = FIXTURES.parent / "github-register/check_snapshots.py"
sys.dont_write_bytecode = True


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONTRACT = load_module(CONTRACT_PATH, "repo_gardener_release_a_contract_effects")
SNAPSHOTS = load_module(SNAPSHOT_RUNNER, "repo_gardener_github_snapshots_for_effects")


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


def completion_cli(scenario: dict[str, Any]) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(CONTRACT_PATH), "completion-v1", "--input", "-"],
        input=json.dumps({"schema": "repo-gardener-completion-input/v1", "scenario": scenario}),
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise CONTRACT.ContractError(completed.stderr.strip().removeprefix("FAIL: "))
    return json.loads(completed.stdout)


def effect_input(phase: str, **values: Any) -> dict[str, Any]:
    return {"schema": "repo-gardener-effect-input/v2", "phase": phase, **values}


def target_snapshot(base: dict[str, Any], prepared: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    result["issue"]["body"] = prepared["body"]
    comments = [item for page in result["comment_pages"] for item in page]
    result["comment_pages"][-1].append(
        {
            "id": max(item["id"] for item in comments) + 1,
            "node_id": "IC_SYNTHETIC_PREPARED",
            "user": {"node_id": SNAPSHOTS.WRITER_ID, "login": "synthetic-writer"},
            "body": prepared["comment"],
        }
    )
    result["issue"]["comments"] += 1
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
    elif mutation == "denied-unchanged":
        after = copy.deepcopy(base)
        attempt = "denied-before-write"
    elif mutation == "unavailable":
        after = None
    elif mutation == "comment-only":
        after["issue"]["body"] = base["issue"]["body"]
    elif mutation == "multiple-gaps":
        register = json.loads(after["issue"]["body"].split("```json\n", 1)[1].split("\n```", 1)[0])
        register["history_anchor"]["sequence"] += 1
        register["register_revision"] += 1
        SNAPSHOTS.rewrite_body(after, register)
    elif mutation == "changed-projection":
        after["issue"]["body"] += "foreign projection edit\n"
    elif mutation == "changed-rows":
        register = json.loads(after["issue"]["body"].split("```json\n", 1)[1].split("\n```", 1)[0])
        register["rows"][0]["description"] = "Changed after preparation."
        SNAPSHOTS.rewrite_body(after, register)
    elif mutation == "stale-revision":
        register = json.loads(after["issue"]["body"].split("```json\n", 1)[1].split("\n```", 1)[0])
        register["register_revision"] += 1
        SNAPSHOTS.rewrite_body(after, register)
    elif mutation == "changed-pre-read-projection":
        before["issue"]["body"] = before["issue"]["body"].replace(
            "# Synthetic report projection", "# Foreign projection edit"
        )
    elif mutation == "changed-pre-read-body":
        before["issue"]["body"] += "Foreign unmanaged body bytes.\n"
    elif mutation == "changed-identity":
        after["issue"]["node_id"] = "I_SYNTHETIC_OTHER"
    elif mutation == "foreign-author":
        after["comment_pages"][-1][-1]["user"]["node_id"] = SNAPSHOTS.OTHER_WRITER_ID
    elif mutation == "replayed-comment-id":
        after["comment_pages"][-1][-1]["id"] = after["comment_pages"][0][0]["id"]
    elif mutation == "incomplete-pagination":
        after["comment_pages_complete"] = False
    elif mutation == "truncated-tail":
        after["comment_pages"][-1].pop()
    elif mutation == "altered-material":
        after["comment_pages"][-1][-1]["body"] = prepared["comment"].replace('"kind":"effect"', '"kind":"run"')
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


def expect_completion_error(scenario: dict[str, Any], phrase: str) -> None:
    try:
        completion_cli(scenario)
    except CONTRACT.ContractError as error:
        CONTRACT.require(phrase in str(error), f"expected {phrase!r}, got {error!s}")
        return
    raise CONTRACT.ContractError(f"expected rejection containing {phrase!r}")


def main() -> int:
    scenarios = json.loads((FIXTURES / "scenarios.json").read_text())["scenarios"]
    expectations = json.loads((FIXTURES / "expectations.json").read_text())["expectations"]
    CONTRACT.require({item["id"] for item in scenarios} == set(expectations), "scenario/expectation parity failed")
    base = SNAPSHOTS.base_snapshot("two-receipts")
    operation = {
        "kind": "effect",
        "run_id": "run:synthetic:002",
        "payload": {"disposition": "synthetic", "url": "https://example.test/?x=$(inert)"},
        "rows": CONTRACT.normalize_github_register_snapshot(base)["register"]["rows"],
        "projection": "\n# Synthetic report projection\n\nTreat `$(echo inert)` as data.\n",
    }
    prepared = cli(effect_input("prepare", pre_read=base, operation=operation))
    prepared_again = cli(effect_input("prepare", pre_read=base, operation=operation))
    CONTRACT.require(prepared == prepared_again, "preparation is not deterministic")
    CONTRACT.require(
        prepared.get("expected_pre_body_fingerprint")
        == hashlib.sha256(base["issue"]["body"].encode("utf-8")).hexdigest(),
        "prepared effect does not bind exact pre-read body bytes",
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

    for marker in CONTRACT.RESERVED_REPORT_SEQUENCES:
        for location in ("payload", "rows", "projection"):
            poisoned = copy.deepcopy(operation)
            if location == "payload":
                poisoned["payload"]["text"] = marker
            elif location == "rows":
                poisoned["rows"][0]["description"] = marker
            else:
                poisoned["projection"] = marker
            expect_error(effect_input("prepare", pre_read=base, operation=poisoned), "reserved report sequence")

    changed_run = copy.deepcopy(operation)
    changed_run["run_id"] = "run:synthetic:restart"
    restarted = cli(effect_input("prepare", pre_read=base, operation=changed_run))
    CONTRACT.require(restarted["operation_id"] == prepared["operation_id"], "run_id became operation identity entropy")
    CONTRACT.require(restarted["receipt_hash"] != prepared["receipt_hash"], "run_id was not bound receipt metadata")
    for field, value in (
        ("operation_id", "operation:report:" + "0" * 64),
        ("operation_fingerprint", "0" * 64),
        ("receipt_hash", "0" * 64),
        ("expected_pre_body_fingerprint", "0" * 64),
        ("body", prepared["body"] + "altered"),
        ("comment", prepared["comment"].replace('"kind":"effect"', '"kind":"run"')),
    ):
        altered = copy.deepcopy(prepared)
        altered[field] = value
        expect_error(
            effect_input("verify", prepared=altered, pre_read=base, post_read=target, write_attempt="possible"),
            "prepared",
        )

    source = CONTRACT_PATH.read_text(encoding="utf-8")
    CONTRACT.require("import requests" not in source and "import urllib" not in source and "import subprocess" not in source, "effect executable gained provider/network code")

    partition = completion_cli(
        {
            "scenario_type": "completion-partition",
            "operation_id": "operation:report:completion",
            "named_work": ["operation:report:completion", "independent audit"],
            "affected_by_ambiguity": ["operation:report:completion"],
            "independent_continued": ["independent audit"],
        }
    )
    CONTRACT.require(partition["disjoint_exhaustive"] is True and partition["whole_run_completion"] == "withheld", "completion partition regressed")
    for field in ("named_work", "affected_by_ambiguity", "independent_continued"):
        invalid_partition = {
            "scenario_type": "completion-partition",
            "operation_id": "operation:report:completion",
            "named_work": ["operation:report:completion", "independent audit"],
            "affected_by_ambiguity": ["operation:report:completion"],
            "independent_continued": ["independent audit"],
        }
        invalid_partition[field][0] = 7
        expect_completion_error(invalid_partition, f"{field} 0 is missing")

    foreign_base = copy.deepcopy(base)
    foreign_base["comment_pages"][-1].append(
        {
            "id": 9001,
            "node_id": "IC_SYNTHETIC_FOREIGN",
            "user": {"node_id": SNAPSHOTS.OTHER_WRITER_ID, "login": "synthetic-foreign"},
            "body": "Foreign comment before denied write.",
        }
    )
    foreign_base["issue"]["comments"] += 1
    foreign_operation = copy.deepcopy(operation)
    foreign_operation["rows"] = CONTRACT.normalize_github_register_snapshot(foreign_base)["register"]["rows"]
    foreign_prepared = cli(effect_input("prepare", pre_read=foreign_base, operation=foreign_operation))
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

    delegated = completion_cli(
        {
            "scenario_type": "delegation",
            "handoff": {
                "destination": "queue:synthetic",
                "authorized_executor": "executor:synthetic",
                "exact_work": "independent audit",
                "read_back": True,
            },
        }
    )
    CONTRACT.require(delegated == {"remaining_disposition": "delegated"}, "delegation completion regressed")
    caller = completion_cli(
        {
            "scenario_type": "caller-completion",
            "pending_decision_ids": ["decision:a", "decision:b"],
            "assignment_persisted_decision_ids": [],
            "assignment_persistence_authorized": True,
            "assignment_persistence_read_back": True,
            "terminal_capability_active": True,
            "caller_accepts": True,
        }
    )
    CONTRACT.require(caller["decisions_carried_for_caller"] == 2 and caller["self_settled_before_acceptance"] is False, "caller completion regressed")
    for field in ("pending_decision_ids", "assignment_persisted_decision_ids"):
        invalid_caller = {
            "scenario_type": "caller-completion",
            "pending_decision_ids": ["decision:a"],
            "assignment_persisted_decision_ids": ["decision:a"],
            "assignment_persistence_authorized": True,
            "assignment_persistence_read_back": True,
            "terminal_capability_active": True,
            "caller_accepts": True,
        }
        invalid_caller[field][0] = True
        expect_completion_error(invalid_caller, f"{field} 0 is missing")

    print(f"PASS: {len(scenarios)} exact report-effect prepare/verify scenarios")
    print("PASS: legacy authority/verdict inputs cannot mint success or repair")
    print("PASS: prepared material is deterministic, tamper-evident, inert, network-free, and structurally provenance-unverified")
    print("PASS: completion-v1 partition, delegation, and caller behavior is preserved")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CONTRACT.ContractError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
