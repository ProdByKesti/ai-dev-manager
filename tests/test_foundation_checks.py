"""Regression coverage for roadmap validation and its command-line interface."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_foundation.py"
spec = importlib.util.spec_from_file_location("check_foundation", SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
ROADMAP = ROOT / "docs" / "roadmap"
SOURCE = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in ROADMAP.glob("*.json")}


class FoundationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / "docs" / "roadmap"
        self.directory.mkdir(parents=True)
        self.data = copy.deepcopy(SOURCE)
        self.catalogue = self.data["reconstructed-m00-m04.json"]
        self.graph = self.data["dependency-graph.json"]
        self.mapping = self.data["linear-issue-mapping.json"]
        self.manifest = self.data["reconstruction-manifest.json"]
        self.first = self.catalogue["milestones"][0]["packages"][0]

    def run_cli(self, raw=None):
        for name, value in self.data.items():
            (self.directory / name).write_text(json.dumps(value), encoding="utf-8")
        if raw:
            (self.directory / raw[0]).write_text(raw[1], encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)], capture_output=True, text=True)

    def failure(self, expected, raw=None):
        result = self.run_cli(raw)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(expected, result.stderr)

    def test_valid_cli(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("hard=614 conditional=31 edges=645", result.stdout)

    def test_syntax(self):
        self.failure("catalogue-draft.json", ("catalogue-draft.json", "{"))

    def test_duplicate_object_key(self):
        self.failure("duplicate JSON object key", ("catalogue-draft.json", '{"x":{"a":1,"a":2}}'))

    def test_constants(self):
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                self.failure("non-standard numeric constant", ("catalogue-draft.json", '{"x":' + constant + '}'))

    def test_additional_json(self):
        self.failure("extra.json", ("extra.json", "{"))

    def test_required_file(self):
        del self.data["reconstruction-manifest.json"]
        self.failure("reconstruction-manifest.json")

    def test_duplicate_package(self):
        self.catalogue["milestones"][0]["packages"].append(copy.deepcopy(self.first))
        self.failure("duplicate reconstructed package ID")

    def test_graph_set(self):
        self.graph["nodes"][-1] = "M99-99"
        self.failure("topological order")

    def test_mapping_set(self):
        self.mapping["mapping"][-1]["packageId"] = "M13-99"
        self.failure("package mismatch")

    def test_duplicate_linear(self):
        self.mapping["mapping"][1]["linearIdentifier"] = self.mapping["mapping"][0]["linearIdentifier"]
        self.failure("duplicate Linear identifier")

    def test_duplicate_node(self):
        self.graph["nodes"][-1] = self.graph["nodes"][0]
        self.failure("topological order")

    def test_duplicate_mapping(self):
        self.mapping["mapping"][-1]["packageId"] = self.mapping["mapping"][0]["packageId"]
        self.mapping["mapping"][-1]["milestone"] = "M00"
        self.failure("duplicate mapping package ID")

    def test_endpoint(self):
        self.graph["edges"][0]["prerequisite"] = "M99-99"
        self.failure("graph endpoint missing")

    def test_hard_edge_disagreement(self):
        self.first["dependencies"].append("M00-02")
        self.failure("hard dependency mismatch")

    def test_self_edge(self):
        e = self.graph["edges"][0]
        e["dependent"] = e["prerequisite"]
        self.failure("topological order")

    def test_duplicate_edge(self):
        self.graph["edges"][1] = copy.deepcopy(self.graph["edges"][0])
        self.failure("duplicate edge")

    def test_hard_cycle_detection(self):
        self.assertTrue(check.cyclic(["A", "B"], [("A", "B"), ("B", "A")]))
        self.assertFalse(check.cyclic(["A", "B"], [("A", "B")]))
        self.graph["edges"][0]["prerequisite"], self.graph["edges"][0]["dependent"] = self.graph["edges"][0]["dependent"], self.graph["edges"][0]["prerequisite"]
        self.failure("topological order")

    def test_conditional_cycle_detection(self):
        hard = [("A", "B"), ("B", "C")]
        self.assertFalse(check.cyclic(["A", "B", "C"], hard))
        self.assertTrue(check.cyclic(["A", "B", "C"], hard + [("C", "A")]))
        e = next(e for e in self.graph["edges"] if e["kind"] == "conditional")
        e["prerequisite"], e["dependent"] = e["dependent"], e["prerequisite"]
        self.failure("topological order")

    def test_unknown_kind(self):
        self.graph["edges"][0]["kind"] = "unknown"
        self.failure("unknown edge kind")

    def test_empty_consistent(self):
        for name in check.RECONSTRUCTED:
            self.data[name]["milestones"] = []
        self.data["catalogue-draft.json"]["milestones"] = []
        self.manifest["milestones"] = []
        self.manifest["amendments"] = []
        self.manifest["topologicalOrderHard"] = self.manifest["topologicalOrderAllPotentialEdges"] = []
        self.graph["nodes"] = self.graph["edges"] = []
        self.mapping["mapping"] = []
        for key in self.manifest["counts"]:
            self.manifest["counts"][key] = 0
        for key in self.mapping["counts"]:
            self.mapping["counts"][key] = {} if key == "initialStatuses" else 0
        self.failure("baseline milestones")

    def test_consistently_reduced(self):
        m = self.data[check.RECONSTRUCTED[-1]]["milestones"].pop()
        self.data["catalogue-draft.json"]["milestones"].pop()
        removed = {p["id"] for p in m["packages"]}
        self.graph["nodes"] = [n for n in self.graph["nodes"] if n not in removed]
        self.graph["edges"] = [e for e in self.graph["edges"] if e["prerequisite"] not in removed and e["dependent"] not in removed]
        self.mapping["mapping"] = [x for x in self.mapping["mapping"] if x["packageId"] not in removed]
        self.manifest["milestones"].pop()
        for k in ("topologicalOrderHard", "topologicalOrderAllPotentialEdges"):
            self.manifest[k] = [x for x in self.manifest[k] if x not in removed]
        for a in self.manifest["amendments"]:
            a["packages"] = [x for x in a["packages"] if x not in removed]
        self.failure("baseline milestones")

    def test_baseline_counts(self):
        for key in check.BASELINE:
            with self.subTest(key=key):
                bad = dict(check.BASELINE)
                bad[key] += 1
                with self.assertRaisesRegex(ValueError, "baseline " + key):
                    check.schema_and_baseline(self.data, bad)

    def test_manifest_count(self):
        self.manifest["counts"]["packages"] += 1
        self.failure("manifest counts mismatch")

    def test_mapping_count(self):
        self.mapping["counts"]["hardDependenciesVerified"] += 1
        self.failure("mapping counts mismatch")

    def test_manifest_milestone_count(self):
        self.manifest["milestones"][0]["packageCount"] += 1
        self.failure("manifest milestone mismatch")

    def test_missing_milestone(self):
        self.catalogue["milestones"].pop()
        self.failure("historical stable data mismatch")

    def test_duplicate_milestone(self):
        self.catalogue["milestones"].append(copy.deepcopy(self.catalogue["milestones"][0]))
        self.failure("duplicate milestone ID")

    def test_invalid_package_id(self):
        self.first["id"] = "bad"
        self.failure("invalid identifier")

    def test_wrong_package_milestone(self):
        self.first["id"] = "M01-99"
        self.failure("wrong milestone")

    def test_invalid_linear_identifier(self):
        self.mapping["mapping"][0]["linearIdentifier"] = "ADM-0"
        self.failure("invalid identifier")

    def test_wrong_mapping_milestone(self):
        self.mapping["mapping"][0]["milestone"] = "M01"
        self.failure("wrong milestone")

    def test_missing_field(self):
        del self.first["requirements"]
        self.failure("missing required field requirements")

    def test_field_type(self):
        self.first["dependencies"] = "M00-01"
        self.failure("expected list")

    def test_schema_version(self):
        self.graph["schemaVersion"] = 1
        self.failure("invalid schemaVersion")

    def test_missing_criterion_id(self):
        del self.first["acceptanceCriteria"][0]["id"]
        self.failure("missing required field id")

    def test_duplicate_criterion_id(self):
        c = self.first["acceptanceCriteria"]
        c[1]["id"] = c[0]["id"]
        self.failure("duplicate acceptance criteria ID")

    def test_missing_condition(self):
        e = next(e for e in self.graph["edges"] if e["kind"] == "conditional")
        del e["condition"]
        self.failure("missing required field condition")

    def test_empty_condition(self):
        e = next(e for e in self.graph["edges"] if e["kind"] == "conditional")
        e["condition"] = "  "
        self.failure("expected nonempty string")

    def test_invalid_topological_order(self):
        order = self.manifest["topologicalOrderHard"]
        order[0], order[1] = order[1], order[0]
        self.failure("invalid topological order")

    def test_manifest_reference(self):
        self.manifest["amendments"][0]["packages"][0] = "M99-99"
        self.failure("unknown package")

    def test_manifest_source(self):
        self.manifest["sourceFiles"].pop()
        self.failure("sourceFiles mismatch")

    def test_historical_stable_fields(self):
        for key in ("title", "priority"):
            with self.subTest(key=key):
                original = self.data["catalogue-draft.json"]["milestones"][0]["packages"][0][key]
                self.data["catalogue-draft.json"]["milestones"][0]["packages"][0][key] = "changed"
                self.failure("historical stable data mismatch")
                self.data["catalogue-draft.json"]["milestones"][0]["packages"][0][key] = original

    def test_internal_synthetic_baseline_does_not_change_cli_policy(self):
        package = {"id": "M00-01", "title": "Example", "priority": "P0", "owner": "Example", "issueType": "Testing", "requirements": "Example", "provenance": "synthetic", "linearIssueId": None, "dependencies": [], "acceptanceCriteria": [{"id": "M00-01-AC01", "description": "Example", "kind": "foundation", "status": "not-executed"}]}
        milestone = {"id": "M00", "name": "Example", "notes": [], "plannedChecks": None, "packages": [package]}
        historical = {k: package[k] for k in ("id", "title", "priority")}
        historical.update({k: None for k in ("owner", "requirements", "dependencies", "acceptanceCriteria", "linearIssueId")})
        counts = {"packages": 1, "p0": 1, "later": 0, "hardEdges": 0, "conditionalEdges": 0, "plannedChecks": 0, "foundationCriteria": 1}
        d = {name: {"schemaVersion": 1 if name in ("catalogue-draft.json", "linear-issue-mapping.json") else 2, "status": "synthetic"} for name in check.REQUIRED}
        for name in check.RECONSTRUCTED:
            d[name].update(provenance="synthetic", milestones=[])
        d[check.RECONSTRUCTED[0]]["milestones"] = [milestone]
        d["catalogue-draft.json"]["milestones"] = [{"id": "M00", "name": "Example", "plannedChecks": None, "packages": [historical]}]
        d["dependency-graph.json"].update(nodes=["M00-01"], edges=[])
        d["linear-issue-mapping.json"].update(mapping=[{"packageId": "M00-01", "linearIdentifier": "ADM-1", "milestone": "M00", "title": "Example", "initialStatus": "Backlog", "labels": []}], counts={"packages": 1, "hardDependenciesVerified": 0, "conditionalDependenciesVerifiedInDescriptions": 0, "plannedAcceptanceDefinitions": 0, "foundationCriteria": 1, "initialStatuses": {"Backlog": 1}})
        d["reconstruction-manifest.json"].update(sourceFiles=list(check.RECONSTRUCTED), historicalIndex="catalogue-draft.json", milestones=[{"id": "M00", "name": "Example", "packageCount": 1, "plannedChecks": None, "reviewDocument": "M00.md"}], counts=counts, amendments=[], topologicalOrderHard=["M00-01"], topologicalOrderAllPotentialEdges=["M00-01"])
        small = {"milestones": 1, "packages": 1, "p0": 1, "later": 0, "mappings": 1, "nodes": 1, "hardEdges": 0, "conditionalEdges": 0, "edges": 0, "plannedChecks": 0, "foundationCriteria": 1}
        check.schema_and_baseline(d, small)
        with self.assertRaisesRegex(ValueError, "baseline milestones"):
            check.schema_and_baseline(d, check.BASELINE)
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("baseline", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
