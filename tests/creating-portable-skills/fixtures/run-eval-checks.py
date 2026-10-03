"""Exercise the maintained read-only evaluator on disposable synthetic inputs."""

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


if __name__ == "__main__":
    unittest.main()
