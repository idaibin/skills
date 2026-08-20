---
name: dev-typescript
description: "Use when an authorized non-browser TypeScript or JavaScript source change must be implemented or refactored in a Node.js, Bun, or Deno service, API, CLI, MCP server, worker, library, or engineering script; owns source edits and validation, not browser UI, audit-only, review-only, or Git-delivery work."
---

# TypeScript Implementation

## Overview

Implement non-browser TypeScript and JavaScript changes against the repository's real runtime, package manager, module system, type-checker, test runner, and ownership boundaries. Node.js, Bun, and Deno are runtime profiles of this Skill, not separate Skills.

Consume `urn:skills:typescript-change-request:v1`; produce `urn:skills:source-change-result:v1`. Source, package manifests, lockfiles, runtime configuration, generated contracts, and repository guidance remain authoritative.

## Workflow

1. Read effective repository guidance and run `git status --short` before edits.
2. Confirm authorization, requested behavior, acceptance criteria, non-goals, affected files, compatibility constraints, and validation seams. Use host planning when complex requirements remain unresolved.
3. Detect the actual runtime and toolchain from manifests, lockfiles, scripts, configuration, imports, CI, and tests. Load [runtime-profiles.md](references/runtime-profiles.md) and select Node.js, Bun, Deno, or an explicitly evidenced mixed-runtime profile.
4. Trace the smallest complete interface chain across entry point, transport or command, service/domain logic, persistence or external adapter, types/schema, callers, tests, and generated outputs. Prefer reuse, then extension, then adaptation of the nearest reference before creating a new abstraction.
5. Preserve one authority for each contract. Generate types from an existing schema authority where the repository does so; do not introduce a second hand-maintained Zod, JSON Schema, OpenAPI, or TypeScript model merely for local convenience.
6. When a stable public seam exists, load [behavior-first.md](references/behavior-first.md), observe a red-capable focused check, implement the minimum vertical behavior, and repeat. Do not fake red-green evidence when the baseline cannot run.
7. Implement the smallest idiomatic change. Preserve strictness, module format, package-manager ownership, async lifecycle, cancellation, error semantics, resource cleanup, boundary validation, and dependency direction.
8. Update manifests, exports, scripts, generated outputs, tests, documentation, CI, and deployment/runtime configuration only when the authorized boundary requires them.
9. Run focused type, behavior, and lint/format checks first. Run broader repository gates only when proportional to the changed surface or required for final acceptance. Record unavailable runtime proof as `Not verified`.
10. Report the exact changed scope, selected runtime profile, authorities, validation evidence, worktree drift, exclusions, and unresolved gaps. Implementation emits no Git delivery receipt.

## Runtime Profiles

- **Node.js:** preserve the declared engine floor, ESM/CommonJS boundary, Node APIs, process lifecycle, streams, workers, and package export conditions.
- **Bun:** use Bun-native APIs only when the repository or task selects Bun; preserve Node compatibility when it is part of the contract.
- **Deno:** preserve permission declarations, import resolution, Web-standard APIs, tasks, and deployment/runtime compatibility.
- **Mixed runtime:** activate only when the repository explicitly supports more than one runtime. Verify each claimed runtime separately; one passing runtime does not prove parity.

## Do Not Use For

- Browser components, DOM behavior, CSS, client state, accessibility, or visual implementation; use `dev-frontend`.
- Read-only diagnosis, security assessment, architecture audit, or fixed-basis review; use the host diagnosis flow or `repo-review` as appropriate.
- Product/UI specification, repository mapping, or Git staging/commit/push work.
- Java, Rust, or another language whose source owner already exists.

## Hard Rules

- Follow the repository-pinned runtime, package manager, lockfile, module system, TypeScript configuration, formatter, linter, test runner, and generation commands.
- Keep strictness at least as strong as the repository baseline. Do not use `any`, unchecked casts, non-null assertions, broad suppression, or silent fallback to bypass a contract without a narrow documented reason and boundary test.
- Validate untrusted input at runtime; TypeScript types alone do not prove runtime shape. Preserve the repository's existing validation authority and error mapping.
- Make async ownership explicit. Do not float promises, swallow rejections, leak timers/listeners/streams/workers, blindly retry non-idempotent operations, or leave cancellation and shutdown undefined.
- Do not add a runtime-specific API merely because it is shorter. Select it from the runtime profile and compatibility contract.
- Preserve unrelated local changes. Do not mutate Git state; hand fixed-scope changes to review and delivery owners.

## Validation Model

- **Baseline:** repository-defined format/lint, type-check, and focused behavior tests for the changed seam.
- **Boundary checks:** add contract/schema generation, API/CLI integration, persistence, concurrency/cancellation, packaging, or multi-runtime parity checks only when the changed surface reaches them.
- **Full gate:** use workspace-wide builds/tests and release checks for final acceptance, explicit user request, or when no credible focused check exists.

Never claim a runtime, type, test, or compatibility gate passed when its command, dependency, fixture, or target runtime was unavailable.

## Output Contract

Report capability `typescript.source.implement`; input and result package refs when integration is active; scope and changed files; detected runtime/profile, package manager, module system, TypeScript/test contracts, and authority chain; reuse/extension/new-interface decision; validation commands and outcomes; worktree drift; exclusions; and `Not found` or `Not verified` gaps.

## References

- [usage.md](references/usage.md) — triggers and routing boundaries.
- [runtime-profiles.md](references/runtime-profiles.md) — Node.js, Bun, Deno, and mixed-runtime decisions.
- [checklist.md](references/checklist.md) — implementation and evidence checklist.
- [behavior-first.md](references/behavior-first.md) — vertical red-green slices when an honest seam exists.
- [codebase-design.md](references/codebase-design.md) — public seams and dependency design when materially affected.
- [code-quality.md](references/code-quality.md) — evidence-gated cleanup and abstraction work.
- [project-grounding.md](references/project-grounding.md) — reachable runtime, packaging, API, persistence, security, or deployment boundaries.
- [eval-cases.md](references/eval-cases.md) — routing and quality evals.
