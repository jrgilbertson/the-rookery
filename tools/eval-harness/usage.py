"""Price isolated run records with ccusage; keep provider charges separate.

ccusage owns the upstream prices and token-cost arithmetic. All amounts from
this module are API-equivalent estimates, not subscription debits.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def events(path: Path) -> list[dict]:
    raw = path.read_text()
    try:
        value = json.loads(raw)
        if isinstance(value, dict):
            return [value]
    except ValueError:
        pass
    rows = []
    for number, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            raise ValueError(f"Malformed usage JSONL at line {number}") from None
        if not isinstance(row, dict):
            raise ValueError(f"Expected usage JSONL object at line {number}")
        rows.append(row)
    return rows


def claude_rows(trace: list[dict], timestamp: str) -> list[dict]:
    """Completed modelUsage is cumulative and includes delegated work.

Streaming assistant events can contain only initial usage. Adapt the final
per-model summary to ccusage's usage-record format instead of pricing those
partial events. Per-model cache-write TTL is not supplied by modelUsage, so
ccusage's default cache-write estimate applies; retain that limitation.
    """
    results = [e for e in trace if e.get("type") == "result" and e.get("modelUsage")]
    if not results:
        raise ValueError("no completed per-model Claude usage")
    return [{"type": "assistant", "timestamp": timestamp, "requestId": f"model-{i}", "uuid": f"model-{i}",
             "sessionId": "run",
             "message": {"id": f"model-{i}", "type": "message", "role": "assistant",
                         "content": [], "model": model, "usage": {
                 "input_tokens": u["inputTokens"], "output_tokens": u["outputTokens"],
                 "cache_read_input_tokens": u["cacheReadInputTokens"],
                 "cache_creation_input_tokens": u["cacheCreationInputTokens"]}}}
            for i, (model, u) in enumerate(results[-1]["modelUsage"].items())]


def grok_rows(trace: list[dict], timestamp: str) -> tuple[list[dict], int]:
    """Adapt the completed root summary, which already includes child usage.

The CLI summary excludes cached tokens from inputTokens; Grok session updates
include them. Reproduce that native update shape for ccusage, including each
model separately. Never add reasoning tokens to output a second time.
    """
    results = [e for e in trace if e.get("modelUsage") and
               (e.get("type") == "end" or e.get("stopReason") == "end_turn")]
    if not results:
        raise ValueError("no completed per-model Grok usage")
    models = {}
    for model, u in results[-1]["modelUsage"].items():
        cached, created = u["cacheReadInputTokens"], u["cacheCreationInputTokens"]
        inputs, outputs = u["inputTokens"] + cached + created, u["outputTokens"]
        models[model] = {"inputTokens": inputs, "outputTokens": outputs,
                         "cachedReadTokens": cached, "cacheCreationTokens": created,
                         "totalTokens": inputs + outputs}
    total = sum(u["totalTokens"] for u in models.values())
    update = {"sessionUpdate": "turn_completed", "usage": {
        "inputTokens": sum(u["inputTokens"] for u in models.values()),
        "outputTokens": sum(u["outputTokens"] for u in models.values()),
        "totalTokens": total, "modelUsage": models}}
    return [{"timestamp": timestamp, "method": "_x.ai/session/update",
             "params": {"sessionId": "run", "update": update}}], total


def checked_totals(report: dict) -> tuple[float, int]:
    if not isinstance(report, dict):
        raise ValueError("ccusage report is not an object")
    sessions, totals = report.get("sessions"), report.get("totals", {})
    if not isinstance(sessions, list) or not isinstance(totals, dict):
        raise ValueError("ccusage report shape is unavailable")
    if not sessions:
        raise ValueError("ccusage found no completed usage records")
    def incomplete(value):
        if isinstance(value, dict):
            return any(bool(value.get(k)) for k in ("missingPricing", "unpricedModels", "isFallback")) or any(incomplete(v) for v in value.values())
        return isinstance(value, list) and any(incomplete(v) for v in value)
    if incomplete(report):
        raise ValueError("ccusage reported missing prices or a fallback model")
    cost = totals.get("costUSD", totals.get("totalCost"))
    tokens = totals.get("totalTokens")
    if (isinstance(cost, bool) or not isinstance(cost, (int, float))
            or not math.isfinite(cost) or cost < 0):
        raise ValueError("ccusage returned an invalid cost")
    if isinstance(tokens, bool) or not isinstance(tokens, int) or tokens < 0:
        raise ValueError("ccusage returned invalid token usage")
    if tokens and cost == 0:
        raise ValueError("zero cost for nonzero usage: price availability is unverified")
    return cost, tokens


def estimate(adapter: str, transcript: Path, sessions: Path | None,
             output: Path, command: list[str], scratch_root: Path, model: str | None = None) -> dict:
    """Return a recorded estimate or explicit unknown; never hide a failed lookup.

Only the supplied run is made visible to ccusage. The source transcript and
session store remain untouched. No credential is copied into the cost input.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {"source": "ccusage", "basis": "api_equivalent_estimate",
              "retrieved_at": timestamp, "cost_usd": None, "total_tokens": None}
    try:
        with tempfile.TemporaryDirectory(prefix="usage-", dir=scratch_root) as raw:
            root = Path(raw)
            env = {k: v for k, v in os.environ.items() if k not in (
                "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "XAI_API_KEY",
                "CLAUDE_CONFIG_DIR", "CODEX_HOME", "GROK_HOME")}
            env["XDG_CACHE_HOME"] = str(scratch_root / "ccusage-cache")
            expected_tokens = None
            if adapter == "claude":
                dest = root / "projects/run/usage.jsonl"
                dest.parent.mkdir(parents=True)
                rows = claude_rows(events(transcript), timestamp)
                expected_tokens = sum(sum(row["message"]["usage"].values()) for row in rows)
                dest.write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in rows))
                env["CLAUDE_CONFIG_DIR"] = str(root)
                record["limitations"] = ["Per-model cache-write TTL and request-size tiers are unavailable in the aggregate CLI summary."]
            elif adapter == "codex":
                trace = events(transcript)
                turns = [e["type"] for e in trace if e.get("type") in ("turn.completed", "turn.failed", "error")]
                if not turns or turns[-1] != "turn.completed":
                    raise ValueError("Codex attempt has no complete terminal usage")
                if sessions and sessions.is_dir():
                    for path in sessions.rglob("*.jsonl"):
                        if not events(path):
                            raise ValueError("Empty native Codex session record")
                    shutil.copytree(sessions, root / "sessions")
                    env["CODEX_HOME"] = str(root)
                else:
                    # Tool-enabled aggregates lose child usage and per-request tier context.
                    if any(e.get("type") in ("item.started", "item.completed") and
                           e.get("item", {}).get("type") not in ("agent_message", "reasoning") for e in trace):
                        raise ValueError("Tool-enabled Codex calls require native session records")
                    # Tool-free ephemeral graders expose turn.completed in exec JSON.
                    dest = root / "exec.jsonl"
                    if not model:
                        raise ValueError("ephemeral Codex usage requires the recorded invocation model")
                    context = {"type": "turn_context", "timestamp": timestamp, "payload": {"model": model}}
                    dest.write_text(json.dumps(context, separators=(",", ":")) + "\n" + transcript.read_text())
                    record["model_source"] = "recorded invocation"
                    env["CODEX_HOME"] = str(root)
            elif adapter == "grok":
                rows, expected_tokens = grok_rows(events(transcript), timestamp)
                dest = root / "sessions/run/updates.jsonl"
                dest.parent.mkdir(parents=True)
                dest.write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in rows))
                env["GROK_HOME"] = str(root)
                record["limitations"] = ["Grok reports aggregate turn usage; request-size tier estimates may differ from per-request billing."]
            else:
                raise ValueError(f"unsupported usage-record adapter: {adapter}")
            version = subprocess.run([*command, "--version"], env=env, cwd=root,
                                     capture_output=True, text=True, timeout=30, check=True)
            record["version"] = version.stdout.strip()
            config = root / "ccusage.json"
            config.write_text("{}\n")
            argv = [*command, adapter, "session", "--json", "--mode", "calculate", "--config", str(config)]
            if adapter == "codex":
                argv += ["--speed", "auto"]
            result = subprocess.run(argv, env=env, cwd=root, capture_output=True,
                                    text=True, timeout=60, check=True)
            record["report"] = json.loads(result.stdout)
            record["warnings"] = result.stderr.strip()
            if any(word in result.stderr.lower() for word in ("missing pric", "unknown model", "fallback", "not found")):
                raise ValueError("ccusage reported incomplete or fallback pricing")
            cost, tokens = checked_totals(record["report"])
            if expected_tokens is not None and tokens != expected_tokens:
                raise ValueError("ccusage token total differs from completed model usage")
            record["cost_usd"], record["total_tokens"] = cost, tokens
    except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as error:
        record["error"] = str(error)
    output.write_text(json.dumps(record, indent=2) + "\n")
    return record
