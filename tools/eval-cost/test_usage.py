import json
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import os
from pathlib import Path
import usage

class UsageTests(unittest.TestCase):
    def test_claude_uses_last_complete_model_totals(self):
        events = [
            {"type": "assistant", "message": {"usage": {"output_tokens": 3}}},
            {"type": "result", "modelUsage": {"example-model": {"inputTokens": 1, "outputTokens": 20, "cacheReadInputTokens": 10, "cacheCreationInputTokens": 5}}},
            {"type": "result", "modelUsage": {"example-model": {"inputTokens": 2, "outputTokens": 40, "cacheReadInputTokens": 20, "cacheCreationInputTokens": 10}}},
        ]
        rows = usage.claude_rows(events, "2026-09-26T12:00:00Z")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["message"]["usage"]["output_tokens"], 40)
        self.assertEqual(rows[0]["message"]["usage"]["input_tokens"], 2)

    def test_unknown_price_does_not_become_free(self):
        report = {"sessions": [{"modelsUsed": ["new-model"]}], "totals": {"totalCost": 0, "totalTokens": 100}}
        with self.assertRaises(ValueError):
            usage.checked_totals(report)

    def test_cost_and_tokens_are_finite_nonnegative(self):
        for value in [-1, float("nan"), float("inf"), True]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                usage.checked_totals({"sessions": [{}], "totals": {"totalCost": value, "totalTokens": 100}})

    def test_codex_fallback_model_is_not_priced_as_actual(self):
        report = {"sessions": [{"models": {"gpt-fallback": {"isFallback": True}}}], "totals": {"costUSD": .1, "totalTokens": 100}}
        with self.assertRaises(ValueError):
            usage.checked_totals(report)

    def test_mixed_known_and_unknown_prices_reject_partial_total(self):
        report = {"sessions": [{"modelBreakdowns": [{"cost": .1}, {"cost": 0, "missingPricing": True}]}], "totals": {"totalCost": .1, "totalTokens": 100, "unpricedModels": ["future-model"]}}
        with self.assertRaises(ValueError):
            usage.checked_totals(report)

    def test_complete_report_uses_reported_grain(self):
        report = {"sessions": [{}, {}], "totals": {"costUSD": .115, "totalTokens": 185486}}
        self.assertEqual(usage.checked_totals(report), (.115, 185486))

    def test_grok_prices_completed_aggregate_once_in_isolated_config(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            sessions = root / "saved"
            for name, kind in [("parent", "headless"), ("child", "subagent"), ("resumed", "subagent_resume")]:
                d = sessions / name
                d.mkdir(parents=True)
                (d / "summary.json").write_text(json.dumps({"session_kind": kind}))
                (d / "updates.jsonl").write_text(name)
            transcript = root / "transcript"
            transcript.write_text(json.dumps({"type": "end", "modelUsage": {
                "grok-model": {"inputTokens": 60, "outputTokens": 30,
                               "cacheReadInputTokens": 10, "cacheCreationInputTokens": 0}}}))
            def invoke(argv, **kw):
                self.assertNotIn("OPENAI_API_KEY", kw["env"])
                if "--version" in argv:
                    return SimpleNamespace(stdout="ccusage test", stderr="")
                self.assertEqual(argv[1:4], ["grok", "session", "--json"])
                self.assertEqual(argv[argv.index("--mode") + 1], "calculate")
                self.assertEqual(Path(argv[argv.index("--config") + 1]).read_text(), "{}\n")
                files = list(Path(kw["env"]["GROK_HOME"]).rglob("updates.jsonl"))
                self.assertEqual(len(files), 1)
                data = json.loads(files[0].read_text())["params"]["update"]["usage"]
                self.assertEqual(data["totalTokens"], 100)
                self.assertEqual(data["modelUsage"]["grok-model"]["inputTokens"], 70)
                return SimpleNamespace(stdout=json.dumps({"sessions": [{}], "totals": {"totalCost": .1, "totalTokens": 100}}), stderr="")
            with patch.dict(os.environ, {"OPENAI_API_KEY": "must-not-propagate"}), patch("usage.subprocess.run", side_effect=invoke):
                result = usage.estimate("grok", transcript, sessions, root / "cost.json", ["ccusage"], root)
            self.assertEqual(result["cost_usd"], .1)
            self.assertEqual((sessions / "child/updates.jsonl").read_text(), "child")

    def test_missing_cli_is_recorded_as_unknown(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            trace = root / "trace"
            trace.write_text('{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n')
            with patch("usage.subprocess.run", side_effect=FileNotFoundError("ccusage unavailable")):
                record = usage.estimate("codex", trace, None, root / "cost.json", ["ccusage"], root, model="recorded-model")
            self.assertIsNone(record["cost_usd"])
            self.assertIn("unavailable", record["error"])
            self.assertEqual(json.loads((root / "cost.json").read_text()), record)

    def test_corrupt_usage_record_is_unknown_without_pricing(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            trace = root / "trace"
            trace.write_text('{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n{"type":')
            with patch("usage.subprocess.run") as invoke:
                record = usage.estimate("codex", trace, None, root / "cost.json", ["ccusage"], root, model="recorded-model")
                invoke.assert_not_called()
            self.assertIsNone(record["cost_usd"])
            self.assertIn("JSONL", record["error"])

    def test_explicit_native_store_must_exist_and_be_a_directory(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            trace = root / "trace"
            trace.write_text('{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n')
            for sessions in (root / "missing", trace):
                with self.subTest(sessions=sessions), patch("usage.subprocess.run") as invoke:
                    record = usage.estimate("codex", trace, sessions, None, ["ccusage"], root, "recorded-model")
                    self.assertIn("directory", record["error"])
                    invoke.assert_not_called()

    def test_native_usage_can_price_a_failed_call(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            trace = root / "trace"
            trace.write_text('{"type":"turn.failed","error":{"message":"tool failed"}}\n')
            sessions = root / "saved"
            sessions.mkdir()
            (sessions / "run.jsonl").write_text('{"type":"event_msg","payload":{"type":"token_count"}}\n')
            def invoke(argv, **kw):
                if "--version" in argv:
                    return SimpleNamespace(stdout="test", stderr="")
                self.assertTrue((Path(kw["env"]["CODEX_HOME"]) / "sessions/run.jsonl").is_file())
                return SimpleNamespace(stdout=json.dumps({"sessions": [{}], "totals": {"costUSD": .1, "totalTokens": 100}}), stderr="")
            with patch("usage.subprocess.run", side_effect=invoke):
                record = usage.estimate("codex", trace, sessions, None, ["ccusage"], root)
            self.assertEqual(record["cost_usd"], .1)
            with patch("usage.subprocess.run") as invoke:
                record = usage.estimate("codex", trace, None, None, ["ccusage"], root, "recorded-model")
                invoke.assert_not_called()
            self.assertIsNone(record["cost_usd"])

    def test_tool_enabled_codex_requires_native_records(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            trace = root / "trace"
            trace.write_text('{"type":"item.completed","item":{"type":"command_execution"}}\n{"type":"turn.completed","usage":{"input_tokens":100,"output_tokens":10}}\n')
            with patch("usage.subprocess.run") as invoke:
                record = usage.estimate("codex", trace, None, root / "cost.json", ["ccusage"], root, model="recorded-model")
                invoke.assert_not_called()
            self.assertIsNone(record["cost_usd"])
            self.assertIn("native", record["error"])

if __name__ == "__main__": unittest.main()
