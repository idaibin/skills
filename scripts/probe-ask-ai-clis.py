#!/usr/bin/env python3
"""Discover coding-agent CLI paths without launching unqualified programs.

Version/help execution requires --verified-cli PROVIDER EXECUTABLE SHA256 from an
existing headless qualification. Computing a new hash alone is not qualification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import plistlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from xml.parsers.expat import ExpatError


PROVIDERS = (
    ("google-antigravity", ("agy",), ("antigravity", "agy")),
    ("claude-code", ("claude",), ("claude code",)),
    ("qoder-cli-global", ("qodercli",), ("qoder",)),
    ("qoder-cli-cn", ("qoderclicn", "qodercn", "qoder-cn", "qoder"), ("qoder",)),
    ("zcode", ("zcode",), ("zcode",)),
    ("codebuddy-code", ("codebuddy", "codebuddy-code", "cbc"), ("codebuddy",)),
    ("cursor-cli", ("agent",), ("cursor",)),
    ("github-copilot-cli", ("copilot",), ("github copilot cli",)),
    ("kiro-cli", ("kiro-cli", "kiro"), ("kiro",)),
    ("factory-droid", ("droid",), ("droid", "factory")),
    ("opencode", ("opencode",), ("opencode",)),
)

QODER_CN_PATHS = {"qoderclicn", "qodercn", "qoder-cn"}
QODER_CN_MARKERS = ("qoderclicn", "qodercn", "qoder-cn", "qoder cn", "china", "中国", "中文版")
QODER_GLOBAL_MARKERS = ("qoder", "qodercli")


def _command_succeeded(result: dict[str, Any]) -> bool:
    return result["status"] in {"pass", "pass-with-stderr"}


def _matches_entrypoint(path_name: str, entrypoint: str) -> bool:
    """Accept an exact entrypoint or its version-suffixed resolved binary."""
    return path_name == entrypoint or path_name.startswith(f"{entrypoint}-")


def qoder_identity(
    provider: str,
    executable: str,
    version: dict[str, Any],
    help_result: dict[str, Any],
) -> tuple[str, dict[str, bool]]:
    """Require provider-specific command and path evidence without cross-variant fallback."""
    path_name = Path(executable).name.lower()
    version_text = version["output"].lower()
    help_text = help_result["output"].lower()
    identity_text = f"{version_text}\n{help_text}"
    version_ok = _command_succeeded(version)
    help_ok = _command_succeeded(help_result)
    name_ok = any(marker in identity_text for marker in QODER_GLOBAL_MARKERS)
    cn_identity_marker = any(marker in identity_text for marker in QODER_CN_MARKERS)
    if provider == "qoder-cli-global":
        path_ok = _matches_entrypoint(path_name, "qodercli")
        variant_ok = name_ok and not cn_identity_marker
    else:
        resolved_cn_path = any(_matches_entrypoint(path_name, name) for name in QODER_CN_PATHS)
        # A bare ``qoder`` is only a discovery candidate, never CN identity proof.
        path_ok = resolved_cn_path
        variant_ok = cn_identity_marker
    evidence = {
        "version": version_ok,
        "help": help_ok,
        "path": path_ok,
        "name": name_ok,
        "variant": variant_ok,
    }
    return ("matched" if all(evidence.values()) else "not-verified", evidence)


def run(command: list[str], *, cwd: Path, env: dict[str, str], timeout: int) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        combined = f"{result.stdout}\n{result.stderr}".strip()
        status = "fail"
        if result.returncode == 0:
            status = "pass-with-stderr" if result.stderr.strip() else "pass"
        return {
            "status": status,
            "exit_code": result.returncode,
            "first_line": next((line.strip() for line in combined.splitlines() if line.strip()), ""),
            "stderr_first_line": next(
                (line.strip() for line in result.stderr.splitlines() if line.strip()), ""
            ),
            "output_sha256": hashlib.sha256(combined.encode()).hexdigest(),
            "output": combined,
        }
    except subprocess.TimeoutExpired as error:
        combined = "\n".join(
            part.decode(errors="replace") if isinstance(part, bytes) else part or ""
            for part in (error.stdout, error.stderr)
        ).strip()
        return {
            "status": "timeout",
            "exit_code": None,
            "first_line": next((line.strip() for line in combined.splitlines() if line.strip()), ""),
            "output_sha256": hashlib.sha256(combined.encode()).hexdigest(),
            "output": combined,
        }


def git_fingerprint(root: Path) -> str:
    tracked = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--"],
        cwd=root,
        capture_output=True,
        check=True,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=root,
        capture_output=True,
        check=True,
    )
    digest = hashlib.sha256(tracked.stdout)
    for raw_path in sorted(path for path in untracked.stdout.split(b"\0") if path):
        path = root / os.fsdecode(raw_path)
        digest.update(b"\0path\0" + raw_path)
        if path.is_symlink():
            digest.update(b"\0symlink\0" + os.fsencode(os.readlink(path)))
        else:
            digest.update(b"\0file\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def validate_output_path(root: Path, output: Path | None) -> None:
    if output is None:
        return
    root = root.resolve()
    resolved = output.resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return
    ignored = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", str(relative)],
        cwd=root,
        check=False,
    )
    if ignored.returncode != 0:
        raise SystemExit("--output inside the repository must resolve to a Git-ignored path")


def resolve_executable(candidates: tuple[str, ...], search_dirs: list[Path]) -> str | None:
    for directory in search_dirs:
        for candidate in candidates:
            path = directory / candidate
            if path.is_file() and os.access(path, os.X_OK):
                return str(path.resolve())
    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return str(Path(path).resolve())
    return None


def public_result(result: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in result.items() if key != "output"}


def bundle_entrypoint_blocker(executable: Path) -> str | None:
    """Preserve bundle identity even when its main executable is a symlink."""
    for bundle in executable.parents:
        if bundle.suffix.lower() != ".app":
            continue
        contents = bundle / "Contents"
        try:
            with (contents / "Info.plist").open("rb") as handle:
                metadata = plistlib.load(handle)
            if not isinstance(metadata, dict):
                return "bundle-entrypoint-unverified"
            name = metadata.get("CFBundleExecutable")
            if not isinstance(name, str) or not name:
                return "bundle-entrypoint-unverified"
            main = contents / "MacOS" / name
            if main.resolve() == executable.resolve() or (
                main.exists() and executable.exists() and main.samefile(executable)
            ):
                return "desktop-entrypoint"
        except (OSError, ValueError, RuntimeError, plistlib.InvalidFileException, ExpatError):
            return "bundle-entrypoint-unverified"
        break
    return None


def resolve_qualified_executable(
    executable: Path, expected_digest: str,
) -> tuple[Path | None, str | None]:
    """Check bundle context along every symlink hop, then bind the final bytes."""
    blocker = bundle_entrypoint_blocker(executable)
    if blocker:
        return None, blocker
    pending = list(executable.parts[1:])
    resolved = Path(executable.anchor)
    links = 0
    try:
        while pending:
            name = pending.pop(0)
            if name == "..":
                resolved = resolved.parent
                continue
            candidate = resolved / name
            if candidate.is_symlink():
                links += 1
                if links > 40:
                    return None, "entrypoint-resolution-failed"
                target = Path(os.readlink(candidate))
                reference = target if target.is_absolute() else candidate.parent / target
                blocker = bundle_entrypoint_blocker(reference.joinpath(*pending))
                if blocker:
                    return None, blocker
                if target.is_absolute():
                    resolved = Path(target.anchor)
                    pending = list(target.parts[1:]) + pending
                else:
                    pending = list(target.parts) + pending
            else:
                resolved = candidate
    except (OSError, RuntimeError):
        return None, "entrypoint-resolution-failed"
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        return None, "executable-unavailable"
    try:
        digest = hashlib.sha256()
        with resolved.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        if digest.hexdigest() != expected_digest:
            return None, "executable-digest-mismatch"
    except OSError:
        return None, "executable-unreadable"
    return resolved, None


def unrun_probe(reason: str) -> dict[str, Any]:
    return {"status": "not-run", "reason": reason, "output": ""}


def qualified_probe(
    executable: str, option: str, expected_digest: str, *, cwd: Path,
    env: dict[str, str], timeout: int, expected_executable: str | None = None,
) -> dict[str, Any]:
    resolved, blocker = resolve_qualified_executable(Path(executable), expected_digest)
    if blocker:
        return unrun_probe(blocker)
    assert resolved is not None
    if expected_executable is not None and str(resolved) != expected_executable:
        return unrun_probe("entrypoint-drift")
    result = run([str(resolved), option], cwd=cwd, env=env, timeout=timeout)
    return {**result, "executable": str(resolved)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover coding-agent CLI paths; execute version/help only for qualified entries."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Git repository to keep unchanged")
    parser.add_argument(
        "--bin-dir",
        action="append",
        type=Path,
        default=[],
        help="Additional executable directory; repeat when needed",
    )
    parser.add_argument("--timeout", type=int, default=15, help="Seconds per command")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    parser.add_argument(
        "--verified-cli", nargs=3, action="append", default=[],
        metavar=("PROVIDER", "EXECUTABLE", "SHA256"),
        help="Execute version/help for this exact absolute headless entry using its existing "
             "qualification fingerprint; a newly calculated hash does not prove background safety. "
             "Repeat for selected providers. Other entries return present/not-run.",
    )
    args = parser.parse_args()
    providers = {provider for provider, _, _ in PROVIDERS}
    qualified = {}
    for provider, executable, digest in args.verified_cli:
        if provider not in providers or provider in qualified:
            parser.error("--verified-cli requires a known provider exactly once")
        if not Path(executable).is_absolute():
            parser.error("--verified-cli executable must be an absolute path")
        if len(digest) != 64 or any(c not in "0123456789abcdefABCDEF" for c in digest):
            parser.error("--verified-cli SHA256 must contain 64 hexadecimal characters")
        qualified[provider] = (executable, digest.lower())
    args.verified_cli = qualified
    return args


def main() -> int:
    args = parse_args()
    root = args.repo.resolve()
    validate_output_path(root, args.output)
    before = git_fingerprint(root)

    with tempfile.TemporaryDirectory(prefix="ask-ai-cli-probe-") as state_dir:
        state = Path(state_dir)
        env = os.environ.copy()
        env.update(
            {
                "XDG_CACHE_HOME": str(state / "cache"),
                "XDG_CONFIG_HOME": str(state / "config"),
                "XDG_DATA_HOME": str(state / "data"),
                "XDG_STATE_HOME": str(state / "state"),
                "QODER_CONFIG_DIR": str(state / "qoder"),
            }
        )
        probes = []
        for provider, candidates, identity_terms in PROVIDERS:
            qualified = args.verified_cli.get(provider)
            executable = (
                qualified[0]
                if qualified else resolve_executable(candidates, args.bin_dir)
            )
            if not executable:
                probes.append(
                    {
                        "provider": provider,
                        "discovery": "missing",
                        "runtime_conformance": "not-run",
                    }
                )
                continue

            if qualified:
                version = qualified_probe(executable, "--version", qualified[1],
                                          cwd=root, env=env, timeout=args.timeout)
                help_result = (
                    unrun_probe(version["reason"]) if version["status"] == "not-run" else
                    qualified_probe(executable, "--help", qualified[1], cwd=root, env=env,
                                    timeout=args.timeout, expected_executable=version["executable"])
                )
            else:
                version = unrun_probe("qualification-required")
                help_result = unrun_probe("qualification-required")
            execution_path = version.get("executable", executable)
            if provider.startswith("qoder-cli-"):
                identity, identity_evidence = qoder_identity(provider, execution_path, version, help_result)
            else:
                identity_text = f"{version['output']}\n{help_result['output']}".lower()
                command_succeeded = (
                    all(result["status"] != "not-run" for result in (version, help_result))
                    and any(_command_succeeded(result) for result in (version, help_result))
                )
                identity = (
                    "matched"
                    if command_succeeded and any(term in identity_text for term in identity_terms)
                    else "not-verified"
                )
                identity_evidence = None
            probes.append(
                {
                    "provider": provider,
                    "discovery": "present" if Path(executable).is_file() else "missing",
                    "executable": execution_path,
                    "identity": identity,
                    **({"identity_evidence": identity_evidence} if identity_evidence is not None else {}),
                    "version": public_result(version),
                    "help": public_result(help_result),
                    "runtime_conformance": "not-run",
                }
            )

    after = git_fingerprint(root)
    report = {
        "schema_version": "ask-ai-cli-discovery/v1",
        "scope": "discovery-only",
        "repository": str(root),
        "basis_sha": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True
        ).stdout.strip(),
        "worktree_unchanged": before == after,
        "providers": probes,
        "limitations": [
            "No provider prompt was submitted.",
            "Unqualified entries were not launched; version/help may report not-run with a reason.",
            "Caller-supplied fingerprints bind existing headless qualification, not a new safety test "
            "or a sandbox for executable dependencies and side effects.",
            "Authentication, permissions, structured output, sessions, resume, and billing were not tested.",
            "Presence and help output do not establish runtime conformance.",
        ],
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if report["worktree_unchanged"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
