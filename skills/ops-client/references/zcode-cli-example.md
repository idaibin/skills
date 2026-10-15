# Bundled ZCode CLI qualification example

Use only when an authorized task calls for operating an installed ZCode client through
its bundled CLI. This route uses no desktop UI input; it does not prove uninterrupted
foreground continuity, native-window presentation or desktop task-list synchronization. External-AI
provider selection and review quality remain with the requesting workflow.

## Identity and entry

Bind `command -v zcode`, the resolved executable inside the installed app, `--version`,
the exact `--cwd`, account/configuration source and intended session. Read installed
`--help` and run `doctor --json` for packaging and argument checks. `doctor` does not
prove model access, tool restrictions or a completed Agent turn. Use the installed
runtime as authority when upstream source or an older local profile differs.

The qualified macOS 0.16.9 bundle needed a process-local
`ZCODE_BUILTIN_PROVIDER_CONFIG_FILE` pointing to its existing
`config/provider/zcode-builtin.json`. Resolve and verify that resource in the current
installation; do not hard-code another installation's path, alter the app bundle,
copy credentials or change shared provider settings to make a probe pass. A missing
default catalog path is a bounded lookup failure, not proof of provider absence.

## Prompt and exact-session resume

For a bounded headless task, pass `--cwd`, `--prompt`, `--json` and an explicit mode.
The installed 0.16.9 help also advertises `--disallowed-tools`, `--no-color` and
`--resume <sess_...>`. Put a positional subcommand such as `doctor` before the
variadic `--disallowed-tools` option; otherwise it may be consumed as a tool name
and the CLI may enter TUI. In prompt invocations, put `--prompt` after the denylist
so it cannot be consumed as another tool name. `--continue` selects a latest session and is not a substitute for an
exact SID.

Capture direct process exit, stderr, the JSON `sessionId`, `turnId`, `traceId`,
`projection`, `response` and usage, then read the task's actual postcondition.
An exit code or JSON response alone does not prove tool effects or desktop state.
Before `--resume`, verify the original SID, workspace, terminal state and absence of
concurrent work; send once, confirm the returned SID is identical and turn ID is new.
After ambiguous submission, reconcile the existing session instead of replaying.
The CLI may persist session/cache state outside `--cwd`; an empty workspace is not a
zero-side-effect claim.

For model attribution, a completed session-bound `model_usage` row in ZCode's local
CLI database is stronger than the UI model picker or self-report, but it is still
local client evidence, not server attestation. Query only the exact SID after the
turn ends and protect credentials and transcript content. A warning on stderr must
be assessed against the requested capability even when the turn exits successfully.

## Permission and evidence boundary

`--mode plan` and a tool denylist are not a filesystem sandbox or a general read-only
guarantee. In the qualified 0.16.9 read/resume probe, the CLI used only `Read` and
left the disposable workspace file unchanged, yet its persisted session permission
field said `build`. Treat this as a bounded observed effect, not proof that future
file or command tools are disabled. For a real read-only review, require an authorized
isolated workspace or another verified enforcement route, inspect actual tool events
and before/after state, and leave strict write prevention `Not verified` otherwise.
Do not infer a successful app-server route, plugin loading, long-task recovery,
approval handling or foreground continuity from a CLI prompt smoke test.

The 0.16.9 qualification observed `--help` and `doctor --json` exit 0; a no-tool
prompt returned its requested short response with exit 0. A second disposable task
read a file using `Read`, then resumed the exact SID with a distinct turn; both
turns exited 0, the response and file hash matched, and local model usage recorded
`glm-5.3` completed. These are capability examples to revalidate against the
current installation, not reusable acceptance for another task or model.

For rediscovery, consult the [official CLI source](https://github.com/zai-org/ZCode/blob/main/apps/zcode-cli/packages/cli/src/run.ts) and [ZCode Agent mode guide](https://zcode.z.ai/en/docs/agents), then prefer the installed version's observed behavior.
