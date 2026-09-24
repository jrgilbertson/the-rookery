#!/usr/bin/env python3
"""Exercise the shipped map helper against disposable user homes."""

import contextlib
import fcntl
import io
import json
import os
import runpy
import select
import signal
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
HELPER = HERE.parents[2] / "skills/personal-chief-of-staff/scripts/source-bindings.py"
MAP_RELATIVE = Path(".config/the-rookery/personal-chief-of-staff/sources.json")


class SetupChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pcos-setup-checks-")
        self.addCleanup(self.temp.cleanup)
        self.test_home = Path(self.temp.name) / "user"
        self.test_home.mkdir()
        self.map_path = self.test_home / MAP_RELATIVE
        self.strategy = json.loads((HERE / "source-bindings/setup-strategy.json").read_text())
        self.learning = json.loads((HERE / "source-bindings/setup-learning.json").read_text())

    def call(self, *args, payload=None):
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(Path, "home", return_value=self.test_home), \
             patch.object(sys, "argv", [str(HELPER), *args]), \
             patch.object(sys, "stdin", io.StringIO(json.dumps(payload) if payload is not None else "")), \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            try:
                runpy.run_path(str(HELPER), run_name="__main__")
            except SystemExit as exit_result:
                code = exit_result.code
        return code, output.getvalue(), errors.getvalue()

    def snapshot(self):
        code, output, errors = self.call("snapshot")
        self.assertEqual((code, errors), (0, ""))
        return output.strip()

    def write(self, role, bindings, expected):
        return self.call("write", payload={"role": role, "bindings": bindings, "expected": expected})

    def test_approved_single_role_create_and_fresh_read(self):
        expected = self.snapshot()
        code, output, errors = self.write("strategy", self.strategy, expected)
        self.assertEqual((code, errors), (0, ""))
        self.assertEqual(json.loads(output)["roles"], {"strategy": self.strategy})
        self.assertEqual(stat.S_IMODE(self.map_path.stat().st_mode), 0o600)
        for parent in (self.map_path.parent, self.map_path.parent.parent, self.map_path.parent.parent.parent):
            self.assertEqual(stat.S_IMODE(parent.stat().st_mode), 0o700)
        code, output, errors = self.call("read")
        self.assertEqual((code, errors), (0, ""))
        self.assertEqual(json.loads(output)["roles"]["strategy"], self.strategy)

    def test_preserves_other_role_and_rejects_stale_snapshot(self):
        absent = self.snapshot()
        self.assertEqual(self.write("strategy", self.strategy, absent)[0], 0)
        before = self.map_path.read_bytes()
        code, _, errors = self.write("learning", self.learning, absent)
        self.assertNotEqual(code, 0)
        self.assertIn("changed", errors)
        self.assertEqual(self.map_path.read_bytes(), before)
        self.assertEqual(self.write("learning", self.learning, self.snapshot())[0], 0)
        roles = json.loads(self.map_path.read_text())["roles"]
        self.assertEqual(roles, {"strategy": self.strategy, "learning": self.learning})

    def test_rejects_changed_same_content_and_symlinked_targets(self):
        self.assertEqual(self.write("strategy", self.strategy, self.snapshot())[0], 0)
        expected = self.snapshot()
        content = self.map_path.read_bytes()
        replacement = self.map_path.with_name("replacement")
        replacement.write_bytes(content)
        os.replace(replacement, self.map_path)
        self.assertIn("changed", self.write("learning", self.learning, expected)[2])
        self.map_path.unlink()
        self.map_path.symlink_to(HERE / "source-bindings/valid.json")
        self.assertNotEqual(self.write("learning", self.learning, expected)[0], 0)
        self.assertTrue(self.map_path.is_symlink())
        self.map_path.unlink()
        self.map_path.parent.rename(self.map_path.parent.with_name("saved-parent"))
        self.map_path.parent.symlink_to(self.map_path.parent.with_name("saved-parent"), target_is_directory=True)
        self.assertNotEqual(self.write("learning", self.learning, "absent")[0], 0)

    def test_rejects_malformed_unreadable_and_unapproved_shape(self):
        self.map_path.parent.mkdir(parents=True)
        for specimen in ("malformed.txt", "duplicate.json", "unsupported.json"):
            before = (HERE / "source-bindings" / specimen).read_bytes()
            self.map_path.write_bytes(before)
            code, _, errors = self.write("strategy", self.strategy, "absent")
            self.assertNotEqual(code, 0)
            self.assertIn("source map unresolved", errors)
            self.assertEqual(self.map_path.read_bytes(), before)
        self.map_path.write_text('{"version":1,"roles":{}}')
        self.map_path.chmod(0)
        self.assertNotEqual(self.write("strategy", self.strategy, "absent")[0], 0)
        self.map_path.chmod(0o600)
        self.assertNotEqual(self.write("strategy", self.strategy, self.snapshot() + "x")[0], 0)
        self.assertEqual(json.loads(self.map_path.read_text())["roles"], {})

    def test_rejects_invalid_payload_and_lock_contention(self):
        expected = self.snapshot()
        for payload in ({"role": "strategy", "bindings": self.strategy},
                        {"role": "strategy", "bindings": [], "expected": expected},
                        {"role": "strategy", "bindings": self.strategy, "expected": expected, "approved": True}):
            self.assertNotEqual(self.call("write", payload=payload)[0], 0)
        self.assertFalse(self.map_path.exists())
        self.map_path.parent.mkdir(parents=True)
        lock_path = self.map_path.with_name("sources.json.lock")
        lock_fd = os.open(lock_path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertNotEqual(self.write("strategy", self.strategy, expected)[0], 0)
        finally:
            os.close(lock_fd)
        self.assertFalse(self.map_path.exists())
        lock_path.unlink()
        target = lock_path.with_name("lock-target")
        target.write_text("keep")
        lock_path.symlink_to(target)
        self.assertNotEqual(self.write("strategy", self.strategy, expected)[0], 0)
        self.assertEqual(target.read_text(), "keep")
        self.assertFalse(self.map_path.exists())

    def test_killed_writer_releases_lock_for_later_approved_write(self):
        self.assertEqual(self.write("strategy", self.strategy, self.snapshot())[0], 0)
        before = self.map_path.read_bytes()
        expected = self.snapshot()
        payload = json.dumps({"role": "learning", "bindings": self.learning, "expected": expected})
        lock_line = next(
            number for number, line in enumerate(HELPER.read_text().splitlines(), 1)
            if line.strip() == "current, actual = map_state(parent_fd)"
        )
        # The trace hook lives only in this external process, after the real helper takes its lock.
        child_code = """
import io
import runpy
import signal
import sys
from pathlib import Path

helper, payload, lock_line, test_home = sys.argv[1:]
Path.home = classmethod(lambda cls: cls(test_home))
def stop_after_lock(frame, event, arg):
    if (event == "line" and frame.f_code.co_filename == helper
            and frame.f_code.co_name == "write_map" and frame.f_lineno == int(lock_line)):
        print("LOCKED", flush=True)
        while True:
            signal.pause()
    return stop_after_lock

sys.argv = [helper, "write"]
sys.stdin = io.StringIO(payload)
sys.settrace(stop_after_lock)
runpy.run_path(helper, run_name="__main__")
"""
        process = subprocess.Popen(
            [sys.executable, "-c", child_code, str(HELPER), payload, str(lock_line), str(self.test_home)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        try:
            ready, _, _ = select.select([process.stdout], [], [], 5)
            self.assertTrue(ready, "writer did not reach its held lock")
            self.assertEqual(process.stdout.readline().strip(), "LOCKED")
            probe_fd = os.open(self.map_path.with_name("sources.json.lock"), os.O_RDWR | os.O_NOFOLLOW)
            try:
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(probe_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            finally:
                os.close(probe_fd)
        finally:
            if process.poll() is None:
                process.kill()
            process.communicate(timeout=5)
        self.assertEqual(process.returncode, -signal.SIGKILL)
        self.assertEqual(self.map_path.read_bytes(), before)
        lock_path = self.map_path.with_name("sources.json.lock")
        lock_inode = lock_path.stat().st_ino
        code, _, errors = self.write("learning", self.learning, expected)
        self.assertEqual((code, errors), (0, ""))
        self.assertEqual(json.loads(self.map_path.read_text())["roles"], {
            "strategy": self.strategy, "learning": self.learning,
        })
        self.assertTrue(lock_path.is_file())
        self.assertEqual(lock_path.stat().st_ino, lock_inode)
        self.assertEqual(stat.S_IMODE(lock_path.stat().st_mode), 0o600)


if __name__ == "__main__":
    unittest.main()
