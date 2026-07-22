# Repository Scope

`idaibin/skills` is a public catalog of independently installable Agent Skills
for software-engineering work.

## Owns

- publishable packages under `skills/<name>/`;
- package-local references, scripts, assets, and provider metadata;
- catalog and installation documentation;
- concise deterministic validation and shared-protocol sources;
- contributor guidance for adding, changing, renaming, or removing a Skill.

## Does Not Own

- generated application code, reports, articles, or operational output from an
  installed Skill;
- downstream repository conventions or task instances;
- a mandatory end-to-end agent framework or hidden shared runtime;
- provider-specific plugin packaging unless it is explicitly added later.

## Runtime Boundary

A published Skill may load only files inside its own package. Repository-level
`docs/`, `protocols/`, and `scripts/` are maintainer surfaces and must never be
required by an installed package at runtime.

Cross-Skill relationships are optional composition or explicit handoffs. A
package must still complete its basic responsibility when installed alone.
