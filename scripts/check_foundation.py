"""Check the repository's roadmap JSON and dependency consistency."""
import argparse
from collections import Counter, defaultdict, deque
import json
from pathlib import Path
import sys

RECONSTRUCTED = ("reconstructed-m00-m04.json", "reconstructed-m05-m09.json", "reconstructed-m10-m13.json")
REQUIRED = (*RECONSTRUCTED, "catalogue-draft.json", "reconstruction-manifest.json", "dependency-graph.json", "linear-issue-mapping.json")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"non-standard numeric constant: {value}")


def cyclic(nodes, edges):
    incoming = {node: 0 for node in nodes}
    outgoing = defaultdict(list)
    for source, target in edges:
        if source in incoming and target in incoming:
            outgoing[source].append(target)
            incoming[target] += 1
    ready = deque(node for node, count in incoming.items() if count == 0)
    visited = 0
    while ready:
        node = ready.popleft()
        visited += 1
        for target in outgoing[node]:
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
    return visited != len(incoming)


def validate(root):
    directory = root / "docs" / "roadmap"
    errors = []
    data = {}
    paths = sorted(set(directory.glob("*.json")) | {directory / name for name in REQUIRED})
    for path in paths:
        try:
            data[path.name] = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
    if errors:
        return errors, None
    try:
        milestones = [m for name in RECONSTRUCTED for m in data[name]["milestones"]]
        packages = [p for milestone in milestones for p in milestone["packages"]]
        ids = [p["id"] for p in packages]
        graph = data["dependency-graph.json"]
        nodes = graph["nodes"]
        mappings = data["linear-issue-mapping.json"]["mapping"]
        mapped = [m["packageId"] for m in mappings]
        identifiers = [m["linearIdentifier"] for m in mappings]
        edges = graph["edges"]
        for label, values in (("reconstructed package ID", ids), ("graph node", nodes), ("mapping package ID", mapped), ("Linear identifier", identifiers)):
            for value, count in sorted(Counter(values).items()):
                if count > 1:
                    errors.append(f"duplicate {label}: {value}")
        for label, values in (("graph nodes", nodes), ("Linear mapping", mapped)):
            missing, extra = set(ids) - set(values), set(values) - set(ids)
            if missing or extra:
                errors.append(f"{label} package mismatch: missing={sorted(missing)}, extra={sorted(extra)}")
        hard, conditional = [], []
        seen = set()
        for edge in edges:
            source, target, kind = edge["prerequisite"], edge["dependent"], edge["kind"]
            pair = (source, target)
            if source not in nodes or target not in nodes:
                errors.append(f"graph endpoint missing: {source} -> {target}")
            if source == target:
                errors.append(f"self edge: {source} -> {target}")
            if pair in seen:
                errors.append(f"duplicate edge: {source} -> {target}")
            seen.add(pair)
            if kind == "hard":
                hard.append(pair)
            elif kind == "conditional":
                conditional.append(pair)
            else:
                errors.append(f"unknown edge kind {kind!r}: {source} -> {target}")
        expected = {(dep, p["id"]) for p in packages for dep in p["dependencies"]}
        missing, extra = expected - set(hard), set(hard) - expected
        if missing or extra:
            errors.append(f"hard dependency mismatch: missing graph edges={sorted(missing)}, extra graph edges={sorted(extra)}")
        if cyclic(nodes, hard):
            errors.append("cycle in hard graph")
        if cyclic(nodes, hard + conditional):
            errors.append("cycle in maximal graph (hard and conditional edges)")
        counts = (len(milestones), len(ids), len(mappings), len(nodes), len(hard), len(conditional), len(edges))
        return errors, counts
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid roadmap structure: {exc}")
        return errors, None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent, help="repository root (default: script's parent repository)")
    args = parser.parse_args(argv)
    errors, counts = validate(args.root)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print("Roadmap OK: milestones=%d packages=%d mappings=%d nodes=%d hard=%d conditional=%d edges=%d" % counts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
