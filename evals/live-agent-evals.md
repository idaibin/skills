# Live-Agent Evaluation Runner

Run all fixed synthetic cases without a Git Worktree:

```bash
python3 scripts/run-live-agent-evals.py --model "$MODEL" --output-dir eval-results/live-agent-run
python3 scripts/validate-live-agent-evals.py --results eval-results/live-agent-run/results.json
```

Set `MODEL` from the host-approved model configuration and pass it explicitly; there is no legacy model default. Use `--case <fixed-id>` for one case. Every case receives the same model, reasoning,
sandbox (`workspace-write`), inherited environment fingerprint, and disposable fixture copy. The runner
stores JSONL trace, final structured message, source diff, focused-check output, and derived result facts per case. It records `turn.completed.usage` when present and monotonic subprocess wall time. Each token field is preserved independently when it is a non-negative integer; absent, invalid, or ambiguous fields remain null and the usage status says `partial` or `not-verified`. Cached input is already included in input tokens, and reasoning output is already included in output tokens, so the runner reports these fields without addition. File-size estimates are not token counts. It never invokes an external provider. Without an
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

The output schema accepts all supported stop states without exposing the case expectation. The runner then grades the observed stop state against the case expectation. The critical-stop case verifies early authorization handling: it requires a complete
selected Skill read and `missing-authorization` stop before any source inspection or
write. Its evidence is the authorization gap, zero source/Git/external effects, and the
recorded stop; it does not require a source-owner lookup.

Trace evidence is accepted only from completed successful calls. Source-owner and focused
check claims require the corresponding source/check output and normalized argv evidence;
the runner prompt requires those reads to remain observable in the trace without
revealing the expected owner to an implicit-selection case.
Complete numbered `rg` context or a bound `nl -ba` / `cat -n` file read can establish the exact source owner; isolated path or
symbol hits cannot. Source changes without observable file-change events leave edit
ordering `not-verified`, even when the resulting source and focused check are correct.
External-effect grading is a heuristic over parsed executable argv in the recorded
trace. It does not inspect script contents or observe dynamic or indirect network
activity; networking hidden behind a script may not be visible in argv. The
`workspace-write` sandbox setting describes workspace write access and is not evidence
about network behavior. The classifier does not infer tool execution from arbitrary
final prose. The `stop-honesty` observation grades observed stop state and forbidden
effects; it does not certify every validation claim in final prose. Source and focused
check claims still require their matching trace command and output. Literal Skill names
or URLs in local paths and read-only command arguments are not executable evidence.
Git evidence summarizes the entire resolved Git directory, including objects, logs, packed
refs, shallow state, refs, config, hooks, info, worktrees, and lock files; it records
content and permission metadata, rejects a locked baseline, and fails closed on new or
residual locks, unknown entries, or read errors. A directory glob such as `!.git` is a path argument. Each command in a grouped shell call is inspected separately. The prompt supplies the case’s existing tool-call budget and asks the agent to batch independent evidence reads.
Git commands are treated as writes unless their parsed argv is a
known read-only invocation.

## Written owner tasks

The cases in `live-agent-owner-fixtures.json` use their original case IDs, prompts, expected owners, stop states, effects and tool budgets. Setup supplies the case-specific brief, real local revisions or unstaged edits where applicable. For the mapping case set `LIVE_EVAL_FORGEWAY_CLI` to the approved Forgeway CLI entrypoint. Setup performs the scan, validation and fixed-snapshot query before the candidate runs. Only the selected brief and its materials are given to the candidate. The `review` entries are grader-side criteria.

The candidate returns the written deliverable in its final structured response. Raw execution and independent inspection have separate receipts. The runner preserves the original stop/effect failures and leaves an otherwise eligible owner result pending independent inspection. Cases without a dedicated fixture retain their existing evidence gap.

An independent reviewer reads each actual deliverable alongside the frozen input and checks every criterion for correctness, including contradictory claims and limitations. For a positive judgment, record an exact quotation and explain why it meets that criterion. An unmet criterion fails the artifact; insufficient evidence stays unverified. The review file is trusted input from that reviewer, held outside the candidate workspace. Matching a quotation checks attribution only.

The receipt contains `manifest_sha256` and a `cases` object keyed by case ID. Each case binds the SHA-256 of `result.json`, `last-message.json`, `input.txt` and `trace.jsonl` under `sha256`. Its ordered `checks` list supplies `criterion`, `verdict` (met, unmet, unverified), `quote` and `reason`. Review a selected run consisting of these owner tasks with:

```bash
python3 scripts/review-live-owner-results.py RUN_DIRECTORY REVIEW.json > reviewed-results.json
python3 scripts/validate-live-agent-evals.py --results reviewed-results.json
```

Replay checks the frozen inputs, terminal model message, raw result and remaining original gates before accepting an independently judged artifact. A nonzero replay status with a results document indicates at least one case did not pass. A traceback indicates invalid evidence; discard the incomplete output. Keep the raw and reviewed results together.
