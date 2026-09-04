# Tab Identity and Lifecycle

Load this reference only when a browser task reuses, creates, changes, retains, or closes
a tab. It applies to in-app and configured local-browser surfaces without transferring
identity between them.

## Selection and Creation

Reuse only a tab with verified account/session evidence. Narrow candidates by browser
surface and Profile, verified account/session, exact origin, then exact URL.
URL matching never crosses an identity boundary. A configured user-local target absence is a creation
branch: create exactly one target tab only when group creation/placement policy permits,
then re-enumerate and rerun preflight. Missing or ambiguous browser, Profile, account,
group, placement, tab, or readback evidence remains `Not verified`.

## Ownership Ledger

Keep a task-local tab ledger that records task key, browser surface/session identity, tab
identity, target fingerprint, ownership evidence, purpose, lifecycle state, cleanup
disposition, retention authority. Record creation intent before opening and bind the
created identity after re-enumeration. Every executable single-tab action requires one
verified owner and direct readback. Batch only independent in-app tabs with one owner per
stable identity; keep dependent work serial.

## Reconciliation and Cleanup

Reconcile the task-local tab ledger before finishing. Resume ownership only from the same
revalidated browser surface/session, tab identity, and target fingerprint; otherwise mark
ownership `Not verified`. Retain a task-created tab only when the user explicitly
requested it; otherwise close identity-matched task-created tabs and restore authorized
state. Never close a pre-existing user tab without authority. After interruption, do not
close from a stale handle, URL match, or unverifiable ownership.
