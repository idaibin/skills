# AI-assisted Playwright E2E acceptance

## Entry and boundary

Use for an explicitly scoped browser journey when test planning, generated scripts,
repair or native execution needs coordination. Keep the current test plan and IDs.
This profile owns acceptance, not script/source implementation, browser mechanics,
Agent installation, model configuration or a new test framework.

## Procedure

1. Default to current-code/runtime-derived planning for existing projects; a full
   PRD and approval of every inferred case are not prerequisites. Apply the existing
   coverage rules: available confirmed Product/UI/API decisions prevail; otherwise
   label current-behavior baselines and provisional inferences. Resolve application
   and test-source basis, target, environment, account/data and side-effect authority.
   Freeze a finite case/project inventory and expected outcomes before the asserted
   run, including prerequisites, visible/API results, evidence source and cleanup.
2. Reuse the actual runner, configuration and fixtures. Preflight the locked version,
   browser, seed/login and required services. Resolve host-provided planning,
   generation or repair adapters only when present; names or installed files do not
   prove that the current host loaded or executed them. No extra Agent is mandatory.
3. Delegate scoped live exploration to the browser owner. Pass the evidence-labeled
   plan, observed locators/states and test-asset scope to the implementation owner for
   missing scripts. Frontend journeys stay with the frontend implementation owner;
   non-browser runner/configuration work goes to its actual source owner.
4. When scripts exist, freeze their basis and run the selected native test command.
   Keep the application checkout read-only for acceptance. Execute real clicks,
   input, navigation and visible assertions with real services where required.
   Mock tests, API-only tests and source inspection remain separately labeled.
5. Preserve each failing result. Distinguish test defects, product defects,
   expectation conflicts and environment blockers. Explore disputed or unverifiable
   business meaning within budget, then record evidence, affected IDs and the question
   for later human confirmation. Continue independent cases; defer only dependent
   business verdicts or unsafe operations. Send only authorized repairs to their owner.
   Set a finite repair budget, then re-run affected cases on the new basis. An owner handoff does
   not require repeated permission for actions already authorized.
6. Reconcile native output and process exit against the original inventory, not a
   new inventory inferred from whatever tests remain. A baseline/inference pass is
   not business approval. Preserve passed, failed, blocked, not-run and excluded separately. Missing access is blocked, not excluded.

## Acceptance safeguards

A healer may propose a locator/wait/data correction only when the original expected
behavior is preserved and observed evidence supports the change. A generated skip,
fixme, expected failure, dropped case, weakened assertion or automatic screenshot
rebaseline is not a passing repair. Stop that promotion and retain the original case.
A product defect needs source-write authority and a fresh test basis; it does not
justify changing the expected business outcome.

Use the project's native case/report checker when available. Require every selected
case/project pair to execute and pass; reject zero-test success, duplicates,
missing cases, skipped outcomes, global setup/teardown errors and retry-only success.
A summary count or exit 0 alone is insufficient. Check runner/version, source,
configuration, environment and evidence identity; a report file alone is not trusted
proof that the target ran. Do not infer a browser project from its display name.

Use isolated test state and bounded cleanup; keep credentials/auth state out of Git
and shared reports. Retain necessary failures and final comparisons, not recordings
of every passing step. Browser-policy or sandbox denial blocks the operation; do not
switch identities, disable protections or substitute synthetic success.

## Output and completion

Return the existing test result contract with the frozen inventory, script/config
references, command and exit, actual browser/runner, case outcomes, necessary native
reports/traces, cleanup state and unresolved layers. Explicitly state whether the
first real E2E ran, and whether it included the real backend/persistence boundary.
Planning, script generation, installation, live execution and acceptance are distinct
claims. When runtime is blocked, hand off the smallest executable next step without
calling the integration complete.
