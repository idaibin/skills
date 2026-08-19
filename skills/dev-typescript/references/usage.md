# Usage

## Trigger

Use `dev-typescript` for authorized non-browser TypeScript or JavaScript implementation in services, APIs, CLIs, MCP servers, workers, libraries, build tools, and engineering automation running on Node.js, Bun, or Deno.

## Route Elsewhere

- React/Vue/Svelte components, DOM, CSS, browser state, accessibility, and visual work: `dev-frontend`.
- Read-only fixed-basis assessment: `repo-review` or the applicable audit owner.
- Unknown root cause with no edit authorization: host diagnosis flow.
- Git commit, push, merge, or cleanup: `repo-delivery`.

## Examples

- `Implement this Fastify plugin and its type-provider tests.` → `dev-typescript`.
- `Add a Bun CLI command using the existing config and error contracts.` → `dev-typescript` with Bun profile.
- `Fix this Deno worker permission and cancellation behavior.` → `dev-typescript` with Deno profile.
- `Implement this React hook and component state.` → `dev-frontend`.
- `Audit this Node service without editing.` → read-only review/audit path.
