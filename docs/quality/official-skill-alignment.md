# Official Skill Alignment

Reviewed: 2026-07-23

This catalog uses four current primary baselines:

| Lane | Source | Adopted surface |
| --- | --- | --- |
| Portable | [Agent Skills specification](https://agentskills.io/specification) | `SKILL.md`, `name`, `description`, optional `scripts/`, `references/`, and `assets/` |
| OpenAI | [Build skills](https://learn.chatgpt.com/docs/build-skills) | portable package plus optional `agents/openai.yaml`, explicit and implicit invocation; plugins are an optional bundled-distribution layer |
| Anthropic | [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) and [authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | portable `SKILL.md` package, progressive disclosure, and representative evaluation; no per-Skill Anthropic YAML is required |
| Distribution | [skills.sh](https://skills.sh/) | portable repository discovery, installation, and updates documented at the repository root |

## Catalog Decisions

- Require the portable `SKILL.md` contract and keep package instructions concise.
- Keep references one level deep and load them only when needed.
- Require `agents/openai.yaml` because OpenAI is a supported catalog target; do not
  present it as portable or Claude-specific metadata.
- Keep portable `description` metadata for every package. When an OpenAI Skill is
  explicit-only, set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`
  rather than importing another provider's invocation-control frontmatter.
- Do not add `agents/anthropic.yaml` or speculative vendor mirrors. Add a provider
  adapter only for a documented contract and an intentionally supported distribution
  target; keep plugin/marketplace manifests at their provider-defined distribution
  scope rather than duplicating Skill instructions.
- Keep packages self-contained and free of repository maintenance/install guidance.
- Use a few realistic trigger, non-trigger, and edge scenarios for iteration.
- Keep safety and mutation boundaries that prevent accidental writes or external
  actions; these are functional requirements of the engineering Skills.

Raw evaluation output stays ignored and outside the published catalog. A durable
summary is eligible for `docs/quality/` only when it records a fixed current basis,
host/model, scenarios, failures, and coverage limits without private transcripts.

The repository does not require formal held-out campaigns, directory-wide behavior
certification, evidence manifests, independent semantic graders, or token-efficiency
thresholds. Those mechanisms exceeded the requirements of the providers and did not
justify their maintenance cost.

Official formats establish compatibility, not guaranteed model behavior. For a material
workflow change, run the affected Skill on representative tasks and inspect the actual
outputs. Critical production use still requires validation in the target environment.

## Upstream Practice Snapshot

The following repository comparison was refreshed from shallow clones on 2026-07-23.
It is a practice comparison, not an additional compatibility contract.

| Repository and revision | Useful practice | Catalog decision |
| --- | --- | --- |
| Reference catalog A | concise writing guidance, concrete reusable procedures, direct reference links | keep entries operational and avoid forcing one authoring style across every package |
| Reference catalog B | progressive disclosure, bundled deterministic helpers, representative with-Skill evaluation | retain one-level references and behavior canaries; add scripts only for repeated deterministic work |
| Reference catalog C | repository discovery, installation, and distribution validation | keep distribution/tooling checks separate from each Skill's runtime workflow |
| Reference catalog D | compact core loops, provider metadata separated from portable `SKILL.md`, bundled wrappers for tool reliability | retain provider metadata as an adapter and keep portable instructions authoritative |
| Reference catalog E | explicit nearest-neighbor rerouting where ambiguity is real, scored failure-sample iteration | add one short metadata negative only for genuine routing collisions; refine from live failures rather than prose growth |

Across the five repositories, negative metadata is not universal and large entrypoints are
not evidence of better behavior. This catalog therefore does not impose a minimum entry
length, a negative clause on every description, or upstream-specific folder conventions.

The Agent Skills specification points to `skills-ref`, whose upstream repository marks
it as a demonstration library rather than a production validator. This catalog therefore
keeps a focused, tested validator for its portable and provider-specific contracts instead
of downloading an unpinned demonstration tool in CI.
