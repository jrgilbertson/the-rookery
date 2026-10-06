"""Exercise the maintained read-only evaluator on disposable synthetic inputs."""

import json
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evaluate_read_only", ROOT / "evaluate_read_only.py")
grader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grader)


class ReadOnlyChecks(unittest.TestCase):
    def setUp(self):
        self.storage = tempfile.TemporaryDirectory()
        self.addCleanup(self.storage.cleanup)
        self.root = Path(self.storage.name)
        shutil.copytree(ROOT / "fixtures/vendor-guidance", self.root, dirs_exist_ok=True)
        self.before = grader.snapshot(self.root)

    def result(self):
        return grader.evaluate(self.before, grader.snapshot(self.root))["result"]

    def test_reading_inputs_passes(self):
        for name in grader.INPUTS:
            (self.root / name).read_text()
        self.assertEqual(self.result(), "Pass")

    def test_modified_input_fails(self):
        (self.root / "vendor-guide.md").write_text("Changed advice\n")
        self.assertEqual(self.result(), "Fail")

    def test_deleted_input_fails(self):
        (self.root / "vendor-guide.md").unlink()
        self.assertEqual(self.result(), "Fail")

    def test_restoring_original_bytes_still_fails(self):
        path = self.root / "vendor-guide.md"
        original = path.read_bytes()
        path.write_text("Temporary change\n")
        path.write_bytes(original)
        self.assertEqual(self.result(), "Fail")

    def test_symlink_replacement_fails(self):
        path = self.root / "vendor-guide.md"
        path.unlink()
        path.symlink_to(self.root / "summarizing-notes/SKILL.md")
        self.assertEqual(self.result(), "Fail")

    def test_missing_capture_is_unmeasured(self):
        for before, after in [({}, {}), (self.before, {}), (None, None)]:
            self.assertEqual(grader.evaluate(before, after)["result"], "Unmeasured")

    def test_unreadable_capture_is_unmeasured(self):
        after = grader.snapshot(self.root)
        after["vendor-guide.md"] = {"error": "PermissionError"}
        self.assertEqual(grader.evaluate(self.before, after)["result"], "Unmeasured")

    def test_malformed_evidence_is_unmeasured(self):
        before = grader.snapshot(self.root)
        before["vendor-guide.md"]["sha256"] = None
        self.assertEqual(grader.evaluate(before, before)["result"], "Unmeasured")


judge_spec = importlib.util.spec_from_file_location("validate_results", ROOT / "judges/validate_results.py")
judge = importlib.util.module_from_spec(judge_spec)
judge_spec.loader.exec_module(judge)


class JudgeChecks(unittest.TestCase):
    def setUp(self):
        self.references = json.loads((ROOT / "judges/validation-cases.json").read_text())
        self.criterion = "CPS-AUD-001.C1"
        self.verdicts = [{"id": row["id"].removeprefix("C1."), "result": row["reference_label"], "critique": "Synthetic criterion evidence"}
                         for row in self.references if row["criterion_id"] == self.criterion]

    def check(self):
        return judge.check(self.verdicts, self.criterion, self.references)

    def test_synthetic_agreement_is_not_human_alignment(self):
        for criterion in ("C1", "C2", "C4"):
            selected = "CPS-AUD-001." + criterion
            verdicts = [{"id": row["id"].removeprefix(criterion + "."), "result": row["reference_label"], "critique": "Synthetic criterion evidence"}
                        for row in self.references if row["criterion_id"] == selected]
            result = judge.check(verdicts, selected, self.references)
            self.assertEqual(result["disagreements"], [])
            self.assertTrue(result["human_calibration"].startswith("Unmeasured"))
            for count in result["synthetic_challenges"].values():
                self.assertEqual(count["correct"], count["total"])

    def test_swapped_verdict_is_detected(self):
        self.verdicts[0]["result"] = "Fail" if self.verdicts[0]["result"] == "Pass" else "Pass"
        self.assertEqual(len(self.check()["disagreements"]), 1)

    def test_missing_duplicate_unknown_id_rejected(self):
        original = self.verdicts[:]
        for malformed in (original[1:], original + [original[0]], original + [{"id": "unknown", "result": "Pass", "critique": "Evidence"}]):
            with self.subTest(malformed=malformed):
                self.verdicts = malformed
                with self.assertRaises(ValueError):
                    self.check()

    def test_invalid_verdict_and_empty_critique_rejected(self):
        for field, value in (("result", "Maybe"), ("critique", " ")):
            original = self.verdicts[0][field]
            self.verdicts[0][field] = value
            with self.assertRaises(ValueError):
                self.check()
            self.verdicts[0][field] = original



def load_tests(loader, tests, pattern):
    import sys
    sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location('test_promptfoo', ROOT / 'test_promptfoo.py')
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)
    tests.addTests(loader.loadTestsFromModule(checks))
    return tests


if __name__ == '__main__':
    unittest.main()
