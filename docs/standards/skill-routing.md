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
| `ui-design` | visual and interaction design for a page, flow, or shared system | design artifacts only |
| `repo-review` | current Worktree/index or fixed revision review | read-only |
| `dev-frontend` | requested frontend implementation | source files |
| `dev-rust` | requested Rust implementation | source files |
| `audit-frontend` | bounded frontend audit profiles | read-only |
| `audit-rust` | bounded Rust audit profiles | read-only |
| `audit-security` | bounded security assessment | read-only |
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

## Composition

Start with the closest owner. Add a handoff only when the user's requested outcome
actually needs another owner to act now. Handoffs transfer bounded context, never
authorization. Planning and diagnosis use host capabilities and repository instructions
unless they acquire specialized reusable knowledge that warrants a Skill.

Common sequence, when needed:

```text
repo-map -> domain-modeling/product-spec -> ui-design/dev-* -> repo-review -> repo-delivery
```

This is not mandatory ceremony. A known Rust implementation can start directly with
`dev-rust`; a bounded security request can start directly with `audit-security`.

## Review Checklist

- The description clearly says what the Skill owns and when it triggers.
- The nearest similar request is routed elsewhere in `Do Not Use For` or eval cases.
- OpenAI metadata matches the same owner and action boundary.
- References are loaded selectively and linked directly from `SKILL.md`.
- Read-only, source-write, Git-write, browser, and external-action boundaries remain
  distinct.
- The affected trigger, non-trigger, and edge scenarios still behave as intended.
