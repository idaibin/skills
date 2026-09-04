#!/usr/bin/env python3
"""Static contract checks for browser-native recording evidence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class OpsBrowserRecordingContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_recording_is_native_and_claim_bounded(self) -> None:
        skill = self.read("skills/ops-browser/SKILL.md")
        usage = self.read("skills/ops-browser/references/usage.md")
        evals = self.read("skills/ops-browser/references/eval-cases.md")
        combined = skill + usage + evals
        for term in (
            "browser-native recording",
            "native recording capability",
            "does not replace screenshots",
            "ffmpeg",
            "raw CDP screencasting",
            "user says stop",
            "Not verified",
            "method discovery",
            "no-action canary",
            "revalidate the same tab",
            "Direct navigation may prove only",
            "derived artifact",
            "not continuous recording",
            "substitute target",
            "stored or presented as a general browser rule",
        ):
            with self.subTest(term=term):
                self.assertIn(term, combined)

    def test_registry_exposes_recording_capability_revision(self) -> None:
        registry = json.loads(self.read("skills-index.json"))
        package = next(item for item in registry["packages"] if item["name"] == "ops-browser")
        capability = next(
            item
            for item in registry["capabilities"]
            if item["capability_id"] == "browser.runtime.operate"
        )
        self.assertIn("browser recording", package["keywords"])
        self.assertIn(
            "record an authorized browser interaction with native browser capture",
            package["intents"],
        )
        self.assertEqual("1.1.0", capability["capability_version"])
        self.assertIn("native recording evidence", capability["description"])


if __name__ == "__main__":
    unittest.main()
