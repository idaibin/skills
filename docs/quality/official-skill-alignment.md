# Official Skill Alignment

Reviewed: 2026-07-30. Revalidate the linked upstream contracts before changing a
provider surface; this date is disclosure, not proof of current upstream behavior.

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
- Keep cross-package discovery in the repository-level `skills-index.json`; do not
  add unsupported nested routing fields to portable frontmatter or claim that clients
  automatically consume the repository index.
- Use a few realistic trigger, non-trigger, and edge scenarios for iteration.
- Keep safety and mutation boundaries that prevent accidental writes or external
  actions; these are functional requirements of the engineering Skills.
- Keep provider-neutral runtime preferences, such as a preferred persistent review
  context with a Standard Chat fallback, inside package references and focused
  validation. Do not encode provider capability claims in portable metadata.
- Keep provider-family aliases separate from canonical CLI profiles: plain Qoder is
  ambiguous, while an optional user-owned `provider_aliases` mapping may select
  `qoder-cli-global` or `qoder-cli-cn`. The mapping selects only the recipient; fresh
  help/version/path identity and capability gates remain required, and global/CN routes
  never cross-fallback.
- Keep sequential external-AI relay as a bounded, attributed package workflow: one
  fixed basis and stable review round, one relay-turn ID per submitted provider turn,
  separate logical IDs for actual side effects, and one verified conversation per provider:
  create only on that provider's first turn when a new session is actually required,
  then reuse it on later turns and reconcile an interrupted create under its original
  ID. An atomic host create-and-initial-submit call still uses distinct correlated
  create and submit IDs, with capture read-only and idempotent. All configured providers approve the same candidate for success, local
  verification precedes any provider-authored textual promotion, and explicit
  redaction rather than summarization applies when cross-provider data sharing is
  constrained. Legacy two-provider stop values decode to the canonical all-provider
  condition; `changes-required` takes priority over terminal turn exhaustion.
- Keep browser routing provider-neutral and activation-scoped: explicit current routes
  win, otherwise a saved primary is freshly preflighted on every task; a before-submit
  fallback never demotes the next task's primary. Persist only a local browser product
  name, never profile, tab, URL, login, identity, or capability evidence.
- Keep project grounding bounded and evidence-typed: semantic cross-project or
  runtime risks activate the shared protocol, while filenames and framework presence
  alone do not. Source, local checks, built artifacts, and target runtime remain
  separate proof levels; runtime evidence names local, target-like, or deployed scope,
  and verification state stays separate from action disposition. Every completion
  claim is capped at its strongest supported evidence level.

Raw evaluation output stays ignored and outside the published catalog. A durable
summary is eligible for `docs/quality/` only when it records a fixed current basis,
host/model, scenarios, failures, and coverage limits without private transcripts.

The repository does not require formal held-out model campaigns, directory-wide live
behavior certification, or independent semantic graders. It does require an offline
catalog-wide normal/boundary/critical-stop matrix with a committed no-new-regression
baseline. A deterministic character-based context report supplies warnings only; it
is not a token-efficiency certification or substitute for host/model evidence.

The gate reads the routing baseline from the immutable base ref so a candidate cannot
erase history merely by rewriting its own baseline file. Critical-stop prompts are
checked by a deterministic owning-signal classifier plus the declared stop contract;
this remains weaker than observing a real host stop.

Official formats establish compatibility, not guaranteed model behavior. For a material
workflow change, run the affected Skill on representative tasks and inspect the actual
outputs. Critical production use still requires validation in the target environment.
