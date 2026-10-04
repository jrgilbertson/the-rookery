"""Check native capture admissibility, separately from behavioral criterion grades."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re


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
        check(set(want) == {"exitCode", "stdout", "stderr_contains"} and want["exitCode"] in (0, 1) and type(want["exitCode"]) is int and
              isinstance(want["stdout"], str) and (want["exitCode"] == 0 or any(marker in str(want["stderr_contains"]) for marker in DENIED)),
              "deny probe must expect a permission error with exit 1, not a missing path")
    nonces = [want["stdout"] for want in expected if want["exitCode"] == 0 and want["stdout"].strip()]
    denied = [" ".join(params["command"]) for params, want in zip(probes, expected) if want["exitCode"] == 1]
    check(nonces and denied, "plan lacks an allow canary or a deny probe")
    protected = plan["protected_paths"]
    check(protected and all(Path(path).is_absolute() and any(path in command for command in denied) for path in protected),
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

    # Raw model calls: only unified exec, stdin and sleep, each mapped by native identity.
    raw_calls, raw_order, stdin, outputs = {}, {}, [], []
    raw = [event["params"] for event in events if event.get("method") == "rawResponseItem/completed"]
    check(raw and all(item.get("threadId") == thread_id and item.get("turnId") == turn_id for item in raw), "raw native events missing or foreign")
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
    commands = {key: item for key, item in completed.items() if item.get("type") == "commandExecution"}
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
            responses = {event["id"]: event.get("result", {}) for event in events if "id" in event and "method" not in event and "error" not in event}
            starts = [r for r in requests if r.get("method") == "thread/start"]
            turns = [r for r in requests if r.get("method") == "turn/start"]
            if len(starts) != 1 or len(turns) != 1:
                raise ValueError("Expected one native thread/start and one turn/start")
            thread_id = responses.get(starts[0]["id"], {}).get("thread", {}).get("id")
            turn_id = responses.get(turns[0]["id"], {}).get("turn", {}).get("id")
            check(bool(thread_id) and bool(turn_id), "Missing native thread/turn response identity")
            params = turns[0]["params"]
            check(params.get("threadId") == thread_id, "Turn request thread identity mismatch")
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
            check(all(item["id"] in completed for item in started_items), "Outstanding native item identities")
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
                        check(not any(c in path for c in "~$`{*?["),
                              "Native command read path may contain unresolved shell expansion: " + path)
                        check(allowed(path, item.get("cwd", directory)), "Native command read outside approved roots (per-read success cannot be inferred from aggregate exit code): " + path)
            for name in ("hook",):
                begun = {e["params"]["run"]["id"] for e in events if e.get("method") == name + "/started"}
                ended = {e["params"]["run"]["id"] for e in events if e.get("method") == name + "/completed"}
                check(begun <= ended, "Outstanding native hook identities")
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
            tools = {}
            for event in events:
                for part in event.get("message", {}).get("content", []):
                    if part.get("type") == "tool_use":
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
