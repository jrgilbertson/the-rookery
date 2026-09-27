import hashlib
import http.client
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

    def binding_record(self, subject_id, grade_id=None, port=None):
        payload = self.review(port)
        if grade_id is None:
            matches = [item for item in payload["bindings"]
                       if item.get("record_type") == "subject" and item.get("subject_id") == subject_id]
        else:
            matches = [item for item in payload["bindings"]
                       if item.get("subject_id") == subject_id and item.get("record_id") == grade_id]
        self.assertEqual(len(matches), 1, (subject_id, grade_id))
        return matches[0]

    def post(self, payload, headers=None, port=None):
        body = dict(payload)
        if "fingerprint" not in body:
            found = self.binding_record(body["subject_id"], body.get("grade_id"), port)
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
        self.assertEqual(training["proof"], "verified_trigger")
        self.assertEqual(training["selection"], "training")
        self.assertEqual(unverified["proof"], "unverified")
        self.assertEqual(unverified["selection"], "validation_used_for_selection")
        self.assertNotEqual(unverified["proof"], "verified_non_trigger")
        self.assertEqual(validation["proof"], "verified_non_trigger")
        self.assertEqual(validation["selection"], "validation")
        self.assertEqual(fresh["proof"], "verified_non_trigger")
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
        self.assertEqual(binding(payload, "train-grok-loaded")["proof"], "verified_trigger")
        self.assertEqual(binding(payload, "validation-grok-not-loaded")["proof"], "verified_non_trigger")

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


if __name__ == "__main__":
    unittest.main()
