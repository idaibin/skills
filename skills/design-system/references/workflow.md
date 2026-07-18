# Design System Workflow

## Contents

1. Evidence boundary
2. Mode-specific baseline
3. Direction pass
4. Artifact pass
5. Evaluation and promotion

## Evidence boundary

Record confirmed requirements, available data/actions/states, current components and tokens, explicit exclusions, and unresolved questions. Screenshots prove appearance only. DOM, source, API, console, network, accessibility, and native-window claims require their own evidence.

## Mode-specific baseline

- **Create:** prove that no accepted owner exists, then define the minimum durable profile and token/component vocabulary the project needs.
- **Extract:** inventory representative real surfaces and distinguish repeated design rules from one-off implementation details.
- **Maintain:** resolve the accepted revision, identify the evidence that changed, and preserve a rollback target before editing artifacts.
- **Task:** keep durable profile changes separate from one-surface tokens, component decisions, states, and acceptance rules.
- **Evaluate:** resolve the accepted contract first; if implementation evidence is required, request it from the runtime or audit owner instead of inventing it.

## Direction pass

Define:

- **Subject:** product, audience, and the surface's single job.
- **Palette:** four to six named semantic colors with hex values.
- **Type:** display, body, and utility/data roles using available project fonts.
- **Layout:** shell, content owner, density, focus, scroll owner, and target sizes.
- **Material:** solid, translucent, native, or mixed with explicit limits.
- **Motion:** one coherent motion idea tied to state, hierarchy, or subject, with a reduced-motion alternative.
- **Signature:** one memorable detail rooted in the product's actual work.
- **Language:** user-recognizable terms, consistent action names, and actionable empty/error states.

Critique the direction before creating assets. Replace any decision that could be pasted unchanged into an unrelated dashboard or desktop utility. Spend visual boldness on one justified signature, remove unsupported decoration, and reject a direction whose complexity exceeds the implementation budget. Load `visual-direction.md` for the full direction and self-critique method.

## Artifact pass

1. Update `profile.yaml` only for durable project facts.
2. Register each reference with source, rights, `use`, and `ignore`.
3. Create a task brief with route/window, scope, facts, states, budgets, and acceptance.
4. Derive task tokens from existing owners. Mark every new token with an owner and reason.
5. Map components to `reuse`, `adapt`, or `create`; explain every `create`.
6. Create an evaluation file and a versioned manifest.

## Evaluation and promotion

Run deterministic gates first. If a gate fails, status is `rejected` regardless of score. Then score product truth, user-task completion, information architecture, visual coherence, layout/components, interaction/states, engineering fit, and evidence completeness. Promotion requires human approval and preserves the previous accepted revision for rollback.
