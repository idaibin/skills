# Local Browser Workspaces

## Contents

- [Purpose](#purpose)
- [Surface Choice](#surface-choice)
- [Configuration](#configuration)
- [Configuration Changes](#configuration-changes)
- [Resolution](#resolution)
- [Control Session Gate](#control-session-gate)
- [Capability Gate](#capability-gate)
- [Lifecycle](#lifecycle)

## Purpose

A user-owned local browser can preserve logins, extensions, downloads, and existing
tabs better than a separate in-app or managed browser. It also exposes more user state
and may interrupt the user's window. Keep surface selection separate from tab-group
placement: choosing Chrome does not authorize reading unrelated tabs or creating a new
group.

Store optional local preferences at `~/.agents/config/ops-browser/defaults.yaml`.
They are discovery and placement policy, not current login, identity, capability, or
action authorization.

## Surface Choice

| Surface | Prefer when | Main boundary |
| --- | --- | --- |
| Codex in-app Browser | The task should stay non-interrupting and does not require user-profile state | Its cookies, login, tabs, and downloads are separate from the local browser and may expire independently. |
| User local browser | The task requires an existing login, extension, user download context, or an exact user-owned tab | It may affect visible user state; require direct background-safety evidence when non-interruption matters. |
| Isolated managed browser | The task needs repeatable isolation and no user-profile state | It does not inherit the user's login or extensions. |

An authentication failure on one surface never proves another surface is authenticated.
When the current request does not fix a surface, select the one that owns the required
state and verify it live. An explicit current-request surface remains a hard constraint.

## Configuration

```yaml
schema_version: ops-browser-defaults/v1
local_browser:
  product: <user-selected browser product>
  control_session:
    enabled: true
    strategy: unified | by-operation
    default_name: <user-selected control-session name>
    operation_names:
      <exact operation type>: <user-selected control-session name>
    require_verified_reuse: true
    create_if_missing: true
    reuse_existing: true
    allow_unconfigured_sessions: false
  tab_grouping:
    enabled: true
    strategy: unified | by-operation
    default_group: <user-selected group name>
    operation_groups:
      <exact operation type>: <user-selected group name>
    require_verified_placement: true
    create_if_missing: true
    reuse_existing: true
    allow_unconfigured_groups: false
    allow_ungrouped: false
    close_task_tabs_after_use: true
    max_open_tabs_per_domain: <positive integer>
last_verified_at: <informational timestamp>
```

For both `control_session` and `tab_grouping`, `strategy: unified` requires the
corresponding default name and an absent or empty operation map. With
`strategy: by-operation`, resolve an exact current-task operation type through its map,
then use its configured default only when no exact key exists. Session names, group
names, and operation keys are user-owned; the public Skill supplies no personal names
or closed operation map.

Set either section's `enabled: false` to disable only that policy. `last_verified_at`
is informational and never proves that the browser, control session, group, tab, or
login still exists.

## Configuration Changes

Create, modify, disable, or reset this record only when the user explicitly requests
a persistent configuration change. Validate the complete result before one atomic
write, preserve unrelated valid fields, then read back and report the effective
control-session and tab-group strategies, mappings, creation/reuse policy, cleanup
policy, and domain limit.
Changing configuration does not itself create, move, close, or inspect a browser tab.

## Resolution

Resolve local-browser control-session naming and tab grouping independently, each in
this order:

1. an explicit current-request instruction to use, avoid, or override the corresponding
   control-session or grouping policy;
2. a valid `ops-browser-defaults/v1` record;
3. the active browser host's ordinary behavior when no configuration exists.

A current-request override applies only to the current task and does not rewrite the
stored record. Invalid, conflicting, or partially populated workspace configuration
fails closed before opening, claiming, moving, or navigating a tab.

Control-session policy selects the host automation-session identity and label; grouping
selects tab placement. Neither selects an account, provider, Project,
conversation, model, browser permission, external recipient, or write authorization.

## Control Session Gate

Resolve the control-session policy before initializing a local-browser controller.
Starting or naming a host automation session is a browser-state action, not harmless
setup. A user statement that the target is already open means reuse the safely matching
browser session and tab; it does not authorize a second control session, group, or tab.

- Enumerate reusable control sessions when the host exposes that capability. With
  `reuse_existing: true`, bind the one verified session matching the resolved name and
  browser identity before considering creation.
- Call a required session-label operation such as `nameSession` only on the resolved
  session and only with the resolved configured name. Never derive its argument from a
  task title, provider, agent, emoji, page, or conversation name.
- Session naming does not create, select, reuse, merge, or verify a control session. If
  the host creates a session implicitly during controller setup, record that creation
  separately and apply `create_if_missing` before setup whenever the host can expose
  the behavior.
- With `allow_unconfigured_sessions: false`, never create or retain a convenience,
  per-task, per-agent, or per-provider session.
- With `require_verified_reuse: true`, missing session enumeration, selection, or
  after-state identity is `capability-unavailable`; stop before page operation instead
  of naming the current session and claiming reuse.

If the host requires a fresh uninspectable automation session for every task, it cannot
satisfy verified unified-session reuse. Report `capability-unavailable`; do not create a
same-named duplicate and do not weaken the tab-group policy to continue.

## Capability Gate

Before opening or claiming a local-browser tab, enumerate available tabs when exposed
and record only title, URL, recency, and group metadata needed for selection. Do not
inspect unrelated page content.

- Treat a tool-exposed `tabGroup` value as observation of that tab's current group.
- Treat session naming as a label only; it is not proof that the host reused, created,
  moved, or merged a browser tab group.
- Create or move a tab only when the active host exposes that exact capability and the
  after-state proves the resolved group name.
- When `reuse_existing: true`, reuse an existing verified target group and a safe
  matching tab before considering creation.
- When the resolved group does not exist and `create_if_missing: true`, create exactly
  that configured group only when the active host exposes a verifiable group-create or
  tab-placement operation. Re-enumerate afterward and require exactly one matching
  target group.
- When `allow_unconfigured_groups: false`, never create a convenience, inferred, or
  per-agent/session group. With `by-operation`, only names explicitly present in the
  map or its configured default are allowed.
- When `allow_ungrouped: false`, do not open or retain a local-browser tab whose target
  placement cannot be verified.
- When `require_verified_placement: true`, missing group enumeration or placement
  control is `capability-unavailable`; stop instead of guessing.

If the resolved group is absent and creation or placement cannot be verified, return
`capability-unavailable`; do not create an ungrouped tab or claim success from a
session label.

Before opening another tab, normalize the target to its hostname (an IP address or
`localhost` remains its exact host) and count observed tabs for that host in the
resolved group. `max_open_tabs_per_domain` must be an explicitly configured positive
integer. If it is missing while grouping is enabled, do not open another task-created
tab; reuse a safe matching tab or stop `capability-unavailable`. At the configured
limit, reuse a safe matching tab, close an identity-matched unused task-created tab,
or stop. Never close a pre-existing user tab merely to satisfy the limit.

## Lifecycle

Add the resolved control-session identity/name/reuse evidence plus tab-group strategy,
operation type, target group, observed group, placement evidence, and policy source to
the task-local tab ledger. Revalidate session identity and group membership
before changing a claimed tab and after any supported create or move action. A matching
group name does not override account/session or target-identity checks.

When `close_task_tabs_after_use: true`, close every identity-matched task-created tab
after its purpose is complete unless the user explicitly requests a delivery or handoff
tab. Preserve pre-existing user tabs and groups. Never delete, rename, merge, or
reorder a user group unless the current request explicitly authorizes that exact
browser-state change and the host exposes a verifiable operation for it.
