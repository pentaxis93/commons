# Release Process

This document describes how to cut a release of a tesserine cargo-workspace repo under the convention established by [ADR-0006](adr/0006-release-discipline.md). The ADR explains *why* the convention exists; this document explains *how* an operator executes it.

The audience is an operator (human or agent) at a cargo-workspace repo where [`cargo-release`](https://github.com/crate-ci/cargo-release) is already installed and configured. Per-repo adoption — installing the tool, authoring `release.toml` — is one-time work tracked in each repo's adoption issue and is not covered here.

## Preconditions

Before invoking the release command, the following must hold:

- The working tree is clean and on the repo's integration branch (typically `main`).
- The branch is up to date with the remote: `git pull --ff-only`.
- `cargo-release` is installed and a `release.toml` exists at the workspace root.
- `CHANGELOG.md`'s `[Unreleased]` section reflects everything shipping in this release. The `[Unreleased]` heading itself stays — `cargo-release` rolls it into a versioned section as part of the release.
- The version level is decided: `patch` for fixes, `minor` for additive changes, `major` for breaking changes.

If any precondition fails, resolve the discrepancy before releasing. `--allow-dirty` is not part of the release path.

## The release

One command:

```
cargo release <level> --execute
```

Where `<level>` is `patch`, `minor`, or `major`. The command performs, in order, as a single indivisible step from the operator's perspective:

1. Bumps the workspace `Cargo.toml` version by the requested level.
2. Rolls `CHANGELOG.md`'s `[Unreleased]` heading into `[X.Y.Z] — YYYY-MM-DD`.
3. Commits the bump and CHANGELOG roll.
4. Creates an annotated tag `vX.Y.Z` pointing at the commit.
5. Pushes the commit and the tag to the remote.

The operator does not perform any of these steps independently. Splitting the operation reintroduces the gap this convention closes.

## Verification

After the push, on a fresh clone of the tag, build the workspace and check that every shipped binary self-reports the version the tag names:

```
checkdir=$(mktemp -d)
git clone --branch vX.Y.Z --depth 1 <repo-url> "$checkdir"
cd "$checkdir"
cargo build --release
for binary in <binary>...; do
    ./target/release/"$binary" --version
done
```

For each binary the workspace ships, the output must include `X.Y.Z`. If any binary reports otherwise, the workspace-version invariant has been violated and the release is invalid; see *Failure modes* below.

## Failure modes

**Dirty working tree.** `cargo-release` refuses to run. Resolve the dirty state — commit, stash, or discard — and retry. Do not pass `--allow-dirty`.

**Tag already exists upstream.** The release was attempted twice or the tag was created out of band. If the existing tag has no external consumers, delete it locally and remotely (`git tag -d vX.Y.Z && git push origin :refs/tags/vX.Y.Z`) and re-release. If the tag has external consumers, treat it as immutable: cut the next version instead. Public-tag rewriting is a larger problem with consequences beyond this document.

**Workspace-version invariant violated.** The binary at the tag self-reports the wrong version. Do not amend the tagged commit. The remediation path is the same as for "Tag already exists upstream" and inherits the same external-consumer constraint: if no external consumers exist, delete the tag (locally and remotely), correct `Cargo.toml`, and re-release; if external consumers exist, the invalid tag enters the public record and the remediation is to cut the next version, because public-tag rewriting is a larger problem with consequences beyond this document.

**`cargo release` aborts mid-operation.** The atomicity is best-effort: the tool sequences the operation, but a network failure between commit and push can leave the local repo bumped and tagged without the push having landed. Recovery: confirm the commit and tag are present locally and not yet upstream, then `git push --follow-tags` to complete the operation. If the remote already received the commit but not the tag, `git push origin vX.Y.Z` finishes the push.

## Out of band

The following are not part of this document and are intentionally excluded:

- **GitHub release notes.** Whether and how to author a release on GitHub is a separate concern; the tag is the canonical release artifact, the GitHub release is presentation.
- **Artifact signing.** Not currently practiced; if and when introduced, signing becomes its own convention.
- **Pre-release identifiers** (`-rc.N`, `-beta.N`). Deferred until the ecosystem needs them.
- **CHANGELOG authoring** — what entries qualify, voice, granularity. This document covers only the operational roll of `[Unreleased]` into a versioned section at release time.
