# UI Design Usage

## Use this skill for

- creating or revising a repository-owned UI profile;
- defining one page, window, tray, flow, or component redesign before code;
- explaining what to use and ignore from one or more reference images;
- extracting project-compatible tokens without creating a second design system;
- comparing variants with deterministic gates, a weighted rubric, cost, and a recorded decision;
- preparing a complete design package for `implement-frontend`.

## Typical chain

```text
repo evidence -> design-ui -> implement-frontend
                           -> ops-browser or ops-client
                           -> audit-frontend
                           -> repo-review -> repo-delivery
```

Use `code-planner` first only when the implementation itself needs a separate multi-package plan. A task can invoke `design-ui` directly when the requested output is the UI package.

## Artifact location

Prefer the repository's existing design directory. Otherwise use:

```text
docs/ui/
  profile.yaml
  references.yaml
  decisions.md
artifacts/ui/<task-id>/
  task.yaml
  design-tokens.json
  component-map.json
  evaluation.yaml
  artifact-manifest.yaml
```

Keep durable project facts under `docs/ui/`. Keep task-local generation and evidence under `artifacts/ui/` unless repository guidance chooses another owner.

## Handoff examples

- `implement-frontend`: accepted profile, task brief, tokens, component map, exact scope, hard blockers, and required states.
- `ops-browser`: target URL, viewport matrix, exact text/state assertions, console/network expectations, and screenshot paths.
- `ops-client`: launch command, expected app/window identity, target size, state fixture, and screenshot path.
- `audit-frontend`: accepted revision, changed surface, selected audit profiles, and design/implementation deltas to inspect.
