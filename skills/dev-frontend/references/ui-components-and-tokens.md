# Project-Owned UI Components And Tokens

Load the consumer contract when adding, using, or recomposing UI components in a
page, route entry, or feature component, even when shared source is unchanged.
Load owner/adoption details only when that boundary changes. A copy-only change that
does not change composition or states does not activate this reference.

## Contents

- [Authority Chain](#authority-chain)
- [Consumer Contract](#consumer-contract)
- [Public API And Naming](#public-api-and-naming)
- [Shared Owner And Adopted Systems](#shared-owner-and-adopted-systems)
- [Theme And Token Changes](#theme-and-token-changes)
- [Project Checks And Completion](#project-checks-and-completion)

## Authority Chain

- Project-declared UI/design guidance owns shared visual semantics; use the resolved
  `DESIGN.md` when that is the adopted authority. Preserve explicit adoption and
  approval requirements; a Skill example or current screenshot cannot replace them.
- Feature UI specs own page composition, states, interaction, responsive behavior, and
  acceptance.
- Real component source and types own props, slots, events, DOM, accessibility, and
  runtime behavior.
- The project's actual token/variable source owns values and references. Follow its
  builder and generated consumers where present; plain maintained CSS variables do
  not require a structured token pipeline to be authoritative.
- A Component Registry is a maintained projection, not the component API authority.
- Any new durable structured projection requires a named owner, producer, non-LLM
  consumer, semantic version, executable validator, drift policy, and retirement rule.
  Otherwise consume the human contract and live source directly; maintained CSS
  variables alone do not require a projection.

## Consumer Contract

- Read the applicable project contract, actual public exports, component/types/styles,
  and an accepted consumer. Resolve supported variants, attribute forwarding, spacing
  responsibility, and feedback ownership before adding composition. Reuse the nearest
  maintained owner; no optional Registry or token pipeline is required to use a Button.
- Reuse required project controls through their public import. Apply this boundary to
  feature/local components as well as pages; moving a raw control into `components/`
  or giving it an approved name does not establish its source or compliance.
- Preserve semantic HTML and framework-native composition. Do not impose a blanket
  native-tag ban, fixed directory layout, or wrapper for every text/container. Apply a
  stricter component-only page policy only where the project actually adopts it.
  A wrapper must own stable semantics, styling policy, behavior, accessibility, or a
  real replacement/reuse boundary; rename-only pass-throughs are insufficient.
- Keep restricted third-party imports inside declared adapter roots. Resolve aliases,
  re-exports, and registered components when relevant. A bounded exception names the
  exact consumer/import, owner, reason, review condition, and expiry or retirement;
  do not broaden an allowlist or disable a rule to finish a page.
- Respect the project's permitted styling inputs. Arbitrary `class`, `className`,
  `style`, utility values, deep selectors, props spreads, Vue fallthrough attributes,
  or local wrappers must not bypass that policy. Preserve required native semantics,
  accessibility attributes, events, and refs when controlling forwarding.
- Keep page-only business composition local unless a real shared owner is justified.
  Do not create speculative primitive layers or extra DOM/component instances merely
  to satisfy a directory or tag rule, especially inside repeated list/table content.

## Public API And Naming

Apply these rules when authoring/changing APIs or names; consumers keep using the
established contract without redesigning it.

- Name components and actions for their actual purpose; preserve file casing, export
  convention, directory boundaries, and existing prefixes. Do not mass-rename or add
  a universal naming layer. Keep native attributes and framework event syntax intact.
- Express mutually exclusive modes through the established enum/variant or composition
  API. Keep independent booleans independent; do not create combinations that the
  implementation cannot meaningfully support or a page-specific universal component.
- Define supported defaults, state ownership, event payloads, slots, and forwarding at
  the public boundary. When exposed, distinguish controlled state from initial values;
  duplicate draft state requires explicit commit/reset behavior, not blind prop syncing.
- Keep basic controls free of unrelated business requests, routing, and global store
  policy. Put domain composition in its feature owner. Use compound components/context
  only for real coordinated consumers, and verify affected consumers for API changes.

## Shared Owner And Adopted Systems

- Read adoption records, token builders, Registry projections, and generated consumers
  only where the project adopts them. An absent optional record is not a blocker;
  a missing required record, stale approval, or decisive contract conflict still is.
  Continue unaffected authorized work without inventing a second UI authority.
- Preserve the project's declared token graph and consumer policy; do not assume a
  fixed number of tiers. Where `Component -> Semantic -> Primitive` is adopted, keep
  that direction and its consumer boundaries. Validate references, cycles, CSS
  custom-property self-reference, and generated drift through the actual project gate.
- Update owned contracts, projections, generated output, boundaries, and affected
  consumer checks only when their facts change. Keep complete APIs in source/types and
  token values in their actual definition; do not duplicate them in Markdown.

## Theme And Token Changes

- Reuse existing role-based tokens and keep their meaning stable across supported
  themes. Equal current values do not make text, border, surface, and feedback roles
  interchangeable. Add a component-specific token only for a real owned decision.
- Without an adopted token system, reuse current variables/constants. When reusable
  design decisions need extraction within scope, start with the smallest semantic set
  in the existing style owner; do not require JSON, a generator, new themes, or a Registry.
- Tokenize coordinated design choices, not every structural value such as `0`, `100%`,
  or `1fr`. Dynamic runtime data and component geometry responsibilities remain distinct
  from the token scale. Valid tokens alone cannot prevent duplicate inset.
- Trace theme/provider resolution and affected overlay/native-control consumers through
  the selected styling profile. Verify the changed roles in supported states/themes;
  changing token declarations or passing typecheck is not theme or contrast acceptance.

## Project Checks And Completion

- Discover existing commands and effective configuration in the project. Run the
  applicable required checks at the slice boundary, including for local edits.
  Missing tooling is `Not found` with coverage `Not verified`, never an invented pass.
- When implementing UI checks is authorized, extend the existing lint/style/test
  entrypoint before adding a CLI. Use the installed Vue template parser for Vue SFCs
  and the installed JSX/TypeScript parser for React; inspect style sources separately.
  Reuse supported restriction rules and add narrow custom AST rules only for gaps.
  Regex/text search is discovery, not proof of syntactic or resolved-import coverage.
- Bind naming, custom-property, and allowed-value checks to the project's actual style
  syntax and installed tools. Report coverage for SFC styles, preprocessors, CSS-in-JS,
  utility classes, and dynamic styles; scanning `.css` alone is not whole-UI coverage.
- Define checked consumers, public imports, covered native controls, permitted style
  inputs, and narrow implementation exceptions from the project contract. Cover
  feature components and actual style/render entrypoints; verify whether dynamic
  imports, auto/global registration, aliases, and re-exports are checked or report the
  gap. `no-restricted-imports` covers static import/export sources, not dynamic imports.
- For a new/changed gate, execute positive and negative cases: an accepted consumer
  passes; a covered raw control, direct restricted import, or forbidden override fails
  where that rule is adopted. An implementation exception must not exempt its
  consumers. Give diagnostics the allowed component/path or owning rule.
- Preserve narrow existing exceptions and legacy baselines without expanding them
  silently. Do not weaken assertions, add suppressions, widen component styling APIs,
  alter tokens, or accept new screenshots merely to turn a failure green. Intentional
  policy or baseline changes need their own authorized rationale and impact checks.
- Static checks cannot establish effective nested insets, visual equivalence, focus,
  scrolling, or responsive behavior. Use approved expectations and affected runtime
  evidence through the browser/client owner; report unexercised acceptance as
  `Not verified`. Passing checks cover only the rules and file set actually exercised.

Implementation references (verify against installed versions):
[Vue element restrictions](https://eslint.vuejs.org/rules/no-restricted-html-elements),
[ESLint import restrictions](https://eslint.org/docs/latest/rules/no-restricted-imports),
[ESLint AST restrictions](https://eslint.org/docs/latest/rules/no-restricted-syntax),
[Stylelint rules](https://stylelint.io/user-guide/rules/).
Token design reference: [Spectrum](https://spectrum.adobe.com/foundations/design-data/design-tokens).
Use [DTCG](https://www.designtokens.org/technical-reports/) only when token interchange
is relevant; its format does not choose project values, naming, or required tiers.
