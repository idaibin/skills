# Official Skill Alignment

Reviewed: 2026-07-30

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
