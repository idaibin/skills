# UI Specification Artifact Contract

`assets/ui-spec-package.schema.json` is the single machine-readable source for required package files and top-level fields. Templates are examples of that contract; the validator reads the schema instead of carrying a second required-field list.

## Contents

1. Durable files
2. Task files
3. Version and rights rules
4. Budgets and recovery

## Durable files

`profile.yaml` owns the accepted visual-source baseline, product, platform, audience, principles, layout, surface, typography, density, preferred/restricted patterns, state requirements, implementation boundaries, and avoided patterns.

`references.yaml` owns stable reference identifiers, source URLs or local paths, rights status, `use`, `ignore`, and whether a local copy may be committed.

## Task files

`task.yaml` owns one selected visual source, target surface, goal, include/exclude scope, available/unavailable facts, reference use, required states, target sizes, acceptance, and budgets.

`design-tokens.json` owns only values needed by this task. Reuse existing token names and record the canonical source.

`component-map.json` classifies each element as `reuse`, `adapt`, or `create` and records its source path or creation reason.

`evaluation.yaml` separates deterministic results, hard blockers, weighted criteria, score, decision, reviewer, and remaining gaps.

`artifact-manifest.yaml` binds repository/ref, selected-source identity, input revisions, output paths and hashes, evaluation revision, approval, effort, and rollback target.

## Version and rights rules

- Increment the relevant revision when a profile, task, selected source, reference set, token set, mapping, or rubric changes.
- Never overwrite an accepted manifest in place.
- Mark third-party images `reference-only` unless separate evidence permits redistribution.
- Keep code license and reference-content rights separate.
- Preserve the selected visual source unchanged; new alternatives or edits belong to Product Design.

## Budgets and recovery

Every task declares finite inspection, revision, duration, and storage limits. Preserve the last accepted revision, allow resume from the last complete step, and require explicit approval before promotion or destructive cleanup.
