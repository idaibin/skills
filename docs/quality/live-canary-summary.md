# Skill Live Canary Summary

## Basis

- Scope: `ui-spec`, `dev-frontend`, `audit-frontend`, `repo-review`, and
  `ops-browser` from one current Worktree snapshot.
- Package digest: `sha256:3abec9f36ff0c019e817f8822129f8ebf942202563553bdeafddfa6dcc5e70b9`
- Host environment: Codex desktop task; local CLI check: `0.145.0`; model:
  `gpt-5.6-terra`; fresh, read-only explorer sessions.
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
| Catalog discovery | Pass | The standard Skill CLI validated the local source and listed all 14 packages. |
| Isolated project-local install | Pass | The five scoped packages were copied into a disposable project without a global install. |
| Installed-copy parity | Pass | Recursive comparison found no difference between each installed package and its source package. |
| Installed package-local validator | Pass | All five installed validators ran with isolated standard-library Python against the installed synthetic fixture. |
| Explicit host invocation | Pass | A fresh read-only explorer session loaded all five scoped packages and summarized each package's owner boundary correctly. |
| Implicit routing | Pass | A separate fresh read-only explorer session routed five generic requests to `ui-spec`, `dev-frontend`, `audit-frontend`, `repo-review`, and `ops-browser` respectively, without naming those Skills in the requests. |
| Browser capability stop gate | Pass | A separate fresh read-only explorer session selected `ops-browser`, inspected active capabilities, found no actual browser automation, returned `Not verified`, and made no screenshot, geometry, computed-style, or visual-completion claim. |
| Browser two-pass visual closure | Not verified | The canary host exposed no browser automation supporting local navigation, viewport control, screenshots, DOM geometry, and computed styles. Same-state pass 1 and pass 2 evidence therefore was not produced. |

## Sanitized Scenario Ledger

| Case | Trigger shape | Expected owner or stop | Result |
| --- | --- | --- | --- |
| `explicit-owner-01` | Explicitly load the five scoped packages and state each boundary. | All five owners visible and distinct. | Pass |
| `implicit-spec-01` | Approved visual source to implementation-ready contract, no code edit. | `ui-spec` | Pass |
| `implicit-dev-01` | Implement an accepted frontend contract. | `dev-frontend` | Pass |
| `implicit-audit-01` | Read-only current-surface audit without a change basis. | `audit-frontend` | Pass |
| `implicit-review-01` | Read-only Standards and Spec review of Worktree changes. | `repo-review` | Pass |
| `implicit-browser-01` | Direct page capture plus runtime geometry and computed styles. | `ops-browser` | Pass |
| `browser-stop-01` | Request two same-state passes without an available browser capability. | `Not verified`; no visual/runtime claims. | Pass |

This ledger is intentionally semantic rather than a transcript. It retains no raw
prompt, response, path, account, session identifier, or connector payload. Re-run the
ledger when the package digest, host environment, model, enabled catalog, or browser
capability changes.

## Required Behavior Scenarios

When host invocation is authorized, run each scoped Skill on:

1. a normal trigger;
2. its nearest non-trigger or owner boundary;
3. a critical stop condition.

The routing matrix must distinguish specification, source implementation, bounded
audit, fixed-basis review, and direct browser operation. The end-to-end visual canary
must demonstrate source approval, complete acceptance mapping, two same-viewport/state
passes, computed runtime evidence, browser-state restoration, and an honest
`Partial`/`Not Ready` verdict whenever required evidence is absent.

The host reported that Skill descriptions were shortened to fit its Skill context
budget. All five routing cases still passed in this run, but this is a compatibility
risk when many unrelated Skills or plugins are enabled. Re-run implicit routing after
host catalog changes; disable unrelated packages when routing precision matters.

The host also reported an authentication warning from an unrelated optional
connector. It did not affect package discovery, loading, routing, or the browser
capability stop gate and is not evidence about these Skills.

## Verdict

Distribution, installed package self-containment, explicit loading, implicit routing,
and honest browser capability degradation pass. Actual two-pass browser visual closure
remains `Not verified`; the overall live behavior verdict is `Partial`.
