# Resolving Merge Conflicts

Load this reference only when an authorized merge or rebase is already in progress, or the requested delivery target explicitly requires starting one after branch/divergence checks.

## Intent-First Resolution

1. Fix the current merge/rebase state, conflicted paths, immutable target/source revisions, repository rules, and separately authorized actions: resolve files, stage resolutions, continue/commit the operation, and push. Keep the operation abortable while gathering evidence.
2. For each textual conflict and same-rule semantic overlap, trace both sides to their primary intent: the originating requirement/commit and the current owner, callers, tests, generated sources, migrations, or docs.
3. Before changing a conflicted or semantically overlapping file, present a compact conflict brief: path or cohesive intent group, target-side behavior, source-side behavior, proposed resulting behavior, affected acceptance/configuration boundary, and the smallest verification. Do not treat a clean automatic merge as proof that business intent is compatible.
4. Obtain an actual human answer under [Human Selection](checklist.md#human-selection), including its tool-availability and asynchronous-wait rules. Offer outcomes such as preserve target intent, adopt source intent, or apply the stated synthesis. Group conflicts only when one decision genuinely governs them.
5. Resolve only the selected hunk or cohesive group. Preserve compatible intent from both sides; do not pick ours/theirs merely to clear markers. A broad authorization to merge, resolve conflicts, commit, or push does not waive this selection gate.
6. If a new conflict, sensitive overlap, or material effect appears, stop and request a new selection instead of extending the prior answer.
7. Search the resolved file and affected closure for conflict markers, stale names, duplicate declarations, and structural lifecycle gaps.
8. Run the smallest checks that cover the resolution, then applicable repository gates.
9. If staging is authorized, stage only resolved conflicted paths/hunks and inspect the cached diff. Continue or commit the current merge/rebase only when that action is separately authorized; otherwise stop with the resolved files or index in the requested state.

Abort remains a valid safety action when the basis, intent, permissions, or preservation plan cannot be established. Never derive staging, continuation, commit, push, force-push, cleanup, or branch-deletion authority from permission to resolve conflicts.

## Report

Report the operation and revisions, conflicted paths, intent evidence per hunk or group,
question/options and selected answer, resolution, validation, staged state, whether the
merge/rebase was continued or stopped, and every `Not verified` gap.
