#!/usr/bin/env python3
"""Exercise reconciliation as an internal consumer of exact report verification."""

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
POLICY_PATH = ROOT / "skills/repo-gardener/assets/policy-template.yaml"
sys.dont_write_bytecode = True


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONTRACT = load_module(CONTRACT_PATH, "repo_gardener_release_a_contract_reconciliation")
SNAPSHOTS = load_module(SNAPSHOT_RUNNER, "repo_gardener_snapshots_for_reconciliation")


def load(name: str) -> Any:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def cli(command: str, payload: dict[str, Any]) -> dict[str, Any]:
    arguments = [sys.executable, str(CONTRACT_PATH), command, "--input", "-"]
    if command == "reconciliation-v2":
        arguments.extend(["--policy", str(POLICY_PATH)])
    completed = subprocess.run(arguments, input=json.dumps(payload), capture_output=True, text=True)
    if completed.returncode:
        raise CONTRACT.ContractError(completed.stderr.strip().removeprefix("FAIL: "))
    return json.loads(completed.stdout)


def expect_error(payload: dict[str, Any], phrase: str) -> None:
    try:
        cli("reconciliation-v2", payload)
    except CONTRACT.ContractError as error:
        CONTRACT.require(phrase in str(error), f"expected {phrase!r}, got {error!s}")
        return
    raise CONTRACT.ContractError(f"expected rejection containing {phrase!r}")


def target_snapshot(base: dict[str, Any], prepared: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    result["issue"]["body"] = prepared["body"]
    comments = [item for page in result["comment_pages"] for item in page]
    result["comment_pages"][-1].append(
        {
            "id": max(item["id"] for item in comments) + 1,
            "node_id": "IC_SYNTHETIC_RECONCILIATION",
            "user": {"node_id": SNAPSHOTS.WRITER_ID, "login": "synthetic-writer"},
            "body": prepared["comment"],
        }
    )
    result["issue"]["comments"] += 1
    return result


def snapshots(recipe: dict[str, Any], base: dict[str, Any], prepared: dict[str, Any]) -> tuple[dict[str, Any], Any]:
    target = target_snapshot(base, prepared)
    if recipe["mutation"] == "exact-post-read":
        return copy.deepcopy(base), target
    if recipe["mutation"] == "preexisting":
        return copy.deepcopy(target), copy.deepcopy(target)
    if recipe["mutation"] == "body-only":
        after = copy.deepcopy(base)
        after["issue"]["body"] = prepared["body"]
        return copy.deepcopy(base), after
    if recipe["mutation"] == "denied-unchanged":
        return copy.deepcopy(base), copy.deepcopy(base)
    raise AssertionError(recipe["mutation"])


def prepare(base: dict[str, Any], kind: str) -> dict[str, Any]:
    view = CONTRACT.normalize_github_register_snapshot(base)
    operation = {
        "kind": kind,
        "run_id": "run:synthetic:009",
        "payload": {"disposition": "synthetic reconciliation"},
        "rows": view["register"]["rows"],
        "projection": "\n# Synthetic reconciliation projection\n",
    }
    return cli(
        "effect-v1",
        {"schema": "repo-gardener-effect-input/v2", "phase": "prepare", "pre_read": base, "operation": operation},
    )


def work_items(scenario: dict[str, Any], manifest: dict[str, Any], prepared: dict[str, Any]) -> list[dict[str, Any]]:
    repository_id = prepared["repository_id"]
    report_effect = {"repository_id": repository_id, "operation_id": prepared["operation_id"]}
    by_lane = {
        lane: {"repository_id": repository_id, "operation_id": f"operation:lane:{lane}"}
        for lane in manifest["scouts"]
    }
    result = []
    for lane in manifest["scouts"]:
        dependencies = [by_lane[item] for item in scenario["lane_dependencies"].get(lane, [])]
        if lane in scenario["report_dependent_lanes"]:
            dependencies.append(report_effect)
        result.append({**by_lane[lane], "lane": lane, "dependencies": dependencies})
    return result


def payload_for(
    scenario: dict[str, Any],
    recipes: dict[str, dict[str, Any]],
    manifest: dict[str, Any],
    base: dict[str, Any],
) -> dict[str, Any]:
    prepared = prepare(base, scenario["prepared_kind"])
    recipe = recipes[scenario["readback"]]
    pre_read, post_read = snapshots(recipe, base, prepared)
    receipt_collection = load(scenario["receipt_fixture"])
    receipt_collection["repository_id"] = prepared["repository_id"]
    return {
        "schema": "repo-gardener-reconciliation-input/v2",
        "prepared": prepared,
        "pre_read": pre_read,
        "post_read": post_read,
        "write_attempt": recipe["write_attempt"],
        "manifest": manifest,
        "receipts": receipt_collection,
        "work": work_items(scenario, manifest, prepared),
    }


def assert_expected(identity: str, actual: dict[str, Any], expected: dict[str, Any]) -> None:
    counts = {name: len(actual["completion_partition"][name]) for name in ("completed", "blocked", "preserved", "closed")}
    derived = {**actual, **counts}
    for key, value in expected.items():
        CONTRACT.require(derived.get(key) == value, f"{identity} {key}: {derived.get(key)!r} != {value!r}")


def main() -> int:
    scenario_document = load("scenarios.json")
    expectation_document = load("expectations.json")
    recipe_document = load("wrapper-readbacks.json")
    CONTRACT.require(scenario_document.get("schema") == "repo-gardener-reconciliation-scenarios/v2", "scenario schema mismatch")
    CONTRACT.require(expectation_document.get("schema") == "repo-gardener-reconciliation-expectations/v2", "expectation schema mismatch")
    CONTRACT.require(recipe_document.get("schema") == "repo-gardener-reconciliation-readback-recipes/v2", "readback recipe schema mismatch")
    scenarios = {item["id"]: item for item in scenario_document["scenarios"]}
    expectations = expectation_document["expectations"]
    recipes = {item["id"]: item for item in recipe_document["readbacks"]}
    CONTRACT.require(set(scenarios) == set(expectations), "scenario/expectation parity failed")
    base = SNAPSHOTS.base_snapshot("two-receipts")
    manifest = json.loads((FIXTURES.parent / "register/manifest.json").read_text())
    manifest["repository_id"] = base["configured_repository_id"]

    payloads: dict[str, dict[str, Any]] = {}
    for identity, scenario in scenarios.items():
        payload = payload_for(scenario, recipes, manifest, base)
        payloads[identity] = payload
        actual = cli("reconciliation-v2", payload)
        assert_expected(identity, actual, expectations[identity])
        CONTRACT.require(len(actual["lane_dispositions"]) == 9, f"{identity} did not represent nine lanes")
        CONTRACT.require({item["lane"] for item in actual["lane_dispositions"]} == set(manifest["scouts"]), f"{identity} lane coverage drifted")
        partition = actual["completion_partition"]
        identities = [tuple(sorted(item.items())) for name in ("completed", "blocked", "preserved", "closed") for item in partition[name]]
        CONTRACT.require(len(identities) == len(set(identities)) == 10, f"{identity} partition is not disjoint and exhaustive")
        CONTRACT.require(actual["granted_capabilities"] == [], f"{identity} minted source/provider capability")

    incomplete = cli("reconciliation-v2", payloads["incomplete-local"])
    dispositions = {item["lane"]: item["disposition"] for item in incomplete["lane_dispositions"]}
    CONTRACT.require(dispositions["runtime-error-and-alert"] == "incomplete", "incomplete lane passed")
    CONTRACT.require(dispositions["security-secret-and-static-analysis"] == "blocked", "incomplete dependency did not remain local")
    CONTRACT.require(dispositions["dependency-and-vulnerability"] == "complete", "independent lane was blocked")

    ambiguous = cli("reconciliation-v2", payloads["ambiguous-local"])
    CONTRACT.require(ambiguous["unmatched_intent"] is True and ambiguous["blind_retry"] is False, "ambiguous intent recovery regressed")
    CONTRACT.require(ambiguous["repair"] == "append-exact-prepared-comment", "one-tail repair was not preserved")
    report_identity = {
        "repository_id": payloads["ambiguous-local"]["prepared"]["repository_id"],
        "operation_id": payloads["ambiguous-local"]["prepared"]["operation_id"],
    }
    CONTRACT.require(
        ambiguous["completion_partition"]["preserved"].count(report_identity) == 1,
        "ambiguous report identity was not preserved exactly once",
    )
    preserved_operations = {
        item["operation_id"] for item in ambiguous["completion_partition"]["preserved"]
    }
    CONTRACT.require(
        {
            report_identity["operation_id"],
            "operation:lane:issue-implementation",
            "operation:lane:ci-and-failing-test",
        }
        <= preserved_operations,
        "ambiguous report dependency was not preserved through the full two-hop closure",
    )
    failed = cli("reconciliation-v2", payloads["failed-local"])
    CONTRACT.require(failed["unmatched_intent"] is False and failed["blind_retry"] is False, "failed effect recovery regressed")

    receipt_map = CONTRACT.validate_scout_receipts(
        payloads["nine-lane-learn"]["receipts"], manifest, complete=True, expected_scouts=list(CONTRACT.RELEASE_A_LANES)
    )
    deduped = CONTRACT.dedupe_scout_observations(
        [
            {"source_id": "forge:advisory:alpha", "lane": "dependency-and-vulnerability", "receipt_id": receipt_map["dependency-and-vulnerability"]["receipt_id"]},
            {"source_id": "forge:advisory:alpha", "lane": "security-secret-and-static-analysis", "receipt_id": receipt_map["security-secret-and-static-analysis"]["receipt_id"]},
        ],
        receipt_map,
    )
    CONTRACT.require(
        deduped["candidate_count"] == 1
        and len(deduped["contributing_lanes"]) == 2
        and len(deduped["receipt_ids"]) == 2,
        "usable-outcome dedupe lost contributing lane evidence",
    )
    passing_gates = {gate: True for gate in CONTRACT.GATE_ORDER}
    capacity = CONTRACT.render_capacity(
        ["row:retained:one", "row:retained:two"],
        [
            {"source_id": "forge:candidate:one", "gate_facts": passing_gates},
            {"source_id": "forge:candidate:two", "gate_facts": passing_gates},
        ],
        POLICY_PATH,
    )
    CONTRACT.require(
        capacity == {"rendered_slots": 7, "retained_first": True, "available_slots": 3, "recommendations": 2},
        "policy-derived retained-first capacity regressed",
    )

    legacy = copy.deepcopy(payloads["nine-lane-learn"])
    legacy["authority"] = {"exclusive_executor": True}
    expect_error(legacy, "unexpected")
    for field, value in (
        ("persistence_claim", True),
        ("readback_completed", True),
        ("effect_reconciled", True),
        ("result", {"terminal_outcome": "observed"}),
        ("verdict", "observed"),
    ):
        poisoned = copy.deepcopy(payloads["nine-lane-learn"])
        poisoned[field] = value
        expect_error(poisoned, "unexpected")
    source = CONTRACT_PATH.read_text(encoding="utf-8")
    for obsolete in (
        'add_parser("validate-register")',
        "def validate_register(",
        '"repo-gardener-register/v1"',
        '"repo-gardener-provider-authentication/v1"',
    ):
        CONTRACT.require(obsolete not in source, f"obsolete parallel register contract remains: {obsolete}")
    completed = subprocess.run(
        [sys.executable, str(CONTRACT_PATH), "validate-register"], capture_output=True, text=True
    )
    CONTRACT.require(completed.returncode != 0 and "invalid choice" in completed.stderr, "obsolete validate-register command remains public")

    duplicate_lane = copy.deepcopy(payloads["nine-lane-learn"])
    duplicate_lane["work"][1]["lane"] = duplicate_lane["work"][0]["lane"]
    expect_error(duplicate_lane, "exactly once")
    foreign_identity = copy.deepcopy(payloads["nine-lane-learn"])
    foreign_identity["work"][0]["repository_id"] = "forge:repository:foreign"
    expect_error(foreign_identity, "repository")
    report_collision = copy.deepcopy(payloads["nine-lane-learn"])
    report_collision["work"][0]["operation_id"] = report_collision["prepared"]["operation_id"]
    expect_error(report_collision, "collides with prepared report identity")
    unknown_dependency = copy.deepcopy(payloads["nine-lane-learn"])
    unknown_dependency["work"][0]["dependencies"] = [
        {"repository_id": unknown_dependency["prepared"]["repository_id"], "operation_id": "operation:missing"}
    ]
    expect_error(unknown_dependency, "unknown completion dependency")
    missing_terminal = copy.deepcopy(payloads["nine-lane-learn"])
    missing_terminal["receipts"]["receipts"].pop()
    expect_error(missing_terminal, "order/coverage")
    unaffirmed_not_applicable = copy.deepcopy(payloads["nine-lane-learn"])
    issue_receipt = next(
        item for item in unaffirmed_not_applicable["receipts"]["receipts"] if item["outcome"] == "not applicable"
    )
    issue_receipt.pop("affirmative_evidence")
    expect_error(unaffirmed_not_applicable, "schema mismatch")

    print(f"PASS: {len(scenarios)} reconciliation scenarios derive report outcomes internally")
    print("PASS: nine lanes remain explicit and completion partitions are repository-qualified, disjoint, and exhaustive")
    print("PASS: legacy authority, persistence, readback, reconciled-effect, result, and verdict inputs are rejected")
    print("PASS: usable-outcome dedupe and policy-derived retained-first capacity remain covered")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CONTRACT.ContractError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
