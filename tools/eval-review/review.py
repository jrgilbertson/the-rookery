#!/usr/bin/env python3
"""Local review server for skill-evaluation manifests.

Serves one manifest, or one repository index of manifests, plus that skill's
feedback and listed evidence. It does not launch models, grade output, or
manage jobs. The HTTP contract lives in tools/eval-review/README.md.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import unicodedata
import re
import stat
import socketserver
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse


SCHEMA = 1
MAX_BODY = 65536
MAX_NOTE = 4000
MAX_EVIDENCE_BYTES = 2_000_000
MAX_PATH = 2048
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,80}$")
TOOL_DIR = Path(__file__).resolve().parent
HTML_CSP = (
    "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
    "connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"
)
DATA_CSP = "default-src 'none'; base-uri 'none'; frame-ancestors 'none'"


class FeedbackError(Exception):
    def __init__(self, status, message, item=None):
        super().__init__(message)
        self.status = status
        self.item = item


class ConfigError(Exception):
    pass


class SelectorError(Exception):
    def __init__(self, status):
        super().__init__("Rejected." if status == 400 else "Not found.")
        self.status = status


def valid_id(value):
    return isinstance(value, str) and ID_RE.fullmatch(value) is not None


def finite_number(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value) and value >= 0
    except OverflowError:
        return False


def whole_number(value):
    return type(value) is int and value >= 0


def dump_json(payload, **kwargs):
    raw = json.dumps(payload, ensure_ascii=False, **kwargs)
    return raw.encode("utf-8", "backslashreplace").decode("utf-8")


def fingerprint(payload):
    encoded = dump_json(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def remember_subject(model, subject_id, subject_fp):
    model["subjects"][subject_id] = {"fingerprint": subject_fp}
    model["bindings"].append({
        "record_type": "subject",
        "subject_id": subject_id,
        "fingerprint": subject_fp,
        "usable": subject_fp is not None,
    })


def add_error(errors, scope, ident, message):
    errors.append({"scope": scope, "id": ident, "message": message})


def optional_string(value):
    if value is None:
        return None, True
    if isinstance(value, str):
        return value, True
    return None, False


def clean_evidence_refs(value, errors, scope, ident):
    if value is None:
        return [], True
    if not isinstance(value, list):
        add_error(errors, scope, ident, "Evidence references are malformed.")
        return [], False
    refs = []
    ok = True
    for entry in value:
        if not isinstance(entry, dict) or not valid_id(entry.get("id")) or not isinstance(entry.get("label"), str):
            add_error(errors, scope, ident, "An evidence reference is malformed.")
            ok = False
            continue
        refs.append({"id": entry["id"], "label": entry["label"]})
    return refs, ok


def contained_path(root_real, relative):
    # Overlap checks need the listed path even when the file is not created yet.
    if not isinstance(relative, str) or relative == "" or "\\" in relative or "\x00" in relative:
        return None
    rel = Path(relative)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts:
        return None
    try:
        real = Path(os.path.realpath(root_real.joinpath(*rel.parts)))
        real.relative_to(root_real)
    except UnicodeError:
        raise
    except (OSError, ValueError):
        return None
    if real == root_real:
        return None
    return real


def resolve_contained(root_real, relative):
    real = contained_path(root_real, relative)
    if real is None:
        return None
    try:
        info = real.stat()
    except UnicodeError:
        raise
    except OSError:
        return None
    if not stat.S_ISREG(info.st_mode):
        return None
    return real


def evidence_index(manifest_path, data, errors):
    root_value = data.get("evidence_root")
    files = data.get("files")
    index = {}
    listed = []
    if not isinstance(root_value, str) or root_value == "":
        add_error(errors, "manifest", None, "evidence_root is missing.")
        return index, listed
    if not isinstance(files, list):
        add_error(errors, "manifest", None, "files is malformed.")
        return index, listed
    root = Path(root_value)
    if not root.is_absolute():
        root = manifest_path.parent / root
    try:
        root_real = Path(os.path.realpath(root))
    except UnicodeError:
        add_error(errors, "manifest", None, "evidence_root is not a usable filesystem path.")
        return index, listed
    except OSError:
        add_error(errors, "manifest", None, "evidence_root is not available.")
        return index, listed
    root_usable = root_real.is_dir()
    if not root_usable:
        add_error(errors, "manifest", None, "evidence_root is not a directory.")
    blocked = set()
    for entry in files:
        if not isinstance(entry, dict) or not valid_id(entry.get("id")) or not isinstance(entry.get("path"), str):
            add_error(errors, "manifest", None, "A files entry is malformed.")
            continue
        evidence_id = entry["id"]
        try:
            located = contained_path(root_real, entry["path"])
        except UnicodeError:
            add_error(errors, "manifest", evidence_id, f"Evidence path for {evidence_id} is not a usable filesystem path.")
            blocked.add(evidence_id)
            continue
        if located is not None:
            listed.append(located)
        if not root_usable:
            continue
        if evidence_id in index or evidence_id in blocked:
            add_error(errors, "manifest", evidence_id, "Evidence id is duplicated and will not be served.")
            index.pop(evidence_id, None)
            blocked.add(evidence_id)
            continue
        try:
            contained = resolve_contained(root_real, entry["path"])
        except UnicodeError:
            add_error(errors, "manifest", evidence_id, f"Evidence path for {evidence_id} is not a usable filesystem path.")
            blocked.add(evidence_id)
            continue
        if contained is None:
            add_error(errors, "manifest", evidence_id, "Evidence path is outside the evidence root and will not be served.")
            blocked.add(evidence_id)
            continue
        index[evidence_id] = (root_real, entry["path"])
    return index, listed


def refs_resolve(refs, index):
    return bool(refs) and all(evidence_material(ref, index).get("resolved") for ref in refs)


def clean_cost(value, errors, run_id):
    if value is None:
        return None, "unknown"
    if not isinstance(value, dict):
        add_error(errors, "run", run_id, f"Cost for run {run_id} is malformed.")
        return None, "malformed"
    basis = value.get("basis")
    usd = value.get("usd")
    if basis not in ("api_equivalent_estimate", "subscription_charge") or not finite_number(usd):
        add_error(errors, "run", run_id, f"Cost for run {run_id} is malformed.")
        return None, "malformed"
    return {"usd": usd, "basis": basis}, basis


def clean_duration(value, errors, run_id):
    if value is None:
        return None, "unknown"
    if not finite_number(value):
        add_error(errors, "run", run_id, f"Duration for run {run_id} is malformed.")
        return None, "malformed"
    return value, "present"


def clean_tokens(value, errors, run_id):
    if value is None:
        return None, "unknown"
    if not isinstance(value, dict):
        add_error(errors, "run", run_id, f"Tokens for run {run_id} are malformed.")
        return None, "malformed"
    cleaned = {}
    for key in ("input", "output", "total"):
        item = value.get(key)
        if item is None:
            cleaned[key] = None
        elif whole_number(item):
            cleaned[key] = item
        else:
            add_error(errors, "run", run_id, f"Tokens for run {run_id} are malformed.")
            return None, "malformed"
    if all(item is None for item in cleaned.values()):
        return cleaned, "unknown"
    return cleaned, "present"


def clean_availability(value, errors, run_id):
    if value is None:
        return "missing", True
    if value in ("verified", "unverified", "missing"):
        return value, True
    add_error(errors, "run", run_id, f"Skill availability for run {run_id} is malformed.")
    return "malformed", False


def case_subject(case):
    return {
        "title": case["title"],
        "prompt": case["prompt"],
        "inputs": case["inputs"],
        "expected": case["expected"],
        "assertions": case["assertions"],
        "provenance": case["provenance"],
    }


def evidence_material(ref, index):
    evidence_id = ref["id"]
    material = {"id": evidence_id, "label": ref.get("label"), "resolved": False}
    located = index.get(evidence_id)
    if not located:
        return material
    root_real, relative = located
    material["path"] = relative
    try:
        target = resolve_contained(root_real, relative)
    except UnicodeError:
        return material
    if target is None:
        return material
    material["target"] = str(target)
    try:
        info = target.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_EVIDENCE_BYTES:
            material["bytes"] = info.st_size
            return material
        data = target.read_bytes()
    except (OSError, UnicodeError):
        return material
    material["resolved"] = True
    material["bytes"] = len(data)
    material["sha256"] = hashlib.sha256(data).hexdigest()
    return material


def hash_run(run, index):
    return {
        "id": run["id"],
        "arm": run["arm"],
        "target": run["target"],
        "model": run["model"],
        "settings": run["settings"],
        "skill_availability": run["skill_availability"],
        "output": run["output"],
        "summary": run["summary"],
        "duration_ms": run["duration_ms"],
        "tokens": run["tokens"],
        "cost": run["cost"],
        "evidence": [evidence_material(ref, index) for ref in run["evidence"]],
    }


def same_file(left, right):
    try:
        if os.path.exists(left) and os.path.exists(right) and os.path.samefile(left, right):
            return True
    except OSError:
        pass
    try:
        return os.path.realpath(left) == os.path.realpath(right)
    except OSError:
        return False


def path_overlaps(candidate, protected):
    return any(same_file(candidate, item) for item in protected)


def spelling_key(path):
    # Portable spelling key for configured paths. It is not file identity.
    raw = os.fspath(path)
    try:
        text = os.path.realpath(raw)
    except (OSError, UnicodeError, ValueError):
        text = os.path.normpath(raw)
    try:
        text = unicodedata.normalize("NFC", text)
        return tuple(unicodedata.normalize("NFC", part).casefold() for part in Path(text).parts)
    except (UnicodeError, ValueError):
        return tuple(Path(os.path.normpath(raw)).parts)


def spelling_ambiguous(candidate, others):
    key = spelling_key(candidate)
    for item in others:
        if spelling_key(item) == key and not same_file(candidate, item):
            return True
    return False


def load_review(manifest_path, skill_id=None):
    path = Path(manifest_path)
    errors = []
    model = {
        "fatal": None,
        "manifest_path": path,
        "manifest": None,
        "errors": errors,
        "bindings": [],
        "files": {},
        "listed": [],
        "grades": {},
        "assertions": {},
        "subjects": {},
        "round_id": None,
        "skill_id": skill_id if valid_id(skill_id) else None,
    }
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        model["fatal"] = "Manifest could not be read."
        return model
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        model["fatal"] = "Manifest is malformed JSON."
        return model
    if not isinstance(data, dict):
        model["fatal"] = "Manifest must be a JSON object."
        return model
    if data.get("schema") != SCHEMA or type(data.get("schema")) is not int:
        model["fatal"] = "Manifest schema is not 1."
        return model
    round_info = data.get("round")
    if not isinstance(round_info, dict) or not valid_id(round_info.get("id")):
        model["fatal"] = "Manifest round id is missing or malformed."
        return model
    if not isinstance(data.get("cases"), list) or not isinstance(data.get("triggers"), list):
        model["fatal"] = "Manifest cases and triggers must be lists."
        return model
    model["round_id"] = round_info["id"]
    model["files"], model["listed"] = evidence_index(path, data, errors)
    title, title_ok = optional_string(data.get("title"))
    if not title_ok:
        add_error(errors, "manifest", None, "Title is malformed.")
        title = None
    skill = data.get("skill") if isinstance(data.get("skill"), dict) else {}
    if not isinstance(data.get("skill"), dict):
        add_error(errors, "manifest", None, "Skill is malformed.")
    skill_name, name_ok = optional_string(skill.get("name"))
    skill_revision, revision_ok = optional_string(skill.get("revision"))
    if not name_ok or not revision_ok:
        add_error(errors, "manifest", None, "Skill name or revision is malformed.")
        skill_name = skill_name if name_ok else None
        skill_revision = skill_revision if revision_ok else None
    if model["skill_id"] is None and valid_id(skill_name):
        model["skill_id"] = skill_name
    if valid_id(skill_id) and skill_name != skill_id:
        model["fatal"] = f"Skill {skill_id} does not match the manifest skill name."
        model["files"] = {}
        model["bindings"] = []
        return model
    frozen = round_info.get("frozen")
    if type(frozen) is not bool:
        add_error(errors, "manifest", model["round_id"], "Round frozen flag is malformed.")
        frozen = False
    note, note_ok = optional_string(round_info.get("note"))
    if not note_ok:
        add_error(errors, "manifest", model["round_id"], "Round note is malformed.")
        note = None
    display = {
        "schema": SCHEMA,
        "title": title,
        "skill": {"name": skill_name, "revision": skill_revision},
        "round": {"id": model["round_id"], "frozen": frozen, "note": note},
        "cases": [],
        "triggers": [],
    }
    seen_subjects = set()
    for index, case in enumerate(data["cases"]):
        cleaned = clean_case(case, index, errors, model, seen_subjects)
        if cleaned is not None:
            display["cases"].append(cleaned)
    for index, trigger in enumerate(data["triggers"]):
        cleaned = clean_trigger(trigger, index, errors, model, seen_subjects)
        if cleaned is not None:
            display["triggers"].append(cleaned)
    model["manifest"] = display
    return model


def clean_case(case, index, errors, model, seen_subjects):
    if not isinstance(case, dict) or not valid_id(case.get("id")):
        add_error(errors, "manifest", None, f"Case {index + 1} has a malformed id and was omitted.")
        return None
    case_id = case["id"]
    if case_id in seen_subjects:
        add_error(errors, "case", case_id, "Case id is duplicated and the later case was omitted.")
        return None
    seen_subjects.add(case_id)
    title, title_ok = optional_string(case.get("title"))
    prompt, prompt_ok = optional_string(case.get("prompt"))
    expected, expected_ok = optional_string(case.get("expected"))
    provenance, provenance_ok = optional_string(case.get("provenance"))
    if not prompt_ok or prompt is None:
        add_error(errors, "case", case_id, "Prompt is missing or malformed.")
        prompt = "" if prompt is None else ""
        prompt_ok = False
    for field, ok in (("title", title_ok), ("expected", expected_ok), ("provenance", provenance_ok)):
        if not ok:
            add_error(errors, "case", case_id, f"Case {field} is malformed.")
    inputs, inputs_ok = clean_inputs(case.get("inputs"), errors, case_id)
    assertions, assertions_ok = clean_case_assertions(case.get("assertions"), errors, case_id)
    runs = []
    runs_by_id = {}
    if case.get("runs") is None:
        raw_runs = []
    elif not isinstance(case.get("runs"), list):
        add_error(errors, "case", case_id, "Runs are malformed.")
        raw_runs = []
    else:
        raw_runs = case["runs"]
    for run in raw_runs:
        cleaned, binding = clean_run(run, errors, case_id)
        if cleaned is None:
            continue
        if cleaned["id"] in runs_by_id:
            add_error(errors, "run", cleaned["id"], "Run id is duplicated and the later run was omitted.")
            continue
        runs.append(cleaned)
        runs_by_id[cleaned["id"]] = (cleaned, binding)
        model["bindings"].append(binding)
    grades = []
    grade_ids = set()
    raw_grades = case.get("grades")
    if raw_grades is None:
        raw_grades = []
    elif not isinstance(raw_grades, list):
        add_error(errors, "case", case_id, "Grades are malformed.")
        raw_grades = []
    display_case = {
        "id": case_id,
        "title": title,
        "prompt": prompt,
        "inputs": inputs,
        "expected": expected,
        "assertions": assertions,
        "provenance": provenance,
        "runs": runs,
        "grades": grades,
    }
    subject_ok = prompt_ok and inputs_ok and assertions_ok and title_ok and expected_ok and provenance_ok
    subject_fp = fingerprint({
        "v": 1,
        "kind": "subject",
        "skill_id": model["skill_id"],
        "round_id": model["round_id"],
        "subject_id": case_id,
        "subject_type": "case",
        "subject": case_subject(display_case),
    }) if subject_ok else None
    remember_subject(model, case_id, subject_fp)
    for grade in raw_grades:
        cleaned, binding, record = clean_grade(grade, errors, model, display_case, runs_by_id, grade_ids)
        if cleaned is None:
            continue
        grades.append(cleaned)
        model["bindings"].append(binding)
        model["grades"][(case_id, cleaned["id"])] = record
        required = {item["id"] for item in assertions}
        ids = [item["assertion_id"] for item in cleaned["assertions"]]
        for assertion in cleaned["assertions"]:
            assertion_id = assertion["assertion_id"]
            if not record["usable"] or assertion_id not in required or ids.count(assertion_id) != 1:
                continue
            assertion_fp = fingerprint({"grade": record["fingerprint"], "assertion_id": assertion_id})
            model["assertions"][(case_id, cleaned["id"], assertion_id)] = {
                "fingerprint": assertion_fp, "usable": True,
            }
            model["bindings"].append({
                "record_type": "assertion", "subject_id": case_id,
                "record_id": cleaned["id"], "assertion_id": assertion_id,
                "fingerprint": assertion_fp, "usable": True,
            })
    return display_case


def clean_inputs(value, errors, case_id):
    if value is None:
        return [], True
    if not isinstance(value, list):
        add_error(errors, "case", case_id, "Inputs are malformed.")
        return [], False
    inputs = []
    ok = True
    for item in value:
        if not isinstance(item, dict) or not isinstance(item.get("label"), str) or not isinstance(item.get("text"), str):
            add_error(errors, "case", case_id, "An input is malformed.")
            ok = False
            continue
        inputs.append({"label": item["label"], "text": item["text"]})
    return inputs, ok


def clean_case_assertions(value, errors, case_id):
    if value is None:
        return [], True
    if not isinstance(value, list):
        add_error(errors, "case", case_id, "Assertions are malformed.")
        return [], False
    assertions = []
    ok = True
    for item in value:
        if not isinstance(item, dict) or not valid_id(item.get("id")) or not isinstance(item.get("text"), str):
            add_error(errors, "case", case_id, "An assertion is malformed.")
            ok = False
            continue
        if item.get("check") not in ("deterministic", "judgment"):
            add_error(errors, "case", case_id, "An assertion check is malformed.")
            ok = False
            continue
        assertions.append({"id": item["id"], "text": item["text"], "check": item["check"]})
    return assertions, ok


def clean_run(run, errors, case_id):
    if not isinstance(run, dict) or not valid_id(run.get("id")):
        add_error(errors, "case", case_id, "A run has a malformed id and was omitted.")
        return None, None
    run_id = run["id"]
    usable = True
    arm = run.get("arm")
    if arm not in ("with_skill", "without_skill"):
        add_error(errors, "run", run_id, f"Arm for run {run_id} is malformed.")
        arm = None
        usable = False
    target, target_ok = optional_string(run.get("target"))
    if not target_ok or target is None:
        add_error(errors, "run", run_id, f"Target for run {run_id} is missing or malformed.")
        target = None
        usable = False
    model_name, model_ok = optional_string(run.get("model"))
    settings, settings_ok = optional_string(run.get("settings"))
    summary, summary_ok = optional_string(run.get("summary"))
    output, output_ok = optional_string(run.get("output"))
    for field, ok in (("model", model_ok), ("settings", settings_ok), ("summary", summary_ok), ("output", output_ok)):
        if not ok:
            add_error(errors, "run", run_id, f"{field} for run {run_id} is malformed.")
    duration, duration_state = clean_duration(run.get("duration_ms"), errors, run_id)
    tokens, tokens_state = clean_tokens(run.get("tokens"), errors, run_id)
    cost, cost_state = clean_cost(run.get("cost"), errors, run_id)
    availability, availability_ok = clean_availability(run.get("skill_availability"), errors, run_id)
    evidence, evidence_ok = clean_evidence_refs(run.get("evidence"), errors, "run", run_id)
    if not (evidence_ok and model_ok and settings_ok and summary_ok and output_ok):
        usable = False
    cleaned = {
        "id": run_id,
        "target": target,
        "arm": arm,
        "model": model_name,
        "settings": settings,
        "skill_availability": None if availability == "malformed" else availability,
        "output": output,
        "summary": summary,
        "duration_ms": duration,
        "tokens": tokens,
        "cost": cost,
        "evidence": evidence,
    }
    binding = {
        "record_type": "run",
        "subject_id": case_id,
        "record_id": run_id,
        "arm": arm,
        "cost_state": cost_state,
        "duration_state": duration_state,
        "tokens_state": tokens_state,
        "skill_availability": availability,
        "usable": usable,
    }
    return cleaned, binding


def clean_grade(grade, errors, model, display_case, runs_by_id, grade_ids):
    case_id = display_case["id"]
    if not isinstance(grade, dict) or not valid_id(grade.get("id")):
        add_error(errors, "case", case_id, "A grade has a malformed id and was omitted.")
        return None, None, None
    grade_id = grade["id"]
    if grade_id in grade_ids:
        add_error(errors, "grade", grade_id, "Grade id is duplicated and the later grade was omitted.")
        return None, None, None
    grade_ids.add(grade_id)
    usable = True
    grader, grader_ok = optional_string(grade.get("grader"))
    if not grader_ok or grader is None:
        add_error(errors, "grade", grade_id, f"Grade {grade_id} grader is missing or malformed.")
        grader = None
        usable = False
    target, target_ok = optional_string(grade.get("target"))
    summary, summary_ok = optional_string(grade.get("summary"))
    if not target_ok or not summary_ok:
        add_error(errors, "grade", grade_id, f"Grade {grade_id} target or summary is malformed.")
        usable = False
    verdict = grade.get("verdict")
    if verdict not in ("pass", "fail", "mixed", None):
        add_error(errors, "grade", grade_id, f"Grade {grade_id} verdict is malformed.")
        verdict = None
        usable = False
    run_ids = grade.get("run_ids")
    if not isinstance(run_ids, list) or not run_ids or any(not valid_id(item) for item in run_ids) or len(set(run_ids)) != len(run_ids):
        add_error(errors, "grade", grade_id, f"Grade {grade_id} run_ids are malformed.")
        run_ids = []
        usable = False
    hashed_runs = []
    for run_id in run_ids:
        paired = runs_by_id.get(run_id)
        if paired is None or not paired[1]["usable"]:
            add_error(errors, "grade", grade_id, f"Grade {grade_id} references a missing or unusable run.")
            usable = False
            continue
        hashed_runs.append(hash_run(paired[0], model["files"]))
    assertions, assertions_ok = clean_grade_assertions(grade.get("assertions"), errors, grade_id)
    if not assertions_ok:
        usable = False
    evidence, evidence_ok = clean_evidence_refs(grade.get("evidence"), errors, "grade", grade_id)
    if not evidence_ok:
        usable = False
    confirmed, evidence_state, consistency = grade_evidence_state(
        verdict, assertions, evidence, model["files"], display_case["assertions"])
    cleaned = {
        "id": grade_id,
        "grader": grader,
        "target": target,
        "run_ids": run_ids,
        "verdict": verdict,
        "assertions": assertions,
        "summary": summary,
        "evidence": evidence,
    }
    grade_fp = None
    if usable and model["subjects"][case_id]["fingerprint"] is not None:
        grade_fp = fingerprint({
            "v": 1,
            "kind": "grade",
            "skill_id": model["skill_id"],
            "round_id": model["round_id"],
            "subject_id": case_id,
            "grade_id": grade_id,
            "subject": case_subject(display_case),
            "grade": cleaned,
            "grade_evidence": [evidence_material(ref, model["files"]) for ref in evidence],
            "runs": sorted(hashed_runs, key=lambda item: item["id"]),
        })
    else:
        usable = False
    binding = {
        "record_type": "grade",
        "subject_id": case_id,
        "record_id": grade_id,
        "run_ids": run_ids,
        "fingerprint": grade_fp,
        "usable": usable and grade_fp is not None,
        "evidence_state": evidence_state,
        "confirmed": confirmed if grade_fp is not None else False,
        "consistency": consistency,
        "verdict_claim": verdict,
    }
    return cleaned, binding, {"fingerprint": grade_fp, "usable": binding["usable"]}


def clean_grade_assertions(value, errors, grade_id):
    if not isinstance(value, list):
        add_error(errors, "grade", grade_id, f"Grade {grade_id} assertions are malformed.")
        return [], False
    assertions = []
    ok = True
    for item in value:
        if not isinstance(item, dict) or not valid_id(item.get("assertion_id")):
            add_error(errors, "grade", grade_id, f"Grade {grade_id} has a malformed assertion.")
            ok = False
            continue
        if item.get("result") not in ("pass", "fail", "unknown"):
            add_error(errors, "grade", grade_id, f"Grade {grade_id} has a malformed assertion result.")
            ok = False
            continue
        evidence, evidence_ok = optional_string(item.get("evidence"))
        if not evidence_ok:
            add_error(errors, "grade", grade_id, f"Grade {grade_id} has malformed assertion evidence.")
            ok = False
            continue
        assertions.append({"assertion_id": item["assertion_id"], "result": item["result"], "evidence": evidence})
    return assertions, ok


def assertion_coverage(case_assertions, grade_assertions):
    required = [item["id"] for item in case_assertions]
    graded = [item["assertion_id"] for item in grade_assertions]
    return bool(required) and len(graded) == len(set(graded)) == len(required) and set(graded) == set(required)


def grade_evidence_state(verdict, assertions, evidence, files, case_assertions):
    have_text = bool(assertions) and all(
        isinstance(item["evidence"], str) and item["evidence"].strip() != "" for item in assertions)
    known = bool(assertions) and all(item["result"] in ("pass", "fail") for item in assertions)
    if verdict == "pass":
        supports = known and all(item["result"] == "pass" for item in assertions)
    elif verdict == "fail":
        supports = known and any(item["result"] == "fail" for item in assertions)
    elif verdict == "mixed":
        results = {item["result"] for item in assertions}
        supports = known and "pass" in results and "fail" in results
    else:
        supports = False
    present = have_text and refs_resolve(evidence, files)
    state = "present" if present else "missing"
    if not assertion_coverage(case_assertions, assertions):
        return False, state, "incomplete"
    if known and verdict in ("pass", "fail", "mixed") and not supports:
        return False, state, "inconsistent"
    if supports and verdict in ("pass", "fail") and present:
        return True, "present", "consistent"
    return False, state, "incomplete"


def clean_trigger(trigger, index, errors, model, seen_subjects):
    if not isinstance(trigger, dict) or not valid_id(trigger.get("id")):
        add_error(errors, "manifest", None, f"Trigger {index + 1} has a malformed id and was omitted.")
        return None
    trigger_id = trigger["id"]
    if trigger_id in seen_subjects:
        add_error(errors, "trigger", trigger_id, "Trigger id is duplicated and the later trigger was omitted.")
        return None
    seen_subjects.add(trigger_id)
    query, query_ok = optional_string(trigger.get("query"))
    if not query_ok or query is None:
        add_error(errors, "trigger", trigger_id, "Trigger query is missing or malformed.")
        query = ""
        query_ok = False
    expected = trigger.get("expected")
    if expected not in ("trigger", "no_trigger"):
        add_error(errors, "trigger", trigger_id, "Trigger expectation is malformed.")
        expected = None
    note, note_ok = optional_string(trigger.get("note"))
    if not note_ok:
        add_error(errors, "trigger", trigger_id, "Trigger note is malformed.")
        note = None
    display = {"id": trigger_id, "query": query, "expected": expected, "note": note, "observations": []}
    subject_ok = query_ok and note_ok and expected in ("trigger", "no_trigger")
    remember_subject(model, trigger_id, fingerprint({
        "v": 1,
        "kind": "subject",
        "skill_id": model["skill_id"],
        "round_id": model["round_id"],
        "subject_id": trigger_id,
        "subject_type": "trigger",
        "subject": {"query": query, "expected": expected, "note": note},
    }) if subject_ok else None)
    raw = trigger.get("observations")
    if raw is None:
        raw = []
    elif not isinstance(raw, list):
        add_error(errors, "trigger", trigger_id, "Observations are malformed.")
        raw = []
    seen = set()
    for observation in raw:
        cleaned, binding, record = clean_observation(observation, errors, model, display, seen)
        if cleaned is None:
            continue
        display["observations"].append(cleaned)
        model["bindings"].append(binding)
        model["grades"][(trigger_id, cleaned["id"])] = record
    return display


def selection_label(role, used):
    if role == "training":
        return "training"
    if role == "validation" and used is True:
        return "validation_used_for_selection"
    if role == "validation":
        return "validation"
    if role == "fresh" and used is True:
        return "fresh_marked_used_for_selection"
    if role == "fresh":
        return "fresh"
    return None


def clean_observation(observation, errors, model, trigger, seen):
    trigger_id = trigger["id"]
    if not isinstance(observation, dict) or not valid_id(observation.get("id")):
        add_error(errors, "trigger", trigger_id, "An observation has a malformed id and was omitted.")
        return None, None, None
    observation_id = observation["id"]
    if observation_id in seen:
        add_error(errors, "observation", observation_id, "Observation id is duplicated and the later observation was omitted.")
        return None, None, None
    seen.add(observation_id)
    usable = True
    target, target_ok = optional_string(observation.get("target"))
    if not target_ok or target is None:
        add_error(errors, "observation", observation_id, f"Observation {observation_id} target is missing or malformed.")
        target = None
        usable = False
    description, description_ok = optional_string(observation.get("description_revision"))
    if not description_ok:
        add_error(errors, "observation", observation_id, f"Observation {observation_id} description revision is malformed.")
        description = None
        usable = False
    role = observation.get("role")
    if role not in ("training", "validation", "fresh"):
        add_error(errors, "observation", observation_id, f"Observation {observation_id} role is malformed.")
        role = None
        usable = False
    used = observation.get("used_for_selection")
    if type(used) is not bool:
        add_error(errors, "observation", observation_id, f"Observation {observation_id} used_for_selection is malformed.")
        used = None
        usable = False
    observed = observation.get("observed")
    if observed not in ("loaded", "not_loaded", "unverified"):
        add_error(errors, "observation", observation_id, f"Observation {observation_id} observed value is malformed.")
        observed = None
        usable = False
    basis = observation.get("basis")
    if basis not in ("native", "listing_proxy"):
        add_error(errors, "observation", observation_id, f"Observation {observation_id} basis is malformed.")
        basis = None
        usable = False
    summary, summary_ok = optional_string(observation.get("summary"))
    if not summary_ok:
        add_error(errors, "observation", observation_id, f"Observation {observation_id} summary is malformed.")
        summary = None
        usable = False
    evidence, evidence_ok = clean_evidence_refs(observation.get("evidence"), errors, "observation", observation_id)
    if not evidence_ok:
        usable = False
    cleaned = {
        "id": observation_id,
        "target": target,
        "description_revision": description,
        "role": role,
        "used_for_selection": used,
        "observed": observed,
        "basis": basis,
        "summary": summary,
        "evidence": evidence,
    }
    materials = [evidence_material(ref, model["files"]) for ref in evidence]
    has_proof = bool(materials) and all(item["resolved"] for item in materials)
    if has_proof and basis == "native" and observed == "loaded":
        proof = "recorded_trigger"
    elif has_proof and basis == "native" and observed == "not_loaded":
        proof = "recorded_non_trigger"
    else:
        proof = "unverified"
    obs_fp = None
    if usable and model["subjects"][trigger_id]["fingerprint"] is not None:
        hashed_observation = dict(cleaned)
        hashed_observation["evidence"] = materials
        obs_fp = fingerprint({
            "v": 1,
            "kind": "observation",
            "skill_id": model["skill_id"],
            "round_id": model["round_id"],
            "subject_id": trigger_id,
            "grade_id": observation_id,
            "subject": {"query": trigger["query"], "expected": trigger["expected"], "note": trigger["note"]},
            "observation": hashed_observation,
        })
    else:
        usable = False
        proof = "unverified"
    binding = {
        "record_type": "observation",
        "subject_id": trigger_id,
        "record_id": observation_id,
        "fingerprint": obs_fp,
        "usable": usable and obs_fp is not None,
        "proof": proof,
        "basis": basis,
        "observed": observed,
        "role": role,
        "used_for_selection": used,
        "selection": selection_label(role, used),
        "description_revision": description,
        "target": target,
    }
    return cleaned, binding, {"fingerprint": obs_fp, "usable": binding["usable"]}


def feedback_item_ok(item):
    if not isinstance(item, dict):
        return False
    if not valid_id(item.get("round_id")) or not valid_id(item.get("subject_id")):
        return False
    if item.get("grade_id") is not None and not valid_id(item.get("grade_id")):
        return False
    if item.get("assertion_id") is not None and (
        not valid_id(item["assertion_id"]) or item.get("grade_id") is None
    ):
        return False
    if item.get("judgment") not in (None, "agree", "disagree"):
        return False
    if not isinstance(item.get("note"), str) or len(item["note"]) > MAX_NOTE:
        return False
    if type(item.get("revision")) is not int or item["revision"] < 1:
        return False
    if not isinstance(item.get("saved_at"), str) or not isinstance(item.get("fingerprint"), str):
        return False
    return set(item) - {"assertion_id"} == {"round_id", "subject_id", "grade_id", "judgment", "note", "revision", "saved_at", "fingerprint"}


def load_feedback(path):
    file_path = Path(path)
    if not file_path.exists():
        return {"items": []}, None
    if file_path.is_symlink():
        return None, "Feedback path is a symlink and was not changed."
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None, "Feedback file is malformed and was not changed."
    if not isinstance(data, dict) or set(data) != {"items"} or not isinstance(data["items"], list):
        return None, "Feedback file is malformed and was not changed."
    if any(not feedback_item_ok(item) for item in data["items"]):
        return None, "Feedback file is malformed and was not changed."
    return data, None


def annotate_feedback(model, feedback):
    if feedback is None:
        return []
    items = []
    for item in feedback["items"]:
        current = None
        if model["fatal"] is None and item["round_id"] == model["round_id"]:
            if item.get("assertion_id") is not None:
                record = model["assertions"].get((item["subject_id"], item["grade_id"], item["assertion_id"]))
                current = record["fingerprint"] if record else None
            elif item["grade_id"] is None:
                subject = model["subjects"].get(item["subject_id"])
                current = subject["fingerprint"] if subject else None
            else:
                record = model["grades"].get((item["subject_id"], item["grade_id"]))
                current = record["fingerprint"] if record else None
        copy = dict(item)
        copy["binding"] = "current" if current and item["fingerprint"] == current else "earlier"
        items.append(copy)
    return items


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def atomic_write(path, payload):
    file_path = Path(path)
    if file_path.is_symlink():
        raise OSError("Feedback path is a symlink and was not changed.")
    parent = file_path.parent
    if parent.is_symlink() or not parent.is_dir():
        raise OSError("Feedback directory is not available.")
    text = dump_json(payload, indent=2) + "\n"
    fd, name = tempfile.mkstemp(dir=parent, prefix=".feedback-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, file_path)
    except Exception:
        try:
            os.unlink(name)
        except OSError:
            pass
        raise
    if file_path.is_symlink():
        raise OSError("Feedback path is a symlink and was not changed.")


def matching_item(items, round_id, subject_id, grade_id, grade_fp, assertion_id=None):
    for item in items:
        if item["round_id"] == round_id and item["subject_id"] == subject_id and item["grade_id"] == grade_id and item.get("assertion_id") == assertion_id and item["fingerprint"] == grade_fp:
            return item
    return None


def apply_feedback(model, form, path, protected=None):
    if model["fatal"] is not None:
        raise FeedbackError(400, "Not saved: manifest is not reviewable.")
    if protected is None:
        protected = [model["manifest_path"], *model.get("listed", [])]
    if path_overlaps(path, protected):
        raise FeedbackError(400, "Not saved: feedback path overlaps a review input.")
    for key in ("round_id", "subject_id", "grade_id", "judgment", "note", "base_revision", "fingerprint"):
        if key not in form:
            raise FeedbackError(400, "Not saved: feedback body is missing a field.")
    if not valid_id(form["round_id"]) or form["round_id"] != model["round_id"]:
        raise FeedbackError(400, "Not saved: round_id does not match the manifest round.")
    if not valid_id(form["subject_id"]) or form["subject_id"] not in model["subjects"]:
        raise FeedbackError(400, "Not saved: subject_id is not in this round.")
    grade_id = form["grade_id"]
    if grade_id is not None and not valid_id(grade_id):
        raise FeedbackError(400, "Not saved: grade_id is malformed.")
    assertion_id = form.get("assertion_id")
    if assertion_id is not None and (not valid_id(assertion_id) or grade_id is None):
        raise FeedbackError(400, "Not saved: assertion_id requires a valid grade and assertion.")
    judgment = form["judgment"]
    if judgment not in (None, "agree", "disagree"):
        raise FeedbackError(400, "Not saved: judgment is malformed.")
    if not isinstance(form["note"], str):
        raise FeedbackError(400, "Not saved: note is malformed.")
    if len(form["note"]) > MAX_NOTE:
        raise FeedbackError(400, "Not saved: note exceeds 4000 characters.")
    if type(form["base_revision"]) is not int or form["base_revision"] < 0:
        raise FeedbackError(400, "Not saved: base_revision is malformed.")
    if assertion_id is not None:
        record = model["assertions"].get((form["subject_id"], grade_id, assertion_id))
        if record is None or not record["usable"]:
            raise FeedbackError(400, "Not saved: assertion_id is not a usable check on this grade.")
        grade_fp = record["fingerprint"]
    elif grade_id is None:
        if judgment is not None:
            raise FeedbackError(400, "Not saved: agreement requires a grade or observation id.")
        grade_fp = model["subjects"][form["subject_id"]]["fingerprint"]
        if grade_fp is None:
            raise FeedbackError(400, "Not saved: subject is not reviewable.")
    else:
        record = model["grades"].get((form["subject_id"], grade_id))
        if record is None or not record["usable"] or record["fingerprint"] is None:
            raise FeedbackError(400, "Not saved: grade_id is not a usable grade or observation on this subject.")
        grade_fp = record["fingerprint"]
    supplied = form["fingerprint"]
    if not isinstance(supplied, str) or not supplied.startswith("sha256:"):
        raise FeedbackError(400, "Not saved: fingerprint is missing or malformed.")
    if supplied != grade_fp:
        raise FeedbackError(409, "Not saved: the evidence on screen has changed. Reload before saving.")
    feedback, error = load_feedback(path)
    if error is not None:
        raise FeedbackError(500, "Not saved: " + error[0].lower() + error[1:])
    current = matching_item(feedback["items"], form["round_id"], form["subject_id"], grade_id, grade_fp, assertion_id)
    base = form["base_revision"]
    if current is None:
        if base != 0:
            raise FeedbackError(409, "Not saved: this evidence has no feedback at that revision.")
        saved = {
            "round_id": form["round_id"],
            "subject_id": form["subject_id"],
            "grade_id": grade_id,
            "judgment": judgment,
            "note": form["note"],
            "revision": 1,
            "saved_at": now_utc(),
            "fingerprint": grade_fp,
        }
        if assertion_id is not None:
            saved["assertion_id"] = assertion_id
        feedback["items"].append(saved)
    else:
        if current["revision"] != base:
            prior = dict(current)
            prior["binding"] = "current"
            raise FeedbackError(409, "Not saved: a newer edit exists for this feedback.", prior)
        current["judgment"] = judgment
        current["note"] = form["note"]
        current["revision"] = base + 1
        current["saved_at"] = now_utc()
        saved = current
    try:
        atomic_write(path, feedback)
    except OSError as error:
        message = str(error)
        if not message.startswith("Not saved:"):
            message = "Not saved: " + message[0].lower() + message[1:]
        raise FeedbackError(500, message)
    body = dict(saved)
    body["binding"] = "current"
    return body


class SkillSource:
    def __init__(self, manifest_path, feedback_path, skill_id=None):
        self.manifest_path = Path(manifest_path)
        self.feedback_path = Path(feedback_path)
        self.skill_id = skill_id


def configured_path(base, value):
    if not isinstance(value, str) or value == "" or "\x00" in value:
        raise ConfigError("A skill entry is malformed.")
    path = Path(value)
    if not path.is_absolute():
        path = base / path
    return path


def load_index(index_path):
    path = Path(index_path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise ConfigError("Index is missing or malformed JSON.")
    if not isinstance(data, dict) or set(data) != {"repository", "skills"}:
        raise ConfigError("Index must contain repository and skills.")
    repository = data["repository"]
    entries = data["skills"]
    if not valid_id(repository):
        raise ConfigError("Index repository is missing or malformed.")
    if not isinstance(entries, list) or not entries:
        raise ConfigError("Index skills must be a non-empty list.")
    sources = []
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"id", "manifest", "feedback"}:
            raise ConfigError("A skill entry is malformed.")
        skill_id = entry["id"]
        if not valid_id(skill_id):
            raise ConfigError("A skill id is missing or malformed.")
        if skill_id in seen:
            raise ConfigError(f"Skill id {skill_id} is duplicated.")
        seen.add(skill_id)
        sources.append(SkillSource(
            configured_path(path.parent, entry["manifest"]),
            configured_path(path.parent, entry["feedback"]),
            skill_id,
        ))
    models = []
    for source in sources:
        model = load_review(source.manifest_path, skill_id=source.skill_id)
        if model["fatal"] is not None:
            message = model["fatal"]
            if "does not match the manifest skill name" not in message:
                message = f"Skill {source.skill_id} manifest is not usable."
            raise ConfigError(message)
        models.append(model)
    protected = [path]
    for source, model in zip(sources, models):
        protected.append(source.manifest_path)
        protected.extend(model.get("listed") or [])
    for index, source in enumerate(sources):
        others = [other.feedback_path for other_index, other in enumerate(sources) if other_index != index]
        if path_overlaps(source.feedback_path, others):
            raise ConfigError("Two skills share a feedback destination.")
        if spelling_ambiguous(source.feedback_path, others):
            raise ConfigError("Two skills have ambiguous feedback paths.")
        if path_overlaps(source.feedback_path, protected):
            raise ConfigError("A feedback path overlaps a review input.")
        if spelling_ambiguous(source.feedback_path, protected):
            raise ConfigError("A feedback path is ambiguous with a review input.")
    return repository, sources


class ReviewServer(ThreadingHTTPServer):
    allow_reuse_address = False
    daemon_threads = True

    def server_bind(self):
        # HTTPServer.server_bind resolves the host with getfqdn. That lookup
        # can stall a loopback bind for a long time, so keep the name literal.
        socketserver.TCPServer.server_bind(self)
        self.server_name = "127.0.0.1"
        self.server_port = self.server_address[1]

    def __init__(self, address, sources, repository=None, index_path=None, viewer_path=None):
        super().__init__(address, ReviewHandler)
        self.sources = list(sources)
        self.repository = repository
        self.index_path = None if index_path is None else Path(index_path)
        self.viewer_path = None if viewer_path is None else Path(viewer_path)
        self.feedback_lock = threading.Lock()
        port = self.server_address[1]
        self.allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        self.allowed_origins = {f"http://127.0.0.1:{port}", f"http://localhost:{port}"}


class ReviewHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def version_string(self):
        return "EvalReview/1.0"

    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        self.dispatch("GET")

    def do_POST(self):
        self.dispatch("POST")

    def send_error(self, code, message=None, explain=None):
        self.respond(code, {"error": message or "Not found."}, "application/json; charset=utf-8", DATA_CSP)

    def dispatch(self, method):
        if not self.host_allowed() or self.framing_rejected():
            self.respond(403, {"error": "Rejected."}, "application/json; charset=utf-8", DATA_CSP)
            return
        parts = self.segments()
        try:
            if parts == [] and method == "GET":
                self.serve_viewer()
            elif parts == ["api", "skills"] and method == "GET":
                self.serve_skills()
            elif parts == ["api", "review"] and method == "GET":
                self.serve_review()
            elif parts == ["api", "feedback"] and method == "POST":
                self.serve_feedback()
            elif parts is not None and len(parts) == 2 and parts[0] == "evidence" and method == "GET":
                self.serve_evidence(parts[1])
            elif method not in ("GET", "POST"):
                self.respond(405, {"error": "Method not allowed."}, "application/json; charset=utf-8", DATA_CSP)
            else:
                self.respond(404, {"error": "Not found."}, "application/json; charset=utf-8", DATA_CSP)
        except SelectorError as error:
            message = "Rejected." if error.status == 400 else "Not found."
            self.respond(error.status, {"error": message}, "application/json; charset=utf-8", DATA_CSP)
        except FeedbackError as error:
            body = {"error": str(error)}
            if error.status == 409:
                body["item"] = error.item
            self.respond(error.status, body, "application/json; charset=utf-8", DATA_CSP)
        except Exception:
            self.respond(500, {"error": "The review could not be loaded."}, "application/json; charset=utf-8", DATA_CSP)

    def header_values(self, name):
        values = self.headers.get_all(name)
        return values or []

    def one_header(self, name):
        values = self.header_values(name)
        if len(values) != 1:
            return None
        value = values[0]
        if any(char in value for char in " ,\t\r\n"):
            return None
        return value

    def host_allowed(self):
        host = self.one_header("Host")
        if host is None:
            return False
        return host.lower() in self.server.allowed_hosts

    def origin_allowed(self):
        origin = self.one_header("Origin")
        if origin is None:
            return False
        return origin.lower() in self.server.allowed_origins

    def framing_rejected(self):
        if self.header_values("Transfer-Encoding"):
            return True
        return len(self.header_values("Content-Length")) > 1

    def segments(self):
        raw = urllib.parse.urlsplit(self.path).path
        if len(raw) > MAX_PATH:
            return None
        decoded = urllib.parse.unquote(raw)
        if "\\" in decoded or "\x00" in decoded:
            return None
        parts = [part for part in decoded.split("/") if part != ""]
        if any(part in (".", "..") for part in parts):
            return None
        return parts

    def read_body(self):
        lengths = self.header_values("Content-Length")
        if len(lengths) != 1 or not lengths[0].isdigit():
            raise FeedbackError(400, "Not saved: Content-Length is required.")
        length = lengths[0]
        size = int(length)
        if size > MAX_BODY:
            raise FeedbackError(413, "Not saved: request body exceeds 65536 bytes.")
        data = self.rfile.read(size)
        if len(data) != size:
            raise FeedbackError(400, "Not saved: request body was truncated.")
        return data

    def respond(self, status, payload, content_type, policy):
        if isinstance(payload, bytes):
            data = payload
        else:
            data = dump_json(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", policy)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(data)

    def viewer_bytes(self):
        configured = self.server.viewer_path
        if configured is None:
            path = TOOL_DIR / "viewer.html"
            if path.is_symlink():
                return None
            try:
                real = path.resolve(strict=True)
                real.relative_to(TOOL_DIR)
            except (OSError, ValueError):
                return None
            if not stat.S_ISREG(real.stat().st_mode):
                return None
            return real.read_bytes()
        if configured.is_symlink() or not configured.is_file():
            return None
        try:
            if not stat.S_ISREG(configured.stat().st_mode):
                return None
        except OSError:
            return None
        return configured.read_bytes()

    def serve_viewer(self):
        data = self.viewer_bytes()
        if data is None:
            self.respond(404, {"error": "viewer.html is not present"}, "application/json; charset=utf-8", DATA_CSP)
            return
        self.respond(200, data, "text/html; charset=utf-8", HTML_CSP)

    def query_skill(self):
        query = urllib.parse.urlsplit(self.path).query
        values = [value for key, value in urllib.parse.parse_qsl(query, keep_blank_values=True) if key == "skill"]
        if not values:
            return None
        if len(values) != 1 or not valid_id(values[0]):
            raise SelectorError(400)
        return values[0]

    def selected_source(self):
        selected = self.query_skill()
        sources = self.server.sources
        if sources[0].skill_id is not None:
            if selected is None:
                return sources[0]
            for source in sources:
                if source.skill_id == selected:
                    return source
            raise SelectorError(404)
        source = sources[0]
        if selected is None:
            return source
        model = load_review(source.manifest_path)
        name = None
        if model["manifest"] is not None:
            name = model["manifest"]["skill"]["name"]
        if name == selected:
            return source
        raise SelectorError(404)

    def catalog_entry(self, model):
        name = None
        if model["manifest"] is not None:
            candidate = model["manifest"]["skill"]["name"]
            if valid_id(candidate):
                name = candidate
        if name is None:
            return {"id": "", "name": ""}
        return {"id": name, "name": name}

    def serve_skills(self):
        if self.server.index_path is not None:
            skills = [{"id": source.skill_id, "name": source.skill_id} for source in self.server.sources]
            repository = self.server.repository
        else:
            model = load_review(self.server.sources[0].manifest_path)
            skills = [self.catalog_entry(model)]
            repository = None
        self.respond(200, {
            "repository": repository,
            "skills": skills,
            "default_skill": skills[0]["id"],
        }, "application/json; charset=utf-8", DATA_CSP)

    def destination_guard(self, destination):
        protected = []
        selected = None
        if self.server.index_path is not None:
            protected.append(self.server.index_path)
        for source in self.server.sources:
            model = load_review(source.manifest_path, skill_id=source.skill_id)
            protected.append(source.manifest_path)
            if source is not destination:
                protected.append(source.feedback_path)
            protected.extend(model.get("listed") or [])
            if source is destination:
                selected = model
        return selected, protected

    def serve_review(self):
        source = self.selected_source()
        with self.server.feedback_lock:
            model, protected = self.destination_guard(source)
            if path_overlaps(source.feedback_path, protected):
                feedback, error = None, "Feedback path overlaps a review input."
            else:
                feedback, error = load_feedback(source.feedback_path)
        if model["fatal"] is not None:
            errors = [{"scope": "manifest", "id": None, "message": model["fatal"]}]
            manifest = None
            bindings = []
        else:
            errors = model["errors"]
            manifest = model["manifest"]
            bindings = model["bindings"]
        body = {
            "manifest": manifest,
            "feedback": {"items": annotate_feedback(model, feedback), "error": error},
            "errors": errors,
            "bindings": bindings,
        }
        self.respond(200, body, "application/json; charset=utf-8", DATA_CSP)

    def serve_feedback(self):
        if not self.origin_allowed():
            self.respond(403, {"error": "Rejected."}, "application/json; charset=utf-8", DATA_CSP)
            return
        content_type = self.headers.get("Content-Type", "")
        if content_type.split(";", 1)[0].strip().lower() != "application/json":
            raise FeedbackError(400, "Not saved: Content-Type must be application/json.")
        raw = self.read_body()
        try:
            form = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            raise FeedbackError(400, "Not saved: body is not JSON.")
        if not isinstance(form, dict):
            raise FeedbackError(400, "Not saved: body must be a JSON object.")
        source = self.selected_source()
        with self.server.feedback_lock:
            # The overlap check and the write share one lock across every skill.
            model, protected = self.destination_guard(source)
            saved = apply_feedback(model, form, source.feedback_path, protected)
        self.respond(200, {"item": saved}, "application/json; charset=utf-8", DATA_CSP)

    def serve_evidence(self, evidence_id):
        source = self.selected_source()
        if not valid_id(evidence_id):
            self.respond(404, {"error": "Not found."}, "application/json; charset=utf-8", DATA_CSP)
            return
        model = load_review(source.manifest_path, skill_id=source.skill_id)
        located = model["files"].get(evidence_id)
        if located is None:
            self.respond(404, {"error": "Not found."}, "application/json; charset=utf-8", DATA_CSP)
            return
        root_real, relative = located
        target = resolve_contained(root_real, relative)
        if target is None:
            self.respond(404, {"error": "Not found."}, "application/json; charset=utf-8", DATA_CSP)
            return
        try:
            info = target.stat()
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_EVIDENCE_BYTES:
                self.respond(404, {"error": "Not found."}, "application/json; charset=utf-8", DATA_CSP)
                return
            data = target.read_bytes()
        except OSError:
            self.respond(404, {"error": "Not found."}, "application/json; charset=utf-8", DATA_CSP)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", DATA_CSP)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Disposition", 'inline; filename="evidence.txt"')
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(data)


def serve(manifest_path, feedback_path, port=0, viewer_path=None):
    source = SkillSource(manifest_path, feedback_path)
    return ReviewServer(("127.0.0.1", port), [source], viewer_path=viewer_path)


def serve_index(index_path, port=0, viewer_path=None):
    repository, sources = load_index(index_path)
    return ReviewServer(("127.0.0.1", port), sources, repository, index_path, viewer_path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Serve local skill-evaluation reviews.")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--feedback", type=Path)
    parser.add_argument("--index", type=Path)
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args(argv)
    if args.port < 0 or args.port > 65535:
        parser.error("port must be from 0 through 65535")
    if args.index is not None and (args.manifest is not None or args.feedback is not None):
        parser.error("--index cannot be combined with --manifest or --feedback")
    try:
        if args.index is not None:
            server = serve_index(args.index, args.port)
        elif args.manifest is not None and args.feedback is not None:
            server = serve(args.manifest, args.feedback, args.port)
        else:
            parser.error("provide --index, or both --manifest and --feedback")
    except ConfigError as error:
        parser.error(str(error))
    print(f"http://127.0.0.1:{server.server_address[1]}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
