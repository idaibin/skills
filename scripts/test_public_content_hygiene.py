#!/usr/bin/env python3
"""Prevent personal or project-specific evidence from entering public packages."""

from __future__ import annotations

import json
import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIGEST_SCRIPT = ROOT / "scripts" / "skill-package-digest.py"
DIGEST_SPEC = importlib.util.spec_from_file_location("skill_package_digest", DIGEST_SCRIPT)
assert DIGEST_SPEC and DIGEST_SPEC.loader
DIGEST = importlib.util.module_from_spec(DIGEST_SPEC)
DIGEST_SPEC.loader.exec_module(DIGEST)
PUBLIC_ROOTS = [
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "INSTALL.md",
    ROOT / "skills-index.json",
    ROOT / "skills.sh.json",
    ROOT / "docs",
    ROOT / "protocols",
    ROOT / "scripts",
    ROOT / "skills",
]
TEXT_SUFFIXES = {".json", ".md", ".py", ".sh", ".yaml", ".yml"}
HOME_PATH = re.compile(r"/(?:Users|home)/[^/\s`]+/")
UUID_VALUE = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
)
EMAIL_ADDRESS = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PRIVATE_IPV4 = re.compile(
    r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|"
    r"172\.(?:1[6-9]|2[0-9]|3[01])(?:\.\d{1,3}){2})\b"
)
PRIVATE_HOST = re.compile(r"https?://[^/\s`]+\.(?:internal|local)\b", re.IGNORECASE)
WINDOWS_HOME = re.compile(r"\b[A-Za-z]:\\Users\\[^\\\s`]+\\")
SECRET_SHAPE = re.compile(
    r"(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"-----BEGIN [A-Z ]+PRIVATE KEY-----)"
)
PERSONAL_RUNTIME_NAMES = tuple("AI " + suffix for suffix in ("Review", "Design", "Exec"))


def public_text_files() -> list[Path]:
    files: list[Path] = []
    for entry in PUBLIC_ROOTS:
        if entry.is_file():
            files.append(entry)
            continue
        files.extend(
            path
            for path in entry.rglob("*")
            if path.is_file() and path.suffix in TEXT_SUFFIXES
        )
    return sorted(files)


class PublicContentHygieneTests(unittest.TestCase):
    def test_sensitive_shape_detectors_cover_supported_examples(self) -> None:
        self.assertRegex("/" + "Users/example/work", HOME_PATH)
        self.assertRegex("/" + "home/example/work", HOME_PATH)
        self.assertRegex("C:" + r"\Users\example\work", WINDOWS_HOME)
        self.assertRegex("person" + "@" + "example.invalid", EMAIL_ADDRESS)
        for address in (
            ".".join(("10", "1", "2", "3")),
            ".".join(("172", "16", "2", "3")),
            ".".join(("192", "168", "2", "3")),
        ):
            with self.subTest(address=address):
                self.assertRegex(address, PRIVATE_IPV4)
        self.assertRegex("https://service" + ".internal/path", PRIVATE_HOST)

    def test_public_text_has_no_common_sensitive_value_shapes(self) -> None:
        findings: list[str] = []
        for path in public_text_files():
            text = path.read_text(encoding="utf-8")
            if HOME_PATH.search(text):
                findings.append(f"{path.relative_to(ROOT)}: local home path")
            if WINDOWS_HOME.search(text):
                findings.append(f"{path.relative_to(ROOT)}: Windows home path")
            if UUID_VALUE.search(text):
                findings.append(f"{path.relative_to(ROOT)}: UUID-like value")
            if EMAIL_ADDRESS.search(text):
                findings.append(f"{path.relative_to(ROOT)}: email address")
            if PRIVATE_IPV4.search(text):
                findings.append(f"{path.relative_to(ROOT)}: private IPv4 address")
            if PRIVATE_HOST.search(text):
                findings.append(f"{path.relative_to(ROOT)}: private hostname")
            if SECRET_SHAPE.search(text):
                findings.append(f"{path.relative_to(ROOT)}: secret-like value")
        self.assertEqual([], findings)

    def test_public_runtime_contracts_have_no_known_personal_names(self) -> None:
        findings: list[str] = []
        runtime_roots = (ROOT / "skills", ROOT / "protocols", ROOT / "scripts")
        for entry in runtime_roots:
            for path in entry.rglob("*"):
                if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
                    continue
                text = path.read_text(encoding="utf-8")
                for name in PERSONAL_RUNTIME_NAMES:
                    if name in text:
                        findings.append(f"{path.relative_to(ROOT)}: personal runtime name {name}")
        self.assertEqual([], findings)

    def test_visual_fixture_is_explicitly_synthetic_and_generically_named(self) -> None:
        fixture = (
            ROOT
            / "skills"
            / "dev-frontend"
            / "assets"
            / "frontend-visual-evidence.example.json"
        )
        payload = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertTrue(payload["task_id"].startswith("fixture-generic-"))
        self.assertEqual("Approved desktop visual reference", payload["selected_source"]["identity"])
        self.assertEqual("source-revision-001", payload["selected_source"]["revision"])
        self.assertEqual("authorized reviewer", payload["selected_source"]["approval"]["approved_by"])

    def test_visual_fixture_has_no_duplicate_json_keys(self) -> None:
        fixture = (
            ROOT
            / "skills"
            / "dev-frontend"
            / "assets"
            / "frontend-visual-evidence.example.json"
        )

        def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
            result: dict[str, object] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON key: {key}")
                result[key] = value
            return result

        json.loads(fixture.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)

    def test_live_canary_summary_matches_current_package_digest(self) -> None:
        summary = (ROOT / "docs" / "quality" / "live-canary-summary.md").read_text(
            encoding="utf-8"
        )
        expected = DIGEST.digest_paths(ROOT, DIGEST.DEFAULT_SCOPE)
        self.assertIn(f"Package digest: `{expected}`", summary)


if __name__ == "__main__":
    unittest.main()
