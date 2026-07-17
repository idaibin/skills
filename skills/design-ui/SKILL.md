---
name: design-ui
description: "Use when a project needs evidence-grounded UI direction, a project UI profile, scoped reference analysis, task briefs, design tokens, component maps, versioned design assets, or an evaluation contract before frontend source implementation."
---

# UI Design

## Overview

Turn product facts, existing UI evidence, and explicitly scoped references into a versioned UI design package. Own design decisions and task-local assets only; route source edits to `implement-frontend`, runtime evidence to `ops-browser` or `ops-client`, and read-only implementation audits to `audit-frontend`.

## Workflow

1. Read effective repository guidance and run `git status --short` before planning artifacts.
2. Identify product, audience, platform, primary user job, target surface, current component system, available states, data facts, and forbidden inventions.
3. Inspect the smallest useful set of current screenshots, routes, components, tokens, DTOs, and analogous surfaces. Say `Not found` or `Not verified` for missing evidence.
4. Select one primary mode: **profile**, **task**, **reference**, or **evaluation**. Supporting outputs may be included only when needed by that mode.
5. Assign each reference an explicit `use` and `ignore` list plus source and rights status. Never treat a reference as authorization to copy brand, content, or functionality.
6. Create one coherent visual direction: named palette, typography roles, layout concept, density, material, interaction tone, and one justified signature element. Preserve product truth over decoration.
7. Treat `assets/ui-package.schema.json` as the package contract, then produce or update the project profile, task brief, reference registry, design tokens, component map, evaluation, and manifest from `assets/templates/`.
8. Separate deterministic acceptance checks from visual or experience judgment. Apply hard blockers before weighted scoring.
9. Version every input and output in the manifest. Never overwrite the last accepted revision without preserving rollback.
10. Validate the package with `scripts/validate_ui_artifacts.py`, then hand off source work and runtime proof to their owning skills.

## Modes

- **Profile:** establish durable project-specific visual and product constraints.
- **Task:** define one surface, scope, states, facts, tokens, component map, and acceptance contract.
- **Reference:** extract selected layout, material, typography, interaction, or component principles with rights and ignore boundaries.
- **Evaluation:** score a design or rendered implementation using deterministic gates plus calibrated human/model judgment.

## Do Not Use For

- Frontend source changes or refactors; use `implement-frontend` with the accepted design package.
- General future implementation decomposition without UI asset ownership; use `code-planner`.
- Read-only frontend implementation audits; use `audit-frontend`.
- Browser screenshots, console/network evidence, or desktop-window operation; use `ops-browser` or `ops-client`.
- Git staging, commits, pushes, or branch cleanup; use `repo-delivery` after review.

## Hard Rules

- Do not invent metrics, features, routes, permissions, states, or backend behavior.
- Do not create a parallel component library or token system when the project already has an owner.
- Keep the reusable Skill style-neutral; put product colors, geometry, references, and brand rules in the project profile.
- Require `source`, `rights_status`, `use`, and `ignore` for every external reference.
- Require loading, empty, error, populated, and permission states when applicable; explicitly justify exclusions.
- Keep generation, browser, time, cost, and storage budgets finite.
- Treat model ratings as advisory. Deterministic failures and human rejection cannot be averaged away.
- Do not edit product source, stage files, commit, push, publish, or approve a baseline under this skill.

## Output Contract

Report the selected mode, evidence basis, product/audience/job, fact boundary, reference responsibilities and rights, visual direction, profile/task revisions, token and component owners, required states, deterministic gates, weighted score, hard blockers, budgets, rollback target, validation command/result, handoffs, and `Not verified` gaps.

## References

- See [references/usage.md](references/usage.md) for routing and artifact examples.
- See [references/workflow.md](references/workflow.md) for design and handoff details.
- See [references/artifact-contract.md](references/artifact-contract.md) for fields and version rules.
- See [references/evaluation-rubric.md](references/evaluation-rubric.md) for blockers and scoring.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
