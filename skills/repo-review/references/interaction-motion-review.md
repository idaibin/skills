# Interaction And Motion Review

Load this reference only when the selected Worktree or immutable basis changes motion,
gesture behavior, transition ownership, or user-visible interaction feedback. File
extensions, frontend directories, and dependency presence do not activate it alone.

## Review Chain

Trace only the applicable authorities and reachable implementation:

```text
product behavior or acceptance
  -> selected-source UI contract when applicable
  -> resolved design-root DESIGN.md or repository motion tokens when adopted
  -> changed component/style/state ownership
  -> runtime/browser evidence when the claim depends on rendered behavior
```

Keep absent product/UI authority and absent runtime evidence as separate `Not verified`
gaps. Existing implementation values are facts, not automatically approved targets.

## Candidate Checks

- Does each introduced or changed motion communicate state, feedback, spatial
  relationship, or an otherwise evidenced transition rather than decoration alone?
- Does its delay and movement fit the frequency and familiarity of the affected action,
  especially keyboard-driven or repeatedly used controls?
- Does the basis preserve existing component and motion contracts rather than inventing
  a parallel timing, easing, library, or visual system?
- Does feedback keep loading, success, failure, selection, expansion, and dismissal
  understandable without hiding or delaying the resulting state?
- Does changed motion preserve reduced-motion, focus, keyboard, hover-capability, and
  interruption behavior where applicable?
- Does new transition code name its properties? Treat `transition: all` as a candidate,
  not an automatic finding; prove unwanted-property animation, performance cost,
  inconsistent state, or another concrete reachable impact.
- Where an equivalent implementation exists, do transform/opacity and existing
  semantic owners avoid unnecessary layout work or animation-only wrappers? Do not
  demand a rewrite when layout semantics require another property or owner.

## Finding Gate

Apply the ordinary Standards/Spec finding gate. Attribute the issue to the selected
basis as introduced, expanded, exposed, or pre-existing-but-blocking; cite the current
authority or concrete engineering impact; prove the reachable user effect; and assign
P0-P3 from impact and urgency. Do not report personal timing, easing, style, or library
preference as a violation.

Source declarations can establish ownership and candidate behavior, but not perceived
timing, spatial continuity, interruption, hover behavior, or reduced-motion results.
Require runtime evidence for those claims or mark them `Not verified`. Do not create a
parallel frontend-quality profile or require `audit-frontend` by default.
