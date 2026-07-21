# Product Documentation Boundaries

## Location Order

1. Use the repository's existing authoritative product fact source.
2. Use the repository's established feature/spec convention.
3. Only when neither exists and the user explicitly authorizes a new fallback,
   use one of:
   - `docs/product/PRODUCT.md` for a foundation;
   - `docs/product/features/<feature>/spec.md` for a feature.

Do not create both. Do not add a new `docs/product` tree when an equivalent ADR,
RFC, feature, requirements, or product directory already owns the fact.

## Conditional Artifacts

- Glossary: only when shared terminology needs a separate durable source; deep
  domain work belongs to `domain-modeling`.
- ADR: only for a long-lived technical or product decision when the repository
  uses ADRs and the decision owner authorizes it.
- UI evidence/prompt: only when the feature needs visual or state evidence; shared
  visual-system ownership belongs to `ui-design`.
- Handoff: only for unfinished cross-session continuation. Follow repository
  convention, such as `.codex/handoffs/<task-id>.md` for local task/worktree state
  or a repository-approved docs location for explicitly requested team-shared
  continuation. Before writing a local handoff, verify that its directory is ignored;
  use an existing ignored workspace or request authorization to add the ignore rule
  instead of silently changing tracked policy. A handoff is not automatically loaded
  and is not a substitute for durable product facts.

## Authority

`product-spec` may update product documents only after explicit authorization. It
does not own source, Git, technical interface definitions, ui-design assets,
domain models, or runtime evidence. Route current implementation mapping to
`repo-map`; link other authoritative artifacts rather than copying them.
