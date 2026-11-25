#!/usr/bin/env python3
"""Exercise the routing evidence script as a subprocess against synthetic data."""

from __future__ import annotations

import csv
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.etree import ElementTree

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
SCRIPT = REPO_ROOT / "scripts" / "routing" / "evidence.py"
SYNTHETIC = HERE / "synthetic"

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False
    )


def sections(output: str) -> dict[str, list[dict[str, str]]]:
    """Parse the report's tab-separated sections into rows keyed by header."""
    parsed: dict[str, list[dict[str, str]]] = {}
    name, header = None, None
    for line in output.splitlines()[1:]:
        if line.startswith("# "):
            name, header = line[2:], None
            parsed[name] = []
        elif name and header is None:
            header = line.split("\t")
        elif name and line:
            parsed[name].append(dict(zip(header, line.split("\t"))))
    return parsed


def find(rows: list[dict[str, str]], **want: str) -> dict[str, str]:
    for row in rows:
        if all(row.get(key) == value for key, value in want.items()):
            return row
    failures.append(f"no row matching {want}")
    return {}


def broken_copy(mutate) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "data"
        shutil.copytree(SYNTHETIC, target)
        mutate(target)
        return run("report", "--data", str(target))


def check_report() -> None:
    result = run("report", "--data", str(SYNTHETIC))
    check(result.returncode == 0, f"report failed: {result.stdout}{result.stderr}")
    first = result.stdout.splitlines()[0] if result.stdout else ""
    check(first.startswith("OK "), f"line 1 is not an OK verdict: {first!r}")
    check("current-model settings per suite: Alder 10, Birch 7, Elm 6" in first and "anchor" not in first,
          f"line 1 should give each suite's count of current-model settings, with no anchor: {first!r}")
    check("outside the base: Cedar" in first, f"non-base suite not named: {first!r}")
    data = sections(result.stdout)
    suite, combined = data.get("suite figures", []), data.get("combined", [])

    # Both suites rank Gamma > Alpha > Beta at high, so the combined score must too.
    quality = {name: float(find(combined, model=name, effort="high").get("combined_quality", "nan"))
               for name in ("Gamma", "Alpha", "Beta")}
    check(quality["Gamma"] > quality["Alpha"] > quality["Beta"], f"combined order wrong: {quality}")

    solo = find(combined, model="Solo", effort="high")
    check(solo.get("suites") == "1 of 3", f"one-suite model not flagged: {solo}")
    check(find(combined, model="Alpha", effort="high").get("suites") == "3 of 3", "a model every suite tested is flagged wrongly")
    check(find(combined, model="Beta", effort="high").get("suites") == "2 of 3", "a model one suite skipped is flagged wrongly")
    check(find(suite, suite="Birch", model="Alpha", effort="high").get("minutes") == "9.0",
          "the suite figures should carry each setting's time per task")
    check(set(suite[0]) == {"suite", "model", "effort", "score", "pass_rate", "cost_usd", "minutes"}
          and "frontier" not in combined[0], "the report should show only figures the method uses")

    # The knee is the last effort before a step costs more than 20% extra per added point.
    knees = {row["model"]: row["effort"] for row in combined if row.get("best_value") == "yes"}
    # Alpha: low to medium costs about 8% a point, medium to high about 53%.
    check(knees.get("Alpha") == "medium", f"Alpha should stop before its expensive step to high: {knees}")
    # Line pays about 12% a point at every step, so it climbs to its top effort.
    check(knees.get("Line") == "max", f"a model whose every step is cheap should reach its top effort: {knees}")
    # Peak scores less at max than at high, so max is left out before the climb.
    check(knees.get("Peak") == "high", f"an effort a cheaper one beats must never be the knee: {knees}")
    # Twin: medium to high costs about 11% a point, high to max 32%.
    check(knees.get("Twin") == "high", f"Twin should take the cheap step and refuse the dear one: {knees}")
    # Thrift's low effort costs more and scores less than its medium.
    check(knees.get("Thrift") == "medium", f"a model whose lowest effort is beaten should start above it: {knees}")
    # Beta's first step costs about 59% a point, so it stays at its lowest effort.
    check(knees.get("Beta") == "low", f"a model whose first step is too dear should stay at its lowest effort: {knees}")
    check(sum(1 for row in combined if row.get("best_value") not in ("", "yes")) == 0, "the best_value column should hold only yes or nothing")

    # The charted models at their knees, in order. A better-scoring setting goes first only when
    # its extra cost is at most 20% for each point it adds. Beta low scores 12.5 more than Gamma low
    # for about 6% a point, so it goes first. Alpha medium scores 16 more than Gamma low for about
    # 56% a point, so the cheaper Gamma goes ahead of it; Alpha beats Solo medium at about 5% a point.
    listed = [(row["model"], row["effort"]) for row in data.get("candidates", [])]
    check(listed == [("Beta", "low"), ("Gamma", "low"), ("Alpha", "medium"), ("Solo", "medium")],
          f"candidates should be ordered by the 20% trade-off at each model's knee: {listed}")

    # Executor rows start from each vendor's everyday model and Team lead rows from its flagship.
    # Solo medium is OpenAI's everyday model, but Gamma high scores higher for less, so it takes the slot.
    rows = data.get("rows", [])
    executor = [(row["provider"], row["model"], row["effort"], row["replaces"]) for row in rows if row["role"] == "Executor"]
    check(("OpenAI", "Gamma", "high", "Solo") in executor,
          f"an everyday model beaten by an unrationed sibling should give way to it: {executor}")
    check(("Anthropic", "Alpha", "medium", "") in executor, f"an everyday model nothing beats should keep its slot: {executor}")
    lead = [(row["provider"], row["model"]) for row in rows if row["role"] == "Team lead"]
    check(("OpenAI", "Gamma") in lead and ("Anthropic", "Alpha") in lead, f"Team lead should start from each flagship: {lead}")
    # Preference rows weigh their sources equally. Fir puts Alpha 1.22 standard deviations
    # above the mean, Solo at it and Gamma 1.22 below, using Alpha's best effort and ignoring
    # the superseded Beta; Gorse, which skips Solo, puts Gamma one above and Alpha one below.
    # Each model averages only the sources that list it, so Solo (50.0) edges Gamma (48.8).
    preference = {row["model"]: row for row in data.get("preference", []) if row["role"] == "Writing"}
    check(set(preference) == {"Alpha", "Gamma", "Solo"}, f"preference rows should score each current model a source lists: {sorted(preference)}")
    check(preference.get("Alpha", {}).get("preference_score") == "51.1" and preference.get("Gamma", {}).get("preference_score") == "48.9",
          f"each source should count equally after standardizing: {preference}")
    check(preference.get("Solo", {}).get("preference_score") == "50.0" and preference.get("Solo", {}).get("sources") == "1 of 2",
          f"a model should average only the sources that list it: {preference.get('Solo')}")
    check([(row["provider"], row["model"]) for row in preference.values() if row["choice"]] == [("Anthropic", "Alpha"), ("OpenAI", "Solo")],
          f"each provider's best-scoring model should take its slot, best first: {preference}")
    check(preference.get("Alpha", {}).get("effort") == "medium", "a preference pick should list the model's best-value effort")
    # A report as of a date before a preference source's first read scores the row from the
    # sources read by then, instead of failing the whole report.
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "data"
        shutil.copytree(SYNTHETIC, target)
        results = target / "results.csv"
        results.write_text(results.read_text().replace(",2026-01-01,https://example.com/gorse", ",2026-02-01,https://example.com/gorse"))
        earlier = run("report", "--data", str(target), "--as-of", "2026-01-15")
        check(earlier.returncode == 0, f"a report before a preference source's first read should still run: {earlier.stdout[:200]}")
        writing = {row["model"]: row for row in sections(earlier.stdout).get("preference", []) if row["role"] == "Writing"}
        check(writing.get("Alpha", {}).get("sources") == "1 of 2",
              f"a preference source with no reads by the report date should be left out of the score: {writing}")
    # Combined cost is a multiple of each suite's typical current-model setting, not dollars no suite charged.
    check(find(combined, model="Alpha", effort="medium").get("relative_cost") == "1.49",
          "combined cost should be a multiple of a typical charted setting, not dollars")

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "data"
        shutil.copytree(SYNTHETIC, target)
        chart = target / "chart.json"
        chart.write_text(chart.read_text().replace(
            '"models": [', '"models": [\n    {"model": "Peak", "provider": "xAI", "status": "current"},\n'
            '    {"model": "Line", "provider": "Google", "status": "current"},'))
        names = target / "models.csv"
        names.write_text(names.read_text() + "Peak,Peak,xAI,current,\nLine,Line,Google,current,\n")
        order = [row["model"] for row in sections(run("report", "--data", str(target)).stdout).get("candidates", [])]
        # Line's knee scores one point above Peak's for twenty times the cost, far past 20% a point, so Peak goes first.
        check("Peak" in order and "Line" in order and order.index("Peak") < order.index("Line"),
              f"a setting that costs far more for one more point should be listed after the cheaper one: {order}")
        # A rationed sibling never replaces an everyday model, however well it scores.
        chart.write_text(chart.read_text().replace('"flagship": "Gamma", "rationed": []', '"flagship": "Gamma", "rationed": ["Gamma"]'))
        kept = [(row["provider"], row["model"]) for row in sections(run("report", "--data", str(target)).stdout).get("rows", [])
                if row["role"] == "Executor"]
        check(("OpenAI", "Solo") in kept, f"a rationed sibling replaced an everyday model: {kept}")
        chart.write_text(chart.read_text().replace('"everyday": "Solo"', '"everyday": "Nobody"'))
        check(run("report", "--data", str(target)).returncode != 0, "an everyday model chart.json does not list should be refused")
        chart.write_text(chart.read_text().replace('"everyday": "Nobody"', '"everyday": "Solo"'))
        chart.write_text(chart.read_text().replace('"flagship": "Gamma", "rationed": ["Gamma"]', '"flagship": "Gamma", "rationed": []'))

    # The row logic, piece by piece, on direct calls into the script.
    import importlib.util
    sys.dont_write_bytecode = True  # keep the import from leaving a __pycache__ in scripts/routing
    spec = importlib.util.spec_from_file_location("evidence_under_test", SCRIPT)
    ev = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = ev
    spec.loader.exec_module(ev)
    C = ev.Combined
    # A sibling that scores higher but costs more does not take the slot; of two that beat the pick, the cheaper does.
    def vendor(name, everyday, models):
        return {"everyday": everyday, "flagship": everyday, "rationed": [], "colour": "#000000"}, [
            {"model": m, "provider": name, "status": "current"} for m in models]
    v, vm = vendor("V", "Pick", ("Pick", "Cheap", "Cheaper"))
    w, wm = vendor("W", "Solo", ("Solo", "Dear"))
    u, um = vendor("U", "Top", ("Top",))
    data = ev.Data([], [], {}, vm + wm + um, {"V": v, "W": w, "U": u})
    rows = [C("Pick", "low", 50, 1.0, 1), C("Pick", "high", 51, 2.0, 1),
            C("Cheap", "low", 54, 0.9, 1), C("Cheaper", "low", 53, 0.5, 1),
            C("Solo", "low", 40, 1.0, 1), C("Dear", "low", 60, 9.0, 1), C("Top", "low", 70, 0.4, 1)]
    built = [(pick.model, gone) for role, pick, gone in ev.vendor_rows(data, rows) if role == "Executor"]
    check(("Cheaper", "Pick") in built and ("Cheap", "Pick") not in built,
          f"of two siblings that beat the pick, the cheaper should take the slot: {built}")
    check(("Solo", "") in built, f"a sibling that scores higher but costs more should not take the slot: {built}")
    check([model for model, _ in built] == ["Top", "Cheaper", "Solo"], f"the row should follow the price order: {built}")
    # The Executor row follows the price order, and the Team lead row goes by quality.
    p, pm = vendor("P", "Cheap", ("Cheap",))
    q, qm = vendor("Q", "Best", ("Best",))
    pair = ev.Data([], [], {}, pm + qm, {"P": p, "Q": q})
    both = [C("Cheap", "low", 55, 0.5, 1), C("Best", "low", 60, 5.0, 1)]
    by_role = {}
    for role, pick, _ in ev.vendor_rows(pair, both):
        by_role.setdefault(role, []).append(pick.model)
    check(by_role.get("Executor") == ["Cheap", "Best"], f"Executor should put the cheaper setting first when a point costs 180% more: {by_role}")
    check(by_role.get("Team lead") == ["Best", "Cheap"], f"Team lead should put the better-scoring setting first whatever it costs: {by_role}")
    # A sibling is compared on the suites that tested both settings. Sib beats Pick on S1, the
    # only suite they share, but S2 tested only Sib and drags its combined score below Pick's.
    import math
    s, sm = vendor("S", "Pick", ("Pick", "Sib", "Lone"))
    solo_data = ev.Data([], [], {}, sm, {"S": s})
    settings = [C("Pick", "high", 60, 2.0, 1), C("Sib", "high", 52, 1.0, 2)]
    scales = ev.Scaled({"S1": {"Pick": {"high": 1.0}, "Sib": {"high": 1.2}}, "S2": {"Sib": {"high": -1.0}}},
                       {"S1": {"Pick": {"high": math.log(2.0)}, "Sib": {"high": math.log(1.0)}}, "S2": {}}, {})
    def slot(rows, scales=None):
        return [pick.model for role, pick, _ in ev.vendor_rows(solo_data, rows, None, scales) if role == "Executor"]
    check(slot(settings, scales) == ["Sib"], f"a sibling ahead on every suite it shares with the pick should take the slot: {slot(settings, scales)}")
    check(slot(settings) == ["Pick"], "without per-suite figures the combined scores should decide")
    lone = [C("Pick", "high", 50, 2.0, 1), C("Lone", "high", 55, 1.0, 1)]
    check(slot(lone, scales) == ["Lone"], f"with no suite in common the combined scores should decide: {slot(lone, scales)}")
    # A sibling earns the slot with its cheapest winning setting, then is listed at that
    # setting or its best-value effort, whichever is higher. Rise wins only at medium, but
    # its step to high costs about 17% a point, so it is listed at high. Top wins only at
    # max, above its best-value effort of low, so it stays at max.
    r, rm = vendor("R", "Base", ("Base", "Rise"))
    t_, tm = vendor("T", "Floor", ("Floor", "Top"))
    rise = ev.Data([], [], {}, rm + tm, {"R": r, "T": t_})
    listed = {pick.model: pick.effort for role, pick, _ in ev.vendor_rows(rise, [
        C("Base", "high", 55, 2.0, 1), C("Rise", "medium", 56, 1.5, 1), C("Rise", "high", 60, 2.5, 1),
        C("Floor", "high", 50.5, 1.2, 1), C("Top", "low", 50, 0.5, 1), C("Top", "max", 51, 1.0, 1),
    ]) if role == "Executor"}
    check(listed.get("Rise") == "high", f"a sibling should be listed at its best-value effort when that is above the setting that won the slot: {listed}")
    check(listed.get("Top") == "max", f"a sibling should stay at the setting that won the slot when that is above its best-value effort: {listed}")
    # The order follows the 20% price, and a cycle falls back to the best-scoring setting.
    a, b, c = C("A", "low", 50, 1.0, 1), C("B", "low", 51, 1.15, 1), C("C", "low", 52, 1.5, 1)
    check([x.model for x in ev.order([c, b, a])] == ["B", "A", "C"],
          f"B costs 15% more for a point and goes first; C costs about 30% a point more than B and goes last: {[x.model for x in ev.order([c, b, a])]}")
    # Y beats X at 19% a point and Z beats Y at about 19%, but X beats Z at 21%: a cycle.
    x, y, z = C("X", "low", 50, 1.0, 1), C("Y", "low", 51, 1.19, 1), C("Z", "low", 52, 1.42, 1)
    check([p.model for p in ev.order([x, y, z])][0] == "Z", "when every setting is beaten by another, the best-scoring one goes first")
    # The knee stops before a step that costs more than 20% a point, even when the step is only just over.
    check(ev.best_value_effort([C("K", "low", 50, 1.0, 1), C("K", "medium", 51, 1.22, 1)]) == "low", "a step at 22% a point should not be taken")
    check(ev.best_value_effort([C("K", "low", 50, 1.0, 1), C("K", "medium", 51, 1.18, 1)]) == "medium", "a step at 18% a point should be taken")
    check(ev.best_value_effort([C("K", "low", 50, 1.0, 1), C("K", "medium", 50, 1.0, 1), C("K", "high", 52, 1.35, 1)]) == "high",
          "two efforts at the same point should not stop the climb or crash it")
    # Inputs that used to crash now stop with an ERROR line.
    for name, mutate, says in (
        ("an empty recommendations file", lambda d: (d / "recommendations.csv").write_text(",".join(ev.RECOMMENDATION_COLUMNS) + "\n"), "no picks"),
        ("a bad review date", lambda d: (d / "recommendations.csv").write_text((d / "recommendations.csv").read_text().replace("2026-01-02", "not-a-date", 1)), "reviewed"),
        ("a compact review date", lambda d: (d / "recommendations.csv").write_text((d / "recommendations.csv").read_text().replace("2026-01-02", "20260102", 1)), "reviewed"),
        ("a duplicate choice", lambda d: (d / "recommendations.csv").write_text((d / "recommendations.csv").read_text().replace("Executor,2,", "Executor,1,", 1)), "twice"),
        ("an unknown provider", lambda d: (d / "recommendations.csv").write_text((d / "recommendations.csv").read_text().replace("Executor,2,OpenAI", "Executor,2,Nobody", 1)), "provider"),
    ):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "data"
            shutil.copytree(SYNTHETIC, target)
            mutate(target)
            out = run("charts", "--data", str(target), "--out", str(Path(tmp) / "out"))
            check(out.returncode == 2 and out.stdout.startswith("ERROR ") and says in out.stdout and "Traceback" not in out.stderr,
                  f"{name} should stop with an ERROR line: {out.stdout}{out.stderr[-200:]}")
    # Python 3.11 and later parse 20260301 and 2026-W10-1 too; the reads compare dates as text, so only YYYY-MM-DD is safe.
    for as_of in ("2026-1-5", "20260301", "2026-W10-1"):
        out = run("report", "--data", str(SYNTHETIC), "--as-of", as_of)
        check(out.returncode == 2 and out.stdout.startswith("ERROR "), f"--as-of should refuse {as_of}, which is not YYYY-MM-DD: {out.stdout[:200]}")

    # A suite may name a model differently; models.csv joins the two.
    check(find(combined, model="Thrift", effort="low").get("suites") == "2 of 3",
          "an aliased model name should count as the same model")

    again = run("report", "--data", str(SYNTHETIC))
    check(again.stdout == result.stdout, "two runs on the same data differ")

    # A setting's score averages only the suites that tested that setting, so a
    # suite that tested a model at one effort moves that effort and no other.
    def beta(data: Path) -> dict[str, float]:
        rows = sections(run("report", "--data", str(data)).stdout).get("combined", [])
        return {row["effort"]: float(row["combined_quality"]) for row in rows if row["model"] == "Beta"}

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "data"
        shutil.copytree(SYNTHETIC, target)
        with (target / "results.csv").open("a") as handle:
            handle.write("Elm,4.0,Beta,high,45,,2.00,,2026-01-01,https://example.com/elm\n")
        before, after = beta(SYNTHETIC), beta(target)
        shifts = {effort: round(after[effort] - before[effort], 1) for effort in before}
        check(shifts["low"] == 0 and shifts["medium"] == 0 and abs(shifts["high"]) >= 0.5,
              f"a one-effort suite should move only the effort it tested: {shifts}")


def check_validation() -> None:
    def duplicate(target: Path) -> None:
        path = target / "results.csv"
        lines = path.read_text().splitlines()
        path.write_text("\n".join(lines + [lines[1]]) + "\n")

    def drop_column(target: Path) -> None:
        path = target / "results.csv"
        path.write_text(path.read_text().replace(",cost_usd,", ",price,", 1))

    def bad_cost(target: Path) -> None:
        path = target / "results.csv"
        path.write_text(path.read_text().replace(",0.60,", ",sixty cents,", 1))

    def unknown_suite(target: Path) -> None:
        path = target / "results.csv"
        path.write_text(path.read_text() + "Dogwood,1.0,Alpha,low,50,,1.00,,2026-01-01,https://example.com/d\n")

    def out_of_range(target: Path) -> None:
        path = target / "results.csv"
        path.write_text(path.read_text().replace("Birch,2.0,Alpha,low,70,", "Birch,2.0,Alpha,low,170,", 1))

    def swap(name: str, old: str, new: str):
        def mutate(target: Path) -> None:
            path = target / name
            text = path.read_text()
            if old not in text:
                failures.append(f"fixture no longer contains {old!r} in {name}")
            path.write_text(text.replace(old, new, 1))
        return mutate

    def rows(*lines: str):
        def mutate(target: Path) -> None:
            header = (target / "results.csv").read_text().splitlines()[0]
            (target / "results.csv").write_text("\n".join([header, *lines]) + "\n")
        return mutate

    def no_base(target: Path) -> None:
        path = target / "chart.json"
        path.write_text(path.read_text().replace('"base": true', '"base": false'))

    tail = ",,1.00,,2026-01-01,https://example.com/x"
    for name, mutate, word in (
        ("duplicate row", duplicate, "duplicate"),
        ("missing column", drop_column, "cost_usd"),
        ("non-numeric cost", bad_cost, "cost_usd"),
        ("suite missing from chart.json", unknown_suite, "Dogwood"),
        ("base score out of range", out_of_range, "170"),
        ("short row", swap("results.csv", "Cedar,3.0,Alpha,high", "Alder,1.0\nCedar,3.0,Alpha,high"), "columns"),
        ("date that is not YYYY-MM-DD", swap("results.csv", ",2026-01-01,", ",next tuesday,"), "date_read"),
        ("ten-character week date", swap("results.csv", ",2026-01-01,", ",2026-W01-4,"), "date_read"),
        ("unknown effort", swap("results.csv", "Alder,1.0,Alpha,low,", "Alder,1.0,Alpha,ultra,"), "ultra"),
        ("zero cost", swap("results.csv", ",0.60,", ",0,"), "cost_usd"),
        ("unknown model status", swap("chart.json", '"status": "superseded"', '"status": "retired"'), "status"),
        ("model with no provider", swap("chart.json", '"provider": "Anthropic", ', ""), "provider"),
        ("role-inputs.csv missing a column", swap("role-inputs.csv", ",says", ",notes"), "says"),
        ("no base suite", no_base, "base suite"),
        ("frontier top of zero", swap("chart.json", '"top": 4', '"top": 0'), "frontier top"),
        ("frontier top given as true", swap("chart.json", '"top": 4', '"top": true'), "frontier top"),
        ("aliases still in chart.json", swap("chart.json", '"suites": {', '"aliases": {"Thrift Mini": "Thrift"},\n  "suites": {'), "models.csv"),
        ("superseded list still in chart.json", swap("chart.json", '"min_suites": 2}', '"min_suites": 2, "superseded": ["Twin"]}'), "models.csv"),
        ("another name pointing at a model with no row", swap("models.csv", "Thrift Mini,Thrift,", "Thrift Mini,Thrifty,"), "no row of its own"),
        ("another name carrying its own maker", swap("models.csv", "Thrift Mini,Thrift,,,", "Thrift Mini,Thrift,Example,current,"), "leave its maker"),
        ("a name listed twice", swap("models.csv", "Twin,Twin,", "Thrift,Twin,"), "listed twice"),
        ("a model with a bad status", swap("models.csv", "Twin,Twin,Example,superseded", "Twin,Twin,Example,retired"), "status"),
        ("a maker that disagrees with chart.json", swap("models.csv", "Alpha,Alpha,Anthropic", "Alpha,Alpha,OpenAI"), "maker"),
        ("a routed model marked superseded", swap("models.csv", "Alpha,Alpha,Anthropic,current", "Alpha,Alpha,Anthropic,superseded"), "superseded"),
        ("a chart.json model with no models.csv row", swap("models.csv", "Solo,Solo,OpenAI,current,\n", ""), "its own row"),
        ("statuses that disagree", swap("models.csv", "Beta,Beta,OpenAI,superseded", "Beta,Beta,OpenAI,current"), "superseded"),
        ("an effort label mapped to no effort", swap("efforts.csv", "na,none,", "na,ultra,"), "efforts.csv"),
        ("preference source missing from chart.json", swap("chart.json", '["Fir", "Gorse"]', '["Fir", "Dogwood"]'), "Dogwood"),
        ("preference source with one current model", swap("results.csv", "Gorse,1.0,Gamma,high,90", "Gorse,1.0,Beta,high,90"), "at least two"),
        ("a suite with fewer than three current-model settings",
         rows("Alder,1.0,Alpha,low,40" + tail, "Alder,1.0,Alpha,high,60" + tail, "Alder,1.0,Beta,low,50" + tail,
              "Birch,2.0,Alpha,low,70" + tail, "Elm,4.0,Alpha,low,10" + tail), "fewer than three"),
        ("a suite whose current-model settings all score the same",
         rows("Alder,1.0,Alpha,low,40" + tail, "Alder,1.0,Alpha,medium,50" + tail, "Alder,1.0,Alpha,high,60" + tail,
              "Birch,2.0,Alpha,low,50" + tail, "Birch,2.0,Alpha,medium,50" + tail, "Birch,2.0,Alpha,high,50" + tail,
              "Elm,4.0,Alpha,low,10" + tail, "Elm,4.0,Alpha,medium,20" + tail, "Elm,4.0,Alpha,high,30" + tail), "Birch"),
    ):
        result = broken_copy(mutate)
        first = result.stdout.splitlines()[0] if result.stdout else ""
        check(result.returncode != 0, f"{name}: expected a non-zero exit")
        check(first.startswith("ERROR ") and word in first, f"{name}: line 1 should name the problem: {first!r}")


def check_import() -> None:
    sources = HERE / "sources"
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "data"
        shutil.copytree(SYNTHETIC, target)
        chart = target / "chart.json"
        chart.write_text(chart.read_text().replace(
            '"Cedar": {"base": false}',
            '"Cedar": {"base": false}, "FrontierCode": {"base": false}, "VulcanBench": {"base": false}'))
        results = target / "results.csv"
        before = results.read_text().splitlines()

        def imported(fmt: str, name: str) -> subprocess.CompletedProcess[str]:
            return run("import", "--data", str(target), "--format", fmt, "--file", str(sources / name),
                       "--version", "9.9", "--date", "2026-02-02", "--url", f"https://example.com/{fmt}")

        first = imported("frontiercode", "frontiercode-sample.json")
        check(first.returncode == 0 and first.stdout.startswith("OK "), f"FrontierCode import failed: {first.stdout}{first.stderr}")
        lines = results.read_text().splitlines()
        check("FrontierCode,9.9,Alpha,low,40.00,50.00,1.5,,2026-02-02,https://example.com/frontiercode" in lines,
              "FrontierCode row did not convert fractions to percents or drop the Claude prefix")
        check("FrontierCode,9.9,Alpha,xhigh,61.25,75.00,6.25,,2026-02-02,https://example.com/frontiercode" in lines,
              "FrontierCode xhigh row missing")
        check(any(line.startswith("FrontierCode,9.9,Delta,none,8.00,") for line in lines),
              "a model with no effort setting should import at effort none")

        second = imported("vulcanbench", "vulcanbench-sample.csv")
        check(second.returncode == 0, f"VulcanBench import failed: {second.stdout}{second.stderr}")
        lines = results.read_text().splitlines()
        check("VulcanBench,9.9,Alpha,xhigh,91.50,100.00,4.989512,14.25,2026-02-02,https://example.com/vulcanbench" in lines,
              "VulcanBench extra-high should land on xhigh with pass rate from tasks passed")
        check("VulcanBench,9.9,Beta,high,80.25,75.00,,5.5,2026-02-02,https://example.com/vulcanbench" in lines,
              "a VulcanBench row with no cost should import with cost empty")

        # Any other source is transcribed to a plain table and imported under its suite name.
        table = run("import", "--data", str(target), "--format", "table", "--suite", "Cedar",
                    "--file", str(sources / "table-sample.csv"), "--version", "1.1", "--date", "2026-02-03",
                    "--url", "https://example.com/cedar")
        check(table.returncode == 0, f"table import failed: {table.stdout}{table.stderr}")
        lines = results.read_text().splitlines()
        check("Cedar,1.1,Alpha,xhigh,61.50,,8.52,,2026-02-03,https://example.com/cedar" in lines,
              "a table row should import with the same name and effort cleanup as the other formats")
        check("Cedar,1.1,Beta,high,40.00,50.00,1.25,3.5,2026-02-03,https://example.com/cedar" in lines,
              "a table row should keep its pass rate, cost, and minutes")

        # results.csv is append-only: a new read is added after the rows already there, and the report uses the latest.
        check(lines[: len(before)] == before, "an import should leave every earlier row where it was")
        latest = [row["score"] for row in sections(run("report", "--data", str(target)).stdout).get("suite figures", []) if row["suite"] == "Cedar"]
        check(sorted(latest) == ["40.00", "61.50"], f"the report should use only a suite's latest read: {latest}")
        earlier = run("report", "--data", str(target), "--as-of", "2026-01-15")
        cedar = [row["score"] for row in sections(earlier.stdout).get("suite figures", []) if row["suite"] == "Cedar"]
        check(cedar == ["1500.00"], f"--as-of should report what had been read by that date: {cedar}")
        check(run("report", "--data", str(target), "--as-of", "2025-01-01").returncode != 0, "--as-of before the first read should be refused")
        same_day = [row["score"] for row in sections(run("report", "--data", str(target), "--as-of", "2026-02-03").stdout).get("suite figures", [])
                    if row["suite"] == "Cedar"]
        check(sorted(same_day) == ["40.00", "61.50"], f"--as-of should include a read made on that date: {same_day}")

        # The changes command compares each suite's latest read with the one before it.
        moved = Path(tmp) / "moved.csv"
        moved.write_text((sources / "table-sample.csv").read_text().replace("Beta,high,40,50,1.25,3.5", "Beta,high,45,50,1.5,3.5\nGamma,low,10,,0.5,"))
        third = run("import", "--data", str(target), "--format", "table", "--suite", "Cedar", "--file", str(moved),
                    "--version", "1.1", "--date", "2026-02-10", "--url", "https://example.com/cedar")
        check(third.returncode == 0, f"a later read failed to import: {third.stdout}")
        changes = run("changes", "--data", str(target))
        check(changes.returncode == 0 and changes.stdout.startswith("OK "), f"changes failed: {changes.stdout}{changes.stderr}")
        rows = [row for row in sections(changes.stdout).get("changes", []) if row["suite"] == "Cedar"]
        beta = find(rows, model="Beta", effort="high")
        check((beta.get("change"), beta.get("score_before"), beta.get("score_after"), beta.get("cost_before"), beta.get("cost_after"))
              == ("changed", "40.00", "45.00", "1.250", "1.500"), f"a moved score should be reported with both values: {beta}")
        check(find(rows, model="Gamma", effort="low").get("change") == "added", "a setting new in the latest read should be reported as added")
        check(not any(row["model"] == "Alpha" for row in rows), "a setting that did not move should not be reported")
        check((beta.get("read_before"), beta.get("read_after")) == ("2026-02-03", "2026-02-10"), "changes should name the two reads it compared")
        rerun = run("import", "--data", str(target), "--format", "table", "--suite", "Cedar",
                    "--file", str(sources / "table-sample.csv"), "--version", "1.1", "--date", "2026-02-10", "--url", "https://example.com/cedar")
        kept = results.read_text().splitlines()
        check(rerun.returncode == 0 and not any(line.startswith("Cedar,1.1,Gamma,") for line in kept)
              and sum(line.startswith("Cedar,1.1,Beta,high,") for line in kept) == 2,
              "importing again on the same date should replace that day's read and nothing else")
        lines = results.read_text().splitlines()
        unnamed = run("import", "--data", str(target), "--format", "table", "--file", str(sources / "table-sample.csv"),
                      "--version", "1.1", "--date", "2026-02-03", "--url", "https://example.com/cedar")
        check(unnamed.returncode != 0 and unnamed.stdout.startswith("ERROR "), "a table import with no suite name should be refused")

        snapshot = results.read_text()
        again = imported("vulcanbench", "vulcanbench-sample.csv")
        check(again.returncode == 0 and results.read_text() == snapshot, "importing the same file twice changed the results")

        report = run("report", "--data", str(target))
        check(report.returncode == 0, f"report failed after import: {report.stdout}")

        # A file that parses but holds an effort the loader rejects must not be written.
        invalid = Path(tmp) / "invalid.json"
        invalid.write_text((sources / "frontiercode-sample.json").read_text().replace('"xhigh"', '"ultra"'))
        refused = run("import", "--data", str(target), "--format", "frontiercode", "--file", str(invalid),
                      "--version", "9.9", "--date", "2026-02-02", "--url", "https://example.com/x")
        check(refused.returncode != 0 and refused.stdout.startswith("ERROR ") and "ultra" in refused.stdout and "efforts.csv" in refused.stdout,
              f"an import with an effort label efforts.csv doesn't map should be refused and say so: {refused.stdout}")
        check(results.read_text() == snapshot, "an import that failed validation changed the results file")
        undated = run("import", "--data", str(target), "--format", "vulcanbench", "--file", str(sources / "vulcanbench-sample.csv"),
                      "--version", "9.9", "--date", "next tuesday", "--url", "https://example.com/x")
        check(undated.returncode != 0 and results.read_text() == snapshot, "an import with a malformed date should be refused")

        # Every label must have its own row, even one already spelled like an effort.
        labels = target / "efforts.csv"
        kept_labels = labels.read_text()
        labels.write_text("".join(line for line in kept_labels.splitlines(keepends=True) if not line.startswith("high,")))
        unmapped = run("import", "--data", str(target), "--format", "table", "--suite", "Cedar",
                       "--file", str(sources / "table-sample.csv"), "--version", "1.1", "--date", "2026-02-04", "--url", "https://example.com/cedar")
        check(unmapped.returncode != 0 and "efforts.csv" in unmapped.stdout and "'high'" in unmapped.stdout,
              f"a label efforts.csv has no row for should stop the import, even one spelled like an effort: {unmapped.stdout}")
        check(results.read_text() == snapshot, "an import stopped on an unmapped label changed the results file")
        labels.write_text(kept_labels)

        bad = Path(tmp) / "bad.json"
        bad.write_text('{"unexpected": true}')
        broken = run("import", "--data", str(target), "--format", "frontiercode", "--file", str(bad),
                     "--version", "9.9", "--date", "2026-02-02", "--url", "https://example.com/x")
        check(broken.returncode != 0 and broken.stdout.startswith("ERROR "), f"unknown source shape accepted: {broken.stdout}")
        check(results.read_text() == snapshot, "a failed import changed the results file")


SVG = "{http://www.w3.org/2000/svg}"
NAVY = "#042458"
CHARTS = ("routing-base.svg", "routing-frontier.svg", "routing-table.svg")


def check_frontier_rules() -> None:
    """Rank the frontier field by every scored effort, and keep every setting that ties a frontier setting exactly."""
    sys.path.insert(0, str(REPO_ROOT / "scripts" / "routing"))
    import evidence
    data = evidence.load(SYNTHETIC)
    point = evidence.Combined
    data.frontier["top"] = 1
    # Line's best score is at an effort no suite prices; it still outranks Peak.
    field, _ = evidence.frontier_field(data, [point("Line", "low", 40, 1.0, 2), point("Line", "max", 90, None, 2),
                                              point("Peak", "high", 60, 1.0, 2)])
    check([line.model for line in field] == ["Line"], f"the field should rank models by every scored effort, priced or not: {[line.model for line in field]}")
    data.frontier["top"] = 2
    _, edge = evidence.frontier_field(data, [point("Peak", "high", 60, 1.0, 2), point("Line", "high", 60, 1.0, 2)])
    check(sorted(p.model for p in edge) == ["Line", "Peak"], f"two settings at the same cost and score should both sit on the frontier: {edge}")


def check_charts() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        first, second = Path(tmp) / "one", Path(tmp) / "two"
        for out in (first, second):
            result = run("charts", "--data", str(SYNTHETIC), "--out", str(out))
            check(result.returncode == 0 and result.stdout.startswith("OK "), f"charts failed: {result.stdout}{result.stderr}")
        for name in CHARTS:
            if not (first / name).is_file():
                failures.append(f"charts did not write {name}")
                return
            check((first / name).read_bytes() == (second / name).read_bytes(), f"two runs wrote different {name}")

        headline = ElementTree.parse(first / "routing-base.svg").getroot()
        words = " ".join("".join(el.itertext()) for el in headline.iter(f"{SVG}text"))
        check("Relative cost" in words and "$" not in words, "the combined chart should use relative cost, not dollars")
        check("Suites: Alder" in words and "Birch" in words and "Elm" in words, "the footnote should list the base suites")

        # recommendations.csv is drawn as a shareable figure of the recommendations.
        table = " ".join("".join(el.itertext()) for el in ElementTree.parse(first / "routing-table.svg").getroot().iter(f"{SVG}text"))
        for want in ("Executor", "Writing", "Claude Alpha 1.2", "GPT-9.1 Gamma", "2026-01-02", "my judgment"):
            check(want in table, f"the table figure should show {want!r}: {table[:300]}")
        check(table.count("*") >= 2, "a judged cell should carry its asterisk, and the key should explain it")
        lines = {el.get("data-model"): el for el in headline.iter(f"{SVG}polyline") if el.get("class") == "series"}
        check(set(lines) == {"Alpha", "Gamma", "Solo", "Beta"}, f"headline should draw the listed models only: {sorted(lines)}")
        check(lines["Solo"].get("data-suites") == "1" and lines["Alpha"].get("data-suites") == "3",
              "each line should say how many suites tested its model")
        text = words
        check("Solo (1)" in text and "Alpha (3)" in text and "suites that tested" in text,
              "each line label should count the suites that tested the model, and the footer should say so")
        check("2026-01-01" in text, "the chart should state the date its data was read")

        # Each provider's lines use the colour chart.json gives it, and each knee ring takes its own line's colour.
        inks = {el.get("data-model"): el.get("stroke") for el in headline.iter(f"{SVG}polyline") if el.get("class") == "series"}
        check(inks.get("Alpha") == "#C15F3C" and inks.get("Gamma") == "#10A37F",
              f"lines should use each provider's colour from chart.json: {inks}")
        rings = {el.get("data-model"): el.get("stroke") for el in headline.iter(f"{SVG}circle") if el.get("class") == "knee"}
        check(rings and all(rings[model] == inks[model] for model in rings), f"knee rings should match their line's colour: {rings}")
        keys = [el.get("stroke") for el in headline.iter(f"{SVG}circle") if el.get("class") == "key-knee"]
        check(keys == [NAVY], f"the key's best-value mark should be navy: {keys}")
        rings = [el.get("data-model") for el in headline.iter(f"{SVG}circle") if el.get("class") == "knee"]
        check(sorted(rings) == ["Alpha", "Gamma", "Solo"], f"each current model with a knee gets exactly one ring: {rings}")

        labels = [el for el in headline.iter(f"{SVG}text") if el.get("class") == "line-label"]
        check(len(labels) == 4, f"each line should carry one label: {len(labels)}")

        # The frontier chart draws the top models scored by enough suites, leaving out superseded releases,
        # and outlines each setting that no cheaper setting beats.
        field = ElementTree.parse(first / "routing-frontier.svg").getroot()
        lines = {el.get("data-model"): el for el in field.iter(f"{SVG}polyline") if el.get("class") == "series"}
        check(set(lines) == {"Gamma", "Alpha", "Line", "Peak"},
              f"the frontier chart should draw the top four current models scored by two suites, without Beta, Twin, Solo or Thrift: {sorted(lines)}")
        check(lines.get("Alpha") is not None and lines["Alpha"].get("stroke") == "#C15F3C" and lines.get("Line") is not None and lines["Line"].get("stroke") == "#47577A",
              "routed models keep their provider's colour and other makers are grey")
        edge = [(el.get("data-model"), el.get("data-effort")) for el in field.iter(f"{SVG}circle") if el.get("class") == "frontier"]
        check(edge == [("Peak", "low"), ("Gamma", "low"), ("Gamma", "medium"), ("Peak", "high"), ("Gamma", "high")],
              f"the frontier should run from the cheapest setting through each cheaper-unbeaten one: {edge}")
        check(not any(el.get("class") == "knee" for el in field.iter(f"{SVG}circle")), "the frontier chart marks the frontier, not best-value efforts")
        words = " ".join("".join(el.itertext()) for el in field.iter(f"{SVG}text"))
        check("Not routed here" in words and "Other makers" not in words and "On the frontier" in words,
              "the frontier chart's key should call grey lines models not routed here, not other makers, and name the frontier mark")
        bold = sorted("".join(el.itertext()) for el in field.iter(f"{SVG}text") if el.get("class") == "line-label" and el.get("font-weight") == "600")
        check(bold == ["Gamma (3)", "Peak (2)"], f"the frontier chart should bold the models with a frontier setting, not the routed ones: {bold}")

        # No label may cover a data point, in any of the charts.
        for name in (chart for chart in CHARTS if chart != "routing-table.svg"):
            root = ElementTree.parse(first / name).getroot()
            points = [(float(el.get("data-x")), float(el.get("data-y"))) for el in root.iter() if el.get("class") == "point"]
            check(points, f"{name}: no data points found")
            # The key shows one marker for each effort the chart draws, so no effort needs a text label.
            drawn = {el.get("data-effort") for el in root.iter() if el.get("class") == "point"}
            keyed = {el.get("data-effort") for el in root.iter() if el.get("class") == "key"}
            check(drawn <= keyed, f"{name}: the key is missing efforts {sorted(drawn - keyed)}")
            shapes = {el.get("data-effort"): (el.tag, el.get("points") is not None and len(el.get("points").split()), el.get("r"), el.get("fill")) for el in root.iter() if el.get("class") == "key"}
            check(len(set(shapes.values())) == len(shapes), f"{name}: two efforts share a marker shape")
            boxes = []
            for el in root.iter(f"{SVG}text"):
                if el.get("class") != "line-label":
                    continue
                size, text = float(el.get("font-size")), "".join(el.itertext())
                wide = 0.54 * size * len(text)
                left = float(el.get("x")) - (wide if el.get("text-anchor") == "end" else 0)
                top = float(el.get("y")) - size
                covered = [p for p in points if left < p[0] < left + wide and top < p[1] < top + size + 3]
                check(not covered, f"{name}: label {text!r} covers a data point")
                for other in boxes:
                    clash = left < other[2] and other[0] < left + wide and top < other[3] and other[1] < top + size
                    check(not clash, f"{name}: label {text!r} overlaps label {other[4]!r}")
                boxes.append((left, top, left + wide, top + size, text))

    # The committed charts must match what the committed data generates.
    committed = REPO_ROOT / "docs" / "assets"
    for problem in stale_charts(committed):
        failures.append(problem)
    failures.extend(page_alt_text_problems())
    failures.extend(page_names_problems())
    failures.extend(recommendation_drift(REPO_ROOT / "docs" / "routing"))

    with tempfile.TemporaryDirectory() as tmp:
        data = Path(tmp) / "routing"
        shutil.copytree(REPO_ROOT / "docs" / "routing", data)
        picks = data / "recommendations.csv"
        with picks.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        pick = next(row for row in rows if row["role"] == "Executor")
        pick["judgment"] = ""
        pick["effort"] = "low" if pick["effort"] == "max" else "max"

        def save() -> None:
            with picks.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)

        save()
        problems = recommendation_drift(data)
        check(any(pick["model"] in problem and f"at {pick['effort']}" in problem for problem in problems),
              f"the drift gate missed an Executor pick at the wrong effort: {problems}")
        pick["judgment"] = "yes"
        save()
        check(recommendation_drift(data) == [], "the drift gate should let a pick marked as judgment differ from the method")
        writing = next(row for row in rows if row["role"] == "Writing")
        writing["judgment"] = ""
        writing["model"] = "Claude Opus 5.5" if "Opus" not in writing["model"] else "Claude Fable 5.2"
        save()
        problems = recommendation_drift(data)
        check(any(writing["model"] in problem for problem in problems),
              f"the drift gate missed a Writing pick that is not the provider's best-scoring model: {problems}")

    # The gate itself must fail on a chart that differs and on one that is missing.
    with tempfile.TemporaryDirectory() as tmp:
        tampered = Path(tmp)
        for name in CHARTS:
            shutil.copy(committed / name, tampered / name)
        with (tampered / CHARTS[0]).open("a") as handle:
            handle.write(" ")
        (tampered / CHARTS[1]).unlink()
        problems = stale_charts(tampered)
        check(any(CHARTS[0] in problem and "differs" in problem for problem in problems),
              f"the stale-chart gate missed a chart that differs: {problems}")
        check(any(CHARTS[1] in problem and "missing" in problem for problem in problems),
              f"the stale-chart gate missed a missing chart: {problems}")
        (tampered / "routing-retired.svg").write_text("<svg/>")
        check(any("routing-retired.svg" in problem and "no longer" in problem for problem in stale_charts(tampered)),
              "the stale-chart gate missed a routing chart the generator no longer writes")

    # A frontier block that no model can meet fails the charts command instead of drawing an empty chart.
    with tempfile.TemporaryDirectory() as tmp:
        data, out = Path(tmp) / "data", Path(tmp) / "out"
        shutil.copytree(SYNTHETIC, data)
        chart = data / "chart.json"
        chart.write_text(chart.read_text().replace('"min_suites": 2', '"min_suites": 9'))
        result = run("charts", "--data", str(data), "--out", str(out))
        first = result.stdout.splitlines()[0] if result.stdout else ""
        check(result.returncode != 0 and first.startswith("ERROR ") and "suite minimum" in first,
              f"an unmeetable frontier suite minimum should fail the charts command: {first!r}")


def page_names_problems() -> list[str]:
    """ROUTING.md's model-name and effort-label tables must match models.csv and efforts.csv, as the report prints them."""
    result = run("report", "--data", str(REPO_ROOT / "docs" / "routing"))
    printed = result.stdout.split("# names\n", 1)
    if result.returncode != 0 or len(printed) < 2:
        return [f"report did not print its names section: {result.stdout[:200]}"]
    want = [line for line in printed[1].strip().splitlines() if line.startswith("|")]
    page = (REPO_ROOT / "ROUTING.md").read_text(encoding="utf-8")
    heading = "### Names and effort labels\n"
    if heading not in page:
        return ["ROUTING.md has no Names and effort labels section"]
    section = page.split(heading, 1)[1].split("\n### ", 1)[0]
    have = [line for line in section.splitlines() if line.startswith("|")]
    if have != want:
        missing = [line for line in want if line not in have]
        stale = [line for line in have if line not in want]
        return [f"ROUTING.md's names tables differ from the report's names section; copy them over. Missing: {missing}; stale: {stale}"]
    return []


def page_alt_text_problems() -> list[str]:
    """The page shows the recommendations only as a figure, so its alt text must carry every pick for readers and agents."""
    page = (REPO_ROOT / "ROUTING.md").read_text(encoding="utf-8")
    found = re.search(r"!\[([^\]]*)\]\(docs/assets/routing-table\.svg\)", page)
    if not found:
        return ["ROUTING.md does not show docs/assets/routing-table.svg"]
    alt = found.group(1)
    problems = []
    with (REPO_ROOT / "docs" / "routing" / "recommendations.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            want = f"{row['model']} (`{row['model_id']}`) at {row['effort']}"
            if want not in alt:
                problems.append(f"the routing-table alt text does not name {want} for {row['role']}")
            if row["reviewed"] not in alt:
                problems.append(f"the routing-table alt text does not give the review date {row['reviewed']}")
    return sorted(set(problems))


def recommendation_drift(data_dir: Path) -> list[str]:
    """Each pick must be the setting the method computes for its provider.

    The Executor and Team lead rows come from the report's rows section and the
    preference rows from its preference section. Role inputs may reorder a row,
    so only the model and effort are compared. A pick marked as judgment may
    name another setting.
    """
    result = run("report", "--data", str(data_dir))
    if result.returncode != 0:
        return [f"report failed on {data_dir}: {result.stdout}{result.stderr}"]
    report = sections(result.stdout)
    computed = {(row["role"], row["provider"]): row for row in report["rows"]}
    computed.update({(row["role"], row["provider"]): row for row in report.get("preference", []) if row["choice"]})
    scored = {row["role"] for row in report.get("preference", [])} | {"Executor", "Team lead"}
    problems = []
    with (data_dir / "recommendations.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["role"] not in scored or row["judgment"] == "yes":
                continue
            want = computed.get((row["role"], row["provider"]))
            if want is None:
                problems.append(f"recommendations.csv lists {row['provider']} for {row['role']}, but the method computes no {row['provider']} pick for that role")
            elif not (row["model"] == want["model"] or row["model"].endswith(" " + want["model"])) or row["effort"] != want["effort"]:
                problems.append(f"recommendations.csv lists {row['model']} at {row['effort']} for {row['role']}, but the method computes {want['model']} at {want['effort']}: "
                                "update the pick, or mark it as judgment and explain it in ROUTING.md")
    return problems


def stale_charts(charts_dir: Path) -> list[str]:
    """Compare the charts in charts_dir with fresh output from the committed data."""
    problems = []
    with tempfile.TemporaryDirectory() as tmp:
        result = run("charts", "--data", str(REPO_ROOT / "docs" / "routing"), "--out", tmp)
        if result.returncode != 0:
            return [f"charts failed on the committed data: {result.stdout}{result.stderr}"]
        written = sorted(path.name for path in Path(tmp).iterdir())
        for name in sorted(path.name for path in charts_dir.glob("routing-*.svg")):
            if name not in written:
                problems.append(f"{name} is in {charts_dir.name} but the charts command no longer writes it: delete it or restore its data")
        for name in written:
            existing, fresh = charts_dir / name, Path(tmp) / name
            if not existing.is_file():
                problems.append(f"{name} is missing from {charts_dir.name}: generate it with the charts command")
            elif existing.read_bytes() != fresh.read_bytes():
                problems.append(f"{name} differs from what the committed data generates: regenerate it with the charts command")
    return problems


def main() -> int:
    check_report()
    check_validation()
    check_import()
    check_frontier_rules()
    check_charts()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("PASS: routing evidence figures, flags, knees, and validation behave as specified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
