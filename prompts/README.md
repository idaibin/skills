# Prompts

Reusable, standalone prompt assets. The collection is intentionally flat while it remains small; use filenames and this index instead of category directories.

## Index

| Prompt | Use case |
| --- | --- |
| `api-contract-review.md` | Verify a backend-to-frontend API contract chain. |
| `chatgpt-5.6-optimization.md` | Simplify and verify personal GPT-5.6 routing, context, permissions, Skills, plugins, and Codex configuration. |
| `review-chat-history.md` | Turn available daily conversations into a concise work review. |
| `scheduled-topic-digest.md` | Run a configurable, source-backed digest for selected topics and recurring information needs. |

## Authoring Rules

- Keep each file directly executable: state the task, required inputs, constraints, evidence rules, output contract, and validation when applicable.
- Use placeholders only for information the operator must supply. Inspect available context before asking for discoverable values.
- Distinguish verified facts, inferences, missing evidence, and unverified runtime behavior.
- Add an explicit language rule when output language matters.
- Prefer current, source-backed instructions over tool-specific assumptions that may drift.
- Keep active prompts concise. Put historical context, long PRDs, and migration records in git history or a dedicated archive.
- Do not use YAML front matter by default; the filename, visible heading, and this index are the active metadata.
- Add categories only when the collection becomes difficult to scan or a stable group has several closely related prompts.

## Relationship With Skills

- `prompts/` stores evolving source assets; `skills/` stores self-contained published workflows.
- Published skills must not require files under `prompts/` at runtime.
- When a prompt and a skill share a contract, validate the prompt first, then synchronize stable behavior into the matching skill package and its references.
- Keep every prompt usable without the related skill being installed.
