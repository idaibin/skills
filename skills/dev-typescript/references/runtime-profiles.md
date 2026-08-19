# Runtime Profiles

Select a profile from repository evidence, not from filename extensions or personal preference.

## Node.js

- Read `engines`, package-manager metadata, `type`, exports/imports maps, tsconfig inheritance, scripts, and CI versions.
- Preserve ESM/CommonJS interop and conditional exports. Test the consumer form that changed.
- Treat process signals, child processes, streams, workers, timers, and open handles as owned resources with explicit cleanup.
- Do not use an API newer than the declared engine floor without an authorized engine change and compatibility evidence.

## Bun

- Select Bun only when `bun.lock`, scripts, imports, CI, deployment, or the task makes it authoritative.
- Prefer an existing Bun-native API when it is already the local convention and does not violate required Node compatibility.
- Test Bun-specific behavior with Bun. A TypeScript check or Node test is not Bun runtime evidence.
- Keep lockfile and package-manager ownership singular; do not generate an npm/pnpm/yarn lockfile beside an authoritative Bun lockfile.

## Deno

- Read `deno.json`, import maps, tasks, permissions, lint/fmt settings, and deployment target.
- Preserve least-privilege permission requirements and Web-standard APIs where they are authoritative.
- Test import resolution and the actual permission boundary; a type check without runtime permissions is incomplete evidence.

## Mixed Runtime

Use only when multiple runtimes are explicitly supported. Identify the shared contract and isolate runtime adapters. Run the applicable behavior in every runtime claimed by the change, or mark missing parity evidence `Not verified`.

## Runtime Change Gate

Changing runtime, package manager, module system, engine floor, or lockfile authority is a compatibility migration, not incidental cleanup. Require explicit scope, affected consumers, rollout/rollback expectations, and focused compatibility evidence before proceeding.
