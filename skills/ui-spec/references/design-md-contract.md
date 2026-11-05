# DESIGN.md Contract for UI Spec

## Contents

- [Scope and Source](#scope-and-source)
- [CLI and Version Policy](#cli-and-version-policy)
- [Core Semantics](#core-semantics)
- [Two Independent Results](#two-independent-results)
- [First Creation](#first-creation)
- [Validation Boundary](#validation-boundary)

## Scope and Source

- Load this profile only when the project explicitly adopts the Google `DESIGN.md`
  format, including an authorized first adoption, or an accepted consumer already
  requires its additional completeness policy. A filename or shared token/component
  change alone does not activate either requirement.
- Resolve `<design-root>` and the file's declared authority from project guidance and
  consumers. Preserve existing token/component owners and project approval rules;
  format selection does not authorize an authority migration.
- Canonical spec snapshot:
  `https://github.com/google-labs-code/design.md/blob/9bf8eae67128b6cc55ad9bf86665767deb4c11cd/docs/spec.md`

## CLI and Version Policy

- Bind `DESIGN_MD_PACKAGE_ROOT` to an existing `@google/design.md@0.4.0` package
  and verify its package name and version before invocation.
- Resolve the path placeholder from that runtime binding and invoke its Node entry:
  - `node <DESIGN_MD_PACKAGE_ROOT>/dist/index.js lint --format json <file>`
  - `node <DESIGN_MD_PACKAGE_ROOT>/dist/index.js diff <before> <after>`
  - `node <DESIGN_MD_PACKAGE_ROOT>/dist/index.js export --format <format> <file>`
- Do not use the unpinned package name or different versions.
- Review and update the pinned spec snapshot and CLI version together; do not advance one silently.

## Core Semantics

- YAML frontmatter is optional in the Google format. When present, its tokens are
  normative values for that document's declared scope.
- Markdown prose is the application guidance for how those tokens are used.
- Reference the document only for the shared semantics it actually owns; leave
  component APIs and separately owned live token values at their existing sources.
- Frontmatter `version` is optional. Do not use an edit or approval date as its
  default value; omit it when the project has no semantic version policy.
- Keep applicable standard sections in their specified order; the Google format
  permits omitting irrelevant sections and preserving unknown headings. Do not
  silently delete valid token names, component properties or project-local content.
  Fixed eight-section completeness is the separate opt-in policy below.
- Duplicate section headings fail validation. Keep the package regression guard because
  prior CLI behavior could return zero while reporting the duplicate as a warning.
- Diff compares token-level changes; also inspect changed prose and affected consumers
  for semantic regressions.
- For the first accepted DESIGN.md creation, record diff as `Not applicable`; do not invent a before file.
- Lint returns exit code `0` when no errors remain; warnings may exist and still be
  accepted except for duplicate H2, which is always a blocker in this repository.
- Export is only a derived output for approved downstream consumers.

## Two Independent Results

Official lint proves only `official-format-valid`: YAML and Markdown can be parsed and
the official structural rules pass. It never proves that a project has supplied a
complete adopted shared visual authority.

Run `python3 scripts/validate-design-md-completeness.py` after official lint only when
`ui-spec-design-completeness/1` is explicitly adopted by the project or required by
an existing accepted consumer. Google format adoption alone does not require this
policy; otherwise report it `Not applicable`, never passed. An adopted policy cannot
be skipped by relabeling the document or its consumer.

This strict policy adds eight-section completeness, source binding and independent
approval; it is not part of the Google format. It returns `ready-for-human-approval` for a complete first-adoption
candidate. A local adopted-stage record that binds the exact current DESIGN.md hash
returns `awaiting-trusted-approval-verification`, never `complete`: a local record and
caller-supplied hash cannot prove human identity. Independently trusted human approval
evidence bound to the exact immutable result identity and basis may satisfy downstream completeness;
it does not mutate the producer result. Any policy error is `not-ready`, even when
official lint reports zero. All consumers require that same exact immutable result;
approval evidence bound to different bytes or basis is stale and cannot clear the gate.

## First Creation

For Google format without the additional policy, author only applicable sections and
source-backed content, run official format checks, and follow the project's actual
acceptance process. Do not require the strict template, extra token groups or an
independent approver merely because the file is new.

The following template and all eight steps apply only to the explicitly adopted
`ui-spec-design-completeness/1` policy:

1. Copy `assets/DESIGN.md` to the resolved `<design-root>`.
2. Replace its name, description, and prose only from verified sources.
3. Fill `colors`, `typography`, `spacing`, and `rounded` with exact approved machine
   tokens, or use official `omitted` objects with a concrete reason for each group.
   When shared component consumers exist, `components` must contain entries; omission
   is allowed only after proving that the boundary has no shared component consumer.
   When shared SVG iconography exists, bind its approved family, canonical geometry,
   rendering/state, coloring strategy, accessibility, owner/rights, and fallback under
   `## Components` as `### Iconography`; do not add a ninth H2 authority section.
4. Keep exactly the eight canonical H2 headings in canonical order. Put project-local
   detail under their H3/body, and bind every token group to application semantics in
   the corresponding section.
5. Treat CSS, theme, and component source only as implementation/source evidence.
   Exact target values require an approved visual or other verifiable source.
6. Run official lint, then the completeness checker with `--source-ref`, the readable
   `--source-artifact`, its exact `--source-sha256`, required `--source-status`, and the
   shared-component fact. A first-adoption candidate may request approval only
   after `ready-for-human-approval`.
7. Obtain a verifiable JSON approval record from someone other than the
   proposer/implementer. It must contain `status: approved`, the exact current
   `design_sha256`, and stable `approved_by_id`, `proposer_id`, and `implementer_id`.
   Rerun adopted stage with `--approval-record` and its exact
   `--approval-record-sha256` to validate the local binding. This stops at
   `awaiting-trusted-approval-verification`; self-reported CLI actor strings and
   applicant-created JSON are not trusted approval evidence.
8. Record diff as `Not applicable` because no accepted before file exists.

## Validation Boundary

- Obtain authorization before any CLI step that downloads a package or uses the network.
  Existing task authorization satisfies this when it covers that step.
- Treat a blocked required CLI step as `Not verified`; do not mark the affected slice `Ready`.
- The checker does not redefine Google token types. It enforces the explicitly
  adopted policy's completeness, section semantics, source and approval binding.

The completeness validator consumes an existing `@google/design.md@0.4.0` package
through `DESIGN_MD_PACKAGE_ROOT`. It checks the package identity/version and does not
install dependencies. Without that binding, return the missing-parser gap before
validation; source, parser output and human approval remain separate evidence.
