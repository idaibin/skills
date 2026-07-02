# Code Security Checklist

Use this checklist when applying `code-security` to a code, API, config, dependency, or release security review. Trigger phrases include `code security`, `security review`, `authorization risk`, `IDOR`, `API security`, `token leak`, `sensitive data`, and `pre-release security check`.

## Scope Setup

1. Read relevant repo guidance when present.
2. Confirm the reviewed surface: changed files, endpoint chain, auth path, config, dependency, upload/download path, logging path, or release boundary.
3. If this is a full-stack API change and route/method/fields/callers are unclear, route that mapping to `code-review` first or mark the chain `Not verified`.
4. Keep the review scoped; do not expand to a whole-repository audit without an explicit request.

## Security Surfaces

Check only the surfaces relevant to the request:

- Auth: login, token, session, cookie, password reset, device binding
- Authorization: role checks, tenant boundaries, ownership checks, IDOR risk
- Input: schema validation, type narrowing, SQL/command injection, path traversal
- Output: sensitive fields, internal errors, stack traces, PII, secrets
- Browser/API: CORS, CSRF, rate limit, replay, redirect, local storage
- Files: upload content type, extension, size, path, download/export authorization
- Config: debug flags, default secrets, public access, env handling
- Dependencies: new packages, scripts, postinstall, remote downloads, known risky behavior
- Logs: tokens, cookies, API keys, payload secrets, user data

## Severity

- **High:** likely auth bypass, privilege escalation, secret exposure, arbitrary file access, injection, or cross-tenant data access.
- **Medium:** exploitable with constraints, missing validation on sensitive paths, unsafe defaults, or meaningful data exposure.
- **Low:** defense-in-depth gap, weak error handling, minor leakage, or missing security documentation.

## Reporting

For each finding include:

- severity
- file/path or endpoint evidence
- impact
- recommendation
- validation performed or `Not verified`

If no blocking findings are found, report checked surfaces and residual `Not verified` areas instead of claiming the code is secure.

## Reject Conditions

Reject the review quality if it:

- reports generic OWASP items without local evidence
- ignores auth or permission checks on sensitive API changes
- treats frontend-only hiding as backend authorization
- skips sensitive-data exposure checks for tokens, logs, or exports
- replaces `code-review` contract mapping or commit planning
- claims runtime behavior without evidence
