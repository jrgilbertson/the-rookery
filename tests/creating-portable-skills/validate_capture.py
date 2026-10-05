"""Check native capture admissibility, separately from behavioral criterion grades."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shlex


ROOT = Path(__file__).resolve().parent
CASES = {"act": "activation-near-miss.md", "aud": "vendor-guidance-audit.md",
         "author": "activation-authoring.md", "review": "activation-explicit-review.md",
         "writing": "activation-writing-near-miss.md"}
# Fixed native profile and tool surface that an enforcement receipt may vouch for.
PROFILE = {"extends": ":read-only", "filesystem": {":root": "deny", ":minimal": "read", ":workspace_roots": "read", ":tmpdir": "deny", ":slash_tmp": "deny"}, "network": {"enabled": False}}
TOOLS = {"web_search": "disabled", "enabled_mcp_servers": [], "nextCursor": None,
         "features": dict.fromkeys(("view_image", "plugins", "apps", "browser_use", "computer_use", "image_generation",
                                    "multi_agent", "multi_agent_v2", "hooks", "memories", "memory_tool"), False)}
CLIENT_METHODS = {"initialize", "account/read", "skills/list", "thread/start", "config/read", "mcpServerStatus/list", "command/exec", "turn/start", "thread/read"}
RAW_CALLS = {"exec_command", "write_stdin", "clock.sleep"}
DENIED = ("Operation not permitted", "PermissionError")  # EPERM, never a missing path.
SHA256 = re.compile("[0-9a-f]{64}")
SHELLS = ("/bin/zsh", "/bin/bash", "/bin/sh")
# Any shell syntax beyond words and single quotes: operators, substitution, comments, globs, escapes.
SHELL_SYNTAX = set(";&|<>()$`\\\"\n\r#*?[]{}~!^")
# Codex 0.160 protocol event_type and the payload type it carries.
PROTOCOL_EVENTS = {"session_configured": "session_configured", "warning": "warning", "turn_started": "task_started",
                   "turn_complete": "task_complete", "shutdown_complete": "shutdown_complete"}


def probe_target(argv, wrappers=2):
    """Return the one absolute file a structurally known read probe opens, else None.

    Supported: /bin/cat TARGET and /bin/dd if=TARGET of=/dev/null count=0, optionally
    inside at most two exact `SHELL -c|-lc SCRIPT` wrappers. This is a closed grammar,
    not a shell parser; any other form or shell syntax is unknown.
    """
    if wrappers and len(argv) == 3 and argv[0] in SHELLS and argv[1] in ("-c", "-lc"):
        if SHELL_SYNTAX & set(argv[2]):
            return None
        try:
            return probe_target(shlex.split(argv[2]), wrappers - 1)
        except ValueError:
            return None
    if len(argv) == 2 and argv[0] == "/bin/cat":
        target = argv[1]
    elif len(argv) == 4 and argv[0] == "/bin/dd" and argv[1].startswith("if=") and argv[2:] == ["of=/dev/null", "count=0"]:
        target = argv[1].removeprefix("if=")
    else:
        return None
    return target if Path(target).is_absolute() else None


def approved_input(case):
    """Read the canonical INPUT section; allow one transport newline only."""
    text = (ROOT / "cases" / CASES[case]).read_text()
    return text.split(".INPUT\n\n", 1)[1].split("\n\n## ", 1)[0].rstrip("\n")


def prompt_matches(text, approved):
    return text in (approved, approved + "\n")


def rows(path):
    data = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not data or not all(isinstance(row, dict) for row in data):
        raise ValueError("empty or malformed native capture: " + str(path))
    return data


def text_input(content):
    return "".join(part.get("text", "") for part in content if part.get("type") == "text")


def verify_native_graph(directory, raw, commands, thread_id, turn_id, workspace, turn_input):
    """Consume Codex 0.160 schema-1 synchronous exec graphs, without interpreting JS.

    Contract: openai/codex rust-v0.160.0, rollout-trace/src/raw_event.rs and
    core/src/tools/code_mode/{output,delegate}.rs. Raw trace instrumentation and
    executed_tool_call_metadata must be enabled. Display actions are not edges.
    First-request developer and user messages are corroborated against the raw stream;
    base instructions, additional tools and the selected skill body are not attested,
    and neither source is authenticated. The caller verifies the confinement receipt.
    """
    import shlex

    def require(condition, reason):
        if not condition:
            raise ValueError("Native exec graph: " + reason)

    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    def load(path):
        text = path.read_text(encoding="utf-8")
        require("\ufffd" not in text, "lossy payload decoding")
        value = json.loads(text, object_pairs_hook=object_pairs)
        require("\ufffd" not in json.dumps(value, ensure_ascii=False), "lossy payload decoding")
        return value

    def regular(path):
        require(path.is_file() and not path.is_symlink(), "missing or linked trace file")

    trace_root = directory / "traces"
    require(trace_root.is_dir() and not trace_root.is_symlink(), "missing or linked traces directory")
    bundles = list(trace_root.iterdir())
    require(len(bundles) == 1 and bundles[0].is_dir() and not bundles[0].is_symlink(), "expected one native bundle")
    bundle = bundles[0]
    require({p.name for p in bundle.iterdir()} == {"manifest.json", "trace.jsonl", "payloads"}, "unexpected bundle files")
    for name in ("manifest.json", "trace.jsonl"):
        regular(bundle / name)
    manifest = load(bundle / "manifest.json")
    require(type(manifest["schema_version"]) is int and manifest["schema_version"] == 1 and manifest["root_thread_id"] == manifest["rollout_id"] == thread_id and
            manifest["raw_event_log"] == "trace.jsonl" and manifest["payloads_dir"] == "payloads", "manifest identity/schema")
    trace = [json.loads(line, object_pairs_hook=object_pairs) for line in (bundle / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
    kinds = {"rollout_started", "rollout_ended", "thread_started", "thread_ended", "codex_turn_started", "codex_turn_ended",
             "inference_started", "inference_completed", "protocol_event_observed", "code_cell_started", "code_cell_initial_response",
             "code_cell_ended", "tool_call_started", "tool_call_runtime_started", "tool_call_runtime_ended", "tool_call_ended"}
    require(trace and [r["seq"] for r in trace] == list(range(1, len(trace)+1)), "incomplete sequence")
    for row in trace:
        require("\ufffd" not in json.dumps(row, ensure_ascii=False), "lossy trace decoding")
        p = row["payload"]
        require(type(row["seq"]) is int and type(row["schema_version"]) is int and row["schema_version"] == 1 and row["rollout_id"] == thread_id and p["type"] in kinds and
                row["thread_id"] in (None, thread_id) and row["codex_turn_id"] in (None, turn_id), "foreign or unsupported event")
        if p["type"].startswith(("inference_", "code_cell_", "tool_call_")):
            require(row["thread_id"] == thread_id and row["codex_turn_id"] == turn_id, "missing graph thread/turn identity")
        require(p.get("thread_id", thread_id) == thread_id and p.get("codex_turn_id", turn_id) == turn_id,
                "foreign payload identity")
    require(trace[0]["payload"] == {"type": "rollout_started", "trace_id": manifest["trace_id"], "root_thread_id": thread_id} and
            trace[-1]["payload"] == {"type": "rollout_ended", "status": "completed"}, "rollout lifecycle")

    def bykind(kind):
        return [r for r in trace if r["payload"]["type"] == kind]

    for start, end in (("thread_started", "thread_ended"), ("codex_turn_started", "codex_turn_ended")):
        require(len(bykind(start)) == len(bykind(end)) == 1 and bykind(start)[0]["seq"] < bykind(end)[0]["seq"] and
                bykind(end)[0]["payload"]["status"] == "completed", "thread/turn lifecycle")
    thread_start, thread_end = bykind("thread_started")[0]["seq"], bykind("thread_ended")[0]["seq"]
    turn_start, turn_end = bykind("codex_turn_started")[0]["seq"], bykind("codex_turn_ended")[0]["seq"]
    require(thread_start < turn_start < turn_end < thread_end, "turn lifecycle outside thread")
    for row in trace:
        if row["payload"]["type"].startswith(("inference_", "code_cell_", "tool_call_")):
            require(turn_start < row["seq"] < turn_end, "graph work outside native turn")
    payload_dir = bundle / "payloads"
    require(payload_dir.is_dir() and not payload_dir.is_symlink(), "missing or linked payload directory")
    payloads, paths = {}, set()
    ref_kinds = {"metadata_payload": "session_metadata", "event_payload": "protocol_event", "request_payload": "inference_request",
                 "invocation_payload": "tool_invocation", "runtime_payload": "tool_runtime_event", "result_payload": "tool_result"}
    for row in trace:
        for key, ref in row["payload"].items():
            if key.endswith("_payload"):
                require(isinstance(ref, dict), "missing raw payload reference")
                path = ref["path"]
                require(isinstance(path, str) and len(path.split("/")) == 2 and path.split("/")[0] == "payloads" and
                        path.split("/")[1] not in ("", ".", "..") and "\\" not in path, "payload path escapes bundle")
                target = bundle / path
                regular(target)
                require(target.resolve().is_relative_to(payload_dir.resolve()), "payload escapes root")
                rid = ref["raw_payload_id"]
                require(isinstance(rid, str) and rid and rid not in payloads and path not in paths, "duplicate payload reference")
                expected = ("inference_response" if row["payload"]["type"] == "inference_completed" else "tool_result") if key == "response_payload" else ref_kinds[key]
                require(ref["kind"] == {"type": expected}, "unsupported payload kind")
                payloads[rid] = load(target)
                paths.add(path)
    require(paths == {"payloads/" + p.name for p in payload_dir.iterdir()}, "unreferenced or missing payload files")
    pv = lambda ref: payloads[ref["raw_payload_id"]]

    def indexed(kind, key):
        data = bykind(kind)
        ids = [r["payload"][key] for r in data]
        require(all(isinstance(i, str) and i for i in ids) and len(ids) == len(set(ids)), "duplicate/malformed " + kind + " identity")
        return {r["payload"][key]: r for r in data}

    def paired(start, ends, key):
        first = indexed(start, key)
        rest = [indexed(end, key) for end in ends]
        require(all(set(x) == set(first) for x in rest), "missing or foreign " + start + " lifecycle")
        for identity, row in first.items():
            require(row["seq"] < min(x[identity]["seq"] for x in rest), "invalid " + start + " lifecycle order")
        return (first, *rest)

    inferences, responses = paired("inference_started", ["inference_completed"], "inference_call_id")
    cells, initials, terminals = paired("code_cell_started", ["code_cell_initial_response", "code_cell_ended"], "runtime_cell_id")
    dispatches, runtime_starts, runtime_ends, ends = paired("tool_call_started",
        ["tool_call_runtime_started", "tool_call_runtime_ended", "tool_call_ended"], "tool_call_id")
    require(set(dispatches) == set(commands), "command items do not biject native children")
    facades, outputs = {}, {}
    for item in raw:
        require("\ufffd" not in json.dumps(item, ensure_ascii=False), "lossy raw facade decoding")
        kind = item["type"]
        require(kind in ("message", "reasoning", "custom_tool_call", "custom_tool_call_output"), "unsupported model tool/item class")
        if kind in ("custom_tool_call", "custom_tool_call_output"):
            target = facades if kind == "custom_tool_call" else outputs
            fid = item["call_id"]
            require(isinstance(fid, str) and fid and fid not in target, "duplicate facade identity")
            require(kind != "custom_tool_call" or item["name"] == "exec", "unsupported facade")
            require(kind != "custom_tool_call_output" or fid in facades, "facade output precedes raw call")
            target[fid] = item
    require(set(facades) == set(outputs) and Counter(r["payload"]["model_visible_call_id"] for r in cells.values()) == Counter({f:1 for f in facades}), "facade/cell inventory")
    model_calls = []
    for row in responses.values():
        rsp = pv(row["payload"]["response_payload"])
        require(rsp["response_id"] == row["payload"]["response_id"], "inference response identity")
        model_calls.extend(i for i in rsp["output_items"] if i["type"] not in ("message", "reasoning"))
    require(Counter(json.dumps(i, sort_keys=True) for i in model_calls) ==
            Counter(json.dumps(i, sort_keys=True) for i in facades.values()), "inference/raw facade inventory differs")
    require(len({r["payload"]["response_id"] for r in responses.values()}) == len(responses), "duplicate inference response")
    first = min(inferences.values(), key=lambda r: r["seq"]) if inferences else None
    requested = []
    for row in inferences.values():
        for item in pv(row["payload"]["request_payload"])["input"]:
            kind = item["type"]
            require(kind in ("message", "reasoning", "additional_tools", "custom_tool_call", "custom_tool_call_output"),
                    "unsupported inference input item")
            # Later native requests are incremental, so context messages belong to the first one only.
            require(kind != "message" or row is first, "message outside first native request")
            # A fresh thread's first request carries context only, never prior model history.
            require(row is not first or kind in ("message", "additional_tools"), "history in first native request")
            if kind == "message":
                requested.append(item)
            if kind == "custom_tool_call_output":
                require(item["call_id"] in outputs, "foreign outgoing facade output")
            elif kind == "custom_tool_call":
                require(item["call_id"] in facades and item["name"] == "exec" and item["input"] == facades[item["call_id"]]["input"],
                        "foreign outgoing facade call")

    kinds_of = lambda item: item.get("internal_chat_message_metadata_passthrough", {}).get("content_item_kinds")
    streamed = [i for i in raw if i["type"] == "message"]
    require(all(item.get("internal_chat_message_metadata_passthrough", {}).get("turn_id", turn_id) == turn_id for item in requested + streamed),
            "message from a foreign native turn")
    require(all(i.get("role") in ("developer", "user") for i in requested), "unsupported role in native request")
    # The raw stream mirrors every request context message except the developer base instructions.
    context = lambda items: Counter(json.dumps(i, sort_keys=True) for i in items if i.get("role") in ("developer", "user") and
                                    not (i["role"] == "developer" and kinds_of(i) == ["model.base_instructions"]))
    require(context(requested) == context(streamed), "native context messages differ between request and raw stream")
    sent = [i for i in requested if i.get("role") == "user"]
    require([i["content"] for i in sent if kinds_of(i) == ["user.text"]] ==
            [[{"type": "input_text", "text": part["text"]} for part in turn_input if part["type"] == "text"]], "native request prompt differs from approved turn input")
    skills = [f"<skill>\n<name>{part['name']}</name>\n<path>{part['path']}</path>\n" for part in turn_input if part["type"] == "skill"]
    injected = [i["content"] for i in sent if kinds_of(i) == ["skills.selected_skill_instructions"]]
    require(len(injected) == len(skills) and all(len(content) == 1 and content[0]["type"] == "input_text" and content[0]["text"].startswith(prefix)
                                                 for content, prefix in zip(injected, skills)), "native skill injection differs from approved turn input")

    # Trace-side session facts must agree with the receipt's cwd, approval policy and read-only profile.
    meta = pv(bykind("thread_started")[0]["payload"]["metadata_payload"])
    require((meta["thread_id"], meta["cwd"], meta["approval_policy"], meta["sandbox_policy"]) ==
            (thread_id, str(workspace), "never", "ReadOnly { network_access: false }"), "native session metadata differs from receipt")
    configured = [pv(r["payload"]["event_payload"]) for r in bykind("protocol_event_observed") if r["payload"]["event_type"] == "session_configured"]
    require(len(configured) == 1 and (configured[0]["thread_id"], configured[0]["cwd"], configured[0]["approval_policy"],
                                      configured[0]["active_permission_profile"]) ==
            (thread_id, str(workspace), "never", {"id": "preflight", "extends": ":read-only"}), "native session configuration differs from receipt")
    for row in bykind("protocol_event_observed"):
        p = row["payload"]
        require(p["event_type"] in PROTOCOL_EVENTS and pv(p["event_payload"]).get("type") == PROTOCOL_EVENTS[p["event_type"]],
                "unsupported protocol event")
        if p["event_type"] == "warning":
            # The only accepted warning is the one the required feature flag emits in 0.160.
            warning = pv(p["event_payload"])
            require(set(warning) == {"type", "message"} and warning["type"] == "warning" and isinstance(warning["message"], str) and
                    re.fullmatch(r"Under-development features enabled: executed_tool_call_metadata\. Under-development features are incomplete "
                                 r"and may behave unpredictably\. To suppress this warning, set `suppress_unstable_features_warning = true` "
                                 r"in [^\n]+/config\.toml\.", warning["message"]), "unsupported warning")
    for cid, cell in cells.items():
        c = cell["payload"]
        fid = c["model_visible_call_id"]
        require(c["source_js"] == facades[fid]["input"], "facade source differs")
        source_responses = [r for r in responses.values() if any(i.get("call_id") == fid for i in
                            pv(r["payload"]["response_payload"])["output_items"])]
        require(len(source_responses) == 1 and
                inferences[source_responses[0]["payload"]["inference_call_id"]]["seq"] < cell["seq"],
                "cell lacks identified source inference")

        children = [r for r in dispatches.values() if r["payload"]["requester"] == {"type": "code_cell", "runtime_cell_id": cid}]
        runtime_ids = [r["payload"]["code_mode_runtime_tool_id"] for r in children]
        require(all(isinstance(i, str) and i for i in runtime_ids) and len(set(runtime_ids)) == len(runtime_ids), "duplicate/missing runtime child identity")
        executed = []
        for child in children:
            d = child["payload"]
            bid = d["tool_call_id"]
            cmd = commands[bid]
            require(d["model_visible_call_id"] is None and d["kind"] == {"type": "exec_command"}, "unsupported nested tool")
            require(cell["seq"] < child["seq"] < runtime_starts[bid]["seq"] < runtime_ends[bid]["seq"] < ends[bid]["seq"] < initials[cid]["seq"] <= terminals[cid]["seq"], "child lifecycle outside synchronous cell")
            inv = pv(d["invocation_payload"])
            require(inv["tool_name"] == "exec_command" and inv["tool_namespace"] is None and inv["payload"]["type"] == "function", "unsupported invocation")
            args = json.loads(inv["payload"]["arguments"], object_pairs_hook=object_pairs)
            require(isinstance(args, dict) and isinstance(args.get("cmd"), str) and args.get("sandbox_permissions") in (None, "use_default") and
                    args.get("additional_permissions") is None and (args.get("workdir") is None or isinstance(args["workdir"], str)),
                    "child permissions/cwd widened")
            executed.append({"name": "exec_command", "arguments": args})
            rs = pv(runtime_starts[bid]["payload"]["runtime_payload"])
            re_ = pv(runtime_ends[bid]["payload"]["runtime_payload"])
            res = pv(ends[bid]["payload"]["result_payload"])
            require(ends[bid]["payload"]["status"] == "completed" and
                    runtime_ends[bid]["payload"]["status"] == cmd["status"] and cmd["status"] in ("completed", "failed") and
                    res["type"] == "code_mode_response" and "session_id" not in res["value"], "incomplete nested execution")
            require(rs["call_id"] == re_["call_id"] == bid and rs["process_id"] == re_["process_id"] == cmd["processId"] and
                    rs["turn_id"] == re_["turn_id"] == turn_id and rs["cwd"] == re_["cwd"] == cmd["cwd"] and
                    Path(cmd["cwd"]).is_absolute() and Path(cmd["cwd"]).resolve().is_relative_to(workspace) and
                    Path(cmd["cwd"]).resolve() == (workspace / (args.get("workdir") or ".")).resolve() and
                    rs["command"] == re_["command"] == shlex.split(cmd["command"]) and rs["command"][-1] == args["cmd"] and
                    rs["source"] == re_["source"] == "unified_exec_startup", "command identity/payload differs")
            require(re_["aggregated_output"] == cmd["aggregatedOutput"] == res["value"]["output"] and
                    re_["exit_code"] == cmd["exitCode"] == res["value"]["exit_code"] and re_["status"] == cmd["status"] and
                    isinstance(res["value"]["output"], str) and type(res["value"]["exit_code"]) is int, "lossy or altered command result")
        initial, terminal = initials[cid]["payload"], terminals[cid]["payload"]
        ir, tr = pv(initial["response_payload"]), pv(terminal["response_payload"])
        require(ir == tr and initial["status"] == terminal["status"] == "completed" and set(tr["response"]) == {"Result"}, "yielded/failed/altered cell response")
        result = tr["response"]["Result"]
        output = outputs[fid]["output"]
        require(result["cell_id"] == cid and result["error_text"] is None and isinstance(output, list) and output and
                output[0]["type"] == "input_text" and
                re.fullmatch(r"Script completed\nWall time \d+\.\d+ seconds(?: \(code-mode \d+\.\d+ seconds; overhead -?\d+\.\d+ seconds\))?\nOutput:\n", output[0]["text"]) and
                result["content_items"] == output[1:], "facade output differs from native cell")
        for content in result["content_items"]:
            require(content.get("type") == "input_text" and isinstance(content.get("text"), str) and
                    not re.search(r"…\d+ tokens truncated…|Warning: truncated output \(original token count: \d+\)", content["text"]),
                    "unsupported or truncated cell output")
        enriched = [(r["seq"], i) for r in inferences.values()
                    for i in pv(r["payload"]["request_payload"])["input"] if i.get("type") == "custom_tool_call_output" and i.get("call_id") == fid]
        require(enriched and all(seq > terminals[cid]["seq"] for seq, _ in enriched), "facade output missing or sent before native cell terminal")
        for _, item in enriched:
            meta = item.get("internal_chat_message_metadata_passthrough", {})
            require(item["output"] == output and meta.get("cell_id") == fid and meta.get("turn_id") == turn_id and meta.get("tool_calls_complete") is True and
                    Counter(json.dumps(i, sort_keys=True) for i in meta.get("executed_tool_calls", [])) ==
                    Counter(json.dumps(i, sort_keys=True) for i in executed), "incomplete/altered outgoing child inventory or output")
    # The same exact requester predicate that selected per-child checks.
    require(all(r["payload"]["requester"] in ({"type": "code_cell", "runtime_cell_id": cid} for cid in cells) for r in dispatches.values()),
            "orphan native child")


def verify_enforcement(plan, plan_path, directory, roots, requests, events, trailer, thread_id, turn_id, started_items, completed):
    """Recompute a same-server confinement receipt from raw native streams and a frozen operator plan."""
    problems = []

    def check(condition, reason):
        if not condition:
            problems.append("Enforcement receipt: " + reason)

    cwd, probes, expected, hashes = plan["cwd"], plan["probe_params"], plan["probe_expectations"], plan["config_sha256"]
    workspace = Path(cwd).resolve()
    check(plan["version"] == 1 and plan["profile"] == "preflight", "unsupported plan version or profile")
    check(Path(cwd).is_absolute() and roots == [workspace], "plan cwd is not the single approved read root")
    check(isinstance(plan["argv"], list) and plan["argv"] and all(isinstance(arg, str) for arg in plan["argv"]), "malformed approved argv")
    check(all(SHA256.fullmatch(plan[key]) for key in ("launcher_sha256", "binary_sha256")) and hashes and
          all(isinstance(path, str) and SHA256.fullmatch(value) for path, value in hashes.items()), "malformed pinned hashes")
    check(plan["expected_tool_configuration"] == TOOLS, "plan widens the required tool configuration")
    check(len(probes) == len(expected), "probe plan and expectations are misaligned")
    for params, want in zip(probes, expected):
        check(set(params) <= {"command", "cwd", "permissionProfile", "timeoutMs"} and params["cwd"] == cwd and
              params["permissionProfile"] == plan["profile"] and params["command"] and all(isinstance(arg, str) for arg in params["command"]),
              "probe is not bound to the approved workspace and profile: " + json.dumps(params))
        check(probe_target(params["command"]) is not None, "probe is not a known read of one absolute path: " + json.dumps(params["command"]))
        check(set(want) == {"exitCode", "stdout", "stderr_contains"} and want["exitCode"] in (0, 1) and type(want["exitCode"]) is int and
              isinstance(want["stdout"], str) and (want["exitCode"] == 0 or any(marker in str(want["stderr_contains"]) for marker in DENIED)),
              "deny probe must expect a permission error with exit 1, not a missing path")
    nonces = [want["stdout"] for want in expected if want["exitCode"] == 0 and want["stdout"].strip()]
    denied = {probe_target(params["command"]) for params, want in zip(probes, expected) if want["exitCode"] == 1}
    check(nonces and denied, "plan lacks an allow canary or a deny probe")
    protected = plan["protected_paths"]
    # Coverage is the exact read target, never text that merely appears in a probe.
    check(protected and all(Path(path).is_absolute() and path in denied for path in protected),
          "protected path is relative or lacks a deny probe")
    for path in [*protected, directory, plan_path, ROOT]:
        check(not Path(path).resolve().is_relative_to(workspace), "grading or control material resolves inside the workspace: " + str(path))

    # Trusted, hash-bound launcher facts; they bind the run to the plan but are not receipts themselves.
    launch = json.loads((directory / "launch.json").read_text())
    result = json.loads((directory / "result.json").read_text())
    check(all(launch.get(key) == plan[key] for key in ("argv", "cwd", "binary_sha256", "launcher_sha256")) and launch.get("config_before") == hashes,
          "launch facts differ from the approved plan")
    check(result.get("config_after") == hashes and result.get("process_exit_code") == 0 and result.get("completion_verified") is True,
          "post-run hashes or launcher completion differ from the approved plan")
    check(trailer == {"capture_trailer": True, "stdout_lines": len(events), "unparsed_lines": 0} and type(trailer["stdout_lines"]) is int and
          not any("capture_trailer" in event or "unparsed_sha256" in event for event in events), "capture trailer missing or native stream incomplete")

    # Client requests: approved methods only, unique ids, exactly one native response each.
    calls = [row for row in requests if "method" in row and "id" in row]
    replies = [row for row in requests if "method" not in row]
    methods = [row["method"] for row in calls]
    check(set(methods) <= CLIENT_METHODS and [row["method"] for row in requests if "method" in row and "id" not in row] == ["initialized"],
          "unapproved native API request")
    check(all(methods.count(method) == 1 for method in ("initialize", "thread/start", "turn/start")), "expected one initialize, thread and turn")
    answers = {}
    for index, event in enumerate(events):
        if "id" in event and "method" not in event:
            answers.setdefault(event["id"], []).append(index)
    check(Counter(row["id"] for row in calls) == Counter({key: len(value) for key, value in answers.items()}) and
          len({row["id"] for row in calls}) == len(calls), "request ids are not unique with exactly one native response")
    answer = {key: value[0] for key, value in answers.items()}
    server = [event["id"] for event in events if "id" in event and "method" in event]
    check(all(set(reply) == {"id", "error"} for reply in replies) and sorted(map(json.dumps, server)) == sorted(json.dumps(reply.get("id")) for reply in replies) and
          len(set(map(json.dumps, server))) == len(server), "server requests need exactly one paired error reply and no approvals")
    start = calls[methods.index("thread/start")]
    turn = calls[methods.index("turn/start")]
    check(start["params"].get("experimentalRawEvents") is True, "raw native events were not requested")
    check(set(start["params"]) <= {"cwd", "ephemeral", "approvalPolicy", "permissions", "approvalsReviewer", "experimentalRawEvents"} and
          start["params"].get("cwd") == cwd and start["params"].get("permissions") == "preflight" and
          start["params"].get("approvalPolicy") == "never", "thread/start carries unapproved instructions, tools or overrides")
    check(set(turn["params"]) == {"threadId", "input"}, "turn/start carries unapproved overrides")
    thread = events[answer[start["id"]]]["result"]
    check(thread.get("cwd") == cwd and thread.get("runtimeWorkspaceRoots") == [cwd] and thread.get("approvalPolicy") == "never" and
          thread.get("activePermissionProfile") == {"id": "preflight", "extends": ":read-only"} and
          thread.get("sandbox") == {"type": "readOnly", "networkAccess": False}, "effective native thread cwd, roots or profile differ")
    configs = [events[answer[row["id"]]].get("result", {}).get("safeConfiguration") for row in calls if row["method"] == "config/read"]
    check(configs and all(config == {"profile": PROFILE, "default_permissions": "preflight", "approval_policy": "never", **TOOLS} for config in configs),
          "effective configuration projection missing or widened")

    # Exactly two identical probe blocks: before turn/start, and after the native turn completion.
    blocks = []
    for index, method in enumerate(methods):
        if method == "command/exec":
            if blocks and blocks[-1][-1] == index - 1:
                blocks[-1].append(index)
            else:
                blocks.append([index])
    turn_events = [index for index, event in enumerate(events) if event.get("method", "").startswith(("turn/", "item/", "rawResponseItem/"))]
    completion = [index for index, event in enumerate(events) if event.get("method") == "turn/completed"]
    reads = [index for index, method in enumerate(methods) if method == "thread/read"]
    check(len(blocks) == 2 and methods.index("thread/start") < blocks[0][0] and blocks[0][-1] < methods.index("turn/start") < blocks[1][0] and
          reads and min(reads) > blocks[1][-1], "probe blocks are missing, extra or out of order")
    check(len(completion) == 1 and all(index < completion[0] for index in turn_events if events[index].get("method") != "turn/completed"),
          "native turn work appears after completion")
    for block in blocks[:2]:
        check([calls[index]["params"] for index in block] == probes, "probe requests differ from the frozen plan")
        before = block is blocks[0]
        for index, want in zip(block, expected):
            position = answer.get(calls[index]["id"])
            got = events[position].get("result") if position is not None else None
            check(isinstance(got, dict) and set(got) == {"exitCode", "stdout", "stderr"} and type(got["exitCode"]) is int and
                  got["exitCode"] == want["exitCode"] and got["stdout"] == want["stdout"] and isinstance(got["stderr"], str) and
                  (want["stderr_contains"] is None or want["stderr_contains"] in got["stderr"]) and
                  not (want["exitCode"] and any(nonce in got["stderr"] for nonce in nonces)),
                  "native probe response differs from expectation")
            check(position is not None and (position < min(turn_events + [answer[turn["id"]]]) if before else completion and position > completion[0]),
                  "probe response is interleaved with model work")

    raw = [event["params"] for event in events if event.get("method") == "rawResponseItem/completed"]
    check(raw and all(item.get("threadId") == thread_id and item.get("turnId") == turn_id for item in raw), "raw native events missing or foreign")
    commands = {key: item for key, item in completed.items() if item.get("type") == "commandExecution"}
    # A present trace is native evidence too: it is consumed even when the raw stream shows no facades.
    traced = (directory / "traces").exists() or (directory / "traces").is_symlink()
    if traced or any(entry["item"].get("type", "").startswith("custom_tool_call") for entry in raw):
        check(Counter(item["id"] for item in started_items if item.get("type") == "commandExecution") == Counter({key: 1 for key in commands}),
              "native graph commands need exactly one matching start")
        check(not any(item.get("type") == "sleep" for item in completed.values()), "sleep items lack a native graph edge")
        verify_native_graph(directory, [entry["item"] for entry in raw], commands, thread_id, turn_id, workspace, turn["params"]["input"])
    else:
        # Raw model calls: only unified exec, stdin and sleep, each mapped by native identity.
        raw_calls, raw_order, stdin, outputs = {}, {}, [], []
        for order, item in enumerate(entry["item"] for entry in raw):
            kind = item.get("type")
            if kind == "function_call":
                name = ((item["namespace"] + ".") if item.get("namespace") else "") + item["name"]
                name = name.removeprefix("functions.")
                arguments = json.loads(item["arguments"])
                check(name in RAW_CALLS and isinstance(arguments, dict), "unapproved raw native tool call: " + name)
                check(item["call_id"] not in raw_calls, "duplicate raw call identity")
                raw_calls[item["call_id"]], raw_order[item["call_id"]] = name, order
                if name == "exec_command":
                    check(arguments.get("sandbox_permissions") in (None, "use_default") and arguments.get("additional_permissions") is None,
                          "raw exec requests elevated sandbox permissions")
                elif name == "write_stdin":
                    stdin.append((order, arguments.get("session_id")))
            elif kind == "function_call_output":
                check(item.get("call_id") in raw_calls, "raw tool output lacks a matching call")
                outputs.append(item.get("call_id"))
            else:
                check(kind in ("message", "reasoning"), "unapproved raw native item type: " + str(kind))
        check(Counter(outputs) == Counter({key: 1 for key in raw_calls}), "raw tool calls need exactly one matching output")
        sleeps = {key for key, item in completed.items() if item.get("type") == "sleep"}
        check({key for key, name in raw_calls.items() if name == "exec_command"} == set(commands), "command items and raw exec calls do not map one-to-one")
        check({key for key, name in raw_calls.items() if name == "clock.sleep"} == sleeps, "sleep items and raw sleep calls do not map one-to-one")
        for order, session in stdin:
            check(type(session) is int and any(item.get("processId") == str(session) and raw_order[key] < order for key, item in commands.items()),
                  "raw write_stdin lacks a preceding linked command process")
    for item in commands.values():
        check(item.get("status") in ("completed", "failed") and item.get("source") == "unifiedExecStartup" and
              isinstance(item.get("cwd"), str) and Path(item["cwd"]).resolve().is_relative_to(workspace),
              "command item is not a completed model exec inside the workspace: " + str(item.get("id")))
    for item in started_items:
        if item.get("id") in commands:
            check(all(item[key] == commands[item["id"]].get(key) for key in ("command", "cwd", "processId", "source") if key in item),
                  "started command payload diverges from completion: " + str(item.get("id")))
    return problems


def validate(host, case, directory, allowed_roots, history=None, enforcement=None):
    directory = Path(directory)
    approved = approved_input(case)
    problems = []
    roots = [Path(root).resolve() for root in allowed_roots]

    def check(condition, reason):
        if not condition:
            problems.append(reason)

    def approved_parts(content):
        if not isinstance(content, list) or not all(isinstance(part, dict) for part in content):
            return False
        types = [part.get("type") for part in content]
        if types != (["text", "skill"] if case == "aud" else ["text"]):
            return False
        if case == "aud":
            skill = content[1]
            if skill.get("name") != "creating-portable-skills" or not allowed(skill.get("path"), directory):
                return False
        return prompt_matches(text_input(content), approved)

    def allowed(path, cwd):
        if not isinstance(path, str) or not path:
            return False
        resolved = (Path(cwd) / path).resolve()
        return any(resolved.is_relative_to(root) for root in roots)

    try:
        check(bool(roots), "No approved read roots supplied")
        if host == "codex":
            requests = rows(directory / "native-requests.jsonl")
            events = rows(directory / "native-events.jsonl")
            trailer = events.pop() if enforcement is not None else None
            # Client calls carry a method and id; server-direction calls carry both in events and
            # are answered by client rows without a method. Pair each client id with one response.
            calls = Counter(json.dumps(r["id"]) for r in requests if "method" in r and "id" in r)
            answers = Counter(json.dumps(e["id"]) for e in events if "id" in e and "method" not in e)
            if any(count != 1 for count in calls.values()) or answers != calls:
                raise ValueError("Native request ids are not unique with exactly one response each")
            responses = {event["id"]: event.get("result", {}) for event in events if "id" in event and "method" not in event and "error" not in event}
            starts = [r for r in requests if r.get("method") == "thread/start"]
            turns = [r for r in requests if r.get("method") == "turn/start"]
            if len(starts) != 1 or len(turns) != 1:
                raise ValueError("Expected one native thread/start and one turn/start")
            check(not {"developerInstructions", "baseInstructions", "dynamicTools"} & set(starts[0].get("params", {})),
                  "thread/start carries unapproved instructions or tools")
            thread_id = responses.get(starts[0]["id"], {}).get("thread", {}).get("id")
            turn_id = responses.get(turns[0]["id"], {}).get("turn", {}).get("id")
            check(bool(thread_id) and bool(turn_id), "Missing native thread/turn response identity")
            params = turns[0]["params"]
            check(params.get("threadId") == thread_id, "Turn request thread identity mismatch")
            check(set(params) == {"threadId", "input"}, "turn/start carries unapproved overrides")
            check(approved_parts(params["input"]), "Actually sent request differs from approved INPUT")
            for event in events:
                if event.get("method", "").startswith(("item/", "turn/")):
                    identity = event.get("params", {})
                    check(identity.get("threadId") == thread_id and identity.get("turnId", identity.get("turn", {}).get("id")) == turn_id, "Native event thread/turn identity mismatch")
            scoped = [e for e in events if e.get("params", {}).get("threadId") == thread_id and e.get("params", {}).get("turnId", e.get("params", {}).get("turn", {}).get("id")) == turn_id]
            completions = [e["params"]["turn"] for e in scoped if e.get("method") == "turn/completed"]
            check(len(completions) == 1 and completions[0].get("status") == "completed" and not completions[0].get("error"), "Missing successful native turn completion")
            reads = [r for r in requests if r.get("method") == "thread/read" and r.get("params", {}).get("threadId") == thread_id]
            completion_positions = [i for i, event in enumerate(events) if event.get("method") == "turn/completed" and event in scoped]

            def lifecycle(name, identity):
                """Each start is unique and precedes its unique completion, before the turn completes."""
                found = {"started": {}, "completed": {}}
                for index, event in enumerate(events):
                    for phase, at in found.items():
                        if event.get("method") == name + "/" + phase:
                            at.setdefault(identity(event["params"]), []).append(index)
                begun, ended = found["started"], found["completed"]
                end = completion_positions[0] if completion_positions else -1
                return (all(len(at) == 1 for at in [*begun.values(), *ended.values()]) and
                        all(key in ended and at[0] < ended[key][0] < end for key, at in begun.items()))

            check(any(responses.get(r["id"], {}).get("thread", {}).get("id") == thread_id and
                      any(event.get("id") == r["id"] and i > completion_positions[0] for i, event in enumerate(events))
                      for r in reads) if completion_positions else False,
                  "Missing matching post-completion native thread read")
            for read in reads:
                thread = responses.get(read["id"], {}).get("thread", {})
                check(read["params"].get("includeTurns", False) is False and
                      thread.get("status") == {"type": "idle"} and thread.get("turns", []) == [],
                      "Native thread read must confirm idle identity without turn history")
            completed_items = [e["params"]["item"] for e in scoped if e.get("method") == "item/completed"]
            completed = {item["id"]: item for item in completed_items}
            check(len(completed_items) == len(completed), "Duplicate native completed item identities")
            started_items = [e["params"]["item"] for e in scoped if e.get("method") == "item/started"]
            check(lifecycle("item", lambda params: params["item"]["id"]), "Outstanding, duplicate or out-of-order native item identities")
            check(all(item.get("type") == completed[item["id"]].get("type") for item in started_items if item["id"] in completed),
                  "Native item type changed between start and completion")
            user = [item for item in completed.values() if item.get("type") == "userMessage"]
            check(len(user) == 1 and approved_parts(user[0]["content"]), "Native user event differs from approved INPUT or is missing")
            for item in started_items:
                if item.get("type") == "commandExecution":
                    for action in item.get("commandActions") or []:
                        path = action.get("path")
                        if isinstance(path, str) and path:
                            check(allowed(path, item.get("cwd", directory)), "Native started command read outside approved roots: " + path)
            for item in completed.values():
                check(item.get("type") in ("userMessage", "agentMessage", "reasoning", "commandExecution", "sleep"), "Native item lacks inspectable read semantics: " + str(item.get("type")))
                check(item.get("status") not in ("inProgress", "pending", "running") and "collab" not in item.get("type", "").lower(), "Outstanding/delegated work lacks completion evidence")
                if item.get("type") == "sleep":
                    # Codex's clock.sleep display item carries no command or read payload.
                    duration = item.get("durationMs")
                    check(set(item) == {"id", "type", "durationMs"} and
                          isinstance(item.get("id"), str) and bool(item["id"]) and
                          type(duration) is int and 0 <= duration < 2 ** 64,
                          "Malformed native sleep display item")
                if item.get("type") == "commandExecution" and enforcement is not None:
                    # Verified confinement bounds unknown or path-less actions; explicit outside paths stay excluded.
                    for action in item.get("commandActions") or []:
                        path = action.get("path")
                        if isinstance(path, str) and path:
                            check(allowed(path, item.get("cwd", directory)), "Native command read outside approved roots: " + path)
                elif item.get("type") == "commandExecution":
                    actions = item.get("commandActions", [])
                    read_types = ("read", "listFiles", "search")
                    check(bool(actions) and all(a.get("type") in read_types for a in actions), "Command lacks inspectable native read actions")
                    check(all(a.get("type") == "read" for a in actions),
                          "Native listing/search display paths need independent confinement evidence")
                    # Native actions are lossy display metadata, not an exhaustive read audit.
                    for action in actions:
                        if action.get("type") not in read_types:
                            continue
                        path = action.get("path")
                        if not isinstance(path, str) or not path:
                            check(False, "Native command missing or malformed read path: " + str(path))
                            continue
                        check(not any(c in path for c in '~$`{*?[\\"\''),
                              "Native command read path may contain unresolved shell expansion: " + path)
                        check(allowed(path, item.get("cwd", directory)), "Native command read outside approved roots (per-read success cannot be inferred from aggregate exit code): " + path)
            check(lifecycle("hook", lambda params: params["run"]["id"]), "Outstanding, duplicate or out-of-order native hook identities")
            if enforcement is None:
                check(not any(e.get("method") == "rawResponseItem/completed" and
                              e["params"]["item"].get("type", "").startswith("custom_tool_call") for e in events),
                      "Native exec graph requires a same-server enforcement receipt")
                check(not ((directory / "traces").exists() or (directory / "traces").is_symlink()),
                      "Native trace bundle requires a same-server enforcement receipt")
            if enforcement is not None:
                problems.extend(verify_enforcement(json.loads(Path(enforcement).read_text()), Path(enforcement), directory, roots, requests, events,
                                                   trailer, thread_id, turn_id, started_items, completed))
        else:
            check(enforcement is None, "Enforcement receipts are defined only for Codex app-server captures")
            events = rows(directory / "stdout.ndjson")
            init = [e for e in events if e.get("type") == "system" and e.get("subtype") == "init"]
            results = [e for e in events if e.get("type") == "result"]
            session = init[0].get("session_id") if len(init) == 1 else None
            check(bool(session), "Missing unique native session identity")
            check(all(e.get("session_id") == session for e in events), "Native event session identity mismatch")
            check(len(results) == 1 and results[0].get("subtype") == "success" and results[0].get("is_error") is False and not results[0].get("errors") and results[0].get("stop_reason") not in ("cancelled", "error"), "Missing successful native result (process exit alone is insufficient)")
            if history is None:
                check(False, "Missing native chat history for actual prompt verification")
            else:
                check(Path(history).parent.name == session, "Native chat history session directory identity mismatch")
                queries = []
                for row in rows(Path(history)):
                    if row.get("type") == "user":
                        content = row.get("content", [])
                        text = content if isinstance(content, str) else text_input(content)
                        if "prompt_index" in row:
                            check(row["prompt_index"] == 0, "Unexpected additional native prompt index")
                            check(isinstance(content, str) or all(part.get("type") == "text" for part in content), "Unapproved nontext native query input")
                            queries.append(text)
                        elif row.get("synthetic_reason") != "system_reminder":
                            check(False, "Unclassified native user context; cannot infer query identity from prose")
                check(len(queries) == 1 and prompt_matches(queries[0], approved), "Native user query differs from approved INPUT or is missing")
            tools, seen = {}, set()
            for event in events:
                for part in event.get("message", {}).get("content", []):
                    if part.get("type") == "tool_use":
                        check(part["id"] not in seen, "Reused native tool identity: " + str(part["id"]))
                        seen.add(part["id"])
                        tools[part["id"]] = part
                    elif part.get("type") == "tool_result":
                        tool = tools.pop(part.get("tool_use_id"), None)
                        check(tool is not None, "Native tool result lacks matching request")
                        if tool and part.get("is_error") is False:
                            name = tool["name"]
                            data = tool.get("input", {})
                            field = {"read_file": "target_file", "list_dir": "target_directory", "grep": "path"}.get(name)
                            check(field is not None, "Successful tool lacks inspectable native read path: " + name)
                            if field:
                                check(allowed(data.get(field), init[0].get("cwd", directory)), "Successful native read outside approved roots: " + str(data.get(field)))
                        elif tool:
                            check(part.get("is_error") is True, "Native tool result success/error status missing")
            check(not tools, "Outstanding native tool identities")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError) as error:
        problems.append("Unavailable or malformed native evidence: " + str(error))
    scope = ("Prompt, native completion/identity and observed reads only; discovery and confinement require separate host evidence. C3 is separate."
             if enforcement is None else
             "Prompt, native completion/identity, observed reads and a same-server probe receipt for the frozen profile; probes sample named paths "
             "and do not audit every read, and :minimal OS/runtime access remains ambient. C3 is separate.")
    return {"check": "capture-admissibility", "host": host, "case": case, "result": "Unmeasured" if problems else "Pass", "reasons": problems,
            "enforcement": "not supplied" if enforcement is None else "not verified" if problems else "verified", "scope": scope}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", choices=("codex", "grok"))
    parser.add_argument("case", choices=CASES)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--allowed-root", type=Path, action="append", required=True)
    parser.add_argument("--history", type=Path, help="Grok native chat_history.jsonl")
    parser.add_argument("--enforcement", type=Path, help="Frozen operator probe plan (JSON) for a Codex same-server confinement receipt")
    args = parser.parse_args()
    result = validate(args.host, args.case, args.directory, args.allowed_root, args.history, args.enforcement)
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "Pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
