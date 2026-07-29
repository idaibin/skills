# Skill Live Canary Summary

## Basis

- Scope: `ui-spec`, `dev-frontend`, `audit-frontend`, `repo-review`, and
  `ops-browser` from one current Worktree snapshot.
- Package digest: `sha256:9f6b2b9c14c0e5d0343c31b56892957a70f29c0cb5334d8040ced333c22af72c`
- Host environment: Codex desktop task; local CLI check: `0.145.0`; model:
  `gpt-5.6-terra`; fresh, ephemeral, read-only CLI sessions.
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
| Catalog discovery | Pass | The standard Skill CLI validated the publishable `skills/` source and listed exactly 14 packages. Repository-root discovery additionally saw one local workspace-only `.agents` Skill, so that broader result is not used as publishable catalog evidence. |
| Isolated project-local install | Pass | The five scoped packages were copied into a disposable project without a global install. |
| Installed-copy parity | Pass | Recursive comparison found no difference between each installed package and its source package. |
| Installed package-local validator | Pass | All five installed validators ran with isolated standard-library Python against the installed synthetic fixture. |
| Explicit host invocation | Pass | A fresh ephemeral read-only CLI session loaded only the five project-installed copies, read every `SKILL.md`, and distinguished normal triggers, nearest non-triggers, neighboring owners, and critical stop verdicts. |
| Implicit routing | Pass | A separate fresh ephemeral read-only CLI session classified normal, neighboring-owner, and critical-stop requests without Skill names. It kept specification, implementation, bounded audit, fixed-basis review, direct browser evidence, built-in diagnosis, visual exploration, and unavailable Git delivery distinct. |
| Browser capability stop gate | Pass | A separate fresh ephemeral read-only CLI session selected `ops-browser` for a 1920 x 1080 two-pass capture request, found no actual browser automation, returned `Not verified`, and made no viewport, screenshot, geometry, computed-style, or visual-completion claim. |
| Browser two-pass visual closure | Not verified | The canary host exposed no browser automation supporting local navigation, viewport control, screenshots, DOM geometry, and computed styles. Same-state pass 1 and pass 2 evidence therefore was not produced. |

## Sanitized Scenario Ledger

| Case | Trigger shape | Expected owner or stop | Result |
| --- | --- | --- | --- |
| `explicit-owner-01` | Explicitly load the five scoped packages and state each boundary. | All five owners visible and distinct. | Pass |
| `implicit-spec-01` | Approved visual source to implementation-ready contract, no code edit; unapproved-source stop variant. | `ui-spec`; unapproved source is `Not Ready`. | Pass |
| `implicit-dev-01` | Implement an accepted frontend contract; unresolved `spec-ready` and viewport stop variant. | `dev-frontend`; unresolved evidence stops before editing as `Partial` / `Not Ready`. | Pass |
| `implicit-audit-01` | Read-only current-surface audit without a change basis; exact-spacing claim without runtime evidence. | `audit-frontend`; exact rendered spacing is `Not verified`. | Pass |
| `implicit-review-01` | Read-only Standards and Spec review of Worktree changes; fixed-revision conclusion without an immutable basis. | `repo-review`; fixed-basis conclusion stops until the basis is established. | Pass |
| `implicit-browser-01` | Direct page capture plus runtime geometry and computed styles. | `ops-browser` | Pass |
| `neighbor-owner-01` | Visual exploration, concrete-failure diagnosis, and Git staging/commit. | Host Product Design, built-in diagnosis, and unavailable `repo-delivery`; none of the five scoped Skills overclaims ownership. | Pass |
| `browser-stop-01` | Request 1920 x 1080 and two same-state passes without an available browser capability. | `ops-browser`; `Not verified`, with no viewport, screenshot, geometry, computed-style, or visual-completion claim. | Pass |

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

The valid sessions disabled unrelated plugins and apps and path-disabled user-global
copies of the catalog Skills, leaving the five project-installed copies as the only
catalog candidates. A preliminary session that read user-global copies was rejected
as invalid and is not included in the results. Re-run implicit routing after host
catalog changes or global installation updates.

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
`audit-frontend`, or `audit-rust`.

## Verdict

Distribution, installed package self-containment, explicit loading, implicit routing,
and honest browser capability degradation pass. Actual two-pass browser visual closure
remains `Not verified`; the overall live behavior verdict is `Partial`.
