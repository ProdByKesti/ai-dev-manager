import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

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


if __name__ == '__main__':
    unittest.main()
