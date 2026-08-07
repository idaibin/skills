# Eval Cases

## Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Build an implementation-ready contract for this selected mockup of the settings dialog.` | Trigger `ui-spec` Feature Spec. Record selected source and required states, responsive/accessibility rules, and per-slice readiness without generating images. |
| `Our accepted shared Button and spacing conventions changed across dashboard and settings; update the shared contract.` | Trigger `ui-spec` Design System Spec. Resolve `<design-root>`, update its `DESIGN.md`, then report lint and diff gates. |
| `Build a contract for this selected page in a new repo with no DESIGN.md yet.` | Trigger `ui-spec`, resolve `<design-root>`, and define how its `DESIGN.md` is first established before readying any slice. |
| `Create a contract for one flow but do not copy tokens/component semantics from the shared source.` | Trigger `ui-spec` Feature Spec. Reference resolved `<design-root>/DESIGN.md` and reuse owner mapping instead of duplicating shared values in the slice artifact. |
| `Specify this settings page using its selected source; keep shared colors, spacing scale, global typography, radius, and Button semantics in DESIGN.md.` | Trigger `ui-spec` Feature Spec with page-level layout/state/interaction/component mapping only. |
| `This Git repository contains a shared frontend aggregate with two separately built apps; keep one accepted DESIGN.md at that aggregate.` | Resolve the aggregate as `<design-root>` from guidance and consumers; do not force the Git root or duplicate one file per app. |
| `Clean the final UI docs and move all old candidate evidence JSON out of formal docs.` | Keep the current UI contract durable and route historical evidence to verified ignored `.codex/artifacts/`. |
| `Specify this existing settings surface: preserve its brand and routes, keep one primary accent role, add dark mode only if the accepted contract requires it, and map shell/container/component padding without doubling the left or top inset.` | Trigger `ui-spec`; load visual-direction and layout governance, record Preserve mode, conditional dark-mode scope, semantic color exceptions, and the effective inset owner chain. |
| `The selected source has an unknown heading in DESIGN.md input.` | Keep the unknown heading preserved, report it in the notes, and do not fail parser behavior. |
| `A duplicate section appears in DESIGN.md while updating shared semantics.` | Use official diff/lint flow and treat duplicate section as an immediate error condition until resolved by source owner. |
| `Run lint before export and share the derived design output.` | Run lint first, require success without error, and treat export as explicit derived output only after shared authority is accepted. |
| `Specify this approved dialog so long localized content, intermediate widths, its critical action, inner scroll, and overlay behavior remain usable.` | Trigger `ui-spec` Feature Spec and add only the applicable task-completion geometry and acceptance rules. |
| `Admin only needs 1920x1080 verified; 1440x900 is useful if time permits, and mobile is outside this request.` | Trigger `ui-spec` Feature Spec with an Admin-local viewport matrix: `1920x1080` required, `1440x900` optional, mobile excluded with the user's request as evidence. Hand the unchanged matrix to implementation, audit, and runtime verification; do not make this a global default. |
| `The current runtime geometry differs from exact values in the approved source inspect panel.` | Keep source target and browser-computed runtime in separate delta columns; use inspect-panel values as `source-extracted` and do not call current geometry already aligned. |
| `Lanhu shows the same card gap as 16px three times and 17px once; use the default even-grid policy.` | Preserve all four source-extracted values, cluster only the same semantic gap, and target 16px with the recorded user policy; do not rewrite the 17px observation. |
| `Specify the catalog page with SearchBar, CatalogCard, DownloadDialog, and shared states; the project has component guidance and a concise project map.` | Keep page composition, page states, and interaction in the UI slice; use the guidance and project map to reach source owners, leave props/slots/events and tokens in their owners, and require live-source revalidation before implementation. |
| `Specify the dashboard UI from this accepted project screenshot.` | Trigger `ui-spec` with the screenshot as the selected visual source; a versioned project-owned screenshot referenced in the README is an accepted current UI surface. |

## Non-Trigger Eval

| Prompt | Expected |
| --- | --- |
| `Generate three visual alternatives for this dashboard and let me pick.` | Route to host Product Design; do not start `ui-spec` without selected source. |
| `Implement this slice in code now.` | Route to `dev-frontend`; consume implementation-ready `ui-spec` artifact. |
| `Critique this interface and redesign it.` | Route to Product Design or audit owner; do not do redesign in `ui-spec`. |
| `Collect runtime screenshots and network logs for the accepted surface.` | Route to `ops-browser` or `ops-client`; do not claim runtime evidence in `ui-spec`. |
| `DESIGN.md and the matching UI slice already exist; identify their file types before implementation.` | Let the consumer classify and read them directly; do not trigger `ui-spec` merely for recognition. |
| `No visual source or accepted UI surface is available; specify the UI anyway.` | For implicit routing, do not trigger `ui-spec`; route to `product-spec` for unresolved behavior or host Product Design for visual exploration. If `ui-spec` is explicitly invoked, stop as `evidence-incomplete`. Do not fabricate a visual source. |

## Scenario Eval

| Scenario | Correct decision | Reject if |
| --- | --- | --- |
| New repo has no resolved design authority and one selected slice exists | Resolve `<design-root>`, copy the bundled template, fill only verified values, obtain named human approval, lint `DESIGN.md`, record diff `Not applicable`, then proceed with slice readiness gates. | Invents token values, assumes Git root, starts without an approved and linted authority, or fabricates a diff baseline. |
| Feature Spec only reuses accepted shared visuals | Reference `<design-root>/DESIGN.md` semantics and avoid copying token/component values into slice file. | Copies shared token map or component semantics into the slice. |
| Page contract maps a selected source | Keeps page layout, states, interaction, responsive/accessibility behavior, and component mapping in the Feature Spec while linking shared colors/spacing/typography/radius/component meaning to `<design-root>/DESIGN.md`. | Turns the Feature Spec into a parallel design-system document or omits page-level implementation mapping. |
| Page contract uses component guidance and a project map | Names human-readable component roles, reads only relevant guidance/map entries, and verifies paths, registration, states, and interfaces in source. | Creates a component-ID registry for AI, copies props/slots/events or token values into the page spec, omits component composition, or treats a map row as live-source proof. |
| The project has a maintained page projection with human Markdown sources. | Preserve Product, page UI, and component Markdown as separate authorities; consume the projection only for its named non-LLM purpose and verify source reachability and drift lifecycle. | Requires a projection for ordinary UI work, lets it replace Markdown acceptance or cross-page guidance, or duplicates tokens/API/DTO/props/slots/paths. |
| A UI Markdown authority or local reference uses an absolute local path or escapes its declared owner/workspace root. | Reject the reference as non-portable before following it; require an owner-relative path whose resolved target remains inside the boundary. | Accepts the path because it exists on the current machine or because its lexical form is relative. |
| A relative UI Markdown authority or local reference is a symbolic link whose final target leaves the declared owner/workspace root. | Resolve the final target and reject the reference before consuming it, without introducing a schema requirement. | Checks only lexical containment. |
| Shared visual semantics change for multiple domains | Update `<design-root>/DESIGN.md`, run official lint and diff, report regression status, then gate readiness. | Treats change as local page styling only or skips lint/diff gate. |
| Valid evidence JSON exists under formal docs but has no durable team consumer | Move it to verified ignored `.codex/artifacts/`; keep current acceptance in the UI Spec. | Treats schema validity as publication authority or leaves candidate/final history in the index. |
| UI Spec ID or DESIGN version is an edit date | Remove the date-based revision unless the project has a semantic version policy; preserve business-effective dates only when they affect acceptance. | Uses the newest date as an authority rule or deletes a date that changes behavior. |
| DESIGN.md has unknown section heading during review | Preserve the unknown section and continue with known ordered content. | Removes it silently or errors on unknown headings. |
| DESIGN.md has duplicate section heading | Reject with hard blocker until resolved. | Continues and marks Ready. |
| DESIGN.md lint or diff command cannot run due to missing permissions/network | Mark checks as `Not verified` and do not mark slice `Ready`. | Claims success without evidence and issues `Ready`. |
| A desktop-only Admin acceptance request names one mandatory and one budgeted viewport | Matrix records viewport size/orientation, environment, state/fixture, assertions, and evidence source. `1920x1080` is required, `1440x900` is optional, and mobile is excluded only from this slice's acceptance scope. | Treats a skipped optional check as a failure, treats excluded mobile as an unsupported-device claim, or applies Admin sizes to unrelated surfaces. |
| Design tool cannot select an icon, but the screenshot can be viewed at 200% | Use the zoomed image only for `visually-inferred` comparison; keep exact icon size `proposed` or `Not verified`. | Copies the current runtime icon size or a pixel estimate into the target as verified. |
| Repeated Lanhu spacing differs by one pixel | Apply the even-grid rule only when at least three same-semantic samples have a strict even majority and every outlier is within 1px; keep raw evidence and approval separate from the target. | Pools unrelated gaps, rounds an odd majority arbitrarily, or applies the rule to widths, type, borders, radii, icons, or assets. |
| Every product currently uses one generic gradient icon | Specify real per-item asset ownership and only an isolated failed-item fallback. | Treats the current fallback as a normal visual asset strategy. |

## Quality Eval

| Case | Pass evidence | Reject if |
| --- | --- | --- |
| Source gate | selected/accepted source recorded with identity, revision, approval, rights, `use`, `ignore` | starts without source identity or selected-source approval |
| Product truth | product goals, actions, states, and failures grounded and separated from design | invents product logic from mockup appearance |
| Design authority | resolved `<design-root>/DESIGN.md` is the sole shared semantic authority for its proven boundary | assumes Git root, duplicates per app, or introduces another authority |
| Evidence placement | task evidence defaults to verified ignored `.codex/artifacts/`; durable publication passes the consumer/lifecycle gate | commits evidence under formal docs merely because it validates |
| Visual direction | Records a compact Design Read and only applicable dials; keeps one primary accent semantic role with state-color exceptions, makes dark mode conditional, and classifies Preserve versus Overhaul before changing an existing surface. | Installs `8/6/4` as a default, flattens semantic colors, mandates dark mode, or silently overhauls the existing brand/IA. |
| Nested inset ownership | Specifies shell, content-container, page, panel/component, and control ownership; records effective left/top/right/bottom inset and any flush-scrollbar exception without prescribing incidental DOM. | Adds the same page padding at parent and reusable component, ignores top/left alignment, or moves scrollbar inset to the wrong owner. |
| Evidence precision | marks `source-extracted`/`browser-computed`/`visually-inferred`/`proposed`/`Not verified` and includes lint/diff outcomes | treats unknown values as verified facts |
| Delta traceability | keeps source target, current runtime, and accepted contract separate with evidence IDs and uses design inspect values before screenshot estimates | promotes runtime computed values into source targets or summarizes them as safe-to-preserve design values |
| Measurement normalization | Retains every raw source value and evidence ID, records cluster semantics and policy authority, and normalizes `[16,16,16,17]` to a 16px target only under the bounded even-grid rule. | Erases the outlier, treats screenshot pixels as exact, mixes properties, or normalizes non-spacing measurements by default. |
| Design-system gate | shared changes require `@google/design.md@0.3.0` lint + diff and regression review | emits Ready without lint/diff or unresolved regression |
| Accessibility and responsive contract | defines focus, overflow, reduced-motion, localization, and acceptance for each slice | skips accessibility/responsive rules in contracts |
| Viewport acceptance scope | every applicable slice has required/optional/excluded entries with size, environment, state, assertions, and evidence source; current user requirements override older specs | calls one screenshot full coverage, omits the evidence source or state, or treats an excluded viewport as unsupported |
| Multi-surface gating | per-slice readiness plus shared index and explicit partial/complete status | uses one omnibus contract or one package-wide readiness only |
| Handoff | per-slice artifact and readiness delivered to dev-frontend with remaining gaps | omits per-slice readiness or unresolved blockers |
| End-of-work checklist | reports each binary readiness item by name (source fixed, DESIGN.md resolved, lint passed, delta table complete, viewport matrix complete, P1 asset owner, required state coverage, evidence levels tagged); evaluates in numeric order; returns `Not Ready` with the first failed item, `Partial` only when all eight pass but an explicitly non-blocking `Not verified` gap remains, and `Ready` only with all eight passed and no gap | collapses the checklist into a prose Ready, omits or skips the first failing item, downgrades a blocking unknown to `Partial`, or marks Ready with an unreported gap |

## Scoring

Score each quality case 0–10. Minimum pass:

- routing is correct
- every quality case score >= 8
- no hard blocker remains
- applicable DESIGN.md lint/diff gates pass before any `Ready` verdict; unavailable gates produce an explicit blocker and `Not verified`
