---
name: audit-rust
description: "Use when a Rust workspace or known Rust surface needs a scoped, read-only audit of selected architecture, ownership, error, concurrency, performance, persistence, or unsafe-boundary risks; use repo-review when a Worktree or immutable change basis needs coordination."
---

# Rust Audit

## Overview

Audit Rust engineering from repository evidence. Select only the audit profiles required by the task; do not load architecture, performance, memory, SQLite, concurrency, and FFI review into every audit. This workflow is read-only by default; use `dev-rust` for requested changes. `repo-review` may invoke this skill for a bounded Rust specialist subreview under either a Worktree or immutable review basis.

## Rule Priority

Resolve conflicts in this order:

1. The user's current explicit request.
2. Effective repository guidance, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
3. Existing project code, toolchain, and architecture.
4. Project documentation and interface contracts.
5. This skill.
6. External reference repositories.

Do not rewrite a working local design merely to resemble an external project.

## Workflow

1. Read repository guidance, record the inspected revision plus relevant Worktree
   state for reproducibility, run `git status --short`, and inspect only relevant
   manifests, entry points, modules, docs, tests, benches, migrations, CI, and
   runtime configuration. This inspection snapshot does not imply change
   attribution. When delegated, record the exact Rust paths or diff and keep the
   caller as review coordinator.
2. Determine workspace/crate boundaries, library and binary entries, feature flags, MSRV, edition, runtime/thread model, error/tracing style, database linkage, migration strategy, quality commands, and unsafe/FFI/native dependencies that apply to the task.
3. Select one or more audit profiles:
   - **Architecture/baseline:** crate/module/API ownership, dependencies, toolchain policy, structural lifecycle, docs, and legacy exceptions.
   - **Ownership/errors:** resource lifetime, copying/retention, typed errors,
     panic/log/retry boundaries, and applicable Axum HTTP or Tauri IPC
     contracts.
   - **Agent Runtime:** a stateful local-agent workflow, typed protocol/schema,
     durable operation history/recovery, approval/policy/sandbox enforcement, or
     Tauri/local app-server IPC. A Rust async crate, SQLite dependency, or Tauri
     directory alone does not activate this profile; load
     `references/agent-runtime-profile.md` only for a reachable lifecycle or
     boundary.
   - **Concurrency/runtime:** Tokio/blocking work, tasks, channels, locks, backpressure, cancellation, panic propagation, and shutdown.
   - **Performance/memory:** representative workload, release baseline, CPU, allocation, RSS, I/O, binary/compile cost, caches, mmap, allocator/native/OS retention.
   - **SQLite:** runtime/linkage, connections, transactions, WAL, migrations, schema, indexes, plans, maintenance, backup, and recovery.
   - **Unsafe/FFI:** invariants, ABI/layout, pointer ownership, callbacks, threads, panic containment, alloc/free symmetry, and native cleanup.
4. Classify applicable standards as portable governance, organization baseline, new-project template, repository contract, or documented legacy exception. Never turn a version snapshot or example tree into a universal rule.
5. Consume current `repo-map` output or build a targeted inventory of analogous APIs, modules, database access, background tasks, tests, benchmarks, migrations, callers, and architecture docs.
6. When the selected Rust audit crosses reachable runtime/configuration, packaging, API,
   persistence, compatibility, security, deployment, or cross-repository boundaries, load
   `references/project-grounding.md`. Select this from semantic reachability, not from Rust,
   Cargo, or configuration file presence; mark unrelated risk classes `Not applicable` and
   unexercised runtime claims `Not verified`.
7. Map governing invariants, resource owners, shutdown/cancellation paths, error boundaries, workload, baseline, and validation gaps for the selected profiles only. When Agent Runtime is selected, map the smallest Thread/Turn/Operation state machine, one typed protocol/schema authority, uncertain-operation recovery, approval/policy/sandbox layers, durable source/projection authority, and Tauri/local app-server boundary. When duplication, dead/unused code, abstraction, coupling, or maintainability materially applies, load `references/code-quality.md` with audit semantics and Rust reachability rules.
8. When an in-scope selected-profile change adds, reuses, moves, renames, or deletes a structural surface, audit every affected manifest, registration, export, feature, test, migration, generated file, deployment path, architecture document, and index; search for stale references.
9. Validate hypotheses with non-mutating repository-defined commands and representative data. Do not substitute `cargo check` for release, benchmark, concurrency, migration, or runtime evidence.
10. Stop when the selected profiles are supported by evidence. Mark unselected profiles out of scope rather than partially reviewing them.
11. Report severity-ranked findings with impact, exact location, evidence, remediation direction, `Not verified` gaps, and the selected/excluded profile boundary. In specialist mode, return findings to the coordinating `repo-review`; do not stage, commit, post comments, or take over final review ownership.

## Modes

- **Focused profile audit:** one or two selected risk surfaces with bounded evidence and commands.
- **Combined risk audit:** multiple interacting profiles, such as Tokio plus SQLite or unsafe plus performance, with explicit integration risks.
- **Baseline audit:** compare toolchain, workspace, directory, naming, validation, documentation, and legacy-exception policy against real project evidence.
- **Performance experiment review:** define workload, baseline, measurement, one-factor experiment, and comparable before/after evidence; route experiment edits to `dev-rust`.
- **Scoped specialist subreview:** inspect only the Rust paths or diff delegated by `repo-review`; return domain findings without taking review coordination or Git/GitHub ownership.

## Hard Rules

- Resolve toolchain, layout, ownership, and API expectations from the repository; do
  not impose a universal MSRV, directory tree, abstraction, or external template.
- Treat code shape, ownership primitives, panics, query patterns, lints, and apparent
  dead code as signals. Require context, reachability, workload or invariant, impact,
  and counterevidence through the selected references before reporting a finding.
- Load and apply only references for the selected Agent Runtime, architecture,
  ownership/error, concurrency, performance/memory, SQLite, unsafe/FFI, or
  conditional code-quality profile. Require the selected profile's workload,
  runtime, invariant, reachability, or target evidence before conclusions.
- Do not edit, stage, commit, post review comments, or deliver code in audit mode. Route approved remediation to `dev-rust`. `repo-review` owns Worktree and immutable review coordination; `repo-delivery` alone owns Git mutation.
- Do not claim profiles were reviewed when their workload, runtime, target, dataset, or tool support was unavailable. Mark the exact gap `Not verified`.
- When a selected Rust profile exposes a security-relevant condition, return the
  domain evidence—input, control, sink or protected operation, reachable path,
  trust boundary, counterevidence, and proof gap—without claiming exploit
  validation or fix completion. Route an explicit vulnerability scan, attack-path,
  or PoC-validation request to an available host security workflow.

## Do Not Use For

- Repository orientation without a Rust task; use `repo-map`.
- Rust implementation, modification, refactoring, or porting; use `dev-rust`.
- Root-cause diagnosis of a concrete failure; use the host's built-in diagnosis under effective instructions.
- Owning Worktree readiness or immutable repository/range/PR/release coordination; use `repo-review`, which may delegate a bounded Rust surface here.
- Commit, push, squash, branch cleanup, or remote proof; use `repo-delivery` only when the user explicitly requests delivery.
- Review of a fixed Worktree or immutable change basis, including authorization or token risks; use `repo-review`.
- A general repository/path vulnerability scan or explicit exploit validation;
  use an available host security workflow. Keep bounded Rust ownership, Axum,
  Tauri, SQLite, unsafe, and FFI audits here.
- A frontend-only change with no Rust or SQLite boundary.

## Output Contract

Start with the inspection snapshot, selected profiles, and severity-ranked findings. For each finding, report impact, exact location, evidence, remediation direction, and validation gap. Then summarize project class; coordinating owner when this is a scoped specialist subreview; guidance/manifests/code/migrations/docs/tests/commands inspected; existing candidates; ownership and invariants; selected profile evidence; structural lifecycle; workload and before/after data where applicable; explicitly excluded profiles; and `Not found` or `Not verified` gaps.

## References

Load each linked reference independently when its named surface applies; grouping links does not require paired loading.

- Read [architecture-and-modules.md](references/architecture-and-modules.md) for structural boundaries and [project-baseline-and-lifecycle.md](references/project-baseline-and-lifecycle.md) for baseline classification, legacy policy, reuse, and lifecycle.
- Read [ownership-and-resources.md](references/ownership-and-resources.md) for ownership, clone, `Arc`, buffers, and caches and [errors-and-api-design.md](references/errors-and-api-design.md) for invariants, panic, retry, logging, and boundary translation.
- Read [web-and-desktop-boundaries.md](references/web-and-desktop-boundaries.md)
  for Axum extractors/state/middleware/response testing and Tauri command,
  capability, permission, CSP, path, and webview trust boundaries.
- Read [agent-runtime-profile.md](references/agent-runtime-profile.md) only when
  the selected audit reaches a stateful local-agent workflow, typed agent
  protocol/schema, durable operation history/recovery, approval/policy/sandbox
  enforcement, or Tauri/local app-server IPC.
- Read [async-and-concurrency.md](references/async-and-concurrency.md) for runtime, blocking work, tasks, channels, locks, timeouts, cancellation, shutdown, and Loom.
- Read [performance.md](references/performance.md) for workloads, CPU, I/O, binary/compile cost, and measurement and [memory.md](references/memory.md) for allocation, retention, RSS, caches, mmap, and leak classification.
- Read [sqlite.md](references/sqlite.md) for linkage, connections, transactions, WAL, migrations, schema, indexes, plans, maintenance, backup, and recovery.
- Read [testing-and-quality.md](references/testing-and-quality.md) for Cargo, Clippy, Miri, coverage, benchmarks, and risk-based gates and [unsafe-and-security.md](references/unsafe-and-security.md) for unsafe, FFI, native-resource, dependency, and security checks.
- Read [code-quality.md](references/code-quality.md) when duplication,
  dead/unused code, abstraction quality, hidden coupling, or maintainability is
  materially in scope.
- Read [project-grounding.md](references/project-grounding.md) when selected Rust
  evidence crosses reachable runtime/configuration, packaging, API, persistence,
  compatibility, security, deployment, or cross-repository boundaries.
- Read [review-checklist.md](references/review-checklist.md) for profile-scoped gates and [anti-patterns.md](references/anti-patterns.md) for detectable failure patterns.
- Read [reference-corpus.md](references/reference-corpus.md) for official source evidence, adopted rules, and rejected cargo-cult choices.
- Read [usage.md](references/usage.md) and [eval-cases.md](references/eval-cases.md) for routing/reporting/evals; load [codebase-design.md](references/codebase-design.md) only for a selected public-module, seam, abstraction, locality, or testability audit.
