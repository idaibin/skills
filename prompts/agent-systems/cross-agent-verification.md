# Cross-Agent Verification

Use this prompt when a task benefits from using ChatGPT and Codex as separate thinking and verification surfaces.

## Task

Use ChatGPT and Codex to cross-check an idea, plan, implementation, or written output before treating it as ready.

## Language

- Respond in the user's language unless the user explicitly requests another language.
- Keep tool names, file paths, commands, API names, and product names unchanged.

## Roles

- ChatGPT is responsible for strategy, framing, tradeoffs, abstraction, writing direction, and second-opinion review.
- Codex is responsible for repository-grounded verification, file inspection, command execution, implementation details, and evidence from the local workspace.

Do not treat either side as automatically authoritative. Prefer the side that has direct evidence for the claim being made.

## Authority Resolution

Use this order when ChatGPT and Codex disagree:

1. Direct source evidence wins over reasoning.
2. For repository claims, direct runtime or rendered output evidence wins over source-code inference; source-code evidence wins over generic advice.
3. For external factual claims, primary external sources win over secondary summaries and reasoning.
4. Within the same evidence tier, prefer the most direct source for the exact claim; if directness is equal, prefer the newest applicable dated source.
5. When evidence is missing or partial, keep ChatGPT's point as a hypothesis and label it `Not verified`.
6. If evidence conflicts and no source clearly wins, output `Conflict unresolved` instead of blending the conclusions.

For repository work, `source evidence` means local repository source such as files, configuration, scripts, tests, generated output, runtime output, or rendered output. For external factual work, `source evidence` means primary external sources such as official documentation, standards, papers, release notes, or direct public records.

If Codex cannot access the target repository, files, commands, browser state, or external sources needed for the claim, switch to hypothesis-only mode for that claim and state the missing evidence.

In hypothesis-only mode, do not produce a `ready` decision. Use `Not verified` when evidence is missing or insufficient. Use `Conflict unresolved` only when two or more evidence-backed claims conflict and cannot be resolved.

For repository-grounded claims, Codex evidence must include provenance when available: repository path, branch, commit SHA, working tree state, command or file path, exit code for commands, and the relevant output excerpt. Rendered or browser evidence must include browser surface, URL, viewport when relevant, and whether the page was reused or freshly loaded. Treat evidence without enough provenance as weaker than current source evidence.

When evidence changes the answer, keep an audit trail:

```text
Superseded claim:
Correction:
Evidence:
Reason:
```

## Inputs

- Goal or idea: [describe the thing to verify]
- Task key: [short stable task name]
- Current artifact: [paste text, plan, code summary, or file paths]
- Target repository or context: [provide repo/path if relevant]
- ChatGPT session ID: [existing ID / create and record a new ID]
- ChatGPT session URL or title: [optional lookup helper]
- Browser tab handle: [tool-exposed tab/window id if available]
- Browser tab policy: [reuse recorded ChatGPT tab / prefer user's default browser such as Arc / use Chrome plugin fallback only if approved and verified]
- Verification depth: [quick / normal / strict]
- Expected output: [decision / revised plan / implementation notes / article outline / poster copy]

If repository, file, runtime, or source access is required but unavailable, state that limitation before making a conclusion.

## Verification Depth

- `quick`: check the core claim, obvious contradictions, and one most relevant source of evidence. Unknowns are allowed if labeled.
- `normal`: check the core claim, assumptions, relevant repository files or sources, and likely edge cases. Unknowns must be grouped under `Remaining unknowns`.
- `strict`: check the core claim, assumptions, relevant sources, edge cases, failure modes, and readiness gates before publication, merge, or release. Do not mark ready when a required source, command, runtime check, or review gate is unavailable.

## Session Continuity

Use one stable ChatGPT conversation as the reasoning surface for the whole verification loop.

- For a new task, create or select one dedicated ChatGPT conversation and record its session ID before starting the loop.
- For follow-up work on the same task, reuse the recorded ChatGPT session ID.
- Keep a simple session record that maps `Task key -> ChatGPT session ID -> URL/title helper -> browser tab handle -> last used date`.
- Treat the recorded session ID as the source of truth; tab title, URL, and browser tab handles are lookup helpers.
- Reuse the same ChatGPT conversation unless the user explicitly asks to start a new one.
- Reuse the same browser tab when possible, and prefer target-scoped operations by tab handle, exact conversation URL, DOM scripting, Playwright, or CDP.
- Revalidate any browser tab handle against the expected session URL or stable session ID before using it; tab handles can be scoped to a browser, tool session, or runtime lifetime.
- Prefer the browser that owns the recorded session, including Arc when it is the user's default or logged-in browser.
- Combine tools by role: use Codex Remote or the Chrome plugin for browser/tab state and target-scoped operations when available; use Computer Use only for UI steps not exposed through browser APIs, and report any focus, tab, window, or visible-state change.
- Treat Computer Use for Arc or any other browser as visible UI operation unless direct tab control has been observed for the target tab; do not promise background behavior from Computer Use alone.
- Use the Chrome plugin/Codex Chrome Extension as a Chrome fallback only after the user approves the account/session tradeoff and its tab APIs can enumerate or claim the target tab.
- Before sending a follow-up, confirm the target tab is the intended ChatGPT conversation; do not rely only on whichever tab is currently visible or active.
- Do not bring the browser forward, switch visible tabs, or take over unrelated active-tab work when target-scoped operation is available.
- If the tab was closed, replaced, logged out, or navigated away, stop and ask whether to recover the original session or start a new one.
- Do not silently continue in a different ChatGPT conversation and treat it as the same verification thread.
- Do not infer session continuity from model memory, conversation title, or apparent topic similarity. Continuity must come from the explicit session record or observable browser/session evidence.
- When reporting results, mention whether the ChatGPT session and browser tab were preserved, and include session identity confidence.

Use these session identity confidence levels:

- `verified_session_id`: a stable session ID was explicitly available and matched.
- `matched_session_url`: the same conversation URL was verified, but no stronger session ID was available.
- `matched_browser_tab_only`: the same browser tab was reused, but session identity was not independently verified.
- `not_verified`: session identity could not be proven.

## Session Record

Maintain a lightweight external record when using this workflow repeatedly. The record is metadata that the operator, repository, task tracker, or agent environment must store explicitly; do not assume the model will remember it across sessions.

```json
{
  "task_key": "",
  "chatgpt_session_id": "",
  "chatgpt_session_url_or_title": "",
  "browser_tab_handle": "",
  "browser_tab_window_note": "",
  "session_identity_confidence": "",
  "created_at": "",
  "last_used_at": "",
  "status": "active"
}
```

Rules:

- Create one record per task key.
- Use a dedicated review conversation per task; do not mix unrelated topics in the same ChatGPT conversation.
- Do not reuse one ChatGPT session for unrelated tasks just because the tab is still open.
- Do not create a new ChatGPT session for follow-up work when an active session record already exists.
- Update the existing record for follow-up work by replacing `last_used_at` and any changed lookup note; do not overwrite the task key or session ID unless the user starts a new session.
- Archive the record only when the task is complete or the user explicitly wants a fresh conversation.

If no persistent storage is available, include the updated record in the output so it can be copied into the appropriate external location.

If the session record cannot be read or written, do not claim persistence. Output the JSON record block and mark the persistence state as `Not verified`.

## Privacy And Data Boundaries

- Do not paste secrets, tokens, cookies, API keys, auth headers, license keys, `.env` contents, private credentials, or unrelated private user content into another model, browser session, prompt, or external service.
- Redact sensitive repository, browser, or account data before moving context between ChatGPT, Codex, browser tools, logs, screenshots, or external sources.
- Do not screenshot, transmit, or summarize unrelated browser content that is outside the task key.
- Share the smallest context needed for review; prefer summaries and file paths over raw private content when that is enough.
- Ask for explicit approval before sending private repository or user data to a different model, browser session, or external service.

## Workflow

1. Ask ChatGPT to clarify the idea:
   - What is the core claim?
   - What assumptions does it depend on?
   - What would make it useful, wrong, or misleading?
2. Ask Codex to verify the concrete context:
   - Check relevant files, commands, docs, diffs, runtime output, or source evidence.
   - Include evidence provenance for repository, runtime, rendered, or browser claims.
   - Separate verified facts from inferred conclusions.
   - Report missing evidence as `Not verified`.
3. Preserve the conversation thread:
   - Look up the task's recorded ChatGPT session ID before opening or sending messages.
   - Send follow-up questions to the same ChatGPT session and tab.
   - Carry Codex findings back into that same conversation when another ChatGPT pass is needed.
   - Mark any session break as a verification limitation.
4. Compare both results:
   - Keep points where strategy and evidence agree.
   - Revise points where evidence contradicts the idea.
   - Mark open questions where neither side has enough proof.
   - Keep all work within the declared task key unless the user expands the scope.
   - Treat explicitly named files, commands, configs, dependencies, and shared utilities as in scope only when needed to verify the task key.
   - Mark other adjacent findings as `Out-of-scope dependency detected`; put them under `Remaining unknowns` when they affect readiness, or under `Conflicts or corrections` when they changed the conclusion. Record the dependency, whether it blocks the current decision, and whether user approval is needed to expand scope.
5. Produce the final version:
   - Decision or recommendation
   - Evidence summary
   - Remaining risks
   - Next action

## Guardrails

- Do not use cross-agent verification as a way to create false certainty.
- Do not ask Codex to validate claims that require external sources unless browsing or primary sources are available.
- Do not ask ChatGPT to override local repository evidence with a generic best practice.
- Do not convert rough ideas into public claims until the evidence is clear.
- Keep the loop short; one strategy pass and one evidence pass is usually enough.

## Output

Return these sections in this order:

1. `Verified conclusion`
2. `What ChatGPT contributed`
3. `What Codex verified`
4. `Conflicts or corrections`
5. `Remaining unknowns`
6. `Session continuity status`
7. `Session record update`
8. `Next action`

Do not omit a section. Use `None` only when the section was checked and has no content.

Each section must include enough evidence state for the requested depth. Use exactly one primary status for the conclusion: `ready`, `not ready`, `conflict unresolved`, or `not verified`.

- `Verified conclusion`: one decision plus exactly one primary status.
- Every final conclusion must include status, claim, evidence basis, unknowns, and next action.
- `ready`: required evidence supports the decision; non-decision-impacting unknowns may remain.
- `not ready`: evidence exists and shows a readiness blocker.
- `not verified`: evidence is missing or insufficient.
- `conflict unresolved`: two or more evidence-backed claims conflict and no source clearly wins.
- Any unknown that affects merge, release, publication, or task readiness forces `not ready` or `not verified`.
- `What ChatGPT contributed`: strategy, framing, or risk points only.
- `What Codex verified`: concrete files, commands, outputs, sources, evidence provenance, or `Not verified`.
- `Conflicts or corrections`: include the `Superseded claim` block when a claim changed.
- `Remaining unknowns`: include every missing source or check that affects readiness.
- `Session continuity status`: state whether the same ChatGPT session ID and browser tab were preserved, with session identity confidence.
- `Session record update`: include the JSON record or `None`.
- `Next action`: one concrete action or `None`.

## Poster Angle

Short copy for later promotional posters:

> Let ChatGPT shape the idea. Let Codex check the ground truth.
>
> Strategy needs evidence. Evidence needs interpretation.
