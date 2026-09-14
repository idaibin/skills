# Skill Live Canary Summary

## Basis

- Digest scope: all 16 packages declared by `skills-index.json` from the current source
  checkout; the index is the package-set authority.
- Package digest: `sha256:12c05e99da0bd28c747e1b8604c86c889396c943e76fee6b09dbb2ad6970a974`
- Change focus: the durable `to-task` task-ledger owner, consolidation of the three
  audit owners into the single read-only `repo-audit` owner with frontend, Java, and
  Rust language profiles, the shared Code Quality protocol gaining the async failure
  and defensive-catching rules sourced only from `protocols/code-quality-v1.md`, the
  retired-owner closure across current contracts and shared protocols, and the
  routing-baseline retirement migration for rerouted boundary cases, and the
  to-task separated task-ledger authority contract (definition/active/archive/
  evidence roles, active-ledger-only reconciliation, authorized atomic reopen).
- Raw project paths, user data, provider sessions, and task transcripts are excluded.

This summary is bounded to the commands and synthetic cases below. A changed package
digest invalidates it until the same scope is revalidated and this record is refreshed.

## Current Results

| Gate | Result | Evidence boundary |
| --- | --- | --- |
| Package structure | Pass | `scripts/validate-skills.py` validates all 16 packages and their direct reference links. |
| Shared protocol parity | Pass | `scripts/sync-shared-protocols.py --check` confirms CSS, OpenAPI, visual-evidence, code-quality, project-grounding, and other generated Skill copies match their protocol sources. |
| Focused regressions | Pass | All 427 unit cases pass. |
| Entrypoint context budget | Pass | All 16 Skill entrypoints are below the 4,000-token warning threshold. |
| Deterministic routing matrix | Pass | 56/56 routing cases pass with 0 contract errors, including the consolidated `repo-audit` language profiles, its three capability IDs, and the three reroute cases on new stable IDs. |
| Routing baseline (immutable origin/main authority) | Pass | `scripts/run-skill-routing-evals.py --baseline-ref <merge-base with origin/main>` reports 0 regressions: retired owners exit through the extended retirement rule (case `skill` or `observed_owner` absent from both the current catalog and the candidate baseline); the three rerouted boundary cases migrated to `repo-review-audit-reroute`, `dev-java-audit-reroute`, and `dev-rust-audit-reroute` without modifying any existing case definition. |
| Stale-owner closure | Pass | `scripts/test_public_content_hygiene.py` rejects retired audit-owner mentions (including wildcard forms, with replacement-ID boundary guards) across active Skills, protocols, routing cases, and current validation docs. |
| Final catalog gate | Pass | `bash scripts/check-skills.sh` exits 0 against the immutable `origin/main` baseline authority: protocol parity, package validation, routing matrix plus baseline, context checks, design-md regressions, 427 unit tests, and `git diff --check` all pass. |
| Live-Agent behavior | Pass | 14/14 task-local live cases pass on the current Worktree catalog digest (round-2 fresh runs): repo-audit language-profile selection and read-only/contamination behavior match the retired owners under identical prompt/model/reasoning, implementation requests route to `dev-frontend`, `scope-ambiguous` stops; to-task covers single atomic ledger transactions with Ready-frontier, nearest-owner, and `basis-drift` stops, plus the separated four-authority ledger (active-ledger-only reconciliation, verified first against the unmodified package) and the authorized atomic archive reopen. Evidence: `eval-results/live-repoaudit-totask-20260911-063320/` (traces, diffs, Git evidence, results, summary); the run manifest's candidate canonical package digest equals the canary digest above, and the shell-command Git-write classifier is covered by a dedicated regression test. |
| Browser or desktop runtime | Not verified | No browser or desktop-client runtime evidence was collected for this change. |
| Independent provider/model | Not verified | All live runs used one local model; no independent provider result was required or captured. |
| Global package install | Not verified | The current source digest was not installed globally; the installed copy still contains the retired owners and pre-async-rule code-quality copies until an authorized reinstall. |
| Installed-copy parity | Not verified | See above; source-repository upgrade and installed-copy mutation remain separate, authorization-gated scopes. |

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
| `async-defensive-catching` | Shared code-quality protocol gates defensive `try/catch` on the real failure channel; generated copies match the protocol source. | Shared-protocol regression pass; language runtimes not rerun. |
| `visual-aggregate-metric` | RMSE or pixel similarity remains diagnostic and cannot independently establish visual completion. | Shared-protocol regression pass; browser not rerun. |

## Verdict

The current source packages contain the intended conditional governance; the final
catalog gate exits 0 against the immutable baseline authority, and the consolidated
owners pass the task-local live-Agent matrix. Browser/desktop runtime, independent
provider evidence, current-digest global installation, all-package installed-copy
parity, deployment, and production behavior remain `Not verified` as listed above.
