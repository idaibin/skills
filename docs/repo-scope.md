# Repository Scope

## Role

`idaibin/aicraft` is the source repository for reusable AI automation capabilities, prompt assets, skill assets, workflow templates, and shared execution standards.

It defines how AI-assisted workflows should be structured. It does not own the generated content produced by those workflows.

## Owns

- Reusable prompts.
- Reusable skills.
- Reusable workflow patterns.
- Shared automation standards.
- Shared content quality standards.
- Shared GitHub branch and commit rules.
- Deterministic validation and synchronization scripts.
- Canonical cross-skill protocols and validation contracts.
- Version-bound quality status and historical validation evidence.
- Task registry entries that point to concrete repository task specs.

## Does Not Own

- Concrete blog articles.
- Concrete information-feed entries.
- Repository-specific frontmatter schemas.
- Repository-specific content paths.
- Generated posters or covers.
- Production content updates for `blog` or `feeds-hub`.

## Consumes From

None as an authority source.

Project repositories may consume standards from this repository, but this repository should not depend on business repositories for its own rules.

## Automation Rules

Shared automation rules live under:

```text
docs/standards/
```

Concrete scheduled-task instances should be listed in:

```text
docs/task-registry.md
```

## Allowed Paths

Automation-standard maintenance may modify:

```text
docs/standards/**
docs/quality/**
docs/history/**
docs/templates/**
docs/task-registry.md
prompts/**
skills/**
scripts/**
protocols/**
contracts/**
workflows/**
README.md
INSTALL.md
```

It must not write generated blog posts, feed entries, or production content for downstream repositories.
