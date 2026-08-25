# Live-Agent Evaluation Runner

Run all fixed synthetic cases without a Git Worktree:

```bash
python3 scripts/run-live-agent-evals.py --output-dir eval-results/live-agent-run
python3 scripts/validate-live-agent-evals.py --results eval-results/live-agent-run/results.json
```

Use `--case <fixed-id>` for one case. Every case receives the same model, reasoning,
sandbox (`workspace-write`), inherited environment fingerprint, and disposable fixture copy. The runner
stores JSONL trace, final structured message, source diff, focused-check output, and
derived result facts per case. It never invokes an external provider. Without an
explicit attributed AGY Flash result passed by `--provider-evidence`, the provider case
is `not-verified`.

`--provider-evidence` is a path-only handoff, not a self-authenticating receipt. Supply
the independently frozen selected root with `--provider-repository-root`; evidence
without that separate root is rejected. The
runner and standalone validator replay the same fail-closed check over provider-owned
JSONL: the AGY-shaped `init` event must provide `conversation_id` and
`init.{model,cwd,tools}`, while its terminal `result` independently repeats that
conversation and a successful status. The evidence handoff must declare `channel: AGY`,
and both unique, ordered `init` then `result` records must identify canonical provider
`google-antigravity`. The result binds its operation ID, prompt-or-basis digest, frozen
case/diff basis, and non-empty final artifact SHA-256 plus byte count. `init.model` is
the exact effective-model evidence. The executor receipt separately binds zero process exit, a SHA-256
executable fingerprint, version, profile, native mode, `init.model` locator, frozen
basis, and artifact/events hashes; its operation, digest, artifact bytes/hash,
conversation, model, terminal, and cwd/profile scope must agree with the provider
events. Its immutable invocation record must bind process `cwd` and exactly one
`--add-dir` to that selected root, include the verified non-interactive permission
option, and expose no additional directory. Prose logs, missing, reordered, duplicate, or conflicting events; identity,
model/session/terminal or init-cwd mismatches; absent result basis; empty/replaced
artifacts; or receipt runtime/basis mismatches remain `not-verified`.

The critical-stop case verifies early authorization handling: it requires a complete
selected Skill read and `missing-authorization` stop before any source inspection or
write. Its evidence is the authorization gap, zero source/Git/external effects, and the
recorded stop; it does not require a source-owner lookup.

Trace evidence is accepted only from completed successful calls. Source-owner and focused
check claims require the corresponding source/check output and normalized argv evidence.
Git evidence summarizes the entire resolved Git directory, including objects, logs, packed
refs, shallow state, refs, config, hooks, info, worktrees, and lock files; it records
content and permission metadata, rejects a locked baseline, and fails closed on new or
residual locks, unknown entries, or read errors. Git commands are treated as writes unless their parsed argv is a
known read-only invocation.
