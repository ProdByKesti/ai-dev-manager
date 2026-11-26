import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
import io
import contextlib

spec = importlib.util.spec_from_file_location('strict_runner', Path(__file__).resolve().parents[1] / 'scripts/run_foundation_tests.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class StrictRunnerTests(unittest.TestCase):
    def result(self, **kwargs):
        data = dict(testsRun=3, successful_tests=3, failures=[], errors=[], skipped=[], expectedFailures=[], unexpectedSuccesses=[])
        data.update(kwargs)
        return SimpleNamespace(**data)

    def execute_cases(self, *cases):
        suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in cases)
        result = unittest.TextTestRunner(stream=io.StringIO(), resultclass=runner.CountingResult).run(suite)
        stdout, stderr = io.StringIO(), io.StringIO()
        ids = [runner.SYMLINK, 'test_foundation_checks.T.test', 'test_strict_runner.T.test']
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            failed = runner.evaluate(result, ids)
        return result, stdout.getvalue(), failed

    def test_multiple_subtest_failures_count_cases(self):
        class Multiple(unittest.TestCase):
            def test_multiple(self):
                for i in range(2):
                    with self.subTest(i=i):
                        self.fail('synthetic')
        result, output, failed = self.execute_cases(Multiple)
        self.assertEqual(len(result.failures), 2)
        self.assertIn('executed=1 passed=0 failures=2', output)
        self.assertTrue(failed)

    def test_success_alongside_multiple_failures(self):
        class Cases(unittest.TestCase):
            def test_ok(self):
                pass
            def test_bad(self):
                for i in range(2):
                    with self.subTest(i=i):
                        self.fail('synthetic')
        _, output, failed = self.execute_cases(Cases)
        self.assertIn('executed=2 passed=1 failures=2', output)
        self.assertTrue(failed)

    def test_all_successful(self):
        class Cases(unittest.TestCase):
            def test_one(self): pass
            def test_two(self): pass
        _, output, failed = self.execute_cases(Cases)
        self.assertIn('executed=2 passed=2 failures=0 errors=0', output)
        self.assertFalse(failed)

    def test_setup_and_cleanup_errors(self):
        class Setup(unittest.TestCase):
            def setUp(self): raise RuntimeError('setup')
            def test_case(self): pass
        class Cleanup(unittest.TestCase):
            def test_case(self): self.addCleanup(lambda: 1 / 0)
        _, output, failed = self.execute_cases(Setup, Cleanup)
        self.assertIn('executed=2 passed=0 failures=0 errors=2', output)
        self.assertTrue(failed)

    def test_valid(self):
        ids = [runner.SYMLINK, 'test_foundation_checks.T.test', 'test_strict_runner.T.test']
        self.assertFalse(runner.evaluate(self.result(), ids))

    def test_incomplete_and_failure_states(self):
        ids = [runner.SYMLINK, 'test_foundation_checks.T.test', 'test_strict_runner.T.test']
        for field in ('failures', 'errors', 'skipped', 'expectedFailures', 'unexpectedSuccesses'):
            with self.subTest(field=field):
                self.assertTrue(runner.evaluate(self.result(**{field: [object()]}), ids))
        self.assertTrue(runner.evaluate(self.result(testsRun=0), []))
        self.assertTrue(runner.evaluate(self.result(), ids[1:]))
