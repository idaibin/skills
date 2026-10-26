# Conditional Codebase Design

Load this reference before touching a component, module, or page outside the current business scope, or when a change or review materially affects a public module/interface, seam placement, cross-caller abstraction, or testability. Repository-native `service`, `API`, `component`, `boundary`, and other established terms remain authoritative; the terms below are reasoning aids, not a mandatory vocabulary migration.

## Cross-Module Business Gate

Before editing outside the current business module, read the affected owner and real
callers; establish business purpose, permissions, state transitions, data effects,
and existing behavior. A dependency or reuse opportunity is not write authorization.
Do not change another module's existing logic or code speculatively.

If existing behavior or implementation conflicts with the new requirement, present
the current behavior, conflict, proposed options, affected consumers, and exact write
scope. Wait for the user's explicit agreement on the plan and permitted changes before
editing that boundary. Do not rewrite its contract first to manufacture permission.
Reuse an existing explicit decision for the same plan/scope; continue independent
work already authorized. Behavior-preserving work inside an explicitly approved
cross-module scope needs no repeated approval.

## Evidence Questions

- **Deep module:** does a small public interface hide meaningful behavior, invariants, error modes, ordering, configuration, and lifecycle complexity?
- **Seam:** is this the existing public point where behavior can vary and callers/tests observe it, or is a new seam merely hypothetical?
- **Locality:** does the design keep change, knowledge, failure handling, and verification near one owner instead of scattering them across callers?
- **Leverage:** do several real callers or tests receive useful capability from one stable interface?
- **Deletion test:** if the abstraction disappeared, would its complexity vanish, or would it reappear across real callers? Vanishing complexity usually signals a pass-through layer.
- **Public-interface test:** can behavior be verified through the same interface callers use, without private-state inspection or implementation-coupled mocks?

## Terminal Content

Implement the accepted final state. Within authorized scope, remove rejected or
retired code, configuration, entries, examples and active references; do not replace
them with negative declarations, conversation attribution, rationale comments or
placeholders. Do not add compatibility branches merely to preserve a rejected design.
If real consumers or data dependencies remain, resolve the impact through the
cross-module business gate before deletion. Preserve unrelated work.

## Decision Rules

- Before changing a shared owner that affects another business module, inspect its
  actual callers, behavior, permissions and data effects. Keep the change inside the
  user's authorized scope; ask for the missing business decision or expanded scope
  only when the existing request does not settle it. Reuse an explicit decision for
  the same change instead of demanding approval again at each file or owner boundary.
- Prefer the existing repository seam and terminology when they already provide locality and testability.
- Introduce a new shared seam only for real variation, repeated callers, or a proven ownership boundary; one hypothetical alternate implementation is insufficient.
- Deepen or replace a shallow pass-through when evidence shows scattered knowledge; do not add another wrapper layer around it.
- Keep implementation detail private and make required invariants, errors, ordering, and lifecycle visible at the public interface.
- Apply the deletion test before preserving an abstraction and the public-interface test before approving its verification strategy.
