"""Check native capture admissibility, separately from behavioral criterion grades."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CASES = {"act": "activation-near-miss.md", "aud": "vendor-guidance-audit.md"}


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


def validate(host, case, directory, allowed_roots, history=None):
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
            completed = {e["params"]["item"]["id"]: e["params"]["item"] for e in scoped if e.get("method") == "item/completed"}
            started = {e["params"]["item"]["id"] for e in scoped if e.get("method") == "item/started"}
            check(started <= completed.keys(), "Outstanding native item identities")
            user = [item for item in completed.values() if item.get("type") == "userMessage"]
            check(len(user) == 1 and approved_parts(user[0]["content"]), "Native user event differs from approved INPUT or is missing")
            for item in completed.values():
                check(item.get("type") in ("userMessage", "agentMessage", "reasoning", "commandExecution"), "Native item lacks inspectable read semantics: " + str(item.get("type")))
                check(item.get("status") not in ("inProgress", "pending", "running") and "collab" not in item.get("type", "").lower(), "Outstanding/delegated work lacks completion evidence")
                if item.get("type") == "commandExecution":
                    actions = item.get("commandActions", [])
                    check(bool(actions) and all(a.get("type") in ("read", "listFiles", "search") for a in actions), "Command lacks inspectable native read actions")
                    for action in actions:
                        check(allowed(action.get("path"), item.get("cwd", directory)), "Native command read outside approved roots (per-read success cannot be inferred from aggregate exit code): " + str(action.get("path")))
            for name in ("hook",):
                begun = {e["params"]["run"]["id"] for e in events if e.get("method") == name + "/started"}
                ended = {e["params"]["run"]["id"] for e in events if e.get("method") == name + "/completed"}
                check(begun <= ended, "Outstanding native hook identities")
        else:
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
    return {"check": "capture-admissibility", "host": host, "case": case, "result": "Unmeasured" if problems else "Pass", "reasons": problems, "scope": "Prompt, native completion/identity and observed reads only; discovery and confinement require separate host evidence. C3 is separate."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", choices=("codex", "grok"))
    parser.add_argument("case", choices=CASES)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--allowed-root", type=Path, action="append", required=True)
    parser.add_argument("--history", type=Path, help="Grok native chat_history.jsonl")
    args = parser.parse_args()
    result = validate(args.host, args.case, args.directory, args.allowed_root, args.history)
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "Pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
