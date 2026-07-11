# Prompts

Reusable prompt assets are grouped by use case.

## Categories

- `development/`
  - general implementation, strict review, API contract review, and project initialization prompts

- `automation/`
  - scheduled research, reflection, reusable asset search, digest, and advisory or planning prompts

- `agent-systems/`
  - system prompts, agent migration packages, cross-agent workflows, and agent configuration prompts
  - `cross-agent-verification.md`: coordinate ChatGPT strategy review with Codex repository-grounded verification

- `design/`
  - reusable visual-design, image-generation, poster, and brand-system prompts
  - `msi-2026-esports-poster.md`: generate verified MSI 2026 match-result and match-preview posters with a consistent official-inspired visual system

- `rustzen/`
  - prompts tied to Rustzen projects, Rust backend/database rules, or Rustzen-specific architecture decisions

## Rules

- Keep each prompt in the category where it is most likely to be reused.
- Do not keep YAML front matter by default; use the folder, filename, and visible heading as the active metadata.
- Keep Notion/source provenance only when it is still actionable; otherwise archive the source instead of carrying import metadata in active prompts.
- Keep active prompt files focused and directly executable. Move long PRDs, migration packages, and historical source documents out of active prompts; use git history or a dedicated archive directory when one exists.
- Add an explicit language rule when the output language matters.
- Add a new category only when an existing one would make the prompt hard to find.

## Relationship With Skills

- `prompts/` stores evolving source prompt assets.
- `skills/` stores self-contained published workflows.
- Skills may be inspired by prompts, but published skills must not require `prompts/` at runtime.
- When a prompt and skill describe the same capability, validate the behavior in ChatGPT first, then synchronize the stable contracts into both surfaces.
- If a prompt change is required by a skill, update the corresponding `skills/<skill-name>/references/` file in GitHub before upgrading that skill.
- Skill upgrade workflows compare only the matching remote `skills/<skill-name>/` package, not repository-level `prompts/`.
- Keep prompt files usable as standalone task instructions, even when a related skill exists.
