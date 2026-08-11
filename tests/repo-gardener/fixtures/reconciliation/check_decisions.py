#!/usr/bin/env python3
"""Evaluate Release A reconciliation facts and mutation-test the decision gates."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
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


def invoke_cli(command: str, payload: dict[str, Any], *, policy: bool = False) -> dict[str, Any]:
    arguments = [sys.executable, str(CONTRACT_PATH), command, "--input", "-"]
    if policy:
        arguments.extend(["--policy", str(POLICY_PATH)])
    completed = subprocess.run(
        arguments,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise ContractError(completed.stderr.strip().removeprefix("FAIL: "))
    return json.loads(completed.stdout)


def reconciliation_payload(
    scenario: dict[str, Any],
    manifest: dict[str, Any],
    receipt_sets: dict[str, dict[str, Any]],
    complete_receipts: dict[str, Any],
) -> dict[str, Any]:
    register_dir = Path(__file__).resolve().parent.parent / "register"
    return {
        "schema": "repo-gardener-reconciliation-input/v1",
        "scenario": scenario,
        "register": load(register_dir / "canonical-records.json"),
        "authentication": load(register_dir / "provider-authentication.json"),
        "manifest": manifest,
        "receipt_sets": receipt_sets,
        "complete_receipts": complete_receipts,
    }


def evaluate(
    scenario: dict[str, Any],
    manifest: dict[str, Any],
    receipt_sets: dict[str, dict[str, Any]],
    complete_receipts: dict[str, Any],
) -> dict[str, Any]:
    return invoke_cli(
        "reconciliation-v1",
        reconciliation_payload(scenario, manifest, receipt_sets, complete_receipts),
        policy=True,
    )


def assert_expected(identity: str, actual: dict[str, Any], expected: dict[str, Any]) -> None:
    for key, value in expected.items():
        require(actual.get(key) == value, f"{identity} derived {key}={actual.get(key)!r}, expected {value!r}")


def require_contract_error(label: str, expected_text: str, action: Callable[[], Any]) -> None:
    try:
        action()
    except ContractError as error:
        require(expected_text in str(error), f"{label} mutation failed for the wrong reason: {error}")
        return
    raise ContractError(f"{label} mutation survived")


def require_receipt_cli_contract_error(
    label: str,
    expected_text: str,
    receipts: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    with tempfile.TemporaryDirectory(prefix="repo-gardener-receipts-") as temp:
        receipt_path = Path(temp) / "receipts.json"
        manifest_path = Path(temp) / "manifest.json"
        receipt_path.write_text(json.dumps(receipts), encoding="utf-8")
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                str(CONTRACT_PATH),
                "validate-scout-receipts",
                "--receipts",
                str(receipt_path),
                "--manifest",
                str(manifest_path),
            ],
            capture_output=True,
            text=True,
        )
    require(completed.returncode == 1, f"{label} mutation did not fail with the contract exit code")
    require(completed.stderr.startswith("FAIL: "), f"{label} mutation did not fail as ContractError")
    require(expected_text in completed.stderr, f"{label} mutation failed for the wrong reason: {completed.stderr.strip()}")


def rehash_history(records: dict[str, Any]) -> None:
    previous_hash = "0" * 64
    for receipt in records["history_receipts"]:
        receipt["previous_hash"] = previous_hash
        receipt["receipt_hash"] = CONTRACT.receipt_hash(receipt)
        previous_hash = receipt["receipt_hash"]
    records["history_anchor"]["head"] = previous_hash
    records["history_anchor"]["latest_receipt"] = copy.deepcopy(records["history_receipts"][-1])


def assert_mutation_result(
    scenarios: dict[str, dict[str, Any]],
    identity: str,
    label: str,
    mutate: Callable[[dict[str, Any]], None],
    expected_result: dict[str, Any],
    manifest: dict[str, Any],
    receipt_sets: dict[str, dict[str, Any]],
    receipts: dict[str, Any],
) -> None:
    baseline = evaluate(scenarios[identity], manifest, receipt_sets, receipts)
    changed = copy.deepcopy(scenarios[identity])
    mutate(changed)
    actual = evaluate(changed, manifest, receipt_sets, receipts)
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
    effects = (skill_dir / "references" / "applying-effects.md").read_text(encoding="utf-8")
    register = (skill_dir / "references" / "register-and-report.md").read_text(encoding="utf-8")
    core = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    reconcile_words = " ".join(reconcile.split()).lower()
    effects_words = " ".join(effects.split()).lower()
    register_words = " ".join(register.split())
    core_words = " ".join(core.split())
    mutations = re.findall(r"^\s+mutation: (true|false)$", policy, re.MULTILINE)
    require(len(mutations) == 9 and set(mutations) == {"false"}, "policy must contain nine false lane mutations")
    for phrase in (
        "reconcile every Current Portfolio row and every unmatched report intent",
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
        "Persist and read back all supplied Scout Receipts before appending decisions",
        "Render the canonical report and read it back last",
        "repository_portfolio_limit` exactly once",
        "generic terminal fact with no such binding",
        "every reconciliation response states both terminal-row branches",
        "stable terminal-source binding",
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
    require(
        "separate provider-authenticated identity and hash-chain continuity proof results" in reconcile_case,
        "reconciliation rubric does not require separate identity and continuity proof results",
    )
    require(
        "effect_reconciled: true" in reconcile_case
        and "idempotently recorded as an `observed` effect disposition" in reconcile_case,
        "reconciliation rubric does not require the observed reconciled-effect disposition",
    )
    require(
        "Every reconciliation response states the general rule" in reconcile_case
        and "generic unbound fact remains unattached" in reconcile_case,
        "terminal-row rubric does not require both the bound rule and unbound disposition",
    )
    require(
        "effect_reconciled: true" in effects_words
        and "terminal_outcome: observed" in effects_words
        and "idempotently" in effects_words,
        "effect recovery contract does not map reconciled effects to an idempotent observed disposition",
    )
    caller_case = (case_dir / "caller-lifecycle-and-local-blockers.md").read_text(encoding="utf-8")
    require(
        "does not turn a possible persistence path into proof" in caller_case
        and "carrying both for caller persistence is valid" in caller_case,
        "caller lifecycle rubric lost proof-bound caller persistence ownership",
    )
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
    complete_receipt_map = validate_receipts_data(complete_data, manifest, "lane-receipts.json")
    incomplete_data = load(fixture_dir / "lane-receipts-incomplete.json")
    incomplete_receipt_map = validate_receipts_data(incomplete_data, manifest, "lane-receipts-incomplete.json")
    require(incomplete_receipt_map["runtime-error-and-alert"]["outcome"] == "incomplete", "incomplete fixture does not exercise failure coverage")
    missing_data = load(fixture_dir / "lane-receipts-missing.json")
    validate_receipts_data(missing_data, manifest, "lane-receipts-missing.json", complete=False)
    receipt_sets = {
        "lane-receipts.json": complete_data,
        "lane-receipts-incomplete.json": incomplete_data,
        "lane-receipts-missing.json": missing_data,
    }

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
        assert_expected(identity, evaluate(scenarios[identity], manifest, receipt_sets, complete_data), expected)

    gate_scenario = scenarios["ordered-gates-protected-projection"]
    gate_result = invoke_cli(
        "gates-v1",
        {"schema": "repo-gardener-gates-input/v1", "facts": gate_scenario["gate_facts"]},
    )
    require(gate_result["first_failing_gate"] == "policy and authority", "gates-v1 did not expose ordered gate derivation")

    capacity_scenario = scenarios["full-capacity"]
    capacity_result = invoke_cli(
        "capacity-v1",
        {
            "schema": "repo-gardener-capacity-input/v1",
            "retained": capacity_scenario["retained_rows"],
            "candidates": capacity_scenario["eligible_candidates"],
        },
        policy=True,
    )
    require(capacity_result["recommendations"] == 0, "capacity-v1 did not expose policy-derived capacity")

    mutations: list[tuple[str, str, Callable[[dict[str, Any]], None], dict[str, Any]]] = [
        (
            "losing-caller",
            "caller ownership",
            lambda item: item["authority"].__setitem__("exclusive_executor", True),
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
            "honest-no-op",
            "protected boundary rejection",
            lambda item: item.__setitem__("protected_boundary_rejected", True),
            {"attention_state": "Action required", "next_owner_action": "resolve protected boundary"},
        ),
        (
            "honest-no-op",
            "incomplete reconciliation",
            lambda item: item.__setitem__("reconciliation_complete", False),
            {"attention_state": "Action required", "next_owner_action": "complete reconciliation"},
        ),
        (
            "honest-no-op",
            "gate-passing candidates",
            lambda item: item.__setitem__("gate_passing_candidates", 1),
            {"attention_state": "Action required", "next_owner_action": "review gate-passing candidates"},
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
            lambda item: item.update(
                {
                    "current_row": {"row_id": "row:ci:beta", "source_id": "forge:check:beta", "source_revision": "revision:beta:1"},
                    "terminal_source_binding": {"row_id": "row:ci:beta", "source_id": "forge:check:beta", "source_revision": "revision:beta:1"},
                }
            ),
            {"row_action": "release-or-owner-release", "stable_binding_dispositions": ["released-same-update", "action-required-owner-release"]},
        ),
        (
            "unmatched-effect-before-discovery",
            "reconciled effect disposition",
            lambda item: item.__setitem__("effect_reconciled", False),
            {"ordering_valid": False, "terminal_outcome": "ambiguous", "terminal_receipt_recording": "withheld"},
        ),
        (
            "unmatched-effect-before-discovery",
            "zero unmatched intents",
            lambda item: item.__setitem__("unmatched_intents", 0),
            {"ordering_valid": False, "terminal_outcome": "ambiguous", "terminal_receipt_recording": "withheld"},
        ),
        (
            "unmatched-effect-before-discovery",
            "multiple unmatched intents",
            lambda item: item.__setitem__("unmatched_intents", 2),
            {"ordering_valid": False, "terminal_outcome": "ambiguous", "terminal_receipt_recording": "withheld"},
        ),
    ]
    for identity, label, mutate, expected_result in mutations:
        assert_mutation_result(
            scenarios,
            identity,
            label,
            mutate,
            expected_result,
            manifest,
            receipt_sets,
            complete_data,
        )

    capability_baseline = copy.deepcopy(scenarios["shared-dependency-security-complete"])
    capability_baseline["source_mutation_capability_available"] = False
    capability_variant = copy.deepcopy(capability_baseline)
    capability_variant["source_mutation_capability_available"] = True
    require(
        evaluate(capability_baseline, manifest, receipt_sets, complete_data)
        == evaluate(capability_variant, manifest, receipt_sets, complete_data),
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
        require(
            "failure reason" in str(error) or "failure_reason" in str(error),
            "incomplete-reason mutation failed for the wrong reason",
        )
    unknown_receipt = copy.deepcopy(scenarios["stable-identity-dedupe"])
    unknown_receipt["observations"][0]["receipt_id"] = "receipt:scout:unknown"
    try:
        evaluate(unknown_receipt, manifest, receipt_sets, complete_data)
        raise ContractError("unknown dedupe receipt mutation survived")
    except ContractError as error:
        require("unknown Scout Receipt" in str(error), "unknown receipt mutation failed for the wrong reason")

    missing_dedupe_identity = copy.deepcopy(scenarios["stable-identity-dedupe"])
    missing_dedupe_identity["observations"][0].pop("source_id")
    require_contract_error(
        "missing dedupe source identity",
        "dedupe observation 0 source_id",
        lambda: evaluate(missing_dedupe_identity, manifest, receipt_sets, complete_data),
    )
    unhashable_dedupe_identity = copy.deepcopy(scenarios["stable-identity-dedupe"])
    unhashable_dedupe_identity["observations"][0]["source_id"] = []
    require_contract_error(
        "unhashable dedupe source identity",
        "dedupe observation 0 source_id",
        lambda: evaluate(unhashable_dedupe_identity, manifest, receipt_sets, complete_data),
    )

    wrong_disabled_count = copy.deepcopy(scenarios["disabled-lane-observations"])
    wrong_disabled_count["observations"].pop()
    require_contract_error(
        "disabled observation count",
        "exactly two observations",
        lambda: evaluate(wrong_disabled_count, manifest, receipt_sets, complete_data),
    )
    malformed_disabled_observation = copy.deepcopy(scenarios["disabled-lane-observations"])
    malformed_disabled_observation["observations"][1] = []
    require_contract_error(
        "disabled observation object",
        "critical disabled observation must be an object",
        lambda: evaluate(malformed_disabled_observation, manifest, receipt_sets, complete_data),
    )

    missing_cli_key = copy.deepcopy(scenarios["missing-scout-receipt"])
    missing_cli_key.pop("receipt_fixture")
    require_contract_error(
        "CLI KeyError shape mismatch",
        "receipt_fixture",
        lambda: evaluate(missing_cli_key, manifest, receipt_sets, complete_data),
    )

    empty_manifest = copy.deepcopy(manifest)
    empty_manifest["scouts"] = []
    require_contract_error(
        "empty reconciliation manifest",
        "installed policy lane inventory",
        lambda: invoke_cli(
            "reconciliation-v1",
            reconciliation_payload(scenarios["honest-no-op"], empty_manifest, receipt_sets, complete_data),
            policy=True,
        ),
    )
    raw_receipt_map = copy.deepcopy(receipt_sets)
    raw_receipt_map["lane-receipts.json"] = complete_receipt_map
    require_contract_error(
        "raw reconciliation receipt map",
        "Scout Receipt collection schema mismatch",
        lambda: invoke_cli(
            "reconciliation-v1",
            reconciliation_payload(scenarios["honest-no-op"], manifest, raw_receipt_map, complete_data),
            policy=True,
        ),
    )
    incomplete_complete_envelope = copy.deepcopy(complete_data)
    incomplete_complete_envelope.pop("run_id")
    require_contract_error(
        "incomplete complete-receipts envelope",
        "Scout Receipt collection schema mismatch",
        lambda: invoke_cli(
            "reconciliation-v1",
            reconciliation_payload(scenarios["honest-no-op"], manifest, receipt_sets, incomplete_complete_envelope),
            policy=True,
        ),
    )
    foreign_run_receipts = copy.deepcopy(complete_data)
    foreign_run_receipts["run_id"] = "run:synthetic:other"
    require_contract_error(
        "foreign reconciliation run",
        "collection run mismatch",
        lambda: invoke_cli(
            "reconciliation-v1",
            reconciliation_payload(scenarios["honest-no-op"], manifest, receipt_sets, foreign_run_receipts),
            policy=True,
        ),
    )
    incomplete_authority = copy.deepcopy(scenarios["honest-no-op"])
    incomplete_authority["authority"].pop("runtime_scope_valid")
    require_contract_error(
        "incomplete reconciliation authority",
        "authority schema mismatch",
        lambda: evaluate(incomplete_authority, manifest, receipt_sets, complete_data),
    )

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

    malformed_collection = copy.deepcopy(complete_data)
    malformed_collection.pop("schema")
    require_contract_error(
        "Scout Receipt collection schema",
        "collection schema",
        lambda: validate_receipts_data(malformed_collection, manifest, "missing-collection-schema"),
    )
    cross_repository_collection = copy.deepcopy(complete_data)
    cross_repository_collection["repository_id"] = "forge:repository:other"
    require_contract_error(
        "Scout Receipt collection repository",
        "repository mismatch",
        lambda: validate_receipts_data(cross_repository_collection, manifest, "cross-repository-collection"),
    )
    wrong_manifest_schema = copy.deepcopy(manifest)
    wrong_manifest_schema["schema"] = "repo-gardener-scout-manifest/v999"
    require_contract_error(
        "Scout Receipt manifest schema",
        "manifest schema mismatch",
        lambda: validate_receipts_data(complete_data, wrong_manifest_schema, "wrong-manifest-schema"),
    )
    wrong_manifest_repository = copy.deepcopy(manifest)
    wrong_manifest_repository["repository_id"] = "forge:repository:other"
    require_contract_error(
        "Scout Receipt manifest repository",
        "repository mismatch",
        lambda: validate_receipts_data(complete_data, wrong_manifest_repository, "wrong-manifest-repository"),
    )
    invalid_time = copy.deepcopy(complete_data)
    invalid_time["receipts"][0]["observed_at"] = "not-a-time"
    require_contract_error(
        "Scout Receipt UTC observation time",
        "UTC observation time",
        lambda: validate_receipts_data(invalid_time, manifest, "invalid-observation-time"),
    )
    empty_evidence = copy.deepcopy(complete_data)
    empty_evidence["receipts"][0]["evidence_references"] = []
    require_contract_error(
        "complete Scout Receipt evidence",
        "requires evidence",
        lambda: validate_receipts_data(empty_evidence, manifest, "empty-complete-evidence"),
    )
    oversized_evidence = copy.deepcopy(complete_data)
    oversized_evidence["receipts"][0]["evidence_references"] = ["e" * (CONTRACT.IDENTITY_LIMIT + 1)]
    require_contract_error(
        "bounded Scout Receipt evidence",
        "exceeds 128",
        lambda: validate_receipts_data(oversized_evidence, manifest, "oversized-evidence"),
    )

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
        require(
            "provider-authenticated" in str(error) or "dedicated register writer" in str(error),
            "writer authentication mutation failed for the wrong reason",
        )

    foreign_dedicated_writer = copy.deepcopy(records)
    foreign_dedicated_writer["writer_id"] = "forge:writer:other"
    require_contract_error(
        "foreign dedicated writer",
        "dedicated register writer",
        lambda: CONTRACT.validate_register(foreign_dedicated_writer, manifest, authentication, POLICY_PATH),
    )

    for field in ("lane", "rationale", "risk", "budget_use", "evidence_ids"):
        incomplete_row = copy.deepcopy(records)
        incomplete_row["rows"][0].pop(field)
        require_contract_error(
            f"row missing {field}",
            "row 0 schema mismatch",
            lambda incomplete_row=incomplete_row: CONTRACT.validate_register(incomplete_row, manifest, authentication, POLICY_PATH),
        )
    extra_row_field = copy.deepcopy(records)
    extra_row_field["rows"][0]["priority"] = "urgent"
    require_contract_error(
        "row with unknown field",
        "row 0 schema mismatch",
        lambda: CONTRACT.validate_register(extra_row_field, manifest, authentication, POLICY_PATH),
    )

    for field in ("kind", "run_id"):
        incomplete_receipt = copy.deepcopy(records)
        incomplete_receipt["history_receipts"][0].pop(field)
        rehash_history(incomplete_receipt)
        require_contract_error(
            f"history receipt missing {field}",
            "history receipt 1 schema mismatch",
            lambda incomplete_receipt=incomplete_receipt: CONTRACT.validate_register(incomplete_receipt, manifest, authentication, POLICY_PATH),
        )
    unknown_receipt_kind = copy.deepcopy(records)
    unknown_receipt_kind["history_receipts"][0]["kind"] = "caller-asserted-success"
    rehash_history(unknown_receipt_kind)
    require_contract_error(
        "unknown history receipt kind",
        "kind is invalid",
        lambda: CONTRACT.validate_register(unknown_receipt_kind, manifest, authentication, POLICY_PATH),
    )
    missing_latest_receipt = copy.deepcopy(records)
    missing_latest_receipt["history_anchor"].pop("latest_receipt")
    require_contract_error(
        "history anchor repair material",
        "history anchor schema mismatch",
        lambda: CONTRACT.validate_register(missing_latest_receipt, manifest, authentication, POLICY_PATH),
    )
    missing_operation_fingerprint = copy.deepcopy(records)
    missing_operation_fingerprint.pop("last_operation_fingerprint")
    require_contract_error(
        "last operation fingerprint",
        "register schema mismatch",
        lambda: CONTRACT.validate_register(missing_operation_fingerprint, manifest, authentication, POLICY_PATH),
    )
    malformed_operation_fingerprint = copy.deepcopy(records)
    malformed_operation_fingerprint["last_operation_fingerprint"] = "not-a-fingerprint"
    require_contract_error(
        "malformed last operation fingerprint",
        "lowercase SHA-256",
        lambda: CONTRACT.validate_register(malformed_operation_fingerprint, manifest, authentication, POLICY_PATH),
    )
    replayed_provider_receipt = copy.deepcopy(records)
    replayed_provider_receipt["history_receipts"][1]["provider_receipt_id"] = replayed_provider_receipt["history_receipts"][0]["provider_receipt_id"]
    rehash_history(replayed_provider_receipt)
    require_contract_error(
        "replayed provider receipt identity",
        "provider receipt replay",
        lambda: CONTRACT.validate_register(replayed_provider_receipt, manifest, authentication, POLICY_PATH),
    )
    wrong_operation_fingerprint = copy.deepcopy(records)
    wrong_operation_fingerprint["last_operation_fingerprint"] = "0" * 64
    require_contract_error(
        "valid but wrong operation fingerprint",
        "authenticated operation material",
        lambda: CONTRACT.validate_register(wrong_operation_fingerprint, manifest, authentication, POLICY_PATH),
    )
    changed_authenticated_receipt = copy.deepcopy(records)
    changed_authenticated_receipt["history_receipts"][2]["run_id"] = "run:synthetic:forged"
    rehash_history(changed_authenticated_receipt)
    require_contract_error(
        "changed authenticated receipt content",
        "authenticated receipt content",
        lambda: CONTRACT.validate_register(changed_authenticated_receipt, manifest, authentication, POLICY_PATH),
    )

    missing_lane = copy.deepcopy(manifest)
    missing_lane["scouts"].pop()
    require_contract_error(
        "manifest missing installed lane",
        "installed policy lane inventory",
        lambda: CONTRACT.validate_register(records, missing_lane, authentication, POLICY_PATH),
    )

    unknown_row_lane = copy.deepcopy(records)
    unknown_row_lane["rows"][0]["lane"] = "forged-uninstalled-lane"
    require_contract_error(
        "register row outside installed lane inventory",
        "installed policy lane inventory",
        lambda: CONTRACT.validate_register(unknown_row_lane, manifest, authentication, POLICY_PATH),
    )

    empty_standalone_manifest = copy.deepcopy(manifest)
    empty_standalone_manifest["scouts"] = []
    empty_standalone_receipts = copy.deepcopy(complete_data)
    empty_standalone_receipts["receipts"] = []
    require_receipt_cli_contract_error(
        "standalone empty Scout Receipt inventory",
        "installed policy lane inventory",
        empty_standalone_receipts,
        empty_standalone_manifest,
    )

    with tempfile.TemporaryDirectory(prefix="repo-gardener-policy-") as temp:
        policy = Path(temp) / "policy.yaml"
        policy.write_text("unrelated:\n  repository_portfolio_limit: 99\n", encoding="utf-8")
        require_contract_error("wrong-section portfolio limit", "boundaries.repository_portfolio_limit", lambda: CONTRACT.portfolio_limit(policy))
        policy.write_text("boundaries:\n  exact_revision_required_for_verification: true\n", encoding="utf-8")
        require_contract_error("missing portfolio limit", "boundaries.repository_portfolio_limit", lambda: CONTRACT.portfolio_limit(policy))
        policy.write_text("boundaries:\n  repository_portfolio_limit: 8\n", encoding="utf-8")
        require_contract_error("non-seven portfolio limit", "Release A value 7", lambda: CONTRACT.portfolio_limit(policy))
        policy.write_text("boundaries:\n  repository_portfolio_limit: 7\nlanes:\n  dependency-and-vulnerability:\n    mutation: false\n", encoding="utf-8")
        require_contract_error(
            "incomplete installed lane inventory",
            "public Release A contract",
            lambda: CONTRACT.validate_register(records, manifest, authentication, policy),
        )
        canonical_policy = POLICY_PATH.read_text(encoding="utf-8")
        inline_lane_policy = canonical_policy.replace(
            "  dependency-and-vulnerability:\n    mutation: false",
            "  dependency-and-vulnerability: {mutation: false}",
            1,
        )
        policy.write_text(inline_lane_policy, encoding="utf-8")
        require_contract_error(
            "inline lane entry",
            "unparsed or inline entry",
            lambda: CONTRACT.validate_register(records, manifest, authentication, policy),
        )
        for lane in CONTRACT.RELEASE_A_LANES:
            enabled_lane_policy, replacements = re.subn(
                rf"(  {re.escape(lane)}:\n    mutation:) false",
                r"\1 true",
                canonical_policy,
                count=1,
            )
            require(replacements == 1, f"could not construct enabled-lane mutation for {lane}")
            policy.write_text(enabled_lane_policy, encoding="utf-8")
            require_contract_error(
                f"enabled {lane} lane mutation",
                "mutation must be exactly false",
                lambda: CONTRACT.validate_register(records, manifest, authentication, policy),
            )

    require_contract_error(
        "non-identity retained capacity entry",
        "retained row 0",
        lambda: CONTRACT.render_capacity_with_limit([1], [], CONTRACT.RELEASE_A_PORTFOLIO_LIMIT),
    )
    require_contract_error(
        "unhashable retained capacity entry",
        "retained row 1",
        lambda: CONTRACT.render_capacity_with_limit(["row:valid", []], [], CONTRACT.RELEASE_A_PORTFOLIO_LIMIT),
    )

    duplicate_candidate = copy.deepcopy(scenarios["seven-slot-selection"])
    duplicate_candidate["eligible_candidates"][1]["source_id"] = duplicate_candidate["eligible_candidates"][0]["source_id"]
    require_contract_error(
        "duplicate capacity candidate",
        "duplicate candidate source identity",
        lambda: evaluate(duplicate_candidate, manifest, receipt_sets, complete_data),
    )

    noncritical_candidate = copy.deepcopy(scenarios["critical-at-capacity"])
    noncritical_candidate["critical_candidate"]["expected_impact"] = "high"
    require_contract_error(
        "noncritical preemption candidate",
        "critical candidate classification",
        lambda: evaluate(noncritical_candidate, manifest, receipt_sets, complete_data),
    )

    foreign_interruptible_row = copy.deepcopy(scenarios["critical-at-capacity"])
    foreign_interruptible_row["interruptible_row"] = "row:not-retained"
    require_contract_error(
        "foreign interruptible row",
        "interruptible row is not retained",
        lambda: evaluate(foreign_interruptible_row, manifest, receipt_sets, complete_data),
    )
    invalid_interruptible_row = copy.deepcopy(scenarios["critical-at-capacity"])
    invalid_interruptible_row["interruptible_row"] = []
    require_contract_error(
        "invalid interruptible row",
        "interruptible row",
        lambda: evaluate(invalid_interruptible_row, manifest, receipt_sets, complete_data),
    )

    mismatched_terminal_binding = copy.deepcopy(scenarios["terminal-row"])
    mismatched_terminal_binding.update(
        {
            "current_row": {"row_id": "row:ci:beta", "source_id": "forge:check:beta", "source_revision": "revision:beta:1"},
            "terminal_source_binding": {"row_id": "row:ci:beta", "source_id": "forge:check:beta", "source_revision": "revision:beta:2"},
        }
    )
    assert_expected(
        "mismatched terminal row binding",
        evaluate(mismatched_terminal_binding, manifest, receipt_sets, complete_data),
        {"row_action": "unchanged-unassociated"},
    )

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
        require(
            "canonical UTF-8 bytes" in str(error) or "schema mismatch" in str(error),
            "receipt-size mutation failed for the wrong reason",
        )

    try:
        CONTRACT.validate_body("x" * (CONTRACT.BODY_LIMIT + 1))
        raise ContractError("oversized body survived")
    except ContractError as error:
        require("managed body exceeds" in str(error), "body-size mutation failed for the wrong reason")

    validate_sources(repo_root)
    print("PASS: Release A reconciliation outcomes derive from caller, gate, receipt, capacity, and ordering facts")
    print(f"PASS: {len(mutations) + 68} reconciliation, authority, history, policy, schema, bound, and receipt mutations rejected")
    print("NOTE: fresh-context matched cases own behavioral evidence")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ContractError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
