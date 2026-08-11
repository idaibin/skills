# Coding-Agent CLI Routing

## Contents

- [Boundary](#boundary)
- [Shared Execution Contract](#shared-execution-contract)
- [Adaptive Monitoring](#adaptive-monitoring)
- [First-Tier Providers](#first-tier-providers)
- [Configured Runtime Profiles](#configured-runtime-profiles)
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
session continuity, and recovery. Provider rows below identify canonical recipients;
they do not prescribe a user's executable, model, flags, timeout, or output fields.
Resolve those values from the current request and the user-owned `cli_profiles` record
in `ask-ai-defaults/v1`, then verify them against the installed executable. Missing or
stale values fail closed instead of falling back to another provider or guessed flag.

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
6. a task-appropriate turn, time, and cost policy when the CLI exposes one, without a
   universal elapsed-time cutoff;
7. JSON/JSONL/event output when supported, otherwise lossless stdout/stderr capture;
8. separate logical IDs for process start, provider submission, and response capture;
9. exit status, terminal provider event, response attribution, and session ID;
10. a session-registry match before `continue`, `resume`, or `fork`.

The invocation builder must consume a validated profile and construct an exact argument
array. It must not embed provider versions, model IDs, executable paths, option order,
poll intervals, package directories, output field names, or known-bad flags in the
portable Skill. Canonical provider IDs, schema field names, and safety states are
protocol constants, not user preferences.

Before the one authorized submit, also freeze an invocation record with the exact
argument array, requested model/reasoning values, prompt/input transport, estimated
duration class, initial observation cadence, provider deadline when applicable, and
hard-process deadline or explicit no-deadline policy. Validate these separately:

- **Argument binding:** prove prompt-bearing options consume the intended prompt, not
  the next option token. Treat help as a candidate contract until this exact ordering
  succeeds on the installed build.
- **Input reachability:** every package/attachment path must be readable inside the
  selected `cwd` and permission policy. Otherwise move the ignored package under the
  repository review parent or use a bounded self-contained prompt before submit.
- **Model compatibility:** do not pair a model with effort/reasoning flags unless the
  installed build proves that exact combination. A parser/model-selection error with
  zero turns, zero usage, and no conversation ID is failed-before-submit; otherwise
  reconcile rather than retry.
- **Timeout layers:** a host yield/poll interval only schedules observation while the
  original process continues. It is never a provider deadline. Pass a configured
  provider deadline only when appropriate for that task. A hard process deadline that
  kills or detaches after possible submit is `submission-uncertain`; poll/reconcile the
  original process and provider session.

Capture requested and effective model separately. The command/argv proves the request;
only provider-owned structured result/event/log metadata proves the effective model.
Response prose such as "I am Gemini" is untrusted content, never attribution evidence.
When the user requires an exact model, accept the review only with an exact effective
model match plus provider session/conversation identity and terminal completion. A
missing or mismatched field is `Not verified` and the response must not enter an
architecture vote, consensus, approval count, or named-model comparison.

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

## Adaptive Monitoring

Estimate likely runtime from task size, provider mode, input volume, expected tool use,
and current CLI behavior before launch. Select an initial observation cadence from that
estimate: about one minute is a useful hint for short interactive work and about five
minutes for long reviews, research, or agentic work. These are scheduling examples,
not fixed limits. Shorten or lengthen later intervals when direct progress, provider
deadlines, or completion expectations change.

Every observation checks the same process or verified provider session for new output,
terminal state, exit status, model/session attribution, and basis drift. A quiet poll
keeps the operation `running`; it does not authorize a duplicate invocation, a new
conversation, model substitution, process termination, or an extra provider turn.
Stop waiting only on a verified terminal outcome, explicit user cancellation, an
applicable declared deadline/cost boundary, or loss of the original operation after
read-only reconciliation is exhausted.

The primary coordinator may delegate only wait, poll, and capture work to one smallest
capable read-only observer when that reduces blocking. Pass the existing host process
or provider session identity and observation contract, never the authority to submit,
continue, resume, retry, kill, change model, or judge the result. The primary
coordinator remains the single operation owner and locally verifies the captured
terminal evidence. If a configured observer names a role or model such as Luna, verify
the child runtime's effective role/model metadata before reporting that attribution;
on mismatch or unavailable delegation, keep monitoring with the primary owner or a
configured verified fallback without starting another provider invocation.

## First-Tier Providers

| Provider | Configurable boundary | Distinct value | Required live gate |
| --- | --- | --- | --- |
| Google Antigravity | executable, prompt/model/reasoning options, argument order, output and completion evidence come from its local profile | Google agent stack and selectable provider models | verify exact model compatibility, effective-model metadata, completion, conversation identity, and no-write policy |
| Claude Code | executable, print/output, permission, turn/cost, and resume options come from its local profile | schema output, SDK, hooks, bounded cost | verify permission policy, output schema, terminal result, and session identity |
| Qoder CLI Global | canonical recipient `qoder-cli-global`; identity rules and invocation shape come from its own profile | global Qoder distribution and sessions | verify global identity, review policy, terminal output, and session ID |
| Qoder CLI CN | canonical recipient `qoder-cli-cn`; identity rules and invocation shape come from a separate profile | CN Qoder distribution and sessions | verify CN identity independently; never infer it from a family alias or cross-fallback |
| ZCode | executable, headless entry, restrictions, output fields, and resume option come from its local profile | project-bound headless and persisted-session workflows where installed | verify every configured flag by invocation, terminal state, no-write behavior, and repository-bound resume |
| CodeBuddy Code | executable and machine-output contract come from its local profile | Tencent/China-accessible coding-agent stack | verify product identity, permission mode, terminal framing, and session ID |
| Cursor CLI | executable and machine-output contract come from its local profile | plan/ask modes and cloud/worktree workflows | verify vendor identity, workspace, worktree policy, and read-only enforcement |
| GitHub Copilot CLI | executable, prompt/output, planning, and resume options come from its local profile | GitHub-native context and session sync | verify account/repository, remote-control policy, terminal output, and session ID |
| Kiro CLI | executable, headless, trust, output, and session options come from its local profile | directory-scoped sessions and JSON export | verify read-only trust, exit behavior, and session exposure |
| Factory Droid | executable, output, tool restriction, and session options come from its local profile | ACP/JSON-RPC, worktrees, and Missions | verify restricted review mode, terminal output, session ID, and autonomy state |
| OpenCode | executable or local-server transport comes from its local profile | multi-model server, API, SDK, and sessions | verify loopback/auth policy, denied writes, output, and session continuity |

Do not rank these providers by advertised model quality. Select a named provider, or
use a user-approved default only when its distinctive capability is required. ACP may
replace provider-specific process parsing only after the installed agent proves the
needed ACP session, permission, event, completion, and recovery behavior.

### Qoder Variant Boundary

`qoder-cli-global` and `qoder-cli-cn` are separate canonical recipients. Each local
profile supplies its own executable candidates and identity evidence; the global
profile rejects CN evidence and the CN profile rejects global-only evidence.
Plain `Qoder` or `qoder` is an ambiguous family alias. Resolve it only through a user's
`provider_aliases` mapping in `ask-ai-defaults/v1`; that mapping selects the canonical
recipient only and proves neither capability, identity, authentication, nor send
authorization. A selected variant has no cross-variant fallback: if its identity or
capability cannot be verified, stop at Package-only or `Not verified`.

## Configured Runtime Profiles

Store mutable installed-runtime facts only in the user-owned defaults record. A profile
may configure executable candidates, identity markers, discovery arguments, exact
argument order, prompt transport, base/review arguments, model and reasoning options,
model aliases, output format, provider-owned attribution paths, terminal values,
resume option, workspace binding, deadlines, and log redaction. Validate the complete
record, preserve unrelated fields, write atomically, and read it back.

Treat installed help as a candidate contract. Before a material version change is
trusted, run a no-submit argument-binding probe and the relevant conformance cases.
When help advertises an option that the parser rejects, mark that configured option
`unsupported` for the observed executable fingerprint; do not encode the option or
version as a portable exception and do not keep guessing spellings. When a model and
reasoning combination fails before submission, record that exact combination as
incompatible in local evidence and rebuild only from configured, reverified values.

Prompt paths are also runtime facts. Verify package reachability under the exact `cwd`
and permission policy before the authorized submit. A provider log may contain account,
permission, prompt, path, or token-related data; capture only the minimum required
attribution and completion lines, apply configured redaction, and never relay the raw
log to another provider or publish it.

## Session Registry

Persist only a task-local, redacted mapping:

```yaml
schema_version: ask-ai-cli-session/v1
provider: <canonical name>
executable_path: <absolute path>
provider_version: <exact version>
profile_digest: <SHA-256 of effective validated CLI profile>
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
- A host poll/yield expiry with a live process is `running`, not a provider timeout.
  Keep one owner polling that same process; never start another invocation.
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
- Classify failures as `failed-before-submit`, `running`, `provider-rejected`,
  `submission-uncertain`, or `completed`. Only the first state permits rebuilding the
  same logical operation without reconciliation; quota, network, killed-process, empty
  planning-only output, and missing attribution never count as a completed review.

## Conformance

Before marking a provider usable, run the adapter cases in `provider-adapter.md` plus:

1. a no-write repository summary from the exact `cwd`;
2. one structured review with a deliberately invalid output field;
3. capture of exit status, terminal event, provider/session identity, and stderr;
4. exact requested/effective model match when a model is required; reject response
   self-identification as evidence;
5. same-session follow-up and a fresh-process resume;
6. rejection of a resume under a different repository or account;
7. a denied write/tool attempt that leaves the Worktree byte-identical;
8. host-poll, provider-deadline, and hard-process-timeout reconciliation without
   duplicate submission;
9. prompt argument binding and package reachability from the exact `cwd`.

Documentation and schema tests do not satisfy these runtime cases. Record unrun cases
as `not-run` and keep the provider `Not verified` for that capability.

## Official Sources

These links are discovery sources only; recheck the installed runtime before use:

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
