# Frontend Playwright test authoring

## Entry and owner

Use when authorized to write or repair frontend journey tests in the project's
existing test-asset location. The accepted plan owns expected behavior; the current
page and generated scripts do not. Preserve the runtime, runner, lockfile, module,
fixture and authentication owners. Runner-only changes route to their source owner.

## Authoring procedure

1. Read the frozen acceptance IDs, target page/route and test scope; reuse analogous
   tests, seed/auth fixtures and project commands. Distinguish the application basis
   from the test-source basis, especially when they are separate repositories.
2. Consume bounded live locator/state evidence from the browser owner. Prefer
   accessible roles/names, labels and existing stable test IDs over guessed CSS or
   positional selectors. Unobserved selectors remain candidates; do not claim that
   code inspection verified the running page.
3. Generate the smallest independent case for each accepted scenario. Carry its ID
   through the project's existing title/annotation convention. Do not invent an
   additional registry; adopt a required title prefix only for an explicitly selected
   report adapter. Cover the visible outcome, not merely the successful click.
4. Use locator auto-waiting and web-first assertions. Wait for a relevant response or
   state transition rather than fixed sleeps or universal network-idle waits. Verify
   the actual response/business result when the accepted case requires it. Refresh
   alone is not independent database proof, and HTTP 200 alone is not business success.
5. Reuse isolated fixtures, safe unique test data and cleanup. Keep required secrets
   in the existing environment/secret mechanism, not generated code or committed
   storage state. Do not add a production data reset or real external send.
6. Run applicable static/script checks, then hand the scripts and original acceptance
   IDs back for authorized browser execution through the existing owners. An owner
   change does not by itself require another agent, task or user confirmation.

## Repair limits

Repair a demonstrated test defect without changing the accepted oracle. Preserve
first-failure evidence and re-run the same affected case after a minimal patch.
Do not turn product defects into skip/fixme/expected failures, remove cases, swallow
assertion errors, force clicks past an unexplained obstruction, or update screenshot
baselines to obtain green output. A longer timeout needs observed timing evidence
and must respect the accepted latency requirement; it is not a generic fix.

A business-source repair must be separately within the authorized scope. A failed
browser policy/sandbox/environment check is not a reason to alter business code,
weaken security or claim a mock run as real E2E. Preserve uncertain behavior as a gap.

## Handoff

Return changed test/config paths, accepted case mapping, unchanged or revised basis,
static results, actual runtime evidence where available, failure classification and
remaining coverage. Generated files are not proof of successful execution. Native
runner success still needs independent case-inventory and evidence reconciliation.
