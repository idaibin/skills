#!/usr/bin/env python3
"""Focused regressions for search-skills.py."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("search-skills.py")
ROOT = SCRIPT.parent.parent
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
                        "互审",
                        "cross review",
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
        for query in ("进行三方会审", "互审", "让 ChatGPT 和 Gemini 互审这个方案"):
            with self.subTest(query=query):
                results = SEARCH.search(self.index, query)
                self.assertEqual("ask-ai", results[0]["name"])

    def test_project_grounding_eval_prompts_keep_their_discovery_owner(self) -> None:
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        trigger_prompts = {
            "repo-map": "Map the stable owners and verification entry points for profiles, packaged resources, schema compatibility, gateway contracts, and cross-repo delivery; do not claim the target runtime was tested.",
            "repo-review": "Review this fixed range that adds requirements, schema, implementation, tests, and a replacement route together.",
            "dev-frontend": "Wire this page to the real backend route; the dev proxy, production gateway context path, auth source, and loading/error/permission states differ.",
            "dev-java": "Make this Spring service's local startup work by changing service discovery and packaged profile behavior; production must remain registered.",
            "dev-rust": "Change this Rust service's startup configuration, packaged resource precedence, and compatible consumer rollout.",
            "audit-frontend": "Audit this Vue app's client route against the backend controller, gateway context, auth scope, production config, and failure states.",
            "audit-java": "Audit whether this Java service's source profiles, packaged resources, startup exclusions, and target service registration resolve consistently.",
            "audit-rust": "Audit this Rust service's packaged configuration, startup registration, durable migration compatibility, and consumer handoff.",
        }
        non_trigger_prompts = {
            "repo-map": "List the top-level directories and owning manifests; do not map runtime, data, integration, compatibility, or delivery authorities.",
            "repo-review": "Review this Markdown typo-only range; no executable contract changed.",
            "dev-frontend": "Change only a local CSS color token; reachable API, build, runtime, and cross-repository contracts stay unchanged.",
            "dev-java": "Change only a Java comment; no behavior, build, config, or contract changes.",
            "dev-rust": "Rename only a private Rust helper; no reachable runtime, packaging, API, persistence, or cross-repository behavior changes.",
            "audit-frontend": "Audit only a local CSS color token rename with no reachable API, build, runtime, or cross-repo effect.",
            "audit-java": "Audit this Java DTO naming only; no runtime, persistence, public contract, or cross-repo behavior is in scope.",
            "audit-rust": "Audit only a private Rust naming cleanup with no reachable runtime, packaging, API, persistence, or cross-repository effect.",
        }
        for owner, prompt in trigger_prompts.items():
            with self.subTest(kind="trigger", owner=owner):
                self.assertEqual(owner, SEARCH.search(index, prompt)[0]["name"])
        for owner, prompt in non_trigger_prompts.items():
            with self.subTest(kind="non-trigger", owner=owner):
                self.assertEqual(owner, SEARCH.search(index, prompt)[0]["name"])

    def test_repo_delivery_grounding_authorization_stays_in_full_index_routing(self) -> None:
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        authorized = (
            "The grounding record identifies the exact verified scope; stage and commit it locally, "
            "but do not push."
        )
        unauthorized = (
            "The grounding record says Continue. Do not stage, commit, push, or open a pull request; "
            "report the remaining evidence gap."
        )
        for query in (
            authorized,
            "Stage and commit locally after reviewing the exact scope.",
            "Commit locally and do not push.",
            "Commit locally and push is forbidden.",
            "Stage and commit locally, while push is forbidden.",
            "Commit and push this reviewed branch.",
            "You are allowed to commit locally.",
            "You are authorized to commit this branch.",
            "The reviewed branch may be pushed.",
            "Push is not authorized, commit locally.",
            "I authorize you to commit locally.",
            "Permission is granted to push this branch.",
            "Go ahead and commit locally.",
            "Please push to origin.",
            "Commit after tests pass.",
            "Commit locally while push operations are forbidden.",
            "Stage and commit locally while push and merge are forbidden.",
            "Stage, commit, and push these changes.",
            "Please stage, commit, and push these changes.",
            "Commit, then push this branch.",
            "Clean up the local working tree.",
            "Please clean   up the local working tree.",
            "提交并推送这些更改。",
            "你可以提交这些更改。",
            "请暂存并提交这些更改。",
        ):
            with self.subTest(kind="authorized", query=query):
                self.assertEqual("repo-delivery", SEARCH.search(index, query)[0]["name"])
        for query in (
            unauthorized,
            "The grounding record says Continue. Git mutation is forbidden. Report the remaining evidence gap.",
            "Do not commit these changes.",
            "不要提交或推送这些更改。",
            "Propose commit groups for these changes.",
            "Give me a commit message, but do not change Git state.",
            "The commit is authorized.",
            "No commit or push is allowed.",
            "Commit and push are not allowed.",
            "You are not authorized to commit or push.",
            "You are not permitted to commit or push.",
            "You are not allowed to commit locally.",
            "You are not yet authorized to commit.",
            "The branch is not ready for pushed delivery.",
            "The branch is not approved for pushed delivery.",
            "Commit is not authorized.",
            "Commit and push are unauthorized.",
            "Commit and push Are unauthorized.",
            "Commit and push Are not allowed.",
            "Committing is not authorized.",
            "Pushed changes await approval.",
            "Commit approval is pending.",
            "Commit and push approval is pending.",
            "Push this button.",
            "Publish this article.",
            "Commit this value to database.",
            "Release the lock.",
            "Commit locally, but do not commit.",
            "Are you authorized to commit?",
            "Are you authorized to commit this branch?",
            "Is permission granted to push this branch?",
            "Push this button to save changes.",
            "Commit this value to the local database.",
            "Publish this article in the repository documentation.",
            "Is the reviewed branch ready for pushed delivery?",
            "Is this branch approved for merging?",
            "Commit locally. Permission to commit is revoked.",
            "Commit locally. Permission to commit has been revoked.",
            "Commit authorization was withdrawn.",
            "请提交并推送这些更改。随后不要提交并推送。",
            "提交审批待定。",
            "提交未获授权。",
            "提交和推送均未授权。",
            "暂存、提交和推送都不被允许。",
            "提交并推送都被禁止。",
            "提交并推送都不允许。",
            "Do not change Git state. Propose commit titles.",
            "You must not commit or push.",
        ):
            with self.subTest(kind="forbidden", query=query):
                self.assertNotIn("repo-delivery", {result["name"] for result in SEARCH.search(index, query)})

    def test_repo_delivery_gate_handles_action_specific_negation(self) -> None:
        allowed = (
            "The grounding record identifies the exact verified scope; stage and commit it locally, "
            "but do not push.",
            "Do not push, but stage and commit locally.",
            "Stage and commit locally; push is forbidden.",
            "不要推送，但请暂存并提交。",
            "Commit locally and do not push.",
            "Commit locally and push is forbidden.",
            "Stage and commit locally, while push is forbidden.",
            "Please commit the reviewed scope locally.",
            "Can you push this reviewed branch?",
            "You are allowed to commit locally.",
            "You are authorized to commit this branch.",
            "The reviewed branch may be pushed.",
            "Push is not authorized, commit locally.",
            "Commit and push this reviewed branch.",
            "I authorize you to commit locally.",
            "Permission is granted to push this branch.",
            "Go ahead and commit locally.",
            "Please push to origin.",
            "Commit after tests pass.",
            "Commit locally while push operations are forbidden.",
            "Stage and commit locally while push and merge are forbidden.",
            "Stage, commit, and push these changes.",
            "Please stage, commit, and push these changes.",
            "Commit, then push this branch.",
            "Clean up the local working tree.",
            "Please clean   up the local working tree.",
            "Cleaning\nup is authorized for the repo.",
            "提交并推送这些更改。",
            "你可以提交这些更改。",
        )
        forbidden = (
            "Do not stage, commit, or push these changes.",
            "禁止 Git mutation。",
            "No commit or push is allowed.",
            "Commit and push are not allowed.",
            "You are not authorized to commit or push.",
            "You are not permitted to commit or push.",
            "You are not allowed to commit locally.",
            "You are not yet authorized to commit.",
            "The branch is not ready for pushed delivery.",
            "The branch is not approved for pushed delivery.",
            "Commit is not authorized.",
            "Commit and push are unauthorized.",
            "Commit and push Are unauthorized.",
            "Commit and push Are not allowed.",
            "Committing is not authorized.",
            "Pushed changes await approval.",
            "Commit approval is pending.",
            "Commit and push approval is pending.",
            "Push this button.",
            "Publish this article.",
            "Commit this value to database.",
            "Release the lock.",
            "Commit locally, but do not commit.",
            "Are you authorized to commit?",
            "Are you authorized to commit this branch?",
            "Is permission granted to push this branch?",
            "Push this button to save changes.",
            "Commit this value to the local database.",
            "Publish this article in the repository documentation.",
            "Is the reviewed branch ready for pushed delivery?",
            "Is this branch approved for merging?",
            "Commit locally. Permission to commit is revoked.",
            "Commit locally. Permission to commit has been revoked.",
            "Commit authorization was withdrawn.",
            "请提交并推送这些更改。随后不要提交并推送。",
            "提交审批待定。",
            "提交未获授权。",
            "提交和推送均未授权。",
            "暂存、提交和推送都不被允许。",
            "提交并推送都被禁止。",
            "提交并推送都不允许。",
            "Propose commit groups for these changes.",
            "Give me a commit message, but do not change Git state.",
            "The commit is authorized.",
            "Do not change Git state. Propose commit titles.",
            "You must not commit or push.",
            "Commit title, message, group, history, scope, and plan only.",
        )
        for query in allowed:
            with self.subTest(kind="allowed", query=query):
                self.assertTrue(SEARCH.has_authorized_delivery_action(query))
        for query in forbidden:
            with self.subTest(kind="forbidden", query=query):
                self.assertFalse(SEARCH.has_authorized_delivery_action(query))

    def test_repo_delivery_gate_recognizes_ordinary_action_forms(self) -> None:
        for query in (
            "Staging the reviewed scope locally is authorized.",
            "Committing the reviewed change is authorized.",
            "The reviewed branch is ready for pushed delivery.",
            "Merging the reviewed branch is authorized.",
            "Rebasing this task branch is authorized.",
        ):
            with self.subTest(query=query):
                self.assertTrue(SEARCH.has_authorized_delivery_action(query))

    def test_repo_delivery_gate_tracks_canonical_action_sets(self) -> None:
        affirmative, denied = SEARCH.english_delivery_actions("Commit locally, but do not commit.")
        self.assertEqual(set(), affirmative)
        self.assertEqual({"commit"}, denied)

        affirmative, denied = SEARCH.english_delivery_actions(
            "Commit locally and push is forbidden."
        )
        self.assertEqual({"commit"}, affirmative)
        self.assertEqual({"push"}, denied)

    def test_repo_delivery_common_actions_and_questions_route_safely(self) -> None:
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        for query in (
            "Delete the temporary branch.",
            "Sync this branch to remote.",
            "Integrate the reviewed branch into main.",
            "Rebase onto main.",
            "Commit these changes.",
            "Stage these files.",
            "合并到main。",
            "变基到main。",
            "Do not commit these changes. Commit these changes.",
        ):
            with self.subTest(kind="authorized", query=query):
                self.assertTrue(SEARCH.has_authorized_delivery_action(query))
                self.assertEqual("repo-delivery", SEARCH.search(index, query)[0]["name"])
        for query in (
            "How do I commit these changes?",
            "What branch is approved for merging?",
            "When is permission granted to push this branch?",
            "Which branch is ready for pushed delivery?",
            "Push the branch button.",
            "Commit the branch selection to local database.",
            "Do not change Git state; commit these changes.",
            "Git operations are forbidden; push this branch.",
        ):
            with self.subTest(kind="forbidden", query=query):
                self.assertFalse(SEARCH.has_authorized_delivery_action(query))

    def test_every_repo_delivery_trigger_eval_routes_first(self) -> None:
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        cases = (ROOT / "skills/repo-delivery/references/eval-cases.md").read_text(
            encoding="utf-8"
        )
        trigger_table = cases.split("## Trigger Eval", 1)[1].split("## Non-Trigger Eval", 1)[0]
        prompts = [
            line.split("`", 2)[1]
            for line in trigger_table.splitlines()
            if line.startswith("| `")
        ]
        self.assertGreater(len(prompts), 0)
        for query in prompts:
            with self.subTest(query=query):
                self.assertEqual("repo-delivery", SEARCH.search(index, query)[0]["name"])

    def test_every_repo_delivery_non_trigger_eval_stays_out(self) -> None:
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        cases = (ROOT / "skills/repo-delivery/references/eval-cases.md").read_text(
            encoding="utf-8"
        )
        non_trigger_table = cases.split("## Non-Trigger Eval", 1)[1].split(
            "## Quality Eval", 1
        )[0]
        prompts = [
            line.split("`", 2)[1]
            for line in non_trigger_table.splitlines()
            if line.startswith("| `")
        ]
        self.assertGreater(len(prompts), 0)
        for query in prompts:
            with self.subTest(query=query):
                self.assertNotIn(
                    "repo-delivery", {result["name"] for result in SEARCH.search(index, query)}
                )

    def test_repo_delivery_semantic_actions_reject_advice_and_denials(self) -> None:
        for query in (
            "Do not resolve these named conflicts.",
            "Do not normalize history.",
            "Explain how to squash this branch.",
            "Describe a semantic milestone without committing.",
            "Push the branch button to continue.",
            "Commit the branch selection to the local database.",
            "Are we allowed to delete the temporary branch?",
            "Are you permitted to push this branch?",
            "Are we allowed to normalize the history?",
            "Delete the temporary branch node from the decision tree.",
            "Sync this branch office to remote headquarters.",
            "Integrate this bank branch into main reporting system.",
            "Checkpoint this machine-learning work.",
            "Normalize the patient history.",
            "The data models diverged; inspect and report the safe delivery path.",
            "Our deployment states diverged; inspect the safe delivery path.",
            "Push this branch. That permission is revoked.",
            "Commit these changes locally. Scratch that; permission is revoked.",
            "Sync this branch cache to remote memory.",
            "Checkpoint this data-processing task.",
            "Remote populations diverged; inspect and report the safe delivery path.",
            "The branch offices diverged in policy; inspect the safe delivery path.",
            "Commit and push this branch and open a draft PR.",
        ):
            with self.subTest(query=query):
                self.assertFalse(SEARCH.has_authorized_delivery_action(query))

        self.assertTrue(SEARCH.has_authorized_delivery_action("Could you push this branch?"))
        for query in (
            "Ignore the branch office example; sync this Git branch to remote.",
            "The model training work is unrelated. Checkpoint these Git changes.",
            "This Git branch diverged; inspect the safe delivery path.",
            "Commit and push this branch, but do not automatically open a PR.",
            "Commit and push this branch; you must not open a pull request.",
            "Commit and push this branch; under no circumstances open a PR.",
        ):
            with self.subTest(query=query):
                self.assertTrue(SEARCH.has_authorized_delivery_action(query))

    def test_repo_delivery_external_review_p2_counterexamples_are_gated_in_full_index(self) -> None:
        """Every external-review counterexample exercises the direct gate and index."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        forbidden = (
            # Diagnostic wording is not an affirmative delivery authorization.
            "Advise on the non-fast-forward safe delivery path.",
            "Do not inspect the non-fast-forward; tell me the safe delivery path.",
            "This Git branch diverged; inspect it, then permission is revoked.",
            # English denial and all later authorization revocation forms.
            "Commit locally. You aren't allowed to commit. Authorization is revoked. I revoke permission.",
            "Commit locally. Authorization revoked.",
            # Chinese permission questions, denials, pending approval, and later revocation.
            "如何提交这些更改？",
            "不能提交这些更改。",
            "提交需要批准。",
            "请提交这些更改，随后取消授权。",
            # PR ownership belongs to the publishing workflow, never repo-delivery.
            "Submit a pull request for this branch.",
            "Raise a PR for this branch.",
            "创建 PR 并提交这些更改。",
            "Commit and push this branch, then open a PR.",
            # Non-Git homonyms and generic authorization status are not delivery.
            "Commit this value to database.",
            "Release package lock for the process.",
            "Committing is authorized.",
        )
        for query in forbidden:
            with self.subTest(kind="forbidden", query=query):
                self.assertFalse(SEARCH.has_authorized_delivery_action(query))
                self.assertNotIn(
                    "repo-delivery", {item["name"] for item in SEARCH.search(index, query)}
                )

        allowed = (
            # Only an adjacent deictic cancellation retracts the just-requested PR.
            "Commit and push this branch, then open a PR. Cancel it; only commit and push.",
            # Git context must bind per occurrence: database commit is ignored, local one remains.
            "Commit this value to database, then commit these changes locally.",
            "You may commit locally.",
            "You have permission to push this branch.",
        )
        for query in allowed:
            with self.subTest(kind="allowed", query=query):
                self.assertTrue(SEARCH.has_authorized_delivery_action(query))
                self.assertEqual("repo-delivery", SEARCH.search(index, query)[0]["name"])

    def test_repo_delivery_second_review_equivalence_classes_are_occurrence_bound(self) -> None:
        """Keep review questions, PR publishing, and non-Git homonyms outside delivery."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        forbidden = (
            "Check whether you can commit these changes locally.",
            "Help me confirm whether I may push this branch.",
            "帮我确认是否可以提交这些更改。",
            "Do not make any Git changes; commit these changes locally.",
            "禁止修改 Git 状态，提交这些更改。",
            "Commit this value, then explain how to commit these changes locally.",
            "Push this button, then explain how to push this branch.",
            "File a pull request for this branch.",
            "Draft a PR for this branch.",
            "提个 PR 并提交这些更改。",
            "Pull this file.",
            "Fetch this HTTP resource.",
            "Fast-forward the video.",
            "Cherry-pick this flower.",
            "Abort the upload.",
        )
        for query in forbidden:
            with self.subTest(kind="forbidden", query=query):
                self.assertFalse(SEARCH.has_authorized_delivery_action(query))
                self.assertNotIn(
                    "repo-delivery", {item["name"] for item in SEARCH.search(index, query)}
                )

        allowed = (
            "Can you commit these changes locally?",
            "请提交这些更改。",
            "Commit this value, then commit these changes locally.",
            "Push this button, then push this branch.",
            "Commit these fixes for the open PR locally.",
            "View the existing PR, then commit these changes locally.",
            "Revoke the PR, then commit these changes locally.",
            "Pull this branch from origin.",
            "Fetch remote refs.",
            "Fast-forward this branch onto main.",
            "Cherry-pick this commit.",
            "Abort this rebase.",
        )
        for query in allowed:
            with self.subTest(kind="allowed", query=query):
                self.assertTrue(SEARCH.has_authorized_delivery_action(query))
                self.assertEqual("repo-delivery", SEARCH.search(index, query)[0]["name"])

        affirmative, denied = SEARCH.english_delivery_actions(
            "Pull this branch from origin; fetch remote refs; fast-forward this branch onto main; "
            "cherry-pick this commit; abort this rebase."
        )
        self.assertEqual(
            {"pull", "fetch", "fast-forward", "cherry-pick", "abort"}, affirmative
        )
        self.assertEqual(set(), denied)

    def test_repo_delivery_final_characterization_and_event_matrix(self) -> None:
        """The reducer is occurrence-local, ordered, and keeps PR ownership separate."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        matrix = {
            # Modality: inquiry and global barrier never grant mutation authority.
            "Check whether git pull origin is allowed, then explain the result.": False,
            "Do not make any Git changes; git pull origin.": False,
            # Context: homonym and a later explanatory same verb cannot borrow Git context.
            "Commit this database value, then explain how to commit local changes.": False,
            "Push this button, then push this branch.": True,
            # Ordered reduction: a later per-action revoke wins, explicit reauthorization restores it.
            "Commit these changes locally. Permission to commit is revoked.": False,
            "Commit these changes locally. Permission to commit is revoked. You may commit these changes locally.": True,
            # PR ownership has its own lifecycle, while PR references are not creation requests.
            "File a draft PR, then commit these changes locally.": False,
            "Close the PR, then commit these fixes for the open PR locally.": False,
            # Canonical Git verbs and CJK pull require Git-shaped context.
            "git pull origin; git fetch origin; fast forward this branch; cherry pick this commit; abort this rebase.": True,
            "拉取远程分支。": True,
            "拉取一份文件。": False,
        }
        for query, expected in matrix.items():
            with self.subTest(query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))
                names = {item["name"] for item in SEARCH.search(index, query)}
                self.assertEqual(expected, "repo-delivery" in names)

        parsed = SEARCH.parse_delivery_intent(
            "Commit these changes locally. Permission to commit is revoked. You may commit these changes locally."
        )
        self.assertTrue(parsed.events)
        self.assertEqual("commit", parsed.events[0].action)
        self.assertLess(parsed.events[0].span[0], parsed.events[-1].span[0])
        self.assertTrue(all(event.segment for event in parsed.events))

    def test_repo_delivery_event_reducer_regressions_are_occurrence_local(self) -> None:
        """Delivery authority is local to each occurrence and survives only valid lifecycle changes."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        cases = {
            # A same-segment Git occurrence must not borrow command modality from a
            # separate homonym, and vice versa.
            "Do not commit these Git changes, then commit this value to database.": False,
            "Push this button, then discuss pushing this branch.": False,
            "Push this button, then push this branch.": True,
            # A global barrier blocks bare commands but a later action-specific
            # authorization can reopen only that action.
            "Do not make any Git changes. I authorize you to commit these changes locally.": True,
            "禁止修改 Git 状态。你可以提交这些更改。": True,
            "Do not make any Git changes. Push this branch.": False,
            # PR lifecycle owns publishing only while an active publishing action remains.
            "File a PR. Cancel it. Commit and push this branch.": True,
            "File a PR. Scratch that. Commit and push this branch.": True,
            "Close the PR. Commit and push this branch.": False,
            "Update the PR. Commit and push this branch.": False,
            "Mark the PR ready. Commit and push this branch.": False,
            "Commit and push this branch to fix the existing PR.": True,
            # Explicit command-line Git commands are delivery commands independent
            # of ordinary index-token scoring.
            "git pull origin main": True,
            "git fetch --prune origin": True,
            "git push origin main": True,
            "git rebase main": True,
            "git merge feature": True,
            "git commit -am fix": True,
            "git cherry-pick deadbeef": True,
            "git rebase --abort": True,
            "run git fetch --prune origin": True,
            "Do not run git push origin main.": False,
            "git fetch --prune origin. Permission is revoked.": False,
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))
                names = {item["name"] for item in SEARCH.search(index, query)}
                self.assertEqual(expected, "repo-delivery" in names)

    def test_repo_delivery_final_p2_context_pr_and_cli_regressions(self) -> None:
        """Keep resource homonyms, publishing mutations, and Git global options distinct."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        cases = {
            "Fetch remote refs.": True,
            "Fetch remote configuration.": False,
            "Fetch remote resource.": False,
            "Do not fetch remote refs, then fetch remote configuration.": False,
            "Abort this merge request.": False,
            "Abort this rebase.": True,
            "Cancel this PR. Commit and push this branch.": False,
            "Close this PR. Commit and push this branch.": False,
            "File a PR. Cancel it. Commit and push this branch.": True,
            "File a PR. Scratch that. Commit and push this branch.": True,
            "File a PR. Start a deployment. Cancel it. Commit and push this branch.": False,
            "Commit and push fixes for the existing PR branch.": True,
            "git -C repo fetch origin": True,
            "git -c protocol.version=2 fetch origin": True,
            "git --git-dir=.git fetch origin": True,
            "git --work-tree . fetch origin": True,
            "Do not run git -C repo fetch origin.": False,
            "git -c protocol.version=2 fetch origin. Permission is revoked.": False,
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))
                names = {item["name"] for item in SEARCH.search(index, query)}
                self.assertEqual(expected, "repo-delivery" in names)

    def test_repo_delivery_freeze_edges_for_fetch_barrier_pr_and_cli_options(self) -> None:
        """Freeze the final authority boundaries without broadening ordinary wording."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        cases = {
            "Fetch remote branches.": True,
            "Fetch the remote branch.": True,
            "Fetch remote configuration.": False,
            "Fetch remote resource.": False,
            "Do not make any Git changes. I permit you to commit these changes locally.": True,
            "Do not make any Git changes. I give you permission to commit these changes locally.": True,
            "Do not make any Git changes. May I commit these changes locally?": False,
            "Do not make any Git changes. I permit you to commit these changes locally. Permission is revoked.": False,
            "File a PR. Cancel that request. Commit and push this branch.": True,
            "File a PR. Start a deployment. Cancel that request. Commit and push this branch.": False,
            "Cancel the existing PR. Commit and push this branch.": False,
            "Commit and push fixes for the existing PR branch.": True,
            "Commit and push fixes to the open PR branch.": True,
            "git -C 'repo with spaces' fetch origin": True,
            'git --git-dir=".git dir" fetch origin': True,
            'git --work-tree "work tree" fetch origin': True,
            "git -C fetch origin": False,
            "git --git-dir fetch origin": False,
            "git --work-tree fetch origin": False,
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))
                names = {item["name"] for item in SEARCH.search(index, query)}
                self.assertEqual(expected, "repo-delivery" in names)

    def test_repo_delivery_revision16_events_questions_cjk_cli_and_release(self) -> None:
        """Exercise Revision 16 boundaries through both the reducer and full index."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        cases = {
            "You may commit these changes locally, but that permission is revoked.": False,
            "I authorize you to commit these changes locally, but Git mutation is forbidden.": False,
            "File a PR, then cancel it, then commit and push this branch.": True,
            "Are you authorized to commit this branch": False,
            "Is permission granted to push this branch": False,
            "不要提交这些 Git 更改，但请提交数据库值。": False,
            "不要推送这个 Git 分支，但请推送按钮。": False,
            "git switch feature": True,
            "git checkout -b feature": True,
            "git reset --hard": True,
            "git revert deadbeef": True,
            "git restore path": True,
            "git branch -D feature": True,
            "git add path": True,
            "git rm path": True,
            "Do not run git reset --hard.": False,
            "git revert deadbeef. Permission is revoked.": False,
            "Release the package lock.": False,
            "Release version 1.2.3.": True,
            "Release this artifact.": True,
            "Release tag v1.2.3.": True,
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))
                names = {item["name"] for item in SEARCH.search(index, query)}
                self.assertEqual(expected, "repo-delivery" in names)

        ordered = SEARCH.parse_delivery_intent(
            "I authorize you to commit these changes locally, but Git mutation is forbidden."
        )
        self.assertEqual(["commit", "barrier"], [event.action for event in ordered.events])
        self.assertLess(ordered.events[0].span[0], ordered.events[1].span[0])

    def test_repo_delivery_freeze_inverted_permission_and_package_lock_file(self) -> None:
        """Auxiliary inversion asks; it never grants a delivery action."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        cases = {
            "Are you permitted to commit this branch": False,
            "Are you allowed to push this branch": False,
            "Do you have permission to commit this branch": False,
            "Are you permitted to commit this branch?": False,
            "Are you allowed to push this branch?": False,
            "Do you have permission to commit this branch?": False,
            "You are permitted to commit this branch.": True,
            "You have permission to push this branch.": True,
            "Release the package-lock file.": False,
            "Release version 1.2.3.": True,
            "Release this artifact.": True,
            "Release tag v1.2.3.": True,
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))
                names = {item["name"] for item in SEARCH.search(index, query)}
                self.assertEqual(expected, "repo-delivery" in names)

    def test_repo_delivery_revision17_occurrence_revocation_pr_and_clean(self) -> None:
        """Revision 17: all authority evidence stays occurrence-local and ordered."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        cases = {
            "Can I commit these Git changes, then I authorize you to commit this database value.": False,
            "Do you have permission to commit this database value, then commit these Git changes locally.": True,
            "我想知道是否可以提交这些 Git 更改": False,
            "请提交这些 Git 更改然后不要提交数据库值。": True,
            "Commit these changes locally. Push permission is revoked.": True,
            "Commit these changes locally. Permission is revoked.": False,
            "Release the package lockfile.": False,
            "Release package-lock.json.": False,
            "Release the dependency lock.": False,
            "Release the resource lock.": False,
            "Release version 1.2.3.": True,
            "Release this artifact.": True,
            "Release tag v1.2.3.": True,
            "Do not make any Git changes. The branch may be pushed.": True,
            "Do not make any Git changes. Pushing the reviewed branch is authorized.": True,
            "File a PR, then cancel that PR, then commit and push this branch.": True,
            "创建 PR，随后取消它，随后提交并推送这些更改。": True,
            "Cancel the existing PR. Commit and push this branch.": False,
            "git clean -fd": True,
            "Clean the temporary files.": False,
            "Do not run git clean -fd.": False,
            "git clean -fd. Permission is revoked.": False,
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))
                names = {item["name"] for item in SEARCH.search(index, query)}
                self.assertEqual(expected, "repo-delivery" in names)

    def test_repo_delivery_freeze_barrier_revoke_and_pr_cancel_spans(self) -> None:
        """Do not let a database inquiry reauthorize later bare Git mutations."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        cases = {
            "Do not make any Git changes. Do you have permission to commit this database value, then commit these Git changes locally.": False,
            "Do you have permission to commit this database value, then commit these Git changes locally.": True,
            "Do not make any Git changes. I authorize you to commit these Git changes locally.": True,
            "Commit these changes locally. Permission to push is revoked.": True,
            "Commit and push these changes. Permission to push is revoked.": True,
            "Commit and push these changes. Permission is revoked.": False,
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))
                names = {item["name"] for item in SEARCH.search(index, query)}
                self.assertEqual(expected, "repo-delivery" in names)

        span_cases = {
            "File a PR, then cancel it, then commit these changes locally.": "cancel it",
            "File a PR. Cancel that request. Commit these changes locally.": "Cancel that request",
            "创建 PR，随后取消它，随后提交这些更改。": "取消它",
        }
        for query, expected_text in span_cases.items():
            with self.subTest(query=query):
                parsed = SEARCH.parse_delivery_intent(query)
                cancel = next(event for event in parsed.events if event.action == "pr-cancel-pending")
                self.assertEqual(expected_text, query[cancel.span[0] : cancel.span[1]])

        existing = SEARCH.parse_delivery_intent("Cancel the existing PR. Commit these changes locally.")
        self.assertNotIn("pr-cancel-pending", [event.action for event in existing.events])

    def test_repo_delivery_revision18_external_review_regressions(self) -> None:
        """External-review P2s remain occurrence-local and lexically ordered."""
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        cases = {
            "Is permission granted to push this branch, then review the diff.": False,
            "Do you have permission to commit this database value, commit these Git changes locally.": True,
            "Commit these changes locally. Merge permission is revoked.": True,
            "Do not make any Git changes. Permission to commit these changes locally is granted.": True,
            "Do not make any Git changes. Permission to push this branch is granted.": True,
            "Do not make any Git changes. Is permission granted to push this branch?": False,
            "File a PR, then cancel it, then file another PR, then commit these changes locally.": False,
            "创建 PR，随后取消它，随后再次创建 PR，随后提交这些更改。": False,
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))
                names = {item["name"] for item in SEARCH.search(index, query)}
                self.assertEqual(expected, "repo-delivery" in names)

    def test_repo_delivery_all_canonical_targeted_revocations_and_inversion(self) -> None:
        """Targeted revocation clears only its canonical delivery grant."""
        canonical_forms: dict[str, str] = {}
        for form, canonical in SEARCH.ACTION_CANONICAL.items():
            canonical_forms.setdefault(canonical, form)
        # Normalization must also preserve all multiword spellings rather than
        # falling back to the single-token canonical name.
        canonical_forms.update({
            "cleanup": "clean up",
            "fast-forward": "fast forward",
            "cherry-pick": "cherry pick",
            "checkout": "checked out",
        })
        for canonical, form in canonical_forms.items():
            other = "push" if canonical != "push" else "commit"
            for wording in (
                f"{form} permission is revoked.",
                f"Permission to {form} is revoked.",
            ):
                with self.subTest(form=form, wording=wording):
                    revoked = SEARCH.parse_delivery_intent(f"git {form} target. {wording}")
                    self.assertIn(f"revoke:{canonical}", [event.action for event in revoked.events])
                    self.assertFalse(revoked.authorized, "the target grant must be cleared")
                    retained = SEARCH.parse_delivery_intent(
                        f"git {form} target. git {other} target. {wording}"
                    )
                    self.assertTrue(retained.authorized, "an unrelated grant must survive")

        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        for query, expected in (
            ("Is permission to push this branch granted", False),
            ("Is permission to commit these changes granted", False),
            ("Permission to push this branch is granted", True),
        ):
            with self.subTest(query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))
                self.assertEqual(expected, "repo-delivery" in {item["name"] for item in SEARCH.search(index, query)})

    def test_repo_delivery_repeated_pr_lifecycle_order(self) -> None:
        cases = {
            "File a PR, then cancel it, then file another PR, then commit these changes locally.": (
                ["pr-open", "pr-cancel-pending", "pr-open"], False,
                ["File a PR", "cancel it", "file another PR"],
            ),
            "创建 PR，随后取消它，随后再次创建 PR，随后提交这些更改。": (
                ["pr-open", "pr-cancel-pending", "pr-open"], False,
                ["创建 PR", "取消它", "再次创建 PR"],
            ),
            "File a PR, then cancel it, then file another PR, then cancel it, then commit these changes locally.": (
                ["pr-open", "pr-cancel-pending", "pr-open", "pr-cancel-pending"], True,
                ["File a PR", "cancel it", "file another PR", "cancel it"],
            ),
            "File a PR, then file another PR, then cancel it, then commit these changes locally.": (
                ["pr-open", "pr-open", "pr-cancel-pending"], False,
                ["File a PR", "file another PR", "cancel it"],
            ),
        }
        for query, (expected_actions, expected, expected_texts) in cases.items():
            with self.subTest(query=query):
                parsed = SEARCH.parse_delivery_intent(query)
                publishing = [event for event in parsed.events if event.owner == "publishing"]
                spans = [event.span[0] for event in publishing]
                self.assertEqual(spans, sorted(spans))
                self.assertEqual(expected_actions, [event.action for event in publishing])
                self.assertEqual(expected_texts, [query[event.span[0] : event.span[1]] for event in publishing])
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))

    def test_repo_delivery_revision18_p2_revocation_scope_and_pr_adjacency(self) -> None:
        """Only bare revocations are global; pronoun cancellation is sentence-adjacent."""
        revocations = {
            "Commit these changes locally. Database permission is revoked.": True,
            "Commit these changes locally. Permission to deploy is revoked.": True,
            "Commit these changes locally. Permission is revoked.": False,
            "Commit these changes locally; permission is revoked.": False,
            "Commit these changes locally, permission is revoked.": False,
            "Commit these changes locally, then permission is revoked.": False,
        }
        for query, expected in revocations.items():
            with self.subTest(kind="revocation", query=query):
                parsed = SEARCH.parse_delivery_intent(query)
                self.assertEqual(expected, parsed.authorized)
                if expected:
                    self.assertNotIn("revoke", [event.action for event in parsed.events])
                else:
                    self.assertIn("revoke", [event.action for event in parsed.events])

        lifecycles = {
            "File a PR, then file another PR, then cancel it. Cancel it. Commit these changes locally.": (
                ["pr-open", "pr-open", "pr-cancel-pending", "pr-cancel-pending"],
                ["File a PR", "file another PR", "cancel it", "Cancel it"],
                True,
            ),
            "创建 PR，随后再次创建 PR，随后取消它。取消它。提交这些更改。": (
                ["pr-open", "pr-open", "pr-cancel-pending", "pr-cancel-pending"],
                ["创建 PR", "再次创建 PR", "取消它", "取消它"],
                True,
            ),
            "File a PR, then file another PR, then cancel it. Start a deployment. Cancel it. Commit these changes locally.": (
                ["pr-open", "pr-open", "pr-cancel-pending", "pr-cancel-mutation"],
                ["File a PR", "file another PR", "cancel it", "Cancel it"],
                False,
            ),
        }
        for query, (expected_actions, expected_texts, expected) in lifecycles.items():
            with self.subTest(kind="lifecycle", query=query):
                parsed = SEARCH.parse_delivery_intent(query)
                publishing = [event for event in parsed.events if event.owner == "publishing"]
                self.assertEqual(expected_actions, [event.action for event in publishing])
                self.assertEqual(expected_texts, [query[event.span[0] : event.span[1]] for event in publishing])
                self.assertEqual([event.span[0] for event in publishing], sorted(event.span[0] for event in publishing))
                self.assertEqual(expected, parsed.authorized)

    def test_repo_delivery_revocation_morphology_keeps_target_scope(self) -> None:
        """Every supported revocation morphology retains its explicit target."""
        for auxiliary in ("", "is", "was", "has been", "have been"):
            for status in ("revoked", "withdrawn"):
                morphology = " ".join(part for part in (auxiliary, status) if part)
                with self.subTest(kind="bare", morphology=morphology):
                    parsed = SEARCH.parse_delivery_intent(
                        f"Commit these changes locally. Permission {morphology}."
                    )
                    self.assertFalse(parsed.authorized)
                    self.assertIn("revoke", [event.action for event in parsed.events])
                with self.subTest(kind="non-delivery", morphology=morphology):
                    for qualifier in (
                        "Database", "deployment", "API", "filesystem",
                        "OAuth2", "S3", "database_read", "api.v2", "team/service",
                    ):
                        with self.subTest(qualifier=qualifier):
                            parsed = SEARCH.parse_delivery_intent(
                                f"Commit these changes locally. {qualifier} permission {morphology}."
                            )
                            self.assertTrue(parsed.authorized)
                            self.assertNotIn("revoke", [event.action for event in parsed.events])
                for wording in (
                    f"Push permission {morphology}.",
                    f"Permission to push {morphology}.",
                ):
                    with self.subTest(kind="canonical", morphology=morphology, wording=wording):
                        parsed = SEARCH.parse_delivery_intent(f"git push target. {wording}")
                        self.assertFalse(parsed.authorized)
                        self.assertIn("revoke:push", [event.action for event in parsed.events])

    def test_repo_delivery_discourse_prefixes_do_not_scope_bare_revocation(self) -> None:
        """Discourse and request lead-ins differ from a bound permission qualifier."""
        for prefix, separator in (
            ("but", ","),
            ("however", ";"),
            ("also", ","),
            ("note that", "."),
            ("please note that", "."),
        ):
            for morphology in ("is revoked", "was withdrawn", "has been revoked"):
                query = f"Commit these changes locally{separator} {prefix} permission {morphology}."
                with self.subTest(prefix=prefix, morphology=morphology):
                    parsed = SEARCH.parse_delivery_intent(query)
                    self.assertFalse(parsed.authorized)
                    self.assertIn("revoke", [event.action for event in parsed.events])

        for query in (
            "Commit these changes locally. Database permission was revoked.",
            "Commit these changes locally; deployment permission is withdrawn.",
            "Commit these changes locally, API permission has been revoked.",
            "Commit these changes locally. filesystem permission have been withdrawn.",
        ):
            with self.subTest(kind="qualifier", query=query):
                parsed = SEARCH.parse_delivery_intent(query)
                self.assertTrue(parsed.authorized)
                self.assertNotIn("revoke", [event.action for event in parsed.events])

    def test_repo_delivery_technical_qualifier_punctuation_boundaries(self) -> None:
        """Punctuation starts a new permission clause without splitting identifiers."""
        separators = (":", "：", " - ", " – ", " — ")
        morphologies = ("revoked", "was withdrawn", "has been revoked", "have been withdrawn")
        qualifiers = ("OAuth2", "S3", "database_read", "api.v2", "team/service")
        for separator in separators:
            for morphology in morphologies:
                bare = SEARCH.parse_delivery_intent(
                    f"Commit these changes locally{separator} permission {morphology}."
                )
                with self.subTest(kind="bare", separator=separator, morphology=morphology):
                    self.assertFalse(bare.authorized)
                    self.assertIn("revoke", [event.action for event in bare.events])
                for qualifier in qualifiers:
                    with self.subTest(kind="qualifier", separator=separator, morphology=morphology, qualifier=qualifier):
                        parsed = SEARCH.parse_delivery_intent(
                            f"Commit these changes locally{separator} {qualifier} permission {morphology}."
                        )
                        self.assertTrue(parsed.authorized)
                        self.assertNotIn("revoke", [event.action for event in parsed.events])

    def test_repo_delivery_revision19_occurrence_local_regressions(self) -> None:
        """Questions, scopes, PR lifecycles, and CJK commands stay occurrence-local."""
        for action, object_text in (("cherry-pick", "this commit"), ("fast-forward", "this branch")):
            inquiry = f"Is permission to {action} {object_text} granted"
            declarative = f"Permission to {action} {object_text} is granted"
            with self.subTest(kind="inquiry", action=action):
                self.assertFalse(SEARCH.has_authorized_delivery_action(inquiry))
            with self.subTest(kind="declarative", action=action):
                self.assertTrue(SEARCH.has_authorized_delivery_action(declarative))

        for query, expected in (
            ("Commit these changes locally. Therefore permission is revoked.", False),
            ("Commit these changes locally. OAuth 2.0 permission is revoked.", True),
        ):
            with self.subTest(kind="scope", query=query):
                self.assertEqual(expected, SEARCH.has_authorized_delivery_action(query))

        cases = {
            "创建 PR，随后不要再次创建 PR，随后提交并推送这些更改。": (
                ["pr-open", "pr-denied"], False,
            ),
            "File a PR, then start a deployment, then cancel it, then commit these changes locally.": (
                ["pr-open", "pr-cancel-mutation"], False,
            ),
            "创建 PR，随后取消部署，随后提交这些更改。": (["pr-open"], False),
        }
        for query, (expected_events, expected) in cases.items():
            with self.subTest(kind="pr", query=query):
                parsed = SEARCH.parse_delivery_intent(query)
                self.assertEqual(expected_events, [event.action for event in parsed.events if event.owner == "publishing"])
                self.assertEqual(expected, parsed.authorized)

        query = "我想知道是否可以提交数据库值，然后请提交这些 Git 更改。"
        parsed = SEARCH.parse_delivery_intent(query)
        commits = [event for event in parsed.events if event.action == "commit"]
        self.assertEqual(["inquiry", "command"], [event.modality for event in commits])
        self.assertTrue(parsed.authorized)

    def test_repo_delivery_revision19_adjacent_inverted_inquiries_are_occurrence_local(self) -> None:
        """A comma/then continuation cannot turn its preceding permission question into a grant."""
        for query in (
            "Is permission to cherry-pick this commit granted, then review the diff.",
            "Is permission to fast-forward this branch granted, then commit this database value.",
            "Do not make any Git changes. Is permission to cherry-pick this commit granted, then review the diff.",
        ):
            with self.subTest(kind="inquiry", query=query):
                parsed = SEARCH.parse_delivery_intent(query)
                queried = next(event for event in parsed.events if event.action in {"cherry-pick", "fast-forward"})
                self.assertEqual("inquiry", queried.modality)
                self.assertFalse(parsed.authorized)

        declarative = SEARCH.parse_delivery_intent(
            "Permission to cherry-pick this commit is granted, then review the diff."
        )
        self.assertTrue(declarative.authorized)
        self.assertEqual("reauthorize", next(event for event in declarative.events if event.action == "cherry-pick").modality)

        independent = SEARCH.parse_delivery_intent(
            "Is permission to cherry-pick this commit granted, then git commit -am fix."
        )
        queried = next(event for event in independent.events if event.action == "cherry-pick")
        self.assertEqual("inquiry", queried.modality)
        self.assertTrue(independent.authorized)

    def test_repo_delivery_revision19_separator_cli_and_cherry_pick_aliases(self) -> None:
        """A later CLI command and a cherry-pick object's commit stay separate occurrences."""
        for separator in ("but", "while", ":", "：", " - ", " – ", " — "):
            query = f"Is permission to cherry-pick this commit granted {separator} git commit -am fix."
            with self.subTest(kind="separator", separator=separator):
                parsed = SEARCH.parse_delivery_intent(query)
                events = [event for event in parsed.events if event.action in {"cherry-pick", "commit"}]
                self.assertEqual(["cherry-pick", "commit"], [event.action for event in events])
                self.assertEqual(["inquiry", "command"], [event.modality for event in events])
                self.assertTrue(parsed.authorized)

        for spelling in ("cherry pick", "cherry-pick"):
            inquiry = SEARCH.parse_delivery_intent(
                f"Is permission to {spelling} this reviewed commit granted, then review the diff."
            )
            self.assertFalse(inquiry.authorized)
            self.assertEqual(["cherry-pick"], [event.action for event in inquiry.events if event.action in {"cherry-pick", "commit"}])
            declarative = SEARCH.parse_delivery_intent(
                f"Permission to {spelling} this reviewed commit is granted, then review the diff."
            )
            self.assertTrue(declarative.authorized)
            self.assertEqual(["cherry-pick"], [event.action for event in declarative.events if event.action in {"cherry-pick", "commit"}])

        later = SEARCH.parse_delivery_intent(
            "Permission to cherry pick this reviewed commit is granted, then git commit -am fix."
        )
        self.assertEqual(["cherry-pick", "commit"], [event.action for event in later.events if event.action in {"cherry-pick", "commit"}])
        self.assertTrue(later.authorized)

        for modifiers in (
            "this already reviewed",
            "this already reviewed upstream",
            "this already reviewed upstream candidate",
        ):
            for spelling in ("cherry pick", "cherry-pick"):
                declarative = SEARCH.parse_delivery_intent(
                    f"Permission to {spelling} {modifiers} commit is granted."
                )
                inquiry = SEARCH.parse_delivery_intent(
                    f"Is permission to {spelling} {modifiers} commit granted?"
                )
                with self.subTest(kind="long-object", spelling=spelling, modifiers=modifiers):
                    self.assertTrue(declarative.authorized)
                    self.assertFalse(inquiry.authorized)
                    self.assertEqual(["cherry-pick"], [event.action for event in declarative.events if event.action in {"cherry-pick", "commit"}])
                    self.assertEqual(["cherry-pick"], [event.action for event in inquiry.events if event.action in {"cherry-pick", "commit"}])
                for connector in ("then", "but", "while"):
                    later = SEARCH.parse_delivery_intent(
                        f"Permission to {spelling} {modifiers} commit is granted, {connector} git commit -am fix."
                    )
                    with self.subTest(kind="long-object-later", spelling=spelling, modifiers=modifiers, connector=connector):
                        self.assertEqual(["cherry-pick", "commit"], [event.action for event in later.events if event.action in {"cherry-pick", "commit"}])
                        self.assertTrue(later.authorized)

    def test_repo_delivery_revision20_inquiry_boundaries_and_pr_denials(self) -> None:
        """Coordinated questions and denied PR opens cannot leak authority or erase antecedents."""
        for query, actions in (
            ("Can I cherry-pick this commit, then git commit -am fix?", ["cherry-pick", "commit"]),
            ("May I fast-forward this branch, then git push origin HEAD?", ["fast-forward", "push"]),
        ):
            with self.subTest(kind="coordinated-question", query=query):
                parsed = SEARCH.parse_delivery_intent(query)
                events = [event for event in parsed.events if event.action in actions]
                self.assertEqual(actions, [event.action for event in events])
                self.assertEqual(["inquiry", "inquiry"], [event.modality for event in events])
                self.assertFalse(parsed.authorized)

        independent = {
            "我想知道是否可以提交数据库值，然后 git commit -am fix.": (["commit", "commit"], ["inquiry", "command"], True),
            "我想知道是否可以提交数据库值。然后 git commit -am fix.": (["commit", "commit"], ["inquiry", "command"], True),
            "Do not cherry-pick this commit. Therefore git commit -am fix.": (["cherry-pick", "commit"], ["deny", "command"], True),
        }
        for query, (actions, modalities, expected) in independent.items():
            with self.subTest(kind="independent-cli", query=query):
                parsed = SEARCH.parse_delivery_intent(query)
                events = [event for event in parsed.events if event.action in {"cherry-pick", "commit"}]
                self.assertEqual(actions, [event.action for event in events])
                self.assertEqual(modalities, [event.modality for event in events])
                self.assertEqual(expected, parsed.authorized)

        lifecycles = {
            "File a PR, then do not file another PR, then cancel it, then commit these changes locally.": (["pr-open", "pr-denied", "pr-cancel-pending"], True),
            "File a PR. Do not file another PR. Cancel it. Commit these changes locally.": (["pr-open", "pr-denied", "pr-cancel-pending"], True),
            "创建 PR。不要再次创建 PR。取消它。提交这些更改。": (["pr-open", "pr-denied", "pr-cancel-pending"], True),
        }
        for query, (expected_events, expected) in lifecycles.items():
            with self.subTest(kind="pr-denial", query=query):
                parsed = SEARCH.parse_delivery_intent(query)
                self.assertEqual(expected_events, [event.action for event in parsed.events if event.owner == "publishing"])
                self.assertEqual(expected, parsed.authorized)

    def test_project_grounding_literal_does_not_fan_out_to_map_or_review(self) -> None:
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        names = {result["name"] for result in SEARCH.search(index, "project grounding")}
        self.assertNotIn("repo-map", names)
        self.assertNotIn("repo-review", names)

    def test_full_index_keeps_frontend_implementation_and_java_audit_discoverable(self) -> None:
        index = json.loads((ROOT / "skills-index.json").read_text(encoding="utf-8"))
        self.assertEqual("dev-frontend", SEARCH.search(index, "implement a frontend component")[0]["name"])
        self.assertEqual("audit-java", SEARCH.search(index, "audit a Java service")[0]["name"])


if __name__ == "__main__":
    unittest.main()
