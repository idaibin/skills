# Workspace Taskboard Evals

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `$workspace-taskboard status` | Live in-conversation project task panel. |
| `$workspace-taskboard resume ctl-7` | Verify same project roots then CAS/rebind. |
| `修改前端代码并测试` | Default to an in-root worker; no permission expansion. |
| `先讨论架构和范围` | Stay in controller; no worker. |
| `发给 thread-x` | Read ID, scope-check, then queue only. |

Reject cross-project/global board management, external-provider session management,
same-prefix paths, symlink escapes, and unverified multi-folder membership.

## Non-Trigger Eval

| Prompt | Expected owner |
| --- | --- |
| `只讨论这个功能范围` | Controller discussion; no worker creation. |
| `Use two subagents for review` | `adaptive-collaboration`. |
| `Commit and push this branch` | `repo-delivery`; Taskboard does not grant delivery. |
| `Resume this Claude Code session` | Provider owner, not Taskboard. |

## Quality Eval

Cover root and child cwd, parent/sibling/prefix rejection, symlink inside/escape,
host-verified multiple roots, unique reuse, default create, ambiguous choices, explicit ID
scope, closed/archived exclusion, discussion versus execution placement, no implicit Git
or external effects, one-shot create/readback, terminal notification, controller rebind,
status grouping, and no `turn completed => finished` inference.

Minimum evidence is quick validation, focused tests, canonical repository gate, routing
evals, minimal-context forward tests, fixed-basis independent review, and explicitly
bounded live Codex canary. Anything not exercised stays Not verified.
