#!/usr/bin/env python3
"""Render a run's events.jsonl into a reviewable transcript.

Usage: render.py <run-dir> <workspace-dir> [case] [arm]

Writes <run-dir>/response.md and <run-dir>/transcript.json (case, arm, context
and every turn, including tool calls and results), replacing the workspace
path with <workspace>, the home directory with ~, temporary paths with <tmp>,
and the user name with "user" so the transcript can be committed. Prints one
JSON line with the model, cost, tokens, duration, tool counts and skill loads.
"""
import getpass
import json
import os
import re
import sys
from pathlib import Path

run, ws = Path(sys.argv[1]), sys.argv[2]
case = sys.argv[3] if len(sys.argv) > 3 else None
arm = sys.argv[4] if len(sys.argv) > 4 else None
prefixes = sorted({ws, os.path.realpath(ws)}, key=len, reverse=True)
home = os.path.expanduser("~")
config = os.environ.get("CLAUDE_CONFIG_DIR")
user = getpass.getuser()
# Temporary paths and Claude's encoded project folder names embed the
# workspace location and the user name.
TEMP = re.compile(r"(/private)?/(tmp|var/folders)/[^\s\"'`)]*|-private-tmp-[^\s/\"'`)]*")


def scrub(text):
    for p in prefixes:
        text = text.replace(p, "<workspace>")
    if config:
        text = text.replace(config, "<claude-config>")
    text = TEMP.sub("<tmp>", text.replace(home, "~"))
    # Orca keeps one Claude config folder per profile; earlier runs may have used
    # a profile other than the current one. Split "~" so this file holds no home path.
    profiles = re.escape("~" + "/Library/Application Support/orca/claude-profiles/")
    text = re.sub(profiles + r"[0-9a-f-]+/home", "<claude-config>", text)
    text = re.sub(rf"\b{re.escape(user)}\b", "user", text)
    return "\n".join(line.rstrip() for line in text.split("\n"))


init, result, turns, final, tools = {}, {}, [], "", {}
skills = []
for raw in (run / "events.jsonl").read_text().splitlines():
    if not raw.strip():
        continue
    e = json.loads(raw)
    kind = e.get("type")
    if kind == "system" and e.get("subtype") == "init":
        init = e
    elif kind == "assistant":
        for b in e["message"].get("content", []):
            if b["type"] == "text" and b["text"].strip():
                final = b["text"].strip()
                turns.append({"role": "assistant", "content": scrub(final)})
            elif b["type"] == "tool_use":
                tools[b["name"]] = tools.get(b["name"], 0) + 1
                if b["name"] == "Skill":
                    skills.append(b["input"].get("skill"))
                turns.append({"role": "assistant", "tool_call": b["name"],
                              "input": json.loads(scrub(json.dumps(b["input"], ensure_ascii=False)))})
    elif kind == "user":
        content = e["message"].get("content", [])
        for b in content if isinstance(content, list) else []:
            if b.get("type") == "tool_result":
                c = b.get("content")
                if isinstance(c, list):
                    c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                turns.append({"role": "tool", "is_error": bool(b.get("is_error")), "content": scrub(str(c))})
    elif kind == "result":
        result = e

final = result.get("result") or final
(run / "response.md").write_text(scrub(final) + "\n")
if case:
    # The prompt is the text after the case's settings block.
    prompt = (Path(__file__).parent / case / "prompt.md").read_text().split("---\n", 2)[2].strip()
    turns.insert(0, {"role": "user", "content": prompt})
context ={"model": init.get("model"), "effort": "high",
           "runtime": f"Claude Code {init.get('claude_code_version')} via claude -p",
           "working_directory": "<workspace>"}
doc = {"case": case, "arm": arm, "context": context, "turns": turns}
(run / "transcript.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
usage = result.get("usage", {})
print(json.dumps({
    "model": init.get("model"),
    "claude_code": init.get("claude_code_version"),
    "finished": result.get("subtype") == "success",
    "seconds": round(result.get("duration_ms", 0) / 1000, 1),
    "cost_usd": result.get("total_cost_usd"),
    "input_tokens": usage.get("input_tokens"),
    "cache_read_tokens": usage.get("cache_read_input_tokens"),
    "cache_write_tokens": usage.get("cache_creation_input_tokens"),
    "output_tokens": usage.get("output_tokens"),
    "tools": tools,
    "skills_loaded": skills,
}))
