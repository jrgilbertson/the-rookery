#!/usr/bin/env python3
"""Compute the figures behind ROUTING.md from the committed benchmark data.

Commands:
  report --data DIR [--as-of YYYY-MM-DD]
                      Print cost per pass, cost per added quality point, time,
                      the combined score, each model's best-value effort, the
                      charted models at those efforts in order, the Executor and
                      Team lead rows built from each vendor's own guidance, and
                      the preference rows, each scored on its sources weighted
                      equally, from the latest read of each suite. --as-of
                      ignores later reads.
  changes --data DIR  List what moved between each suite's two latest reads.
  import --data DIR --format frontiercode|vulcanbench|table --file PATH
         --version V --date YYYY-MM-DD --url URL [--suite NAME]
                      Add one read of a suite to results.csv from a downloaded
                      leaderboard file. Earlier reads stay in the file. The
                      table format reads a plain CSV of model, effort, score,
                      pass_rate, cost_usd, and minutes for any suite named
                      with --suite.
  charts --data DIR --out DIR
                      Write routing-base.svg, routing-base-providers.svg, and
                      routing-base-suites.svg, and routing-table.svg from
                      recommendations.csv.

Every command prints a verdict on line 1: "OK ..." on success, or
"ERROR ..." naming the problem, with a non-zero exit. The script reads local
files only and never opens a network connection.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import io
import json
import math
import statistics
from dataclasses import dataclass, field
from pathlib import Path

# "none" is a model with no effort setting.
EFFORTS = ("none", "minimal", "low", "medium", "high", "xhigh", "max")
RESULT_COLUMNS = (
    "suite", "suite_version", "model", "effort", "score", "pass_rate",
    "cost_usd", "minutes", "date_read", "source_url",
)
ROLE_INPUT_COLUMNS = ("role", "source", "url", "date_read", "says")
# The most extra cost, in percent, worth paying for each added point of combined quality.
BEST_VALUE_STEP_LIMIT = 40.0
VENDOR_ROLES = (("Executor", "everyday"), ("Team lead", "flagship"))


def escape(text: str) -> str:
    """Escape &, <, and > for SVG text and attribute values, as xml.sax.saxutils.escape does, without its slow import."""
    return text.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")


class DataError(Exception):
    """A problem in the data files that the caller must fix."""


def _iso_date(text: str, where: str) -> str:
    """Return text when it is a date written YYYY-MM-DD, or raise a DataError naming where it came from.

    Python 3.11 and later also parse 20260301 and 2026-W10-1. Reads compare dates as text, so only the
    one written form is safe: "2026-06-01" <= "20260301" is true.
    """
    try:
        if datetime.date.fromisoformat(text).isoformat() == text:
            return text
    except ValueError:
        pass
    raise DataError(f"{where} is not YYYY-MM-DD: {text!r}")


@dataclass(frozen=True)
class Result:
    suite: str
    suite_version: str
    model: str
    effort: str
    score: float
    pass_rate: float | None
    cost: float | None
    date_read: str
    minutes: float | None = None

    @property
    def setting(self) -> tuple[str, str]:
        return (self.model, self.effort)


@dataclass(frozen=True)
class Data:
    results: list[Result]  # the latest read of each suite
    history: list[Result]  # every read in the file
    suites: dict[str, bool]  # suite name -> in the base
    models: list[dict[str, str]]
    anchor: str  # the base suite every other base suite is scaled against
    vendors: dict[str, dict]  # provider -> {"everyday": model, "flagship": model, "rationed": [models]}
    preference: dict[str, list[str]] = field(default_factory=dict)  # role -> the suites that score it, weighted equally

    @property
    def base(self) -> list[str]:
        return [name for name, in_base in self.suites.items() if in_base]


def _number(row: dict[str, str], column: str, line: int, required: bool = False) -> float | None:
    text = (row.get(column) or "").strip()
    if not text:
        if required:
            raise DataError(f"results.csv line {line}: {column} is empty")
        return None
    try:
        value = float(text)
    except ValueError:
        raise DataError(f"results.csv line {line}: {column} is not a number: {text!r}") from None
    if not math.isfinite(value):
        raise DataError(f"results.csv line {line}: {column} is not a number: {text!r}")
    return value


def _read_csv(path: Path, columns: tuple[str, ...], text: str | None = None) -> list[dict[str, str]]:
    if text is None:
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise DataError(f"missing file: {path.name}") from None
    reader = csv.DictReader(io.StringIO(text, newline=""))
    missing = [name for name in columns if name not in (reader.fieldnames or [])]
    if missing:
        raise DataError(f"{path.name} is missing column(s): {', '.join(missing)}")
    return list(reader)


def load(directory: Path, results_text: str | None = None, as_of: str | None = None) -> Data:
    """Read and validate the three data files. Every command uses this loader.

    results.csv keeps every read of every suite. The figures come from each
    suite's latest read, or its latest on or before as_of. results_text stands
    in for results.csv so import can validate before it writes.
    """
    try:
        chart = json.loads((directory / "chart.json").read_text(encoding="utf-8"))
        suites = {name: bool(entry["base"]) for name, entry in chart["suites"].items()}
        models = [dict(entry) for entry in chart["models"]]
        anchor = chart["anchor"]
        aliases = dict(chart.get("aliases", {}))
        vendors = {name: dict(entry) for name, entry in chart.get("vendors", {}).items()}
        preference = {role: list(names) for role, names in chart.get("preference", {}).items()}
        for role, names in preference.items():
            for name in names:
                if name not in suites:
                    raise DataError(f"chart.json: preference names {name} for {role}, but suites does not list it")
        listed = {(entry["model"], entry["provider"]) for entry in models}
        for provider, entry in vendors.items():
            entry.setdefault("rationed", [])
            for name in (entry["everyday"], entry["flagship"], *entry["rationed"]):
                if (name, provider) not in listed:
                    raise DataError(f"chart.json: vendors names {name} for {provider}, but models does not list it under {provider}")
        if not suites.get(anchor):
            raise DataError(f"chart.json: anchor {anchor!r} is not a base suite")
        for entry in models:
            if entry["status"] not in ("current", "superseded"):
                raise DataError(f"chart.json: status of {entry['model']} must be current or superseded")
    except DataError:
        raise
    except FileNotFoundError:
        raise DataError("missing file: chart.json") from None
    except (ValueError, KeyError, TypeError, AttributeError) as error:
        raise DataError(f"chart.json is malformed: {error}") from None

    _read_csv(directory / "role-inputs.csv", ROLE_INPUT_COLUMNS)

    history: list[Result] = []
    seen: set[tuple[str, str, str, str]] = set()
    for line, row in enumerate(_read_csv(directory / "results.csv", RESULT_COLUMNS, results_text), start=2):
        if None in row or any(row[name] is None for name in RESULT_COLUMNS):
            raise DataError(f"results.csv line {line}: expected {len(RESULT_COLUMNS)} columns")
        suite, model, effort = row["suite"].strip(), row["model"].strip(), row["effort"].strip()
        model = aliases.get(model, model)
        if suite not in suites:
            raise DataError(f"results.csv line {line}: suite {suite} is not listed in chart.json")
        if effort not in EFFORTS:
            raise DataError(f"results.csv line {line}: unknown effort {effort!r}")
        score = _number(row, "score", line, required=True)
        if suites[suite] and not 0 <= score <= 100:
            raise DataError(f"results.csv line {line}: base suite score {score:g} is outside 0 to 100")
        cost = _number(row, "cost_usd", line)
        if cost is not None and cost <= 0:
            raise DataError(f"results.csv line {line}: cost_usd must be above zero")
        minutes = _number(row, "minutes", line)
        date_read = _iso_date(row["date_read"].strip(), f"results.csv line {line}: date_read")
        key = (suite, date_read, model, effort)
        if key in seen:
            raise DataError(f"results.csv line {line}: duplicate row for {suite}, {model}, {effort}, read {date_read}")
        seen.add(key)
        history.append(Result(
            suite, row["suite_version"].strip(), model, effort, score,
            _number(row, "pass_rate", line), cost, date_read, minutes,
        ))
    if as_of is not None:
        _iso_date(as_of, "--as-of")
        history = [result for result in history if result.date_read <= as_of]
        if not history:
            raise DataError(f"results.csv holds no read on or before {as_of}")
    latest: dict[str, str] = {}
    for result in history:
        latest[result.suite] = max(latest.get(result.suite, ""), result.date_read)
    results = [result for result in history if result.date_read == latest[result.suite]]
    return Data(results, history, suites, models, anchor, vendors, preference)


def cost_per_pass(result: Result) -> float | str:
    if result.cost is None or result.pass_rate is None:
        return "missing"
    if result.pass_rate == 0:
        return "no passes"
    return result.cost / (result.pass_rate / 100)


def _by_effort(results: list[Result]) -> list[Result]:
    return sorted(results, key=lambda result: EFFORTS.index(result.effort))


def cost_per_added_point(previous: Result, current: Result) -> float | str:
    """Dollars per extra quality point over the next lower effort tested."""
    if previous.cost is None or current.cost is None:
        return "missing"
    gain = current.score - previous.score
    if gain <= 0:
        return "no gain"
    if current.cost < previous.cost:
        return "cheaper"
    return (current.cost - previous.cost) / gain


def _logit(percent: float) -> float:
    clamped = min(max(percent, 1.0), 99.0)
    return math.log(clamped / (100 - clamped))


@dataclass(frozen=True)
class Combined:
    model: str
    effort: str
    quality: float
    cost: float | None
    suites: int


def combine(data: Data) -> tuple[list[Combined], dict[str, int]]:
    """Put the base suites on one scale and average them.

    Each suite is scaled against the anchor suite on the settings the two
    share, so a suite that tested only some models still joins. A setting's
    score averages whichever suites tested it. Returns the combined rows and
    each suite's count of settings shared with the anchor.
    """
    base = data.base
    if not base:
        raise DataError("chart.json names no base suite")
    by_suite = {name: {r.setting: r for r in data.results if r.suite == name} for name in base}
    anchor = by_suite[data.anchor]
    if len(anchor) < 3:
        raise DataError(f"the anchor suite {data.anchor} holds fewer than three settings")
    logits = [_logit(row.score) for row in anchor.values()]
    mean, spread = statistics.fmean(logits), statistics.pstdev(logits)
    if spread == 0:
        raise DataError(f"every setting scores the same on {data.anchor}")
    anchor_quality = {setting: (_logit(row.score) - mean) / spread for setting, row in anchor.items()}

    # scaled[suite][model][effort] holds that suite's score on the anchor's scale.
    scaled: dict[str, dict[str, dict[str, float]]] = {data.anchor: {}}
    priced: dict[str, dict[str, dict[str, float]]] = {data.anchor: {}}
    for (model, effort), value in anchor_quality.items():
        scaled[data.anchor].setdefault(model, {})[effort] = value
    for (model, effort), row in anchor.items():
        if row.cost is not None:
            priced[data.anchor].setdefault(model, {})[effort] = math.log(row.cost)
    overlap: dict[str, int] = {}
    for name, rows in by_suite.items():
        if name == data.anchor:
            continue
        shared = sorted(set(rows) & set(anchor))
        overlap[name] = len(shared)
        if len(shared) < 3:
            raise DataError(f"{name} shares fewer than three settings with the anchor {data.anchor}")
        own = [_logit(rows[setting].score) for setting in shared]
        target = [anchor_quality[setting] for setting in shared]
        own_mean, own_spread = statistics.fmean(own), statistics.pstdev(own)
        if own_spread == 0:
            raise DataError(f"every setting {name} shares with the anchor scores the same")
        scale, shift = statistics.pstdev(target) / own_spread, statistics.fmean(target)
        # A suite's price level is how far its costs sit, at the median, from
        # the anchor's for the same setting.
        both = [s for s in shared if rows[s].cost is not None and anchor[s].cost is not None]
        level = statistics.median(math.log(rows[s].cost) - math.log(anchor[s].cost) for s in both) if both else None
        scaled[name], priced[name] = {}, {}
        for (model, effort), row in rows.items():
            scaled[name].setdefault(model, {})[effort] = (_logit(row.score) - own_mean) * scale + shift
            if row.cost is not None and level is not None:
                priced[name].setdefault(model, {})[effort] = math.log(row.cost) - level

    combined = []
    for model in sorted({model for suite in scaled.values() for model in suite}):
        quality = _blend({name: suite[model] for name, suite in scaled.items() if model in suite})
        cost = _blend({name: suite[model] for name, suite in priced.items() if model in suite})
        for effort in sorted(quality, key=EFFORTS.index):
            tested = sum(1 for suite in scaled.values() if effort in suite.get(model, {}))
            combined.append(Combined(
                model, effort, 50 + 10 * quality[effort],
                math.exp(cost[effort]) if effort in cost else None, tested,
            ))
    return combined, overlap


def _blend(cells: dict[str, dict[str, float]]) -> dict[str, float]:
    """Average one model's values across suites, effort by effort.

    A suite that tested only some efforts still says something about the
    model as a whole. Its average gap from the other suites, at the efforts
    they share, is applied to every effort, so it moves the curve up or down
    without bending it. With every suite at every effort this is a plain mean.
    """
    efforts = sorted({effort for values in cells.values() for effort in values})
    if not efforts:
        return {}
    point = {e: statistics.fmean(v[e] for v in cells.values() if e in v) for e in efforts}
    gap = {name: 0.0 for name in cells}
    for _ in range(200):
        settled = (gap, point)
        gap = {name: statistics.fmean(value - point[e] for e, value in values.items()) for name, values in cells.items()}
        point = {e: statistics.fmean(v[e] - gap[name] for name, v in cells.items() if e in v) for e in efforts}
        if (gap, point) == settled:
            break
    level = statistics.fmean(gap.values())
    return {e: point[e] + level for e in efforts}


def _dominates(a: Combined, b: Combined) -> bool:
    """Whether a scores at least as well as b for no more cost, and is not the same point."""
    return a.quality >= b.quality and a.cost <= b.cost and (a.quality > b.quality or a.cost < b.cost)


def frontier(combined: list[Combined]) -> set[tuple[str, str]]:
    """Settings no other setting beats on both quality and cost."""
    priced = [row for row in combined if row.cost is not None]
    return {(row.model, row.effort) for row in priced if not any(_dominates(other, row) for other in priced)}


def best_value_effort(points: list[Combined]) -> str | None:
    """The effort to stop at: the last one before a step up costs too much for what it adds.

    Efforts that a cheaper effort of the same model beats are left out first.
    Then, climbing by cost, it is the last effort reached before a step raises
    cost by more than BEST_VALUE_STEP_LIMIT percent per added point. A model
    with no priced effort has none; one with a single priced effort stops there.
    """
    priced = [point for point in _by_effort(points) if point.cost is not None]
    if not priced:
        return None
    kept = [point for point in priced if not any(_dominates(other, point) for other in priced)]
    by_position = {(point.cost, point.quality): point for point in reversed(kept)}
    kept = sorted(by_position.values(), key=lambda point: point.cost)
    stop = kept[0]
    for point in kept[1:]:
        if _step_price(stop, point) > BEST_VALUE_STEP_LIMIT:
            break
        stop = point
    return stop.effort


def _step_price(lower: Combined, higher: Combined) -> float:
    """Percent more cost for each added point, going from lower to higher quality."""
    return 100 * (higher.cost / lower.cost - 1) / (higher.quality - lower.quality)


def _beats(a: Combined, b: Combined) -> bool:
    """Whether setting a should be listed ahead of setting b.

    A setting at least as good for no more cost goes first. Otherwise the
    better-scoring one goes first only when its step price is within
    BEST_VALUE_STEP_LIMIT; past that, the cheaper one goes first.
    """
    if a.quality >= b.quality and a.cost <= b.cost:
        return (a.quality, -a.cost) != (b.quality, -b.cost) or a.model < b.model
    if b.quality >= a.quality and b.cost <= a.cost:
        return False
    if a.quality > b.quality:
        return _step_price(b, a) <= BEST_VALUE_STEP_LIMIT
    return _step_price(a, b) > BEST_VALUE_STEP_LIMIT


def order(settings: list[Combined]) -> list[Combined]:
    """List settings so each goes ahead of every setting after it, by _beats.

    When no remaining setting goes ahead of all the others, the best-scoring
    one goes next.
    """
    left = [row for row in settings if row.cost is not None]
    ordered = []
    while left:
        winners = [row for row in left if all(_beats(row, other) for other in left if other is not row)]
        pick = winners[0] if winners else max(left, key=lambda row: (row.quality, -row.cost))
        ordered.append(pick)
        left.remove(pick)
    return ordered


def vendor_rows(data: Data, combined: list[Combined], skipped: list[str] | None = None) -> list[tuple[str, Combined, str]]:
    """Build the rows that start from each vendor's own guidance, as (role, setting, replaced model).

    Each vendor contributes its everyday model to the Executor row and its
    flagship to the Team lead row, at the model's best-value effort. If another current,
    unrationed model from the same vendor scores higher for less at any
    effort, the cheapest such setting takes the slot instead. The Executor row
    follows the 40% price order; the Team lead row goes by combined quality,
    the cheaper setting first on a tie.
    """
    providers = {entry["model"]: entry["provider"] for entry in data.models if entry["status"] == "current"}
    marked = best_value_settings(combined)
    rows = []
    for role, kind in VENDOR_ROLES:
        picks = []
        for provider, entry in data.vendors.items():
            name = entry[kind]
            start = next((row for row in combined if row.model == name and (row.model, row.effort) in marked), None)
            if start is None:
                if skipped is not None:
                    skipped.append(f"{provider} {role} ({name} has no best-value effort)")
                continue
            better = [
                row for row in combined
                if row.model != name and providers.get(row.model) == provider and row.model not in entry["rationed"]
                and row.cost is not None and row.quality > start.quality and row.cost < start.cost
            ]
            pick = min(better, key=lambda row: (row.cost, -row.quality)) if better else start
            picks.append((pick, "" if pick is start else name))
        replaced = {id(pick): name for pick, name in picks}
        chosen = [pick for pick, _ in picks]
        ranked = order(chosen) if role == "Executor" else sorted(chosen, key=lambda row: (-row.quality, row.cost))
        rows += [(role, pick, replaced[id(pick)]) for pick in ranked]
    return rows


@dataclass(frozen=True)
class Preference:
    role: str
    model: str
    score: float
    sources: int
    effort: str | None  # the model's best-value effort in the base, if it has one


def preference_scores(data: Data, combined: list[Combined]) -> list[Preference]:
    """Score each current model on each preference row's sources, weighted equally.

    A source's scores are standardized across the current models it lists,
    taking each model's best score at any effort. A model's score is the mean
    over the sources that list it, on the base's scale: 50 plus 10 for each
    standard deviation. Rows come back best first within each role.
    """
    current = {entry["model"] for entry in data.models if entry["status"] == "current"}
    marked = dict(best_value_settings(combined))
    scored = []
    for role, names in data.preference.items():
        standard: dict[str, list[float]] = {}
        for name in names:
            best: dict[str, float] = {}
            for result in data.results:
                if result.suite == name and result.model in current:
                    best[result.model] = max(best.get(result.model, result.score), result.score)
            spread = statistics.pstdev(best.values()) if len(best) > 1 else 0
            if spread == 0:
                raise DataError(f"{name} needs at least two current models with different scores to score {role}")
            mean = statistics.fmean(best.values())
            for model, value in best.items():
                standard.setdefault(model, []).append((value - mean) / spread)
        rows = [Preference(role, model, 50 + 10 * statistics.fmean(values), len(values), marked.get(model))
                for model, values in standard.items()]
        scored += sorted(rows, key=lambda row: (-row.score, row.model))
    return scored


def best_value_settings(combined: list[Combined]) -> set[tuple[str, str]]:
    """Each model's best-value effort, as (model, effort) pairs."""
    by_model: dict[str, list[Combined]] = {}
    for row in combined:
        by_model.setdefault(row.model, []).append(row)
    picks = {model: best_value_effort(rows) for model, rows in by_model.items()}
    return {(model, effort) for model, effort in picks.items() if effort}


def cost_unit(data: Data) -> float:
    """The cost of a typical setting on the anchor suite: the geometric mean of its costs.

    Combined cost is reported as a multiple of this, so 1 means a typical
    setting and 2 means twice that, the way 50 on the quality scale means the
    anchor suite's average.
    """
    costs = [result.cost for result in data.results if result.suite == data.anchor and result.cost]
    if not costs:
        raise DataError(f"the anchor suite {data.anchor} has no costs, so relative cost cannot be computed")
    return math.exp(sum(math.log(cost) for cost in costs) / len(costs))


def _relative(cost: float | None, unit: float) -> str:
    return "missing" if cost is None else f"{cost / unit:.2f}"


def _money(value: float | str | None) -> str:
    if value is None:
        return "missing"
    return value if isinstance(value, str) else f"{value:.3f}"


def report(data: Data) -> list[str]:
    combined, overlap = combine(data)
    unit = cost_unit(data)
    outside = [name for name, in_base in data.suites.items() if not in_base]
    verdict = (
        f"OK routing evidence: {len(data.results)} rows from the latest read of each suite, "
        f"{len(data.history)} in the file; base suites: {', '.join(data.base)}; "
        f"anchor: {data.anchor}"
    )
    if overlap:
        verdict += "; settings shared with the anchor: " + ", ".join(f"{name} {count}" for name, count in overlap.items())
    if outside:
        verdict += f"; outside the base: {', '.join(outside)}"
    lines = [verdict, "# suite figures",
             "\t".join(("suite", "model", "effort", "score", "pass_rate", "cost_usd",
                        "cost_per_pass", "cost_per_added_point", "minutes"))]
    groups: dict[tuple[str, str], list[Result]] = {}
    for result in data.results:
        groups.setdefault((result.suite, result.model), []).append(result)
    for (suite, model) in sorted(groups):
        previous = None
        for result in _by_effort(groups[(suite, model)]):
            step = "-" if previous is None else cost_per_added_point(previous, result)
            lines.append("\t".join((
                suite, model, result.effort, f"{result.score:.2f}",
                "missing" if result.pass_rate is None else f"{result.pass_rate:.2f}",
                _money(result.cost), _money(cost_per_pass(result)), _money(step),
                "missing" if result.minutes is None else f"{result.minutes:.1f}",
            )))
            previous = result
    marked, best = best_value_settings(combined), frontier(combined)
    lines += ["# combined",
              "\t".join(("model", "effort", "combined_quality", "relative_cost", "suites", "best_value", "frontier"))]
    for row in combined:
        lines.append("\t".join((
            row.model, row.effort, f"{row.quality:.1f}", _relative(row.cost, unit),
            f"{row.suites} of {len(data.base)}", "yes" if (row.model, row.effort) in marked else "",
            "frontier" if (row.model, row.effort) in best else "",
        )))

    providers = {entry["model"]: entry["provider"] for entry in data.models}
    at_best_value = [row for row in combined if row.model in providers and (row.model, row.effort) in marked]
    lines += ["# candidates", "\t".join(("model", "provider", "effort", "combined_quality", "relative_cost", "suites", "frontier"))]
    for pick in order(at_best_value):
        lines.append("\t".join((
            pick.model, providers[pick.model], pick.effort, f"{pick.quality:.1f}", _relative(pick.cost, unit),
            f"{pick.suites} of {len(data.base)}", "frontier" if (pick.model, pick.effort) in best else "",
        )))
    lines += ["# rows", "\t".join(("role", "provider", "model", "effort", "combined_quality", "relative_cost", "replaces"))]
    skipped: list[str] = []
    built = vendor_rows(data, combined, skipped)
    if skipped:
        lines[0] += "; left out of rows: " + ", ".join(skipped)
    for role, pick, replaced in built:
        lines.append("\t".join((
            role, providers[pick.model], pick.model, pick.effort, f"{pick.quality:.1f}", _relative(pick.cost, unit), replaced,
        )))
    lines += ["# preference", "\t".join(("role", "provider", "model", "effort", "preference_score", "sources", "choice"))]
    chosen: dict[str, set[str]] = {}
    for row in preference_scores(data, combined):
        taken = chosen.setdefault(row.role, set())
        choice = ""
        if providers[row.model] not in taken:
            taken.add(providers[row.model])
            choice = str(len(taken))
        lines.append("\t".join((
            row.role, providers[row.model], row.model, row.effort or "missing", f"{row.score:.1f}",
            f"{row.sources} of {len(data.preference[row.role])}", choice,
        )))
    return lines


def changes(data: Data) -> list[str]:
    """What moved between each suite's latest read and the read before it."""
    rows, single = [], []
    for suite in data.suites:
        dates = sorted({result.date_read for result in data.history if result.suite == suite})
        if len(dates) < 2:
            single.append(suite)
            continue
        before, after = ({result.setting: result for result in data.history if result.suite == suite and result.date_read == date}
                         for date in dates[-2:])
        for setting in sorted(set(before) | set(after), key=lambda pair: (pair[0], EFFORTS.index(pair[1]))):
            old, new = before.get(setting), after.get(setting)
            if old and new and (old.score, old.cost, old.pass_rate) == (new.score, new.cost, new.pass_rate):
                continue
            rows.append("\t".join((
                suite, *setting, "changed" if old and new else "added" if new else "removed",
                f"{old.score:.2f}" if old else "", f"{new.score:.2f}" if new else "",
                _money(old.cost) if old else "", _money(new.cost) if new else "", dates[-2], dates[-1],
            )))
    compared = len(data.suites) - len(single)
    verdict = f"OK compared the two latest reads of {compared} suite(s); {len(rows)} difference(s)"
    if single:
        verdict += f"; one read only: {', '.join(single)}"
    return [verdict, "# changes",
            "\t".join(("suite", "model", "effort", "change", "score_before", "score_after",
                       "cost_before", "cost_after", "read_before", "read_after")), *rows]


# Chart palette and type, from DESIGN.md.
NAVY, COBALT, GRAPHITE, PAPER = "#042458", "#0050CC", "#47577A", "#F6F7FA"
TEXT_FONT = "Baskerville,Georgia,serif"
TITLE_FONT = "Didot,'Bodoni MT',Georgia,serif"
FALLBACK_INKS = (NAVY, COBALT, GRAPHITE)
MODEL_DASHES = ("", "7 5", "2 5", "12 4 2 4")
COST_TICKS = (0.02, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 200)
CHART_WIDTH = 1200
FOOTER = "One line per model, joining its efforts from lowest to highest. A dash pattern tells one provider's models apart."


@dataclass(frozen=True)
class Series:
    model: str
    provider: str
    current: bool
    suites: int
    points: list[Combined]


def _series(data: Data, rows: list[Combined]) -> list[Series]:
    """One entry per model chart.json lists that has priced results."""
    drawn = []
    for entry in data.models:
        points = [row for row in _by_effort([r for r in rows if r.model == entry["model"]]) if row.cost is not None]
        if points:
            drawn.append(Series(entry["model"], entry["provider"], entry["status"] == "current",
                                max(point.suites for point in points), points))
    return drawn


def _text(x: float, y: float, content: str, size: float, fill: str, **extra: str) -> str:
    attributes = "".join(f' {name.replace("_", "-")}="{value}"' for name, value in extra.items())
    family = extra.get("font_family")
    font = "" if family else f' font-family="{TEXT_FONT}"'
    return f'<text x="{x:.1f}" y="{y:.1f}"{font} font-size="{size:g}" fill="{fill}"{attributes}>{escape(content)}</text>'


@dataclass(frozen=True)
class Scale:
    """The axis ranges every panel of one figure shares."""
    low: float
    high: float
    floor: float
    ceiling: float

    @classmethod
    def of(cls, series: list[Series]) -> "Scale":
        costs = [point.cost for line in series for point in line.points]
        scores = [point.quality for line in series for point in line.points]
        pad = (max(scores) - min(scores)) * 0.08 or 1.0
        return cls(math.log10(min(costs)) - 0.06, math.log10(max(costs)) + 0.06, min(scores) - pad, max(scores) + pad)


def _spots(radii: tuple[int, ...], angles: tuple[int, ...]) -> list[tuple[float, float, str, int]]:
    """Label positions around a point, nearest ring first, as (dx, dy, text anchor, ring radius)."""
    out = []
    for radius in radii:
        for angle in angles:
            dx = radius * math.cos(math.radians(angle))
            out.append((dx, -radius * math.sin(math.radians(angle)), "start" if dx >= -0.01 else "end", radius))
    return out


LINE_LABEL_SPOTS = _spots((14, 30, 46, 62, 78, 94, 110, 126), (0, -30, 30, -60, 60, -90, 90, 180, -150, 150, -120, 120))


def _marker(effort: str, x: float, y: float, ink: str) -> str:
    """One data point, drawn in the shape that names its effort."""
    ring = f'stroke="{PAPER}" stroke-width="1.6" stroke-linejoin="round"'
    tag = f'class="point" data-effort="{effort}" data-x="{x:.1f}" data-y="{y:.1f}"'

    def polygon(corners: list[tuple[float, float]]) -> str:
        path = " ".join(f"{x + dx:.1f},{y + dy:.1f}" for dx, dy in corners)
        return f'<polygon {tag} points="{path}" fill="{ink}" {ring}/>'

    if effort == "none":
        return f'<circle {tag} cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{PAPER}" stroke="{ink}" stroke-width="1.8"/>'
    if effort == "minimal":
        return f'<circle {tag} cx="{x:.1f}" cy="{y:.1f}" r="2.8" fill="{ink}" {ring}/>'
    if effort == "low":
        return f'<circle {tag} cx="{x:.1f}" cy="{y:.1f}" r="4.4" fill="{ink}" {ring}/>'
    if effort == "medium":
        return polygon([(-4.2, -4.2), (4.2, -4.2), (4.2, 4.2), (-4.2, 4.2)])
    if effort == "high":
        return polygon([(0, -5.6), (5.4, 4), (-5.4, 4)])
    if effort == "xhigh":
        return polygon([(0, -6), (5.2, 0), (0, 6), (-5.2, 0)])
    star = [(r * math.sin(math.radians(36 * i)), -r * math.cos(math.radians(36 * i))) for i in range(10) for r in ((7, 3.1)[i % 2],)]
    return polygon(star)


def _best_value_mark(x: float, y: float, ink: str, radius: float, tag: str) -> list[str]:
    """A soft tint of the line's colour behind a point, edged with a hairline ring in the same colour."""
    return [f'<circle class="knee-halo" cx="{x:.1f}" cy="{y:.1f}" r="{radius:g}" fill="{ink}" fill-opacity=".14"/>',
            f'<circle {tag} cx="{x:.1f}" cy="{y:.1f}" r="{radius:g}" fill="none" stroke="{ink}" stroke-width="1"/>']


def _effort_key(efforts: list[str], y: float) -> list[str]:
    """The key every figure shares: one marker per effort, then the best-value mark."""
    out = [_text(40, y + 4, "Effort", 12, GRAPHITE, font_style="italic")]
    x = 86.0
    for effort in efforts:
        out.append(_marker(effort, x, y, NAVY).replace('class="point"', 'class="key"'))
        out.append(_text(x + 11, y + 4, effort.capitalize(), 12, NAVY, **{"class": "legend"}))
        x += 11 + 0.56 * 12 * len(effort) + 20
    x += 14
    out += _best_value_mark(x, y, NAVY, 8.5, 'class="key-knee"')
    out.append(_text(x + 14, y + 4, f"Best-value effort: the last step costing at most {BEST_VALUE_STEP_LIMIT:g}% more per point", 12, NAVY, **{"class": "legend"}))
    return out


def _panel(x0: float, y0: float, width: float, height: float, scale: Scale,
           styled: list[tuple[Series, str, str]], context: list[Series], legend: list[tuple[str, str, str]],
           title: str, y_label: str, x_label: str, show_counts: bool, money: bool = True,
           legend_rows: int = 1) -> list[str]:
    """Draw one plot. styled pairs each highlighted series with its ink and dash."""
    left, right, top, bottom = 62, 128, 46, 44
    size = 13.0
    widths = [32 + 0.56 * (size - 1) * len(name) + 18 for name, _, _ in legend]
    rows_used, run = 1, 0.0
    for wide in widths:
        if run and run + wide > width - left - right + 100:
            rows_used, run = rows_used + 1, 0.0
        run += wide
    top += 18 * (max(rows_used, legend_rows) - 1)

    def px(cost: float) -> float:
        return x0 + left + (math.log10(cost) - scale.low) / (scale.high - scale.low) * (width - left - right)

    def py(score: float) -> float:
        return y0 + height - bottom - (score - scale.floor) / (scale.ceiling - scale.floor) * (height - top - bottom)

    out = [_text(x0 + left, y0 + 16, title, size + 3, NAVY, font_weight="600")] if title else []
    for tick in COST_TICKS:
        if scale.low <= math.log10(tick) <= scale.high:
            out.append(f'<line x1="{px(tick):.1f}" x2="{px(tick):.1f}" y1="{y0 + top:.1f}" y2="{y0 + height - bottom:.1f}" stroke="{GRAPHITE}" stroke-opacity=".16"/>')
            out.append(_text(px(tick), y0 + height - bottom + 17, f"${tick:g}" if money else f"{tick:g}×", size - 1, GRAPHITE, text_anchor="middle"))
    step = next((s for s in (0.5, 1, 2, 5, 10, 20, 50) if (scale.ceiling - scale.floor) / s <= 6), 50)
    tick = math.ceil(scale.floor / step) * step
    while tick <= scale.ceiling:
        out.append(f'<line x1="{x0 + left:.1f}" x2="{x0 + width - right:.1f}" y1="{py(tick):.1f}" y2="{py(tick):.1f}" stroke="{GRAPHITE}" stroke-opacity=".16"/>')
        out.append(_text(x0 + left - 8, py(tick) + 4, f"{tick:g}", size - 1, GRAPHITE, text_anchor="end"))
        tick += step
    out.append(f'<rect x="{x0 + left:.1f}" y="{y0 + top:.1f}" width="{width - left - right:.1f}" height="{height - top - bottom:.1f}" fill="none" stroke="{GRAPHITE}" stroke-opacity=".45"/>')
    if x_label:
        out.append(_text(x0 + left + (width - left - right) / 2, y0 + height - 6, x_label, size, GRAPHITE, text_anchor="middle"))
    if y_label:
        middle = y0 + top + (height - top - bottom) / 2
        out.append(f'<text transform="translate({x0 + 16:.1f},{middle:.1f}) rotate(-90)" font-family="{TEXT_FONT}" font-size="{size:g}" fill="{GRAPHITE}" text-anchor="middle">{escape(y_label)}</text>')

    # Legend: a short sample of each line, then its name in text ink.
    key_x, key_y = x0 + left, y0 + 32
    for (name, ink, dash), wide in zip(legend, widths):
        if key_x > x0 + left and key_x - (x0 + left) + wide > width - left - right + 100:
            key_x, key_y = x0 + left, key_y + 18
        stroke = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<line x1="{key_x:.1f}" x2="{key_x + 26:.1f}" y1="{key_y:.1f}" y2="{key_y:.1f}" stroke="{ink}" stroke-width="2"{stroke} stroke-linecap="round"/>')
        out.append(_text(key_x + 32, key_y + 4, name, size - 1, NAVY, **{"class": "legend"}))
        key_x += wide

    for line in context:
        path = " ".join(f"{px(point.cost):.1f},{py(point.quality):.1f}" for point in line.points)
        out.append(f'<polyline class="context" data-model="{escape(line.model)}" points="{path}" fill="none" stroke="{GRAPHITE}" stroke-opacity=".32" stroke-width="1.2" stroke-linejoin="round" stroke-linecap="round"/>')

    ink_points: list[tuple[float, float]] = []
    blocked: list[tuple[float, float, float, float]] = []
    line_labels = []
    # Best-value marks go down first, so every line and point stays crisp on top of the tint.
    rings = []
    for line, ink, _ in styled:
        if line.current and len(line.points) > 1:
            effort = best_value_effort(line.points)
            for point in line.points:
                if point.effort == effort:
                    x, y = px(point.cost), py(point.quality)
                    halo, ring = _best_value_mark(x, y, ink, 11, f'class="knee" data-model="{escape(line.model)}"')
                    out.append(halo)
                    rings.append(ring)
                    blocked.append((x - 12, y - 12, x + 12, y + 12))
    for line, ink, dash in styled:
        stroke = f' stroke-dasharray="{dash}"' if dash else ""
        spots = [(px(point.cost), py(point.quality)) for point in line.points]
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in spots)
        out.append(f'<polyline class="series" data-model="{escape(line.model)}" data-suites="{line.suites}" points="{path}" fill="none" stroke="{ink}" stroke-width="2"{stroke} stroke-linejoin="round" stroke-linecap="round"/>')
        for (ax, ay), (bx, by) in zip(spots, spots[1:]):
            steps = max(1, int(math.hypot(bx - ax, by - ay) / 4))
            ink_points += [(ax + (bx - ax) * i / steps, ay + (by - ay) * i / steps) for i in range(steps + 1)]
        for x, y in spots:
            blocked.append((x - 6, y - 6, x + 6, y + 6))
        out += [_marker(point.effort, x, y, ink) for point, (x, y) in zip(line.points, spots)]
        name = f"{line.model} ({line.suites})" if show_counts else line.model
        line_labels.append((spots[-1][0], spots[-1][1], name, line.current))

    out += rings
    frame = (x0 + left + 2, y0 + top + 2, x0 + width - 4, y0 + height - bottom - 2)

    def place(x: float, y: float, text: str, text_size: float, spots, leader: bool, **attributes: str) -> None:
        """Put a label at the nearest spot clear of lines, markers, and other labels."""
        wide = 0.56 * text_size * len(text)
        best = None
        for dx, dy, anchor, reach in spots:
            start = x + dx if anchor == "start" else x + dx - wide
            base = y + dy + text_size / 3
            box = (start - 2, base - text_size, start + wide + 2, base + 4)
            on_ink = sum(1 for ix, iy in ink_points if box[0] - 2 <= ix <= box[2] + 2 and box[1] - 2 <= iy <= box[3] + 2)
            on_block = sum(1 for other in blocked if box[0] < other[2] and other[0] < box[2] and box[1] < other[3] and other[1] < box[3])
            outside = box[0] < frame[0] or box[2] > frame[2] or box[1] < frame[1] or box[3] > frame[3]
            penalty = 25 * on_ink + 1000 * on_block + (400 if outside else 0) + reach
            if best is None or penalty < best[0]:
                best = (penalty, box, anchor, x + dx, base)
        _, box, anchor, tx, ty = best
        blocked.append(box)
        near_x, near_y = min(max(x, box[0]), box[2]), min(max(y, box[1]), box[3])
        if leader and math.hypot(near_x - x, near_y - y) > 16:
            out.append(f'<line class="leader" x1="{x:.1f}" y1="{y:.1f}" x2="{near_x:.1f}" y2="{near_y:.1f}" stroke="{GRAPHITE}" stroke-width="0.8"/>')
            steps = int(math.hypot(near_x - x, near_y - y) / 4)
            ink_points.extend((x + (near_x - x) * i / steps, y + (near_y - y) * i / steps) for i in range(2, steps))
        out.append(_text(tx, ty, text, text_size, NAVY, text_anchor=anchor, **attributes))

    for x, y, text, current in sorted(line_labels, key=lambda label: (not label[3], label[1])):
        place(x, y, text, size, LINE_LABEL_SPOTS, True, font_weight="600" if current else "400", **{"class": "line-label"})
    return out


def provider_inks(data: Data) -> dict[str, str]:
    """Each provider's colour: the one chart.json gives it, or a fallback in order."""
    providers = list(dict.fromkeys(entry["provider"] for entry in data.models))
    plain = iter(FALLBACK_INKS * len(providers))
    return {provider: data.vendors.get(provider, {}).get("colour") or next(plain) for provider in providers}


def _styles(series: list[Series], inks: dict[str, str]) -> dict[str, tuple[str, str]]:
    """Give each model its provider's ink and its own dash, the same in every figure."""
    styles = {}
    for line in series:
        peers = [other.model for other in series if other.provider == line.provider and other.current]
        ink = inks[line.provider]
        styles[line.model] = (ink, MODEL_DASHES[peers.index(line.model) % len(MODEL_DASHES)]) if line.current else (GRAPHITE, "1 4")
    return styles


def _corner_marks(w: float, h: float) -> str:
    return f"M14 26V14H26M{w - 26} 14H{w - 14}V26M14 {h - 26}V{h - 14}H26M{w - 26} {h - 14}H{w - 14}V{h - 26}"


def _ground(w: int, h: int) -> list[str]:
    """Chalk Paper, the hairline that holds it on a white page, and the corner marks."""
    return [
        f'<rect width="{w}" height="{h}" fill="{PAPER}"/>',
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" fill="none" stroke="{GRAPHITE}" stroke-opacity=".32"/>',
        f'<path d="{_corner_marks(w, h)}" fill="none" stroke="{GRAPHITE}" stroke-opacity=".5"/>',
    ]


def _frame(body: list[str], title: str, subtitle: str, footer: list[str], h: int, efforts: list[str]) -> str:
    w, h = CHART_WIDTH, h + 26
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">',
        f"<title>{escape(title)}</title>",
        *_ground(w, h),
        _text(40, 52, title, 30, NAVY, font_family=TITLE_FONT),
        _text(40, 78, subtitle, 15, COBALT, font_weight="600"),
        *_effort_key(efforts, 104),
        '<g transform="translate(0,26)">',
        *body,
        "</g>",
        *[_text(40, h - 18 - 16 * (len(footer) - 1 - index), line, 12, GRAPHITE) for index, line in enumerate(footer)],
        "</svg>",
    ]) + "\n"


def _provider_grid(series: list[Series], styles: dict[str, tuple[str, str]], scale: Scale, y_label: str, x_label: str,
                   show_counts: bool, money: bool = True) -> tuple[list[str], int]:
    """One panel per provider on a shared scale, with the other providers' models faint behind."""
    providers = list(dict.fromkeys(line.provider for line in series))
    width, height, columns = (CHART_WIDTH - 60) / 2, 350, 2
    rows = math.ceil(len(providers) / columns)
    most = max(sum(1 for line in series if line.provider == provider) for provider in providers)
    legend_rows = 1 + (most > 3)
    body: list[str] = []
    for index, provider in enumerate(providers):
        own = [line for line in series if line.provider == provider]
        styled = [(line, *styles[line.model]) for line in own]
        legend = [(f"{line.model} ({line.suites})" if show_counts else line.model, ink, dash) for line, ink, dash in styled]
        column, row = index % columns, index // columns
        body.append(f'<g data-provider="{escape(provider)}">')
        body += _panel(30 + column * width, 100 + row * height, width, height - 14, scale, styled,
                       [line for line in series if line.provider != provider], legend, provider,
                       y_label if column == 0 else "", x_label if index + columns >= len(providers) else "", False, money,
                       legend_rows)
        body.append("</g>")
    return body, 100 + rows * height + 44


def charts(data: Data) -> dict[str, str]:
    """Build the chart files as SVG text, keyed by file name."""
    combined, _ = combine(data)
    unit = cost_unit(data)
    combined = [Combined(row.model, row.effort, row.quality, None if row.cost is None else row.cost / unit, row.suites)
                for row in combined]
    base = data.base
    read = max(result.date_read for result in data.results if result.suite in base)
    versions = {result.suite: result.suite_version for result in data.results}
    everyone = _series(data, combined)
    if not everyone:
        raise DataError("none of the models chart.json lists has results with a cost")
    scale = Scale.of(everyone)
    y_label = f"Combined quality (50 = {data.anchor} average)"
    x_label = f"Relative cost per task (1 = a typical {data.anchor} setting), log scale"
    efforts = [effort for effort in EFFORTS if any(point.effort == effort for line in everyone for point in line.points)]
    notes = [f"{FOOTER} The marker's shape names the effort.",
             f"The number beside a name counts the suites that tested it at any effort, of {len(base)}. Data read {read}.",
             "Suites: " + ", ".join(f"{suite} {versions.get(suite, '')}".strip() for suite in base) + "."]

    inks = provider_inks(data)
    styles = _styles(everyone, inks)
    styled = [(line, *styles[line.model]) for line in everyone]
    providers = list(dict.fromkeys(line.provider for line in everyone))
    legend = [(provider, inks[provider], "") for provider in providers]
    together = _frame(
        _panel(30, 100, CHART_WIDTH - 60, 600, scale, styled, [], legend, "", y_label, x_label, True, False),
        "What each model gains as you raise its effort",
        f"{len(base)} benchmark suites on one scale. Colour names the provider, shape names the effort, and each line is labelled with its model.",
        notes, 776, efforts,
    )

    body, height = _provider_grid(everyone, styles, scale, y_label, x_label, True, False)
    apart = _frame(
        body, "The same chart, one provider at a time",
        "Every panel has the same axes as the chart above. The faint lines are the other providers' models.",
        notes, height + 30, efforts,
    )

    panels: list[str] = []
    offset = 100
    for suite in base:
        rows = [Combined(r.model, r.effort, r.score, r.cost, 1) for r in data.results if r.suite == suite]
        series = _series(data, rows)
        if not series:
            continue
        version = next(r.suite_version for r in data.results if r.suite == suite)
        grid, used = _provider_grid(series, styles, Scale.of(series), "Score, 0 to 100", "Cost per task, log scale", False)
        panels.append(f'<g data-suite="{escape(suite)}">')
        panels.append(_text(40, offset + 4, f"{suite} {version}", 18, NAVY, font_weight="600"))
        panels.append(f'<g transform="translate(0,{offset - 78})">')
        panels += grid
        panels.append("</g></g>")
        offset += used - 62
    below = _frame(
        panels, "The same settings, suite by suite",
        "Each suite on its own scale, one panel per provider, with the best-value effort each suite finds.",
        [f"{FOOTER} The marker's shape names the effort. Data read {read}."], offset + 30, efforts,
    )
    return {"routing-base.svg": together, "routing-base-providers.svg": apart, "routing-base-suites.svg": below}


RECOMMENDATION_COLUMNS = ("role", "choice", "provider", "model", "model_id", "effort", "judgment", "reviewed")


def table_chart(directory: Path, data: Data) -> str | None:
    """Draw recommendations.csv as a shareable figure, one row per role. None when the file is absent."""
    path = directory / "recommendations.csv"
    if not path.is_file():
        return None
    by_role: dict[str, list[tuple[int, str, str, str, bool]]] = {}
    dates = []
    known = provider_inks(data)
    for line, row in enumerate(_read_csv(path, RECOMMENDATION_COLUMNS), start=2):
        if None in row or any(row[name] is None for name in RECOMMENDATION_COLUMNS):
            raise DataError(f"recommendations.csv line {line}: expected {len(RECOMMENDATION_COLUMNS)} columns")
        _iso_date(row["reviewed"], f"recommendations.csv line {line}: reviewed")
        if (row["effort"] not in EFFORTS or row["judgment"] not in ("", "yes") or row["choice"] not in ("1", "2", "3")
                or row["provider"] not in known or not row["model"].strip() or not row["model_id"].strip()):
            raise DataError(f"recommendations.csv line {line}: needs choice 1 to 3, a provider chart.json lists, a model and id, "
                            "a known effort, and judgment empty or yes")
        picks = by_role.setdefault(row["role"], [])
        if any(pick[0] == int(row["choice"]) for pick in picks):
            raise DataError(f"recommendations.csv line {line}: {row['role']} has choice {row['choice']} twice")
        picks.append((int(row["choice"]), row["provider"], row["model"], row["effort"], row["judgment"] == "yes"))
        dates.append(row["reviewed"])
    if not by_role:
        raise DataError("recommendations.csv holds no picks")
    rows = [(role, [pick[1:] for pick in sorted(picks)]) for role, picks in by_role.items()]
    reviewed = max(dates)
    left, label_w, top, row_h = 40, 170, 150, 92
    col_w = (CHART_WIDTH - 2 * left - label_w) / 3
    body = []
    for index, heading in enumerate(("First choice", "Second choice", "Third choice")):
        body.append(_text(left + label_w + index * col_w + 16, top - 14, heading, 13, GRAPHITE, font_style="italic"))
    for number, (role, picks) in enumerate(rows):
        y = top + number * row_h
        body.append(f'<line x1="{left}" x2="{CHART_WIDTH - left}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GRAPHITE}" stroke-opacity=".3"/>')
        body.append(_text(left, y + row_h / 2 + 7, role, 20, NAVY, font_family=TITLE_FONT))
        for column, (provider, name, effort, judged) in enumerate(picks):
            x = left + label_w + column * col_w + 16
            colour = known[provider]
            body.append(f'<rect x="{x - 16:.1f}" y="{y + 18:.1f}" width="4" height="{row_h - 36:.1f}" rx="2" fill="{colour}"/>')
            body.append(_text(x, y + 40, name + (" *" if judged else ""), 18, NAVY, font_weight="600"))
            body.append(_text(x, y + 67, f"{effort.capitalize()} effort · {provider}", 14, GRAPHITE))
    end = top + len(rows) * row_h
    body.append(f'<line x1="{left}" x2="{CHART_WIDTH - left}" y1="{end:.1f}" y2="{end:.1f}" stroke="{GRAPHITE}" stroke-opacity=".3"/>')
    footer = ["Take the first model in a row that you can run. The bar's colour names the provider.",
              "* Marks my judgment over the method. Last reviewed " + reviewed + "."]
    h = end + 80
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CHART_WIDTH} {h}" width="{CHART_WIDTH}" height="{h}" role="img">',
        "<title>Which model to use for which work</title>",
        *_ground(CHART_WIDTH, h),
        _text(left, 52, "Which model to use for which work", 30, NAVY, font_family=TITLE_FONT),
        _text(left, 80, "Three providers per row, best first, each at the effort setting worth its cost.", 15, COBALT, font_weight="600"),
        *body,
        *[_text(left, h - 34 + 16 * index, line, 12, GRAPHITE) for index, line in enumerate(footer)],
        "</svg>",
    ]) + "\n"


SOURCE_SUITES = {"frontiercode": "FrontierCode", "vulcanbench": "VulcanBench"}
SOURCE_EFFORTS = {"extra-high": "xhigh", "extra high": "xhigh", "na": "none"}
TABLE_COLUMNS = ("model", "effort", "score", "pass_rate", "cost_usd", "minutes")


def _plain(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".")


def _source_rows(fmt: str, path: Path) -> list[tuple[str, str, str, str, str, str]]:
    """Read a downloaded leaderboard into (model, effort, score, pass_rate, cost, minutes)."""
    rows = []
    try:
        if fmt == "table":
            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                missing = [name for name in TABLE_COLUMNS if name not in (reader.fieldnames or [])]
                if missing:
                    raise ValueError(f"missing column(s): {', '.join(missing)}")
                for entry in reader:
                    rows.append((
                        entry["model"], entry["effort"].strip().lower(), f"{float(entry['score']):.2f}",
                        f"{float(entry['pass_rate']):.2f}" if entry["pass_rate"] else "",
                        _plain(float(entry["cost_usd"])) if entry["cost_usd"] else "",
                        _plain(float(entry["minutes"])) if entry["minutes"] else "",
                    ))
        elif fmt == "frontiercode":
            source = json.loads(path.read_text(encoding="utf-8"))
            for model, efforts in source["data"].items():
                for effort, subsets in efforts.items():
                    entry = subsets["main"]
                    cost, minutes = entry.get("cost"), entry.get("duration_min")
                    rows.append((
                        model, effort, f"{entry['new_score'] * 100:.2f}", f"{entry['correct'] * 100:.2f}",
                        "" if cost is None else _plain(cost), "" if minutes is None else _plain(minutes),
                    ))
        else:
            with path.open(newline="", encoding="utf-8") as handle:
                for entry in csv.DictReader(handle):
                    rows.append((
                        entry["model"], entry["effort"], f"{float(entry['combined_33']):.2f}",
                        f"{100 * int(entry['passed']) / int(entry['passed_of']):.2f}",
                        _plain(float(entry["mean_usd"])) if entry["mean_usd"] else "",
                        _plain(float(entry["mean_minutes"])) if entry["mean_minutes"] else "",
                    ))
    except (OSError, ValueError, KeyError, TypeError, AttributeError, ZeroDivisionError) as error:
        raise DataError(f"{path.name} is not a readable {fmt} file: {error!r}") from None
    if not rows:
        raise DataError(f"{path.name} holds no results")
    return rows


def import_source(directory: Path, fmt: str, path: Path, version: str, date: str, url: str,
                  suite: str | None = None) -> str:
    """Add one read of a suite to results.csv, leaving every other row as written.

    The file is append-only: a new read goes after the rows already there.
    Importing a suite again on the same date replaces that day's read in place.
    """
    suite = suite or SOURCE_SUITES.get(fmt)
    if not suite:
        raise DataError("a table import needs --suite with the suite's name")
    results_path = directory / "results.csv"
    try:
        existing = [line for line in results_path.read_text(encoding="utf-8").splitlines()[1:] if line]
    except FileNotFoundError:
        existing = []
    fresh = []
    for model, effort, score, pass_rate, cost, minutes in _source_rows(fmt, path):
        model, effort = model.removeprefix("Claude ").strip(), SOURCE_EFFORTS.get(effort, effort)
        cells = io.StringIO()
        csv.writer(cells, lineterminator="").writerow((suite, version, model, effort, score, pass_rate, cost, minutes, date, url))
        fresh.append(((model, EFFORTS.index(effort) if effort in EFFORTS else -1), cells.getvalue()))
    fresh_lines = [line for _, line in sorted(fresh, key=lambda pair: pair[0])]

    body, slot = [], None
    for line in existing:
        cells = next(csv.reader([line]))
        if len(cells) != len(RESULT_COLUMNS):
            raise DataError(f"results.csv has a row without {len(RESULT_COLUMNS)} columns: {line!r}")
        if cells[0] == suite and cells[8] == date:
            slot = len(body) if slot is None else slot
            continue
        body.append(line)
    slot = len(body) if slot is None else slot
    body[slot:slot] = fresh_lines
    text = "\n".join([",".join(RESULT_COLUMNS), *body]) + "\n"
    data = load(directory, results_text=text)
    results_path.write_text(text, encoding="utf-8")
    reads = len({result.date_read for result in data.history if result.suite == suite})
    return f"OK imported {len(fresh_lines)} {suite} rows read {date}; results.csv now holds {reads} read(s) of {suite} and {len(data.history)} rows"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--data", type=Path, default=Path("docs/routing"))
    report_parser = commands.add_parser("report", help="print the figures", parents=[shared])
    report_parser.add_argument("--as-of", help="use only reads on or before this date, YYYY-MM-DD")
    commands.add_parser("changes", help="list what moved between each suite's two latest reads", parents=[shared])
    import_parser = commands.add_parser("import", help="add one read of a suite from a downloaded file", parents=[shared])
    import_parser.add_argument("--format", choices=[*sorted(SOURCE_SUITES), "table"], required=True)
    import_parser.add_argument("--suite", help="suite name, required for --format table")
    import_parser.add_argument("--file", type=Path, required=True)
    import_parser.add_argument("--version", required=True)
    import_parser.add_argument("--date", required=True)
    import_parser.add_argument("--url", required=True)
    charts_parser = commands.add_parser("charts", help="write the chart files", parents=[shared])
    charts_parser.add_argument("--out", type=Path, default=Path("docs/assets"))
    args = parser.parse_args(argv)
    try:
        if args.command == "report":
            print("\n".join(report(load(args.data, as_of=args.as_of))))
        elif args.command == "changes":
            print("\n".join(changes(load(args.data))))
        elif args.command == "import":
            print(import_source(args.data, args.format, args.file, args.version, args.date, args.url, args.suite))
        elif args.command == "charts":
            data = load(args.data)
            files = charts(data)
            table = table_chart(args.data, data)
            if table:
                files["routing-table.svg"] = table
            args.out.mkdir(parents=True, exist_ok=True)
            for name, text in files.items():
                (args.out / name).write_text(text, encoding="utf-8")
            print(f"OK wrote {', '.join(files)} to {args.out}")
    except DataError as error:
        print(f"ERROR {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
