# App-Native Capability Canary

Use this canary before an App-native ChatGPT submission. It classifies current host
evidence and never calls `create_thread`, sends a prompt, or changes App state.

## Capture

1. Inspect the live schemas for `list_projects`, `list_threads`, `create_thread`,
   `read_thread`, and `send_message_to_thread`.
2. Call `list_projects` and `list_threads` read-only.
3. Build a sanitized JSON snapshot. Keep stable opaque IDs only when they are required
   to prove an exact Project mapping; remove labels, paths, titles, summaries, prompts,
   account data, and unrelated threads.

```json
{
  "schema_version": "ask-chatgpt-app-native-canary/v1",
  "requested_surface": "project",
  "explicit_quick_chat": false,
  "project_id": "g-p-opaque",
  "tool_schema": {
    "operations": [
      "list_projects",
      "list_threads",
      "create_thread",
      "read_thread",
      "send_message_to_thread"
    ],
    "create_thread_targets": [
      "project",
      "projectless",
      "chatgptWorkCloud"
    ]
  },
  "list_projects": {
    "projects": [
      {
        "projectId": "g-p-opaque",
        "projectKind": "chatgpt",
        "isGitRepository": false
      }
    ]
  },
  "list_threads": {
    "threads": [
      {
        "id": "chat-opaque",
        "kind": "chatgpt"
      }
    ],
    "unavailableSources": []
  }
}
```

## Run

```bash
python3 skills/ask-chatgpt/scripts/app_native_canary.py snapshot.json
```

Interpret the exit status:

- `0`: exact Project or explicitly requested Quick Chat mapping is ready;
- `10`: ask the user to open/switch to ChatGPT or Quick Chat once, then capture fresh
  `list_projects` and `list_threads` results;
- `20`: generic Standard Chat has no distinct current Native target; use an authorized
  browser route or Package-only;
- `30`: required operations/target are missing, evidence conflicts, the Project is not
  uniquely verified, or the snapshot is invalid.

The output's `state_change_allowed` applies only to capability mapping. The Skill's
external-action authorization, package, identity, model/reasoning, and ledger gates
still apply. Re-run after App restart, schema/authentication change, or any
`unavailableSources: [chatgpt]` result.

Run the offline routing, legacy-ledger, attestation, prompt-fingerprint, candidate,
and truncation regressions with:

```bash
python3 -m unittest scripts.test_ask_chatgpt_app_native
```
