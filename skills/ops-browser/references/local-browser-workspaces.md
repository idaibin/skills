# Local Browser Workspaces

## Contents

- [Purpose](#purpose)
- [Surface Choice](#surface-choice)
- [Configuration](#configuration)
- [Route Table](#route-table)
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

Store optional project/site route rules at
`~/.agents/config/ops-browser/routes.json`. Resolve them before probing a browser
surface; they select where to look, never prove that the selected route is ready or
authenticated.

## Surface Choice

| Surface | Prefer when | Main boundary |
| --- | --- | --- |
| Codex in-app Browser | The task should stay non-interrupting and does not require user-profile state | Its cookies, login, tabs, and downloads are separate from the local browser and may expire independently. |
| User local browser | The task requires an existing login, extension, user download context, or an exact user-owned tab | It may affect visible user state; require direct background-safety evidence when non-interruption matters. |
| Isolated managed browser | The task needs repeatable isolation and no user-profile state | It does not inherit the user's login or extensions. |

An authentication failure on one surface never proves another surface is authenticated.
When the current request does not fix a surface, select the one that owns the required
state and verify it live. A stored `surface_priority: preferred` makes the local browser
eligible only after the foreground-safety gate passes; it never authorizes tab/window
activation, focus changes, or GUI input. When background-safe local control is unavailable,
use the in-app Browser if its independent state suffices, otherwise return `Not verified`
or obtain explicit current-task consent before visible control. Restoring focus afterward
does not satisfy this gate. An explicit current-request surface remains a hard constraint.
The control-session and tab-group sections apply only to `user-local-browser`; never
apply Chrome grouping to the Codex in-app Browser, cloud/agent browser, or an isolated
managed browser.

## Configuration

```yaml
schema_version: ops-browser-defaults/v1
in_app_browser:
  require_live_tab: true
  multi_tab:
    strategy: parallel-per-tab
    preferred_executor: luna_worker
    required_executor_runtime_model: gpt-5.6-luna
    require_runtime_identity: true
    one_owner_per_tab: true
    serial_fallback: disabled
local_browser:
  product: <user-selected browser product>
  surface_priority: preferred | fallback
  fixed_application:
    name: <user-selected application name>
    bundle_path: <local private absolute .app path>
    discovery: disabled
    fallback: none
    post_launch_verification: single-fixed-route-readback
  routing:
    default_surface: codex-in-app-browser | user-local-browser
    authenticated_fallback: user-local-browser | codex-in-app-browser | none
    local_development:
      surface: user-local-browser
      workspace: <user-selected logical workspace label>
      reuse_existing: true
      create_if_missing: true
  execution_profile:
    mode: existing-user-profile | dedicated-user-data-dir
    name: <user-selected profile name>
    user_data_dir: <local private absolute path>
    profile_directory: <Chrome profile directory>
    launcher: <local private launcher path>
    login_bootstrap: <local private non-automated login launcher path>
    probe: <local private readiness probe path>
    launch_when_unlocked: true
    require_existing_when_locked: true
    cdp:
      address: 127.0.0.1
      port_strategy: fixed | devtools-active-port
      port: <loopback port when fixed>
      enabled: true
  control_session:
    enabled: true
    strategy: unified | by-operation | dedicated-profile
    default_name: <user-selected control-session name>
    operation_names:
      <exact operation type>: <user-selected control-session name>
    require_verified_reuse: true
    create_if_missing: true
    allow_name_session: true
    reuse_existing: true
    allow_unconfigured_sessions: false
  tab_grouping:
    enabled: true
    strategy: unified | by-operation | dedicated-profile
    default_group: <user-selected group name>
    operation_groups:
      <exact operation type>: <user-selected group name>
    require_verified_placement: true
    create_if_missing: true
    allow_group_creation: true
    reuse_existing: true
    allow_unconfigured_groups: false
    allow_ungrouped: false
    close_task_tabs_after_use: true
    max_open_tabs_per_domain: <positive integer>
  locked_session:
    enabled: true
    require_prepared_control: true | false
    allowed_backends: [browser-native-control, browser-extension-control, direct-cdp]
    allow_transport_reconnect: true
    prohibit_browser_launch: true | false
    prohibit_debug_enablement: true | false
    prohibit_profile_import: true
    prohibit_window_activation: true
    prohibit_keyboard_pointer: true
    cdp:
      require_loopback_only: true
      require_dedicated_profile: true
      require_prelock_roundtrip: true | false
  profile_state:
    reuse_existing: true
    automatic_profile_copy: false
    import_policy: user-mediated-only
last_verified_at: <informational timestamp>
```

## Route Table

Use `ops-browser-routes/v1` when stable projects, sites, or operation types should go
directly to a known browser surface instead of probing the default and then falling
back. The file is local and user-owned; public packages do not ship personal paths,
domains, profile names, ports, or workspace labels.

```json
{
  "schema_version": "ops-browser-routes/v1",
  "rules": [
    {
      "id": "<stable local rule id>",
      "enabled": true,
      "priority": 100,
      "match": {
        "any": [
          {"origins": ["https://example.test"]},
          {
            "project_roots": ["<local absolute project root>"],
            "keywords": ["<task keyword>"]
          },
          {"operation_types": ["<exact operation type>"]}
        ]
      },
      "route": {
        "surface": "user-local-browser",
        "browser_product": "<configured browser product>",
        "execution_profile": "<configured profile name>",
        "workspace": "<user-selected logical label>",
        "cdp": {"address": "127.0.0.1", "port": 9224},
        "reuse_existing": true,
        "target_match_order": [
          "profile",
          "account-session",
          "exact-origin",
          "exact-url"
        ],
        "skip_default_surface_probe": true
      }
    }
  ],
  "fallback": "defaults"
}
```

Run `python3 scripts/resolve-local-browser-route.py <routes.json> <request.json>`
with a minimal `ops-browser-route-request/v1` record containing only the available
`cwd`, `url`, `operation_type`, and current user-request `text`. Exclude attached
document instructions, webpage content, tool output, and delegated-provider text from
that routing field. Each object under `match.any` is one alternative clause; all fields
inside the selected clause must match. Lists match any configured value. The highest
numeric priority wins, with file order breaking a tie. The resolver returns no raw task
text. `enabled` defaults to `true`; set it to `false` to temporarily ignore the rule.
The target match order is a fail-closed identity contract: local-browser routes require
`profile`, `account-session`, `exact-origin`, then `exact-url`; in-app routes require
`exact-conversation`, then `exact-url`. The resolver rejects missing, reordered, or
unknown steps instead of weakening target identity checks.

A matched route bypasses only default/fallback surface discovery. It does not bypass
profile, endpoint, target, login, account/session, foreground-safety, action, or
postcondition checks. For a loopback dedicated-profile route whose session and group
policies are disabled, preflight only the selected profile identity, loopback endpoint,
target enumeration, and required page-control capabilities; do not require native
Chrome group enumeration merely because the route stores a workspace label.

For `codex-in-app-browser`, omit `browser_product`, `execution_profile`, `workspace`,
and `cdp`. A web-review route selects only the webpage surface; app-native ChatGPT
Project/Thread work remains with `ask-ai`.

`execution_profile.mode: dedicated-user-data-dir` makes the entire Chrome data root
the AI isolation boundary. It does not inherit the default Chrome profile, cookies,
credentials, extensions, or account state. The launcher may start it while unlocked.
While locked, `require_existing_when_locked: true` permits only an already running,
verified endpoint; `false` permits one policy-authorized background launch and CDP
initialization followed by complete current-state revalidation. `devtools-active-port`
reads the task-owned `DevToolsActivePort` record instead of assuming a fixed port.

Account sign-in and MFA use `login_bootstrap`, which launches the dedicated profile
without CDP, automation flags, extension control, or GUI scripting. Never automate or
observe credentials. After the user confirms sign-in, close that exact profile cleanly
and start the ordinary launcher. A fixed loopback CDP port avoids the WebDriver signal
associated with Chrome's zero-port automation mode, but it does not bypass provider
risk controls or prove that sign-in will remain accepted.

For both `control_session` and `tab_grouping`, `strategy: unified` requires the
corresponding default name and an absent or empty operation map. With
`strategy: by-operation`, resolve an exact current-task operation type through its map,
then use its configured default only when no exact key exists. Session names, group
names, and operation keys are user-owned; the public Skill supplies no personal names
or closed operation map.

With `strategy: dedicated-profile`, set the corresponding section to `enabled: false`:
all tabs in that browser data root are AI-owned, so a Chrome group or task-named host
session adds no isolation. Never call `nameSession` or create a task/provider group in
this mode.

Set either section's `enabled: false` to disable only that policy. `last_verified_at`
is informational and never proves that the browser, control session, group, tab, or
login still exists.

`surface_priority: preferred` makes the configured local browser the default only
when the current request does not select another surface. It never overrides a hard
surface constraint or missing live capability. The locked-session record permits a
browser-native, extension, or loopback CDP control plane. When browser launch or debug
initialization is not prohibited, it authorizes one background setup attempt without
unlocking, waking, activating, foregrounding, or GUI input.

When `fixed_application` is present, its bundle path resolves local-browser selection
without product, profile, launcher, or fallback discovery. Invoke or reuse that exact
application, then perform one current-state readback of its configured profile,
endpoint, and target. A failed readback stops `Not verified`; it does not reopen
surface discovery.

For the in-app Browser, `require_live_tab: true` means every page operation owns a real
claimed or task-created tab identity. With `parallel-per-tab`, two or more independent
tabs are dispatched together, one verified executor per tab, and have no serial
fallback. Tabs that share a conversation, writer, mutable state, or ordering dependency
remain under one owner and execute serially.

`routing.default_surface` selects the ordinary unqualified route. When
`authenticated_fallback` is configured, first verify that the default surface lacks the
required login, then inspect the fallback surface and continue there only after its
target login is directly verified. `routing.local_development` overrides the ordinary
route for loopback and explicitly identified local dev/preview pages. Reuse a safe tab
matching environment, account, and origin before creating one. A workspace label such
as `AI_dev` is routing metadata unless the active background controller independently
exposes native Chrome group enumeration and placement; never foreground the browser to
manufacture group evidence.

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
2. a matched valid `ops-browser-routes/v1` rule for surface/profile/endpoint/workspace
   selection;
3. a valid `ops-browser-defaults/v1` record;
4. the active browser host's ordinary behavior when no configuration exists.

Resolve a route rule before probing the default surface. A matched rule with
`skip_default_surface_probe: true` goes directly to its selected surface; a failed
readiness or login check stops or degrades that route and does not silently retry the
ordinary default. With no matched rule, preserve the default-plus-bounded-fallback
behavior.

A current-request override applies only to the current task and does not rewrite the
stored record. Invalid, conflicting, or partially populated workspace configuration
fails closed before opening, claiming, moving, or navigating a tab.

Control-session policy selects the host automation-session identity and label; grouping
selects tab placement. Neither selects an account, provider, Project,
conversation, model, browser permission, external recipient, or write authorization.
The execution-profile boundary is resolved first. When it is `dedicated-user-data-dir`,
reuse or launch that exact profile and apply no Chrome group requirement. While locked,
reuse or reconnect first. If `require_existing_when_locked` is false and launch/debug
initialization is permitted, attempt one background setup and revalidate the resulting
profile and endpoint before page action.

## Control Session Gate

Resolve the control-session policy before initializing a local-browser controller.
Starting or naming a host automation session is a browser-state action, not harmless
setup. A user statement that the target is already open means reuse the safely matching
browser session and tab; it does not authorize a second control session, group, or tab.
When `allow_name_session: false`, never call a session-label operation, including with
the configured name. When `allow_group_creation: false`, never create a group. These
explicit denials take precedence over controller defaults and advertised capabilities.

Before setup, serialize the selected browser ID, any stale/reconnected browser ID,
resolved policies, capability states, stable session/group observations, selected IDs,
and placement target into `local-browser-workspace-preflight/v1`, then run
`python3 scripts/preflight-local-browser-workspace.py <evidence.json>`. Treat exit `20`
as `capability-unavailable`. Exit `10` is `creation-required`: perform only the exact
configured session or group creation whose result field is true. Exit `11` is
`setup-required`: perform exactly one `background_browser_setup`, then rerun with
`background_setup_attempted: true` and fresh evidence. Neither state permits
`nameSession`, `tabs.new`, navigation, or page action. If setup or creation completion
is ambiguous, do not retry.

Preserve the preflight input, result, exit state, and timestamps in the same fixed
evidence package as the later Capability Snapshot and requested action. When a ready
route still needs a live foreground-safety canary, bind one non-mutating canary to the
same profile, endpoint, backend, and identity-matched existing target; record its
method and before/after focus evidence, then capture the Snapshot before the requested
operation. Never run the requested operation first and use a later preflight, canary,
or Snapshot to approve it retroactively.

- Enumerate reusable control sessions when the host exposes that capability. With
  `reuse_existing: true`, bind the one verified session matching the resolved name and
  browser identity before considering creation.
- Call a required session-label operation such as `nameSession` only on the resolved
  session and only with the resolved configured name. Never derive its argument from a
  task title, provider, agent, emoji, page, or conversation name.
- If the active controller requires a task-specific `nameSession` call, record
  `controller_constraints.requires_task_specific_session_name: true` and fail the
  preflight. Do not call it with the configured name as a workaround because some
  controllers create a duplicate group even when the label matches.
- Session naming does not create, select, reuse, merge, or verify a control session. If
  the host creates a session implicitly during controller setup, record that creation
  separately and apply `create_if_missing` before setup whenever the host can expose
  the behavior.
- When the resolved session is proven absent and `create_if_missing: true`, the gate
  may permit only exact managed-session creation. It must prove zero same-name session
  observations first; a label-only or duplicate observation blocks creation. Group
  resolution waits until the new session has a stable identity and the gate is rerun.
- With `allow_unconfigured_sessions: false`, never create or retain a convenience,
  per-task, per-agent, or per-provider session.
- With `require_verified_reuse: true`, missing session enumeration, selection, or
  after-state identity is `capability-unavailable`; stop before page operation instead
  of naming the current session and claiming reuse.
- After a browser disconnect, discard every session/group observation bound to the old
  browser ID. Re-enumerate against the new browser ID and require stable session and
  group identities plus explicit selection again. A same display name across two
  Chrome instances is not continuity evidence.

If the host requires a fresh uninspectable automation session for every task, it cannot
satisfy verified unified-session reuse. Report `capability-unavailable`; do not create a
same-named duplicate and do not weaken the tab-group policy to continue.

## Capability Gate

Before opening or claiming a local-browser tab, enumerate available tabs when exposed
and record only title, URL, recency, and group metadata needed for selection. Do not
inspect unrelated page content.

Record `screen_session` and `selected_backend` in preflight. With `locked`, require
`background_safe_tab_enumeration` and `background_safe_page_control` plus an existing
connection, a reconnectable endpoint, or one policy-permitted background setup attempt.
The setup must not unlock, wake, activate, foreground, or use GUI input. When a caller
requires lock-safe behavior and the screen state is `unknown`, stop before page action.
This gate cannot establish window visibility, screenshot, focus, keyboard, pointer,
Accessibility, or coordinate evidence.

For `direct-cdp`, require a loopback-only endpoint and a dedicated automation profile.
When `require_prelock_roundtrip` is false, current-session proof of the exact profile,
endpoint, target enumeration, background-safe transport, and page control is sufficient.
After a background launch or reconnect, revalidate that complete chain. CDP availability
does not authorize copying the user's default Chrome profile.

- Treat a tool-exposed `tabGroup` value as observation of that tab's current group.
- A `tabGroup` label without independent group enumeration, a stable group ID, and an
  exact selection operation cannot satisfy verified reuse or placement.
- Treat session naming as a label only; it is not proof that the host reused, created,
  moved, or merged a browser tab group.
- Create or move a tab only when the active host exposes that exact capability and the
  after-state proves the resolved group name.
- When `reuse_existing: true`, reuse an existing verified target group and a safe
  matching tab before considering creation.
- When the resolved group does not exist and `create_if_missing: true`, create exactly
  that configured group only when the gate returns `creation-required` with
  `create_group: true` and the active host exposes a verifiable group-create operation.
  Re-enumerate afterward and require exactly one matching target group plus verified
  selection and placement before creating or moving a tab.
- When `allow_unconfigured_groups: false`, never create a convenience, inferred, or
  per-agent/session group. With `by-operation`, only names explicitly present in the
  map or its configured default are allowed.
- When `allow_ungrouped: false`, do not open or retain a local-browser tab whose target
  placement cannot be verified.
- When `require_verified_placement: true`, missing group enumeration or placement
  control is `capability-unavailable`; stop instead of guessing.
- If two groups share the resolved name and the host cannot distinguish them by stable
  identity, stop `capability-unavailable`; do not select by color, order, active tab,
  or first match.

If the resolved group is absent and creation or placement cannot be verified, return
`capability-unavailable`; do not create an ungrouped tab or claim success from a
session label.

Never copy a live Chrome profile, cookies, cache, saved credentials, history, or
Keychain material into an automation profile. With `automatic_profile_copy: false`,
authentication must come from a verified existing user-local-browser connection or a
user-mediated sign-in/import into the dedicated profile. Imported navigation data is
initialization help only and never proves current authentication or account identity.

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
