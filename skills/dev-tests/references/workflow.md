# Execution workflow

## Contents

- [Establish the run](#1-establish-the-run)
- [Build finite coverage](#2-build-finite-coverage)
- [Execute each journey](#3-execute-each-journey)
- [Diagnose and retest](#4-diagnose-and-retest)
- [Exit](#5-exit)

## 1. Establish the run

Read effective project instructions and only the relevant Product, UI and API items.
Record the repository root, branch/SHA and relevant dirty-file identities separately
from the live runtime. Verify process command/cwd and endpoint where available;
distinguish same-port IPv4/IPv6 listeners and multiple checkouts. HTTP reachability
does not prove runtime identity. A proxy and its upstream belong in the environment
record. Verify the rendered application, route, role and dataset before interacting.

Inspect current scripts/configuration and choose actual declared commands. Reuse the
nearest effective tests; do not invent `test`/`lint` commands, treat a build as testing,
or launch new infrastructure implicitly. Capture a task-local baseline before tests.

When tests resolve packages through another checkout/application, temporary links or
ambient modules, record that dependency provenance as part of the run identity. Such
results prove only that environment, not an independent lockfile installation. After
replacing or removing those dependencies, rebind and rerun the affected checks; retain
the original pass without promoting it to the new environment. Missing harness packages
are environment/testability gaps, not product assertion failures. Dependency edits
belong to their implementation owner and require the existing task authority.

Exit this step with one identified target and known effects. If authentication,
identity, network or tools are missing, mark dependent cases BLOCKED and continue
available static/Mock/read-only cases with their narrower evidence label.

## 2. Build finite coverage

Derive the inventory from registered routes, reachable menus, feature specs, roles,
shared controls and API consumers. File or handler counts are not functional coverage.
Track every in-scope module through its journeys and state transitions. Keep a page
inventory separate from case coverage; opening one page does not cover its functions.

For each journey name its prerequisite, steps, expected state, evidence and cleanup.
Cover the applicable success path, invalid/boundary inputs, permission differences,
empty/error/loading states, cancellation, refresh/readback and recovery. Include
cross-module producers/consumers when required by the existing business contract.
Use pairwise/risk-based samples for large theme/viewport/role matrices and disclose
unsampled combinations. Do not silently reduce a requested full walkthrough to smoke.

Prioritize access/environment blockers, core business journeys, high-impact writes,
shared controls, then remaining pages. Freeze the finite inventory and report its
denominator. Add cases only for newly observed requirements or gaps, not to keep busy.

Bind required evidence layers to the accepted outcome. For an explicitly Mock-scoped
run, formal-service acceptance stays separate; it blocks this run only if required by
that outcome. Preserve explicitly required full walkthroughs and recordings.
On resume, reconcile latest evidence into the original case IDs before choosing work.
Name the missing assertion and why existing evidence cannot answer it. Recover usable
raw evidence before repeating actions; a fixture version change invalidates only cases
whose consumed data or behavior changed. Reproduce stale defect claims before repair.

When the project maintains a generated asset/case catalogue, consume its existing
stable IDs and run its drift/reference checks before selecting cases. Reconcile
registered routes, request definitions, controls/options and their direct/indirect
consumers separately. Apply the [generated coverage boundaries](coverage.md#generated-coverage-boundaries)
to the graph and oracle approval state. Keep unresolved extraction and unexecuted
obligations visible in the final denominator; catalogue validation is structural
evidence, not case execution.

## 3. Execute each journey

1. Check current basis and test data; capture the initial page/state and relevant
   network/console boundary. Wait for semantic readiness, including loaded fonts and
   settled data when visual assertions depend on them.
2. Perform real user input and clicks using fresh DOM/AX evidence. Read the input
   value back before submission, especially controlled inputs and rich-text editors.
3. Correlate the UI action with the request, business response and visible result.
   Use a new query/reload/detail view for independent persistence assertions; in-memory
   local echo is insufficient. Test cancel without submitting and check no side effect.
4. Exercise the planned negative/recovery branch only in an authorized isolated
   environment. Track HTTP errors, business failures and UI state independently.
   Missing fault-injection authority means that branch remains unverified.
5. Restore only task-owned test data and state via supported scoped operations.
   Verify restored records, counts and fault settings. Restarting a shared Mock or
   clearing all storage is not cleanup of one test record.

For a requested performance recording, freeze capture as part of the execution plan.
Use a separate scripted replay when recording overhead is excluded from measurement;
bind both phases to the same source, data, viewport, motion policy and case sequence.
If capture is included in the measured windows, disclose it and hold it equal across
compared runs. Validate the actual video and its covered operations independently;
a metric pass does not establish that a recording exists or is usable.

Close the case with its actual evidence and status before the next business journey.
If a write outcome is uncertain, reconcile it by readback before retrying; do not
produce duplicates. If another task changes source/fixtures mid-run, invalidate only
affected cases and rebind their basis. Do not interrupt or alter the other task.

## 4. Diagnose and retest

Distinguish product defect, contract disagreement, fixture gap, environment failure,
and automation failure. Reproduce with the smallest reversible sequence and record
expected/actual behavior plus causal request/state evidence. A locator timeout is not
automatically a product bug. After two failures for the same cause, retain both
outcomes and stop that unchanged hypothesis; continue only with diagnostic evidence
for a different route, while independent cases may proceed. A flawed Mock may hide missing fields or replacement
semantics; verify against the contract before changing any fixture.

Test ownership does not authorize source repair. When repair is already in scope,
the coordinator continues through the implementation owner, with required spec updates
and cross-module decisions, and returns for the failing case plus affected neighbors.
Retain the original failure and the new result; no need to rerun unrelated passed cases.

## 5. Exit

For performance comparisons, follow [performance measurement](performance-measurement.md)
for interpretation and acceptance. Receive raw browser/client observations from the
operations owner; it does not own the cross-layer verdict. Retest protected recovery
and keyboard states affected by the optimization, not just the faster path.

Reconcile the inventory: passes, failures, blocked/not-run cases and justified N/A.
All required assertions must have current evidence for the scoped journey to pass.
Finish when the authorized finite scope has terminal results, or all remaining work
has concrete recovery dependencies. The run can finish with failures; the system has
not thereby passed. Preserve evidence, reconcile created tabs/files/data, and return
the recovery queue rather than expanding into cleanup or optimization projects.
