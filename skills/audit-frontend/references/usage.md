# Frontend Audit Usage

## Trigger Examples

- `Review this Console for duplicate tables, dialogs, spacing, stores, and request mechanisms.`
- `Audit this frontend architecture for component reuse, state ownership, accessibility, performance, and documentation drift; there is no current Git change set.`
- `Check whether this hook, service, or store belongs in the feature or shared layer.`
- `Audit this Vue 3 feature for SFC/API consistency, reactivity escape, watcher dependencies, provide/inject ownership, Router guard teardown, and keep-alive request cleanup.`
- `Audit this Tauri frontend boundary for progress, cancellation, errors, menus, and shortcuts.`
- `As a read-only specialist under code-review, inspect only the changed Vue files for state, lifecycle, accessibility, and performance risks.`

## Non-Triggers

- `Change this button label in the known component.` — prefer
  `implement-frontend`.
- `Find why this page crashes.` — prefer `diagnose` until the cause is known.
- `Verify the page in a browser.` — prefer `ops-browser`.
- `Review all dirty files, decide ownership, stage commits, and declare commit readiness.` — use `code-review` for the read-only inventory, staging plan, specialist coordination, and readiness decision, then `code-delivery` for authorized staging and commit creation. `audit-frontend` owns neither.
- `Review the current frontend diff for reuse, state, accessibility, and performance.` — `code-review` owns the read-only change-set review and may delegate an explicit frontend path to `audit-frontend`; `code-delivery` owns any later Git mutation.

## Expected Report

Lead with severity-ranked findings, then report direct-audit or specialist mode,
delegated paths and `code-review` read-only Git-change review owner when applicable, inspected evidence,
project class/framework profile, reuse candidates, ownership assessment,
state/reactivity/data/native boundaries, component/injection/router/lifetime
contracts, feedback states, token/layout owners, accessibility/performance
evidence, documentation lifecycle, validation, and residual `Not verified`
risks.
