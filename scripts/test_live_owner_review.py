import copy
import importlib.util
import json
import unittest
from pathlib import Path
import tempfile
from unittest.mock import patch

from live_owner_fixture import prepare_owner_input

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("owner_review", ROOT / "scripts/review-live-owner-results.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class OwnerReviewTests(unittest.TestCase):
    def setUp(self):
        cases = json.loads(review.CASES.read_text())["cases"]
        self.case = next(c for c in cases if c["id"] == "ask-ai-implicit-route")
        self.raw = dict(case_id=self.case["id"], status="not-verified", not_verified=["owner-artifact-oracle"],
                        selected_skill=self.case["expected_skill"], process=["read-effective-instructions"],
                        observations=["skill-selection", "effect", "efficiency"], artifacts=[], effects=[],
                        source_owners=[], stop={"state": "completed"},
                        efficiency={"tool_calls": 1, "successful_tool_calls": 1},
                        trace={"exit_code": 0, "write_order_verified": True, "changed_files": [],
                               "forbidden_command_class_hits": [], "git": {"ok": True, "changed_git_state": {}}})
        self.check = dict(criterion="addresses two cases", verdict="met", quote="case B", reason="contrasts A and B")

    def grade(self):
        return review.evaluate(self.case, self.raw, "case A vs case B", ["addresses two cases"], [self.check])

    def test_review_adds_only_missing_artifact_and_keeps_raw(self):
        before = copy.deepcopy(self.raw)
        self.assertEqual("passed", self.grade()["status"])
        self.assertEqual(before, self.raw)

    def test_quote_must_exist_and_check_must_match(self):
        for key, value in (("quote", "unseen"), ("criterion", "different"), ("reason", "")):
            with self.subTest(key=key):
                original = self.check[key]
                self.check[key] = value
                with self.assertRaises(ValueError):
                    self.grade()
                self.check[key] = original

    def test_wrong_owner_failed_execution_and_budget_still_fail(self):
        self.raw["selected_skill"] = "to-task"
        self.assertEqual("failed", self.grade()["status"])
        self.raw["selected_skill"] = self.case["expected_skill"]
        self.raw["trace"]["exit_code"] = 1
        self.assertEqual("failed", self.grade()["status"])
        self.raw["trace"]["exit_code"] = 0
        self.raw["efficiency"]["tool_calls"] = self.case["max_tool_calls"] + 1
        self.assertEqual("failed", self.grade()["status"])

    def test_pregraded_pass_still_requires_criteria_and_trace(self):
        self.raw = self.grade()
        expected = copy.deepcopy(self.raw)
        self.assertEqual(expected, self.grade())
        for verdict, status in (("unmet", "failed"), ("unverified", "not-verified")):
            with self.subTest(verdict=verdict):
                self.check["verdict"] = verdict
                self.assertEqual(status, self.grade()["status"])
        self.check["verdict"] = "met"
        self.raw["trace"]["exit_code"] = 1
        self.assertEqual("failed", self.grade()["status"])

    def test_review_cannot_overturn_original_failure(self):
        self.raw["status"] = "failed"
        self.assertEqual("failed", self.grade()["status"])

    def test_unmet_and_unverified_remain_distinct(self):
        for label, expected in (("unmet", "failed"), ("unverified", "not-verified")):
            self.check["verdict"] = label
            self.assertEqual(expected, self.grade()["status"])

class OwnerInputTests(unittest.TestCase):
    def test_briefs_keep_implicit_selection_and_reviewer_checks_separate(self):
        cases = {c["id"]: c for c in json.loads(review.CASES.read_text())["cases"]}
        fixtures = json.loads(review.FIXTURES.read_text())
        for name, material in fixtures.items():
            with self.subTest(case=name):
                self.assertEqual("implicit", cases[name]["mode"])
                self.assertIn("owner-result", cases[name]["required_artifacts"])
                self.assertNotIn(cases[name]["expected_skill"].casefold(), material["brief"].casefold())
                self.assertTrue(all(r.strip() for r in material["review"]))
                self.assertEqual(len(material["review"]), len(set(material["review"])))

    def test_missing_graph_binding_records_gap_and_keeps_other_runs_available(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict("os.environ", {"LIVE_EVAL_FORGEWAY_CLI": ""}):
            root = Path(temp)
            workspace = root / "fixture"
            workspace.mkdir()
            brief = prepare_owner_input(workspace, root, {"brief": "Graph task", "graph": True}, lambda _: None)
            self.assertEqual(brief, (root / "input.txt").read_text())
            self.assertIn("No validated graph receipt", brief)
