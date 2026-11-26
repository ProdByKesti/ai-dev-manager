"""Check the repository's roadmap JSON and dependency consistency."""
import argparse
from collections import Counter, defaultdict, deque
import json
import re
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


# Change these values only with an explicitly approved baseline revision, in the
# same reviewed change as its roadmap data and test evidence (see PR policy).
BASELINE = {"milestones": 14, "packages": 201, "p0": 167, "later": 34,
            "mappings": 201, "nodes": 201, "hardEdges": 614,
            "conditionalEdges": 31, "edges": 645, "plannedChecks": 526,
            "foundationCriteria": 22}
MILESTONE = re.compile(r"M[0-9]{2}\Z")
PACKAGE = re.compile(r"M[0-9]{2}-[0-9]{2}\Z")
LINEAR = re.compile(r"ADM-[1-9][0-9]*\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def obj(value, where):
    require(isinstance(value, dict), f"{where}: expected object")
    return value


def array(value, where):
    require(isinstance(value, list), f"{where}: expected list")
    return value


def string(value, where, pattern=None):
    require(isinstance(value, str) and bool(value.strip()), f"{where}: expected nonempty string")
    if pattern:
        require(pattern.fullmatch(value) is not None, f"{where}: invalid identifier {value!r}")
    return value


def field(record, key, where):
    obj(record, where)
    require(key in record, f"{where}: missing required field {key}")
    return record[key]


def text_field(record, key, where, pattern=None):
    return string(field(record, key, where), f"{where}.{key}", pattern)


def number(value, where, nullable=False):
    require((nullable and value is None) or (type(value) is int and value >= 0), f"{where}: expected nonnegative integer" + (" or null" if nullable else ""))
    return value


def strings(value, where, pattern=None):
    return [string(x, where, pattern) for x in array(value, where)]


def unique(values, where):
    require(len(values) == len(set(values)), f"duplicate {where}")


def schema_and_baseline(data, baseline):
    for name in REQUIRED:
        d = obj(data[name], name)
        version = 1 if name in ("catalogue-draft.json", "linear-issue-mapping.json") else 2
        require(type(field(d, "schemaVersion", name)) is int and d["schemaVersion"] == version, f"{name}: invalid schemaVersion (expected {version})")
        text_field(d, "status", name)
    manifest = data["reconstruction-manifest.json"]
    require(strings(field(manifest, "sourceFiles", "manifest"), "manifest.sourceFiles") == list(RECONSTRUCTED), "manifest sourceFiles mismatch")
    require(text_field(manifest, "historicalIndex", "manifest") == "catalogue-draft.json", "manifest historicalIndex mismatch")
    milestones, packages, criteria = [], [], []
    for name in RECONSTRUCTED:
        d = data[name]
        text_field(d, "provenance", name)
        for m in array(field(d, "milestones", name), name + ".milestones"):
            mid = text_field(m, "id", name + ".milestone", MILESTONE)
            text_field(m, "name", mid)
            strings(field(m, "notes", mid), mid + ".notes")
            number(field(m, "plannedChecks", mid), mid + ".plannedChecks", nullable=(mid == "M00"))
            milestones.append(m)
            for p in array(field(m, "packages", mid), mid + ".packages"):
                pid = text_field(p, "id", mid + ".package", PACKAGE)
                require(pid[:3] == mid, f"package {pid}: wrong milestone {mid}")
                for key in ("title", "priority", "owner", "issueType", "requirements", "provenance"):
                    text_field(p, key, pid)
                require(field(p, "linearIssueId", pid) is None or isinstance(p["linearIssueId"], str) and LINEAR.fullmatch(p["linearIssueId"]), f"{pid}.linearIssueId: invalid identifier")
                deps = strings(field(p, "dependencies", pid), pid + ".dependencies", PACKAGE)
                unique(deps, pid + " hard dependency")
                if name == RECONSTRUCTED[2]:
                    conditional_ids = []
                    for c in array(field(p, "conditionalDependencies", pid), pid + ".conditionalDependencies"):
                        conditional_ids.append(text_field(c, "id", pid + ".conditionalDependency", PACKAGE))
                        text_field(c, "condition", pid + ".conditionalDependency")
                    unique(conditional_ids, pid + " conditional dependency")
                for c in array(field(p, "acceptanceCriteria", pid), pid + ".acceptanceCriteria"):
                    cid = text_field(c, "id", pid + ".criterion")
                    require(re.fullmatch(re.escape(pid) + r"-AC[0-9]{2}", cid) is not None, f"{pid}: invalid criterion ID {cid}")
                    for key in ("description", "kind", "status"):
                        text_field(c, key, cid)
                    require(c["kind"] == ("foundation" if mid == "M00" else "planned"), f"{cid}: wrong criterion kind")
                    criteria.append((mid, cid))
                packages.append(p)
    mids = [m["id"] for m in milestones]
    unique(mids, "milestone ID")
    ids = [p["id"] for p in packages]
    unique(ids, "reconstructed package ID")
    unique([c[1] for c in criteria], "acceptance criteria ID")
    by_id = {p["id"]: p for p in packages}
    for p in packages:
        for c in p.get("conditionalDependencies", []):
            require(c["id"] in by_id, f"{p['id']}: unknown conditional prerequisite {c['id']}")
    historical = data["catalogue-draft.json"]
    historical_ids = []
    historical_mids = []
    for m in array(field(historical, "milestones", "historical"), "historical.milestones"):
        mid = text_field(m, "id", "historical milestone", MILESTONE)
        historical_mids.append(mid)
        text_field(m, "name", mid)
        number(field(m, "plannedChecks", mid), "historical plannedChecks", nullable=(mid == "M00"))
        for p in array(field(m, "packages", mid), "historical packages"):
            pid = text_field(p, "id", "historical package", PACKAGE)
            require(pid[:3] == mid, f"historical package {pid}: wrong milestone")
            historical_ids.append(pid)
            for key in ("title", "priority"):
                text_field(p, key, pid)
            for key in ("owner", "requirements", "dependencies", "acceptanceCriteria", "linearIssueId"):
                require(field(p, key, pid) is None, f"historical {pid}.{key}: expected null")
            require(pid in by_id and all(p[k] == by_id[pid][k] for k in ("title", "priority")), f"historical stable data mismatch: {pid}")
    unique(historical_mids, "historical milestone ID")
    unique(historical_ids, "historical package ID")
    require(set(historical_mids) == set(mids) and set(historical_ids) == set(ids), "historical catalogue set mismatch")
    graph = data["dependency-graph.json"]
    nodes = strings(field(graph, "nodes", "graph"), "graph node", PACKAGE)
    edges = array(field(graph, "edges", "graph"), "graph.edges")
    for e in edges:
        source = text_field(e, "prerequisite", "edge", PACKAGE)
        target = text_field(e, "dependent", "edge", PACKAGE)
        kind = text_field(e, "kind", f"edge {source} -> {target}")
        require(kind in ("hard", "conditional"), f"unknown edge kind {kind!r}: {source} -> {target}")
        if kind == "conditional":
            text_field(e, "condition", f"conditional edge {source} -> {target}")
    expected_conditional = {(c["id"], p["id"], c["condition"]) for p in packages for c in p.get("conditionalDependencies", [])}
    graph_conditional = {(e["prerequisite"], e["dependent"], e["condition"]) for e in edges if e["kind"] == "conditional"}
    require(expected_conditional == graph_conditional, f"conditional dependency mismatch: missing graph edges={sorted(expected_conditional - graph_conditional)}, extra graph edges={sorted(graph_conditional - expected_conditional)}")
    mapping = data["linear-issue-mapping.json"]
    mappings = array(field(mapping, "mapping", "mapping"), "mapping.mapping")
    for m in mappings:
        pid = text_field(m, "packageId", "mapping", PACKAGE)
        text_field(m, "linearIdentifier", pid + " mapping", LINEAR)
        mid = text_field(m, "milestone", pid + " mapping", MILESTONE)
        require(pid[:3] == mid, f"mapping {pid}: wrong milestone {mid}")
        for key in ("title", "initialStatus"):
            text_field(m, key, pid + " mapping")
        strings(field(m, "labels", pid + " mapping"), pid + ".labels")
        if pid in by_id:
            require(m["title"] == f"{pid} – {by_id[pid]['title']}", f"mapping title mismatch: {pid}")
    mm = array(field(manifest, "milestones", "manifest"), "manifest.milestones")
    manifest_mids = [text_field(m, "id", "manifest milestone", MILESTONE) for m in mm]
    unique(manifest_mids, "manifest milestone ID")
    require(set(manifest_mids) == set(mids), "manifest milestone set mismatch")
    actual_milestones = {m["id"]: m for m in milestones}
    for m in mm:
        mid = m["id"]
        text_field(m, "name", "manifest " + mid)
        text_field(m, "reviewDocument", "manifest " + mid)
        count = number(field(m, "packageCount", mid), mid + ".packageCount")
        checks = number(field(m, "plannedChecks", mid), mid + ".plannedChecks", nullable=(mid == "M00"))
        actual = actual_milestones[mid]
        require(m["name"] == actual["name"] and count == len(actual["packages"]) and checks == actual["plannedChecks"], f"manifest milestone mismatch: {mid}")
        if mid != "M00":
            require(checks == sum(len(p["acceptanceCriteria"]) for p in actual["packages"]), f"planned criteria mismatch: {mid}")
    for a in array(field(manifest, "amendments", "manifest"), "manifest.amendments"):
        aid = text_field(a, "id", "manifest amendment")
        for ref in strings(field(a, "packages", aid), aid + ".packages", PACKAGE):
            require(ref in by_id, f"manifest {aid}: unknown package {ref}")
    for key, kinds in (("topologicalOrderHard", {"hard"}), ("topologicalOrderAllPotentialEdges", {"hard", "conditional"})):
        order = strings(field(manifest, key, "manifest"), "manifest." + key, PACKAGE)
        require(len(order) == len(nodes) and len(set(order)) == len(order) and set(order) == set(nodes), f"manifest {key}: incomplete or duplicate topological order")
        rank = {node: i for i, node in enumerate(order)}
        for e in edges:
            if e["kind"] in kinds and e["prerequisite"] in rank and e["dependent"] in rank:
                require(rank[e["prerequisite"]] < rank[e["dependent"]], f"manifest {key}: invalid topological order at {e['prerequisite']} -> {e['dependent']}")
    actual = {"milestones": len(milestones), "packages": len(packages), "p0": sum(p["priority"] == "P0" for p in packages), "later": sum(p["priority"] != "P0" for p in packages), "mappings": len(mappings), "nodes": len(nodes), "hardEdges": sum(e["kind"] == "hard" for e in edges), "conditionalEdges": sum(e["kind"] == "conditional" for e in edges), "edges": len(edges), "plannedChecks": sum(mid != "M00" for mid, _ in criteria), "foundationCriteria": sum(mid == "M00" for mid, _ in criteria)}
    for key, expected in baseline.items():
        require(actual[key] == expected, f"baseline {key}: expected {expected}, actual {actual[key]}")
    counts = obj(field(manifest, "counts", "manifest"), "manifest.counts")
    for key in ("packages", "p0", "later", "hardEdges", "conditionalEdges", "plannedChecks", "foundationCriteria"):
        require(number(field(counts, key, "manifest.counts"), "manifest.counts." + key) == actual[key], f"manifest counts mismatch: {key}")
    mc = obj(field(mapping, "counts", "mapping"), "mapping.counts")
    for key, actual_key in (("packages", "packages"), ("hardDependenciesVerified", "hardEdges"), ("conditionalDependenciesVerifiedInDescriptions", "conditionalEdges"), ("plannedAcceptanceDefinitions", "plannedChecks"), ("foundationCriteria", "foundationCriteria")):
        require(number(field(mc, key, "mapping.counts"), "mapping.counts." + key) == actual[actual_key], f"mapping counts mismatch: {key}")
    statuses = obj(field(mc, "initialStatuses", "mapping.counts"), "mapping.counts.initialStatuses")
    for k, v in statuses.items():
        string(k, "initial status")
        number(v, "initial status count")
    require(statuses == dict(Counter(m["initialStatus"] for m in mappings)), "mapping initialStatuses counts mismatch")


def validate(root, baseline=BASELINE):
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
        schema_and_baseline(data, baseline)
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
