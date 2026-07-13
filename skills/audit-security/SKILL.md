---
name: audit-security
description: "Use when a known code change or scoped API, config, dependency, upload/download, logging, auth, authorization, token/session, CORS/CSRF, secret, privacy, or release surface needs a lightweight evidence-grounded security audit rather than a repository-wide or deep vulnerability scan, including when repo-review delegates an explicit security surface for a read-only specialist subreview."
---

# Security Audit

## Overview

Audit known code and configuration surfaces for concrete security risks. Use this after the target surface is clear, either directly or as a read-only specialist over paths or a diff explicitly delegated by `repo-review`. Apply framework-specific checks only when the repository actually uses that stack, and produce a bounded threat sketch when no dedicated threat-model workflow is available.

## Workflow

1. Read repo guidance related to the target files or system boundary.
2. Identify the audited surface: changed files, API chain, auth path, config, dependency, upload/download path, logging path, release boundary, or native IPC boundary. In specialist mode, record the exact delegated paths/diff and do not expand beyond them.
3. For full-stack API changes, rely on `repo-review` to map route, method, fields, helpers, types, callers, and data shaping when that contract chain is not already clear.
4. Identify assets, trust boundaries, authenticated roles/tenants, entry points, sensitive operations, and attacker-controlled inputs relevant to the scoped surface.
5. Select applicable profiles:
   - **Web/browser:** cookies, tokens, storage, CORS, CSRF, redirects, XSS sinks, CSP, clickjacking, and client-side exposure.
   - **API/service:** authentication, authorization, ownership/tenant boundaries, input/output validation, injection, replay, rate limits, error and log exposure.
   - **Rust/Axum:** extractor validation, middleware ordering, state ownership, path/query/body limits, typed errors, unsafe/command execution, and dependency features.
   - **Vue/frontend:** template/HTML injection, unsafe directives or DOM sinks, route-guard assumptions, token storage, debug data, source maps, and frontend-only permission checks.
   - **Tauri/native IPC:** command allowlists, capability/permission config, path and shell access, payload validation, window/webview trust, file URLs, and frontend-to-Rust authorization.
   - **SQLite/files:** SQL construction, path traversal, file permissions, export/download authorization, backup contents, transaction boundaries, and sensitive local data.
6. Inspect the mapped surface for auth, authorization, validation, sensitive-data exposure, browser/API protections, config defaults, dependency risk, abuse paths, and failure behavior.
7. When no dedicated threat-model skill is available, include a compact scoped threat sketch: assets, trust boundaries, plausible abuse cases, existing controls, and unverified assumptions. Do not present it as a whole-system threat model.
8. Run only safe, repository-supported checks. Recommend optional secrets/dependency/static scans when relevant, but do not claim they ran unless evidence exists.
9. Report findings only when grounded in code, config, docs, runtime evidence, or clearly marked assumptions.

## Modes

- **Security audit:** inspect a code, API, config, dependency, file, browser, or native IPC change for scoped security risks.
- **Full-stack API security:** audit an already-mapped frontend/backend API chain for auth, authorization, data exposure, input validation, and abuse risks.
- **Release check:** perform a lightweight pass over security-sensitive changes, runtime config, public artifacts, and dependency deltas without replacing formal assurance.
- **Scoped threat sketch:** document assets, trust boundaries, abuse cases, controls, and evidence gaps when a dedicated threat-model workflow is unavailable.
- **Scoped specialist subreview:** inspect only the security surface delegated by `repo-review`; return security findings and gaps while the coordinator retains review scope, integration, severity, readiness, and report ownership.

## Do Not Use For

- API contract alignment, Worktree readiness/staging guidance, or immutable repository/range/PR/release/package coordination; use `repo-review`, which may delegate a bounded security surface here.
- Actual staging, commit creation, rebase/squash, push, or delivery; use `repo-delivery` after review.
- Whole-system threat modeling when a dedicated threat-model workflow is available and the user requests that scope.
- Repository-wide, deep, exhaustive, or multi-pass vulnerability scanning.
- First-pass repository discovery or future implementation planning; use `repo-map` or `code-planner`.
- Browser/client operation evidence; use `ops-browser` or `ops-client`.

## Hard Rules

- Do not replace `repo-review` for Worktree or immutable review coordination, readiness, staging guidance, or specialist orchestration; and do not replace `repo-delivery` for Git mutation.
- In specialist mode, inspect only the delegated security paths or diff. Do not reclassify unrelated files, expand scope, edit files, stage, commit, push, post review comments, or claim whole-review readiness.
- Do not treat a scoped threat sketch as a complete threat model or security certification.
- Do not run heavy scanners, network tests, exploit attempts, or destructive checks unless explicitly requested, authorized, and supported by repository policy.
- Do not make speculative findings sound proven; use `Not verified` for missing runtime, deployment, config, permission, or attacker-control evidence.
- Do not broaden a focused audit into a whole-repository audit unless the user asks for that scope and `repo-review` coordinates it.
- Preserve unrelated local changes.
- Frontend visibility, disabled controls, route guards, and hidden menu items are never sufficient backend authorization evidence.
- Trace authorization to the server/native boundary and verify subject, action, resource, ownership/tenant, and failure behavior.
- Vue's normal template escaping does not protect `v-html` or other DOM/URL sinks, and it says nothing about persisted tokens, redirects, or source maps. Trace each value to its actual browser sink and trust boundary.
- Tauri command registration, TypeScript typing, capability/permission config, and allowlists limit exposure but do not replace payload, path, or resource authorization inside the Rust/native boundary.
- Parameterized SQL addresses value injection, not row/tenant authorization. Treat exports, backups, local databases, temp files, diagnostics, and generated artifacts as sensitive-data surfaces with independent access, retention, and cleanup checks.
- Distinguish authentication from authorization, validation from normalization, encryption from access control, and local storage from secret storage.
- Check sensitive data across responses, errors, logs, telemetry, exports, backups, source maps, browser storage, crash reports, and generated artifacts where applicable.
- Check dependency changes for source, version pinning, feature flags, build scripts, postinstall, remote downloads, native code, and lockfile impact; do not report generic dependency risk without a concrete delta.
- For uploads and paths, verify size/type/content/path handling, canonicalization, overwrite/symlink behavior, storage permissions, processing isolation, and download authorization as applicable.
- For release checks, never say “secure” or “safe to release” solely because no findings were observed. Report checked surfaces and residual gaps.

## Output Contract

Start with severity-ranked findings. If no blocking findings are found, state that only for the audited scope and list residual `Not verified` areas. Include the audit mode; in specialist mode, name the delegated path/diff boundary and coordinating `repo-review` owner. Include selected profiles, assets and trust boundaries, checked files/endpoints/configs, evidence, impact, recommended fix or validation, optional tools not run, and intentionally excluded scope.

## Skill Maintenance

When maintaining this package, update `references/eval-cases.md`, `references/usage.md`, `agents/openai.yaml`, and framework-specific guidance when triggers, profiles, or output contracts change. In AICraft, run `python3 scripts/validate-skills.py --skill audit-security` before publishing.

## References

- See [references/usage.md](references/usage.md) for summary, triggers, and examples.
- See [references/checklist.md](references/checklist.md) for security audit surfaces and reporting details.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
