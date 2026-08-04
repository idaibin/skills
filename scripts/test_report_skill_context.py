#!/usr/bin/env python3
"""Regressions for Skill context-budget reporting."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "report-skill-context.py"
SPEC = importlib.util.spec_from_file_location("report_skill_context", SCRIPT)
assert SPEC and SPEC.loader
REPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORTER)


class SkillContextReportTests(unittest.TestCase):
    def test_reports_entrypoint_runtime_reference_and_excludes_eval_from_runtime_closure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "sample-skill"
            references = package / "references"
            references.mkdir(parents=True)
            (package / "SKILL.md").write_text(
                "# Sample\n\nSee [usage](references/usage.md) and "
                "[evals](references/eval-cases.md).\n",
                encoding="utf-8",
            )
            (references / "usage.md").write_text("runtime detail", encoding="utf-8")
            (references / "eval-cases.md").write_text("maintenance eval", encoding="utf-8")
            report = REPORTER.package_report(package)
        self.assertEqual(2, report["direct_reference_count"])
        self.assertEqual(1, report["runtime_reference_count"])
        runtime = [item for item in report["references"] if item["runtime_candidate"]]
        self.assertEqual(["references/usage.md"], [item["path"] for item in runtime])

    def test_token_estimate_is_deterministic_and_nonzero(self) -> None:
        self.assertEqual(1, REPORTER.estimated_tokens("a"))
        self.assertEqual(2, REPORTER.estimated_tokens("abcde"))


if __name__ == "__main__":
    unittest.main()
