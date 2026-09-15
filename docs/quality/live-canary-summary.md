# Skill Live Canary Summary

## Basis

- Digest scope: all 16 packages declared by `skills-index.json` from the current source
  checkout; the index is the package-set authority.
- Package digest: `sha256:6b334d5fed5ae8a0ee20b0ca557b2f50a2754c0f1fc00d404205f5fcc2c99eca`
- Change focus: shared Skill guidance adds context-pointer, environment-authority,
  hard/soft-dependency, and positive-target rules; `dev-frontend` adds evidence-based
  change distribution and deletion tests; `to-task` adds expand-contract slicing;
  `product-spec`, `ui-spec`, and `to-task` expose prerequisite-complete decisions through an available
  native choice control with a scoped fallback; `ask-ai` no longer advertises a retired
  package name; and `repo-delivery` no longer ships an unreferenced mutation helper.
- Raw project paths, user data, provider sessions, and task transcripts are excluded.

This summary is bounded to the commands and synthetic cases below. A changed package
digest invalidates it until the same scope is revalidated and this record is refreshed.

## Current Results

| Gate | Result | Evidence boundary |
| --- | --- | --- |
| Package structure | Pass | `scripts/validate-skills.py` validates all 16 packages and their direct reference links. |
| Shared protocol parity | Pass | `scripts/sync-shared-protocols.py --check` confirms CSS, OpenAPI, visual-evidence, code-quality, project-grounding, and other generated Skill copies match their protocol sources. |
| Focused regressions | Pass | All 449 unit methods pass; same-contract syntax variants run as named subtests. |
| Entrypoint context budget | Pass | All 16 Skill entrypoints are below the 2,000-token warning threshold; current estimates range from 365 to 1,297 tokens. |
| Deterministic routing matrix | Pass | 56/56 routing cases pass with 0 contract errors, including the consolidated `repo-audit` language profiles, its three capability IDs, and the three reroute cases on new stable IDs. |
| Routing baseline (immutable origin/main authority) | Pass | `scripts/run-skill-routing-evals.py --baseline-ref <merge-base with origin/main>` reports 0 regressions: retired owners exit through the extended retirement rule (case `skill` or `observed_owner` absent from both the current catalog and the candidate baseline); the three rerouted boundary cases migrated to `repo-review-audit-reroute`, `dev-java-audit-reroute`, and `dev-rust-audit-reroute` without modifying any existing case definition. |
| Stale-owner closure | Pass | `scripts/test_public_content_hygiene.py` rejects retired audit-owner mentions (including wildcard forms, with replacement-ID boundary guards) across active Skills, protocols, routing cases, and current validation docs. |
| Final catalog gate | Pass | `bash scripts/check-skills.sh` exits 0 against the immutable `origin/main` baseline authority: protocol parity, package validation, routing matrix plus baseline, context checks, focused regressions, and `git diff --check` all pass. |
| Live-Agent behavior | Partial | Five of six selected current-digest cases pass. `to-task` routing, nearest-owner, and critical-stop pass 3/3; `dev-frontend` nearest-owner and critical-stop pass, while the implementation case completed the source/check outcome but failed twice to capture required pre-write owner-symbol evidence, so it remains failed and was not retried again. Decomposition-specific and expand-contract execution, other packages, unselected cases, and the independent-provider case are `Not verified` for this digest. |
| Native structured choice | Not verified | The non-interactive Default-mode runner does not expose the host-native choice control; deterministic contracts cover the selection/fallback rule, not rendered Plan-mode UI. |
| Browser or desktop runtime | Not verified | No browser or desktop-client runtime evidence was collected for this change. |
| Independent provider/model | Not verified | All live runs used one local model; no independent provider result was required or captured. |
| Global package install | Not verified | The current source digest was not installed globally. |
| Installed-copy parity | Not verified | Source and installed copies were not compared for this source digest; installation remains separately authorization-gated. |

## Sanitized Scenario Ledger

| Case | Expected behavior | Current result |
| --- | --- | --- |
| `dev-frontend` selected set | Implement the bounded source/test change with focused evidence, route an implementation-not-ready UI contract to `ui-spec`, and stop without source-write authorization. | 2/3 passed. Both implementation attempts made the correct bounded source/test change and ran the focused check, but neither captured the required pre-write owner-symbol evidence; retry stopped after the second same-item failure. |
| `to-task` selected set | Maintain the accepted ledger, route unresolved owner decisions, and stop on incomplete authority. | 3/3 passed in 3/1/1 tool calls with zero source, Git, or external effects. |

## Verdict

The current source packages contain the repaired boundaries and the final catalog gate
exits 0 against the immutable baseline authority. Five of six selected current-digest
behaviors pass; the repeated `dev-frontend` owner-evidence failure remains open.
Decomposition-specific and expand-contract live execution, native structured-choice
rendering, other packages, all unselected live cases, global installation/parity,
browser/desktop runtime, independent-provider evidence, deployment, and production
behavior remain `Not verified` as listed above.
