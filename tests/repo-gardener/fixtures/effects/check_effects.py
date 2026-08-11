#!/usr/bin/env python3
"""Evaluate Release A report-effect facts and mutation-test their authority."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parents[4]
CONTRACT_PATH = REPO_ROOT / "skills" / "repo-gardener" / "scripts" / "release_a_contract.py"
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("repo_gardener_release_a_contract", CONTRACT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load production contract: {CONTRACT_PATH}")
CONTRACT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTRACT)
ContractError = CONTRACT.ContractError
AUTHORITY_FIELDS = CONTRACT.AUTHORITY_FIELDS
require = CONTRACT.require


COMPLETION_SCENARIOS = {"completion-partition", "delegation", "optional-scout", "caller-completion"}


def evaluate(scenario: dict[str, Any]) -> dict[str, Any]:
    command = "completion-v1" if scenario.get("scenario_type") in COMPLETION_SCENARIOS else "effect-v1"
    schema = (
        "repo-gardener-completion-input/v1"
        if command == "completion-v1"
        else "repo-gardener-effect-input/v1"
    )
    completed = subprocess.run(
        [sys.executable, str(CONTRACT_PATH), command, "--input", "-"],
        input=json.dumps({"schema": schema, "scenario": scenario}),
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise ContractError(completed.stderr.strip().removeprefix("FAIL: "))
    return json.loads(completed.stdout)


def load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def assert_expected(identity: str, actual: dict[str, Any], expected: dict[str, Any]) -> None:
    for key, value in expected.items():
        require(actual.get(key) == value, f"{identity} derived {key}={actual.get(key)!r}, expected {value!r}")


def assert_mutation_result(
    scenarios: dict[str, dict[str, Any]],
    identity: str,
    label: str,
    mutate: Callable[[dict[str, Any]], None],
    expected_result: dict[str, Any],
) -> None:
    baseline = evaluate(scenarios[identity])
    changed = copy.deepcopy(scenarios[identity])
    mutate(changed)
    actual = evaluate(changed)
    require(
        any(baseline.get(key) != value for key, value in expected_result.items()),
        f"mutation target does not differ from baseline: {label}",
    )
    assert_expected(f"{identity} mutation {label}", actual, expected_result)


def validate_sources(repo_root: Path) -> None:
    skill_dir = repo_root / "skills" / "repo-gardener"
    effects = (skill_dir / "references" / "applying-effects.md").read_text(encoding="utf-8")
    core = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    register = (skill_dir / "references" / "register-and-report.md").read_text(encoding="utf-8")
    contract = (skill_dir / "scripts" / "release_a_contract.py").read_text(encoding="utf-8")
    effects_words = " ".join(effects.split())
    core_words = " ".join(core.split())
    register_words = " ".join(register.split())
    for phrase in (
        "Mint one stable `operation_id` before the first attempt",
        "Persist and read back one intended-effect receipt",
        "invoke the narrow wrapper at most once",
        "authoritative complete register post-read",
        "Retry is allowed only when source-native register evidence proves absence",
        "disjoint and exhaustive",
        "Name every missing invoke boundary separately",
        "omit `terminal_outcome`",
        "Multiple receipt gaps remain `ambiguous`",
        "render stable `operation_id` and mutable `preconditions` as separate fields",
        "the `terminal_outcome` field contains only one exact canonical token",
        "Render retry proof as four distinct facts",
        "Name the ambiguous report operation itself in `affected_work`",
        "Whenever repair states are requested, state the single-tail mechanics in full",
        "For every rendered report-operation scenario, state separately whether the",
        "repository-qualified pair",
        "preserve the requested repository-qualified identity",
        "If either identity component is absent or invalid before the first attempt",
        "missing terminal readback overrides both success tokens",
        "Explicitly render `whole_run_completion: withheld` for an ambiguous-operation safe stop",
    ):
        require(phrase in effects_words, f"effect contract missing: {phrase}")
    recovery_case = (repo_root / "tests" / "repo-gardener" / "cases" / "effect-recovery-and-ambiguity.md").read_text(encoding="utf-8")
    require(
        "exact stored receipt is appended" in recovery_case
        and "whether the body is" in recovery_case,
        "effect-recovery prompt does not request exact single-tail mechanics",
    )
    authority_case = (repo_root / "tests" / "repo-gardener" / "cases" / "effect-authority-and-wrapper-scope.md").read_text(encoding="utf-8")
    require("Intended-effect receipt readback precedes invoke" in authority_case, "effect authority rubric lost pre-invoke readback")
    caller_case = (repo_root / "tests" / "repo-gardener" / "cases" / "caller-lifecycle-and-local-blockers.md").read_text(encoding="utf-8")
    require("No narrow-wrapper authorization or readback is supplied" in caller_case, "caller lifecycle prompt supplies or implies assignment persistence proof")
    remainder_case = (repo_root / "tests" / "repo-gardener" / "cases" / "mixed-remainder-dispositions.md").read_text(encoding="utf-8")
    require("`whole_run_completion: withheld` is explicit" in remainder_case, "mixed remainder rubric does not require explicit whole-run withholding")
    for phrase in (
        "Keep it active until the caller accepts exactly one terminal",
        "Carry every unpersisted decision exactly once in that single terminal report for caller persistence",
        "do not block, fail, cancel, revoke, release, or otherwise settle",
        "Stop after acceptance",
        "Do not infer assignment authority from a possible persistence path or from the current assignment itself",
        "Caller persistence of every still-unpersisted decision is valid",
    ):
        require(phrase in core_words, f"caller report ordering missing: {phrase}")
    require(
        core_words.count("Carry every unpersisted decision exactly once in that single terminal report for caller persistence") == 1,
        "caller persistence instruction is not one canonical phrase",
    )
    require("def installed_lanes(" not in contract, "unused installed_lanes policy wrapper remains")
    for phrase in (
        "prepared body replacement and one comment append",
        "not an atomic transaction or distributed lock",
        "append that exact stored receipt once without rewriting the body",
    ):
        require(phrase in register_words, f"report recovery contract missing: {phrase}")


def main() -> int:
    fixture_dir = Path(__file__).resolve().parent
    repo_root = fixture_dir.parents[3]
    items = load(fixture_dir / "scenarios.json")
    expectations = load(fixture_dir / "expectations.json")
    scenarios = {item["id"]: item for item in items}
    require(len(scenarios) == len(items), "duplicate effect scenario id")
    require(set(scenarios) == set(expectations), "scenario/expectation id parity failed")

    for identity, expected in expectations.items():
        assert_expected(identity, evaluate(scenarios[identity]), expected)

    mutation_specs: list[tuple[str, str, Callable[[dict[str, Any]], None], dict[str, Any]]] = []
    for field in AUTHORITY_FIELDS:
        mutation_specs.append(
            (
                "observed",
                f"authority.{field}",
                lambda item, field=field: item["authority"].__setitem__(field, False),
                {"terminal_outcome": "failed", "invoke_count": 0},
            )
        )
    mutation_specs.extend(
        (
            (
                "observed",
                "post_read",
                lambda item: item.__setitem__("post_read", "unavailable"),
                {"terminal_outcome": "ambiguous"},
            ),
            (
                "observed",
                "repository identity",
                lambda item: item["authority"].__setitem__("repository_id", "forge:repository:other"),
                {"terminal_outcome": "failed", "invoke_count": 0},
            ),
            (
                "observed",
                "preconditions",
                lambda item: item.__setitem__("preconditions_match", False),
                {"terminal_outcome": "failed", "invoke_count": 0},
            ),
            (
                "observed",
                "terminal receipt readback",
                lambda item: item.__setitem__("terminal_receipt_read_back", False),
                {"terminal_outcome": "ambiguous", "persistence_claim": False},
            ),
            (
                "already-satisfied",
                "already-satisfied terminal receipt readback",
                lambda item: item.__setitem__("terminal_receipt_read_back", False),
                {"terminal_outcome": "ambiguous", "persistence_claim": False},
            ),
            (
                "observed",
                "initial operation identity",
                lambda item: item.pop("operation_id"),
                {"terminal_outcome": "failed", "invoke_count": 0, "identity_valid": False},
            ),
            (
                "observed",
                "initial repository identity",
                lambda item: item.pop("repository_id"),
                {"terminal_outcome": "failed", "invoke_count": 0, "identity_valid": False},
            ),
            (
                "ambiguous-dependent-work",
                "duplicate completion item",
                lambda item: item["affected_by_ambiguity"].append(item["affected_by_ambiguity"][0]),
                {"disjoint_exhaustive": False, "whole_run_completion": "withheld"},
            ),
            (
                "report-first-caller-completion",
                "assignment persistence readback",
                lambda item: item.__setitem__("assignment_persistence_read_back", False),
                {"assignment_persisted_decisions": 0, "decisions_carried_for_caller": 2, "decision_partition_exact": True, "assignment_persistence_proven": False, "caller_only_allocation_valid": True},
            ),
            (
                "report-first-caller-completion",
                "assignment persistence authorization",
                lambda item: item.__setitem__("assignment_persistence_authorized", False),
                {"assignment_persisted_decisions": 0, "decisions_carried_for_caller": 2, "decision_partition_exact": True, "assignment_persistence_proven": False, "caller_only_allocation_valid": True},
            ),
            (
                "proven-absence-retry",
                "operation identity",
                lambda item: item.__setitem__("retry_operation_id", "operation:report:replacement"),
                {"retry_allowed": False, "operation_identity_reused": False, "invoke_count": 0},
            ),
            (
                "proven-absence-retry",
                "retry repository identity",
                lambda item: item.__setitem__("retry_repository_id", "forge:repository:other"),
                {"retry_allowed": False, "operation_identity_reused": False, "invoke_count": 0},
            ),
            (
                "proven-absence-retry",
                "retry authority repository identity",
                lambda item: item["authority"].__setitem__("repository_id", "forge:repository:other"),
                {"retry_allowed": False, "invoke_count": 0},
            ),
            (
                "cross-repository-collision",
                "cross-repository qualification",
                lambda item: item.__setitem__("existing_repository_id", item["repository_id"]),
                {"terminal_outcome": "already satisfied"},
            ),
            (
                "cross-repository-collision",
                "collision desired-state post-read",
                lambda item: (item.__setitem__("existing_repository_id", item["repository_id"]), item.__setitem__("post_read", "unavailable")),
                {"terminal_outcome": "ambiguous"},
            ),
            (
                "cross-repository-collision",
                "collision terminal receipt readback",
                lambda item: (item.__setitem__("existing_repository_id", item["repository_id"]), item.__setitem__("terminal_receipt_read_back", False)),
                {"terminal_outcome": "ambiguous"},
            ),
            (
                "cross-repository-collision",
                "requested identity preservation",
                lambda item: item["result_operation_identity"].__setitem__(
                    "operation_id", "operation:report:replacement"
                ),
                {"operation_identity_preserved": False},
            ),
            (
                "cross-repository-collision",
                "replacement identity minting",
                lambda item: item.__setitem__(
                    "minted_replacement_identity",
                    {
                        "repository_id": item["repository_id"],
                        "operation_id": "operation:report:replacement",
                    },
                ),
                {"replacement_identity_minted": True},
            ),
            (
                "proven-absence-retry",
                "wrapper precondition",
                lambda item: item.__setitem__("wrapper_scope_unchanged", False),
                {"retry_allowed": False, "invoke_count": 0},
            ),
            (
                "one-valid-receipt-ahead",
                "repair integrity authority",
                lambda item: item.__setitem__("complete_integrity_read", False),
                {"repair_allowed": False, "invoke_count": 0, "terminal_outcome": "ambiguous"},
            ),
            (
                "one-valid-receipt-ahead",
                "repair authority repository identity",
                lambda item: item["authority"].__setitem__("repository_id", "forge:repository:other"),
                {"repair_allowed": False, "invoke_count": 0, "terminal_outcome": "ambiguous"},
            ),
        )
    )
    for identity, label, mutate, expected_result in mutation_specs:
        assert_mutation_result(scenarios, identity, label, mutate, expected_result)

    missing_fingerprint = copy.deepcopy(scenarios["already-satisfied"])
    missing_fingerprint.pop("existing_effect_fingerprint")
    assert_expected(
        "already-satisfied missing compatibility fingerprint",
        evaluate(missing_fingerprint),
        {"terminal_outcome": "ambiguous", "invoke_count": 0, "persistence_claim": False},
    )

    incompatible_payload = copy.deepcopy(scenarios["already-satisfied"])
    incompatible_payload["existing_effect_payload"]["verb"] = "append-comment"
    assert_expected(
        "already-satisfied incompatible payload",
        evaluate(incompatible_payload),
        {"terminal_outcome": "failed", "invoke_count": 0, "persistence_claim": False},
    )

    incompatible_collision = copy.deepcopy(scenarios["cross-repository-collision"])
    incompatible_collision["existing_repository_id"] = incompatible_collision["repository_id"]
    incompatible_collision["existing_effect_fingerprint"] = "f" * 64
    assert_expected(
        "same-identity incompatible collision",
        evaluate(incompatible_collision),
        {"terminal_outcome": "failed", "invoke_count": 0},
    )

    uncertain_compatibility = copy.deepcopy(scenarios["uncertain-deduplication"])
    uncertain_compatibility.update(
        {
            "invoke_result": "accepted",
            "post_read": "exact effect observed",
            "terminal_receipt_read_back": True,
        }
    )
    assert_expected(
        "uncertain compatibility with apparent success",
        evaluate(uncertain_compatibility),
        {"terminal_outcome": "ambiguous", "invoke_count": 0, "persistence_claim": False},
    )

    invalid_repair_identity = copy.deepcopy(scenarios["one-valid-receipt-ahead"])
    invalid_repair_identity["operation_id"] = []
    try:
        evaluate(invalid_repair_identity)
        raise ContractError("invalid repair operation identity survived")
    except ContractError as error:
        require("operation_id" in str(error), "invalid repair operation identity failed for the wrong reason")

    malformed_partition = copy.deepcopy(scenarios["ambiguous-dependent-work"])
    malformed_partition["affected_by_ambiguity"].append([])
    try:
        evaluate(malformed_partition)
        raise ContractError("unhashable completion identity survived")
    except ContractError as error:
        require("unhashable" in str(error), "TypeError did not produce stable FAIL output")

    duplicate_decision = copy.deepcopy(scenarios["report-first-caller-completion"])
    duplicate_decision["assignment_persisted_decision_ids"].append("decision:follow-up:a")
    try:
        evaluate(duplicate_decision)
        raise ContractError("duplicate assignment decision survived")
    except ContractError as error:
        require("duplicate assignment-persisted decision" in str(error), "duplicate decision mutation failed for the wrong reason")

    validate_sources(repo_root)
    print("PASS: Release A report-effect outcomes derive from scenario facts")
    print(f"PASS: {len(mutation_specs) + 5} load-bearing authority, readback, identity, compatibility, partition, and precondition mutations rejected")
    print("NOTE: fresh-context matched cases own behavioral evidence")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ContractError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
