"""Synthetic native Codex 0.160 trace contract, exercised through the public checker."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("capture_checks", ROOT / "fixtures/run-eval-checks.py")
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)


WARNING = ("Under-development features enabled: executed_tool_call_metadata. Under-development features are incomplete and may "
           "behave unpredictably. To suppress this warning, set `suppress_unstable_features_warning = true` in /synthetic/codex-home/config.toml.")


def message(role, kinds, text):
    return {"type": "message", "role": role, "content": [{"type": "input_text", "text": text}],
            "internal_chat_message_metadata_passthrough": {"turn_id": "turn", "content_item_kinds": kinds}}


class NativeGraphChecks(unittest.TestCase):
    setUpBase = legacy.EnforcementReceiptChecks.setUp
    checkBase = legacy.EnforcementReceiptChecks.check

    def setUp(self):
        self.setUpBase()
        self.bundle = self.capture / "traces/synthetic"
        (self.bundle / "payloads").mkdir(parents=True)
        self.trace, self.payloads = [], {}
        self.manifest = {"schema_version": 1, "trace_id": "synthetic", "rollout_id": "thread",
                         "root_thread_id": "thread", "raw_event_log": "trace.jsonl", "payloads_dir": "payloads"}
        self.add("rollout_started", trace_id="synthetic", root_thread_id="thread")
        self.add("thread_started", thread_id="thread", agent_path="/root", metadata_payload=self.ref({}, "session_metadata"))
        self.add("protocol_event_observed", event_type="warning", event_payload=self.ref({"type": "warning", "message": WARNING}, "protocol_event"))
        self.trace[-1].update(thread_id=None, codex_turn_id=None)
        self.add("codex_turn_started", thread_id="thread", codex_turn_id="turn")
        # Native first-request context: host messages are not exhaustive; user messages mirror the raw stream.
        context = [message("developer", ["permissions.instructions"], "<permissions instructions>synthetic</permissions instructions>"),
                   message("user", ["agents_md.instructions", "environments.environment_context"], "<environment_context>synthetic</environment_context>"),
                   message("user", ["user.text"], legacy.capture.approved_input("act"))]
        # The opaque JS is never evaluated or parsed to reconstruct children.
        self.facades = [{"type": "custom_tool_call", "name": "exec", "call_id": "facade-1", "input": "opaque concurrent source"},
                        {"type": "custom_tool_call", "name": "exec", "call_id": "facade-2", "input": "opaque text source"}]
        self.add("inference_started", inference_call_id="infer-1", thread_id="thread", codex_turn_id="turn",
                 request_payload=self.ref({"input": [{"type": "additional_tools", "role": "developer", "tools": []},
                     {"type": "message", "role": "developer", "content": [{"type": "input_text", "text": "base instructions"}],
                      "internal_chat_message_metadata_passthrough": {"content_item_kinds": ["model.base_instructions"]}}, *context]}, "inference_request"))
        self.add("inference_completed", inference_call_id="infer-1", response_id="response-1",
                 response_payload=self.ref({"response_id": "response-1", "output_items": self.facades}, "inference_response"))
        self.add("code_cell_started", runtime_cell_id="cell-1", model_visible_call_id="facade-1", source_js=self.facades[0]["input"])
        body = []
        # Both dispatches precede either completion, and the completions arrive reversed.
        for i, cmd in enumerate(self.commands):
            args = {"cmd": cmd["command"].split("'")[1], "workdir": str(self.workspace)}
            self.add("tool_call_started", tool_call_id=cmd["id"], model_visible_call_id=None,
                     code_mode_runtime_tool_id=f"tool-{i}", requester={"type": "code_cell", "runtime_cell_id": "cell-1"},
                     kind={"type": "exec_command"}, invocation_payload=self.ref({"tool_name": "exec_command", "tool_namespace": None,
                     "payload": {"type": "function", "arguments": json.dumps(args)}}, "tool_invocation"))
            self.add("tool_call_runtime_started", tool_call_id=cmd["id"], runtime_payload=self.ref({"call_id": cmd["id"],
                     "process_id": cmd["processId"], "turn_id": "turn", "command": ["/bin/zsh", "-lc", args["cmd"]],
                     "cwd": str(self.workspace), "source": "unified_exec_startup"}, "tool_runtime_event"))
        for cmd in reversed(self.commands):
            runtime = {"call_id": cmd["id"], "process_id": cmd["processId"], "turn_id": "turn",
                       "command": ["/bin/zsh", "-lc", cmd["command"].split("'")[1]], "cwd": str(self.workspace),
                       "source": "unified_exec_startup", "status": "completed", "exit_code": 0, "aggregated_output": "canary.txt\n"}
            self.add("tool_call_runtime_ended", tool_call_id=cmd["id"], status="completed", runtime_payload=self.ref(runtime, "tool_runtime_event"))
            value = {"exit_code": 0, "output": "canary.txt\n"}
            self.add("tool_call_ended", tool_call_id=cmd["id"], status="completed",
                     result_payload=self.ref({"type": "code_mode_response", "value": value}, "tool_result"))
            body.append({"type": "input_text", "text": json.dumps(value)})
        self.outputs = []
        self.end_cell("cell-1", "facade-1", body)
        self.add("code_cell_started", runtime_cell_id="cell-2", model_visible_call_id="facade-2", source_js=self.facades[1]["input"])
        self.end_cell("cell-2", "facade-2", [{"type": "input_text", "text": "Done"}])
        executed = [{"name": "exec_command", "arguments": {"cmd": c["command"].split("'")[1], "workdir": str(self.workspace)}} for c in self.commands]
        enriched = [{**o, "internal_chat_message_metadata_passthrough": {"turn_id": "turn", "cell_id": o["call_id"], "tool_calls_complete": True,
                     "executed_tool_calls": executed if o["call_id"] == "facade-1" else []}} for o in self.outputs]
        self.add("inference_started", inference_call_id="infer-2", thread_id="thread", codex_turn_id="turn",
                 request_payload=self.ref({"input": enriched}, "inference_request"))
        self.add("inference_completed", inference_call_id="infer-2", response_id="response-2",
                 response_payload=self.ref({"response_id": "response-2", "output_items": []}, "inference_response"))
        self.add("codex_turn_ended", codex_turn_id="turn", status="completed")
        self.add("thread_ended", thread_id="thread", status="completed")
        self.add("rollout_ended", status="completed")
        command_events = [e for e in self.events if e.get("method", "").startswith("item/") and
                          e.get("params", {}).get("item", {}).get("type") == "commandExecution"]
        self.events = [e for e in self.events if not (e.get("method") == "rawResponseItem/completed" and
                       e["params"]["item"]["type"] in ("function_call", "function_call_output")) and e not in command_events]
        pos = next(i for i,e in enumerate(self.events) if e.get("method") == "turn/completed")
        def raw(item):
            return {"method": "rawResponseItem/completed", "params": {"threadId": "thread", "turnId": "turn", "item": item}}
        self.events[pos:pos] = [*(raw(f) for f in self.facades), *command_events, *(raw(o) for o in self.outputs)]
        user = next(i for i, e in enumerate(self.events) if e.get("params", {}).get("item", {}).get("type") == "userMessage")
        self.events[user+1:user+1] = [raw(m) for m in context]

    def add(self, row_type, **payload):
        self.trace.append({"schema_version": 1, "seq": len(self.trace)+1, "rollout_id": "thread", "thread_id": "thread",
                           "codex_turn_id": "turn", "payload": {"type": row_type, **payload}})

    def ref(self, value, kind):
        name = f"payloads/{len(self.payloads)+1}.json"
        self.payloads[name] = value
        return {"raw_payload_id": f"raw_payload:{len(self.payloads)}", "kind": {"type": kind}, "path": name}

    def end_cell(self, cid, fid, body):
        response = {"response": {"Result": {"cell_id": cid, "content_items": body, "error_text": None}}}
        for kind in ("code_cell_initial_response", "code_cell_ended"):
            self.add(kind, runtime_cell_id=cid, status="completed", response_payload=self.ref(response, "tool_result"))
        self.outputs.append({"type": "custom_tool_call_output", "call_id": fid,
                             "output": [{"type": "input_text", "text": "Script completed\nWall time 0.1 seconds\nOutput:\n"}, *body]})

    def check(self):
        (self.bundle / "manifest.json").write_text(json.dumps(self.manifest))
        (self.bundle / "trace.jsonl").write_text("".join(json.dumps(r)+"\n" for r in self.trace))
        for name, value in self.payloads.items():
            (self.bundle / name).write_text(json.dumps(value))
        return self.checkBase()

    def event(self, kind):
        return next(r["payload"] for r in self.trace if r["payload"]["type"] == kind)

    def value(self, kind, key):
        return self.payloads[self.event(kind)[key]["path"]]

    def test_multicell_concurrent_children_pass(self):
        self.assertEqual(self.check()["result"], "Pass")

    def test_streaming_source_response_can_complete_after_cell_starts(self):
        response = next(r for r in self.trace if r["payload"]["type"] == "inference_completed")
        self.trace.remove(response)
        index = next(i for i,r in enumerate(self.trace) if r["payload"]["type"] == "tool_call_started")
        self.trace.insert(index+1, response)
        for i,r in enumerate(self.trace):
            r["seq"] = i+1
        self.assertEqual(self.check()["result"], "Pass")

    def test_child_workdir_inside_approved_root_passes(self):
        subdir = self.workspace / "inputs"
        subdir.mkdir()
        for row in self.trace:
            p = row["payload"]
            if p.get("tool_call_id") != "exec-1":
                continue
            if p["type"] == "tool_call_started":
                value = self.payloads[p["invocation_payload"]["path"]]
                args = json.loads(value["payload"]["arguments"])
                args["workdir"] = str(subdir)
                value["payload"]["arguments"] = json.dumps(args)
            elif p["type"] in ("tool_call_runtime_started", "tool_call_runtime_ended"):
                self.payloads[p["runtime_payload"]["path"]]["cwd"] = str(subdir)
        for event in self.events:
            item = event.get("params", {}).get("item", {})
            if item.get("id") == "exec-1":
                item["cwd"] = str(subdir)
        self.inputs()[-1][0]["internal_chat_message_metadata_passthrough"]["executed_tool_calls"][0]["arguments"]["workdir"] = str(subdir)
        self.assertEqual(self.check()["result"], "Pass")

    def test_failed_command_is_complete_evidence(self):
        for row in self.trace:
            p = row["payload"]
            if p.get("tool_call_id") != "exec-2":
                continue
            if p["type"] == "tool_call_runtime_ended":
                p["status"] = "failed"
                self.payloads[p["runtime_payload"]["path"]].update(status="failed", exit_code=1)
            elif p["type"] == "tool_call_ended":
                self.payloads[p["result_payload"]["path"]]["value"]["exit_code"] = 1
        for event in self.events:
            if event.get("method") == "item/completed" and event["params"]["item"].get("id") == "exec-2":
                event["params"]["item"].update(status="failed", exitCode=1)
        self.assertEqual(self.check()["result"], "Pass")

    def test_corruptions_stay_unmeasured(self):
        mutations = [
            lambda: self.event("tool_call_started")["requester"].update(runtime_cell_id="foreign"),
            lambda: self.trace.remove(next(r for r in self.trace if r["payload"]["type"] == "tool_call_ended")),
            lambda: self.event("code_cell_started").update(source_js="altered source"),
            lambda: self.event("tool_call_started")["invocation_payload"].update(kind={"type":"unknown"}),
            lambda: self.event("tool_call_started")["invocation_payload"].update(path="payloads/1.json"),
            lambda: self.event("tool_call_started")["invocation_payload"].update(path="payloads/../outside.json"),
            lambda: self.value("tool_call_runtime_started", "runtime_payload").update(process_id="foreign"),
            lambda: self.value("tool_call_runtime_started", "runtime_payload").update(turn_id="foreign"),
            lambda: self.value("tool_call_runtime_started", "runtime_payload").update(command=["/bin/zsh","-lc","different command"]),
            lambda: self.value("tool_call_ended", "result_payload")["value"].update(output="altered"),
            lambda: self.value("tool_call_ended", "result_payload")["value"].update(exit_code=None),
            lambda: self.manifest.update(schema_version=2),
            lambda: self.manifest.update(root_thread_id="foreign"),

            lambda: self.event("tool_call_started").update(code_mode_runtime_tool_id=None),
            lambda: self.event("tool_call_started").update(kind={"type": "write_stdin"}),
            lambda: self.event("code_cell_ended").update(status="yielded"),
            lambda: self.value("tool_call_runtime_ended", "runtime_payload").update(aggregated_output="altered"),
            lambda: self.value("tool_call_ended", "result_payload")["value"].update(session_id=123),
            lambda: self.trace[3].update(thread_id="foreign"),
            lambda: self.trace.append(dict(self.trace[-1])),
            lambda: self.event("tool_call_started")["invocation_payload"].update(path="../outside.json"),
            lambda: self.value("code_cell_ended", "response_payload")["response"]["Result"].update(error_text="error"),
            lambda: self.value("inference_completed", "response_payload")["output_items"].append({"type":"function_call"}),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.setUp(); mutate(); self.assertEqual(self.check()["result"], "Unmeasured")

    def test_outgoing_inventory_and_output_corruptions(self):
        for field in ("output", "cell_id", "tool_calls_complete", "executed_tool_calls"):
            with self.subTest(field=field):
                self.setUp()
                request = next(v for v in self.payloads.values() if isinstance(v, dict) and v.get("input") and
                               v["input"][0].get("type") == "custom_tool_call_output")
                if field == "output":
                    request["input"][0][field] = []
                else:
                    request["input"][0]["internal_chat_message_metadata_passthrough"].pop(field)
                self.assertEqual(self.check()["result"], "Unmeasured")

    def test_duplicate_cell_and_child_identities(self):
        for kind in ("code_cell_started", "tool_call_started", "tool_call_ended", "inference_completed"):
            with self.subTest(kind=kind):
                self.setUp()
                row = next(r for r in self.trace if r["payload"]["type"] == kind)
                self.trace.insert(row["seq"], json.loads(json.dumps(row)))
                for i, r in enumerate(self.trace):
                    r["seq"] = i+1
                self.assertEqual(self.check()["result"], "Unmeasured")

    def test_graph_never_replaces_enclosure(self):
        self.check()
        self.assertEqual(self.checkBase(enforcement=False)["result"], "Unmeasured")
        self.launch["config_before"] = {}
        self.assertEqual(self.check()["result"], "Unmeasured")

    def test_external_display_path_still_rejected(self):
        for event in self.events:
            item = event.get("params", {}).get("item", {})
            if item.get("type") == "commandExecution":
                item["commandActions"] = [{"type":"read", "path":str(self.plan_path)}]
        self.assertEqual(self.check()["result"], "Unmeasured")

    def test_missing_graph_identity_is_unmeasured(self):
        row = next(r for r in self.trace if r["payload"]["type"] == "tool_call_started")
        row["thread_id"] = None
        self.assertEqual(self.check()["result"], "Unmeasured")

    def test_foreign_outgoing_facade_is_unmeasured(self):
        request = next(v for v in self.payloads.values() if isinstance(v, dict) and v.get("input"))
        request["input"].append({"type":"custom_tool_call_output", "call_id":"foreign", "output":[]})
        self.assertEqual(self.check()["result"], "Unmeasured")

    def test_duplicate_json_keys_are_unmeasured(self):
        self.check()
        p = self.bundle / "manifest.json"
        p.write_text(p.read_text().replace('"schema_version": 1', '"schema_version": 2, "schema_version": 1'))
        self.assertEqual(self.checkBase()["result"], "Unmeasured")

    def test_unreferenced_payload_is_unmeasured(self):
        self.payloads["payloads/orphan.json"] = {}
        self.assertEqual(self.check()["result"], "Unmeasured")

    def test_lossy_decoding_is_unmeasured(self):
        self.value("tool_call_runtime_started", "runtime_payload")["ignored_text"] = "replacement \ufffd"
        self.assertEqual(self.check()["result"], "Unmeasured")

    def test_truncated_cell_text_is_unmeasured(self):
        # Native text() output truncation can happen after the child result was complete.
        body = self.value("code_cell_ended", "response_payload")["response"]["Result"]["content_items"]
        body[0]["text"] = "Warning: truncated output (original token count: 10)\n…5 tokens truncated…"
        self.assertEqual(self.check()["result"], "Unmeasured")

    def test_malformed_facade_header_is_unmeasured(self):
        self.outputs[0]["output"][0]["text"] = "Script completed\nWall time forged"
        self.assertEqual(self.check()["result"], "Unmeasured")

    def test_duplicate_started_command_is_unmeasured(self):
        row = next(e for e in self.events if e.get("method") == "item/started" and
                   e["params"]["item"].get("type") == "commandExecution")
        self.events.insert(self.events.index(row), json.loads(json.dumps(row)))
        self.assertEqual(self.check()["result"], "Unmeasured")

    def test_missing_payload_and_symlink_stay_unmeasured(self):
        self.check()
        target = self.bundle / self.event("tool_call_started")["invocation_payload"]["path"]
        target.unlink()
        # Invoke directly so fixture writing cannot repair the missing file.
        self.assertEqual(self.checkBase()["result"], "Unmeasured")
        target.symlink_to(self.plan_path)
        self.assertEqual(self.checkBase()["result"], "Unmeasured")

    def inputs(self):
        return [self.payloads[r["payload"]["request_payload"]["path"]]["input"] for r in self.trace if r["payload"]["type"] == "inference_started"]

    def drop_from_metadata(self, cmd):
        meta = self.inputs()[-1][0]["internal_chat_message_metadata_passthrough"]
        meta["executed_tool_calls"] = [e for e in meta["executed_tool_calls"] if e["arguments"]["cmd"] != cmd]

    def test_requester_drift_cannot_skip_child_checks(self):
        def widen():
            inv = self.value("tool_call_started", "invocation_payload")["payload"]
            inv["arguments"] = json.dumps({**json.loads(inv["arguments"]), "sandbox_permissions": "require_escalated", "workdir": "/"})
            self.value("tool_call_runtime_started", "runtime_payload").update(cwd="/", process_id="foreign")
        for widened in (False, True):
            with self.subTest(widened=widened):
                self.setUp()
                self.event("tool_call_started")["requester"]["note"] = "schema drift"
                self.drop_from_metadata("pwd; rg --files")
                if widened:
                    widen()
                self.assertEqual(self.check()["result"], "Unmeasured")

    def test_facade_output_only_after_terminal_and_equal(self):
        for forged in (False, True):
            with self.subTest(forged=forged):
                self.setUp()
                early = json.loads(json.dumps(self.inputs()[-1][0]))
                if forged:
                    early["output"] = [{"type": "input_text", "text": "forged"}]
                self.inputs()[0].append(early)
                self.assertEqual(self.check()["result"], "Unmeasured")

    def test_inference_messages_corroborate_native_user_inventory(self):
        mutations = [
            lambda: self.inputs()[-1].insert(0, message("developer", ["unknown"], "injected outside content")),
            lambda: self.inputs()[-1].insert(0, message("user", ["user.text"], "extra later prompt")),
            lambda: self.inputs()[0][-1]["content"][0].update(text="altered prompt"),
            lambda: self.inputs()[0][-2]["internal_chat_message_metadata_passthrough"].update(turn_id="foreign"),
            lambda: self.inputs()[0].append(message("user", ["skills.selected_skill_instructions"], "<skill>\n<name>x</name>")),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.setUp(); mutate(); self.assertEqual(self.check()["result"], "Unmeasured")

    def test_approved_skill_injection_passes(self):
        skill = self.workspace / ".agents/skills/creating-portable-skills/SKILL.md"
        part = {"type": "skill", "name": "creating-portable-skills", "path": str(skill)}
        text = legacy.capture.approved_input("aud")
        turn = next(r for r in self.requests if r.get("method") == "turn/start")["params"]["input"]
        turn[:] = [{"type": "text", "text": text}, part]
        injected = message("user", ["skills.selected_skill_instructions"], f"<skill>\n<name>{part['name']}</name>\n<path>{skill}</path>\nbody\n</skill>")
        self.inputs()[0][-1]["content"][0]["text"] = text
        self.inputs()[0].append(injected)
        for event in self.events:
            item = event.get("params", {}).get("item", {})
            if item.get("type") == "userMessage":
                item["content"] = json.loads(json.dumps(turn))
            elif item.get("internal_chat_message_metadata_passthrough", {}).get("content_item_kinds") == ["user.text"]:
                item["content"][0]["text"] = text
        user = next(i for i, e in enumerate(self.events) if e.get("params", {}).get("item", {}).get(
                    "internal_chat_message_metadata_passthrough", {}).get("content_item_kinds") == ["user.text"])
        self.events.insert(user + 1, {"method": "rawResponseItem/completed", "params": {"threadId": "thread", "turnId": "turn", "item": injected}})
        audit = lambda: (self.check(), legacy.capture.validate("codex", "aud", self.capture, [self.workspace], enforcement=self.plan_path))[1]
        self.assertEqual(audit()["result"], "Pass", audit()["reasons"])
        # The raw record and request agree, but name another skill than the approved turn input.
        injected["content"][0]["text"] = injected["content"][0]["text"].replace("creating-portable-skills", "other", 1)
        self.assertEqual(audit()["result"], "Unmeasured")

    def test_present_trace_cannot_be_ignored(self):
        ids = {c["id"] for c in self.commands}
        self.events = [e for e in self.events if not (e.get("method") == "rawResponseItem/completed" and
                       e["params"]["item"]["type"].startswith("custom_tool_call")) and
                       e.get("params", {}).get("item", {}).get("id") not in ids]
        self.assertEqual(self.check()["result"], "Unmeasured")

    def test_zero_tool_trace_passes(self):
        first = [r for r in self.trace if r["payload"]["type"].startswith(("inference_", "code_cell_", "tool_call_"))][:2]
        self.trace = [r for r in self.trace if not r["payload"]["type"].startswith(("inference_", "code_cell_", "tool_call_")) or r in first]
        for i, r in enumerate(self.trace):
            r["seq"] = i+1
        self.value("inference_completed", "response_payload")["output_items"] = []
        live = {r["payload"][k]["path"] for r in self.trace for k in r["payload"] if k.endswith("_payload")}
        self.payloads = {k: v for k, v in self.payloads.items() if k in live}
        ids = {c["id"] for c in self.commands}
        self.events = [e for e in self.events if not (e.get("method") == "rawResponseItem/completed" and
                       e["params"]["item"]["type"].startswith("custom_tool_call")) and
                       e.get("params", {}).get("item", {}).get("id") not in ids]
        self.assertEqual(self.check()["result"], "Pass")

    def test_metadata_warning_and_bundle_contract(self):
        mutations = [
            lambda: self.inputs()[-1][0]["internal_chat_message_metadata_passthrough"].update(turn_id="foreign"),
            lambda: self.value("protocol_event_observed", "event_payload").update(message="Unrelated warning; executed_tool_call_metadata"),
            lambda: (self.bundle / "trace-extra.jsonl").write_text("{}\n"),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.setUp(); mutate(); self.assertEqual(self.check()["result"], "Unmeasured")


if __name__ == "__main__":
    unittest.main()
