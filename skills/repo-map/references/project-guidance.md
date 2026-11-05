# Repository Guidance Handoff

Read this reference only to recognize and reroute an explicit request to create,
bootstrap, or repair repository guidance such as `AGENTS.md`. `repo-map` indexes
existing authorities; it does not author those instructions.

## Resolve The Owner

- Return guidance authoring to the task's implementation or documentation owner.
  Frontend-specific guidance belongs with `dev-frontend`; mixed-repository guidance
  follows the proven repository owner instead of a directory-name guess.
- Continue within existing task authorization. A change of owner does not require
  the same permission again and does not authorize unrelated source or Git changes.
- Do not run a graph scan merely to draft guidance. The writing owner can inspect
  known files, manifests, commands, and nearby accepted consumers directly.

## Bounded Evidence Handoff

When a requested graph query is independently useful, return only its basis-bound
evidence: effective guidance paths, proven repository/subproject boundaries,
manifest and command-source locations, current contract owners, relevant consumers,
and conflicts or unresolved coverage. Keep source bodies in their native files.

An observed command is not a verified successful execution. Existing implementation
is evidence of the current state, not approval for a new normative rule. Missing
guidance is `Not found` within the inspected scope; it does not establish that the
whole project has no conventions.

## Stop At The Affected Boundary

An ambiguous target or conflicting authority blocks only the dependent authoring
decision. An unavailable graph runtime blocks graph operations with
`CAPABILITY_MISSING`; it does not block ordinary source inspection by the writing
owner. Do not manufacture a map, an `AGENTS.md`, or an approval to close that gap.
