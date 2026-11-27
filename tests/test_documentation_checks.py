import importlib.util
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/check_links.py'
spec = importlib.util.spec_from_file_location('check_links', SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class DocumentationChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for p in check.REQUIRED:
            self.write(p, '# Document\n')
        self.write('docs/architecture/system-invariants.md', '\n'.join(f'## INV-{i:02} — Example' for i in range(1, 13)))
        self.write('docs/architecture/consolidation.md', '\n'.join(f'## K{i:02} — Example' for i in range(1, 19)))
        for i in range(1, 16):
            self.write(f'docs/architecture/decisions/adr-{i:03}-test.md', f'# ADR-{i:03}: Example\n')

    def write(self, name, content):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf8')

    def cli(self):
        return subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root)], capture_output=True, text=True)

    def failure(self, message):
        r = self.cli()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(message, r.stderr)

    def test_valid_links_and_code(self):
        self.write('other file.md', '# Hello World\n# Hello World\n')
        self.write('README.md', '# Start\n[a](other%20file.md#hello-world)\n[b](other%20file.md#hello-world-1)\n[c](#start)\n[d][ref]\n[ref]: other%20file.md\n`[ignored](missing)`\n```md\n[ignored](missing)\n```\n[external](https://example.invalid)\n')
        r = self.cli()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('external_excluded=1', r.stdout)

    def test_missing_file(self):
        self.write('README.md', '[broken](absent.md)')
        self.failure('missing target')

    def test_missing_anchor(self):
        self.write('README.md', '[broken](#absent)')
        self.failure('missing anchor')

    def test_missing_reference(self):
        self.write('README.md', '[broken][missing]')
        self.failure('unresolved reference')

    def test_escape(self):
        self.write('README.md', '[broken](../outside.md)')
        self.failure('escapes repository')

    def test_missing_required(self):
        (self.root / 'AGENTS.md').unlink()
        self.failure('missing required document')

    def test_missing_id(self):
        self.write('docs/architecture/system-invariants.md', '## INV-01 — only\n')
        self.failure('definition INV-02')

    def test_duplicate_id(self):
        p = self.root / 'docs/architecture/consolidation.md'
        p.write_text(p.read_text(encoding='utf8') + '\n## K01 — duplicate', encoding='utf8')
        self.failure('definition K01: expected 1, found 2')

    def test_reference_is_not_definition(self):
        self.write('README.md', 'INV-01 K01 ADR-001 are references.')
        self.assertEqual(self.cli().returncode, 0)

    def test_shortcut_and_collapsed(self):
        self.write('README.md', '[shortcut] [collapsed][] [plain text]\n\n[shortcut]: AGENTS.md\n[collapsed]: docs/\n')
        r = self.cli()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('internal_links=2', r.stdout)

    def test_bad_resolved_reference(self):
        self.write('README.md', '[shortcut]\n\n[shortcut]: missing.md\n')
        self.failure('missing target')

    def test_unsupported_link(self):
        self.write('README.md', '[nested [label]](file.md)')
        self.failure('unsupported link construction')

    def test_html_link_is_reported(self):
        self.write('README.md', '<a href="file.md">link</a>')
        self.failure('unsupported link construction')

    def test_escaped_syntax(self):
        self.write('README.md', r'\[example](missing.md)' + '\n')
        self.assertEqual(self.cli().returncode, 0)

    def test_image_link(self):
        self.write('README.md', '![image](missing.png)')
        self.failure('missing target')

    def test_duplicate_adr(self):
        self.write('docs/architecture/decisions/adr-999-extra.md', '# ADR-001: duplicate')
        self.failure('definition ADR-001: expected 1, found 2')

    def test_multiline_link_is_reported(self):
        self.write('README.md', '[label]\n(target.md)')
        self.failure('unsupported link construction')

    def test_hidden_directory_checked(self):
        self.write('.hidden/test.md', '[bad](missing)')
        self.failure('missing target')

    def test_definition_in_code_is_not_counted(self):
        self.write('docs/architecture/system-invariants.md', '```md\n## INV-01 — example\n```\n')
        self.failure('definition INV-01: expected 1, found 0')

    def test_valid_definition_with_code_example(self):
        p = self.root / 'docs/architecture/consolidation.md'
        p.write_text(p.read_text(encoding='utf8') + '\n```\n## K01 — example\n```', encoding='utf8')
        self.assertEqual(self.cli().returncode, 0)

    def test_first_reference_definition_wins(self):
        self.write('README.md', '[ref]\n\n[ref]: AGENTS.md\n[ref]: missing.md\n')
        self.assertEqual(self.cli().returncode, 0)

    def test_unsupported_reference_definition(self):
        self.write('README.md', '[ref]: <broken\n')
        self.failure('unsupported reference definition')

    def test_multiline_label(self):
        self.write('README.md', '[multi\nline](AGENTS.md)')
        self.failure('unsupported link construction')

    def test_walk_error(self):
        import os
        original = os.walk
        def failed(root, **kwargs):
            kwargs['onerror'](PermissionError('synthetic traversal failure'))
            return iter(())
        with mock.patch('os.walk', failed):
            errors, _ = check.run(self.root)
        self.assertTrue(any('directory traversal failed' in e for e in errors))

    def test_read_error(self):
        original = Path.read_text
        def failed(path, *args, **kwargs):
            if path.name == 'README.md':
                raise PermissionError('synthetic read failure')
            return original(path, *args, **kwargs)
        with mock.patch.object(Path, 'read_text', failed):
            errors, _ = check.run(self.root)
        self.assertTrue(any('cannot read' in e for e in errors))

    def test_external_symlink_source(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / 'external.md'
            target.write_text('external', encoding='utf8')
            try:
                (self.root / 'external.md').symlink_to(target)
            except OSError as exc:
                self.skipTest(f'symlink creation unavailable: {exc}')
            self.failure('unsafe path outside repository')

    def test_exact_exclusion_and_other_documents(self):
        self.write('apps/desktop/node_modules/pkg/bad.md', '[bad](missing)')
        r = self.cli()
        self.assertEqual(r.returncode, 0, r.stderr)
        for name in ('node_modules/bad.md', 'apps/node_modules/bad.md',
                     'apps/desktop/node_modules_extra/bad.md',
                     'apps/desktop/own.md', 'apps/desktop/.hidden/bad.md'):
            with self.subTest(name=name):
                self.write(name, '[bad](missing)')
                self.failure('missing target')
                (self.root / name).unlink()

    def test_missing_excluded_directory_is_allowed(self):
        self.assertEqual(self.cli().returncode, 0)

    def test_links_into_excluded_directory_are_errors(self):
        self.write('apps/desktop/node_modules/pkg/readme.md', '# Package')
        for target in ('apps/desktop/node_modules/pkg/readme.md',
                       'apps/desktop/../desktop/node_modules/pkg/readme.md',
                       'apps/desktop/%6eode_modules/pkg/readme.md'):
            with self.subTest(target=target):
                self.write('README.md', f'[package]({target})')
                self.failure('link to excluded path')

    def test_resolved_link_into_excluded_directory(self):
        self.write('apps/desktop/node_modules/pkg/readme.md', '# Package')
        try:
            (self.root / 'alias').symlink_to(self.root / 'apps/desktop/node_modules', target_is_directory=True)
        except OSError as exc:
            self.skipTest(f'symlink creation unavailable: {exc}')
        self.write('README.md', '[package](alias/pkg/readme.md)')
        self.failure('link to excluded path')

    def test_index_detects_staged_and_missing_files(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)
        name = 'apps/desktop/node_modules/pkg/readme.md'
        self.write(name, '# Package')
        subprocess.run(['git', '-C', str(self.root), 'add', '-f', '--', name], check=True, capture_output=True)
        self.failure('tracked or staged content')
        (self.root / name).unlink()
        self.failure('tracked or staged content')

    def test_index_failure_is_reported(self):
        (self.root / '.git').mkdir()
        errors, _ = check.run(self.root)
        self.assertTrue(any('cannot inspect Git index' in e for e in errors))

    def test_unsafe_exclusion_components(self):
        for name in ('apps', 'apps/desktop', 'apps/desktop/node_modules'):
            with self.subTest(name=name):
                component = self.root / name
                component.mkdir(parents=True, exist_ok=True)
                original = Path.lstat
                def reparse(path, *args, **kwargs):
                    info = original(path, *args, **kwargs)
                    if path == component:
                        return mock.Mock(st_mode=info.st_mode, st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)
                    return info
                with mock.patch.object(Path, 'lstat', reparse):
                    errors, _ = check.run(self.root)
                self.assertTrue(any('unsafe exclusion path' in e for e in errors))

    def test_index_path_components_and_case(self):
        for path_type in (PurePosixPath, PureWindowsPath):
            self.assertTrue(check.index_path_excluded(b'apps/desktop/node_modules/odd\nname.bin', path_type))
            self.assertFalse(check.index_path_excluded(b'apps/desktop/node_modules_extra/file', path_type))
            self.assertFalse(check.index_path_excluded(b'other/node_modules/file', path_type))
        self.assertTrue(check.index_path_excluded(b'Apps/Desktop/Node_Modules/file', PureWindowsPath))
        self.assertFalse(check.index_path_excluded(b'Apps/Desktop/Node_Modules/file', PurePosixPath))

    def test_regular_file_in_exclusion_components_stops_walk(self):
        for name in ('apps', 'apps/desktop', 'apps/desktop/node_modules'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('not a directory', encoding='utf8')
                with mock.patch('os.walk', side_effect=AssertionError('unsafe traversal')):
                    errors, _ = check.run(root)
                self.assertTrue(any('unsafe exclusion path' in e for e in errors))

    def test_real_symlink_exclusion_component_stops_walk(self):
        with tempfile.TemporaryDirectory() as outside:
            try:
                (self.root / 'apps').symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f'symlink creation unavailable: {exc}')
            with mock.patch('os.walk', side_effect=AssertionError('unsafe traversal')):
                errors, _ = check.run(self.root)
            self.assertTrue(any('unsafe exclusion path' in e for e in errors))

    def test_exclusion_metadata_failure_stops_walk(self):
        original = Path.lstat
        def denied(path, *args, **kwargs):
            if path == self.root / 'apps':
                raise PermissionError('synthetic denial')
            return original(path, *args, **kwargs)
        with mock.patch.object(Path, 'lstat', denied), mock.patch('os.walk', side_effect=AssertionError('unsafe traversal')):
            errors, _ = check.run(self.root)
        self.assertTrue(any('cannot inspect exclusion path' in e for e in errors))

    def test_git_marker_metadata_failure(self):
        original = Path.lstat
        def denied(path, *args, **kwargs):
            if path == self.root / '.git':
                raise PermissionError('synthetic denial')
            return original(path, *args, **kwargs)
        with mock.patch.object(Path, 'lstat', denied):
            errors, _ = check.run(self.root)
        self.assertTrue(any('cannot inspect Git marker' in e for e in errors))

    def test_git_redirect_environment_does_not_hide_index(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)
        name = 'apps/desktop/node_modules/pkg/unusual name.txt'
        self.write(name, 'tracked')
        subprocess.run(['git', '-C', str(self.root), 'add', '-f', '--', name], check=True, capture_output=True)
        redirected = dict(os.environ, GIT_INDEX_FILE=str(self.root / 'missing-index'),
                          GIT_WORK_TREE=str(self.root.parent), GIT_DIR=str(self.root / 'missing-git'))
        with mock.patch.object(check.os, 'environ', redirected):
            errors, _ = check.run(self.root)
        self.assertTrue(any('tracked or staged content' in e for e in errors))

    def test_git_timeout_and_missing_index_fail_closed(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)
        errors, _ = check.run(self.root)
        self.assertTrue(any('cannot inspect Git index' in e for e in errors))
        with mock.patch.object(check.subprocess, 'run', side_effect=subprocess.TimeoutExpired('git', 10)):
            errors, _ = check.run(self.root)
        self.assertTrue(any('cannot inspect Git index' in e for e in errors))

    def test_wrong_git_worktree_fails_closed(self):
        (self.root / '.git').mkdir()
        with mock.patch.object(check.subprocess, 'run') as run:
            run.side_effect = [mock.Mock(stdout=os.fsencode(str(self.root.parent))),
                               mock.Mock(stdout=os.fsencode(str(self.root / '.git'))),
                               mock.Mock(stdout=os.fsencode(str(self.root / '.git' / 'index')))]
            errors, _ = check.run(self.root)
        self.assertTrue(any('unexpected Git worktree or index path' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
