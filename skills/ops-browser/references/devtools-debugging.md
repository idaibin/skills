# DevTools Debugging

## Contents

- [Request Readiness](#request-readiness)
- [Capability And Evidence Selection](#capability-and-evidence-selection)
- [Runtime Ownership And Non-Interrupting Operation](#runtime-ownership-and-non-interrupting-operation)
- [Readiness Then Red/Green Loop](#readiness-then-redgreen-loop)
- [State Safety And Cleanup](#state-safety-and-cleanup)
- [Return Contract](#return-contract)

Use Browser Debug Evidence only for a specified browser-layer failure on
localhost, a LAN development address, a test environment, a public page, or a
production page the user is authorized to inspect.

## Request Readiness

Fix these fields before operating:

- exact URL and environment;
- reproducible action sequence;
- expected behavior and observed symptom;
- relevant viewport, account, storage, cache, or input state;
- requested evidence and the red/green decision it supports;
- allowed state changes and explicit stop conditions.

Resolve required viewports in this order: exact user-supplied dimensions; an
accepted viewport matrix; an explicit repository convention; then one minimal
representative value for each category the user named (for example, one mobile
and one desktop value). Record that final choice as an assumption. Do not add
an unmentioned category or breakpoint coverage because it seems customary.

Route an unexplained or cross-system symptom back to the host diagnosis flow.
Do not use exploratory browser activity to invent a frontend, API, backend, or
database root cause.

## Capability And Evidence Selection

Preflight only the surfaces needed by the request:

| Surface | Direct claims it can support |
| --- | --- |
| DOM/accessibility | rendered elements, semantics, attributes, state, and deterministic selectors |
| CSS/layout | computed styles, box geometry, stacking, clipping, and responsive state |
| Console | client exceptions, warnings, logs, and browser policy errors |
| Network | request URL/method/status/timing, exposed headers, payload, response, and initiator |
| Cookies/storage | browser-visible cookie and local/session storage presence, scope, and changes without exposing secrets |
| Route/resources/cache | navigation, redirects, loaded or failed assets, cache behavior, and browser-enforced CORS |
| Screenshot/viewport | visible state at the recorded viewport and time |
| Upload/download | selected source or resulting artifact and browser-visible transfer state |

If the active browser cannot expose a requested surface, mark that claim `Not
verified` and name the exact trace, HAR, console export, screenshot, or manual
inspection needed. A screenshot does not prove network, storage, or backend
state.

## Runtime Ownership And Non-Interrupting Operation

When this task starts a local runtime, create a small task ledger before launch:

- exact launch command, working directory, and task identifier;
- parent PID and any discovered child PIDs that belong to that launch, plus
  each process start time, executable or command, working directory when
  observable, and parent-child source;
- exact bound port or socket, when observable;
- task-specific browser profile and evidence/artifact paths.

Do not claim background safety from headless terminology alone. When the user
requires no window, mouse, or keyboard interruption, use an isolated route only
after the active tool proves `background_safe`; otherwise use supported
non-browser evidence or stop. Do not focus, move, resize, or reuse a user-owned
window as a fallback.

Before sending a signal, re-observe every candidate process and compare its PID,
start time, executable or command, working directory, and recorded parent-child
source with the ledger. A mismatch can indicate PID reuse, a detached orphan,
or another task's process: do not signal it and report it as not cleaned. A
port proves only that a listener is present or absent; never select a kill
target by port or a broad name/port scan. At completion, stop or remove only
identity-matched ledger-owned processes, profiles, and artifacts, then verify
their exact PIDs and recorded ports are gone when the tool can observe them. If
the caller started or owns the runtime, return the launch/cleanup responsibility
and any observed runtime identifiers to that caller instead of stopping it.

## Readiness Then Red/Green Loop

Keep setup readiness distinct from the requested product behavior:

1. Check the minimum readiness condition needed to run the stated reproduction,
   such as a listener, route response, or required rendered control.
2. If readiness is absent, record the direct setup fact. Retry only that
   readiness check a bounded number of times when it has no external side effect
   and no user-owned state is touched.
3. Once ready, run the product behavior sequence once per authorized attempt;
   a failed behavior assertion is red evidence, not a reason to repeat setup or
   action blindly.

Then run the red/green loop:

1. Reproduce the symptom without changing unrelated state.
2. Wait for the relevant hydrated, loaded, or settled page state.
3. Capture the smallest evidence set that proves the red condition.
4. State one falsifiable browser hypothesis.
5. Change one safe variable or run one deterministic observation.
6. Repeat the same steps and capture green, persistent red, or inconclusive evidence.
7. Return direct browser facts, inference labels, missing evidence, and the next owner.

Prefer deterministic DOM, Console, or Network checks and a short repeatable
sequence over exploratory clicking. If reproduction fails, report the attempted
states and missing artifact instead of guessing.

## State Safety And Cleanup

- Treat reload, cache/storage clearing, cookie edits, account or environment
  switching, form actions, uploads, downloads, and production data changes as
  separate operations; perform them only when required and authorized.
- Never reveal cookies, tokens, credentials, private payloads, or unrelated
  account data in retained evidence. Redact sensitive values while preserving
  the facts needed for diagnosis.
- Tag task-only probes, filters, screenshots, traces, tabs, runtime ledger, and
  temporary browser profile with a task-specific identifier. Remove disposable
  state when safe.
- Retain referenced evidence until it is embedded, archived, transferred, or
  accepted by the caller; then report retained and removed artifacts separately.

## Return Contract

Return the target/environment, Capability Snapshot ID, reproduction steps,
expected and observed behavior, selected evidence surfaces, red/green result,
one-variable experiment, direct browser facts, explicitly labeled inferences,
`Not verified` gaps, state changes, sensitive-data handling, artifact paths or
identifiers, runtime ownership/ledger, cleanup verification, and the caller-owned
next decision.
