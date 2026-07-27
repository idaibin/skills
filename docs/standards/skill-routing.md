# Skill Routing And Design Standard

A public Skill represents a stable user intent and execution owner. Technology names
and checklist categories remain profiles when they share the same authority, workflow,
and output.

## Current Owners

| Skill | Owns | Mutation |
| --- | --- | --- |
| `repo-map` | repository boundaries, commands, reuse, and durable maps | named map artifact only |
| `domain-modeling` | shared business terms, rules, and ambiguity | named fact source only |
| `product-spec` | feature behavior, scope, states, and acceptance | named product artifact only |
| `ui-spec` | implementation-ready UI specification from a selected visual source, with Google DESIGN.md at the repository root as the sole shared visual authority and per-slice Feature Specs | specification artifacts only |
| `repo-review` | current Worktree/index or fixed revision review | read-only |
| `dev-frontend` | requested frontend implementation | source files |
| `dev-rust` | requested Rust implementation | source files |
| `audit-frontend` | bounded frontend audit profiles | read-only |
| `audit-rust` | bounded Rust audit profiles | read-only |
| `repo-delivery` | staging, commit, integration, push, and cleanup | Git |
| `ops-browser` | authorized browser operations and evidence | browser state |
| `ops-client` | authorized desktop-client operations and evidence | client state |
| `ask-chatgpt` | local request packages and authorized ChatGPT collaboration | local artifact or authorized external action |
| `human-writing` | source-grounded drafting, rewriting, diagnosis, and adaptation | requested writing output |

## Split Or Profile

Create a new Skill only when all are materially distinct:

1. user intent;
2. authority or mutation boundary;
3. workflow and stop condition;
4. independently useful output.

Otherwise add a focused reference/profile to the existing owner. React and Vue remain
inside frontend Skills; Rust subsystem checks remain inside Rust Skills. A future Java
or Python Skill should appear only after repeated real implementation work shows that
its workflow and domain knowledge justify an independently maintained package.

## Shared Code Quality Model

Cross-language quality principles live in one synchronized protocol rather than
being redeclared by every Skill. Language/framework references refine
reachability and semantics; owner Skills apply the stage meaning:

| Owner | Quality question |
| --- | --- |
| `repo-review` | Did the fixed basis introduce, expand, expose, or directly depend on the issue? |
| `audit-frontend` / `audit-rust` | What currently exists inside the declared profile and path scope? |
| `dev-frontend` / `dev-rust` | How does the authorized change avoid the issue and remove only what it makes obsolete? |

Duplication, dead/unused code, over-design, pass-through layers, and hidden
coupling are findings only after reachability, concrete impact, precise owner,
stage attribution, and falsifiable verification are established. React, Vue,
Vite/Rolldown, Rust/Clippy, async, FFI, and similar details stay in their domain
profiles. They do not create a new public Skill or an unconstrained whole-repo
scan inside `repo-review`.

## Composition

Start with the closest owner. Add a handoff only when the user's requested outcome
actually needs another owner to act now. Handoffs transfer bounded context, never
authorization. Planning and diagnosis use host capabilities and repository instructions
unless they acquire specialized reusable knowledge that warrants a Skill.

Common sequence, when needed:

```text
repo-map -> domain-modeling/product-spec -> ui-spec/dev-* -> repo-review -> repo-delivery
```

This is not mandatory ceremony. A known Rust implementation can start directly with
`dev-rust`. `repo-review` evaluates correctness, security, performance, and
maintainability together on its selected basis. Security risk does not create a
separate routing path or external scanning dependency.

For a frontend surface with applicable contracts, `dev-frontend` reads the effective
instructions, product requirements or product Feature Spec, selected-source UI
Feature Spec, root `DESIGN.md`, any existing repo-map only for navigation, then live
source/config before editing. The two Feature Spec types have separate authorities;
when both apply they are both read, while missing optional artifacts remain separate
`Not verified` gaps only when they affect behavior or acceptance. Root `DESIGN.md`
owns shared visual semantics; themes and component libraries are implementation adapters. A
Component/Layout `audit-frontend` profile may trace that contract to adapters,
components/consumers, and runtime evidence. `repo-review` keeps the sole
change-basis gateway and adds this check only for visual or UI-contract changes.

## Review Checklist

- The description clearly says what the Skill owns and when it triggers; when a real
  nearest neighbor is ambiguous, it also names the shortest negative or rerouting
  condition without copying the full non-trigger list.
- The nearest similar request is routed elsewhere in `Do Not Use For` or eval cases.
- OpenAI metadata matches the same owner and action boundary.
- References are loaded selectively and linked directly from `SKILL.md`.
- Read-only, source-write, Git-write, browser, and external-action boundaries remain
  distinct.
- The affected trigger, non-trigger, and edge scenarios still behave as intended.
