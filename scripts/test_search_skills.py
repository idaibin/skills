#!/usr/bin/env python3
"""Focused regressions for search-skills.py."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("search-skills.py")
SPEC = importlib.util.spec_from_file_location("search_skills", SCRIPT)
assert SPEC and SPEC.loader
SEARCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEARCH)


class SearchSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.index = {
            "skills": [
                {
                    "name": "repo-map",
                    "category": "repository-engineering",
                    "intents": ["bootstrap layered repository guidance"],
                    "keywords": ["AGENTS.md", "monorepo", "frontend", "backend"],
                    "excludes": ["source implementation"],
                    "related": ["repo-review"],
                },
                {
                    "name": "repo-review",
                    "category": "repository-engineering",
                    "intents": ["review a fixed commit or worktree"],
                    "keywords": ["code review", "release gate"],
                    "excludes": ["source implementation"],
                    "related": ["repo-map"],
                },
                {
                    "name": "ask-ai",
                    "category": "collaboration",
                    "intents": [
                        "coordinate an authorized external AI result",
                        "prepare an image review, generation, edit, or visual exploration",
                    ],
                    "keywords": [
                        "Qwen",
                        "通义千问",
                        "GLM",
                        "智谱清言",
                        "image review",
                        "image generate",
                        "image edit",
                        "visual exploration",
                        "图片审查",
                        "图片生成",
                        "图片编辑",
                        "视觉探索",
                        "进行三方会审",
                    ],
                    "excludes": ["local-only review"],
                    "related": ["ops-browser"],
                },
            ]
        }

    def test_guidance_query_prefers_repo_map(self) -> None:
        results = SEARCH.search(self.index, "create AGENTS.md for frontend and backend")
        self.assertEqual("repo-map", results[0]["name"])

    def test_review_query_prefers_repo_review(self) -> None:
        results = SEARCH.search(self.index, "code review release gate")
        self.assertEqual("repo-review", results[0]["name"])

    def test_unmatched_query_returns_no_results(self) -> None:
        self.assertEqual([], SEARCH.search(self.index, "calendar meeting schedule"))

    def test_cjk_provider_keyword_finds_ask_ai(self) -> None:
        for query in (
            "通义千问",
            "智谱清言",
            "请用通义千问独立审查这个架构方案",
            "请用智谱清言审查这个固定分支",
        ):
            with self.subTest(query=query):
                results = SEARCH.search(self.index, query)
                self.assertEqual("ask-ai", results[0]["name"])

    def test_image_capability_keywords_find_ask_ai(self) -> None:
        for query in ("image review", "图片编辑", "视觉探索", "请帮我做图片编辑"):
            with self.subTest(query=query):
                results = SEARCH.search(self.index, query)
                self.assertEqual("ask-ai", results[0]["name"])

    def test_saved_review_instruction_phrase_finds_ask_ai(self) -> None:
        results = SEARCH.search(self.index, "进行三方会审")
        self.assertEqual("ask-ai", results[0]["name"])


if __name__ == "__main__":
    unittest.main()
