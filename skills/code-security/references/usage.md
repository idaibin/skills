# Code Security

## Summary

Review code and configuration changes for security risks after the target surface is clear. It complements `code-review`; it does not replace contract alignment, dirty-tree ownership, staging, or commit planning.

## Best For

- Auth, session, token, or cookie changes
- Permission checks, tenant isolation, and IDOR risk
- Full-stack API security after route/method/field mapping is known
- File upload, download, export, import, or path handling
- Logging, error, and sensitive-data exposure checks
- CORS, CSRF, rate limit, and browser/API protection checks
- Dependency, script, or config changes with security impact
- Lightweight release security checks

## Triggers

Use for prompts like:

- `Review this API for authorization or IDOR risk.`
- `Run a code security review.`
- `Check whether token/session/cookie handling is safe.`
- `Check whether this upload API has security issues.`
- `Run a lightweight pre-release security check.`
- `Check whether sensitive data can leak.`
- `use code-security`

Do not use for general repository onboarding, future task planning, API contract alignment, commit grouping, or system-wide threat modeling; prefer `code-context`, `code-planner`, `code-review`, or `security-threat-model` for those.

## Output

Expect severity-ordered security findings with file/path evidence, impact, recommendation, checked surfaces, and `Not verified` gaps. No finding should be reported as proven without code, config, docs, runtime evidence, or a clearly marked assumption.

## Maintenance

Use `references/eval-cases.md` for trigger and quality checks. In AICraft, validate with `python3 scripts/validate-skills.py`; end-user installs use `npx skills add https://github.com/idaibin/aicraft`, and end-user updates use `npx skills update`.
