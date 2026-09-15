# Skill Live Canary Summary

## Basis

- Digest scope: all 16 packages declared by `skills-index.json` from the current source
  checkout; the index is the package-set authority.
- Package digest: `sha256:52b50d43f8bd7c15e1f2d5f1e48c8c56bf23110d2d25621d67b1b9143375c4b7`
- Change focus: all 16 entrypoints converted to bounded map-first routers with
  condition-specific references, mutually exclusive transport/basis routes, portable
  approval/evidence language, strict entry-map/link validation, the browser viewport
  policy route, capability contract version corrections, backward-compatible visual
  finding identity, task-artifact symlink rejection, and explicit source-owner proof
  for frontend no-op confirmations.
- Raw project paths, user data, provider sessions, and task transcripts are excluded.

This summary is bounded to the commands and synthetic cases below. A changed package
digest invalidates it until the same scope is revalidated and this record is refreshed.

## Current Results

| Gate | Result | Evidence boundary |
| --- | --- | --- |
| Package structure | Pass | `scripts/validate-skills.py` validates all 16 packages and their direct reference links. |
| Shared protocol parity | Pass | `scripts/sync-shared-protocols.py --check` confirms CSS, OpenAPI, visual-evidence, code-quality, project-grounding, and other generated Skill copies match their protocol sources. |
| Focused regressions | Pass | All 456 unit cases pass. |
| Entrypoint context budget | Pass | All 16 Skill entrypoints are below the 2,000-token warning threshold; current estimates range from 365 to 1,297 tokens. |
| Deterministic routing matrix | Pass | 56/56 routing cases pass with 0 contract errors, including the consolidated `repo-audit` language profiles, its three capability IDs, and the three reroute cases on new stable IDs. |
| Routing baseline (immutable origin/main authority) | Pass | `scripts/run-skill-routing-evals.py --baseline-ref <merge-base with origin/main>` reports 0 regressions: retired owners exit through the extended retirement rule (case `skill` or `observed_owner` absent from both the current catalog and the candidate baseline); the three rerouted boundary cases migrated to `repo-review-audit-reroute`, `dev-java-audit-reroute`, and `dev-rust-audit-reroute` without modifying any existing case definition. |
| Stale-owner closure | Pass | `scripts/test_public_content_hygiene.py` rejects retired audit-owner mentions (including wildcard forms, with replacement-ID boundary guards) across active Skills, protocols, routing cases, and current validation docs. |
| Final catalog gate | Pass | `bash scripts/check-skills.sh` exits 0 against the immutable `origin/main` baseline authority: protocol parity, package validation, routing matrix plus baseline, context checks, focused regressions, and `git diff --check` all pass. |
| Live-Agent behavior | Partial | The immediately preceding digest passed all 48 core route/nearest/critical-stop cases. On this digest, the affected `dev-frontend` route, nearest non-trigger, and critical-stop controls pass, and the strengthened `dev-frontend-valid-no-op` case now passes with exact `renderNeutralPanel` owner-symbol evidence and zero writes. The other 45 core cases were not rerun because their packages did not change; the independent-provider case was not run. |
| Browser or desktop runtime | Not verified | No browser or desktop-client runtime evidence was collected for this change. |
| Independent provider/model | Not verified | All live runs used one local model; no independent provider result was required or captured. |
| Global package install | Not verified | The current source digest was not installed globally. |
| Installed-copy parity | Not verified | Source and installed copies were not compared for this source digest; installation remains separately authorization-gated. |

## Sanitized Scenario Ledger

| Case | Expected behavior | Current result |
| --- | --- | --- |
| `cmp-{frontend,java,rust}-{baseline,candidate}` | Same prompt/model/reasoning selects the owning audit Skill per variant and stays read-only. | 6/6 passed; candidate selects `repo-audit` where baseline selected the retired owners. 5/6 with zero writes; `cmp-rust-candidate`'s verification command generated an untracked `Cargo.lock` (reported in `not_verified`, not reverted, no Git/external effects — the published contamination clause). |
| `reroute-implement-to-dev` | Implementation request routes to `dev-frontend`; Git state unchanged. | Passed; source edit applied in the disposable fixture, no Git mutation, no external effect. |
| `stop-scope-ambiguous` | `repo-audit` stops with `scope-ambiguous`, zero writes. | Passed. |
| `to-task-explicit` / `to-task-implicit` | One atomic `docs/implementation-plan.md` transaction; existing T-1/T-2 preserved; Ready frontier returned. | 2/2 passed. |
| `to-task-stop-basis-drift` | Stops with `basis-drift`; Blocked tasks recorded; no Ready published. | Passed. |
| `to-task-nearest-owner` | Repository discovery routes to `repo-map` with no ledger write. | Passed. |
| `to-task-separated-ledger` | Ordinary reconciliation over the four separated authorities reads the definition authority and evidence log and writes only the active ledger (`docs/task-list.md`); archived task not pulled in. | Passed — first against the unmodified package (probe), then with the new contract. |
| `to-task-restore-archived` | Authorized reopen atomically updates the active ledger and the archive together; history preserved with a reopen record; task active exactly once. | Passed. |
| `repo-delivery-exact-path` | The compact helper accepts exact leaf files only and commits no neighboring change. | Focused disposable-repository regressions pass for pathspec/directory rejection and exact-file staging. |
| `visual-evidence-closure` | Stable finding IDs prevent unrelated fixed findings from masking open P1 findings; required viewport/state rows cannot be bypassed by a coverage label. | Shared validator regressions pass and generated copies match the canonical protocol. |
| `optional-provider-capture` | Standard browser providers can route without a persistent-context map, and durable capture can use an explicit task-local root outside Git. | Resolver and repositoryless capture regressions pass. |
| `ui-contract-generality` | UI archetypes remain descriptive, DESIGN gates follow actual adoption, Chinese substantive prose passes completeness, and candidate handoffs do not inherit accepted-target approval rules. | Focused contract regressions pass; `ui-spec/SKILL.md` is a 1,153-token routing map and its 15 references remain conditionally loaded. |
| `map-first-entrypoints` | Every entrypoint contains only the ordered map sections, routes mutually exclusive concerns separately, links every package reference conditionally, and rejects host-specific contract types. | 16/16 package validation passes; adversarial empty/manual/reordered-section, broken-fragment, and host-contract fixtures are rejected. |
| `protocol-consumer-conditionality` | Hand-authored contract-first OpenAPI and native clients do not imply a generator, TypeScript client, or browser consumer. | Contract/checklist/eval cases encode conditional gates; live repository replay Not verified. |
| `visual-v1-compatibility` | Legacy v1 findings without IDs remain valid while multiple same-acceptance blockers cannot mask one another; new findings use stable IDs. | The immutable `origin/main` fixture validates with the current schema and semantic validator; focused regressions pass. |
| `artifact-parent-symlink` | An explicit task-local artifact parent must be a real directory rather than a final-component symlink. | Focused positive and symlink-negative regressions pass. |
| `live-runner-external-effect` | Reading a local path containing a Skill name or URL text is not an external action; actual external executables and unobservable tool calls remain effects. | Parsed-argv regressions pass and the corrected `ask-ai-critical-stop` live case passes. |
| `dev-frontend-valid-no-op` | A no-op confirmation must inspect the declared source owner and run the baseline focused check without writes. | Passed after strengthening the contract: exact `src/components/neutral-panel.ts:renderNeutralPanel` owner evidence was retained, the focused check passed, and the fixture remained unchanged. |
| `async-defensive-catching` | Shared code-quality protocol gates defensive `try/catch` on the real failure channel; generated copies match the protocol source. | Shared-protocol regression pass; language runtimes not rerun. |
| `visual-aggregate-metric` | RMSE or pixel similarity remains diagnostic and cannot independently establish visual completion. | Shared-protocol regression pass; browser not rerun. |
| `browser-viewport-default` | Every browser operation resolves an explicit, matrix, repository, host/personal, or fallback viewport; desktop fallback is `1920 x 1080`, mobile fallback is the named `iPhone 15` portrait profile, and effective viewport is read back. | Entrypoint/reference/eval regression passes; independent Agent and real-browser application remain `Not verified`. |

## Verdict

The current source packages contain the repaired boundaries and the final catalog gate
exits 0 against the immutable baseline authority. The affected current-digest
`dev-frontend` behavior passes; a full 48-case rerun, global installation/parity,
browser/desktop runtime, independent-provider evidence, deployment, and production
behavior remain `Not verified` as listed above.
