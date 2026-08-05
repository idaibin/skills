# Documentation Authority Optimization Plan

## Objective

Keep `product-spec`, `ui-spec`, `repo-map`, and `repo-review` capable of rebuilding
project documentation into one current, navigable authority system without copying
task history, inventing product facts, duplicating visual systems, or creating an
unowned machine-readable source of truth.

## Work packages

### Product specification

- Treat durable product documents as current terminal contracts; Git owns history.
- Support one foundation plus independently loadable slices when user jobs, rules,
  permissions, failure semantics, or acceptance differ.
- Keep technical enums, routes, DTOs, layout, and visual tokens outside Product Specs.
- Gate every implementation slice as `Ready`, `Partial`, `Not Ready`, or `Not found`
  without deriving missing product approval from source code.
- Admit YAML/JSON/Schema only with owner, producer, consumer, semantic version,
  validator, drift policy, and retirement rule.

### UI specification

- Resolve `<design-root>` from effective guidance and shared consumers rather than
  assuming the Git root or creating one `DESIGN.md` per application.
- Keep one shared `DESIGN.md` per proven visual boundary and one independently
  loadable UI contract per page domain or connected flow.
- Preserve selected-source identity, named approval, rights, `use`/`ignore`, viewport,
  evidence level, current-runtime delta, accessibility, and readiness.
- Store task captures and visual evidence under an ignored `.codex/artifacts/`
  location unless the durable-evidence lifecycle gate is fully satisfied.
- Run pinned Google DESIGN lint/diff against the resolved design-root.

### Repository map

- Keep one root navigation authority with bounded maps for applications, boundaries,
  contracts, domains, design bindings, and reusable providers only when justified.
- Separate canonical/source owner, build/deploy owner, runtime identity, and
  gateway/registration alias.
- Map repository-native HTTP authority and consumers; do not require or copy OpenAPI
  unless an adopted generation, validation, compatibility, and consumer pipeline exists.
- Reconcile all indexes, links, owners, consumers, deletions, and stale references
  when a full rebuild is explicitly authorized.

### Repository review

- Activate Documentation Authority Review whenever a basis creates, restructures,
  moves, deletes, or claims completion of authoritative documentation.
- Review Standards and Spec independently and reject current-basis self-assertion as
  proof of product approval, runtime behavior, or migration safety.
- Check terminal-current content, navigation closure, authority separation,
  transient evidence placement, sidecar admission, ownership identities, and
  deleted/untracked paths.
- Freeze a new complete basis after every fix and replay the failing checks before
  issuing a final verdict.

## Cross-package acceptance gates

1. Shared protocols and every generated consumer copy are synchronized.
2. Catalog metadata routes terminal rebuild, design-root, source/runtime mapping,
   and documentation-authority review without displacing implementation Skills.
3. Trigger/non-trigger evals cover the four owners and known routing conflicts.
4. Documentation-authority tests reject root-only DESIGN assumptions, dated version
   defaults, unmanaged sidecars, and stale review-basis closure.
5. `bash scripts/check-skills.sh`, package discovery, `git diff --check`, independent
   mutual review, remote-main equality, and global-install parity all pass.

## Project canary loop

For each future iteration:

1. Fix a current Worktree or immutable project basis and declare exclusions.
2. Apply the installed Skills to one real multi-surface project without editing code
   unless implementation is separately authorized.
3. Validate document structure, links, DESIGN, authority boundaries, source facts,
   transient-evidence placement, and structured-artifact lifecycle.
4. Run independent project-truth and cross-Skill reviews on the repaired basis.
5. Convert only repeated, portable failures into Skill, protocol, routing, or eval
   changes; keep project-specific facts in the project.
6. Re-run the Skill suite, merge reviewed task commits into `main`, push, install from
   published `main`, and compare every installed file with its source.
7. Update the companion validation report with current reusable outcomes and explicit
   `Not verified` boundaries; do not append a task chronology.

## Current iteration boundary

The frontend-unify canary has completed all static documentation, Skill suite,
mutual-review, remote delivery, and global-install parity gates. Browser, SSO,
gateway registration, deployment, production permissions, and live-object behavior
remain outside this documentation-only iteration. Context-size warnings for
`repo-map` and `repo-review` remain a monitored optimization candidate, not a failed
behavior gate.
