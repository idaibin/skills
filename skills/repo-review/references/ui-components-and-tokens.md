# Reviewing Adopted UI Components And Tokens

Load this reference only when the selected basis changes or directly relies on a
declared project-owned UI component boundary, third-party UI adapter, structured token
pipeline, Component Registry, or adoption record. Do not require these optional assets
in a project that has not adopted them.

## Review Closure

- Verify the adoption record and human component contract against live public imports,
  component files, exports, consumers, adapter roots, restricted dependencies, and
  complete bounded escape hatches.
- Keep real component source and types authoritative over Registry metadata. Require
  the project-native validator to catch missing, stale, or duplicate source and public
  import drift instead of accepting a documentation-marker check.
- Trace `Component -> Semantic -> Primitive`, generated outputs, business-only
  Semantic consumption, owner-scoped Component Token usage, and negative coverage for
  unknown, cyclic, bypass, authored CSS self-reference, and generated drift.
- Attribute findings only when the basis introduces, expands, exposes, or directly
  relies on the mismatch. An unadopted optional Registry or token pipeline is `Not
  applicable`, not a defect.
- Keep static gates separate from runtime. Whole-image similarity is diagnostic only;
  critical state, accessibility, computed-style, and geometry claims require their own
  evidence at the accepted viewport/state and contract-owned tolerance.

Review the validator and its negative fixtures, not only its passing output. A green
marker-only test proves document presence, not project governance behavior.
