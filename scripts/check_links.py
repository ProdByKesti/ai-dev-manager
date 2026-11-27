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
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from urllib.parse import unquote, urlsplit

REQUIRED = ('README.md', 'AGENTS.md', 'docs/README.md', 'docs/product/product-specification.md', 'docs/architecture/README.md', 'docs/architecture/system-invariants.md', 'docs/architecture/consolidation.md', 'docs/developer-guide/development-rules.md', 'docs/developer-guide/git-workflow.md', 'docs/developer-guide/quality-evidence.md')
LINK = re.compile(r'!?\[([^\[\]]+)\]\((<[^>]*>|[^\s()]*(?:\([^()]*\)[^\s()]*)?)(?:\s+"[^"]*")?\)|!?\[([^\[\]]+)\]\[([^\[\]]*)\]')
DEF = re.compile(r'^\s{0,3}\[([^\]]+)\]:\s*(<[^>]*>|[^\s<>]+)(?:\s+"[^"]*")?\s*$')
HEADING = re.compile(r'^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$')
EXCLUDED = Path('apps/desktop/node_modules')
GIT_TIMEOUT = 10


def index_path_excluded(entry, path_type=Path):
    path = path_type(os.fsdecode(entry))
    excluded = path_type(EXCLUDED.as_posix())
    return path == excluded or path.is_relative_to(excluded)


def check_index(root, errors):
    marker = root / '.git'
    try:
        marker.lstat()
    except FileNotFoundError:
        return  # Synthetic, non-Git root.
    except OSError as exc:
        errors.append(f'{marker}: cannot inspect Git marker: {exc}')
        return

    # Ignore inherited Git redirections and external configuration. Local Git
    # configuration is still read; verify the resulting worktree and index.
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
    def git(*args):
        return subprocess.run(
            ['git', '-C', str(root), '-c', 'core.fsmonitor=false', *args],
            capture_output=True, check=True, timeout=GIT_TIMEOUT, env=env,
        ).stdout
    try:
        top = Path(os.fsdecode(git('rev-parse', '--show-toplevel')).strip()).resolve()
        git_dir = Path(os.fsdecode(git('rev-parse', '--absolute-git-dir')).strip()).resolve()
        index = Path(os.fsdecode(git('rev-parse', '--path-format=absolute', '--git-path', 'index')).strip())
        if top != root or index != git_dir / 'index':
            raise ValueError('unexpected Git worktree or index path')
        info = index.lstat()
        if (not stat.S_ISREG(info.st_mode) or
                getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
            raise ValueError('Git index is not a regular file')
        for entry in git('ls-files', '--cached', '-z').split(b'\0'):
            if entry and index_path_excluded(entry):
                errors.append(f'tracked or staged content in excluded path: {os.fsdecode(entry)}')
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        errors.append(f'cannot inspect Git index: {exc}')


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
    excluded = root / EXCLUDED
    # Inspect every existing component without following links, including Windows
    # junctions and other reparse points (Path.is_symlink alone misses those).
    unsafe = False
    for component in (root / 'apps', root / 'apps/desktop', excluded):
        try:
            info = component.lstat()
        except FileNotFoundError:
            break
        except OSError as exc:
            errors.append(f'{component}: cannot inspect exclusion path: {exc}')
            unsafe = True
            break
        try:
            unsafe_component = (not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode) or
                                getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT or
                                component.resolve() != component)
        except (OSError, RuntimeError) as exc:
            errors.append(f'{component}: cannot resolve exclusion path: {exc}')
            unsafe = True
            break
        if unsafe_component:
            errors.append(f'{component}: unsafe exclusion path')
            unsafe = True
            break

    check_index(root, errors)
    if unsafe:
        return errors, counts  # Never traverse a rejected exclusion component.
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
    files = []
    def walk_error(exc):
        errors.append(f"directory traversal failed: {exc}")

    for base, dirs, names in os.walk(root, followlinks=False, onerror=walk_error):
        for d in list(dirs):
            candidate = Path(base) / d
            if candidate.is_symlink():
                errors.append(f"{candidate}: unsupported symlink directory")
                dirs.remove(d)
        dirs[:] = sorted(d for d in dirs if not (Path(base) == root and d in (".git", ".test-tmp")) and Path(base) / d != excluded)
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
                raw_dest = file.parent / unquote(parsed.path) if parsed.path else file
                lexical_dest = Path(os.path.abspath(raw_dest))
                dest = raw_dest.resolve()
                if not dest.is_relative_to(root):
                    errors.append(f'{file.relative_to(root)}:{number}: link escapes repository: {target}')
                elif lexical_dest.is_relative_to(excluded) or dest.is_relative_to(excluded):
                    errors.append(f'{file.relative_to(root)}:{number}: link to excluded path: {target}')
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
