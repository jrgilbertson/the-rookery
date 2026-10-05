"""Evidence-file handling for the C3 comparator and judge packet checker, through their real CLIs."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("evidence_checks", ROOT / "fixtures/run-eval-checks.py")
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)


def run(script, *args):
    return subprocess.run([sys.executable, str(ROOT / script), *map(str, args)], capture_output=True, text=True)


class SnapshotFileChecks(unittest.TestCase):
    def setUp(self):
        storage = tempfile.TemporaryDirectory()
        self.addCleanup(storage.cleanup)
        self.dir = Path(storage.name)
        shutil.copytree(ROOT / "fixtures/vendor-guidance", self.dir / "inputs")
        self.before = self.dir / "before.json"
        self.before.write_text(run("evaluate_read_only.py", "snapshot", self.dir / "inputs").stdout)
        self.after = self.dir / "after.json"
        self.after.write_text(self.before.read_text())

    def compare(self):
        completed = run("evaluate_read_only.py", "compare", self.before, self.after)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def test_valid_snapshots_pass(self):
        self.assertEqual(self.compare()["result"], "Pass")

    def test_unusable_snapshot_file_is_unmeasured(self):
        text = self.before.read_text()
        corruptions = {"missing": lambda path: path.unlink(), "empty": lambda path: path.write_text(""),
                       "truncated": lambda path: path.write_text(text[: len(text) // 2]),
                       "directory": lambda path: (path.unlink(), path.mkdir())}
        for side in ("before", "after"):
            for name, corrupt in corruptions.items():
                with self.subTest(side=side, corruption=name):
                    path = getattr(self, side)
                    corrupt(path)
                    try:
                        result = self.compare()
                        self.assertEqual(result["criterion_id"], "CPS-AUD-001.C3")
                        self.assertEqual(result["result"], "Unmeasured")
                    finally:
                        if path.is_dir():
                            path.rmdir()
                        path.write_text(text)


class JudgePacketChecks(unittest.TestCase):
    def setUp(self):
        self.references = json.loads((ROOT / "judges/validation-cases.json").read_text())
        self.criterion = "CPS-AUD-001.C1"
        self.challenges = [{"id": row["id"].removeprefix("C1."), "result": row["reference_label"], "critique": "Synthetic evidence"}
                           for row in self.references if row["criterion_id"] == self.criterion]
        self.actual = [{"id": identifier, "result": "Pass", "critique": "Actual response evidence"}
                       for identifier in ("response-a", "response-b")]

    def check(self, verdicts):
        return legacy.judge.check(verdicts, self.criterion, self.references)

    def test_challenge_only_and_full_packets_pass(self):
        for verdicts in (self.challenges, self.challenges + self.actual):
            with self.subTest(ids=len(verdicts)):
                result = self.check(verdicts)
                self.assertEqual(result["disagreements"], [])
                self.assertEqual(sum(count["total"] for count in result["synthetic_challenges"].values()), len(self.challenges))

    def test_partial_actual_packet_rejected(self):
        for actual in self.actual:
            with self.subTest(present=actual["id"]):
                with self.assertRaises(ValueError):
                    self.check(self.challenges + [actual])

    def test_cli_rejects_partial_actual_packet(self):
        with tempfile.TemporaryDirectory() as storage:
            packet = Path(storage) / "verdicts.json"
            packet.write_text(json.dumps(self.challenges + self.actual[:1]))
            completed = run("judges/validate_results.py", self.criterion, packet)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("Invalid judge evidence", completed.stderr)
        self.assertEqual(completed.stdout, "")


if __name__ == "__main__":
    unittest.main()
