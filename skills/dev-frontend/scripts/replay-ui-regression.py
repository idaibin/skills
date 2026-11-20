#!/usr/bin/env python3
"""Replay one named, top-level Node TAP assertion against two explicit source roots."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys


def verify(result, name, assertion, control):
    output = result.stdout
    expected = "not ok" if control else "ok"
    counts = {"tests": 1, "pass": int(not control), "fail": int(control),
              "cancelled": 0, "skipped": 0, "todo": 0}
    for key, count in counts.items():
        if not re.search(rf"^# {key} {count}$", output, re.MULTILINE):
            return False
    if result.returncode != int(control) or f"{expected} 1 - {name}" not in output.splitlines():
        return False
    if not control:
        return True
    # Use the assertion diagnostic, not a subtest title, stack line or console output.
    error = re.search(r"^  error: (.+)$", output, re.MULTILINE)
    if not error or not re.search(r"""^  code: ['"]?ERR_ASSERTION['"]?$""", output, re.MULTILINE):
        return False
    message = error[1].strip("'\x22")
    if message in {"|", "|-", "|+"}:
        block = output[error.end():].splitlines()
        message = block[1].strip() if len(block) > 1 else ""
    return assertion in message


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-env", required=True, help="project-native source root environment variable")
    parser.add_argument("--control-root", required=True, type=Path)
    parser.add_argument("--candidate-root", required=True, type=Path)
    parser.add_argument("--name", required=True, help="exact top-level test name")
    parser.add_argument("--assertion", required=True, help="distinctive assertion error message fragment")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="-- node --test --test-reporter=tap ...")
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    roots = [args.control_root.resolve(), args.candidate_root.resolve()]
    if not command or not args.assertion.strip() or not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", args.root_env):
        parser.error("provide a test command, root variable and nonempty assertion fragment")
    if roots[0] == roots[1] or not all(root.is_dir() for root in roots):
        parser.error("provide distinct existing control and candidate source directories")
    for root, control in zip(roots, (True, False)):
        result = subprocess.run(command, env={**os.environ, args.root_env: str(root)},
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if not verify(result, args.name, args.assertion, control):
            sys.stderr.write(result.stdout)
            print(f"Unexpected TAP outcome at {root}", file=sys.stderr)
            return 1
        print(f"{'Expected assertion failed' if control else 'Candidate passed'}: {args.name} ({root})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
