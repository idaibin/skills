# Skill Live Canary Summary

## Basis

- Digest scope: all 17 packages declared by `skills-index.json` from the current source
  checkout; the index is the package-set authority.
- Package digest: `sha256:128b6a698ff699042497067b020af2371f5fac00a4b1193db48c2ef783a49bf2`
- Change focus: synchronized frontend CSS and OpenAPI governance, self-contained thin
  adapters for implementation/audit/review owners, frontend contract-consumer audit,
  browser-native recording, desktop-client cancellation recovery plus application
  presence evidence boundaries, and functional entrypoint splits for browser routing,
  tab lifecycle, and repository-review profiles/integration.
- Raw project paths, user data, provider sessions, and task transcripts are excluded.

This summary is bounded to the commands and synthetic cases below. A changed package
digest invalidates it until the same scope is revalidated and this record is refreshed.

## Current Results

| Gate | Result | Evidence boundary |
| --- | --- | --- |
| Package structure | Pass | `scripts/validate-skills.py` validates all 17 packages and their direct reference links. |
| Shared protocol parity | Pass | `scripts/sync-shared-protocols.py --check` confirms CSS, OpenAPI, visual-evidence, and other generated Skill copies match their protocol sources. |
| Focused regressions | Pass | 90 focused unit cases cover browser recording, tab/backend contracts, Skill routing, repository-review contracts, implementation, UI/document authority, review closure, and frontend visual evidence. |
| Entrypoint context budget | Pass | All 17 Skill entrypoints are below the 4,000-token warning threshold; `ops-browser` estimates 3,394 and `repo-review` 3,239. |
| Project-owned UI activation | Pass, static | Evals require the adoption profile only for shared component, third-party adapter, structured token, Registry, or adoption-record changes; ordinary feature composition and unadopted projects remain outside the profile. |
| Authority separation | Pass, static | Evals keep `DESIGN.md`, Feature Specs, component source/types, Registry projections, generated token outputs, and runtime evidence in distinct owners. |
| Negative governance behavior | Pass, static | Contracts require project-native failures for restricted-import bypass, stale Registry/source/public imports, token cycles/bypass/self-reference, and generated drift. Target-project execution remains separate evidence. |
| Visual metric boundary | Pass, static | Shared protocol states that RMSE, pixel similarity, and perceptual distance are diagnostic only and cannot replace state, accessibility, computed-style, or geometry evidence. |
| Independent forward review | Pass, static | A read-only reviewer exercised adopted implementation, unadopted composition, fixed-basis governance review, and low-RMSE/incomplete-runtime scenarios; no actionable findings. This is not live host/model execution proof. |
| Final catalog gate | Pass | `bash scripts/check-skills.sh` passed 422 unit regressions, 57/57 routing cases, protocol parity, context checks, package validation, and the remaining catalog gates on this Worktree. |
| Live-Agent behavior | Not rerun | No current-digest host/model invocation was executed; static Skill and Eval results do not prove model behavior. |
| Browser or desktop runtime | Not rerun for ops changes | Prior project-bounded portal consumer evidence does not verify browser-native recording or desktop cancellation recovery in the current change. |
| Global package install | Not rerun | The current source digest was not installed globally; source-repository upgrade and installed-copy mutation remain separate scopes. |
| Installed-copy parity | Not rerun | Current-digest parity against the global installed packages was not claimed because no current-digest install was performed. |

## Sanitized Scenario Ledger

| Case | Expected behavior | Current result |
| --- | --- | --- |
| `adopted-ui-implementation` | `dev-frontend` reads adoption/source owners, preserves public imports and token direction, and runs project-native gates. | Static contract pass; live Agent not rerun. |
| `unadopted-feature-change` | Ordinary feature composition does not require Registry or structured tokens. | Static contract pass; live Agent not rerun. |
| `adopted-ui-audit` | `audit-frontend` compares adoption/Registry/generated projections with live source and remains read-only. | Static contract pass; live Agent not rerun. |
| `adopted-ui-review` | `repo-review` rejects marker-only proof and checks native negative fixtures on the selected basis. | Static contract pass; live Agent not rerun. |
| `page-contract-separation` | `ui-spec` keeps page states/composition separate from component APIs, Registry, and token values. | Static contract pass; live Agent not rerun. |
| `visual-aggregate-metric` | RMSE or pixel similarity remains diagnostic and cannot independently establish visual completion. | Shared-protocol regression pass; browser not rerun. |

## Verdict

The current source packages contain the intended conditional governance; focused and
final catalog regressions pass. Live-Agent behavior, browser-native recording, desktop
cancellation recovery, current-digest global installation, all-package installed-copy
parity, deployment, and production behavior remain `Not verified` as listed above.
