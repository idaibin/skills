# Local Browser Workspaces

## Contents

- [Purpose](#purpose)
- [Surface Choice](#surface-choice)
- [Configuration](#configuration)
- [Route Table](#route-table)
- [Resolution](#resolution)
- [Capability Gate](#capability-gate)
- [Lifecycle](#lifecycle)

## Purpose

A user-owned Chrome Profile preserves existing logins, extensions, downloads, tabs,
and native tab groups. It also exposes user state and may interrupt visible work.
Select this surface only through a connected Chrome extension whose current browser,
Profile, tab, and group can be read back without activation.

Store local preferences at `~/.agents/config/ops-browser/defaults.yaml` and optional
project/site route rules at `~/.agents/config/ops-browser/routes.json`. These records
select where to look; they never prove current connection, authentication, placement,
background safety, or action authorization.

## Surface Choice

| Surface | Prefer when | Main boundary |
| --- | --- | --- |
| Codex in-app Browser | The task does not require the user's Chrome state | Its login, tabs, and downloads are independent. |
| User local Chrome | The task requires an existing login, extension, download context, exact tab, or native group | Require a connected Chrome extension and direct foreground-safety evidence. |
| Isolated managed browser | Repeatable isolation matters and user-profile state is unnecessary | It does not inherit user state or native groups. |

An explicit current-request surface wins. Otherwise apply the configured default.
Authentication on one surface never transfers to another. A local preference does not
authorize application activation, tab selection, GUI input, Profile creation, or
browser launch. If the selected Chrome extension route is unavailable, stop or use only
an explicitly configured eligible fallback.

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
  product: <user-selected Chrome product>
  application_path: <absolute path to the selected existing browser application>
  bundle_id: <selected browser bundle identifier>
  channel: <selected installed release channel>
  allowed_products: [<exact eligible browser product>]
  prohibit_alternate_binaries: true
  prohibit_managed_browser_downloads: true
  automation_runtime:
    playwright_channel: <installed browser channel>
    puppeteer_executable_path: <absolute path to the selected browser executable>
  surface_priority: preferred | fallback
  routing:
    default_surface: codex-in-app-browser | user-local-browser
    authenticated_fallback: user-local-browser | codex-in-app-browser | none
    local_development:
      surface: user-local-browser
      workspace: <user-selected logical label>
      reuse_existing: true
      create_if_missing: true
  execution_profile:
    mode: existing-user-profile
    selection: extension-connected-current
    launch_when_unlocked: false
    require_existing_when_locked: true
  extension_control:
    enabled: true
    install_target: existing-profile-only
    profile_selection: extension-connected-current
    connector: <Chrome plugin connector>
    browser_selector: chrome
    cdp_transport: chrome.debugger
    group_observation: openTabs.tabGroup
    no_profile_creation: true
  control_session:
    enabled: true
    strategy: unified | by-operation
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
    strategy: unified | by-operation
    default_group: <user-selected native group name>
    operation_groups:
      <exact operation type>: <user-selected native group name>
    require_verified_placement: true
    create_if_missing: true
    allow_group_creation: true
    create_tab_if_target_missing: true
    reuse_existing: true
    allow_unconfigured_groups: false
    allow_ungrouped: false
    close_task_tabs_after_use: true
    max_open_tabs_per_domain: <positive integer>
  locked_session:
    enabled: true
    require_prepared_control: true
    allowed_backends: [browser-extension-control]
    allow_transport_reconnect: true
    prohibit_browser_launch: true
    prohibit_debug_enablement: true
    prohibit_profile_import: true
    prohibit_window_activation: true
    prohibit_keyboard_pointer: true
  profile_state:
    reuse_existing: true
    automatic_profile_copy: false
    import_policy: user-mediated-only
last_verified_at: <informational timestamp>
```

`execution_profile.mode` accepts only `existing-user-profile`.
`extension-connected-current` selects the existing Profile reported by the connected
extension at runtime; it is not a literal Profile name and must not be rewritten to
`Default`. The selected connector must bind the browser family `chrome` and that
observed existing Profile. Never copy
cookies, cache, credentials, history, Keychain material, or Profile files. Never start
another browser or Profile to recover a failed connector.

When `allowed_products` is configured, it is a closed allowlist rather than a preference.
Bind the application path, bundle identifier, channel, product, and existing Profile before
use. With `prohibit_alternate_binaries` or `prohibit_managed_browser_downloads`, browser
automation must reuse the configured installed product through its supported installed
channel, executable, extension, or CDP connector. It must not run a browser installer or
fall back to another managed browser build. A test requiring a different engine or pinned
browser version stops `Not verified` unless the current request explicitly changes scope.

`last_verified_at` is informational. It does not prove the connector, Profile, native
group, tab, login, account, or foreground safety still exists.

## Route Table

Use `ops-browser-routes/v1` when stable projects, sites, or operation types should go
directly to a known surface.

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
        "browser_product": "<configured Chrome product>",
        "execution_profile": "extension-connected-current",
        "workspace": "<user-selected logical label>",
        "connector": "<Chrome plugin connector>",
        "browser_selector": "chrome",
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

Run `python3 scripts/resolve-local-browser-route.py <routes.json> <request.json>` with
only the available `cwd`, `url`, `operation_type`, and current user-request `text` in an
`ops-browser-route-request/v1` record. A matched route selects the connector and Profile;
it does not bypass live identity, login, group, foreground-safety, or action checks.
When several rules match, the highest numeric priority wins; file order breaks only an
exact priority tie.

Local target matching is fixed to Profile, account/session, origin, then URL. An in-app
route uses exact conversation, then URL, and declares no local-browser fields.

## Resolution

Resolve local control-session naming and native grouping independently:

1. explicit current-request instruction;
2. matched valid route rule;
3. valid local defaults;
4. active host behavior only when no configuration exists.

For `strategy: unified`, use the configured default name and no operation map. For
`strategy: by-operation`, resolve the exact operation type before the configured
default. Names are user-owned; never derive them from provider, task, agent, emoji,
page, or conversation labels.

Before browser setup, serialize one closed identity chain into
`local-browser-workspace-preflight/v1`: connected extension connector, selected browser
identity, extension-reported existing Profile, verified account/session, target kind plus stable ID or exact URL and
target fingerprint, target-tab state, and native group identity. When the target tab is
present, include its exact identity. Bind every element to
the selected browser and Profile; bind the target and tab to the verified account/session;
bind the tab to the target fingerprint and resolved native group. Also serialize the
stale/reconnected identity, policies, capabilities, group/session observations, selected
IDs, and placement target, then run
`python3 scripts/preflight-local-browser-workspace.py <evidence.json>`.

- Exit `0`: the configured existing workspace is ready.
- Exit `10`: perform only the explicitly permitted configured session/group/tab creation,
  then re-enumerate and rerun preflight.
- Exit `20`: stop `capability-unavailable` before claiming, creating, moving, or
  navigating a tab.
- Exit `2`: the evidence record is invalid or incomplete; stop and report `Not verified`.

## Capability Gate

Require one current connected Chrome extension identity, its reported existing Profile,
a verified account/session, target, and native group. A present target also requires an
exact tab identity. When current enumeration proves the target absent,
`target_tab_state: absent`, an empty `observations.target_tabs`, and available tab creation, stable identity,
and group-placement capabilities may return `creation-required` with only `create_tab`.
After creation, re-enumerate and rerun with the exact tab binding; only that second pass
may authorize `claim_verified_tab`. Enumerate only tab title, URL, recency, and group metadata needed
for target selection; do not inspect unrelated page content.

For strict grouping:

- Require independent group enumeration, stable group identity, exact group selection,
  and verifiable placement.
- Reuse an existing identity-matched tab in the configured group before considering
  creation. A missing page alone is not a stop condition when the group is unique and
  one-tab creation plus placement and readback are supported.
- A group label from one tab is observation only; it is not unique group identity.
- Session naming is not native-group placement proof.
- Create or move a tab only when the host exposes that exact operation and after-state
  proves the configured group.
- If the group is absent and creation is disabled or unverifiable, stop.
- If two groups share the configured name and stable identity cannot distinguish them,
  stop instead of selecting by color, order, active tab, or first match.
- With `allow_ungrouped: false`, never open or retain an unverifiably placed tab.

Before opening a tab, normalize the hostname and count observed tabs for that host in
the resolved group. At `max_open_tabs_per_domain`, reuse a safe matching tab, close only
an identity-matched unused task-created tab, or stop. Never close a pre-existing user
tab to make room.

While locked, require an already connected or reconnectable extension plus direct
proof of background-safe tab enumeration and page control. Never launch a browser,
enable browser debugging, activate a window, select a visible tab, import a Profile, or
use GUI input. A missing prepared connector stops the route.

## Lifecycle

Maintain a task-local tab ledger with operation ID, surface, browser/Profile identity,
opaque account fingerprint, native group identity, tab identity, target fingerprint,
ownership evidence, purpose, lifecycle state, and cleanup authority. Revalidate group
membership before changing a claimed tab and after any supported create or move.

Maintain one canonical restoration record per operation. Compute its SHA-256 fingerprint
over the target kind and ID/URL, surface, account, browser/Profile, group, tab,
before-state, and
authorized restoration plan. Completion requires one matching post-restoration readback;
duplicates, conflicts, or stale records make completion `Not verified`.

When `close_task_tabs_after_use: true`, close identity-matched task-created tabs unless
the user explicitly requests retention. Preserve pre-existing user tabs and groups.
Never delete, rename, merge, or reorder a user group without explicit authorization and
a verifiable host operation.

For an authorized configuration change, preserve unrelated valid fields, then read back
the complete effective record. A successful write still does not prove a live connector,
Profile, group, target, or page operation.
