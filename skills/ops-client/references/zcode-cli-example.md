# Bundled ZCode CLI qualification example

Use for an authorized installed ZCode CLI operation. Bind the existing user session
when requested; this transport does not select a reviewer/provider or authorize new
business work. CLI state and desktop presentation remain separate evidence layers.

## Contents

- [Identity and account binding](#identity-and-account-binding)
- [Resume and submit once](#resume-and-submit-once)
- [Readback and attribution](#readback-and-attribution)
- [Permission, privacy and route limits](#permission-privacy-and-route-limits)

## Identity and account binding

Resolve the executable inside the current app, version, help, exact workspace/key,
session ID and account/configuration source. Reuse matching caller-owned qualification
records; check drift before repeating probes. Help and doctor validate packaging and
arguments, not model access, tool effects or completed turns.

The qualified macOS CLI 0.16.9 supports process-local configuration:

| Variable | Meaning to verify in the installed runtime |
| --- | --- |
| ZCODE_DATA_BASE_DIR | Parent of the original account's .zcode directory; not that directory itself |
| ZCODE_BUILTIN_PROVIDER_CONFIG_FILE | Existing bundle config/provider/zcode-builtin.json |
| ZCODE_PERSONAL_PROVIDER_CONFIG_FILE | Original account's existing .zcode/v2/provider_config.json |

A desktop launched from another working directory may use an account root different
from the shell default. Locate the actual desktop task index/configuration through
verified process open files, installed path resolution and exact task metadata. A
missing catalog or provider under the shell default is only a scoped lookup failure.
Use paths to the original stores and let the CLI load credentials natively; do not
print/copy tokens, change global config, switch accounts/models or create a replacement
session to repair binding. Preserve exact provider/model IDs and reasoning variant;
case-normalized model labels and the UI picker alone do not establish identity.

Account configuration, desktop task index and CLI transcript database can resolve to
different roots. Discover each independently; an account-root override does not prove
that the session database moved. Keep personal paths, SIDs and live receipts outside
the published Skill.

## Resume and submit once

Before sending, read the exact SID's workspace, latest input, model and terminal state,
pending approvals and concurrent activity. Resume only the intended idle session. If
work is running, query it; after an uncertain send, reconcile it instead of replaying.
Use --resume with the exact SID; --continue selects a latest session and is unsuitable
for this binding. Do not send a no-op model probe into a live user task merely to test
connectivity when retained evidence or an authorized real continuation suffices.

Use an argument array with the installed executable, for example:

```javascript
const args = [
  '--cwd', workspace, '--resume', sessionId,
  '--json', '--no-color', '--mode', verifiedMode,
  '--disallowed-tools', ...taskDeniedTools,
  '--prompt', authorizedPrompt,
];
// Spawn with process-local verified configuration; stream stdout/stderr to
// private caller-owned evidence. Preserve the original account and session mode.
```

In 0.16.9 the denylist is variadic: place --prompt after it, and positional commands
such as doctor before it, or they can be consumed as tool names. Read current help
before reuse. Headless slash-command handling differs from TUI: /model was not a
supported model-selection route in the qualified headless flow. Use verified existing
binding rather than assuming a slash prompt changes configuration.

Capture process exit/signal, stderr and returned sessionId/turnId/traceId, response,
projection and usage when supplied. Verify the same SID and a new matching turn.
Accepted input, a zero exit or a generated report alone does not prove completion.
Distinguish process/transport exit from the task's persisted terminal state; a finished
assistant message does not prove a still-open transport exited successfully.

## Readback and attribution

Use supported exact-session queries first. When the installed route requires local
persisted evidence, inspect the schema and open SQLite read-only; restrict queries to
the exact SID, submitted input and subsequent turn. Message/part records can establish
assistant finish, matching tool calls, arguments, status, outputs and final text.
Inspect actual events, not only the final self-report. Avoid dumping unrelated history.

Correlate completed model_usage records with the exact session and current turn/trace,
including provider_id, model_id and variant. This is local client attribution, not
server attestation. Verify result files and hashes independently and compare authorized
before/after state. A correction resumes the same idle session with the concrete
remaining issue; do not redispatch the original work or open an equivalent task.

## Permission, privacy and route limits

Mode names, plan mode and tool denylists do not create a path sandbox. Denying Edit
still leaves writes possible through Bash or Write. Preserve the authorized permission
boundary, report missing enforcement and inspect actual tools and before/after state;
do not claim strict read-only prevention without verified isolation. The CLI can persist
session/cache state outside --cwd. An unchanged file hash proves endpoint equality,
not absence of intermediate changes; equal database counts do not prove content equality.

For process configuration, capture only in memory and emit an explicit nonsecret
whitelist. Parse connection URLs and emit only needed host/port/database metadata;
exclude userinfo, password and query. Filtering variable names for PASSWORD/TOKEN does
not sanitize a DATABASE_URL. Never emit raw process environments or credential files.

The bundled app-server is a separate host-driven protocol: standalone account-backed
model access may depend on native-host account synchronization. A standalone empty
account source does not prove that the desktop account is unavailable. Prefer the
qualified direct CLI route for same-account headless continuation; qualify app-server
separately if selected. Do not emulate host credential synchronization by copying keys.

A completed CLI tool task does not prove desktop task-list refresh, screenshots,
uninterrupted foreground continuity, approval handling or disconnect recovery. Retain
user sessions and preserve relevant failed-route evidence. Consult current installed
implementation first; [official CLI source](https://github.com/zai-org/ZCode/blob/main/apps/zcode-cli/packages/cli/src/run.ts)
and [Agent mode guide](https://zcode.z.ai/en/docs/agents) are rediscovery pointers, not
substitutes for the installed build's observed behavior.
