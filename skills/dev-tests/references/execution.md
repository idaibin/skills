# Existing-check execution

Match verification to the stage and change impact. During iteration, run focused checks
and necessary adjacent regressions; a wording edit, isolated logic fix and cross-module
change need different scope. Before final submission/commit, require the complete
applicable project gate on the assembled final basis. Before an authorized merge,
verify the actual integration candidate through its applicable integration gate. Reuse
unchanged evidence only with a basis/impact rationale and when project rules permit;
“complete” neither means every unrelated suite nor waives required blocked gates.
Return these gate results to `repo-delivery`; testing grants no commit or merge authority.

1. Resolve commands from the current repository configuration and instructions. Inspect
   scripts, setup, dependency/runtime versions and likely side effects before execution.
   Establish target revision and artifact destinations. Installation or environment
   changes require their own authority; never silently acquire credentials or expand access.
2. Select the smallest reproducible run that can falsify the acceptance claim, followed
   by affected regression checks. Record oracle, prerequisites, fixtures, seed/time
   controls, real and substituted dependencies, and expected cleanup before running.
   Preserve a versioned pre-run plan/oracle snapshot for acceptance or comparative
   claims; bind its identity to results and record later changes instead of rewriting
   the original expectation. Reuse project evidence storage, not a second ledger.
3. Run only authorized existing checks. Prefer isolated disposable test data/resources;
   an “integration” label does not make a destructive or external effect safe. A browser
   or native-client step transfers the scenario and oracle to its operations owner under
   the same permission boundary. If that owner/capability is unavailable, block that row.
4. Capture exact command or interaction recipe, working directory, runtime/build and
   dependency versions, start/end times, exit code, relevant assertions and artifact
   locations/digests. Scrub credentials and sensitive records from shareable evidence.
   Verify the observed application/process corresponds to the frozen target.
5. On failure distinguish assertion/product failure, harness failure and unmet environment
   prerequisite. Preserve the first failure and a minimal reproducible sequence. A failed
   assertion is `failed`; inability to exercise it is `blocked`. Never count missing
   assertions, zero discovered tests or truncated output as passing.
6. Retry only a diagnosed recoverable cause within the original authority and bounded
   resource/time budget. Keep each attempt and intervening change visible. A green retry
   does not erase a flake; unresolved nondeterminism remains an acceptance gap. Route
   source/test/harness fixes to their implementation owner, then rerun on the new basis.
7. Verify cleanup and residual processes/resources for each run. Stop at the declared
   acceptance scope or a named prerequisite/authorization blocker; return incomplete
   dependent claims rather than cycling through alternate denied execution paths.

Do not modify tests to match observed behavior when it contradicts accepted requirements.
When no relevant existing test exists, return the missing assertion and owner; a manual
observation may support only what it actually checks, not pretend automated coverage.
Unit, contract, integration, UI and E2E results retain their individual evidence levels.
