# Bundled app-server qualification example

Load only for a client exposing a bundled session app-server. This example was
qualified against ZCode 3.15.3's bundled zcode.cjs; it is not the universal protocol.
Resolve the installed resource root and current schema before reusing it. Keep local
account paths, session IDs, receipts and live status in caller-owned evidence.

## Entry and framing

The qualified entry was Node running the bundle with
`app-server --stdio --surface desktop`. The desktop surface argument does not
register a task in the desktop list. Keep stdout for NDJSON and stderr separate.
Each request has `id`, `method`, `params`; this schema rejects an extra
`jsonrpc` field. Correlate error responses as well as successful responses.

The packaged resource layout required process-local
`ZCODE_BUILTIN_PROVIDER_CONFIG_FILE` pointing to the bundle's
`config/provider/zcode-builtin.json`, and
`ZCODE_PERSONAL_PROVIDER_CONFIG_FILE` pointing to the existing account's
`.zcode/v2/provider_config.json`. Verify those paths through the installed parser
and resource inventory. Pass paths only; let the app read credentials normally.

## Qualified method mapping

| Intent | Method and fields |
| --- | --- |
| Capability read | `runtime/capabilities`, empty params |
| New session | `session/create`, workspace and scoped runtime options; identity is in `result.session.sessionId` |
| Resume | `session/resume`, sessionId and workspace {workspacePath, workspaceKey} |
| Query | `session/read`, sessionId; inspect session, projection, runtime and messages |
| Select model when authorized | `session/setModel`, sessionId and model {providerId, modelId, options} |
| Submit | `session/send`, sessionId and content; accepted is not completion |

Create/resume accepts `mcpServers`, `toolAllowlist`,
`offPeakToolEnabled`, `dynamicWorkflowMode` in this build. Empty/default
allowlist semantics must not be assumed to disable tools: the no-tool probe used a
non-empty deliberately unmatched name. Restrict tools explicitly for each task.
Read-only qualification uses only the observed built-in `Read` tool; it has no
path sandbox merely because it is allowlisted. Do not carry a test's tool filter
into a real task without resolving that task's effects and isolation.

Model selection is session-specific. One tested provider required an explicit
`options.reasoningLevel`; use currently advertised model settings instead of a
fixed provider/model default. A requested plan mode returning build mode does not
establish read-only isolation.

Read matching user/assistant messages, status and tool parts; reconcile
`v4/telemetry/event` with kind `turn.terminal` and its actual status when emitted.
Preserve failures, including accepted sends that terminate with configuration errors.
Return unsupported client requests as errors during qualification rather than granting
permissions. End owned stdio transport; do not call `session/close` on an existing
user session because this build disposes its event store.

## Known qualification boundaries

No-tool submission/result readback and a read-only tool task are separate checks.
Record current results rather than treating this example as a live success receipt.
New protocol sessions were not proven to populate the desktop task list. Desktop
synchronization, long tasks, approvals and recovery require their own qualification.

For GUI diagnostics in this build, AXReplaceRangeWithText takes AXReplacementRange
(AXValue/CFRange) and AXReplacementText (string). The observed AppKit implementation
uses the already focused accessibility element and current input context; an unfocused
editor returned API success but false result and unchanged text. Do not set focus or
repeat that failed state. A transformed Stage Manager thumbnail does not qualify as
full-window capture; continue independent protocol work without raising the window.
