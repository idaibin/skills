#!/usr/bin/env python3
"""Focused safety tests for the exact-path delivery helper."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "skills/repo-delivery/scripts/compact-delivery.sh"


class CompactDeliveryTests(unittest.TestCase):
    def run_helper(self, repository: Path, *paths: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(HELPER), "--message", "synthetic exact-path test", "--", *paths],
            cwd=repository,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def repository(self, root: Path) -> Path:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "config", "user.name", "Synthetic Test"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "synthetic.invalid"], cwd=root, check=True)
        (root / "nested").mkdir()
        (root / "nested/one.txt").write_text("one\n", encoding="utf-8")
        (root / "two.txt").write_text("two\n", encoding="utf-8")
        subprocess.run(["git", "add", "--", "nested/one.txt", "two.txt"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "synthetic baseline"], cwd=root, check=True)
        return root

    def test_rejects_pathspec_magic_and_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = self.repository(Path(directory))
            (repository / "two.txt").write_text("changed\n", encoding="utf-8")
            for path in (":(exclude)two.txt", "nested"):
                with self.subTest(path=path):
                    result = self.run_helper(repository, path)
                    self.assertEqual(2, result.returncode)
                    self.assertEqual([], subprocess.run(
                        ["git", "diff", "--cached", "--name-only"],
                        cwd=repository,
                        text=True,
                        stdout=subprocess.PIPE,
                        check=True,
                    ).stdout.splitlines())

    def test_commits_only_the_exact_leaf_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = self.repository(Path(directory))
            (repository / "nested/one.txt").write_text("changed one\n", encoding="utf-8")
            (repository / "two.txt").write_text("changed two\n", encoding="utf-8")
            result = self.run_helper(repository, "nested/one.txt")
            self.assertEqual(0, result.returncode, result.stderr)
            committed = subprocess.run(
                ["git", "show", "--pretty=", "--name-only", "HEAD"],
                cwd=repository,
                text=True,
                stdout=subprocess.PIPE,
                check=True,
            ).stdout.splitlines()
            self.assertEqual(["nested/one.txt"], committed)
            self.assertIn("two.txt", subprocess.run(
                ["git", "status", "--short"],
                cwd=repository,
                text=True,
                stdout=subprocess.PIPE,
                check=True,
            ).stdout)


    def test_normalizes_leading_dot_slash_prefixes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = self.repository(Path(directory))
            for path in ("./two.txt", "././two.txt"):
                with self.subTest(path=path):
                    (repository / "two.txt").write_text(f"changed {path}\n", encoding="utf-8")
                    result = self.run_helper(repository, path)
                    self.assertEqual(0, result.returncode, result.stderr)
                    committed = subprocess.run(
                        ["git", "show", "--pretty=", "--name-only", "HEAD"],
                        cwd=repository,
                        text=True,
                        stdout=subprocess.PIPE,
                        check=True,
                    ).stdout.splitlines()
                    self.assertEqual(["two.txt"], committed)
            result = self.run_helper(repository, "./..")
            self.assertEqual(2, result.returncode)
            self.assertIn("unsafe path", result.stderr)
            self.assertEqual([], subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=repository,
                text=True,
                stdout=subprocess.PIPE,
                check=True,
            ).stdout.splitlines())


if __name__ == "__main__":
    unittest.main()
