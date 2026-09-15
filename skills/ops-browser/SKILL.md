---
name: ops-browser
description: "Use when explicitly authorized browser operation or same-state runtime visual evidence is needed; not for ordinary frontend implementation, UI specification, or unauthorized browser state changes."
---

# Browser Operations

## Entry Gate

Operate only an explicitly authorized browser surface. Preflight browser/profile/tab, target URL/state, account/identity boundary, and allowed side effects; stop if the exact target cannot be identified or authorization is absent.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any browser operation | [platform operations](references/platform-operations.md), [tab lifecycle](references/tab-lifecycle.md), and [viewport policy](references/viewport-policy.md) | Bounded target operation at a verified viewport |
| Local workspace/browser ownership applies | [local workspaces](references/local-browser-workspaces.md) | Verified target selection |
| Runtime visual comparison applies | [visual evidence](references/frontend-visual-evidence.md) | Same-state capture/comparison |
| DevTools/console/network debugging applies | [DevTools debugging](references/devtools-debugging.md) | Scoped observation |
| Axure/Lanhu evidence extraction applies | [Axure evidence](references/axure-product-evidence.md) and/or [Lanhu evidence](references/lanhu-ui-evidence.md) | Qualified source evidence |

## Invariants

- Inventory and identify the exact target before action; absent target with no creation policy is not verified.
- Separate read observation from side effects; never infer identity, authorization, or application acceptance from browser reachability.
- Preserve target/profile and avoid focus theft; report actual postcondition and unverified gaps.

## Output Map

Return surface/profile/tab identity, target state, authorized action, evidence/captures, postcondition, cleanup state, and gaps.

## Reference Map

- Read [platform operations](references/platform-operations.md), [tab lifecycle](references/tab-lifecycle.md), [viewport policy](references/viewport-policy.md), and [browser operation protocol](references/browser-operation-protocol.md) for every selected operation.
- Read [local workspaces](references/local-browser-workspaces.md), [visual evidence](references/frontend-visual-evidence.md), [DevTools debugging](references/devtools-debugging.md), [Axure evidence](references/axure-product-evidence.md), and [Lanhu evidence](references/lanhu-ui-evidence.md) only when applicable.
- Read [usage](references/usage.md) when selecting a backend or mode, performing a write, capture, recording, or download, or producing a protocol handoff. Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
