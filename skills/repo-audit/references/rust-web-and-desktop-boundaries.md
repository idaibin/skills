# Web And Desktop Rust Boundaries

Load only when the selected Rust surface includes an Axum HTTP boundary or a
Tauri native command/configuration boundary. Keep transport thin and apply the
ordinary Ownership/errors, Concurrency/runtime, SQLite, or Unsafe/FFI profiles
independently when their risks also apply.

## Axum

- Trace router nesting and state types through handlers, middleware, fallback,
  error conversion, tests, and server startup. Prefer typed extractors and
  `State`/`FromRef` composition that match the repository; `Arc<AppState>` and
  `Extension` are options, not universal defaults.
- Account for the request-body one-consumer boundary and extractor ordering.
  Verify rejection mapping, body limits, content type, path/query validation,
  authentication/authorization context, and sensitive logging before treating
  a handler signature as safe.
- Convert domain/infrastructure failures into stable `IntoResponse` behavior at
  one outer boundary. Do not expose internal errors or log-and-rethrow at every
  layer.
- Inspect Tower layer order and scope for timeout, load shedding, concurrency
  limits, CORS, tracing, compression, and authorization. Reject universal
  timeout values and permissive origins; derive them from workload and trust
  boundaries.
- Exercise routers as services for status, headers, body, rejection, auth, and
  state behavior without requiring a real socket when the repository supports
  that seam. Real network/proxy behavior remains a separate runtime gap.

## Tauri

- Treat frontend-to-Rust IPC arguments as untrusted even when the UI ships in
  the same application. Validate command arguments, paths, URLs, payload sizes,
  identifiers, and resource limits in Rust; frontend typing is not enforcement.
- Separate authorization layers. Core/plugin permissions use Tauri v2
  capabilities, but custom application commands registered through
  `invoke_handler` are allowed to all application windows/webviews by default.
  Before claiming per-window/webview invocation ACL for a custom command, check
  `build.rs`, `tauri_build::AppManifest::commands`, generated
  `allow-<command>`/`deny-<command>` permissions, and their capability
  assignments. Verify configured scopes are enforced by the command or plugin
  implementation, and enforce user/domain authorization at the Rust domain
  owner when application identity or business policy applies. Do not duplicate
  platform ACL mechanically inside every command. CSP is defense in depth,
  not command authorization.
- Trace each command through registration, typed request/result/error mapping,
  domain owner, async/blocking execution, progress/cancellation, caller, tests,
  build manifest/generated app-command permissions when applicable,
  capability, permission, scope, and window/webview assignment.
- Apply least privilege to capabilities and permissions. Broad filesystem,
  shell, process, HTTP, or remote-content access requires an explicit product
  need and bounded scope; a command registration alone does not authorize it.
- Review CSP and remote-content behavior against the actual webview origin and
  plugins. Do not copy a permissive source list merely to make development work.
- Route JS/TS adapter and UI behavior to the frontend owner, Rust command/domain
  behavior here, and real window/menu/file-dialog/runtime proof to the client
  operator. A cross-boundary change must validate both contracts.
