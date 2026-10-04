# Native Rust UI Profile

## Contents

- [Activation And Ownership](#activation-and-ownership)
- [Dependency And Platform Evidence](#dependency-and-platform-evidence)
- [State, Work, And Lifetime](#state-work-and-lifetime)
- [Interaction And Accessibility](#interaction-and-accessibility)
- [Performance And Completion](#performance-and-completion)
- [GPUI Kit Source Checkpoint](#gpui-kit-source-checkpoint)

## Activation And Ownership

Load for an authorized Rust-rendered desktop UI change, including GPUI or a
GPUI-based component kit. Keep the repository's chosen UI framework, crate,
dependency revision, renderer, and runtime. A library mention or comparison does
not authorize adoption: technology selection remains research/planning until a
choice is accepted; browser/webview UI source remains with `dev-frontend`.

Read the accepted product/visual contract and the nearest working component,
state owner, theme/token adapter, action/focus path, and tests. Reuse those owners.
Components implement the accepted interaction and visual contract; a showcase
or component catalog does not define the product's required states. Delegate
real native-window operations to `ops-client` under the existing task authority;
source edits and native acceptance retain their separate owners.

## Dependency And Platform Evidence

- Resolve the exact Cargo package, source URL, locked revision/version, enabled
  features, Rust/toolchain requirements, and existing initialization order. Names
  such as GPUI, a GPUI fork, and a component kit are not interchangeable APIs.
- Match upstream examples and documentation to that revision. Inspect actual
  exported types, platform gates, renderer/backend, text stack, and component
  prerequisites (including Kit initialization and the release-appropriate root/
  window host) before copying an example or adding a dependency.
- Record evidence separately for each in-scope OS, architecture, display/backend,
  and packaged build. A support table, successful cross-compile, browser/WASM
  showcase, and native release execution establish different facts. A WASM demo
  does not prove that an arbitrary native application can ship unchanged on web.
- Recheck version-sensitive claims against official sources when the adopted
  revision changes; preserve the local dependency unless migration is authorized.

## State, Work, And Lifetime

- Keep view/entity state and framework context updates on their required thread;
  trace the pinned API's entity/weak-handle and executor semantics rather than
  substituting a Tokio task or shared lock for the UI framework's lifecycle.
- Move blocking IO and expensive computation off the UI event/render path using
  the existing executor boundary. Bound progress queues, coalesce superseded
  updates when the contract permits, and apply results through the current view
  identity. A closed window or newer request must not receive a stale result.
- Preserve task, subscription, callback, focus, and window lifetimes. Test the
  changed close/cancel/reopen or replacement path; handle failures visibly under
  the accepted behavior. Select Concurrency/runtime or Unsafe/FFI only for the
  actual changed seam, not merely because the UI uses native rendering.
- Keep side effects outside rendering/layout callbacks. Reuse the existing
  invalidation, list virtualization, asset/font, and resource-cache mechanisms;
  introduce optimization only after representative measurement identifies a need.

## Interaction And Accessibility

For the affected control, exercise applicable pointer and keyboard actions,
visible focus, tab order, shortcuts, Escape/dismissal, focus restoration, disabled
and pending states, and repeated input. Text entry also needs the target input
method's composition, selection, caret, clipboard, and Unicode behavior; a
synthetic key event does not establish IME correctness.

Trace semantic role/name/value/state, focus and action routing through the
framework to its platform accessibility adapter. Headless AccessKit/tree
snapshots prove emitted semantics only. They do not prove that the exact packaged
build exposes a usable native tree or works with a target screen reader. Record
OS accessibility inspection and screen-reader/keyboard observations separately;
mark unavailable acceptance `Not verified` rather than claiming platform parity.

## Performance And Completion

- Derive thresholds from the product's accepted workload and supported hardware.
  GPU rendering or a library benchmark does not guarantee a frame rate. If 120 Hz
  is an explicit target, its nominal frame interval is about 8.33 ms; identify
  which end-to-end measurement must meet it and the allowed missed-frame rate.
- Measure the real release window under representative data, resize/scroll/input,
  and relevant background work. Record build/revision, OS, GPU/driver, display
  refresh, scale factor, workload, warm-up, sample count, and instrumentation scope.
  Report whole-window frame/present distributions (including tail percentiles and
  missed frames), with input-to-visible latency where required. CPU-only render
  timings, one average, headless tests, or component microbenchmarks cannot satisfy
  a full-window smoothness claim; name unavailable present evidence explicitly.
- Run repository Baseline and only applicable Contract, Concurrency/runtime,
  Target/platform, or other risk overlays. Headless behavior/semantic tests,
  source/build checks, native interaction/accessibility, performance, and packaged
  execution each keep their own status. Existing accepted evidence on the same
  basis can support a no-change result; do not create a new harness without a gap.
- Report changed owner/revision, exercised states and platforms, exact evidence
  basis, failures, exclusions, and remaining `Not verified` gaps. Neither a clean
  compile nor a successful showcase closes missing native acceptance.

## GPUI Kit Source Checkpoint

The following are source-reading prompts from Longbridge GPUI Kit **v0.7.0**,
commit `0c830f4d257e69fdd17200650533ab4ca9a40cc0`, checked 2026-10-04.
This is a fixed evidence basis, not a required dependency or a claim about future
releases. Re-resolve each contract for the repository's actual locked version.

- [Cargo manifest](https://github.com/longbridge/gpui-kit/blob/0c830f4d257e69fdd17200650533ab4ca9a40cc0/Cargo.toml): this revision uses exact per-package `gpui-pre-*` pins; resolve each package individually from the adopted manifest/lock rather than assuming one family-wide version or mixing examples/types from another GPUI family. Some installation prose at this tag has older package examples, so resolve dependencies from the adopted manifest/lock and API.
- [Tasks](https://github.com/longbridge/gpui-kit/blob/0c830f4d257e69fdd17200650533ab4ca9a40cc0/website/docs/task.md): `cx.spawn` is foreground; `cx.background_spawn` accepts owned `Send` work. Return entity changes through the proper context. Dropping an unfinished task cancels it but does not interrupt a synchronous blocking call already running; retain/await or deliberately detach tasks under the applicable lifecycle policy.
- [FPS instrumentation](https://github.com/longbridge/gpui-kit/blob/0c830f4d257e69fdd17200650533ab4ca9a40cc0/website/docs/fps.md): the `MAX FPS` estimate omits presentation and GPU completion. It cannot establish the release-window acceptance above. Large example row counts and README throughput figures likewise need task-specific measurement.
- For large-table or editor work, distinguish the [virtualized DataTable](https://github.com/longbridge/gpui-kit/blob/0c830f4d257e69fdd17200650533ab4ca9a40cc0/website/component/data-table.md) from the [nonvirtualized Table](https://github.com/longbridge/gpui-kit/blob/0c830f4d257e69fdd17200650533ab4ca9a40cc0/website/component/table.md); sorting still needs the app delegate. [Editor LSP provider defaults](https://github.com/longbridge/gpui-kit/blob/0c830f4d257e69fdd17200650533ab4ca9a40cc0/crates/base/src/input/editor/lsp/mod.rs) return no service until an app supplies one. A component or extension point is not a complete data/IDE integration.
- [Headless tests](https://github.com/longbridge/gpui-kit/blob/0c830f4d257e69fdd17200650533ab4ca9a40cc0/website/docs/test.md) and [accessibility](https://github.com/longbridge/gpui-kit/blob/0c830f4d257e69fdd17200650533ab4ca9a40cc0/website/docs/accessibility.md): use event/model/geometry/semantic snapshots for their stated layer; keep offscreen pixels, OS accessibility adapters, screen readers and native IME/compositor evidence separate.
- [WebAssembly scope](https://github.com/longbridge/gpui-kit/blob/0c830f4d257e69fdd17200650533ab4ca9a40cc0/website/docs/webassembly.md): documented support is the Showcase, with a single top-level window and no additional-window/reopen path. It is not production portability proof for an arbitrary desktop app.
