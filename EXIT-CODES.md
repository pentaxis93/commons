# Exit Codes

Shared exit code convention for session outcomes across the Tesserine
ecosystem.

## Purpose

Exit codes are the contract between a runner and its caller. The caller uses
them to decide whether to proceed, wait, retry, alert, or treat the session as
failed work. This convention is designed from those caller decisions, not from
one runner's internal state machine.

The vocabulary is intentionally small:

- compatible with legacy runners that only return `0` or `1`
- additive to POSIX and shell conventions rather than replacing them
- explicit about forward compatibility so callers degrade safely

## Design Constraints

- `0` and `1` must retain useful meaning for simple runners.
- Code `2` is reserved for incorrect invocation or usage.
- Codes `126`, `127`, and signal-derived codes `128+N` are not available for
  application-defined meanings.
- Normal terminal states that require no operator alarm must be distinct from
  failures.
- A caller must be able to distinguish "work was attempted and failed" from
  "the environment or runner failed before meaningful completion."

## Survey of Established Conventions

This convention borrows distinctions from existing practice, but only where
those distinctions serve the caller's decisions.

### POSIX and shell conventions

- POSIX `sh` reserves `126` for "found but not executable" and `127` for
  "not found", and requires signal termination to surface as an exit status
  greater than `128`.
- GNU Bash documents the conventional shell mapping `128+N` for fatal signal
  `N`.
- GNU Bash also documents exit status `2` for incorrect usage of builtins.

Adopted:

- preserve `126`, `127`, and signal-derived `128+N`
- reserve `2` for usage or invocation error

Rejected:

- overloading signal-derived codes with application meanings

Why:

- these meanings are already widely understood by shells, wrappers, and
  operators; reusing them would create boundary ambiguity

### BSD `sysexits.h`

`sysexits.h` distinguishes incorrect usage (`EX_USAGE`), internal software
error (`EX_SOFTWARE`), operating system failure (`EX_OSERR`), temporary failure
(`EX_TEMPFAIL`), and configuration error (`EX_CONFIG`).

Adopted:

- the distinction between invocation error, internal/work failure, and
  environment or system failure

Rejected:

- the `64-78` numeric range and the full BSD taxonomy

Why:

- the BSD range is not required for this contract
- the full taxonomy is more detailed than the caller's session-level decisions
- keeping application-defined codes in a compact low range preserves clean
  interoperability with `0/1` runners

### GitHub Actions

GitHub Actions uses a binary convention: `0` means success and any non-zero
exit status means failure.

Adopted:

- the requirement that a coarse `0/1` runner remains correctly interpretable

Rejected:

- collapsing every non-zero outcome into one failure category

Why:

- session runners need to report normal terminal states such as "blocked" and
  "nothing ready", which are not failures from the caller's perspective

### GitLab CI and GitLab Runner

GitLab distinguishes specific exit-coded policies in two places:

- `allow_failure:exit_codes` and `retry:exit_codes` let callers attach policy
  to particular codes
- the custom executor distinguishes build failure from system failure through
  separate runner-provided failure codes

Adopted:

- code-specific caller policy is valuable
- "work failed" and "system failure" are different outcome classes

Rejected:

- encoding retry policy directly into the exit code vocabulary

Why:

- retryability depends on caller policy and deployment context; the exit code
  should describe the outcome, and the caller should decide the policy

### Language Server Protocol

The Language Server Protocol keeps process exit semantics minimal: after an
orderly shutdown the server exits `0`; otherwise it exits `1`.

Adopted:

- keep the process-level vocabulary minimal

Rejected:

- proliferating fine-grained application-specific exit codes where a caller
  does not need them

Why:

- exit codes are a narrow channel; richer semantics belong in richer protocol
  surfaces when those surfaces exist

## Assigned Codes

Application-defined session outcome codes:

| Code | Label | Meaning | Caller interpretation |
| --- | --- | --- | --- |
| `0` | `success` | All required work completed successfully. | Proceed normally. |
| `1` | `generic_failure` | The session failed, but the runner cannot or does not provide a more specific classification. This is the compatibility bucket for legacy `0/1` runners. | Treat as failure. Preserve the raw code. Do not infer whether work was attempted. |
| `2` | `usage_error` | The caller invoked the runner incorrectly: wrong flags, invalid arguments, malformed command shape, or other invocation misuse. | Fail fast. Fix invocation or caller configuration, not the work item. |
| `3` | `blocked` | The session reached a normal terminal state where actionable work exists in principle, but execution is blocked on unmet dependencies or prerequisites. | Do not mark as failed work. Wait for unblocking conditions rather than retrying immediately. |
| `4` | `nothing_ready` | The session reached a normal terminal state with no actionable work available. | Do not mark as failed work. Treat as a quiescent no-op outcome. |
| `5` | `work_failed` | Work was attempted, but required postconditions or completion checks failed. Methodology state may have changed and partial progress may exist. | Treat as failed work, not as an infrastructure fault. Preserve the possibility of partial progress. |
| `6` | `infrastructure_failure` | The runner, environment, bootstrap, or execution substrate failed before meaningful completion could be established. | Route as an environment or runtime fault. This is distinct from `work_failed` because it does not imply the work itself failed. |

Reserved external meanings that callers must preserve:

| Code | Label | Meaning | Caller interpretation |
| --- | --- | --- | --- |
| `126` | `command_not_executable` | The selected command or entrypoint was found but could not be executed. | Treat as launcher or environment failure. |
| `127` | `command_not_found` | The selected command or entrypoint was not found. | Treat as launcher or environment failure. |
| `128+N` | `terminated_by_signal` | The process terminated because it received signal `N`. `130` is the conventional `SIGINT` case. | Treat as interrupted or externally terminated, preserving the raw code and signal-derived meaning. |

## Rationale for the Distinctions

### `generic_failure` versus `infrastructure_failure`

These are not duplicates.

- `generic_failure` means the caller only knows that execution did not succeed.
  This is the fallback for legacy runners and unknown non-zero outcomes.
- `infrastructure_failure` means a compliant runner knows the failure came from
  the environment, bootstrap, or runtime substrate rather than from attempted
  work.

The caller action is therefore different:

- `generic_failure`: fail safely without assuming anything about progress
- `infrastructure_failure`: route as a runner or environment fault, with retry
  or remediation policy chosen by the caller

### `work_failed` versus `generic_failure`

`work_failed` is the rich category for "the agent ran, but the work did not
satisfy required postconditions." It differs from `generic_failure` in two
ways:

- it implies work was attempted
- it permits the caller to assume that methodology state may have changed

That distinction matters for scheduling, logging, and operator review.

## Runner Guidance

- Return an application-defined code only when the runner can justify that
  semantic category from observed reality.
- Use `1` when the runner can say only "failed" and nothing more precise.
- Use `2` for invocation misuse by the caller, not for failed work.
- Use `5` only when work was actually attempted and required completion checks
  failed.
- Use `6` for environment, bootstrap, runtime, or substrate failures where the
  runner can distinguish them from failed work.
- Do not remap `126`, `127`, or signal-derived `128+N` into application
  meanings. Those codes already carry shared semantics.
- A runner that only emits `0` and `1` is compliant by default.

## Caller Guidance

Interpret exit codes in this order:

1. `0` is `success`.
2. `126`, `127`, and `128+N` keep their external meanings.
3. Known application-defined codes `1-6` use the table above.
4. Any other non-zero exit code is `generic_failure`.

Additional rules:

- Preserve the raw numeric exit code in logs and APIs even when you map it to
  a semantic label.
- Do not treat `blocked` or `nothing_ready` as failures.
- Do not treat `work_failed` as an infrastructure fault.
- Do not infer partial progress from `generic_failure` or
  `infrastructure_failure`.
- Timeout is not an exit code. If a caller enforces time limits, timeout
  remains a caller-layer outcome outside this vocabulary.

## Forward Compatibility

Unknown-code handling is part of the contract.

Callers must:

- preserve the raw exit code
- classify any unrecognized non-zero application code as `generic_failure`
- continue honoring reserved POSIX and shell meanings for `126`, `127`, and
  signal-derived `128+N`

This rule makes the convention evolvable: older callers remain safe when newer
runners emit codes they do not yet understand.

## References

- POSIX `sh` exit status rules:
  <https://pubs.opengroup.org/onlinepubs/9799919799/utilities/sh.html>
- POSIX command search and signal-derived shell exit status:
  <https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html>
- GNU Bash exit status conventions:
  <https://www.gnu.org/s/bash/manual/html_node/Exit-Status.html>
- BSD `sysexits.h` manual:
  <https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3&manpath=OpenBSD+6.9>
- GitHub Actions exit code behavior:
  <https://docs.github.com/en/actions/how-tos/create-and-publish-actions/set-exit-codes>
- GitHub workflow cancellation and signal delivery:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-cancellation>
- GitLab CI `allow_failure:exit_codes` and `retry:exit_codes`:
  <https://docs.gitlab.com/ci/yaml/>
- GitLab Runner custom executor failure categories:
  <https://docs.gitlab.com/runner/executors/custom/>
- Language Server Protocol 3.17 shutdown and exit behavior:
  <https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/>
