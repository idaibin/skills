# Skill Live Canary Summary

## Basis

- Digest scope: all 16 packages declared by `skills-index.json`; the index owns the package set.
- Package digest: `sha256:475f18f7761c293e86e9199f3c171ab7b1e2cad9baa0dcce03028c67d1b18c5e`
- Change focus: shorter action-first descriptions, conditional frontend/browser references,
  reuse-first focused checks, one qualifying visual comparison unless correction or an
  accepted project requirement needs more, and continuation within existing task authority.
- Prior live results do not certify this digest. Raw task and provider evidence stays private.
- Release review aligned the frontend default prompt, protocol completion rule, and
  catalog description with the one-comparison policy. Live cases predate this correction.

## Current Results

| Gate | Result | Evidence boundary |
| --- | --- | --- |
| Package structure and shared protocol parity | Pass | 16 packages; linked references and generated copies validate. |
| Deterministic routing | Pass | 56/56 cases, zero regressions against the immutable base. |
| Context warnings | Pass | Zero entrypoint/direct-reference warnings; estimates are not measured model tokens. |
| Regression suite | Pass | 452/452 checks, including 52 visual-evidence checks. |
| Final catalog gate | Pass | The canonical gate exited 0 after the release review corrections: 16 packages, 56 routing cases, 452 regressions, external DESIGN.md contract checks, and diff validation. Source discovery also returned exactly the 16 catalog packages. |
| CLI live comparison | Not verified | Both baseline and candidate five-case runs ended before any agent tool call. Codex CLI 0.150.0 returned HTTP 400 requiring a newer client for the requested GPT-6 Astra model. The model was not substituted. |
| Host independent forward-test | Prior candidate only | Five cases passed their fixture scope before the release review correction: source change, no-op, write-authorization stop, missing-source specification boundary, and already-authorized local-browser handoff. Parent readback found exactly two authorized fixture-line changes; no-op and blocked-write fixtures stayed unchanged. The focused check verifies content consistency, not TypeScript execution. The blocked-write case permits source reads and does not certify the stricter CLI pre-inspection stop case. Current-digest live behavior remains unverified. |
| Installed-copy parity | Delivery-time check | The preceding candidate matched all 16 installed package trees. Verify this digest against the authorized installation after Git delivery; installation receipts remain local. |
| Browser/client execution and model-efficiency improvement | Not verified | No real browser/client run or valid before/after model-cost comparison was completed. |

## Boundary

Static checks establish package and validator consistency. The visual validator accepts
complete first-pass evidence, preserves an explicitly required pass count, and rejects
failed or incomplete completion claims. Fixtures are synthetic and do not establish real
page fidelity. The host cases are not a controlled model comparison; exact model
attribution and cost were not established. Installed bytes do not prove that existing
sessions reloaded discovery.
