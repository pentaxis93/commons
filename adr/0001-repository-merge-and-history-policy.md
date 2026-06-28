# ADR-0001: Repository Merge and History Policy

**Status:** Accepted
**Traces to:** [Transmission](https://github.com/pentaxis93/principles/blob/main/principles/transmission.md) (primary), [Grounding](https://github.com/pentaxis93/principles/blob/main/principles/grounding.md), [Parsimony](https://github.com/pentaxis93/principles/blob/main/principles/parsimony.md)

## Decision

Every active pentaxis93 repository carries one uniform merge and history
policy, configured in its forge settings:

- **Allowed merges: squash and rebase. Merge commits are disabled.** Both
  permitted methods produce a linear result; the merge commit — the only method
  that creates a branch topology on the default branch — is the one removed.
- **Merged head branches are deleted automatically.**
- **Squash commits default to the pull-request title and body**, not the
  concatenation of the branch's intermediate commit messages.
- **Where the plan permits branch protection, the default branch enforces
  linear history**, with force-pushes and branch deletion disabled.

Within that frame the author chooses per pull request:

- **Squash** an iterative series — one logical change developed as a lead commit
  plus follow-up corrections ("feature + fixups"). The default branch receives a
  single coherent, individually-buildable commit; the branch's working commits
  remain on the pull request.
- **Rebase** a curated series — commits that are each independent and
  self-coherent, where the sequence is itself information worth keeping.

The two methods are not redundant: each is correct for a different *shape* of
pull request, and the policy is to match the method to the shape rather than to
mandate one method for every change.

## Context

History is a transmission medium. A linear, legible default branch where each
commit is a meaningful, buildable state is what lets a later reader — human or
agent — bisect a regression, attribute a line, or revert a change without first
reverse-engineering a tangle of merge bubbles and half-built intermediate
commits. Settling one policy across the projects means that reasoning transfers
unchanged from one repository to the next.

The method choice is grounded in the actual shape of merged pull requests, not
in convention. Commit *message* hygiene tends to be strong (conventional
commits), but commit *granularity* is iterative: a single change often arrives
as a lead commit plus a run of follow-up fixes. That rules out both
single-method absolutes. Rebase-only would replay those fixup commits — several
of which do not individually build — onto the default branch, defeating the very
bisectability linear history exists to provide. Squash-only would erase the
structure of the genuinely-atomic multi-commit pull requests that do exist.
Allowing squash *or* rebase under enforced linear history takes the benefit of
each and the cost of neither, while still removing the merge commit.

This ADR is the pentaxis93 base layer's merge-and-history policy. The Tesserine
ecosystem's [`commons`](https://github.com/tesserine/commons) inherits this base
rather than restating it, so one history discipline governs both projects (the
inheritance is declared on the Tesserine side).

## Consequences

- The default branch of every repository where protection applies is linear and
  free of merge bubbles; `git bisect`, `git blame`, and single-change reverts
  behave predictably across the projects.
- A squash never flattens the default branch — it collapses only one pull
  request's own working commits. The safeguard against history loss is the
  force-push protection, not the merge method; the two are set together but are
  independent guarantees.
- Authors carry a per-pull-request judgment (squash the iterative, rebase the
  curated). Neither method is a default to reach for without looking at the
  change's shape.
- Enforced linear history requires every pull request to be rebasable onto the
  base before it merges. A pull request that has fallen behind must be rebased,
  not merged-in. This friction is intended: it is the cost of a linear record.
- The policy is realized in each repository's forge settings, which are the live
  source of truth for the configuration; this ADR is the decision and its
  rationale, not a mirror of the settings. There is no automated drift check
  between the two today.
- **Plan limitation (pentaxis93 account).** On the pentaxis93 account's current
  plan, branch protection — and therefore linear-history *enforcement* — is
  available only on **public** repositories. Private repositories conform in
  their merge methods but cannot carry the protection rule until they are made
  public or the pentaxis93 account moves to a plan that supports
  private-repository protection. The active public repositories enforce linear
  history; the active private repositories rest on the merge-method
  configuration alone.
