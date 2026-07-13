# Eval Cases

Use these cases when changing `audit-security` triggers, profiles, scope, outputs, delegation boundaries, or metadata.

## Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review this API for authorization or IDOR risk.` | Should trigger `audit-security`. | Permission and IDOR risk. |
| `Check whether token/session/cookie handling is safe.` | Should trigger Web/API profiles. | Auth/session security. |
| `Review this Vue page and Tauri command boundary for frontend-only permission checks, unsafe IPC, and path access.` | Should trigger Vue, Tauri IPC, and file profiles. | Framework-specific scoped security. |
| `Review this Axum route's extractor limits, middleware order, tenant authorization, and typed errors.` | Should trigger Rust/Axum and API profiles. | Rust service security boundary. |
| `Trace this Vue v-html and redirect URL flow, including token storage, Router guard assumptions, and source maps.` | Should trigger Vue and Web profiles. | Browser sinks, navigation trust, and client exposure. |
| `Check whether this Tauri capability and typed command still enforce native authorization and canonicalize paths.` | Should trigger Tauri IPC and file profiles. | Exposure configuration is not resource authorization. |
| `This SQLite query is parameterized; review row authorization plus export and backup data access.` | Should trigger SQLite/File and API or native authorization profiles. | Injection control does not prove authorization. |
| `Run a lightweight pre-release security check.` | Should trigger release mode. | Release security audit. |
| `Run a lightweight security audit of this scoped API change, not a repository-wide scan.` | Should trigger scoped audit. | Bounded change audit. |
| `Does this upload API have path traversal or sensitive data exposure risk?` | Should trigger file/API profiles. | Upload and data exposure risk. |
| `No threat-model skill is available; give me a scoped threat sketch for this endpoint.` | Should trigger scoped threat-sketch mode. | Local fallback without claiming whole-system coverage. |
| `Under repo-review, inspect only the delegated API and Tauri files for security risks.` | Should trigger a scoped specialist and keep `repo-review` as local-change coordinator. | Bounded dirty-tree delegation. |
| `Under repo-review, inspect only the auth and release configuration paths.` | Should trigger a scoped specialist and keep `repo-review` as immutable-review coordinator. | Bounded repository/range delegation. |

## Non-Trigger Eval

| User prompt | Expected result | Why |
| --- | --- | --- |
| `Review whether frontend and backend API fields align, then split commits.` | Should use `repo-review` for alignment/staging plan/readiness, then `repo-delivery` for authorized staging and commit creation. | Local change review has a separate owner. |
| `Review the whole repository and coordinate frontend, Rust, security, CI, and docs findings.` | Should prefer `repo-review`, which may delegate security paths here. | Whole-review coordination is broader than a security specialist. |
| `Create a full threat model for this system.` | Should prefer a dedicated threat-model workflow when available. | Whole-system modeling is broader than this skill. |
| `Run a deep repository-wide vulnerability scan with multiple passes.` | Should prefer a dedicated deep security scan workflow. | Repository-wide scanning is outside scoped audit. |
| `Split this requirement into executable tasks.` | Should prefer `code-planner`. | Future implementation planning. |
| `Understand this repository's real commands and directory structure first.` | Should prefer `repo-map`. | Repository mapping. |
| `Review all local changes and generate commit groups.` | Should prefer `repo-review`. | Dirty-tree review and commit planning. |

## Quality Eval

| Case | Expected evidence | Reject if |
| --- | --- | --- |
| Scope mapping | Identifies audited files/endpoints/configs, assets, attacker-controlled inputs, trust boundaries, roles/tenants, sensitive operations, and excluded surfaces. | Starts from a generic OWASP checklist without local ownership or entry points. |
| Profile selection | Selects only applicable Web/API, Rust/Axum, Vue, Tauri IPC, SQLite/File, dependency, or release checks from actual repository evidence. | Applies every framework checklist or assumes a stack from the prompt alone. |
| Web/browser security | Traces cookie/token/session lifetime, browser storage, CORS/CSRF, redirects, CSP/frame controls, DOM/HTML/URL sinks, source maps, and third-party exposure only where applicable. | Treats browser storage as secret storage, assumes one sanitizer fits every sink, or lists headers without config/evidence. |
| API security | Checks authentication separately from subject/action/resource authorization, ownership/tenant boundaries, all input channels, output minimization, IDOR/mass assignment, replay/idempotency, rate limits, and abuse risks after route/method/field mapping is known. | Stops at endpoint names, duplicates contract alignment only, or treats authenticated as authorized. |
| Rust/Axum security | Verifies extractor/body limits, middleware ordering, state/request scope, rejection/error mapping, async/blocking boundaries, path/command/unsafe behavior, and concrete Cargo feature deltas where relevant. | Applies generic Rust advice without tracing the Axum layer/handler/state path or invents dependency risk without a delta. |
| Vue/frontend security | Traces `v-html`, DOM/template and URL sinks, token/persisted-store exposure, redirect/route input, Router-guard assumptions, debug/source-map data, and frontend permission controls to their authoritative API/native boundary. | Calls template escaping, hidden UI, disabled controls, or a route guard sufficient authorization. |
| Tauri/native IPC | Maps caller, wrapper, command registration, capabilities/permissions or allowlist, webview/window trust, Rust handler, payload/path/shell validation, and subject/action/resource authorization at the native boundary. | Treats typed wrappers, command registration, or capability presence alone as native authorization proof. |
| SQLite/files | Distinguishes bound-value injection control from row/tenant authorization; checks SQL fragments/identifiers, transactions, canonicalization/traversal, permissions, overwrite/symlink behavior, temp/WAL data, export/download access, backup contents, retention, and cleanup as applicable. | Treats parameterized SQL as authorization or ignores sensitive exports/backups/generated files. |
| Permission review | Distinguishes authentication, authorization, validation, encryption, and storage; verifies subject/action/resource/owner or tenant/failure behavior. | Collapses all controls into “authenticated” or “encrypted.” |
| Sensitive data | Checks responses, errors, logs, telemetry, exports, backups, storage, crash reports, source maps, and generated artifacts where relevant. | Ignores exposure paths or reports generic leakage without evidence. |
| Dependency delta | Reviews source, pinning, features, build/postinstall scripts, remote downloads, native code, and lockfile impact for actual dependency changes. | Reports dependency risk without a concrete delta. |
| Scoped threat sketch | Records scoped assets and sensitive operations, browser/API/native/storage trust boundaries and entry points, plausible role/input-specific abuse cases, authoritative controls, excluded surfaces, and unverified assumptions while clearly stating it is not a full threat model. | Presents a generic checklist as complete threat modeling, penetration testing, certification, or evidence about excluded surfaces. |
| Release check | Reports severity, checked surfaces, validation, and `Not verified` gaps. | Says the release or system is secure because no findings were observed. |
| Scoped specialist boundary | States the delegated paths/diff and selected profiles, inspects only that surface, returns findings and gaps to `repo-review`, and leaves files and Git/GitHub state unchanged. | Reclassifies unrelated files, expands scope, edits, stages, commits, pushes, comments, or claims whole-review readiness. |
| Tool safety | Avoids heavy scanners, exploit attempts, or network tests unless explicitly requested, authorized, and supported. | Runs broad or destructive checks by default. |

## Scoring

Score each quality case from 0 to 10. Minimum pass: all trigger/non-trigger expectations are correct and every quality case scores at least 8.
