# Workspace Task Routing

## Placement First

Keep product/architecture discussion, scope, priorities, decisions, and simple questions
in the controller. Treat implementation, tests, investigation, review, monitoring,
external AI, and Git delivery as worker placement by default. Placement never broadens
the request's mutation or external-effect authorization.

## One-shot Project Scope

The overview conversation does not own project files. Selecting a project creates one
visible, one-shot scope token with `project_id`, `control_id`, project controller ID,
canonical root, allowed-roots version, exact target cwd, authorization profile, and a stable
dispatch operation ID. Treat the label as display only. On submit, validate the token against
fresh project/controller readback, consume it once, and run this routing table immediately.
Do not analyze or rewrite the task in the overview conversation. A missing, stale, or
out-of-root token stops before send or create. Candidate ambiguity returns a structured
existing-task/New-task chooser; it is a routing stop, not a model discussion.

## Root Filter

Call project/list-read, thread/list-read, then resolve realpaths. Retain only local Codex
tasks whose project ID matches verified saved-project readback and whose cwd equals or is
a component-aware descendant of one versioned allowed root. Symlink targets inside pass;
escapes, parents, siblings, prefix collisions, projectless, remote, ChatGPT, and unknown
cwd entries do not. Filter before identity/reuse and never display excluded details.

## Decision Table

| Condition | Result |
| --- | --- |
| Discussion-only | execute in controller; no worker |
| Explicit ID in roots | queue only to that task |
| Explicit ID outside/non-local | `OUT_OF_SCOPE_WORKSPACE`; no send |
| Explicit ID cwd unreadable | `PLACEMENT_UNVERIFIED`; no send |
| Unique compatible `<project>:<worker cwd>:<responsibility>` | auto-reuse |
| Multiple/uncertain compatible candidates | list all plus `New task`; stop |
| Closed or archived similar task | exclude; create a new task |
| No candidate for execution | create normalized worker without delegation question |
| Missing project/read/create/registry evidence | stable fail-closed state |

Candidate choices include sequence, title, task ID, canonical cwd, responsibility, host
state, and bounded recent goal. Use structured input when available.
Treat both `status=archived` and the Codex archive receipt shape
`archived=true` as archived throughout explicit routing, reuse, resume, notification,
and status projection.

## Create And Readback

Immediately re-list saved projects. Use the host's real environment selection:
`isGitRepository=true` selects worktree and false selects local. Require the adapter to
mark placement readback mandatory. Before reservation, prove the selected create route
can place the exact requested canonical cwd. A local saved-project create proves its
canonical project root only. A child or attached-root cwd needs an exact
`host-create-adapter` placement receipt tied to the current allowed-roots version. If the
API has no cwd selector or equivalent receipt, return `PLACEMENT_UNVERIFIED` before any
create call; post-create readback cannot repair an avoidable orphan task.

Reserve/consume one create operation, then record
thread ID and host ID and read the task. Finalize only if the returned exact cwd lies in
the verified allowed roots and all project fields still agree. Out-of-root placement is
`PLACEMENT_UNVERIFIED`/`BASIS_DRIFT` and is never silently managed. Reconcile pending
client IDs or uncertain returns; do not create twice.

Use current `list_projects`, `list_threads`, `read_thread`, `create_thread`,
`send_message_to_thread`, `wait_threads`, title, and explicitly authorized archive tools.
Long-lived visible work uses Codex tasks, not subagents. External provider sessions remain
inside their owner adapters and are not board cards.
