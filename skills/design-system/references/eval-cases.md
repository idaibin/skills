# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Create the first design system for this product from verified routes, components, and user jobs.` | Trigger `design-system` Create mode. |
| `Extract the durable tokens and component rules already used across these representative screens.` | Trigger Extract mode without claiming screenshots prove runtime behavior. |
| `Update the accepted design profile for the new dense-data surface and preserve the rollback revision.` | Trigger Maintain mode. |
| `Use image A only for material and B only for layout; produce tokens and a task brief.` | Trigger Task mode with explicit use/ignore and rights fields. |
| `Design a new operations page from real routes and DTOs, but do not edit source yet.` | Trigger Task mode and preserve fact boundaries. |
| `Give this new product a distinctive visual direction rooted in its audience and subject, then define the tokens, states, and acceptance contract before code.` | Trigger Create or Task mode, reject interchangeable defaults, and keep source mutation out of scope. |
| `Compare these three UI variants with deterministic gates, cost, and a 100-point rubric.` | Trigger Evaluate mode. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Implement the accepted UI package in this React app.` | Prefer `implement-frontend`; consume `design-system` assets. |
| `Audit the changed frontend for accessibility and token drift.` | Prefer `audit-frontend`. |
| `Plan a backend, frontend, migration, and CI rollout.` | Do not trigger this Skill; use the host's built-in planning. |
| `Open the page and capture console, network, and screenshots.` | Prefer `ops-browser`. |
| `Launch the Tauri app and prove the real window.` | Prefer `ops-client`. |
| `Commit and push the accepted UI changes.` | Prefer `repo-delivery`. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Grounding | records product, audience, job, data/actions/states, components, tokens, and gaps from source evidence | invents a generic dashboard brief |
| Mode | selects create, extract, maintain, task, or evaluate and applies its evidence baseline | blends modes until ownership and acceptance are unclear |
| Reference scope | every reference has source, rights, use, and ignore | says only `make it look like this` |
| Direction | defines palette, type roles, layout, material, density, and one product-rooted signature | defaults to unrelated neon, glass, hero, or KPI cards |
| Differentiation | traces the visual thesis and one justified aesthetic risk to the subject, then removes interchangeable or unsupported decoration | copies a fashionable preset or spends boldness across unrelated effects |
| Interface language | uses recognizable concepts, consistent action names, and actionable empty/error states | uses generic labels, filler copy, or contradictory action vocabulary |
| Responsive interaction | specifies target sizes, focus, reduced motion, overflow, and realistic content behavior | treats one polished desktop screenshot as a complete design |
| Project isolation | durable style lives in the project profile, not the reusable Skill | hardcodes one product's colors or geometry in the Skill |
| Reuse | component map checks existing owners before adapt/create | creates another kit or token layer |
| Fact boundary | distinguishes available and unavailable product capabilities | turns visual references into features |
| States | covers applicable loading, empty, error, populated, permission, focus, and reduced motion | approves a single happy screenshot |
| Evaluation | deterministic blockers precede weighted judgment | averages away build, overflow, rights, or truth failures |
| Versioning | manifest binds revisions, paths, generation identity, approval, cost, and rollback | overwrites accepted assets or omits promotion owner |
| Authority | writes design assets only and hands off source/runtime/Git work | edits product source, launches clients, or commits |

## Scoring

Score each quality case 0–10. Minimum pass: trigger/non-trigger routing is correct, every quality case scores at least 8, no hard blocker exists, and all required artifact templates validate.
