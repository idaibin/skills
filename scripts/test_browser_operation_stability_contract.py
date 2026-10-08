#!/usr/bin/env python3
"""Offline regressions for browser attachment and stable-response evidence."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BrowserOperationStabilityContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def normalized(self, relative: str) -> str:
        return re.sub(r"\s+", " ", self.read(relative))

    def test_canonical_contract_and_generated_owners_keep_the_rules(self) -> None:
        canonical = self.normalized("protocols/browser-operation-v1.md")
        for token in (
            "before file selection",
            "no file was selected or uploaded",
            "same reverified browser/session, tab, target, and composer",
            "finite observation window and sampling cadence",
            "including one at the end of the window",
            "immediate consecutive snapshots do not qualify",
            "same sanitized content hash",
            "lingering control remains a separate `Not verified` terminal-UI gap",
            "Capture the accepted response once and stop",
            "fixed package, invocation, events, response-partial, and response-final paths",
            "atomic_write: verified",
            "completion-not-verified",
        ):
            with self.subTest(token=token):
                self.assertIn(token, canonical)

        source = self.read("protocols/browser-operation-v1.md")
        for relative in (
            "skills/ask-ai/references/browser-operation-protocol.md",
            "skills/ops-browser/references/browser-operation-protocol.md",
        ):
            self.assertEqual(source, self.read(relative))

    def test_provider_and_owner_evals_cover_both_confirmed_gaps(self) -> None:
        ask_eval = self.read("skills/ask-ai/references/eval-cases.md")
        ops_eval = self.read("skills/ops-browser/references/eval-cases.md")
        self.assertIn("Attachment chooser failure", ask_eval)
        self.assertIn("Stable ChatGPT response with lingering stop control", ask_eval)
        self.assertIn("Attachment phase evidence", ops_eval)
        self.assertIn("Stable response with lingering control", ops_eval)


if __name__ == "__main__":
    unittest.main()
