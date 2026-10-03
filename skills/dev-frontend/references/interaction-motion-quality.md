# Interaction And Motion Quality

Load this reference only when the authorized frontend change adds or changes motion,
gesture behavior, transition ownership, or user-visible interaction feedback. Do not
load it for every frontend edit or use it to redesign an approved surface.

## Authority And Purpose

1. Read the applicable product behavior, UI contract, resolved `<design-root>/DESIGN.md`, and existing
   component or motion tokens before choosing an implementation.
2. State the communication purpose: state indication, action feedback, spatial
   relationship, change explanation, or prevention of a jarring transition. Remove or
   omit motion with no purpose unless an approved contract explicitly requires it.
3. Match motion cost to interaction frequency and familiarity. Keep keyboard-driven
   and high-frequency actions immediate; do not add decorative delay to routine work.
4. Preserve the repository's established motion vocabulary. Do not introduce a new
   library, timing scale, easing system, or visual style for one local change.

## Implementation Checks

- Provide immediate, unambiguous feedback for loading, success, failure, selection,
  expansion, dismissal, and disabled actions that the changed flow materially uses.
- Specify transitioned properties; do not introduce `transition: all`. Do not expand
  the task merely to remove unchanged occurrences outside the authorized scope.
- Prefer the shortest duration and least movement that communicate the change. Exact
  timing, easing, spring, scale, and displacement values come from repository contracts
  or task evidence, not a universal personal preference.
- Prefer transform or opacity when they preserve the required layout and semantics;
  do not rewrite necessary layout behavior merely to satisfy that preference.
- Keep rapid, reversible, or gesture-driven interactions interruptible so a new input
  can take control without waiting for a stale sequence to finish.
- Respect reduced-motion preferences when movement is material, preserve focus and
  keyboard behavior, and gate hover-only effects on devices that support hover.
  When reduced-motion overrides affect measured or positioned overlays, inspect the
  effective transition properties and verify actual geometry and interaction lifecycle
  with motion disabled. A near-zero global duration may still animate synchronous
  positioning writes; choose the correction at the existing owner rather than assuming
  shorter duration is equivalent to no transition.
- Avoid animation-only wrappers when an existing semantic or state-owning element can
  own the same effect without changing layout, accessibility, or reuse boundaries.

## Interaction State And Admission

For affected controls, distinguish transient hover/press, visible keyboard focus,
persistent selection, business-disabled, and request-pending states. Preserve the
existing component/library state owner and applicable semantics; a palette override
or pointer cursor does not establish complete feedback across its variants.

- Trace every reachable activation path for an async write: click, native form submit,
  keyboard activation, and alternate retry/action entrypoints. When overlap would
  duplicate a side effect, admit synchronously at the shared handler owner before
  awaiting work, release on terminal success/failure, and keep retry reachable. Reuse
  an equivalent existing guard; do not add locks to harmless synchronous controls.
- Keep business-disabled confirmation separate from request-pending interaction.
  Apply the accepted pending-dismissal policy at the actual dialog/Drawer owner,
  including Close, Escape, mask, Cancel and nested paths, not merely a footer button.
  An unavailable business action does not itself justify trapping dismissal.
- When a keyboard action opens or replaces a focused surface, trace originating
  keydown/default activation through focus transfer and the resulting click/submit.
  Prevent an evidenced unintended default at its owner; preserve legitimate Enter,
  Space, form submission and library keyboard behavior rather than blanket blocking.
- Verify field labels reach the rendered control's accessible name, including
  controlled fields outside automatic form registration. Use the stack's existing
  association mechanism, with unique control IDs when explicit label binding is needed.
- On failure, preserve useful input, expose recoverable feedback and release admission;
  distinguish retry from close/reopen reset. Verify focus after the actual close
  transition settles before introducing custom restoration or trapping code.

## Validation

Source inspection proves declarations and ownership only. For changed interaction
families, exercise the applicable variant × state × surface/theme combinations on
rendered maintained components; include selected+focused and pressed states when
reachable. A passing solid-primary control does not prove outlined, link, danger,
menu or elevated-surface variants. Use focused dispatch/readback assertions for
reentrant actions; loading/disabled appearance alone does not prove single admission.

Source inspection alone does not prove runtime behavior. Exercise the affected states
and rapid repeated input at the relevant viewport when timing, interruption, spatial
continuity, hover capability, or perceived feedback is part of acceptance. Record
reduced-motion behavior when applicable. If runtime evidence is unavailable, report
the affected behavior `Not verified`; do not claim interaction or motion quality from
build, lint, typecheck, or static CSS alone.
