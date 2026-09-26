#!/usr/bin/env python3
"""Sequential, subscription-only skill evals. See README.md; --round is required."""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import fcntl
import hashlib
import io
import json
import math
import os
import random
import re
import shlex
import shutil
import stat as stat_module
import statistics
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

import usage

H = Path(__file__).resolve().parent
REAL_HOME = Path.home()
BASE_PATH = os.environ.get("PATH", os.defpath)
SKILL_DIR_NAMES = (".claude/skills", ".agents/skills", ".codex/skills", ".grok/skills")
CAPABILITIES = ("subagents", "web")
CFG = {}
ARGS = None
# Written to each grader's disposable workspace, never next to the runner.
GRADE_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["grades"],
 "properties": {"grades": {"type": "array", "items": {"type": "object", "additionalProperties": False,
 "required": ["letter", "items", "passed"], "properties": {
 "letter": {"type": "string"}, "passed": {"type": "boolean"},
 "items": {"type": "array", "items": {"type": "object", "additionalProperties": False,
 "required": ["n", "evidence", "reasoning", "passed"], "properties": {
 "n": {"type": "integer"}, "evidence": {"type": "string"}, "reasoning": {"type": "string"},
 "passed": {"type": "boolean"}}}}}}}}}

class Budget(RuntimeError):
    pass

class Halt(RuntimeError):
    pass

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def wjson(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent,
                                         prefix=f'.{path.name}.', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(data, stream, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

def rjson(path: Path):
    return json.loads(path.read_text())

def git(*args: str) -> str:
    return subprocess.run(["git", "-C", CFG["repo_path"], *args], check=True, capture_output=True,
                          text=True).stdout.strip()

def skill_dir() -> Path:
    return Path(CFG["archive_root"]) / CFG["repo"] / CFG["skill"]

def iteration_dir(it=None) -> Path:
    return skill_dir() / f"iteration-{it or CFG['iteration']}"

def load_evals() -> tuple[list[dict], str]:
    skill = Path(CFG["repo_path"]) / "skills" / CFG["skill"]
    raw = (skill / "evals/evals.json").read_bytes()
    evals = json.loads(raw)["evals"]
    digest = hashlib.sha256(raw)
    for name in sorted({name for ev in evals for name in ev.get("files", [])}):
        fixture = (skill / name).resolve()
        if not fixture.is_relative_to(skill.resolve() / "evals/files"):
            raise ValueError("Eval fixture is outside evals/files")
        metadata = fixture.stat()
        digest.update(name.encode() + b"\0" + str(stat_module.S_IMODE(metadata.st_mode)).encode() + b"\0"
                      + str(metadata.st_mtime_ns).encode() + b"\0" + fixture.read_bytes())
    return evals, digest.hexdigest()


def selected_evals() -> list[dict]:
    only = [int(x) for x in ARGS.evals.split(",") if x] if ARGS and ARGS.evals else CFG.get("evals") or []
    selected = [e for e in load_evals()[0] if not only or e["id"] in only]
    if not selected or set(only) - {e["id"] for e in selected}:
        raise ValueError("Eval selection is empty or contains unknown IDs")
    return selected

def eval_name(ev: dict) -> str:
    derived = "-".join(re.findall(r"[a-z0-9]+", ev["expected_output"].lower())[:4])
    name = ev.get("name") or CFG.get("eval_names", {}).get(str(ev["id"])) or derived
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", name) or type(ev["id"]) is not int:
        raise ValueError("Eval id/name must be safe archive path components")
    return name

def eval_dir_name(ev: dict) -> str:
    return f"eval-{ev['id']}-{eval_name(ev)}"

def run_dir(target: str, ev: dict, arm: str, k: int, it=None) -> Path:
    return iteration_dir(it) / target / eval_dir_name(ev) / arm / f"run-{k}"

def status_of(rd: Path) -> str:
    if not rd.exists():
        return 'absent'
    try:
        record = rjson(rd / 'status.json')
    except (OSError, UnicodeError, ValueError):
        return 'unavailable'
    if not isinstance(record, dict) or record.get('status') not in (
            'ok', 'discarded', 'error', 'timeout', 'login_or_quota'):
        return 'unavailable'
    return record['status']

def tree_hash(root: Path) -> str:
    lines = []
    root_metadata = root.lstat()
    paths = [root, *sorted(root.rglob('*'))] if stat_module.S_ISDIR(root_metadata.st_mode) else [root]
    for path in paths:
        metadata = root_metadata if path == root else path.lstat()
        if stat_module.S_ISDIR(metadata.st_mode):
            kind, content = 'directory', ''
        elif stat_module.S_ISREG(metadata.st_mode):
            kind, content = 'file', sha256_bytes(path.read_bytes())
        elif stat_module.S_ISLNK(metadata.st_mode):
            kind, content = 'symlink', sha256_bytes(os.fsencode(os.readlink(path)))
        else:
            kind, content = f'special:{stat_module.S_IFMT(metadata.st_mode):o}', str(metadata.st_rdev)
        lines.append(f"{path.relative_to(root).as_posix()}\0{kind}\0"
                     f"{stat_module.S_IMODE(metadata.st_mode):o}\0{metadata.st_mtime_ns}\0{content}\n")
    return "sha256:" + sha256_bytes("".join(lines).encode())

def variants(path: str) -> set[str]:
    """A path and its /private-less or /private-ful twin (macOS /tmp, /var)."""
    if path.startswith("/private/"):
        return {path, path[len("/private"):]}
    return {path, "/private" + path} if path.startswith(("/tmp/", "/var/")) else {path}

def tools_for(adapter, caps) -> list[str]:
    return adapter.TOOLS["base"] + [n for c in CAPABILITIES if c in caps for n in adapter.TOOLS[c]]

def caps_of(adapter, argv) -> list[str]:
    allowed = adapter.allowed(argv)
    return [c for c in CAPABILITIES if all(n in allowed for n in adapter.TOOLS[c])]

def init_ok(adapter, init, argv):
    """None when the CLI reported no tool surface; else whether it matches the allowlist."""
    if init is None:
        return None
    return (set(init.get("tools") or []) == set(adapter.allowed(argv)) and not init.get("skills")
            and not init.get("mcp_servers") and not init.get("slash_commands"))

def flag(argv: list[str], name: str) -> str:
    return argv[argv.index(name) + 1] if name in argv else ""

def strings(value, key="") -> list[str]:
    """Every string in a tool input except descriptions: what the call acted on."""
    if isinstance(value, str):
        return [] if key in ("description", "title") else [value]
    if isinstance(value, dict):
        return [s for k, v in value.items() for s in strings(v, k)]
    return [s for v in value for s in strings(v, key)] if isinstance(value, list) else []

def literal_path(path: str, cwd: Path, home: Path) -> Path:
    """Resolve a literal tool path using its working directory and isolated HOME."""
    for prefix in ('~', '$HOME', '${HOME}'):
        if path == prefix or path.startswith(prefix + '/'):
            path = str(home) + path[len(prefix):]
            break
    return Path(os.path.normpath(path if path.startswith('/') else cwd / path))


def path_inputs(value, cwd: Path, home: Path) -> list[tuple[str, Path, bool]]:
    """Path-bearing inputs with their declared working directory; no shell expansion."""
    if isinstance(value, str):
        return [(value, cwd, False)]
    if isinstance(value, list):
        return [row for item in value for row in path_inputs(item, cwd, home)]
    if isinstance(value, dict):
        declared = value.get('cwd', value.get('workdir', '.'))
        base = literal_path(declared, cwd, home) if isinstance(declared, str) else cwd
        rows = []
        for key, item in value.items():
            if key.lower() in {'cwd', 'workdir'}:
                rows += [(s, cwd, False) for s in strings(item)]
            elif key.lower() in {'command', 'cmd', 'path', 'file_path', 'filepath', 'target_file', 'directory', 'glob'}:
                rows += [(s, base, key.lower() in {'command', 'cmd'}) for s in strings(item)]
            elif isinstance(item, (dict, list)):
                rows += path_inputs(item, base, home)
        return rows
    return []

def new_trace() -> dict:
    return {"tool_calls": [], "final_text": "", "tokens": 0, "token_detail": {}, "cost_usd": None, "is_error": False,
            "errors": 0, "steps": 0, "init": None, "structured": None, "cli_duration_ms": None}

def events(path: Path) -> list[dict]:
    out = []
    for number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            e = json.loads(line)
        except ValueError as error:
            raise ValueError(f"Malformed JSONL event in {path.name} line {number}") from error
        if not isinstance(e, dict):
            raise ValueError(f"Non-object JSONL event in {path.name} line {number}")
        out.append(e)
    return out

class Claude:
    """Claude Code: the real HOME and keychain login, customizations off by flags."""
    NAME, PROVIDER, BIN, GREP, THROWAWAY_HOME = "claude", "anthropic", "claude", "Grep", False
    SESSIONS = None  # the stream marks subagent calls with parent_tool_use_id
    TOOLS = {"base": ["Read", "Glob", "Grep", "Bash"], "subagents": ["Task"], "web": ["WebFetch", "WebSearch"]}
    SAFE = ["--safe-mode", "--setting-sources", "project", "--disable-slash-commands", "--strict-mcp-config",
            "--no-session-persistence"]

    def env(self, home):
        return {"HOME": str(REAL_HOME), "DISABLE_AUTOUPDATER": "1"}

    def exec_argv(self, t, ws, prompt, final_path, budget, caps):
        tools = ",".join(tools_for(self, caps))
        return [self.BIN, "-p", prompt, "--model", t["model"], "--effort", t["effort"], "--output-format",
                "stream-json", "--verbose", *self.SAFE, "--tools", tools, "--allowedTools", tools, "--add-dir",
                str(ws["parent"])] + (["--max-budget-usd", f"{budget:.2f}"] if budget else [])

    def grade_argv(self, t, packet, out_path, budget, schema=None):
        return [self.BIN, "-p", packet, "--model", t["model"], "--effort", t["effort"], "--output-format",
                "stream-json", "--verbose", "--json-schema", schema.read_text(), *self.SAFE, "--tools", ""] + \
            (["--max-budget-usd", f"{budget:.2f}"] if budget else [])

    def allowed(self, argv):
        return flag(argv, "--tools").split(",")

    def parse(self, transcript, final_path):
        r, ids, results = new_trace(), {}, []
        for e in events(transcript):
            if e.get("type") == "system" and e.get("subtype") == "init":
                r["init"] = {k: e.get(k) for k in ("tools", "skills", "mcp_servers", "slash_commands", "model")}
            elif e.get("type") == "assistant":
                for c in e.get("message", {}).get("content", []) or []:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        if c.get("name") == "StructuredOutput":  # how --json-schema returns its answer
                            r["structured"] = r["structured"] or c.get("input")
                            continue
                        ids[c.get("id")] = len(r["tool_calls"])
                        r["tool_calls"].append({"name": c.get("name"), "input": c.get("input"), "output": "",
                                                "failed": False,
                                                "by": "subagent" if e.get("parent_tool_use_id") else "main"})
            elif e.get("type") == "user" and isinstance(e.get("message", {}).get("content"), list):
                for c in e["message"]["content"]:
                    if isinstance(c, dict) and c.get("type") == "tool_result" and c.get("tool_use_id") in ids:
                        r["tool_calls"][ids[c["tool_use_id"]]]["output"] = json.dumps(c.get("content"))
                        r["tool_calls"][ids[c["tool_use_id"]]]["failed"] = bool(c.get("is_error"))
                        r["errors"] += bool(c.get("is_error"))
            elif e.get("type") == "result":
                u = e.get("usage") or {}
                r["token_detail"] = {k: u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens",
                                                             "cache_read_input_tokens", "output_tokens")}
                results.append(e.get("result") or "")  # each main-context turn ends in one; keep them all
                r.update(final_text="\n\n".join(x for x in results if x.strip()), is_error=bool(e.get("is_error")),
                         cost_usd=e.get("total_cost_usd"), steps=e.get("num_turns") or 0,
                         tokens=sum(r["token_detail"].values()), cli_duration_ms=e.get("duration_ms"),
                         structured=e.get("structured_output") or r["structured"])
        return r

class Codex:
    """Codex CLI: throwaway HOME and CODEX_HOME holding only auth.json; ChatGPT login only."""
    NAME, PROVIDER, BIN, GREP, THROWAWAY_HOME = ("codex", "openai", "codex", None, True)
    SESSIONS = ".codex/sessions"  # exec --json omits subagent threads; their rollouts hold the calls
    TOOLS = {"base": ["command_execution", "file_change"], "subagents": ["collab_tool_call"], "web": ["web_search"]}
    OFF = ("apps", "plugins", "browser_use", "browser_use_external", "computer_use", "image_generation",
           "in_app_browser")
    OUTPUT_FIELDS = ("id", "type", "status", "aggregated_output", "exit_code", "result", "error", "text")

    def env(self, home):
        (home / ".codex").mkdir(parents=True, exist_ok=True)
        shutil.copy2(REAL_HOME / ".codex" / "auth.json", home / ".codex" / "auth.json")
        return {"HOME": str(home), "CODEX_HOME": str(home / ".codex")}

    def common(self, caps):
        off = list(self.OFF) + ([] if "subagents" in caps else ["multi_agent"])
        return ["-c", 'forced_login_method="chatgpt"', "-c", "skills.bundled.enabled=false", "-c",
                f'web_search="{"live" if "web" in caps else "disabled"}"'] + [x for f in off for x in ("--disable", f)]

    def exec_argv(self, t, ws, prompt, final_path, budget, caps):
        return [self.BIN, "exec", "-m", t["model"], "-c", f"model_reasoning_effort={t['effort']}", *self.common(caps),
                "-s", "workspace-write", "--add-dir", str(ws["parent"]), "--skip-git-repo-check",
                "--ignore-user-config", "--ignore-rules", "--color", "never", "--json", "-o", str(final_path),
                "-C", str(ws["project"]), prompt]

    def grade_argv(self, t, packet, out_path, budget, schema=None):
        return [self.BIN, "exec", "-m", t["model"], "-c", f"model_reasoning_effort={t['effort']}", *self.common([]),
                "--disable", "shell_tool", "--disable", "unified_exec", "-s", "read-only", "--skip-git-repo-check",
                "--ignore-user-config", "--ignore-rules", "--color", "never", "--json",
                "--output-schema", str(schema), "-o", str(out_path), packet]

    def subagent_calls(self, sessions: Path) -> list[dict]:
        """Tool calls of child threads (the dispatch message itself is stored encrypted)."""
        calls = []
        for f in sorted(sessions.rglob("rollout-*.jsonl")):
            evs = events(f)
            meta = next((e.get("payload") or {} for e in evs if e.get("type") == "session_meta"), {})
            source = meta.get("source", {})
            if not (meta.get("parent_thread_id") or isinstance(source, dict) and source.get("subagent")):
                continue
            for e in evs:
                payload = e.get("payload") or {}
                if e.get("type") == "response_item" and payload.get("type") in ("function_call", "custom_tool_call"):
                    raw = payload.get("arguments", payload.get("input", ""))
                    try:
                        inp = json.loads(raw) if isinstance(raw, str) else raw
                    except ValueError:
                        inp = raw
                    calls.append({"name": payload.get("name"), "by": "subagent", "input": inp, "output": ""})
                it = payload.get("item") or {}
                if e.get("type") == "event_msg" and e["payload"].get("type") == "item_completed" and \
                        it.get("type") not in (None, "Reasoning", "AgentMessage", "UserMessage", "SubAgentActivity"):
                    name = "web_search" if it.get("kind") == "web.search" else \
                        re.sub(r"(?<!^)(?=[A-Z])", "_", it["type"]).lower()
                    cmd = it.get("command")
                    calls.append({"name": name, "by": "subagent",
                                  "input": {"command": cmd[-1] if isinstance(cmd, list) and cmd else cmd} if cmd else
                                  {k: v for k, v in it.items() if k not in self.OUTPUT_FIELDS + ("stdout", "stderr",
                                   "formatted_output", "duration", "process_id", "cwd", "parsed_cmd", "source")},
                                  "output": (it.get("aggregated_output") or ""),
                                  "failed": it.get("exit_code") not in (None, 0) or it.get("status") in ("failed", "error")})
        return calls

    def allowed(self, argv):
        disabled = {argv[i + 1] for i, a in enumerate(argv) if a == "--disable"}
        return self.TOOLS["base"] + (self.TOOLS["subagents"] if "multi_agent" not in disabled else []) + \
            (self.TOOLS["web"] if 'web_search="live"' in argv else [])

    def parse(self, transcript, final_path):
        r, usage, last = new_trace(), {}, ""
        for e in events(transcript):
            it = e.get("item") or {}
            if e.get("type") == "item.completed" and it.get("type") == "agent_message":
                last = it.get("text") or ""
            elif e.get("type") == "item.completed" and it.get("type") not in (None, "reasoning"):
                r["tool_calls"].append({"name": it["type"] + (f":{it['tool']}" if it.get("tool") else ""), "by": "main",
                                        "input": {k: v for k, v in it.items() if k not in self.OUTPUT_FIELDS},
                                        "output": (it.get("aggregated_output") or ""),
                                        "failed": it.get("exit_code") not in (None, 0) or it.get("status") in ("failed", "error")})
                r["errors"] += it.get("exit_code") not in (None, 0) or it.get("status") in ("failed", "error")
            elif e.get("type") == "turn.completed":
                r["steps"] += 1
                for k, v in (e.get("usage") or {}).items():
                    usage[k] = usage.get(k, 0) + v
            elif e.get("type") in ("error", "turn.failed"):
                r["is_error"] = True
        r.update(token_detail=usage, tokens=usage.get("input_tokens", 0) + usage.get("output_tokens", 0))
        r["tool_calls"] += self.subagent_calls(transcript.parent / "sessions")
        r["final_text"] = final_path.read_text(errors="replace") if final_path and final_path.exists() else last
        try:
            r["structured"] = json.loads(r["final_text"])
        except ValueError:
            pass
        return r

class Grok:
    """Grok CLI: throwaway HOME holding .grok/auth.json (grok.com login) and a config.toml that
    hides the bundled skills Grok downloads there. In grok 1.0.41 --tools does not filter the tool
    list, so the allowlist is sent as a denylist of every other known tool; a tool Grok adds later
    shows up in the reported tool list and fails init_ok."""
    NAME, PROVIDER, BIN, GREP, THROWAWAY_HOME = "grok", "xai", "grok", "grep", True
    SESSIONS = ".grok/sessions"  # the stream interleaves subagent calls; child sessions name their call ids
    TOOLS = {"base": ["read_file", "list_dir", "grep", "run_terminal_command"],
             "subagents": ["spawn_subagent", "get_command_or_subagent_output", "kill_command_or_subagent"],
             "web": ["web_search", "web_fetch"]}
    OTHER = ["search_replace", "write", "todo_write", "scheduler_create", "scheduler_delete", "scheduler_list",
             "monitor", "workflow", "enter_plan_mode", "exit_plan_mode", "ask_user_question", "send_feedback",
             "image_gen", "image_edit", "image_to_video", "reference_to_video", "search_tool", "use_tool"]

    def known(self):
        return self.OTHER + [n for v in self.TOOLS.values() for n in v]

    def env(self, home):
        (home / ".grok").mkdir(parents=True, exist_ok=True)
        shutil.copy2(REAL_HOME / ".grok" / "auth.json", home / ".grok" / "auth.json")
        (home / ".grok" / "config.toml").write_text(f'[skills]\nignore = ["{home}/.grok/bundled"]\n')
        return {"HOME": str(home)}

    def exec_argv(self, t, ws, prompt, final_path, budget, caps):
        denied = [n for n in self.known() if n not in tools_for(self, caps)]
        return [self.BIN, "-p", prompt, "-m", t["model"], "--reasoning-effort", t["effort"], "--output-format",
                "streaming-json", "--always-approve", "--max-turns", str(CFG.get("max_turns", 60)),
                "--disallowed-tools", ",".join(denied), "--sandbox", "workspace"] + \
            ([] if "web" in caps else ["--disable-web-search"])

    def grade_argv(self, t, packet, out_path, budget, schema=None):
        return [self.BIN, "-p", packet, "-m", t["model"], "--reasoning-effort", t["effort"], "--json-schema",
                schema.read_text(), "--always-approve", "--max-turns", "3", "--disable-web-search",
                "--disallowed-tools", ",".join(self.known())]

    def allowed(self, argv):
        denied = flag(argv, "--disallowed-tools").split(",")
        return [n for n in self.known() if n not in denied]

    def parse(self, transcript, final_path):
        r, ids, text, last, ids_in_order = new_trace(), {}, [], "", []
        try:  # --json-schema prints one JSON object (the grading call)
            obj = json.loads(transcript.read_text(errors="replace"))
        except ValueError:
            obj = None
        single = isinstance(obj, dict) and "type" not in obj
        for e in [obj] if single else events(transcript):
            kind = e.get("type")
            if kind == "available_commands" and r["init"] is None:
                r["init"] = {"tools": e.get("tools") or []}
            elif kind == "tool_call":
                inp = e.get("rawInput") or {}
                ids[e.get("toolCallId")] = len(r["tool_calls"])
                ids_in_order.append(e.get("toolCallId"))
                r["tool_calls"].append({"name": "web_search" if inp.get("variant") == "WebSearch" else e.get("toolName"),
                                        "input": inp, "output": ""})
                text = []  # narration before a tool call is not the final answer
            elif kind == "tool_call_update" and e.get("toolCallId") in ids:
                tc, out = r["tool_calls"][ids[e["toolCallId"]]], e.get("rawOutput")
                texts = "".join(c.get("content", {}).get("text", "") for c in e.get("content") or [] if isinstance(c, dict))
                tc["output"] = (json.dumps(out) if out is not None else texts or tc["output"])
                tc["failed"] = tc.get("failed", False) or e.get("status") in ("failed", "error") or \
                    isinstance(out, dict) and bool(out.get("error"))
                if isinstance(out, dict) and isinstance(out.get("action"), dict):  # server-side web tools
                    tc["input"] = {**tc["input"], **{k: v for k, v in out["action"].items() if k in ("query", "url")}}
                r["errors"] += e.get("status") == "failed"
            elif kind == "text":  # subagent text is interleaved; the final answer is the last response
                text.append(e.get("data") or "")
            elif kind == "usage":
                last, text = "".join(text), []
            if kind in ("end", "error", None):
                u = e.get("usage") or {}
                r.update(token_detail=u, tokens=u.get("total_tokens", 0), cost_usd=e.get("total_cost_usd"),
                         steps=e.get("num_turns") or 0, is_error=r["is_error"] or kind == "error")
        r["final_text"] = (obj.get("text") or "") if single else "".join(text) or last
        r["structured"] = obj.get("structuredOutput") if single else None
        sessions = transcript.parent / "sessions"
        if sessions.is_dir():
            children = {rjson(m).get("child_session_id") for m in sessions.rglob("subagents/*/meta.json")}
            child_ids = {(e.get("params") or {}).get("update", {}).get("toolCallId") for d in sessions.glob("*/*")
                         if d.name in children and (d / "updates.jsonl").exists() for e in events(d / "updates.jsonl")}
            for c, cid in zip(r["tool_calls"], ids_in_order):
                c["by"] = "subagent" if cid in child_ids else "main"
        return r

ADAPTERS = {a.NAME: a for a in (Claude(), Codex(), Grok())}

def adapter_of(target: str):
    return ADAPTERS[CFG["targets"][target]["adapter"]]

def new_home(adapter) -> Path | None:
    if not adapter.THROWAWAY_HOME:
        return None
    Path(CFG["workspace_root"]).mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="home-", dir=CFG["workspace_root"])).resolve()

def drop_home(home: Path | None) -> None:
    if home is not None and home != REAL_HOME:  # never the owner's HOME
        shutil.rmtree(home, ignore_errors=True)

def wrapper(install: Path, prompt: str) -> str:
    return (f"A skill package is installed at {install}. Read {install}/SKILL.md and follow it to handle the request "
            "below, reading the files it references when it directs you to. Use cat or a native file-read tool "
            "for the SKILL.md read, and make sure the read succeeds. Use no other skill. This is a "
            "non-interactive run: where the skill would ask the user something, state the question and the answer "
            "you would need, then continue as far as the skill allows. Paths in the request are relative to the "
            f"current directory. Keep filesystem access within {install.parent.parent}; do not search its "
            "parent or sibling workspaces. A named synthetic subject need not exist outside the supplied "
            "fixtures.\n\nRequest:\n\n" + prompt)

def staged_prompt(ev: dict) -> str:
    return ev["prompt"].replace("evals/files/", "")

def ancestors_with_agent_files(path: Path) -> list[str]:
    return [str(a / n) for a in [path, *path.parents]
            for n in ("CLAUDE.md", "AGENTS.md", ".claude", ".agents", ".codex", ".grok") if (a / n).exists()]

def require_project_root(root: Path) -> None:
    if not stat_module.S_ISDIR(root.lstat().st_mode):
        raise ValueError('Project root must be a real directory')

def snapshot(root: Path) -> dict:
    require_project_root(root)
    result = {}
    for path in sorted(root.rglob("*")):
        if not stat_module.S_ISREG(path.lstat().st_mode):
            continue
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        result[path.relative_to(root).as_posix()] = {"sha256": sha256_bytes(data), "text": text}
    return result

NESTED_CLI = re.compile(r"(^|[\s;&|(\"'/])(claude|codex|grok)\s+(-p\b|--print\b|--single\b|exec\b|e\b)")
HEREDOC = re.compile(r"<<(-?)[ \t]*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2")


def heredoc_markers(line: str, quote: str) -> tuple[list[tuple[str, bool]], str]:
    """Find literal heredoc operators outside quoted shell words."""
    markers, index = [], 0
    while index < len(line):
        char = line[index]
        if char == '\\' and quote != "'":
            index += 2
            continue
        if quote:
            if char == quote:
                quote = ''
        elif char in ('"', "'"):
            quote = char
        elif (char == '<' and (index == 0 or line[index - 1] != '<')
              and not line.startswith('<<<', index) and (match := HEREDOC.match(line, index))):
            markers.append((match.group(3), bool(match.group(1))))
            index = match.end()
            continue
        index += 1
    return markers, quote


def without_heredoc_bodies(script: str) -> str:
    """Keep literal shell lines, excluding bodies passed as heredoc input."""
    kept, pending, quote = [], [], ''
    for line in script.splitlines():
        if pending:
            delimiter, strip_tabs = pending[0]
            if (line.lstrip('\t') if strip_tabs else line) == delimiter:
                pending.pop(0)
            continue
        kept.append(line)
        markers, quote = heredoc_markers(line, quote)
        pending.extend(markers)
    return '\n'.join(kept)

def foreign_patterns(adapter) -> list[str]:
    """What a run must never act on: user-level skill copies, the repo and the arm packages
    (another arm's text), Grok's bundled skills, and the public repo on the web."""
    dirs = [str(REAL_HOME / d) for d in SKILL_DIR_NAMES]
    if not adapter.THROWAWAY_HOME:  # ~ and $HOME resolve to the real HOME
        dirs += [f"{h}/{d}" for h in ("~", "$HOME", "${HOME}") for d in SKILL_DIR_NAMES]
    repos = sorted({m.group(1) for m in re.finditer(r"github\.com[:/]([^/]+/[^/.]+)", git("remote", "-v"))})
    web = [p for repo in repos for p in (f"github.com/{repo}", f"raw.githubusercontent.com/{repo}")]
    return dirs + [CFG["repo_path"], str(iteration_dir() / "packages"), "/.grok/bundled/"] + web

def parse(adapter, transcript: Path, final_path: Path | None) -> dict:
    return adapter.parse(transcript, final_path)

def identity(tr: dict, ws: dict, adapter, argv: list[str]) -> dict:
    want = {str(Path(v) / "SKILL.md") for v in variants(str(ws["install"]))}
    loaded = []
    pats, foreign, nested = foreign_patterns(adapter), [], []
    own = [o for w in (ws["parent"], ws["home"]) if w for o in variants(str(w))]
    staged = variants(str(ws["parent"]))
    roots = sorted(variants(CFG["workspace_root"].rstrip("/")), key=len, reverse=True)
    under_root = re.compile("(?:" + "|".join(map(re.escape, roots)) + r")(?=/|[\s'\"`;|&)]|$)[^\s'\"`;|&)]*")
    parent = Path(ws["parent"])
    project = Path(ws["project"])
    home = Path(ws['home']) if adapter.THROWAWAY_HOME else REAL_HOME
    for c in tr["tool_calls"]:  # inputs only; a grep pattern is text searched for, not a place
        inp = {k: v for k, v in c["input"].items() if k != "pattern"} if c["name"] == adapter.GREP else c["input"]
        for s in strings(inp):
            nested += [s[:300]] if NESTED_CLI.search(s) else []
            foreign += [p for p in pats if p in s]
            foreign += [f"another workspace: {m}" for m in under_root.findall(s)  # a sibling run's parent or HOME
                        if not any(m == o or m.startswith(o + "/") for o in own)]
        for s, cwd, command in path_inputs(inp, project, home):
            try:
                words = shlex.split(s)
            except ValueError:
                words = s.split()
            # Codex command_execution commonly records one shell -c/-lc wrapper.
            # Inspect that literal script with the existing static path checks.
            if (command and len(words) >= 3 and Path(words[0]).name in {'sh', 'bash', 'zsh', 'dash', 'ksh'}
                    and words[1] in {'-c', '-lc'}):
                s = words[2]
            if command and '<<' in s:
                s = without_heredoc_bodies(s)
            try:
                words = shlex.split(s)
            except ValueError:
                words = s.split()
            # Honor the common explicit shell prefix; this remains a static detector,
            # not an interpreter for variables, substitutions, or persistent shell state.
            while command and len(words) >= 3 and words[0] == 'cd' and words[2] == '&&':
                cwd = literal_path(words[1], cwd, home)
                if not cwd.is_relative_to(parent):
                    foreign.append(f"relative workspace escape: {words[1]}")
                words = words[3:]
            read_result = bool(c.get('output')) and not c.get('failed', False)
            reads_file = ((command and c['name'] in {'command_execution', 'run_terminal_command', 'Bash'}
                           and words and Path(words[0]).name == 'cat' and '\n' not in s.strip()
                           and not any(any(ch in word for ch in '|;&<>') for word in words))
                          or (not command and c['name'] in {'read_file', 'Read'}))
            for index, word in enumerate(words):
                path = word.rsplit('=', 1)[-1].lstrip('(<')
                resolved = literal_path(path, cwd, home)
                if read_result and reads_file and path.endswith('SKILL.md') and str(resolved) in want:
                    loaded.append(path)
                # An absolute first command token names the executable, not a file it read.
                if command and index == 0 and path.startswith('/'):
                    continue
                if path.startswith(('/', '~', '$HOME', '${HOME}')):
                    if not any(str(resolved) == root or str(resolved).startswith(root + '/') for root in staged):
                        foreign.append(f"absolute outside workspace: {path}")
                elif '..' in Path(path).parts and not resolved.is_relative_to(parent):
                    foreign.append(f"relative workspace escape: {path}")
    return {"loaded_paths": sorted(set(loaded)), "foreign_access": sorted(set(foreign)), "nested_agent_cli": nested,
            "init_surface_ok": init_ok(adapter, tr["init"], argv)}

def scrub(text: str, b: dict) -> str:
    """Neutral names for a run's workspace, archive, harness, HOME, and installed revision."""
    reps = [(v, n) for key, n in (("install_path", f"/workspace/skills/{CFG['skill']}"), ("project", "/workspace/project"),
                                  ("workspace", "/workspace"), ("home", "/home/user")) if b.get(key)
            for v in variants(b[key])]
    reps += [(str(skill_dir()), "/archive"), (str(H), "/harness"), (str(REAL_HOME), "/Users/user")]
    reps += [(r, "<rev>") for r in (b["skill_revision"], b["skill_revision"][:7])]
    for old, new in sorted(reps, key=lambda x: -len(x[0])):
        text = text.replace(old, new)
    return text

HEADER = """You are grading anonymous agent outputs against a list of assertions. Each output answered the same request after reading a skill package. You do not know which package version or which run produced which output; do not guess.

## Request the agent received

{request}

## Assertions

{assertions}

Grade only what each assertion asks, and judge each output only from its text and any harness observations shown with it. For every output and every assertion, first write the evidence: quote the exact span of the output or observation the verdict rests on (for a failure caused by absence, quote the closest relevant span or write "absent"). Then write your reasoning. Only then give the verdict, `passed` true or false. An output passes only if every assertion passes. Reply as JSON matching the provided schema, with one entry per output letter and one item per assertion number.

## Outputs

"""

def build_packet(ev: dict, runs: list[tuple], seed: str) -> tuple[str, dict]:
    answered = [r for r in runs if r[3] == "ok"]
    random.Random(seed).shuffle(answered)
    key, parts = {}, []
    for i, (arm, k, rd, _) in enumerate(answered):
        letter, b = chr(65 + i), rjson(rd / "build.json")
        b["project"] = b["workspace"] + "/project"
        key[letter] = {"arm": arm, "run": k, "run_dir": str(rd)}
        body = scrub((rd / "outputs" / "final.md").read_text(errors="replace"), b).strip() or "(empty output)"
        obs = rd / "outputs" / "observations.json"
        parts.append(f"### Output {letter}\n\n{body}\n" + (f"\n#### Harness observations for output {letter}\n\n"
                                                           f"```json\n{scrub(obs.read_text(), b)}\n```\n"
                                                           if obs.exists() else ""))
    assertions = "\n".join(f"{n}. {a}" for n, a in enumerate(ev["assertions"], 1))
    return HEADER.format(request=staged_prompt(ev), assertions=assertions) + "\n".join(parts), key

def validate(obj, key: dict, n_items: int) -> str | None:
    if not isinstance(obj, dict) or not isinstance(obj.get("grades"), list):
        return "no structured grade object"
    letters = [x.get("letter") for x in obj["grades"] if isinstance(x, dict)]
    if any(not isinstance(letter, str) for letter in letters):
        return "invalid output letters"
    if len(letters) != len(obj["grades"]) or len(set(letters)) != len(letters) or set(letters) != set(key):
        return f"letters {letters} != packet {sorted(key)}"
    for x in obj["grades"]:
        items = x.get("items") or []
        if not isinstance(items, list) or any(not isinstance(i, dict) or type(i.get("n")) is not int for i in items):
            return "malformed assertion items"
        if sorted(i.get("n") for i in items) != list(range(1, n_items + 1)):
            return f"{x['letter']}: item numbers {[i.get('n') for i in items]} != 1..{n_items}"
        if any(type(i.get("passed")) is not bool or type(i.get("evidence")) is not str
               or not i["evidence"].strip() or type(i.get("reasoning")) is not str
               or not i["reasoning"].strip() for i in items):
            return f"{x['letter']}: an item lacks evidence, reasoning, or a boolean verdict"
        if type(x.get("passed")) is not bool or x["passed"] != all(i["passed"] for i in items):
            return f"{x['letter']}: passed flag disagrees with its items"
    return None

def write_grading(rd: Path, ev: dict, items: list[dict], grader: dict) -> None:
    res = [{"text": a, "evidence": f"{i['evidence']} Reasoning: {i['reasoning']}", "passed": i["passed"]}
           for a, i in zip(ev["assertions"], sorted(items, key=lambda i: i["n"]))]
    p = sum(r["passed"] for r in res)
    wjson(rd / "grading.json", {"assertion_results": res, "grader": grader, "summary": {
        "passed": p, "failed": len(res) - p, "total": len(res),
        "pass_rate": round(p / len(res), 4) if res else None}})

def checked_grading(rd: Path, ev: dict, grader_model: str) -> tuple[dict | None, str | None]:
    path = rd / 'grading.json'
    if not path.exists():
        return None, None
    try:
        grade = rjson(path)
    except (OSError, UnicodeError, ValueError):
        return None, 'Unreadable grading.json; recover it from the preserved grader attempt evidence'
    if not isinstance(grade, dict) or not isinstance(grade.get('grader'), dict) or \
            grade['grader'].get('model') != grader_model or not isinstance(grade.get('assertion_results'), list):
        return None, 'Invalid grading.json; recover it from the preserved grader attempt evidence'
    results = grade['assertion_results']
    if (len(results) != len(ev['assertions']) or
            any(not isinstance(item, dict) or item.get('text') != assertion or
                type(item.get('evidence')) is not str or not item['evidence'].strip() or
                type(item.get('passed')) is not bool
                for item, assertion in zip(results, ev['assertions']))):
        return None, 'Invalid grading.json; recover it from the preserved grader attempt evidence'
    passed = sum(item['passed'] for item in results)
    expected = {'passed': passed, 'failed': len(results) - passed, 'total': len(results),
                'pass_rate': round(passed / len(results), 4) if results else None}
    summary = grade.get('summary')
    if (not isinstance(summary, dict) or summary != expected or
            any(type(summary[key]) is not int for key in ('passed', 'failed', 'total')) or
            (type(summary['pass_rate']) is not float if results else summary['pass_rate'] is not None)):
        return None, 'Invalid grading.json; recover it from the preserved grader attempt evidence'
    return grade, None

def report_run_object(path: Path) -> tuple[dict | None, str | None]:
    if not path.exists():
        return None, None
    try:
        record = rjson(path)
    except (OSError, UnicodeError, ValueError):
        return None, f'{path.name} is unreadable; recover the saved run evidence'
    if not isinstance(record, dict):
        return None, f'{path.name} is invalid; recover the saved run evidence'
    return record, None

def stat(xs: list[float]) -> dict:
    return {"mean": round(statistics.mean(xs), 4) if xs else 0.0,
            "stddev": round(statistics.stdev(xs), 4) if len(xs) > 1 else 0.0}

def billing_keys(value):
    """Reject credential/billing overrides without ever printing their values."""
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = re.sub(r'[^a-z]', '', key.lower())
            if item and (normalized.endswith('apikey') or normalized in ('baseurl', 'modelprovider') or normalized in (
                    'billing', 'billingmode', 'provider', 'authmode')
                    and str(item).lower() in ('api', 'apikey', 'api_key', 'payg')):
                return True
            if billing_keys(item):
                return True
    elif isinstance(value, list):
        return any(billing_keys(x) for x in value)
    return False


def subscription_guard(adapter):
    if any(value for key, value in os.environ.items() if key.endswith('_API_KEY') or key in (
            'ANTHROPIC_AUTH_TOKEN', 'CLAUDE_CODE_OAUTH_TOKEN', 'OPENAI_BASE_URL', 'ANTHROPIC_BASE_URL',
            'XAI_BASE_URL')) or billing_keys(CFG):
        raise Halt('API credentials or billing overrides are present; subscription-only calls refused')
    if adapter.NAME == 'claude':
        raise Halt('Claude invocation is disabled; its adapter is retained for archived evidence only')
    try:
        auth = rjson(REAL_HOME / f'.{adapter.NAME}' / 'auth.json')
    except (OSError, ValueError):
        raise Halt(f'{adapter.NAME}: subscription login file missing or unreadable') from None
    if billing_keys(auth):
        raise Halt(f'{adapter.NAME}: API-key authentication refused')
    try:
        if adapter.NAME == 'codex':
            if auth.get('auth_mode') != 'chatgpt':
                raise ValueError('not ChatGPT login')
            token = auth['tokens']['access_token']
            payload = json.loads(base64.urlsafe_b64decode(token.split('.')[1] + '==='))
            expires = float(payload['exp'])
        else:
            # The official CLI stores one OIDC browser login under issuer::client.
            if len(auth) != 1:
                raise ValueError('ambiguous Grok login')
            account, login = next(iter(auth.items()))
            if (not account.startswith('https://auth.x.ai::') or login.get('auth_mode') != 'oidc'
                    or not login.get('key')):
                raise ValueError('not Grok subscription login')
            expires = dt.datetime.fromisoformat(login['expires_at'].replace('Z', '+00:00')).timestamp()
        if not math.isfinite(expires) or expires <= time.time() + 60:
            raise ValueError('expired subscription access token')
    except (KeyError, ValueError, TypeError, IndexError):
        raise Halt(f'{adapter.NAME}: current supported subscription login required; refresh it in the official CLI. No API fallback.') from None


def child_env(adapter, home):
    subscription_guard(adapter)
    return {'PATH': BASE_PATH, 'USER': os.environ.get('USER', 'user'), 'SHELL': '/bin/sh',
            'TERM': 'dumb', 'LANG': 'en_US.UTF-8', **adapter.env(home)}


def outside_repo(path):
    resolved = Path(path).expanduser().resolve()
    repo = Path(CFG['repo_path']).resolve()
    if resolved == repo or repo in resolved.parents or resolved == H or H in resolved.parents:
        raise ValueError('Config and generated artifacts must be outside the repository and runner directory')
    return resolved


def validate_config(path, require_executor=True):
    CFG['repo_path'] = str(Path(CFG['repo_path']).expanduser().resolve())
    outside_repo(path)
    for key in ('repo', 'skill'):
        if not re.fullmatch(r'[A-Za-z0-9_-]+', CFG[key]):
            raise ValueError(f'{key} must be a single safe path component')
    if not isinstance(CFG['iteration'], int) or CFG['iteration'] < 1:
        raise ValueError('iteration must be a positive round number')
    for key in ('archive_root', 'workspace_root'):
        CFG[key] = str(outside_repo(CFG[key]))
    archive, workspace = Path(CFG['archive_root']), Path(CFG['workspace_root'])
    repo = Path(CFG['repo_path']).resolve()
    if any(p == repo or p in repo.parents for p in (archive, workspace)):
        raise ValueError('Artifact roots cannot contain the source repository')
    if archive == workspace or archive in workspace.parents or workspace in archive.parents:
        raise ValueError('Archive and workspace roots must be separate')
    removed = {'thresholds', 'carry_forward', 'reuse', 'capped_providers', 'max_attempts',
               'grade_reserve_usd', 'call_ceiling_usd', 'min_call_budget_usd'} & CFG.keys()
    if removed:
        raise ValueError('Remove obsolete options: ' + ', '.join(sorted(removed)))
    if billing_keys(CFG):
        raise ValueError('API credential or billing configuration is prohibited')
    CFG.setdefault('runs', 1)
    if not isinstance(CFG['runs'], int) or CFG['runs'] < 1:
        raise ValueError('runs must be a positive integer')
    CFG.setdefault('run_arms', [CFG['changed_arm']])
    for arm in CFG['arms']:
        if arm not in ('with_skill', 'old_skill'):
            raise ValueError('This runner supports with_skill and old_skill; no-skill diagnosis needs another runner')
        if not re.fullmatch(r'[A-Za-z0-9_-]+', arm):
            raise ValueError('Unsafe arm name')
    if len(CFG['run_arms']) != 1 or any(a not in CFG['arms'] for a in CFG['run_arms']):
        raise ValueError('Select one configured arm per round; diagnose the baseline separately')
    for key in ('budget_usd', 'call_allowance_usd'):
        value = CFG.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f'{key} must be a finite positive number')
    CFG.setdefault('cap_seconds', 1500)
    value = CFG['cap_seconds']
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError('cap_seconds must be a finite positive number')
    CFG.setdefault('ccusage_command', ['ccusage'])
    if not isinstance(CFG['ccusage_command'], list) or not CFG['ccusage_command'] or not all(
            isinstance(x, str) and x for x in CFG['ccusage_command']):
        raise ValueError('ccusage_command must be a nonempty argv list')
    if set(CFG.get('capabilities', [])) - set(CAPABILITIES):
        raise ValueError('Unsupported capability')
    for name, target in CFG['targets'].items():
        if not require_executor:
            if isinstance(target, dict):
                target.setdefault('effort', 'high')
            continue
        if not re.fullmatch(r'[a-z0-9]+(?:[.-][a-z0-9]+)*', name) or target['adapter'] not in ADAPTERS:
            raise ValueError('Invalid target')
        if 'jobs' in target:
            raise ValueError('Calls are sequential; remove jobs')
        target.setdefault('effort', 'high')
        if 'grader' in target:
            grader = CFG['targets'][target['grader']]
            if grader['model'] == target['model']:
                raise ValueError('Blind grader must use a different model from the Executor')
    if require_executor and not executor_targets():
        raise ValueError('At least one Executor with a grader is required')


def executor_targets():
    return [name for name, target in CFG['targets'].items() if target.get('grader')]


def ledger_entries():
    ledger = iteration_dir() / '_ledger.jsonl'
    if not ledger.exists():
        return []
    # Malformed/torn records are errors, never silently discounted.
    return [json.loads(line) for line in ledger.read_text().splitlines()]


def verified_cost(entry):
    """A settled ccusage record and its ledger row must describe the same attempt."""
    path = entry.get('cost_record')
    if not isinstance(path, str):
        raise Budget('Missing linked cost record; recover the attempt before inference')
    path = Path(path).resolve()
    if not path.is_relative_to(iteration_dir().resolve()) or not path.is_file():
        raise Budget('Missing linked cost record; recover the attempt before inference')
    try:
        record = rjson(path)
        cost, tokens = usage.checked_totals(record['report'])
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise Budget('Incomplete cost record; recover the attempt before inference') from error
    if (type(record.get('cost_usd')) not in (int, float) or type(entry.get('cost_usd')) not in (int, float)
            or record.get('source') != 'ccusage' or record.get('basis') != 'api_equivalent_estimate'
            or record.get('error') or record.get('errors')
            or record.get('cost_usd') != cost or record.get('total_tokens') != tokens
            or entry.get('cost_usd') != cost or entry.get('total_tokens') != tokens
            or entry.get('source') != record['source']
            or entry.get('errors') != record.get('errors', record.get('error'))):
        raise Budget('Ledger and linked cost record disagree or are incomplete')
    return cost


def reconcile_call_cost_records(entries):
    """Require every execution and grading attempt cost file to have a ledger row."""
    root = iteration_dir()
    call_records = {path.resolve() for pattern in ('*/eval-*/*/run-*/cost.json',
                                                    '*/grading/eval-*/attempt-*/cost.json')
                    for path in root.glob(pattern)}
    linked = {Path(entry['cost_record']).resolve() for entry in entries
              if isinstance(entry.get('cost_record'), str)}
    if call_records - linked:
        raise Budget('Unaccounted attempt exists; recover its ledger entry before inference')
    if linked - call_records:
        raise Budget('Missing linked cost record; recover the attempt before inference')
    if len(linked) != len(entries):
        raise Budget('Duplicate or unlinked ledger attempt; recover its entry before inference')
    for entry in entries:
        parts = Path(entry['cost_record']).resolve().relative_to(root.resolve()).parts
        if len(parts) != 5 or parts[-1] != 'cost.json':
            raise Budget('Ledger attempt attribution is invalid; recover its entry before inference')
        eval_match = re.fullmatch(r'eval-(\d+)-[A-Za-z0-9_-]+', parts[2 if parts[1] == 'grading' else 1])
        if not eval_match or type(entry.get('eval')) is not int or entry['eval'] != int(eval_match[1]):
            raise Budget('Ledger attempt attribution is invalid; recover its entry before inference')
        if parts[1] == 'grading':
            attempt = re.fullmatch(r'attempt-(\d+)', parts[3])
            expected_grader = CFG['targets'].get(parts[0], {}).get('grader')
            valid = (attempt and entry.get('kind') == 'grade' and entry.get('executor') == parts[0]
                     and entry.get('target') == expected_grader and expected_grader is not None
                     and type(entry.get('attempt')) is int and entry['attempt'] == int(attempt[1]))
        else:
            run = re.fullmatch(r'run-(\d+)', parts[3])
            valid = (run and entry.get('kind') == 'exec' and entry.get('target') == parts[0]
                     and parts[0] in executor_targets() and parts[2] in CFG['run_arms']
                     and entry.get('arm') == parts[2]
                     and type(entry.get('run')) is int and entry['run'] == int(run[1]))
        if not valid:
            raise Budget('Ledger attempt attribution is invalid; recover its entry before inference')


def spent():
    total = 0.0
    entries = ledger_entries()
    reconcile_call_cost_records(entries)
    for entry in entries:
        total += verified_cost(entry)
    return total


def freeze_inputs():
    """Store the exact round and eval definitions before an execution or grade."""
    source = iteration_dir() / 'runner'
    source.mkdir(parents=True, exist_ok=True)
    for name in ('harness.py', 'usage.py'):
        data = (H / name).read_bytes()
        saved_source = source / name
        if saved_source.exists() and saved_source.read_bytes() != data:
            raise Halt('Runner source changed; use the archived runner or start a new round')
        if not saved_source.exists():
            saved_source.write_bytes(data)
    saved = iteration_dir() / 'round.json'
    if saved.exists() and rjson(saved) != CFG:
        raise Halt('Round configuration changed; use a new iteration to preserve evidence')
    if not saved.exists():
        wjson(saved, CFG)
    evals, digest = load_evals()
    frozen = iteration_dir() / 'evals.sha256'
    if frozen.exists() and frozen.read_text().strip() != digest:
        raise Halt('Eval assertions changed; start a new round')
    if not frozen.exists():
        frozen.write_text(digest + '\n')
    definitions = iteration_dir() / 'evals.json'
    if definitions.exists() and rjson(definitions) != {'evals': evals}:
        raise Halt('Frozen eval definitions changed; start a new round')
    if not definitions.exists():
        wjson(definitions, {'evals': evals})


def allowance():
    amount = CFG['call_allowance_usd']
    if spent() + amount > CFG['budget_usd']:
        raise Budget('Current-round budget cannot reserve another call allowance')
    return amount


def charge(entry):
    path = iteration_dir() / '_ledger.jsonl'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a') as stream:
        stream.write(json.dumps({'ts': now(), **entry}) + '\n')
        stream.flush()
        os.fsync(stream.fileno())


def prepare():
    info = {}
    for arm in CFG['run_arms']:
        revision = git('rev-parse', f"{CFG['arms'][arm]}^{{commit}}")
        dest = iteration_dir() / 'packages' / arm / CFG['skill']
        manifest = dest.parent / 'build.json'
        if dest.exists() and not manifest.exists():
            raise Halt('Frozen package has no identity record; recover it or start a new round')
        if not dest.exists():
            raw = subprocess.run(['git', '-C', CFG['repo_path'], 'archive', revision,
                                  f"skills/{CFG['skill']}"], check=True, capture_output=True).stdout
            with tempfile.TemporaryDirectory(dir=CFG['workspace_root']) as temporary:
                with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
                    archive.extractall(temporary, filter='data')
                package = Path(temporary) / 'skills' / CFG['skill']
                if any(p.is_symlink() for p in package.rglob('*')):
                    raise ValueError('Skill package symlinks are not supported in isolated evals')
                shutil.rmtree(package / 'evals', ignore_errors=True)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(package), dest)
        identity = {'skill_revision': revision, 'package_hash': tree_hash(dest)}
        if manifest.exists() and rjson(manifest) != identity:
            raise Halt('Resolved revision or frozen package changed; start a new round')
        wjson(manifest, identity)
        info[arm] = identity
    manifest = iteration_dir() / 'packages.json'
    if manifest.exists() and rjson(manifest) != info:
        raise Halt('Package revision or contents changed; start a new round')
    wjson(manifest, info)
    return info


def stage(ev, arm, adapter):
    parent = Path(tempfile.mkdtemp(prefix='ws-', dir=CFG['workspace_root'])).resolve()
    project = parent / 'project'
    project.mkdir()
    for name in ev.get('files', []):
        relative = Path(name.removeprefix('evals/files/'))
        if relative.is_absolute() or '..' in relative.parts or not name.startswith('evals/files/'):
            raise ValueError('Eval fixtures must be contained in evals/files')
        source = Path(CFG['repo_path']) / 'skills' / CFG['skill'] / name
        if source.is_symlink():
            raise ValueError('Fixture symlinks are not supported')
        dest = project / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    install = parent / 'skills' / CFG['skill']
    shutil.copytree(iteration_dir() / 'packages' / arm / CFG['skill'], install)
    return {'parent': parent, 'project': project, 'install': install, 'home': new_home(adapter)}


def call(argv, cwd, env, transcript, stderr):
    started = time.monotonic()
    with transcript.open('wb') as out, stderr.open('wb') as err:
        try:
            process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                       stdout=out, stderr=err, start_new_session=True)
        except OSError:
            err.write(b'CLI could not be started\n')
            rc = 127
        else:
            try:
                rc = process.wait(timeout=CFG.get('cap_seconds', 1500))
            except subprocess.TimeoutExpired:
                import signal
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                rc = -14
            except BaseException:
                import signal
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except OSError:
                    pass
                while True:
                    try:
                        process.wait()
                        break
                    except KeyboardInterrupt:
                        continue
                    except BaseException:
                        break
                raise
    return rc, int((time.monotonic() - started) * 1000)


def child_readouts(adapter, sessions):
    readouts = []
    if not sessions.exists():
        return readouts
    if adapter.NAME == 'codex':
        for path in sorted(sessions.rglob('*.jsonl')):
            rows = events(path)
            meta = next((e.get('payload', {}) for e in rows if e.get('type') == 'session_meta'), {})
            source = meta.get('source', {})
            if not (meta.get('parent_thread_id') or isinstance(source, dict) and source.get('subagent')):
                continue
            texts = []
            for row in rows:
                payload = row.get('payload', {})
                item = payload.get('item', {})
                if payload.get('type') == 'agent_message':
                    texts.append(payload.get('message', ''))
                elif payload.get('type') == 'task_complete' and payload.get('last_agent_message'):
                    texts.append(payload['last_agent_message'])
                elif item.get('type') == 'AgentMessage':
                    texts.append(item.get('text', ''))
                elif row.get('type') == 'response_item' and payload.get('role') == 'assistant':
                    texts.extend(c.get('text', '') for c in payload.get('content', []) if c.get('type') == 'output_text')
            readouts.append({'session': path.name, 'final_readout': texts[-1] if texts else None,
                             'dispatch_prompt': 'unavailable: encrypted; exact prompt cannot be inferred'})
    elif adapter.NAME == 'grok':
        for path in sorted(sessions.rglob('summary.json')):
            if rjson(path).get('session_kind') not in ('subagent', 'subagent_resume'):
                continue
            updates = path.parent / 'updates.jsonl'
            texts = []
            for row in events(updates) if updates.exists() else []:
                update = row.get('params', {}).get('update', row)
                if update.get('sessionUpdate') == 'agent_message_chunk':
                    texts.append(update.get('content', {}).get('text', ''))
                elif update.get('type') == 'text':
                    texts.append(update.get('data', ''))
            readouts.append({'session': path.parent.name, 'final_readout': ''.join(texts) or None})
    return readouts



def cli_version(binary, env, cwd):
    result = subprocess.run([binary, '--version'], env=env, cwd=cwd,
                            capture_output=True, text=True, timeout=30, check=True)
    version = result.stdout.strip()
    if not version:
        raise Halt('CLI version unavailable; no inference launched')
    return version


def invoke(target, kind, directory, cwd, home, make_argv, metadata):
    """Persist pending charge before launch; every attempt has its own evidence directory."""
    adapter, target_config = adapter_of(target), CFG['targets'][target]
    budget = allowance()
    env = child_env(adapter, home)
    transcript, stderr, final = directory / 'transcript', directory / 'stderr.txt', directory / 'final.md'
    argv = make_argv(final, budget)
    binary = shutil.which(argv[0], path=BASE_PATH)
    if not binary:
        raise Halt(f'{adapter.NAME}: CLI binary not found on PATH')
    argv[0] = binary
    version = cli_version(binary, env, cwd)
    directory.mkdir(parents=True, exist_ok=False)
    record = {'kind': kind, 'target': target, 'provider': adapter.PROVIDER, 'model': target_config['model'],
              'cost_record': str(directory / 'cost.json'), 'cost_usd': None, **metadata}
    # A crash before settlement leaves an unknown ledger entry and blocks the next call.
    wjson(directory / 'cost.json', {'source': 'ccusage', 'cost_usd': None, 'total_tokens': None,
                                    'errors': ['Attempt pending settlement']})
    charge(record)
    transcript.touch()
    stderr.touch()
    trace = new_trace()
    rc, ms = call(argv, cwd, env, transcript, stderr)
    # An interrupted call keeps its pending, unknown charge for operator recovery.
    # After a completed call, cost/session failures preserve the attempt and HOME.
    sessions = directory / 'sessions'
    if adapter.SESSIONS and (home / adapter.SESSIONS).exists():
        shutil.copytree(home / adapter.SESSIONS, sessions)
    try:
        trace = parse(adapter, transcript, final)
        trace['child_readouts'] = child_readouts(adapter, sessions)
    except (ValueError, KeyError, TypeError) as error:
        trace['is_error'] = True
        wjson(directory / 'parse-error.json', {'error': str(error)})
    try:
        cost = usage.estimate(adapter.NAME, transcript, sessions if sessions.exists() else None,
                              directory / 'cost.json', CFG['ccusage_command'], Path(CFG['workspace_root']),
                              model=target_config['model'])
    except Exception:
        cost = {'source': 'ccusage', 'cost_usd': None, 'total_tokens': None,
                'errors': ['Usage estimator failed; inspect preserved attempt before resolving']}
    wjson(directory / 'cost.json', cost)
    record.update(cost_usd=cost.get('cost_usd'), total_tokens=cost.get('total_tokens'),
                  source=cost.get('source'), errors=cost.get('errors', cost.get('error')),
                  cli_cost_usd=trace['cost_usd'])
    rows = ledger_entries()
    rows[-1] = {'ts': rows[-1]['ts'], **record}
    temporary = iteration_dir() / '_ledger.tmp'
    temporary.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    temporary.replace(iteration_dir() / '_ledger.jsonl')
    wjson(directory / 'invocation.json', {'command': argv, 'rc': rc, 'duration_ms': ms,
                                        'model': target_config['model'], 'allowance_usd': budget, 'harness_version': version})
    wjson(directory / 'trace.json', trace)
    final.write_text(trace['final_text'])
    return trace, rc, ms, argv, cost


def service_failure(rc, trace, stderr, transcript=''):
    # Successful answers may discuss hypothetical quota/auth failures in the eval.
    said = stderr
    if rc or trace['is_error']:
        said += trace['final_text'] + transcript
    if re.search(r'usage limit|session limit|out of credits|credits exhausted|quota|login required|not logged in|unauthorized|authentication failed|token expired|\b401\b', said, re.I):
        return 'login_or_quota'
    if rc == -14:
        return 'timeout'
    return 'error' if rc or trace['is_error'] or not (trace['final_text'].strip() or trace['structured']) else None


def observations(trace, before=None, after=None, skill_package_unchanged=True):
    # Keep raw tool outputs in trace.json; reads of the installed skill reveal its text.
    actions = [{k: call[k] for k in ('name', 'by', 'input') if k in call} for call in trace['tool_calls']]
    result = {'tool_calls': actions, 'child_readouts': trace.get('child_readouts', []),
              'skill_package_unchanged': skill_package_unchanged,
              'dispatch_visibility': 'Encrypted dispatch prompts are unavailable; never infer their exact text.'}
    if before is not None:
        result['filesystem'] = {'before': before, 'after': after,
                                'limitation': 'Snapshots cannot detect writes later undone or outside the workspace.'}
    return result


def execute_one(target, ev, arm, k, ev_sha, packages):
    freeze_inputs()
    rd, adapter = run_dir(target, ev, arm, k), adapter_of(target)
    # One execution per configured slot; failed attempts are evidence, not automatic retries.
    if rd.exists():
        if status_of(rd) == 'login_or_quota':
            raise Halt('Round contains a login/quota failure; resolve access and start a new round')
        return status_of(rd)
    allowance()
    subscription_guard(adapter)
    ws = stage(ev, arm, adapter)
    prompt = wrapper(ws['install'], staged_prompt(ev))
    before = snapshot(ws['project']) if CFG.get('observe_filesystem', True) else None
    installed_hash = tree_hash(ws['install'])
    try:
        trace, rc, ms, argv, cost = invoke(target, 'exec', rd, ws['project'], ws['home'],
            lambda final, budget: adapter.exec_argv(CFG['targets'][target], ws, prompt, final, budget,
                                                    CFG.get('capabilities', [])),
            {'eval': ev['id'], 'arm': arm, 'run': k})
        idn = identity(trace, ws, adapter, argv)
        package_unchanged = tree_hash(ws['install']) == installed_hash
        failure = service_failure(rc, trace, (rd / 'stderr.txt').read_text(errors='replace'),
                                  (rd / 'transcript').read_text(errors='replace'))
        surface_unverified = (idn['init_surface_ok'] is not True if adapter.NAME == 'grok'
                              else idn['init_surface_ok'] is False)
        status = failure or ('discarded' if not package_unchanged or not idn['loaded_paths'] or idn['foreign_access'] or
                             idn['nested_agent_cli'] or surface_unverified else 'ok')
        outputs = rd / 'outputs'
        outputs.mkdir()
        shutil.copy2(rd / 'final.md', outputs / 'final.md')
        capture_error = None
        after = None
        try:
            require_project_root(ws['project'])
            for path in ws['project'].rglob('*'):
                mode = path.lstat().st_mode
                if not (stat_module.S_ISREG(mode) or stat_module.S_ISDIR(mode)
                        or stat_module.S_ISLNK(mode)):
                    raise ValueError(f'Unsupported project artifact: {path.relative_to(ws["project"])}')
            shutil.copytree(ws['project'], outputs / 'project', symlinks=True)
            after = snapshot(ws['project']) if before is not None else None
        except (OSError, ValueError, shutil.Error) as error:
            capture_error = f'Project artifact capture failed: {error}'
            shutil.rmtree(outputs / 'project', ignore_errors=True)
            status = failure or 'discarded'
        wjson(outputs / 'observations.json', observations(trace, before, after, package_unchanged))
        wjson(rd / 'build.json', {**packages[arm], 'model': CFG['targets'][target]['model'],
              'effort': CFG['targets'][target]['effort'], 'adapter': adapter.NAME,
              'harness_version': rjson(rd / 'invocation.json')['harness_version'], 'workspace': str(ws['parent']), 'home': str(ws['home']),
              'install_path': str(ws['install']), 'eval_inputs_sha256': ev_sha})
        wjson(rd / 'timing.json', {'duration_ms': ms, 'total_tokens': cost.get('total_tokens'),
                                  'cost_usd': cost.get('cost_usd'), 'cli_cost_usd': trace['cost_usd']})
        wjson(rd / 'metrics.json', {'total_tool_calls': len(trace['tool_calls']), 'errors_encountered': trace['errors']})
        wjson(rd / 'status.json', {'status': status, 'identity': idn, 'rc': rc, 'finished': now(),
                                  **({'capture_error': capture_error} if capture_error else {})})
    except BaseException:
        # Preflight never launched or persisted an attempt; remove copied auth and scratch.
        # Keep a failed persistence attempt's HOME for recovery.
        if not rd.exists():
            drop_home(ws['home'])
            shutil.rmtree(ws['parent'])
        raise
    else:
        drop_home(ws['home'])
        shutil.rmtree(ws['parent'])
    if status == 'login_or_quota':
        raise Halt('Login/quota failure; stop and resolve subscription access. No fallback.')
    spent()  # Unknown cost stops this command before it can continue.
    return status


def run_round(targets):
    packages = prepare()
    evals, digest = selected_evals(), load_evals()[1]
    results = [execute_one(target, ev, arm, k, digest, packages)
               for target in targets for ev in evals for arm in CFG['run_arms']
               for k in range(1, CFG['runs'] + 1)]
    return all(status == 'ok' for status in results)


def counted_runs(target, ev):
    runs = [(a, k, run_dir(target, ev, a, k)) for a in CFG['run_arms'] for k in range(1, CFG['runs'] + 1)]
    return [(a, k, rd, status_of(rd)) for a, k, rd in runs if status_of(rd) == 'ok'], [
        f'{a}/run-{k}:{status_of(rd)}' for a, k, rd in runs if status_of(rd) != 'ok']


def grade_one(target, ev):
    freeze_inputs()
    runs, missing = counted_runs(target, ev)
    grader = CFG['targets'][target]['grader']
    grader_model = CFG['targets'][grader]['model']
    if any(checked_grading(rd, ev, grader_model)[1] for _, _, rd, _ in runs):
        return False  # Preserve malformed evidence for explicit operator recovery.
    pending = [r for r in runs if not (r[2] / 'grading.json').exists()]
    if not pending:
        return not missing
    if CFG['targets'][grader]['model'] == CFG['targets'][target]['model']:
        raise ValueError('Grader must be a different model')
    adapter = adapter_of(grader)
    allowance()
    subscription_guard(adapter)
    packet, key = build_packet(ev, pending, f"{target}:{ev['id']}:{CFG['iteration']}")
    gdir = iteration_dir() / target / 'grading' / eval_dir_name(ev)
    gdir.mkdir(parents=True, exist_ok=True)
    attempt = 1
    while (gdir / f'attempt-{attempt}').exists():
        attempt += 1
    directory = gdir / f'attempt-{attempt}'
    cwd = Path(tempfile.mkdtemp(prefix='grade-', dir=CFG['workspace_root']))
    home = new_home(adapter)
    schema = cwd / 'schema.json'
    wjson(schema, GRADE_SCHEMA)
    try:
        trace, rc, ms, argv, cost = invoke(grader, 'grade', directory, cwd, home,
            lambda final, budget: adapter.grade_argv(CFG['targets'][grader], packet, final, budget, schema),
            {'executor': target, 'eval': ev['id'], 'attempt': attempt})
        (directory / 'packet.txt').write_text(packet)
        wjson(directory / 'key.json', key)
        failure = service_failure(rc, trace, (directory / 'stderr.txt').read_text(errors='replace'),
                                  (directory / 'transcript').read_text(errors='replace'))
        error = failure or ('grader used tools' if trace['tool_calls'] else validate(trace['structured'], key, len(ev['assertions'])))
        wjson(directory / 'validation.json', {'valid': error is None, 'error': error})
        if error is None:
            for row in trace['structured']['grades']:
                write_grading(Path(key[row['letter']]['run_dir']), ev, row['items'],
                              {'model': CFG['targets'][grader]['model'], 'effort': CFG['targets'][grader]['effort'],
                               'harness': adapter.NAME, 'packet': str(directory / 'packet.txt'), 'letter': row['letter']})
    except BaseException:
        if not directory.exists():
            drop_home(home)
            shutil.rmtree(cwd)
        raise
    else:
        drop_home(home)
        shutil.rmtree(cwd)
    if failure == 'login_or_quota':
        raise Halt('Grader login/quota failure; no fallback')
    spent()
    return error is None and not missing


def grade_round(targets):
    results = [grade_one(target, ev) for target in targets for ev in selected_evals()]
    return all(results)


def report(targets=None):
    global CFG
    live = CFG
    archive = iteration_dir()
    saved = archive / 'round.json'
    definitions = archive / 'evals.json'
    digest_file = archive / 'evals.sha256'
    issues = []
    frozen_cfg = rjson(saved) if saved.exists() else None
    if frozen_cfg is None:
        issues.append('Frozen round configuration is missing')
    elif frozen_cfg != live:
        issues.append('Current round configuration differs from the frozen configuration')
    frozen_evals = rjson(definitions)['evals'] if definitions.exists() else None
    if frozen_evals is None or not digest_file.exists():
        issues.append('Frozen eval definitions or digest are missing')
    else:
        try:
            if load_evals()[1] != digest_file.read_text().strip():
                issues.append('Current eval inputs differ from the frozen inputs')
        except (OSError, ValueError, KeyError):
            issues.append('Current eval inputs cannot be verified')
    CFG = frozen_cfg or live
    try:
        selected = targets if targets is not None else executor_targets()
        if any(target not in executor_targets() for target in selected):
            raise ValueError('Report targets must name frozen configured Executors')
        return _report(selected, frozen_evals, issues)
    finally:
        CFG = live


def _report(targets, frozen_evals, identity_issues):
    written = []
    all_evals = frozen_evals if frozen_evals is not None else load_evals()[0]
    only = [int(x) for x in ARGS.evals.split(',') if x] if ARGS and ARGS.evals else CFG.get('evals') or []
    evals = [ev for ev in all_evals if not only or ev['id'] in only]
    if not evals or set(only) - {ev['id'] for ev in evals}:
        raise ValueError('Eval selection is empty or contains unknown IDs')
    package_manifest = iteration_dir() / 'packages.json'
    packages = rjson(package_manifest) if package_manifest.exists() else None
    if not isinstance(packages, dict):
        packages = None
    if packages is None:
        identity_issues.append('Frozen package manifest is missing')
    else:
        for arm in CFG['run_arms']:
            package = iteration_dir() / 'packages' / arm / CFG['skill']
            recorded = packages.get(arm)
            if (not package.is_dir() or not isinstance(recorded, dict)
                    or recorded.get('package_hash') != tree_hash(package)):
                identity_issues.append(f'Frozen package identity differs for {arm}')
    for target in targets:
        rows, per = [], {}
        target_issues = list(identity_issues)
        for ev in evals:
            for arm in CFG['run_arms']:
                for k in range(1, CFG['runs'] + 1):
                    rd = run_dir(target, ev, arm, k)
                    status = status_of(rd)
                    row = {'eval_id': ev['id'], 'eval_name': eval_name(ev), 'configuration': arm,
                           'run_number': k, 'status': status, 'archive_ref': str(rd.relative_to(CFG['archive_root']))}
                    if status == 'unavailable':
                        target_issues.append(f'{arm}/run-{k}: status.json is unavailable; recover the saved run evidence')
                    grade, grade_issue = checked_grading(
                        rd, ev, CFG['targets'][CFG['targets'][target]['grader']]['model'])
                    if grade_issue:
                        target_issues.append(f'{arm}/run-{k}: {grade_issue}')
                    timing, timing_issue = report_run_object(rd / 'timing.json')
                    metrics, metrics_issue = report_run_object(rd / 'metrics.json')
                    build, build_issue = report_run_object(rd / 'build.json')
                    if timing is not None and (type(timing.get('duration_ms')) not in (int, float) or
                                               not math.isfinite(timing['duration_ms']) or timing['duration_ms'] < 0):
                        timing, timing_issue = None, 'timing.json has invalid duration_ms; recover the saved run evidence'
                    for issue in (timing_issue, metrics_issue, build_issue):
                        if issue:
                            target_issues.append(f'{arm}/run-{k}: {issue}')
                    timing, metrics = timing or {}, metrics or {}
                    frozen_digest = iteration_dir() / 'evals.sha256'
                    if row['status'] == 'ok' and build is None:
                        target_issues.append(f'Run identity is missing for {arm}/run-{k}')
                    if build is not None and (not frozen_digest.exists() or
                            build.get('eval_inputs_sha256') != frozen_digest.read_text().strip()
                            or build.get('model') != CFG['targets'][target]['model']
                            or build.get('effort') != CFG['targets'][target]['effort']
                            or build.get('adapter') != CFG['targets'][target]['adapter']
                            or not packages or any(build.get(field) != packages.get(arm, {}).get(field)
                                                   for field in ('skill_revision', 'package_hash'))):
                        target_issues.append(f'Run identity differs for {arm}/run-{k}')
                    row['harness_version'] = build.get('harness_version') if build else None
                    if grade and grade.get('grader', {}).get('model') != CFG['targets'][CFG['targets'][target]['grader']]['model']:
                        target_issues.append(f'Grader identity differs for {arm}/run-{k}')
                    if grade and [item.get('text') for item in grade.get('assertion_results', [])] != ev['assertions']:
                        target_issues.append(f'Graded assertions differ for {arm}/run-{k}')
                    row['result'] = {'pass_rate': grade['summary']['pass_rate'] if grade else None,
                                     'time_seconds': None if timing_issue else timing.get('duration_ms', 0) / 1000,
                                     'tokens': timing.get('total_tokens'), 'cost_usd': timing.get('cost_usd'),
                                     'tool_calls': metrics.get('total_tool_calls'), 'errors': metrics.get('errors_encountered')}
                    if grade:
                        row['result'].update({x: grade['summary'][x] for x in ('passed', 'failed', 'total')})
                        row['assertion_results'] = grade['assertion_results']
                    row['needs_operator_review'] = (row['status'] != 'ok' or not grade
                                                    or grade['summary']['pass_rate'] is None
                                                    or grade['summary']['failed'] > 0)
                    for metric in ('pass_rate', 'time_seconds', 'tokens'):
                        value = row['result'][metric]
                        if value is not None and grade:
                            per.setdefault(arm, {}).setdefault(metric, []).append(value)
                    rows.append(row)
        charges = []
        try:
            entries = ledger_entries()
            charges = [entry for entry in entries if
                       entry.get('kind') == 'exec' and entry.get('target') == target or
                       entry.get('kind') == 'grade' and entry.get('executor') == target]
            reconcile_call_cost_records(entries)
            charge_costs = [verified_cost(entry) for entry in charges]
            known, cost_issue = True, None
        except (Budget, OSError, UnicodeError, ValueError, TypeError, AttributeError, KeyError) as error:
            charges, charge_costs, known = [], [], False
            cost_issue = f'Ledger costs are unavailable until operator recovery: {error}'
        if target_issues or cost_issue:
            for row in rows:
                row['needs_operator_review'] = True
                if cost_issue:
                    row['result']['cost_usd'] = None
        t = CFG['targets'][target]
        metadata = {'skill_name': CFG['skill'], 'executor_model': t['model'], 'timestamp': now(),
                    'runs_per_configuration': CFG['runs'], 'harness': ', '.join(sorted({r['harness_version'] for r in rows if r['harness_version']})) or t['adapter'],
                    'grader': CFG['targets'][t['grader']]['model'], 'cost_available': known,
                    'identity_verified': not target_issues,
                    'archive_ref': str((iteration_dir() / target).relative_to(CFG['archive_root']))}
        if known:
            metadata['cost_usd'] = sum(charge_costs)
        complete = not target_issues and known and all(row['status'] == 'ok' and row['result']['pass_rate'] is not None for row in rows)
        tested_arm = CFG['run_arms'][0]
        revision = (packages or {}).get(tested_arm, {}).get('skill_revision', CFG['arms'][tested_arm])[:8]
        filename = f"{now()[:10]}-{revision}--iteration-{CFG['iteration']}-{target}.json"
        out = iteration_dir() / target / ('benchmark' if complete else 'incomplete') / filename
        public_charges = [{k: v for k, v in entry.items() if k in (
            'kind', 'target', 'executor', 'provider', 'model', 'cost_usd', 'total_tokens', 'source', 'cli_cost_usd')}
            for entry in charges]
        wjson(out, {'metadata': metadata, 'runs': rows,
                    'run_summary': {a: {m: stat(v) for m, v in values.items()} for a, values in per.items()},
                    'cost_records': public_charges,
                    'notes': [*sorted(set(target_issues)), *([cost_issue] if cost_issue else []),
                              'Raw results only; inspect every failure and attribute it before the operator decides to ship.',
                              'Run the old skill separately on failing cases; no aggregate cross-cohort deltas are computed.',
                              'Costs include executions and grading attempts, across providers, in this round only. API-equivalent estimates are not subscription bills.']})
        written.append(out)
    return written



def check_pricing_tool():
    try:
        subprocess.run([*CFG['ccusage_command'], '--version'], capture_output=True,
                       text=True, timeout=30, check=True)
    except (OSError, subprocess.SubprocessError) as error:
        raise Halt('ccusage is unavailable; install or configure it before inference') from error


def isolation_check(targets):
    """Static zero-inference checks; CLI runtime isolation is checked on each saved trace."""
    if ancestors_with_agent_files(Path(CFG['workspace_root'])):
        raise Halt('Workspace ancestors contain agent configuration')
    for name in {n for t in targets for n in (t, CFG['targets'][t]['grader'])}:
        adapter = adapter_of(name)
        subscription_guard(adapter)
        if not shutil.which(adapter.BIN, path=BASE_PATH):
            raise Halt(f'{adapter.NAME}: binary not found on PATH')
        home = new_home(adapter)
        try:
            env = child_env(adapter, home)
            if any(k.endswith('_API_KEY') for k in env):
                raise Halt('API-key environment escaped the subscription guard')
        finally:
            drop_home(home)
    check_pricing_tool()
    print('Static isolation checks passed; runtime tool surfaces still require trace validation.')
    return 0


def detector_check():
    """Use the same fake-subprocess suite as development; never invokes an inference CLI."""
    import unittest
    suite = unittest.defaultTestLoader.discover(str(H), pattern='test_harness.py')
    return int(not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())


def main():
    global ARGS, CFG
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['run', 'grade', 'report', 'isolation-check', 'detector-check'])
    parser.add_argument('--round', required=True, help='Private config outside the source repository')
    parser.add_argument('--targets', default='')
    parser.add_argument('--evals', default='')
    ARGS = parser.parse_args()
    CFG = rjson(Path(ARGS.round))
    validate_config(ARGS.round, require_executor=ARGS.command != 'report')
    targets = ARGS.targets.split(',') if ARGS.targets else None
    if ARGS.command != 'report' and targets is None:
        targets = executor_targets()
    if ARGS.command != 'report' and any(t not in executor_targets() for t in targets):
        raise ValueError('--targets must name configured Executors')
    if ARGS.command == 'detector-check':
        return detector_check()
    Path(CFG['workspace_root']).mkdir(parents=True, exist_ok=True)
    iteration_dir().mkdir(parents=True, exist_ok=True)
    with (iteration_dir() / '.harness.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if ARGS.command == 'report':
            for path in report(targets):
                print(path)
            return 0
        if ARGS.command == 'isolation-check':
            return isolation_check(targets)
        if ancestors_with_agent_files(Path(CFG['workspace_root'])):
            raise Halt('Workspace ancestors contain agent configuration')
        freeze_inputs()
        for name in {n for t in targets for n in (t, CFG['targets'][t]['grader'])}:
            subscription_guard(adapter_of(name))
        check_pricing_tool()
        spent()
        return int(not (run_round(targets) if ARGS.command == 'run' else grade_round(targets)))


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (Budget, Halt, ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
