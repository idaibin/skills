# Eval Cases

Use these cases when changing `code-security` triggers, scope, outputs, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review this API for authorization or IDOR risk.` | Should trigger `code-security`. | Permission and IDOR risk. |
| `Check whether token/session/cookie handling is safe.` | Should trigger `code-security`. | Auth/session security. |
| `Run a lightweight pre-release security check.` | Should trigger `code-security`. | Release security review. |
| `Does this upload API have path traversal or sensitive data exposure risk?` | Should trigger `code-security`. | Upload and data exposure risk. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review whether frontend and backend API fields align, then split commits.` | Should prefer `code-review`. | Contract alignment and commit planning. |
| `Create a full threat model for this system.` | Should prefer `security-threat-model`. | System-wide threat modeling. |
| `Split this requirement into executable tasks.` | Should prefer `code-planner`. | Future implementation planning. |
| `Understand this repository's real commands and directory structure first.` | Should prefer `code-context`. | Repository grounding. |
| `Review all local changes and generate commit groups.` | Should prefer `code-review`. | Dirty-tree review and commit planning. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| API security | Checks auth, authorization, input/output validation, sensitive data, and abuse risks after route/method/field mapping is known. | Stops at endpoint names or duplicates contract alignment only. |
| Permission review | Distinguishes frontend visibility from backend authorization and checks ownership or tenant boundaries. | Treats hidden UI as sufficient permission control. |
| Sensitive data | Checks logs, errors, response fields, storage, and exports for tokens, secrets, or PII. | Ignores exposure paths or reports generic leakage without evidence. |
| Release check | Reports severity, checked surfaces, validation, and `Not verified` gaps. | Claims the release is secure without scoped evidence. |
| Tool safety | Avoids heavy scanners or network tests unless explicitly requested and permitted. | Runs broad or destructive checks by default. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 7.
