# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Build an implementation-ready contract for this selected mockup of the settings dialog.` | Trigger `ui-spec` Feature Spec. Record selected source and required states, responsive/accessibility rules, and per-slice readiness without generating images. |
| `Our accepted shared Button and spacing conventions changed across dashboard and settings; update the shared contract.` | Trigger `ui-spec` Design System Spec. Update repository-root `DESIGN.md`, then report lint and diff gates. |
| `Build a contract for this selected page in a new repo with no DESIGN.md yet.` | Trigger `ui-spec` and define how the root `DESIGN.md` is first established before readying any slice. |
| `Create a contract for one flow but do not copy tokens/component semantics from the shared source.` | Trigger `ui-spec` Feature Spec. Reference root `DESIGN.md` and reuse owner mapping instead of duplicating shared values in the slice artifact. |
| `The selected source has an unknown heading in DESIGN.md input.` | Keep the unknown heading preserved, report it in the notes, and do not fail parser behavior. |
| `A duplicate section appears in DESIGN.md while updating shared semantics.` | Use official diff/lint flow and treat duplicate section as an immediate error condition until resolved by source owner. |
| `Run lint before export and share the derived design output.` | Run lint first, require success without error, and treat export as explicit derived output only after shared authority is accepted. |
| `Specify this approved dialog so long localized content, intermediate widths, its critical action, inner scroll, and overlay behavior remain usable.` | Trigger `ui-spec` Feature Spec and add only the applicable task-completion geometry and acceptance rules. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Generate three visual alternatives for this dashboard and let me pick.` | Route to host Product Design; do not start `ui-spec` without selected source. |
| `Implement this slice in code now.` | Route to `dev-frontend`; consume implementation-ready `ui-spec` artifact. |
| `Critique this interface and redesign it.` | Route to Product Design or audit owner; do not do redesign in `ui-spec`. |
| `Collect runtime screenshots and network logs for the accepted surface.` | Route to `ops-browser` or `ops-client`; do not claim runtime evidence in `ui-spec`. |
| `DESIGN.md and the matching UI slice already exist; identify their file types before implementation.` | Let the consumer classify and read them directly; do not trigger `ui-spec` merely for recognition. |

## Scenario Eval

| Scenario | Correct decision | Reject if |
| --- | --- | --- |
| New repo has no root design authority and one selected slice exists | Copy the bundled template, fill only verified values, obtain named human approval, lint root `DESIGN.md`, record diff `Not applicable`, then proceed with slice readiness gates. | Invents token values, starts Feature Spec without an approved and linted root `DESIGN.md`, or fabricates a diff baseline. |
| Feature Spec only reuses accepted shared visuals | Reference root `DESIGN.md` semantics and avoid copying token/component values into slice file. | Copies shared token map or component semantics into the slice. |
| Shared visual semantics change for multiple domains | Update root `DESIGN.md`, run official lint and diff, report regression status, then gate readiness. | Treats change as local page styling only or skips lint/diff gate. |
| DESIGN.md has unknown section heading during review | Preserve the unknown section and continue with known ordered content. | Removes it silently or errors on unknown headings. |
| DESIGN.md has duplicate section heading | Reject with hard blocker until resolved. | Continues and marks Ready. |
| DESIGN.md lint or diff command cannot run due to missing permissions/network | Mark checks as `Not verified` and do not mark slice `Ready`. | Claims success without evidence and issues `Ready`. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Source gate | selected/accepted source recorded with identity, revision, approval, rights, `use`, `ignore` | starts without source identity or selected-source approval |
| Product truth | product goals, actions, states, and failures grounded and separated from design | invents product logic from mockup appearance |
| Design authority | root `DESIGN.md` is the sole shared semantic authority | introduces another shared design authority |
| Evidence precision | marks verified/extracted/proposed/`Not verified` and includes lint/diff outcomes | treats unknown values as verified facts |
| Design-system gate | shared changes require `@google/design.md@0.3.0` lint + diff and regression review | emits Ready without lint/diff or unresolved regression |
| Accessibility and responsive contract | defines focus, overflow, reduced-motion, localization, and acceptance for each slice | skips accessibility/responsive rules in contracts |
| Multi-surface gating | per-slice readiness plus shared index and explicit partial/complete status | uses one omnibus contract or one package-wide readiness only |
| Handoff | per-slice artifact and readiness delivered to dev-frontend with remaining gaps | omits per-slice readiness or unresolved blockers |

## Scoring

Score each quality case 0–10. Minimum pass:

- routing is correct
- every quality case score >= 8
- no hard blocker remains
- applicable DESIGN.md lint/diff gates pass before any `Ready` verdict; unavailable gates produce an explicit blocker and `Not verified`
