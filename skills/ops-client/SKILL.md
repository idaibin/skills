---
name: ops-client
description: "Use when explicitly authorized desktop-client operation or native-window evidence is needed; not for browser proxies, source implementation, diagnosis-only work, or Git delivery."
---

# Client Operations

## Entry Gate

Operate a named desktop client only after confirming target process/window/build, adapter capability, allowed side effects, and evidence boundary. Installation, process, window, menu, and runtime behavior are separate claims.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Launch/inspect/interact/capture a client | [usage](references/usage.md) | Verified client-layer evidence or safe stop |
| Need examples/edge cases | [usage](references/usage.md) | Correct mode/boundary |

## Invariants

- Do not substitute browser, build, process, or menu evidence for real native-window acceptance.
- Attempt the user-named app before aliasing; report checked sources rather than declaring machine-wide absence.
- Keep diagnostics, source fixes, browser behavior, and Git mutation with their owners; clean disposable probes.

## Output Map

Return app/process/window/build identity, authorized actions, direct evidence, cleanup, and `Not verified` claims.

## Reference Map

- Read [usage](references/usage.md) for client modes, targeting, safety, evidence, and stop conditions.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
