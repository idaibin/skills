# Platform Operations

Use one common operation pattern. Add platform detail only when it changes target
identity, required fields, authorization, side effects, or proof.

## Operation Patterns

| Pattern | Typical actions | Minimum proof |
| --- | --- | --- |
| Search and read | open, navigate, search, filter, inspect notifications or metrics | target URL/identity, query/filter, rendered result |
| Draft and fill | prepare a post, comment, reply, message, form, or metadata without submit | verified account/target, mapped fields, final draft state |
| Publish and interact | publish, edit, delete, comment, reply, message, like, follow, share | explicit authorization, pre-submit state, direct side effect, final state |
| Upload and download | attach media/assets or retrieve reports/design files | exact local/remote target, transfer evidence, resulting file/state, cleanup |
| Inspect and verify | inspect UI, annotations, permissions, console/network, or outcome | claim-matched before/after evidence and `Not verified` gaps |

Read-only collection may proceed within the requested scope. Drafting may stop at
a locally reviewable state or an explicitly authorized unsent state. Before typing
or attaching files, determine whether the site autosaves, notifies recipients, or
persists uploads; treat any such behavior as an external write. Every external
write requires current proof of account, target, exact action, and authorization.
Stop on login credentials, MFA, CAPTCHA, risk control, consent, account switch,
permission grant, payment, destructive ambiguity, or an unverified recipient. Do
not bulk-engage or bypass platform limits.

## Platform Categories

- **Content communities** such as X, Xiaohongshu, Reddit, or Juejin: search/read,
  draft, publish, comment/reply/message, and inspect visible metrics.
- **Design collaboration**: open an authorized source, switch views,
  inspect annotations, comment, and download authorized assets.
- **Development collaboration** such as GitHub or GitLab: inspect issues, reviews,
  and checks; fill or submit authorized comments and forms.
- **Admin, CMS, and data tools:** authenticate, filter, edit forms, transfer files,
  and verify resulting state.

These examples are routing categories, not claims of current site capability.
Verify the live surface and platform rules at execution time.

## Thin Adapter Record

Record only task-relevant differences:

- category, canonical origin, and exact target;
- current account/workspace proof and freshness;
- semantic navigation and controls (role, label, text, stable DOM attribute);
- supported operation patterns and special required fields;
- confirmation boundary and possible side effects;
- success, failure, and transfer evidence;
- CAPTCHA, risk-control, rate, permission, or policy stop conditions;
- evidence source/date and every `Not verified` capability.

Never hardcode screen coordinates or assume labels, URLs, quotas, or policies stay
stable. Account goals, voice, editorial calendar, audience strategy, and engagement
policy remain caller-owned inputs; `ops-browser` executes the bounded operation and
returns evidence.
