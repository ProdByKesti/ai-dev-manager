import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

spec = importlib.util.spec_from_file_location('strict_runner', Path(__file__).resolve().parents[1] / 'scripts/run_foundation_tests.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class StrictRunnerTests(unittest.TestCase):
    def result(self, **kwargs):
        data = dict(testsRun=3, failures=[], errors=[], skipped=[], expectedFailures=[], unexpectedSuccesses=[])
        data.update(kwargs)
        return SimpleNamespace(**data)

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
