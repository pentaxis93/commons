# Exit Codes

Shared exit code convention for session outcomes across the Tesserine
ecosystem.

Exit codes are the contract between a runner and its caller. The caller uses
them to decide whether to proceed, wait, retry, alert, or treat the session as
failed work. This convention is defined from those caller decisions, not from
one runner's internal state machine.

## Contract

This vocabulary is intentionally small and authoritative:

- `0` and `1` retain useful meaning for simple runners.
- Code `2` is reserved for incorrect invocation or usage.
- Codes `126`, `127`, and signal-derived `128+N` keep their external POSIX and
  shell meanings.
- Normal terminal states that require no operator alarm are distinct from
  failures.
- A caller can distinguish failed work from runner or environment failure.
- A runner that emits only `0` and `1` is compliant by default.

## Application-Defined Codes

| Code | Label | Meaning | Caller interpretation |
| --- | --- | --- | --- |
| `0` | `success` | All required work completed successfully. | Proceed normally. |
| `1` | `generic_failure` | The session failed, but the runner cannot or does not provide a more specific classification. This is the compatibility bucket for legacy `0/1` runners. | Treat as failure. Preserve the raw code. Do not infer whether work was attempted. |
| `2` | `usage_error` | The caller invoked the runner incorrectly: wrong flags, invalid arguments, malformed command shape, or other invocation misuse. | Fail fast. Fix invocation or caller configuration, not the work item. |
| `3` | `blocked` | The session reached a normal terminal state where actionable work exists in principle, but execution is blocked on unmet dependencies or prerequisites. | Do not mark as failed work. Wait for unblocking conditions rather than retrying immediately. |
| `4` | `nothing_ready` | The session reached a normal terminal state with no actionable work available. | Do not mark as failed work. Treat as a quiescent no-op outcome. |
| `5` | `work_failed` | Work was attempted, but required postconditions or completion checks failed. Methodology state may have changed and partial progress may exist. | Treat as failed work, not as an infrastructure fault. Preserve the possibility of partial progress. |
| `6` | `infrastructure_failure` | The runner, environment, bootstrap, or execution substrate failed before meaningful completion could be established. | Route as an environment or runtime fault. This is distinct from `work_failed` because it does not imply the work itself failed. |

## Reserved External Meanings

These meanings are not application-defined and callers must preserve them.

| Code | Label | Meaning | Caller interpretation |
| --- | --- | --- | --- |
| `126` | `command_not_executable` | The selected command or entrypoint was found but could not be executed. | Treat as launcher or environment failure. |
| `127` | `command_not_found` | The selected command or entrypoint was not found. | Treat as launcher or environment failure. |
| `128+N` | `terminated_by_signal` | The process terminated because it received signal `N`. `130` is the conventional `SIGINT` case. | Treat as interrupted or externally terminated, preserving the raw code and signal-derived meaning. |

## Runner Contract

- Return an application-defined code only when the runner can justify that
  semantic category from observed reality.
- Use `1` when the runner can say only "failed" and nothing more precise.
- Use `2` for invocation misuse by the caller, not for failed work.
- Use `5` only when work was actually attempted and required completion checks
  failed.
- Use `6` for environment, bootstrap, runtime, or substrate failures when the
  runner can distinguish them from failed work.
- Do not remap `126`, `127`, or signal-derived `128+N` into application
  meanings.
- A runner that emits only `0` and `1` remains compliant.

## Caller Contract

Interpret exit codes in this order:

1. `0` is `success`.
2. `126`, `127`, and `128+N` keep their external meanings.
3. Known application-defined codes `1-6` use the table above.
4. Any other non-zero exit code is `generic_failure`.

Callers must also:

- preserve the raw numeric exit code in logs and APIs even when mapping it to
  a semantic label
- not treat `blocked` or `nothing_ready` as failures
- not treat `work_failed` as an infrastructure fault
- not infer partial progress from `generic_failure` or
  `infrastructure_failure`
- treat caller-enforced timeout as a caller-layer outcome outside this
  vocabulary

## Forward Compatibility

Unknown-code handling is part of the contract.

Callers must:

- preserve the raw exit code
- classify any unrecognized non-zero application code as `generic_failure`
- continue honoring reserved external meanings for `126`, `127`, and
  signal-derived `128+N`

This rule makes the convention evolvable: older callers remain safe when newer
runners emit codes they do not yet understand.
