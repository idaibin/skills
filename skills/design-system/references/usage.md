# Design System Usage

## Use this skill for

- creating a repository-owned design system for a new product or surface;
- extracting durable rules from existing code, screenshots, tokens, and components;
- maintaining an accepted profile without overwriting its history;
- defining one page, window, tray, flow, or component redesign before code;
- creating a distinctive visual direction grounded in the product's subject, audience, and real work;
- explaining what to use and ignore from one or more reference images;
- deriving project-compatible tokens without creating a competing owner;
- comparing variants with deterministic gates, a weighted rubric, cost, and a recorded decision;
- preparing a complete design package for `implement-frontend`.

This Skill absorbs visual-direction guidance but does not own frontend source mutation. A request to design the contract and implement it routes from `design-system` to `implement-frontend`; a request to code an already accepted direction starts with `implement-frontend`.

## Typical chain

```text
repo evidence -> design-system -> implement-frontend
                              -> ops-browser or ops-client
                              -> audit-frontend
                              -> repo-review -> repo-delivery
```

Use the host's built-in planning first only when implementation needs a separate multi-package plan. Invoke `design-system` directly when the requested output is the repository-owned design contract. The Skill remains independently usable: it performs its own bounded evidence collection when no `repo-map` output exists.

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
