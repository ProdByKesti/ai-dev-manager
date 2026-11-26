import importlib.util
from pathlib import Path
import subprocess
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_rust_toolchain.py"
spec = importlib.util.spec_from_file_location("check_rust_toolchain", SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class ToolchainChecks(unittest.TestCase):
    def run_tool(self, output, returncode=0):
        result = subprocess.CompletedProcess([], returncode, output, "")
        with mock.patch.object(check.shutil, "which", return_value="tool"), \
             mock.patch.object(check.subprocess, "run", return_value=result):
            return check.check_tool("rustc")

    def test_supported_stable_version(self):
        self.assertIsNone(self.run_tool("rustc 1.100.0 (abc 2026-01-01)\n"))
        self.assertIsNone(self.run_tool("rustc 1.101.0\n"))

    def test_missing_tool(self):
        with mock.patch.object(check.shutil, "which", return_value=None):
            self.assertIn("not found", check.check_tool("cargo"))

    def test_old_version(self):
        self.assertIn("too old", self.run_tool("rustc 1.99.0\n"))

    def test_prerelease_and_malformed_versions(self):
        for output in ("rustc 1.100.0-nightly\n", "unexpected\n", "cargo 1.100.0\n"):
            with self.subTest(output=output):
                self.assertIn("Unrecognized", self.run_tool(output))

    def test_failed_version_command(self):
        self.assertIn("exit 2", self.run_tool("", 2))

    def test_unlaunchable_and_timed_out_tool(self):
        for error in (OSError("unavailable"), subprocess.TimeoutExpired("tool", 10)):
            with self.subTest(error=error), mock.patch.object(check.shutil, "which", return_value="tool"), \
                 mock.patch.object(check.subprocess, "run", side_effect=error):
                self.assertIn("Cannot run", check.check_tool("rustc"))

    def test_main_fails_for_old_python_and_missing_tools(self):
        with mock.patch.object(check.sys, "version_info", (3, 10)), \
             mock.patch.object(check.shutil, "which", return_value=None), \
             mock.patch("sys.stderr"):
            self.assertEqual(check.main(), 1)

    def test_main_succeeds(self):
        with mock.patch.object(check, "check_tool", return_value=None), mock.patch("builtins.print"):
            self.assertEqual(check.main(), 0)


if __name__ == "__main__":
    unittest.main()
