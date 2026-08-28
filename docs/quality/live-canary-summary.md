# Skill Live Canary Summary

## Basis

- Digest/install-parity scope: `ui-spec`, `ask-ai`, `dev-frontend`,
  `audit-frontend`, `repo-review`, and `ops-browser` from one
  current source-checkout snapshot. Behavior scenarios remain evidence-bounded per row and
  do not imply live invocation of every package in this digest scope.
- Package digest: `sha256:498ef2b1fb393df88d61f46de21b671ba6acb726a06a49801ff25b1e883b68f8`
- Host environment: Codex desktop on macOS. This digest refresh ran offline contract,
  completeness, routing, source-discovery, and disposable synthetic live-Agent checks.
  An explicitly authorized AGY Flash final review ran once against a fixed disposable
  checkout copy. Provider-owned JSONL proved the exact model and conversation, but its
  terminal event was `ERROR` after an invalid artifact-path write; the provider case is
  therefore `Not verified` and was not retried. After focused source validation, the six
  changed public packages were installed from this local catalog into the Codex global
  Skill directory and matched source byte-for-byte, excluding interpreter cache files.
  Live browser operation was not rerun.
- Raw checkout paths, accounts, prompts, session identifiers, and repository refs are
  intentionally omitted from this durable summary.
- Recompute the digest with `python3 scripts/skill-package-digest.py`. A package
  change makes the content-hygiene regression fail until this canary is rerun and the
  summary is updated.

This is evidence only for the commands and scenarios below. It is not catalog-wide
behavior certification and does not replace target-environment runtime validation.

## Current Results

| Gate | Result | Evidence boundary |
| --- | --- | --- |
| Repository package validation | Pass | `bash scripts/check-skills.sh` validates structure, metadata, links, synchronized protocols, the visual-evidence fixture, and current unit regressions. The test count comes from command output and is not copied into this durable record. |
| Disposable live-Agent capability matrix | Partial | On the hardened current runner, explicit source change and missing-authorization early stop passed strict evidence gates. The implicit change completed correctly but did not prove a full current-owner read; the nearest non-trigger produced the correct stop but exceeded its tool budget after an environment preflight failure; the no-op produced the correct baseline result but did not prove complete candidate-Skill loading or owner inspection. The provider case was correctly classified `not-verified`. |
| Catalog discovery | Pass | The installer discovered the current local catalog and selected the six requested packages by exact name. This proves installer discovery, not implicit model routing. |
| Visual-direction contract regression | Pass | Focused offline tests verify conditional dark mode, one primary accent semantic role with independent state colors, Preserve/Overhaul boundaries, contextual layout repetition, and nested inset ownership by axis. This is contract evidence, not model or browser behavior. |
| Documentation-evidence lifecycle regression | Pass | Focused offline tests verify resolved design-root ownership, ignored task-evidence placement, the complete structured-projection lifecycle, and the distinction between locator-only navigation and copied authority. This is static contract evidence, not host-routing or browser proof. |
| DESIGN.md completeness policy | Pass | Official 0.4.0 format lint and `ui-spec-design-completeness/1` regressions distinguish format validity from first-adoption readiness/adoption, bind source and approval record bytes by SHA-256, reject prose-only/token-dump/placeholders/stale approval, and detect concurrent DESIGN.md drift. This is policy evidence, not human approval. |
| Forgeway DESIGN handoff contract | Pass | Offline validator/eval coverage binds `ui.contract.specify@1.1.0` to compatible consumer `forgeway-ui-design-completeness/1`, exact package-relative artifact hashes/byte lengths, and claim `gate:ui-design-complete`; producer status remains `awaiting-trusted-approval-verification`. Real host principal resolution, receipt adapter, and target DESIGN runtime were not exercised. |
| Browser tab-lifecycle contract regression | Pass | Focused offline tests verify identity-first tab selection, explicit retention authority, recoverable task-tab ownership, and representative same-URL/different-session cases. This is static contract evidence, not a live browser canary. |
| Browser backend handoff regression | Pass | Focused offline tests verify shared protocol copy parity, deterministic/agentic/CDP capability fields, action-shape and budget constraints, backend attribution, deterministic-first fixed writes, and the Ask AI provider-adapter links. `test_browser_operation_stability_contract` also covers complete negative evidence for attachment failure and stable-response evidence while keeping a lingering stop control as a separate gap. This is contract evidence, not live browser or provider behavior. |
| Community feature specification | Not rerun | Prior canary evidence is historical and is not promoted to this package digest. |
| Community behavior-first implementation | Not rerun | Prior target-repository test/build evidence is historical and is not promoted to this package digest. |
| Fixed-basis frontend audit and review | Not rerun | No external target Worktree audit was rerun for this digest. |
| Live headless-browser page operation | Not rerun | No browser page operation was run for this digest. |
| Local-browser session/group capability | Partial | Executable regressions cover two browser identities, stale-ID reconnect, stable reuse, duplicate names, label-only ambiguity, missing capabilities, exact create-required transitions, and each enabled-policy combination. No live user-local Chrome inventory or page operation was run. |
| Global package install | Pass | After focused source validation, the six changed packages were installed non-interactively from the validated local catalog for Codex: `ui-spec`, `ask-ai`, `dev-frontend`, `audit-frontend`, `repo-review`, and `ops-browser`. |
| Installed-copy parity | Pass | Recursive source-to-installed comparison passed for those six packages; interpreter cache directories and bytecode were excluded as non-package runtime artifacts. |
| Installed package-local validator | Not verified | The repository validator requires root catalog files that global package installation intentionally does not copy, so it cannot validate the installed directory as a standalone catalog. Source validation and installed-copy parity passed separately. |
| Explicit host invocation | Partial | The fresh explicit change and missing-authorization cases passed. The no-op behavior and focused check were correct, but strict Skill-loading and owner-read provenance were not proven. The AGY result remains `Not verified` because its provider terminal event was `ERROR`. |
| Implicit routing | Partial | Fresh routing selected the correct owners and produced the intended behavior, but the implementation case lacked a full current-owner read and the nearest non-trigger exceeded the fixed efficiency budget after one failed environment preflight. |
| Critical stop routing | Pass | The synthetic missing-source-write-authorization case read the complete candidate Skill, stopped before source inspection or editing, preserved zero source/Git/external effects, and reported `missing-authorization`. This does not prove every critical stop in the catalog. |
| Browser capability stop gate | Pass | Offline executable fixtures fail closed before naming, tab creation, group creation, or page action when stable selection or placement cannot be proven; creation is exposed only as an exact intermediate action followed by mandatory re-enumeration. This is not live Chrome capability evidence. |
| Browser two-pass visual closure | Not verified | The generated image is exploratory evidence awaiting human approval; no frontend implementation or same-state selected-source browser comparison was performed. |

## Sanitized Scenario Ledger

| Case | Trigger shape | Expected owner or stop | Result |
| --- | --- | --- | --- |
| `explicit-owner-01` | Explicitly select the frontend implementation owner for a bounded synthetic change. | `dev-frontend`; source and matching contract change, followed by the focused check. | Pass |
| `implicit-spec-01` | Approved visual source to implementation-ready contract, no code edit; unapproved-source stop variant. | `ui-spec`; unapproved source is `Not Ready`. | Target behavior pass; implicit host routing not verified |
| `implicit-dev-01` | Implement a bounded synthetic frontend change without naming a Skill. | `dev-frontend`; select the real source owner, change only the source and matching test contract, then run the focused check. | Partial: behavior passed; complete owner-read evidence failed |
| `implicit-audit-01` | Read-only current-surface audit without a change basis; exact-spacing claim without runtime evidence. | `audit-frontend`; exact rendered spacing is `Not verified`. | Target behavior pass; implicit host routing not verified |
| `visual-direction-01` | Existing settings redesign with one primary accent semantic role, independent state colors, optional dials, and dark mode only when the accepted contract selects it. | `ui-spec` records Preserve/Overhaul and accepted direction; `dev-frontend` implements; `audit-frontend` stays evidence-bound. | Not verified |
| `nested-inset-01` | Outer content container already owns page inset while a standard inner panel also adds left/top padding and the scrollbar must stay flush right. | Trace shell → container → page → component → control, keep one owner per boundary, and verify effective insets by axis plus shared-owner sibling impact. | Not verified |
| `implicit-review-01` | Read-only Standards and Spec review of Worktree changes; fixed-revision conclusion without an immutable basis. | `repo-review`; fixed-basis conclusion stops until the basis is established. | Target behavior pass; implicit host routing not verified |
| `implicit-browser-01` | Direct page capture plus runtime geometry and computed styles. | `ops-browser` | Partial: in-app provider operation completed; no selected-source frontend visual comparison |
| `neighbor-owner-01` | Decide unresolved product behavior and stage/commit/push reviewed changes. | Unavailable `product-spec` and `repo-delivery`; none of the five scoped Skills overclaims ownership. | Not verified |
| `nearest-negative-01` | Request an implementation-ready selected-source UI specification without source editing. | `ui-spec`; stop `evidence-incomplete` when the selected visual source and acceptance basis are absent. | Partial: owner and stop passed; efficiency budget failed |
| `valid-no-op-01` | Confirm the accepted baseline already holds without changing source. | `dev-frontend`; run the baseline-focused check and preserve a clean diff. | Partial: behavior passed; complete Skill/owner-read evidence failed |
| `authorization-stop-01` | Request a source change while source-write authorization is explicitly absent. | `dev-frontend`; stop before source inspection or editing and report `missing-authorization`. | Pass |
| `provider-review-01` | Require an independent AGY Flash review for the fixed synthetic source diff. | `dev-frontend` plus attributed AGY review evidence; provider identity, immutable basis, and successful provider terminal must match. | Not verified: exact model/session proven; provider terminal was `ERROR` |
| `browser-stop-01` | Request two same-viewport/state passes without an available browser capability. | `ops-browser`; exact viewport, screenshots, DOM geometry, computed styles, responsive states, both passes, and final visual completion are `Not verified`. | Not verified |

This ledger is intentionally semantic rather than a transcript. It retains no raw
prompt, response, path, account, session identifier, or connector payload. Re-run the
ledger when the package digest, host environment, model, enabled catalog, or browser
capability changes.

## Required Behavior Scenarios

When fresh host-routing invocation is authorized and selected, run each scoped Skill on:

1. a normal trigger;
2. its nearest non-trigger or owner boundary;
3. a critical stop condition.

The routing matrix must distinguish specification, source implementation, bounded
audit, fixed-basis review, and direct browser operation. The end-to-end visual canary
must demonstrate source approval, complete acceptance mapping, two same-viewport/state
passes, computed runtime evidence, browser-state restoration, and an honest
`Partial`/`Not Ready` verdict whenever required evidence is absent.

The six current synthetic cases cover the listed `dev-frontend` and nearest-owner
boundaries only. Their partial and failed evidence gates are retained rather than
converted into passes by retry. Rerun only on a new authorized evaluation basis; any
new external-provider operation requires separate authorization.

## External Security Provider Compatibility

This is a separate compatibility probe, not part of the six-package digest. Static
contract inspection confirms the intended split: ordinary security-sensitive change
review stays in `repo-review`; a security-only Git diff review/scan, repository/path
scan, or named-finding validation belongs to the matching host security workflow;
completed provider evidence may return to `repo-review` for a broader verdict.

The current AGY operation reviewed the fixed synthetic Skills evidence basis; it was
not a security-provider discovery or security scan. Treat automatic provider discovery
in a larger host catalog as `Not verified` for this basis; explicitly invoke or verify
the selected provider before claiming scan coverage. Do not compensate by embedding a partial scanner in `repo-review`,
`audit-frontend`, `audit-java`, or `audit-rust`.

## Verdict

Offline repository, DESIGN, Forgeway, live-runner, provider-evidence, Git/effect, and
visual-evidence contracts, the final repository gate, six-package Codex global install,
and installed-copy parity pass. The latest strict live-Agent
matrix is Partial, and the AGY provider case is `Not verified` because its terminal was
`ERROR`; these states are intentionally fail-closed. Live browser/session capability,
catalog-wide routing, real-project
implementation, human visual approval, same-state browser acceptance, accessibility,
deployment, and production behavior remain `Not verified` until separately evidenced.
