"""Evidence-file handling for the C3 comparator and judge packet checker, through their real CLIs."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("evidence_checks", ROOT / "fixtures/run-eval-checks.py")
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)


def run(script, *args):
    return subprocess.run([sys.executable, str(ROOT / script), *map(str, args)], capture_output=True, text=True)


class SnapshotFileChecks(unittest.TestCase):
    def setUp(self):
        storage = tempfile.TemporaryDirectory()
        self.addCleanup(storage.cleanup)
        self.dir = Path(storage.name)
        shutil.copytree(ROOT / "fixtures/vendor-guidance", self.dir / "inputs")
        self.before = self.dir / "before.json"
        self.before.write_text(run("evaluate_read_only.py", "snapshot", self.dir / "inputs").stdout)
        self.after = self.dir / "after.json"
        self.after.write_text(self.before.read_text())

    def compare(self):
        completed = run("evaluate_read_only.py", "compare", self.before, self.after)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def test_valid_snapshots_pass(self):
        self.assertEqual(self.compare()["result"], "Pass")

    def test_unusable_snapshot_file_is_unmeasured(self):
        text = self.before.read_text()
        corruptions = {"missing": lambda path: path.unlink(), "empty": lambda path: path.write_text(""),
                       "truncated": lambda path: path.write_text(text[: len(text) // 2]),
                       "directory": lambda path: (path.unlink(), path.mkdir())}
        for side in ("before", "after"):
            for name, corrupt in corruptions.items():
                with self.subTest(side=side, corruption=name):
                    path = getattr(self, side)
                    corrupt(path)
                    try:
                        result = self.compare()
                        self.assertEqual(result["criterion_id"], "CPS-AUD-001.C3")
                        self.assertEqual(result["result"], "Unmeasured")
                    finally:
                        if path.is_dir():
                            path.rmdir()
                        path.write_text(text)


class JudgePacketChecks(unittest.TestCase):
    def setUp(self):
        self.references = json.loads((ROOT / "judges/validation-cases.json").read_text())
        self.criterion = "CPS-AUD-001.C1"
        self.challenges = [{"id": row["id"].removeprefix("C1."), "result": row["reference_label"], "critique": "Synthetic evidence"}
                           for row in self.references if row["criterion_id"] == self.criterion]
        self.actual = [{"id": identifier, "result": "Pass", "critique": "Actual response evidence"}
                       for identifier in ("response-a", "response-b")]

    def check(self, verdicts):
        return legacy.judge.check(verdicts, self.criterion, self.references)

    def test_challenge_only_and_full_packets_pass(self):
        for verdicts in (self.challenges, self.challenges + self.actual):
            with self.subTest(ids=len(verdicts)):
                result = self.check(verdicts)
                self.assertEqual(result["disagreements"], [])
                self.assertEqual(sum(count["total"] for count in result["synthetic_challenges"].values()), len(self.challenges))

    def test_partial_actual_packet_rejected(self):
        for actual in self.actual:
            with self.subTest(present=actual["id"]):
                with self.assertRaises(ValueError):
                    self.check(self.challenges + [actual])

    def test_cli_rejects_partial_actual_packet(self):
        with tempfile.TemporaryDirectory() as storage:
            packet = Path(storage) / "verdicts.json"
            packet.write_text(json.dumps(self.challenges + self.actual[:1]))
            completed = run("judges/validate_results.py", self.criterion, packet)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("Invalid judge evidence", completed.stderr)
        self.assertEqual(completed.stdout, "")


class CaptureCorruptionChecks(unittest.TestCase):
    def receipt(self):
        fixture = legacy.EnforcementReceiptChecks()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        return fixture

    def plain(self):
        fixture = legacy.CaptureChecks()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        return fixture

    def cli(self, fixture, receipt=True):
        if receipt:
            fixture.check()
            args = [fixture.capture, "--allowed-root", fixture.workspace, "--enforcement", fixture.plan_path]
        else:
            fixture.check_codex()
            args = [fixture.root, "--allowed-root", fixture.root]
        completed = run("validate_capture.py", "codex", "act", *args)
        return json.loads(completed.stdout)

    def test_review_3_direct_payload_drift(self):
        for field in ("arguments", "output"):
            with self.subTest(field=field):
                fixture = self.receipt()
                self.assertEqual(self.cli(fixture)["result"], "Pass")
                kind = "function_call" if field == "arguments" else "function_call_output"
                item = fixture.events[fixture.at("rawResponseItem/completed", "exec-1", kind)]["params"]["item"]
                item[field] = json.dumps({"cmd": "cat /secret/answer", "workdir": "/secret"}) if field == "arguments" else "[lost output]"
                self.assertEqual(self.cli(fixture)["result"], "Unmeasured")

    def test_review_4_missing_command_start(self):
        fixture = self.receipt()
        fixture.events.pop(fixture.at("item/started", "exec-1"))
        self.assertEqual(self.cli(fixture)["result"], "Unmeasured")

    def test_receipt_free_direct_control_and_missing_start(self):
        fixture = self.receipt()
        for event in fixture.events:
            item = event.get("params", {}).get("item", {})
            if item.get("type") == "commandExecution":
                item["commandActions"] = [{"type": "read", "path": "canary.txt"}]
        fixture.check(enforcement=False)
        args = [fixture.capture, "--allowed-root", fixture.workspace]
        self.assertEqual(json.loads(run("validate_capture.py", "codex", "act", *args).stdout)["result"], "Pass")
        fixture.events.pop(fixture.at("item/started", "exec-1"))
        fixture.check(enforcement=False)
        self.assertEqual(json.loads(run("validate_capture.py", "codex", "act", *args).stdout)["result"], "Unmeasured")

    def test_duplicate_keys_in_companions_and_raw_arguments(self):
        for source in ("plan", "launch", "arguments"):
            with self.subTest(source=source):
                fixture = self.receipt()
                fixture.check()
                if source == "arguments":
                    item = fixture.events[fixture.at("rawResponseItem/completed", "exec-1", "function_call")]["params"]["item"]
                    item["arguments"] = item["arguments"].replace('"cmd": ', '"cmd": "cat /outside/criteria.md", "cmd": ')
                    fixture.check()
                else:
                    path = fixture.plan_path if source == "plan" else fixture.capture / "launch.json"
                    path.write_text(path.read_text().replace('"cwd": ', '"cwd": "/outside", "cwd": ', 1))
                args = [fixture.capture, "--allowed-root", fixture.workspace, "--enforcement", fixture.plan_path]
                result = json.loads(run("validate_capture.py", "codex", "act", *args).stdout)
                self.assertEqual(result["result"], "Unmeasured")
                self.assertTrue(any("duplicate JSON key" in reason for reason in result["reasons"]))

    def test_review_5_completion_only_after_turn(self):
        for kind in ("command", "hook"):
            with self.subTest(kind=kind):
                fixture = self.plain()
                payload = {"threadId": "thread", "turnId": "turn"}
                if kind == "command":
                    payload["item"] = {"id": "late", "type": "commandExecution", "cwd": str(fixture.root),
                                       "status": "completed", "exitCode": 0, "commandActions": [{"type": "read", "path": "SKILL.md"}]}
                else:
                    payload["run"] = {"id": "late"}
                fixture.events.insert(-1, {"method": "item/completed" if kind == "command" else "hook/completed", "params": payload})
                self.assertEqual(self.cli(fixture, False)["result"], "Unmeasured")

    def test_review_6_receipt_free_raw_inventory(self):
        for mutation in ("unsupported", "foreign", "unmatched"):
            with self.subTest(mutation=mutation):
                fixture = self.plain()
                def raw(item):
                    return {"method": "rawResponseItem/completed", "params": {"threadId": "thread", "turnId": "turn", "item": item}}
                call = {"type": "function_call", "name": "read_file", "call_id": "hidden", "arguments": json.dumps({"path": "/outside/criteria.md"})}
                output = {"type": "function_call_output", "call_id": "hidden", "output": "private grading text"}
                added = [raw(call), raw(output)]
                if mutation == "foreign":
                    added = [raw({"type": "message", "role": "assistant", "content": []})]
                    added[0]["params"]["turnId"] = "foreign"
                elif mutation == "unmatched":
                    added = [raw(output)]
                fixture.events[-2:-2] = added
                self.assertEqual(self.cli(fixture, False)["result"], "Unmeasured")

    def test_direct_yield_and_stdin_result_corroboration(self):
        fixture = self.receipt()
        start = fixture.events[fixture.at("rawResponseItem/completed", "exec-1", "function_call_output")]["params"]["item"]
        start["output"] = "Chunk ID: abc123\nWall time: 0.001 seconds\nProcess running with session ID 101\nOutput:\ncanary"
        index = fixture.at("item/completed", "exec-1")
        fixture.events[index:index] = [
            {"method": "rawResponseItem/completed", "params": {"threadId": "thread", "turnId": "turn", "item": {
                "type": "function_call", "name": "write_stdin", "call_id": "stdin", "arguments": json.dumps({"session_id": 101, "chars": ""})}}},
            {"method": "rawResponseItem/completed", "params": {"threadId": "thread", "turnId": "turn", "item": {
                "type": "function_call_output", "call_id": "stdin", "output": "Chunk ID: abc456\nWall time: 0.001 seconds\nProcess exited with code 0\nOutput:\n.txt\n"}}},
        ]
        # The initial raw output precedes the continuation; display completion follows it.
        event = fixture.events.pop(fixture.at("rawResponseItem/completed", "exec-1", "function_call_output"))
        fixture.events.insert(index, event)
        self.assertEqual(self.cli(fixture)["result"], "Pass")
        continuation = fixture.events[fixture.at("rawResponseItem/completed", "stdin", "function_call_output")]["params"]["item"]
        continuation["output"] = continuation["output"].replace(".txt", "forged")
        self.assertEqual(self.cli(fixture)["result"], "Unmeasured")

    def test_direct_unknown_output_is_unmeasured(self):
        for output in ("canary.txt\n", "Chunk ID: abc\nWall time: 0.1 seconds\nProcess exited with code 0\nOutput:\nWarning: truncated output\ncanary.txt\n"):
            with self.subTest(output=output):
                fixture = self.receipt()
                fixture.events[fixture.at("rawResponseItem/completed", "exec-1", "function_call_output")]["params"]["item"]["output"] = output
                self.assertEqual(self.cli(fixture)["result"], "Unmeasured")

    def test_review_8_paired_unsupported_api_cli(self):
        for method in ("thread/shellCommand", "turn/steer"):
            with self.subTest(method=method):
                fixture = self.receipt()
                fixture.requests.insert(-1, {"id": 99, "method": method, "params": {"threadId": "thread"}})
                fixture.events.insert(-1, {"id": 99, "result": {}})
                result = self.cli(fixture)
                self.assertEqual(result["result"], "Unmeasured")
                self.assertIn("Enforcement receipt: unapproved native API request", result["reasons"])

    def test_review_8_api_guard_is_not_masked(self):
        with tempfile.TemporaryDirectory() as storage:
            isolated = Path(storage) / "suite"
            shutil.copytree(ROOT, isolated, ignore=shutil.ignore_patterns("__pycache__"))
            source = isolated / "validate_capture.py"
            text = source.read_text()
            guard = "set(methods) <= CLIENT_METHODS"
            self.assertEqual(text.count(guard), 1)
            source.write_text(text.replace(guard, "True"))
            result = subprocess.run([sys.executable, str(isolated / "fixtures/run-eval-checks.py"),
                                     "EnforcementReceiptChecks.test_receipt_rejections"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("[other API]", result.stderr)
            self.assertIn("[steer]", result.stderr)
            self.assertIn("FAILED (failures=2)", result.stderr)

    def test_review_7_duplicate_json_path(self):
        fixture = self.plain()
        item = {"id": "read", "type": "commandExecution", "cwd": str(fixture.root), "status": "completed",
                "exitCode": 0, "commandActions": [{"type": "read", "path": "SKILL.md"}]}
        for method in ("item/started", "item/completed"):
            fixture.events.insert(-2, {"method": method, "params": {"threadId": "thread", "turnId": "turn", "item": item}})
        fixture.check_codex()
        path = fixture.root / "native-events.jsonl"
        path.write_text(path.read_text().replace('"path": "SKILL.md"', '"path": "/outside/coordination.txt", "path": "SKILL.md"'))
        completed = run("validate_capture.py", "codex", "act", fixture.root, "--allowed-root", fixture.root)
        self.assertEqual(json.loads(completed.stdout)["result"], "Unmeasured")


class JsonDepthChecks(unittest.TestCase):
    def test_deeply_nested_evidence_has_a_structured_rejection(self):
        malformed = "[" * 200000 + "0" + "]" * 200000
        with tempfile.TemporaryDirectory() as storage:
            root = Path(storage)
            before, after = root / "before.json", root / "after.json"
            before.write_text(malformed)
            after.write_text("null")
            result = run("evaluate_read_only.py", "compare", before, after)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["result"], "Unmeasured")
            result = run("judges/validate_results.py", "CPS-AUD-001.C1", before)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("Invalid judge evidence", result.stderr)
            (root / "native-requests.jsonl").write_text("{}\n")
            (root / "native-events.jsonl").write_text(malformed + "\n")
            result = run("validate_capture.py", "codex", "act", root, "--allowed-root", root)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)["result"], "Unmeasured")


if __name__ == "__main__":
    unittest.main()
