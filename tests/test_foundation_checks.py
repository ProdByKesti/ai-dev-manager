import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_foundation.py"


class FoundationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / "docs" / "roadmap"
        self.directory.mkdir(parents=True)
        self.files = {
            "reconstructed-m00-m04.json": {"milestones": [{"packages": [{"id": "A", "dependencies": []}, {"id": "B", "dependencies": ["A"]}, {"id": "C", "dependencies": []}]}]},
            "reconstructed-m05-m09.json": {"milestones": []},
            "reconstructed-m10-m13.json": {"milestones": []},
            "catalogue-draft.json": {}, "reconstruction-manifest.json": {},
            "dependency-graph.json": {"nodes": ["A", "B", "C"], "edges": [{"prerequisite": "A", "dependent": "B", "kind": "hard"}, {"prerequisite": "B", "dependent": "C", "kind": "conditional"}]},
            "linear-issue-mapping.json": {"mapping": [{"packageId": x, "linearIdentifier": "ADM-" + str(i)} for i, x in enumerate("ABC", 1)]},
        }

    def run_cli(self, raw=None):
        for name, value in self.files.items():
            (self.directory / name).write_text(json.dumps(value), encoding="utf-8")
        if raw:
            (self.directory / raw[0]).write_text(raw[1], encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)], capture_output=True, text=True)

    def assert_failure(self, expected, raw=None):
        result = self.run_cli(raw)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(expected, result.stderr)

    def test_valid_cli(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("hard=1 conditional=1 edges=2", result.stdout)

    def test_json_syntax(self):
        self.assert_failure("catalogue-draft.json", ("catalogue-draft.json", "{"))

    def test_duplicate_object_key(self):
        self.assert_failure("duplicate JSON object key", ("catalogue-draft.json", '{"x":{"a":1,"a":2}}'))

    def test_nonstandard_constants(self):
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                self.assert_failure("non-standard numeric constant", ("catalogue-draft.json", '{"x":' + constant + '}'))

    def test_all_roadmap_json_files(self):
        self.assert_failure("extra.json", ("extra.json", "{"))

    def test_missing_required_file(self):
        del self.files["reconstruction-manifest.json"]
        self.assert_failure("reconstruction-manifest.json")

    def test_duplicate_package_id(self):
        self.files["reconstructed-m05-m09.json"]["milestones"] = copy.deepcopy(self.files["reconstructed-m00-m04.json"]["milestones"])
        self.assert_failure("duplicate reconstructed package ID")

    def test_graph_package_set(self):
        self.files["dependency-graph.json"]["nodes"] = ["A", "B", "D"]
        self.assert_failure("graph nodes package mismatch")

    def test_mapping_package_set(self):
        self.files["linear-issue-mapping.json"]["mapping"][2]["packageId"] = "D"
        self.assert_failure("Linear mapping package mismatch")

    def test_duplicate_linear_identifier(self):
        mapping = self.files["linear-issue-mapping.json"]["mapping"]
        mapping[1]["linearIdentifier"] = mapping[0]["linearIdentifier"]
        self.assert_failure("duplicate Linear identifier")

    def test_duplicate_graph_node_and_mapping(self):
        self.files["dependency-graph.json"]["nodes"].append("A")
        self.files["linear-issue-mapping.json"]["mapping"].append(copy.deepcopy(self.files["linear-issue-mapping.json"]["mapping"][0]))
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate graph node", result.stderr)
        self.assertIn("duplicate mapping package ID", result.stderr)

    def test_missing_endpoint(self):
        self.files["dependency-graph.json"]["edges"][1]["dependent"] = "D"
        self.assert_failure("graph endpoint missing")

    def test_hard_dependency_mismatch_both_directions(self):
        self.files["dependency-graph.json"]["edges"][0]["dependent"] = "C"
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing graph edges=[('A', 'B')]", result.stderr)
        self.assertIn("extra graph edges=[('A', 'C')]", result.stderr)

    def test_self_edge(self):
        self.files["dependency-graph.json"]["edges"].append({"prerequisite": "A", "dependent": "A", "kind": "conditional"})
        self.assert_failure("self edge")

    def test_duplicate_edge_across_kinds(self):
        self.files["dependency-graph.json"]["edges"].append({"prerequisite": "A", "dependent": "B", "kind": "conditional"})
        self.assert_failure("duplicate edge")

    def test_hard_cycle(self):
        self.files["dependency-graph.json"]["edges"].append({"prerequisite": "B", "dependent": "A", "kind": "hard"})
        self.assert_failure("cycle in hard graph")

    def test_conditional_cycle_only_in_maximal_graph(self):
        self.files["dependency-graph.json"]["edges"].append({"prerequisite": "C", "dependent": "A", "kind": "conditional"})
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cycle in maximal graph", result.stderr)
        self.assertNotIn("cycle in hard graph", result.stderr)

    def test_unknown_edge_kind(self):
        self.files["dependency-graph.json"]["edges"][1]["kind"] = "unknown"
        self.assert_failure("unknown edge kind")

    def test_invalid_structure(self):
        del self.files["dependency-graph.json"]["nodes"]
        self.assert_failure("invalid roadmap structure")


if __name__ == "__main__":
    unittest.main()
