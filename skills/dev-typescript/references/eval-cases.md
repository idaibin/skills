# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Implement this Fastify TypeScript plugin and its Vitest contract tests.` | Route to `dev-typescript`. |
| `Add a Bun CLI subcommand using the repository's existing lockfile and error model.` | Route to `dev-typescript`; select Bun profile. |
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
| Validation | Runs focused type, behavior, and repository lint/format gates, then proportional boundary checks. | Claims runtime proof from types alone or runs unrelated full/heavy gates by default. |
| Routing boundary | Keeps browser UI with `dev-frontend`, read-only work with review/audit, and Git mutation with delivery. | Absorbs adjacent owners because they also use TypeScript. |

Minimum pass: every routing expectation is correct and every quality row scores at least 8/10.
