# Skill Live Canary Summary

## Basis

- Scope: `ui-spec`, `dev-frontend`, `audit-frontend`, `repo-review`, and
  `ops-browser` from one current Worktree snapshot.
- Package digest: `sha256:216338fa56639e1606977222a12327d76910c40f5d67705acdee2e0e9467d4f3`
- Host environment: Codex desktop task; local Volta CLI check: `0.146.0`;
  fresh external model sessions were not authorized for this digest.
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
| Catalog discovery | Pass | `npx skills@latest add ./skills --list` validated the local publishable source and found exactly 16 packages. |
| Isolated project-local install | Not verified | The five scoped packages were not installed into a disposable project for this digest. |
| Installed-copy parity | Not verified | No installed-copy comparison was accepted for this digest. |
| Installed package-local validator | Not verified | Installed package validators were not rerun for this digest. |
| Explicit host invocation | Not verified | No fresh host-routing model invocation was run for this digest. |
| Implicit routing | Not verified | No fresh host-routing model invocation was run for this digest. |
| Critical stop routing | Not verified | No fresh host-routing model invocation was run for this digest. |
| Browser capability stop gate | Not verified | No fresh host invocation was run for this digest. |
| Browser two-pass visual closure | Not verified | No fresh browser visual canary was run for this digest. |

## Sanitized Scenario Ledger

| Case | Trigger shape | Expected owner or stop | Result |
| --- | --- | --- | --- |
| `explicit-owner-01` | Explicitly load the five scoped packages and state each boundary. | All five owners visible and distinct. | Not verified |
| `implicit-spec-01` | Approved visual source to implementation-ready contract, no code edit; unapproved-source stop variant. | `ui-spec`; unapproved source is `Not Ready`. | Not verified |
| `implicit-dev-01` | Implement an accepted frontend contract; unresolved `spec-ready` and viewport stop variant. | `dev-frontend`; unresolved evidence stops before editing as `Partial` / `Not Ready`. | Not verified |
| `implicit-audit-01` | Read-only current-surface audit without a change basis; exact-spacing claim without runtime evidence. | `audit-frontend`; exact rendered spacing is `Not verified`. | Not verified |
| `implicit-review-01` | Read-only Standards and Spec review of Worktree changes; fixed-revision conclusion without an immutable basis. | `repo-review`; fixed-basis conclusion stops until the basis is established. | Not verified |
| `implicit-browser-01` | Direct page capture plus runtime geometry and computed styles. | `ops-browser` | Not verified |
| `neighbor-owner-01` | Decide unresolved product behavior and stage/commit/push reviewed changes. | Unavailable `product-spec` and `repo-delivery`; none of the five scoped Skills overclaims ownership. | Not verified |
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

No fresh host-routing model canary was run for this digest. Re-run explicit and
implicit routing after authorization, host catalog changes, or global installation
updates.

## External Security Provider Compatibility

This is a separate compatibility probe, not part of the five-package digest. Static
contract inspection confirms the intended split: ordinary security-sensitive change
review stays in `repo-review`; a security-only Git diff review/scan, repository/path
scan, or named-finding validation belongs to the matching host security workflow;
completed provider evidence may return to `repo-review` for a broader verdict.

Live provider routing was intentionally excluded from this isolated five-package run.
Treat automatic provider discovery in a larger host catalog as `Not verified` for
this basis; explicitly invoke or verify the selected provider before claiming scan
coverage. Do not compensate by embedding a partial scanner in `repo-review`,
`audit-frontend`, `audit-java`, or `audit-rust`.

## Verdict

Repository validation and local catalog discovery pass. Isolated installation,
installed-copy parity and validators, model routing, and browser behavior remain
`Not verified` for this digest; the overall live behavior verdict is `Not verified`.
