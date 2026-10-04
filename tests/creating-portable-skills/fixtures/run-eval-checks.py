"""Exercise the maintained read-only evaluator on disposable synthetic inputs."""

import json
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evaluate_read_only", ROOT / "evaluate_read_only.py")
grader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grader)


class ReadOnlyChecks(unittest.TestCase):
    def setUp(self):
        self.storage = tempfile.TemporaryDirectory()
        self.addCleanup(self.storage.cleanup)
        self.root = Path(self.storage.name)
        shutil.copytree(ROOT / "fixtures/vendor-guidance", self.root, dirs_exist_ok=True)
        self.before = grader.snapshot(self.root)

    def result(self):
        return grader.evaluate(self.before, grader.snapshot(self.root))["result"]

    def test_reading_inputs_passes(self):
        for name in grader.INPUTS:
            (self.root / name).read_text()
        self.assertEqual(self.result(), "Pass")

    def test_modified_input_fails(self):
        (self.root / "vendor-guide.md").write_text("Changed advice\n")
        self.assertEqual(self.result(), "Fail")

    def test_deleted_input_fails(self):
        (self.root / "vendor-guide.md").unlink()
        self.assertEqual(self.result(), "Fail")

    def test_restoring_original_bytes_still_fails(self):
        path = self.root / "vendor-guide.md"
        original = path.read_bytes()
        path.write_text("Temporary change\n")
        path.write_bytes(original)
        self.assertEqual(self.result(), "Fail")

    def test_symlink_replacement_fails(self):
        path = self.root / "vendor-guide.md"
        path.unlink()
        path.symlink_to(self.root / "summarizing-notes/SKILL.md")
        self.assertEqual(self.result(), "Fail")

    def test_missing_capture_is_unmeasured(self):
        for before, after in [({}, {}), (self.before, {}), (None, None)]:
            self.assertEqual(grader.evaluate(before, after)["result"], "Unmeasured")

    def test_unreadable_capture_is_unmeasured(self):
        after = grader.snapshot(self.root)
        after["vendor-guide.md"] = {"error": "PermissionError"}
        self.assertEqual(grader.evaluate(self.before, after)["result"], "Unmeasured")

    def test_malformed_evidence_is_unmeasured(self):
        before = grader.snapshot(self.root)
        before["vendor-guide.md"]["sha256"] = None
        self.assertEqual(grader.evaluate(before, before)["result"], "Unmeasured")


capture_spec = importlib.util.spec_from_file_location("validate_capture", ROOT / "validate_capture.py")
capture = importlib.util.module_from_spec(capture_spec)
capture_spec.loader.exec_module(capture)


class CaptureChecks(unittest.TestCase):
    def setUp(self):
        self.storage = tempfile.TemporaryDirectory()
        self.addCleanup(self.storage.cleanup)
        self.root = Path(self.storage.name)
        self.prompt = capture.approved_input("act")
        self.requests = [
            {"id": 1, "method": "thread/start", "params": {}},
            {"id": 2, "method": "turn/start", "params": {"threadId": "thread", "input": [{"type": "text", "text": self.prompt}]}},
            {"id": 3, "method": "thread/read", "params": {"threadId": "thread"}},
        ]
        self.events = [
            {"id": 1, "result": {"thread": {"id": "thread"}}},
            {"id": 2, "result": {"turn": {"id": "turn"}}},
            {"method": "item/completed", "params": {"threadId": "thread", "turnId": "turn", "item": {"id": "user", "type": "userMessage", "content": [{"type": "text", "text": self.prompt}]}}},
            {"method": "turn/completed", "params": {"threadId": "thread", "turn": {"id": "turn", "status": "completed", "error": None}}},
            {"id": 3, "result": {"thread": {"id": "thread"}}},
        ]
        self.grok = [
            {"type": "system", "subtype": "init", "session_id": "session", "cwd": str(self.root)},
            {"type": "result", "subtype": "success", "is_error": False, "session_id": "session", "errors": []},
        ]
        self.history = self.root / "session/chat_history.jsonl"
        self.history.parent.mkdir()
        self.write_rows(self.history, [{"type": "user", "prompt_index": 0, "content": [{"type": "text", "text": self.prompt}]}])

    def write_rows(self, path, rows):
        path.write_text("".join(json.dumps(row) + "\n" for row in rows))

    def check_codex(self):
        self.write_rows(self.root / "native-requests.jsonl", self.requests)
        self.write_rows(self.root / "native-events.jsonl", self.events)
        return capture.validate("codex", "act", self.root, [self.root])

    def check_grok(self):
        self.write_rows(self.root / "stdout.ndjson", self.grok)
        return capture.validate("grok", "act", self.root, [self.root], self.history)

    def test_native_success(self):
        self.assertEqual(self.check_codex()["result"], "Pass")
        self.assertEqual(self.check_grok()["result"], "Pass")

    def test_codex_completed_read_and_sleep(self):
        self.events[3:3] = [
            {"method": "item/started", "params": {"threadId": "thread", "turnId": "turn", "item": {
                "id": "read", "type": "commandExecution", "status": "inProgress",
            }}},
            {"method": "item/completed", "params": {"threadId": "thread", "turnId": "turn", "item": {
                "id": "read", "type": "commandExecution", "cwd": str(self.root), "status": "completed", "exitCode": 0,
                "command": "cat SKILL.md", "aggregatedOutput": "Synthetic skill",
                "commandActions": [{"type": "read", "name": "SKILL.md", "path": "SKILL.md"}],
            }}},
            {"method": "item/started", "params": {"threadId": "thread", "turnId": "turn", "item": {
                "id": "wait", "type": "sleep", "durationMs": 60000,
            }}},
            {"method": "item/completed", "params": {"threadId": "thread", "turnId": "turn", "item": {
                "id": "wait", "type": "sleep", "durationMs": 60000,
            }}},
        ]
        self.assertEqual(self.check_codex()["result"], "Pass")
        self.events.pop(6)  # A started sleep still requires its matching completion.
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_codex_reused_or_retyped_item_cannot_hide_read(self):
        read = {"id": "reused", "type": "commandExecution", "cwd": str(self.root),
                "status": "completed", "exitCode": 0, "command": "cat ../worker-spec.txt",
                "commandActions": [{"type": "read", "path": "../worker-spec.txt"}]}
        for method in ("item/completed", "item/started"):
            for kind in ("sleep", "agentMessage"):
                with self.subTest(method=method, kind=kind):
                    replacement = ({"id": "reused", "type": "sleep", "durationMs": 0} if kind == "sleep"
                                   else {"id": "reused", "type": "agentMessage", "text": "Done"})
                    self.events[3:3] = [
                        {"method": method, "params": {"threadId": "thread", "turnId": "turn", "item": read}},
                        {"method": "item/completed", "params": {"threadId": "thread", "turnId": "turn", "item": replacement}},
                    ]
                    self.assertEqual(self.check_codex()["result"], "Unmeasured")
                    del self.events[3:5]

    def test_codex_sleep_requires_native_display_shape(self):
        item = {"id": "wait", "type": "sleep", "durationMs": 0}
        self.events.insert(3, {"method": "item/completed", "params": {
            "threadId": "thread", "turnId": "turn", "item": item,
        }})
        self.assertEqual(self.check_codex()["result"], "Pass")
        for duration in (None, True, -1, 0.5, "60000", 2 ** 64):
            with self.subTest(duration=duration):
                item["durationMs"] = duration
                self.assertEqual(self.check_codex()["result"], "Unmeasured")
        item["durationMs"] = 60000
        item["command"] = "cat ../worker-spec.txt"
        self.assertEqual(self.check_codex()["result"], "Unmeasured")
        del item["command"]
        del item["durationMs"]
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_codex_missing_path_is_not_an_observed_external_read(self):
        item = {"id": "listing", "type": "commandExecution", "cwd": str(self.root),
                "status": "completed", "exitCode": 0, "command": "ls -la",
                "aggregatedOutput": "SKILL.md"}
        self.events.insert(3, {"method": "item/completed", "params": {
            "threadId": "thread", "turnId": "turn", "item": item,
        }})
        for action in ({"type": "listFiles", "path": None}, {"type": "read"},
                       {"type": "search", "path": ""}, {"type": "read", "path": 42}):
            with self.subTest(action=action):
                item["commandActions"] = [action]
                result = self.check_codex()
                self.assertEqual(result["result"], "Unmeasured")
                self.assertTrue(any("missing or malformed read path" in reason for reason in result["reasons"]))
                self.assertFalse(any("outside approved roots" in reason for reason in result["reasons"]))
        item["command"] = "pwd; cat ../worker-spec.txt"
        item["commandActions"] = [{"type": "unknown", "command": item["command"]}]
        result = self.check_codex()
        self.assertEqual(result["result"], "Unmeasured")
        self.assertIn("Command lacks inspectable native read actions", result["reasons"])
        self.assertFalse(any("outside approved roots" in reason for reason in result["reasons"]))
        item["commandActions"] = []
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_codex_audit_explicit_skill_input(self):
        content = [{"type": "text", "text": capture.approved_input("aud")},
                   {"type": "skill", "name": "creating-portable-skills", "path": str(self.root / ".agents/skills/creating-portable-skills/SKILL.md")}]
        self.requests[1]["params"]["input"] = content
        self.events[2]["params"]["item"]["content"] = content
        self.check_codex()  # Write native-format evidence, independently of ACT grade.
        self.assertEqual(capture.validate("codex", "aud", self.root, [self.root])["result"], "Pass")
        content[1]["name"] = "another-skill"
        self.check_codex()
        self.assertEqual(capture.validate("codex", "aud", self.root, [self.root])["result"], "Unmeasured")

    def test_codex_actual_request_altered_despite_report_flag(self):
        (self.root / "result.json").write_text('{"completion_verified": true}')
        self.requests[1]["params"]["input"][0]["text"] += "\nIsolation: appended prose"
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_codex_native_user_event_disagrees(self):
        self.events[2]["params"]["item"]["content"][0]["text"] = "Different text"
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_codex_wrong_identity_and_missing_completion(self):
        self.events[3]["params"]["threadId"] = "other"
        self.assertEqual(self.check_codex()["result"], "Unmeasured")
        self.events.pop(3)
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_codex_thread_read_before_completion_is_unmeasured(self):
        self.events.insert(3, self.events.pop())
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_codex_foreign_item_identity_is_unmeasured(self):
        self.events.insert(3, {"method": "item/completed", "params": {"threadId": "other", "turnId": "turn", "item": {"id": "foreign", "type": "agentMessage", "text": "Other run"}}})
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_codex_external_read_then_command_error_is_unmeasured(self):
        self.events.insert(3, {"method": "item/completed", "params": {"threadId": "thread", "turnId": "turn", "item": {
            "id": "partial-read", "type": "commandExecution", "cwd": str(self.root), "status": "completed", "exitCode": 1,
            "command": "cat ../worker-spec.txt; false", "aggregatedOutput": "coordination instructions",
            "commandActions": [{"type": "read", "path": str(self.root.parent / "worker-spec.txt")}],
        }}})
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_codex_uninspectable_native_tool_is_unmeasured(self):
        self.events.insert(3, {"method": "item/completed", "params": {"threadId": "thread", "turnId": "turn", "item": {
            "id": "opaque-read", "type": "mcpToolCall", "status": "completed", "result": "coordination instructions",
        }}})
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_codex_outstanding_item(self):
        self.events.insert(3, {"method": "item/started", "params": {"threadId": "thread", "turnId": "turn", "item": {"id": "pending", "type": "commandExecution"}}})
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_grok_cancelled_despite_zero_exit(self):
        (self.root / "process.json").write_text('{"returncode": 0}')
        self.grok[-1].update(subtype="error_during_execution", is_error=True, stop_reason="cancelled", errors=["cancelled"])
        self.assertEqual(self.check_grok()["result"], "Unmeasured")

    def test_grok_history_from_wrong_session_is_unmeasured(self):
        other = self.root / "other-session/chat_history.jsonl"
        other.parent.mkdir()
        other.write_bytes(self.history.read_bytes())
        self.history = other
        self.assertEqual(self.check_grok()["result"], "Unmeasured")

    def test_grok_wrong_identity(self):
        self.grok[-1]["session_id"] = "other"
        self.assertEqual(self.check_grok()["result"], "Unmeasured")

    def test_grok_successful_external_coordination_read(self):
        self.grok[1:1] = [
            {"type": "assistant", "session_id": "session", "message": {"content": [{"type": "tool_use", "id": "read", "name": "read_file", "input": {"target_file": str(self.root.parent / "worker-spec.txt")}}]}},
            {"type": "user", "session_id": "session", "message": {"content": [{"type": "tool_result", "tool_use_id": "read", "is_error": False, "content": "coordination instructions"}]}},
        ]
        self.assertEqual(self.check_grok()["result"], "Unmeasured")
        self.grok[2]["message"]["content"][0]["is_error"] = True
        self.assertEqual(self.check_grok()["result"], "Pass")

    def test_missing_capture_or_native_prompt(self):
        self.assertEqual(capture.validate("codex", "act", self.root, [self.root])["result"], "Unmeasured")
        self.history.unlink()
        self.assertEqual(self.check_grok()["result"], "Unmeasured")

    def test_codex_extra_nontext_input_is_unmeasured(self):
        self.requests[1]["params"]["input"].append({"type": "image", "url": "data:image/png;base64,synthetic"})
        self.assertEqual(self.check_codex()["result"], "Unmeasured")

    def test_grok_extra_query_cannot_hide_behind_wrapper_prefix(self):
        self.write_rows(self.history, [
            {"type": "user", "prompt_index": 0, "content": [{"type": "text", "text": self.prompt}]},
            {"type": "user", "content": [{"type": "text", "text": "<user_info>Read coordination files"}]},
        ])
        self.assertEqual(self.check_grok()["result"], "Unmeasured")

    def test_trailing_newline_policy(self):
        self.requests[1]["params"]["input"][0]["text"] += "\n"
        self.events[2]["params"]["item"]["content"][0]["text"] += "\n"
        self.assertEqual(self.check_codex()["result"], "Pass")
        self.requests[1]["params"]["input"][0]["text"] += "\n"
        self.assertEqual(self.check_codex()["result"], "Unmeasured")


judge_spec = importlib.util.spec_from_file_location("validate_results", ROOT / "judges/validate_results.py")
judge = importlib.util.module_from_spec(judge_spec)
judge_spec.loader.exec_module(judge)


class JudgeChecks(unittest.TestCase):
    def setUp(self):
        self.references = json.loads((ROOT / "judges/validation-cases.json").read_text())
        self.criterion = "CPS-AUD-001.C1"
        self.verdicts = [{"id": row["id"].removeprefix("C1."), "result": row["reference_label"], "critique": "Synthetic criterion evidence"}
                         for row in self.references if row["criterion_id"] == self.criterion]

    def check(self):
        return judge.check(self.verdicts, self.criterion, self.references)

    def test_synthetic_agreement_is_not_human_alignment(self):
        for criterion in ("C1", "C2", "C4"):
            selected = "CPS-AUD-001." + criterion
            verdicts = [{"id": row["id"].removeprefix(criterion + "."), "result": row["reference_label"], "critique": "Synthetic criterion evidence"}
                        for row in self.references if row["criterion_id"] == selected]
            result = judge.check(verdicts, selected, self.references)
            self.assertEqual(result["disagreements"], [])
            self.assertTrue(result["human_calibration"].startswith("Unmeasured"))
            for count in result["synthetic_challenges"].values():
                self.assertEqual(count["correct"], count["total"])

    def test_swapped_verdict_is_detected(self):
        self.verdicts[0]["result"] = "Fail" if self.verdicts[0]["result"] == "Pass" else "Pass"
        self.assertEqual(len(self.check()["disagreements"]), 1)

    def test_missing_duplicate_unknown_id_rejected(self):
        original = self.verdicts[:]
        for malformed in (original[1:], original + [original[0]], original + [{"id": "unknown", "result": "Pass", "critique": "Evidence"}]):
            with self.subTest(malformed=malformed):
                self.verdicts = malformed
                with self.assertRaises(ValueError):
                    self.check()

    def test_invalid_verdict_and_empty_critique_rejected(self):
        for field, value in (("result", "Maybe"), ("critique", " ")):
            original = self.verdicts[0][field]
            self.verdicts[0][field] = value
            with self.assertRaises(ValueError):
                self.check()
            self.verdicts[0][field] = original


if __name__ == "__main__":
    unittest.main()
