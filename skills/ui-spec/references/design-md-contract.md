# DESIGN.md Contract for UI Spec

## Scope and Source

- `<design-root>/DESIGN.md` is the canonical shared visual authority for the proven
  shared visual boundary.
- This document defines how this Skill uses the official Google `DESIGN.md` spec and
  the CLI for shared-system changes only.
- Canonical spec snapshot:
  `https://github.com/google-labs-code/design.md/blob/2513a54eca0dc414b7881d48aaa44353397e0c88/docs/spec.md`

## CLI and Version Policy

- Use Node.js + npm CLI package `@google/design.md@0.3.0` only.
- Use one cross-platform command form for all platforms:
  - `npx -p @google/design.md@0.3.0 designmd lint --format json <file>`
  - `npx -p @google/design.md@0.3.0 designmd diff <before> <after>`
  - `npx -p @google/design.md@0.3.0 designmd export --format <format> <file>`
- Do not use the unpinned package name or different versions.
- Review and update the pinned spec snapshot and CLI version together; do not advance one silently.

## Core Semantics

- YAML frontmatter tokens are normative contract values.
- Markdown prose is the application guidance for how those tokens are used.
- Only the resolved `<design-root>/DESIGN.md` can carry long-lived token and component semantics for that boundary.
- Frontmatter `version` is optional. Do not use an edit or approval date as its
  default value; omit it when the project has no semantic version policy.
- Preserve unknown Markdown sections, valid token names, and component properties instead of deleting them during an edit.
- Duplicate section headings fail validation.
- `@google/design.md@0.3.0` currently may report duplicate H2 via warning output while returning lint exit code `0`; this Skill must still treat duplicate H2 as a hard blocker and reject those cases.
- Diff compares token-level changes and is the regression gate for shared visual updates.
- For the first accepted DESIGN.md creation, record diff as `Not applicable`; do not invent a before file.
- Lint returns exit code `0` when no errors remain; warnings may exist and still be
  accepted except for duplicate H2, which is always a blocker in this repository.
- Export is only a derived output for approved downstream consumers.

## First Creation

1. Copy `assets/DESIGN.md` to the resolved `<design-root>`.
2. Replace its name, description, and prose only from verified sources.
3. Add token groups only when their exact values and meanings are verified; never derive exact values from pixels alone.
4. Obtain named human approval for the new shared authority.
5. Run official lint and record diff as `Not applicable` because no accepted before file exists.

## Validation Boundary

- Obtain authorization before any CLI step that downloads a package or uses the network.
- Treat a blocked required CLI step as `Not verified`; do not mark the affected slice `Ready`.
- Do not implement another schema, manifest, package validator, or compatibility format beside the official DESIGN.md contract.
