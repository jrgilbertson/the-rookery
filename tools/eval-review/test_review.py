import contextlib
import hashlib
import http.client
import io
import json
import os
from pathlib import Path
import shutil
import socket
import sys
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import review


FIXTURE = ROOT / "fixtures" / "manifest.json"
EVIDENCE = ROOT / "fixtures" / "evidence"
ROUND = "2026-09-26-synthetic"


def binding(payload, record_id):
    return next(item for item in payload["bindings"] if item.get("record_id") == record_id)


def case(payload, case_id):
    return next(item for item in payload["manifest"]["cases"] if item["id"] == case_id)


def run_record(payload, run_id):
    for item in payload["manifest"]["cases"]:
        for candidate in item["runs"]:
            if candidate["id"] == run_id:
                return candidate
    raise AssertionError(run_id)


class ReviewHttpTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest_path = self.root / "manifest.json"
        self.feedback_path = self.root / "feedback.json"
        data = json.loads(FIXTURE.read_text())
        data["evidence_root"] = str(EVIDENCE)
        self.manifest_path.write_text(json.dumps(data))
        self.evidence_hashes = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in EVIDENCE.iterdir() if path.is_file()
        }
        self.server = None
        self.port = None
        self.start_default()

    def start_default(self):
        self.server, self.port = self.open_server(self.manifest_path, self.feedback_path)

    def open_server(self, manifest, feedback, viewer=None):
        server = review.serve(manifest, feedback, viewer_path=viewer)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        return server, server.server_address[1]

    def request(self, method, path, body=None, headers=None, port=None):
        port = self.port if port is None else port
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        sent = {"Host": f"127.0.0.1:{port}"}
        if body is not None:
            sent["Content-Type"] = "application/json"
            sent["Origin"] = f"http://127.0.0.1:{port}"
            sent["Content-Length"] = str(len(body))
        if headers:
            sent.update(headers)
        connection.request(method, path, body=body, headers=sent)
        response = connection.getresponse()
        data = response.read()
        header_map = {key: value for key, value in response.getheaders()}
        status = response.status
        connection.close()
        return status, data, header_map

    def review(self, port=None):
        status, data, headers = self.request("GET", "/api/review", port=port)
        self.assertEqual(status, 200, data)
        self.assertIn("application/json", headers["Content-Type"])
        return json.loads(data.decode())

    def binding_record(self, subject_id, grade_id=None, port=None, assertion_id=None):
        payload = self.review(port)
        if grade_id is None:
            matches = [item for item in payload["bindings"]
                       if item.get("record_type") == "subject" and item.get("subject_id") == subject_id]
        else:
            matches = [item for item in payload["bindings"]
                       if item.get("subject_id") == subject_id and item.get("record_id") == grade_id
                       and item.get("assertion_id") == assertion_id]
        self.assertEqual(len(matches), 1, (subject_id, grade_id))
        return matches[0]

    def post(self, payload, headers=None, port=None):
        body = dict(payload)
        if "fingerprint" not in body:
            found = self.binding_record(body["subject_id"], body.get("grade_id"), port,
                                        body.get("assertion_id"))
            fingerprint = found.get("fingerprint")
            body["fingerprint"] = fingerprint if isinstance(fingerprint, str) else "sha256:" + ("0" * 64)
        status, data, response_headers = self.request(
            "POST", "/api/feedback", json.dumps(body).encode(), headers, port)
        return status, json.loads(data.decode()), response_headers

    def feedback(self, **overrides):
        payload = {
            "round_id": ROUND,
            "subject_id": "ask-owner-before-dropping-audit",
            "grade_id": None,
            "judgment": None,
            "note": "",
            "base_revision": 0,
        }
        payload.update(overrides)
        return payload

    def assert_evidence_unchanged(self):
        for path in EVIDENCE.iterdir():
            if path.is_file():
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(digest, self.evidence_hashes[path.name])

    def test_assertion_feedback_is_separate_from_siblings_and_overall_grade(self):
        payload = self.review()
        c = case(payload, "protect-export-boundaries")
        ids = [a["assertion_id"] for a in c["grades"][0]["assertions"]]
        self.assertGreaterEqual(len(ids), 2)
        common = dict(subject_id=c["id"], grade_id=c["grades"][0]["id"])
        original_manifest = self.manifest_path.read_bytes()
        for aid, judgment in [(ids[0], "disagree"), (ids[1], "agree"), (None, "agree")]:
            status, saved, _ = self.post(self.feedback(**common, assertion_id=aid,
                                                      judgment=judgment, note=str(aid)))
            self.assertEqual(status, 200, saved)
        items = self.review()["feedback"]["items"]
        self.assertEqual(len(items), 3)
        self.assertEqual({i.get("assertion_id"): i["judgment"] for i in items},
                         {ids[0]: "disagree", ids[1]: "agree", None: "agree"})
        self.assertTrue(all(i["binding"] == "current" for i in items))
        self.assertEqual(self.manifest_path.read_bytes(), original_manifest)
        self.assert_evidence_unchanged()

    def test_assertion_feedback_rejects_unknown_id_and_stale_evidence(self):
        c = case(self.review(), "protect-export-boundaries")
        grade = c["grades"][0]
        aid = grade["assertions"][0]["assertion_id"]
        common = dict(subject_id=c["id"], grade_id=grade["id"], assertion_id=aid)
        shown = self.binding_record(c["id"], grade["id"], assertion_id=aid)["fingerprint"]
        status, saved, _ = self.post(self.feedback(**common, judgment="disagree", fingerprint=shown))
        self.assertEqual(status, 200, saved)
        before = self.feedback_path.read_bytes()
        status, rejected, _ = self.post(self.feedback(subject_id=c["id"], grade_id=grade["id"],
            assertion_id="not-a-check", judgment="agree", fingerprint=shown))
        self.assertEqual(status, 400, rejected)
        status, rejected, _ = self.post(self.feedback(**common, judgment="agree", fingerprint=shown))
        self.assertEqual(status, 409, rejected)
        self.assertEqual(self.feedback_path.read_bytes(), before)
        data = json.loads(self.manifest_path.read_text())
        next(c for c in data["cases"] if c["id"] == common["subject_id"])["grades"][0]["assertions"][0]["evidence"] += " Changed."
        self.manifest_path.write_text(json.dumps(data))
        self.assertEqual(self.review()["feedback"]["items"][0]["binding"], "earlier")
        status, rejected, _ = self.post(self.feedback(**common, judgment="agree", base_revision=1, fingerprint=shown))
        self.assertEqual(status, 409, rejected)
        self.assertEqual(self.feedback_path.read_bytes(), before)

    def test_prerun_case_accepts_a_note_and_reloads_it(self):
        payload = self.review()
        proposed = case(payload, "ask-owner-before-dropping-audit")
        subject = self.binding_record("ask-owner-before-dropping-audit")
        self.assertEqual(subject["record_type"], "subject")
        self.assertTrue(subject["usable"])
        self.assertTrue(subject["fingerprint"].startswith("sha256:"))
        self.assertEqual(proposed["runs"], [])
        self.assertEqual(proposed["grades"], [])
        self.assertIn("Ask the owner", proposed["prompt"])
        self.assertEqual(proposed["inputs"][0]["label"], "Open question")
        self.assertEqual(proposed["assertions"][0]["id"], "asks-owner")
        note = "The audit waiver is the question to freeze before any run."
        status, body, _ = self.post(self.feedback(note=note))
        self.assertEqual(status, 200)
        self.assertEqual(body["item"]["judgment"], None)
        self.assertEqual(body["item"]["binding"], "current")
        self.assertEqual(body["item"]["revision"], 1)
        self.assertNotIn("item", body["item"])
        stored = json.loads(self.feedback_path.read_text())
        self.assertEqual(stored["items"][0]["note"], note)
        self.assertNotIn("binding", stored["items"][0])
        again = self.review()
        item = again["feedback"]["items"][0]
        self.assertEqual(item["note"], note)
        self.assertEqual(item["binding"], "current")
        self.assertIsNone(item["grade_id"])
        status, rejected, _ = self.post(self.feedback(
            subject_id="ask-owner-before-dropping-audit", judgment="agree", note=note))
        self.assertEqual(status, 400)
        self.assertIn("Not saved", rejected["error"])
        self.assertEqual(json.loads(self.feedback_path.read_text())["items"][0]["judgment"], None)

    def test_agreement_binds_one_grade_and_evidence_bytes_stay_put(self):
        note = "Agree with the protected-boundary grade."
        status, body, _ = self.post(self.feedback(
            subject_id="protect-export-boundaries",
            grade_id="grade-protect-with",
            judgment="agree",
            note=note,
        ))
        self.assertEqual(status, 200)
        self.assertEqual(body["item"]["grade_id"], "grade-protect-with")
        payload = self.review()
        saved = [item for item in payload["feedback"]["items"] if item["grade_id"] == "grade-protect-with"]
        self.assertEqual(saved[0]["judgment"], "agree")
        self.assertEqual(saved[0]["note"], note)
        self.assertEqual(saved[0]["binding"], "current")
        self.assertEqual(
            [item for item in payload["feedback"]["items"] if item["grade_id"] == "grade-protect-without"], [])
        grade = binding(payload, "grade-protect-with")
        self.assertTrue(grade["confirmed"])
        self.assertEqual(grade["evidence_state"], "present")
        self.assertEqual(grade["run_ids"], ["run-protect-with"])
        status, trace, headers = self.request("GET", "/evidence/protect-with-trace")
        self.assertEqual(status, 200)
        self.assertEqual(trace, (EVIDENCE / "protect-with-trace.json").read_bytes())
        self.assertIn("text/plain", headers["Content-Type"])
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("default-src 'none'", headers["Content-Security-Policy"])
        self.assert_evidence_unchanged()
        self.assertEqual(list(self.root.glob(".feedback-*")), [])
        other, other_port = self.open_server(self.manifest_path, self.feedback_path)
        del other
        reopened = self.review(other_port)
        self.assertEqual(reopened["feedback"]["items"][0]["note"], note)
        self.assertEqual(reopened["feedback"]["items"][0]["judgment"], "agree")

    def test_changed_grade_round_and_output_do_not_inherit_agreement(self):
        self.post(self.feedback(
            subject_id="protect-export-boundaries",
            grade_id="grade-protect-with",
            judgment="agree",
            note="agreement-note-for-grade-a",
        ))
        data = json.loads(self.manifest_path.read_text())
        grade = data["cases"][0]["grades"][0]
        self.assertEqual(grade["id"], "grade-protect-with")
        grade["summary"] = "Changed summary must not inherit agreement."
        self.manifest_path.write_text(json.dumps(data))
        payload = self.review()
        earlier = [item for item in payload["feedback"]["items"] if item["grade_id"] == "grade-protect-with"]
        self.assertEqual(len(earlier), 1)
        self.assertEqual(earlier[0]["binding"], "earlier")
        self.assertEqual(earlier[0]["judgment"], "agree")
        status, rejected, _ = self.post(self.feedback(
            subject_id="protect-export-boundaries",
            grade_id="grade-protect-with",
            judgment="agree",
            note="should-not-land",
            base_revision=1,
        ))
        self.assertEqual(status, 409)
        self.assertIn("Not saved", rejected["error"])
        self.assertIsNone(rejected["item"])
        disk = json.loads(self.feedback_path.read_text())
        self.assertEqual(len(disk["items"]), 1)
        self.assertEqual(disk["items"][0]["note"], "agreement-note-for-grade-a")
        data["round"]["id"] = "2026-09-26-synthetic-next"
        data["cases"][0]["grades"][0]["summary"] = "The readout keeps authorization, redaction, the audit event, and the bounded stream."
        self.manifest_path.write_text(json.dumps(data))
        payload = self.review()
        self.assertEqual(payload["feedback"]["items"][0]["binding"], "earlier")
        self.assertEqual(payload["manifest"]["round"]["id"], "2026-09-26-synthetic-next")

    def test_changed_run_output_retires_agreement_for_the_same_grade_id(self):
        self.post(self.feedback(
            subject_id="protect-export-boundaries",
            grade_id="grade-protect-with",
            judgment="disagree",
            note="output-bound-note",
        ))
        data = json.loads(self.manifest_path.read_text())
        data["cases"][0]["runs"][0]["output"] = "A rewritten output under the same run id."
        self.manifest_path.write_text(json.dumps(data))
        payload = self.review()
        item = payload["feedback"]["items"][0]
        self.assertEqual(item["grade_id"], "grade-protect-with")
        self.assertEqual(item["binding"], "earlier")
        self.assertEqual(item["judgment"], "disagree")
        self.assertEqual(json.loads(self.feedback_path.read_text())["items"][0]["note"], "output-bound-note")

    def test_first_save_rejects_a_stale_displayed_fingerprint(self):
        case_shown = self.binding_record("ask-owner-before-dropping-audit")["fingerprint"]
        trigger_shown = self.binding_record("simplify-an-overbuilt-plan")["fingerprint"]
        data = json.loads(self.manifest_path.read_text())
        data["cases"][1]["prompt"] = "The case wording changed before the note was saved."
        data["triggers"][0]["note"] = "The query note changed before the note was saved."
        self.manifest_path.write_text(json.dumps(data))
        status, body, _ = self.post(self.feedback(
            note="typed against the old case", fingerprint=case_shown))
        self.assertEqual(status, 409)
        self.assertIn("Not saved", body["error"])
        self.assertIsNone(body["item"])
        self.assertFalse(self.feedback_path.exists())
        status, body, _ = self.post(self.feedback(
            subject_id="simplify-an-overbuilt-plan",
            note="typed against the old query note",
            fingerprint=trigger_shown,
        ))
        self.assertEqual(status, 409)
        self.assertIn("Not saved", body["error"])
        self.assertIsNone(body["item"])
        self.assertFalse(self.feedback_path.exists())
        status, saved, _ = self.post(self.feedback(note="note for the current wording"))
        self.assertEqual(status, 200)
        self.assertEqual(saved["item"]["note"], "note for the current wording")
        self.assertEqual(saved["item"]["fingerprint"], self.binding_record("ask-owner-before-dropping-audit")["fingerprint"])
        self.assertNotEqual(saved["item"]["fingerprint"], case_shown)

    def test_stale_revision_is_rejected_without_data_loss(self):
        first = "first-tab-note"
        status, _, _ = self.post(self.feedback(note=first))
        self.assertEqual(status, 200)
        status, body, _ = self.post(self.feedback(note="second-tab-note", base_revision=0))
        self.assertEqual(status, 409)
        self.assertIn("Not saved", body["error"])
        self.assertEqual(body["item"]["note"], first)
        self.assertEqual(body["item"]["revision"], 1)
        disk = json.loads(self.feedback_path.read_text())
        self.assertEqual(disk["items"][0]["note"], first)
        self.assertNotIn("second-tab-note", self.feedback_path.read_text())
        status, updated, _ = self.post(self.feedback(note="fresh-edit", base_revision=1))
        self.assertEqual(status, 200)
        self.assertEqual(updated["item"]["revision"], 2)
        self.assertEqual(updated["item"]["note"], "fresh-edit")

    def test_failed_save_is_not_reported_as_saved(self):
        parent = self.root / "not-a-directory"
        parent.write_text("keep")
        feedback = parent / "feedback.json"
        _, port = self.open_server(self.manifest_path, feedback)
        status, body, _ = self.post(self.feedback(note="cannot-save"), port=port)
        self.assertEqual(status, 500)
        self.assertIn("Not saved", body["error"])
        self.assertNotIn("item", body)
        self.assertFalse(feedback.exists())
        self.assertEqual(parent.read_text(), "keep")
        outside = self.root / "outside.json"
        outside.write_text('{"secret":"untouched"}\n')
        link = self.root / "linked-feedback.json"
        link.symlink_to(outside)
        _, link_port = self.open_server(self.manifest_path, link)
        status, body, _ = self.post(self.feedback(note="symlink-write"), port=link_port)
        self.assertEqual(status, 500)
        self.assertIn("Not saved", body["error"])
        self.assertEqual(outside.read_text(), '{"secret":"untouched"}\n')
        self.assertNotIn(b"untouched", json.dumps(body).encode())

    def test_incomplete_pass_and_unknown_cost_stay_unconfirmed(self):
        payload = self.review()
        grade = binding(payload, "grade-omitted-with")
        arm = binding(payload, "run-omitted-with")
        record = run_record(payload, "run-omitted-with")
        self.assertEqual(grade["verdict_claim"], "pass")
        self.assertFalse(grade["confirmed"])
        self.assertEqual(grade["evidence_state"], "missing")
        self.assertTrue(grade["usable"])
        self.assertEqual(arm["cost_state"], "unknown")
        self.assertEqual(arm["duration_state"], "unknown")
        self.assertEqual(arm["tokens_state"], "unknown")
        self.assertNotIn("usd", arm)
        self.assertIsNone(record["cost"])
        self.assertIsNone(record["duration_ms"])
        self.assertIsNone(record["tokens"])
        self.assertEqual(arm["skill_availability"], "unverified")
        status, body, _ = self.post(self.feedback(
            subject_id="omitted-verification",
            grade_id="grade-omitted-with",
            judgment="disagree",
            note="The pass omitted the verification quote.",
        ))
        self.assertEqual(status, 200)
        self.assertEqual(body["item"]["judgment"], "disagree")

    def test_malformed_grade_and_cost_keep_the_other_cases(self):
        payload = self.review()
        messages = [item["message"] for item in payload["errors"]]
        self.assertIn("Cost for run run-malformed-with is malformed.", messages)
        self.assertIn("Duration for run run-malformed-with is malformed.", messages)
        self.assertIn("Tokens for run run-malformed-with are malformed.", messages)
        self.assertIn("Grade grade-malformed-with verdict is malformed.", messages)
        broken = case(payload, "malformed-grade-cost")
        self.assertIn("ownership question stays visible", broken["runs"][0]["output"])
        self.assertIsNone(broken["runs"][0]["cost"])
        self.assertIsNone(broken["runs"][0]["duration_ms"])
        self.assertIsNone(broken["runs"][0]["tokens"])
        self.assertIsNone(broken["grades"][0]["verdict"])
        self.assertFalse(binding(payload, "grade-malformed-with")["usable"])
        self.assertIn("account administrators", case(payload, "protect-export-boundaries")["prompt"])
        self.assertEqual(len(payload["manifest"]["cases"]), 4)
        status, body, _ = self.post(self.feedback(
            subject_id="malformed-grade-cost",
            grade_id="grade-malformed-with",
            judgment="agree",
        ))
        self.assertEqual(status, 400)
        self.assertIn("Not saved", body["error"])
        self.assertFalse(self.feedback_path.exists())

    def test_trigger_proof_roles_stay_distinct(self):
        payload = self.review()
        training = binding(payload, "train-grok-loaded")
        unverified = binding(payload, "validation-grok-unverified")
        validation = binding(payload, "validation-grok-not-loaded")
        fresh = binding(payload, "fresh-grok-not-loaded")
        listing = binding(payload, "fresh-grok-listing-proxy")
        self.assertEqual(training["proof"], "recorded_trigger")
        self.assertEqual(training["selection"], "training")
        self.assertEqual(unverified["proof"], "unverified")
        self.assertEqual(unverified["selection"], "validation_used_for_selection")
        self.assertNotEqual(unverified["proof"], "recorded_non_trigger")
        self.assertEqual(validation["proof"], "recorded_non_trigger")
        self.assertEqual(validation["selection"], "validation")
        self.assertEqual(fresh["proof"], "recorded_non_trigger")
        self.assertEqual(fresh["selection"], "fresh")
        self.assertEqual(listing["basis"], "listing_proxy")
        self.assertEqual(listing["observed"], "loaded")
        self.assertEqual(listing["proof"], "unverified")
        self.assertIsNone(listing["description_revision"])
        trigger_ids = [item["id"] for item in payload["manifest"]["triggers"]]
        case_ids = [item["id"] for item in payload["manifest"]["cases"]]
        self.assertNotIn("simplify-an-overbuilt-plan", case_ids)
        self.assertEqual(trigger_ids, ["simplify-an-overbuilt-plan", "compare-architectures"])

    def test_model_markup_is_json_or_plain_text(self):
        status, data, headers = self.request("GET", "/api/review")
        self.assertEqual(status, 200)
        self.assertIn("application/json", headers["Content-Type"])
        self.assertNotIn("text/html", headers["Content-Type"])
        self.assertFalse(data.lstrip().startswith(b"<"))
        self.assertIn("default-src 'none'", headers["Content-Security-Policy"])
        self.assertIn("<script>alert(1)</script>", data.decode())
        status, evidence, evidence_headers = self.request("GET", "/evidence/protect-without-output")
        self.assertEqual(status, 200)
        self.assertEqual(evidence, (EVIDENCE / "protect-without-output.txt").read_bytes())
        self.assertIn("text/plain", evidence_headers["Content-Type"])
        self.assertEqual(evidence_headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("default-src 'none'", evidence_headers["Content-Security-Policy"])
        self.assertNotIn("evidence_root", self.review()["manifest"])
        self.assertNotIn("files", self.review()["manifest"])

    def test_host_origin_and_body_limit_reject_without_disclosure(self):
        secret_note = "PRIVATE-NOTE-TOKEN"
        self.post(self.feedback(note=secret_note))
        status, data, _ = self.request("GET", "/api/review", headers={"Host": "evil.example"})
        self.assertEqual(status, 403)
        self.assertNotIn(b"account administrators", data)
        self.assertNotIn(b"PRIVATE-NOTE-TOKEN", data)
        status, data, _ = self.request("GET", "/evidence/protect-with-trace", headers={"Host": "evil.example"})
        self.assertEqual(status, 403)
        self.assertNotIn(b"skill_loaded", data)
        status, data, _ = self.request(
            "GET", "/api/review", headers={"Host": "localhost:%d" % self.port})
        self.assertEqual(status, 200)
        self.assertIn(b"protect-export-boundaries", data)
        status, data, _ = self.request(
            "GET", "/api/review", headers={"Host": "127.0.0.1:1"})
        self.assertEqual(status, 403)
        evil = json.dumps(self.feedback(note="origin-attack")).encode()
        status, data, _ = self.request(
            "POST", "/api/feedback", evil,
            headers={"Host": "127.0.0.1:%d" % self.port, "Origin": "http://evil.example",
                     "Content-Type": "application/json", "Content-Length": str(len(evil))})
        self.assertEqual(status, 403)
        self.assertNotIn(b"PRIVATE-NOTE-TOKEN", data)
        self.assertNotIn(b"account administrators", data)
        self.assertIn(secret_note, self.feedback_path.read_text())
        self.assertNotIn("origin-attack", self.feedback_path.read_text())
        status, _, _ = self.request(
            "POST", "/api/feedback", evil,
            headers={"Host": "127.0.0.1:%d" % self.port, "Origin": "https://127.0.0.1:%d" % self.port,
                     "Content-Type": "application/json", "Content-Length": str(len(evil))})
        self.assertEqual(status, 403)
        oversized = b'{"note":"' + (b"a" * 70000) + b'"}'
        status, body_bytes, _ = self.request("POST", "/api/feedback", oversized)
        self.assertEqual(status, 413)
        self.assertIn("Not saved", body_bytes.decode())
        self.assertNotIn("a" * 100, self.feedback_path.read_text())

    def test_unlisted_traversal_and_symlink_evidence_are_unreadable(self):
        root = self.root / "root"
        outside = self.root / "outside"
        root.mkdir()
        outside.mkdir()
        (outside / "secret.txt").write_text("OUTSIDE-SECRET-9f3a")
        (root / "ok.txt").write_text("listed-trace-ok")
        (root / "unlisted.txt").write_text("UNLISTED-FILE-9f3a")
        (root / "escape.txt").symlink_to(outside / "secret.txt")
        manifest = {
            "schema": 1,
            "title": "Attack fixture",
            "skill": {"name": "checking-simplicity", "revision": None},
            "round": {"id": "attack-round", "frozen": True, "note": None},
            "evidence_root": str(root),
            "files": [
                {"id": "ok-trace", "path": "ok.txt"},
                {"id": "escape-trace", "path": "escape.txt"},
                {"id": "traversal-trace", "path": "../outside/secret.txt"},
            ],
            "cases": [{
                "id": "attack-case",
                "title": "Attack case",
                "prompt": "LEAK-MARKER-PROMPT",
                "inputs": [],
                "expected": None,
                "assertions": [],
                "provenance": None,
                "runs": [],
                "grades": [],
            }],
            "triggers": [],
        }
        manifest_path = self.root / "attack.json"
        manifest_path.write_text(json.dumps(manifest))
        _, port = self.open_server(manifest_path, self.root / "attack-feedback.json")
        status, data, headers = self.request("GET", "/evidence/ok-trace", port=port)
        self.assertEqual(status, 200)
        self.assertEqual(data, b"listed-trace-ok")
        self.assertIn("text/plain", headers["Content-Type"])
        for route in (
            "/evidence/escape-trace",
            "/evidence/traversal-trace",
            "/evidence/unlisted",
            "/evidence/../outside/secret.txt",
            "/evidence/%2e%2e/outside/secret.txt",
            "/evidence/ok-trace/../../outside/secret.txt",
        ):
            status, data, _ = self.request("GET", route, port=port)
            self.assertEqual(status, 404, route)
            self.assertNotIn(b"OUTSIDE-SECRET-9f3a", data)
            self.assertNotIn(b"UNLISTED-FILE-9f3a", data)
            self.assertNotIn(b"LEAK-MARKER-PROMPT", data)
        payload = self.review(port)
        leaked = json.dumps(payload)
        self.assertNotIn("OUTSIDE-SECRET-9f3a", leaked)
        self.assertNotIn("UNLISTED-FILE-9f3a", leaked)
        self.assertIn("LEAK-MARKER-PROMPT", leaked)

    def test_committed_fixture_uses_its_relative_evidence_root(self):
        _, port = self.open_server(FIXTURE, self.root / "relative-feedback.json")
        status, data, headers = self.request("GET", "/evidence/protect-with-trace", port=port)
        self.assertEqual(status, 200)
        self.assertEqual(data, (EVIDENCE / "protect-with-trace.json").read_bytes())
        self.assertIn("text/plain", headers["Content-Type"])
        payload = self.review(port)
        self.assertEqual(payload["manifest"]["round"]["id"], ROUND)
        self.assertIsNone(payload["feedback"]["error"])

    def test_fatal_manifest_is_a_visible_error(self):
        bad = self.root / "broken.json"
        bad.write_text("{")
        _, port = self.open_server(bad, self.feedback_path)
        payload = self.review(port)
        self.assertIsNone(payload["manifest"])
        self.assertEqual(payload["bindings"], [])
        self.assertIn("malformed JSON", payload["errors"][0]["message"])
        status, body, _ = self.post(self.feedback(
            note="nope", fingerprint="sha256:" + ("ab" * 32)), port=port)
        self.assertEqual(status, 400)
        self.assertIn("Not saved", body["error"])
        self.assertFalse(self.feedback_path.exists())

    def test_viewer_file_is_served_unchanged_or_reported_absent(self):
        page = self.root / "page.html"
        page.write_bytes(b"<!DOCTYPE html><title>Review</title><style>body{color:#042458}</style>")
        _, port = self.open_server(self.manifest_path, self.root / "viewer-feedback.json", viewer=page)
        status, data, headers = self.request("GET", "/", port=port)
        self.assertEqual(status, 200)
        self.assertEqual(data, page.read_bytes())
        self.assertIn("text/html", headers["Content-Type"])
        policy = headers["Content-Security-Policy"]
        self.assertIn("default-src 'none'", policy)
        self.assertIn("connect-src 'self'", policy)
        self.assertIn("style-src 'unsafe-inline'", policy)
        secret = self.root / "secret.html"
        secret.write_text("VIEWER-SECRET")
        link = self.root / "viewer-link.html"
        link.symlink_to(secret)
        _, link_port = self.open_server(self.manifest_path, self.root / "link-feedback.json", viewer=link)
        status, data, _ = self.request("GET", "/", port=link_port)
        self.assertEqual(status, 404)
        self.assertNotIn(b"VIEWER-SECRET", data)
        status, data, _ = self.request("GET", "/")
        sibling = ROOT / "viewer.html"
        if sibling.is_file() and not sibling.is_symlink():
            self.assertEqual(status, 200)
            self.assertEqual(data, sibling.read_bytes())
        else:
            self.assertEqual(status, 404)
            self.assertIn(b"viewer.html is not present", data)

    def test_explicit_no_feedback_is_distinct_from_absence(self):
        payload = self.review()
        self.assertEqual(payload["feedback"]["items"], [])
        status, body, _ = self.post(self.feedback(
            subject_id="protect-export-boundaries",
            grade_id="grade-protect-without",
            judgment=None,
            note="No feedback on the baseline grade.",
        ))
        self.assertEqual(status, 200)
        self.assertIsNone(body["item"]["judgment"])
        payload = self.review()
        self.assertEqual(len(payload["feedback"]["items"]), 1)
        self.assertIsNone(payload["feedback"]["items"][0]["judgment"])
        self.assertEqual(payload["feedback"]["items"][0]["binding"], "current")

    def raw(self, payload, port=None):
        port = self.port if port is None else port
        connection = socket.create_connection(("127.0.0.1", port), timeout=5)
        try:
            connection.sendall(payload)
            chunks = []
            while True:
                chunk = connection.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
        finally:
            connection.close()
        raw = b"".join(chunks)
        head, _, body = raw.partition(b"\r\n\r\n")
        status = int(head.split(b" ", 2)[1])
        return status, body

    def test_native_observation_without_resolvable_proof_stays_unverified(self):
        data = json.loads(self.manifest_path.read_text())
        data["triggers"][0]["observations"].append({
            "id": "native-loaded-without-proof",
            "target": "grok-4.7-high",
            "description_revision": "description-synthetic-1",
            "role": "fresh",
            "used_for_selection": False,
            "observed": "loaded",
            "basis": "native",
            "summary": "Claims a load with no trace.",
            "evidence": [],
        })
        data["triggers"][1]["observations"].append({
            "id": "native-absent-unlisted",
            "target": "grok-4.7-high",
            "description_revision": None,
            "role": "fresh",
            "used_for_selection": False,
            "observed": "not_loaded",
            "basis": "native",
            "summary": "Names a trace that is not listed.",
            "evidence": [{"id": "not-a-listed-file", "label": "Missing trace"}],
        })
        self.manifest_path.write_text(json.dumps(data))
        payload = self.review()
        self.assertEqual(binding(payload, "native-loaded-without-proof")["proof"], "unverified")
        self.assertEqual(binding(payload, "native-absent-unlisted")["proof"], "unverified")
        self.assertEqual(binding(payload, "train-grok-loaded")["proof"], "recorded_trigger")
        self.assertEqual(binding(payload, "validation-grok-not-loaded")["proof"], "recorded_non_trigger")

    def test_feedback_path_cannot_replace_manifest_or_evidence(self):
        evidence = self.root / "real-evidence"
        evidence.mkdir()
        trace = evidence / "trace.json"
        original_trace = b'{"items":[]}\n'
        trace.write_bytes(original_trace)
        aliased_trace = self.root / "real-evidence" / ".." / "real-evidence" / "trace.json"
        manifest = {
            "schema": 1,
            "title": "Overlap",
            "skill": {"name": "checking-simplicity", "revision": None},
            "round": {"id": "overlap-round", "frozen": True, "note": None},
            "evidence_root": str(evidence),
            "files": [{"id": "trace-file", "path": "trace.json"}],
            "cases": [{
                "id": "overlap-case",
                "title": "Overlap case",
                "prompt": "Keep the evidence file intact.",
                "inputs": [],
                "expected": None,
                "assertions": [],
                "provenance": None,
                "runs": [],
                "grades": [],
            }],
            "triggers": [],
        }
        manifest_path = self.root / "overlap-manifest.json"
        manifest_path.write_text(json.dumps(manifest))
        manifest_bytes = manifest_path.read_bytes()
        _, port = self.open_server(manifest_path, aliased_trace)
        status, body, _ = self.post(self.feedback(
            round_id="overlap-round",
            subject_id="overlap-case",
            note="must not replace the trace",
        ), port=port)
        self.assertNotEqual(status, 200)
        self.assertIn("Not saved", body["error"])
        self.assertIn("overlap", body["error"])
        self.assertEqual(trace.read_bytes(), original_trace)
        self.assertEqual(aliased_trace.read_bytes(), original_trace)
        _, manifest_port = self.open_server(manifest_path, manifest_path)
        status, body, _ = self.post(self.feedback(
            round_id="overlap-round",
            subject_id="overlap-case",
            note="must not replace the manifest",
            fingerprint="sha256:" + ("ab" * 32),
        ), port=manifest_port)
        self.assertNotEqual(status, 200)
        self.assertIn("overlap", body["error"])
        self.assertEqual(manifest_path.read_bytes(), manifest_bytes)

    def test_evidence_content_and_path_retire_agreement(self):
        evidence = self.root / "copied-evidence"
        shutil.copytree(EVIDENCE, evidence)
        data = json.loads(self.manifest_path.read_text())
        data["evidence_root"] = str(evidence)
        self.manifest_path.write_text(json.dumps(data))
        shown = self.binding_record("protect-export-boundaries", "grade-protect-with")["fingerprint"]
        observed = self.binding_record("simplify-an-overbuilt-plan", "train-grok-loaded")["fingerprint"]
        (evidence / "protect-with-trace.json").write_text('{"kind":"changed-trace"}\n')
        status, body, _ = self.post(self.feedback(
            subject_id="protect-export-boundaries",
            grade_id="grade-protect-with",
            judgment="agree",
            note="saved against the old trace",
            fingerprint=shown,
        ))
        self.assertEqual(status, 409)
        self.assertIn("Not saved", body["error"])
        self.assertIsNone(body["item"])
        self.assertFalse(self.feedback_path.exists())
        status, saved, _ = self.post(self.feedback(
            subject_id="simplify-an-overbuilt-plan",
            grade_id="train-grok-loaded",
            judgment="agree",
            note="observation before the trace edit",
            fingerprint=observed,
        ))
        self.assertEqual(status, 200, saved)
        (evidence / "train-loaded.json").write_text('{"kind":"changed-activation"}\n')
        payload = self.review()
        item = next(entry for entry in payload["feedback"]["items"] if entry["grade_id"] == "train-grok-loaded")
        self.assertEqual(item["binding"], "earlier")
        self.assertEqual(item["judgment"], "agree")
        data = json.loads(self.manifest_path.read_text())
        for listed in data["files"]:
            if listed["id"] == "protect-with-trace":
                listed["path"] = "protect-without-trace.json"
        self.manifest_path.write_text(json.dumps(data))
        status, body, _ = self.post(self.feedback(
            subject_id="protect-export-boundaries",
            grade_id="grade-protect-with",
            judgment="agree",
            note="saved against the retargeted id",
            fingerprint=shown,
        ))
        self.assertEqual(status, 409)
        self.assertIsNone(body["item"])
        self.assertFalse(any(
            entry.get("note") == "saved against the retargeted id"
            for entry in json.loads(self.feedback_path.read_text())["items"]
        ))

    def test_duplicate_host_origin_and_content_length_are_rejected(self):
        port = self.port
        status, body = self.raw((
            f"GET /api/review HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{port}\r\n"
            f"Host: evil.example\r\n"
            f"Connection: close\r\n\r\n"
        ).encode())
        self.assertEqual(status, 403)
        self.assertNotIn(b"account administrators", body)
        shown = self.binding_record("ask-owner-before-dropping-audit")["fingerprint"]
        payload = json.dumps(self.feedback(note="duplicate-origin", fingerprint=shown)).encode()
        status, body = self.raw((
            f"POST /api/feedback HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{port}\r\n"
            f"Origin: http://127.0.0.1:{port}\r\n"
            f"Origin: http://evil.example\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(payload)}\r\n"
            f"Connection: close\r\n\r\n"
        ).encode() + payload)
        self.assertEqual(status, 403)
        self.assertFalse(self.feedback_path.exists())
        self.assertNotIn(b"duplicate-origin", body)
        payload = json.dumps(self.feedback(note="ambiguous-length", fingerprint=shown)).encode()
        status, body = self.raw((
            f"POST /api/feedback HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{port}\r\n"
            f"Origin: http://127.0.0.1:{port}\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(payload)}\r\n"
            f"Content-Length: {len(payload) + 8}\r\n"
            f"Connection: close\r\n\r\n"
        ).encode() + payload)
        self.assertIn(status, (400, 403))
        self.assertNotIn(b"Saved", body)
        self.assertFalse(self.feedback_path.exists())

    def test_pass_with_a_failed_assertion_stays_an_unconfirmed_claim(self):
        data = json.loads(self.manifest_path.read_text())
        grade = data["cases"][0]["grades"][0]
        self.assertEqual(grade["id"], "grade-protect-with")
        grade["assertions"] = [
            {"assertion_id": "keeps-authorization", "result": "fail", "evidence": "Drop the administrator check."},
            {"assertion_id": "recognizes-reuse", "result": "pass", "evidence": "Reusing those helpers is the smaller shape."},
        ]
        self.manifest_path.write_text(json.dumps(data))
        found = binding(self.review(), "grade-protect-with")
        self.assertEqual(found["verdict_claim"], "pass")
        self.assertFalse(found["confirmed"])
        self.assertEqual(found["consistency"], "inconsistent")
        self.assertEqual(found["evidence_state"], "present")
        grade["verdict"] = "fail"
        self.manifest_path.write_text(json.dumps(data))
        supported = binding(self.review(), "grade-protect-with")
        self.assertEqual(supported["verdict_claim"], "fail")
        self.assertTrue(supported["confirmed"])
        self.assertEqual(supported["consistency"], "consistent")
        self.assertEqual(supported["evidence_state"], "present")

    def test_unreadable_evidence_cannot_confirm_a_grade_or_native_proof(self):
        evidence = self.root / "bounded-evidence"
        evidence.mkdir()
        huge = evidence / "huge.txt"
        huge.write_bytes(b"x" * (review.MAX_EVIDENCE_BYTES + 1))
        blocked = evidence / "blocked.txt"
        blocked.write_text("secret activation trace")
        blocked.chmod(0)
        manifest = {
            "schema": 1,
            "title": "Bounded evidence",
            "skill": {"name": "checking-simplicity", "revision": None},
            "round": {"id": "bounded-round", "frozen": True, "note": None},
            "evidence_root": str(evidence),
            "files": [
                {"id": "huge-trace", "path": "huge.txt"},
                {"id": "blocked-trace", "path": "blocked.txt"},
            ],
            "cases": [{
                "id": "bounded-case",
                "title": "Oversized trace",
                "prompt": "The trace is listed but not readable within the bound.",
                "inputs": [],
                "expected": None,
                "assertions": [
                    {"id": "names-boundary", "text": "Names the bound.", "check": "judgment"},
                ],
                "provenance": None,
                "runs": [{
                    "id": "run-bounded",
                    "target": "grok-4.7-high",
                    "arm": "with_skill",
                    "model": "grok-4.7",
                    "settings": "high",
                    "skill_availability": "verified",
                    "output": "Names the bound.",
                    "summary": None,
                    "duration_ms": None,
                    "tokens": None,
                    "cost": None,
                    "evidence": [{"id": "huge-trace", "label": "Oversized trace"}],
                }],
                "grades": [{
                    "id": "grade-bounded",
                    "grader": "blind grader",
                    "target": "grok-4.7-high",
                    "run_ids": ["run-bounded"],
                    "verdict": "pass",
                    "assertions": [
                        {"assertion_id": "names-boundary", "result": "pass", "evidence": "Names the bound."},
                    ],
                    "summary": "Claimed pass against an unreadable trace.",
                    "evidence": [{"id": "huge-trace", "label": "Oversized trace"}],
                }],
            }],
            "triggers": [{
                "id": "bounded-trigger",
                "query": "Is the oversized log native proof?",
                "expected": "trigger",
                "note": None,
                "observations": [
                    {
                        "id": "obs-huge",
                        "target": "grok-4.7-high",
                        "description_revision": "description-synthetic-1",
                        "role": "fresh",
                        "used_for_selection": False,
                        "observed": "loaded",
                        "basis": "native",
                        "summary": "Claims a load from an oversized trace.",
                        "evidence": [{"id": "huge-trace", "label": "Oversized trace"}],
                    },
                    {
                        "id": "obs-blocked",
                        "target": "grok-4.7-high",
                        "description_revision": "description-synthetic-1",
                        "role": "fresh",
                        "used_for_selection": False,
                        "observed": "not_loaded",
                        "basis": "native",
                        "summary": "Claims a non-load from an unreadable trace.",
                        "evidence": [{"id": "blocked-trace", "label": "Unreadable trace"}],
                    },
                ],
            }],
        }
        path = self.root / "bounded.json"
        path.write_text(json.dumps(manifest))
        _, port = self.open_server(path, self.root / "bounded-feedback.json")
        self.addCleanup(blocked.chmod, 0o644)
        payload = self.review(port)
        grade = binding(payload, "grade-bounded")
        self.assertEqual(grade["verdict_claim"], "pass")
        self.assertFalse(grade["confirmed"])
        self.assertEqual(grade["consistency"], "incomplete")
        self.assertEqual(grade["evidence_state"], "missing")
        self.assertTrue(grade["usable"])
        self.assertEqual(binding(payload, "obs-huge")["proof"], "unverified")
        self.assertEqual(binding(payload, "obs-blocked")["proof"], "unverified")
        for evidence_id in ("huge-trace", "blocked-trace"):
            status, body, headers = self.request("GET", "/evidence/" + evidence_id, port=port)
            self.assertEqual(status, 404, evidence_id)
            self.assertNotIn(b"secret activation", body)
            self.assertIn("application/json", headers["Content-Type"])

    def test_grade_must_cover_every_case_assertion_once(self):
        data = json.loads(FIXTURE.read_text())
        data["evidence_root"] = str(EVIDENCE)
        grade = data["cases"][0]["grades"][0]
        self.assertEqual(grade["id"], "grade-protect-with")
        self.assertEqual(
            [item["id"] for item in data["cases"][0]["assertions"]],
            ["keeps-authorization", "recognizes-reuse"])
        grade["assertions"] = [item for item in grade["assertions"] if item["assertion_id"] == "keeps-authorization"]
        path = self.root / "partial-grade.json"
        path.write_text(json.dumps(data))
        _, port = self.open_server(path, self.root / "partial-feedback.json")
        found = binding(self.review(port), "grade-protect-with")
        self.assertEqual(found["verdict_claim"], "pass")
        self.assertFalse(found["confirmed"])
        self.assertEqual(found["consistency"], "incomplete")
        self.assertTrue(found["usable"])
        status, saved, _ = self.post(self.feedback(
            round_id=data["round"]["id"],
            subject_id="protect-export-boundaries",
            grade_id="grade-protect-with",
            judgment="disagree",
            note="The grade dropped recognizes-reuse.",
        ), port=port)
        self.assertEqual(status, 200, saved)
        self.assertEqual(saved["item"]["judgment"], "disagree")
        data["cases"][0]["grades"][0]["assertions"] = [
            {"assertion_id": "keeps-authorization", "result": "pass", "evidence": "Administrators stay the only exporters."},
            {"assertion_id": "recognizes-reuse", "result": "pass", "evidence": "Reusing those helpers is the smaller shape."},
            {"assertion_id": "not-a-case-assertion", "result": "pass", "evidence": "Extra claim."},
        ]
        path.write_text(json.dumps(data))
        unknown = binding(self.review(port), "grade-protect-with")
        self.assertEqual(unknown["verdict_claim"], "pass")
        self.assertFalse(unknown["confirmed"])
        self.assertEqual(unknown["consistency"], "incomplete")
        data["cases"][0]["grades"][0]["assertions"] = [
            {"assertion_id": "keeps-authorization", "result": "pass", "evidence": "Administrators stay the only exporters."},
            {"assertion_id": "keeps-authorization", "result": "pass", "evidence": "Repeated quote."},
            {"assertion_id": "recognizes-reuse", "result": "pass", "evidence": "Reusing those helpers is the smaller shape."},
        ]
        path.write_text(json.dumps(data))
        duplicate = binding(self.review(port), "grade-protect-with")
        self.assertFalse(duplicate["confirmed"])
        self.assertEqual(duplicate["consistency"], "incomplete")
        self.assertEqual(duplicate["verdict_claim"], "pass")

    def test_oversized_numeric_fields_do_not_hide_sibling_cases(self):
        data = json.loads(FIXTURE.read_text())
        data["evidence_root"] = str(EVIDENCE)
        data["cases"][0]["runs"][0]["duration_ms"] = 10 ** 400
        data["cases"][0]["runs"][0]["cost"] = {"usd": 10 ** 400, "basis": "api_equivalent_estimate"}
        path = self.root / "overflow.json"
        path.write_text(json.dumps(data))
        _, port = self.open_server(path, self.root / "overflow-feedback.json")
        status, raw, _ = self.request("GET", "/api/review", port=port)
        self.assertEqual(status, 200, raw)
        payload = json.loads(raw.decode())
        self.assertIn("Ask the owner", case(payload, "ask-owner-before-dropping-audit")["prompt"])
        record = run_record(payload, "run-protect-with")
        self.assertIsNone(record["duration_ms"])
        self.assertIsNone(record["cost"])
        messages = [item["message"] for item in payload["errors"]]
        self.assertIn("Duration for run run-protect-with is malformed.", messages)
        self.assertIn("Cost for run run-protect-with is malformed.", messages)
        self.assertEqual(binding(payload, "run-protect-with")["duration_state"], "malformed")
        self.assertEqual(binding(payload, "run-protect-with")["cost_state"], "malformed")

    def test_lone_surrogate_serializes_and_unicode_fingerprint_stays_utf8(self):
        payload = {"prompt": "检查 café"}
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual(review.fingerprint(payload), "sha256:" + hashlib.sha256(encoded).hexdigest())
        self.assertIn("café".encode(), encoded)
        self.assertNotIn(b"\\u00e9", encoded)
        lone = "before \ud800 after café"
        literal = "before \\ud800 after café"
        self.assertNotEqual(review.fingerprint({"prompt": lone}), review.fingerprint({"prompt": literal}))
        restored = json.loads(review.dump_json({"prompt": lone}))["prompt"]
        self.assertEqual(restored, lone)
        self.assertNotEqual(restored, literal)
        data = json.loads(FIXTURE.read_text())
        data["evidence_root"] = str(EVIDENCE)
        data["cases"][0]["prompt"] = "broken \ud800 prompt"
        data["cases"][1]["prompt"] = "Sibling prompt stays readable."
        path = self.root / "surrogate.json"
        path.write_text(json.dumps(data, ensure_ascii=True))
        _, port = self.open_server(path, self.root / "surrogate-feedback.json")
        status, raw, headers = self.request("GET", "/api/review", port=port)
        self.assertEqual(status, 200, raw)
        self.assertIn("application/json", headers["Content-Type"])
        body = raw.decode("utf-8")
        self.assertIn("Sibling prompt stays readable.", body)
        status, saved, _ = self.post(self.feedback(
            round_id=data["round"]["id"],
            subject_id="ask-owner-before-dropping-audit",
            note="note \ud800 café",
        ), port=port)
        self.assertEqual(status, 200, saved)
        stored = (self.root / "surrogate-feedback.json").read_text(encoding="utf-8")
        self.assertIn("café", stored)
        self.assertEqual(json.loads(stored)["items"][0]["note"], "note \ud800 café")

    def test_same_bytes_under_another_evidence_root_retire_agreement(self):
        first = self.root / "archive-a"
        second = self.root / "archive-b"
        first.mkdir()
        second.mkdir()
        content = b'{"kind":"same-bytes"}\n'
        (first / "trace.json").write_bytes(content)
        (second / "trace.json").write_bytes(content)
        manifest = {
            "schema": 1,
            "title": "Root move",
            "skill": {"name": "checking-simplicity", "revision": None},
            "round": {"id": "root-move", "frozen": True, "note": None},
            "evidence_root": str(first),
            "files": [{"id": "trace-file", "path": "trace.json"}],
            "cases": [{
                "id": "root-case",
                "title": "Same relative trace",
                "prompt": "The bytes and relative path match another archive.",
                "inputs": [],
                "expected": None,
                "assertions": [{"id": "one-check", "text": "One check.", "check": "judgment"}],
                "provenance": None,
                "runs": [{
                    "id": "run-root",
                    "target": "grok-4.7-high",
                    "arm": "with_skill",
                    "model": None,
                    "settings": None,
                    "skill_availability": "verified",
                    "output": "One check.",
                    "summary": None,
                    "duration_ms": None,
                    "tokens": None,
                    "cost": None,
                    "evidence": [{"id": "trace-file", "label": "Trace"}],
                }],
                "grades": [{
                    "id": "grade-root",
                    "grader": "blind grader",
                    "target": None,
                    "run_ids": ["run-root"],
                    "verdict": "pass",
                    "assertions": [{"assertion_id": "one-check", "result": "pass", "evidence": "One check."}],
                    "summary": "Pass on this archive.",
                    "evidence": [{"id": "trace-file", "label": "Trace"}],
                }],
            }],
            "triggers": [],
        }
        path = self.root / "root-move.json"
        path.write_text(json.dumps(manifest))
        _, port = self.open_server(path, self.root / "root-move-feedback.json")
        shown = self.binding_record("root-case", "grade-root", port)["fingerprint"]
        manifest["evidence_root"] = str(second)
        path.write_text(json.dumps(manifest))
        status, rejected, _ = self.post(self.feedback(
            round_id="root-move",
            subject_id="root-case",
            grade_id="grade-root",
            judgment="agree",
            note="agreement from the first archive",
            fingerprint=shown,
        ), port=port)
        self.assertEqual(status, 409, rejected)
        self.assertIsNone(rejected["item"])
        self.assertFalse((self.root / "root-move-feedback.json").exists())

    def test_same_bytes_under_another_relative_path_have_a_different_fingerprint(self):
        root = self.root / "path-archive"
        root.mkdir()
        content = b'{"kind":"same-bytes"}\n'
        (root / "one.json").write_bytes(content)
        (root / "two.json").write_bytes(content)
        def manifest_for(relative):
            return {
                "schema": 1,
                "title": "Path identity",
                "skill": {"name": "checking-simplicity", "revision": None},
                "round": {"id": "path-move", "frozen": True, "note": None},
                "evidence_root": str(root),
                "files": [{"id": "trace-file", "path": relative}],
                "cases": [{
                    "id": "path-case",
                    "title": "Relative path",
                    "prompt": "Same bytes, different relative path.",
                    "inputs": [],
                    "expected": None,
                    "assertions": [{"id": "one-check", "text": "One check.", "check": "judgment"}],
                    "provenance": None,
                    "runs": [],
                    "grades": [],
                }],
                "triggers": [{
                    "id": "path-trigger",
                    "query": "Did it load?",
                    "expected": "trigger",
                    "note": None,
                    "observations": [{
                        "id": "path-obs",
                        "target": "grok-4.7-high",
                        "description_revision": None,
                        "role": "fresh",
                        "used_for_selection": False,
                        "observed": "loaded",
                        "basis": "native",
                        "summary": "Recorded against this path.",
                        "evidence": [{"id": "trace-file", "label": "Trace"}],
                    }],
                }],
            }
        first = self.root / "path-one.json"
        second = self.root / "path-two.json"
        first.write_text(json.dumps(manifest_for("one.json")))
        second.write_text(json.dumps(manifest_for("two.json")))
        _, first_port = self.open_server(first, self.root / "path-one-feedback.json")
        _, second_port = self.open_server(second, self.root / "path-two-feedback.json")
        left = self.binding_record("path-trigger", "path-obs", first_port)["fingerprint"]
        right = self.binding_record("path-trigger", "path-obs", second_port)["fingerprint"]
        self.assertNotEqual(left, right)

    def test_readable_trace_is_recorded_not_verified_activation(self):
        evidence = self.root / "recorded-evidence"
        evidence.mkdir()
        (evidence / "contradiction.json").write_text(
            '{"basis":"native","observed":"not_loaded","skill_loaded":false,"summary":"The native session did not load checking-simplicity."}\n')
        manifest = {
            "schema": 1,
            "title": "Recorded activation",
            "skill": {"name": "checking-simplicity", "revision": None},
            "round": {"id": "recorded-round", "frozen": True, "note": None},
            "evidence_root": str(evidence),
            "files": [{"id": "contradiction", "path": "contradiction.json"}],
            "cases": [],
            "triggers": [{
                "id": "recorded-trigger",
                "query": "Simplify this overbuilt plan.",
                "expected": "trigger",
                "note": None,
                "observations": [{
                    "id": "obs-contradiction",
                    "target": "grok-4.7-high",
                    "description_revision": "description-synthetic-1",
                    "role": "fresh",
                    "used_for_selection": False,
                    "observed": "loaded",
                    "basis": "native",
                    "summary": "The manifest claims the skill loaded.",
                    "evidence": [{"id": "contradiction", "label": "Contradictory trace"}],
                }],
            }],
        }
        path = self.root / "recorded.json"
        path.write_text(json.dumps(manifest))
        _, port = self.open_server(path, self.root / "recorded-feedback.json")
        status, raw, _ = self.request("GET", "/api/review", port=port)
        self.assertEqual(status, 200, raw)
        proof = binding(json.loads(raw.decode()), "obs-contradiction")["proof"]
        self.assertEqual(proof, "recorded_trigger")
        self.assertNotIn("verified_trigger", raw.decode())
        self.assertNotIn("verified_non_trigger", raw.decode())

    def oversized_manifest(self, root, round_id):
        return {
            "schema": 1,
            "title": "Oversized identity",
            "skill": {"name": "checking-simplicity", "revision": None},
            "round": {"id": round_id, "frozen": True, "note": None},
            "evidence_root": str(root),
            "files": [{"id": "huge-trace", "path": "huge.txt"}],
            "cases": [{
                "id": "huge-case",
                "title": "Oversized trace",
                "prompt": "The trace is listed but larger than the bound.",
                "inputs": [],
                "expected": None,
                "assertions": [{"id": "names-bound", "text": "Names the bound.", "check": "judgment"}],
                "provenance": None,
                "runs": [{
                    "id": "run-huge",
                    "target": "grok-4.7-high",
                    "arm": "with_skill",
                    "model": None,
                    "settings": None,
                    "skill_availability": "verified",
                    "output": "Names the bound.",
                    "summary": None,
                    "duration_ms": None,
                    "tokens": None,
                    "cost": None,
                    "evidence": [{"id": "huge-trace", "label": "Oversized trace"}],
                }],
                "grades": [{
                    "id": "grade-huge",
                    "grader": "blind grader",
                    "target": None,
                    "run_ids": ["run-huge"],
                    "verdict": "pass",
                    "assertions": [{"assertion_id": "names-bound", "result": "pass", "evidence": "Names the bound."}],
                    "summary": "Pass claim against an oversized trace.",
                    "evidence": [{"id": "huge-trace", "label": "Oversized trace"}],
                }],
            }],
            "triggers": [{
                "id": "huge-trigger",
                "query": "Did the oversized log show a load?",
                "expected": "trigger",
                "note": None,
                "observations": [{
                    "id": "obs-huge",
                    "target": "grok-4.7-high",
                    "description_revision": None,
                    "role": "fresh",
                    "used_for_selection": False,
                    "observed": "loaded",
                    "basis": "native",
                    "summary": "Manifest claims a load.",
                    "evidence": [{"id": "huge-trace", "label": "Oversized trace"}],
                }],
            }],
        }

    def test_oversized_files_in_different_roots_do_not_share_agreement(self):
        first = self.root / "huge-a"
        second = self.root / "huge-b"
        first.mkdir()
        second.mkdir()
        payload = b"x" * (review.MAX_EVIDENCE_BYTES + 1)
        (first / "huge.txt").write_bytes(payload)
        (second / "huge.txt").write_bytes(payload)
        path = self.root / "huge-move.json"
        path.write_text(json.dumps(self.oversized_manifest(first, "huge-round")))
        _, port = self.open_server(path, self.root / "huge-feedback.json")
        shown = self.binding_record("huge-case", "grade-huge", port)["fingerprint"]
        self.assertEqual(binding(self.review(port), "obs-huge")["proof"], "unverified")
        self.assertFalse(binding(self.review(port), "grade-huge")["confirmed"])
        path.write_text(json.dumps(self.oversized_manifest(second, "huge-round")))
        status, rejected, _ = self.post(self.feedback(
            round_id="huge-round",
            subject_id="huge-case",
            grade_id="grade-huge",
            judgment="agree",
            note="agreement from the first oversized archive",
            fingerprint=shown,
        ), port=port)
        self.assertEqual(status, 409, rejected)
        self.assertIsNone(rejected["item"])
        self.assertFalse((self.root / "huge-feedback.json").exists())

    def test_surrogate_paths_keep_sibling_cases_visible(self):
        evidence = self.root / "plain-evidence"
        evidence.mkdir()
        (evidence / "ok.txt").write_text("readable trace")
        data = json.loads(FIXTURE.read_text())
        data["evidence_root"] = str(evidence)
        data["files"] = [
            {"id": "ok-trace", "path": "ok.txt"},
            {"id": "bad-trace", "path": "bad\ud800.txt"},
        ]
        path = self.root / "surrogate-path.json"
        path.write_text(json.dumps(data, ensure_ascii=True))
        _, port = self.open_server(path, self.root / "surrogate-path-feedback.json")
        status, raw, _ = self.request("GET", "/api/review", port=port)
        self.assertEqual(status, 200, raw)
        body = raw.decode("utf-8")
        payload = json.loads(body)
        self.assertIn("Ask the owner", case(payload, "ask-owner-before-dropping-audit")["prompt"])
        messages = [item["message"] for item in payload["errors"]]
        self.assertTrue(any("bad-trace" in message and "usable filesystem path" in message for message in messages), messages)
        root_data = json.loads(FIXTURE.read_text())
        root_data["evidence_root"] = str(evidence) + "\ud800"
        root_path = self.root / "surrogate-root.json"
        root_path.write_text(json.dumps(root_data, ensure_ascii=True))
        _, root_port = self.open_server(root_path, self.root / "surrogate-root-feedback.json")
        status, raw, _ = self.request("GET", "/api/review", port=root_port)
        self.assertEqual(status, 200, raw)
        payload = json.loads(raw.decode("utf-8"))
        self.assertIn("Ask the owner", case(payload, "ask-owner-before-dropping-audit")["prompt"])
        self.assertTrue(any(
            item["scope"] == "manifest" and item["message"].startswith("evidence_root")
            for item in payload["errors"]), payload["errors"])

    def review_skill(self, skill=None, port=None, query=""):
        path = "/api/review" if skill is None else "/api/review?skill=" + skill
        if query:
            path += ("&" if "?" in path else "?") + query
        status, data, headers = self.request("GET", path, port=port)
        self.assertEqual(status, 200, data)
        self.assertIn("application/json", headers["Content-Type"])
        return json.loads(data.decode())

    def grade_fingerprint(self, skill, port):
        payload = self.review_skill(skill, port)
        return binding(payload, "shared-grade")["fingerprint"]

    def open_index(self, index_path):
        server = review.serve_index(index_path)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        return server, server.server_address[1]

    def plant_manifest(self, folder, skill_id, prompt, evidence_root, evidence_body, round_id="shared-round"):
        folder.mkdir(parents=True, exist_ok=True)
        evidence_root.mkdir(parents=True, exist_ok=True)
        (evidence_root / "trace.json").write_bytes(evidence_body)
        document = {
            "schema": 1,
            "title": skill_id,
            "skill": {"name": skill_id, "revision": None},
            "round": {"id": round_id, "frozen": True, "note": None},
            "evidence_root": str(evidence_root),
            "files": [{"id": "shared-trace", "path": "trace.json"}],
            "cases": [{
                "id": "shared-case",
                "title": "Shared identifiers",
                "prompt": prompt,
                "inputs": [],
                "expected": None,
                "assertions": [{
                    "id": "shared-assertion",
                    "text": "Check the trace.",
                    "check": "judgment",
                }],
                "provenance": None,
                "runs": [{
                    "id": "shared-run",
                    "target": "grok-4.7-high",
                    "arm": "with_skill",
                    "model": None,
                    "settings": None,
                    "skill_availability": "verified",
                    "output": prompt,
                    "summary": None,
                    "duration_ms": None,
                    "tokens": None,
                    "cost": None,
                    "evidence": [{"id": "shared-trace", "label": "Trace"}],
                }],
                "grades": [{
                    "id": "shared-grade",
                    "grader": "reviewer",
                    "target": "grok-4.7-high",
                    "run_ids": ["shared-run"],
                    "verdict": "pass",
                    "assertions": [{
                        "assertion_id": "shared-assertion",
                        "result": "pass",
                        "evidence": "The trace matches this skill.",
                    }],
                    "summary": prompt,
                    "evidence": [{"id": "shared-trace", "label": "Trace"}],
                }],
            }],
            "triggers": [],
        }
        manifest_path = folder / "manifest.json"
        manifest_path.write_text(json.dumps(document))
        return manifest_path, folder / "feedback.json"

    def write_index(self, directory, skills, repository="repo-one"):
        directory.mkdir(parents=True, exist_ok=True)
        index_path = directory / "repo-index.json"
        index_path.write_text(json.dumps({"repository": repository, "skills": skills}))
        return index_path

    def feedback_form(self, fingerprint, note, judgment="agree", grade_id="shared-grade", base_revision=0):
        return {
            "round_id": "shared-round",
            "subject_id": "shared-case",
            "grade_id": grade_id,
            "judgment": judgment,
            "note": note,
            "fingerprint": fingerprint,
            "base_revision": base_revision,
        }

    def test_one_manifest_catalog_selects_that_skill_only(self):
        status, data, _ = self.request("GET", "/api/skills")
        self.assertEqual(status, 200, data)
        catalog = json.loads(data.decode())
        self.assertEqual(set(catalog), {"repository", "skills", "default_skill"})
        self.assertIsNone(catalog["repository"])
        self.assertEqual(catalog["skills"], [{
            "id": "checking-simplicity",
            "name": "checking-simplicity",
        }])
        self.assertEqual(catalog["default_skill"], "checking-simplicity")
        self.assertNotIn(str(self.root), data.decode())
        self.assertNotIn("/", data.decode())
        plain = self.review()
        selected = self.review_skill("checking-simplicity")
        self.assertEqual(selected["manifest"]["round"]["id"], plain["manifest"]["round"]["id"])
        self.assertEqual(
            binding(plain, "grade-protect-with")["fingerprint"],
            binding(selected, "grade-protect-with")["fingerprint"],
        )
        status, data, _ = self.request("GET", "/api/review?skill=other-skill")
        self.assertEqual(status, 404, data)
        self.assertNotIn(b"Ask the owner", data)
        status, data, _ = self.request("GET", "/api/review?skill=checking-simplicity&skill=other-skill")
        self.assertEqual(status, 400, data)
        self.assertIn(b"Rejected", data)
        self.assertNotIn(b"Ask the owner", data)
        for query in ("skill=", "skill=../secret", "skill=bad%20id"):
            status, data, _ = self.request("GET", "/api/review?" + query)
            self.assertEqual(status, 400, query)
            self.assertNotIn(b"Ask the owner", data)
        status, trace, _ = self.request("GET", "/evidence/protect-with-trace?skill=checking-simplicity")
        self.assertEqual(status, 200)
        self.assertEqual(trace, (EVIDENCE / "protect-with-trace.json").read_bytes())
        status, data, _ = self.request("GET", "/evidence/protect-with-trace?skill=other-skill")
        self.assertEqual(status, 404)
        self.assertNotEqual(data, trace)
        self.assertNotIn(b"protect-with-trace", data)
        status, data, _ = self.request("POST", "/api/feedback?skill=other-skill", b"not-json")
        self.assertEqual(status, 400, data)
        self.assertIn(b"Not saved", data)
        self.assertFalse(self.feedback_path.exists())
        shown = next(item["fingerprint"] for item in plain["bindings"]
                     if item.get("record_type") == "subject" and item.get("subject_id") == "ask-owner-before-dropping-audit")
        form = self.feedback(note="scoped note", fingerprint=shown)
        status, data, _ = self.request(
            "POST", "/api/feedback?skill=other-skill", json.dumps(form).encode())
        self.assertEqual(status, 404, data)
        self.assertFalse(self.feedback_path.exists())
        status, data, _ = self.request(
            "POST", "/api/feedback?skill=checking-simplicity", json.dumps(form).encode(),
            headers={"Origin": "http://evil.example"})
        self.assertEqual(status, 403, data)
        self.assertNotIn(b"Ask the owner", data)
        self.assertFalse(self.feedback_path.exists())
        status, body = self.raw((
            f"GET /api/review?skill=checking-simplicity HTTP/1.1\r\n"
            f"Host: evil.example\r\n"
            f"Connection: close\r\n\r\n"
        ).encode())
        self.assertEqual(status, 403)
        self.assertNotIn(b"Ask the owner", body)
        status, saved, _ = self.post(self.feedback(note="scoped note"))
        self.assertEqual(status, 200, saved)
        chosen = self.review_skill("checking-simplicity")
        self.assertEqual(chosen["feedback"]["items"][0]["note"], "scoped note")

    def test_index_isolates_shared_case_grade_and_evidence_ids(self):
        zeta_manifest, _zeta_feedback = self.plant_manifest(
            self.root / "zeta", "skill-zeta", "ZETA-PROMPT-9f3a",
            self.root / "zeta-evidence", b"ZETA-TRACE-9f3a\n")
        alpha_manifest, alpha_feedback = self.plant_manifest(
            self.root / "alpha", "skill-alpha", "ALPHA-PROMPT-9f3a",
            self.root / "alpha" / "evidence", b"ALPHA-TRACE-9f3a\n")
        index_path = self.write_index(self.root / "catalog", [])
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [
                {
                    "id": "skill-zeta",
                    "manifest": os.path.relpath(zeta_manifest, index_path.parent),
                    "feedback": "zeta-feedback.json",
                },
                {
                    "id": "skill-alpha",
                    "manifest": str(alpha_manifest),
                    "feedback": str(alpha_feedback),
                },
            ],
        }))
        _, port = self.open_index(index_path)
        status, data, _ = self.request("GET", "/api/skills?path=/etc/passwd", port=port)
        self.assertEqual(status, 200, data)
        catalog = json.loads(data.decode())
        self.assertEqual(catalog["repository"], "repo-one")
        self.assertEqual([item["id"] for item in catalog["skills"]], ["skill-zeta", "skill-alpha"])
        self.assertEqual([item["name"] for item in catalog["skills"]], ["skill-zeta", "skill-alpha"])
        self.assertEqual(catalog["default_skill"], "skill-zeta")
        self.assertEqual([{*item} for item in catalog["skills"]], [{"id", "name"}, {"id", "name"}])
        decoded = data.decode()
        self.assertNotIn(str(self.root), decoded)
        self.assertNotIn("manifest", decoded)
        self.assertNotIn("feedback", decoded)
        self.assertNotIn("/", decoded)
        default_payload = self.review_skill(None, port)
        zeta_payload = self.review_skill("skill-zeta", port, "path=/tmp/not-a-skill")
        alpha_payload = self.review_skill("skill-alpha", port)
        self.assertEqual(default_payload["manifest"]["title"], "skill-zeta")
        self.assertIn("ZETA-PROMPT-9f3a", zeta_payload["manifest"]["cases"][0]["prompt"])
        self.assertNotIn("ALPHA-PROMPT-9f3a", json.dumps(zeta_payload))
        self.assertIn("ALPHA-PROMPT-9f3a", alpha_payload["manifest"]["cases"][0]["prompt"])
        self.assertNotIn("ZETA-PROMPT-9f3a", json.dumps(alpha_payload))
        self.assertEqual(zeta_payload["manifest"]["cases"][0]["id"], "shared-case")
        self.assertEqual(alpha_payload["manifest"]["cases"][0]["grades"][0]["id"], "shared-grade")
        status, zeta_trace, _ = self.request("GET", "/evidence/shared-trace?skill=skill-zeta", port=port)
        status_alpha, alpha_trace, _ = self.request("GET", "/evidence/shared-trace?skill=skill-alpha", port=port)
        self.assertEqual(status, 200)
        self.assertEqual(status_alpha, 200)
        self.assertEqual(zeta_trace, b"ZETA-TRACE-9f3a\n")
        self.assertEqual(alpha_trace, b"ALPHA-TRACE-9f3a\n")
        status, data, _ = self.request("GET", "/evidence/shared-trace?skill=skill-beta", port=port)
        self.assertEqual(status, 404)
        self.assertNotIn(b"ZETA-TRACE-9f3a", data)
        self.assertNotIn(b"ALPHA-TRACE-9f3a", data)
        status, data, _ = self.request("GET", "/api/review?skill=skill-zeta&skill=skill-alpha", port=port)
        self.assertEqual(status, 400, data)
        self.assertNotIn(b"ZETA-PROMPT-9f3a", data)
        self.assertNotIn(b"ALPHA-PROMPT-9f3a", data)
        zeta_fp = binding(zeta_payload, "shared-grade")["fingerprint"]
        alpha_fp = binding(alpha_payload, "shared-grade")["fingerprint"]
        self.assertNotEqual(zeta_fp, alpha_fp)
        zeta_form = self.feedback_form(zeta_fp, "zeta agrees")
        status, saved, _ = self.request(
            "POST", "/api/feedback?skill=skill-zeta", json.dumps(zeta_form).encode(), port=port)
        self.assertEqual(status, 200, saved)
        alpha_view = self.review_skill("skill-alpha", port)
        self.assertEqual(alpha_view["feedback"]["items"], [])
        self.assertFalse(alpha_feedback.exists())
        alpha_form = self.feedback_form(alpha_fp, "alpha agrees")
        status, saved, _ = self.request(
            "POST", "/api/feedback?skill=skill-alpha", json.dumps(alpha_form).encode(), port=port)
        self.assertEqual(status, 200, saved)
        zeta_notes = [item["note"] for item in self.review_skill("skill-zeta", port)["feedback"]["items"]]
        alpha_notes = [item["note"] for item in self.review_skill("skill-alpha", port)["feedback"]["items"]]
        self.assertEqual(zeta_notes, ["zeta agrees"])
        self.assertEqual(alpha_notes, ["alpha agrees"])
        stored_zeta = json.loads((index_path.parent / "zeta-feedback.json").read_text())
        stored_alpha = json.loads(alpha_feedback.read_text())
        self.assertEqual(stored_zeta["items"][0]["note"], "zeta agrees")
        self.assertEqual(stored_alpha["items"][0]["note"], "alpha agrees")
        self.assertNotEqual(stored_zeta["items"][0]["fingerprint"], stored_alpha["items"][0]["fingerprint"])

    def test_identical_case_bytes_cannot_replay_onto_another_skill(self):
        shared = self.root / "shared-evidence"
        zeta_manifest, zeta_feedback = self.plant_manifest(
            self.root / "zeta", "skill-zeta", "SAME-PROMPT-9f3a", shared, b'{"kind":"same-trace"}\n')
        alpha_manifest, alpha_feedback = self.plant_manifest(
            self.root / "alpha", "skill-alpha", "SAME-PROMPT-9f3a", shared, b'{"kind":"same-trace"}\n')
        index_path = self.write_index(self.root / "catalog", [
            {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(zeta_feedback)},
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
        ])
        _, port = self.open_index(index_path)
        zeta = self.review_skill("skill-zeta", port)
        alpha = self.review_skill("skill-alpha", port)
        self.assertEqual(zeta["manifest"]["cases"][0]["prompt"], alpha["manifest"]["cases"][0]["prompt"])
        self.assertEqual(zeta["manifest"]["cases"][0]["id"], alpha["manifest"]["cases"][0]["id"])
        self.assertEqual(zeta["manifest"]["title"], "skill-zeta")
        self.assertEqual(alpha["manifest"]["title"], "skill-alpha")
        zeta_grade = binding(zeta, "shared-grade")["fingerprint"]
        alpha_grade = binding(alpha, "shared-grade")["fingerprint"]
        zeta_subject = next(item["fingerprint"] for item in zeta["bindings"]
                            if item["record_type"] == "subject" and item["subject_id"] == "shared-case")
        alpha_subject = next(item["fingerprint"] for item in alpha["bindings"]
                             if item["record_type"] == "subject" and item["subject_id"] == "shared-case")
        self.assertNotEqual(zeta_grade, alpha_grade)
        self.assertNotEqual(zeta_subject, alpha_subject)
        status, zeta_trace, _ = self.request("GET", "/evidence/shared-trace?skill=skill-zeta", port=port)
        status_alpha, alpha_trace, _ = self.request("GET", "/evidence/shared-trace?skill=skill-alpha", port=port)
        self.assertEqual(status, 200)
        self.assertEqual(status_alpha, 200)
        self.assertEqual(zeta_trace, alpha_trace)
        form = self.feedback_form(zeta_grade, "replay me")
        status, saved, _ = self.request(
            "POST", "/api/feedback?skill=skill-zeta", json.dumps(form).encode(), port=port)
        self.assertEqual(status, 200, saved)
        zeta_bytes = zeta_feedback.read_bytes()
        status, rejected_raw, _ = self.request(
            "POST", "/api/feedback?skill=skill-alpha", json.dumps(form).encode(), port=port)
        rejected = json.loads(rejected_raw.decode())
        self.assertEqual(status, 409, rejected)
        self.assertIn("Not saved", rejected["error"])
        self.assertIsNone(rejected["item"])
        self.assertFalse(alpha_feedback.exists())
        self.assertEqual(zeta_feedback.read_bytes(), zeta_bytes)
        note = self.feedback_form(zeta_subject, "subject replay", judgment=None, grade_id=None)
        status, saved, _ = self.request(
            "POST", "/api/feedback?skill=skill-zeta", json.dumps(note).encode(), port=port)
        self.assertEqual(status, 200, saved)
        status, rejected_raw, _ = self.request(
            "POST", "/api/feedback?skill=skill-alpha", json.dumps(note).encode(), port=port)
        rejected = json.loads(rejected_raw.decode())
        self.assertEqual(status, 409, rejected)
        self.assertFalse(alpha_feedback.exists())
        own = self.feedback_form(alpha_grade, "alpha's own grade")
        status, saved, _ = self.request(
            "POST", "/api/feedback?skill=skill-alpha", json.dumps(own).encode(), port=port)
        self.assertEqual(status, 200, saved)
        self.assertEqual(
            [item["note"] for item in json.loads(alpha_feedback.read_text())["items"]],
            ["alpha's own grade"])
        self.assertEqual(
            [item["note"] for item in json.loads(zeta_feedback.read_text())["items"]],
            ["replay me", "subject replay"])

    def test_index_startup_rejects_bad_config_and_shared_destinations(self):
        def expect(index_path, text):
            with self.subTest(text=text):
                with self.assertRaises(review.ConfigError) as caught:
                    review.load_index(index_path)
                self.assertIn(text, str(caught.exception))
                self.assertNotIn(str(self.root), str(caught.exception))

        broken = self.root / "broken-index.json"
        broken.write_text("{")
        expect(broken, "malformed JSON")
        shape = self.root / "shape"
        index_path = self.write_index(shape, [])
        index_path.write_text(json.dumps({"repository": "repo-one"}))
        expect(index_path, "repository and skills")
        index_path.write_text(json.dumps({
            "repository": "repo-one", "skills": [], "path": str(self.root),
        }))
        expect(index_path, "repository and skills")
        index_path.write_text(json.dumps({"repository": "../secret", "skills": []}))
        expect(index_path, "repository is missing")
        index_path.write_text(json.dumps({"repository": "repo-one", "skills": []}))
        expect(index_path, "non-empty")
        zeta_manifest, zeta_feedback = self.plant_manifest(
            self.root / "zeta", "skill-zeta", "ZETA-PROMPT-9f3a",
            self.root / "zeta-evidence", b"ZETA-TRACE-9f3a\n")
        alpha_manifest, alpha_feedback = self.plant_manifest(
            self.root / "alpha", "skill-alpha", "ALPHA-PROMPT-9f3a",
            self.root / "alpha-evidence", b"ALPHA-TRACE-9f3a\n")
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [{"id": "../secret", "manifest": "missing.json", "feedback": "missing-feedback.json"}],
        }))
        expect(index_path, "skill id")
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [
                {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(zeta_feedback)},
                {"id": "skill-zeta", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
            ],
        }))
        expect(index_path, "duplicated")
        mismatch = json.loads(zeta_manifest.read_text())
        mismatch["skill"]["name"] = "skill-alpha"
        zeta_manifest.write_text(json.dumps(mismatch))
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [
                {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(zeta_feedback)},
                {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
            ],
        }))
        expect(index_path, "does not match")
        mismatch["skill"]["name"] = "skill-zeta"
        zeta_manifest.write_text(json.dumps(mismatch))
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [{"id": "skill-zeta", "manifest": str(self.root / "absent.json"), "feedback": str(zeta_feedback)}],
        }))
        expect(index_path, "not usable")
        shared_feedback = self.root / "shared-feedback.json"
        shared_feedback.write_text('{"items":[]}\n')
        alias = self.root / "alias-feedback.json"
        alias.symlink_to(shared_feedback)
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [
                {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(alias)},
                {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(shared_feedback)},
            ],
        }))
        expect(index_path, "share a feedback destination")
        alias.unlink()
        os.link(shared_feedback, alias)
        expect(index_path, "share a feedback destination")
        alias.unlink()
        lexical = self.root / "lexical"
        index_path = self.write_index(lexical, [])
        nested = lexical / "zeta"
        nested.mkdir()
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [
                {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": "zeta/feedback.json"},
                {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": "zeta/../zeta/feedback.json"},
            ],
        }))
        expect(index_path, "share a feedback destination")
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [
                {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(alpha_manifest)},
                {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
            ],
        }))
        expect(index_path, "overlaps a review input")
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [
                {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(index_path)},
                {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
            ],
        }))
        expect(index_path, "overlaps a review input")
        trace = self.root / "zeta-evidence" / "trace.json"
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [
                {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(trace)},
                {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
            ],
        }))
        expect(index_path, "overlaps a review input")
        missing_trace = self.root / "zeta-evidence" / "gone.json"
        listed = json.loads(zeta_manifest.read_text())
        listed["files"].append({"id": "gone-trace", "path": "gone.json"})
        zeta_manifest.write_text(json.dumps(listed))
        index_path.write_text(json.dumps({
            "repository": "repo-one",
            "skills": [
                {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(missing_trace)},
                {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
            ],
        }))
        expect(index_path, "overlaps a review input")
        stderr = io.StringIO()
        with self.assertRaises(SystemExit) as caught:
            with contextlib.redirect_stderr(stderr):
                review.main(["--index", str(index_path), "--manifest", str(zeta_manifest), "--feedback", str(zeta_feedback), "--port", "0"])
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("--index", stderr.getvalue())
        stderr = io.StringIO()
        with self.assertRaises(SystemExit) as caught:
            with contextlib.redirect_stderr(stderr):
                review.main(["--manifest", str(zeta_manifest), "--port", "0"])
        self.assertEqual(caught.exception.code, 2)

    def test_broken_evidence_stays_a_manifest_error(self):
        zeta_manifest, zeta_feedback = self.plant_manifest(
            self.root / "zeta", "skill-zeta", "ZETA-PROMPT-9f3a",
            self.root / "zeta-evidence", b"ZETA-TRACE-9f3a\n")
        alpha_manifest, alpha_feedback = self.plant_manifest(
            self.root / "alpha", "skill-alpha", "ALPHA-PROMPT-9f3a",
            self.root / "alpha-evidence", b"ALPHA-TRACE-9f3a\n")
        listed = json.loads(zeta_manifest.read_text())
        listed["files"].append({"id": "gone-trace", "path": "gone.json"})
        listed["files"].append({"id": "dir-trace", "path": "not-a-file"})
        zeta_manifest.write_text(json.dumps(listed))
        (self.root / "zeta-evidence" / "not-a-file").mkdir()
        index_path = self.write_index(self.root / "catalog", [
            {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(zeta_feedback)},
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
        ])
        repository, sources = review.load_index(index_path)
        self.assertEqual(repository, "repo-one")
        self.assertEqual([source.skill_id for source in sources], ["skill-zeta", "skill-alpha"])
        _, port = self.open_index(index_path)
        status, data, _ = self.request("GET", "/api/review?skill=skill-zeta", port=port)
        self.assertEqual(status, 200, data)
        self.assertNotIn(str(self.root).encode(), data)
        payload = json.loads(data.decode())
        self.assertEqual(payload["manifest"]["cases"][0]["prompt"], "ZETA-PROMPT-9f3a")
        messages = [item["message"] for item in payload["errors"]]
        self.assertTrue(any("gone-trace" in message or "outside" in message for message in messages), messages)
        alpha_payload = self.review_skill("skill-alpha", port)
        self.assertEqual(alpha_payload["manifest"]["cases"][0]["prompt"], "ALPHA-PROMPT-9f3a")
        self.assertEqual(alpha_payload["errors"], [])

    def test_runtime_retarget_cannot_overwrite_another_skill_input(self):
        zeta_manifest, zeta_feedback = self.plant_manifest(
            self.root / "zeta", "skill-zeta", "ZETA-PROMPT-9f3a",
            self.root / "zeta-evidence", b"ZETA-TRACE-9f3a\n")
        alpha_manifest, alpha_feedback = self.plant_manifest(
            self.root / "alpha", "skill-alpha", "ALPHA-PROMPT-9f3a",
            self.root / "alpha-evidence", b"ALPHA-TRACE-9f3a\n")
        notes = self.root / "zeta-evidence" / "notes.json"
        index_path = self.write_index(self.root / "catalog", [
            {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(notes)},
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
        ])
        _, port = self.open_index(index_path)
        zeta_fp = self.grade_fingerprint("skill-zeta", port)
        alpha_fp = self.grade_fingerprint("skill-alpha", port)
        status, saved, _ = self.request(
            "POST", "/api/feedback?skill=skill-zeta",
            json.dumps(self.feedback_form(zeta_fp, "zeta note")).encode(), port=port)
        self.assertEqual(status, 200, saved)
        status, saved, _ = self.request(
            "POST", "/api/feedback?skill=skill-alpha",
            json.dumps(self.feedback_form(alpha_fp, "alpha note")).encode(), port=port)
        self.assertEqual(status, 200, saved)
        alpha_bytes = alpha_feedback.read_bytes()
        manifest_bytes = alpha_manifest.read_bytes()
        trace_bytes = (self.root / "alpha-evidence" / "trace.json").read_bytes()
        index_bytes = index_path.read_bytes()
        def rejected_save(note, fingerprint):
            status, raw, _ = self.request(
                "POST", "/api/feedback?skill=skill-zeta",
                json.dumps(self.feedback_form(fingerprint, note)).encode(), port=port)
            body = json.loads(raw.decode())
            self.assertEqual(status, 400, body)
            self.assertIn("overlap", body["error"])

        notes.unlink()
        notes.symlink_to(alpha_feedback)
        rejected_save("overwrite alpha feedback", zeta_fp)
        self.assertEqual(alpha_feedback.read_bytes(), alpha_bytes)
        notes.unlink()
        notes.symlink_to(alpha_manifest)
        rejected_save("overwrite alpha manifest", zeta_fp)
        self.assertEqual(alpha_manifest.read_bytes(), manifest_bytes)
        notes.unlink()
        os.link(self.root / "alpha-evidence" / "trace.json", notes)
        rejected_save("overwrite alpha trace", zeta_fp)
        self.assertEqual((self.root / "alpha-evidence" / "trace.json").read_bytes(), trace_bytes)
        notes.unlink()
        notes.symlink_to(index_path)
        rejected_save("overwrite index", zeta_fp)
        self.assertEqual(index_path.read_bytes(), index_bytes)
        notes.unlink()
        notes.write_text(json.dumps({"items": json.loads(alpha_bytes)["items"]}))
        original_notes = notes.read_bytes()
        listed = json.loads(zeta_manifest.read_text())
        listed["files"].append({"id": "notes-file", "path": "notes.json"})
        zeta_manifest.write_text(json.dumps(listed))
        refreshed = self.grade_fingerprint("skill-zeta", port)
        rejected_save("overwrite listed notes", refreshed)
        self.assertEqual(notes.read_bytes(), original_notes)
        self.assertEqual(alpha_feedback.read_bytes(), alpha_bytes)

    def test_concurrent_feedback_writes_stay_on_the_selected_skill(self):
        zeta_manifest, zeta_feedback = self.plant_manifest(
            self.root / "zeta", "skill-zeta", "ZETA-PROMPT-9f3a",
            self.root / "zeta-evidence", b"ZETA-TRACE-9f3a\n")
        alpha_manifest, alpha_feedback = self.plant_manifest(
            self.root / "alpha", "skill-alpha", "ALPHA-PROMPT-9f3a",
            self.root / "alpha-evidence", b"ALPHA-TRACE-9f3a\n")
        index_path = self.write_index(self.root / "catalog", [
            {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(zeta_feedback)},
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
        ])
        _, port = self.open_index(index_path)
        zeta_fp = self.grade_fingerprint("skill-zeta", port)
        alpha_fp = self.grade_fingerprint("skill-alpha", port)
        raced = []
        barrier = threading.Barrier(2)

        def race_zeta(note):
            barrier.wait(timeout=5)
            status, data, _ = self.request(
                "POST", "/api/feedback?skill=skill-zeta",
                json.dumps(self.feedback_form(zeta_fp, note)).encode(), port=port)
            raced.append((status, json.loads(data.decode())))

        racers = [
            threading.Thread(target=race_zeta, args=("racer-a",)),
            threading.Thread(target=race_zeta, args=("racer-b",)),
        ]
        for thread in racers:
            thread.start()
        for thread in racers:
            thread.join(timeout=5)
        self.assertEqual(sorted(item[0] for item in raced), [200, 409], raced)
        stored = json.loads(zeta_feedback.read_text())["items"]
        self.assertEqual(len(stored), 1)
        self.assertIn(stored[0]["note"], {"racer-a", "racer-b"})
        self.assertFalse(alpha_feedback.exists())
        saved_note = stored[0]["note"]
        crossed = []
        barrier = threading.Barrier(2)

        def save(skill, payload):
            barrier.wait(timeout=5)
            status, data, _ = self.request(
                "POST", "/api/feedback?skill=" + skill, json.dumps(payload).encode(), port=port)
            crossed.append((skill, status, json.loads(data.decode())))

        threads = [
            threading.Thread(target=save, args=(
                "skill-zeta", self.feedback_form(zeta_fp, "zeta updated", base_revision=1))),
            threading.Thread(target=save, args=(
                "skill-alpha", self.feedback_form(alpha_fp, "alpha concurrent"))),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=5)
        self.assertEqual(sorted(item[0] for item in crossed), ["skill-alpha", "skill-zeta"], crossed)
        self.assertTrue(all(item[1] == 200 for item in crossed), crossed)
        zeta_items = json.loads(zeta_feedback.read_text())["items"]
        alpha_items = json.loads(alpha_feedback.read_text())["items"]
        self.assertEqual([item["note"] for item in zeta_items], ["zeta updated"])
        self.assertEqual(zeta_items[0]["revision"], 2)
        self.assertNotEqual(saved_note, "zeta updated")
        self.assertEqual([item["note"] for item in alpha_items], ["alpha concurrent"])

    def reject_skill_save(self, port, fingerprint, note, feedback_path, original):
        status, raw, _ = self.request(
            "POST", "/api/feedback?skill=skill-zeta",
            json.dumps(self.feedback_form(fingerprint, note, base_revision=1)).encode(), port=port)
        body = json.loads(raw.decode())
        self.assertEqual(status, 400, body)
        self.assertIn("Not saved", body["error"])
        self.assertNotIn("ALPHA-PROMPT-9f3a", body["error"])
        self.assertNotIn("ALPHA-TRACE-9f3a", raw.decode())
        self.assertEqual(feedback_path.read_bytes(), original)

    def test_replaced_manifest_is_not_served_or_saved_for_that_skill(self):
        zeta_manifest, zeta_feedback = self.plant_manifest(
            self.root / "zeta", "skill-zeta", "ZETA-PROMPT-9f3a",
            self.root / "zeta-evidence", b"ZETA-TRACE-9f3a\n")
        alpha_manifest, alpha_feedback = self.plant_manifest(
            self.root / "alpha", "skill-alpha", "ALPHA-PROMPT-9f3a",
            self.root / "alpha-evidence", b"ALPHA-TRACE-9f3a\n")
        original = zeta_manifest.read_text()
        index_path = self.write_index(self.root / "catalog", [
            {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(zeta_feedback)},
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
        ])
        _, port = self.open_index(index_path)
        zeta_fp = self.grade_fingerprint("skill-zeta", port)
        alpha_fp = self.grade_fingerprint("skill-alpha", port)
        status, saved, _ = self.request(
            "POST", "/api/feedback?skill=skill-zeta",
            json.dumps(self.feedback_form(zeta_fp, "zeta note")).encode(), port=port)
        self.assertEqual(status, 200, saved)
        saved_bytes = zeta_feedback.read_bytes()
        drifted = json.loads(original)
        drifted["skill"]["name"] = "skill-alpha"
        zeta_manifest.write_text(json.dumps(drifted))
        status, raw, _ = self.request("GET", "/api/review?skill=skill-zeta", port=port)
        self.assertEqual(status, 200, raw)
        body = json.loads(raw.decode())
        self.assertIsNone(body["manifest"])
        self.assertEqual(body["bindings"], [])
        self.assertTrue(any("does not match" in item["message"] for item in body["errors"]))
        self.assertNotIn(b"ZETA-PROMPT-9f3a", raw)
        self.assertNotIn(b"ALPHA-PROMPT-9f3a", raw)
        status, evidence, _ = self.request("GET", "/evidence/shared-trace?skill=skill-zeta", port=port)
        self.assertEqual(status, 404, evidence)
        self.assertNotIn(b"ZETA-TRACE-9f3a", evidence)
        self.assertNotIn(b"ALPHA-TRACE-9f3a", evidence)
        self.reject_skill_save(port, zeta_fp, "stale after name drift", zeta_feedback, saved_bytes)
        self.reject_skill_save(port, alpha_fp, "fresh after name drift", zeta_feedback, saved_bytes)
        zeta_manifest.unlink()
        zeta_manifest.symlink_to(alpha_manifest)
        status, raw, _ = self.request("GET", "/api/review?skill=skill-zeta", port=port)
        self.assertEqual(status, 200, raw)
        body = json.loads(raw.decode())
        self.assertIsNone(body["manifest"])
        self.assertEqual(body["bindings"], [])
        self.assertNotIn(b"ALPHA-PROMPT-9f3a", raw)
        self.assertNotIn(b"B extra", raw)
        status, evidence, _ = self.request("GET", "/evidence/shared-trace?skill=skill-zeta", port=port)
        self.assertEqual(status, 404, evidence)
        self.assertNotEqual(evidence, b"ALPHA-TRACE-9f3a\n")
        self.assertNotIn(b"ALPHA-TRACE-9f3a", evidence)
        self.reject_skill_save(port, zeta_fp, "stale after retarget", zeta_feedback, saved_bytes)
        self.reject_skill_save(port, alpha_fp, "fresh after retarget", zeta_feedback, saved_bytes)
        alpha_view = self.review_skill("skill-alpha", port)
        self.assertEqual(alpha_view["manifest"]["cases"][0]["prompt"], "ALPHA-PROMPT-9f3a")
        self.assertEqual(alpha_feedback.exists(), False)
        zeta_manifest.unlink()
        zeta_manifest.write_text(original)
        restored = self.review_skill("skill-zeta", port)
        self.assertEqual(restored["manifest"]["skill"]["name"], "skill-zeta")
        self.assertEqual(restored["manifest"]["cases"][0]["prompt"], "ZETA-PROMPT-9f3a")
        self.assertEqual(restored["feedback"]["items"][0]["note"], "zeta note")
        status, evidence, _ = self.request("GET", "/evidence/shared-trace?skill=skill-zeta", port=port)
        self.assertEqual(status, 200)
        self.assertEqual(evidence, b"ZETA-TRACE-9f3a\n")
        restored_fp = binding(restored, "shared-grade")["fingerprint"]
        status, saved, _ = self.request(
            "POST", "/api/feedback?skill=skill-zeta",
            json.dumps(self.feedback_form(restored_fp, "zeta restored", base_revision=1)).encode(),
            port=port)
        self.assertEqual(status, 200, saved)
        self.assertEqual(json.loads(zeta_feedback.read_text())["items"][0]["note"], "zeta restored")
        self.assertFalse(alpha_feedback.exists())

    def test_unusable_evidence_root_keeps_listed_paths_for_overlap(self):
        alpha_manifest, alpha_feedback = self.plant_manifest(
            self.root / "alpha", "skill-alpha", "ALPHA-PROMPT-9f3a",
            self.root / "alpha-evidence", b"ALPHA-TRACE-9f3a\n")
        missing = self.root / "missing-root"
        zeta_manifest, zeta_feedback = self.plant_manifest(
            self.root / "zeta", "skill-zeta", "ZETA-PROMPT-9f3a",
            self.root / "zeta-evidence", b"ZETA-TRACE-9f3a\n")
        listed = json.loads(zeta_manifest.read_text())
        listed["evidence_root"] = str(missing)
        zeta_manifest.write_text(json.dumps(listed))
        index_path = self.write_index(self.root / "catalog", [
            {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(zeta_feedback)},
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
        ])
        _, port = self.open_index(index_path)
        status, raw, _ = self.request("GET", "/api/review?skill=skill-zeta", port=port)
        self.assertEqual(status, 200, raw)
        payload = json.loads(raw.decode())
        self.assertEqual(payload["manifest"]["cases"][0]["prompt"], "ZETA-PROMPT-9f3a")
        self.assertTrue(any("not a directory" in item["message"] for item in payload["errors"]))
        status, evidence, _ = self.request("GET", "/evidence/shared-trace?skill=skill-zeta", port=port)
        self.assertEqual(status, 404, evidence)
        self.assertNotIn(b"ZETA-TRACE-9f3a", evidence)
        blocked = self.write_index(self.root / "blocked-missing", [
            {"id": "skill-zeta", "manifest": str(zeta_manifest), "feedback": str(missing / "trace.json")},
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
        ])
        with self.assertRaises(review.ConfigError) as caught:
            review.load_index(blocked)
        self.assertIn("overlaps a review input", str(caught.exception))
        file_root = self.root / "file-root"
        file_root.write_text("not a directory")
        file_listed = json.loads(zeta_manifest.read_text())
        file_listed["evidence_root"] = str(file_root)
        file_manifest = self.root / "file-manifest.json"
        file_manifest.write_text(json.dumps(file_listed))
        open_root = self.write_index(self.root / "open-file-root", [
            {"id": "skill-zeta", "manifest": str(file_manifest), "feedback": str(self.root / "safe-feedback.json")},
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
        ])
        _, file_port = self.open_index(open_root)
        status, raw, _ = self.request("GET", "/api/review?skill=skill-zeta", port=file_port)
        self.assertEqual(status, 200, raw)
        payload = json.loads(raw.decode())
        self.assertEqual(payload["manifest"]["cases"][0]["prompt"], "ZETA-PROMPT-9f3a")
        self.assertTrue(any("not a directory" in item["message"] for item in payload["errors"]))
        blocked_file = self.write_index(self.root / "blocked-file-root", [
            {"id": "skill-zeta", "manifest": str(file_manifest), "feedback": str(file_root / "trace.json")},
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
        ])
        with self.assertRaises(review.ConfigError) as caught:
            review.load_index(blocked_file)
        self.assertIn("overlaps a review input", str(caught.exception))

    def test_review_read_hides_feedback_aliased_to_another_skill(self):
        alpha_manifest, alpha_feedback = self.plant_manifest(
            self.root / "alpha", "skill-alpha", "ALPHA-PROMPT-9f3a",
            self.root / "alpha-evidence", b"ALPHA-TRACE-9f3a\n")
        beta_manifest, beta_feedback = self.plant_manifest(
            self.root / "beta", "skill-beta", "BETA-PROMPT-9f3a",
            self.root / "beta-evidence", b"BETA-TRACE-SECRET-9f3a\n")
        index_path = self.write_index(self.root / "catalog", [
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(alpha_feedback)},
            {"id": "skill-beta", "manifest": str(beta_manifest), "feedback": str(beta_feedback)},
        ])
        _, port = self.open_index(index_path)
        beta_fp = self.grade_fingerprint("skill-beta", port)
        note = "BETA-PRIVATE-NOTE-9f3a"
        status, saved, _ = self.request(
            "POST", "/api/feedback?skill=skill-beta",
            json.dumps(self.feedback_form(beta_fp, note)).encode(), port=port)
        self.assertEqual(status, 200, saved)
        beta_bytes = beta_feedback.read_bytes()
        manifest_bytes = beta_manifest.read_bytes()
        trace_bytes = (self.root / "beta-evidence" / "trace.json").read_bytes()

        def retarget(make):
            if alpha_feedback.is_symlink() or alpha_feedback.exists():
                alpha_feedback.unlink()
            make()

        def assert_hidden(label):
            status, raw, _ = self.request("GET", "/api/review?skill=skill-alpha", port=port)
            self.assertEqual(status, 200, raw)
            body = json.loads(raw.decode())
            self.assertEqual(body["manifest"]["cases"][0]["prompt"], "ALPHA-PROMPT-9f3a", label)
            self.assertEqual(body["feedback"]["items"], [], label)
            self.assertEqual(body["feedback"]["error"], "Feedback path overlaps a review input.", label)
            self.assertNotIn(note, raw.decode())
            self.assertNotIn("BETA-TRACE-SECRET-9f3a", raw.decode())
            self.assertNotIn(str(self.root), raw.decode())
            self.assertEqual(beta_feedback.read_bytes(), beta_bytes)
            self.assertEqual(beta_manifest.read_bytes(), manifest_bytes)
            self.assertEqual((self.root / "beta-evidence" / "trace.json").read_bytes(), trace_bytes)

        retarget(lambda: alpha_feedback.symlink_to(beta_feedback))
        assert_hidden("symlink feedback")
        retarget(lambda: os.link(beta_feedback, alpha_feedback))
        assert_hidden("hardlink feedback")
        retarget(lambda: alpha_feedback.symlink_to(beta_manifest))
        assert_hidden("symlink manifest")
        retarget(lambda: os.link(beta_manifest, alpha_feedback))
        assert_hidden("hardlink manifest")
        trace = self.root / "beta-evidence" / "trace.json"
        retarget(lambda: alpha_feedback.symlink_to(trace))
        assert_hidden("symlink evidence")
        retarget(lambda: os.link(trace, alpha_feedback))
        assert_hidden("hardlink evidence")
        beta_view = self.review_skill("skill-beta", port)
        self.assertEqual(beta_view["feedback"]["items"][0]["note"], note)

    def test_startup_rejects_ambiguous_feedback_spellings(self):
        alpha_manifest, _alpha_feedback = self.plant_manifest(
            self.root / "alpha", "skill-alpha", "ALPHA-PROMPT-9f3a",
            self.root / "alpha-evidence", b"ALPHA-TRACE-9f3a\n")
        beta_manifest, _beta_feedback = self.plant_manifest(
            self.root / "beta", "skill-beta", "BETA-PROMPT-9f3a",
            self.root / "beta-evidence", b"BETA-TRACE-9f3a\n")
        case_index = self.write_index(self.root / "case-catalog", [
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(self.root / "Feedback.json")},
            {"id": "skill-beta", "manifest": str(beta_manifest), "feedback": str(self.root / "feedback.json")},
        ])
        with self.assertRaises(review.ConfigError) as caught:
            review.load_index(case_index)
        self.assertIn("ambiguous feedback paths", str(caught.exception))
        self.assertNotIn(str(self.root), str(caught.exception))
        nfc = self.root / "caf\u00e9-feedback.json"
        nfd = self.root / "cafe\u0301-feedback.json"
        unicode_index = self.write_index(self.root / "unicode-catalog", [
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(nfc)},
            {"id": "skill-beta", "manifest": str(beta_manifest), "feedback": str(nfd)},
        ])
        with self.assertRaises(review.ConfigError) as caught:
            review.load_index(unicode_index)
        self.assertIn("ambiguous feedback paths", str(caught.exception))
        listed = json.loads(beta_manifest.read_text())
        missing_root = self.root / "beta-evidence"
        listed["files"].append({"id": "later-trace", "path": "later.json"})
        beta_manifest.write_text(json.dumps(listed))
        evidence_index = self.write_index(self.root / "evidence-catalog", [
            {"id": "skill-alpha", "manifest": str(alpha_manifest), "feedback": str(missing_root / "LATER.JSON")},
            {"id": "skill-beta", "manifest": str(beta_manifest), "feedback": str(self.root / "beta-feedback.json")},
        ])
        with self.assertRaises(review.ConfigError) as caught:
            review.load_index(evidence_index)
        self.assertIn("ambiguous with a review input", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
