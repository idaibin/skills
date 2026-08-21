#!/usr/bin/env python3
"""Focused tests for Ask AI browser capture persistence."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "ask-ai" / "scripts" / "browser_capture_artifacts.py"
SPEC = importlib.util.spec_from_file_location("browser_capture_artifacts", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Args:
    repo: str
    review_id: str
    provider: str
    operation_id: str
    conversation_id: str
    response_container_id: str


class BrowserCaptureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / ".gitignore").write_text(".codex/\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "add", ".gitignore"], check=True)
        self.parent = self.repo / ".codex" / "reviews"
        self.parent.mkdir(parents=True)
        (self.parent / "review-1-package.md").write_text("frozen package\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def args(self) -> Args:
        args = Args()
        args.repo = str(self.repo)
        args.review_id = "review-1"
        args.provider = "chatgpt"
        args.operation_id = "round-1:chatgpt:capture"
        args.conversation_id = "conversation-1"
        args.response_container_id = "response-1"
        return args

    def test_prepare_and_finalize_produce_verified_receipt(self) -> None:
        prepared = MODULE.prepare(self.args())
        self.assertEqual(prepared["status"], "prepared")
        expected = {
            "package",
            "invocation",
            "events",
            "response_partial",
            "response_final",
        }
        self.assertEqual(set(prepared["artifacts"]), expected)
        partial = self.parent / "review-1-response.partial.md"
        partial.write_text("完整外部回复", encoding="utf-8")
        captured = MODULE.finalize(self.args())
        receipt = captured["response_capture"]
        self.assertEqual(captured["status"], "captured")
        self.assertTrue(receipt["content"]["complete"])
        self.assertFalse(receipt["content"]["truncated"])
        self.assertEqual(receipt["content"]["character_count"], 6)
        self.assertTrue(receipt["artifact"]["readback_verified"])
        invocation = json.loads((self.parent / "review-1-invocation.json").read_text())
        self.assertEqual(invocation["state"], "captured")

    def test_finalize_rejects_missing_identity_or_empty_partial(self) -> None:
        MODULE.prepare(self.args())
        args = self.args()
        args.response_container_id = ""
        with self.assertRaisesRegex(ValueError, "stable conversation"):
            MODULE.finalize(args)
        args.response_container_id = "response-1"
        with self.assertRaisesRegex(ValueError, "response.partial is empty"):
            MODULE.finalize(args)

    def test_prepare_rejects_non_ignored_parent(self) -> None:
        (self.repo / ".gitignore").write_text("", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not ignored"):
            MODULE.prepare(self.args())

    def test_review_id_cannot_escape_capture_parent(self) -> None:
        args = self.args()
        args.review_id = "../escape"
        with self.assertRaisesRegex(ValueError, "invalid review_id"):
            MODULE.prepare(args)


if __name__ == "__main__":
    unittest.main()
