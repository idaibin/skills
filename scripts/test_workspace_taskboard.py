#!/usr/bin/env python3
"""Focused regressions for Workspace Taskboard project-root control."""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "skills" / "workspace-taskboard" / "scripts" / "task_control.py"
SPEC = importlib.util.spec_from_file_location("workspace_taskboard_control", MODULE)
assert SPEC and SPEC.loader
CONTROL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTROL)

CAPS = {"list_projects": True, "list_threads": True, "read_thread": True, "create_thread": True, "send_message_to_thread": True, "persistent_registry": True}


class FileRegistryFixture:
    """Executable non-LLM fixture for persistent readback and optimistic CAS."""

    def __init__(self, path: Path):
        self.path = path
        self._lock = threading.Lock()
        self.events = []
        self._event_operations = set()

    def read(self):
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text(encoding="utf-8"))

    def cas(self, expected_digest, manifest):
        errors = CONTROL.validate_manifest(manifest)
        if errors:
            return {"applied": False, "reason": "manifest-invalid", "errors": errors}
        with self._lock:
            current = self.read()
            current_digest = current["manifest_digest"] if current else None
            if current_digest != expected_digest:
                return {"applied": False, "reason": "basis-drift", "current_digest": current_digest}
            record = {
                "schema_version": "workspace-taskboard-registry-fixture/v1",
                "registry_version": 1 if current is None else current["registry_version"] + 1,
                "manifest_digest": CONTROL.digest(manifest),
                "manifest": manifest,
            }
            temporary = self.path.with_suffix(f".tmp-{threading.get_ident()}")
            temporary.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True), encoding="utf-8")
            os.replace(temporary, self.path)
            return {"applied": True, **record}

    def record_event_if_current(self, plan):
        """Model the adapter's atomic registry check and idempotent board-event boundary."""
        with self._lock:
            current = self.read()
            if not current or current["manifest_digest"] != plan["expected_registry_digest"]:
                return {"recorded": False, "reason": "basis-drift"}
            controller = current["manifest"]["current_controller_thread_id"]
            if controller != plan["expected_controller_thread_id"]:
                return {"recorded": False, "reason": "controller-rebound"}
            if plan["operation_id"] in self._event_operations:
                return {"recorded": False, "reason": "already-recorded"}
            self._event_operations.add(plan["operation_id"])
            self.events.append({"operation_id": plan["operation_id"], "controller_thread_id": controller, "worker_thread_id": plan["worker_thread_id"], "unread": True})
            return {"recorded": True, "controller_thread_id": controller}


class WorkspaceTaskboardTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name)
        self.root = base / "repo"
        self.root.mkdir()
        self.frontend = self.root / "frontend"
        self.frontend.mkdir()
        self.backend = self.root / "backend"
        self.backend.mkdir()
        self.sibling = base / "repo-other"
        self.sibling.mkdir()
        self.prefix = base / "repo-copy"
        self.prefix.mkdir()
        self.outside = base / "outside"
        self.outside.mkdir()
        self.project = {
            "project_id": "project-1", "project_identity": "git:test/repo", "project_kind": "local",
            "canonical_project_root": CONTROL.canonical_path(str(self.root)),
            "allowed_roots": [CONTROL.canonical_path(str(self.root))], "allowed_roots_version": "readback-1",
            "allowed_root_membership": [{"canonical_root": CONTROL.canonical_path(str(self.root)), "source": "host-project-readback", "version": "readback-1"}],
            "membership_verified": True, "is_git_repository": False, "creation_environment": "local", "placement_readback": "required",
            "create_placement_receipts": [{"canonical_cwd": CONTROL.canonical_path(str(self.frontend)), "source": "host-create-adapter", "version": "readback-1"}],
        }

    def candidate(self, thread_id: str, cwd: Path, responsibility: str = "frontend", **values):
        item = {
            "thread_id": thread_id, "title": "Repo｜Frontend", "kind": "codex", "project_id": "project-1",
            "project_kind": "local", "cwd": str(cwd), "responsibility": responsibility, "status": "idle",
            "recent_goal": "maintain frontend", "goal_compatibility": "compatible", "host_id": "local",
        }
        item.update(values)
        return item

    def manifest(self, worker_cwd: Path | None = None, closed: bool = False):
        cwd = CONTROL.canonical_path(str(worker_cwd or self.frontend))
        key = f"git:test/repo:{cwd}:frontend"
        return {
            "schema_version": "workspace-taskboard-control/v1", "control_id": "ctl-1",
            "project_id": "project-1", "project_identity": "git:test/repo",
            "canonical_project_root": CONTROL.canonical_path(str(self.root)), "allowed_roots_version": "readback-1",
            "allowed_roots": [CONTROL.canonical_path(str(self.root))], "current_controller_thread_id": "controller-old",
            "predecessor_thread_ids": [], "default_authorization_profile": "implementation",
            "worker_mappings": [{"reuse_key": key, "thread_id": "worker-a", "canonical_cwd": cwd, "project_identity": "git:test/repo", "responsibility": "frontend", "rank": 10, "closed": closed}],
            "dependency_edges": [],
        }

    def route(self, candidates, **extra):
        payload = {
            "controller_cwd": str(self.root), "controller_project_root": str(self.root), "project_readback": self.project,
            "request": {"intent": "implementation", "responsibility": "frontend", "worker_cwd": str(self.frontend)},
            "host_capabilities": CAPS, "candidates": candidates, "worker_mappings": [],
        }
        payload.update(extra)
        return CONTROL.route(payload)

    def scope(self, manifest=None):
        result = {"project_readback": self.project, "controller_cwd": str(self.root), "controller_project_root": str(self.root)}
        if manifest is not None:
            result["manifest_digest"] = CONTROL.digest(manifest)
            result["current_registry_digest"] = CONTROL.digest(manifest)
        return result

    def test_root_and_child_cwd_are_in_scope(self):
        for cwd in (self.root, self.frontend):
            with self.subTest(cwd=cwd):
                result = self.route([self.candidate("worker", cwd)], request={"intent": "implementation", "responsibility": "frontend", "worker_cwd": str(cwd)})
                self.assertEqual("reuse-existing", result["action"])

    def test_parent_sibling_and_prefix_collision_are_rejected(self):
        for cwd in (self.root.parent, self.sibling, self.prefix):
            with self.subTest(cwd=cwd):
                result = self.route([self.candidate("outside", cwd)], request={"intent": "implementation", "responsibility": "frontend", "worker_cwd": str(cwd)})
                self.assertNotEqual("reuse-existing", result["action"])
                self.assertNotIn("outside", {item.get("thread_id") for item in result.get("choices", [])})

    def test_symlink_inside_is_accepted_and_escape_rejected(self):
        inside_link = self.root / "ui-link"
        inside_link.symlink_to(self.frontend, target_is_directory=True)
        outside_link = self.root / "escape"
        outside_link.symlink_to(self.outside, target_is_directory=True)
        accepted = self.route([self.candidate("inside", inside_link)], request={"intent": "implementation", "responsibility": "frontend", "worker_cwd": str(inside_link)})
        rejected = self.route([self.candidate("outside", outside_link)], request={"intent": "implementation", "responsibility": "frontend", "worker_cwd": str(outside_link)})
        self.assertEqual("reuse-existing", accepted["action"])
        self.assertNotEqual("reuse-existing", rejected["action"])

    def test_multi_folder_only_host_verified_roots(self):
        extra = self.outside / "attached"
        extra.mkdir()
        verified = dict(self.project, allowed_roots=[CONTROL.canonical_path(str(self.root)), CONTROL.canonical_path(str(extra))], allowed_roots_version="readback-2", allowed_root_membership=[{"canonical_root": CONTROL.canonical_path(str(self.root)), "source": "host-project-readback", "version": "readback-2"}, {"canonical_root": CONTROL.canonical_path(str(extra)), "source": "host-project-readback", "version": "readback-2"}])
        result = self.route([self.candidate("attached", extra)], project_readback=verified, request={"intent": "implementation", "responsibility": "frontend", "worker_cwd": str(extra)})
        self.assertEqual("reuse-existing", result["action"])
        unverified = dict(verified, membership_verified=False)
        result = self.route([], project_readback=unverified)
        self.assertEqual("PLACEMENT_UNVERIFIED", result["failure_code"])

    def test_same_project_but_outside_verified_roots_is_rejected(self):
        result = self.route([self.candidate("outside", self.sibling)])
        self.assertNotEqual("reuse-existing", result["action"])

    def test_unique_candidate_reuses(self):
        result = self.route([self.candidate("one", self.frontend)])
        self.assertEqual(("reuse-existing", "one"), (result["action"], result["thread_id"]))

    def test_no_candidate_defaults_to_create_without_delegation_question(self):
        base = {"manifest_digest": "sha256:basis", "control_id": "ctl-1"}
        result = self.route([], **base)
        self.assertEqual("reserve-create", result["action"])
        self.assertNotEqual("decision-needed", result["action"])

    def test_ambiguous_lists_all_in_scope_candidates_and_new(self):
        result = self.route([self.candidate("one", self.frontend), self.candidate("two", self.frontend), self.candidate("outside", self.sibling)])
        self.assertEqual("decision-needed", result["action"])
        self.assertEqual({"one", "two"}, {item["thread_id"] for item in result["choices"][:-1]})
        self.assertEqual("new-task", result["choices"][-1]["choice"])

    def test_explicit_in_scope_routes_and_out_of_scope_rejects(self):
        inside = self.route([self.candidate("inside", self.backend)], request={"intent": "implementation", "explicit_thread_id": "inside"})
        outside = self.route([self.candidate("outside", self.sibling)], request={"intent": "implementation", "explicit_thread_id": "outside"})
        self.assertEqual("queue-existing", inside["action"])
        self.assertEqual("OUT_OF_SCOPE_WORKSPACE", outside["failure_code"])

    def test_explicit_closed_or_archived_never_queues(self):
        closed = self.route([self.candidate("worker-a", self.frontend)], worker_mappings=self.manifest(closed=True)["worker_mappings"], request={"intent": "implementation", "explicit_thread_id": "worker-a"})
        archived = self.route([self.candidate("old", self.frontend, status="archived")], request={"intent": "implementation", "explicit_thread_id": "old"})
        self.assertEqual("CLOSED_TASK", closed["failure_code"])
        self.assertEqual("archived-candidate", archived["stop_state"])

    def test_send_capability_is_required_before_reuse_or_create(self):
        caps = dict(CAPS, send_message_to_thread=False)
        reused = self.route([self.candidate("worker", self.frontend)], host_capabilities=caps)
        created = self.route([], host_capabilities=caps, manifest_digest="sha256:basis", control_id="ctl-1")
        self.assertEqual("CAPABILITY_MISSING", reused["failure_code"])
        self.assertEqual("CAPABILITY_MISSING", created["failure_code"])

    def test_remote_projectless_chatgpt_excluded(self):
        candidates = [
            self.candidate("remote", self.frontend, remote=True, project_kind="remote"),
            self.candidate("projectless", self.frontend, project_id=None, projectless=True),
            self.candidate("chatgpt", self.frontend, kind="chatgpt"),
        ]
        result = self.route(candidates, manifest_digest="sha256:basis", control_id="ctl-1")
        self.assertEqual("reserve-create", result["action"])

    def test_closed_and_archived_are_excluded_and_similar_work_creates(self):
        closed_mapping = self.manifest(closed=True)["worker_mappings"]
        closed = self.candidate("worker-a", self.frontend, closed=True)
        archived = self.candidate("archived", self.frontend, status="archived")
        result = self.route([closed, archived], worker_mappings=closed_mapping, manifest_digest="sha256:basis", control_id="ctl-1")
        self.assertEqual("reserve-create", result["action"])

    def test_closed_mapping_excludes_live_task_even_without_candidate_flag(self):
        closed_mapping = self.manifest(closed=True)["worker_mappings"]
        live_host_task = self.candidate("worker-a", self.frontend)
        result = self.route([live_host_task], worker_mappings=closed_mapping, manifest_digest="sha256:basis", control_id="ctl-1")
        self.assertEqual("reserve-create", result["action"])

    def test_plan_discussion_stays_in_controller(self):
        result = self.route([], request={"intent": "architecture", "responsibility": "frontend"})
        self.assertEqual("handle-in-controller", result["action"])
        self.assertFalse(result["create"])

    def test_implementation_defaults_to_worker(self):
        result = self.route([self.candidate("worker", self.frontend)])
        self.assertEqual("reuse-existing", result["action"])
        self.assertFalse(result["execute_locally"])

    def test_unknown_intent_stops_instead_of_guessing(self):
        result = self.route([], request={"intent": "maybe"})
        self.assertEqual("intent-uncertain", result["stop_state"])

    def test_create_uses_host_environment_and_one_shot_reservation(self):
        base = {"manifest_digest": "sha256:basis", "control_id": "ctl-1"}
        reserved = self.route([], **base)
        record = {"control_id": "ctl-1", "operation_id": reserved["operation_id"], "manifest_digest": "sha256:basis", "state": "reserved", "acquired": True, "claim_token": "winner"}
        created = self.route([], **base, create_reservation=record, create_claim_token="winner")
        loser = self.route([], **base, create_reservation=record, create_claim_token="loser")
        self.assertEqual("invoke-create-via-adapter", created["action"])
        self.assertFalse(created["direct_host_create"])
        self.assertEqual("reconcile-create", loser["action"])

    def test_create_readback_finalizes_only_verified_placement(self):
        manifest_digest = "sha256:basis"
        control_id = "ctl-1"
        key = f"git:test/repo:{CONTROL.canonical_path(str(self.frontend))}:frontend"
        operation_id = "create:" + CONTROL.hashlib.sha256(f"{control_id}:{manifest_digest}:{key}".encode()).hexdigest()
        operation = {"operation_id": operation_id, "state": "completed", "thread_id": "created", "control_id": control_id, "manifest_digest": manifest_digest, "reuse_key": key}
        created = self.candidate("created", self.frontend, host_id="local")
        base = {"controller_cwd": str(self.root), "controller_project_root": str(self.root), "project_readback": self.project, "create_operation": operation, "created_task": created, "request": {"responsibility": "frontend", "worker_cwd": str(self.frontend)}, "manifest_digest": manifest_digest, "control_id": control_id}
        result = CONTROL.create_readback_plan(base)
        self.assertEqual("finalize-created-worker", result["action"])
        self.assertEqual(CONTROL.canonical_path(str(self.frontend)), result["mapping"]["canonical_cwd"])
        escaped = self.candidate("created", self.sibling, host_id="local")
        result = CONTROL.create_readback_plan({**base, "created_task": escaped})
        self.assertEqual("PLACEMENT_UNVERIFIED", result["failure_code"])

    def test_create_readback_rejects_foreign_operation_or_wrong_requested_cwd(self):
        base_digest = "sha256:basis"
        key = f"git:test/repo:{CONTROL.canonical_path(str(self.frontend))}:frontend"
        operation_id = "create:" + CONTROL.hashlib.sha256(f"ctl-1:{base_digest}:{key}".encode()).hexdigest()
        operation = {"operation_id": operation_id, "state": "completed", "thread_id": "created", "control_id": "ctl-1", "manifest_digest": base_digest, "reuse_key": key}
        payload = {"controller_cwd": str(self.root), "controller_project_root": str(self.root), "project_readback": self.project, "create_operation": operation, "created_task": self.candidate("created", self.frontend), "request": {"responsibility": "frontend", "worker_cwd": str(self.frontend)}, "manifest_digest": base_digest, "control_id": "ctl-1"}
        foreign = CONTROL.create_readback_plan({**payload, "create_operation": {**operation, "operation_id": "create:foreign"}})
        wrong_cwd = CONTROL.create_readback_plan({**payload, "created_task": self.candidate("created", self.backend)})
        self.assertEqual("SUBMISSION_UNCERTAIN", foreign["failure_code"])
        self.assertEqual("BASIS_DRIFT", wrong_cwd["failure_code"])

    def test_create_placement_unverified_fails_closed(self):
        for project in (dict(self.project, placement_readback=None), dict(self.project, creation_environment="worktree"), dict(self.project, is_git_repository=True, creation_environment="local")):
            with self.subTest(project=project):
                result = self.route([], project_readback=project, manifest_digest="sha256:basis", control_id="ctl-1")
                self.assertEqual("PLACEMENT_UNVERIFIED", result["failure_code"])

    def test_child_create_requires_exact_host_placement_receipt(self):
        without_receipt = dict(self.project, create_placement_receipts=[])
        child = self.route([], project_readback=without_receipt, manifest_digest="sha256:basis", control_id="ctl-1")
        self.assertEqual("PLACEMENT_UNVERIFIED", child["failure_code"])
        self.assertFalse(child["create"])

        root = self.route(
            [], project_readback=without_receipt, manifest_digest="sha256:basis", control_id="ctl-1",
            request={"intent": "implementation", "responsibility": "root-canary", "worker_cwd": str(self.root)},
        )
        self.assertEqual("reserve-create", root["action"])

    def test_permissions_are_not_expanded(self):
        skill = (ROOT / "skills" / "workspace-taskboard" / "SKILL.md").read_text(encoding="utf-8")
        for token in ("does not authorize commit", "does not authorize push", "does not authorize deployment", "separate explicit authorization"):
            self.assertIn(token, skill)

    def test_manifest_accepts_child_mapping_and_rejects_escape(self):
        current = self.manifest()
        self.assertEqual([], CONTROL.validate_manifest(current))
        escaped = self.manifest()
        escaped["worker_mappings"][0]["canonical_cwd"] = CONTROL.canonical_path(str(self.sibling))
        escaped["worker_mappings"][0]["reuse_key"] = f"git:test/repo:{CONTROL.canonical_path(str(self.sibling))}:frontend"
        self.assertTrue(CONTROL.validate_manifest(escaped))

    def test_resume_rebinds_live_child_and_excludes_closed(self):
        current = self.manifest()
        basis = CONTROL.digest(current)
        result = CONTROL.resume_plan({
            "host_capabilities": CAPS, "manifest": current, "manifest_digest": basis, "current_registry_digest": basis,
            "project_readback": self.project, "new_controller_thread_id": "controller-new", "new_controller_cwd": str(self.root),
            "observed_new_controller": self.candidate("controller-new", self.root, responsibility="controller"),
            "effective_authorization_profile": "implementation", "observed_workers": [self.candidate("worker-a", self.frontend)],
        })
        self.assertEqual("resume-rebind", result["action"])
        self.assertEqual(["worker-a"], [item["thread_id"] for item in result["messages"]])
        closed = self.manifest(closed=True)
        closed_basis = CONTROL.digest(closed)
        result = CONTROL.resume_plan({**{
            "host_capabilities": CAPS, "manifest": closed, "manifest_digest": closed_basis, "current_registry_digest": closed_basis,
            "project_readback": self.project, "new_controller_thread_id": "controller-new", "new_controller_cwd": str(self.root),
            "observed_new_controller": self.candidate("controller-new", self.root, responsibility="controller"), "effective_authorization_profile": "implementation", "observed_workers": []},
        })
        self.assertEqual([], result["messages"])

    def test_resume_controller_in_verified_attached_root(self):
        attached = self.outside / "attached-controller"
        attached.mkdir()
        attached_project = dict(self.project, allowed_roots=[CONTROL.canonical_path(str(self.root)), CONTROL.canonical_path(str(attached))], allowed_roots_version="readback-2", allowed_root_membership=[{"canonical_root": CONTROL.canonical_path(str(self.root)), "source": "host-project-readback", "version": "readback-2"}, {"canonical_root": CONTROL.canonical_path(str(attached)), "source": "host-project-readback", "version": "readback-2"}])
        current = self.manifest()
        current["allowed_roots"] = attached_project["allowed_roots"]
        current["allowed_roots_version"] = "readback-2"
        basis = CONTROL.digest(current)
        result = CONTROL.resume_plan({"host_capabilities": CAPS, "manifest": current, "manifest_digest": basis, "current_registry_digest": basis, "project_readback": attached_project, "new_controller_thread_id": "controller-new", "new_controller_cwd": str(attached), "observed_new_controller": self.candidate("controller-new", attached, responsibility="controller"), "effective_authorization_profile": "implementation", "observed_workers": [self.candidate("worker-a", self.frontend)]})
        self.assertEqual("resume-rebind", result["action"])

    def test_resume_different_project_or_outside_controller_fails(self):
        current = self.manifest()
        basis = CONTROL.digest(current)
        result = CONTROL.resume_plan({"host_capabilities": CAPS, "manifest": current, "manifest_digest": basis, "current_registry_digest": basis, "project_readback": self.project, "new_controller_thread_id": "new", "new_controller_cwd": str(self.sibling), "observed_new_controller": self.candidate("new", self.sibling, responsibility="controller")})
        self.assertIn(result.get("failure_code"), {"BASIS_DRIFT", "OUT_OF_SCOPE_WORKSPACE"})

    def test_resume_cannot_elevate_or_use_unknown_authorization_profile(self):
        current = self.manifest()
        basis = CONTROL.digest(current)
        base = {"host_capabilities": CAPS, "manifest": current, "manifest_digest": basis, "current_registry_digest": basis, "project_readback": self.project, "new_controller_thread_id": "controller-new", "new_controller_cwd": str(self.root), "observed_new_controller": self.candidate("controller-new", self.root, responsibility="controller"), "observed_workers": [self.candidate("worker-a", self.frontend)]}
        elevated = CONTROL.resume_plan({**base, "effective_authorization_profile": "controlled-delivery"})
        unknown = CONTROL.resume_plan({**base, "effective_authorization_profile": "superuser"})
        self.assertEqual("authority-elevation-unproven", elevated["reason"])
        self.assertEqual("unknown-profile", unknown["reason"])
        self.assertNotIn("messages", elevated)

    def test_terminal_notification_records_unread_board_event(self):
        current = self.manifest()
        result = CONTROL.notification_plan({"manifest": current, **self.scope(current), "observed_controller": self.candidate("controller-old", self.root, responsibility="controller"), "observed_worker": self.candidate("worker-a", self.frontend), "event_sequence": 2})
        self.assertEqual("record-board-event", result["action"])
        self.assertFalse(result["direct_host_send"])
        self.assertFalse(result["inject_overview_message"])
        self.assertTrue(result["unread"])
        current["worker_mappings"][0]["closed"] = True
        stopped = CONTROL.notification_plan({"manifest": current, **self.scope(current), "observed_controller": self.candidate("controller-old", self.root, responsibility="controller"), "observed_worker": self.candidate("worker-a", self.frontend)})
        self.assertEqual("BASIS_DRIFT", stopped["failure_code"])

    def test_decision_and_authorization_events_open_structured_surfaces(self):
        current = self.manifest()
        base = {"manifest": current, **self.scope(current), "observed_controller": self.candidate("controller-old", self.root, responsibility="controller"), "observed_worker": self.candidate("worker-a", self.frontend), "event_sequence": 3}
        decision = CONTROL.notification_plan({**base, "event_kind": "decision"})
        approval = CONTROL.notification_plan({**base, "event_kind": "authorization"})
        invalid = CONTROL.notification_plan({**base, "event_kind": "chat-message"})
        self.assertEqual(("open-decision-panel", True), (decision["interaction"], decision["requires_user_action"]))
        self.assertEqual(("open-native-approval", True), (approval["interaction"], approval["requires_user_action"]))
        self.assertEqual("identity-incomplete", invalid["stop_state"])

    def test_notification_adapter_prevents_event_after_controller_rebind(self):
        registry = FileRegistryFixture(self.root.parent / "notify-registry.json")
        initial = self.manifest()
        created = registry.cas(None, initial)
        plan = CONTROL.notification_plan({
            "manifest": initial, **self.scope(initial),
            "observed_controller": self.candidate("controller-old", self.root, responsibility="controller"),
            "observed_worker": self.candidate("worker-a", self.frontend), "event_sequence": 7,
        })
        rebound = json.loads(json.dumps(initial))
        rebound["predecessor_thread_ids"] = ["controller-old"]
        rebound["current_controller_thread_id"] = "controller-new"
        self.assertTrue(registry.cas(created["manifest_digest"], rebound)["applied"])
        self.assertEqual({"recorded": False, "reason": "basis-drift"}, registry.record_event_if_current(plan))
        self.assertEqual([], registry.events)

        rebound_scope = self.scope(rebound)
        rebound_plan = CONTROL.notification_plan({
            "manifest": rebound, **rebound_scope,
            "observed_controller": self.candidate("controller-new", self.root, responsibility="controller"),
            "observed_worker": self.candidate("worker-a", self.frontend), "event_sequence": 7,
        })
        self.assertTrue(registry.record_event_if_current(rebound_plan)["recorded"])
        self.assertEqual("already-recorded", registry.record_event_if_current(rebound_plan)["reason"])
        self.assertEqual(["controller-new"], [item["controller_thread_id"] for item in registry.events])

    def test_stale_registry_snapshot_cannot_notify_or_close(self):
        stale = self.manifest()
        current = json.loads(json.dumps(stale))
        current["predecessor_thread_ids"] = ["controller-old"]
        current["current_controller_thread_id"] = "controller-new"
        basis = {"manifest_digest": CONTROL.digest(stale), "current_registry_digest": CONTROL.digest(current)}
        notify = CONTROL.notification_plan({"manifest": stale, **self.scope(), **basis, "observed_controller": self.candidate("controller-old", self.root, responsibility="controller"), "observed_worker": self.candidate("worker-a", self.frontend)})
        close = CONTROL.close_plan({"manifest": stale, **self.scope(), **basis, "thread_id": "worker-a", "explicit_user_close_authorization": True, "archive_readback": self.candidate("worker-a", self.frontend, archived=True)})
        self.assertEqual(["BASIS_DRIFT", "BASIS_DRIFT"], [notify["failure_code"], close["failure_code"]])
        self.assertNotIn("send", notify)
        self.assertNotIn("updated_manifest", close)

    def test_close_requires_authorization_and_archive_readback(self):
        current = self.manifest()
        dry = CONTROL.close_plan({"manifest": current, **self.scope(current), "thread_id": "worker-a"})
        self.assertEqual("dry-run-close", dry["action"])
        self.assertFalse(dry["archive"])
        missing = CONTROL.close_plan({"manifest": current, **self.scope(current), "thread_id": "worker-a", "explicit_user_close_authorization": True})
        self.assertEqual("ARCHIVE_UNVERIFIED", missing["failure_code"])
        archived = self.candidate("worker-a", self.frontend, status="archived")
        closed = CONTROL.close_plan({"manifest": current, **self.scope(current), "thread_id": "worker-a", "explicit_user_close_authorization": True, "archive_readback": archived})
        self.assertEqual("close-card", closed["action"])
        self.assertTrue(closed["updated_manifest"]["worker_mappings"][0]["closed"])
        receipt = self.candidate("worker-a", self.frontend, status="notLoaded", archived=True)
        closed_from_receipt = CONTROL.close_plan({"manifest": current, **self.scope(current), "thread_id": "worker-a", "explicit_user_close_authorization": True, "archive_readback": receipt})
        self.assertEqual("close-card", closed_from_receipt["action"])
        bare_receipt = {"thread_id": "worker-a", "archived": True}
        rejected = CONTROL.close_plan({"manifest": current, **self.scope(current), "thread_id": "worker-a", "explicit_user_close_authorization": True, "archive_readback": bare_receipt})
        self.assertEqual("ARCHIVE_UNVERIFIED", rejected["failure_code"])

    def test_registry_fixture_persists_cas_rebind_and_closed_policy(self):
        registry = FileRegistryFixture(self.root.parent / "registry.json")
        initial = self.manifest()
        created = registry.cas(None, initial)
        self.assertTrue(created["applied"])
        self.assertEqual((1, CONTROL.digest(initial)), (registry.read()["registry_version"], registry.read()["manifest_digest"]))

        rebound = json.loads(json.dumps(initial))
        rebound["predecessor_thread_ids"] = [initial["current_controller_thread_id"]]
        rebound["current_controller_thread_id"] = "controller-new"
        outcomes = []
        barrier = threading.Barrier(2)

        def attempt(value):
            barrier.wait()
            outcomes.append(registry.cas(created["manifest_digest"], value))

        first = threading.Thread(target=attempt, args=(rebound,))
        second = threading.Thread(target=attempt, args=(rebound,))
        first.start()
        second.start()
        first.join()
        second.join()
        self.assertEqual(1, sum(item["applied"] for item in outcomes))
        self.assertEqual(1, sum(item.get("reason") == "basis-drift" for item in outcomes))

        live = registry.read()
        self.assertEqual("controller-new", live["manifest"]["current_controller_thread_id"])
        closed = json.loads(json.dumps(live["manifest"]))
        closed["worker_mappings"][0]["closed"] = True
        applied = registry.cas(live["manifest_digest"], closed)
        self.assertTrue(applied["applied"])
        readback = registry.read()
        self.assertTrue(readback["manifest"]["worker_mappings"][0]["closed"])
        self.assertEqual(applied["manifest_digest"], readback["manifest_digest"])

        routed = self.route(
            [self.candidate("worker-a", self.frontend, status="archived")],
            worker_mappings=readback["manifest"]["worker_mappings"],
            manifest_digest=readback["manifest_digest"],
            control_id=readback["manifest"]["control_id"],
        )
        self.assertEqual("reserve-create", routed["action"])

    def test_hide_card_is_presentation_only_and_worker_remains_reusable(self):
        current = self.manifest()
        hidden = CONTROL.visibility_plan({"manifest": current, **self.scope(current), "thread_id": "worker-a", "hidden": True})
        self.assertEqual("hide-card", hidden["action"])
        self.assertFalse(hidden["worker_lifecycle_changed"])
        hidden_manifest = hidden["updated_manifest"]
        self.assertTrue(hidden_manifest["worker_mappings"][0]["hidden"])
        projection = CONTROL.status_projection({"manifest": hidden_manifest, **self.scope(hidden_manifest), "observed_threads": [self.candidate("worker-a", self.frontend)]})
        self.assertEqual(([], 1), (projection["cards"], projection["hidden_count"]))
        routed = self.route([self.candidate("worker-a", self.frontend)], worker_mappings=hidden_manifest["worker_mappings"])
        self.assertEqual("reuse-existing", routed["action"])

    def test_status_projection_groups_and_turn_completed_not_finished(self):
        current = self.manifest()
        projection = CONTROL.status_projection({"manifest": current, **self.scope(current), "observed_threads": [self.candidate("worker-a", self.frontend, status="completed")], "worker_envelopes": []})
        card = projection["cards"][0]
        self.assertEqual("执行中", card["group"])
        self.assertNotEqual("finished", card["worker_status"])
        envelope = {"type": "worker-status", "schema_version": "workspace-taskboard-worker-status/v1", "control_id": "ctl-1", "worker_thread_id": "worker-a", "reuse_key": current["worker_mappings"][0]["reuse_key"], "status": "finished", "event_sequence": 2, "observed_at": "2026-08-13T00:00:00Z", "worker_basis_digest": CONTROL.worker_status_basis(current, current["worker_mappings"][0]), "allowed_roots_version": "readback-1", "canonical_cwd": CONTROL.canonical_path(str(self.frontend)), "recommended_next_action": "review"}
        finished = CONTROL.status_projection({"manifest": current, **self.scope(current), "observed_threads": [self.candidate("worker-a", self.frontend, status="completed")], "worker_envelopes": [envelope]})
        self.assertEqual("已结束", finished["cards"][0]["group"])
        self.assertTrue(finished["cards"][0]["unread"])
        read = CONTROL.status_projection({"manifest": current, **self.scope(current), "observed_threads": [self.candidate("worker-a", self.frontend, status="completed")], "worker_envelopes": [envelope], "last_read_sequences": {"worker-a": 2}})
        self.assertFalse(read["cards"][0]["unread"])
        self.assertFalse(finished["updates_existing_message"])

    def test_live_only_status_requires_no_registry(self):
        result = CONTROL.status_projection({**self.scope(), "observed_threads": [self.candidate("worker-a", self.frontend, status="active")]})
        self.assertEqual(("status-projection", "live-only", "running"), (result["action"], result["registry_mode"], result["cards"][0]["host_status"]))
        self.assertNotIn("closed", result["cards"][0]["board_status"])

    def test_archived_true_is_never_reused_rebound_notified_or_shown_active(self):
        archived = self.candidate("worker-a", self.frontend, status="notLoaded", archived=True)
        explicit = self.route([archived], request={"intent": "implementation", "explicit_thread_id": "worker-a"})
        automatic = self.route([archived], worker_mappings=self.manifest()["worker_mappings"], manifest_digest="sha256:basis", control_id="ctl-1")
        self.assertEqual("archived-candidate", explicit["stop_state"])
        self.assertEqual("reserve-create", automatic["action"])

        current = self.manifest()
        basis = CONTROL.digest(current)
        resumed = CONTROL.resume_plan({"host_capabilities": CAPS, "manifest": current, "manifest_digest": basis, "current_registry_digest": basis, "project_readback": self.project, "new_controller_thread_id": "controller-new", "new_controller_cwd": str(self.root), "observed_new_controller": self.candidate("controller-new", self.root, responsibility="controller"), "effective_authorization_profile": "implementation", "observed_workers": [archived]})
        self.assertEqual([], resumed["messages"])
        self.assertEqual("archived", resumed["terminated_workers"][0]["status"])
        notified = CONTROL.notification_plan({"manifest": current, **self.scope(current), "observed_controller": self.candidate("controller-old", self.root, responsibility="controller"), "observed_worker": archived})
        self.assertEqual("BASIS_DRIFT", notified["failure_code"])
        card = CONTROL.status_projection({"manifest": current, **self.scope(current), "observed_threads": [archived]})["cards"][0]
        self.assertEqual(("archived", "blocked", "等待"), (card["host_status"], card["worker_status"], card["group"]))

    def test_worker_envelope_survives_unrelated_board_metadata_cas(self):
        current = self.manifest()
        mapping = current["worker_mappings"][0]
        envelope = {"type": "worker-status", "schema_version": "workspace-taskboard-worker-status/v1", "control_id": "ctl-1", "worker_thread_id": "worker-a", "reuse_key": mapping["reuse_key"], "status": "finished", "event_sequence": 4, "observed_at": "2026-08-13T00:00:00Z", "worker_basis_digest": CONTROL.worker_status_basis(current, mapping), "allowed_roots_version": "readback-1", "canonical_cwd": mapping["canonical_cwd"], "recommended_next_action": "review"}
        updated = json.loads(json.dumps(current))
        updated["current_controller_thread_id"] = "controller-new"
        updated["predecessor_thread_ids"] = ["controller-old"]
        updated["worker_mappings"][0]["rank"] = 99
        updated["dependency_edges"] = [{"producer_reuse_key": mapping["reuse_key"], "consumer_reuse_key": mapping["reuse_key"]}]
        card = CONTROL.status_projection({"manifest": updated, **self.scope(updated), "observed_threads": [self.candidate("worker-a", self.frontend)], "worker_envelopes": [envelope]})["cards"][0]
        self.assertEqual("finished", card["worker_status"])
        moved = json.loads(json.dumps(updated))
        moved["worker_mappings"][0]["canonical_cwd"] = CONTROL.canonical_path(str(self.backend))
        moved["worker_mappings"][0]["reuse_key"] = f"git:test/repo:{CONTROL.canonical_path(str(self.backend))}:frontend"
        moved["dependency_edges"] = []
        moved_card = CONTROL.status_projection({"manifest": moved, **self.scope(moved), "observed_threads": [self.candidate("worker-a", self.backend)], "worker_envelopes": [envelope]})["cards"][0]
        self.assertNotEqual("finished", moved_card["worker_status"])

    def test_deleted_worker_cwd_keeps_manifest_readable_and_live_escape_rejected(self):
        current = self.manifest()
        self.frontend.rmdir()
        self.assertEqual([], CONTROL.validate_manifest(current))
        card = CONTROL.status_projection({"manifest": current, **self.scope(current)})["cards"][0]
        self.assertEqual(("unreachable", "blocked"), (card["host_status"], card["worker_status"]))
        self.frontend.symlink_to(self.outside, target_is_directory=True)
        escaped = self.route([self.candidate("worker-a", self.frontend)], request={"intent": "implementation", "explicit_thread_id": "worker-a"})
        self.assertEqual("OUT_OF_SCOPE_WORKSPACE", escaped["failure_code"])

    def test_deleted_attached_root_keeps_manifest_readable_and_symlink_escape_rejected(self):
        attached = self.outside / "attached-deleted"
        attached.mkdir()
        root_path = CONTROL.canonical_path(str(self.root))
        attached_path = CONTROL.canonical_path(str(attached))
        project = dict(
            self.project,
            allowed_roots=[root_path, attached_path],
            allowed_roots_version="readback-2",
            allowed_root_membership=[
                {"canonical_root": root_path, "source": "host-project-readback", "version": "readback-2"},
                {"canonical_root": attached_path, "source": "host-project-readback", "version": "readback-2"},
            ],
        )
        current = self.manifest(worker_cwd=attached)
        current["allowed_roots"] = [root_path, attached_path]
        current["allowed_roots_version"] = "readback-2"
        attached.rmdir()
        self.assertEqual([], CONTROL.validate_manifest(current))
        card = CONTROL.status_projection({
            "manifest": current, "manifest_digest": CONTROL.digest(current),
            "current_registry_digest": CONTROL.digest(current), "project_readback": project,
            "controller_cwd": str(self.root), "observed_threads": [],
        })["cards"][0]
        self.assertEqual(("unreachable", "blocked"), (card["host_status"], card["worker_status"]))
        attached.symlink_to(self.outside, target_is_directory=True)
        escaped = CONTROL.route({
            "controller_cwd": str(self.root), "controller_project_root": str(self.root),
            "project_readback": project, "host_capabilities": CAPS,
            "request": {"intent": "implementation", "explicit_thread_id": "worker-a"},
            "candidates": [self.candidate("worker-a", attached)], "worker_mappings": current["worker_mappings"],
        })
        self.assertEqual("OUT_OF_SCOPE_WORKSPACE", escaped["failure_code"])

    def test_terminal_host_lifecycle_never_projects_as_execution(self):
        for state in (
            self.candidate("worker-a", self.frontend, status="archived"),
            self.candidate("worker-a", self.frontend, status="notLoaded", archived=True),
            self.candidate("worker-a", self.frontend, status="deleted"),
            self.candidate("worker-a", self.frontend, status="unavailable"),
            self.candidate("worker-a", self.frontend, status="delivered"),
        ):
            with self.subTest(state=state.get("status"), archived=state.get("archived")):
                live = CONTROL.status_projection({**self.scope(), "observed_threads": [state]})["cards"][0]
                persistent = CONTROL.status_projection({
                    "manifest": self.manifest(), **self.scope(self.manifest()), "observed_threads": [state],
                })["cards"][0]
                self.assertEqual("等待", live["group"])
                self.assertEqual("blocked", live["worker_status"])
                self.assertEqual("等待", persistent["group"])
                self.assertEqual("blocked", persistent["worker_status"])

    def test_panel_redacts_and_bounds_untrusted_display_text(self):
        current = self.manifest()
        email = "test" + "@" + "example.invalid"
        state = self.candidate("worker-a", self.frontend, title="Deploy ghp_ABCDEFGHIJKL\x1b[31m <script>[click](bad)", recent_goal="password=TOPSECRET contact " + email + " " + "x" * 300)
        card = CONTROL.status_projection({"manifest": current, **self.scope(current), "observed_threads": [state]})["cards"][0]
        rendered = card["title"] + " " + card["recent_goal"]
        for secret in ("ghp_ABCDEFGHIJKL", "TOPSECRET", email, "\x1b"):
            self.assertNotIn(secret, rendered)
        for markdown in ("<script>", "[click]"):
            self.assertNotIn(markdown, rendered)
        self.assertLessEqual(len(card["recent_goal"]), 180)

    def test_status_rejects_unattributed_terminal_envelope(self):
        current = self.manifest()
        forged = {"worker_thread_id": "worker-a", "status": "finished"}
        card = CONTROL.status_projection({"manifest": current, **self.scope(current), "observed_threads": [self.candidate("worker-a", self.frontend)], "worker_envelopes": [forged]})["cards"][0]
        self.assertNotEqual("finished", card["worker_status"])

    def test_status_projection_closed_and_unreachable(self):
        current = self.manifest(closed=True)
        card = CONTROL.status_projection({"manifest": current, **self.scope(current)})["cards"][0]
        self.assertEqual(("已关闭", "unreachable", "closed"), (card["group"], card["host_status"], card["board_status"]))

    def test_detached_root_blocks_notify_close_and_status(self):
        current = self.manifest()
        detached = dict(self.project, allowed_roots_version="readback-2", allowed_root_membership=[{"canonical_root": CONTROL.canonical_path(str(self.root)), "source": "host-project-readback", "version": "readback-2"}])
        common = {"manifest": current, "project_readback": detached, "controller_cwd": str(self.root), "manifest_digest": CONTROL.digest(current), "current_registry_digest": CONTROL.digest(current)}
        notify = CONTROL.notification_plan({**common, "observed_controller": self.candidate("controller-old", self.root, responsibility="controller"), "observed_worker": self.candidate("worker-a", self.frontend)})
        close = CONTROL.close_plan({**common, "thread_id": "worker-a"})
        status = CONTROL.status_projection(common)
        self.assertEqual(["BASIS_DRIFT"] * 3, [notify["failure_code"], close["failure_code"], status["failure_code"]])

    def test_out_of_order_old_envelope_cannot_override_newer(self):
        current = self.manifest()
        base = {"type": "worker-status", "schema_version": "workspace-taskboard-worker-status/v1", "control_id": "ctl-1", "worker_thread_id": "worker-a", "reuse_key": current["worker_mappings"][0]["reuse_key"], "observed_at": "2026-08-13T00:00:00Z", "worker_basis_digest": CONTROL.worker_status_basis(current, current["worker_mappings"][0]), "allowed_roots_version": "readback-1", "canonical_cwd": CONTROL.canonical_path(str(self.frontend))}
        active = {**base, "status": "active", "event_sequence": 3}
        stale = {**base, "status": "finished", "event_sequence": 2}
        card = CONTROL.status_projection({"manifest": current, **self.scope(current), "observed_threads": [self.candidate("worker-a", self.frontend)], "worker_envelopes": [active, stale]})["cards"][0]
        self.assertEqual("active", card["worker_status"])

    def test_invalid_high_sequence_envelope_cannot_shadow_or_recommend(self):
        current = self.manifest()
        base = {"type": "worker-status", "schema_version": "workspace-taskboard-worker-status/v1", "control_id": "ctl-1", "worker_thread_id": "worker-a", "reuse_key": current["worker_mappings"][0]["reuse_key"], "observed_at": "2026-08-13T00:00:00Z", "worker_basis_digest": CONTROL.worker_status_basis(current, current["worker_mappings"][0]), "allowed_roots_version": "readback-1", "canonical_cwd": CONTROL.canonical_path(str(self.frontend))}
        valid = {**base, "status": "active", "event_sequence": 2, "recommended_next_action": "continue tests"}
        forged = {"worker_thread_id": "worker-a", "event_sequence": 999, "status": "finished", "recommended_next_action": "push-and-deploy"}
        card = CONTROL.status_projection({"manifest": current, **self.scope(current), "observed_threads": [self.candidate("worker-a", self.frontend)], "worker_envelopes": [valid, forged]})["cards"][0]
        self.assertEqual(("active", "continue tests"), (card["worker_status"], card["recommended_next_action"]))

    def test_malformed_manifest_fails_closed(self):
        for value in ({"worker_mappings": "bad"}, {**self.manifest(), "allowed_roots": []}, {**self.manifest(), "allowed_roots": ["bad\0path"]}):
            self.assertTrue(CONTROL.validate_manifest(value))


if __name__ == "__main__":
    unittest.main()
