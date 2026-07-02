---
name: code-security
description: Use when code, API, config, dependency, upload/download, logging, auth, authorization, token/session, CORS/CSRF, secret, privacy, or release changes need security-risk review.
---

# Code Security

## Overview

Review code and configuration changes for concrete security risks. Use this after repository scope is clear, especially for auth, permission, API, sensitive-data, dependency, or release-sensitive changes.

## Workflow

1. Read repo guidance related to the target files or system boundary.
2. Identify the reviewed surface: changed files, API chain, auth path, config, dependency, upload/download path, logging path, or release boundary.
3. For full-stack API changes, rely on `code-review` to map route, method, fields, helpers, types, callers, and data shaping when that contract chain is not already clear.
4. Inspect the mapped surface for auth, authorization, input/output validation, sensitive-data exposure, browser/API protections, config defaults, dependency risk, and abuse paths.
5. Report security findings only when grounded in code, config, docs, runtime evidence, or clearly marked assumptions.
6. Recommend focused validation or mark gaps `Not verified`.

## Modes

- **Security review:** inspect a code, API, config, dependency, or release change for security risks.
- **Full-stack API security:** review an already-mapped frontend/backend API chain for auth, authorization, data exposure, input validation, and abuse risks.
- **Release check:** do a lightweight pre-release pass over security-sensitive changes without replacing full threat modeling.
- **Upgrade mode:** compare only remote `skills/code-security/` against local files; preview before writing.

## Do Not Use For

- API contract alignment, dirty-tree ownership, staging, commit grouping, or commit messages; use `code-review`.
- Whole-system threat modeling unless the user requests that scope; use `security-threat-model` when available.
- First-pass repository discovery or future implementation planning; use `code-context` or `code-planner`.
- Browser/client operation evidence; use `ops-browser` or `ops-client`.

## Hard Rules

- Do not replace `code-review` for API contract alignment, dirty-tree ownership, staging, commit planning, or commit messages.
- Do not replace `security-threat-model` for system-wide threat modeling.
- Do not run heavy scanners, network tests, or destructive checks unless the user explicitly asks and permissions allow it.
- Do not make speculative findings sound proven; use `Not verified` for missing runtime, config, or permission evidence.
- Do not broaden a focused review into a whole-repository audit unless the user asks for that scope.
- Preserve unrelated local changes.

## Output Contract

Start with security findings ordered by severity. If no blocking findings are found, say that clearly and list residual `Not verified` areas. Include checked surfaces, evidence, recommended fixes or validation, and any scope intentionally excluded.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, and `agents/openai.yaml` with trigger, mode, or output changes. In AICraft, run `python3 scripts/validate-skills.py` before publishing and `npx skills add https://github.com/idaibin/aicraft --list` after publishing to GitHub.

## References

- See [references/usage.md](references/usage.md) for summary, triggers, and examples.
- See [references/checklist.md](references/checklist.md) for security review surfaces and reporting details.
- See [references/upstream-sources.md](references/upstream-sources.md) for trusted source metadata.
- See [references/upgrade-workflow.md](references/upgrade-workflow.md) for the upgrade process.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
