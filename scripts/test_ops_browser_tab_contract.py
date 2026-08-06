#!/usr/bin/env python3
"""Static contract checks for identity-safe browser tab reuse and cleanup."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER_FIELDS = (
    "task key",
    "browser surface/session identity",
    "tab identity",
    "target fingerprint",
    "ownership evidence",
    "purpose",
    "lifecycle state",
    "cleanup disposition",
    "retention authority",
)


class OpsBrowserTabContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def normalized(self, relative: str) -> str:
        return re.sub(r"\s+", " ", self.read(relative))

    def tab_ledger_fields(self) -> str:
        text = self.normalized("skills/ops-browser/SKILL.md")
        match = re.search(
            r"task-local tab ledger .*? records (?P<fields>.*?)\. Record creation intent",
            text,
        )
        self.assertIsNotNone(match, "missing task-local tab ledger field block")
        assert match is not None
        return match.group("fields")

    def test_tab_selection_is_identity_first(self) -> None:
        for path in (
            "skills/ops-browser/SKILL.md",
            "skills/ops-browser/references/usage.md",
        ):
            text = self.read(path)
            with self.subTest(path=path):
                self.assertIn("verified account/session", text)
                self.assertIn("URL matching never crosses an identity boundary", text)
                self.assertNotIn("Match an exact URL first", text)
                self.assertNotIn("search by exact URL first", text)

    def test_tab_ledger_supports_safe_reconciliation(self) -> None:
        fields = self.tab_ledger_fields()
        for field in LEDGER_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, fields)

    def test_each_tab_ledger_field_is_locally_required(self) -> None:
        fields = self.tab_ledger_fields()
        for field in LEDGER_FIELDS:
            mutated = fields.replace(field, "", 1)
            with self.subTest(removed=field):
                self.assertFalse(
                    all(required in mutated for required in LEDGER_FIELDS),
                    f"ledger stayed complete after removing {field}",
                )

    def test_reconciliation_revalidates_identity_and_fingerprint(self) -> None:
        text = self.normalized("skills/ops-browser/SKILL.md")
        match = re.search(
            r"Reconcile the task-local tab ledger before finishing\.(?P<reconcile>.*?)"
            r"Never close a pre-existing user tab",
            text,
        )
        self.assertIsNotNone(match, "missing tab reconciliation block")
        assert match is not None
        reconcile = match.group("reconcile")
        for term in (
            "revalidated browser surface/session",
            "tab identity",
            "target fingerprint",
            "ownership `Not verified`",
            "identity-matched task-created",
            "user explicitly requested it",
        ):
            with self.subTest(term=term):
                self.assertIn(term, reconcile)

    def test_retention_requires_explicit_request(self) -> None:
        skill = self.read("skills/ops-browser/SKILL.md")
        usage = self.read("skills/ops-browser/references/usage.md")
        self.assertIn("only when the user explicitly", skill)
        self.assertIn("unless the user explicitly requested a delivery tab", usage)

    def test_behavior_evals_cover_identity_and_lifecycle(self) -> None:
        text = self.read("skills/ops-browser/references/eval-cases.md")
        self.assertIn("Same URL, different identities", text)
        self.assertIn("Task-tab lifecycle", text)


if __name__ == "__main__":
    unittest.main()
