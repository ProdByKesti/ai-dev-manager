"""Run the complete foundation suite and reject incomplete evidence."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {'test_foundation_checks', 'test_documentation_checks', 'test_strict_runner'}
SYMLINK = 'test_documentation_checks.DocumentationChecks.test_external_symlink_source'


class CountingResult(unittest.TextTestResult):
    """Count successful test cases, not individual subtest events."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successful_tests = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successful_tests += 1


def evaluate(result, ids):
    modules = {name.split('.')[0] for name in ids}
    errors = []
    if not result.testsRun:
        errors.append('no tests executed')
    if REQUIRED - modules:
        errors.append(f'missing test modules: {sorted(REQUIRED - modules)}')
    if SYMLINK not in ids:
        errors.append('required symlink test missing')
    if result.failures or result.errors or result.skipped or result.expectedFailures or result.unexpectedSuccesses:
        errors.append('failed, errored, skipped or expected/unexpected tests present')
    passed = result.successful_tests
    print(f'tests: executed={result.testsRun} passed={passed} failures={len(result.failures)} errors={len(result.errors)} skipped={len(result.skipped)} expected_failures={len(result.expectedFailures)} unexpected_successes={len(result.unexpectedSuccesses)}')
    for error in errors:
        print('ERROR:', error, file=sys.stderr)
    return bool(errors)


def ids_in(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from ids_in(item)
        else:
            yield item.id()


def main():
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    ids = list(ids_in(suite))
    result = unittest.TextTestRunner(verbosity=2, resultclass=CountingResult).run(suite)
    return evaluate(result, ids)


if __name__ == '__main__':
    sys.exit(main())
