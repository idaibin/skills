"""Static guidance regressions only; these do not prove live Agent behavior."""
from pathlib import Path
import re
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "skills/dev-tests/references"


class TestingEntryContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qa = tomllib.loads((ROOT / "integrations/codex/agents/qa.toml").read_text())
        cls.prompt = cls.qa["developer_instructions"]
        cls.api = (REFS / "api-and-logic.md").read_text()
        cls.record = (REFS / "test-record.md").read_text()
        cls.result = (REFS / "result-contract.md").read_text()
        cls.cases = (REFS / "eval-cases.md").read_text()

    def test_qa_schema_does_not_add_runtime_overrides(self):
        self.assertEqual(set(self.qa), {"name", "description", "developer_instructions"})
        self.assertEqual(self.qa["name"], "qa")
        self.assertTrue(all(isinstance(value, str) and value.strip() for value in self.qa.values()))

    def test_qa_has_the_same_brownfield_default(self):
        self.assertIn("完整 PRD 不是前置条件", self.prompt)
        for category in ("已确认规则", "现状基线", "暂定推断"):
            self.assertIn(category, self.prompt)
        self.assertIn("执行前", self.prompt)

    def test_qa_blocks_only_dependent_cases(self):
        self.assertIn("仅将依赖缺失条件的用例标记 blocked", self.prompt)
        self.assertIn("继续独立检查", self.prompt)
        self.assertIn("待人工确认", self.prompt)

    def test_qa_preserves_test_authoring_ownership(self):
        self.assertIn("dev-tests", self.prompt)
        self.assertIn("匹配的实现 owner", self.prompt)
        self.assertIn("同一 Agent 可以顺序承担", self.prompt)

    def test_qa_preserves_safety_and_claim_limits(self):
        for rule in ("不得修改产品源码", "用 skip 或 fixme 把失败变绿", "不绕限制", "不自行改全局配置"):
            self.assertIn(rule, self.prompt)
        self.assertIn("不等于业务规则批准", self.prompt)

    def test_api_route_does_not_require_a_missing_formal_spec(self):
        self.assertIn("coverage.md#existing-project-default", self.api)
        self.assertIn("Missing documentation alone does not block", self.api)
        self.assertIn("regression/exploration", self.api)
        self.assertNotIn("Use the API owner's formal contract, accepted feature behavior", self.api)

    def test_api_authorization_is_not_relaxed(self):
        for rule in ("does not grant direct service mutation", "compatible authorized runner", "unauthorized backend repository"):
            self.assertIn(rule, self.api)

    def test_record_retains_per_case_oracle_basis(self):
        self.assertIn("Expected result / basis", self.record)
        for category in ("confirmed rule", "current-behavior baseline", "provisional inference"):
            self.assertIn(category, self.record)
        self.assertIn("before execution", self.record)
        self.assertIn("not business approval", self.record)

    def test_record_keeps_the_existing_result_states(self):
        states = set(re.findall(r"^\| `([^`]+)` \|", self.result, re.M))
        self.assertEqual(states, {"passed", "failed", "blocked", "not-run", "excluded"})
        self.assertIn("No extra machine schema is required", self.record)

    def test_new_references_resolve_to_existing_heading_owners(self):
        links = [(self.api, "coverage.md", "existing-project-default"),
                 (self.record, "result-contract.md", "oracle-basis-and-pending-human-decisions")]
        for text, filename, anchor in links:
            with self.subTest(filename=filename):
                self.assertIn(f"({filename}#{anchor})", text)
                headings = re.findall(r"^#{1,6} (.+)$", (REFS / filename).read_text(), re.M)
                slugs = {re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-") for heading in headings}
                self.assertIn(anchor, slugs)

    def test_live_cases_cover_changed_entrypoints_without_claiming_execution(self):
        ids = re.findall(r"^\| (NOPRD-\d+)\b", self.cases, re.M)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue({"NOPRD-11", "NOPRD-12", "NOPRD-13"}.issubset(ids))
        self.assertIn("not executed results", self.cases)

    def test_catalog_count_matches_its_table(self):
        readme = (ROOT / "README.md").read_text()
        declared = re.search(r"Browse the (\d+) available Skills:", readme)
        self.assertIsNotNone(declared)
        catalog = readme.split("## Catalog\n", 1)[1].split("\n## ", 1)[0]
        names = re.findall(r"^\| `([^`]+)` \|", catalog, re.M)
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(int(declared.group(1)), len(names))


if __name__ == "__main__":
    unittest.main()
