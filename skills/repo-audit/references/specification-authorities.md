# Product and UI Specification Authorities

## Classify Authority by Meaning

- **Product facts:** user behavior, scope, business rules, permissions, failure
  semantics, compatibility, and product acceptance. Use the repository's declared
  requirement authority or established convention. `PRD` is an authority role, not
  a required root filename or a universal Markdown schema.
- **Shared visual semantics:** the project-declared design guidance and component
  contracts own shared intent, variants, and cross-surface rules. Use the resolved
  `<design-root>/DESIGN.md` when it is the adopted owner; the filename alone does not
  establish Google format or an additional approval policy. Actual token/variable
  sources own values and references, and component source/types own public APIs.
  Preserve the project's declared relationship between these owners.
- **Slice UI contract:** the accepted selected-source contract for one page, flow, or
  domain. It owns layout, component/token mapping, interaction, responsive and
  accessibility rules, and UI acceptance.
- **Technical plan or ADR:** implementation approach and architecture decisions. It
  never becomes product or visual authority merely because it is Markdown.

Do not classify a document from `design`, `prd`, `requirements`, or `spec` in its
filename alone. Confirm its declared owner, path convention, content, links, and
approval state.

## Resolve and Read

1. Read effective repository guidance and any declared authority paths or exceptions.
   Project guidance such as `AGENTS.md` may declare adoption, actual locations, and
   exceptions. Skills supply the workflow; they do not replace project contracts
   with a universal filename, schema, token hierarchy, or approval process.
2. Read the repository's existing product foundation or shared index only when the
   target slice depends on it, then read the target product slice. Do not load sibling
   slices by default.
3. When UI contracts are relevant, resolve the actual shared owners, any applicable
   UI index, and the target slice. Do not infer authority from the Git root, a filename,
   generated metadata, or the existence of a reusable component. Apply only the
   declared validation profile:
   - Project-native contracts use their existing checks and approval rules; shared
     changes do not require migration to Google DESIGN.md.
   - Explicit Google format adoption requires its pinned format/lint evidence and
     applicable diff. Format validity does not prove accepted design decisions.
   - Require `ui-spec-design-completeness/1` and its independent approval binding only
     when that additional policy is explicitly adopted or an established consumer
     requires it. Preserve those requirements: a missing, `not-ready`, stale-hash,
     format-only, or local `awaiting-trusted-approval-verification` result cannot clear
     that gate. Only independently trusted human approval bound to the exact immutable
     result identity and basis satisfies its consumer claim; the producer result stays
     `awaiting-trusted-approval-verification`.
   Resolve uncertain policy ownership before a dependent readiness claim. Do not mark
   an existing required policy inapplicable merely to use a lighter path.
4. Cross-check implementation and runtime evidence against those contracts without
   silently treating current code as approval for an unresolved product or visual
   decision.

Repository-declared locations win. Only an owner Skill creating an explicitly
authorized artifact may apply its fallback paths; consumer Skills do not create a
parallel `docs/prd/`, `docs/ui/`, root `PRD.md`, or visual authority.

## Consume or Hand Off

- Consume an existing usable contract directly. Do not invoke `product-spec` or
  `ui-spec` merely to recognize or read a file.
- Hand unresolved behavior, business rules, permissions, failure semantics, or
  product acceptance to `product-spec` only when those decisions are required for
  the requested outcome.
- Hand missing, conflicting, unapproved, or changed selected-source/shared visual
  contracts to `ui-spec` only when the requested outcome requires that UI decision.
- A missing optional artifact does not create mandatory ceremony for a known scoped
  implementation or audit. Report it as `Not found` or `Not applicable`; block only
  when the missing decision can change the requested behavior or acceptance.
- Preserve authorization boundaries: a handoff transfers context, not permission to
  write product facts, UI specifications, source, or Git state.
- Update only the authority whose accepted behavior or presentation changes; do not
  manufacture document edits for unaffected layers. Keep Product and UI readiness
  separate, and verify source, automated checks and runtime evidence on their own
  bases after implementation. An explicit user decision in the current task can
  supply the needed approval; an unchanged contract does not need reapproval.

## Report

Name the authorities read, target slice, applicable revision or approval state,
conflicts, handoffs, and every `Not found` or `Not verified` contract gap.
