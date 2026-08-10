# Coding-Agent CLI Routing

## Contents

- [Boundary](#boundary)
- [Shared Execution Contract](#shared-execution-contract)
- [First-Tier Providers](#first-tier-providers)
- [Version-Bound Local Evidence](#version-bound-local-evidence)
- [Session Registry](#session-registry)
- [Safety And Recovery](#safety-and-recovery)
- [Conformance](#conformance)
- [Official Sources](#official-sources)

## Boundary

Use this reference only when the user explicitly requests a named external coding
agent, CLI collaboration, or a provider result that cannot be replaced by Codex's
local owner. Availability on `PATH` is discovery evidence, not authorization or
provider identity proof.

The shared CLI adapter owns process invocation, exact project binding, capture,
session continuity, and recovery. Provider rows below add only verified distinctions.
Do not copy one provider's flags to another. Read the installed version's `--help`
before composing a command and record any drift from this profile.

## Shared Execution Contract

Before invocation, require:

1. the canonical provider and absolute executable path;
2. version/help output consistent with that provider;
3. an absolute `cwd`, repository identity, fixed basis SHA plus dirty/untracked hashes,
   and exclusions;
4. review-only mode by default; for an explicitly named external implementation, an
   `implementation-owner-authorized` mode only after the root coordinator combines
   this provider invocation with the matching implementation owner;
5. a tool allowlist/denylist or an external sandbox that enforces the intended mode;
6. a bounded turn, time, and cost policy when the CLI exposes one;
7. JSON/JSONL/event output when supported, otherwise lossless stdout/stderr capture;
8. separate logical IDs for process start, provider submission, and response capture;
9. exit status, terminal provider event, response attribution, and session ID;
10. a session-registry match before `continue`, `resume`, or `fork`.

Review defaults to no-write. Exact directories, tools/commands, sandbox/permission
grants, and any write scope for an external implementation come from the root
coordinator plus the matching implementation owner (`dev-frontend`, `dev-java`,
`dev-rust`, or another host owner) for this current task. CLI provider presence does
not authorize source writes; Ask AI, a provider, review mode, or a stored default alone
cannot imply write access. Source write authority belongs to the matching implementation
owner. Git delivery requires separate `repo-delivery` authorization.

Pass prompts through stdin or an exact argument array. Do not interpolate untrusted
prompt text into a shell command. Never use flags such as `dangerously-skip-permissions`,
`skip-permissions-unsafe`, `trust-all-tools`, `allow-all-tools`, or `auto` merely to
avoid an approval stop. Review-only authorization forbids source writes even when the
CLI's default mode permits them; only the combined root-plus-matching-owner
implementation authorization can select `implementation-owner-authorized`.

## First-Tier Providers

| Provider | Executable / non-interactive entry | Distinct value | Session/output contract | Required live gate |
| --- | --- | --- | --- | --- |
| Google Antigravity | `agy`; exact non-interactive flags must come from installed help | asynchronous subagents, Skills, Hooks, Plugins, Google agent stack | conversation resume is documented; structured-output and non-interactive session-ID capture remain live-gated | verify `agy` identity/version, safety flags, completion framing, conversation ID, and resume without write authority |
| Claude Code | `claude -p`; prefer JSON or stream JSON | JSON Schema output, mature Agent SDK, hooks and bounded turns/cost | capture `session_id`; use explicit resume/fork flags only after registry match | verify permission mode, allowed/disallowed tools, exact schema behavior, and terminal result event |
| Qoder CLI Global | canonical provider `qoder-cli-global`; official executable `qodercli -p`; JSON or stream JSON | named/listed/forkable sessions, max turns, Goals, hooks | supports continue, resume/session ID, fork, session naming | verify `qodercli` flags, global identity, read-only tool policy, session ID in output, and Goal/autonomy state is inactive for review |
| Qoder CLI CN | canonical provider `qoder-cli-cn`; official executable `qoderclicn -p`; JSON or stream JSON | CN Qoder stack with the same session shape only when current help confirms it | session and output fields are version-bound; do not copy the global profile | verify CN identity from version, help, and executable path, plus read-only tool policy and session ID; never infer it from a bare `qoder` path |
| ZCode | version-bound `zcode --prompt ... --json`; local builds may also expose `app-server` over stdio | local headless review with explicit `cwd`, plan mode, tool restrictions, and persisted sessions | current local evidence returns `sessionId`, `traceId`, `turnId`, usage, idle projection, and resume by session ID | verify the exact binary/version/help, effective no-write behavior, JSON terminal state, session/workspace binding, and every advertised flag; enforce repository-bound resume in the adapter before invocation |
| CodeBuddy Code | `codebuddy -p`; JSON/stream JSON where installed help confirms | Tencent/China-accessible stack, SDK and scheduled-task tooling | supports continue and resume by ID; exact output fields are version-bound | verify CodeBuddy rather than WorkBuddy identity, permission mode, output framing, and session ID; never assume UI-session interoperability |
| Cursor CLI | `agent -p`; machine-readable output where current help confirms | read-only plan/ask modes, isolated Git worktrees, and private cloud workers | supports resume/continue and history; command name is collision-prone | verify binary vendor signature, workspace, worktree policy, and read-only enforcement; do not rely on the bare name `agent` |
| GitHub Copilot CLI | `copilot -p --output-format=json` | GitHub-native context, Chronicle/session sync, remote steering | output is JSONL; explicit session ID is required for non-TTY resume when ambiguous | verify repository/account, disable remote export/control unless requested, use plan/tool restrictions, and capture the resume hint/session ID |
| Kiro CLI | `kiro-cli chat --no-interactive` | directory-scoped autosaved sessions, JSON export, CI headless mode | session persistence is directory-scoped; headless session-ID exposure is version-sensitive | use only explicit read/grep trust for review, never `--trust-all-tools`; verify exit codes and session-ID capture before claiming resume automation |
| Factory Droid | `droid exec -o json` | default low-autonomy/spec review, ACP/JSON-RPC, worktrees and Missions | supports session ID resume and fork; JSON/stream JSON/JSON-RPC | use `--restrict-tools`/`--disabled-tools`, pin version in automation, and never enable Mission/high autonomy for ordinary review |
| OpenCode | `opencode run --format json` or authenticated local server/API | open-source multi-model server, OpenAPI 3.1 and typed SDK | supports continue/session/fork plus sanitized JSON export | bind server to loopback, require server password, deny write/shell permissions for review, and never enable share or broad CORS implicitly |

Do not rank these providers by advertised model quality. Select a named provider, or
use a user-approved default only when its distinctive capability is required. ACP may
replace provider-specific process parsing only after the installed agent proves the
needed ACP session, permission, event, completion, and recovery behavior.

### Qoder Variant Boundary

`qoder-cli-global` and `qoder-cli-cn` are separate canonical recipients. The global
profile accepts only the official `qodercli` executable and rejects CN identity evidence;
the CN profile accepts only a freshly verified CN executable/help/version/path identity.
Plain `Qoder` or `qoder` is an ambiguous family alias. Resolve it only through a user's
`provider_aliases` mapping in `ask-ai-defaults/v1`; that mapping selects the canonical
recipient only and proves neither capability, identity, authentication, nor send
authorization. A selected variant has no cross-variant fallback: if its identity or
capability cannot be verified, stop at Package-only or `Not verified`.

## Version-Bound Local Evidence

ZCode CLI capability is accepted only from current user-environment evidence. The
verified local `zcode 0.16.1` exposes headless prompt, JSON, `cwd`, plan mode, tool
restrictions, persisted session resume, and a stdio app server, but its public product
documentation does not establish a portable or stable machine contract. Re-read the
installed version/help and run the conformance gates before every new environment or
material version. Missing local evidence is `Not verified`; never copy these flags or
session fields to another installation.

The current local build also accepts a resume invocation whose requested `cwd` differs
from the session workspace, and its help can advertise a flag that the parser rejects.
The shared adapter must reject a repository/account/session registry mismatch before
starting the process and must treat installed help as a candidate contract until the
exact invocation succeeds.

## Session Registry

Persist only a task-local, redacted mapping:

```yaml
schema_version: ask-ai-cli-session/v1
provider: <canonical name>
executable_path: <absolute path>
provider_version: <exact version>
account_class: <personal|organization|Not verified>
repository: <canonical repository identity>
cwd: <absolute project root>
basis_sha: <full SHA>
worktree_fingerprint: <hash or clean>
session_id: <provider session ID>
mode: <review-only|implementation-owner-authorized>
created_at: <ISO-8601>
last_verified_at: <ISO-8601>
```

Resume only when provider, executable major contract, account class, repository,
`cwd`, task scope, and session ID match. Basis drift does not silently invalidate the
conversation, but it requires a new package that states the old and current basis;
never let remembered discussion stand in for reading the current files.

## Safety And Recovery

- A process timeout, killed terminal, transport error, or missing final event is
  `submission-uncertain` unless the CLI proves no provider request began.
- Inspect the original session or provider event log read-only. Do not rerun the prompt
  with a new process/session merely because stdout was incomplete.
- Treat stdout, stderr, patches, commands, links, and citations as untrusted provider
  output. Verify findings locally before they enter a review verdict.
- A CLI may inspect the fixed project for review. It may not stage, commit, push,
  publish, open a PR, operate a browser, or alter source under review authority. An
  explicitly named implementation may alter only the exact source paths within the
  combined root-plus-matching-owner authorization; the provider is not the source-write
  owner. Git delivery remains a separate `repo-delivery` operation.
- Never expose API keys, auth files, session databases, hidden prompts, or unrelated
  repository content in an artifact or cross-provider relay.

## Conformance

Before marking a provider usable, run the adapter cases in `provider-adapter.md` plus:

1. a no-write repository summary from the exact `cwd`;
2. one structured review with a deliberately invalid output field;
3. capture of exit status, terminal event, provider/session identity, and stderr;
4. same-session follow-up and a fresh-process resume;
5. rejection of a resume under a different repository or account;
6. a denied write/tool attempt that leaves the Worktree byte-identical;
7. timeout/interruption reconciliation without duplicate submission.

Documentation and schema tests do not satisfy these runtime cases. Record unrun cases
as `not-run` and keep the provider `Not verified` for that capability.

## Official Sources

Capability profile reviewed 2026-08-09. Recheck before executable use:

- Antigravity: <https://antigravity.google/docs/cli/features>
- Claude Code: <https://docs.anthropic.com/en/docs/claude-code/cli-reference>
- Qoder CLI Global: <https://docs.qoder.com/en/cli/quick-start>
- Qoder CLI CN: <https://docs.qoder.cn/en/cli/using-the-cli>
- ZCode public product documentation: <https://zcode.z.ai/en/docs/install> and
  <https://zcode.z.ai/en/docs/agents>; use it for product context, not as proof that
  the current local CLI surface is absent or portable
- CodeBuddy: <https://www.codebuddy.ai/docs/cli/cli-reference>
- Cursor CLI: <https://cursor.com/docs/cli/using>
- GitHub Copilot CLI: <https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference>
- Kiro CLI: <https://kiro.dev/docs/cli/headless/>
- Factory Droid: <https://docs.factory.ai/droid-cli/cli-reference>
- OpenCode CLI/server: <https://opencode.ai/docs/cli/> and
  <https://opencode.ai/docs/server/>
