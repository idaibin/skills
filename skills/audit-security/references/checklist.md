# Security Audit Checklist

Use this checklist when applying `audit-security` to a code, API, config, dependency, or release security audit. Trigger phrases include `security audit`, `security review`, `authorization risk`, `IDOR`, `API security`, `token leak`, `sensitive data`, and `pre-release security check`.

## Scope Setup

1. Read relevant repo guidance when present.
2. Confirm the audited surface: changed files, endpoint chain, auth path, browser/Vue surface, native IPC boundary, config, dependency, SQLite/file/upload/download/export/backup path, logging path, or release boundary.
3. If this is a full-stack API change and route/method/fields/callers are unclear, route that mapping to `repo-review` first, or mark the chain `Not verified`.
4. Keep the audit scoped; do not expand to a whole-repository review without explicit scope and `repo-review` coordination.
5. If `repo-review` delegated a specialist subreview, record the exact paths or diff, inspect only that boundary, keep the caller as coordinator, and leave files and Git/GitHub state unchanged.

## Profile Selection

Select only profiles supported by the mapped code/config. For each selected profile, record assets, attacker-controlled inputs, trust boundaries, roles or tenants, sensitive operations, existing controls, and missing evidence.

### Web / Browser

- Trace cookie attributes, token/session lifetime, logout/revocation, refresh behavior, and where browser credentials are stored or exposed.
- Review CORS origins/credentials, CSRF protection, redirect and return URL allowlisting, CSP/frame protections, source maps, debug data, and public env variables when applicable.
- Trace attacker-controlled values into HTML/DOM sinks, URLs, navigation, downloads, storage, logging, analytics, and third-party scripts. Encoding is context-specific; sanitization at one sink does not prove another sink safe.
- Treat `localStorage`, `sessionStorage`, IndexedDB, browser caches, and client logs as user-accessible storage, not secret storage.

### API / Service

- Separate authentication from authorization. At the server boundary verify subject, action, resource, role, ownership/tenant, and deny/failure behavior.
- Validate and bound path, query, header, cookie, and body inputs; normalize identifiers before authorization when representation differences matter.
- Review object/field-level authorization, IDOR, mass assignment, response data minimization, internal errors, replay/idempotency, rate limits, and abuse of expensive operations.
- Trace request identity and authorization through middleware, handler/service, persistence, export/download, and audit logging. Frontend visibility is not a server control.

### Rust / Axum

- Verify extractor and body limits, path/query/body parsing, typed validation, rejection mapping, and whether custom extractors run before sensitive work.
- Trace middleware/layer ordering for auth, authorization, CORS, request IDs, tracing, timeouts, rate limits, and sensitive error handling; ordering is part of the control.
- Review `State` ownership and tenant/request scoping, blocking work on async executors, unsafe or shell/command execution, path handling, deserialization limits, and cancellation/resource cleanup where relevant.
- Inspect actual Cargo/lockfile deltas, enabled features, build scripts, native code, and remote downloads before reporting dependency risk.

### Vue / Frontend

- Trace `v-html`, `innerHTML`, DOM APIs, dynamic component/template behavior, and URL attributes such as `href`, `src`, `srcdoc`, and CSS URLs back to their attacker-controlled source and context-specific sanitizer/allowlist.
- Review token/session data in Pinia, composables, persisted stores, local/session storage, query strings, logs, error reporting, hydration data, and source maps.
- Treat Router guards, hidden routes/menu items, disabled controls, and frontend role checks as UX only. Verify authorization again at the API or native command boundary.
- Check external navigation, redirect/return URLs, route params/query, file previews/downloads, and protocol handlers for scheme, origin, and path trust.
- Inspect debug tools, feature flags, public build-time env values, cached keep-alive state, and error payloads for sensitive-data exposure.

### Tauri / Native IPC

- Map frontend caller → typed wrapper → command registration → capability or permission config/allowlist → Rust handler → domain/resource operation.
- Verify that only required commands/plugins/windows/webviews are exposed and that capability files, allowlists, remote URL/webview settings, CSP, and file protocol scopes match the intended trust boundary.
- Treat TypeScript types and hidden UI as untrusted. Revalidate payloads and enforce subject/action/resource/ownership authorization at the Rust/native boundary before filesystem, shell, database, credential, updater, or OS work.
- Resolve or canonicalize paths against an allowed root as the operation permits; for a new target, validate the resolved parent plus final-name/creation rules. Consider absolute, relative, `..`, alternate separators, symlinks, hard links, overwrite/race, file URL, and platform behavior. Do not authorize a raw path string before resolution.
- Review shell/process arguments, URL opening, event/channel origin, window labels, command errors, logs, and long-running task cancellation for injection, confused-deputy behavior, or data exposure.

### SQLite / Files

- Use bound parameters for values and strict allowlists for identifiers or SQL fragments that cannot be parameterized. Parameterized SQL prevents a class of injection; it does not prove that the caller may read or mutate the selected row, tenant, table, export, or backup.
- Trace authorization and tenant/ownership predicates through reads, writes, deletes, bulk operations, exports, downloads, imports, and administrative maintenance. Verify affected-row and not-found/denied behavior.
- Review transaction scope, partial failure, concurrency/locking, rollback, migration defaults, destructive operations, and sensitive temp/journal/WAL artifacts where applicable.
- Validate paths, content type/size, overwrite and symlink behavior, permissions, temp-file lifecycle, atomic replacement, archive extraction, and cleanup.
- Treat exports, backups, diagnostics, crash bundles, and local databases as sensitive-data surfaces. Check who can create/read/download them, fields and secrets included, encryption/access controls, retention, predictable names, cleanup, logs, and generated artifact permissions.

### Cross-Cutting Config, Logs, And Dependencies

- Config: debug flags, default secrets, public access, env handling, production overrides, capabilities, CSP, and unsafe fallback behavior.
- Logs/telemetry: tokens, cookies, API keys, payloads, PII, path contents, command output, panic/stack data, and export/backup locations.
- Dependencies: source, pinning, lockfile, features, build/postinstall scripts, remote downloads, native code, release artifact impact, and actual changed reachability.

## Scoped Threat Sketch

Use this only when the audited boundary is known and no dedicated threat-model workflow is available. Keep it compact and explicitly scoped:

1. List protected assets and sensitive operations.
2. Draw the relevant browser/API/native/storage trust boundaries and entry points.
3. State plausible abuse cases tied to attacker-controlled inputs and roles.
4. Map existing controls and their authoritative enforcement boundary.
5. List assumptions and `Not verified` deployment/runtime/config evidence.

Do not present this sketch as a whole-system threat model, penetration test, security certification, or proof that excluded surfaces are safe.

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

Reject the audit quality if it:

- reports generic OWASP items without local evidence
- ignores auth or permission checks on sensitive API changes
- treats frontend-only hiding as backend authorization
- treats Vue Router guards, typed IPC wrappers, or Tauri capability presence as resource authorization
- treats parameterized SQL as proof of row, tenant, export, or backup authorization
- skips sensitive-data exposure checks for tokens, logs, or exports
- ignores backups, diagnostics, local databases, temporary files, or generated artifacts on a SQLite/file surface
- replaces `repo-review` Worktree/immutable coordination or readiness work, or replaces `repo-delivery` Git mutation
- expands a delegated specialist subreview beyond its paths/diff, edits files, mutates Git/GitHub, or claims whole-review readiness
- claims runtime behavior without evidence
