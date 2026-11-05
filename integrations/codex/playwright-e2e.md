# Project-local Playwright Test Agents

## Ownership and prerequisites

This optional integration uses Playwright's own Planner/Generator/Healer definitions.
Do not vendor copies, create extra public Skills, or rewrite personal Codex settings.
`dev-tests` owns coverage/acceptance, `dev-frontend` owns frontend journey scripts,
the applicable source owner owns runner changes, and `ops-browser` owns live page
operations. Official agent names do not transfer permissions or business authority.

Resolve the authorized test workspace, its current worktree, locked Playwright
package, existing runner/config/fixtures, seed/auth state, target URL and isolated
data before installation. Preserve the application/test repository boundary required
by the project. This is not permission to initialize agents in every application.

## Prepare and verify

Use the existing package manager's locally installed CLI, not an unpinned `npx`
download. Example for a workspace exposing a local npm-compatible binary:

```bash
./node_modules/.bin/playwright --version
./node_modules/.bin/playwright init-agents --help
./node_modules/.bin/playwright init-agents --loop=codex
```

Check the actual version against the lockfile and the advertised loop support first.
Run generation in an authorized clean staging copy when existing agent/configuration
files could be overwritten. Inspect the actual generated paths and complete diff;
promote only intended files after reconciling local customizations. Do not assume
that upstream always writes the same directories or creates a working host connection.
Regenerate/review after an authorized Playwright update; do not overwrite personal
model choices, permissions, sessions, secrets or unrelated configuration.

Use the existing Codex host's documented discovery/reload mechanism and verify the
agent/tools are visible in the current session. No forced new session is required
when the host can reload. Installed bytes are not loaded-agent or successful-run proof.
If the host/CLI/version is unavailable, report that boundary without silent fallback.

## Use the integration

Provide one bounded task and application/test basis. For existing projects, default
to deriving the case inventory from current source, interfaces, existing tests and
available live behavior; a complete PRD or reconstructed spec is not a prerequisite.
Use available confirmed rules first, label baselines/inferences, and freeze the plan
before generation/execution. The same host may perform the roles sequentially;
separate agents are optional.

> Explore only the authorized target and test data using the existing seed fixtures.
> Infer scoped cases from current code and real observations without waiting for a PRD.
> Preserve confirmed rules; label baseline/inferred expectations and freeze their IDs
> and outcomes before execution. Never copy an actual result into its expected value.
> Explore conflicting or unverifiable business meaning within budget, then record the
> evidence, affected IDs and precise question for later human confirmation. Continue
> independent cases; withhold only dependent business verdicts or unsafe operations.
> Generate executable tests using the existing runner and test-asset location.
> Run the selected native suite and preserve the command, exit and raw report.
> Classify failures before repair; change only authorized tests or business source.
> Never skip, fixme, mark expected failure, drop cases, weaken assertions or rebaseline
> visual differences to make a required case pass. Stop on policy/sandbox denial.
> Return case-by-case results, expectation sources, pending human decisions, actual
> evidence, blockers and unexecuted layers. A green baseline is not business approval.

Adopt `forbidOnly: true`, zero acceptance retries, JSON reporting, failure-only
screenshots and `trace: 'retain-on-failure'` where they fit the existing configuration.
Keep the original runner exit status. Retain prior failures; protect authentication
state and traces from public commits/uploads. Do not add a new report dashboard.

For Forgeway consumers, use its current fixed-revision AI E2E standard and existing
Evidence/Attempt binding. Its optional native report checker receives the independent
case/project inventory and exact runner version; generated reports never self-approve.
Without Forgeway, the project's existing trusted verifier owns the same reconciliation.
The portable Skills do not depend on this integration or import Forgeway internals.

## Qualification before adoption

On a fixed task, demonstrate planning -> generated source -> real browser execution
-> native report reconciliation, including a rejected healed skip and missing case.
Record source/test/config versions, the actual host/runner/browser and data boundary.
Use the repository's full applicable checks and live-Agent cases before final
acceptance. Static route checks or a synthetic report fixture prove neither the host
loop nor the business journey. Until those layers run, installation/adoption remains
`Not verified`; a source branch alone is not an installed update.

## Official sources inspected

Playwright, `https://playwright.dev/docs/test-agents`, ref: live documentation,
inspected 2026-11-05. The page documents `init-agents --loop=codex`, seed tests,
Planner/Generator/Healer and the possibility of a healer-produced skipped test.
Playwright, `https://playwright.dev/docs/best-practices`, ref: live documentation,
inspected 2026-11-05. These sources establish the documented method, not compatibility
or installed state of a particular local dependency or Codex session.
