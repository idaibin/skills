# Skill Routing And Design Standard

This standard defines when the catalog should keep capabilities together, split them into public Skills, or model them as internal profiles.

Portable and provider-specific package surfaces are defined separately in
[`../quality/official-skill-alignment.md`](../quality/official-skill-alignment.md).
Routing ownership must remain host-neutral even when OpenAI or Claude metadata
adds provider-specific invocation behavior.

## Core Principle

A public skill represents a stable user intent and execution owner, not merely a technology name or checklist category.

Two capabilities should remain separate when they differ materially in:

1. **Primary object** — what is being acted on or judged.
2. **Authorization boundary** — read-only, source mutation, Git mutation, browser/external action, or document writing.
3. **Workflow** — the sequence of evidence, decisions, and stop conditions.
4. **Output contract** — the artifact or decision the user receives.
5. **Nearest non-triggers** — similar requests that must route elsewhere.

Framework-specific or domain-specific checks should stay as profiles when these five properties remain the same.

## Current Repository Routing

| Skill | Primary object | Mutation | Primary output |
| --- | --- | --- | --- |
| `repo-map` | workspace/repository semantics and reuse map | read-only by default; repo-map write only after explicit request | real boundaries, task routes, verified reuse entries, alignment gaps |
| `domain-modeling` | shared business language, ambiguity, rules, and conditional lifecycle/context depth | read-only by default; existing fact-source update only after explicit request | resolved terms/rules, contradictions, decisions, scenarios, and open questions |
| `product-spec` | product behavior, scope, rules, states, and acceptance for one implementation slice | read-only by default; named product-artifact write only after explicit request | one feature/foundation spec or bounded product-fact update with Ready-for-slice verdict |
| `ui-design` | one page/flow visual and interaction design; conditional shared-system change | design-artifact write only; no source/runtime/Git mutation | Feature UI artifacts and handoff, or a bounded shared-system revision |
| `repo-review` | current Worktree/index, fixed immutable SHA/range, or verified review package; PR resolves to base/head and Release is conditional | read-only | basis-specific readiness, staging guidance, or consolidated P0-P3 findings |
| `dev-frontend` | requested frontend source change | source mutation | implemented and validated frontend change |
| `dev-rust` | requested Rust source change | source mutation | implemented and validated Rust change |
| `audit-frontend` | selected frontend domain profiles | read-only | bounded frontend findings and validation gaps |
| `audit-rust` | selected Rust domain profiles | read-only | bounded Rust findings and validation gaps |
| `audit-security` | known security-sensitive surface | read-only | scoped security findings and threat sketch |
| `repo-delivery` | reviewed local changes or a fixed source branch range | Git mutation | categorized commits or explicit single commit, evidence-based integration, refs, and proof |
| `ops-browser` | browser session/page state and bounded platform operation | authorized browser actions | browser evidence and state-change report |
| `ops-client` | real desktop client process/window | authorized client actions | process/window/runtime evidence |
| `ask-chatgpt` | local ChatGPT request package or independently required ChatGPT web collaboration | local artifact write or authorized external action | bounded request, attributed response/artifact, and locally verified implications |
| `human-writing` | source-grounded drafting, rewriting, diagnosis, or platform adaptation | owned writing transformation; not literal translation-only | publication-ready text or bounded diagnostic findings in the requested final language |

## Engineering Lifecycle

```text
repo-map (only when repository truth needs a durable map)
  -> domain-modeling (shared language/rules unclear)
  -> product-spec (product behavior or acceptance unclear)
  -> host planning (technical design and task slices needed)
  -> ui-design (concrete UI design needed)
  -> dev-* (source mutation requested)
  -> repo-review (Standards and Spec axes)
  -> repo-delivery (authorized Git mutation)
```

This chain is composable, not mandatory ceremony. Start at the earliest unresolved owner and stop at the last outcome the user requested.

`domain-modeling` remains separate from general planning: it resolves shared business meaning and rules independent of implementation. It does not default to technical DDD structures, APIs, databases, or frontend/backend design. Lifecycle and bounded contexts load only when material complexity requires them. Technical design, tasks, and validation use host planning and the appropriate implementation owner.

`product-spec` is also separate from general planning: it owns unresolved product
behavior and an authorized product-fact artifact, while host planning owns technical
decomposition after the relevant implementation slice is ready. It does not own a
complete domain model, shared Design System profile, technical interface definition, or source work.

## `repo-map` And `repo-review`

These remain separate because context mapping may write navigation docs, while review is always read-only and evaluates change safety.

### `repo-map`

Answers:

- What exists?
- Where is the real entry point or owner?
- Which canonical component, function, type, or API can be reused, extended, or wrapped before declaring another one?
- Which current-source declaration owns a protocol contract, which native client and
  real consumers depend on it, and which generated artifacts exist when applicable?
- Do project docs and current structure agree?

It stops when the requested facts are supported. It does not rank defects or determine commit/release safety.
Its API Contract Map profile records bounded authority and consumer topology only;
ordinary REST does not require OpenAPI or a generated client. The profile records
those fields only when the repository already owns them or an explicit trial adds them.
`repo-review` still owns fixed-basis compatibility/readiness findings, and runtime
operators still own live evidence.

### `repo-review`

Answers:

- What changed in the requested Worktree scope and necessary interface closure?
- When commit-readiness is requested, which changes belong together and how can they be staged safely?
- What actionable defects exist in a fixed repository snapshot, branch comparison, commit range, PR, release candidate, or verified review package?
- Which findings should block merge or release?
- How do frontend, Rust, security, CI, tests, docs, and structural evidence integrate?

It selects one basis first. Worktree findings-only inventories full status but deeply
reviews only the requested scope and interface closure. Worktree commit-readiness
adds complete ownership/mixed-hunk classification and staging guidance. Immutable
modes resolve SHAs and own P0-P3 findings. All modes stay read-only.

## Security Audit

`audit-security` remains separate from review coordinators because its primary object is a known security-sensitive surface and its output is a bounded security assessment.

- Under Worktree `repo-review`, it inspects only delegated local changed paths.
- Under immutable `repo-review`, it inspects only delegated fixed paths/ranges.
- Direct use is appropriate when the user requests only a scoped security audit after the target surface is known.
- It never takes over staging, commit readiness, whole-review severity integration, or Git mutation.

## Diagnosis And Implementation

General diagnosis uses the host's built-in reasoning plus effective personal and repository instructions. Confirm the failure, evidence, cause, and regression seam before applying a permanent fix. When the user requests remediation, the matching `dev-*` Skill owns the source change, `repo-review` checks the resulting local diff, and `repo-delivery` performs authorized Git mutation.

## Cross-Skill Handoff Contracts

Cross-skill workflows must transfer bounded state without transferring
authority. The caller owns intent, authorization, scope, and the next-state
decision; the executor owns only its direct action and evidence.

For discovery and routing evaluation, the **primary owner** is the published
Skill responsible for the current request's requested result, authority
boundary, and next-state decision. A **handoff** is another published Skill
that must actually execute a bounded part of the same request now, or must own
a later phase that the user explicitly requested in the same request. Do not
emit optional recommendations, alternative owners, internal implementation
details, or unrequested future work as handoffs. If the primary owner can
complete the requested outcome alone, the handoff list is empty.

Routing correctness is a full case contract: the selected owner must be
accepted, every required direct handoff and exactly one member of every
required one-of group must be present, and no undeclared, optional, or
forbidden handoff may appear. Exact top-1 remains a diagnostic and per-Skill
coverage metric, but it is not sufficient on its own.

Compose only owners needed for an independently required result. Keep one owner when
it can finish the request, load only selected references/profiles, reuse evidence while
the basis and environment remain unchanged, and run focused checks before broader
risk or repository gates. Do not create tasks, subagents, browser operations, durable
artifacts, or review rounds merely because the catalog can support them. Continue safe
local work and collect deferrable approval blockers at the end.

Host-specific model selection remains an execution policy in effective Agent
instructions, not a public Skill or handoff. A faster model may execute one bounded
slice, but the owning Skill, authorization, evidence basis, and coordinator validation
remain unchanged; fallback must not duplicate work or reinterpret ordinary failures
as capacity exhaustion.

For combined review, `ask-chatgpt` fixes one basis and creates an unbiased package;
`repo-review` and ChatGPT inspect it independently. Codex verifies and deduplicates both
finding sets in live source, applies only confirmed fixes through the matching owner,
runs proportionate validation, and performs one final local review. Repeat ChatGPT only
with explicit authorization plus a confirmed P0/P1, permission/privacy/security,
migration/irreversible, public-compatibility, production/release, or equivalent new
risk. A verified ChatGPT Project provides durable context but never replaces
the per-round package and fixed basis.

ChatGPT collaboration starts only after a Codex-first gate: when Codex, an existing Skill, or an available host tool can complete the requested result and no independent ChatGPT output was requested, use that local owner and stop. Otherwise `ask-chatgpt` derives a bounded request from natural language, selects a product/domain, UI/design, architecture, repository, implementation/security/delivery, review, or open-ended theme separately from Standard Chat, Search, Deep Research, Images, or reviewer-browser capability, and reuses the same package, authorization, operation, attribution, and local-verification infrastructure. Deep Research may supply a reviewable plan; a separate prompt-refinement chat is optional, not a mandatory round. External output does not mutate product facts, source, Git, or other systems.

For `ask-chatgpt -> ops-browser -> ask-chatgpt`, both
published packages carry the identical `browser-operation/v1` protocol. The
bridge owns the Capability requirements, Handoff Request, operation ledger,
`operation_id`, retry decision, rounds, and attribution. `ops-browser` owns the
measured Capability Snapshot and same-ID Handoff Result. An interruption with
uncertain side effects is `ambiguous` and must stop for reconciliation rather
than trigger a replacement operation.

`protocols/browser-operation-v1.md` is the repository authority;
`scripts/sync-shared-protocols.py` generates both published copies. Repository
validation rejects any copy that differs from that source.
Behavior evals must cover at least normal completion, failure before submit,
duplicate-submit prevention, ambiguous interruption, stale capability evidence,
and unauthorized handoff.

For `repo-map -> repo-review`, `repo-map` owns the durable semantic repo
map: current ownership and runtime boundaries, commands, shortest task routes,
and verified reuse entries with canonical owners, access/registration entries, consumers,
and constraints. `repo-review` may
use that map to select an initial read set, but independently verifies every
fact that affects a finding at its selected Worktree or immutable review basis. Missing mapped paths
are resolved from the nearest existing ancestor with a bounded subtree search;
the read-only reviewer records the mismatch and routes document repair back to
`repo-map`. This collaboration does not transfer P0-P3 authority.

## Public Skill Versus Internal Profile

Create a new public skill only when all of the following are true:

- a user can express a distinct intent without naming internal implementation details;
- it has a distinct authority or mutation boundary;
- at least a substantial part of its workflow and stop conditions differs from existing skills;
- its output contract is independently useful;
- it has at least three clear trigger and three clear non-trigger cases;
- the workflow has repeated across several real tasks or repositories.

Use an internal profile when the capability shares the same owner, evidence inventory, mutation boundary, and output format.

### Frontend Example

Keep these inside `audit-frontend`:

- React
- Vue Composition
- Vue Options
- architecture/reuse
- state/data/contracts
- component/layout/design system
- accessibility
- performance
- Tauri desktop boundary

Do not create `audit-react`, `audit-vue`, or `audit-ui` solely to divide checklists. The profiles frequently interact and use the same ownership map and report contract.

A future `audit-ux` could become separate only if it is primarily screenshot/Figma/runtime-experience based, can operate independently of source architecture, and has a distinct visual/product-experience output contract.

## Required Package Surfaces

Every public skill must keep these synchronized:

- `SKILL.md`
- `agents/openai.yaml`
- `references/eval-cases.md`
- all linked reference guidance
- `README.md`
- `INSTALL.md`
- `skills.sh.json`

Changes to triggers, authority, modes/profiles, output, or routing require pairwise evals against the closest neighboring skills.

The machine-readable nearest-neighbor inventory lives in
`docs/skills/routing-graph.json`. Every public package must appear in the graph,
every edge must be symmetric, and both endpoint packages must name the other in
their Trigger or Non-Trigger eval sections. An empty list is valid only when a
skill has no plausible routing competitor in the published suite.

## Routing Review Checklist

Before publishing a skill change:

- confirm the description starts with `Use when` and names the real user intent;
- confirm runtime guidance refers to effective repository/host instructions
  rather than assuming one provider reads a particular filename;
- confirm `Do Not Use For` names the closest competing skills;
- confirm metadata routes to the same owner and mutation boundary as `SKILL.md`;
- add pairwise trigger/non-trigger cases for every nearest neighbor;
- ensure only `repo-delivery` owns Git mutation;
- ensure audits and reviews remain read-only;
- ensure implementation skills do not claim staging, commit, push, or PR ownership;
- ensure external/browser actions require their own explicit authorization;
- run the applicable targeted or full tier from `skills/AGENTS.md`, never both for one unchanged basis.
