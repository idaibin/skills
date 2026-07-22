# Official Skill Alignment

Reviewed: 2026-07-22

This catalog uses three current primary baselines:

| Lane | Source | Adopted surface |
| --- | --- | --- |
| Portable | [Agent Skills specification](https://agentskills.io/specification) | `SKILL.md`, `name`, `description`, optional `scripts/`, `references/`, and `assets/` |
| Anthropic | [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) and [authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | progressive disclosure, concise descriptions, direct references, representative evaluation |
| OpenAI | [Build skills](https://learn.chatgpt.com/docs/build-skills) | portable package plus optional `agents/openai.yaml`, explicit and implicit invocation |
| Distribution | [skills.sh](https://skills.sh/) | repository discovery, installation, and updates documented at the repository root |

## Catalog Decisions

- Require the portable `SKILL.md` contract and keep package instructions concise.
- Keep references one level deep and load them only when needed.
- Require `agents/openai.yaml` because OpenAI is a supported catalog target; do not
  present it as portable or Claude-specific metadata.
- Keep packages self-contained and free of repository maintenance/install guidance.
- Use a few realistic trigger, non-trigger, and edge scenarios for iteration.
- Keep safety and mutation boundaries that prevent accidental writes or external
  actions; these are functional requirements of the engineering Skills.

The repository does not require formal held-out campaigns, directory-wide behavior
certification, evidence manifests, independent semantic graders, or token-efficiency
thresholds. Those mechanisms exceeded the requirements of the providers and did not
justify their maintenance cost.

Official formats establish compatibility, not guaranteed model behavior. For a material
workflow change, run the affected Skill on representative tasks and inspect the actual
outputs. Critical production use still requires validation in the target environment.
