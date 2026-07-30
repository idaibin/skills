#!/usr/bin/env python3
"""Search the repository Skill discovery index without installing a Skill."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9.+#-]*", re.IGNORECASE)
STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "from",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_index(root: Path) -> dict[str, object]:
    return json.loads((root / "skills-index.json").read_text(encoding="utf-8"))


def normalize(value: str) -> str:
    return " ".join(
        token
        for token in TOKEN_RE.findall(value.lower().replace("-", " "))
        if token not in STOP_WORDS
    )


def score_entry(entry: dict[str, object], query: str) -> tuple[int, list[str]]:
    normalized_query = normalize(query)
    query_tokens = set(normalized_query.split())
    weighted_fields = (
        ("name", [str(entry["name"])], 6),
        ("intent", list(entry["intents"]), 4),
        ("keyword", list(entry["keywords"]), 3),
        ("category", [str(entry["category"])], 2),
    )
    score = 0
    reasons: list[str] = []
    for label, values, weight in weighted_fields:
        normalized_values = [(str(value), normalize(str(value))) for value in values]
        field_tokens = {
            token for _, normalized_value in normalized_values for token in normalized_value.split()
        }
        overlap = query_tokens & field_tokens
        phrase_matches = [
            value
            for value, normalized_value in normalized_values
            if normalized_query and normalized_query in normalized_value
        ]
        if label == "name" and not phrase_matches:
            field_score = 0
        elif phrase_matches:
            field_score = weight * max(2, len(overlap))
        else:
            field_score = weight * len(overlap)
        score += field_score
        if not field_score:
            continue
        if phrase_matches:
            reason_values = set(phrase_matches)
        else:
            reason_values = {
                value
                for value, normalized_value in normalized_values
                if query_tokens & set(normalized_value.split())
            }
        for value, normalized_value in normalized_values:
            if value in reason_values:
                reasons.append(f"{label}: {value}")
    return score, reasons


def search(index: dict[str, object], query: str) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for raw_entry in index["skills"]:
        entry = dict(raw_entry)
        score, reasons = score_entry(entry, query)
        if score:
            results.append(
                {
                    "name": entry["name"],
                    "category": entry["category"],
                    "score": score,
                    "matched": reasons,
                    "excludes": entry["excludes"],
                    "related": entry["related"],
                }
            )
    return sorted(results, key=lambda item: (-int(item["score"]), str(item["name"])))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="Task or capability to search for")
    parser.add_argument("--limit", type=int, default=5, help="Maximum results to print")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")

    query = " ".join(args.query)
    results = search(load_index(repo_root()), query)[: args.limit]
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0
    if not results:
        print("No matching Skill found.")
        return 1
    for result in results:
        matched = "; ".join(result["matched"][:2])
        print(f"{result['name']}\t{result['score']}\t{result['category']}\t{matched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
