# Unsafe And Security

## Unsafe Review

For every unsafe block, unsafe function, unsafe trait implementation, or raw
pointer boundary:

1. State the safety invariant immediately beside the operation.
2. Identify who establishes and preserves the invariant.
3. Check pointer provenance, validity, aliasing, alignment, initialization,
   bounds, lifetime, thread safety, and panic/unwind behavior.
4. Keep the unsafe region minimal and expose a safe API that cannot construct an
   invalid state.
5. Check every exit path for ownership transfer, double free, use after free,
   forgotten drop, or leaked native resource.
6. Identify focused test gaps; route requested test additions to `dev-rust`,
   and run existing Miri coverage when the code and dependencies are supported.
   Use sanitizers or platform tools only when the project already supports them.

Do not use unsafe merely to remove a bounds check, clone, or allocation without
a measured hot path, benchmark, safe baseline, and explicit proof.

## FFI And Native Dependencies

- Verify ABI, calling convention, symbol/version compatibility, integer widths,
  encoding, buffer length/capacity, nullability, alignment, and lifetime.
- Make allocation and release ownership explicit across the boundary. Pair
  native handles with one cleanup owner and test partial initialization.
- Prevent Rust panics from crossing an FFI boundary. Convert callback failures
  to the protocol the foreign side expects.
- Define thread-affinity and callback reentrancy. Do not send a native handle
  across threads unless its contract permits it.
- Treat mmap and shared memory as unsafe external mutation/truncation surfaces
  even when a wrapper exposes a safe type.
- Verify bundled versus system native libraries, compile options, runtime
  version, platform packaging, and update policy.

## Dependency And Data Security

- Inspect new dependency purpose, feature set, default features, native/build
  code, maintenance, license, advisories, MSRV, binary/compile cost, and whether
  the standard library or an existing crate already covers the need.
- Keep `Cargo.lock` changes scoped. Do not update unrelated packages while
  adding or fixing one dependency.
- Use RustSec tooling when installed and relevant, but validate advisory impact
  against enabled features and reachable code.
- Keep credentials, tokens, personal data, SQL values, filesystem paths, and
  native error payloads out of logs unless policy explicitly allows them.
- Validate untrusted lengths, counts, paths, archive entries, SQL parameters,
  IPC payloads, and resource limits at the boundary.

## Finding Contract

Report unsafe or security findings with the violated invariant or trust
boundary, reachable input, impact, exact location, minimal repair, and validation
evidence. Do not describe an unsafe block as vulnerable solely because it is
unsafe.
