# App-owned session protocols

Use for an installed client's own CLI, stdio, socket or HTTP session API. The app and
transport are runtime inputs; no specific product, model or host path is required.
Prefer a verified semantic route for background tasks before probing GUI input.
For an installed ZCode CLI, read the [bounded CLI example](zcode-cli-example.md) to
qualify its actual command, configuration source, prompt and exact-session resume.
Use the [app-server example](app-server-example.md) only when that separate protocol
is the selected route. Neither example selects an external AI provider or approves
a new review request on behalf of its owner.

## Entry and reuse

Bind executable/bundle identity, build or hash, protocol envelope/version, transport,
configuration source, account boundary and exact workspace/session. A directory's
real path may differ from the stored workspace key; preserve the application's key.
Inspect installed help/schema/implementation only for unresolved fields. Do not open
a debugging port, restart the app or copy credentials to make a protocol work.

Reuse a qualification record whose executable/protocol/configuration, operation,
tool policy and session conditions still match. Keep the record in caller-owned
runtime evidence, with source locators, measured result, focus coverage, known failed
routes and their recovery conditions. Revalidate cheap identity/capability checks;
repeat an expensive probe only when diagnosed drift affects that operation. Failed
GUI writes and captures do not block independently verified protocol submission.
Do not retry an unchanged failed route or switch adapters around a policy denial.

## Submit and query

1. Resolve the authorized project/workspace and create or resume only the intended
   session. Read identity, current model, status, latest input and pending approvals.
   Concurrent work or an ambiguous session blocks sending; status queries may continue.
2. Bound the task, permitted paths, tools, effects, network and approval handling.
   Enforce supported tool filters and isolation in the execution layer; a prompt is
   not a sandbox. A tool-name allowlist limits tool kinds, not filesystem paths.
   Missing path isolation must be reported and limits the kinds of tasks accepted.
   Read-only qualification proves neither write safety nor arbitrary coding ability.
3. Submit once, retaining request identity and returned session/turn/revision. A
   transport success or accepted response means only received. After a timeout or
   disconnect, reconcile messages/events before sending again; absent native
   idempotency, an uncertain submission must not be replayed.
4. Query or subscribe within a bounded interval and budget. Bind status, message,
   tool-call/result and approval events to this session and the submitted turn.
   Separate queued, running, waiting-for-approval, terminal-success, terminal-failure
   and unknown using the actual protocol's states. Do not invent percentage complete.
   Empty active-tool lists at the end do not establish a tool-free turn.
5. Validate completion from matching user input, terminal event, assistant result and
   the task's observable postcondition. For tool tasks inspect actual tool name,
   arguments, completion and outputs; approval requests remain pending unless exact
   authority covers them. Never grant blanket approval or change global permissions.
6. End only owned transport processes after reconciling task status. Transport EOF,
   session deletion, cancellation and task termination are different effects. Retain
   user sessions. Do not cancel work on a query timeout without cancellation authority.

Apply the background profile's bounded foreground/focus observation when required.
Record activity or missing signals honestly; no activation calls in a client does not
prove uninterrupted focus. A later quiet interval cannot erase an earlier gap.

## Result and handoff

Return target/build/protocol identity, operation and authorization, workspace/session,
request/turn correlation, tool and path enforcement limits, accepted/running/terminal
observations, task postcondition, focus coverage, retained state and recovery conditions.
Keep secrets and business transcripts private. Bind evidence to the current task and
basis; new sessions or models do not inherit another session's successful result.

Backend project binding and session history prove protocol state. Desktop project
selection, visible task registration/refresh, AX input and full-window capture remain
separate claims. Long tasks, approval interactions, disconnect recovery and unattended
operation require their own observations.
