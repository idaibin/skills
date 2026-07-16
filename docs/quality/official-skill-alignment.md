# Official Skill Alignment

This record defines the external baseline used to review AICraft's Skill
packages. It separates the portable Agent Skills core from provider-specific
OpenAI and Claude features, then records which stricter repository policies
AICraft applies locally.

## Review Record

- Reviewed: `2026-07-16`
- Review due: `2026-10-16`
- Machine-readable authority:
  [`contracts/skill-validation.json`](../../contracts/skill-validation.json)

| Lane | Primary source | Pinned evidence |
| --- | --- | --- |
| Portable core | [Agent Skills specification](https://agentskills.io/specification) | Retrieved `2026-07-16` |
| OpenAI Codex | [Build Skills](https://learn.chatgpt.com/docs/build-skills) | Retrieved `2026-07-16` |
| OpenAI distribution examples | [openai/plugins](https://github.com/openai/plugins) | Commit `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` |
| Claude reference packages | [anthropics/skills](https://github.com/anthropics/skills) | Commit `9d2f1ae187231d8199c64b5b762e1bdf2244733d` |
| Claude Code behavior | [Extend Claude with skills](https://code.claude.com/docs/en/skills) and [How Claude remembers your project](https://code.claude.com/docs/en/memory) | Retrieved `2026-07-16` |
| Skill evaluation | [Agent Skills evaluation](https://agentskills.io/skill-creation/evaluating-skills) | Commit `38a2ff82958afee88dadf4831509e6f7e9d8ef4e` |
| Evaluation architecture | [UK AISI Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) | Commit `ea007a79c556e30fb391c5e98ce2bf80b2362fbf` |
| Agent workflow evaluation | [OpenAI Agent Evals](https://developers.openai.com/api/docs/guides/agent-evals) | Retrieved `2026-07-16` |

The pinned repositories are comparison snapshots, not vendored dependencies.
The retrieved documentation is time-sensitive and must be reviewed again by
the due date. Validation must fail rather than silently treating an expired
baseline as current.

The evaluation sources define reusable experiment structure and evidence
practices. They do not replace AICraft's repository-specific owner, handoff,
authority, or workflow assertions.

## Portable Core

The portable contract is a directory containing `SKILL.md` with YAML
frontmatter and Markdown instructions. `name` and `description` are required;
supporting `scripts/`, `references/`, and `assets/` are optional and should be
loaded only when needed.

Portable frontmatter may also carry optional `license`, `compatibility`, and
string-map `metadata` fields, plus the experimental `allowed-tools` field.
AICraft intentionally uses the stricter `name`/`description` subset, applies
the repository-level `LICENSE` to the published collection, and does not
duplicate license or host-specific capability metadata across every package.

AICraft adopts this progressive-disclosure model. Its package limits, metadata
rules, reference navigation requirements, and validation thresholds may be
stricter than the portable specification. Those local limits live in
`contracts/skill-validation.json`; prose documents must not create competing
numeric authorities.

## OpenAI Lane

OpenAI Codex uses the portable `SKILL.md` contract and may add
`agents/openai.yaml` for Codex-facing display metadata and a starter prompt.
AICraft requires this file for its published packages, keeps
`short_description` compact, and uses a short self-routing `default_prompt`
that names the Skill as `$skill-name`.

Codex builds its initial discovery list from each Skill's name, description,
and path under a two-percent or 8,000-character context budget, shortening or
omitting descriptions when necessary. AICraft's tighter per-description limit
and aggregate footprint measurement are local safeguards for that discovery
budget, not portable schema requirements.

`agents/openai.yaml` is an OpenAI integration surface, not part of the portable
Agent Skills minimum. AICraft keeps skills.sh as its cross-provider install
path. The current OpenAI plugin repository informs packaging and metadata
quality, but this review does not replace portable distribution with an
OpenAI-only plugin wrapper.

## Claude Lane

Claude Code follows the Agent Skills standard and adds optional host features
such as invocation controls, tool restrictions, hooks, subagent execution, and
dynamic context. These extensions are useful only when a package requires the
corresponding Claude behavior; they must not be presented as portable fields or
copied into every AICraft package by default.

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. The repository therefore keeps
small `CLAUDE.md` files that import the same-directory `AGENTS.md` with the
official `@path` syntax. Runtime Skill instructions should refer to effective
repository or host guidance rather than assuming that every host reads one
specific filename.

## Adopted Decisions

- Keep `SKILL.md` focused on trigger, workflow, authority, output, and direct
  navigation; move detailed examples and checklists to linked references.
- Keep startup metadata concise because every Skill description competes for
  discovery context before invocation.
- Validate the portable package against current provider specifications with
  AICraft's repository checks. Record a provider-owned validator and its exact
  version separately when one is actually executed; none is implied here.
- Keep provider-specific metadata in its provider lane.
- Use held-out natural-language requests and repeated real runs for behavior
  claims; retain raw outputs and execution evidence.
- Compare a changed Skill in one matched candidate/previous/no-Skill group
  before claiming that it noticeably improves outcomes or Skill-attributable
  input efficiency.
- Preregister formal held-out trials in a committed post-anchor campaign and
  freeze the contract, runner, scorer, comparator, validator, canonical prompt,
  adjudication, host/environment/retry policy, revisions, and full attempt set
  before any model call.
- Permit at most one within-slot host retry, only for the exact canonical Codex
  model-capacity JSON error with no valid result and no exposed token counts;
  retain both attempts and never retry behavior, structured-output, timeout, or
  generic host failures.
- Review official sources on a recorded cadence and update contracts, fixtures,
  tests, and documentation together when the external baseline changes.

## Not Adopted As Universal Rules

- OpenAI plugin manifests or `agents/openai.yaml` as portable Agent Skills
  requirements.
- Portable experimental `allowed-tools`, or Claude-specific invocation
  controls, hooks, and forked context, when a package does not need those
  behaviors.
- Provider example structure as proof that a package is correct for AICraft's
  authority and routing boundaries.
- A provider's maximum file size as AICraft's working target when the local
  contract intentionally sets a tighter limit.
- Subjective maturity labels or claims based only on package count, Markdown
  eval tables, deterministic fixtures, or validator success.

## Evidence Boundary

Official-format compatibility and static repository validation prove structure
only. They do not prove that a model selects the right Skill, respects
authority, hands off correctly, finishes a repository task, or improves
quality, time, or token use.

Contract correctness can be evaluated without a baseline. A claim such as
"noticeably improves collaboration" requires controlled candidate, previous,
and no-Skill runs using the same prompts and canonical environment policy in
parallel when the host supports it, at least the required repeated trials,
held-out requests for changed discovery text, raw traces, duration and token
data when exposed by the host, outcome grading, and workspace-diff evidence.
The current hash binds the environment-variable allowlist and fixed isolation
overrides, including required executable-toolchain roots such as `VOLTA_HOME`,
not the actual PATH, toolchain-root, proxy, locale, or certificate values; that
runtime drift remains visible only through trusted execution records. A
separate frozen `retry_policy_sha256` binds the one-retry limit, backoff, host,
and exact capacity classifier. Result schema `6`, raw-evidence schema `3`,
campaign schema `2`, comparison report schema `4`, and reviewer version `6`
require ordered evidence for every host attempt plus case-level attempt and
retry counts. Capacity is
retryable only when no valid structured result and no input or output token
count exists; terminal case tokens mirror the final host attempt, while all
per-attempt token fields remain auditable. See
[`validation-plan.md`](validation-plan.md) and [`status.md`](status.md).

Recorded hashes provide tamper evidence under a trusted evidence producer; they
are not host signatures and do not independently establish that a self-reported
tool action or verifier label is semantically true. The current machine claim
gate therefore permits only scoped routing outcome contribution or marginal
Skill-input efficiency claims.
The marginal input claim additionally requires candidate overhead to be no
greater than previous in every group, at least 15% relative reduction, and at
least 50 saved input tokens per case on average.
Authority and workflow stay `not_verified` until an independent semantic
verifier is part of the contract.
