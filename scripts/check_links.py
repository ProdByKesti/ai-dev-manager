"""Check documentation links and central definitions without network access.

Supports ATX headings, inline links and images, full/collapsed/shortcut
reference links, angle destinations, and optional double-quoted titles.
Fenced and inline code and escaped Markdown punctuation are excluded. Shortcut
references are links only when a matching definition exists. Nested labels,
multiline links, HTML links/images and complex destinations are unsupported;
recognizable unsupported link syntax is reported with location. Heading slugs
approximate GitHub punctuation handling; this is not a Markdown renderer.
"""
import argparse
from collections import Counter
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

REQUIRED = ('README.md', 'AGENTS.md', 'docs/README.md', 'docs/product/product-specification.md', 'docs/architecture/README.md', 'docs/architecture/system-invariants.md', 'docs/architecture/consolidation.md', 'docs/developer-guide/development-rules.md', 'docs/developer-guide/git-workflow.md', 'docs/developer-guide/quality-evidence.md')
LINK = re.compile(r'!?\[([^\[\]]+)\]\((<[^>]*>|[^\s()]*(?:\([^()]*\)[^\s()]*)?)(?:\s+"[^"]*")?\)|!?\[([^\[\]]+)\]\[([^\[\]]*)\]')
DEF = re.compile(r'^\s{0,3}\[([^\]]+)\]:\s*(<[^>]*>|[^\s<>]+)(?:\s+"[^"]*")?\s*$')
HEADING = re.compile(r'^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$')


def label(s):
    return ' '.join(s.split()).casefold()


def visible(text):
    fence = None
    for line in text.splitlines():
        m = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if m:
            mark = m.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
            yield ''
            continue
        if fence:
            yield ''
            continue
        line = re.sub(r'(`+).*?\1', '', line)
        line = re.sub(r'\\[!\[\]()]', lambda m: ' ' * len(m.group()), line)
        yield line


def anchors(text):
    seen = Counter()
    result = set()
    for line in visible(text):
        m = HEADING.match(line)
        if not m:
            continue
        title = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', m.group(2)).lower()
        slug = ''.join(c for c in title if c.isalnum() or c in ' _-').replace(' ', '-')
        index = seen[slug]
        seen[slug] += 1
        result.add(slug if index == 0 else f'{slug}-{index}')
    return result


def run(root):
    root = root.resolve()
    errors = []
    counts = Counter()
    def read_safe(path):
        try:
            if not path.resolve().is_relative_to(root):
                errors.append(f"{path}: unsafe path outside repository")
                return None
            return path.read_text(encoding="utf8")
        except (OSError, UnicodeError, RuntimeError) as exc:
            errors.append(f"{path}: cannot read: {exc}")
            return None

    for path in REQUIRED:
        if not (root / path).resolve().is_relative_to(root):
            errors.append(f"{path}: unsafe path outside repository")
        elif not (root / path).is_file():
            errors.append(f'{path}: missing required document')
    definitions = Counter()
    for path, regex in [('docs/architecture/system-invariants.md', r'^## (INV-\d{2})\b'), ('docs/architecture/consolidation.md', r'^## (K\d{2})\b')]:
        f = root / path
        if f.is_file():
            text = read_safe(f)
            if text is not None:
                definitions.update(re.findall(regex, '\n'.join(visible(text)), re.M))
    adr = root / 'docs/architecture/decisions'
    if adr.is_dir():
        for f in sorted(adr.glob('adr-*.md')):
            text = read_safe(f)
            if text is not None:
                definitions.update(re.findall(r'^# (ADR-\d{3})\b', '\n'.join(visible(text)), re.M))
    for prefix, total, width in [('INV-', 12, 2), ('K', 18, 2), ('ADR-', 15, 3)]:
        for i in range(1, total + 1):
            key = f'{prefix}{i:0{width}d}'
            if definitions[key] != 1:
                errors.append(f'definition {key}: expected 1, found {definitions[key]}')
    # Exclude only Git metadata and the known sandbox test artifacts.
    import os
    files = []
    def walk_error(exc):
        errors.append(f"directory traversal failed: {exc}")

    for base, dirs, names in os.walk(root, followlinks=False, onerror=walk_error):
        for d in list(dirs):
            candidate = Path(base) / d
            if candidate.is_symlink():
                errors.append(f"{candidate}: unsupported symlink directory")
                dirs.remove(d)
        dirs[:] = sorted(d for d in dirs if not (Path(base) == root and d in (".git", ".test-tmp")))
        files.extend(Path(base) / n for n in sorted(names) if n.lower().endswith('.md'))
    for file in files:
        counts['files'] += 1
        text = read_safe(file)
        if text is None:
            continue
        lines = list(visible(text))
        refs = {}
        for line in lines:
            m = DEF.match(line)
            if m:
                refs.setdefault(label(m.group(1)), m.group(2))
            elif re.match(r"^\s{0,3}\[[^]]+\]:", line):
                errors.append(f"{file.relative_to(root)}:{lines.index(line) + 1}: unsupported reference definition")
        for number, line in enumerate(lines, 1):
            if DEF.match(line):
                continue
            matches = list(LINK.finditer(line))
            masked = list(line)
            found = []
            for m in matches:
                masked[m.start():m.end()] = ' ' * (m.end() - m.start())
                if m.group(1) is not None:
                    found.append(m.group(2).strip('<>'))
                else:
                    name = label(m.group(4) or m.group(3))
                    if name not in refs:
                        errors.append(f'{file.relative_to(root)}:{number}: unresolved reference {name}')
                    else:
                        found.append(refs[name].strip('<>'))
            remaining = ''.join(masked)
            for m in re.finditer(r'!?\[([^\[\]]+)\](?![\[(])', remaining):
                name = label(m.group(1))
                if name in refs:
                    found.append(refs[name].strip('<>'))
                    masked[m.start():m.end()] = ' ' * (m.end() - m.start())
            remaining = ''.join(masked)
            next_line = lines[number] if number < len(lines) else ''
            multiline_link = re.search(r'!?\[[^\n]*\]\s*$', remaining) and re.match(r'\s*[\[(]', next_line)
            open_label = re.search(r'!?\[[^]\n]*$', remaining) and re.search(r'^[^\[]*\]\s*[\[(]', next_line)
            if open_label or multiline_link or re.search(r'!?\[[^\n]*\]\s*[\[(]|<\s*(?:a|img)\b', remaining, re.I):
                errors.append(f'{file.relative_to(root)}:{number}: unsupported link construction')
                counts['unsupported'] += 1
            for target in found:
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or target.startswith('//'):
                    counts['external'] += 1
                    continue
                counts['links'] += 1
                dest = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file.resolve()
                if not dest.is_relative_to(root):
                    errors.append(f'{file.relative_to(root)}:{number}: link escapes repository: {target}')
                elif not dest.exists():
                    errors.append(f'{file.relative_to(root)}:{number}: missing target: {target}')
                elif parsed.fragment:
                    counts['anchors'] += 1
                    content = read_safe(dest) if dest.is_file() and dest.suffix.lower() == '.md' else None
                    if content is None or unquote(parsed.fragment) not in anchors(content):
                        errors.append(f'{file.relative_to(root)}:{number}: missing anchor: {target}')
    return errors, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    errors, counts = run(args.root)
    for error in errors:
        print('ERROR:', error, file=sys.stderr)
    print(f"Documentation: files={counts['files']} internal_links={counts['links']} anchors={counts['anchors']} external_excluded={counts['external']} unsupported={counts['unsupported']} errors={len(errors)}")
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
