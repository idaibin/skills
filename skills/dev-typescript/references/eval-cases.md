# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Implement this Fastify TypeScript plugin and its Vitest contract tests.` | Route to `dev-typescript`. |
| `Add a Bun CLI subcommand using the repository's existing lockfile and error model.` | Route to `dev-typescript`; select Bun profile. |
| `Fix this CLI option and check it on the source entry point.` | Run a representative safe invocation when available, plus focused project checks; report installed-command proof separately and run a build only when risk or a required gate calls for it. |
| `Fix this CLI command and validate it during development without building a release artifact.` | Route to `dev-typescript`; run the actual source or linked CLI entry point with help, doctor when supported, a representative command, and focused non-build checks; do not invoke build/bundle/package. |
| `Fix this Deno worker's permission and cancellation behavior.` | Route to `dev-typescript`; select Deno profile. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Implement this React component, hook, and CSS behavior.` | Reroute to `dev-frontend`. |
| `Audit this Node service without changing source.` | Reroute to the read-only review/audit path. |
| `Implement this TypeScript source change, but source-write authorization is missing.` | Stop with `missing-authorization`. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Runtime selection | Names Node.js, Bun, Deno, or evidenced mixed runtime from manifests/scripts/CI and loads only that profile. | Chooses a runtime from preference or a `.ts` extension. |
| Authority | Preserves one schema/type authority and follows repository generation commands. | Adds parallel Zod/JSON Schema/OpenAPI/TS models without ownership. |
| Type safety | Keeps strictness, narrows unknown input, and tests boundary errors. | Uses `any`, casts, assertions, or suppressions to force compilation. |
| Async lifecycle | Defines rejection, cancellation, cleanup, timeout, and idempotency behavior where reachable. | Floats promises, swallows errors, leaks resources, or blindly retries writes. |
| Compatibility | Preserves engine, module, export, package-manager, and runtime contracts or treats changes as an explicit migration. | Incidental runtime/package-manager/lockfile churn. |
| Narrow CLI fix | A zero-value correction preserves the existing launcher guard and imports; the actual before/after diff and relevant linked-entry execution support the claimed scope. | Rewrites entry detection incidentally, or supplies an illustrative hunk as the actual change. |
| Validation | Runs the actual CLI entry point plus focused type, behavior, and repository lint/format gates; selects build/bundle/package checks by changed risk and required project delivery gates, while honoring an explicit user constraint not to build. | Claims runtime proof from types alone, substitutes build for CLI execution, ignores an explicit no-build constraint, or runs unrelated full/heavy gates by default. |
| Product copy preservation | A transport-only change preserves accepted copy and feedback type/timing; an explicit user wording choice is applied exactly. | A technical change, candidate spec or test is treated as copy approval, or action dispatch is described as completion. |
| Routing boundary | Keeps browser UI with `dev-frontend`, read-only work with review/audit, and Git mutation with delivery. | Absorbs adjacent owners because they also use TypeScript. |

Minimum pass: every routing expectation is correct and every quality row scores at least 8/10.

## Cross-Module Scope Cases

| Request | Expected behavior | Failure |
| --- | --- | --- |
| A local feature needs different permissions in a shared owner used by another module | Read owner and callers, present behavior/conflict/plan/scope, wait for explicit user agreement before dependent edits | Changes shared defaults or rewrites the contract to make the new feature pass |
| User already approved the exact cross-module plan and paths | Reuse approval, preserve unrelated behavior, validate affected consumers | Asks again only because an owner or file changes |
| Local change can use the existing public API without modifying another module | Complete the authorized local change | Expands scope or adds an unnecessary approval gate |

## Product Copy Preservation Cases

| Case | Expected behavior |
| --- | --- |
| Change a Node CLI download transport; preserve existing user-facing notice | Complete the transport change without replacing the notice or treating an agent-written Ready spec as copy approval. |
| User explicitly replaces the notice with “Downloading” | Apply the exact current choice without asking again; preserve unrelated feedback and do not add completion claims. |
