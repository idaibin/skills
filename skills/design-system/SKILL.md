---
name: design-system
description: "Use when a project needs an evidence-grounded design system or intentional visual direction created, extracted, maintained, or evaluated as versioned profiles, tokens, component maps, task briefs, and acceptance contracts before frontend implementation."
---

# Design System

## Overview

Turn product facts, existing UI evidence, and explicitly scoped references into a versioned, repository-owned design system. Own creation, extraction, maintenance, task design, and design evaluation; route product-source edits to `implement-frontend`, runtime evidence to `ops-browser` or `ops-client`, and read-only implementation audits to `audit-frontend`.

## Workflow

1. Read effective repository guidance and run `git status --short` before planning artifacts.
2. Identify product, audience, platform, primary user job, target surface, current component system, available states, data facts, and forbidden inventions.
3. Inspect the smallest useful set of current screenshots, routes, components, tokens, DTOs, and analogous surfaces. Say `Not found` or `Not verified` for missing evidence.
4. Select one primary mode: **create**, **extract**, **maintain**, **task**, or **evaluate**. Supporting outputs may be included only when needed by that mode.
5. Assign each reference an explicit `use` and `ignore` list plus source and rights status. Never treat a reference as authorization to copy brand, content, or functionality.
6. Create one coherent, subject-specific visual direction: named palette, typography roles, layout concept, density, material, interaction tone, and one justified signature element. Reject interchangeable AI-design defaults and preserve product truth over decoration. Load `references/visual-direction.md` when creating or materially reshaping that direction.
7. Treat `assets/ui-package.schema.json` as the package contract, then produce or update the project profile, task brief, reference registry, design tokens, component map, evaluation, and manifest from `assets/templates/`.
8. Separate deterministic acceptance checks from visual or experience judgment. Apply hard blockers before weighted scoring.
9. Version every input and output in the manifest. Never overwrite the last accepted revision without preserving rollback.
10. When Python and PyYAML are available, validate the package with `scripts/validate_ui_artifacts.py`; otherwise report artifact validation as `Not verified` without installing dependencies implicitly. Then hand off source work and runtime proof to their owning Skills.

## Modes

- **Create:** establish a new repository-owned profile, token vocabulary, component principles, states, and acceptance rules from verified product context.
- **Extract:** derive reusable design rules from existing screenshots, routes, components, tokens, and scoped references without treating appearance as runtime proof.
- **Maintain:** revise an existing design system, preserve accepted history, and record why durable rules changed.
- **Task:** define one surface, scope, states, facts, tokens, component map, and acceptance contract for later implementation.
- **Evaluate:** judge a design proposal or rendered result against the accepted system using deterministic gates plus calibrated human/model judgment; implementation-code findings remain owned by `audit-frontend`.

## Do Not Use For

- Frontend source changes or refactors; use `implement-frontend` with the accepted design package.
- General future implementation decomposition without UI asset ownership; use the host's built-in planning.
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
- See [references/visual-direction.md](references/visual-direction.md) for distinctive visual direction, interface writing, motion, restraint, and self-critique.
- See [references/artifact-contract.md](references/artifact-contract.md) for fields and version rules.
- See [references/evaluation-rubric.md](references/evaluation-rubric.md) for blockers and scoring.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
