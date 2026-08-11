#!/usr/bin/env python3
"""Evaluate Release A reconciliation facts and mutation-test the decision gates."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parents[4]
CONTRACT_PATH = REPO_ROOT / "skills" / "repo-gardener" / "scripts" / "release_a_contract.py"
POLICY_PATH = REPO_ROOT / "skills" / "repo-gardener" / "assets" / "policy-template.yaml"
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("repo_gardener_release_a_contract", CONTRACT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load production contract: {CONTRACT_PATH}")
CONTRACT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTRACT)
ContractError = CONTRACT.ContractError
require = CONTRACT.require


def load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def scenario_map(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        identity = item.get("id")
        require(isinstance(identity, str) and identity, "scenario id must be nonempty")
        require(identity not in result, f"duplicate scenario id: {identity}")
        result[identity] = item
    return result


def validate_register(fixture_dir: Path) -> dict[str, Any]:
    register_dir = fixture_dir.parent / "register"
    records = load(register_dir / "canonical-records.json")
    manifest = load(register_dir / "manifest.json")
    expected = load(register_dir / "expectations.json")
    authentication = load(register_dir / "provider-authentication.json")
    result = CONTRACT.validate_register(records, manifest, authentication, POLICY_PATH)
    require(len(records["rows"]) == expected["expected_row_count"], "row count mismatch")
    anchor = records["history_anchor"]
    require(anchor["sequence"] == expected["expected_history_sequence"], "history sequence mismatch")
    require(result["history_head"] == anchor["head"], "history head mismatch")
    require(manifest["manifest_id"] == expected["expected_manifest_id"], "manifest identity mismatch")
    require(len(manifest["scouts"]) == expected["expected_scout_count"], "manifest scout count mismatch")
    return manifest


def validate_receipts_data(data: dict[str, Any], manifest: dict[str, Any], label: str, complete: bool = True) -> dict[str, dict[str, Any]]:
    try:
        return CONTRACT.validate_scout_receipts(data, manifest, complete=complete)
    except ContractError as error:
        raise ContractError(f"{label}: {error}") from error


def read_receipt_fixture(fixture_dir: Path, manifest: dict[str, Any], filename: str) -> dict[str, dict[str, Any]]:
    return validate_receipts_data(load(fixture_dir / filename), manifest, filename, complete=filename != "lane-receipts-missing.json")


def evaluate(
    scenario: dict[str, Any],
    fixture_dir: Path,
    manifest: dict[str, Any],
    complete_receipts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    receipt_sets = {
        filename: read_receipt_fixture(fixture_dir, manifest, filename)
        for filename in (
            "lane-receipts.json",
            "lane-receipts-incomplete.json",
            "lane-receipts-missing.json",
        )
    }
    return CONTRACT.evaluate_reconciliation(
        scenario, manifest, receipt_sets, complete_receipts, POLICY_PATH
    )


def assert_expected(identity: str, actual: dict[str, Any], expected: dict[str, Any]) -> None:
    for key, value in expected.items():
        require(actual.get(key) == value, f"{identity} derived {key}={actual.get(key)!r}, expected {value!r}")


def assert_mutation_result(
    scenarios: dict[str, dict[str, Any]],
    identity: str,
    label: str,
    mutate: Callable[[dict[str, Any]], None],
    expected_result: dict[str, Any],
    fixture_dir: Path,
    manifest: dict[str, Any],
    receipts: dict[str, dict[str, Any]],
) -> None:
    baseline = evaluate(scenarios[identity], fixture_dir, manifest, receipts)
    changed = copy.deepcopy(scenarios[identity])
    mutate(changed)
    actual = evaluate(changed, fixture_dir, manifest, receipts)
    require(
        any(baseline.get(key) != value for key, value in expected_result.items()),
        f"mutation target does not differ from baseline: {label}",
    )
    assert_expected(f"{identity} mutation {label}", actual, expected_result)


def validate_sources(repo_root: Path) -> None:
    skill_dir = repo_root / "skills" / "repo-gardener"
    case_dir = repo_root / "tests" / "repo-gardener" / "cases"
    policy = (skill_dir / "assets" / "policy-template.yaml").read_text(encoding="utf-8")
    reconcile = (skill_dir / "references" / "reconciliation.md").read_text(encoding="utf-8")
    register = (skill_dir / "references" / "register-and-report.md").read_text(encoding="utf-8")
    core = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    reconcile_words = " ".join(reconcile.split()).lower()
    register_words = " ".join(register.split())
    core_words = " ".join(core.split())
    mutations = re.findall(r"^\s+mutation: (true|false)$", policy, re.MULTILINE)
    require(len(mutations) == 9 and set(mutations) == {"false"}, "policy must contain nine false lane mutations")
    for phrase in (
        "reconcile every Current Portfolio row and every unmatched intended-effect receipt",
        "Even when a safe stop prevents those operations",
        "after the missing proof is restored, append exactly one",
        "must not replace valid-path reconciliation",
        "Persist and read it back before dispatch",
        "one numbered list in its supplied stable order",
        "incomplete (no receipt)",
        "State that exception whenever coverage is incomplete",
        "Apply and render all six gates in this exact order",
        "Ephemeral recommendation eligibility does not require lane mutation authority",
        "own named specialist",
        "through the narrow report wrapper",
        "separate seven-slot projection",
        "it remains eligible while lane mutation is disabled",
        "grants no effect authority",
        "creates no portfolio state",
        "For every candidate and independent subcase, render all six named gate results",
        "no source claim, queue, edit, merge, or provider-maintenance effect occurred",
        "Stored `writer_id`, anchor, sequence, or hash fields are register data",
        "multiple runs or coverage variants",
        "stable source identity is used only as the final tie-break",
        "disabled-lane observations as separate from the compared runs",
        "then render each ephemeral recommendation in a free slot",
        "Render exactly that many numbered slots",
        "append exactly one terminal run receipt and read it back",
        "Render the canonical report and read it back last",
        "repository_portfolio_limit` exactly once",
        "generic terminal fact with no such binding",
        "outside recommendation eligibility",
    ):
        require(phrase.lower() in reconcile_words, f"reconciliation contract missing: {phrase}")
    case_texts = [path.read_text(encoding="utf-8") for path in sorted(case_dir.glob("*.md"))]
    rubric_items = sum(text.count("- [ ] ") for text in case_texts)
    require(rubric_items == 48, f"behavioral rubric count drifted: {rubric_items}")
    selection_case = (case_dir / "seven-slot-dry-run-selection.md").read_text(encoding="utf-8")
    require(
        "remain eligible with lane mutation disabled" in selection_case
        and "grant no effect authority or portfolio state" in selection_case,
        "seven-slot rubric lost the Release A recommendation-authority criterion",
    )
    require(
        "State whether each recommendation remains" in selection_case
        and "eligible when lane mutation is disabled" in selection_case,
        "seven-slot prompt does not request the recommendation-eligibility fact",
    )
    require(
        "final tie-break" in selection_case and "master score" in selection_case,
        "seven-slot prompt does not request comparison invariants",
    )
    no_op_case = (case_dir / "honest-no-op-and-disabled-lanes.md").read_text(encoding="utf-8")
    require(
        "separate, fully numbered seven-slot projection" in no_op_case
        and "for each run" in no_op_case,
        "no-op prompt does not request both complete slot projections",
    )
    require(
        "reconciliation_complete: true" in no_op_case
        and "outside both run completions" in no_op_case,
        "no-op prompt does not isolate run completion from separate observations",
    )
    reconcile_case = (case_dir / "reconcile-before-rediscovery.md").read_text(encoding="utf-8")
    require(
        "fields alone as authentication" in reconcile_case,
        "reconciliation prompt does not distinguish stored identity data from proof",
    )
    require("generic fact is not attached to either named row" in reconcile_case, "terminal-row rubric permits an invented row association")
    caller_case = (case_dir / "caller-lifecycle-and-local-blockers.md").read_text(encoding="utf-8")
    require("assigns each decision exactly once" in caller_case, "caller lifecycle rubric lost shared persistence ownership")
    normalization_case = (case_dir / "normalization-and-safety-gates.md").read_text(encoding="utf-8")
    require("source-mutation capability remains unavailable and is not required" in " ".join(normalization_case.replace(">", " ").split()), "capability rubric requires source-mutation authority")
    require("exactly one manifest persistence operation" in reconcile_words, "manifest persistence ordering is not single-operation")
    require("scripts/release_a_contract.py" in core_words, "core does not invoke the executable contract")
    require("Row creation, reservation, and replacement are unavailable in Release A." in register_words, "Release A row-creation exclusion is missing")
    require("reserve or replace exactly one row" not in register_words, "row reservation primitive leaked into Release A")
    for phrase in ("zero to seven rows", "not an atomic transaction or distributed lock", "exactly one valid receipt ahead", "Multiple gaps", "incomplete (no receipt)"):
        require(phrase in register_words, f"register contract missing: {phrase}")
    for phrase in ("report-register write is its only possible effect", "one disjoint, exhaustive partition", "one-shot terminal-report capability"):
        require(phrase in core_words, f"core contract missing: {phrase}")
    forbidden_phrases = ("Release " + "B", "adopt" + "-only", "proposal_issue" + "_authoring", "dependency-and-vulnerability" + ".authoring")
    for path in skill_dir.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".yaml", ".py"}:
            text = path.read_text(encoding="utf-8")
            for forbidden in forbidden_phrases:
                require(forbidden not in text, f"later behavior leaked into Release A: {forbidden}")


def main() -> int:
    fixture_dir = Path(__file__).resolve().parent
    repo_root = fixture_dir.parents[3]
    manifest = validate_register(fixture_dir)
    complete_data = load(fixture_dir / "lane-receipts.json")
    complete_receipts = validate_receipts_data(complete_data, manifest, "lane-receipts.json")
    incomplete_data = load(fixture_dir / "lane-receipts-incomplete.json")
    incomplete_receipts = validate_receipts_data(incomplete_data, manifest, "lane-receipts-incomplete.json")
    require(incomplete_receipts["runtime-error-and-alert"]["outcome"] == "incomplete", "incomplete fixture does not exercise failure coverage")
    missing_data = load(fixture_dir / "lane-receipts-missing.json")
    validate_receipts_data(missing_data, manifest, "lane-receipts-missing.json", complete=False)

    scenario_items = load(fixture_dir / "scenarios.json")
    for item in scenario_items:
        if item.get("stub_fixture"):
            stub = load(fixture_dir / item["stub_fixture"])
            require(stub.get("schema") == "repo-gardener-test-wrapper-readbacks/v1", "wrapper readback stub schema mismatch")
            item["report_facts"] = stub["report_facts"]
    scenarios = scenario_map(scenario_items)
    expectations = load(fixture_dir / "expectations.json")
    require(set(scenarios) == set(expectations), "scenario/expectation id parity failed")
    for identity, expected in expectations.items():
        assert_expected(identity, evaluate(scenarios[identity], fixture_dir, manifest, complete_receipts), expected)

    mutations: list[tuple[str, str, Callable[[dict[str, Any]], None], dict[str, Any]]] = [
        (
            "losing-caller",
            "caller ownership",
            lambda item: item.__setitem__("exclusive_executor", True),
            {"writes": 1, "last_safe_stage": "Act"},
        ),
        (
            "ordered-gates-protected-projection",
            "policy gate",
            lambda item: item["gate_facts"].__setitem__("policy and authority", True),
            {"first_failing_gate": "protected boundary"},
        ),
        (
            "honest-no-op",
            "receipt coverage",
            lambda item: item.__setitem__("receipt_fixture", "lane-receipts-missing.json"),
            {"attention_state": "Action required", "next_owner_action": "complete missing coverage"},
        ),
        (
            "full-capacity",
            "capacity",
            lambda item: item["retained_rows"].pop(),
            {"recommendations": 1},
        ),
        (
            "report-first-sequence",
            "ordering",
            lambda item: item["events"].__setitem__(3, "read-run-start"),
            {"ordered": False, "readback_after_each_write": False},
        ),
        (
            "completed-narrow-wrapper-readbacks",
            "completed report-fact readback",
            lambda item: item["report_facts"][2].__setitem__("authoritative_readback_completed", False),
            {
                "persistence_claim": True,
                "persisted_report_facts": [
                    "run-start",
                    "manifest",
                    "reconciliation",
                    "decisions",
                    "terminal run",
                    "canonical report",
                ],
                "source_fact_persistence_claim": False,
            },
        ),
        (
            "terminal-row",
            "terminal source binding",
            lambda item: item.__setitem__("terminal_source_binding", True),
            {"row_action": "release-or-owner-release", "allowed_results": ["released-same-update", "action-required-owner-release"]},
        ),
    ]
    for identity, label, mutate, expected_result in mutations:
        assert_mutation_result(
            scenarios,
            identity,
            label,
            mutate,
            expected_result,
            fixture_dir,
            manifest,
            complete_receipts,
        )

    capability_baseline = copy.deepcopy(scenarios["shared-dependency-security-complete"])
    capability_baseline["source_mutation_capability_available"] = False
    capability_variant = copy.deepcopy(capability_baseline)
    capability_variant["source_mutation_capability_available"] = True
    require(
        evaluate(capability_baseline, fixture_dir, manifest, complete_receipts)
        == evaluate(capability_variant, fixture_dir, manifest, complete_receipts),
        "source-mutation capability changed read-only recommendation eligibility",
    )

    duplicate_scout = copy.deepcopy(complete_data)
    duplicate_scout["receipts"][1]["scout_id"] = duplicate_scout["receipts"][0]["scout_id"]
    try:
        validate_receipts_data(duplicate_scout, manifest, "duplicate-scout")
        raise ContractError("duplicate scout identity mutation survived")
    except ContractError as error:
        require("duplicate" in str(error) or "order/coverage" in str(error), "duplicate scout mutation failed for the wrong reason")
    incomplete_without_reason = copy.deepcopy(incomplete_data)
    next(item for item in incomplete_without_reason["receipts"] if item["outcome"] == "incomplete").pop("failure_reason", None)
    try:
        validate_receipts_data(incomplete_without_reason, manifest, "incomplete-without-reason")
        raise ContractError("incomplete receipt without reason mutation survived")
    except ContractError as error:
        require("failure reason" in str(error), "incomplete-reason mutation failed for the wrong reason")
    unknown_receipt = copy.deepcopy(scenarios["stable-identity-dedupe"])
    unknown_receipt["observations"][0]["receipt_id"] = "receipt:scout:unknown"
    try:
        evaluate(unknown_receipt, fixture_dir, manifest, complete_receipts)
        raise ContractError("unknown dedupe receipt mutation survived")
    except ContractError as error:
        require("unknown Scout Receipt" in str(error), "unknown receipt mutation failed for the wrong reason")

    scout_schema_fields = (
        "run_id",
        "manifest_id",
        "lane",
        "observed_at",
        "source_id",
        "evidence_references",
        "candidate_count",
    )
    for field in scout_schema_fields:
        malformed = copy.deepcopy(complete_data)
        malformed["receipts"][0].pop(field)
        try:
            validate_receipts_data(malformed, manifest, f"missing-{field}")
            raise ContractError(f"Scout Receipt without {field} survived")
        except ContractError as error:
            require(field in str(error) or field.replace("_", " ") in str(error), f"Scout Receipt {field} mutation failed for the wrong reason")

    register_dir = fixture_dir.parent / "register"
    records = load(register_dir / "canonical-records.json")
    authentication = load(register_dir / "provider-authentication.json")
    broken_chain = copy.deepcopy(records)
    broken_chain["history_receipts"][3]["previous_hash"] = "f" * 64
    try:
        CONTRACT.validate_register(broken_chain, manifest, authentication, POLICY_PATH)
        raise ContractError("broken prior hash survived")
    except ContractError as error:
        require("previous hash mismatch" in str(error), "broken prior hash mutation failed for the wrong reason")

    unauthenticated = copy.deepcopy(authentication)
    unauthenticated["authenticated_receipts"][4]["writer_id"] = "forge:writer:other"
    try:
        CONTRACT.validate_register(records, manifest, unauthenticated, POLICY_PATH)
        raise ContractError("unauthenticated receipt writer survived")
    except ContractError as error:
        require("provider-authenticated" in str(error), "writer authentication mutation failed for the wrong reason")

    oversized_identity = copy.deepcopy(records)
    oversized_identity["repository_id"] = "r" * (CONTRACT.IDENTITY_LIMIT + 1)
    try:
        CONTRACT.validate_register(oversized_identity, manifest, authentication, POLICY_PATH)
        raise ContractError("oversized identity survived")
    except ContractError as error:
        require("exceeds 128" in str(error), "identity-size mutation failed for the wrong reason")

    oversized_display = copy.deepcopy(records)
    oversized_display["rows"][0]["description"] = "x" * (CONTRACT.DISPLAY_LIMIT + 1)
    try:
        CONTRACT.validate_register(oversized_display, manifest, authentication, POLICY_PATH)
        raise ContractError("oversized display survived")
    except ContractError as error:
        require("exceeds 512" in str(error), "display-size mutation failed for the wrong reason")

    oversized_receipt = copy.deepcopy(records)
    oversized_receipt["history_receipts"][0]["padding"] = "x" * CONTRACT.RECEIPT_LIMIT
    try:
        CONTRACT.validate_register(oversized_receipt, manifest, authentication, POLICY_PATH)
        raise ContractError("oversized receipt survived")
    except ContractError as error:
        require("canonical UTF-8 bytes" in str(error), "receipt-size mutation failed for the wrong reason")

    try:
        CONTRACT.validate_body("x" * (CONTRACT.BODY_LIMIT + 1))
        raise ContractError("oversized body survived")
    except ContractError as error:
        require("managed body exceeds" in str(error), "body-size mutation failed for the wrong reason")

    validate_sources(repo_root)
    print("PASS: Release A reconciliation outcomes derive from caller, gate, receipt, capacity, and ordering facts")
    print(f"PASS: {len(mutations) + 17} reconciliation, history, schema, bound, and receipt mutations rejected")
    print("NOTE: fresh-context matched cases own behavioral evidence")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ContractError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
