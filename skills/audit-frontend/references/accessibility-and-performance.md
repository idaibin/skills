# Accessibility And Performance

Evidence basis: shadcn/Radix compound primitives, Outline and Appwrite
accessibility patterns, WAI-ARIA Authoring Practices, React's official
`useMemo` guidance, Tauri's async/channel guidance, and reference-repository
virtualized/paginated lists.

## Accessibility

Check:

- native interactive elements and complete keyboard operation;
- visible focus and logical focus order;
- Dialog/Popover/Menu initial focus, containment, Escape behavior, close
  control, and focus restoration;
- labels, descriptions, validation errors, required state, and submitting state;
- accessible names for icon-only buttons;
- expanded/selected/pressed state where semantics require it;
- status not communicated by color alone;
- loading, async completion, progress, and errors announced without excessive
  live-region noise;
- table headers/captions and row-action reachability;
- desktop shortcuts do not conflict with text inputs, editors, browser/webview
  defaults, or assistive technology.

Prefer tested accessible primitives over rebuilding focus management locally.
ARIA does not repair the wrong native element.

## Performance Review Order

1. Trace the interaction, framework render/reactivity boundary, request path,
   cache updates, context/store/composable subscribers, native calls, and loaded
   bundles.
2. Identify unbounded lists, repeated requests, large global objects, broad
   context/store updates, duplicated derived state, synchronous blocking work,
   duplicate dependencies, or high-frequency IPC.
3. Measure in a production-like build or provide explicit complexity evidence.
4. Apply the smallest correction and measure again.

Do not optimize from component line count alone. Do not add `memo`, `useMemo`,
or `useCallback` as decoration; React documents them as performance tools whose
value depends on an actual expensive calculation or render boundary.

For Vue 3, do not recommend `computed`, `shallowRef`, `markRaw`, store splitting,
or watcher replacement as generic optimization. Trace which refs/reactive
properties, computed values, watchers/watchEffects, Pinia subscriptions, and
template regions update for the interaction. Check broad deep watchers,
accidental dependencies in `watchEffect`, unstable object replacement, duplicated
derived state, store-wide subscriptions, repeated guard/listener registration,
and requests restarted on every activation. Require profiling, request counts,
or explicit fan-out/complexity evidence before claiming a performance defect.

## Common Corrections

- paginate or virtualize unbounded collections;
- for React, narrow subscriptions/selectors and context providers;
- narrow Vue watcher sources, Pinia subscriptions, and reactive ownership when
  traced fan-out is broader than the feature needs;
- remove duplicated derived state and effect-driven update chains;
- deduplicate requests and use established cache invalidation;
- split bundles at existing route/feature boundaries when measurement supports it;
- move blocking native work off the UI thread and stream progress;
- batch or subscribe instead of issuing high-frequency IPC calls.
