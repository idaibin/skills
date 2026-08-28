# Skill Live Canary Summary

## Basis

- Digest scope: `ui-spec`, `ask-ai`, `dev-frontend`, `audit-frontend`,
  `repo-review`, and `ops-browser` from the current source checkout.
- Package digest: `sha256:bde5a0567ec6f7dc7285f44118e629822542a342621f1e5183981c5417aae10a`
- Change focus: conditional project-owned UI component and Design Token governance,
  project-native negative gates, and aggregate-image metrics as diagnostic evidence.
- Raw project paths, user data, provider sessions, and task transcripts are excluded.

This summary is bounded to the commands and synthetic cases below. A changed package
digest invalidates it until the same scope is revalidated and this record is refreshed.

## Current Results

| Gate | Result | Evidence boundary |
| --- | --- | --- |
| Package structure | Pass | `scripts/validate-skills.py` validates all 17 packages; `quick_validate.py` passes for the five changed/generated package surfaces. |
| Shared protocol parity | Pass | `scripts/sync-shared-protocols.py --check` confirms the visual-evidence protocol and generated Skill copies are identical. |
| Focused governance regressions | Pass | 70 focused unit cases cover implementation, UI/document authority, review closure, and frontend visual evidence. |
| Project-owned UI activation | Pass, static | Evals require the adoption profile only for shared component, third-party adapter, structured token, Registry, or adoption-record changes; ordinary feature composition and unadopted projects remain outside the profile. |
| Authority separation | Pass, static | Evals keep `DESIGN.md`, Feature Specs, component source/types, Registry projections, generated token outputs, and runtime evidence in distinct owners. |
| Negative governance behavior | Pass, static | Contracts require project-native failures for restricted-import bypass, stale Registry/source/public imports, token cycles/bypass/self-reference, and generated drift. Target-project execution remains separate evidence. |
| Visual metric boundary | Pass, static | Shared protocol states that RMSE, pixel similarity, and perceptual distance are diagnostic only and cannot replace state, accessibility, computed-style, or geometry evidence. |
| Independent forward review | Pass, static | A read-only reviewer exercised adopted implementation, unadopted composition, fixed-basis governance review, and low-RMSE/incomplete-runtime scenarios; no actionable findings. This is not live host/model execution proof. |
| Final catalog gate | Pass | `bash scripts/check-skills.sh` passed 417 unit regressions, 57/57 routing cases, protocol parity, context checks, package validation, and the remaining catalog gates on this Worktree. |
| Live-Agent behavior | Not rerun | No current-digest host/model invocation was executed; static Skill and Eval results do not prove model behavior. |
| Browser or desktop runtime | Not rerun | No current-digest browser/client operation or selected-source comparison was executed. |
| Global package install | Not performed | Source changes were not installed into the global Skill directory in this task. |
| Installed-copy parity | Not verified | Prior-digest installation parity is historical and is not promoted to this digest. |

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
final catalog regressions pass. Live-Agent behavior, global installation,
installed-copy parity, browser/runtime acceptance, deployment, and production behavior
remain `Not verified` as listed above.
