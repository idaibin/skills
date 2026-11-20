import importlib.util
from pathlib import Path
import subprocess
import unittest


spec = importlib.util.spec_from_file_location("replay_ui", Path(__file__).with_name("replay-ui-regression.py"))
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


def result(control, diagnostic="", *, code=None):
    failed = int(control)
    tap = f"""TAP version 13
{'not ok' if control else 'ok'} 1 - chosen case
{diagnostic}
1..1
# tests 1
# pass {1 - failed}
# fail {failed}
# cancelled 0
# skipped 0
# todo 0
"""
    return subprocess.CompletedProcess([], failed if code is None else code, stdout=tap)


class RegressionReplay(unittest.TestCase):
    def verify(self, output, control=True):
        return replay.verify(output, "chosen case", "accepted width", control)

    def test_requires_matching_failure_and_clean_candidate(self):
        for error in ["  error: 'accepted width'", "  error: |-\n    accepted width\n    60 !== 196"]:
            with self.subTest(error=error):
                self.assertTrue(self.verify(result(True, error + "\n  code: 'ERR_ASSERTION'")))
        self.assertTrue(self.verify(result(False), False))
        self.assertFalse(self.verify(result(False)))
        self.assertFalse(self.verify(result(True), False))

    def test_cannot_pass_with_setup_failure_or_unrelated_assertion(self):
        self.assertFalse(self.verify(result(True, "  error: accepted width\n  code: 'ERR_MODULE_NOT_FOUND'")))
        self.assertFalse(self.verify(result(True, "  error: unrelated failure\n  code: 'ERR_ASSERTION'\n# accepted width")))
        self.assertFalse(self.verify(result(False, code=1), False))

    def test_rejects_different_skipped_or_missing_test(self):
        good = result(False)
        for old, new in [("chosen case", "other case"), ("# skipped 0", "# skipped 1"),
                         ("# tests 1", "# tests 0"), ("# todo 0", "# todo 1")]:
            with self.subTest(new=new):
                self.assertFalse(self.verify(subprocess.CompletedProcess([], 0, stdout=good.stdout.replace(old, new)), False))


if __name__ == "__main__":
    unittest.main()
