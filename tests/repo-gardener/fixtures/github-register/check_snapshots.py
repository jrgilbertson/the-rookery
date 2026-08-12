#!/usr/bin/env python3
"""Exercise synthetic, live-shaped GitHub register snapshots."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
FIXTURES = Path(__file__).resolve().parent
CONTRACT_PATH = ROOT / "skills/repo-gardener/scripts/release_a_contract.py"
REPOSITORY_ID = "R_SYNTHETIC_REPOSITORY_001"
REPORT_ID = "I_SYNTHETIC_REPORT_001"
WRITER_ID = "U_SYNTHETIC_WRITER_001"
OTHER_WRITER_ID = "U_SYNTHETIC_OTHER_001"
BODY_BEGIN = "<!-- orchestrator:current-portfolio:v1:begin -->"
BODY_END = "<!-- orchestrator:current-portfolio:v1:end -->"
RECEIPT_BEGIN = "<!-- orchestrator:history-receipt:v1:begin -->"
RECEIPT_END = "<!-- orchestrator:history-receipt:v1:end -->"


def receipt_hash(receipt: dict[str, Any]) -> str:
    receipt_without_hash = {key: value for key, value in receipt.items() if key != "receipt_hash"}
    material = b"\0".join(
        (
            b"orchestrator-history/v1",
            REPOSITORY_ID.encode("ascii"),
            REPORT_ID.encode("ascii"),
            json.dumps(receipt_without_hash, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        )
    )
    return hashlib.sha256(material).hexdigest()


def make_receipts(count: int) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    previous_hash = "GENESIS"
    middle_kinds = ("manifest", "scout", "evidence", "decision", "effect", "release", "run")
    for sequence in range(1, count + 1):
        if sequence == 1:
            kind = "run-opened"
        elif sequence == count:
            kind = "run-closed"
        else:
            kind = middle_kinds[(sequence - 2) % len(middle_kinds)]
        receipt = {
            "schema": "orchestrator-history/v1",
            "sequence": sequence,
            "previous_hash": previous_hash,
            "receipt_hash": "",
            "operation_id": f"operation:synthetic:{sequence:03d}",
            "kind": kind,
            "run_id": "run:synthetic:001",
            "payload": {"disposition": "synthetic", "ordinal": sequence},
        }
        receipt["receipt_hash"] = receipt_hash(receipt)
        receipts.append(receipt)
        previous_hash = receipt["receipt_hash"]
    return receipts


def receipt_comment(receipt: dict[str, Any], sequence: int) -> dict[str, Any]:
    raw = json.dumps(receipt, ensure_ascii=False, separators=(",", ":"))
    return {
        "id": 10_000 + sequence,
        "node_id": f"IC_SYNTHETIC_{sequence:03d}",
        "user": {"node_id": WRITER_ID, "login": "synthetic-writer"},
        "body": f"{RECEIPT_BEGIN}\n{raw}\n{RECEIPT_END}",
    }


def make_register(receipts: list[dict[str, Any]], *, genesis: bool = False) -> dict[str, Any]:
    if genesis:
        return {
            "schema": "orchestrator-register/v1",
            "repository_id": REPOSITORY_ID,
            "report_issue_id": REPORT_ID,
            "writer_id": WRITER_ID,
            "register_revision": 0,
            "last_operation_id": None,
            "last_operation_fingerprint": None,
            "history_anchor": {"sequence": 0, "head": "GENESIS", "latest_receipt": None},
            "rows": [],
        }
    latest = receipts[-1]
    return {
        "schema": "orchestrator-register/v1",
        "repository_id": REPOSITORY_ID,
        "report_issue_id": REPORT_ID,
        "writer_id": WRITER_ID,
        "register_revision": len(receipts),
        "last_operation_id": latest["operation_id"],
        "last_operation_fingerprint": "f" * 64,
        "history_anchor": {"sequence": len(receipts), "head": latest["receipt_hash"], "latest_receipt": latest},
        "rows": [
            {
                "row_id": "row:synthetic:001",
                "source_id": "source:synthetic:001",
                "source_revision": "revision:synthetic:001",
                "description": "Review the synthetic fixture candidate.",
                "work_state": "To do",
                "lane": "issue-implementation",
                "outcome": "selected",
                "rationale": "Synthetic fixture evidence supports review.",
                "risk": "low",
                "budget_use": "one portfolio slot",
                "evidence": ["evidence:synthetic:001"],
                "next_action": "review synthetic fixture",
                "row_revision": 1,
            }
        ],
    }


def machine_body(register: dict[str, Any]) -> str:
    raw = json.dumps(register, ensure_ascii=False, separators=(",", ":"))
    return f"{BODY_BEGIN}\n```json\n{raw}\n```\n{BODY_END}\n\n# Synthetic report projection\n"


def base_snapshot(label: str) -> dict[str, Any]:
    count = {"genesis": 0, "two-receipts": 2, "live-scale": 103, "provider-page-30": 45}[label]
    receipts = make_receipts(count)
    register = make_register(receipts, genesis=not receipts)
    comments = [receipt_comment(receipt, index) for index, receipt in enumerate(receipts, start=1)]
    if label == "live-scale":
        comments.insert(
            50,
            {
                "id": 20_001,
                "node_id": "IC_SYNTHETIC_ORDINARY",
                "user": {"node_id": OTHER_WRITER_ID, "login": "synthetic-owner"},
                "body": "Synthetic owner note.",
            },
        )
    page_size = 30 if label == "provider-page-30" else 100
    pages = [comments[index : index + page_size] for index in range(0, len(comments), page_size)] or [[]]
    return {
        "schema": "repo-gardener-github-register-snapshot/v1",
        "configured_repository_id": REPOSITORY_ID,
        "configured_report_issue_id": REPORT_ID,
        "configured_writer_id": WRITER_ID,
        "issue": {"id": 3336, "node_id": REPORT_ID, "body": machine_body(register), "state": "open", "comments": len(comments)},
        "comment_pages_complete": True,
        "comment_pages": pages,
    }


def rewrite_body(snapshot: dict[str, Any], register: dict[str, Any]) -> None:
    snapshot["issue"]["body"] = machine_body(register)


def apply_mutation(snapshot: dict[str, Any], mutation: str) -> None:
    if mutation == "none":
        return
    comments = [item for page in snapshot["comment_pages"] for item in page]
    if mutation == "add-authority":
        snapshot["authority"] = {"authenticated": True, "proof_complete": True}
    elif mutation == "add-verdict":
        snapshot["verdict"] = {"result": "observed", "trusted": True}
    elif mutation == "receipt-terminal-lf":
        for comment in comments:
            comment["body"] += "\n"
    elif mutation == "receipt-surrounding-prose":
        comments[0]["body"] += "\nprose"
    elif mutation == "add-unrelated-comment":
        snapshot["comment_pages"][0].append(
            {
                "id": 20_001,
                "node_id": "IC_SYNTHETIC_ORDINARY",
                "user": {"node_id": OTHER_WRITER_ID, "login": "synthetic-owner"},
                "body": "Synthetic owner note.",
            }
        )
        snapshot["issue"]["comments"] += 1
    elif mutation == "incomplete-pagination":
        snapshot["comment_pages_complete"] = False
    elif mutation == "forged-writer-marker":
        snapshot["comment_pages"][0].append(
            {
                "id": 20_002,
                "node_id": "IC_SYNTHETIC_FORGED",
                "user": {"node_id": OTHER_WRITER_ID, "login": "synthetic-owner"},
                "body": comments[0]["body"],
            }
        )
    elif mutation == "wrong-writer":
        snapshot["configured_writer_id"] = OTHER_WRITER_ID
    elif mutation == "missing-page":
        snapshot["comment_pages"].insert(0, [])
    elif mutation == "truncated-tail":
        snapshot["comment_pages"][-1].pop()
    elif mutation == "nonuniform-pages":
        tail = snapshot["comment_pages"][1]
        snapshot["comment_pages"] = [snapshot["comment_pages"][0], tail[:-1], tail[-1:]]
    elif mutation == "duplicate-comment-id":
        comments[1]["node_id"] = comments[0]["node_id"]
    elif mutation == "nul-identity":
        snapshot["configured_repository_id"] = f"{REPOSITORY_ID}\0suffix"
    elif mutation == "control-identity":
        snapshot["configured_writer_id"] = f"{WRITER_ID}\x1fsuffix"
    elif mutation in {"sequence-gap", "altered-payload", "bad-previous-hash"}:
        receipt = json.loads(comments[1]["body"].split(RECEIPT_BEGIN)[1].split(RECEIPT_END)[0])
        if mutation == "sequence-gap":
            receipt["sequence"] = 3
        elif mutation == "altered-payload":
            receipt["payload"]["disposition"] = "altered"
        else:
            receipt["previous_hash"] = "0" * 64
        comments[1]["body"] = f"{RECEIPT_BEGIN}\n{json.dumps(receipt, ensure_ascii=False, separators=(',', ':'))}\n{RECEIPT_END}"
    else:
        body = snapshot["issue"]["body"]
        register = json.loads(body.split("```json\n", 1)[1].split("\n```", 1)[0])
        if mutation == "bad-body-anchor":
            register["history_anchor"]["head"] = "0" * 64
        elif mutation == "revision-anchor-mismatch":
            register["register_revision"] += 1
        elif mutation == "empty-description":
            register["rows"][0]["description"] = ""
        elif mutation == "duplicate-evidence":
            register["rows"][0]["evidence"] *= 2
        elif mutation == "wrong-repository":
            register["repository_id"] = "R_SYNTHETIC_WRONG"
        elif mutation == "wrong-report":
            register["report_issue_id"] = "I_SYNTHETIC_WRONG"
        else:
            raise AssertionError(f"unknown mutation: {mutation}")
        rewrite_body(snapshot, register)


def load_contract() -> Any:
    spec = importlib.util.spec_from_file_location("release_a_contract", CONTRACT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    scenarios = json.loads((FIXTURES / "scenarios.json").read_text())["scenarios"]
    expectations = json.loads((FIXTURES / "expectations.json").read_text())["expectations"]
    contract = load_contract()
    failures: list[str] = []
    concepts = (ROOT / "CONCEPTS.md").read_text()
    run_history = concepts.split("### Run History", 1)[1].split("### Scout Receipt", 1)[0]
    documented_kinds = set(re.findall(r"`([^`]+)`", run_history))
    if documented_kinds != contract.ORCHESTRATOR_HISTORY_KINDS:
        failures.append(
            "CONCEPTS.md Run History kinds do not match ORCHESTRATOR_HISTORY_KINDS"
        )
    for scenario in scenarios:
        snapshot = copy.deepcopy(base_snapshot(scenario["base"]))
        apply_mutation(snapshot, scenario["mutation"])
        expected = expectations[scenario["id"]]
        try:
            result = contract.normalize_github_register_snapshot(snapshot)
        except contract.ContractError as error:
            if expected.get("error") != str(error):
                failures.append(f"{scenario['id']}: expected {expected!r}, got error {error!s}")
            continue
        if "error" in expected:
            failures.append(f"{scenario['id']}: expected error {expected['error']!r}, got success")
            continue
        actual = {
            "history_sequence": result["history_sequence"],
            "register_revision": result["register"]["register_revision"],
            "row_count": len(result["register"]["rows"]),
            "writer_receipts": len(result["history_receipts"]),
            "ordinary_comments": len(result["ordinary_comment_ids"]),
            "structural_integrity": result["structural_integrity"],
            "provenance": result["provenance"],
        }
        if actual != expected:
            failures.append(f"{scenario['id']}: expected {expected!r}, got {actual!r}")
        raw_comments = [item for page in snapshot["comment_pages"] for item in page if item["user"]["node_id"] == WRITER_ID]
        if [item["raw_receipt_json"] for item in result["history_receipts"]] != [
            item["body"].split(RECEIPT_BEGIN)[1].split(RECEIPT_END)[0].strip() for item in raw_comments
        ]:
            failures.append(f"{scenario['id']}: raw receipt JSON bytes were not preserved")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    cli = subprocess.run(
        [sys.executable, str(CONTRACT_PATH), "normalize-github-register", "--input", "-"],
        input=json.dumps(base_snapshot("genesis")),
        text=True,
        capture_output=True,
        check=False,
    )
    if cli.returncode != 0 or json.loads(cli.stdout)["history_sequence"] != 0:
        print(f"CLI normalization failed: {cli.stderr.strip()}", file=sys.stderr)
        return 1
    print(f"PASS: {len(scenarios)} synthetic GitHub register snapshots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
