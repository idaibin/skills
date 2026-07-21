# Security Audit

## Summary

Audit a known code change or scoped API/configuration surface for security risks after the target is clear. It can also act as a read-only specialist over security paths or a diff explicitly delegated by `repo-review`. It is not a repository-wide or deep vulnerability scan and does not replace repository grounding, contract alignment, dirty-tree review, immutable review coordination, staging plans, or delivery.

## Best For

- Auth, session, token, or cookie changes
- Permission checks, tenant isolation, and IDOR risk
- Full-stack API security after route/method/field mapping is known
- File upload, download, export, import, or path handling
- Logging, error, and sensitive-data exposure checks
- CORS, CSRF, rate limit, and browser/API protection checks
- Rust/Axum extractor, middleware-ordering, state, error, and command/path checks
- Vue `v-html`/URL sinks, token/storage exposure, Router trust, source-map, and frontend-only permission checks
- Tauri command capability/allowlist, webview trust, native authorization, shell, and filesystem boundary checks
- SQLite query construction, row/tenant authorization, transactions, local data, exports, backups, and file permissions
- Dependency, script, or config changes with security impact
- Lightweight release security checks
- A compact scoped threat sketch for a known boundary when no dedicated threat-model workflow is available
- A bounded security specialist subreview delegated by `repo-review`

## Profile Routing

- **Web/browser:** select for cookies, tokens, storage, DOM/URL sinks, CORS, CSRF, redirects, CSP, clickjacking, source maps, and client exposure.
- **API/service:** select for authentication, subject/action/resource authorization, tenant/ownership boundaries, validation, output exposure, replay, rate limits, and abuse paths.
- **Rust/Axum:** select when extractors, middleware/layers, shared state, typed errors, unsafe/command execution, async resource behavior, or Cargo features are in the audited surface.
- **Vue/frontend:** select for `v-html` and other template/DOM sinks, URL trust, token or persisted-store exposure, Router guard assumptions, debug/source-map data, and frontend-only permission controls.
- **Tauri/native IPC:** select for commands, plugins, capabilities/permissions or allowlists, window/webview trust, frontend-to-Rust authorization, path/file URL handling, shell/process access, events, and native errors.
- **SQLite/files:** select for SQL construction, row/tenant permissions, transactions, path traversal/canonicalization, file permissions, import/export, backups, local databases, temp/WAL artifacts, and sensitive generated files.

Select multiple profiles only when the evidence crosses those boundaries. A full-stack Vue → Axum → SQLite or Vue → Tauri → filesystem change should state where each control is authoritative; do not apply every profile by default.

## Triggers

Use for prompts like:

- `Review this API for authorization or IDOR risk.`
- `Run a security audit.`
- `Check whether token/session/cookie handling is safe.`
- `Check whether this upload API has security issues.`
- `Review this Axum route's extractor limits, middleware order, tenant authorization, and typed error exposure.`
- `Trace this Vue v-html and external URL flow; include token storage, Router guard assumptions, and source-map exposure.`
- `Review this Tauri command from Vue caller through capabilities and Rust authorization, including path canonicalization and shell arguments.`
- `Check this parameterized SQLite export for row authorization, backup contents, file permissions, retention, and download access.`
- `Run a lightweight pre-release security check.`
- `Run a lightweight security audit of this scoped API change, not a repository-wide scan.`
- `Check whether sensitive data can leak.`
- `No dedicated threat-model workflow is available; give me a scoped threat sketch for this endpoint and its storage boundary.`
- `Under repo-review, inspect only the delegated API and Tauri files for security risks and return a read-only specialist assessment.`
- `Under repo-review, audit only the selected auth and release configuration paths.`
- `use audit-security`

Do not use for general repository onboarding, future task planning, API contract alignment, local commit grouping, whole-repository review coordination, system-wide threat modeling, or repository-wide/deep vulnerability scanning; prefer `repo-map`, host planning, `repo-review`, threat-model, or security-scan workflows as applicable.

## Output

Expect severity-ordered security findings with audit mode, selected profiles, scoped assets and trust boundaries, file/endpoint/config evidence, impact, recommendation, validation, excluded surfaces, and `Not verified` gaps. Specialist output must state the delegated path/diff boundary and return to `repo-review` without editing or taking coordinator/Git ownership. A scoped threat sketch must list abuse cases and existing controls while saying it is not a whole-system threat model.
