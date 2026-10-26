# Bundled ZCode CLI qualification example

Use for an authorized installed ZCode CLI operation. Apply the shared
[session protocol procedure](session-protocols.md#submit-and-query) for session
selection, submission and reconciliation; this reference covers ZCode-specific
configuration, arguments and persisted readback.

## Contents

- [Installed configuration roots](#installed-configuration-roots)
- [Exact-session invocation](#exact-session-invocation)
- [Persisted readback](#persisted-readback)
- [CLI and app-server limits](#cli-and-app-server-limits)

## Installed configuration roots

Resolve the executable inside the current app, version and help. In the qualified
macOS CLI 0.17.0 (native-review live-canary 2026-10-20; exact-session resume canary
2026-10-21), process-local configuration accepts these variables:

| Variable | Installed-runtime meaning |
| --- | --- |
| ZCODE_DATA_BASE_DIR | Parent of the account's .zcode directory; not that directory itself |
| ZCODE_BUILTIN_PROVIDER_CONFIG_FILE | Bundle config/provider/zcode-builtin.json |
| ZCODE_PERSONAL_PROVIDER_CONFIG_FILE | Account .zcode/v2/provider_config.json |

Before any prompt, verify that the resolved executable and the selected original
builtin configuration file exist and are readable. Derive the bundle resource root
from the installed executable/package layout; the launcher directory need not be
the configuration directory. Qualify supported process-local bindings against the
installed build before use. A failed default lookup does not prove the installation
has no configuration. Do not dump file contents, create replacement configuration,
or change provider/account to repair discovery.

The desktop may resolve a different account root from the shell default. Locate its
actual task index/configuration through verified process open files, installed path
resolution and exact task metadata. Account configuration, desktop task index and
CLI transcript database can resolve independently; changing the account-root override
does not establish a new transcript root. Pass the original configuration paths and
let the CLI load credentials natively, without dumping their contents.

Bind the stored workspace key and exact provider/model/variant IDs from that session.
Case-normalized model labels and the UI picker alone do not establish those IDs.

## Exact-session invocation

Use --resume with the exact idle SID. --continue selects a latest session and is
unsuitable for exact-session binding. Use an argument array, for example:

```javascript
const args = [
  '--cwd', workspace, '--resume', sessionId,
  '--json', '--no-color', '--mode', verifiedMode,
  '--disallowed-tools', ...taskDeniedTools,
  '--prompt', authorizedPrompt,
];
```

In 0.17.0 the denylist is variadic: place --prompt after it, and positional commands
such as doctor before it, or they can be consumed as tool names. Check current help
before reuse. The qualified headless flow did not support /model as a model-selection
route; preserve the verified session binding rather than treating that slash prompt
as configuration.

Capture direct process exit/signal, stderr and the returned sessionId, turnId,
traceId, response, projection and usage when supplied. An exact resume must return
the same SID and a new corresponding turn; inspect persisted permission/model state
when it differs from the requested --mode.

## Persisted readback

Prefer supported exact-session queries. If the installed route requires SQLite
readback, inspect its schema, open it read-only and restrict queries to the exact SID,
submitted input and subsequent turn. Message/part records expose assistant finish,
tool calls, arguments, status, outputs and final text. Correlate completed model_usage
rows through session/turn/trace and provider_id, model_id and variant.

## CLI and app-server limits

--cwd does not contain CLI session/cache persistence. Mode and tool-name filters do
not enforce filesystem paths; require suitable isolation for the accepted operation.
In 0.17.0 --resume itself is not repository-bound: resuming an exact SID under a
--cwd from a different repository succeeds, so repository binding relies on the
caller-side session registry, not on the CLI.
Do not repair unresolved binding by switching account/model or creating a substitute
session.

The bundled app-server is a separate host-driven protocol; standalone account-backed
model access may depend on native-host account synchronization. Qualify it separately
when selected. A missing standalone account source does not establish that the
desktop account is unavailable, and is not a reason to copy keys into that transport.
See the [app-server example](app-server-example.md) for that route.

Consult the installed implementation first. The [official CLI source](https://github.com/zai-org/ZCode/blob/main/apps/zcode-cli/packages/cli/src/run.ts)
and [Agent mode guide](https://zcode.z.ai/en/docs/agents) are rediscovery pointers;
version-dependent arguments and persisted schemas require installed-build checks.
