import json
import os
from pathlib import Path
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
        for event_type in ("response-captured", "verification-update"):
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
