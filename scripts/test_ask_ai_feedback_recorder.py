import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RECORDER = ROOT / "skills" / "ask-ai" / "scripts" / "record_feedback.py"


class AskAIFeedbackRecorderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.log = self.root / "state" / "feedback.jsonl"
        self.config = self.root / "feedback.yaml"
        self.config.write_text(
            "schema_version: ask-ai-feedback/v1\n"
            "enabled: true\n"
            f"round_log: {self.log}\n",
            encoding="utf-8",
        )
        self.event_file = self.root / "event.json"
        self.event = {
            "schema_version": "ask-ai-feedback/v1",
            "event_id": "round-1:verification-update:1:abcd",
            "event_type": "verification-update",
            "timestamp": "2026-08-12T10:20:23+08:00",
            "feedback_id": "round-1",
            "review_id": "review-1",
            "round_id": "round-1",
            "fixed_basis_hash": "a" * 64,
            "provider": "configured-provider",
            "local_verdict": "pass",
            "task_phase": "review",
            "task_class": "architecture",
            "first_pass_outcome": "rework-required",
            "rework_rounds": 1,
            "unresolved_attempts": 0,
            "final_acceptance": "accepted",
            "user_correction": "none",
        }

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_recorder(self):
        self.event_file.write_text(json.dumps(self.event), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(RECORDER), "--config", str(self.config), "--event-file", str(self.event_file)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_appends_and_reads_back_one_terminal_event(self) -> None:
        result = self.run_recorder()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("feedback-recorded", result.stdout)
        self.assertEqual(self.event, json.loads(self.log.read_text(encoding="utf-8")))
        if os.name != "nt":
            lock_mode = self.log.with_suffix(".jsonl.lock").stat().st_mode & 0o777
            self.assertEqual(0o600, lock_mode)

    def output_snapshot(self):
        return {
            str(path.relative_to(self.root)): (
                path.stat().st_mode & 0o777,
                path.read_bytes() if path.is_file() else None,
            )
            for path in self.root.rglob("*")
            if path not in (self.config, self.event_file)
        }

    def assert_config_rejected_without_writes(self, text):
        self.config_case = getattr(self, "config_case", 0) + 1
        self.event["event_id"] = f"config-rejection:{self.config_case}"
        self.config.write_text(text, encoding="utf-8")
        before = self.output_snapshot()
        result = self.run_recorder()
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("feedback-deferred:", result.stderr)
        self.assertEqual(before, self.output_snapshot())

    def test_config_enablement_cannot_be_overridden_by_nested_or_duplicate_keys(self):
        base = f"schema_version: ask-ai-feedback/v1\nround_log: {self.log}\n"
        for tail in (
            "enabled: false\nsummary:\n  enabled: true\n",
            "enabled: false\nenabled: true\n",
            "enabled: true\nenabled: false\n",
            'enabled: "true"\n', "enabled: 'true'\n", "", "enabled: yes\n",
            f"enabled: true\nround_log: {self.root / 'other.jsonl'}\n",
            "enabled: true\nschema_version: ask-ai-feedback/v1\n",
        ):
            with self.subTest(tail=tail):
                self.assert_config_rejected_without_writes(base + tail)

    def test_unsupported_or_malformed_config_is_rejected_before_any_output(self):
        base = f"schema_version: ask-ai-feedback/v1\nenabled: true\nround_log: {self.log}\n"
        for tail in (
            "summary:\n  enabled: true\n", "  extra: value\n", "not a mapping\n",
            "extra: [a, b]\n", "extra: {a: b}\n", "extra: |\n", "extra: >\n",
            "extra: &anchor value\n", "extra: *anchor\n", "extra: !tag value\n",
            "extra: null\n", "extra: ~\n", "extra:\n", "extra: a: b\n",
            "extra: 'unterminated\n", 'extra: "unterminated\n',
            "extra: 'value' trailing\n", 'extra: "value" trailing\n',
        ):
            with self.subTest(tail=tail):
                self.assert_config_rejected_without_writes(base + tail)

    def test_invalid_decoded_log_paths_preserve_missing_and_existing_outputs(self):
        base = "schema_version: ask-ai-feedback/v1\nenabled: true\nround_log: "
        for existing in (False, True):
            if existing:
                self.assertEqual(0, self.run_recorder().returncode)
                lock = self.log.with_suffix(".jsonl.lock")
                lock.write_bytes(b"existing-lock")
                lock.chmod(0o640)
            for suffix in ("\x00", "\ud800", "\udfff", "\udc80"):
                with self.subTest(existing=existing, suffix=repr(suffix)):
                    self.assert_config_rejected_without_writes(
                        base + json.dumps(str(self.root / "new-parent" / "feedback.jsonl") + suffix) + "\n"
                    )
            self.config.write_text(base + str(self.log) + "\n", encoding="utf-8")

    def test_flat_config_paths_and_unknown_scalar_settings_remain_compatible(self):
        for index, (name, quote) in enumerate((
            ("state#plain", "plain"), ("state #single", "single"),
            ("state #double", "double"), ("state with spaces", "plain"),
            ("状态#保留", "double"), ("state'quote", "single"),
        )):
            with self.subTest(name=name, quote=quote):
                log = self.root / name / "feedback.jsonl"
                value = str(log)
                if quote == "single":
                    value = "'" + value.replace("'", "''") + "'"
                elif quote == "double":
                    value = json.dumps(value, ensure_ascii=False)
                self.config.write_text(
                    "# user configuration\nschema_version: ask-ai-feedback/v1\n"
                    f"enabled: true # local opt-in\nround_log: {value} # path\n"
                    "retention: 30\nthreshold: 0.75\nlabel: user setting\nextra: ''\n",
                    encoding="utf-8",
                )
                self.event["event_id"] = f"config-path:{index}"
                result = self.run_recorder()
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertTrue(log.exists(), result.stdout)
                self.assertEqual(self.event, json.loads(log.read_text(encoding="utf-8")))
                self.assertTrue(log.with_suffix(".jsonl.lock").exists())

    def test_config_scalar_preserves_relative_and_windows_path_text(self):
        load_config = runpy.run_path(str(RECORDER))["load_config"]
        for value in ("状态#保留/feedback.jsonl", r"C:\fixture\state#keep\feedback.jsonl"):
            for encoded in (value, "'" + value + "'", json.dumps(value)):
                with self.subTest(value=value, encoded=encoded):
                    self.config.write_text(
                        "schema_version: ask-ai-feedback/v1\nenabled: true\n"
                        f"round_log: {encoded}\n", encoding="utf-8",
                    )
                    self.assertEqual(value, load_config(self.config)["round_log"])
        self.assertFalse(self.log.parent.exists())


    def test_rejects_all_feedback_events_failed_before_submit(self) -> None:
        self.event = {key: self.event[key] for key in (
            "schema_version", "event_id", "event_type", "timestamp", "feedback_id",
            "review_id", "round_id", "fixed_basis_hash", "provider",
        )}
        self.event["completion_state"] = "failed-before-submit"
        for event_type in ("review-attempt", "response-captured", "verification-update"):
            with self.subTest(event_type=event_type):
                self.event["event_type"] = event_type
                result = self.run_recorder()
                self.assertEqual(1, result.returncode)
                self.assertIn("failed-before-submit", result.stderr)
                self.assertFalse(self.log.exists())

    def test_preserves_submitted_and_ambiguous_review_attempts(self) -> None:
        self.event = {key: self.event[key] for key in (
            "schema_version", "event_id", "event_type", "timestamp", "feedback_id",
            "review_id", "round_id", "fixed_basis_hash", "provider",
        )}
        self.event["event_type"] = "review-attempt"
        for state in ("submitted", "ambiguous"):
            with self.subTest(state=state):
                self.event["event_id"] = "round-1:review-attempt:" + state
                self.event["completion_state"] = state
                result = self.run_recorder()
                self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(2, len(self.log.read_text(encoding="utf-8").splitlines()))

    def test_rejected_pre_submit_event_preserves_existing_log(self) -> None:
        self.assertEqual(0, self.run_recorder().returncode)
        original = self.log.read_bytes()
        self.event = {key: self.event[key] for key in (
            "schema_version", "event_id", "event_type", "timestamp", "feedback_id",
            "review_id", "round_id", "fixed_basis_hash", "provider",
        )}
        self.event["completion_state"] = "failed-before-submit"
        for event_type in ("review-attempt", "response-captured", "verification-update"):
            with self.subTest(event_type=event_type):
                self.event["event_type"] = event_type
                self.event["event_id"] = "rejected:" + event_type
                result = self.run_recorder()
                self.assertEqual(1, result.returncode)
                self.assertIn("failed-before-submit", result.stderr)
                self.assertEqual(original, self.log.read_bytes())

    def test_rejects_duplicate_event_id(self) -> None:
        self.assertEqual(0, self.run_recorder().returncode)
        result = self.run_recorder()
        self.assertEqual(1, result.returncode)
        self.assertIn("duplicate event_id", result.stderr)
        self.assertEqual(1, len(self.log.read_text(encoding="utf-8").splitlines()))

    def test_rejects_raw_content_and_paths(self) -> None:
        self.event["raw_content"] = "secret"
        self.assertEqual(1, self.run_recorder().returncode)
        self.event.pop("raw_content")
        self.event["summary"] = "/" + "Users/example/private"
        self.assertEqual(1, self.run_recorder().returncode)
        self.assertFalse(self.log.exists())

    def test_rejects_pii_relative_paths_domains_and_token_like_values(self) -> None:
        for field, value in (
            ("local_verdict", "alice" + "@" + "example.invalid"),
            ("response_artifact_id", ".codex/reviews/raw-response.md"),
            ("response_artifact_id", "C:\\Users\\example\\response.md"),
            ("completion_evidence", "review.example.com"),
            ("model_evidence", "a" * 40),
        ):
            with self.subTest(field=field, value=value):
                event = dict(self.event)
                event[field] = value
                self.event = event
                self.assertEqual(1, self.run_recorder().returncode)
                self.event = dict(self.event)
                self.event.pop(field, None)
        self.assertFalse(self.log.exists())

    def test_requires_hash_fields_to_be_lowercase_sha256(self) -> None:
        for field in ("conversation_fingerprint", "prompt_artifact_hash", "response_artifact_hash"):
            with self.subTest(field=field):
                self.event[field] = "not-a-fingerprint"
                self.assertEqual(1, self.run_recorder().returncode)
                self.event.pop(field)
        self.assertFalse(self.log.exists())

    def test_rejects_retired_free_text_fields_for_new_events(self) -> None:
        for field in ("summary", "prompt_hypothesis", "next_experiment"):
            with self.subTest(field=field):
                self.event[field] = "sanitized text"
                result = self.run_recorder()
                self.assertEqual(1, result.returncode)
                self.assertIn("unknown fields", result.stderr)
                self.event.pop(field)
        self.assertFalse(self.log.exists())

    def test_rejects_null_nested_and_invalid_scalar_types(self) -> None:
        for value in (None, {"nested": "value"}, 7):
            with self.subTest(value=value):
                self.event["summary"] = value
                self.assertEqual(1, self.run_recorder().returncode)
        self.assertFalse(self.log.exists())

    def test_accepts_task_classification_before_local_reconciliation(self) -> None:
        self.event["event_type"] = "response-captured"
        for field in (
            "first_pass_outcome",
            "rework_rounds",
            "unresolved_attempts",
            "final_acceptance",
            "user_correction",
        ):
            self.event.pop(field)
        result = self.run_recorder()
        self.assertEqual(0, result.returncode, result.stderr)

    def test_accepts_legacy_v1_events_without_task_effect_fields(self) -> None:
        task_effect_fields = (
            "task_phase",
            "task_class",
            "first_pass_outcome",
            "rework_rounds",
            "unresolved_attempts",
            "final_acceptance",
            "user_correction",
        )
        for event_type in ("review-attempt", "response-captured", "verification-update"):
            with self.subTest(event_type=event_type):
                self.event["event_id"] = f"legacy:{event_type}:1:abcd"
                self.event["event_type"] = event_type
                for field in task_effect_fields:
                    self.event.pop(field, None)
                result = self.run_recorder()
                self.assertEqual(0, result.returncode, result.stderr)

    def test_rejects_result_fields_before_verification_update(self) -> None:
        self.event["event_type"] = "response-captured"
        result = self.run_recorder()
        self.assertEqual(1, result.returncode)
        self.assertIn("verification-only fields", result.stderr)
        self.assertFalse(self.log.exists())

    def test_rejects_unknown_controlled_values(self) -> None:
        for field, value in (
            ("task_phase", "planning"),
            ("task_class", "security"),
            ("first_pass_outcome", "mostly-good"),
            ("final_acceptance", "pass"),
            ("user_correction", "minor"),
        ):
            with self.subTest(field=field):
                self.event[field] = value
                result = self.run_recorder()
                self.assertEqual(1, result.returncode)
                self.assertIn("unsupported controlled value", result.stderr)
                self.event = dict(self.event)
                self.event.update(
                    task_phase="review",
                    task_class="architecture",
                    first_pass_outcome="rework-required",
                    final_acceptance="accepted",
                    user_correction="none",
                )
        self.assertFalse(self.log.exists())

    def test_rejects_invalid_rework_counts(self) -> None:
        for field in ("rework_rounds", "unresolved_attempts"):
            for value in (-1, 1.5, True, "1"):
                with self.subTest(field=field, value=value):
                    self.event[field] = value
                    result = self.run_recorder()
                    self.assertEqual(1, result.returncode)
                    self.assertIn("non-negative integer", result.stderr)
            self.event[field] = 0
        self.assertFalse(self.log.exists())

    def test_serializes_concurrent_appenders(self) -> None:
        processes = []
        for index in range(8):
            event = dict(self.event)
            event["event_id"] = f"round-{index}:verification-update:1:abcd"
            event["feedback_id"] = f"round-{index}"
            event_file = self.root / f"event-{index}.json"
            event_file.write_text(json.dumps(event), encoding="utf-8")
            processes.append(
                subprocess.Popen(
                    [
                        sys.executable,
                        str(RECORDER),
                        "--config",
                        str(self.config),
                        "--event-file",
                        str(event_file),
                    ],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            )
        results = [
            process.communicate(timeout=10) + (process.returncode,)
            for process in processes
        ]
        self.assertTrue(all(returncode == 0 for _, _, returncode in results), results)
        events = [
            json.loads(line)
            for line in self.log.read_text(encoding="utf-8").splitlines()
        ]
        self.assertEqual(8, len(events))
        self.assertEqual(8, len({event["event_id"] for event in events}))


if __name__ == "__main__":
    unittest.main()
